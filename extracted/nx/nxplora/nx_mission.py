"""
NX CLI — AUTONOMOUS MISSIONS ($mission). Dispatch NX/Nexplora to go DO an outcome — make sales, do outreach,
market, research — over the operator's connected integrations + the open web, running unattended for minutes or
HOURS, on the operator's own settings, with whatever model the operator picks (NX default, BYOK otherwise).

Unlike $desktop (which NX runs on the operator's Mac), a mission runs SERVER-SIDE: NX dispatches it to Nexplora's
backend, which drives it autonomously segment-by-segment via the cron mission-runner and survives the tab. So this
module is a thin, operator-authed CLIENT — dispatch, then poll status / authorize-live / cancel — mirroring
nx_desktop's transport (operator's own bearer token against api.nexplora.ai; the missions API is operator-scoped
server-side, so NX only ever touches the operator's OWN missions).

SAFETY (enforced server-side, surfaced here): a mission defaults to dry_run (draft everything, SEND NOTHING). A
live mission does not send until the operator authorizes it (authorize_live) — then it runs at full autonomy within
the mission's step + cost budget. Credentials/payments are NEVER entered by the agent, in any mode.

The pure request/parse/summarize helpers are unit-tested with no network; the HTTP transport is deploy-proven like
nx_desktop's.
"""

from __future__ import annotations

import json
from typing import Any, Optional

_VALID_MODES = ("dry_run", "live")
_GOAL_CAP = 8000


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# PURE — request bodies, response parsing, operator-facing summaries (no network).
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

def mission_payload(goal: str, mode: str = "dry_run", settings: Optional[dict] = None,
                    model_intent: Optional[str] = None, source: str = "nx_cli") -> dict:
    """Build the POST /api/autonomous/missions body. mode is clamped to a valid value (default dry_run — the safe
    default: draft everything, send nothing). Pure."""
    body: dict[str, Any] = {
        "goal": (goal or "").strip()[:_GOAL_CAP],
        "mode": mode if mode in _VALID_MODES else "dry_run",
        "source": source,
    }
    if settings:
        body["settings"] = settings
    if model_intent:
        body["model_intent"] = model_intent
    return body


def parse_mission_id(resp: Optional[dict]) -> Optional[str]:
    """Pull the missionId from a dispatch response ({ok, missionId}). None on any not-ok / missing shape."""
    if not resp or not resp.get("ok"):
        return None
    mid = resp.get("missionId")
    return str(mid) if mid else None


def status_label(status: str) -> str:
    """A short operator-facing label for a mission status."""
    return {
        "queued": "queued",
        "running": "running",
        "awaiting_authorization": "waiting for your OK to go live",
        "done": "done",
        "failed": "failed",
        "canceled": "canceled",
    }.get(status, status or "unknown")


def is_terminal(status: str) -> bool:
    return status in ("done", "failed", "canceled")


def summarize_mission(row: Optional[dict]) -> str:
    """A one-block operator-facing summary of a mission row (status + tallies + summary). Never surfaces a secret —
    the server's trace/summary never carries one. Pure."""
    if not row:
        return "No mission found."
    status = str(row.get("status") or "unknown")
    sends = int(row.get("sends") or 0)
    drafts = int(row.get("drafts") or 0)
    refused = int(row.get("refused") or 0)
    goal = str(row.get("goal") or "")
    line = "Mission [%s]: %s" % (status_label(status), goal[:200])
    tally = "  %d sent · %d drafted · %d left for you" % (sends, drafts, refused)
    out = line + "\n" + tally
    if status == "awaiting_authorization":
        out += "\n  → it's ready to act. Authorize live to let it send, or cancel."
    summary = row.get("summary")
    if summary:
        out += "\n  " + str(summary)
    return out


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# TRANSPORT (deploy-proven) — the operator-authed Nexplora autonomous-missions API.
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

def _http_json(url: str, token: str, method: str, payload: Optional[dict] = None, timeout: float = 30.0) -> Optional[dict]:
    """Operator-authed JSON request (bearer token). None on any error (network/HTTP/parse) — callers treat None as
    'not available' and never raise. Stdlib urllib (no new dep)."""
    import urllib.request
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + (token or "")},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:  # nosec - operator's own authed backend
            return json.loads(r.read().decode("utf-8") or "{}")
    except Exception:
        return None


def dispatch_mission(base: str, token: str, goal: str, mode: str = "dry_run",
                     settings: Optional[dict] = None, model_intent: Optional[str] = None) -> Optional[str]:
    """Dispatch a mission via POST /api/autonomous/missions. Returns the missionId, or None on failure."""
    r = _http_json(base.rstrip("/") + "/api/autonomous/missions", token, "POST",
                   mission_payload(goal, mode, settings, model_intent))
    return parse_mission_id(r)


def get_mission(base: str, token: str, mission_id: str) -> Optional[dict]:
    """Read a mission's status + trace via GET /api/autonomous/missions/<id>. Returns the mission row or None."""
    r = _http_json(base.rstrip("/") + "/api/autonomous/missions/" + str(mission_id), token, "GET")
    if not r or not r.get("ok"):
        return None
    return r.get("mission")


def authorize_live(base: str, token: str, mission_id: str) -> bool:
    """Authorize a live mission to perform REAL sends (full autonomy within its budget). True on ok."""
    r = _http_json(base.rstrip("/") + "/api/autonomous/missions/" + str(mission_id), token, "POST",
                   {"action": "authorize_live"})
    return bool(r and r.get("ok"))


def cancel_mission(base: str, token: str, mission_id: str) -> bool:
    """Cancel a non-terminal mission. True on ok."""
    r = _http_json(base.rstrip("/") + "/api/autonomous/missions/" + str(mission_id), token, "POST",
                   {"action": "cancel"})
    return bool(r and r.get("ok"))


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# RECURRING SCHEDULES + PERSISTENT SETTINGS — "set it for cron to run on its own, on my settings".
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

_VALID_CADENCES = ("hourly", "every_6h", "every_12h", "daily", "weekly", "custom")


def schedule_payload(goal: str, cadence: str = "daily", mode: str = "dry_run",
                     settings: Optional[dict] = None, model_intent: Optional[str] = None) -> dict:
    """Build the POST /api/autonomous/schedules body. cadence + mode are clamped to valid values (default
    daily / dry_run — the safe default). Pure."""
    body: dict[str, Any] = {
        "goal": (goal or "").strip()[:_GOAL_CAP],
        "cadence": cadence if cadence in _VALID_CADENCES else "daily",
        "mode": mode if mode in _VALID_MODES else "dry_run",
    }
    if settings:
        body["settings"] = settings
    if model_intent:
        body["model_intent"] = model_intent
    return body


def parse_schedule_id(resp: Optional[dict]) -> Optional[str]:
    """Pull the scheduleId from a create response ({ok, scheduleId}). None on any not-ok / missing shape."""
    if not resp or not resp.get("ok"):
        return None
    sid = resp.get("scheduleId")
    return str(sid) if sid else None


def cadence_from_text(text: str) -> str:
    """Map a free-text cadence word to a canonical cadence (default daily). Pure — lets the operator say
    'every day' / 'hourly' / 'weekly' naturally."""
    t = (text or "").lower()
    if "hour" in t:
        return "hourly"
    if "week" in t:
        return "weekly"
    if "12" in t:
        return "every_12h"
    if "6" in t:
        return "every_6h"
    return "daily"


def summarize_schedules(rows: Optional[list]) -> str:
    """A one-block operator-facing summary of the operator's recurring schedules. Pure."""
    if not rows:
        return "No recurring missions scheduled."
    lines = ["Recurring missions:"]
    for r in rows:
        goal = str(r.get("goal") or "")[:120]
        cadence = str(r.get("cadence") or "daily")
        mode = str(r.get("mode") or "dry_run")
        on = "on" if r.get("enabled") else "paused"
        lines.append("  · [%s · %s · %s] %s" % (cadence, mode, on, goal))
    return "\n".join(lines)


def create_schedule(base: str, token: str, goal: str, cadence: str = "daily",
                    mode: str = "dry_run", settings: Optional[dict] = None,
                    model_intent: Optional[str] = None) -> Optional[str]:
    """Create a recurring mission via POST /api/autonomous/schedules. Returns the scheduleId, or None."""
    r = _http_json(base.rstrip("/") + "/api/autonomous/schedules", token, "POST",
                   schedule_payload(goal, cadence, mode, settings, model_intent))
    return parse_schedule_id(r)


def list_schedules(base: str, token: str) -> Optional[list]:
    """List the operator's recurring missions via GET /api/autonomous/schedules. Returns rows or None."""
    r = _http_json(base.rstrip("/") + "/api/autonomous/schedules", token, "GET")
    if not r or not r.get("ok"):
        return None
    return r.get("schedules") or []


def get_settings(base: str, token: str) -> Optional[dict]:
    """Read the operator's saved mission settings via GET /api/autonomous/settings. Returns the settings or None."""
    r = _http_json(base.rstrip("/") + "/api/autonomous/settings", token, "GET")
    if not r or not r.get("ok"):
        return None
    return r.get("settings")


def save_settings(base: str, token: str, settings: Optional[dict] = None,
                  default_mode: Optional[str] = None, default_model_intent: Optional[str] = None) -> bool:
    """Save the operator's default mission settings via PUT /api/autonomous/settings. True on ok."""
    body: dict[str, Any] = {}
    if settings is not None:
        body["settings"] = settings
    if default_mode in _VALID_MODES:
        body["default_mode"] = default_mode
    if default_model_intent is not None:
        body["default_model_intent"] = default_model_intent
    r = _http_json(base.rstrip("/") + "/api/autonomous/settings", token, "PUT", body)
    return bool(r and r.get("ok"))
