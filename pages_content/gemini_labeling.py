import plotly.express as px
import streamlit as st

from constants import CLASS_ORDER, LABEL_COLORS
from pipeline_loader import load_gemini_labeling
from ui_helpers import metric_row


def render() -> None:
    st.header("🏷️ Labeling Otomatis (Gemini)")
    st.caption("Label awal dari Gemini 2.5 Flash Lite, sebelum divalidasi manual.")

    df = load_gemini_labeling()
    counts = df["sentiment_label"].value_counts().reindex(CLASS_ORDER).fillna(0).astype(int)
    metric_row([(kelas.capitalize(), int(n)) for kelas, n in counts.items()])

    tab_ringkasan, tab_contoh = st.tabs(["Ringkasan", "Contoh Komentar"])

    with tab_ringkasan:
        col1, col2 = st.columns(2)
        summary = counts.reset_index()
        summary.columns = ["Kelas", "Jumlah"]
        with col1:
            fig_bar = px.bar(summary, x="Kelas", y="Jumlah", color="Kelas", color_discrete_map=LABEL_COLORS)
            st.plotly_chart(fig_bar, use_container_width=True)
        with col2:
            fig_pie = px.pie(summary, names="Kelas", values="Jumlah", color="Kelas", color_discrete_map=LABEL_COLORS)
            st.plotly_chart(fig_pie, use_container_width=True)

    with tab_contoh:
        with st.expander("Filter", expanded=True):
            kelas = st.selectbox("Kelas Sentimen", ["Semua"] + CLASS_ORDER)

        subset = df if kelas == "Semua" else df[df["sentiment_label"] == kelas]
        st.caption(f"{len(subset)} komentar cocok dengan filter.")

        for _, row in subset.head(10).iterrows():
            with st.container(border=True):
                st.markdown(f"**{row['sentiment_label']}** · confidence: {row['label_confidence']}")
                st.write(row["clean_text"])
                st.caption(f"Alasan: {row['label_reason']}")
