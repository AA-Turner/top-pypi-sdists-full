"""Select changed, existing workflow files from the strict committed diff."""

from __future__ import annotations

from pathlib import Path, PurePosixPath

from agentic_devtools.cli.checks.changed_files import get_strict_committed_changed_files


def select_changed_workflow_files(cwd: Path) -> list[str]:
    """Return changed, existing YAML files directly under ``.github/workflows``."""
    workflow_directory = PurePosixPath(".github/workflows")
    return [
        changed_path
        for changed_path in get_strict_committed_changed_files(cwd)
        if (path := PurePosixPath(changed_path)).parent == workflow_directory
        and path.suffix in {".yml", ".yaml"}
        and (cwd / Path(changed_path)).is_file()
    ]
