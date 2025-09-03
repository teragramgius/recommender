# pages/2_🧩_Workshop.py
import streamlit as st
from datetime import date
from utils.enums import MODALITIES, EVIDENCE_TYPES, PRINCIPLES, CHANNELS, CHANNEL_LABEL, DIMENSIONS, DIMENSION_LABEL, GUIDELINES, TIME_HORIZONS
from utils.ids import workshop_id, evidence_id, insight_id
from utils.persistence import save_json, load_all, load_by_id, compute_priority_quadrant, ts
from utils.validators import validate_insight

st.set_page_config(page_title="Workshop", page_icon="🧩", layout="wide")
st.title("🧩 Workshop → Evidence & Insights")

unis = {u["university_id"]: u for u in load_all("universities")}
if not unis:
    st.warning("Please create a University first in the Self-Assessment page.")
    st.stop()

uni_sel = st.selectbox("Select University", options=list(unis.keys()), format_func=lambda k: f"{unis[k]['name']} ({k})")

st.subheader("Create Workshop")
col = st.columns(4)
with col[0]:
    modality = st.selectbox("Modality", options=MODALITIES, index=0)
with col[1]:
    w_date = st.date_input("Date", value=date.today())
with col[2]:
    location = st.text_input("Location", value="")
with col[3]:
    participants = st.number_input("Participants", min_value=1, value=12)

roles = st.text_input("Roles (comma-separated)", value="Rectorate, Deans, TTO, Industry, Region")

if st.button("💾 Save Workshop"):
    wid = workshop_id(uni_sel, w_date)
    wk = {
        "workshop_id": wid,
        "university_id": uni_sel,
        "date": w_date.isoformat(),
        "modality": modality,
        "location": location,
        "participants_count": int(participants),
        "roles": [r.strip() for r in roles.split(",") if r.strip()]
    }
    save_json(wk, "workshops", wid)
    st.success(f"Workshop saved as {wid}")

st.divider()
st.subheader("Add Workshop Evidence")
with st.form("w_evidence"):
    wk_id_input = st.text_input("Workshop ID (e.g., WS-YYYYMMDD-uni)", value="")
    e_type = st.selectbox("Type", options=EVIDENCE_TYPES, index=1)
    content = st.text_area("Quote or note (content)", height=80)
    card_ref = st.text_input("Card code (e.g., B7) if applicable", value="")
    submitted = st.form_submit_button("💾 Save Evidence")
    if submitted:
        ev_id = evidence_id()
        ev = {"evidence_id": ev_id, "type": e_type, "content": content or "—", "source": wk_id_input or "—"}
        if wk_id_input:
            ev["workshop_id"] = wk_id_input
        if card_ref:
            ev["card_ref"] = card_ref
        save_json(ev, "evidence", ev_id)
        st.success(f"Saved Evidence {ev_id}")
        st.json(ev)

st.divider()
st.subheader("Create a Workshop-derived Insight")

with st.form("wk_insight"):
    wk_id = st.text_input("Workshop ID to link", value="")
    c1, c2, c3 = st.columns(3)
    with c1:
        channel = st.selectbox("Channel", options=CHANNELS, format_func=lambda x: CHANNEL_LABEL[x])
    with c2:
        dimension = st.selectbox("Dimension", options=DIMENSIONS, format_func=lambda x: DIMENSION_LABEL[x])
    with c3:
        time_h = st.selectbox("Time Horizon", options=TIME_HORIZONS, index=2)

    policy_gap = st.text_input("Policy Gap")
    root_cause = st.text_input("Root Cause")
    proposed_objective = st.text_input("Proposed Policy Objective")

    a_cards = st.text_input("A (Assessment) codes", value="")
    b_cards = st.text_input("B (Challenge) codes", value="B7")
    c_cards = st.text_input("C (Scenario) codes", value="")
    d_cards = st.text_input("D (Objective) codes", value="")
    e_principles = st.multiselect("E (Principles)", options=PRINCIPLES, default=["E5","E6"])

    gls = st.multiselect("Related Guidelines", options=list(GUIDELINES.keys()), default=[])
    owner_role = st.text_input("Owner Role", value="Vice-Rector Policy")

    impact = st.slider("Impact (1–5)", 1, 5, 5)
    effort = st.slider("Effort (1–5)", 1, 5, 3)
    priority = compute_priority_quadrant(impact, effort)

    ev_ids = st.text_input("Attach Evidence IDs (comma-separated)", value="")

    submitted = st.form_submit_button("💾 Save Insight")
    if submitted:
        ins_id = insight_id()
        cards = {
            "A": [x.strip() for x in a_cards.split(",") if x.strip()],
            "B": [x.strip() for x in b_cards.split(",") if x.strip()],
            "C": [x.strip() for x in c_cards.split(",") if x.strip()],
            "D": [x.strip() for x in d_cards.split(",") if x.strip()],
            "E": e_principles,
        }
        ins = {
            "insight_id": ins_id,
            "university_id": uni_sel,
            "workshop_id": wk_id or None,
            "channel": channel,
            "dimension": dimension,
            "cards": cards,
            "policy_gap": policy_gap,
            "root_cause": root_cause,
            "proposed_objective": proposed_objective,
            "principles_selected": e_principles,
            "stakeholder_ids": [],
            "evidence_ids": [x.strip() for x in ev_ids.split(",") if x.strip()],
            "related_guidelines": gls,
            "impact_1to5": impact,
            "effort_1to5": effort,
            "priority_quadrant": priority,
            "owner_role": owner_role,
            "time_horizon": time_h,
            "status": "validated",
            "tags": [],
            "created_at": ts(),
            "updated_at": ts()
        }
        errs = validate_insight(ins)
        if errs:
            st.error("Validation errors:\n- " + "\n- ".join(errs))
        else:
            save_json(ins, "insights", ins_id)
            st.success(f"Insight saved as {ins_id} (Priority: {priority})")
            st.json(ins)
