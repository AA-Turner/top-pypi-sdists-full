"""Tests for failed page result construction."""

from agentic_devtools.cli.ci.agent_task_inventory import _failed_agent_task_page
from agentic_devtools.cli.ci.models import FailureCategory


def test_failure_keeps_explicit_status() -> None:
    result = _failed_agent_task_page(FailureCategory.HTTP_NOT_FOUND, http_status=404)
    assert result.tasks == ()
    assert not result.complete
    assert result.availability == "unavailable"
    assert result.http_status == 404
    assert result.failure_category is FailureCategory.HTTP_NOT_FOUND
    assert result.incomplete_reasons == ("http_not_found",)
