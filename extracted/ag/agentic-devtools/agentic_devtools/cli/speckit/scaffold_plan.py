"""
Native Python scaffold command for the SpecKit planning phase.

Replaces the legacy ``.specify/scripts/bash/setup-plan.sh`` script: creates
the active feature's ``specs/<feature-dir>/`` directory (if needed), seeds
``plan.md`` from the repository's plan template (or the ``specify-cli``
core-pack fallback template), and reports the resolved paths.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from agentic_devtools.background_tasks import run_function_in_background
from agentic_devtools.state import is_dry_run
from agentic_devtools.task_state import print_task_tracking_info

from .scaffold_common import ActiveFeature, FeatureResolutionError, resolve_active_feature

#: Repo-local plan template, relative to the repository root.
PRESET_TEMPLATE_RELATIVE_PATH = Path(".specify") / "presets" / "agdt-templates" / "templates" / "plan-template.md"

__all__ = [
    "PRESET_TEMPLATE_RELATIVE_PATH",
    "prepare_plan",
    "scaffold_plan_async",
    "scaffold_plan_command",
]


def _core_fallback_template() -> Path | None:
    """Return the ``specify-cli`` bundled plan template, if the package is installed."""
    try:
        import specify_cli
    except ImportError:  # pragma: no cover - specify-cli is a pinned dependency
        return None
    candidate = Path(specify_cli.__file__).resolve().parent / "core_pack" / "templates" / "plan-template.md"
    return candidate if candidate.is_file() else None


def resolve_plan_template(repo_root: Path) -> Path | None:
    """
    Resolve the plan template to seed ``plan.md`` from.

    Args:
        repo_root: Repository root to look for the repo-local preset template in.

    Returns:
        The repo-local preset template path if it exists, otherwise the
        ``specify-cli`` core-pack fallback template path, otherwise None if
        neither is available.
    """
    resolved_repo_root = repo_root.resolve()
    preset_template = repo_root / PRESET_TEMPLATE_RELATIVE_PATH
    if preset_template.is_file():
        resolved_preset_template = preset_template.resolve()
        try:
            resolved_preset_template.relative_to(resolved_repo_root)
        except ValueError:
            return _core_fallback_template()
        return resolved_preset_template
    return _core_fallback_template()


def prepare_plan(active: ActiveFeature, *, dry_run: bool = False) -> Path:
    """
    Ensure the active feature directory exists and seed ``plan.md``.

    Args:
        active: Resolved active feature context.
        dry_run: When ``True``, skip all filesystem mutations (``mkdir``,
            ``write_text``, ``touch``) and return the *predicted* plan path
            without creating it.  Safety checks (symlink guards, path-escape
            guard) still run so that dry-run output is accurate.

    Returns:
        Path to the prepared (or predicted) ``plan.md`` file. Existing content
        is left untouched; only a missing ``plan.md`` is seeded from the
        template.  In dry-run mode the path is returned even if it does not
        exist on disk yet.

    Raises:
        FeatureResolutionError: If the resolved feature directory escapes the
            repository root or if ``plan.md`` is a symlink.
    """
    try:
        active.feature_dir.resolve().relative_to(active.repo_root.resolve())
    except ValueError as exc:
        raise FeatureResolutionError(
            f"Feature directory resolves outside the repository root: {active.feature_dir}"
        ) from exc
    # In a live run, create the directory first so that the symlink and
    # non-file guards below can evaluate against the real filesystem state
    # (matching the original ordering).  In dry-run mode the directory is
    # not created, but the guards still run against whatever is already
    # present on disk.
    if not dry_run:
        active.feature_dir.mkdir(parents=True, exist_ok=True)
    impl_plan = active.feature_dir / "plan.md"
    if impl_plan.is_symlink():
        raise FeatureResolutionError(f"Refusing to seed symlinked plan.md: {impl_plan}")
    if impl_plan.exists() and not impl_plan.is_file():
        raise FeatureResolutionError(f"Refusing to seed non-file plan.md: {impl_plan}")
    if not dry_run:
        if not impl_plan.exists():
            template = resolve_plan_template(active.repo_root)
            if template is not None:
                impl_plan.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")
            else:
                impl_plan.touch()
    return impl_plan


def scaffold_plan_async(_argv: list[str] | None = None) -> None:
    """Background wrapper for ``agdt-speckit-scaffold-plan``."""
    argv = list(sys.argv[1:] if _argv is None else _argv)
    task = run_function_in_background(
        module_path="agentic_devtools.cli.speckit.scaffold_plan",
        function_name="scaffold_plan_command",
        command_display_name="agdt-speckit-scaffold-plan",
        func_kwargs={"argv": argv},
    )
    print_task_tracking_info(task)


def scaffold_plan_command(argv: list[str] | None = None) -> None:
    """CLI entry point for ``agdt-speckit-scaffold-plan``."""
    parser = argparse.ArgumentParser(
        prog="agdt-speckit-scaffold-plan",
        description="Scaffold the active SpecKit feature's plan.md and report resolved paths.",
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        default=False,
        help="Output results in JSON format",
    )
    args = parser.parse_args(argv)

    try:
        active = resolve_active_feature()
        dry_run = is_dry_run()
        impl_plan = prepare_plan(active, dry_run=dry_run)
    except FeatureResolutionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.json_output:
        print(
            json.dumps(
                {
                    "FEATURE_DIR": str(active.feature_dir),
                    "IMPL_PLAN": str(impl_plan),
                    "SPECS_DIR": str(active.feature_dir),
                    "BRANCH": active.branch,
                    **({"DRY_RUN": True} if dry_run else {}),
                }
            )
        )
    else:
        if dry_run:
            print(
                f"[DRY RUN] Would scaffold plan — no files created or modified.\n"
                f"FEATURE_DIR: {active.feature_dir}\n"
                f"IMPL_PLAN: {impl_plan}\n"
                f"SPECS_DIR: {active.feature_dir}\n"
                f"BRANCH: {active.branch}"
            )
        else:
            print(f"FEATURE_DIR: {active.feature_dir}")
            print(f"IMPL_PLAN: {impl_plan}")
            print(f"SPECS_DIR: {active.feature_dir}")
            print(f"BRANCH: {active.branch}")
