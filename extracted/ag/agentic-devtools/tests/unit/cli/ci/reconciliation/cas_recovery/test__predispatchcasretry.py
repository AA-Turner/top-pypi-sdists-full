"""Tests for _PreDispatchCASRetry."""

import pytest

from agentic_devtools.cli.ci.reconciliation.cas_recovery import _PreDispatchCASRetry


def test_predispatchcasretry_carries_conflict_reason() -> None:
    with pytest.raises(_PreDispatchCASRetry, match="stale queue revision"):
        raise _PreDispatchCASRetry("stale queue revision")
