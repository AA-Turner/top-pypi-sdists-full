"""Deterministic fix-loop control module (report-driven, bounded).

Pure logic module that classifies setup outcomes and determines whether
to retry, what remedy to apply, and when to give up.  Contains no I/O —
report loading and stdout capture are the caller's responsibility.
"""

from __future__ import annotations

import enum
import re
from dataclasses import dataclass

from agentic_devtools.cli.setup.exit_codes import ExitCode

# ── Constants ─────────────────────────────────────────────────────────────────

MAX_ATTEMPTS_PER_CLASS: int = 2
MAX_TOTAL_ITERATIONS: int = 6


# ── ErrorClass Enum ───────────────────────────────────────────────────────────


@enum.unique
class ErrorClass(enum.Enum):
    """Canonical error classification for setup outcomes."""

    SUCCESS = "success"
    MISSING_DEPENDENCY = "missing-dependency"
    STALE_PARTIAL_INSTALL = "stale-partial-install"
    CERT_CA_FETCH = "cert-ca-fetch"
    MANAGED_CLI_MISSING = "managed-cli-missing"
    PATH_PROFILE_NOT_UPDATED = "path-profile-not-updated"
    GIT_HOOKS_NOT_CONFIGURED = "git-hooks-not-configured"
    SKILL_INJECTION_PERMS = "skill-injection-perms"
    TRANSIENT_NETWORK = "transient-network"
    AUTH_SECRET = "auth-secret"  # nosec B105 - enum label for setup classification, not a credential
    UNKNOWN = "unknown"


# ── FixAction Dataclass ───────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class FixAction:
    """Immutable verdict from the fix-loop decision logic."""

    give_up: bool
    remedy: str | None
    re_exec: bool


# ── Private Mappings ──────────────────────────────────────────────────────────

_EXIT_CODE_MAP: dict[int, ErrorClass] = {
    ExitCode.OK.value: ErrorClass.SUCCESS,
    ExitCode.WARNINGS.value: ErrorClass.SUCCESS,
    ExitCode.MISSING_REQUIRED_DEP.value: ErrorClass.MISSING_DEPENDENCY,
    ExitCode.VERSION_BLOCKED.value: ErrorClass.UNKNOWN,
    ExitCode.UPGRADED_RERUN_NEEDED.value: ErrorClass.UNKNOWN,
    ExitCode.REPO_MUTATION_FAILED.value: ErrorClass.UNKNOWN,
    ExitCode.AUTORUN_FAILED.value: ErrorClass.UNKNOWN,
}

_REPORT_CLASS_MAP: dict[str, ErrorClass] = {
    "success": ErrorClass.SUCCESS,
    "missing-dependency": ErrorClass.MISSING_DEPENDENCY,
    "stale-partial-install": ErrorClass.STALE_PARTIAL_INSTALL,
    "cert-ca-fetch": ErrorClass.CERT_CA_FETCH,
    "managed-cli-missing": ErrorClass.MANAGED_CLI_MISSING,
    "path-profile-not-updated": ErrorClass.PATH_PROFILE_NOT_UPDATED,
    "git-hooks-not-configured": ErrorClass.GIT_HOOKS_NOT_CONFIGURED,
    "skill-injection-perms": ErrorClass.SKILL_INJECTION_PERMS,
    "transient-network": ErrorClass.TRANSIENT_NETWORK,
    "auth-secret": ErrorClass.AUTH_SECRET,
    "unknown": ErrorClass.UNKNOWN,
}

_STDOUT_PATTERNS: list[tuple[re.Pattern[str], ErrorClass]] = [
    (
        re.compile(r"\b(?:command not found|not installed|missing.+dependency)\b", re.IGNORECASE),
        ErrorClass.MISSING_DEPENDENCY,
    ),
    (
        re.compile(
            r"\b(?:token|secret|credential|pat|api\.key)\b.+(?:missing|invalid|expired)\b",
            re.IGNORECASE | re.DOTALL,
        ),
        ErrorClass.AUTH_SECRET,
    ),
    (
        re.compile(
            r"\b(?:certificate|ssl|ca\.bundle|cert)\b.+\b(?:fail|error|invalid|expired)",
            re.IGNORECASE | re.DOTALL,
        ),
        ErrorClass.CERT_CA_FETCH,
    ),
    (
        re.compile(r"\b(?:stale|partial|corrupt(?:ed|ion)?)\b.{0,200}?\binstall(?:ation)?\b", re.IGNORECASE),
        ErrorClass.STALE_PARTIAL_INSTALL,
    ),
    (
        re.compile(
            r"\b(?:timeout|connection refused|network.+unreachable|name.+resolution.+failed)\b",
            re.IGNORECASE,
        ),
        ErrorClass.TRANSIENT_NETWORK,
    ),
    (
        re.compile(r"\b(?:PATH|profile).+(?:not updated|not found|missing)\b", re.IGNORECASE),
        ErrorClass.PATH_PROFILE_NOT_UPDATED,
    ),
    (
        re.compile(
            r"\bpermission\b.*\b(?:denied|fail(?:ed)?|error)\b.*\b(?:skill(?:[\s._-]?inject(?:ion|or)?)|copilot)\b|\b(?:skill(?:[\s._-]?inject(?:ion|or)?)|copilot)\b.*\bpermission\b.*\b(?:denied|fail(?:ed)?|error)\b",
            re.IGNORECASE | re.DOTALL,
        ),
        ErrorClass.SKILL_INJECTION_PERMS,
    ),
]

_REMEDY_MAP: dict[ErrorClass, tuple[str, bool]] = {
    ErrorClass.MISSING_DEPENDENCY: ("Install missing dependency and retry.", False),
    ErrorClass.STALE_PARTIAL_INSTALL: ("Reinstall from scratch and re-execute.", True),
    ErrorClass.CERT_CA_FETCH: ("Re-fetch CA certificates and retry.", False),
    ErrorClass.MANAGED_CLI_MISSING: ("Install missing managed CLI and retry.", False),
    ErrorClass.PATH_PROFILE_NOT_UPDATED: ("Reload shell profile and retry.", False),
    ErrorClass.GIT_HOOKS_NOT_CONFIGURED: ("Configure git hooks path and retry.", False),
    ErrorClass.SKILL_INJECTION_PERMS: ("Fix file permissions for skill injection and retry.", False),
    ErrorClass.TRANSIENT_NETWORK: ("Wait for network availability and retry.", False),
}


# ── Public Functions ──────────────────────────────────────────────────────────


def classify_outcome(
    report: dict[str, object] | None,
    exit_code: int,
    stdout: str,
) -> ErrorClass:
    """Classify a setup outcome into a canonical error class.

    Priority:
    1. Exit codes 0/1 → SUCCESS (unconditional).
    2. Report with recognized ``error_class`` field → mapped ErrorClass.
    3. Exit-code taxonomy lookup via ``_EXIT_CODE_MAP``.
    4. Stdout regex fallback.
    5. Default → UNKNOWN.
    """
    # FR-002: exit codes 0 and 1 are always SUCCESS
    if exit_code in (ExitCode.OK.value, ExitCode.WARNINGS.value):
        return ErrorClass.SUCCESS

    # FR-001/FR-002: report-primary path
    if report and isinstance(report.get("error_class"), str):
        error_class_str: str = report["error_class"]  # type: ignore[assignment]
        mapped = _REPORT_CLASS_MAP.get(error_class_str)
        if mapped is not None:
            return mapped

    # FR-003 step 1: exit-code taxonomy fallback
    ec_mapped = _EXIT_CODE_MAP.get(exit_code)
    if ec_mapped is not None and ec_mapped is not ErrorClass.UNKNOWN:
        return ec_mapped

    # FR-003 step 2: stdout regex fallback
    for pattern, error_class in _STDOUT_PATTERNS:
        if pattern.search(stdout):
            return error_class

    return ErrorClass.UNKNOWN


def next_action(error_class: ErrorClass, attempts: int, total: int) -> FixAction:
    """Determine the next action for the fix loop.

    Args:
        error_class: The classified error from the last setup run.
        attempts: Number of previously executed fix-loop iterations for this
            specific error class (0-based).
        total: Total number of previously executed fix-loop iterations across
            all error classes (0-based).

    Returns:
        A FixAction indicating whether to give up, what remedy to apply,
        and whether re-execution is required.

    Raises:
        ValueError: If *attempts* or *total* is negative.
    """
    if attempts < 0 or total < 0:
        raise ValueError(f"next_action requires attempts >= 0 and total >= 0, got attempts={attempts}, total={total}")
    # FR-004: SUCCESS is always a no-op
    if error_class is ErrorClass.SUCCESS:
        return FixAction(give_up=False, remedy=None, re_exec=False)

    # FR-005: AUTH_SECRET is never auto-fixed
    if error_class is ErrorClass.AUTH_SECRET:
        return FixAction(give_up=True, remedy=None, re_exec=False)

    # FR-011: UNKNOWN is never auto-fixed
    if error_class is ErrorClass.UNKNOWN:
        return FixAction(give_up=True, remedy=None, re_exec=False)

    # FR-006/FR-010: cap enforcement
    if attempts >= MAX_ATTEMPTS_PER_CLASS or total >= MAX_TOTAL_ITERATIONS:
        return FixAction(give_up=True, remedy=None, re_exec=False)

    # Retryable error class — return remedy
    remedy_info = _REMEDY_MAP.get(error_class)
    if remedy_info is None:  # pragma: no cover
        return FixAction(give_up=True, remedy=None, re_exec=False)

    remedy_text, re_exec = remedy_info
    return FixAction(give_up=False, remedy=remedy_text, re_exec=re_exec)


def backoff_seconds(n: int) -> int:
    """Return deterministic exponential backoff capped at 30 seconds.

    Args:
        n: The attempt number (0-based, must be >= 0).

    Returns:
        ``min(2**n, 30)``

    Raises:
        ValueError: If *n* is negative.
    """
    if n < 0:
        raise ValueError(f"backoff_seconds requires n >= 0, got {n}")
    # Cap the exponent before computing to avoid allocating large integers.
    # 2**5 = 32 already exceeds the 30-second ceiling, so any n >= 5 maps to 30.
    return min(2 ** min(n, 5), 30)
