from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.models import AgentTaskInventoryLoadResult
from agentic_devtools.cli.ci.pipeline.session_detector import _AGENT_TASK_INVENTORY_UNSET, _load_session_inventory
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError


def test_explicit_none_never_loads_provider() -> None:
    provider = MagicMock()
    result = _load_session_inventory(provider, 7, repo="org/repo", supplied=None)
    assert not result.complete
    provider.list_agent_tasks.assert_not_called()


def test_unset_uses_direct_loader() -> None:
    with patch(
        "agentic_devtools.cli.ci.pipeline.session_detector.load_agent_task_inventory",
        return_value=AgentTaskInventoryLoadResult(()),
    ) as load:
        result = _load_session_inventory(MagicMock(), 7, repo="org/repo", supplied=_AGENT_TASK_INVENTORY_UNSET)
    assert result is load.return_value


@pytest.mark.parametrize("failure", [RuntimeError("HTTP 500"), ProviderRateLimitError(is_rate_limit=False)])
def test_provider_override_failure_is_unavailable(failure: Exception) -> None:
    class Provider(MagicMock):
        def list_agent_tasks(self, repo: str) -> None:
            raise failure

    result = _load_session_inventory(Provider(), 7, repo="org/repo", supplied=_AGENT_TASK_INVENTORY_UNSET)
    assert not result.complete
    assert result.availability == "unavailable"


def test_provider_override_success_does_not_invoke_rest_loader() -> None:
    inventory = AgentTaskInventoryLoadResult(
        (),
        complete=False,
        incomplete_reasons=("page 2: provider_unavailable",),
        http_status=503,
    )

    class Provider(MagicMock):
        def list_agent_tasks(self, repo: str) -> AgentTaskInventoryLoadResult:
            return inventory

    with patch("agentic_devtools.cli.ci.pipeline.session_detector.load_agent_task_inventory") as load:
        result = _load_session_inventory(Provider(), 7, repo="org/repo", supplied=_AGENT_TASK_INVENTORY_UNSET)
    assert result is inventory
    assert result.incomplete_reasons == ("page 2: provider_unavailable",)
    assert result.http_status == 503
    load.assert_not_called()


def test_retryable_provider_cooldown_is_not_swallowed() -> None:
    class Provider(MagicMock):
        def list_agent_tasks(self, repo: str) -> list:
            raise RetryableError(provider="github", credential_identity="reader", retry_after=12, is_rate_limit=True)

    with pytest.raises(ProviderRateLimitError) as caught:
        _load_session_inventory(Provider(), 7, repo="org/repo", supplied=_AGENT_TASK_INVENTORY_UNSET)
    assert caught.value.provider == "github"
    assert caught.value.credential_identity == "reader"
    assert caught.value.retry_after_seconds == 12
