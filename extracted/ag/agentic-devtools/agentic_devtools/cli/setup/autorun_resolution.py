"""Auto-run resolution logic for agdt-setup.

Determines whether auto-run of the generated setup script should be enabled
based on a strict precedence chain:

1. ``--run`` CLI flag → ``True``
2. ``--no-run`` CLI flag → ``False``
3. ``AGDT_SETUP_NO_AUTORUN`` env var truthy → ``False``
4. ``AGDT_SETUP_RUN`` env var truthy → ``True``
5. CI detected or non-TTY → ``False``
6. Interactive terminal (fallback) → ``True``

It also exposes :func:`get_workflow_suppression_reason`, which reports whether
an active agentic-devtools workflow is in a phase where auto-run must be
suppressed by default.

The module is side-effect-free aside from reading environment variables,
reading the persisted workflow state, and calling ``sys.stdin.isatty()``.
"""

from __future__ import annotations

import os
import sys

_TRUTHY_VALUES: frozenset[str] = frozenset({"1", "true", "yes"})

_CI_INDICATORS: tuple[str, ...] = ("CI", "GITHUB_ACTIONS", "TF_BUILD", "BUILD_BUILDID")

# Workflow steps during which auto-run must be suppressed: the workspace is
# still being scaffolded (branch/worktree creation or review initiation), so
# running the generated setup script would act on an unfinished workspace.
_SUPPRESSING_WORKFLOW_STEPS: dict[str, str] = {
    "work-on-jira-issue": "setup",
    "pull-request-review": "initiate",
}


def _is_env_truthy(name: str) -> bool:
    """Return ``True`` when the environment variable *name* holds a truthy value.

    Truthy values are ``"1"``, ``"true"``, and ``"yes"`` (case-insensitive).
    Any other value — including the empty string or absence — is falsy.
    """
    value = os.environ.get(name, "")
    return value.lower() in _TRUTHY_VALUES


def _is_ci_environment() -> bool:
    """Return ``True`` when a well-known CI environment variable is set to a non-empty value."""
    return any(os.environ.get(var, "") != "" for var in _CI_INDICATORS)


def _is_interactive() -> bool:
    """Return ``True`` when stdin is attached to an interactive terminal.

    Returns ``False`` when ``sys.stdin.isatty()`` raises ``OSError`` or
    ``AttributeError`` (e.g. stdin is ``None`` or closed).
    """
    try:
        return sys.stdin.isatty()
    except (OSError, AttributeError):
        return False


def resolve_autorun_enabled(
    cli_run: bool | None,
    cli_no_run: bool | None,
) -> bool:
    """Compute the ``autorun_enabled`` boolean using a strict precedence chain.

    Args:
        cli_run: ``True`` when ``--run`` was passed, ``None`` otherwise.
        cli_no_run: ``True`` when ``--no-run`` was passed, ``None`` otherwise.

    Returns:
        ``True`` when auto-run should be enabled, ``False`` otherwise.

    Raises:
        ValueError: When both *cli_run* and *cli_no_run* are ``True``
            (programming error — argparse mutual exclusion should prevent this).
    """
    # Tier 0: fail-fast guard for invalid direct calls
    if cli_run is True and cli_no_run is True:
        raise ValueError("--run and --no-run are mutually exclusive")

    # Tier 1: --run flag → True
    if cli_run is True:
        return True

    # Tier 2: --no-run flag → False
    if cli_no_run is True:
        return False

    # Tier 3: AGDT_SETUP_NO_AUTORUN truthy → False
    if _is_env_truthy("AGDT_SETUP_NO_AUTORUN"):
        return False

    # Tier 4: AGDT_SETUP_RUN truthy → True
    if _is_env_truthy("AGDT_SETUP_RUN"):
        return True

    # Tier 5: CI detected or non-TTY → False
    if _is_ci_environment() or not _is_interactive():
        return False

    # Tier 6: interactive terminal fallback → True
    return True


def get_workflow_suppression_reason() -> str | None:
    """Return why an active workflow suppresses auto-run, or ``None``.

    Auto-run is suppressed while the ``work-on-jira-issue`` workflow is at its
    ``setup`` step and while the ``pull-request-review`` workflow is at its
    ``initiate`` step, because both steps are still scaffolding the workspace.

    The persisted workflow state is read defensively: a missing state, a
    malformed (non-dict) payload, a missing or non-string ``active`` value, a
    missing, empty, or non-string ``step`` value (``set_workflow_state`` omits
    ``step`` when it is ``None``), and an unreadable state file each resolve to
    "no suppression".

    Returns:
        A human-readable reason naming the workflow and step, or ``None`` when
        auto-run must not be suppressed.
    """
    from agentic_devtools.state import get_workflow_state

    try:
        workflow = get_workflow_state()
    except (OSError, UnicodeError):
        return None

    if not isinstance(workflow, dict):
        return None

    active = workflow.get("active")
    step = workflow.get("step")
    # Persisted values are untyped: guard against non-string payloads (e.g. a
    # truthy list/dict) which would be unhashable and raise ``TypeError`` in the
    # dict lookup below. Anything that is not a non-empty string degrades to
    # "no suppression", as this function promises.
    if not isinstance(active, str) or not isinstance(step, str) or not active or not step:
        return None

    if _SUPPRESSING_WORKFLOW_STEPS.get(active) != step:
        return None

    return f"the '{active}' workflow is at the '{step}' step"
