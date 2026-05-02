import pytest
from contextlib import redirect_stdout
from importlib.metadata import version
import io
import json
from queue import Empty
import re
import time
from unittest import mock
from uuid import uuid4

from pydantic_core import PydanticSerializationError
import requests_mock

from vellum.workflows.emitters.base import WorkflowEvent
from vellum.workflows.emitters.vellum_emitter import VellumEmitter
from workflow_server.code_exec_runner import run_code_exec_stream
from workflow_server.core.executor import _dump_event
from workflow_server.server import create_app
from workflow_server.utils.system_utils import get_active_process_count


def flask_stream(request_body: dict) -> tuple[int, list]:
    flask_app = create_app()
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/stream", json=request_body)
        status_code = response.status_code

        return status_code, [
            json.loads(line)
            for line in response.data.decode().split("\n")
            if line
            and line
            not in [
                "WAITING",
                "END",
            ]
        ]


@mock.patch("workflow_server.api.workflow_view.ENABLE_PROCESS_WRAPPER", False)
def flask_stream_disable_process_wrapper(request_body: dict) -> tuple[int, list]:
    flask_app = create_app()
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/stream", json=request_body)
        status_code = response.status_code

        return status_code, [
            json.loads(line)
            for line in response.data.decode().split("\n")
            if line
            and line
            not in [
                "WAITING",
                "END",
            ]
        ]


def code_exec_stream(request_body: dict) -> tuple[int, list]:
    output = io.StringIO()

    with mock.patch("os.read") as mocked_os_read, redirect_stdout(output):
        mocked_os_read.return_value = (json.dumps(request_body) + "\n--vellum-input-stop--\n").encode("utf-8")
        run_code_exec_stream()

    lines = output.getvalue().split("\n")
    events = []
    for line in lines:
        if "--event--" in line:
            events.append(json.loads(line.replace("--event--", "")))

    return 200, events


@pytest.fixture(params=[flask_stream, code_exec_stream, flask_stream_disable_process_wrapper])
def both_stream_types(request):
    return request.param


def test_stream_workflow_flask_route__verify_headers():
    # GIVEN a valid request body
    span_id = uuid4()
    request_body = {
        "execution_id": str(span_id),
        "inputs": [],
        "environment_api_key": "test",
        "module": "workflow",
        "timeout": 360,
        "files": {
            "__init__.py": "",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow

class Workflow(BaseWorkflow):
    pass
""",
        },
    }

    # WHEN we call the stream route
    flask_app = create_app()
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/stream", json=request_body)
        status_code = response.status_code

    # THEN we get a 200 response
    assert status_code == 200, response.text

    # AND the version headers are present
    assert "X-Vellum-SDK-Version" in response.headers
    assert "X-Vellum-Server-Version" in response.headers
    assert "X-Vellum-Workflow-Span-Id" in response.headers


def test_stream_workflow_route__happy_path(both_stream_types):
    # GIVEN a valid request body
    span_id = uuid4()
    request_body = {
        "execution_id": str(span_id),
        "inputs": [],
        "environment_api_key": "test",
        "module": "test",
        "timeout": 360,
        "files": {
            "__init__.py": "",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow

class Workflow(BaseWorkflow):
    class Outputs(BaseWorkflow.Outputs):
        foo = "hello"
""",
        },
    }

    with mock.patch("builtins.open", mock.mock_open(read_data="104857600")):
        # WHEN we call the stream route
        ts_ns = time.time_ns()
        request_body["vembda_service_initiated_timestamp"] = ts_ns
        status_code, events = both_stream_types(request_body)

    # THEN we get a 200 response
    assert status_code == 200, events

    # THEN we get the expected events
    assert events[0] == {
        "id": mock.ANY,
        "trace_id": mock.ANY,
        "span_id": str(span_id),
        "timestamp": mock.ANY,
        "api_version": "2024-10-25",
        "parent": None,
        "links": None,
        "name": "vembda.execution.initiated",
        "body": {
            "sdk_version": version("vellum-ai"),
            "server_version": "local",
        },
    }

    assert events[1]["name"] == "workflow.execution.initiated", events[1]
    assert events[1]["body"]["workflow_definition"]["module"] == ["test", "workflow"]
    assert "display_context" in events[1]["body"], events[1]["body"]
    display_context = events[1]["body"]["display_context"]
    assert "node_displays" in display_context
    assert "workflow_inputs" in display_context
    assert "workflow_outputs" in display_context
    assert isinstance(display_context["node_displays"], dict)
    assert isinstance(display_context["workflow_inputs"], dict)
    assert isinstance(display_context["workflow_outputs"], dict)
    assert "foo" in display_context["workflow_outputs"]

    # AND the initiated event should have server_metadata with version info and memory usage
    assert "server_metadata" in events[1]["body"], events[1]["body"]
    server_metadata = events[1]["body"]["server_metadata"]
    assert server_metadata is not None, "server_metadata should not be None"
    assert "server_version" in server_metadata
    assert "sdk_version" in server_metadata
    assert "memory_usage_mb" in server_metadata
    assert isinstance(server_metadata["memory_usage_mb"], (int, float))
    assert "is_new_server" in server_metadata
    assert server_metadata["is_new_server"] is False

    # AND the initiated event should have initiated_latency within a reasonable range
    assert "initiated_latency" in server_metadata, "initiated_latency should be present in server_metadata"
    initiated_latency = server_metadata["initiated_latency"]
    assert isinstance(initiated_latency, int), "initiated_latency should be an integer (nanoseconds)"
    # Latency should be positive and less than 60 seconds (60_000_000_000 nanoseconds) for CI
    assert (
        0 < initiated_latency < 60_000_000_000
    ), f"initiated_latency should be between 0 and 60 seconds, got {initiated_latency} ns"

    assert events[2]["name"] == "workflow.execution.fulfilled", events[2]
    assert events[2]["body"]["workflow_definition"]["module"] == ["test", "workflow"]

    # AND the fulfilled event should have server_metadata with memory usage
    assert "server_metadata" in events[2]["body"], events[2]["body"]
    fulfilled_metadata = events[2]["body"]["server_metadata"]
    assert fulfilled_metadata is not None, "fulfilled server_metadata should not be None"
    assert "memory_usage_mb" in fulfilled_metadata
    assert isinstance(fulfilled_metadata["memory_usage_mb"], (int, float))

    assert events[3] == {
        "id": mock.ANY,
        "trace_id": events[0]["trace_id"],
        "span_id": str(span_id),
        "timestamp": mock.ANY,
        "api_version": "2024-10-25",
        "parent": None,
        "links": None,
        "name": "vembda.execution.fulfilled",
        "body": mock.ANY,
    }
    assert events[3]["body"] == {
        "exit_code": 0,
        "log": "",
        "stderr": "",
        "timed_out": False,
        "container_overhead_latency": mock.ANY,
    }

    assert len(events) == 4


def test_stream_workflow_route__happy_path_with_inputs(both_stream_types):
    # GIVEN a valid request body
    span_id = uuid4()
    request_body = {
        "timeout": 360,
        "execution_id": str(span_id),
        "inputs": [
            {"name": "foo", "type": "STRING", "value": "hello"},
        ],
        "environment_api_key": "test",
        "module": "workflow",
        "files": {
            "__init__.py": "",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow
from vellum.workflows.state import BaseState
from .inputs import Inputs

class Workflow(BaseWorkflow[Inputs, BaseState]):
    class Outputs(BaseWorkflow.Outputs):
        foo = "hello"
""",
            "inputs.py": """\
from vellum.workflows.inputs import BaseInputs

class Inputs(BaseInputs):
    foo: str
""",
        },
    }

    # WHEN we call the stream route
    status_code, events = both_stream_types(request_body)

    # THEN we get a 200 response
    assert status_code == 200, events

    # THEN we get the expected events
    assert events[0] == {
        "id": mock.ANY,
        "trace_id": mock.ANY,
        "span_id": str(span_id),
        "timestamp": mock.ANY,
        "api_version": "2024-10-25",
        "parent": None,
        "links": None,
        "name": "vembda.execution.initiated",
        "body": {
            "sdk_version": version("vellum-ai"),
            "server_version": "local",
        },
    }

    assert events[1]["name"] == "workflow.execution.initiated", events[1]
    assert "display_context" in events[1]["body"], events[1]["body"]
    display_context = events[1]["body"]["display_context"]
    assert "node_displays" in display_context
    assert "workflow_inputs" in display_context
    assert "workflow_outputs" in display_context
    assert isinstance(display_context["node_displays"], dict)
    assert isinstance(display_context["workflow_inputs"], dict)
    assert isinstance(display_context["workflow_outputs"], dict)
    assert "foo" in display_context["workflow_inputs"]
    assert "foo" in display_context["workflow_outputs"]
    assert events[2]["name"] == "workflow.execution.fulfilled", events[2]

    assert events[3] == {
        "id": mock.ANY,
        "trace_id": events[0]["trace_id"],
        "span_id": str(span_id),
        "timestamp": mock.ANY,
        "api_version": "2024-10-25",
        "parent": None,
        "links": None,
        "name": "vembda.execution.fulfilled",
        "body": mock.ANY,
    }
    assert events[3]["body"] == {
        "exit_code": 0,
        "log": "",
        "stderr": "",
        "timed_out": False,
        "container_overhead_latency": mock.ANY,
    }

    assert len(events) == 4


def test_stream_workflow_route__happy_path_with_state(both_stream_types):
    # GIVEN a valid request body
    span_id = uuid4()
    request_body = {
        "timeout": 360,
        "execution_id": str(span_id),
        "state": {"foo": "bar"},
        "environment_api_key": "test",
        "module": "workflow",
        "files": {
            "__init__.py": "",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow
from vellum.workflows.inputs import BaseInputs
from .state import State

class Workflow(BaseWorkflow[BaseInputs, State]):
    class Outputs(BaseWorkflow.Outputs):
        foo = State.foo
""",
            "state.py": """\
from vellum.workflows.state import BaseState

class State(BaseState):
    foo: str
""",
        },
    }

    # WHEN we call the stream route
    status_code, events = both_stream_types(request_body)

    # THEN we get a 200 response
    assert status_code == 200, events

    # THEN we get the expected events
    assert events[0] == {
        "id": mock.ANY,
        "trace_id": mock.ANY,
        "span_id": str(span_id),
        "timestamp": mock.ANY,
        "api_version": "2024-10-25",
        "parent": None,
        "links": None,
        "name": "vembda.execution.initiated",
        "body": {
            "sdk_version": version("vellum-ai"),
            "server_version": "local",
        },
    }

    assert events[1]["name"] == "workflow.execution.initiated", events[1]
    assert "display_context" in events[1]["body"], events[1]["body"]
    display_context = events[1]["body"]["display_context"]
    assert "node_displays" in display_context
    assert "workflow_inputs" in display_context
    assert "workflow_outputs" in display_context
    assert isinstance(display_context["node_displays"], dict)
    assert isinstance(display_context["workflow_inputs"], dict)
    assert isinstance(display_context["workflow_outputs"], dict)
    assert "foo" in display_context["workflow_outputs"]
    assert events[2]["name"] == "workflow.execution.fulfilled", events[2]
    assert events[2]["body"]["outputs"] == {"foo": "bar"}

    assert events[3] == {
        "id": mock.ANY,
        "trace_id": events[0]["trace_id"],
        "span_id": str(span_id),
        "timestamp": mock.ANY,
        "api_version": "2024-10-25",
        "parent": None,
        "links": None,
        "name": "vembda.execution.fulfilled",
        "body": mock.ANY,
    }
    assert events[3]["body"] == {
        "exit_code": 0,
        "log": "",
        "stderr": "",
        "timed_out": False,
        "container_overhead_latency": mock.ANY,
    }

    assert len(events) == 4


def test_stream_workflow_route__bad_indent_in_inputs_file(both_stream_types):
    # GIVEN a valid request body
    span_id = uuid4()
    trace_id = uuid4()
    parent_span_id = uuid4()
    request_body = {
        "timeout": 360,
        "execution_id": str(span_id),
        "execution_context": {
            "trace_id": str(trace_id),
            "parent_context": {"span_id": str(parent_span_id)},
        },
        "inputs": [
            {"name": "foo", "type": "STRING", "value": "hello"},
        ],
        "environment_api_key": "test",
        "module": "workflow",
        "files": {
            "__init__.py": "",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow
from vellum.workflows.state import BaseState
from .inputs import Inputs

class Workflow(BaseWorkflow[Inputs, BaseState]):
    class Outputs(BaseWorkflow.Outputs):
        foo = "hello"
""",
            "inputs.py": """\
from vellum.workflows.inputs import BaseInputs

  class Inputs(BaseInputs):
     foo: str
""",
        },
    }

    # WHEN we call the stream route
    status_code, events = both_stream_types(request_body)

    # THEN we get a 200 response
    assert status_code == 200, events

    # THEN we get the expected events: vembda initiated, workflow initiated, workflow rejected, vembda fulfilled
    assert len(events) == 4

    assert events[0] == {
        "id": mock.ANY,
        "trace_id": str(trace_id),
        "span_id": str(span_id),
        "timestamp": mock.ANY,
        "api_version": "2024-10-25",
        "parent": None,
        "links": None,
        "name": "vembda.execution.initiated",
        "body": {
            "sdk_version": version("vellum-ai"),
            "server_version": "local",
        },
    }

    assert events[1]["name"] == "workflow.execution.initiated"
    assert events[1]["trace_id"] == str(trace_id), "workflow initiated event should use request trace_id"
    assert events[1]["parent"] is not None, "workflow initiated event should have parent context"
    assert events[1]["parent"]["span_id"] == str(
        parent_span_id
    ), "workflow initiated event parent should match request parent_context"

    assert events[2]["name"] == "workflow.execution.rejected"
    assert events[2]["trace_id"] == str(trace_id), "workflow rejected event should use request trace_id"
    assert events[2]["span_id"] == events[1]["span_id"]
    assert events[2]["parent"] is not None, "workflow rejected event should have parent context"
    assert events[2]["parent"]["span_id"] == str(
        parent_span_id
    ), "workflow rejected event parent should match request parent_context"
    assert (
        "Syntax Error raised while loading Workflow: "
        "unexpected indent (inputs.py, line 3)" in events[2]["body"]["error"]["message"]
    )

    assert events[3] == {
        "id": mock.ANY,
        "trace_id": events[0]["trace_id"],
        "span_id": str(span_id),
        "timestamp": mock.ANY,
        "api_version": "2024-10-25",
        "parent": None,
        "links": None,
        "name": "vembda.execution.fulfilled",
        "body": mock.ANY,
    }
    assert events[3]["body"] == {
        "exit_code": 0,
        "log": "",
        "stderr": "",
        "timed_out": False,
        "container_overhead_latency": mock.ANY,
    }


def test_stream_workflow_route__invalid_inputs_initialization_events(both_stream_types):
    """
    Tests that invalid inputs initialization gets us back a workflow initiated and workflow rejected event.
    """
    # GIVEN a valid request body with valid inputs file but omitting required input to cause
    # WorkflowInitializationException
    span_id = uuid4()
    request_body = {
        "timeout": 360,
        "execution_id": str(span_id),
        "inputs": [
            # Omit the required input to trigger WorkflowInitializationException
        ],
        "environment_api_key": "test",
        "module": "workflow",
        "files": {
            "__init__.py": "",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow
from vellum.workflows.state import BaseState
from .inputs import Inputs

class Workflow(BaseWorkflow[Inputs, BaseState]):
    class Outputs(BaseWorkflow.Outputs):
        foo = "hello"
""",
            "inputs.py": """\
from vellum.workflows.inputs import BaseInputs

class Inputs(BaseInputs):
    foo: str
""",
        },
    }

    # WHEN we call the stream route
    status_code, events = both_stream_types(request_body)

    # THEN we get a 200 response
    assert status_code == 200, events

    # THEN we get the expected events: vembda initiated, workflow initiated, workflow rejected, vembda fulfilled
    assert len(events) == 4

    # AND the first event should be vembda execution initiated
    assert events[0]["name"] == "vembda.execution.initiated"
    assert events[0]["span_id"] == str(span_id)

    # AND the second event should be workflow execution initiated
    assert events[1]["name"] == "workflow.execution.initiated"

    # AND the third event should be workflow execution rejected
    assert events[2]["name"] == "workflow.execution.rejected"
    assert events[1]["span_id"] == events[2]["span_id"]
    actual_error_message = events[2]["body"]["error"]["message"]
    assert "Required input variables" in actual_error_message
    assert "foo" in actual_error_message
    assert "should have defined value" in actual_error_message

    # AND the fourth event should be vembda execution fulfilled
    assert events[3]["name"] == "vembda.execution.fulfilled"
    assert events[3]["span_id"] == str(span_id)
    assert events[3]["body"]["exit_code"] == 0


@pytest.mark.parametrize(
    ["execute_workflow_stream", "assert_last_request"],
    [
        (flask_stream, False),  # Unfortunately, can't make assertions on requests made in a subprocess.
        (code_exec_stream, True),
        (flask_stream_disable_process_wrapper, True),
    ],
    ids=["flask_stream", "code_exec_stream", "flask_stream_disable_process_wrapper"],
)
def test_stream_workflow_route__cancel(execute_workflow_stream, assert_last_request):
    # GIVEN a valid request body
    span_id = uuid4()
    request_body = {
        "timeout": 360,
        "execution_id": str(span_id),
        "inputs": [],
        "environment_api_key": "test",
        "module": "workflow",
        "vembda_public_url": "http://test.biz",
        "files": {
            "__init__.py": "",
            "workflow.py": """\
import time

from vellum.workflows.nodes.bases.base import BaseNode
from vellum.workflows.workflows.base import BaseWorkflow


class StartNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        value: str

    def run(self) -> Outputs:
        time.sleep(2)
        return self.Outputs(value="hello world")


class BasicCancellableWorkflow(BaseWorkflow):
    graph = StartNode
    class Outputs(BaseWorkflow.Outputs):
        final_value = StartNode.Outputs.value

""",
        },
    }

    # WHEN we call the stream route with a mock cancelled return true
    with requests_mock.Mocker() as mocker:
        response_mock = mocker.get(
            re.compile("http://test.biz/vembda-public/cancel-workflow-execution-status"), json={"cancelled": True}
        )
        status_code, events = execute_workflow_stream(request_body)

    # THEN we get a 200 response
    assert status_code == 200, events

    # THEN we get the expected cancelled events
    assert events[0] == {
        "id": mock.ANY,
        "trace_id": mock.ANY,
        "span_id": str(span_id),
        "timestamp": mock.ANY,
        "api_version": "2024-10-25",
        "parent": None,
        "links": None,
        "name": "vembda.execution.initiated",
        "body": {
            "sdk_version": version("vellum-ai"),
            "server_version": "local",
        },
    }

    assert events[1]["name"] == "workflow.execution.initiated", events[1]
    assert "display_context" in events[1]["body"], events[1]["body"]

    cancelled_event = events[-2]
    assert cancelled_event["name"] == "workflow.execution.rejected"
    assert cancelled_event["body"]["error"]["message"] == "Workflow run cancelled"

    # AND we called the cancel endpoint with the correct execution id
    workflow_span_id = events[1]["span_id"]
    if assert_last_request:
        assert response_mock.last_request
        assert (
            response_mock.last_request.url
            == f"http://test.biz/vembda-public/cancel-workflow-execution-status/{workflow_span_id}"
        )


def test_stream_workflow_route__timeout_emits_rejection_events():
    """
    Tests that when a workflow times out, we emit node and workflow rejection events.
    """

    span_id = uuid4()
    request_body = {
        "timeout": 1,
        "execution_id": str(span_id),
        "inputs": [],
        "environment_api_key": "test",
        "module": "workflow",
        "files": {
            "__init__.py": "",
            "workflow.py": """\
import time

from vellum.workflows.nodes.bases.base import BaseNode
from vellum.workflows.workflows.base import BaseWorkflow


class LongRunningNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        value: str

    def run(self) -> Outputs:
        time.sleep(30)
        return self.Outputs(value="hello world")


class TimeoutWorkflow(BaseWorkflow):
    graph = LongRunningNode
    class Outputs(BaseWorkflow.Outputs):
        final_value = LongRunningNode.Outputs.value

""",
        },
    }

    status_code, events = flask_stream(request_body)

    assert status_code == 200

    event_names = [e["name"] for e in events]

    assert "vembda.execution.initiated" in event_names
    assert "workflow.execution.initiated" in event_names
    assert "node.execution.initiated" in event_names

    assert "node.execution.rejected" in event_names, "Should emit node.execution.rejected on timeout"
    node_execution_rejected = next(e for e in events if e["name"] == "node.execution.rejected")
    assert "vellum/workflows/runner/runner.py" in node_execution_rejected["body"]["stacktrace"]

    assert "workflow.execution.rejected" in event_names, "Should emit workflow.execution.rejected on timeout"
    workflow_execution_rejected = next(e for e in events if e["name"] == "workflow.execution.rejected")
    assert workflow_execution_rejected["body"]["error"]["code"] == "WORKFLOW_TIMEOUT"
    # TODO: Uncomment once version 1.8.1 is released
    # assert "stacktrace" in workflow_execution_rejected["body"]
    # assert "vellum/workflows/runner/runner.py" in workflow_execution_rejected["body"]["stacktrace"]

    assert "vembda.execution.fulfilled" in event_names
    vembda_fulfilled = next(e for e in events if e["name"] == "vembda.execution.fulfilled")
    assert vembda_fulfilled["body"]["timed_out"] is True


def test_stream_workflow_route__very_large_events(both_stream_types):
    # GIVEN a valid request body
    span_id = uuid4()
    request_body = {
        "execution_id": str(span_id),
        "inputs": [
            {"name": "foo", "type": "STRING", "value": "hello" * 10_000_000},
        ],
        "environment_api_key": "test",
        "module": "workflow",
        "files": {
            "__init__.py": "",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow
from vellum.workflows.state import BaseState
from .inputs import Inputs

class Workflow(BaseWorkflow[Inputs, BaseState]):
    class Outputs(BaseWorkflow.Outputs):
        foo = "hello"
""",
            "inputs.py": """\
from vellum.workflows.inputs import BaseInputs

class Inputs(BaseInputs):
    foo: str
""",
        },
    }

    # WHEN we call the stream route
    status_code, events = both_stream_types(request_body)

    # THEN we get a 200 response
    assert status_code == 200, events

    # THEN we get the expected events
    assert events[0] == {
        "id": mock.ANY,
        "trace_id": mock.ANY,
        "span_id": str(span_id),
        "timestamp": mock.ANY,
        "api_version": "2024-10-25",
        "parent": None,
        "links": None,
        "name": "vembda.execution.initiated",
        "body": {
            "sdk_version": version("vellum-ai"),
            "server_version": "local",
        },
    }

    assert events[1]["name"] == "workflow.execution.initiated", events[1]
    assert "display_context" in events[1]["body"], events[1]["body"]
    assert events[2]["name"] == "workflow.execution.fulfilled", events[2]

    assert events[3] == {
        "id": mock.ANY,
        "trace_id": events[0]["trace_id"],
        "span_id": str(span_id),
        "timestamp": mock.ANY,
        "api_version": "2024-10-25",
        "parent": None,
        "links": None,
        "name": "vembda.execution.fulfilled",
        "body": mock.ANY,
    }
    assert events[3]["body"] == {
        "exit_code": 0,
        "log": "",
        "stderr": "",
        "timed_out": False,
        "container_overhead_latency": mock.ANY,
    }

    assert len(events) == 4


def test_stream_workflow_route__happy_path_run_from_node(both_stream_types):
    # GIVEN a valid request body representing a run from a node
    node_id = uuid4()
    span_id = uuid4()
    request_body = {
        "timeout": 360,
        "execution_id": str(span_id),
        "node_id": str(node_id),
        "environment_api_key": "test",
        "module": "workflow",
        "files": {
            "__init__.py": "from .display import *",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow
from .nodes.start import StartNode
from .nodes.end import EndNode

class Workflow(BaseWorkflow):
    graph = StartNode >> EndNode

    class Outputs(BaseWorkflow.Outputs):
        foo = EndNode.Outputs.value
""",
            "nodes/__init__.py": """
from .start import StartNode
from .end import EndNode

__all__ = ["StartNode", "EndNode"]
""",
            "nodes/start.py": """\
from vellum.workflows.nodes import BaseNode

class StartNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        value = "apple"
""",
            "nodes/end.py": """\
from vellum.workflows.nodes import BaseNode
from .start import StartNode

class EndNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        value = StartNode.Outputs.value.coalesce("banana")
""",
            "display/__init__.py": """
from .nodes import *
from .workflow import *
""",
            "display/workflow.py": """
from uuid import UUID
from vellum_ee.workflows.display.workflows import BaseWorkflowDisplay
from vellum_ee.workflows.display.base import EdgeDisplay
from ..nodes.start import StartNode
from ..nodes.end import EndNode

class WorkflowDisplay(BaseWorkflowDisplay):
    edge_displays = {
        (StartNode.Ports.default, EndNode): EdgeDisplay(
            id=UUID("63606ff1-1c70-4516-92c6-cbaba9336424")
        ),
    }
""",
            "display/nodes/__init__.py": """
from .start import StartNodeDisplay
from .end import EndNodeDisplay

__all__ = ["StartNodeDisplay", "EndNodeDisplay"]
""",
            "display/nodes/start.py": """\
from vellum_ee.workflows.display.nodes import BaseNodeDisplay
from ...nodes.start import StartNode

class StartNodeDisplay(BaseNodeDisplay[StartNode]):
    pass
""",
            "display/nodes/end.py": f"""\
from uuid import UUID

from vellum_ee.workflows.display.nodes import BaseNodeDisplay
from ...nodes.end import EndNode

class EndNodeDisplay(BaseNodeDisplay[EndNode]):
    node_id = UUID("{node_id}")
""",
        },
    }

    # WHEN we call the stream route
    status_code, events = both_stream_types(request_body)

    # THEN we get a 200 response
    assert status_code == 200, events

    # THEN we get the expected workflow and node fulfilled events
    assert events[-4]["name"] == "node.execution.fulfilled", json.dumps(events[-1])
    assert events[-4]["body"]["node_definition"]["id"] == str(node_id)
    assert events[-2]["name"] == "workflow.execution.fulfilled", json.dumps(events[-1])
    assert events[-2]["body"]["outputs"] == {"foo": "banana"}
    assert [event["name"] for event in events] == [
        "vembda.execution.initiated",
        "workflow.execution.initiated",
        "node.execution.initiated",
        "workflow.execution.snapshotted",
        "node.execution.fulfilled",
        "workflow.execution.streaming",
        "workflow.execution.fulfilled",
        "vembda.execution.fulfilled",
    ]


def test_stream_workflow_route__happy_path_run_from_node_with_state(both_stream_types):
    # GIVEN a valid request body representing a run from a node with state
    node_id = uuid4()
    span_id = uuid4()
    request_body = {
        "timeout": 360,
        "execution_id": str(span_id),
        "node_id": str(node_id),
        "environment_api_key": "test",
        "module": "workflow",
        "state": {"meta": {"node_outputs": {"StartNode.Outputs.value": "cherry"}}},
        "files": {
            "__init__.py": "from .display import *",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow
from .nodes.start import StartNode
from .nodes.end import EndNode

class Workflow(BaseWorkflow):
    graph = StartNode >> EndNode

    class Outputs(BaseWorkflow.Outputs):
        foo = EndNode.Outputs.value
""",
            "nodes/__init__.py": """
from .start import StartNode
from .end import EndNode

__all__ = ["StartNode", "EndNode"]
""",
            "nodes/start.py": """\
import random
from vellum.workflows.nodes import BaseNode

class StartNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        value = str
    def run(self) -> Outputs:
        return self.Outputs(value=random.choice(["apple", "banana", "cherry"]))
""",
            "nodes/end.py": """\
from vellum.workflows.nodes import BaseNode
from .start import StartNode

class EndNode(BaseNode):
    fruit = StartNode.Outputs.value.coalesce("date")

    class Outputs(BaseNode.Outputs):
        value: str

    def run(self) -> Outputs:
        return self.Outputs(value=self.fruit)
""",
            "display/__init__.py": """
from .nodes import *
from .workflow import *
""",
            "display/workflow.py": """
from uuid import UUID
from vellum_ee.workflows.display.workflows import BaseWorkflowDisplay
from vellum_ee.workflows.display.base import EdgeDisplay
from ..nodes.start import StartNode
from ..nodes.end import EndNode

class WorkflowDisplay(BaseWorkflowDisplay):
    edge_displays = {
        (StartNode.Ports.default, EndNode): EdgeDisplay(
            id=UUID("63606ff1-1c70-4516-92c6-cbaba9336424")
        ),
    }
""",
            "display/nodes/__init__.py": """
from .start import StartNodeDisplay
from .end import EndNodeDisplay

__all__ = ["StartNodeDisplay", "EndNodeDisplay"]
""",
            "display/nodes/start.py": """\
from vellum_ee.workflows.display.nodes import BaseNodeDisplay
from ...nodes.start import StartNode

class StartNodeDisplay(BaseNodeDisplay[StartNode]):
    pass
""",
            "display/nodes/end.py": f"""\
from uuid import UUID

from vellum_ee.workflows.display.nodes import BaseNodeDisplay
from ...nodes.end import EndNode

class EndNodeDisplay(BaseNodeDisplay[EndNode]):
    node_id = UUID("{node_id}")
""",
        },
    }

    # WHEN we call the stream route
    status_code, events = both_stream_types(request_body)

    # THEN we get a 200 response
    assert status_code == 200, events

    # THEN we get the expected workflow and node initiated events
    assert len(events) > 3, json.dumps(events[-1])
    assert events[2]["name"] == "node.execution.initiated", json.dumps(events[-1])
    assert events[2]["body"]["inputs"] == {"fruit": "cherry"}


@mock.patch("workflow_server.api.workflow_view.wait_for_available_process")
def test_stream_workflow_route__concurrent_request_rate_exceeded(mock_wait_for_available_process):
    # GIVEN a valid request body
    span_id = uuid4()
    request_body = {
        "execution_id": str(span_id),
        "inputs": [],
        "workspace_api_key": "test",
        "environment_api_key": "test",
        "module": "workflow",
        "timeout": 360,
        "files": {
            "__init__.py": "",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow

class Workflow(BaseWorkflow):
    class Outputs(BaseWorkflow.Outputs):
        foo = "hello"
""",
        },
    }

    # AND wait_for_available_process returns False
    mock_wait_for_available_process.return_value = False

    # WHEN we call the stream route
    status_code, events = flask_stream(request_body)

    # THEN we get a 429 response
    assert status_code == 429, events

    # AND we get a simple JSON error response
    assert len(events) == 1
    assert events[0] == {
        "detail": f"Workflow server concurrent request rate exceeded. Process count: {get_active_process_count()}"
    }


def test_stream_workflow_route__with_environment_variables(both_stream_types):
    # GIVEN a valid request body with environment variables
    span_id = uuid4()
    request_body = {
        "execution_id": str(span_id),
        "inputs": [],
        "environment_api_key": "test",
        "module": "workflow",
        "timeout": 360,
        "environment_variables": {"TEST_ENV_VAR": "test_value", "ANOTHER_VAR": "another_value"},
        "files": {
            "__init__.py": "",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow
from vellum.workflows.references import EnvironmentVariableReference

class Workflow(BaseWorkflow):
    class Outputs(BaseWorkflow.Outputs):
        env_var_value = EnvironmentVariableReference(name="TEST_ENV_VAR", default="not_found")
        another_var_value = EnvironmentVariableReference(name="ANOTHER_VAR", default="not_found")
""",
        },
    }

    # WHEN we call the stream route
    status_code, events = both_stream_types(request_body)

    # THEN we get a 200 response
    assert status_code == 200, events

    # THEN we get the expected events
    assert events[0]["name"] == "vembda.execution.initiated"
    assert events[1]["name"] == "workflow.execution.initiated"
    assert events[2]["name"] == "workflow.execution.fulfilled"

    # AND the environment variables are accessible in the workflow
    outputs = events[2]["body"]["outputs"]
    assert outputs["env_var_value"] == "test_value"
    assert outputs["another_var_value"] == "another_value"


@mock.patch("workflow_server.api.workflow_view.Queue")
def test_stream_workflow_route__queue_get_timeout(mock_queue_class):
    # GIVEN a valid request body
    span_id = uuid4()
    request_body = {
        "execution_id": str(span_id),
        "inputs": [],
        "environment_api_key": "test",
        "module": "workflow",
        "timeout": 360,
        "files": {
            "__init__.py": "",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow

class Workflow(BaseWorkflow):
    class Outputs(BaseWorkflow.Outputs):
        foo = "hello"
""",
        },
    }

    # AND the queue.get method raises Empty exception
    mock_queue_instance = mock_queue_class.return_value
    mock_queue_instance.get.side_effect = Empty()

    # WHEN we call the stream route
    flask_app = create_app()
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/stream", json=request_body)
        status_code = response.status_code
        response_data = response.get_json()

    # THEN we get a 408 response
    assert status_code == 408

    # AND we get the expected timeout error message
    assert response_data == {"detail": "Request timed out trying to initiate the Workflow"}


@pytest.mark.parametrize("non_process_stream_types", [code_exec_stream, flask_stream_disable_process_wrapper])
def test_stream_workflow_route__vembda_emitting_calls_monitoring_api(non_process_stream_types):
    """
    Tests that the monitoring API is called when vembda emitting is enabled.
    """

    # GIVEN a valid request body with vembda emitting enabled
    span_id = uuid4()
    request_body = {
        "execution_id": str(span_id),
        "inputs": [],
        "environment_api_key": "test",
        "module": "workflow",
        "timeout": 360,
        "feature_flags": {"vembda-event-emitting-enabled": True},
        "files": {
            "__init__.py": "",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow

class Workflow(BaseWorkflow):
    class Outputs(BaseWorkflow.Outputs):
        foo = "hello"
""",
        },
    }
    emitted_events = []

    def send_events(self, events: list[WorkflowEvent]) -> None:
        for event in events:
            emitted_events.append(event)

    VellumEmitter._send_events = send_events

    # WHEN we call the stream route with mocked monitoring API
    status_code, events = non_process_stream_types(request_body)

    # THEN we get a 200 response
    assert status_code == 200, events

    # AND the expected workflow events were emitted
    event_names = [event.name for event in emitted_events]
    assert len(event_names) == 2, "Should include 2 events"
    assert "workflow.execution.initiated" in event_names, "Should include workflow.execution.initiated event"
    assert "workflow.execution.fulfilled" in event_names, "Should include workflow.execution.fulfilled event"


def test_stream_workflow_route__with_invalid_nested_set_graph(both_stream_types):
    """
    Tests that a workflow with an invalid nested set graph structure raises a clear error in the stream response.
    """
    # GIVEN a Flask application and invalid workflow content with nested set graph
    span_id = uuid4()

    invalid_workflow_content = """
from vellum.workflows import BaseWorkflow
from vellum.workflows.nodes import BaseNode

class TestNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        value = "test"

class InvalidWorkflow(BaseWorkflow):
    graph = {TestNode, {TestNode}}

    class Outputs(BaseWorkflow.Outputs):
        result = TestNode.Outputs.value
"""

    request_body = {
        "timeout": 360,
        "execution_id": str(span_id),
        "inputs": [],
        "environment_api_key": "test",
        "module": "workflow",
        "files": {
            "__init__.py": "",
            "workflow.py": invalid_workflow_content,
        },
    }

    # WHEN we call the stream route
    status_code, events = both_stream_types(request_body)

    # THEN we get a 200 response
    assert status_code == 200, events

    # THEN we get the expected events: vembda initiated, workflow initiated, workflow rejected, vembda fulfilled
    assert len(events) == 4

    # AND the first event should be vembda execution initiated
    assert events[0]["name"] == "vembda.execution.initiated"
    assert events[0]["span_id"] == str(span_id)

    # AND the second event should be workflow execution initiated
    assert events[1]["name"] == "workflow.execution.initiated"

    # AND the third event should be workflow execution rejected
    assert events[2]["name"] == "workflow.execution.rejected"
    assert events[1]["span_id"] == events[2]["span_id"]

    # AND the error message should contain information about the invalid graph structure
    error_message = events[2]["body"]["error"]["message"]
    expected_message = (
        "Invalid graph structure detected. "
        "Nested sets or unsupported graph types are not allowed. "
        "Please contact Vellum support for assistance with Workflow configuration."
    )
    assert error_message == expected_message

    # AND the fourth event should be vembda execution fulfilled
    assert events[3]["name"] == "vembda.execution.fulfilled"
    assert events[3]["span_id"] == str(span_id)
    assert events[3]["body"]["exit_code"] == 0


@mock.patch("workflow_server.api.workflow_view.get_is_oom_killed")
def test_stream_workflow_route__oom_does_not_set_timed_out_flag(mock_get_is_oom_killed):
    """
    Tests that when an OOM error occurs, we don't set the timed_out flag in the vembda fulfilled event.
    """
    # GIVEN a workflow that takes some time to execute
    span_id = uuid4()
    request_body = {
        "timeout": 10,
        "execution_id": str(span_id),
        "inputs": [],
        "environment_api_key": "test",
        "module": "workflow",
        "files": {
            "__init__.py": "",
            "workflow.py": """\
import time

from vellum.workflows.nodes.bases.base import BaseNode
from vellum.workflows.workflows.base import BaseWorkflow


class SlowNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        value: str

    def run(self) -> Outputs:
        time.sleep(2)
        return self.Outputs(value="hello world")


class OOMWorkflow(BaseWorkflow):
    graph = SlowNode
    class Outputs(BaseWorkflow.Outputs):
        final_value = SlowNode.Outputs.value

""",
        },
    }

    # WHEN we mock the OOM killer to trigger after a few checks
    call_count = [0]

    def mock_oom_side_effect():
        call_count[0] += 1
        if call_count[0] > 3:
            return True
        return False

    mock_get_is_oom_killed.side_effect = mock_oom_side_effect

    # AND we call the stream route
    status_code, events = flask_stream(request_body)

    # THEN we get a 200 response
    assert status_code == 200

    # AND we get the expected events
    event_names = [e["name"] for e in events]

    assert "vembda.execution.initiated" in event_names

    # THEN the key assertion: if there's a vembda.execution.fulfilled event, it should NOT have timed_out=True
    vembda_fulfilled_event = next(e for e in events if e["name"] == "vembda.execution.fulfilled")
    assert (
        vembda_fulfilled_event["body"].get("timed_out") is not True
    ), "timed_out flag should not be set when OOM occurs"


@mock.patch("workflow_server.api.workflow_view.ENABLE_PROCESS_WRAPPER", False)
def test_stream_workflow_route__client_disconnect_emits_rejected_event():
    """
    Tests that when a client disconnects mid-stream (GeneratorExit), we emit a workflow execution
    rejected event to the events.create API.
    """
    # GIVEN a valid request body for a workflow that yields multiple events
    span_id = uuid4()
    trace_id = uuid4()
    request_body = {
        "timeout": 360,
        "execution_id": str(span_id),
        "execution_context": {
            "trace_id": str(trace_id),
        },
        "inputs": [],
        "environment_api_key": "test",
        "module": "workflow",
        "files": {
            "__init__.py": "",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow

class Workflow(BaseWorkflow):
    class Outputs(BaseWorkflow.Outputs):
        foo = "hello"
""",
        },
    }

    # AND a mock to capture events.create calls
    events_create_calls = []

    def mock_events_create(request):
        events_create_calls.append(request)

    # WHEN we call the stream route and simulate a client disconnect
    flask_app = create_app()
    with flask_app.test_client() as test_client:
        with mock.patch("workflow_server.core.workflow_executor_context.create_vellum_client") as mock_create_client:
            mock_client = mock.MagicMock()
            mock_client.events.create = mock_events_create
            mock_create_client.return_value = mock_client

            response = test_client.post("/workflow/stream", json=request_body)

            # Get the response iterator and consume a few chunks to start the stream
            response_iter = response.response
            next(response_iter)

            # Close the response to trigger GeneratorExit
            response_iter.close()

    # THEN the events.create API should have been called with rejected event
    assert len(events_create_calls) > 0, "events.create should have been called on client disconnect"

    # AND the call should include a workflow.execution.rejected event (sent as SDK event model)
    last_call = events_create_calls[-1]
    assert isinstance(last_call, list), "events.create should be called with a list"
    assert len(last_call) == 1, "Should have exactly one rejected event"

    rejected_event = last_call[0]
    assert rejected_event.name == "workflow.execution.rejected", "Should be a rejected event"

    # AND the rejected event should have the correct error message
    assert "client disconnected" in rejected_event.body.error.message.lower()

    # AND the rejected event should have a workflow_definition
    # TODO: In the future, we should capture the real workflow_definition from the initiated event.
    # For now, we use BaseWorkflow as a placeholder.
    assert rejected_event.body.workflow_definition is not None, "Should have a workflow_definition"


def test_stream_workflow_route__array_input_string_methods(both_stream_types):
    """
    Tests that array inputs of strings can have string methods called on them.

    This is a regression test for APO-2423 where array inputs of strings were being
    deserialized as VellumValue objects instead of plain strings, causing string
    methods like .upper() to fail.
    """

    # GIVEN a workflow that takes an array of strings and calls .upper() on each item
    span_id = uuid4()
    request_body = {
        "timeout": 360,
        "execution_id": str(span_id),
        "inputs": [
            {
                "name": "items",
                "type": "ARRAY",
                "value": [
                    {"type": "STRING", "value": "hello"},
                    {"type": "STRING", "value": "world"},
                ],
            },
        ],
        "environment_api_key": "test",
        "module": "workflow",
        "files": {
            "__init__.py": "",
            "workflow.py": """\
from typing import List

from vellum.workflows import BaseWorkflow
from vellum.workflows.inputs import BaseInputs
from vellum.workflows.nodes.bases.base import BaseNode
from vellum.workflows.state import BaseState


class Inputs(BaseInputs):
    items: List[str]


class UppercaseNode(BaseNode):
    items = Inputs.items

    class Outputs(BaseNode.Outputs):
        result: List[str]

    def run(self) -> Outputs:
        # This should work if items is a list of strings
        # but will fail if items is a list of VellumValue objects
        uppercased = [item.upper() for item in self.items]
        return self.Outputs(result=uppercased)


class Workflow(BaseWorkflow[Inputs, BaseState]):
    graph = UppercaseNode

    class Outputs(BaseWorkflow.Outputs):
        result = UppercaseNode.Outputs.result
""",
        },
    }

    # WHEN we call the stream route
    status_code, events = both_stream_types(request_body)

    # THEN we get a 200 response
    assert status_code == 200, events

    # AND we should get the expected events without errors
    event_names = [e["name"] for e in events]
    assert "vembda.execution.initiated" in event_names
    assert "workflow.execution.initiated" in event_names
    assert "workflow.execution.fulfilled" in event_names

    # AND the workflow should NOT be rejected
    assert "workflow.execution.rejected" not in event_names, (
        f"Workflow was rejected when it should have succeeded. " f"Events: {events}"
    )

    # AND the output should be the uppercased strings
    fulfilled_event = next(e for e in events if e["name"] == "workflow.execution.fulfilled")
    assert fulfilled_event["body"]["outputs"]["result"] == ["HELLO", "WORLD"]


def test_stream_workflow_route__emits_workflow_events_when_exception_during_trigger_init(both_stream_types):
    """
    Tests that when an exception is raised during trigger __init__ (after workflow import
    but before workflow.execution.initiated is emitted), the API response stream still contains
    workflow lifecycle events.
    """
    # GIVEN a request with a workflow that has a trigger with __init__ that raises
    span_id = uuid4()
    trace_id = uuid4()
    parent_span_id = uuid4()
    request_body = {
        "timeout": 360,
        "execution_id": str(span_id),
        "execution_context": {
            "trace_id": str(trace_id),
            "parent_context": {"span_id": str(parent_span_id)},
        },
        "inputs": [],
        "environment_api_key": "test",
        "module": "workflow",
        "files": {
            "__init__.py": "",
            "metadata.json": """\
{
    "trigger_path_to_id_mapping": {
        ".triggers.failing_trigger.FailingTrigger": "11111111-1111-1111-1111-111111111111"
    }
}
""",
            "triggers/__init__.py": "",
            "triggers/failing_trigger.py": """\
from vellum.workflows.triggers import BaseTrigger


class FailingTrigger(BaseTrigger):
    pass
""",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow, BaseNode, BaseInputs
from vellum.workflows.triggers import BaseTrigger

from .triggers.failing_trigger import FailingTrigger


class StartNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        result: str

    def run(self):
        return self.Outputs(result="done")


class Workflow(BaseWorkflow):
    graph = FailingTrigger >> StartNode

    class Outputs(BaseWorkflow.Outputs):
        result = StartNode.Outputs.result

    @staticmethod
    def deserialize_trigger(trigger_id: str, inputs: BaseInputs) -> BaseTrigger:
        raise RuntimeError("Exception during trigger deserialization")
""",
        },
        # The trigger_id matches the ID in metadata.json for FailingTrigger
        "trigger_id": "11111111-1111-1111-1111-111111111111",
    }

    # WHEN we call the stream route
    status_code, events = both_stream_types(request_body)

    # THEN we get a 200 response
    assert status_code == 200, events

    # AND the response should contain vembda events
    event_names = [e["name"] for e in events]
    assert "vembda.execution.initiated" in event_names
    assert "vembda.execution.fulfilled" in event_names

    # AND the response should contain workflow lifecycle events
    assert "workflow.execution.initiated" in event_names, (
        f"Expected workflow.execution.initiated to be emitted when exception occurs during trigger init. "
        f"Events: {event_names}"
    )
    assert "workflow.execution.rejected" in event_names, (
        f"Expected workflow.execution.rejected to be emitted when exception occurs during trigger init. "
        f"Events: {event_names}"
    )
    assert events[-2]["body"]["error"]["code"] == "INTERNAL_ERROR", events[-2]["body"]["error"]["message"]


@pytest.mark.parametrize(
    "event_filter,expected_node_events",
    [
        (None, True),  # Default (EXCLUDE_NESTED_SNAPSHOTTED) includes node events
        ("EXCLUDE_NESTED_SNAPSHOTTED", True),  # Explicitly set includes node events
        ("ALL", True),  # ALL includes node events
        ("ROOT_WORKFLOW_AND_ROOT_NODE", True),  # Includes node events from root workflow
        ("ROOT_WORKFLOW_ONLY", False),  # Only workflow events, no node events
        ("INVALID_FILTER", True),  # Invalid filter falls back to default (includes node events)
    ],
)
def test_stream_workflow_route__event_filter_parameter(both_stream_types, event_filter, expected_node_events):
    """
    Tests that the event_filter parameter controls which events are included in the stream.

    - ROOT_WORKFLOW_ONLY: Only workflow events (initiated, fulfilled, rejected, etc.)
    - ROOT_WORKFLOW_AND_ROOT_NODE: Workflow events + node events from the root workflow
    - EXCLUDE_NESTED_SNAPSHOTTED: All events except snapshotted from nested workflows (default)
    - ALL: All events
    - Invalid filters fall back to default behavior (EXCLUDE_NESTED_SNAPSHOTTED)
    """
    # GIVEN a workflow with a node that will emit node events
    span_id = uuid4()
    request_body = {
        "execution_id": str(span_id),
        "inputs": [],
        "environment_api_key": "test",
        "module": "workflow",
        "timeout": 360,
        "files": {
            "__init__.py": "",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow
from vellum.workflows.nodes import BaseNode

class MyNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        result = "hello"

class Workflow(BaseWorkflow):
    graph = MyNode

    class Outputs(BaseWorkflow.Outputs):
        result = MyNode.Outputs.result
""",
        },
    }

    # AND the event_filter is set (or not set for default behavior)
    if event_filter is not None:
        request_body["event_filter"] = event_filter

    # WHEN we call the stream route
    status_code, events = both_stream_types(request_body)

    # THEN we get a 200 response
    assert status_code == 200, events

    # AND we always get vembda events
    event_names = [e["name"] for e in events]
    assert "vembda.execution.initiated" in event_names
    assert "vembda.execution.fulfilled" in event_names

    # AND we always get workflow events
    assert "workflow.execution.initiated" in event_names
    assert "workflow.execution.fulfilled" in event_names

    # AND node events are included or excluded based on the filter
    has_node_events = any(name.startswith("node.") for name in event_names)
    if expected_node_events:
        assert has_node_events, (
            f"Expected node events to be included with event_filter={event_filter}, " f"but got events: {event_names}"
        )
        assert "node.execution.initiated" in event_names
        assert "node.execution.fulfilled" in event_names
    else:
        assert not has_node_events, (
            f"Expected no node events with event_filter={event_filter}, " f"but got events: {event_names}"
        )


def test_stream_workflow_route__exclude_vembda_events(both_stream_types):
    """
    Tests that when exclude_vembda_events is True, vembda.execution.* events are filtered out.
    """
    # GIVEN a simple workflow
    span_id = uuid4()
    request_body = {
        "execution_id": str(span_id),
        "inputs": [],
        "environment_api_key": "test",
        "module": "workflow",
        "timeout": 360,
        "files": {
            "__init__.py": "",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow

class Workflow(BaseWorkflow):
    class Outputs(BaseWorkflow.Outputs):
        foo = "hello"
""",
        },
    }

    # AND exclude_vembda_events is set to True
    request_body["exclude_vembda_events"] = True

    # WHEN we call the stream route
    status_code, events = both_stream_types(request_body)

    # THEN we get a 200 response
    assert status_code == 200, events

    # THEN vembda.execution.* events should be filtered out
    event_names = [e["name"] for e in events]
    assert "vembda.execution.initiated" not in event_names
    assert "vembda.execution.fulfilled" not in event_names

    # AND workflow events should still be present
    assert "workflow.execution.initiated" in event_names
    assert "workflow.execution.fulfilled" in event_names


def test_stream_workflow_route__exclude_vembda_events_workflow_exception(both_stream_types):
    """
    Tests that when exclude_vembda_events is True and an exception occurs during workflow streaming,
    a workflow.execution.rejected event is emitted instead of vembda.execution.fulfilled.
    """
    # GIVEN a workflow that raises an exception during trigger deserialization
    span_id = uuid4()
    trace_id = uuid4()
    parent_span_id = uuid4()
    request_body = {
        "timeout": 360,
        "execution_id": str(span_id),
        "execution_context": {
            "trace_id": str(trace_id),
            "parent_context": {"span_id": str(parent_span_id)},
        },
        "inputs": [],
        "environment_api_key": "test",
        "module": "workflow",
        "files": {
            "__init__.py": "",
            "metadata.json": """\
{
    "trigger_path_to_id_mapping": {
        ".triggers.failing_trigger.FailingTrigger": "11111111-1111-1111-1111-111111111111"
    }
}
""",
            "triggers/__init__.py": "",
            "triggers/failing_trigger.py": """\
from vellum.workflows.triggers import BaseTrigger


class FailingTrigger(BaseTrigger):
    pass
""",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow, BaseNode, BaseInputs
from vellum.workflows.triggers import BaseTrigger

from .triggers.failing_trigger import FailingTrigger


class StartNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        result: str

    def run(self):
        return self.Outputs(result="done")


class Workflow(BaseWorkflow):
    graph = FailingTrigger >> StartNode

    class Outputs(BaseWorkflow.Outputs):
        result = StartNode.Outputs.result

    @staticmethod
    def deserialize_trigger(trigger_id: str, inputs: BaseInputs) -> BaseTrigger:
        raise RuntimeError("Exception during trigger deserialization")
""",
        },
        "trigger_id": "11111111-1111-1111-1111-111111111111",
    }

    # AND exclude_vembda_events is set to True
    request_body["exclude_vembda_events"] = True

    # WHEN we call the stream route
    status_code, events = both_stream_types(request_body)

    # THEN we get a 200 response
    assert status_code == 200, events

    # THEN vembda.execution.* events should be filtered out
    event_names = [e["name"] for e in events]
    assert "vembda.execution.initiated" not in event_names
    assert "vembda.execution.fulfilled" not in event_names

    # AND workflow.execution.rejected should be emitted
    assert "workflow.execution.initiated" in event_names
    assert "workflow.execution.rejected" in event_names

    # AND the rejected event should have the correct error code
    rejected_event = next(e for e in events if e["name"] == "workflow.execution.rejected")
    assert rejected_event["body"]["error"]["code"] == "INTERNAL_ERROR"


def test_stream_workflow_route__exclude_vembda_events_node_exception(both_stream_types):
    """
    Tests that when exclude_vembda_events is True and an exception occurs during node streaming,
    a node.execution.rejected event is emitted instead of vembda.execution.fulfilled.
    """
    # GIVEN a workflow with a node that raises an exception during execution
    span_id = uuid4()
    request_body = {
        "timeout": 360,
        "execution_id": str(span_id),
        "inputs": [],
        "environment_api_key": "test",
        "module": "workflow",
        "files": {
            "__init__.py": "",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow
from vellum.workflows.nodes import BaseNode


class FailingNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        result: str

    def run(self):
        raise RuntimeError("Node execution failed")


class Workflow(BaseWorkflow):
    graph = FailingNode

    class Outputs(BaseWorkflow.Outputs):
        result = FailingNode.Outputs.result
""",
        },
    }

    # AND exclude_vembda_events is set to True
    request_body["exclude_vembda_events"] = True

    # WHEN we call the stream route
    status_code, events = both_stream_types(request_body)

    # THEN we get a 200 response
    assert status_code == 200, events

    # THEN vembda.execution.* events should be filtered out
    event_names = [e["name"] for e in events]
    assert "vembda.execution.initiated" not in event_names
    assert "vembda.execution.fulfilled" not in event_names

    # AND node.execution.rejected should be emitted (the node itself rejects)
    assert "node.execution.rejected" in event_names

    # AND workflow.execution.rejected should also be emitted (workflow rejects due to node failure)
    assert "workflow.execution.rejected" in event_names


def test_stream_workflow_route__generator_in_node_output_skips_failed_event_and_continues(both_stream_types):
    """
    Tests that when a node output contains a generator object that causes a PydanticSerializationError,
    the failed event is skipped and the workflow continues to completion.
    """
    # GIVEN a workflow where a node outputs a generator object
    span_id = uuid4()
    trace_id = uuid4()
    parent_span_id = uuid4()
    request_body = {
        "timeout": 360,
        "execution_id": str(span_id),
        "execution_context": {
            "trace_id": str(trace_id),
            "parent_context": {"span_id": str(parent_span_id)},
        },
        "inputs": [],
        "environment_api_key": "test",
        "module": "workflow",
        "files": {
            "__init__.py": "",
            "workflow.py": """\
from typing import Any, Iterator
from vellum.workflows import BaseWorkflow
from vellum.workflows.nodes import BaseNode


class GeneratorNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        data: Any

    def run(self):
        def my_generator():
            yield 1
            yield 2
            yield 3
        return self.Outputs(data=my_generator())


class Workflow(BaseWorkflow):
    graph = GeneratorNode

    class Outputs(BaseWorkflow.Outputs):
        result = GeneratorNode.Outputs.data
""",
        },
    }

    # WHEN we call the stream route
    status_code, events = both_stream_types(request_body)

    # THEN we get a 200 response
    assert status_code == 200, events

    # AND we should have at least a vembda.execution.initiated event
    event_names = [e["name"] for e in events]
    assert "vembda.execution.initiated" in event_names

    # AND the workflow should complete (either fulfilled or rejected based on workflow logic)
    # The key is that the serialization error doesn't kill the workflow - it just skips the failed event
    assert (
        "workflow.execution.initiated" in event_names
    ), f"Expected workflow.execution.initiated event, got: {event_names}"

    # AND we should have a terminal workflow event (fulfilled or rejected)
    has_terminal_event = "workflow.execution.fulfilled" in event_names or "workflow.execution.rejected" in event_names
    assert has_terminal_event, f"Expected a terminal workflow event (fulfilled or rejected), got: {event_names}"


@mock.patch("workflow_server.api.workflow_view.ENABLE_PROCESS_WRAPPER", False)
def test_stream_workflow_route__serialization_error_skips_event_and_continues():
    """
    Tests that when a PydanticSerializationError occurs during event serialization,
    the failed event is skipped and the workflow continues to completion.
    """
    # GIVEN a valid workflow with a specified workflow_span_id
    workflow_span_id = uuid4()
    trace_id = uuid4()
    parent_span_id = uuid4()
    request_body = {
        "timeout": 360,
        "execution_id": str(uuid4()),
        "workflow_span_id": str(workflow_span_id),
        "execution_context": {
            "trace_id": str(trace_id),
            "parent_context": {"span_id": str(parent_span_id)},
        },
        "inputs": [],
        "environment_api_key": "test",
        "module": "workflow",
        "files": {
            "__init__.py": "",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow


class Workflow(BaseWorkflow):
    class Outputs(BaseWorkflow.Outputs):
        result = "done"
""",
        },
    }

    # AND _dump_event is mocked to raise a PydanticSerializationError on the second call
    # (first call is for vembda.execution.initiated, second is for workflow.execution.initiated)
    # Note: We use the _dump_event imported at the top of this file (before any patching)
    call_count = [0]

    def mock_dump_event(event, executor_context):
        call_count[0] += 1
        if call_count[0] == 2:
            raise PydanticSerializationError("Object of type generator is not JSON serializable")
        return _dump_event(event, executor_context)

    # WHEN we call the stream route with the mocked _dump_event
    flask_app = create_app()
    with flask_app.test_client() as test_client:
        with mock.patch("workflow_server.core.executor._dump_event", side_effect=mock_dump_event):
            response = test_client.post("/workflow/stream", json=request_body)
            status_code = response.status_code

            events = [
                json.loads(line)
                for line in response.data.decode().split("\n")
                if line and line not in ["WAITING", "END"]
            ]

    # THEN we get a 200 response
    assert status_code == 200, events

    # AND we should have at least a vembda.execution.initiated event
    event_names = [e["name"] for e in events]
    assert "vembda.execution.initiated" in event_names

    # AND the workflow should complete with a vembda.execution.fulfilled event
    # (the workflow.execution.fulfilled event may have been skipped due to serialization error)
    assert "vembda.execution.fulfilled" in event_names, f"Expected vembda.execution.fulfilled event, got: {event_names}"

    # AND the workflow.execution.initiated event should still be present (it was the first event, before the error)
    assert (
        "workflow.execution.initiated" in event_names
    ), f"Expected workflow.execution.initiated event, got: {event_names}"
