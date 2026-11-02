"""Mirror bundled agent/prompt/skill files into a target repository.

Three kinds are mirrored:

* ``agents`` and ``prompts`` are flattened into the target's ``.github`` tree.
* ``skills`` retain their directory structure under ``.agents/skills``.

Each target directory carries a managed ``agdt.README.md`` manifest.
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

from agentic_devtools.config import VALID_CODE_HOSTING, VALID_ISSUE_ADAPTERS
from agentic_devtools.skill_injector_execution import _execute_plan
from agentic_devtools.skill_injector_markdown import _format_plans
from agentic_devtools.skill_injector_models import InjectionPlan, InjectionSummary
from agentic_devtools.skill_injector_paths import (
    _KINDS,
    _SKILLS_KIND,
    _get_source_dir,
    _target_dir,
)
from agentic_devtools.skill_injector_planning import _normalize_platform_arg, _plan_skills_kind
from agentic_devtools.skill_injector_prepare_flat import _prepare_flat_kind
from agentic_devtools.skill_injector_prepare_skills import _prepare_skills_kind
from agentic_devtools.skill_injector_repo import _is_self_repo


def inject_skills_with_summary(
    git_root: Path | None,
    *,
    issue_adapter: str | None = None,
    code_hosting: str | None = None,
    dry_run: bool = False,
    assume_yes: bool = False,
) -> tuple[bool, InjectionSummary]:
    """Mirror bundled agent/prompt/skill files into the target repo.

    Places files directly into ``{git_root}/.github/agents/`` and
    ``{git_root}/.github/prompts/`` (flat layout), copying all relevant
    ``.md`` files and generating a managed ``agdt.README.md`` manifest in
    each.  Files from source subdirectories are flattened by encoding the
    directory name into the filename.

    The ``skills`` kind is mirrored differently: each skill directory under the
    packaged ``.agents/skills/`` tree is copied verbatim into
    ``{git_root}/.agents/skills/``, carrying its ``SKILL.md`` and its one-level
    deep resources.  Skill names are never flattened.

    A planning phase runs first and computes, per kind, the files that would be
    added, overwritten with different bytes, and deleted by stale cleanup.  The
    resulting manifest diff is printed on every run — including the executed
    one — so the operation is auditable after the fact.

    As a one-time migration, any old ``.agdt/`` subdirectories/symlinks inside
    the target kind directories are removed.  That migration is represented in
    the manifest diff as ``.agdt/`` and runs only when execution proceeds.

    When *git_root* is the agentic-devtools repository itself (see
    :func:`_is_self_repo`) the whole operation is skipped — nothing is copied
    or deleted — because those directories are tracked source there.

    Args:
        git_root: Repository/worktree root.  When ``None`` (not in a git
            repo) no files are written and the function returns ``False``.
        issue_adapter: Resolved issue adapter for the target repo (e.g.
            ``"jira"``, ``"github"``).  When ``None``, empty, whitespace-only,
            or an unrecognised value, the issue-adapter axis is unrestricted
            (all files pass).  Unrecognised values emit a :class:`RuntimeWarning`.
        code_hosting: Resolved code hosting platform for the target repo
            (e.g. ``"github"``, ``"azure_devops"``).  When ``None``, empty,
            whitespace-only, or an unrecognised value, the code-hosting axis is
            unrestricted (all files pass).  Unrecognised values emit a
            :class:`RuntimeWarning`.
        dry_run: When ``True``, print the manifest diff and return without
            writing, copying or unlinking anything (not even the target
            directories or the ``agdt.README.md`` manifests).
        assume_yes: Explicit opt-in required before any planned deletion is
            executed.  When deletions are pending and this is ``False``, the
            delete list is
            printed, nothing is executed for any kind, and the returned
            summary carries ``deletions_blocked=True``.  Ignored under
            *dry_run*, which never deletes anything anyway.

    Returns:
        A ``(success, summary)`` tuple.  ``success`` is ``True`` when all three
        kinds (agents/prompts/skills) were injected successfully, and ``False``
        when:
        - ``git_root`` is ``None``,
        - a source directory for a required kind cannot be resolved,
        - a shared skill resource collides with a consumer-authored file,
        - deletions are pending without *assume_yes*,
        - a ``UnicodeDecodeError`` occurs while reading source files (non-UTF8
          content), or
        - an ``OSError`` occurs while writing mirrored files or manifests.
        ``summary`` is an :class:`InjectionSummary` carrying best-effort counts
        of injected and pruned files (populated even on the ``OSError`` path)
        plus the per-kind manifest diff.
        When *git_root* is the agentic-devtools repository itself the result is
        ``(True, InjectionSummary(0, 0))`` and a :class:`RuntimeWarning` is
        emitted.
    """
    if git_root is None:
        return False, InjectionSummary(injected=0, pruned=0)

    if _is_self_repo(git_root):
        # The agentic-devtools repository is the *source* of these files:
        # ``.github/agents/`` and ``.github/prompts/`` are tracked source that
        # is force-included into the wheel.  Injecting here would delete every
        # classification-filtered file via stale cleanup and (under a wheel
        # install) overwrite the survivors with released content.  Skip
        # entirely and report success so callers do not surface a failure.
        warnings.warn(
            "agentic-devtools: skipping skill injection — the target repository "
            "is the agentic-devtools repository itself, where .github/agents/ and "
            ".github/prompts/ are tracked source rather than injected output.",
            RuntimeWarning,
        )
        return True, InjectionSummary(injected=0, pruned=0)

    injected_total = 0
    pruned_total = 0

    def record_counts(injected: int, pruned: int) -> None:
        nonlocal injected_total, pruned_total
        injected_total += injected
        pruned_total += pruned

    # Normalize both axes: strip whitespace; treat empty strings and
    # unrecognised values as None (unresolved / inject-all for that axis).
    issue_adapter = _normalize_platform_arg(issue_adapter, "issue_adapter", VALID_ISSUE_ADAPTERS)
    code_hosting = _normalize_platform_arg(code_hosting, "code_hosting", VALID_CODE_HOSTING)

    try:
        overall_success = True
        plans: list[InjectionPlan] = []
        plans_tuple: tuple[InjectionPlan, ...] = ()
        shared_resource_collision = False
        # Plan each kind before any target file is mutated.
        pending: list[tuple[InjectionPlan, Path, dict[str, Path], dict[Path, dict[str, object]]]] = []
        for kind in _KINDS:
            source_dir = _get_source_dir(kind)
            if source_dir is None:
                overall_success = False
                continue
            target_dir = _target_dir(git_root, kind)
            if kind == _SKILLS_KIND:
                plan, origins, fm_cache, _, _, collision = _prepare_skills_kind(
                    source_dir,
                    target_dir,
                    issue_adapter=issue_adapter,
                    code_hosting=code_hosting,
                    plan_skills_kind=_plan_skills_kind,
                    on_counts=record_counts,
                )
                shared_resource_collision |= collision
                if collision:
                    overall_success = False
            else:
                plan, origins, fm_cache, _ = _prepare_flat_kind(
                    kind,
                    source_dir,
                    target_dir,
                    issue_adapter=issue_adapter,
                    code_hosting=code_hosting,
                    on_counts=record_counts,
                )
            plans.append(plan)
            pending.append((plan, target_dir, origins, fm_cache))

        plans_tuple = tuple(plans)
        if plans_tuple:
            print(_format_plans(plans_tuple))

        if dry_run:
            # Nothing has been written, copied or unlinked up to this point.
            return overall_success, InjectionSummary(
                injected=injected_total,
                pruned=pruned_total,
                plans=plans_tuple,
            )

        if shared_resource_collision:
            return False, InjectionSummary(
                injected=injected_total,
                pruned=pruned_total,
                plans=plans_tuple,
            )

        pending_deletions = sum(len(plan.deleted) for plan in plans_tuple)
        if pending_deletions and not assume_yes:
            print(
                f"agentic-devtools: refusing to delete {pending_deletions} managed skill entries "
                "without confirmation — re-run with assume_yes=True (`agdt-setup --yes`) to allow "
                "deletions, or dry_run=True (`agdt-setup --dry-run`) to preview the manifest diff. "
                "Nothing was changed.",
                file=sys.stderr,
            )
            for plan in plans_tuple:
                if not plan.deleted:
                    continue
                print(f"  {plan.kind} deletes ({len(plan.deleted)}):", file=sys.stderr)
                for name in plan.deleted:
                    print(f"    - {name}", file=sys.stderr)
            return False, InjectionSummary(
                injected=injected_total,
                pruned=pruned_total,
                plans=plans_tuple,
                deletions_blocked=True,
            )

        # Execute one planned kind at a time; a failed kind does not prevent later kinds.
        for plan, target_dir, origins, fm_cache in pending:
            kind_success = _execute_plan(plan, target_dir, origins, fm_cache)
            overall_success = kind_success and overall_success

        return overall_success, InjectionSummary(
            injected=injected_total,
            pruned=pruned_total,
            plans=plans_tuple,
        )
    except OSError:
        return False, InjectionSummary(
            injected=injected_total,
            pruned=pruned_total,
            plans=plans_tuple or tuple(plans),
        )


def inject_skills(
    git_root: Path | None,
    *,
    issue_adapter: str | None = None,
    code_hosting: str | None = None,
    dry_run: bool = False,
    assume_yes: bool = False,
) -> bool:
    """Mirror bundled agent/prompt/skill files into the target repo (bool wrapper).

    Thin backward-compatible wrapper around
    :func:`inject_skills_with_summary` that discards the
    :class:`InjectionSummary` and returns only the success flag.  See
    :func:`inject_skills_with_summary` for full argument and behavior details.

    Returns:
        ``True`` when all three kinds (agents/prompts/skills) were injected
        successfully,
        ``False`` otherwise (see :func:`inject_skills_with_summary`) — including
        when pending deletions were blocked for want of *assume_yes*.
    """
    success, _summary = inject_skills_with_summary(
        git_root,
        issue_adapter=issue_adapter,
        code_hosting=code_hosting,
        dry_run=dry_run,
        assume_yes=assume_yes,
    )
    return success
