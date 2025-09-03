# app.py
import streamlit as st

st.set_page_config(page_title="KV Semantic Interoperability", page_icon="🔗", layout="wide")

st.title("KV — Semantic Interoperability Prototype")
st.markdown("""
This prototype captures **Self-Assessment** and **Workshop** insights as **append-only JSON** aligned with a shared vocabulary (channels, dimensions, cards A–E, principles E1–E6).
Use the pages on the left:

1. **Self Assessment** — create universities and record SAT-derived insights.  
2. **Workshop** — log workshop events, quotes/evidence, and create/validate insights.  
3. **Recommendations** — generate policy recommendations from validated insights.  
""")
