import json
import os
from functools import lru_cache
from typing import Optional, Dict, Any

CATALOG_PATH_DEFAULT = os.path.join(os.path.dirname(__file__), "controls_catalog.json")

@lru_cache(maxsize=1)
def _load_catalog(path: Optional[str] = None) -> Dict[str, Any]:
    p = path or CATALOG_PATH_DEFAULT
    if not os.path.exists(p):
        return {}
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Index by Control_ID
    index = {}
    for entry in data.get("controls", []):
        cid = entry.get("Control_ID")
        if cid:
            index[cid] = entry
    return index

def get_control(control_id: str, path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    catalog = _load_catalog(path)
    return catalog.get(control_id)

def reset_cache():
    _load_catalog.cache_clear()
