# utils/validators.py
from jsonschema import validate, Draft202012Validator

INSIGHT_SCHEMA = {
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["insight_id","university_id","channel","dimension","cards","impact_1to5","effort_1to5","priority_quadrant"],
  "properties": {
    "insight_id": {"type": "string"},
    "university_id": {"type": "string"},
    "workshop_id": {"type": "string"},
    "channel": {"type": "string"},
    "dimension": {"type": "string"},
    "cards": {
      "type": "object",
      "properties": {
        "A":{"type":"array","items":{"type":"string"}},
        "B":{"type":"array","items":{"type":"string"}},
        "C":{"type":"array","items":{"type":"string"}},
        "D":{"type":"array","items":{"type":"string"}},
        "E":{"type":"array","items":{"type":"string"}}
      },
      "additionalProperties": False
    },
    "policy_gap": {"type":"string"},
    "root_cause": {"type":"string"},
    "proposed_objective": {"type":"string"},
    "principles_selected": {"type":"array","items":{"type":"string"}},
    "stakeholder_ids": {"type":"array","items":{"type":"string"}},
    "evidence_ids": {"type":"array","items":{"type":"string"}},
    "related_guidelines": {"type":"array","items":{"type":"string"}},
    "impact_1to5": {"type":"integer","minimum":1,"maximum":5},
    "effort_1to5": {"type":"integer","minimum":1,"maximum":5},
    "priority_quadrant": {"type":"string"},
    "owner_role": {"type":"string"},
    "time_horizon": {"type":"string"},
    "status": {"type":"string"},
    "tags": {"type":"array","items":{"type":"string"}},
    "created_at": {"type":"string"},
    "updated_at": {"type":"string"}
  }
}

def validate_insight(obj: dict) -> list[str]:
    v = Draft202012Validator(INSIGHT_SCHEMA)
    errs = [f"{e.message} at {'/'.join([str(x) for x in e.path])}" for e in v.iter_errors(obj)]
    return errs
