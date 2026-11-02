"""Jitter bounds are deterministic under a patched random source."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.reconciliation.contention import wait_for_contention


@pytest.mark.parametrize(("attempt", "upper"), [(1, 0.5), (2, 1.0), (4, 4.0), (5, 5.0), (1200, 5.0)])
def test_jitter_is_positive_exponential_and_capped(attempt, upper):
    with (
        patch("agentic_devtools.cli.ci.reconciliation.contention.random.uniform", return_value=0.3) as uniform,
        patch("agentic_devtools.cli.ci.reconciliation.contention.time.sleep") as sleep,
    ):
        wait_for_contention(attempt)
    uniform.assert_called_once_with(0.25, upper)
    sleep.assert_called_once_with(0.3)


def test_invalid_attempt_is_rejected():
    with pytest.raises(ValueError, match="positive"):
        wait_for_contention(0)
