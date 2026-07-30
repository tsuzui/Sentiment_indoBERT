import pandas as pd
import streamlit as st

from constants import (
    CLEANING_PATH,
    DATASET_GROUP_LABELS,
    GEMINI_LABELING_PATH,
    MANUAL_VALIDATION_PATH,
    MANUAL_VALIDATION_SHEET,
    RAW_SCRAPE_X_PATHS,
    YOUTUBE_RAW_PATH,
)

_X_DATASET_GROUP = {
    "MSIB Setara": "MSIB Setara",
    "MSIB Full": "MSIB Full (Matang)",
    "Magang Berdampak": "Magang Berdampak",
}


@st.cache_data
def load_raw_scrape() -> pd.DataFrame:
    frames = []
    for dataset_label, path in RAW_SCRAPE_X_PATHS.items():
        df = pd.read_csv(path, usecols=["text", "createdAt"])
        df = df.rename(columns={"text": "raw_text", "createdAt": "created_at"})
        df["sumber"] = "X/Twitter"
        df["dataset_label"] = f"X - {dataset_label}"
        df["dataset_group"] = _X_DATASET_GROUP[dataset_label]
        frames.append(df)

    yt = pd.read_csv(YOUTUBE_RAW_PATH, usecols=["dataset_group", "comment_text", "comment_published_at"])
    yt = yt.rename(columns={"comment_text": "raw_text", "comment_published_at": "created_at"})
    yt["sumber"] = "YouTube"
    yt["dataset_group_raw"] = yt["dataset_group"]
    yt["dataset_group"] = yt["dataset_group_raw"].map(DATASET_GROUP_LABELS)
    yt["dataset_label"] = "YouTube - " + yt["dataset_group"]
    yt = yt.drop(columns=["dataset_group_raw"])
    frames.append(yt)

    return pd.concat(frames, ignore_index=True)


@st.cache_data
def load_cleaning_data() -> pd.DataFrame:
    df = pd.read_csv(CLEANING_PATH)
    df["dataset_group"] = df["dataset_group"].map(DATASET_GROUP_LABELS)
    return df


@st.cache_data
def load_gemini_labeling() -> pd.DataFrame:
    df = pd.read_csv(GEMINI_LABELING_PATH)
    df["dataset_group"] = df["dataset_group"].map(DATASET_GROUP_LABELS)
    return df


@st.cache_data
def load_manual_validation() -> pd.DataFrame:
    df = pd.read_excel(MANUAL_VALIDATION_PATH, sheet_name=MANUAL_VALIDATION_SHEET)
    df["dataset_group"] = df["dataset_group"].map(DATASET_GROUP_LABELS)
    return df
