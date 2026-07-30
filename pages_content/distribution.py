import pandas as pd
import plotly.express as px
import streamlit as st

from constants import CLASS_ORDER, LABEL_COLORS
from ui_helpers import metric_row


def render(df: pd.DataFrame) -> None:
    st.header("📊 Distribusi Sentimen per Program")

    dataset_label = st.selectbox("Pilih dataset", df["label"].unique())
    subset = df[df["label"] == dataset_label]

    counts = subset["predicted_label"].value_counts().reindex(CLASS_ORDER).fillna(0).astype(int)
    percentages = (counts / counts.sum() * 100).round(1)

    table = pd.DataFrame({"Kelas": CLASS_ORDER, "Jumlah": counts.values, "Persentase (%)": percentages.values})

    kelas_dominan = table.loc[table["Jumlah"].idxmax(), "Kelas"]
    pct_dominan = table.loc[table["Jumlah"].idxmax(), "Persentase (%)"]
    metric_row([
        ("Total Komentar", int(counts.sum())),
        ("Kelas Dominan", kelas_dominan.capitalize()),
        ("Persentase Dominan", f"{pct_dominan}%"),
    ])

    col1, col2 = st.columns(2)
    with col1:
        fig_bar = px.bar(
            table,
            x="Kelas",
            y="Jumlah",
            color="Kelas",
            color_discrete_map=LABEL_COLORS,
            text=table["Persentase (%)"].astype(str) + "%",
            title=f"Jumlah Sentimen — {dataset_label}",
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        fig_pie = px.pie(
            table,
            names="Kelas",
            values="Jumlah",
            color="Kelas",
            color_discrete_map=LABEL_COLORS,
            title=f"Proporsi Sentimen — {dataset_label}",
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with st.expander("Tabel Detail"):
        st.dataframe(table, use_container_width=True, hide_index=True)
