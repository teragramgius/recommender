# pages/3_📝_Recommendations.py
import streamlit as st
import json
from utils.persistence import load_all
from utils.recommender import recommend_from_insight

st.set_page_config(page_title="Recommendations", page_icon="📝", layout="wide")
st.title("📝 Recommendations from Insights")

insights = load_all("insights")
if not insights:
    st.info("No insights yet. Create some from Self-Assessment or Workshop pages.")
    st.stop()

# Filter by status/channel/etc.
status = st.selectbox("Filter by status", options=["all","draft","validated","archived"], index=1)
if status != "all":
    insights = [i for i in insights if i.get("status") == status]

sel = st.selectbox("Choose an Insight", options=[i["insight_id"] for i in insights])

ins = next(i for i in insights if i["insight_id"] == sel)
st.json(ins)

if st.button("✨ Generate Recommendation"):
    rc = recommend_from_insight(ins)
    st.success(f"Recommendation saved as {rc['recommendation_id']}")
    st.text_area("Recommendation Text", rc["text"], height=140)
    st.download_button("Download Recommendation JSON", data=json.dumps(rc, indent=2), file_name=f"{rc['recommendation_id']}.json", mime="application/json")
