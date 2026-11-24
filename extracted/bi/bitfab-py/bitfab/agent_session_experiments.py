from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from bitfab.git_state import resolve_agent_session_id

_SAFE_SESSION_ID = re.compile(r"^[A-Za-z0-9_-][A-Za-z0-9._-]*$")


def _session_id_for_path(explicit: str | None) -> str | None:
    try:
        session_id = resolve_agent_session_id(explicit)
    except Exception:
        return None
    if session_id is None or not _SAFE_SESSION_ID.match(session_id):
        return None
    return session_id


def record_agent_session_experiment(
    *,
    experiment_id: str,
    experiment_url: str,
    name: str | None,
    service_url: str,
    explicit_agent_session_id: str | None,
) -> None:
    session_id = _session_id_for_path(explicit_agent_session_id)
    if session_id is None:
        return
    try:
        directory = (
            Path(os.path.expanduser("~")) / ".bitfab" / "agent-sessions" / session_id
        )
        directory.mkdir(parents=True, exist_ok=True)
        line = json.dumps(
            {
                "experimentId": experiment_id,
                "experimentUrl": experiment_url,
                "name": name,
                "serviceUrl": service_url,
                "startedAt": datetime.now(timezone.utc).isoformat(),
            }
        )
        with open(directory / "experiments.jsonl", "a", encoding="utf-8") as handle:
            handle.write(line + "\n")
    except Exception:
        return
