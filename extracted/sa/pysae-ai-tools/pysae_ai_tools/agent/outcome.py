"""Parse the AUTOPILOT_RESULT footer emitted by /code-autopilot.

Two stages:
1. ``parse_outcome`` — pure stdout parsing, no side effects, no I/O.
2. ``resolve_outcome`` — wraps parse_outcome with a GitLab fallback that
   queries the issue's related MRs when the footer is missing or unparseable.
   The agent is a noisy narrator on long runs; GitLab is the source of
   truth for what actually shipped.
"""

import json
import logging
import re
import urllib.parse
from typing import Any, cast

from ..common.glab.runner import glab_api
from .models import Outcome, OutcomeStatus

logger = logging.getLogger(__name__)

_FOOTER_RE = re.compile(
    r"<<<AUTOPILOT_RESULT\s*(.*?)\s*AUTOPILOT_RESULT>>>",
    re.DOTALL,
)

FOOTER_MISSING_REASON = "AUTOPILOT_RESULT footer missing"
_FOOTER_UNPARSEABLE_PREFIX = "footer unparseable:"


def parse_outcome(stdout: str, fallback_iid: int, fallback_project: str) -> Outcome:
    matches = _FOOTER_RE.findall(stdout)
    if not matches:
        return _unparseable(fallback_iid, fallback_project, FOOTER_MISSING_REASON)
    raw = matches[-1]
    try:
        data: dict[str, object] = json.loads(raw)
        # The footer uses issue_iid; Outcome uses ticket_iid — remap transparently.
        if "issue_iid" in data and "ticket_iid" not in data:
            data["ticket_iid"] = data.pop("issue_iid")
        return Outcome.model_validate(data)
    except (json.JSONDecodeError, ValueError) as exc:
        return _unparseable(fallback_iid, fallback_project, f"{_FOOTER_UNPARSEABLE_PREFIX} {exc}")


def resolve_outcome(stdout: str, fallback_iid: int, fallback_project: str) -> Outcome:
    """Parse the footer, fall back to GitLab state when it is missing/unparseable."""
    outcome = parse_outcome(stdout, fallback_iid, fallback_project)
    if not _is_footer_failure(outcome):
        return outcome
    rescued = _resolve_from_gitlab(fallback_iid, fallback_project, original_reason=outcome.escalation_reason or "")
    return rescued if rescued is not None else outcome


def _is_footer_failure(outcome: Outcome) -> bool:
    if outcome.status != OutcomeStatus.ESCALATED:
        return False
    reason = outcome.escalation_reason or ""
    return reason == FOOTER_MISSING_REASON or reason.startswith(_FOOTER_UNPARSEABLE_PREFIX)


def _resolve_from_gitlab(iid: int, project_path: str, original_reason: str) -> Outcome | None:
    """Query GitLab for the MR linked to this issue and reconstruct the outcome.

    Returns None when GitLab cannot help (network error, no MR at all) so the
    caller keeps the original footer-failure outcome.
    """
    mr = _fetch_related_mr(iid, project_path)
    if mr is None:
        logger.info("[gitlab-fallback] no related MR for #%d on %s", iid, project_path)
        return None

    state = mr.get("state")
    mr_url = mr.get("web_url")
    mr_iid = mr.get("iid")
    base = {
        "ticket_iid": iid,
        "project_path": project_path,
        "mr_url": mr_url,
        "mr_iid": mr_iid,
        "tokens_used": 0,
        "duration_seconds": 0,
    }
    note = "(rescued from GitLab after footer failure)"
    if state == "merged":
        logger.info("[gitlab-fallback] #%d resolved as success via merged MR !%s", iid, mr_iid)
        return Outcome(status=OutcomeStatus.SUCCESS, escalation_reason=None, **base)
    if state == "opened":
        merge_status = mr.get("detailed_merge_status") or mr.get("merge_status") or "unknown"
        reason = f"footer failure; MR !{mr_iid} open ({merge_status}) — manual merge needed {note}"
        return Outcome(status=OutcomeStatus.ESCALATED, escalation_reason=reason, **base)
    # closed without merge (rare for the agent flow, but possible)
    reason = f"footer failure; MR !{mr_iid} closed without merge {note}"
    return Outcome(status=OutcomeStatus.ESCALATED, escalation_reason=reason, **base)


def _fetch_related_mr(iid: int, project_path: str) -> dict[str, Any] | None:
    """Return the most recent MR related to the issue, or None."""
    project = urllib.parse.quote(project_path, safe="")
    mrs = glab_api(f"projects/{project}/issues/{iid}/related_merge_requests")
    if not isinstance(mrs, list) or not mrs:
        if mrs is None:
            logger.warning("[gitlab-fallback] glab call failed for #%d on %s", iid, project_path)
        return None
    mrs.sort(key=lambda m: m.get("created_at", ""), reverse=True)
    return cast(dict[str, Any], mrs[0])


def _unparseable(iid: int, project: str, reason: str) -> Outcome:
    return Outcome(
        ticket_iid=iid,
        project_path=project,
        status=OutcomeStatus.ESCALATED,
        mr_url=None,
        mr_iid=None,
        escalation_reason=reason,
        tokens_used=0,
        duration_seconds=0,
    )
