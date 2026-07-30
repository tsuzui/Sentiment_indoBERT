import pandas as pd
import plotly.express as px
import streamlit as st

from constants import CLASSIFICATION_REPORTS, CONFUSION_MATRICES, MODEL_SCENARIOS
from ui_helpers import metric_row


def _scenario_summary_row(scenario: str) -> dict:
    report = pd.DataFrame(CLASSIFICATION_REPORTS[scenario]).set_index("kelas")
    return {
        "Model": scenario,
        "Accuracy": report.loc["Accuracy", "f1_score"],
        "Macro Precision": report.loc["Macro Average", "precision"],
        "Macro Recall": report.loc["Macro Average", "recall"],
        "Macro F1": report.loc["Macro Average", "f1_score"],
        "Weighted F1": report.loc["Weighted Average", "f1_score"],
    }


def render(df: pd.DataFrame) -> None:
    st.header("📊 Evaluasi Model — Perbandingan 3 Skenario")
    st.caption("Baseline vs penanganan imbalance (Class Weight, Random Oversampling) pada 157 data uji.")

    comparison = pd.DataFrame([_scenario_summary_row(s) for s in MODEL_SCENARIOS]).set_index("Model")
    st.subheader("Ringkasan Perbandingan")
    st.dataframe(comparison.style.format("{:.2f}"), use_container_width=True)
    st.caption("Random Oversampling dipilih sebagai model terbaik karena Macro F1 tertinggi (mendeteksi kelas minoritas positif/negatif lebih baik).")

    tabs = st.tabs(MODEL_SCENARIOS)
    for tab, scenario in zip(tabs, MODEL_SCENARIOS):
        with tab:
            row = comparison.loc[scenario]
            metric_row([
                ("Accuracy", f"{row['Accuracy']:.2f}"),
                ("Macro F1", f"{row['Macro F1']:.2f}"),
                ("Weighted F1", f"{row['Weighted F1']:.2f}"),
            ])

            st.subheader("Classification Report")
            report_df = pd.DataFrame(CLASSIFICATION_REPORTS[scenario]).set_index("kelas")
            st.dataframe(report_df, use_container_width=True)

            st.subheader("Confusion Matrix")
            classes = ["Negatif", "Netral", "Positif"]
            cm_df = pd.DataFrame(CONFUSION_MATRICES[scenario], index=classes, columns=classes)
            fig = px.imshow(
                cm_df,
                text_auto=True,
                color_continuous_scale="Blues",
                labels=dict(x="Prediksi", y="Aktual", color="Jumlah"),
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption(f"Sumber: Hasil_Classification_Report_3_Model.pdf & Confusion matrix — skenario {scenario}.")
