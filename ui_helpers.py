import streamlit as st


def metric_row(items: list[tuple]) -> None:
    """items: list of (label, value), (label, value, delta), or (label, value, delta, help) tuples."""
    cols = st.columns(len(items))
    for col, item in zip(cols, items):
        label, value = item[0], item[1]
        delta = item[2] if len(item) > 2 else None
        help_text = item[3] if len(item) > 3 else None
        with col:
            st.metric(label, value, delta=delta, help=help_text)
