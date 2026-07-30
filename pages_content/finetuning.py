import streamlit as st

from constants import DATA_SPLIT, SCENARIO_DESCRIPTIONS, TRAINING_CONFIG
from ui_helpers import metric_row


def render() -> None:
    st.header("🧠 Fine-Tuning Model")
    st.caption("Dataset hasil validasi manual (ground truth) digunakan untuk melatih model IndoBERT dengan 3 skenario penanganan class imbalance.")

    st.subheader("Pembagian Data (Stratified Train-Test Split)")
    metric_row([
        (label, f"{v['jumlah']} ({v['persentase']})")
        for label, v in DATA_SPLIT.items()
    ])

    st.subheader("Konfigurasi Pelatihan")
    metric_row([(k, v) for k, v in TRAINING_CONFIG.items()])

    st.subheader("Skenario Fine-Tuning")
    st.caption("Ketiga skenario menggunakan dataset, konfigurasi pelatihan, dan proses evaluasi yang sama — perbedaannya hanya pada cara menangani ketidakseimbangan kelas pada data latih.")
    for scenario, deskripsi in SCENARIO_DESCRIPTIONS.items():
        with st.container(border=True):
            st.markdown(f"**{scenario}**")
            st.write(deskripsi)
