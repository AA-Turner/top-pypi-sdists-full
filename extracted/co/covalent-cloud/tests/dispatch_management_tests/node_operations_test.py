# Copyright 2025 Agnostiq Inc.

"""Unit tests for node operations in dispatch management."""

from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from covalent_cloud.dispatch_management.node_operations import (
    get_first_failure,
    get_node_errors,
    get_node_results,
    get_node_stderr,
    get_node_stdout,
)
from covalent_cloud.shared.classes.exceptions import AuthenticationError, ResourceNotFoundError
from covalent_cloud.shared.classes.settings import Settings
from covalent_cloud.shared.schemas.node import (
    NodeError,
    NodeFailure,
    NodeOutput,
    NodeResult,
    NodeStderr,
)


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    settings = Settings()
    settings.dispatcher_uri = "https://api.dev.covalent.xyz"
    return settings


@pytest.fixture
def mock_transport_graph():
    """Mock transport graph with sample nodes."""
    mock_tg = MagicMock()
    mock_tg._graph.nodes = [0, 1, 2, 3]

    # Mock node data
    node_data = {
        0: {"name": "setup", "status": "COMPLETED", "output": MagicMock()},
        1: {"name": "calculate", "status": "COMPLETED", "output": MagicMock()},
        2: {"name": "calculate", "status": "FAILED", "output": None},
        3: {"name": "finalize", "status": "PENDING", "output": None},
    }

    # Mock get_node_value method
    def mock_get_node_value(node_id, attribute):
        return node_data[node_id].get(attribute)

    mock_tg.get_node_value = mock_get_node_value

    # Mock result loading
    node_data[0]["output"].load.return_value = {"setup": "complete"}
    node_data[1]["output"].load.return_value = 42

    return mock_tg


@pytest.fixture
def mock_result_manager(mock_transport_graph):
    """Mock result manager with populated result object."""
    mock_rm = MagicMock()
    mock_result_object = MagicMock()
    mock_lattice = MagicMock()
    mock_lattice.transport_graph = mock_transport_graph
    mock_result_object.lattice = mock_lattice
    mock_rm.result_object = mock_result_object
    return mock_rm


class TestGetNodeResults:
    """Test cases for get_node_results function."""

    @patch("covalent_cloud.dispatch_management.node_operations.rm.get_result_manager")
    def test_get_all_node_results_success(self, mock_get_rm, mock_result_manager, mock_settings):
        """Test getting results for all nodes successfully."""
        mock_get_rm.return_value = mock_result_manager

        results = get_node_results("test-dispatch-123", node=None, settings=mock_settings)

        assert len(results) == 4
        assert all(isinstance(result, NodeResult) for result in results)

        # Check first two results have actual data
        assert results[0].node_id == 0
        assert results[0].function_name == "setup"
        assert results[0].result == {"setup": "complete"}
        assert results[0].status == "COMPLETED"

        assert results[1].node_id == 1
        assert results[1].function_name == "calculate"
        assert results[1].result == 42
        assert results[1].status == "COMPLETED"

    @patch("covalent_cloud.dispatch_management.node_operations.rm.get_result_manager")
    def test_get_node_results_by_id(self, mock_get_rm, mock_result_manager, mock_settings):
        """Test getting results for a specific node ID."""
        mock_get_rm.return_value = mock_result_manager

        results = get_node_results("test-dispatch-123", node=1, settings=mock_settings)

        assert len(results) == 1
        assert results[0].node_id == 1
        assert results[0].function_name == "calculate"
        assert results[0].result == 42

    @patch("covalent_cloud.dispatch_management.node_operations.rm.get_result_manager")
    def test_get_node_results_by_function_name(
        self, mock_get_rm, mock_result_manager, mock_settings
    ):
        """Test getting results for nodes with specific function name."""
        mock_get_rm.return_value = mock_result_manager

        results = get_node_results("test-dispatch-123", node="calculate", settings=mock_settings)

        # Should return both nodes with function name "calculate"
        assert len(results) == 2
        assert results[0].node_id == 1
        assert results[0].function_name == "calculate"
        assert results[1].node_id == 2
        assert results[1].function_name == "calculate"

    @patch("covalent_cloud.dispatch_management.node_operations.rm.get_result_manager")
    def test_get_node_results_invalid_node_id(
        self, mock_get_rm, mock_result_manager, mock_settings
    ):
        """Test getting results for non-existent node ID."""
        mock_get_rm.return_value = mock_result_manager

        with pytest.raises(ResourceNotFoundError, match="Node 99 not found in dispatch"):
            get_node_results("test-dispatch-123", node=99, settings=mock_settings)

    @patch("covalent_cloud.dispatch_management.node_operations.rm.get_result_manager")
    def test_get_node_results_invalid_function_name(
        self, mock_get_rm, mock_result_manager, mock_settings
    ):
        """Test getting results for non-existent function name."""
        mock_get_rm.return_value = mock_result_manager

        with pytest.raises(
            ResourceNotFoundError, match="No nodes found with function name 'nonexistent'"
        ):
            get_node_results("test-dispatch-123", node="nonexistent", settings=mock_settings)

    @patch("covalent_cloud.dispatch_management.node_operations.rm.get_result_manager")
    def test_get_node_results_dispatch_not_found(self, mock_get_rm, mock_settings):
        """Test handling dispatch not found error."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        error = Exception("Not found")
        error.response = mock_response
        mock_get_rm.side_effect = error

        with pytest.raises(ResourceNotFoundError, match="Dispatch test-dispatch-123 not found"):
            get_node_results("test-dispatch-123", settings=mock_settings)

    @patch("covalent_cloud.dispatch_management.node_operations.rm.get_result_manager")
    def test_get_node_results_authentication_error(self, mock_get_rm, mock_settings):
        """Test handling authentication error."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        error = Exception("Unauthorized")
        error.response = mock_response
        mock_get_rm.side_effect = error

        with pytest.raises(AuthenticationError, match="Authentication failed"):
            get_node_results("test-dispatch-123", settings=mock_settings)


class TestGetNodeErrors:
    """Test cases for get_node_errors function."""

    @patch("covalent_cloud.dispatch_management.node_operations.rm.get_result_manager")
    def test_get_node_errors_success(self, mock_get_rm, mock_result_manager, mock_settings):
        """Test getting node errors successfully."""
        mock_get_rm.return_value = mock_result_manager

        # Mock error data for failed node
        mock_error_future = MagicMock()
        mock_error_future.load.return_value = "Division by zero"

        # Complete node data including names, statuses, and errors
        def mock_get_node_value(node_id, attr):
            node_data = {
                0: {"name": "setup", "status": "COMPLETED", "error": None},
                1: {"name": "calculate", "status": "COMPLETED", "error": None},
                2: {"name": "calculate", "status": "FAILED", "error": mock_error_future},
                3: {"name": "finalize", "status": "PENDING", "error": None},
            }
            return node_data.get(node_id, {}).get(attr)

        mock_result_manager.result_object.lattice.transport_graph.get_node_value = (
            mock_get_node_value
        )

        errors = get_node_errors("test-dispatch-123", settings=mock_settings)

        assert len(errors) == 4
        assert all(isinstance(error, NodeError) for error in errors)

        # Check that only node 2 has an error
        error_node = next(err for err in errors if err.node_id == 2)
        # Verify that the error is properly loaded from the mock_error_future
        assert error_node.node_id == 2
        assert error_node.error == "Division by zero"

    @patch("covalent_cloud.dispatch_management.node_operations.rm.get_result_manager")
    def test_get_node_errors_by_function_name(
        self, mock_get_rm, mock_result_manager, mock_settings
    ):
        """Test getting errors for specific function name."""
        mock_get_rm.return_value = mock_result_manager

        errors = get_node_errors("test-dispatch-123", node="calculate", settings=mock_settings)

        assert len(errors) == 2
        assert all(err.function_name == "calculate" for err in errors)


class TestGetNodeStdout:
    """Test cases for get_node_stdout function."""

    @patch("covalent_cloud.dispatch_management.node_operations.rm.get_result_manager")
    def test_get_node_stdout_success(self, mock_get_rm, mock_result_manager, mock_settings):
        """Test getting node stdout successfully."""
        mock_get_rm.return_value = mock_result_manager

        # Mock stdout data
        mock_stdout_future = MagicMock()
        mock_stdout_future.load.return_value = "Processing complete\nResult: 42"

        # Complete node data including names, statuses, and stdout
        def mock_get_node_value(node_id, attr):
            node_data = {
                0: {"name": "setup", "status": "COMPLETED", "stdout": None},
                1: {"name": "calculate", "status": "COMPLETED", "stdout": mock_stdout_future},
                2: {"name": "calculate", "status": "FAILED", "stdout": None},
                3: {"name": "finalize", "status": "PENDING", "stdout": None},
            }
            return node_data.get(node_id, {}).get(attr)

        mock_result_manager.result_object.lattice.transport_graph.get_node_value = (
            mock_get_node_value
        )

        stdout_results = get_node_stdout("test-dispatch-123", node=1, settings=mock_settings)

        assert len(stdout_results) == 1
        assert isinstance(stdout_results[0], NodeOutput)
        assert stdout_results[0].node_id == 1
        assert stdout_results[0].stdout == "Processing complete\nResult: 42"


class TestGetNodeStderr:
    """Test cases for get_node_stderr function."""

    @patch("covalent_cloud.dispatch_management.node_operations.rm.get_result_manager")
    def test_get_node_stderr_success(self, mock_get_rm, mock_result_manager, mock_settings):
        """Test getting node stderr successfully."""
        mock_get_rm.return_value = mock_result_manager

        # Mock stderr data
        mock_stderr_future = MagicMock()
        mock_stderr_future.load.return_value = "Warning: deprecated function used"

        # Complete node data including names, statuses, and stderr
        def mock_get_node_value(node_id, attr):
            node_data = {
                0: {"name": "setup", "status": "COMPLETED", "stderr": None},
                1: {"name": "calculate", "status": "COMPLETED", "stderr": None},
                2: {"name": "calculate", "status": "FAILED", "stderr": mock_stderr_future},
                3: {"name": "finalize", "status": "PENDING", "stderr": None},
            }
            return node_data.get(node_id, {}).get(attr)

        mock_result_manager.result_object.lattice.transport_graph.get_node_value = (
            mock_get_node_value
        )

        stderr_results = get_node_stderr("test-dispatch-123", node=2, settings=mock_settings)

        assert len(stderr_results) == 1
        assert isinstance(stderr_results[0], NodeStderr)
        assert stderr_results[0].node_id == 2
        assert stderr_results[0].stderr == "Warning: deprecated function used"


class TestGetFirstFailure:
    """Test cases for get_first_failure function."""

    @patch("covalent_cloud.dispatch_management.node_operations.rm.get_result_manager")
    def test_get_first_failure_success(self, mock_get_rm, mock_result_manager, mock_settings):
        """Test getting first failure successfully."""
        mock_get_rm.return_value = mock_result_manager

        # Mock node with earliest failure timestamp
        mock_result_manager.result_object.lattice.transport_graph.get_node_value.side_effect = (
            lambda node_id, attr: {
                (2, "error"): MagicMock(),  # Failed node
                (2, "start_time"): datetime(2023, 1, 1, 10, 0, 0),
            }.get((node_id, attr), None)
        )

        failure = get_first_failure("test-dispatch-123", settings=mock_settings)

        assert isinstance(failure, NodeFailure)
        assert failure.node_id == 2
        assert failure.function_name == "calculate"

    @patch("covalent_cloud.dispatch_management.node_operations.rm.get_result_manager")
    def test_get_first_failure_no_failures(self, mock_get_rm, mock_settings):
        """Test getting first failure when no failures exist."""
        mock_rm = MagicMock()
        mock_tg = MagicMock()
        mock_tg._graph.nodes = [0, 1]
        mock_tg.get_node_value.return_value = None  # No errors

        mock_result_object = MagicMock()
        mock_lattice = MagicMock()
        mock_lattice.transport_graph = mock_tg
        mock_result_object.lattice = mock_lattice
        mock_rm.result_object = mock_result_object
        mock_get_rm.return_value = mock_rm

        failure = get_first_failure("test-dispatch-123", settings=mock_settings)

        assert failure is None

    @patch("covalent_cloud.dispatch_management.node_operations.rm.get_result_manager")
    def test_get_first_failure_validation_error(self, mock_get_rm, mock_settings):
        """Test validation error handling."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        error = Exception("Bad request")
        error.response = mock_response
        mock_get_rm.side_effect = error

        with pytest.raises(Exception, match="Bad request"):
            get_first_failure("test-dispatch-123", settings=mock_settings)


class TestErrorHandling:
    """Test comprehensive error handling scenarios."""

    @patch("covalent_cloud.dispatch_management.node_operations.rm.get_result_manager")
    def test_network_error(self, mock_get_rm, mock_settings):
        """Test network error handling."""
        mock_get_rm.side_effect = ConnectionError("Network unreachable")

        with pytest.raises(ConnectionError, match="Network unreachable"):
            get_node_results("test-dispatch", settings=mock_settings)

    @patch("covalent_cloud.dispatch_management.node_operations.rm.get_result_manager")
    def test_timeout_error(self, mock_get_rm, mock_settings):
        """Test timeout error handling."""
        mock_get_rm.side_effect = TimeoutError("Request timeout")

        with pytest.raises(TimeoutError, match="Request timeout"):
            get_node_results("test-dispatch", settings=mock_settings)

    @patch("covalent_cloud.dispatch_management.node_operations.rm.get_result_manager")
    def test_partial_node_failure(self, mock_get_rm, mock_settings):
        """Test handling when some nodes can't be loaded."""
        mock_rm = MagicMock()
        mock_tg = MagicMock()
        mock_tg._graph.nodes = [0, 1]

        # First node loads successfully, second fails
        def mock_get_value(node_id, attr):
            if node_id == 0:
                return {"name": "success", "status": "COMPLETED", "output": MagicMock()}.get(attr)
            else:
                return {"name": "failure", "status": "FAILED", "output": None}.get(attr)

        mock_tg.get_node_value = mock_get_value

        mock_result_object = MagicMock()
        mock_lattice = MagicMock()
        mock_lattice.transport_graph = mock_tg
        mock_result_object.lattice = mock_lattice
        mock_rm.result_object = mock_result_object
        mock_get_rm.return_value = mock_rm

        results = get_node_results("test-dispatch", settings=mock_settings)

        # Should still return results for both nodes, with None for failed loads
        assert len(results) == 2
        assert results[0].function_name == "success"
        assert results[1].function_name == "failure"
        assert results[1].result is None
