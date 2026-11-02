"""Tests for the events provider capability."""

import pytest

from agentic_devtools.cli.ci.models import (
    AgentTaskInventory,
    AgentTaskInventoryAvailability,
    AgentTaskInventoryFailureCategory,
    AgentTaskInventoryLoadResult,
    CheckRunStatus,
    EventPayload,
    PRMetadata,
    ReviewInfo,
)
from tests.unit.cli.ci.provider._fixtures import _ConcreteProvider


class TestProviderEventsMixin:
    """Tests for the events provider capability."""

    def test_parse_event_signature(self) -> None:
        provider = _ConcreteProvider()
        result = provider.parse_event({"number": 42}, "pull_request")
        assert isinstance(result, EventPayload)
        assert result.pr_number == 42

    def test_get_pr_metadata_returns_correct_type(self) -> None:
        provider = _ConcreteProvider()
        result = provider.get_pr_metadata(10)
        assert isinstance(result, PRMetadata)
        assert result.number == 10

    def test_list_check_runs_returns_list(self) -> None:
        provider = _ConcreteProvider()
        result = provider.list_check_runs("abc123")
        assert isinstance(result, list)
        assert all(isinstance(r, CheckRunStatus) for r in result)

    def test_codeql_is_not_configured_by_default(self) -> None:
        assert _ConcreteProvider().is_codeql_configured() is False

    def test_list_reviews_returns_list(self) -> None:
        provider = _ConcreteProvider()
        result = provider.list_reviews(1)
        assert isinstance(result, list)
        assert all(isinstance(r, ReviewInfo) for r in result)

    def test_list_pr_session_summaries_returns_empty_by_default(self) -> None:
        """Base providers have no optional Copilot session enrichment."""
        assert _ConcreteProvider().list_pr_session_summaries(1) == []

    def test_agent_task_lifecycle_defaults_are_explicitly_unsupported(self) -> None:
        """Base providers report unsupported task inventories and absent durable clocks."""
        provider = _ConcreteProvider()

        inventory = provider.list_pr_agent_task_lifecycles(1)

        assert inventory == AgentTaskInventory((), complete=False, incomplete_reasons=("unsupported-provider",))
        assert (
            provider.get_or_record_agent_task_first_observed_at(
                1,
                task_id="task-1",
                expected_head_sha="a" * 40,
            )
            is None
        )
        assert provider.get_agent_task_first_observed_at(1, task_id="task-1", expected_head_sha="a" * 40) is None

    def test_get_agent_task_prompt_returns_empty_by_default(self) -> None:
        """Providers without Agent Task detail support expose no recoverable prompt."""
        assert _ConcreteProvider().get_agent_task_prompt("task-1") == ""

    def test_list_agent_tasks_returns_typed_unavailable_inventory_by_default(self) -> None:
        """Providers without Agent Tasks support report typed unavailable evidence."""
        inventory = _ConcreteProvider().list_agent_tasks("owner/repo")

        assert isinstance(inventory, AgentTaskInventoryLoadResult)
        assert inventory.tasks == ()
        assert inventory.availability is AgentTaskInventoryAvailability.UNAVAILABLE
        assert inventory.failure_category is AgentTaskInventoryFailureCategory.PROVIDER_UNAVAILABLE
        assert inventory.complete is False
        assert inventory.incomplete_reasons == ("unsupported-provider",)

    def test_dispatch_agent_retry_default_is_unsupported(self) -> None:
        with pytest.raises(NotImplementedError, match="does not implement dispatch_agent_retry"):
            _ConcreteProvider().dispatch_agent_retry(1, "prompt", "event-1")

    def test_internal_delivery_dispatch_default_is_unsupported(self) -> None:
        with pytest.raises(NotImplementedError, match="does not implement initial-delivery dispatch"):
            _ConcreteProvider()._dispatch_agent_retry(1, "prompt", "event-1", initial_delivery=True)
