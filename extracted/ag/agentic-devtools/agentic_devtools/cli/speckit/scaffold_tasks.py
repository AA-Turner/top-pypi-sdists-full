"""Native Python scaffold command for seeding the active feature's tasks.md."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from agentic_devtools.background_tasks import run_function_in_background
from agentic_devtools.state import is_dry_run
from agentic_devtools.task_state import print_task_tracking_info

from .scaffold_common import (
    FEATURE_DIR_PREFIX_RE,
    ActiveFeature,
    FeatureResolutionError,
    get_current_branch,
    get_repo_root,
    has_git_repo,
    resolve_active_feature,
)

PRESET_TEMPLATE_RELATIVE_PATH = Path(".specify") / "presets" / "agdt-templates" / "templates" / "tasks-template.md"

__all__ = [
    "PRESET_TEMPLATE_RELATIVE_PATH",
    "prepare_tasks",
    "resolve_tasks_template",
    "scaffold_tasks_async",
    "scaffold_tasks_command",
]


def _core_fallback_template() -> Path | None:
    """Return the ``specify-cli`` bundled tasks template, if the package is installed."""
    try:
        import specify_cli
    except ImportError:  # pragma: no cover - specify-cli is a pinned dependency
        return None
    candidate = Path(specify_cli.__file__).resolve().parent / "core_pack" / "templates" / "tasks-template.md"
    return candidate if candidate.is_file() else None  # pragma: no cover - bundled template is optional


def resolve_tasks_template(repo_root: Path) -> Path | None:
    """Resolve the template used to seed ``tasks.md`` for the active feature."""
    resolved_repo_root = repo_root.resolve()
    preset_template = repo_root / PRESET_TEMPLATE_RELATIVE_PATH
    if preset_template.is_file():
        resolved_preset_template = preset_template.resolve()
        try:
            resolved_preset_template.relative_to(resolved_repo_root)
        except ValueError:  # pragma: no cover - preset outside repo root falls back to bundled template
            return _core_fallback_template()
        return resolved_preset_template
    return _core_fallback_template()


def prepare_tasks(active: ActiveFeature, *, dry_run: bool = False) -> Path:
    """Ensure the active feature directory exists and seed ``tasks.md`` if missing."""
    resolved_repo_root = active.repo_root.resolve()
    specs_root = (active.repo_root / "specs").resolve()
    try:
        specs_root.relative_to(resolved_repo_root)
    except ValueError as exc:
        raise FeatureResolutionError(
            f"Repository specs directory resolves outside the repository root: {specs_root}"
            f" (repo root: {resolved_repo_root})"
        ) from exc
    resolved_feature_dir = active.feature_dir.resolve()
    try:
        resolved_feature_dir.relative_to(resolved_repo_root)
    except ValueError as exc:
        raise FeatureResolutionError(
            f"Feature directory resolves outside the repository root: {active.feature_dir}"
        ) from exc
    try:
        feature_relative = resolved_feature_dir.relative_to(specs_root)
    except ValueError as exc:
        raise FeatureResolutionError(
            f"Feature directory resolves outside repository specs directory: {resolved_feature_dir}"
        ) from exc
    if feature_relative == Path("."):
        raise FeatureResolutionError(
            f"Feature directory must be a strict descendant of the repository specs directory: {resolved_feature_dir}"
        )
    if active.feature_dir.is_symlink() or (active.feature_dir.exists() and not active.feature_dir.is_dir()):
        raise FeatureResolutionError(
            f"Refusing to scaffold tasks in a symlinked or non-directory feature path: {active.feature_dir}"
        )

    if not dry_run:
        active.feature_dir.mkdir(parents=True, exist_ok=True)

    tasks_path = active.feature_dir / "tasks.md"
    if tasks_path.is_symlink():
        raise FeatureResolutionError(f"Refusing to seed symlinked tasks.md: {tasks_path}")
    if tasks_path.exists() and not tasks_path.is_file():
        raise FeatureResolutionError(f"Refusing to seed non-file tasks.md: {tasks_path}")
    if not dry_run and not tasks_path.exists():
        template = resolve_tasks_template(active.repo_root)
        if template is not None:
            tasks_path.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")
        else:
            tasks_path.touch()  # pragma: no cover - empty fallback file is trivial but kept as a guard
    return tasks_path


def _resolve_active_feature_from_args(spec_dir: str | None) -> ActiveFeature:
    if not spec_dir:
        return resolve_active_feature()
    repo_root = get_repo_root().resolve()
    candidate = Path(spec_dir)
    unresolved = candidate if candidate.is_absolute() else repo_root / candidate
    if unresolved.is_symlink():
        raise FeatureResolutionError(f"--spec-dir must not be a symlink: {unresolved}")
    feature_dir = unresolved.resolve()
    specs_root = repo_root / "specs"
    try:
        feature_dir.relative_to(specs_root)
    except ValueError as exc:
        raise FeatureResolutionError(f"--spec-dir resolves outside repository specs directory: {feature_dir}") from exc
    resolved_feature_dir = feature_dir
    has_git = has_git_repo(repo_root)
    branch = feature_dir.name
    try:
        resolved_active = resolve_active_feature(repo_root)
    except FeatureResolutionError:
        resolved_active = None
    if resolved_active and resolved_active.feature_dir.resolve() == resolved_feature_dir:
        branch = resolved_active.branch
    elif has_git:
        current_branch = get_current_branch(repo_root)
        if current_branch:
            branch_match = FEATURE_DIR_PREFIX_RE.match(current_branch)
            dir_match = FEATURE_DIR_PREFIX_RE.match(feature_dir.name)
            if branch_match and dir_match and int(branch_match.group(1)) == int(dir_match.group(1)):
                branch = current_branch
    return ActiveFeature(repo_root=repo_root, feature_dir=feature_dir, branch=branch, has_git=has_git)


def _resolve_spec_context(
    active: ActiveFeature, hierarchy_level: str, spec_context: str | None
) -> tuple[Path, Path] | None:
    """Return ``(spec_path, plan_path)`` for task-level scaffolding, or ``None`` for other levels.

    Both the parent ``spec.md`` and ``plan.md`` are required for task-level scaffolding.
    """
    if hierarchy_level != "task":
        return None
    if spec_context:
        candidate = Path(spec_context)
        context_dir = (candidate if candidate.is_absolute() else active.repo_root / candidate).resolve()
        resolved_repo_root = active.repo_root.resolve()
        specs_root = (active.repo_root / "specs").resolve()
        try:
            specs_root.relative_to(resolved_repo_root)
        except ValueError as exc:
            raise FeatureResolutionError(
                f"Repository specs directory resolves outside the repository root: {specs_root}"
                f" (repo root: {resolved_repo_root})"
            ) from exc
        try:
            context_dir.relative_to(specs_root)
        except ValueError as exc:
            raise FeatureResolutionError(
                f"--spec-context resolves outside repository specs directory: {context_dir}"
            ) from exc
        if context_dir == specs_root:
            raise FeatureResolutionError(
                f"--spec-context must point to a directory below repository specs directory: {context_dir}"
            )
        resolved_spec = context_dir / "spec.md"
        resolved_plan = context_dir / "plan.md"
    else:
        parent_dir = (active.feature_dir.parent).resolve()
        specs_root = (active.repo_root / "specs").resolve()
        try:
            parent_dir.relative_to(specs_root)
        except ValueError as exc:
            raise FeatureResolutionError(
                f"Inferred spec-context resolves outside repository specs directory: {parent_dir}"
            ) from exc
        if parent_dir == specs_root:
            raise FeatureResolutionError(
                "Task-level scaffolding requires a nested feature spec; "
                f"the active feature has no parent spec directory below {specs_root}"
            )
        resolved_spec = parent_dir / "spec.md"
        resolved_plan = parent_dir / "plan.md"
    if resolved_spec.is_symlink() or not resolved_spec.is_file():
        raise FeatureResolutionError(
            f"Task-level scaffolding requires a regular, non-symlinked parent spec.md: {resolved_spec}"
        )
    if resolved_plan.is_symlink() or not resolved_plan.is_file():
        raise FeatureResolutionError(
            f"Task-level scaffolding requires a regular, non-symlinked parent plan.md: {resolved_plan}"
        )
    return resolved_spec, resolved_plan


def scaffold_tasks_async(_argv: list[str] | None = None) -> None:
    """Background wrapper for ``agdt-speckit-scaffold-tasks``."""
    argv = list(sys.argv[1:] if _argv is None else _argv)
    task = run_function_in_background(
        module_path="agentic_devtools.cli.speckit.scaffold_tasks",
        function_name="scaffold_tasks_command",
        command_display_name="agdt-speckit-scaffold-tasks",
        func_kwargs={"argv": argv},
    )
    print_task_tracking_info(task)


def scaffold_tasks_command(argv: list[str] | None = None) -> None:
    """CLI entry point for ``agdt-speckit-scaffold-tasks``."""
    parser = argparse.ArgumentParser(
        prog="agdt-speckit-scaffold-tasks",
        description="Scaffold the active SpecKit feature's tasks.md and report resolved paths.",
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        default=False,
        help="Output results in JSON format",
    )
    parser.add_argument("--spec-dir", default=None, help="Optional feature spec directory path")
    parser.add_argument(
        "--hierarchy-level",
        choices=("epic", "feature", "task"),
        default="feature",
        help="Hierarchy level to scaffold for (epic, feature, or task)",
    )
    parser.add_argument(
        "--spec-context",
        default=None,
        help="Optional parent spec directory path for task-level scaffolding",
    )
    args = parser.parse_args(argv)

    if args.spec_context and args.hierarchy_level != "task":
        print(
            f"ERROR: --spec-context is only valid with --hierarchy-level=task (got '{args.hierarchy_level}')",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        active = _resolve_active_feature_from_args(args.spec_dir)
        dry_run = is_dry_run()
        plan_path = active.feature_dir / "plan.md"
        if args.hierarchy_level == "feature" and (plan_path.is_symlink() or not plan_path.is_file()):
            raise FeatureResolutionError(
                f"Feature-level scaffolding requires a regular, non-symlinked plan.md: {plan_path}"
            )
        spec_context_result = _resolve_spec_context(active, args.hierarchy_level, args.spec_context)
        tasks_path = prepare_tasks(active, dry_run=dry_run)
    except FeatureResolutionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    spec_context: Path | None = None
    plan_context: Path | None = None
    if spec_context_result is not None:
        spec_context, plan_context = spec_context_result

    if args.json_output:
        payload: dict[str, str | bool] = {
            "FEATURE_DIR": str(active.feature_dir),
            "TASKS_FILE": str(tasks_path),
            "SPECS_DIR": str(active.feature_dir),
            "BRANCH": active.branch,
            "HIERARCHY_LEVEL": args.hierarchy_level,
        }
        if spec_context is not None:
            payload["SPEC_CONTEXT"] = str(spec_context)
        if plan_context is not None:
            payload["PARENT_PLAN_CONTEXT"] = str(plan_context)
        if dry_run:
            payload["DRY_RUN"] = True
        print(json.dumps(payload))
    else:
        if dry_run:  # pragma: no cover - smoke tests cover the dry-run branch by direct function use
            print(
                f"[DRY RUN] Would scaffold tasks — no files created or modified.\n"
                f"FEATURE_DIR: {active.feature_dir}\n"
                f"TASKS_FILE: {tasks_path}\n"
                f"SPECS_DIR: {active.feature_dir}\n"
                f"BRANCH: {active.branch}\n"
                f"HIERARCHY_LEVEL: {args.hierarchy_level}"
            )
            if spec_context is not None:
                print(f"SPEC_CONTEXT: {spec_context}")
            if plan_context is not None:
                print(f"PARENT_PLAN_CONTEXT: {plan_context}")
        else:
            print(
                f"FEATURE_DIR: {active.feature_dir}"
            )  # pragma: no cover - printable output is intentionally excluded from file coverage
            print(f"TASKS_FILE: {tasks_path}")  # pragma: no cover
            print(f"SPECS_DIR: {active.feature_dir}")  # pragma: no cover
            print(f"BRANCH: {active.branch}")  # pragma: no cover
            print(f"HIERARCHY_LEVEL: {args.hierarchy_level}")  # pragma: no cover
            if spec_context is not None:  # pragma: no cover
                print(f"SPEC_CONTEXT: {spec_context}")
            if plan_context is not None:  # pragma: no cover
                print(f"PARENT_PLAN_CONTEXT: {plan_context}")
