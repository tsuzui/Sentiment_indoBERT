import re

import pandas as pd
import streamlit as st

_EMOJI_CODE_RE = re.compile(r":[a-z_]+:")
_BRACKET_PREAMBLE_RE = re.compile(r"^\s*[\[\(][^\]\)]{0,200}[\]\)]")
_PROMO_KEYWORDS = (
    "narahubung", "info selengkapnya", "informasi selengkapnya", "cek bio",
    "link di bio", "yuk daftar", "yuk check", "check this out", "more informasi",
    "daftarkan diri", "kunjungi", "buruan daftar", "cp:", "cp :",
)
_ANNOUNCEMENT_KEYWORDS = (
    "sehubungan dengan", "diinformasikan", "dalam rangka", "menindaklanjuti",
    "berkenaan dengan", "cuti bersama", "layanan perpustakaan", "surat edaran",
    "jam operasional", "libur nasional", "buka kembali", "press release",
    "siaran pers", "rilis resmi",
)
_INSTITUTION_KEYWORDS = (
    "bpjph", "kemendikbud", "kemenag", "kominfo", "kemenristekdikti", "kemdikbud",
    "ristekdikti", "kemenko", "kementerian", "dirjen dikti", "humas",
)


def is_quality_comment(text: str, min_words: int = 4, max_words: int = 60) -> bool:
    """Heuristik teks komentar yang enak ditampilkan di sidang.

    Buang sisa noise hasil cleaning (URL, mention, kode emoji ':nama_emoji:',
    preamble berkurung '[...]'/'(...)', teks promosi/pengumuman, atau teks
    yang kependekan/kepanjangan) tanpa mengubah data hasil cleaning aslinya.
    """
    if not isinstance(text, str):
        return False
    t = text.strip()
    if not t:
        return False
    words = t.split()
    if len(words) < min_words or len(words) > max_words:
        return False
    lowered = t.lower()
    if "http" in lowered or "www." in lowered:
        return False
    if "@" in t:
        return False
    if _EMOJI_CODE_RE.search(t):
        return False
    if _BRACKET_PREAMBLE_RE.match(t):
        return False
    if any(kw in lowered for kw in _PROMO_KEYWORDS):
        return False
    if any(kw in lowered for kw in _ANNOUNCEMENT_KEYWORDS):
        return False
    if any(kw in lowered for kw in _INSTITUTION_KEYWORDS):
        return False
    alpha_chars = sum(c.isalpha() for c in t)
    if alpha_chars < len(t) * 0.6:
        return False
    digit_chars = sum(c.isdigit() for c in t)
    if digit_chars > len(t) * 0.03:
        return False
    return True


def filter_quality_comments(df: pd.DataFrame, text_col: str = "clean_text", min_words: int = 4) -> pd.DataFrame:
    mask = df[text_col].apply(lambda t: is_quality_comment(t, min_words=min_words))
    return df[mask]


def metric_row(items: list[tuple]) -> None:
    """items: list of (label, value), (label, value, delta), or (label, value, delta, help) tuples."""
    cols = st.columns(len(items))
    for col, item in zip(cols, items):
        label, value = item[0], item[1]
        delta = item[2] if len(item) > 2 else None
        help_text = item[3] if len(item) > 3 else None
        with col:
            st.metric(label, value, delta=delta, help=help_text)
