"""Konstanta dashboard: path data dan metrik model yang di-hardcode dari skripsi."""

from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

FILE_PATHS = {
    "MSIB Setara": DATA_DIR / "hasil_klasifikasi" / "MSIB_Setara_Hasil.xlsx",
    "Magang Berdampak": DATA_DIR / "hasil_klasifikasi" / "Magang_Berdampak_Hasil.xlsx",
    "MSIB Matang": DATA_DIR / "hasil_klasifikasi" / "MSIB_Matang_Hasil.xlsx",
}

RAW_SCRAPE_X_PATHS = {
    "MSIB Setara": DATA_DIR / "raw_scrape" / "x_dataset_msib_setara.csv",
    "Magang Berdampak": DATA_DIR / "raw_scrape" / "x_dataset_magang_berdampak.csv",
    "MSIB Full": DATA_DIR / "raw_scrape" / "x_dataset_msib_full.csv",
}
YOUTUBE_RAW_PATH = DATA_DIR / "raw_scrape" / "youtube_raw.csv"

CLEANING_PATH = DATA_DIR / "after_cleaning" / "dataset_clean_conservative.csv"

GEMINI_LABELING_PATH = DATA_DIR / "after_labeling" / "dataset_labeled_gemini_progress.csv"

MANUAL_VALIDATION_PATH = DATA_DIR / "after_labeling" / "Labeling_Manual.xlsx"
MANUAL_VALIDATION_SHEET = "Copy of dataset_labeled_gemini_"

DATASET_GROUP_LABELS = {
    "MSIB_awal_setara": "MSIB Setara",
    "MSIB_full": "MSIB Full (Matang)",
    "Magang_Berdampak_awal": "Magang Berdampak",
}
DATASET_GROUP_ORDER = ["MSIB Setara", "MSIB Full (Matang)", "Magang Berdampak"]

TRAINING_CONFIG = {
    "Model Dasar": "IndoBERT Base P1 (indobenchmark/indobert-base-p1)",
    "Epoch": 3,
    "Learning Rate": "2e-5",
    "Batch Size": 16,
    "Optimizer": "AdamW",
    "Weight Decay": 0.01,
}

DATA_SPLIT = {
    "Data Latih (Train)": {"jumlah": 730, "persentase": "70%"},
    "Data Validasi (Val)": {"jumlah": 157, "persentase": "15%"},
    "Data Uji (Test)": {"jumlah": 157, "persentase": "15%"},
}

SCENARIO_DESCRIPTIONS = {
    "Baseline": "Model dilatih menggunakan data pelatihan dengan distribusi kelas asli tanpa penanganan class imbalance.",
    "Class Weight": "Model dilatih menggunakan data pelatihan asli dengan pemberian bobot lebih besar pada kelas minoritas melalui parameter class weight.",
    "Random Oversampling": "Model dilatih menggunakan data pelatihan yang telah diseimbangkan menggunakan teknik Random Oversampling sehingga jumlah data pada setiap kelas menjadi setara.",
}

LABEL_COLORS = {
    "positif": "#2ca02c",
    "netral": "#7f7f7f",
    "negatif": "#d62728",
}

CLASS_ORDER = ["negatif", "netral", "positif"]

# Sumber: Hasil_Classification_Report_3_Model.pdf & Confusion *.png (folder "Evaluasi model").
# Jangan dihitung ulang -- ini angka final yang dilaporkan di skripsi (Tabel 4.5-4.7).
CLASSIFICATION_REPORTS = {
    "Baseline": [
        {"kelas": "Negatif", "precision": 0.60, "recall": 0.62, "f1_score": 0.61, "support": 34},
        {"kelas": "Netral", "precision": 0.84, "recall": 0.87, "f1_score": 0.86, "support": 110},
        {"kelas": "Positif", "precision": 0.12, "recall": 0.08, "f1_score": 0.10, "support": 13},
        {"kelas": "Accuracy", "precision": None, "recall": None, "f1_score": 0.75, "support": 157},
        {"kelas": "Macro Average", "precision": 0.52, "recall": 0.52, "f1_score": 0.52, "support": 157},
        {"kelas": "Weighted Average", "precision": 0.73, "recall": 0.75, "f1_score": 0.74, "support": 157},
    ],
    "Class Weight": [
        {"kelas": "Negatif", "precision": 0.58, "recall": 0.62, "f1_score": 0.60, "support": 34},
        {"kelas": "Netral", "precision": 0.88, "recall": 0.74, "f1_score": 0.80, "support": 110},
        {"kelas": "Positif", "precision": 0.21, "recall": 0.46, "f1_score": 0.29, "support": 13},
        {"kelas": "Accuracy", "precision": None, "recall": None, "f1_score": 0.69, "support": 157},
        {"kelas": "Macro Average", "precision": 0.56, "recall": 0.61, "f1_score": 0.56, "support": 157},
        {"kelas": "Weighted Average", "precision": 0.72, "recall": 0.69, "f1_score": 0.72, "support": 157},
    ],
    "Random Oversampling": [
        {"kelas": "Negatif", "precision": 0.56, "recall": 0.59, "f1_score": 0.57, "support": 34},
        {"kelas": "Netral", "precision": 0.87, "recall": 0.74, "f1_score": 0.80, "support": 110},
        {"kelas": "Positif", "precision": 0.29, "recall": 0.62, "f1_score": 0.39, "support": 13},
        {"kelas": "Accuracy", "precision": None, "recall": None, "f1_score": 0.69, "support": 157},
        {"kelas": "Macro Average", "precision": 0.57, "recall": 0.65, "f1_score": 0.59, "support": 157},
        {"kelas": "Weighted Average", "precision": 0.74, "recall": 0.69, "f1_score": 0.72, "support": 157},
    ],
}

# Baris = aktual, kolom = prediksi. Urutan: Negatif, Netral, Positif.
CONFUSION_MATRICES = {
    "Baseline": [
        [21, 10, 3],
        [10, 96, 4],
        [4, 8, 1],
    ],
    "Class Weight": [
        [21, 8, 5],
        [11, 81, 18],
        [4, 3, 6],
    ],
    "Random Oversampling": [
        [20, 10, 4],
        [13, 81, 16],
        [3, 2, 8],
    ],
}

MODEL_SCENARIOS = ["Baseline", "Class Weight", "Random Oversampling"]
BEST_MODEL = "Random Oversampling"
