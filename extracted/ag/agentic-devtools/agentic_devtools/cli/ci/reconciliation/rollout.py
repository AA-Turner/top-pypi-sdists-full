"""Trusted-reconciliation rollout and feature-flag controls."""

from __future__ import annotations

from dataclasses import dataclass

from agentic_devtools.cli.ci.reconciliation import config


@dataclass(frozen=True)
class TrustedReconciliationRollout:
    """Feature flags controlling staged trusted-reconciliation rollout."""

    enabled: bool
    shadow_mode: bool
    enforce_fail_closed: bool


def load_rollout() -> TrustedReconciliationRollout:
    """Load rollout state from environment-backed reconciliation config."""
    return TrustedReconciliationRollout(
        enabled=config.TRUSTED_RECONCILIATION_ROLLOUT_ENABLED,
        shadow_mode=not config.TRUSTED_RECONCILIATION_ROLLOUT_ENABLED,
        enforce_fail_closed=True,
    )
