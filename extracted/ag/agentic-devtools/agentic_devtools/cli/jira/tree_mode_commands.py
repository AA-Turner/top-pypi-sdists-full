"""Tree-mode command handoff for ``agdt-create-epic`` (issue #2117 / #2118).

Issue #2117 reserved the stable tree-mode dispatch contract that the router in
:mod:`agentic_devtools.cli.jira.create_epic_router` forwards to.  Issue #2118
implements the concrete pipeline body: :func:`create_epic_tree` derives the
repository root from ``git rev-parse --show-toplevel`` and delegates to
:func:`~agentic_devtools.cli.jira.creation_pipeline.run_creation_pipeline`,
discarding the returned :class:`OperationPlan` to preserve the established
``-> None`` CLI contract.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

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


def create_epic_tree(
    file_path: str,
    *,
    start_from: str | None = None,
    provider: str | None = None,
    dry_run: bool = False,
) -> None:
    """Tree-mode entry point delegating to the #2118 creation pipeline.

    Derives ``repo_path`` from ``git rev-parse --show-toplevel`` (never from
    ``file_path.parent``), converts ``file_path`` to a :class:`~pathlib.Path`,
    and forwards the parsed invocation to
    :func:`~agentic_devtools.cli.jira.creation_pipeline.run_creation_pipeline`.
    The returned :class:`OperationPlan` is intentionally discarded to preserve
    the ``-> None`` CLI contract.

    Args:
        file_path: Path to the JSON epic-tree plan.
        start_from: Reserved for future resumption support. Any non-``None``
            value is currently rejected by preflight validation.
        provider: Optional normalized provider value (``"github"`` or
            ``"jira"``).  Any other value is rejected by preflight validation.
        dry_run: Effective invocation-scoped dry-run value.

    Returns:
        None.

    Raises:
        PipelineValidationError: If the repository root cannot be determined or
            preflight validation fails.
        PipelineExecutionError: If an adapter mutation fails during execution.
    """
    repo_path = _resolve_repo_root()
    run_creation_pipeline(
        repo_path,
        Path(file_path),
        provider=provider,
        start_from=start_from,
        dry_run=dry_run,
    )
    return None
