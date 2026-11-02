"""Execution mode resolution and validation (FR-001).

Resolves the effective execution mode from multiple signals using
most-restrictive-wins semantics: ``restricted`` > ``dry_run`` > ``live``.
"""

from __future__ import annotations

import enum
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


class ExecutionMode(enum.Enum):
    """Execution mode for the safety policy.

    Ordered from least to most restrictive:
    - live: All actions execute normally with audit logging
    - dry_run: External mutations simulated, local mutations allowed
    - restricted: Only read operations allowed
    """

    live = "live"
    dry_run = "dry_run"
    restricted = "restricted"


# Restrictiveness ordering (higher = more restrictive)
_MODE_RESTRICTIVENESS: dict[ExecutionMode, int] = {
    ExecutionMode.live: 0,
    ExecutionMode.dry_run: 1,
    ExecutionMode.restricted: 2,
}


def resolve_execution_mode(
    *,
    cli_mode: str | None = None,
    state_mode: str | None = None,
    env_dry_run: str | None = None,
    state_dry_run: Any = None,
) -> ExecutionMode:
    """Resolve the effective execution mode from multiple signals.

    Signal sources (all optional):
    - cli_mode: ``--execution-mode`` CLI flag value
    - state_mode: ``orchestration.execution_mode`` state key
    - env_dry_run: ``AGDT_DRY_RUN`` environment variable
    - state_dry_run: ``dry_run`` state key value

    Resolution rules (FR-001):
    1. Collect all non-None signals and parse them into ExecutionMode values
    2. Legacy ``dry_run=true``/``AGDT_DRY_RUN=1`` map to ``dry_run``
    3. Apply most-restrictive-wins: the highest restrictiveness level wins

    Returns:
        The resolved ExecutionMode.
    """
    candidates: list[ExecutionMode] = []

    # Parse CLI mode
    if cli_mode is not None:
        parsed = _parse_mode_string(cli_mode)
        if parsed is not None:
            candidates.append(parsed)

    # Parse state mode
    if state_mode is not None:
        parsed = _parse_mode_string(state_mode)
        if parsed is not None:
            candidates.append(parsed)

    # Legacy AGDT_DRY_RUN env var
    if env_dry_run is None:
        env_dry_run = os.environ.get("AGDT_DRY_RUN")
    if env_dry_run in ("1", "true", "True", "TRUE"):
        candidates.append(ExecutionMode.dry_run)

    # Legacy dry_run state key
    if _is_truthy(state_dry_run):
        candidates.append(ExecutionMode.dry_run)

    if not candidates:
        return ExecutionMode.live

    # Most-restrictive-wins
    return max(candidates, key=lambda m: _MODE_RESTRICTIVENESS[m])


def resolve_execution_mode_from_state() -> ExecutionMode:
    """Convenience: resolve mode reading from actual state and environment.

    This reads from the live state file and environment variables.
    """
    from agentic_devtools.state import get_value

    state_mode = get_value("orchestration.execution_mode")
    state_dry_run = get_value("dry_run")
    return resolve_execution_mode(
        state_mode=state_mode,
        state_dry_run=state_dry_run,
    )


def validate_mode_on_resume(
    persisted_mode: str | None,
    resolved_mode: ExecutionMode,
    *,
    force_override: bool = False,
) -> ExecutionMode:
    """Validate mode consistency on workflow resume (FR-001).

    Rejects mode transitions unless explicitly overridden.

    Args:
        persisted_mode: The mode stored from the previous run (may be None for first run).
        resolved_mode: The freshly resolved mode.
        force_override: If True, allow the transition without raising.

    Returns:
        The validated mode to use.

    Raises:
        ValueError: If modes mismatch and force_override is False.
    """
    if persisted_mode is None:
        return resolved_mode

    persisted = _parse_mode_string(persisted_mode)
    if persisted is None:
        logger.warning("Invalid persisted mode %r, treating as first run", persisted_mode)
        return resolved_mode

    if persisted != resolved_mode:
        if force_override:
            logger.warning(
                "Mode transition override: %s -> %s",
                persisted.value,
                resolved_mode.value,
            )
            return resolved_mode
        raise ValueError(
            f"Execution mode mismatch on resume: persisted={persisted.value!r}, "
            f"resolved={resolved_mode.value!r}. "
            f"Pass force_override=True to validate_mode_on_resume() to allow the transition."
        )

    return resolved_mode


def persist_execution_mode(mode: ExecutionMode) -> None:
    """Persist the resolved execution mode to state."""
    from agentic_devtools.state import set_value

    set_value("orchestration.execution_mode", mode.value)


def _parse_mode_string(value: str) -> ExecutionMode | None:
    """Parse a string into an ExecutionMode, returning None on failure."""
    try:
        return ExecutionMode(value)
    except ValueError:
        # Try common variants
        normalized = value.lower().strip().replace("-", "_")
        try:
            return ExecutionMode(normalized)
        except ValueError:
            logger.warning("Unrecognized execution mode: %r", value)
            return None


def _is_truthy(value: Any) -> bool:
    """Check if a value is truthy in the boolean sense."""
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("1", "true", "yes")
    return bool(value)
