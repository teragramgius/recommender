# pages/1_🎯_Self_Assessment.py
import streamlit as st
from datetime import date
from utils.enums import CHANNELS, CHANNEL_LABEL, DIMENSIONS, DIMENSION_LABEL, GUIDELINES, TIME_HORIZONS, PRINCIPLES
from utils.ids import uni_id, evidence_id, insight_id
from utils.persistence import save_json, load_all, compute_priority_quadrant, ts
from utils.validators import validate_insight

st.set_page_config(page_title="Self Assessment", page_icon="🎯", layout="wide")
st.title("🎯 Self-Assessment → Insight")

# --- University picker / creator ---
st.subheader("University")
unis = {u["university_id"]: u for u in load_all("universities")}
col1, col2 = st.columns([2,1])
with col1:
    if unis:
        uni_sel = st.selectbox("Select University", options=list(unis.keys()), format_func=lambda k: f"{unis[k]['name']} ({k})")
    else:
        uni_sel = None
with col2:
    st.caption("Create a new university")
    with st.popover("➕ New University"):
        name = st.text_input("Name")
        country = st.text_input("Country")
        if st.button("Create"):
            if name:
                uid = uni_id(name)
                obj = {"university_id": uid, "name": name, "country": country or "—"}
                save_json(obj, "universities", uid)
                st.success(f"Created {uid}. Refresh the selector.")
            else:
                st.error("Please enter a university name.")

if not uni_sel and not unis:
    st.info("Create a university to begin.")
    st.stop()
elif not uni_sel:
    st.warning("Select a university from the dropdown.")
    st.stop()

st.divider()
st.subheader("Create SAT Evidence (optional)")
with st.expander("Add a SAT Evidence note (becomes linkable in Insights)"):
    note = st.text_area("SAT note (e.g., 'Organisational readiness for mobility = 2/5')", height=80)
    if st.button("Save SAT Evidence"):
        ev_id = evidence_id()
        ev = {"evidence_id": ev_id, "type": "SAT Score", "content": note or "SAT note", "source": f"Self-Assessment Tool, {date.today().isoformat()}"}
        save_json(ev, "evidence", ev_id)
        st.success(f"Saved Evidence {ev_id}")

st.divider()
st.subheader("Compose a SAT-derived Insight")

with st.form("sat_insight"):
    c1, c2, c3 = st.columns(3)
    with c1:
        channel = st.selectbox("Channel", options=CHANNELS, format_func=lambda x: CHANNEL_LABEL[x])
    with c2:
        dimension = st.selectbox("Dimension", options=DIMENSIONS, format_func=lambda x: DIMENSION_LABEL[x])
    with c3:
        time_h = st.selectbox("Time Horizon", options=TIME_HORIZONS, index=1)

    policy_gap = st.text_input("Policy Gap (what is missing?)")
    root_cause = st.text_input("Root Cause (why?)")
    proposed_objective = st.text_input("Proposed Policy Objective (what to achieve?)")

    st.markdown("**Cards used** (A/B/C/D/E). Use codes like A3, B7, C2, D4. Choose principles for E.")
    a_cards = st.text_input("A (Assessment) codes, comma-separated", value="A3")
    b_cards = st.text_input("B (Challenge) codes, comma-separated", value="B7")
    c_cards = st.text_input("C (Scenario) codes, comma-separated", value="")
    d_cards = st.text_input("D (Objective) codes, comma-separated", value="D4")
    e_principles = st.multiselect("E (Principles)", options=PRINCIPLES, default=["E2"])

    guidelines = st.multiselect("Related Guidelines", options=list(GUIDELINES.keys()), default=["PG03"])
    owner_role = st.text_input("Owner Role", value="Rectorate")

    impact = st.slider("Impact (1–5)", 1, 5, 4)
    effort = st.slider("Effort (1–5)", 1, 5, 2)
    priority = compute_priority_quadrant(impact, effort)

    evidence_hint = st.text_input("Link Evidence IDs (comma-separated, optional)", value="")

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
            "channel": channel,
            "dimension": dimension,
            "cards": cards,
            "policy_gap": policy_gap,
            "root_cause": root_cause,
            "proposed_objective": proposed_objective,
            "principles_selected": e_principles,
            "stakeholder_ids": [],
            "evidence_ids": [x.strip() for x in evidence_hint.split(",") if x.strip()],
            "related_guidelines": guidelines,
            "impact_1to5": impact,
            "effort_1to5": effort,
            "priority_quadrant": priority,
            "owner_role": owner_role,
            "time_horizon": time_h,
            "status": "draft",
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
