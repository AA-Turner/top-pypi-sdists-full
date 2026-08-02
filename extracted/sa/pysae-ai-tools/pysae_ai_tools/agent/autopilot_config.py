"""Resolve a repo's :class:`Autopilot` config for the batch commands.

Every batch knob (max tickets, success floor, completeness audit, deploy-watch jobs
and tuning) has a per-repo value in ``.pysae-ai-tools.yaml`` under ``autopilot``; the
CLI flags override it. This helper is the single, best-effort resolution point shared
by ``rank``, ``watch-deploy`` and the headless ``run`` pipeline: a missing config or a
load failure yields the schema defaults (never a crash, never a false escalation).
"""

import logging

from ..common.project_config import Autopilot, load_project_config_for

logger = logging.getLogger(__name__)


def load_autopilot(project: str | None) -> Autopilot:
    """The ``autopilot`` config block for ``project`` (schema defaults when unresolved).

    Best-effort: any load failure (unreachable GitLab, missing/malformed config, network
    blip) falls back to the schema defaults — resolving batch tuning must never crash a run.
    """
    if not project:
        return Autopilot()
    try:
        config = load_project_config_for(project)
    except Exception as exc:  # noqa: BLE001 — best-effort; defaults must always win over a crash
        logger.warning("cannot load autopilot config for %s; using defaults: %s", project, exc)
        return Autopilot()
    return config.autopilot if config else Autopilot()


# Sentinel for "verify the whole CI" (as opposed to an explicit — possibly empty — job list).
ALL_CI_JOBS = None


def resolve_ci_selection(value: list[str] | bool | None) -> list[str] | None:
    """Normalise a ``*_ci_jobs`` value to either ``None`` (= all CI) or an explicit list.

    ``None`` / ``True`` → all CI ; ``False`` → nothing (``[]``) ; a list → exactly those
    jobs (an empty list is also "nothing", but ``False`` is the explicit spelling).
    """
    if value is None or value is True:
        return None
    if value is False:
        return []
    return list(value)


def merge_ci_selections(a: list[str] | bool | None, b: list[str] | bool | None) -> list[str] | None:
    """Union of two selections (for ``--ci-at-end``). ``None`` (all) on either side wins."""
    ra, rb = resolve_ci_selection(a), resolve_ci_selection(b)
    if ra is None or rb is None:
        return None
    return sorted(set(ra) | set(rb))
