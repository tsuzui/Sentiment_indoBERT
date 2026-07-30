import pandas as pd
import plotly.express as px
import streamlit as st

from constants import CLASS_ORDER, LABEL_COLORS
from ui_helpers import metric_row


def _comparison_block(df: pd.DataFrame, title: str, label_a: str, label_b: str) -> None:
    st.subheader(title)
    subset = df[df["label"].isin([label_a, label_b])]

    grouped = (
        subset.groupby(["label", "predicted_label"]).size().reset_index(name="Jumlah")
    )
    grouped["predicted_label"] = pd.Categorical(grouped["predicted_label"], categories=CLASS_ORDER, ordered=True)
    grouped = grouped.sort_values("predicted_label")

    pct_table = (
        subset.groupby("label")["predicted_label"]
        .value_counts(normalize=True)
        .mul(100)
        .round(1)
        .unstack()
        .reindex(columns=CLASS_ORDER)
    )

    metric_items = []
    for kelas in CLASS_ORDER:
        if kelas in pct_table.columns and label_a in pct_table.index and label_b in pct_table.index:
            selisih = round(pct_table.loc[label_a, kelas] - pct_table.loc[label_b, kelas], 1)
            metric_items.append((
                f"Selisih {kelas.capitalize()}",
                f"{selisih:+.1f}pp",
                None,
                f"pp = poin persentase (percentage point): selisih langsung dua angka persen "
                f"({label_a} dikurangi {label_b}), bukan persentase relatif.",
            ))
    if metric_items:
        metric_row(metric_items)

    fig = px.bar(
        grouped,
        x="predicted_label",
        y="Jumlah",
        color="label",
        barmode="group",
        labels={"predicted_label": "Kelas Sentimen", "label": "Program"},
        title=title,
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Tabel Persentase"):
        st.dataframe(pct_table, use_container_width=True)


def render(df: pd.DataFrame) -> None:
    st.header("⚖️ Perbandingan Antar Program")

    _comparison_block(df, "Fase Awal — MSIB Setara vs Magang Berdampak", "MSIB Setara", "Magang Berdampak")
    st.divider()
    _comparison_block(df, "Fase Matang — MSIB Matang vs Magang Berdampak", "MSIB Matang", "Magang Berdampak")

    st.caption(
        "Catatan: dataset Magang Berdampak hanya tersedia satu (808 komentar), "
        "sehingga digunakan kembali pada kedua perbandingan di atas — sesuai struktur penelitian pada skripsi."
    )
