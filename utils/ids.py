# utils/ids.py
import uuid
from datetime import date

def slugify(s: str) -> str:
    out = "".join(ch.lower() if ch.isalnum() else "-" for ch in s.strip())
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-")

def uni_id(name: str) -> str:
    return f"UNI-{slugify(name)}"

def stakeholder_id(uni: str, name: str) -> str:
    return f"ST-{slugify(uni)}-{slugify(name)}"

def workshop_id(uni: str, d: date | None = None) -> str:
    d = d or date.today()
    return f"WS-{d.strftime('%Y%m%d')}-{slugify(uni)}"

def evidence_id() -> str:
    return f"EV-{uuid.uuid4().hex[:10]}"

def insight_id() -> str:
    return f"IN-{uuid.uuid4().hex[:10]}"

def recommendation_id(insight_id_str: str) -> str:
    return f"RC-{insight_id_str}"
