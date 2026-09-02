"""PATH profile repair for the doctor framework.

Ensures the managed bin directory (absolute path to ``~/.agdt/bin``) is
present on PATH in the user's shell profile.  The entry is written as an
absolute path, e.g. ``export PATH="/home/user/.agdt/bin:$PATH"``.
Idempotent: if the entry already exists, returns ``False`` (no-op).
"""

from __future__ import annotations

from pathlib import Path

from ..dependency_checker import _MANAGED_BIN_DIR, DependencyStatus
from ..shell_profile import (
    _path_assignment_contains_entry,
    detect_shell_profile,
    detect_shell_type,
    persist_path_entry,
)


def repair_path_profile(dep: DependencyStatus) -> bool:
    """Repair a missing PATH entry for the managed bin directory.

    Appends ``export PATH="<absolute-path-to-.agdt/bin>:$PATH"`` (bash/zsh)
    or the PowerShell equivalent to the user's shell profile.

    Args:
        dep: The ``DependencyStatus`` for the ``path-profile`` check.

    Returns:
        ``True`` if the entry was written (applied), ``False`` if it was
        already present (no-op).

    Raises:
        RuntimeError: If the shell type is unknown or the profile path
            cannot be determined, or if the write fails.
    """
    shell_type = detect_shell_type()
    profile_path = detect_shell_profile()

    if profile_path is None:
        raise RuntimeError(
            f"Cannot repair PATH: unsupported shell type '{shell_type}' or profile path could not be determined."
        )

    path_entry = str(_MANAGED_BIN_DIR)
    wrote = persist_path_entry(profile_path, path_entry, shell_type)

    if wrote:
        # Entry was appended — repair applied.
        dep.found = True
        return True

    # persist_path_entry returned False — either already present or write failed.
    # Post-check: verify the entry actually exists in a PATH-assignment line.
    if _path_entry_in_profile(profile_path, path_entry, shell_type):
        dep.found = True
        return False

    raise RuntimeError(
        f"Failed to persist PATH entry '{path_entry}' to {profile_path}. "
        f"The entry was not found in the profile after attempted write."
    )


def _path_entry_in_profile(profile_path: Path, path_entry: str, shell_type: str) -> bool:
    """Check whether *path_entry* appears as an exact PATH component in *profile_path*."""
    import re

    if not profile_path.exists():
        return False

    try:
        content = profile_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False

    if shell_type in ("bash", "zsh"):
        path_line_re = re.compile(r"^\s*(?:export\s+)?PATH\s*=")
    else:  # powershell
        path_line_re = re.compile(r"^\s*\$env:PATH\s*=", re.IGNORECASE)

    for line in content.splitlines():
        if path_line_re.match(line) and _path_assignment_contains_entry(line, path_entry, shell_type):
            return True
    return False
