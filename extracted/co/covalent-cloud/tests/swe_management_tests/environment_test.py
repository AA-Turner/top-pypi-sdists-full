# Copyright 2025 Agnostiq Inc.

"""Additional unit tests for environment management functions."""

from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
import requests
import responses

from covalent_cloud.shared.classes.exceptions import CovalentGenericAPIError, CovalentSDKError
from covalent_cloud.shared.classes.settings import Settings
from covalent_cloud.swe_management.models.environment_logs import EnvironmentLogs, LogEvent
from covalent_cloud.swe_management.models.hardware import HardwareSpec
from covalent_cloud.swe_management.swe_manager import (
    get_environment_build_logs,
    get_environment_yaml,
    list_hardware,
)

TEST_ENV_ID = "550e8400-e29b-41d4-a716-446655440000"
TEST_ENV_NAME = "test-environment"


@pytest.fixture
def mock_settings():
    """Mock settings for tests."""
    settings = Settings()
    settings.dispatcher_uri = "https://api.dev.covalent.xyz"
    return settings


class TestGetEnvironmentYaml:
    """Test cases for get_environment_yaml function."""

    @responses.activate
    def test_get_environment_yaml_by_name_success(self, mock_settings):
        """Test getting environment YAML by name successfully."""
        # Create a mock environment object with .id attribute
        mock_env = MagicMock()
        mock_env.id = TEST_ENV_ID
        mock_env.name = TEST_ENV_NAME
        mock_env.status = "READY"

        # Mock environment list response
        env_list_response = {TEST_ENV_NAME: mock_env}

        # Mock environment details response
        env_details_response = {
            "id": TEST_ENV_ID,
            "name": TEST_ENV_NAME,
            "definition": "https://s3.amazonaws.com/bucket/env.yaml",
            "status": "READY",
        }

        yaml_content = """name: test-environment
channels:
  - conda-forge
dependencies:
  - python=3.9
  - numpy=1.21.*
  - pip:
    - tensorflow==2.10.0"""

        with patch(
            "covalent_cloud.swe_management.swe_manager._get_envs_filtered"
        ) as mock_get_envs:
            mock_get_envs.return_value = env_list_response

            responses.add(
                responses.GET,
                f"https://api.dev.covalent.xyz/api/v2/envs/{TEST_ENV_ID}",
                json=env_details_response,
                status=200,
            )

            responses.add(
                responses.GET,
                "https://s3.amazonaws.com/bucket/env.yaml",
                body=yaml_content,
                status=200,
            )

            result = get_environment_yaml(TEST_ENV_NAME, settings=mock_settings)

            assert result == yaml_content
            mock_get_envs.assert_called_once_with(mock_settings, name=TEST_ENV_NAME)

    @responses.activate
    def test_get_environment_yaml_by_id_success(self, mock_settings):
        """Test getting environment YAML by ID successfully."""
        env_details_response = {
            "id": TEST_ENV_ID,
            "name": TEST_ENV_NAME,
            "definition": "https://s3.amazonaws.com/bucket/env.yaml",
            "status": "READY",
        }

        yaml_content = """name: test-environment
channels:
  - conda-forge
dependencies:
  - python=3.9"""

        responses.add(
            responses.GET,
            f"https://api.dev.covalent.xyz/api/v2/envs/{TEST_ENV_ID}",
            json=env_details_response,
            status=200,
        )

        responses.add(
            responses.GET,
            "https://s3.amazonaws.com/bucket/env.yaml",
            body=yaml_content,
            status=200,
        )

        result = get_environment_yaml(TEST_ENV_ID, settings=mock_settings)

        assert result == yaml_content

    def test_get_environment_yaml_environment_not_found_by_name(self, mock_settings):
        """Test handling environment not found by name."""
        with patch(
            "covalent_cloud.swe_management.swe_manager._get_envs_filtered"
        ) as mock_get_envs:
            mock_get_envs.return_value = {}  # Empty dict means not found

            with pytest.raises(CovalentSDKError, match="Environment 'nonexistent' not found"):
                get_environment_yaml("nonexistent", settings=mock_settings)

    @responses.activate
    def test_get_environment_yaml_environment_not_found_by_id(self, mock_settings):
        """Test handling environment not found by ID."""
        responses.add(
            responses.GET,
            f"https://api.dev.covalent.xyz/api/v2/envs/{TEST_ENV_ID}",
            status=404,
        )

        with pytest.raises(CovalentSDKError, match=f"Environment '{TEST_ENV_ID}' not found"):
            get_environment_yaml(TEST_ENV_ID, settings=mock_settings)

    @responses.activate
    def test_get_environment_yaml_no_definition_url(self, mock_settings):
        """Test handling environment with no definition URL."""
        env_details_response = {
            "id": TEST_ENV_ID,
            "name": TEST_ENV_NAME,
            "status": "READY",
        }

        responses.add(
            responses.GET,
            f"https://api.dev.covalent.xyz/api/v2/envs/{TEST_ENV_ID}",
            json=env_details_response,
            status=200,
        )

        with pytest.raises(CovalentSDKError, match="Environment definition not available"):
            get_environment_yaml(TEST_ENV_ID, settings=mock_settings)

    @responses.activate
    def test_get_environment_yaml_s3_download_failure(self, mock_settings):
        """Test handling S3 download failure."""
        env_details_response = {
            "id": TEST_ENV_ID,
            "name": TEST_ENV_NAME,
            "definition": "https://s3.amazonaws.com/bucket/env.yaml",
            "status": "READY",
        }

        responses.add(
            responses.GET,
            f"https://api.dev.covalent.xyz/api/v2/envs/{TEST_ENV_ID}",
            json=env_details_response,
            status=200,
        )

        responses.add(
            responses.GET,
            "https://s3.amazonaws.com/bucket/env.yaml",
            status=403,  # Access denied
        )

        with pytest.raises(CovalentSDKError, match="Failed to download environment definition"):
            get_environment_yaml(TEST_ENV_ID, settings=mock_settings)

    @responses.activate
    def test_get_environment_yaml_api_server_error(self, mock_settings):
        """Test handling API server error."""
        responses.add(
            responses.GET,
            f"https://api.dev.covalent.xyz/api/v2/envs/{TEST_ENV_ID}",
            status=500,
        )

        with pytest.raises(CovalentSDKError, match="HTTP 500 error while fetching environment"):
            get_environment_yaml(TEST_ENV_ID, settings=mock_settings)


class TestGetEnvironmentBuildLogs:
    """Test cases for get_environment_build_logs function."""

    @responses.activate
    def test_get_environment_build_logs_by_name_success(self, mock_settings):
        """Test getting build logs by environment name successfully."""
        # Create a mock environment object with .id attribute
        mock_env = MagicMock()
        mock_env.id = TEST_ENV_ID
        mock_env.name = TEST_ENV_NAME
        mock_env.status = "READY"

        # Mock environment list response
        env_list_response = {TEST_ENV_NAME: mock_env}

        logs_response = {
            "events": [
                {
                    "timestamp": 1640995200000,  # milliseconds
                    "message": "Starting environment build...",
                },
                {
                    "timestamp": 1640995260000,
                    "message": "Installing dependencies...",
                },
                {
                    "timestamp": 1640995320000,
                    "message": "Build completed successfully.",
                },
            ],
            "nextForwardToken": "token_123",
        }

        with patch(
            "covalent_cloud.swe_management.swe_manager._get_envs_filtered"
        ) as mock_get_envs:
            mock_get_envs.return_value = env_list_response

            responses.add(
                responses.GET,
                f"https://api.dev.covalent.xyz/api/v2/envs/{TEST_ENV_ID}/logs",
                json=logs_response,
                status=200,
            )

            result = get_environment_build_logs(TEST_ENV_NAME, settings=mock_settings)

            assert isinstance(result, EnvironmentLogs)
            assert len(result.events) == 3
            assert result.events[0].message == "Starting environment build..."
            assert result.next_token == "token_123"
            mock_get_envs.assert_called_once_with(mock_settings, name=TEST_ENV_NAME)

    @responses.activate
    def test_get_environment_build_logs_by_id_success(self, mock_settings):
        """Test getting build logs by environment ID successfully."""
        logs_response = {
            "events": [
                {
                    "timestamp": 1640995200000,
                    "message": "Build started",
                }
            ],
            "nextBackwardToken": "backward_token_456",
        }

        responses.add(
            responses.GET,
            f"https://api.dev.covalent.xyz/api/v2/envs/{TEST_ENV_ID}/logs",
            json=logs_response,
            status=200,
        )

        result = get_environment_build_logs(TEST_ENV_ID, settings=mock_settings)

        assert isinstance(result, EnvironmentLogs)
        assert len(result.events) == 1
        assert result.events[0].message == "Build started"
        assert result.next_token == "backward_token_456"

    @responses.activate
    def test_get_environment_build_logs_with_pagination(self, mock_settings):
        """Test getting build logs with pagination parameters."""
        logs_response = {
            "events": [],
            "nextForwardToken": None,
        }

        responses.add(
            responses.GET,
            f"https://api.dev.covalent.xyz/api/v2/envs/{TEST_ENV_ID}/logs",
            json=logs_response,
            status=200,
        )

        result = get_environment_build_logs(
            TEST_ENV_ID, next_token="existing_token", limit=50, settings=mock_settings
        )

        assert isinstance(result, EnvironmentLogs)
        assert len(result.events) == 0
        assert result.next_token is None

        # Check that parameters were passed correctly
        assert len(responses.calls) == 1
        request_params = responses.calls[0].request.params
        assert request_params["limit"] == "50"
        assert request_params["next_token"] == "existing_token"

    def test_get_environment_build_logs_invalid_limit(self, mock_settings):
        """Test validation of limit parameter."""
        with pytest.raises(CovalentSDKError):
            get_environment_build_logs(TEST_ENV_ID, limit=0, settings=mock_settings)

        with pytest.raises(CovalentSDKError):
            get_environment_build_logs(TEST_ENV_ID, limit=10001, settings=mock_settings)

        with pytest.raises(CovalentSDKError):
            get_environment_build_logs(TEST_ENV_ID, limit=-1, settings=mock_settings)

    def test_get_environment_build_logs_environment_not_found_by_name(self, mock_settings):
        """Test handling environment not found by name."""
        with patch(
            "covalent_cloud.swe_management.swe_manager._get_envs_filtered"
        ) as mock_get_envs:
            mock_get_envs.return_value = {}  # Empty dict means not found

            with pytest.raises(CovalentSDKError, match="Environment 'nonexistent' not found"):
                get_environment_build_logs("nonexistent", settings=mock_settings)

    @responses.activate
    def test_get_environment_build_logs_environment_not_found_by_id(self, mock_settings):
        """Test handling environment not found by ID."""
        responses.add(
            responses.GET,
            f"https://api.dev.covalent.xyz/api/v2/envs/{TEST_ENV_ID}/logs",
            status=404,
        )

        with pytest.raises(CovalentSDKError, match=f"Environment '{TEST_ENV_ID}' not found"):
            get_environment_build_logs(TEST_ENV_ID, settings=mock_settings)

    @responses.activate
    def test_get_environment_build_logs_server_error(self, mock_settings):
        """Test handling server error."""
        responses.add(
            responses.GET,
            f"https://api.dev.covalent.xyz/api/v2/envs/{TEST_ENV_ID}/logs",
            status=500,
        )

        with pytest.raises(CovalentSDKError):
            get_environment_build_logs(TEST_ENV_ID, settings=mock_settings)

    @responses.activate
    def test_get_environment_build_logs_empty_response(self, mock_settings):
        """Test handling empty logs response."""
        logs_response = {
            "events": [],
            "nextForwardToken": None,
        }

        responses.add(
            responses.GET,
            f"https://api.dev.covalent.xyz/api/v2/envs/{TEST_ENV_ID}/logs",
            json=logs_response,
            status=200,
        )

        result = get_environment_build_logs(TEST_ENV_ID, settings=mock_settings)

        assert isinstance(result, EnvironmentLogs)
        assert len(result.events) == 0
        assert result.next_token is None

    @responses.activate
    def test_get_environment_build_logs_network_error(self, mock_settings):
        """Test handling network error."""
        responses.add(
            responses.GET,
            f"https://api.dev.covalent.xyz/api/v2/envs/{TEST_ENV_ID}/logs",
            body=requests.exceptions.ConnectionError("Connection error"),
        )

        with pytest.raises(CovalentSDKError, match="Connection error"):
            get_environment_build_logs(TEST_ENV_ID, settings=mock_settings)

    def test_get_environment_build_logs_default_limit(self, mock_settings):
        """Test default limit parameter."""
        with patch("covalent_cloud.swe_management.swe_manager.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.json.return_value = {"events": [], "nextForwardToken": None}
            mock_client.get.return_value = mock_response
            mock_get_client.return_value = mock_client

            get_environment_build_logs(TEST_ENV_ID, settings=mock_settings)

            # Check default limit
            call_args = mock_client.get.call_args
            params = call_args[1]["request_options"]["params"]
            assert params["limit"] == 10000


class TestListHardware:
    """Test cases for list_hardware function."""

    @responses.activate
    def test_list_hardware_success(self, mock_settings):
        """Test listing hardware successfully."""
        hardware_response = {
            "hardware": [
                {
                    "id": "hw-1",
                    "name": "CPU Small",
                    "provider": "covalent",
                    "status": "ACTIVE",
                    "cost_per_hour": 0.10,
                    "display_cost": "$0.10",
                    "gpu_type": None,
                    "gpus_allowed": [],
                    "memory": 2048,
                    "vcpus": 2,
                    "gpu_memory": None,
                    "gpu_vendor": None,
                    "vcpu_type": "Intel Xeon",
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                    "is_active": True,
                },
                {
                    "id": "hw-2",
                    "name": "GPU Large",
                    "provider": "covalent",
                    "status": "ACTIVE",
                    "cost_per_hour": 2.50,
                    "display_cost": "$2.50",
                    "gpu_type": "Tesla V100",
                    "gpus_allowed": [1, 2, 4],
                    "memory": 16384,
                    "vcpus": 8,
                    "gpu_memory": 16384,
                    "gpu_vendor": "NVIDIA",
                    "vcpu_type": "Intel Xeon",
                    "gpu_cuda_cores": 5120,
                    "gpu_tensor_cores": 640,
                    "gpu_tensor_core_type": "Volta",
                    "gpu_memory_type": "HBM2",
                    "gpu_compute_capability": "7.0",
                    "gpu_interconnect": "NVLink",
                    "memory_per_gpu": 8192,
                    "vcpu_per_gpu": 4,
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                    "is_active": True,
                },
            ],
            "metadata": {"total_count": 2, "count": 2, "page": 0},
        }

        responses.add(
            responses.GET,
            "https://api.dev.covalent.xyz/api/v2/hardware",
            json=hardware_response,
            status=200,
        )

        result = list_hardware(mock_settings)

        assert isinstance(result, list)
        assert len(result) == 2

        # Check CPU hardware
        cpu_hw = result[0]
        assert isinstance(cpu_hw, HardwareSpec)
        assert cpu_hw.name == "CPU Small"
        assert cpu_hw.cost_per_hour == 0.10
        assert cpu_hw.display_cost == "$0.10"
        assert cpu_hw.vcpus == 2
        assert cpu_hw.memory == 2048
        assert not cpu_hw.has_gpu

        # Check GPU hardware
        gpu_hw = result[1]
        assert isinstance(gpu_hw, HardwareSpec)
        assert gpu_hw.name == "GPU Large"
        assert gpu_hw.cost_per_hour == 2.50
        assert gpu_hw.gpu_type == "Tesla V100"
        assert gpu_hw.gpu_vendor == "NVIDIA"
        assert gpu_hw.has_gpu

    @responses.activate
    def test_list_hardware_empty_response(self, mock_settings):
        """Test handling empty hardware list."""
        responses.add(
            responses.GET,
            "https://api.dev.covalent.xyz/api/v2/hardware",
            json={"hardware": [], "metadata": {"total_count": 0, "count": 0, "page": 0}},
            status=200,
        )

        result = list_hardware(mock_settings)

        assert isinstance(result, list)
        assert len(result) == 0

    @responses.activate
    def test_list_hardware_api_error(self, mock_settings):
        """Test error handling for API failure."""
        responses.add(
            responses.GET,
            "https://api.dev.covalent.xyz/api/v2/hardware",
            status=500,
        )

        with pytest.raises(CovalentGenericAPIError):
            list_hardware(mock_settings)


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    @responses.activate
    def test_get_environment_yaml_large_file(self, mock_settings):
        """Test handling large YAML files."""
        env_details_response = {
            "id": TEST_ENV_ID,
            "definition": "https://s3.amazonaws.com/bucket/large-env.yaml",
        }

        # Create a large YAML content
        large_yaml = "name: large-environment\ndependencies:\n" + "\n".join(
            [f"  - package{i}=1.0" for i in range(1000)]
        )

        responses.add(
            responses.GET,
            f"https://api.dev.covalent.xyz/api/v2/envs/{TEST_ENV_ID}",
            json=env_details_response,
            status=200,
        )

        responses.add(
            responses.GET,
            "https://s3.amazonaws.com/bucket/large-env.yaml",
            body=large_yaml,
            status=200,
        )

        result = get_environment_yaml(TEST_ENV_ID, settings=mock_settings)

        assert result == large_yaml
        assert len(result) > 10000  # Verify it's actually large

    @responses.activate
    def test_get_environment_build_logs_many_events(self, mock_settings):
        """Test handling many log events."""
        # Create many log events
        events = [
            {
                "timestamp": 1640995200000 + i * 1000,
                "message": f"Log event {i}",
            }
            for i in range(100)
        ]

        logs_response = {
            "events": events,
            "nextForwardToken": None,
        }

        responses.add(
            responses.GET,
            f"https://api.dev.covalent.xyz/api/v2/envs/{TEST_ENV_ID}/logs",
            json=logs_response,
            status=200,
        )

        result = get_environment_build_logs(TEST_ENV_ID, settings=mock_settings)

        assert isinstance(result, EnvironmentLogs)
        assert len(result.events) == 100
        assert result.events[0].message == "Log event 0"
        assert result.events[99].message == "Log event 99"

    def test_environment_name_with_special_characters(self, mock_settings):
        """Test environment name with special characters."""
        # Should handle names with hyphens and underscores
        env_name = "test-env_123"

        with patch(
            "covalent_cloud.swe_management.swe_manager._get_envs_filtered"
        ) as mock_get_envs:
            mock_get_envs.return_value = {}  # Will cause not found error

            with pytest.raises(CovalentSDKError, match=r"Environment 'test-env_123' not found."):
                get_environment_yaml(env_name, settings=mock_settings)


class TestModels:
    """Test cases for new model classes."""

    def test_log_event_creation(self):
        """Test LogEvent model creation."""
        event = LogEvent(timestamp=datetime(2024, 1, 1, 12, 0, 0), message="Test log message")

        assert isinstance(event.timestamp, datetime)
        assert event.message == "Test log message"

    def test_environment_logs_creation(self):
        """Test EnvironmentLogs model creation."""
        events = [
            LogEvent(timestamp=datetime(2024, 1, 1, 12, 0, 0), message="Event 1"),
            LogEvent(timestamp=datetime(2024, 1, 1, 12, 1, 0), message="Event 2"),
        ]

        logs = EnvironmentLogs(events=events, next_token="token_123")

        assert len(logs.events) == 2
        assert logs.events[0].message == "Event 1"
        assert logs.next_token == "token_123"

    def test_environment_logs_server_response_conversion(self):
        """Test EnvironmentLogs conversion from server response format."""
        server_response = {
            "events": [
                {
                    "timestamp": 1640995200000,  # milliseconds
                    "message": "Build started",
                },
                {
                    "timestamp": 1640995260000,
                    "message": "Build finished",
                },
            ],
            "nextForwardToken": "forward_token_123",
        }

        logs = EnvironmentLogs.model_validate(server_response)

        assert len(logs.events) == 2
        assert logs.events[0].message == "Build started"
        assert logs.next_token == "forward_token_123"

    def test_hardware_spec_creation(self):
        """Test HardwareSpec model creation."""
        hardware = HardwareSpec(
            id="hw-123",
            name="Test Hardware",
            provider="covalent",
            status="ACTIVE",
            cost_per_hour=1.25,
            display_cost="$1.25",
            memory=4096,
            vcpus=4,
            created_at=datetime(2024, 1, 1, 12, 0, 0),
            updated_at=datetime(2024, 1, 1, 12, 0, 0),
            is_active=True,
        )

        assert hardware.name == "Test Hardware"
        assert hardware.cost_per_hour == 1.25
        assert hardware.vcpus == 4
        assert not hardware.has_gpu  # No GPU type specified

    def test_hardware_spec_with_gpu(self):
        """Test HardwareSpec with GPU configuration."""
        hardware = HardwareSpec(
            id="hw-gpu-123",
            name="GPU Hardware",
            provider="covalent",
            status="ACTIVE",
            cost_per_hour=3.50,
            display_cost="$3.50",
            gpu_type="Tesla A100",
            gpu_vendor="NVIDIA",
            memory=8192,
            vcpus=8,
            created_at=datetime(2024, 1, 1, 12, 0, 0),
            updated_at=datetime(2024, 1, 1, 12, 0, 0),
            is_active=True,
        )

        assert hardware.gpu_type == "Tesla A100"
        assert hardware.gpu_vendor == "NVIDIA"
        assert hardware.has_gpu  # Should be True due to gpu_type
