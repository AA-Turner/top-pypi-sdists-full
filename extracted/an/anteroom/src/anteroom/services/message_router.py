"""Message-to-run router for follow-up messages (#889).

Classifies incoming user messages against active workflow runs and
produces a routing action: attach, update, cancel, replace, spawn,
or ask_user.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Literal

RouterAction = Literal["attach", "update", "cancel", "replace", "spawn", "ask_user"]

MAX_ACTIVE_RUNS_PER_CONVERSATION = 3

# ---------------------------------------------------------------------------
# Keyword patterns
# ---------------------------------------------------------------------------

_CANCEL_PATTERNS = re.compile(
    r"\b(cancel|stop|abort|nevermind|never\s*mind)\b",
    re.IGNORECASE,
)

_UPDATE_PATTERNS = re.compile(
    r"\b(actually|wait|change|update|instead|use\s+\S+\s+instead)\b",
    re.IGNORECASE,
)

_ATTACH_PATTERNS = re.compile(
    r"\b(I\s+pushed|I\s+fixed|done|ready|finished|here'?s)\b",
    re.IGNORECASE,
)

_SPAWN_HINT_PATTERN = re.compile(
    r"\b(deploy|run|start|create|build|test|check|scan|review)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class RouteResult:
    """Outcome of message routing."""

    action: RouterAction
    target_run_id: str | None = None
    spawn_hint: str | None = None
    clarification: str | None = None


def route_message(text: str, active_runs: list[dict[str, Any]]) -> RouteResult:
    """Route a user message against active workflow runs.

    Uses keyword heuristics (not LLM) to classify intent.
    When multiple runs match ambiguously, returns ask_user.
    """
    text_stripped = text.strip()

    # No active runs -> always spawn
    if not active_runs:
        hint = _extract_spawn_hint(text_stripped)
        return RouteResult(action="spawn", spawn_hint=hint)

    has_cancel = bool(_CANCEL_PATTERNS.search(text_stripped))
    has_update = bool(_UPDATE_PATTERNS.search(text_stripped))
    has_attach = bool(_ATTACH_PATTERNS.search(text_stripped))

    # Replace: cancel + spawn signal in one message
    if has_cancel and (has_update or _SPAWN_HINT_PATTERN.search(text_stripped)):
        if len(active_runs) == 1:
            hint = _extract_spawn_hint(text_stripped)
            return RouteResult(action="replace", target_run_id=active_runs[0]["id"], spawn_hint=hint)
        return _ask_user_for_ambiguity(active_runs)

    # Cancel
    if has_cancel:
        if len(active_runs) == 1:
            return RouteResult(action="cancel", target_run_id=active_runs[0]["id"])
        return _ask_user_for_ambiguity(active_runs)

    # Update
    if has_update:
        if len(active_runs) == 1:
            return RouteResult(action="update", target_run_id=active_runs[0]["id"])
        return _ask_user_for_ambiguity(active_runs)

    # Attach
    if has_attach:
        if len(active_runs) == 1:
            return RouteResult(action="attach", target_run_id=active_runs[0]["id"])
        return _ask_user_for_ambiguity(active_runs)

    # No clear intent with active runs -> spawn new work
    hint = _extract_spawn_hint(text_stripped)
    return RouteResult(action="spawn", spawn_hint=hint)


def _extract_spawn_hint(text: str) -> str | None:
    m = _SPAWN_HINT_PATTERN.search(text)
    return m.group(1).lower() if m else None


def _ask_user_for_ambiguity(active_runs: list[dict[str, Any]]) -> RouteResult:
    run_descriptions = []
    for i, r in enumerate(active_runs[:MAX_ACTIVE_RUNS_PER_CONVERSATION], 1):
        wf_id = r.get("workflow_id", "unknown")
        status = r.get("status", "unknown")
        run_descriptions.append(f"  {i}. {wf_id} (status: {status}, id: {r['id'][:8]})")
    runs_text = "\n".join(run_descriptions)
    clarification = (
        f"Multiple workflow runs are active for this conversation:\n{runs_text}\n"
        "Which run should this message apply to? "
        "(Reply with the number, workflow name, or run id prefix.)"
    )
    return RouteResult(action="ask_user", clarification=clarification)


def resolve_disambiguation(
    text: str,
    pending_runs: list[dict[str, Any]],
) -> str | None:
    """Try to resolve a disambiguation follow-up message to a specific run_id.

    Called when the previous router decision was ``ask_user`` and the user
    has replied. Matches by:

    1. List position (``1``, ``2``, ``#1``, ``#2``)
    2. Workflow ID prefix (case-insensitive substring of ``workflow_id``)
    3. Run ID prefix (first 4+ hex chars of the run UUID)

    Returns the ``run_id`` of the matched run, or ``None`` if the text
    doesn't clearly resolve to a single run.
    """
    text_stripped = text.strip().lower()
    if not text_stripped or not pending_runs:
        return None

    # 1. Match by list position: "1", "2", "#1", "#2", "the first one"
    pos_match = re.match(r"^#?(\d+)$", text_stripped)
    if pos_match:
        idx = int(pos_match.group(1)) - 1  # 1-indexed
        if 0 <= idx < len(pending_runs):
            return pending_runs[idx]["id"]
        return None

    ordinals = {"first": 0, "second": 1, "third": 2}
    for word, idx in ordinals.items():
        if word in text_stripped and idx < len(pending_runs):
            return pending_runs[idx]["id"]

    # 2. Match by workflow_id (case-insensitive): full-text substring first,
    #    then word-level matching for replies like "the code review one".
    matches_by_wf = [r for r in pending_runs if text_stripped in r.get("workflow_id", "").lower()]
    if len(matches_by_wf) == 1:
        return matches_by_wf[0]["id"]

    # Word-level: extract significant words (3+ chars, not stop words) and
    # check if any single word uniquely matches exactly one workflow_id.
    _stop = {"the", "one", "that", "this", "for", "and", "with"}
    words = [w for w in re.findall(r"[a-z0-9]+", text_stripped) if len(w) >= 3 and w not in _stop]
    for word in words:
        word_matches = [r for r in pending_runs if word in r.get("workflow_id", "").lower()]
        if len(word_matches) == 1:
            return word_matches[0]["id"]

    # 3. Match by run_id prefix (first 4+ hex chars)
    hex_match = re.match(r"^([0-9a-f]{4,})$", text_stripped)
    if hex_match:
        prefix = hex_match.group(1)
        matches_by_id = [r for r in pending_runs if r["id"].lower().startswith(prefix)]
        if len(matches_by_id) == 1:
            return matches_by_id[0]["id"]

    return None
