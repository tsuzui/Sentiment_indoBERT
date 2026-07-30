import pandas as pd
import streamlit as st

from constants import FILE_PATHS

COLUMNS_NEEDED = [
    "program",
    "dataset_group",
    "platform",
    "raw_text",
    "clean_text",
    "predicted_label",
    "like_count",
]


@st.cache_data
def load_all_data() -> pd.DataFrame:
    frames = []
    for label, path in FILE_PATHS.items():
        df = pd.read_excel(path, engine="openpyxl")[COLUMNS_NEEDED].copy()
        df["label"] = label
        frames.append(df)
    return pd.concat(frames, ignore_index=True)
