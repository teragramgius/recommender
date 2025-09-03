# utils/recommender.py
from utils.enums import CHANNEL_LABEL, DIMENSION_LABEL
from utils.ids import recommendation_id
from utils.persistence import save_json

def recommend_from_insight(insight: dict) -> dict:
    ch = CHANNEL_LABEL.get(insight["channel"], insight["channel"])
    dim = DIMENSION_LABEL.get(insight["dimension"], insight["dimension"])
    pr = ", ".join(insight.get("principles_selected", [])) or "—"
    gl = ", ".join(insight.get("related_guidelines", [])) or "—"

    text = (
        f"For the channel {ch} in the {dim} dimension, we observed {insight.get('policy_gap','—')}. "
        f"We propose {insight.get('proposed_objective','—')} guided by {pr} and aligned with {gl}. "
        f"Priority: {insight['priority_quadrant']} (Impact {insight['impact_1to5']}/Effort {insight['effort_1to5']}); "
        f"Owner: {insight.get('owner_role','—')}; Time horizon: {insight.get('time_horizon','—')}."
    )

    rc = {
      "recommendation_id": recommendation_id(insight["insight_id"]),
      "insight_id": insight["insight_id"],
      "text": text,
      "channel": insight["channel"],
      "dimension": insight["dimension"],
      "priority_quadrant": insight["priority_quadrant"],
      "guidelines": insight.get("related_guidelines", [])
    }
    save_json(rc, "recommendations", rc["recommendation_id"])
    return rc
