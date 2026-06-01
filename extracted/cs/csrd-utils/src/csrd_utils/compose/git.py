"""Git integration helpers for compose workspaces."""

import subprocess
from pathlib import Path


def maybe_git_init(output_dir: Path) -> None:
    """Run ``git init`` inside *output_dir* if the directory is not already a git repo."""

    if (output_dir / ".git").exists():
        return
    subprocess.run(
        ["git", "init"],
        cwd=output_dir,
        check=True,
        capture_output=True,
    )
