"""Parse the DESIGN_RESULT footer emitted by a headless `/design-generate` run.

Mirror of ``agent.outcome`` but for the design lane: there is no MR/merge, the
artifact is a GitLab Pages preview URL. Reuses the shared ``Outcome`` model
(``mr_*`` stay None, ``preview_url`` carries the proto link).
"""

import json
import re

from ..models import Outcome, OutcomeStatus

_FOOTER_RE = re.compile(r"<<<DESIGN_RESULT\s*(.*?)\s*DESIGN_RESULT>>>", re.DOTALL)

FOOTER_MISSING_REASON = "DESIGN_RESULT footer missing"
_UNPARSEABLE_PREFIX = "footer unparseable:"


def _escalated(iid: int, project: str, reason: str) -> Outcome:
    return Outcome(
        ticket_iid=iid,
        project_path=project,
        status=OutcomeStatus.ESCALATED,
        mr_url=None,
        mr_iid=None,
        escalation_reason=reason,
    )


def resolve_design_outcome(stdout: str, fallback_iid: int, fallback_project: str) -> Outcome:
    """Parse the last DESIGN_RESULT footer. Missing/unparseable → escalated."""
    matches = _FOOTER_RE.findall(stdout)
    if not matches:
        return _escalated(fallback_iid, fallback_project, FOOTER_MISSING_REASON)
    try:
        data: dict[str, object] = json.loads(matches[-1])
    except (json.JSONDecodeError, ValueError) as exc:
        return _escalated(fallback_iid, fallback_project, f"{_UNPARSEABLE_PREFIX} {exc}")

    status = str(data.get("status", "")).strip().lower()
    if status == "success":
        return Outcome(
            ticket_iid=fallback_iid,
            project_path=fallback_project,
            status=OutcomeStatus.SUCCESS,
            mr_url=None,
            mr_iid=None,
            escalation_reason=None,
            preview_url=str(data.get("preview_url", "") or ""),
        )
    reason = str(data.get("reason", "") or "").strip() or "design escalated (no reason given)"
    return _escalated(fallback_iid, fallback_project, reason[:300])
