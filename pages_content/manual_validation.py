import plotly.express as px
import streamlit as st

from pipeline_loader import load_gemini_labeling, load_manual_validation
from ui_helpers import filter_quality_comments, metric_row


def render() -> None:
    st.header("✅ Validasi Manual")
    st.info(
        "Validasi manual dilakukan pada 1.044 data dari Program MSIB Setara dan Magang "
        "Berdampak; Program MSIB Matang tidak melalui tahap validasi manual, sesuai cakupan "
        "penelitian pada skripsi."
    )

    df = load_manual_validation()
    gemini_df = load_gemini_labeling()

    total = len(df)
    benar = int((df["status_validasi"] == "benar").sum())
    salah = int((df["status_validasi"] == "salah").sum())
    akurasi = round(benar / total * 100, 1)

    metric_row([
        ("Total Divalidasi", total),
        ("Benar", benar),
        ("Dikoreksi", salah),
        ("Akurasi Gemini", f"{akurasi}%"),
    ])

    st.subheader("Cakupan Validasi per Dataset")
    coverage_rows = []
    for group in ["MSIB Setara", "Magang Berdampak"]:
        eligible = int((gemini_df["dataset_group"] == group).sum())
        validated = int((df["dataset_group"] == group).sum())
        pct = round(validated / eligible * 100, 1) if eligible else 0
        coverage_rows.append((f"Cakupan {group}", f"{validated}/{eligible} ({pct}%)"))
    metric_row(coverage_rows)
    st.caption(
        "Tidak semua komentar yang sudah dilabel Gemini ikut divalidasi manual. Untuk Magang "
        "Berdampak, 164 komentar dikeluarkan karena tidak relevan dengan kata kunci penelitian "
        "(mis. tercampur dengan istilah lain seperti \"Kampus Berdampak\") sehingga dihapus "
        "sebelum tahap validasi."
    )

    tab_ringkasan, tab_koreksi = st.tabs(["Ringkasan", "Contoh Koreksi"])

    with tab_ringkasan:
        summary = df["status_validasi"].value_counts().reset_index()
        summary.columns = ["Status", "Jumlah"]
        fig = px.pie(summary, names="Status", values="Jumlah", color="Status",
                     color_discrete_map={"benar": "#2ca02c", "salah": "#d62728"})
        st.plotly_chart(fig, use_container_width=True)

    with tab_koreksi:
        koreksi = df[df["sentiment_label"] != df["label_manual"]]
        st.caption(f"{len(koreksi)} komentar dikoreksi labelnya oleh validator manual.")
        pool = filter_quality_comments(koreksi, text_col="clean_text")
        st.dataframe(
            pool[["clean_text", "sentiment_label", "label_manual"]].rename(columns={
                "clean_text": "Teks",
                "sentiment_label": "Label Gemini",
                "label_manual": "Label Manual",
            }),
            use_container_width=True,
            hide_index=True,
        )
