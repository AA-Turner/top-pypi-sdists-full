import asyncio
import json
import uuid
from typing import Any, cast

import httpx
from pydantic import BaseModel, TypeAdapter
from temporalio.client import WorkflowHandle

from mistralai.workflows.protocol.v1.events import (
    CustomTaskCompleted,
    CustomTaskInProgress,
    CustomTaskStarted,
    WorkflowEvent,
    WorkflowEventType,
)
from mistralai.workflows.protocol.v1.streaming import StreamEventSsePayload
from mistralai.workflows.testing.constants import TEST_TASK_QUEUE

SSE_DATA_PREFIX = "data:"
SSE_RETRY_PREFIX = "retry:"

sse_payload_adapter: TypeAdapter[StreamEventSsePayload] = TypeAdapter(StreamEventSsePayload)
workflow_event_adapter: TypeAdapter[WorkflowEvent] = TypeAdapter(WorkflowEvent)


async def create_workflow(
    client: httpx.AsyncClient,
    workflow_identifier: str,
    input_data: dict[str, Any] | None = None,
    task_queue: str | None = TEST_TASK_QUEUE,
) -> dict[str, Any]:
    body: dict[str, Any] = {}
    if input_data is not None:
        body["input"] = input_data
    if task_queue is not None:
        body["task_queue"] = task_queue
    response = await client.post(
        f"/v1/workflows/{workflow_identifier}/execute",
        json=body,
    )
    response.raise_for_status()
    return cast(dict[str, Any], response.json())


async def get_workflow_status(client: httpx.AsyncClient, execution_id: str) -> dict[str, Any]:
    response = await client.get(f"/v1/workflows/executions/{execution_id}")
    response.raise_for_status()
    return cast(dict[str, Any], response.json())


async def get_workflow_definition(client: httpx.AsyncClient, workflow_identifier: str) -> dict[str, Any]:
    response = await client.get(f"/v1/workflows/{workflow_identifier}")
    response.raise_for_status()
    return cast(dict[str, Any], response.json())


async def terminate_workflow(client: httpx.AsyncClient, execution_id: str) -> None:
    response = await client.post(f"/v1/workflows/executions/{execution_id}/terminate")
    response.raise_for_status()


async def cancel_workflow(client: httpx.AsyncClient, execution_id: str) -> httpx.Response:
    return await client.post(f"/v1/workflows/executions/{execution_id}/cancel")


async def signal_workflow(
    client: httpx.AsyncClient, execution_id: str, signal_name: str, signal_input: Any = None
) -> None:
    response = await client.post(
        f"/v1/workflows/executions/{execution_id}/signals",
        json={"name": signal_name, "input": signal_input},
    )
    response.raise_for_status()


async def query_workflow(
    client: httpx.AsyncClient, execution_id: str, query_name: str, query_input: Any = None
) -> dict[str, Any]:
    payload = {"name": query_name}
    if query_input is not None:
        payload["input"] = query_input
    response = await client.post(
        f"/v1/workflows/executions/{execution_id}/queries",
        json=payload,
    )
    response.raise_for_status()
    return cast(dict[str, Any], response.json())


async def update_workflow(
    client: httpx.AsyncClient, execution_id: str, update_name: str, update_input: Any = None
) -> dict[str, Any]:
    payload = {"name": update_name}
    if update_input is not None:
        payload["input"] = update_input
    response = await client.post(
        f"/v1/workflows/executions/{execution_id}/updates",
        json=payload,
    )
    response.raise_for_status()
    return cast(dict[str, Any], response.json())


async def update_workflow_definition(
    client: httpx.AsyncClient, workflow_identifier: str, payload: dict[str, Any]
) -> dict[str, Any]:
    response = await client.put(f"/v1/workflows/{workflow_identifier}", json=payload)
    response.raise_for_status()
    return cast(dict[str, Any], response.json())


async def register_workflow(
    client: httpx.AsyncClient,
    workflow_name: str,
    task_queue: str = "default",
    input_schema: dict[str, Any] | None = None,
    deployment_name: str | None = None,
    display_name: str | None = None,
) -> dict[str, Any]:
    if input_schema is None:
        input_schema = {"type": "object", "properties": {}, "additionalProperties": True}
    definition: dict[str, Any] = {
        "name": workflow_name,
        "task_queue": task_queue,
        "input_schema": input_schema,
    }
    if display_name is not None:
        definition["display_name"] = display_name
    body: dict[str, Any] = {"definitions": [definition]}
    if deployment_name is not None:
        body["deployment_name"] = deployment_name
    response = await client.post("/v1/workflows/register", json=body)
    response.raise_for_status()
    return cast(dict[str, Any], response.json())


def unique_name(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


async def list_workflows(
    client: httpx.AsyncClient,
    **params: Any,
) -> dict[str, Any]:
    response = await client.get("/v1/workflows", params=params)
    response.raise_for_status()
    return cast(dict[str, Any], response.json())


async def list_internal_workflows(
    client: httpx.AsyncClient,
    **params: Any,
) -> dict[str, Any]:
    response = await client.get("/v1/internals/workflows", params=params)
    response.raise_for_status()
    return cast(dict[str, Any], response.json())


async def paginate_workflows(
    list_fn: Any,
    client: httpx.AsyncClient,
    *,
    limit: int,
    **params: Any,
) -> list[dict[str, Any]]:
    all_rows: list[dict[str, Any]] = []
    cursor: str | None = None
    for _ in range(200):
        result = await list_fn(client=client, limit=limit, cursor=cursor, **params)
        all_rows.extend(result["workflows"])
        cursor = result.get("next_cursor")
        if cursor is None:
            break
    return all_rows


async def paginate_workflows_all(
    list_fn: Any,
    client: httpx.AsyncClient,
    *,
    limits: list[int] | None = None,
    **params: Any,
) -> list[dict[str, Any]]:
    if limits is None:
        limits = [1, 2, 4, 8, 20]

    reference = await paginate_workflows(list_fn, client, limit=limits[0], **params)
    reference_ids = [w["id"] for w in reference]

    for limit in limits[1:]:
        rows = await paginate_workflows(list_fn, client, limit=limit, **params)
        ids = [w["id"] for w in rows]
        assert ids == reference_ids, f"Pagination with limit={limit} returned different results than limit={limits[0]}"

    return reference


async def archive_workflow(client: httpx.AsyncClient, workflow_identifier: str) -> httpx.Response:
    response = await client.put(f"/v1/workflows/{workflow_identifier}/archive")
    return response


async def unarchive_workflow(client: httpx.AsyncClient, workflow_identifier: str) -> httpx.Response:
    response = await client.put(f"/v1/workflows/{workflow_identifier}/unarchive")
    return response


async def create_workflow_raw(
    client: httpx.AsyncClient,
    workflow_identifier: str,
    input_data: dict[str, Any],
    task_queue: str | None = TEST_TASK_QUEUE,
) -> httpx.Response:
    """Start a workflow without raising on error status."""
    body: dict[str, Any] = {"input": input_data}
    if task_queue is not None:
        body["task_queue"] = task_queue
    return await client.post(
        f"/v1/workflows/{workflow_identifier}/execute",
        json=body,
    )


async def signal_workflow_raw(
    client: httpx.AsyncClient, execution_id: str, signal_name: str, signal_input: dict[str, Any] | None = None
) -> httpx.Response:
    """Send a signal without raising on error status."""
    payload: dict[str, Any] = {"name": signal_name}
    if signal_input is not None:
        payload["input"] = signal_input
    return await client.post(
        f"/v1/workflows/executions/{execution_id}/signals",
        json=payload,
    )


async def query_workflow_raw(
    client: httpx.AsyncClient, execution_id: str, query_name: str, query_input: dict[str, Any] | None = None
) -> httpx.Response:
    """Send a query without raising on error status."""
    payload: dict[str, Any] = {"name": query_name}
    if query_input is not None:
        payload["input"] = query_input
    return await client.post(
        f"/v1/workflows/executions/{execution_id}/queries",
        json=payload,
    )


async def update_workflow_raw(
    client: httpx.AsyncClient, execution_id: str, update_name: str, update_input: dict[str, Any] | None = None
) -> httpx.Response:
    """Send an update without raising on error status."""
    payload: dict[str, Any] = {"name": update_name}
    if update_input is not None:
        payload["input"] = update_input
    return await client.post(
        f"/v1/workflows/executions/{execution_id}/updates",
        json=payload,
    )


async def get_workflow(client: httpx.AsyncClient, workflow_identifier: str) -> dict[str, Any]:
    response = await client.get(f"/v1/workflows/{workflow_identifier}")
    response.raise_for_status()
    return cast(dict[str, Any], response.json())


async def wait_for_workflow_completion(
    client: httpx.AsyncClient, execution_id: str, max_retries: int = 50, delay: float = 0.1
) -> dict[str, Any]:
    for _ in range(max_retries):
        status_response = await get_workflow_status(client, execution_id)
        if status_response["status"] in ["COMPLETED", "FAILED", "TERMINATED", "CANCELED"]:
            return status_response
        await asyncio.sleep(delay)
    raise AssertionError(f"Workflow {execution_id} did not complete after {max_retries} retries")


def build_workflow_event_payload(
    execution_id: str,
    workflow_run_id: str,
    workflow_name: str,
    event_type: str,
    attributes: dict[str, Any],
) -> dict[str, Any]:
    return {
        "event": {
            "event_id": str(uuid.uuid4()),
            "event_timestamp": 1234567890000000000,
            "root_workflow_exec_id": execution_id,
            "workflow_exec_id": execution_id,
            "workflow_run_id": workflow_run_id,
            "workflow_name": workflow_name,
            "event_type": event_type,
            "attributes": attributes,
        }
    }


async def poll_workflow_status(
    client: httpx.AsyncClient,
    execution_id: str,
    expected_status: str,
    timeout_seconds: int = 30,
) -> dict[str, Any]:
    last_status: str | None = None
    for _ in range(timeout_seconds):
        await asyncio.sleep(1)
        status_response = await client.get(f"/v1/workflows/executions/{execution_id}")
        status_response.raise_for_status()
        status_data = status_response.json()
        last_status = status_data.get("status")

        if last_status == expected_status:
            return cast(dict[str, Any], status_data)
        elif last_status in ["FAILED", "TERMINATED", "TIMED_OUT", "CANCELED", "COMPLETED"]:
            if last_status != expected_status:
                raise RuntimeError(f"Workflow ended with status: {last_status}, expected: {expected_status}")

    raise TimeoutError(
        f"Workflow did not reach {expected_status} status within {timeout_seconds}s (last known status: {last_status})"
    )


async def poll_pending_inputs(
    client: httpx.AsyncClient,
    execution_id: str,
    expected_count: int = 1,
    timeout_seconds: int = 10,
    exclude_task_ids: set[str] | None = None,
) -> list[dict[str, Any]]:
    _exclude = exclude_task_ids or set()
    for _ in range(timeout_seconds * 10):
        await asyncio.sleep(0.1)
        try:
            pending_response = await client.post(
                f"/v1/workflows/executions/{execution_id}/queries",
                json={"name": "__get_pending_inputs"},
            )
            pending_response.raise_for_status()
            pending_data = pending_response.json()
            pending_inputs = [
                p for p in pending_data.get("result", {}).get("pending_inputs", []) if p.get("task_id") not in _exclude
            ]

            if len(pending_inputs) >= expected_count:
                return cast(list[dict[str, Any]], pending_inputs)
        except (httpx.HTTPError, ValueError, KeyError):
            pass

    raise TimeoutError(f"Did not receive {expected_count} pending inputs within {timeout_seconds}s")


async def poll_worker_activity_status(
    client: httpx.AsyncClient,
    expected_active_status: bool,
    workflow_identifier: str | None = None,
    workflow_registration_id: uuid.UUID | None = None,
    timeout_seconds: int = 15,
) -> None:
    if workflow_identifier:
        route = f"/v1/workflows/{workflow_identifier}"
    elif workflow_registration_id:
        route = f"/v1/workflows/registrations/{workflow_registration_id}"
    else:
        raise ValueError("Either workflow_identifier or workflow_registration_id must be provided")

    deadline = asyncio.get_event_loop().time() + timeout_seconds
    while True:
        response = await client.get(route)
        response.raise_for_status()
        active = response.json().get("workflow", {}).get("active")
        if active == expected_active_status:
            return
        if asyncio.get_event_loop().time() >= deadline:
            break
        await asyncio.sleep(1)

    raise TimeoutError(f"Worker activity status is still not '{str(expected_active_status)}' after {timeout_seconds}s")


async def submit_workflow_update(
    client: httpx.AsyncClient,
    execution_id: str,
    update_name: str,
    update_input: dict[str, Any],
) -> None:
    update_response = await client.post(
        f"/v1/workflows/executions/{execution_id}/updates",
        json={
            "name": update_name,
            "input": update_input,
        },
    )
    update_response.raise_for_status()


async def execute_workflow(
    client: httpx.AsyncClient,
    workflow_name: str,
    input_data: dict[str, Any],
    task_queue: str | None = TEST_TASK_QUEUE,
) -> str:
    body: dict[str, Any] = {"input": input_data}
    if task_queue is not None:
        body["task_queue"] = task_queue
    response = await client.post(
        f"/v1/workflows/{workflow_name}/execute",
        json=body,
    )
    response.raise_for_status()
    data = response.json()
    execution_id = data.get("execution_id")
    if not execution_id:
        raise ValueError(f"No execution_id returned: {data}")
    return cast(str, execution_id)


async def wait_for_workflow_events(
    client: httpx.AsyncClient, execution_id: str, max_retries: int = 10
) -> dict[str, Any]:
    for _ in range(max_retries):
        response = await client.get("/v1/workflows/events/list", params={"workflow_exec_id": execution_id, "limit": 1})
        response.raise_for_status()
        events_data = response.json()
        if "events" in events_data and len(events_data["events"]) > 0:
            return cast(dict[str, Any], events_data)
        await asyncio.sleep(0.5)
    raise AssertionError(f"No events found for execution {execution_id} after {max_retries} retries")


async def stream_workflow_events(
    client: httpx.AsyncClient,
    execution_id: str,
    timeout_seconds: float = 30.0,
) -> list[dict[str, Any]]:
    async with asyncio.timeout(timeout_seconds):
        received_events: list[dict[str, Any]] = []
        retry_delay: float = 1  # by default 1 second

        while True:
            start_seq = 0
            if received_events:
                start_seq = received_events[-1]["broker_sequence"] + 1
            async with client.stream(
                "GET",
                "/v1/workflows/events/stream",
                params={"workflow_exec_id": execution_id, "start_seq": start_seq},
                timeout=timeout_seconds,
            ) as stream_response:
                stream_response.raise_for_status()
                async for line in stream_response.aiter_lines():
                    if not line or line.startswith(":"):
                        continue
                    if line.startswith(SSE_DATA_PREFIX):
                        event_data = line[len(SSE_DATA_PREFIX) :].strip()
                        if event_data:
                            event = json.loads(event_data)
                            sse_payload_adapter.validate_python(event)
                            received_events.append(event)
                            event_type = event.get("data", {}).get("event_type")
                            if event_type == WorkflowEventType.WORKFLOW_EXECUTION_COMPLETED:
                                return received_events
                    elif line.startswith(SSE_RETRY_PREFIX):
                        event_retry = line[len(SSE_RETRY_PREFIX) :].strip()
                        if event_retry:
                            try:
                                retry_delay = float(event_retry) / 1000  # the retry is passed in milliseconds
                            except ValueError:
                                continue

            # delay the next retry by the provided amount before retrying
            await asyncio.sleep(retry_delay)


def get_event_types(events: list[dict[str, Any]]) -> list[str]:
    return [e.get("data", {}).get("event_type") for e in events]


def filter_events_by_type(events: list[dict[str, Any]], event_types: list[WorkflowEventType]) -> list[dict[str, Any]]:
    filtered = []
    for e in events:
        event_type = e.get("data", {}).get("event_type")
        if event_type in event_types:
            workflow_event_adapter.validate_python(e.get("data", {}))
            filtered.append(e)
    return filtered


def filter_events_by_custom_task_type(events: list[dict[str, Any]], custom_task_type: str) -> list[dict[str, Any]]:
    filtered = []
    for e in events:
        attrs = e.get("data", {}).get("attributes", {})
        if attrs.get("custom_task_type") == custom_task_type:
            workflow_event_adapter.validate_python(e.get("data", {}))
            filtered.append(e)
    return filtered


def extract_state_from_event(event: dict[str, Any]) -> dict[str, Any] | None:
    validated = sse_payload_adapter.validate_python(event)
    event_data = validated.data
    if isinstance(event_data, (CustomTaskStarted, CustomTaskInProgress, CustomTaskCompleted)):
        payload = event_data.attributes.payload
        if payload.type == "json":
            return cast(dict[str, Any], payload.value)
    return None


def extract_json_patches_from_event(event: dict[str, Any]) -> list[dict[str, Any]]:
    validated = sse_payload_adapter.validate_python(event)
    event_data = validated.data
    if isinstance(event_data, (CustomTaskInProgress, CustomTaskCompleted)):
        payload = event_data.attributes.payload
        if payload.type == "json_patch":
            if isinstance(payload.value, str):
                raise ValueError("Cannot extract patches from encrypted payload")
            return [p.model_dump() for p in payload.value]
    return []


async def execute_workflow_and_wait(
    client: httpx.AsyncClient,
    workflow_name: str,
    input_data: dict[str, Any],
    timeout_seconds: int = 30,
    task_queue: str | None = TEST_TASK_QUEUE,
) -> dict[str, Any]:
    body: dict[str, Any] = {"input": input_data}
    if task_queue is not None:
        body["task_queue"] = task_queue
    response = await client.post(
        f"/v1/workflows/{workflow_name}/execute",
        json=body,
    )
    response.raise_for_status()
    data = response.json()

    execution_id = data.get("execution_id")
    if not execution_id:
        raise ValueError(f"No execution_id returned: {data}")

    last_status: str | None = None
    for _ in range(timeout_seconds):
        await asyncio.sleep(1)

        status_response = await client.get(f"/v1/workflows/executions/{execution_id}")
        status_response.raise_for_status()
        status_data = status_response.json()

        last_status = status_data.get("status")
        if last_status == "COMPLETED":
            return cast(dict[str, Any], status_data)
        elif last_status in ["FAILED", "TERMINATED", "TIMED_OUT", "CANCELED"]:
            raise RuntimeError(f"Workflow {workflow_name} ended with status: {last_status}")

    raise TimeoutError(
        f"Workflow {workflow_name} did not complete within {timeout_seconds}s (last known status: {last_status})"
    )


async def poll_trace_events_available(
    client: httpx.AsyncClient, execution_id: str, timeout: float = 30.0, poll_interval: float = 0.5
) -> None:
    start_time = asyncio.get_event_loop().time()

    while True:
        try:
            response = await client.get(f"/v1/workflows/executions/{execution_id}/trace/events")
            if response.status_code == 200:
                return
        except httpx.HTTPStatusError:
            pass

        elapsed = asyncio.get_event_loop().time() - start_time
        if elapsed > timeout:
            raise TimeoutError(f"Trace events not available for execution {execution_id} after {timeout}s")

        await asyncio.sleep(poll_interval)


def _extract_otel_spans(trace_data: dict[str, Any]) -> list[dict[str, Any]]:
    spans: list[dict[str, Any]] = []
    for batch in trace_data.get("otel_trace_data", {}).get("batches", []):
        for scope_span in batch.get("scopeSpans", []):
            spans.extend(scope_span.get("spans", []))
    return spans


async def poll_trace_otel_data_available(
    client: httpx.AsyncClient,
    execution_id: str,
    timeout: float = 90.0,
    poll_interval: float = 0.5,
    required_span_prefixes: list[str] | None = None,
) -> dict[str, Any]:
    """
    Poll until OTEL trace data is available for an execution and return the trace payload.

    Args:
        client: HTTP client to use for requests
        execution_id: The workflow execution ID
        timeout: Maximum time to wait in seconds. Defaults to 90s because terminal spans (e.g.
            "WorkflowReport:") are exported last through the OTEL->store pipeline, whose tail
            latency exceeds 30s under load on the busy internal worker.
        poll_interval: Time between polls in seconds
        required_span_prefixes: Optional list of span name prefixes; polling continues until at
            least one span matches every prefix. When omitted or empty, polling returns as soon
            as any span is available.
    """
    start_time = asyncio.get_event_loop().time()

    while True:
        try:
            response = await client.get(f"/v1/workflows/executions/{execution_id}/trace/otel")
            response.raise_for_status()

            trace_data = response.json()
            spans = _extract_otel_spans(trace_data)

            if not required_span_prefixes:
                if spans:
                    return cast(dict[str, Any], trace_data)
            else:
                span_names = [span.get("name", "") for span in spans]
                if all(any(name.startswith(prefix) for name in span_names) for prefix in required_span_prefixes):
                    return cast(dict[str, Any], trace_data)
        except httpx.HTTPStatusError:
            pass

        elapsed = asyncio.get_event_loop().time() - start_time
        if elapsed > timeout:
            waiting_for = f" (waiting for span prefixes: {required_span_prefixes})" if required_span_prefixes else ""
            raise TimeoutError(
                f"OTEL trace data not available for execution {execution_id} after {timeout}s{waiting_for}"
            )

        await asyncio.sleep(poll_interval)


async def wait_for_pending_inputs(
    handle: WorkflowHandle,
    expected_count: int = 1,
    timeout: float = 5.0,
    label: str | None = None,
) -> list[dict[str, Any]]:
    start_time = asyncio.get_event_loop().time()

    while True:
        try:
            pending_result = await handle.query("__get_pending_inputs")
            pending_inputs = pending_result["pending_inputs"]

            if label:
                pending_inputs = [inp for inp in pending_inputs if inp.get("label") == label]

            if len(pending_inputs) >= expected_count:
                return cast(list[dict[str, Any]], pending_inputs)

        except Exception:
            pass

        if asyncio.get_event_loop().time() - start_time > timeout:
            raise TimeoutError(
                f"Timeout waiting for {expected_count} pending inputs" + (f" with label '{label}'" if label else "")
            )

        await asyncio.sleep(0.05)


class HeartbeatProcessingParams(BaseModel):
    total_items: int
    items_per_second: int = 10
    get_stuck_at_item: int | None = None
    crash_at_item: int | None = None


class HeartbeatProcessingResult(BaseModel):
    items_processed: int
    heartbeat_count: int
    completed: bool
