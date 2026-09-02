"""SK-R15 — startup-time validator for skill→tool references.

Every active ``skill.definition.allowed_tools`` entry must resolve to a real
``tool_def`` row. A dangling reference is a configuration bug; we crash
boot loud rather than discover it mid-request.

Pairs with ``aidream/startup/tools_check.py`` — same shape, same exit code.
Called from ``aidream.api.app`` startup alongside the tool validator.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID

from matrx_utils import vcprint


class SkillValidationError(Exception):
    """Raised when ``skill.definition.allowed_tools`` references a missing
    or inactive ``tool_def`` row.

    The host passes ``strict=`` to :func:`validate_allowed_tools_on_startup`
    (aidream derives it from ``runtime_env.strict_startup_gates`` — fail boot on
    a real deployment, warn on a laptop / test run).
    """


async def validate_allowed_tools_on_startup(*, strict: bool = True) -> dict[str, Any]:
    """Walk every active skill, verify every ``allowed_tools`` UUID resolves.

    Returns a dict with ``skills_checked``, ``references_checked``,
    ``missing`` (list of ``{skill_id, missing_tool_id}`` dicts). When
    ``strict=True`` and ``missing`` is non-empty, raises
    ``SkillValidationError``.
    """
    report: dict[str, Any] = {
        "skills_checked": 0,
        "references_checked": 0,
        "missing": [],
        "invalid_uuid": [],
    }

    # Lazy resolution through the registry so the validator can be imported
    # anywhere without crashing the package's bare import path — and never
    # reaches for the aidream tree.
    try:
        from matrx_ai.db._registry import get_instance
        from matrx_ai.tools.tool_def_db import get_tool_def_manager

        defs_mgr = get_instance("skl_definitions_manager")
        tool_mgr = get_tool_def_manager()
    except Exception as exc:
        # The managers aren't wired — most likely a context that hasn't run
        # the host's configure(). Log loudly and continue; the live
        # system-prompt path will surface its own error if actually used.
        vcprint(
            f"[skills.startup_check] manager resolution failed ({exc!r}); skipping validation",
            color="yellow",
        )
        return report

    skills = await defs_mgr.filter_items(is_active=True)
    report["skills_checked"] = len(skills)

    # Pre-load the active tool UUID set once so we don't N+1 the DB.
    active_tools = await tool_mgr.filter_items(is_active=True)
    active_tool_ids = {UUID(str(t.id)) for t in active_tools}

    for skill in skills:
        raw = getattr(skill, "allowed_tools", None) or []
        if not isinstance(raw, list):
            continue
        skill_id_display = getattr(skill, "skill_id", None) or str(skill.id)

        for entry in raw:
            report["references_checked"] += 1
            if isinstance(entry, UUID):
                tool_uuid = entry
            elif isinstance(entry, str):
                try:
                    tool_uuid = UUID(entry)
                except ValueError:
                    report["invalid_uuid"].append({"skill_id": skill_id_display, "value": entry})
                    continue
            else:
                report["invalid_uuid"].append({"skill_id": skill_id_display, "value": repr(entry)})
                continue

            if tool_uuid not in active_tool_ids:
                report["missing"].append(
                    {
                        "skill_id": skill_id_display,
                        "missing_tool_id": str(tool_uuid),
                    }
                )

    if report["missing"] or report["invalid_uuid"]:
        details = {
            "missing": report["missing"],
            "invalid_uuid": report["invalid_uuid"],
        }
        msg = (
            f"[skills.startup_check] {len(report['missing'])} missing tool reference(s), "
            f"{len(report['invalid_uuid'])} invalid UUID(s) across {report['skills_checked']} skill(s). "
            "Fix the skill.definition.allowed_tools entries or deactivate the affected skills."
        )
        vcprint(details, msg, color="red")
        if strict:
            raise SkillValidationError(msg)
    # Verified — silent on success; only a missing/invalid reference (red) speaks.

    return report
