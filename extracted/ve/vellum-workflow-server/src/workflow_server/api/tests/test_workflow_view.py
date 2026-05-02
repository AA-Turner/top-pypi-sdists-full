import json
import logging
import re
from unittest.mock import patch
from uuid import UUID, uuid4

from deepdiff import DeepDiff

from workflow_server.server import create_app


def test_version_route():
    flask_app = create_app()

    with flask_app.test_client() as test_client:
        response = test_client.get("/workflow/version")
        assert response.status_code == 200
        assert re.match(r"[0-9]*\.[0-9]*\.[0-9]*", response.json["sdk_version"])
        assert response.json["server_version"] == "local"


def test_version_route__with_single_node_file(tmp_path):
    # GIVEN a temporary custom_nodes directory with a test node
    custom_nodes_dir = tmp_path / "vellum_custom_nodes"
    custom_nodes_dir.mkdir()

    node_file = custom_nodes_dir / "test_node.py"
    node_file.write_text(
        """
from vellum.workflows.nodes import BaseNode

class TestNode(BaseNode):
    \"""A test node for processing data.\"""
"""
    )

    flask_app = create_app()

    # WHEN we make a request to the version route
    with patch("os.getcwd", return_value=str(tmp_path)), flask_app.test_client() as test_client:
        response = test_client.get("/workflow/version")

    # THEN we should get a successful response
    assert response.status_code == 200

    # AND we should find exactly one node
    nodes = response.json["nodes"]
    assert len(nodes) == 1

    # AND the node should have the correct metadata
    node = nodes[0]
    assert UUID(node["id"])
    assert node["module"] == ["vellum_custom_nodes", "test_node"]
    assert node["name"] == "TestNode"
    assert node["label"] == "Test Node"
    assert "A test node for processing data." in node["description"]
    assert node["exec_config"] == {
        "adornments": None,
        "attributes": [],
        "base": {"module": ["vellum", "workflows", "nodes", "bases", "base"], "name": "BaseNode"},
        "definition": {"module": ["vellum_custom_nodes", "test_node"], "name": "TestNode"},
        "display_data": {
            "comment": {"expanded": True, "value": "A test node for processing data."},
            "position": {"x": 0.0, "y": 0.0},
        },
        "id": "6f4c9178-9f46-4723-bcb7-0bd59db54eca",
        "label": "Test Node",
        "outputs": [],
        "ports": [{"id": "4394823f-79a8-4dbc-99ae-06a1df6c7408", "name": "default", "type": "DEFAULT"}],
        "trigger": {"id": "07240af1-67c6-4460-b53d-53f0b0f1b90e", "merge_behavior": "AWAIT_ATTRIBUTES"},
        "type": "GENERIC",
    }


def test_version_route__with_nodes_in_multiple_files(tmp_path):
    # GIVEN a temporary custom_nodes directory
    custom_nodes_dir = tmp_path / "vellum_custom_nodes"
    custom_nodes_dir.mkdir()

    # AND a first node file
    first_node_file = custom_nodes_dir / "first_node.py"
    first_node_file.write_text(
        """
from vellum.workflows.nodes import BaseNode

class SomeNode(BaseNode):
    \"""This is Some Node.\"""
"""
    )

    # AND a second node file
    second_node_file = custom_nodes_dir / "second_node.py"
    second_node_file.write_text(
        """
from vellum.workflows.nodes import BaseNode

class SomeOtherNode(BaseNode):
    \"""This is Some Other Node.\"""
"""
    )

    flask_app = create_app()

    # WHEN we make a request to the version route
    with patch("os.getcwd", return_value=str(tmp_path)), flask_app.test_client() as test_client:
        response = test_client.get("/workflow/version")

    # THEN we should get a successful response
    assert response.status_code == 200

    # AND we should find both nodes
    nodes = response.json["nodes"]
    assert len(nodes) == 2

    # AND the first node should have correct metadata
    some_node = nodes[0]
    assert some_node["label"] == "Some Node"
    assert some_node["description"] == "This is Some Node."
    assert UUID(some_node["id"])
    assert some_node["module"] == ["vellum_custom_nodes", "first_node"]
    assert some_node["exec_config"] == {
        "adornments": None,
        "attributes": [],
        "base": {"module": ["vellum", "workflows", "nodes", "bases", "base"], "name": "BaseNode"},
        "definition": {"module": ["vellum_custom_nodes", "first_node"], "name": "SomeNode"},
        "display_data": {
            "comment": {"expanded": True, "value": "This is Some Node."},
            "position": {"x": 0.0, "y": 0.0},
        },
        "id": "89e84bac-5a5f-4f64-8083-7d3ebec98be1",
        "label": "Some Node",
        "outputs": [],
        "ports": [{"id": "2983ea5c-1d29-483a-b896-53098f5de4f1", "name": "default", "type": "DEFAULT"}],
        "trigger": {"id": "6996efb0-5a20-4719-8835-34fe6552764a", "merge_behavior": "AWAIT_ATTRIBUTES"},
        "type": "GENERIC",
    }

    # AND the second node should have correct metadata
    some_other_node = nodes[1]
    assert some_other_node["label"] == "Some Other Node"
    assert some_other_node["description"] == "This is Some Other Node."
    assert UUID(some_other_node["id"])
    assert some_other_node["module"] == ["vellum_custom_nodes", "second_node"]
    assert some_other_node["exec_config"] == {
        "adornments": None,
        "attributes": [],
        "base": {"module": ["vellum", "workflows", "nodes", "bases", "base"], "name": "BaseNode"},
        "definition": {"module": ["vellum_custom_nodes", "second_node"], "name": "SomeOtherNode"},
        "display_data": {
            "comment": {"expanded": True, "value": "This is Some Other Node."},
            "position": {"x": 0.0, "y": 0.0},
        },
        "id": "3cdbba02-8a34-4e0f-8b94-770a944dcaa3",
        "label": "Some Other Node",
        "outputs": [],
        "ports": [{"id": "1839bde5-2ad4-4723-b21b-2c55fa833a7a", "name": "default", "type": "DEFAULT"}],
        "trigger": {"id": "c36df8a8-5624-45be-99c9-826cf511a951", "merge_behavior": "AWAIT_ATTRIBUTES"},
        "type": "GENERIC",
    }


def test_version_route__no_custom_nodes_dir(tmp_path):
    # GIVEN a Flask application and an empty temp directory
    flask_app = create_app()

    # WHEN we make a request to the version route
    with patch("os.getcwd", return_value=str(tmp_path)), flask_app.test_client() as test_client:
        response = test_client.get("/workflow/version")

    # THEN we should get a successful response
    assert response.status_code == 200

    # AND the nodes list should be empty
    assert response.json["nodes"] == []


def test_version_route__with_multiple_nodes_in_file(tmp_path):
    # Create a temporary custom_nodes directory with multiple nodes in one file
    custom_nodes_dir = tmp_path / "vellum_custom_nodes"
    custom_nodes_dir.mkdir()

    # Create a test node file with multiple nodes
    node_file = custom_nodes_dir / "multiple_nodes.py"
    node_file.write_text(
        """
from vellum.workflows.nodes import BaseNode

class ProcessingNode(BaseNode):
    \"""Processes input data.\"""

class TransformationNode(BaseNode):
    \"""Transforms data format.\"""

# This class should not be discovered
class HelperClass:
    pass
"""
    )

    flask_app = create_app()

    # Mock the current working directory to point to our temp directory
    with patch("os.getcwd", return_value=str(tmp_path)), flask_app.test_client() as test_client:
        response = test_client.get("/workflow/version")

        assert response.status_code == 200
        nodes = response.json["nodes"]
        assert len(nodes) == 2

        # Nodes should be discovered regardless of their order in the file
        node_names = {node["name"] for node in nodes}
        assert node_names == {"ProcessingNode", "TransformationNode"}

        # Find and assert each node individually
        processing_node = next(node for node in nodes if node["name"] == "ProcessingNode")
        assert processing_node["exec_config"] == {
            "adornments": None,
            "attributes": [],
            "base": {"module": ["vellum", "workflows", "nodes", "bases", "base"], "name": "BaseNode"},
            "definition": {"module": ["vellum_custom_nodes", "multiple_nodes"], "name": "ProcessingNode"},
            "display_data": {
                "comment": {"expanded": True, "value": "Processes input data."},
                "position": {"x": 0.0, "y": 0.0},
            },
            "id": "7121bcb9-98a1-4907-bf9b-9734d773fd15",
            "label": "Processing Node",
            "outputs": [],
            "ports": [{"id": "de27da74-30e9-4e7b-95c2-92bdfc5bf042", "name": "default", "type": "DEFAULT"}],
            "trigger": {"id": "e02bd85e-8b03-4b21-8b3e-f411042334ce", "merge_behavior": "AWAIT_ATTRIBUTES"},
            "type": "GENERIC",
        }

        transformation_node = next(node for node in nodes if node["name"] == "TransformationNode")
        assert transformation_node["exec_config"] == {
            "adornments": None,
            "attributes": [],
            "base": {"module": ["vellum", "workflows", "nodes", "bases", "base"], "name": "BaseNode"},
            "definition": {"module": ["vellum_custom_nodes", "multiple_nodes"], "name": "TransformationNode"},
            "display_data": {
                "comment": {"expanded": True, "value": "Transforms data format."},
                "position": {"x": 0.0, "y": 0.0},
            },
            "id": "6a785cb0-f631-4f03-94c6-e82331c14c1a",
            "label": "Transformation Node",
            "outputs": [],
            "ports": [{"id": "67a13ea0-fd6b-44dc-af46-c72da06aa11f", "name": "default", "type": "DEFAULT"}],
            "trigger": {"id": "08d4e317-baa8-478f-b278-99362e50e6b4", "merge_behavior": "AWAIT_ATTRIBUTES"},
            "type": "GENERIC",
        }


def test_version_route__with_invalid_node_file(tmp_path, caplog):
    caplog.set_level(logging.WARNING)

    # GIVEN a temporary custom_nodes directory
    custom_nodes_dir = tmp_path / "vellum_custom_nodes"
    custom_nodes_dir.mkdir()

    # AND a valid node file
    valid_node_file = custom_nodes_dir / "valid_node.py"
    valid_node_file.write_text(
        """
from vellum.workflows.nodes import BaseNode

class SomeNode(BaseNode):
    \"\"\"This is Some Node.\"\"\"
"""
    )

    # AND an invalid node file with syntax error of missing colon in the class
    invalid_node_file = custom_nodes_dir / "invalid_node.py"
    invalid_node_file.write_text(
        """
from vellum.workflows.nodes import BaseNode

class BrokenNode(BaseNode)
    \"\"\"This node has a syntax error.\"\"\"
"""
    )

    flask_app = create_app()

    # WHEN we make a request to the version route
    with patch("os.getcwd", return_value=str(tmp_path)), flask_app.test_client() as test_client:
        response = test_client.get("/workflow/version")

    # THEN we should get a successful response
    assert response.status_code == 200

    # AND we should find only the valid node
    nodes = response.json["nodes"]
    assert len(nodes) == 1

    # AND the valid node should have correct metadata
    valid_node = nodes[0]
    assert valid_node["label"] == "Some Node"
    assert valid_node["description"] == "This is Some Node."
    assert UUID(valid_node["id"])
    assert valid_node["module"] == ["vellum_custom_nodes", "valid_node"]
    assert valid_node["exec_config"] == {
        "adornments": None,
        "attributes": [],
        "base": {"module": ["vellum", "workflows", "nodes", "bases", "base"], "name": "BaseNode"},
        "definition": {"module": ["vellum_custom_nodes", "valid_node"], "name": "SomeNode"},
        "display_data": {
            "comment": {"expanded": True, "value": "This is Some Node."},
            "position": {"x": 0.0, "y": 0.0},
        },
        "id": "a2706730-074b-4ea3-968a-25e68af1caed",
        "label": "Some Node",
        "outputs": [],
        "ports": [{"id": "e0ee3653-e071-4b91-9dfc-5e1dca9c665b", "name": "default", "type": "DEFAULT"}],
        "trigger": {"id": "8d931b01-30ca-4c0d-b1b7-7c18379c83e6", "merge_behavior": "AWAIT_ATTRIBUTES"},
        "type": "GENERIC",
    }

    # AND the error should be logged with full traceback
    assert len(caplog.records) > 0
    error_message = caplog.records[0].message
    assert "Failed to load node from module invalid_node" in error_message
    assert "invalid_node.py, line 4" in error_message


def test_version_route__with_attributes(tmp_path):
    # GIVEN a temporary custom_nodes directory
    custom_nodes_dir = tmp_path / "vellum_custom_nodes"
    custom_nodes_dir.mkdir()

    # AND an addition node file
    node_file = custom_nodes_dir / "addition_node.py"
    node_file.write_text(
        """
from vellum.workflows.nodes import BaseNode


class MyAdditionNode(BaseNode):
    \"\"\"Custom node that performs simple addition.\"\"\"
    arg1: int
    arg2: int

    class Outputs(BaseNode.Outputs):
        result: int

    def run(self) -> BaseNode.Outputs:
        result = self.arg1 + self.arg2
        return self.Outputs(result=result)
"""
    )

    flask_app = create_app()

    # WHEN we make a request to the version route
    with patch("os.getcwd", return_value=str(tmp_path)), flask_app.test_client() as test_client:
        response = test_client.get("/workflow/version")

    # THEN we should get a successful response
    assert response.status_code == 200

    # AND we should find the addition node
    nodes = response.json["nodes"]
    assert len(nodes) == 1

    # AND the node should have the correct metadata
    node = nodes[0]
    assert node["label"] == "My Addition Node"
    assert node["description"] == "Custom node that performs simple addition."
    assert UUID(node["id"])
    assert node["module"] == ["vellum_custom_nodes", "addition_node"]
    assert node["name"] == "MyAdditionNode"
    assert node["exec_config"] == {
        "adornments": None,
        "attributes": [
            {
                "id": "4223b340-447f-46c2-b35d-30ef16c5ae17",
                "name": "arg1",
                "value": None,
            },
            {
                "id": "1de0f46a-95f6-4cd0-bb0f-e2414054d507",
                "name": "arg2",
                "value": None,
            },
        ],
        "base": {"module": ["vellum", "workflows", "nodes", "bases", "base"], "name": "BaseNode"},
        "definition": {"module": ["vellum_custom_nodes", "addition_node"], "name": "MyAdditionNode"},
        "display_data": {
            "comment": {"expanded": True, "value": "Custom node that performs simple addition."},
            "position": {"x": 0.0, "y": 0.0},
        },
        "id": "2464b610-fb6d-495b-b17c-933ee147f19f",
        "label": "My Addition Node",
        "outputs": [
            {
                "id": "f39d85c9-e7bf-45e1-bb67-f16225db0118",
                "name": "result",
                "type": "NUMBER",
                "value": None,
                "schema": {"type": "integer"},
            }
        ],
        "ports": [{"id": "bc489295-cd8a-4aa2-88bb-34446374100d", "name": "default", "type": "DEFAULT"}],
        "trigger": {"id": "ff580cad-73d6-44fe-8f2c-4b8dc990ee70", "merge_behavior": "AWAIT_ATTRIBUTES"},
        "type": "GENERIC",
        "should_file_merge": True,
    }


def test_serialize_route__with_no_files():
    # GIVEN a Flask application
    flask_app = create_app()

    # WHEN we make a request with no files
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/serialize", json={"files": {}})

    # THEN we should get a bad request response
    assert response.status_code == 400

    # AND the response should contain an error message
    assert "detail" in response.json
    assert "No files received" in response.json["detail"]


def test_serialize_route__with_invalid_python_syntax():
    # GIVEN a Flask application
    flask_app = create_app()

    # AND a file with invalid Python syntax
    invalid_content = """
from vellum.workflows.nodes import BaseNode

class BrokenNode(BaseNode)  # Missing colon
    \"\"\"This node has a syntax error.\"\"\"
"""

    # WHEN we make a request to the serialize route
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/serialize", json={"files": {"broken_node.py": invalid_content}})

    # THEN we should get a 400 response
    assert response.status_code == 400

    # AND the response should contain an error message
    assert "detail" in response.json
    assert "Serialization failed" in response.json["detail"]


def test_serialize_route__with__workflow():
    # GIVEN a Flask application
    flask_app = create_app()

    # AND a complete workflow with multiple files
    workflow_files = {
        "__init__.py": "# flake8: noqa: F401, F403\n\n",
        "inputs.py": "from typing import Any, Optional\n\nfrom vellum.workflows.inputs import BaseInputs\n\n\nclass Inputs(BaseInputs):\n    text: str\n    var_1: Optional[Any]\n",  # noqa: E501
        "workflow.py": "from vellum.workflows import BaseWorkflow\nfrom vellum.workflows.state import BaseState\n\nfrom .inputs import Inputs\nfrom .nodes.final_output import FinalOutput\nfrom .nodes.templating_node import TemplatingNode\n\n\nclass Workflow(BaseWorkflow[Inputs, BaseState]):\n    graph = TemplatingNode >> FinalOutput\n\n    class Outputs(BaseWorkflow.Outputs):\n        final_output = FinalOutput.Outputs.value\n",  # noqa: E501
        "nodes/__init__.py": 'from .final_output import FinalOutput\nfrom .templating_node import TemplatingNode\n\n__all__ = [\n    "FinalOutput",\n    "TemplatingNode",\n]\n',  # noqa: E501
        "nodes/templating_node.py": 'from vellum.workflows.nodes.displayable import TemplatingNode as BaseTemplatingNode\nfrom vellum.workflows.state import BaseState\n\nfrom ..inputs import Inputs\n\n\nclass TemplatingNode(BaseTemplatingNode[BaseState, str]):\n    template = """{{ text }}"""\n    inputs = {\n        "text": Inputs.text,\n    }\n',  # noqa: E501
        "nodes/final_output.py": "from vellum.workflows.nodes.displayable import FinalOutputNode\nfrom vellum.workflows.state import BaseState\n\nfrom .templating_node import TemplatingNode\n\n\nclass FinalOutput(FinalOutputNode[BaseState, str]):\n    class Outputs(FinalOutputNode.Outputs):\n        value = TemplatingNode.Outputs.result\n",  # noqa: E501
    }

    # WHEN we make a request to the serialize route
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/serialize", json={"files": workflow_files})

    # THEN we should get a successful response
    assert response.status_code == 200

    # AND the response should contain the full WorkflowSerializationResult
    assert "exec_config" in response.json
    assert "errors" in response.json
    assert "dataset" in response.json or response.json.get("dataset") is None
    assert "type_errors" not in response.json
    assert "type_checker_failure" not in response.json
    exec_config = response.json["exec_config"]

    # AND the exec_config should have workflow_raw_data
    assert "workflow_raw_data" in exec_config
    nodes = exec_config["workflow_raw_data"]["nodes"]

    # AND we should find the workflow nodes
    node_labels = {node["data"]["label"] for node in nodes}
    expected_nodes = {"Templating Node", "Final Output", "Entrypoint Node"}

    # AND at least some of the expected nodes should be present
    assert not DeepDiff(node_labels, expected_nodes, ignore_order=True)


def test_serialize_route__with_workspace_api_key():
    """
    Tests that the serialize route accepts workspace_api_key and passes it through serialization.
    """
    # GIVEN a Flask application
    flask_app = create_app()

    # AND a complete workflow with multiple files
    workflow_files = {
        "__init__.py": "# flake8: noqa: F401, F403\n\n",
        "inputs.py": "from typing import Any, Optional\n\nfrom vellum.workflows.inputs import BaseInputs\n\n\nclass Inputs(BaseInputs):\n    text: str\n    var_1: Optional[Any]\n",  # noqa: E501
        "workflow.py": "from vellum.workflows import BaseWorkflow\nfrom vellum.workflows.state import BaseState\n\nfrom .inputs import Inputs\nfrom .nodes.final_output import FinalOutput\nfrom .nodes.templating_node import TemplatingNode\n\n\nclass Workflow(BaseWorkflow[Inputs, BaseState]):\n    graph = TemplatingNode >> FinalOutput\n\n    class Outputs(BaseWorkflow.Outputs):\n        final_output = FinalOutput.Outputs.value\n",  # noqa: E501
        "nodes/__init__.py": 'from .final_output import FinalOutput\nfrom .templating_node import TemplatingNode\n\n__all__ = [\n    "FinalOutput",\n    "TemplatingNode",\n]\n',  # noqa: E501
        "nodes/templating_node.py": 'from vellum.workflows.nodes.displayable import TemplatingNode as BaseTemplatingNode\nfrom vellum.workflows.state import BaseState\n\nfrom ..inputs import Inputs\n\n\nclass TemplatingNode(BaseTemplatingNode[BaseState, str]):\n    template = """{{ text }}"""\n    inputs = {\n        "text": Inputs.text,\n    }\n',  # noqa: E501
        "nodes/final_output.py": "from vellum.workflows.nodes.displayable import FinalOutputNode\nfrom vellum.workflows.state import BaseState\n\nfrom .templating_node import TemplatingNode\n\n\nclass FinalOutput(FinalOutputNode[BaseState, str]):\n    class Outputs(FinalOutputNode.Outputs):\n        value = TemplatingNode.Outputs.result\n",  # noqa: E501
    }

    # WHEN we make a request to the serialize route with workspace_api_key
    with flask_app.test_client() as test_client:
        response = test_client.post(
            "/workflow/serialize", json={"files": workflow_files, "workspace_api_key": "test_workspace_key"}
        )

    # THEN we should get a successful response
    assert response.status_code == 200

    # AND the response should contain the full WorkflowSerializationResult
    assert "exec_config" in response.json
    assert "errors" in response.json


def test_serialize_route__with_invalid_workspace_api_key():
    """
    Tests that the serialize route handles invalid workspace_api_key gracefully.
    """
    # GIVEN a Flask application
    flask_app = create_app()

    workflow_files = {
        "__init__.py": "",
        "workflow.py": (
            "from vellum.workflows import BaseWorkflow\n\n"
            "class Workflow(BaseWorkflow):\n"
            "    class Outputs(BaseWorkflow.Outputs):\n"
            "        foo = 'hello'\n"
        ),
    }

    # WHEN we make a request with an invalid workspace_api_key
    with flask_app.test_client() as test_client:
        response = test_client.post(
            "/workflow/serialize", json={"files": workflow_files, "workspace_api_key": ""}  # Invalid empty key
        )

    # THEN we should still get a successful response (graceful degradation)
    assert response.status_code == 200

    # AND the response should contain the serialization result
    assert "exec_config" in response.json


def test_serialize_route__with_is_new_server_header():
    """
    Tests that the serialize route returns the is_new_server header.
    """
    # GIVEN a Flask application
    flask_app = create_app()

    workflow_files = {
        "__init__.py": "",
        "workflow.py": (
            "from vellum.workflows import BaseWorkflow\n\n"
            "class Workflow(BaseWorkflow):\n"
            "    class Outputs(BaseWorkflow.Outputs):\n"
            "        foo = 'hello'\n"
        ),
    }

    # WHEN we make a request with is_new_server=True
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/serialize", json={"files": workflow_files, "is_new_server": True})

    # THEN we should get a successful response
    assert response.status_code == 200

    # AND the response should contain the is_new_server header set to true
    assert "X-Vellum-Is-New-Server" in response.headers
    assert response.headers["X-Vellum-Is-New-Server"] == "true"

    # WHEN we make a request with is_new_server=False
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/serialize", json={"files": workflow_files, "is_new_server": False})

    # THEN we should get a successful response
    assert response.status_code == 200

    # AND the response should contain the is_new_server header set to false
    assert "X-Vellum-Is-New-Server" in response.headers
    assert response.headers["X-Vellum-Is-New-Server"] == "false"

    # WHEN we make a request without is_new_server
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/serialize", json={"files": workflow_files})

    # THEN we should get a successful response
    assert response.status_code == 200

    # AND the response should contain the is_new_server header set to false (default)
    assert "X-Vellum-Is-New-Server" in response.headers
    assert response.headers["X-Vellum-Is-New-Server"] == "false"


def test_stream_node_route__with_node_id():
    """
    Tests that the stream-node endpoint works with node_id.
    """
    # GIVEN a valid request body with node_id
    node_id = uuid4()
    span_id = uuid4()
    request_body = {
        "timeout": 360,
        "execution_id": str(span_id),
        "node_id": str(node_id),
        "inputs": [],
        "environment_api_key": "test",
        "module": "workflow",
        "files": {
            "__init__.py": "from .display import *",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow
from .nodes.test_node import TestNode

class Workflow(BaseWorkflow):
    graph = TestNode

    class Outputs(BaseWorkflow.Outputs):
        result = TestNode.Outputs.value
""",
            "nodes/__init__.py": "from .test_node import TestNode\n__all__ = ['TestNode']",
            "nodes/test_node.py": """\
from vellum.workflows.nodes import BaseNode

class TestNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        value = "test_result"
""",
            "display/__init__.py": "from .nodes import *\nfrom .workflow import *",
            "display/workflow.py": """\
from vellum_ee.workflows.display.workflows import BaseWorkflowDisplay
""",
            "display/nodes/__init__.py": "from .test_node import TestNodeDisplay\n__all__ = ['TestNodeDisplay']",
            "display/nodes/test_node.py": f"""\
from uuid import UUID
from vellum_ee.workflows.display.nodes import BaseNodeDisplay
from ...nodes.test_node import TestNode

class TestNodeDisplay(BaseNodeDisplay[TestNode]):
    node_id = UUID("{node_id}")
""",
        },
    }

    flask_app = create_app()

    # WHEN we call the stream-node route
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/stream-node", json=request_body)

    # THEN we get a 200 response
    assert response.status_code == 200

    events = [json.loads(line) for line in response.data.decode().strip().split("\n") if line.strip()]
    assert len(events) == 4
    assert events[0]["name"] == "vembda.execution.initiated"
    assert events[1]["name"] == "node.execution.initiated"
    assert events[2]["name"] == "node.execution.fulfilled"
    assert events[3]["name"] == "vembda.execution.fulfilled"


def test_stream_node_route__with_node_module_and_name_backward_compatibility():
    """
    Tests that the stream-node endpoint still works with node_module and node_name for backward compatibility.
    """
    # GIVEN a valid request body with node_module and node_name (old format)
    span_id = uuid4()
    request_body = {
        "timeout": 360,
        "execution_id": str(span_id),
        "node_module": "nodes.test_node",
        "node_name": "TestNode",
        "inputs": [],
        "environment_api_key": "test",
        "module": "workflow",
        "files": {
            "__init__.py": "",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow
from .nodes.test_node import TestNode

class Workflow(BaseWorkflow):
    graph = TestNode
""",
            "nodes/__init__.py": "from .test_node import TestNode",
            "nodes/test_node.py": """\
from vellum.workflows.nodes import BaseNode

class TestNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        value = "test_result"
""",
        },
    }

    flask_app = create_app()

    # WHEN we call the stream-node route
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/stream-node", json=request_body)

    # THEN we get a 200 response
    assert response.status_code == 200

    events = [json.loads(line) for line in response.data.decode().strip().split("\n") if line.strip()]
    assert events[0]["name"] == "vembda.execution.initiated"
    assert events[1]["name"] == "node.execution.initiated", json.dumps(events[1]["body"])
    assert events[2]["name"] == "node.execution.fulfilled"
    assert events[3]["name"] == "vembda.execution.fulfilled"
    assert len(events) == 4


def test_stream_node_route__missing_node_info_validation():
    """
    Tests that the stream-node endpoint returns validation error when neither
    node_id nor node_module/node_name are provided.
    """
    # GIVEN a request body missing node identification
    span_id = uuid4()
    request_body = {
        "timeout": 360,
        "execution_id": str(span_id),
        "inputs": [],
        "environment_api_key": "test",
        "module": "workflow",
        "files": {"__init__.py": "", "workflow.py": ""},
    }

    flask_app = create_app()

    # WHEN we call the stream-node route
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/stream-node", json=request_body)

    # THEN we get a 400 response
    assert response.status_code == 400

    # AND we get a validation error message
    assert "Either node_id or both node_module and node_name must be provided" in response.get_json()["detail"]


def test_stream_node_route__invalid_node_id():
    """
    Tests that the stream-node endpoint returns 404 for invalid node_id.
    """
    # GIVEN a request body with invalid node_id
    invalid_node_id = uuid4()
    span_id = uuid4()
    request_body = {
        "timeout": 360,
        "execution_id": str(span_id),
        "node_id": str(invalid_node_id),
        "inputs": [],
        "environment_api_key": "test",
        "module": "workflow",
        "files": {
            "__init__.py": "",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow

class Workflow(BaseWorkflow):
    pass
""",
        },
    }

    flask_app = create_app()

    # WHEN we call the stream-node route
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/stream-node", json=request_body)

    # THEN we get a 200 response
    # TODO: In the future, we would want this to return a 4xx response by returning the workflow
    # instance and the node definition that we want to run as part of request deserialization.
    assert response.status_code == 200, response.text

    # AND we get an appropriate error message
    # TODO: In a future where we are returning 4xx responses, we assert the following data:
    # response_data = response.get_json()
    # assert "Node with ID" in response_data["detail"]
    # assert "not found" in response_data["detail"]
    events = [json.loads(line) for line in response.data.decode().strip().split("\n") if line.strip()]
    assert events[0]["name"] == "vembda.execution.initiated"
    assert events[1]["name"] == "vembda.execution.fulfilled"
    assert len(events) == 2


def test_serialize_route__with_invalid_nested_set_graph():
    """
    Tests that a workflow with an invalid nested set graph structure raises a clear user-facing exception.
    """
    # GIVEN a Flask application
    flask_app = create_app()

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

    workflow_files = {
        "__init__.py": "",
        "workflow.py": invalid_workflow_content,
    }

    # WHEN we make a request to the serialize route
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/serialize", json={"files": workflow_files})

    # THEN we should get a 400 response
    assert response.status_code == 400

    # AND the response should contain a user-friendly error message
    assert "detail" in response.json
    error_detail = response.json["detail"]
    assert "Serialization failed" in error_detail
    assert "Invalid graph structure detected" in error_detail
    assert "contact Vellum support" in error_detail
