"""Tests for HTTP failure classification."""

import pytest

from agentic_devtools.cli.ci.agent_task_inventory import _agent_task_failure_category


@pytest.mark.parametrize(
    ("status", "category"),
    [
        (401, "authentication"),
        (403, "permission"),
        (404, "http_not_found"),
        (500, "provider_unavailable"),
        (None, "provider_unavailable"),
    ],
)
def test_classifies_observed_status(status, category) -> None:
    assert _agent_task_failure_category(status).value == category
