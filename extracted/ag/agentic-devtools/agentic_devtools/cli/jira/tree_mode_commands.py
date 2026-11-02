"""Tree-mode command handoff for ``agdt-create-epic`` (issue #2117 / #2118).

Issue #2117 reserved the stable tree-mode dispatch contract that the router in
:mod:`agentic_devtools.cli.jira.create_epic_router` forwards to.  Issue #2118
implements the concrete pipeline body: :func:`create_epic_tree` derives the
repository root from ``git rev-parse --show-toplevel`` and delegates to
:func:`~agentic_devtools.cli.jira.creation_pipeline.run_creation_pipeline`,
emits a one-line execution summary, and preserves the established ``-> None``
CLI contract.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from agentic_devtools.adapters.operation_plan import OperationPlan

from .creation_pipeline import PipelineValidationError, run_creation_pipeline


def _resolve_repo_root() -> Path:
    """Return the repository root via ``git rev-parse --show-toplevel``.

    Raises:
        PipelineValidationError: If the command fails (i.e. the working
            directory is not inside a Git repository).  Raised before the
            pipeline or any provider is invoked so no provider mutation can
            occur when the repository root cannot be determined.
    """
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise PipelineValidationError(
            "Unable to determine repository root via "
            "'git rev-parse --show-toplevel'; the current working directory "
            "is not inside a Git repository.",
            cause=exc,
        ) from exc
    root = completed.stdout.strip()
    if not root:
        raise PipelineValidationError(
            "Unable to determine repository root via 'git rev-parse --show-toplevel'; the command returned no output."
        )
    return Path(root)


def _emit_operation_summary(plan: OperationPlan) -> None:
    """Write a single-line summary record for the completed tree-mode run."""
    summary = {"event": "create_epic.summary", **plan.to_dict()["summary"]}
    sys.stdout.write(json.dumps(summary, ensure_ascii=False) + "\n")


def create_epic_tree(
    file_path: str,
    *,
    start_from: str | None = None,
    provider: str | None = None,
    dry_run: bool = False,
    force_resume: bool = False,
) -> None:
    """Tree-mode entry point delegating to the #2118 creation pipeline.

    Derives ``repo_path`` from ``git rev-parse --show-toplevel`` (never from
    ``file_path.parent``), converts ``file_path`` to a :class:`~pathlib.Path`,
    and forwards the parsed invocation to
    :func:`~agentic_devtools.cli.jira.creation_pipeline.run_creation_pipeline`.
    The returned :class:`OperationPlan` is used only to emit a one-line summary
    record before being discarded so the command continues to return ``None``.

    Args:
        file_path: Path to the JSON epic-tree plan.
        start_from: Optional ref from which to resume tree execution. Skipped
            prerequisite refs must already have verified mapped identifiers so
            downstream parent/dependency relationships can be reconciled safely.
        provider: Optional normalized provider value (``"github"`` or
            ``"jira"``).  Any other value is rejected by preflight validation.
        dry_run: Effective invocation-scoped dry-run value.
        force_resume: Explicitly allow a single retry for a stale pending entry
            after provider reconciliation and a duplicate-risk warning.

    Returns:
        None.

    Raises:
        PipelineValidationError: If the repository root cannot be determined or
            preflight validation fails.
        PipelineExecutionError: If an adapter mutation fails during execution.
    """
    repo_path = _resolve_repo_root()
    plan = run_creation_pipeline(
        repo_path,
        Path(file_path),
        provider=provider,
        start_from=start_from,
        dry_run=dry_run,
        force_resume=force_resume,
    )
    _emit_operation_summary(plan)
    return None
