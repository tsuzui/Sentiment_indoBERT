import streamlit as st

from data_loader import load_all_data
from pages_content import (
    cleaning,
    comparison,
    distribution,
    examples,
    finetuning,
    gemini_labeling,
    kesimpulan,
    manual_validation,
    model_metrics,
    raw_scraping,
)

st.set_page_config(layout="wide", page_title="Dashboard Analisis Sentimen MSIB vs Magang Berdampak")

st.sidebar.title("📈 Analisis Sentimen")
st.sidebar.caption("MSIB vs Magang Berdampak — Fine-Tuned IndoBERT")

with st.sidebar.expander("ℹ️ Informasi Penelitian", expanded=False):
    st.markdown(
        """
**Judul**: Analisis Sentimen Publik antara Program MSIB dan Magang Berdampak
di Media Sosial Menggunakan Fine-Tuned IndoBERT

**Peneliti**: Aziz Alfarizi (NIM 20220801268)

**Program Studi**: Teknik Informatika, Universitas Esa Unggul

**Pembimbing**: Dewi Setiowati, A.Md., S.Pd., M.Tr.Kom

**Metode**: Scraping (X/Twitter + YouTube) → Cleaning → Labeling
Gemini 2.5 Flash Lite → Validasi Manual → Fine-Tuning IndoBERT
(indobenchmark/indobert-base-p1) → Evaluasi 3 skenario penanganan
class imbalance → Inferensi ke seluruh dataset penelitian
        """
    )

st.sidebar.divider()

PIPELINE_PAGES = {
    "📡 Data Scraping Mentah": raw_scraping,
    "🧹 Hasil Pre-processing": cleaning,
    "🏷️ Labeling Otomatis (Gemini)": gemini_labeling,
    "✅ Validasi Manual": manual_validation,
    "🧠 Fine-Tuning Model": finetuning,
    "📈 Evaluasi Model": model_metrics,
}

RESULT_PAGES = {
    "📊 Distribusi Sentimen per Program": distribution,
    "⚖️ Perbandingan Antar Program": comparison,
    "💬 Contoh Komentar": examples,
}

STANDALONE_PAGES = {
    "🎯 Kesimpulan": kesimpulan,
}

page = st.sidebar.radio(
    "Navigasi",
    list(PIPELINE_PAGES.keys()) + list(RESULT_PAGES.keys()) + list(STANDALONE_PAGES.keys()),
)

if page in PIPELINE_PAGES:
    if page == "📈 Evaluasi Model":
        df = load_all_data()
        model_metrics.render(df)
    else:
        PIPELINE_PAGES[page].render()
elif page in RESULT_PAGES:
    df = load_all_data()
    RESULT_PAGES[page].render(df)
else:
    STANDALONE_PAGES[page].render()
