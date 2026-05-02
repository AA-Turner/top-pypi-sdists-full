import pytest
import logging
import time
from uuid import uuid4

from workflow_server.server import create_app
from workflow_server.utils.system_utils import get_active_process_count


@pytest.fixture(autouse=True)
def drain_background_threads():
    """
    Ensures background threads from previous tests complete before starting the next test.
    This prevents cross-test interference in process count assertions.
    """
    baseline = get_active_process_count()
    yield

    deadline = time.time() + 15
    while time.time() < deadline:
        current_count = get_active_process_count()
        if current_count == baseline:
            break
        time.sleep(0.1)


def test_async_exec_route__happy_path():
    """
    Tests that the async-exec route successfully accepts a valid workflow and returns immediately.
    """
    # GIVEN a Flask application
    flask_app = create_app()

    # AND a valid workflow request
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

    # WHEN we make a request to the async-exec route
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/async-exec", json=request_body)

    # THEN we should get a 200 response
    assert response.status_code == 200

    # AND the response should indicate success
    assert response.json == {"success": True}


def test_async_exec_route__with_inputs():
    """
    Tests that the async-exec route handles workflows with inputs correctly.
    """
    # GIVEN a Flask application
    flask_app = create_app()

    # AND a valid workflow request with inputs
    span_id = uuid4()
    request_body = {
        "execution_id": str(span_id),
        "inputs": [
            {"name": "foo", "type": "STRING", "value": "hello"},
        ],
        "environment_api_key": "test",
        "module": "workflow",
        "timeout": 360,
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

    # WHEN we make a request to the async-exec route
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/async-exec", json=request_body)

    # THEN we should get a 200 response
    assert response.status_code == 200

    # AND the response should indicate success
    assert response.json == {"success": True}


def test_async_exec_route__with_state():
    """
    Tests that the async-exec route handles workflows with state correctly.
    """
    # GIVEN a Flask application
    flask_app = create_app()

    # AND a valid workflow request with state
    span_id = uuid4()
    request_body = {
        "execution_id": str(span_id),
        "state": {"foo": "bar"},
        "environment_api_key": "test",
        "module": "workflow",
        "timeout": 360,
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

    # WHEN we make a request to the async-exec route
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/async-exec", json=request_body)

    # THEN we should get a 200 response
    assert response.status_code == 200

    # AND the response should indicate success
    assert response.json == {"success": True}


def test_async_exec_route__invalid_context():
    """
    Tests that the async-exec route returns 400 for invalid request context.
    """
    # GIVEN a Flask application
    flask_app = create_app()

    # AND an invalid request missing required fields
    request_body = {
        "inputs": [],
    }

    # WHEN we make a request to the async-exec route
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/async-exec", json=request_body)

    # THEN we should get a 400 response
    assert response.status_code == 400

    # AND the response should contain error details
    assert "detail" in response.json
    assert "Invalid context" in response.json["detail"]


def test_async_exec_route__missing_files():
    """
    Tests that the async-exec route returns 400 when files are missing.
    """
    # GIVEN a Flask application
    flask_app = create_app()

    span_id = uuid4()
    request_body = {
        "execution_id": str(span_id),
        "inputs": [],
        "environment_api_key": "test",
        "module": "workflow",
        "timeout": 360,
    }

    # WHEN we make a request to the async-exec route
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/async-exec", json=request_body)

    # THEN we should get a 400 response
    assert response.status_code == 400

    # AND the response should contain error details
    assert "detail" in response.json
    assert "Invalid context" in response.json["detail"]


def test_async_exec_route__with_syntax_error_in_workflow():
    """
    Tests that the async-exec route handles workflows with syntax errors gracefully.
    """
    # GIVEN a Flask application
    flask_app = create_app()

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

class Workflow(BaseWorkflow)
    class Outputs(BaseWorkflow.Outputs):
        foo = "hello"
""",
        },
    }

    # WHEN we make a request to the async-exec route
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/async-exec", json=request_body)

    # THEN we should get a 200 response (async execution is accepted)
    assert response.status_code == 200

    # AND the response should indicate success
    assert response.json == {"success": True}


def test_async_exec_route__with_invalid_inputs():
    """
    Tests that the async-exec route handles workflows with invalid inputs gracefully.
    """
    # GIVEN a Flask application
    flask_app = create_app()

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

    # WHEN we make a request to the async-exec route
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/async-exec", json=request_body)

    # THEN we should get a 200 response (async execution is accepted)
    assert response.status_code == 200

    # AND the response should indicate success
    assert response.json == {"success": True}


def test_async_exec_route__background_thread_completes(caplog):
    """
    Verifies that the async background worker thread runs to completion.
    """
    # GIVEN a Flask application with log capture enabled
    caplog.set_level(logging.INFO, logger="workflow_server.api.workflow_view")
    flask_app = create_app()

    baseline = get_active_process_count()

    # AND a valid workflow request
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

    # WHEN we call the async-exec route
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/async-exec", json=request_body)

    # THEN we get immediate acceptance
    assert response.status_code == 200
    assert response.json == {"success": True}

    # AND the background thread should complete
    completion_deadline = time.time() + 15
    saw_completion_log = False
    while time.time() < completion_deadline:
        if any("Workflow async exec completed" in rec.message for rec in caplog.records):
            saw_completion_log = True
            break
        time.sleep(0.1)

    # THEN we should observe the completion log
    assert saw_completion_log, "Did not observe background completion log within 15 seconds"

    cleanup_deadline = time.time() + 15
    process_count_returned = False
    while time.time() < cleanup_deadline:
        current_count = get_active_process_count()
        if current_count == baseline:
            process_count_returned = True
            break
        time.sleep(0.1)

    current_count = get_active_process_count()
    assert process_count_returned, (
        f"Process count did not return to baseline within 15 seconds after completion log. "
        f"Expected: {baseline}, Current: {current_count}"
    )


def test_async_exec_route__background_thread_completes_on_error(caplog):
    """
    Verifies that the background worker completes even when the workflow fails early.
    """
    # GIVEN a Flask application with log capture enabled
    caplog.set_level(logging.INFO, logger="workflow_server.api.workflow_view")
    flask_app = create_app()

    baseline = get_active_process_count()

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

class Workflow(BaseWorkflow)
    class Outputs(BaseWorkflow.Outputs):
        foo = "hello"
""",
        },
    }

    # WHEN we call the async-exec route
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/async-exec", json=request_body)

    # THEN we get immediate acceptance
    assert response.status_code == 200
    assert response.json == {"success": True}

    # AND the background thread should complete and clean up resources
    deadline = time.time() + 15
    process_count_returned = False
    while time.time() < deadline:
        current_count = get_active_process_count()
        if current_count == baseline:
            process_count_returned = True
            break
        time.sleep(0.1)

    current_count = get_active_process_count()
    assert process_count_returned, (
        f"Process count did not return to baseline on error within 15 seconds. "
        f"Expected: {baseline}, Current: {current_count}"
    )
