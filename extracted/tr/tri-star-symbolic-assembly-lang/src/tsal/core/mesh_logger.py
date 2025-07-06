import json
import time
from pathlib import Path
from typing import Dict, Any

LOG_FILE = Path("data/mesh_log.jsonl")
VERBOSE_LOGGING = False

def log_event(
    event_type: str,
    payload: Dict[str, Any],
    phase: str | None = None,
    origin: str | None = None,
    verbose: bool = False,
) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("payload must be a dict")
    entry = {
        "timestamp": time.time(),
        "event_type": event_type,
        "phase": phase or "unknown",
        "payload": payload,
        "origin": origin or "core",
    }
    LOG_FILE.parent.mkdir(exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")
    if verbose or VERBOSE_LOGGING:
        print(json.dumps(entry))
    return entry
