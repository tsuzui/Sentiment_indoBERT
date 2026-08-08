import pandas as pd
import streamlit as st

from ui_helpers import filter_quality_comments


def render(df: pd.DataFrame) -> None:
    st.header("💬 Contoh Komentar")

    with st.expander("Filter", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            program = st.selectbox("Program", ["Semua"] + list(df["label"].unique()))
        with col2:
            kelas = st.selectbox("Kelas Sentimen", ["Semua", "positif", "netral", "negatif"])
        with col3:
            text_col = st.radio("Tampilkan teks", ["raw_text", "clean_text"], horizontal=True)

    subset = df.copy()
    if program != "Semua":
        subset = subset[subset["label"] == program]
    if kelas != "Semua":
        subset = subset[subset["predicted_label"] == kelas]

    st.caption(f"{len(subset)} komentar cocok dengan filter di atas.")

    pool = filter_quality_comments(subset, text_col=text_col)

    jumlah = st.slider("Jumlah contoh ditampilkan", 1, min(50, max(len(pool), 1)), min(10, max(len(pool), 1)))

    if st.button("Tampilkan Contoh Lain"):
        st.session_state["examples_seed"] = st.session_state.get("examples_seed", 0) + 1

    seed = st.session_state.get("examples_seed", 0)

    if len(pool) == 0:
        st.info("Tidak ada komentar yang cocok dengan filter.")
        return

    sample = pool.sample(n=min(jumlah, len(pool)), random_state=seed)

    for _, row in sample.iterrows():
        with st.container(border=True):
            st.markdown(f"**{row['label']}** · sentimen: **{row['predicted_label']}** · {row['platform']}")
            st.write(row[text_col])
