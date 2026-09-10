"""The execution metrics report names the model the run used; the placeholder stands in only when nothing did."""

from datetime import datetime, timezone
from typing import Any
from unittest.mock import Mock

import pytest

from xpander_sdk.models.configuration import Configuration
from xpander_sdk.models.shared import Tokens
from xpander_sdk.modules.events.events_module import Events
from xpander_sdk.modules.tasks.models.task import AgentExecutionInput
from xpander_sdk.modules.tasks.sub_modules.task import Task

API_CLIENT = "xpander_sdk.modules.tasks.sub_modules.task.APIClient"


def _configuration() -> Configuration:
    return Configuration(api_key="k", organization_id="o1")


def _task(**overrides: Any) -> Task:
    """A minimally populated Task with reportable tokens; overrides win."""
    fields: dict[str, Any] = dict(
        id="t1",
        agent_id="a1",
        organization_id="o1",
        created_at=datetime.now(timezone.utc),
        source="api",
        input=AgentExecutionInput(text="hello"),
        tokens=Tokens(prompt_tokens=1, completion_tokens=1, total_tokens=2),
        configuration=_configuration(),
    )
    fields.update(overrides)
    return Task(**fields)


@pytest.mark.asyncio
async def test_metrics_report_prefers_the_served_model(mock_api_client) -> None:
    api = mock_api_client(API_CLIENT, return_value={})
    task = _task(llm_model_name="gpt-5.4")
    task.mark_served_model(" Claude-Sonnet-5 ")
    await task.areport_metrics(_configuration())
    assert (
        api.make_request.await_args.kwargs["payload"]["ai_model"] == "claude-sonnet-5"
    )


@pytest.mark.asyncio
async def test_metrics_report_falls_back_to_the_override_then_the_placeholder(
    mock_api_client,
) -> None:
    api = mock_api_client(API_CLIENT, return_value={})
    await _task(llm_model_name="GPT-5.4").areport_metrics(_configuration())
    assert api.make_request.await_args.kwargs["payload"]["ai_model"] == "gpt-5.4"
    await _task().areport_metrics(_configuration())
    assert api.make_request.await_args.kwargs["payload"]["ai_model"] == "xpander"


@pytest.mark.asyncio
async def test_finish_path_saves_then_reports_the_served_model(
    mock_api_client, monkeypatch
) -> None:
    """The PATCH echo carries no model field; the report that follows still names the served model."""
    monkeypatch.setenv("XPANDER_AGENT_ID", "a1")
    calls: list[tuple[str, str]] = []

    async def backend(
        path: str, method: str = "GET", payload: Any = None, **_: Any
    ) -> Any:
        calls.append((method, path))
        if path.endswith("/update"):
            echo = dict(payload or {})
            echo.pop("llm_model_name", None)
            echo.pop("llm_model_provider", None)
            return echo
        if path.endswith("/status"):
            return _task().model_dump_safe()
        return {}

    api = mock_api_client(API_CLIENT, side_effect=backend)
    task = _task()

    async def handler(incoming: Task) -> Task:
        incoming.mark_served_model("claude-sonnet-5")
        incoming.result = "done"
        return incoming

    await Events(configuration=_configuration()).handle_task_execution_request(
        Mock(), task, handler
    )

    metrics = [
        c
        for c in api.make_request.await_args_list
        if c.kwargs["path"].endswith("/execution")
    ]
    assert metrics and metrics[-1].kwargs["payload"]["ai_model"] == "claude-sonnet-5"
    order = [
        f"{c.kwargs.get('method', 'GET')} {c.kwargs['path'].rsplit('/', 1)[-1]}"
        for c in api.make_request.await_args_list
    ]
    assert order.index("PATCH update") < order.index("POST execution")
