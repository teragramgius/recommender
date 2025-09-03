# utils/persistence.py
from pathlib import Path
import json, datetime
from typing import Any, Dict, List

DATA_DIR = Path("data")

FOLDERS = [
    "universities", "stakeholders", "workshops",
    "guidelines", "evidence", "insights", "recommendations"
]

def init_data_dirs():
    for f in FOLDERS:
        (DATA_DIR / f).mkdir(parents=True, exist_ok=True)

def ts() -> str:
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def save_json(obj: Dict[str, Any], folder: str, file_id: str) -> str:
    init_data_dirs()
    path = DATA_DIR / folder / f"{file_id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return str(path)

def load_all(folder: str) -> List[Dict[str, Any]]:
    init_data_dirs()
    items = []
    for p in (DATA_DIR / folder).glob("*.json"):
        try:
            items.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception:
            pass
    return items

def load_by_id(folder: str, file_id: str) -> Dict[str, Any] | None:
    p = DATA_DIR / folder / f"{file_id}.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return None

def compute_priority_quadrant(impact: int, effort: int) -> str:
    if impact >= 3 and effort < 3:
        return "Strategic Quick Win"
    if impact >= 3 and effort >= 3:
        return "Strategic Investment"
    if impact < 3 and effort < 3:
        return "Avoid"
    return "Policy Maintenance"
