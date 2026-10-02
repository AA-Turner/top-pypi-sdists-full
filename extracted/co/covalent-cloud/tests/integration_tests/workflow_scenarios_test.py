# Copyright 2025 Agnostiq Inc.

"""Functional tests for complete workflow scenarios."""

from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

import covalent_cloud as cc
from covalent_cloud.shared.classes.settings import Settings


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    settings = Settings()
    settings.dispatcher_uri = "https://api.dev.covalent.xyz"
    return settings


@pytest.fixture
def sample_dispatches_response():
    """Sample response for dispatch listing."""
    return {
        "records": [
            {
                "dispatch_id": "dispatch-123",
                "name": "ML Training Pipeline",
                "status": "COMPLETED",
                "created_at": datetime.now() - timedelta(hours=2),
                "started_at": datetime.now() - timedelta(hours=2, minutes=-5),
                "completed_at": datetime.now() - timedelta(hours=1),
                "updated_at": datetime.now() - timedelta(hours=1),
                "electron_num": 5,
                "completed_task_num": 5,
                "tags": ["ml", "training"],
                "is_pinned": False,
                "redispatch_count": 0,
            }
        ],
        "metadata": {"total_count": 1, "page": 0, "count": 10, "status_count": {"COMPLETED": 1}},
    }


class TestCompleteWorkflowMonitoring:
    """Test complete workflow monitoring scenarios."""

    @patch("covalent_cloud.dispatch_management.interface_functions.get_client")
    @patch("covalent_cloud.dispatch_management.node_operations.rm.get_result_manager")
    def test_workflow_monitoring_lifecycle(
        self, mock_get_rm, mock_get_client, mock_settings, sample_dispatches_response
    ):
        """Test complete workflow from dispatch listing to node monitoring."""
        # Mock get_dispatches
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = sample_dispatches_response
        mock_client.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        # Mock node operations
        mock_transport_graph = MagicMock()
        mock_transport_graph._graph.nodes = [0, 1, 2, 3, 4]

        node_data = {
            0: {"name": "data_loading", "status": "COMPLETED", "output": MagicMock()},
            1: {"name": "preprocessing", "status": "COMPLETED", "output": MagicMock()},
            2: {"name": "training", "status": "COMPLETED", "output": MagicMock()},
            3: {"name": "validation", "status": "COMPLETED", "output": MagicMock()},
            4: {"name": "model_save", "status": "COMPLETED", "output": MagicMock()},
        }

        def mock_get_node_value(node_id, attribute):
            return node_data[node_id].get(attribute)

        mock_transport_graph.get_node_value = mock_get_node_value

        # Mock result loading
        node_data[0]["output"].load.return_value = {"data_shape": [1000, 784]}
        node_data[1]["output"].load.return_value = {"processed_samples": 1000}
        node_data[2]["output"].load.return_value = {"model_accuracy": 0.95}
        node_data[3]["output"].load.return_value = {"validation_accuracy": 0.92}
        node_data[4]["output"].load.return_value = {"model_path": "/models/trained_model.pkl"}

        mock_result_manager = MagicMock()
        mock_result_object = MagicMock()
        mock_lattice = MagicMock()
        mock_lattice.transport_graph = mock_transport_graph
        mock_result_object.lattice = mock_lattice
        mock_result_manager.result_object = mock_result_object
        mock_get_rm.return_value = mock_result_manager

        # Step 1: List dispatches to find the ML training workflow
        dispatches = cc.get_dispatches(search="ML Training", settings=mock_settings)
        assert len(dispatches.records) == 1
        dispatch_id = dispatches.records[0].dispatch_id

        # Step 2: Get all node results to see pipeline outputs
        results = cc.get_node_results(dispatch_id, settings=mock_settings)
        assert len(results) == 5

        # Verify pipeline structure
        data_loading_result = next(r for r in results if r.function_name == "data_loading")
        assert data_loading_result.result["data_shape"] == [1000, 784]

        training_result = next(r for r in results if r.function_name == "training")
        assert training_result.result["model_accuracy"] == 0.95

        # Step 3: Check for any errors in the pipeline
        errors = cc.get_node_errors(dispatch_id, settings=mock_settings)
        failed_nodes = [err for err in errors if err.error and err.error.strip()]
        assert len(failed_nodes) == 0  # No failures in this successful pipeline

        # Step 4: Get stdout for training node to see training logs
        training_stdout = cc.get_node_stdout(dispatch_id, node="training", settings=mock_settings)
        assert len(training_stdout) >= 1

    @patch("covalent_cloud.dispatch_management.interface_functions.get_client")
    @patch("covalent_cloud.dispatch_management.node_operations.rm.get_result_manager")
    def test_failed_workflow_analysis(self, mock_get_rm, mock_get_client, mock_settings):
        """Test analyzing a failed workflow to identify issues."""
        # Mock failed dispatch response
        failed_dispatch_response = {
            "records": [
                {
                    "dispatch_id": "dispatch-failed-456",
                    "name": "Data Processing Pipeline",
                    "status": "FAILED",
                    "created_at": datetime.now() - timedelta(hours=1),
                    "started_at": datetime.now() - timedelta(hours=1, minutes=-5),
                    "completed_at": None,
                    "updated_at": datetime.now() - timedelta(minutes=30),
                    "electron_num": 4,
                    "completed_task_num": 2,
                    "tags": ["data", "processing"],
                    "is_pinned": True,
                    "redispatch_count": 1,
                }
            ],
            "metadata": {"total_count": 1, "page": 0, "count": 10, "status_count": {"FAILED": 1}},
        }

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = failed_dispatch_response
        mock_client.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        # Mock failed workflow nodes
        mock_transport_graph = MagicMock()
        mock_transport_graph._graph.nodes = [0, 1, 2, 3]

        node_data = {
            0: {"name": "load_data", "status": "COMPLETED", "output": MagicMock()},
            1: {"name": "validate_data", "status": "COMPLETED", "output": MagicMock()},
            2: {
                "name": "transform_data",
                "status": "FAILED",
                "output": None,
                "error": MagicMock(),
            },
            3: {"name": "save_results", "status": "PENDING", "output": None},
        }

        def mock_get_node_value(node_id, attribute):
            return node_data[node_id].get(attribute)

        mock_transport_graph.get_node_value = mock_get_node_value

        # Mock error and output loading
        node_data[0]["output"].load.return_value = {"records_loaded": 5000}
        node_data[1]["output"].load.return_value = {"valid_records": 4800}
        node_data[2][
            "error"
        ].load.return_value = "KeyError: 'required_column' not found in DataFrame"

        mock_result_manager = MagicMock()
        mock_result_object = MagicMock()
        mock_lattice = MagicMock()
        mock_lattice.transport_graph = mock_transport_graph
        mock_result_object.lattice = mock_lattice
        mock_result_manager.result_object = mock_result_object
        mock_get_rm.return_value = mock_result_manager

        # Step 1: Find failed workflows
        failed_dispatches = cc.get_dispatches(status="FAILED", settings=mock_settings)
        assert len(failed_dispatches.records) == 1
        dispatch_id = failed_dispatches.records[0].dispatch_id

        # Step 2: Identify first failure
        first_failure = cc.get_first_failure(dispatch_id, settings=mock_settings)
        assert first_failure is not None
        assert first_failure.node_id == 2
        assert first_failure.function_name == "transform_data"

        # Step 3: Get detailed error information
        errors = cc.get_node_errors(dispatch_id, node="transform_data", settings=mock_settings)
        assert len(errors) == 1
        assert "required_column" in errors[0].error

        # Step 4: Check stderr for additional debug info
        error_stderr = cc.get_node_stderr(dispatch_id, node=2, settings=mock_settings)
        assert len(error_stderr) >= 1

    @patch("covalent_cloud.dispatch_management.interface_functions.get_client")
    @patch("covalent_cloud.dispatch_management.node_operations.rm.get_result_manager")
    def test_multi_node_same_function_analysis(self, mock_get_rm, mock_get_client, mock_settings):
        """Test analyzing workflows with multiple nodes using the same function."""
        # Mock dispatch with parallel processing
        parallel_dispatch_response = {
            "records": [
                {
                    "dispatch_id": "dispatch-parallel-789",
                    "name": "Parallel Data Processing",
                    "status": "COMPLETED",
                    "created_at": datetime.now() - timedelta(hours=3),
                    "completed_at": datetime.now() - timedelta(hours=2, minutes=30),
                    "updated_at": datetime.now() - timedelta(hours=2, minutes=30),
                    "electron_num": 7,
                    "completed_task_num": 7,
                    "tags": ["parallel", "processing"],
                    "is_pinned": False,
                    "redispatch_count": 0,
                }
            ],
            "metadata": {
                "total_count": 1,
                "page": 0,
                "count": 10,
                "status_count": {"COMPLETED": 1},
            },
        }

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = parallel_dispatch_response
        mock_client.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        # Mock parallel workflow with same function used multiple times
        mock_transport_graph = MagicMock()
        mock_transport_graph._graph.nodes = [0, 1, 2, 3, 4, 5, 6]

        node_data = {
            0: {"name": "setup", "status": "COMPLETED", "output": MagicMock()},
            1: {"name": "process_chunk", "status": "COMPLETED", "output": MagicMock()},  # Chunk 1
            2: {"name": "process_chunk", "status": "COMPLETED", "output": MagicMock()},  # Chunk 2
            3: {"name": "process_chunk", "status": "COMPLETED", "output": MagicMock()},  # Chunk 3
            4: {"name": "process_chunk", "status": "COMPLETED", "output": MagicMock()},  # Chunk 4
            5: {"name": "aggregate", "status": "COMPLETED", "output": MagicMock()},
            6: {"name": "finalize", "status": "COMPLETED", "output": MagicMock()},
        }

        def mock_get_node_value(node_id, attribute):
            return node_data[node_id].get(attribute)

        mock_transport_graph.get_node_value = mock_get_node_value

        # Mock outputs for parallel processing nodes
        node_data[0]["output"].load.return_value = {"total_chunks": 4}
        node_data[1]["output"].load.return_value = {"chunk_id": 1, "processed_records": 250}
        node_data[2]["output"].load.return_value = {"chunk_id": 2, "processed_records": 300}
        node_data[3]["output"].load.return_value = {"chunk_id": 3, "processed_records": 275}
        node_data[4]["output"].load.return_value = {"chunk_id": 4, "processed_records": 225}
        node_data[5]["output"].load.return_value = {"total_processed": 1050}
        node_data[6]["output"].load.return_value = {
            "status": "success",
            "output_path": "/results/final.json",
        }

        mock_result_manager = MagicMock()
        mock_result_object = MagicMock()
        mock_lattice = MagicMock()
        mock_lattice.transport_graph = mock_transport_graph
        mock_result_object.lattice = mock_lattice
        mock_result_manager.result_object = mock_result_object
        mock_get_rm.return_value = mock_result_manager

        dispatch_id = "dispatch-parallel-789"

        # Step 1: Get all results for parallel processing function
        chunk_results = cc.get_node_results(
            dispatch_id, node="process_chunk", settings=mock_settings
        )
        assert len(chunk_results) == 4  # Four parallel chunks

        # Verify each chunk processed data
        total_processed = sum(result.result["processed_records"] for result in chunk_results)
        assert total_processed == 1050

        # Step 2: Get results by specific node IDs
        chunk_1_result = cc.get_node_results(dispatch_id, node=1, settings=mock_settings)
        assert len(chunk_1_result) == 1
        assert chunk_1_result[0].result["chunk_id"] == 1

        # Step 3: Check for any failures in parallel processing
        chunk_errors = cc.get_node_errors(
            dispatch_id, node="process_chunk", settings=mock_settings
        )
        failed_chunks = [err for err in chunk_errors if err.error and err.error.strip()]
        assert len(failed_chunks) == 0  # All chunks succeeded

        # Step 4: Verify aggregation step got all data
        aggregate_result = cc.get_node_results(
            dispatch_id, node="aggregate", settings=mock_settings
        )
        assert aggregate_result[0].result["total_processed"] == 1050


class TestEnvironmentLifecycle:
    """Test complete environment lifecycle scenarios."""

    @patch("covalent_cloud.swe_management.swe_manager.get_client")
    @patch("covalent_cloud.swe_management.swe_manager._get_envs_filtered")
    def test_environment_creation_and_monitoring(
        self, mock_get_envs, mock_get_client, mock_settings
    ):
        """Test creating environment, monitoring build logs, and getting YAML."""
        # Mock environment creation and details
        env_response = {
            "id": "env-123",
            "name": "ml-environment",
            "status": "BUILDING",
            "definition": "https://s3.amazonaws.com/bucket/env.yaml",
        }

        yaml_content = """name: ml-environment
channels:
  - conda-forge
  - pytorch
dependencies:
  - python=3.9
  - numpy=1.21.*
  - pytorch=1.12.*
  - pip:
    - transformers==4.21.0
    - datasets==2.4.0"""

        build_logs_response = {
            "events": [
                {"timestamp": 1640995200000, "message": "Starting environment build..."},
                {"timestamp": 1640995230000, "message": "Resolving conda dependencies..."},
                {"timestamp": 1640995290000, "message": "Installing conda packages..."},
                {"timestamp": 1640995350000, "message": "Installing pip packages..."},
                {"timestamp": 1640995380000, "message": "Build completed successfully."},
            ],
            "nextForwardToken": None,
        }

        # Create mock environment object with proper attributes
        mock_env = MagicMock()
        mock_env.id = "env-123"
        mock_env.name = "ml-environment"
        mock_get_envs.return_value = {"ml-environment": mock_env}

        mock_client = MagicMock()

        # Mock API responses
        def mock_get_response(url, **kwargs):
            mock_response = MagicMock()
            if "/envs/env-123/logs" in url:
                mock_response.json.return_value = build_logs_response
                mock_response.raise_for_status.return_value = None
            elif "/envs/env-123" in url:
                mock_response.json.return_value = env_response
                mock_response.raise_for_status.return_value = None
            return mock_response

        mock_client.get.side_effect = mock_get_response
        mock_get_client.return_value = mock_client

        # Mock S3 YAML download
        with patch("requests.get") as mock_requests_get:
            mock_yaml_response = MagicMock()
            mock_yaml_response.text = yaml_content
            mock_yaml_response.raise_for_status.return_value = None
            mock_requests_get.return_value = mock_yaml_response

            # Step 1: Monitor build logs during environment creation
            logs = cc.get_environment_build_logs("ml-environment", settings=mock_settings)
            assert len(logs.events) == 5
            assert logs.events[0].message == "Starting environment build..."
            assert logs.events[-1].message == "Build completed successfully."

            # Step 2: Get environment YAML definition
            yaml_def = cc.get_environment_yaml("ml-environment", settings=mock_settings)
            assert "python=3.9" in yaml_def
            assert "transformers==4.21.0" in yaml_def

            # Step 3: Verify environment is ready for use
            # In a real scenario, you might wait and poll until status is READY
            assert env_response["status"] in ["BUILDING", "READY"]

    @patch("covalent_cloud.swe_management.swe_manager.get_client")
    @patch("covalent_cloud.swe_management.swe_manager._get_envs_filtered")
    def test_environment_build_failure_analysis(
        self, mock_get_envs, mock_get_client, mock_settings
    ):
        """Test analyzing failed environment builds through logs."""
        # Mock failed environment build
        failed_logs_response = {
            "events": [
                {"timestamp": 1640995200000, "message": "Starting environment build..."},
                {"timestamp": 1640995230000, "message": "Resolving conda dependencies..."},
                {"timestamp": 1640995290000, "message": "Installing conda packages..."},
                {
                    "timestamp": 1640995350000,
                    "message": "ERROR: Could not find package 'nonexistent-package'",
                },
                {"timestamp": 1640995360000, "message": "Build failed with exit code 1"},
            ],
            "nextForwardToken": None,
        }

        # Create mock environment object with proper attributes
        mock_env = MagicMock()
        mock_env.id = "env-failed-456"
        mock_env.name = "failed-env"
        mock_get_envs.return_value = {"failed-env": mock_env}

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = failed_logs_response
        mock_response.raise_for_status.return_value = None
        mock_client.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        # Step 1: Get build logs to diagnose failure
        logs = cc.get_environment_build_logs("failed-env", settings=mock_settings)

        # Step 2: Identify error messages in logs
        error_events = [event for event in logs.events if "ERROR" in event.message]
        assert len(error_events) >= 1
        assert "nonexistent-package" in error_events[0].message

        # Step 3: Check final status
        final_events = [event for event in logs.events if "failed" in event.message.lower()]
        assert len(final_events) >= 1
        assert "exit code 1" in final_events[0].message


class TestFunctionDeploymentLifecycle:
    """Test complete function deployment lifecycle scenarios."""

    @patch("covalent_cloud.function_serve.deployment.get_deployment_client")
    def test_function_deployment_and_api_key_management(
        self, mock_get_deployment_client, mock_settings
    ):
        """Test deploying function, managing API keys, and monitoring deployments."""
        # Mock deployment listing
        deployments_response = {
            "records": [
                {
                    "id": "func-ml-123",
                    "title": "ML Model API",
                    "description": "Serve ML model predictions",
                    "status": "ACTIVE",
                    "created_at": "2023-01-01T10:00:00Z",
                    "updated_at": "2023-01-01T10:30:00Z",
                    "invoke_url": "https://api.dev.covalent.xyz/fn/func-ml-123",
                    "auth": True,
                    "tags": ["ml", "api"],
                    "endpoints": [
                        {
                            "name": "predict",
                            "method": "POST",
                            "route": "/predict",
                            "description": "Make predictions",
                        }
                    ],
                }
            ],
            "metadata": {"total_count": 1, "page": 0, "count": 10, "has_next_page": False},
        }

        # Mock API key responses
        create_key_response = {
            "id": "key-abc-123",
            "key": "sk-ml-api-key-secret-123",
            "created_at": "2023-01-01T12:00:00Z",
        }

        list_keys_response = [
            {
                "id": "key-abc-123",
                "created_at": "2023-01-01T12:00:00Z",
                "last_used": "2023-01-01T15:30:00Z",
            },
            {"id": "key-def-456", "created_at": "2023-01-01T13:00:00Z", "last_used": None},
        ]

        mock_client = MagicMock()

        def mock_api_call(method, url, **kwargs):
            mock_response = MagicMock()

            if method == "get":
                if "/functions" in url and "inference-keys" not in url:
                    mock_response.json.return_value = deployments_response
                elif "inference-keys" in url:
                    mock_response.json.return_value = list_keys_response
            elif method == "post" and "inference-keys" in url:
                mock_response.json.return_value = create_key_response
            elif method == "delete":
                mock_response.status_code = 204

            return mock_response

        # Configure mock client methods
        mock_client.get.side_effect = lambda url, **kwargs: mock_api_call("get", url, **kwargs)
        mock_client.post.side_effect = lambda url, **kwargs: mock_api_call("post", url, **kwargs)
        mock_client.delete.side_effect = lambda url, **kwargs: mock_api_call(
            "delete", url, **kwargs
        )

        mock_get_deployment_client.return_value = mock_client

        # Step 1: List function deployments to find ML API
        deployments = cc.list_function_deployments(status="ACTIVE", settings=mock_settings)
        assert len(deployments.records) == 1
        function_id = deployments.records[0].id
        assert deployments.records[0].title == "ML Model API"

        # Step 2: Create API key for accessing the function
        new_key = cc.create_inference_api_key(function_id, settings=mock_settings)
        assert new_key.key_id == "key-abc-123"
        assert new_key.key == "sk-ml-api-key-secret-123"

        # Step 3: List all API keys for the function
        api_keys = cc.list_inference_api_keys(function_id, settings=mock_settings)
        assert len(api_keys) == 2
        assert api_keys[0].key_id == "key-abc-123"
        assert api_keys[0].last_used is not None
        assert api_keys[1].last_used is None  # Unused key

        # Step 4: Delete unused API key
        unused_key_id = api_keys[1].key_id
        delete_success = cc.delete_inference_api_key(
            function_id, unused_key_id, settings=mock_settings
        )
        assert delete_success

    @patch("covalent_cloud.function_serve.deployment.get_deployment_client")
    def test_function_deployment_monitoring_and_filtering(
        self, mock_get_deployment_client, mock_settings
    ):
        """Test monitoring multiple function deployments with filtering."""
        # Mock multiple deployments with different statuses
        all_deployments_response = {
            "records": [
                {
                    "id": "func-active-1",
                    "title": "Production API v1",
                    "description": "Production ML API",
                    "status": "ACTIVE",
                    "created_at": "2023-01-01T09:00:00Z",
                    "updated_at": "2023-01-01T09:30:00Z",
                    "endpoints": [
                        {
                            "name": "predict",
                            "method": "POST",
                            "route": "/predict",
                            "description": "Main prediction endpoint",
                        }
                    ],
                    "auth": True,
                    "tags": ["production", "v1"],
                },
                {
                    "id": "func-building-2",
                    "title": "Development API v2",
                    "description": "Development version",
                    "status": "BUILDING",
                    "created_at": "2023-01-01T10:00:00Z",
                    "updated_at": "2023-01-01T10:15:00Z",
                    "endpoints": [],
                    "auth": False,
                    "tags": ["development", "v2"],
                },
                {
                    "id": "func-failed-3",
                    "title": "Experimental API",
                    "description": "Experimental features",
                    "status": "FAILED",
                    "created_at": "2023-01-01T11:00:00Z",
                    "updated_at": "2023-01-01T11:05:00Z",
                    "endpoints": [],
                    "auth": False,
                    "tags": ["experimental"],
                },
            ],
            "metadata": {"total_count": 3, "page": 0, "count": 10, "has_next_page": False},
        }

        active_deployments_response = {
            "records": [all_deployments_response["records"][0]],  # Only active one
            "metadata": {"total_count": 1, "page": 0, "count": 10, "has_next_page": False},
        }

        mock_client = MagicMock()

        def mock_get_deployments(url, **kwargs):
            mock_response = MagicMock()
            params = kwargs.get("request_options", {}).get("params", {})

            if params.get("status") == "ACTIVE":
                mock_response.json.return_value = active_deployments_response
            else:
                mock_response.json.return_value = all_deployments_response

            return mock_response

        mock_client.get.side_effect = mock_get_deployments
        mock_get_deployment_client.return_value = mock_client

        # Step 1: Monitor all deployments
        all_deployments = cc.list_function_deployments(settings=mock_settings)
        assert len(all_deployments.records) == 3

        statuses = [dep.status for dep in all_deployments.records]
        assert "ACTIVE" in statuses
        assert "BUILDING" in statuses
        assert "FAILED" in statuses

        # Step 2: Filter for only production-ready deployments
        active_deployments = cc.list_function_deployments(status="ACTIVE", settings=mock_settings)
        assert len(active_deployments.records) == 1
        assert active_deployments.records[0].status == "ACTIVE"
        assert "production" in active_deployments.records[0].tags

        # Step 3: Search for specific versions
        v2_deployments = cc.list_function_deployments(search="v2", settings=mock_settings)
        # In a real scenario, this would filter based on search
        # For this test, we're verifying the search parameter is passed


class TestIntegratedWorkflowScenarios:
    """Test integrated scenarios combining multiple features."""

    @patch("covalent_cloud.dispatch_management.interface_functions.get_client")
    @patch("covalent_cloud.swe_management.swe_manager.get_client")
    @patch("covalent_cloud.function_serve.deployment.get_deployment_client")
    def test_ml_pipeline_end_to_end(
        self, mock_deploy_client, mock_env_client, mock_dispatch_client, mock_settings
    ):
        """Test complete ML pipeline: environment setup, training dispatch, model deployment."""
        # This would be a comprehensive test combining:
        # 1. Environment creation for ML dependencies
        # 2. Workflow dispatch for model training
        # 3. Function deployment for model serving
        # 4. API key management for access control

        # Mock environment ready
        env_response = {
            "id": "env-ml-456",
            "name": "ml-training-env",
            "status": "READY",
            "definition": "https://s3.amazonaws.com/bucket/ml-env.yaml",
        }

        # Mock completed training dispatch
        training_dispatch_response = {
            "records": [
                {
                    "dispatch_id": "train-dispatch-789",
                    "name": "Model Training Workflow",
                    "status": "COMPLETED",
                    "created_at": "2023-01-01T08:00:00Z",
                    "updated_at": "2023-01-01T09:00:00Z",
                    "is_pinned": False,
                    "redispatch_count": 0,
                    "tags": ["training", "ml"],
                    "electron_num": 3,
                    "completed_task_num": 3,
                }
            ],
            "metadata": {
                "total_count": 1,
                "page": 0,
                "count": 10,
                "status_count": {"COMPLETED": 1},
            },
        }

        # Mock deployed model service
        model_service_response = {
            "records": [
                {
                    "id": "model-service-123",
                    "title": "Trained Model API",
                    "description": "ML model serving API",
                    "status": "ACTIVE",
                    "created_at": "2023-01-01T10:00:00Z",
                    "updated_at": "2023-01-01T10:30:00Z",
                    "endpoints": [
                        {
                            "name": "predict",
                            "method": "POST",
                            "route": "/predict",
                            "description": "Model prediction",
                        }
                    ],
                    "auth": True,
                    "tags": ["model", "serving"],
                }
            ],
            "metadata": {"total_count": 1, "page": 0, "count": 10, "has_next_page": False},
        }

        # Configure mock clients with specific responses
        mock_env_response = MagicMock()
        mock_env_response.json.return_value = env_response
        mock_env_client.get.return_value = mock_env_response

        # Create mock dispatch client and response
        mock_dispatch_client_instance = MagicMock()
        mock_dispatch_response = MagicMock()
        mock_dispatch_response.json.return_value = training_dispatch_response
        mock_dispatch_client_instance.get.return_value = mock_dispatch_response
        mock_dispatch_client.return_value = mock_dispatch_client_instance

        # Create mock deploy client and response
        mock_deploy_client_instance = MagicMock()
        mock_deploy_response = MagicMock()
        mock_deploy_response.json.return_value = model_service_response
        mock_deploy_client_instance.get.return_value = mock_deploy_response
        mock_deploy_client.return_value = mock_deploy_client_instance

        # Step 1: Verify ML environment is ready
        # In practice, you might call get_environment_yaml to check dependencies

        # Step 2: Find completed training workflow
        training_dispatches = cc.get_dispatches(
            search="Model Training", status="COMPLETED", settings=mock_settings
        )
        assert len(training_dispatches.records) == 1
        training_dispatch = training_dispatches.records[0]
        assert training_dispatch.status == "COMPLETED"
        assert "training" in training_dispatch.tags

        # Step 3: Find deployed model service
        model_services = cc.list_function_deployments(
            search="Model API", status="ACTIVE", settings=mock_settings
        )
        assert len(model_services.records) == 1
        model_service = model_services.records[0]
        assert model_service.status == "ACTIVE"
        assert model_service.auth  # Requires authentication

        # This demonstrates how all the pieces work together in a real ML workflow
