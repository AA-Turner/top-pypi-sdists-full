import json

import httpx

from mistralai.workflows.protocol.v1.events import WorkflowEventType
from mistralai.workflows.testing.workflow_helpers import stream_workflow_events


def _completed_event(
    workflow_exec_id: str,
    *,
    root_workflow_exec_id: str | None = None,
    broker_sequence: int = 1,
) -> dict[str, object]:
    return {
        "stream": "events",
        "data": {
            "event_id": f"event-{broker_sequence}",
            "root_workflow_exec_id": root_workflow_exec_id or workflow_exec_id,
            "workflow_exec_id": workflow_exec_id,
            "workflow_run_id": f"run-{workflow_exec_id}",
            "workflow_name": "workflow-1",
            "event_type": WorkflowEventType.WORKFLOW_EXECUTION_COMPLETED,
            "attributes": {
                "task_id": "task-1",
                "result": {"type": "json", "value": "done"},
            },
        },
        "workflow_context": {
            "namespace": "customer:workspace",
            "workflow_name": "workflow-1",
            "workflow_exec_id": workflow_exec_id,
        },
        "broker_sequence": broker_sequence,
    }


class TestStreamWorkflowEvents:
    async def test_reconnects_after_stream_read_error(self) -> None:
        completed_event = _completed_event("exec-1")
        responses = [
            "event: error\n"
            'data: {"error":"Stream read error: Failed to read stream: nats: timeout","reason":"read_error"}\n'
            "retry: 0\n\n",
            f"data: {json.dumps(completed_event)}\n\n",
        ]
        requests: list[httpx.Request] = []

        def handle(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            return httpx.Response(200, text=responses.pop(0))

        async with httpx.AsyncClient(base_url="http://test", transport=httpx.MockTransport(handle)) as client:
            events = await stream_workflow_events(client, "exec-1")

        assert events == [completed_event]
        assert len(requests) == 2
        assert all(request.url.params["start_seq"] == "0" for request in requests)

    async def test_root_stream_reconnects_and_waits_for_root_completion(self) -> None:
        child_completed = _completed_event("child-exec", root_workflow_exec_id="root-exec", broker_sequence=1)
        root_completed = _completed_event("root-exec", broker_sequence=2)
        responses = [
            f"data: {json.dumps(child_completed)}\n\n"
            "event: error\n"
            'data: {"error":"Stream read error: Failed to read stream: nats: timeout","reason":"read_error"}\n'
            "retry: 0\n\n",
            f"data: {json.dumps(root_completed)}\n\n",
        ]
        requests: list[httpx.Request] = []

        def handle(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            return httpx.Response(200, text=responses.pop(0))

        async with httpx.AsyncClient(base_url="http://test", transport=httpx.MockTransport(handle)) as client:
            events = await stream_workflow_events(client, "root-exec", include_child_workflows=True)

        assert events == [child_completed, root_completed]
        assert len(requests) == 2
        assert all(request.url.params["root_workflow_exec_id"] == "root-exec" for request in requests)
        assert all("workflow_exec_id" not in request.url.params for request in requests)
        assert [request.url.params["start_seq"] for request in requests] == ["0", "2"]
