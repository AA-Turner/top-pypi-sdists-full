"""Exit-code taxonomy for agdt-setup.

Provides unique, machine-classifiable exit codes so that orchestrators and
AI agents can determine the category of failure without parsing prose output.

The ``ExitCode`` IntEnum defines a sequential 0–6 range. There is
intentionally **no** ``DRY_RUN`` member — dry-run is an execution mode and
does not change the semantic exit-code taxonomy.
"""

from __future__ import annotations

import enum


@enum.unique
class ExitCode(enum.IntEnum):
    """Stable exit-code taxonomy for ``agdt-setup``."""

    OK = 0
    WARNINGS = 1
    MISSING_REQUIRED_DEP = 2
    VERSION_BLOCKED = 3
    UPGRADED_RERUN_NEEDED = 4
    REPO_MUTATION_FAILED = 5
    AUTORUN_FAILED = 6


# ── Helper functions ──────────────────────────────────────────────────────────


def code_for(name: str) -> int:
    """Return the integer exit code for a member *name*.

    Raises ``KeyError`` for names that do not match an ``ExitCode`` member
    (case-sensitive, exact match required).
    """
    return ExitCode[name].value


def name_for(code: int) -> str:
    """Return the member name for a given exit-code integer.

    Returns ``"UNKNOWN_{code}"`` (preserving sign) when *code* does not
    correspond to any ``ExitCode`` member.
    """
    try:
        return ExitCode(code).name
    except ValueError:
        return f"UNKNOWN_{code}"


# ── Derived lookup dicts (consumed by expectations_validator, etc.) ────────────

ALL_EXIT_CODES: dict[str, int] = {member.name: member.value for member in ExitCode}

EXIT_CODE_DESCRIPTIONS: dict[int, str] = {
    ExitCode.OK: "Setup completed successfully.",
    ExitCode.WARNINGS: "Setup completed but one or more optional checks produced warnings.",
    ExitCode.MISSING_REQUIRED_DEP: "A required dependency is missing.",
    ExitCode.VERSION_BLOCKED: "Running version is older than the project-pinned minimum.",
    ExitCode.UPGRADED_RERUN_NEEDED: "Package was upgraded; a re-run is required.",
    ExitCode.REPO_MUTATION_FAILED: "A repository file-modification step failed.",
    ExitCode.AUTORUN_FAILED: (
        "The auto-run of the generated setup script failed, or an unexpected internal error occurred."
    ),
}


def get_exit_code_name(code: int) -> str:
    """Return the constant name for a given exit-code integer.

    Thin wrapper around :func:`name_for` retained for backward compatibility.
    """
    return name_for(code)
