"""
NX CLI — DESKTOP AGENT (the client half of the web→live-machine transport). When the operator hands off a desktop
mission from Nexplora's web code agent (the computer_operator tool), it lands in a durable per-operator queue. THIS
is the agent that runs ON the operator's Mac: it polls Nexplora for the operator's next queued mission, CLAIMS it,
drives it with the computer-use engine (nx_computer.control_computer — every action still confirmed by the
operator, credentials/payments never entered), and REPORTS the outcome back for the web UI to surface. Invoked
with `$desktop` (run the queued missions now).

Auth: the operator's own NX bearer token (cfg['token']) against api.nexplora.ai — the missions API is operator-
scoped server-side, so this agent only ever sees its OWN operator's missions.

The orchestration (poll → run → report, bounded) is PURE with an injected transport + runner, so it's unit-tested
with no network + no Mac. The concrete HTTP transport + the control_computer executor are deploy/device-proven,
like nx_browse's Playwright + nx_computer's cliclick paths.
"""

from __future__ import annotations

import json
from typing import Any, Callable, Optional

MAX_MISSIONS_DEFAULT = 3
_SUMMARY_CAP = 4000


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# PURE — map a control_computer run to a mission report (status + honest summary).
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

def map_run_to_report(goal: str, result: dict) -> tuple[str, str]:
    """Map an nx_computer.control_computer result ({ok, done, halted, steps, guidance?}) to a terminal mission
    (status, summary). A not-ok / planner error is 'failed'; a completed run OR an honest partial stop (operator
    declined, a credential/payment step refused, the step cap hit) is 'done', with the detail in the summary. The
    summary NEVER contains a typed secret (control_computer's describe hides typed text; refused steps aren't run).
    Pure."""
    ok = result.get("ok", True)
    halted = result.get("halted")
    status = "failed" if (ok is False or halted == "planner_error") else "done"
    try:
        import nx_computer as _nc
        did = "; ".join(
            "%s%s" % (_nc.describe_action(s.get("action", {})), "" if s.get("executed") else " (skipped)")
            for s in (result.get("steps") or [])
        ) or "(no actions taken)"
    except Exception:
        did = "%d step(s)" % len(result.get("steps") or [])
    ended = halted or ("done" if result.get("done") else "stopped")
    summary = "Goal: %s\nWhat I did: %s\nEnded: %s." % (goal, did, ended)
    if halted == "prohibited":
        summary += " I stopped at a credential/payment step — that one's yours to do."
    if result.get("guidance"):
        summary += "\n" + str(result["guidance"])
    return status, summary[:_SUMMARY_CAP]


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# ORCHESTRATION — poll → run → report, bounded. Injected transport + runner (testable).
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

def run_desktop_missions(
    fetch_next: Callable[[], Optional[dict]],
    run_mission: Callable[[str], dict],
    report: Callable[[str, str, str], bool],
    on_step: Optional[Callable[[str], None]] = None,
    max_missions: int = MAX_MISSIONS_DEFAULT,
) -> dict:
    """Claim + run queued desktop missions until the queue is empty or the cap is hit. Injected:
      fetch_next() -> {mission_id, goal} | None (claims the operator's next queued mission; None = queue empty),
      run_mission(goal) -> a control_computer result dict,
      report(mission_id, status, summary) -> bool.
    A run that raises is reported 'failed' (the mission never silently vanishes). Pure orchestration — no network,
    no Mac. Returns {ran, failed}."""
    on_step = on_step or (lambda _s: None)
    ran = 0
    failed = 0
    for _ in range(max(1, min(int(max_missions), 20))):
        try:
            m = fetch_next()
        except Exception:
            break
        if not m or not m.get("mission_id"):
            break  # queue empty
        mid = str(m["mission_id"])
        goal = str(m.get("goal") or "")
        on_step("claimed mission: " + goal)
        try:
            result = run_mission(goal)
        except Exception as e:
            report(mid, "failed", "The desktop agent errored: " + type(e).__name__)
            failed += 1
            continue
        status, summary = map_run_to_report(goal, result)
        report(mid, status, summary)
        on_step("reported %s — %s" % (status, goal))
        ran += 1
        if status == "failed":
            failed += 1
    return {"ran": ran, "failed": failed}


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# TRANSPORT (deploy-proven) — the operator-authed Nexplora missions API.
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

def _http_post_json(url: str, token: str, payload: dict, timeout: float = 30.0) -> Optional[dict]:
    """POST JSON with the operator's bearer token; parse a JSON reply. None on any error (network/HTTP/parse) — the
    orchestration treats None as 'no mission' / 'report failed', never raising. Uses stdlib urllib (no new dep)."""
    import urllib.request
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, method="POST",
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + (token or "")},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:  # nosec - operator's own authed backend
            return json.loads(r.read().decode("utf-8") or "{}")
    except Exception:
        return None


def nexplora_fetch_next(base: str, token: str, agent_label: str) -> Optional[dict]:
    """Claim the operator's next queued desktop mission via POST /api/desktop/missions/next. Returns
    {mission_id, goal} or None (empty queue / error). Normalizes the API's camelCase missionId."""
    r = _http_post_json(base.rstrip("/") + "/api/desktop/missions/next", token, {"agentLabel": agent_label})
    if not r or not r.get("ok"):
        return None
    mission = r.get("mission")
    if not mission or not mission.get("missionId"):
        return None
    return {"mission_id": mission["missionId"], "goal": mission.get("goal", "")}


def nexplora_report(base: str, token: str, mission_id: str, status: str, summary: str) -> bool:
    """Report a mission's outcome via POST /api/desktop/missions/report. True on ok."""
    r = _http_post_json(base.rstrip("/") + "/api/desktop/missions/report", token,
                        {"missionId": mission_id, "status": status, "resultSummary": summary})
    return bool(r and r.get("ok"))


def make_transport(base: str, token: str, agent_label: str) -> tuple[Callable[[], Optional[dict]], Callable[[str, str, str], bool]]:
    """Build (fetch_next, report) bound to the operator's Nexplora backend + token, for run_desktop_missions."""
    return (
        lambda: nexplora_fetch_next(base, token, agent_label),
        lambda mid, status, summary: nexplora_report(base, token, mid, status, summary),
    )
