import plotly.express as px
import streamlit as st

from constants import DATASET_GROUP_ORDER
from pipeline_loader import load_raw_scrape
from ui_helpers import metric_row


def render() -> None:
    st.header("📡 Data Scraping Mentah")
    st.caption(
        "Data sebelum difilter/cleaning — jumlahnya wajar jauh lebih besar dari data final. "
        "Dibagi 3 dataset: MSIB Setara, MSIB Full (Matang), dan Magang Berdampak."
    )

    df = load_raw_scrape()
    per_group = df.groupby("dataset_group").size().reindex(DATASET_GROUP_ORDER).fillna(0).astype(int)
    metric_row([(label, int(n)) for label, n in per_group.items()])

    tab_ringkasan, tab_contoh = st.tabs(["Ringkasan", "Contoh Data"])

    with tab_ringkasan:
        summary = df.groupby(["dataset_group", "sumber"]).size().reset_index(name="Jumlah")
        fig = px.bar(
            summary,
            x="dataset_group",
            y="Jumlah",
            color="sumber",
            barmode="stack",
            category_orders={"dataset_group": DATASET_GROUP_ORDER},
            labels={"dataset_group": "Dataset", "sumber": "Sumber"},
            title="Jumlah Data Mentah per Dataset dan Sumber",
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(
            summary.rename(columns={"dataset_group": "Dataset", "sumber": "Sumber"}),
            use_container_width=True,
            hide_index=True,
        )

    with tab_contoh:
        with st.expander("Filter", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                sumber = st.selectbox("Sumber", ["Semua"] + list(df["sumber"].unique()))
            with col2:
                dataset_group = st.selectbox("Dataset", ["Semua"] + DATASET_GROUP_ORDER)

        subset = df.copy()
        if sumber != "Semua":
            subset = subset[subset["sumber"] == sumber]
        if dataset_group != "Semua":
            subset = subset[subset["dataset_group"] == dataset_group]

        st.caption(f"{len(subset)} baris cocok dengan filter.")
        st.dataframe(subset[["dataset_label", "dataset_group", "raw_text", "created_at"]].head(50), use_container_width=True)
