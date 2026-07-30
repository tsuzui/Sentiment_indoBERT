import plotly.express as px
import streamlit as st

from constants import DATASET_GROUP_ORDER
from pipeline_loader import load_cleaning_data, load_raw_scrape
from ui_helpers import metric_row


def render() -> None:
    st.header("🧹 Hasil Pre-processing")
    st.caption("Perbandingan jumlah data sebelum dan sesudah cleaning (duplikat, di luar rentang tanggal, tidak relevan, dll dibuang), per dataset (MSIB Setara, MSIB Full/Matang, Magang Berdampak).")

    raw_df = load_raw_scrape()
    clean_df = load_cleaning_data()

    total_raw = len(raw_df)
    total_clean = len(clean_df)
    pct_drop = round((1 - total_clean / total_raw) * 100, 1)

    metric_row([
        ("Total Sebelum Cleaning", total_raw),
        ("Total Setelah Cleaning", total_clean),
        ("Persentase Terbuang", f"{pct_drop}%"),
    ])

    tab_ringkasan, tab_contoh = st.tabs(["Ringkasan", "Contoh Perubahan"])

    with tab_ringkasan:
        per_group = clean_df.groupby("dataset_group").size().reindex(DATASET_GROUP_ORDER).fillna(0).astype(int).reset_index(name="Jumlah")
        fig = px.bar(
            per_group,
            x="dataset_group",
            y="Jumlah",
            color="dataset_group",
            category_orders={"dataset_group": DATASET_GROUP_ORDER},
            labels={"dataset_group": "Dataset"},
            title="Jumlah Data Setelah Cleaning per Dataset",
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(per_group.rename(columns={"dataset_group": "Dataset"}), use_container_width=True, hide_index=True)

    with tab_contoh:
        if st.button("Tampilkan Contoh Lain", key="cleaning_reroll"):
            st.session_state["cleaning_seed"] = st.session_state.get("cleaning_seed", 0) + 1
        seed = st.session_state.get("cleaning_seed", 0)
        sample = clean_df.sample(n=min(10, len(clean_df)), random_state=seed)
        st.dataframe(sample[["dataset_group", "raw_text", "clean_text"]], use_container_width=True)
