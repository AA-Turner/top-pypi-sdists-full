"""GitLab side-effects for the AC gate.

Pure builders (testable) + thin glab CLI wrappers (mocked in tests).
"""

import json
from collections.abc import Sequence
from datetime import datetime, timedelta, timezone
from typing import Any

from ...common.glab.runner import run_glab
from ...common.references.gitlab_labels import DEFAULT_BOARD_LABEL
from .models import (
    CheckboxViolation,
    LLMReview,
    ReadyCheckResult,
    SectionViolation,
    Violation,
)

READY_CHECK_MARKER = "<!-- pysae-ai-tools:ready-check -->"
SUGGESTION_MARKER = "<!-- pysae-ai-tools:ac-quality-suggestion -->"


def _format_violation(v: Violation) -> str:
    if isinstance(v, SectionViolation):
        return f"- Section `{v.section}` : {v.reason}"
    if isinstance(v, CheckboxViolation):
        return f'- Checkbox "{v.checkbox}" : {v.reason}'
    return f"- {v}"


def build_failure_comment(
    violations: Sequence[Violation],
    author_username: str | None,
    tool_version: str,
) -> str:
    mention = f"@{author_username}" if author_username else "L'auteur du ticket"
    bullets = "\n".join(_format_violation(v) for v in violations)
    return (
        "🚧 **L'autopilot a tenté de prendre en charge ce ticket, mais les "
        "prérequis ne sont pas réunis.**\n\n"
        "**Violations détectées** :\n"
        f"{bullets}\n\n"
        f"{mention} merci de compléter le ticket et de recocher les cases "
        '"Préparation au développement" correspondantes. Une fois prêt, '
        "retire le label `agent::needs-spec` et remets `agent::ready` pour "
        "relancer l'autopilot.\n\n"
        f"_Check exécuté par `pysae-ai-tools glab issue ready-check`, version `{tool_version}`._\n"
        f"\n{READY_CHECK_MARKER}\n"
    )


def build_suggestion_comment(review: LLMReview) -> str:
    missing = "\n".join(f"- {item}" for item in review.missing_aspects) or "- (aucun)"
    suggestions = "\n".join(f"- {item}" for item in review.suggestions) or "- (aucune)"
    return (
        f"💡 **L'autopilot a évalué la qualité des critères d'acceptation à {review.quality_score}/5.**\n\n"
        "**Aspects qui pourraient manquer** :\n"
        f"{missing}\n\n"
        "**Suggestions** :\n"
        f"{suggestions}\n\n"
        "L'implémentation va démarrer malgré tout. Si tu veux affiner les AC avant, "
        "ajoute le label `agent::needs-spec` pour mettre en pause.\n"
        f"\n{SUGGESTION_MARKER}\n"
    )


def find_recent_bot_comment(
    notes: Sequence[dict[str, Any]],
    marker: str,
    window_hours: int,
    now: str | None = None,
) -> int | None:
    now_iso = now or datetime.now(timezone.utc).isoformat()
    now_dt = datetime.fromisoformat(now_iso.replace("Z", "+00:00"))
    cutoff = now_dt - timedelta(hours=window_hours)
    for note in notes:
        body = note.get("body") or ""
        if marker not in body:
            continue
        created = note.get("created_at")
        if not created:
            continue
        created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
        if created_dt >= cutoff:
            return int(note["id"])
    return None


def _glab(*args: str, timeout: int = 30) -> str:
    res = run_glab(*args, timeout=timeout)
    if not res.ok:
        raise RuntimeError(f"glab {' '.join(args[:2])} failed (exit {res.returncode}): {res.stderr}")
    return res.stdout


def apply_failure_actions(
    project_path: str,
    issue_iid: int,
    result: ReadyCheckResult,
    author_username: str | None,
    tool_version: str,
) -> list[str]:
    applied: list[str] = []
    encoded = project_path.replace("/", "%2F")
    notes_raw = _glab(
        "api",
        f"projects/{encoded}/issues/{issue_iid}/notes?per_page=50&order_by=created_at&sort=desc",
    )
    notes = json.loads(notes_raw) if notes_raw else []
    if find_recent_bot_comment(notes, READY_CHECK_MARKER, window_hours=24) is not None:
        applied.append("comment-skipped-dedup")
    else:
        body = build_failure_comment(
            violations=result.violations,
            author_username=author_username,
            tool_version=tool_version,
        )
        _glab("issue", "note", str(issue_iid), "--message", body, "-R", project_path)
        applied.append("commented")

    _glab("issue", "update", str(issue_iid), "--unlabel", "agent::ready", "-R", project_path)
    applied.append("removed:agent::ready")
    _glab(
        "issue",
        "update",
        str(issue_iid),
        "--label",
        f"agent::needs-spec,{DEFAULT_BOARD_LABEL}",
        "-R",
        project_path,
    )
    applied.append("added:agent::needs-spec")
    applied.append(f"added:{DEFAULT_BOARD_LABEL}")
    return applied


def apply_suggestion_comment(
    project_path: str,
    issue_iid: int,
    review: LLMReview,
) -> list[str]:
    encoded = project_path.replace("/", "%2F")
    notes_raw = _glab(
        "api",
        f"projects/{encoded}/issues/{issue_iid}/notes?per_page=50&order_by=created_at&sort=desc",
    )
    notes = json.loads(notes_raw) if notes_raw else []
    if find_recent_bot_comment(notes, SUGGESTION_MARKER, window_hours=24) is not None:
        return ["suggestion-skipped-dedup"]
    body = build_suggestion_comment(review)
    _glab("issue", "note", str(issue_iid), "--message", body, "-R", project_path)
    return ["suggestion-commented"]
