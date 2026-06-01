import asyncio
import os
import uuid

import httpx
import pytest

from mistralai.workflows.protocol.v1.events import (
    JSONPatchPayload,
    WorkflowEventType,
    json_patch,
)
from mistralai.workflows.testing import (
    TEST_TASK_QUEUE,
    activity_completed,
    activity_started,
    compare_itemwise,
    custom_task_completed,
    custom_task_in_progress,
    custom_task_started,
    execute_workflow,
    execute_workflow_and_wait,
    filter_events_by_type,
    get_event_types,
    min_api_version,
    poll_pending_inputs,
    poll_workflow_status,
    sse_payload_adapter,
    stream_workflow_events,
    submit_workflow_update,
    workflow_completed,
    workflow_started,
)

_server_url = os.environ.get("SERVER_URL", "http://localhost:7444")
requires_external_api = pytest.mark.skipif(
    _server_url.startswith("http://localhost"),
    reason=f"Requires external Mistral API (SERVER_URL={_server_url})",
)
requires_local = pytest.mark.skipif(
    not _server_url.startswith("http://localhost"),
    reason=f"Requires local services (SERVER_URL={_server_url})",
)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_hello_world_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "example-hello-world-workflow",
            {"document_title": "test-document"},
        )

        assert result["status"] == "COMPLETED"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_utf8_encoding_workflow(api_client: httpx.AsyncClient) -> None:
    test_message = "Bonjour ! 😊 Je vais très bien, merci de demander ✨ et toi, comment ça va aujourd'hui ? 🌟"

    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "utf8-encoding-test-workflow",
            {"message": test_message},
        )

        assert result["status"] == "COMPLETED"
        workflow_result = result.get("result", {})
        assert workflow_result.get("original_message") == test_message, (
            f"UTF-8 encoding was corrupted. Expected: {test_message!r}, "
            f"Got: {workflow_result.get('original_message')!r}"
        )
        assert workflow_result.get("message_length") == len(test_message)
        assert workflow_result.get("contains_emoji") is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_chain_executor_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "chain-executor-pydantic-example",
            {},
            timeout_seconds=60,
        )

        assert result["status"] == "COMPLETED"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_list_executor_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "list-executor-pydantic-example",
            {},
        )

        assert result["status"] == "COMPLETED"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_offset_pagination_executor_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "offset-pagination-pydantic-example",
            {},
        )

        assert result["status"] == "COMPLETED"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_continue_as_new_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "example-continue-as-new",
            {"offset": 500, "limit": 100, "total_processed": 0},  # start at offset 500 to complete immediately
            timeout_seconds=60,  # Increased timeout
        )

        assert result["status"] == "COMPLETED"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_finance_agent_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "finance_agent_workflow",
            {"question": "What was the ECB interest rate in 2023?", "mock_session": True},
        )

        assert result["status"] == "COMPLETED"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sub_workflow_execution(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "example-with-sub-workflow",
            {"document_title": "test-sub-workflow"},
        )

        assert result["status"] == "COMPLETED"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_compare_child_wait_modes(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "example-compare-child-wait-modes",
            {"document_title": "test-wait-modes"},
        )

        assert result["status"] == "COMPLETED"
        workflow_result = result.get("result", {})
        assert workflow_result["match"] is True, (
            f"wait=True and wait=False returned different results: "
            f"wait_true={workflow_result['wait_true']}, wait_false={workflow_result['wait_false']}"
        )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_scheduled_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "example-with-schedule",
            {"document_title": "test-scheduled-workflow"},
        )

        assert result["status"] == "COMPLETED"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_rate_limited_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "rate-limited-workflow",
            {"n_turns": 3, "rate_limit": 2},
        )

        assert result["status"] == "COMPLETED"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_local_activities_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "local-activity-demo",
            {"email": "test@example.com", "name": "Test User"},
        )

        assert result["status"] == "COMPLETED"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_different_task_queue_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "example-different-task-queue-workflow",
            {"document_title": "test-task-queue"},
        )

        assert result["status"] == "COMPLETED"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_riddle_game_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        execution_id = await execute_workflow(
            api_client,
            "example-interactive-game-workflow",
            {"initial_player_name": "TestPlayer", "max_riddles": 2},
        )

        await asyncio.sleep(2)
        signal_response = await api_client.post(
            f"/v1/workflows/executions/{execution_id}/signals",
            json={"name": "submit_answer", "input": {"answer": "map"}},
        )
        signal_response.raise_for_status()
        await asyncio.sleep(2)
        signal_response = await api_client.post(
            f"/v1/workflows/executions/{execution_id}/signals",
            json={"name": "submit_answer", "input": {"answer": "needle"}},
        )
        signal_response.raise_for_status()

        result = await poll_workflow_status(api_client, execution_id, "COMPLETED", timeout_seconds=30)
        assert result["status"] == "COMPLETED"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_assist_hello_world_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "assist-workflow-hello-world",
            {"document_title": "test-assist-document"},
        )

        assert result["status"] == "COMPLETED"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_long_hello_world_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "example-long-hello-world-workflow",
            {"document_title": "test-long-document"},
            timeout_seconds=60,
        )

        assert result["status"] == "COMPLETED"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_dependency_injection_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "example-dependency-injection-workflow",
            {"user": "test-user"},
            timeout_seconds=60,
        )

        assert result["status"] == "COMPLETED"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_worker_versioning_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "WorkerVersioningExample",
            {"message": "test-versioning"},
        )

        assert result["status"] == "COMPLETED"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_failing_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        execution_id = await execute_workflow(
            api_client,
            "example-failing-workflow",
            {"document_title": "test-document"},
        )

        result = await poll_workflow_status(api_client, execution_id, "FAILED", timeout_seconds=30)
        assert result["status"] == "FAILED"


@pytest.mark.skip(reason="Requires external Mistral API access for agent execution")
@pytest.mark.integration
@pytest.mark.asyncio
async def test_failing_tool_call_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        execution_id = await execute_workflow(
            api_client,
            "failing-tool-call-workflow",
            {},
        )

        result = await poll_workflow_status(api_client, execution_id, "COMPLETED", timeout_seconds=30)
        assert result["status"] == "COMPLETED"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_streaming_tokens_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        execution_id = await execute_workflow(
            api_client,
            "streaming-tokens-example",
            {"text": "Hello world test", "model": "test-model"},
        )

        received_events = await stream_workflow_events(api_client, execution_id)

        assert len(received_events) > 0, "No events received"

        validated_events = [sse_payload_adapter.validate_python(e) for e in received_events]

        expected_event_data = [
            activity_started(),
            workflow_started(),
            activity_completed(),
            activity_started(),
            custom_task_started("token-stream", {"tokens": [], "current_token": ""}),
            custom_task_in_progress(
                "token-stream",
                JSONPatchPayload(
                    value=[
                        json_patch("add", "/tokens/0", "Hello"),
                        json_patch("append", "/current_token", "Hello"),
                    ]
                ),
            ),
            custom_task_in_progress(
                "token-stream",
                JSONPatchPayload(
                    value=[
                        json_patch("add", "/tokens/1", "world"),
                        json_patch("replace", "/current_token", "world"),
                    ]
                ),
            ),
            custom_task_in_progress(
                "token-stream",
                JSONPatchPayload(
                    value=[
                        json_patch("add", "/tokens/2", "test"),
                        json_patch("replace", "/current_token", "test"),
                    ]
                ),
            ),
            custom_task_completed(
                "token-stream",
                {
                    "tokens": ["Hello", "world", "test"],
                    "current_token": "test",
                },
            ),
            activity_completed(),
            activity_started(),
            workflow_completed(),
        ]

        actual_event_data = [e.data for e in validated_events]

        errors = compare_itemwise(
            expected_event_data,
            actual_event_data,
            order_independent_paths={"attributes.payload.value"},
            exclude_paths={
                "event_id",
                "event_timestamp",
                "root_workflow_exec_id",
                "parent_workflow_exec_id",
                "workflow_exec_id",
                "workflow_run_id",
                "workflow_name",
                "attributes.task_id",
                "attributes.workflow_name",
                "attributes.activity_name",
                "attributes.custom_task_id",
                "attributes.input",
                "attributes.result",
            },
        )
        assert len(errors) == 0, "Event sequence mismatch:\n" + "\n".join(errors)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_streaming_tokens_with_progress_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        execution_id = await execute_workflow(
            api_client,
            "streaming-tokens-with-progress-example",
            {"text": "Hello world", "model": "test-model"},
        )

        received_events = await stream_workflow_events(api_client, execution_id)

        assert len(received_events) > 0

        validated_events = [sse_payload_adapter.validate_python(e) for e in received_events]

        expected_event_data = [
            activity_started(),
            workflow_started(),
            activity_completed(),
            activity_started(),
            custom_task_started(
                "progress-stream",
                {
                    "progress_idx": 0,
                    "progress_total": 2,
                    "processed_words": [],
                },
            ),
            custom_task_in_progress(
                "progress-stream",
                JSONPatchPayload(
                    value=[
                        json_patch("replace", "/progress_idx", 1),
                        json_patch("add", "/processed_words/0", "Hello"),
                    ]
                ),
            ),
            custom_task_in_progress(
                "progress-stream",
                JSONPatchPayload(
                    value=[
                        json_patch("replace", "/progress_idx", 2),
                        json_patch("add", "/processed_words/1", "world"),
                    ]
                ),
            ),
            custom_task_completed(
                "progress-stream",
                {
                    "progress_idx": 2,
                    "progress_total": 2,
                    "processed_words": ["Hello", "world"],
                },
            ),
            activity_completed(),
            activity_started(),
            workflow_completed(),
        ]

        actual_event_data = [e.data for e in validated_events]

        errors = compare_itemwise(
            expected_event_data,
            actual_event_data,
            order_independent_paths={"attributes.payload.value"},
            exclude_paths={
                "event_id",
                "event_timestamp",
                "root_workflow_exec_id",
                "parent_workflow_exec_id",
                "workflow_exec_id",
                "workflow_run_id",
                "workflow_name",
                "attributes.task_id",
                "attributes.workflow_name",
                "attributes.activity_name",
                "attributes.custom_task_id",
                "attributes.input",
                "attributes.result",
            },
        )
        assert len(errors) == 0, "Event sequence mismatch:\n" + "\n".join(errors)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_streaming_with_retry_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        execution_id = await execute_workflow(
            api_client,
            "streaming-with-retry-example",
            {"text": "test", "model": "test-model"},
        )

        received_events = await stream_workflow_events(api_client, execution_id, timeout_seconds=60.0)

        assert len(received_events) > 0, "No events received"

        event_types = get_event_types(received_events)
        assert WorkflowEventType.WORKFLOW_EXECUTION_COMPLETED in event_types

        retry_events = filter_events_by_type(received_events, [WorkflowEventType.ACTIVITY_TASK_STARTED])
        assert len(retry_events) >= 1, f"Expected at least 1 activity start event, got {len(retry_events)}"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_expense_approval_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        response = await api_client.post(
            "/v1/workflows/expense-approval-workflow/execute",
            json={
                "input": {
                    "employee_id": "emp-123",
                    "amount": 500.0,
                    "category": "Travel",
                    "description": "Conference travel",
                },
                "task_queue": TEST_TASK_QUEUE,
            },
        )
        response.raise_for_status()
        data = response.json()
        execution_id = data.get("execution_id")
        if not execution_id:
            raise ValueError(f"No execution_id returned: {data}")

        pending_inputs = await poll_pending_inputs(api_client, execution_id, expected_count=1)
        manager_task_id = pending_inputs[0]["task_id"]

        await submit_workflow_update(
            api_client,
            execution_id,
            "__submit_input",
            {
                "task_id": manager_task_id,
                "input": {"approved": True, "reason": "Approved by manager"},
            },
        )

        result = await poll_workflow_status(api_client, execution_id, "COMPLETED", timeout_seconds=30)
        assert result["status"] == "COMPLETED"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_parallel_review_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        response = await api_client.post(
            "/v1/workflows/parallel-review-workflow/execute",
            json={
                "input": {"document_id": "doc-123", "reviewers": ["reviewer1", "reviewer2"]},
                "task_queue": TEST_TASK_QUEUE,
            },
        )
        response.raise_for_status()
        data = response.json()
        execution_id = data.get("execution_id")
        if not execution_id:
            raise ValueError(f"No execution_id returned: {data}")

        pending_inputs = await poll_pending_inputs(api_client, execution_id, expected_count=2)
        assert len(pending_inputs) == 2

        for pending_input in pending_inputs:
            task_id = pending_input["task_id"]
            await submit_workflow_update(
                api_client,
                execution_id,
                "__submit_input",
                {
                    "task_id": task_id,
                    "input": {"approved": True, "comments": "LGTM", "score": 5},
                },
            )

        result = await poll_workflow_status(api_client, execution_id, "COMPLETED", timeout_seconds=30)
        assert result["status"] == "COMPLETED"


@pytest.mark.skip(reason="Requires external Mistral API access for agent execution")
@pytest.mark.integration
@pytest.mark.asyncio
async def test_agent_tool_with_explicit_params_and_kwargs(api_client: httpx.AsyncClient) -> None:
    """Agent tool with explicit params + **kwargs."""
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "case1_weather_with_kwargs",
            {"question": "What's the weather in Paris, France?"},
            timeout_seconds=180,
        )

        assert result["status"] == "COMPLETED"
        workflow_result = result.get("result", {})
        answer = workflow_result.get("answer", "").lower()
        # Activity returns temperature=22, condition="sunny"
        assert "paris" in answer and "22" in answer and "sunny" in answer, (
            f"Expected answer to mention Paris, 22°, and sunny. Got: {answer}"
        )


@pytest.mark.skip(reason="Requires external Mistral API access for agent execution")
@pytest.mark.integration
@pytest.mark.asyncio
async def test_agent_tool_with_only_kwargs(api_client: httpx.AsyncClient) -> None:
    """Agent tool with only **kwargs."""
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "case2_weather_dynamic",
            {"question": "What's the weather in London?"},
            timeout_seconds=180,
        )

        assert result["status"] == "COMPLETED"
        workflow_result = result.get("result", {})
        answer = workflow_result.get("answer", "").lower()
        # Activity returns temperature=18, condition="cloudy", humidity=65
        assert "london" in answer and "18" in answer and "cloudy" in answer and "65" in answer, (
            f"Expected answer to mention London, 18°, cloudy, and 65% humidity. Got: {answer}"
        )


@pytest.mark.skip(reason="Requires external Mistral API access for agent execution")
@pytest.mark.integration
@pytest.mark.asyncio
async def test_agent_tool_with_extensible_basemodel(api_client: httpx.AsyncClient) -> None:
    """Agent tool with BaseModel that has extra='allow'."""
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "case3_weather_extensible",
            {"question": "What's the weather in Berlin, Germany?"},
            timeout_seconds=180,
        )

        assert result["status"] == "COMPLETED"
        workflow_result = result.get("result", {})
        answer = workflow_result.get("answer", "").lower()
        # Activity returns temperature=25, condition="partly cloudy"
        assert "berlin" in answer and "25" in answer and "partly cloudy" in answer, (
            f"Expected answer to mention Berlin, 25°, and partly cloudy. Got: {answer}"
        )


@pytest.mark.skip(reason="Requires external Mistral API access for agent execution")
@pytest.mark.integration
@pytest.mark.asyncio
async def test_agent_tool_with_primitive_param(api_client: httpx.AsyncClient) -> None:
    """Agent tool with simple primitive param (backward compat)."""
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "case4_weather_simple",
            {"question": "What's the weather in Tokyo?"},
            timeout_seconds=180,
        )

        assert result["status"] == "COMPLETED"
        workflow_result = result.get("result", {})
        answer = workflow_result.get("answer", "").lower()
        # Activity returns temperature=20, condition="clear", humidity=50
        assert "tokyo" in answer and "20" in answer and "clear" in answer and "50" in answer, (
            f"Expected answer to mention Tokyo, 20°, clear, and 50% humidity. Got: {answer}"
        )


@min_api_version("2026-5")
@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "workflow_name",
    [
        "example-executor-identity-e2e-workflow",
        "example-executor-identity-token-e2e-workflow",
    ],
)
async def test_executor_identity_e2e_workflow(api_client: httpx.AsyncClient, workflow_name: str) -> None:
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            workflow_name,
            {},
        )

        assert result["status"] == "COMPLETED"
        workflow_result = result.get("result", {})
        uuid.UUID(workflow_result["customer_id"])
        uuid.UUID(workflow_result["workspace_id"])


@min_api_version("2026-5")
@pytest.mark.integration
@pytest.mark.asyncio
async def test_executor_credentials_e2e_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "example-executor-credentials-e2e-workflow",
            {},
            timeout_seconds=60,
        )

        assert result["status"] == "COMPLETED"
        workflow_result = result.get("result", {})
        assert workflow_result["execution_id"] == result["execution_id"]
        assert workflow_result["workflow_name"] == "example-executor-credentials-e2e-workflow"


# TODO: Remove this dedicated test once v2 no longer downgrades to v1; the
# shared example-workflow integration test can then be parametrized by version.
@min_api_version("2026-5")
@pytest.mark.integration
@pytest.mark.asyncio
# TODO: Remove this local-only guard once Kong exposes v2 workflow routes in staging.
@requires_local
async def test_event_route_v2_e2e_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "example-event-route-v2-e2e-workflow",
            {},
            timeout_seconds=60,
        )

        assert result["status"] == "COMPLETED"
        workflow_result = result.get("result", {})
        assert workflow_result["used_v2_event_route"] is True

        events_response = await api_client.get(
            "/v1/workflows/events/list",
            params={"workflow_exec_id": result["execution_id"], "limit": 100},
        )
        events_response.raise_for_status()
        events = events_response.json()["events"]
        event = next(
            (event for event in events if event["event_id"] == workflow_result["event_id"]),
            None,
        )
        assert event is not None
        assert event["event_type"] == WorkflowEventType.CUSTOM_TASK_COMPLETED.value
        assert event["attributes"]["custom_task_id"] == workflow_result["custom_task_id"]


@min_api_version("2026-5")
@requires_external_api
@pytest.mark.integration
@pytest.mark.asyncio
async def test_executor_credentials_chat_e2e_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "example-executor-credentials-chat-e2e-workflow",
            {},
            timeout_seconds=120,
        )

        assert result["status"] == "COMPLETED"
        workflow_result = result.get("result", {})
        assert len(workflow_result["response_content"]) > 0


@min_api_version("2026-5")
@requires_external_api
@pytest.mark.integration
@pytest.mark.asyncio
async def test_executor_credentials_connectors_e2e_workflow(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "example-executor-credentials-connectors-e2e-workflow",
            {},
            timeout_seconds=60,
        )

        assert result["status"] == "COMPLETED"
        workflow_result = result.get("result", {})
        assert workflow_result["connector_count"] >= 0


# Note: The following workflows are excluded from integration tests because they:
# - Require interactive user input (multi_turn_chat_workflow)
# - Require document attachments/URLs (insurance_claims_workflow)
# - Are streaming workflows that require complex interaction patterns
#   (travel_agent_streaming_workflow, local_session_streaming_workflow)
# - Use external MCP servers that may not be available in test environment
#   (mcp_sse_workflow, mcp_tools_workflow, web-search-workflow)
# - Use updates and run indefinitely (simple-chatbot-workflow)
