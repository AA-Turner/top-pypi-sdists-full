"""
Native Python scaffold command for checking SpecKit workflow prerequisites.

Replaces the legacy ``.specify/scripts/bash/check-prerequisites.sh`` script:
resolves the active feature directory, validates that the required planning
documents exist, and reports which optional planning documents are available.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

from agentic_devtools.background_tasks import run_function_in_background
from agentic_devtools.task_state import print_task_tracking_info

from .scaffold_common import FeatureResolutionError, resolve_active_feature

#: Optional planning documents evaluated, in the order they are reported.
_OPTIONAL_DOC_NAMES = ("spec.md", "research.md", "data-model.md", "quickstart.md")
_CONTRACTS_DIR_NAME = "contracts"
_TASKS_DOC_NAME = "tasks.md"
_PLAN_DOC_NAME = "plan.md"

__all__ = [
    "PrereqCheckResult",
    "check_prerequisites",
    "scaffold_check_prereqs_async",
    "scaffold_check_prereqs_command",
]


@dataclass(frozen=True)
class PrereqCheckResult:
    """Outcome of a SpecKit prerequisite check.

    Attributes:
        feature_dir: The active feature's ``specs/`` directory.
        available_docs: Names of the optional planning documents/directories
            found to be present (``"contracts/"`` uses a trailing slash).
    """

    feature_dir: Path
    available_docs: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        """Return the JSON-serialisable representation of this result."""
        return {"FEATURE_DIR": str(self.feature_dir), "AVAILABLE_DOCS": list(self.available_docs)}


def _reject_symlinked_artifact(path: Path, artifact_name: str) -> None:
    """Raise ``ValueError`` when *path* is a symlinked artifact."""
    if path.is_symlink():
        raise ValueError(f"Refusing symlinked {artifact_name}: {path}")


def _contracts_dir_has_content(contracts_dir: Path) -> bool:
    """Return True if *contracts_dir* has at least one non-symlink entry.

    An unreadable directory (e.g. permission denied) is treated as having no
    content so the prerequisite check can continue rather than aborting with a
    traceback.
    """
    if not contracts_dir.is_dir():
        return False
    try:
        entries = list(contracts_dir.iterdir())
    except OSError:
        return False
    for entry in entries:
        _reject_symlinked_artifact(entry, f"{_CONTRACTS_DIR_NAME}/ entry")
    return bool(entries)


def check_prerequisites(feature_dir: Path, *, require_tasks: bool, include_tasks: bool) -> PrereqCheckResult:
    """
    Validate a feature directory's prerequisites and list its available docs.

    Args:
        feature_dir: Active feature directory (e.g. ``specs/042-my-feature``).
        require_tasks: If True, fail when ``tasks.md`` is missing.
        include_tasks: If True and ``tasks.md`` exists, include it in
            ``AVAILABLE_DOCS``.

    Returns:
        PrereqCheckResult with the feature directory and available docs.

    Raises:
        FileNotFoundError: If the feature directory or ``plan.md`` is
            missing, or if *require_tasks* is set and ``tasks.md`` is missing.
        ValueError: If any required or reported artifact is a symlink.
    """
    if not feature_dir.is_dir():
        raise FileNotFoundError(f"Feature directory not found: {feature_dir}. Run agdt-speckit-specify first.")

    plan_path = feature_dir / _PLAN_DOC_NAME
    _reject_symlinked_artifact(plan_path, _PLAN_DOC_NAME)
    if not plan_path.is_file():
        raise FileNotFoundError(f"plan.md not found in {feature_dir}. Run agdt-speckit-plan first.")

    tasks_path = feature_dir / _TASKS_DOC_NAME
    _reject_symlinked_artifact(tasks_path, _TASKS_DOC_NAME)
    if require_tasks and not tasks_path.is_file():
        raise FileNotFoundError(f"tasks.md not found in {feature_dir}. Run agdt-speckit-tasks first.")

    docs: list[str] = []
    for name in _OPTIONAL_DOC_NAMES:
        doc_path = feature_dir / name
        _reject_symlinked_artifact(doc_path, name)
        if doc_path.is_file():
            docs.append(name)

    contracts_dir = feature_dir / _CONTRACTS_DIR_NAME
    _reject_symlinked_artifact(contracts_dir, f"{_CONTRACTS_DIR_NAME}/")
    if _contracts_dir_has_content(contracts_dir):
        docs.append(f"{_CONTRACTS_DIR_NAME}/")
    if include_tasks and tasks_path.is_file():
        docs.append(_TASKS_DOC_NAME)

    return PrereqCheckResult(feature_dir=feature_dir, available_docs=docs)


def scaffold_check_prereqs_async(_argv: list[str] | None = None) -> None:
    """Background wrapper for ``agdt-speckit-scaffold-check-prereqs``."""
    argv = list(sys.argv[1:] if _argv is None else _argv)
    task = run_function_in_background(
        module_path="agentic_devtools.cli.speckit.scaffold_check_prereqs",
        function_name="scaffold_check_prereqs_command",
        command_display_name="agdt-speckit-scaffold-check-prereqs",
        func_kwargs={"argv": argv},
    )
    print_task_tracking_info(task)


def scaffold_check_prereqs_command(argv: list[str] | None = None) -> None:
    """CLI entry point for ``agdt-speckit-scaffold-check-prereqs``."""
    parser = argparse.ArgumentParser(
        prog="agdt-speckit-scaffold-check-prereqs",
        description="Check SpecKit workflow prerequisites for the active feature.",
    )
    parser.add_argument(
        "--require-tasks",
        action="store_true",
        default=False,
        help="Require tasks.md to exist (for the implementation phase)",
    )
    parser.add_argument(
        "--include-tasks",
        action="store_true",
        default=False,
        help="Include tasks.md in AVAILABLE_DOCS",
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        default=False,
        help="Output results in JSON format",
    )
    parser.add_argument(
        "--paths-only",
        action="store_true",
        default=False,
        help="Resolve and print active feature paths without validating prerequisites.",
    )
    args = parser.parse_args(argv)
    if args.paths_only and (args.require_tasks or args.include_tasks):
        parser.error("--paths-only cannot be combined with --require-tasks or --include-tasks.")

    try:
        active = resolve_active_feature()
        if args.paths_only:
            result = PrereqCheckResult(feature_dir=active.feature_dir, available_docs=[])
        else:
            result = check_prerequisites(
                active.feature_dir,
                require_tasks=args.require_tasks,
                include_tasks=args.include_tasks,
            )
    except (FeatureResolutionError, FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.json_output:
        print(json.dumps(result.to_dict()))
    else:
        print(f"FEATURE_DIR:{result.feature_dir}")
        print("AVAILABLE_DOCS:")
        for doc in result.available_docs:
            print(f"  - {doc}")
