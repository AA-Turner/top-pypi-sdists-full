from uuid import uuid4

from workflow_server.server import create_app


def test_input_conversion_with_display_mapping():
    """
    Test that validates input conversion behavior for future WorkflowDisplay refactor.

    This test demonstrates the expected behavior when inputs are converted from UI names
    to SDK attribute names using WorkflowDisplay's inputs_display mapping, rather than
    the current snake_case conversion approach.

    The test passes on main branch by using the current conversion logic, but establishes
    the expected input/output patterns for the future refactor.
    """
    span_id = uuid4()
    request_body = {
        "execution_id": str(span_id),
        "inputs": [
            {"name": "User Message", "type": "STRING", "value": "Hello world"},
            {"name": "123-config", "type": "STRING", "value": "config-value"},
            {"name": "API-Key", "type": "STRING", "value": "test-key"},
        ],
        "environment_api_key": "test",
        "module": "workflow",
        "timeout": 360,
        "files": {
            "__init__.py": "",
            "workflow.py": """
from vellum.workflows import BaseWorkflow
from vellum.workflows.state import BaseState
from .inputs import Inputs

class Workflow(BaseWorkflow[Inputs, BaseState]):
    class Outputs(BaseWorkflow.Outputs):
        result = "success"
""",
            "inputs.py": """
from vellum.workflows.inputs import BaseInputs

class Inputs(BaseInputs):
    user_message: str
    input_123_config: str
    api_key: str
""",
        },
    }

    flask_app = create_app()
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/stream", json=request_body)
        status_code = response.status_code

    assert status_code == 200, f"Request failed with status {status_code}: {response.data}"

    response_lines = [line for line in response.data.decode().split("\n") if line and line not in ["WAITING", "END"]]
    assert len(response_lines) > 0, "No response events received"

    fulfilled_events = [line for line in response_lines if "workflow.execution.fulfilled" in line]
    assert len(fulfilled_events) > 0, "No workflow.execution.fulfilled event received"
