import pytest

from deepdiff import DeepDiff

from workflow_server.server import create_app


@pytest.mark.parametrize(
    "type_checker",
    [
        True,
        "zuban",
        "mypy",
    ],
)
def test_serialize_route__with__workflow_type_error(type_checker):
    # GIVEN a Flask application
    flask_app = create_app()

    # AND a complete workflow with multiple files
    workflow_files = {
        "__init__.py": """\
# flake8: noqa: F401, F403
""",
        "inputs.py": """\
from typing import Any, Optional

from vellum.workflows.inputs import BaseInputs


class Inputs(BaseInputs):
    text: str
    var_1: Optional[Any]
""",
        "workflow.py": """\
from vellum.workflows import BaseWorkflow
from vellum.workflows.state import BaseState

from .inputs import Inputs
from .nodes.final_output import FinalOutput
from .nodes.my_custom_node import MyCustomNode


class Workflow(BaseWorkflow[Inputs, BaseState]):
    graph = MyCustomNode >> FinalOutput

    class Outputs(BaseWorkflow.Outputs):
        final_output = FinalOutput.Outputs.value

""",
        "nodes/__init__.py": """\
from .final_output import FinalOutput
from .my_custom_node import MyCustomNode

__all__ = [
    "FinalOutput",
    "MyCustomNode",
]
""",
        "nodes/my_custom_node.py": """\
from vellum.workflows.nodes import BaseNode


class MyCustomNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        value: str

    def run(self) -> Outputs:
        schema_response = (
            self._context.vellum_client.integrations.execute_integration_tool(
                "test_integration_name",
                "test_integration_provider",
                "test_tool_name",
                arguments={
                    "text": "some_text",
                },
                bad_kwarg=None,  # ERROR: Bad kwarg.
            )
        )
        _ = schema_response.output  # ERROR: Invalid attribute.

        return self.Outputs(value=schema_response.provider)
""",
        "nodes/final_output.py": """\
from vellum.workflows.nodes.displayable import FinalOutputNode
from vellum.workflows.state import BaseState

from .my_custom_node import MyCustomNode


class FinalOutput(FinalOutputNode[BaseState, str]):
    class Outputs(FinalOutputNode.Outputs):
        value = MyCustomNode.Outputs.value
""",
    }

    # WHEN we make a request to the serialize route
    with flask_app.test_client() as test_client:
        response = test_client.post(
            "/workflow/serialize",
            json={"files": workflow_files, "run_type_check": type_checker},
        )

    # THEN we should get a successful response
    assert response.status_code == 200

    # AND the response should contain the full WorkflowSerializationResult
    assert "exec_config" in response.json
    assert "errors" in response.json
    assert "dataset" in response.json or response.json.get("dataset") is None
    exec_config = response.json["exec_config"]

    # AND the exec_config should have workflow_raw_data
    assert "workflow_raw_data" in exec_config
    nodes = exec_config["workflow_raw_data"]["nodes"]

    # AND we should find the workflow nodes
    node_labels = {node["data"]["label"] if "data" in node else node["label"] for node in nodes}
    expected_nodes = {"My Custom Node", "Final Output", "Entrypoint Node"}

    assert not DeepDiff(node_labels, expected_nodes, ignore_order=True)

    # AND we should see certain type errors
    expected_type_errors = [
        'nodes/my_custom_node.py:10: error: Unexpected keyword argument "bad_kwarg" for "execute_integration_tool" of "IntegrationsClient"  [call-arg]',  # noqa: E501
        'nodes/my_custom_node.py:20: error: "ComposioExecuteToolResponse" has no attribute "output"  [attr-defined]',  # noqa: E501
    ]
    actual_type_errors = response.json["type_errors"].splitlines()

    assert all(
        expected_type_error in actual_type_errors for expected_type_error in expected_type_errors
    ), actual_type_errors


@pytest.mark.parametrize(
    "type_checker",
    [
        True,
        "zuban",
        "mypy",
    ],
)
def test_type_check__empty_directory(type_checker):
    # Ensure we don't write empty directories as files.

    # GIVEN a Flask application
    flask_app = create_app()

    # AND a complete workflow with multiple files
    workflow_files = {
        "workflow.py": """\
from vellum.workflows import BaseWorkflow
from vellum.workflows.state import BaseState
from vellum.workflows.inputs import BaseInputs

from typing import Optional, Any

class Inputs(BaseInputs):
    text: str
    var_1: Optional[Any]

class Workflow(BaseWorkflow[Inputs, BaseState]):
    pass
""",
        "nodes/execute_code_node/": "",
        "nodes/execute_code_node/scripts/": "",
        "nodes/execute_fixed_code_node/": "",
        "nodes/execute_fixed_code_node/scripts/": "",
        "nodes/output.py": "a: int = '1'",
    }

    # WHEN we make a request to the serialize route
    with flask_app.test_client() as test_client:
        response = test_client.post(
            "/workflow/serialize",
            json={"files": workflow_files, "run_type_check": type_checker},
        )

    # THEN we should get a successful response
    assert response.status_code == 200, response.json

    # AND we should see certain type errors
    actual_type_errors = response.json["type_errors"]
    assert (
        actual_type_errors
        == """\
nodes/output.py:1: error: Incompatible types in assignment (expression has type "str", variable has type "int")  [assignment]
Found 1 error in 1 file (checked 2 source files)
"""
    ), actual_type_errors
