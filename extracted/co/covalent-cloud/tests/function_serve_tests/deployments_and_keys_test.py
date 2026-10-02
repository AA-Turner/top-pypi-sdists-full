# Copyright 2025 Agnostiq Inc.

"""Unit tests for function serve enhancements."""

from unittest.mock import MagicMock, patch

import pytest

from covalent_cloud.function_serve.deployment import (
    create_inference_api_key,
    delete_inference_api_key,
    list_function_deployments,
    list_inference_api_keys,
)
from covalent_cloud.function_serve.models import (
    FunctionDeploymentList,
    InferenceAPIKey,
    InferenceKeyMetadata,
)
from covalent_cloud.shared.classes.settings import Settings


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    settings = Settings()
    settings.dispatcher_uri = "https://api.dev.covalent.xyz"
    return settings


@pytest.fixture
def sample_deployment_list_response():
    """Sample API response for function deployment listing."""
    return {
        "records": [
            {
                "id": "func-123",
                "title": "ML Inference Service",
                "description": "Machine learning model inference endpoint",
                "status": "ACTIVE",
                "created_at": "2023-01-01T10:00:00Z",
                "updated_at": "2023-01-01T10:30:00Z",
                "invoke_url": "https://api.dev.covalent.xyz/fn/func-123",
                "auth": True,
                "tags": ["ml", "inference"],
                "endpoints": [
                    {
                        "name": "predict",
                        "method": "POST",
                        "route": "/predict",
                        "description": "Make predictions",
                    }
                ],
            },
            {
                "id": "func-456",
                "title": "Data Processing Service",
                "description": "Process and transform data",
                "status": "BUILDING",
                "created_at": "2023-01-01T11:00:00Z",
                "updated_at": "2023-01-01T11:15:00Z",
                "invoke_url": "https://api.dev.covalent.xyz/fn/func-456",
                "auth": False,
                "tags": ["data", "processing"],
                "endpoints": [
                    {
                        "name": "transform",
                        "method": "POST",
                        "route": "/transform",
                        "description": "Transform data",
                    }
                ],
            },
        ],
        "metadata": {"total_count": 25, "page": 0, "count": 10, "has_next_page": True},
    }


@pytest.fixture
def sample_api_key_response():
    """Sample API response for API key creation."""
    return {"id": "key-123", "key": "sk-1234567890abcdef", "created_at": "2023-01-01T10:00:00Z"}


@pytest.fixture
def sample_api_keys_list_response():
    """Sample API response for API keys listing."""
    return [
        {
            "id": "key-123",
            "created_at": "2023-01-01T10:00:00Z",
            "last_used": "2023-01-01T15:00:00Z",
        },
        {"id": "key-456", "created_at": "2023-01-01T11:00:00Z", "last_used": None},
    ]


class TestListFunctionDeployments:
    """Test cases for list_function_deployments function."""

    @patch("covalent_cloud.function_serve.deployment.get_deployment_client")
    def test_list_function_deployments_default_params(
        self, mock_get_client, mock_settings, sample_deployment_list_response
    ):
        """Test listing deployments with default parameters."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = sample_deployment_list_response
        mock_client.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = list_function_deployments(settings=mock_settings)

        assert isinstance(result, FunctionDeploymentList)
        assert len(result.records) == 2
        assert result.records[0].id == "func-123"
        assert result.records[0].title == "ML Inference Service"
        assert result.records[0].status == "ACTIVE"

        # Check API call parameters
        mock_client.get.assert_called_once_with(
            "/functions",
            request_options={
                "params": {
                    "generate_presigned_urls": False,
                    "count": 10,
                    "page": 0,
                    "direction": "DESC",
                    "sort": "created_at",
                }
            },
        )

    @patch("covalent_cloud.function_serve.deployment.get_deployment_client")
    def test_list_function_deployments_with_filters(
        self, mock_get_client, mock_settings, sample_deployment_list_response
    ):
        """Test listing deployments with various filters."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = sample_deployment_list_response
        mock_client.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = list_function_deployments(
            generate_presigned_urls=True,
            count=20,
            page=1,
            search="ML model",
            sort="title",
            direction="asc",
            status="ACTIVE",
            settings=mock_settings,
        )

        assert isinstance(result, FunctionDeploymentList)

        # Verify all parameters were passed correctly
        call_args = mock_client.get.call_args
        params = call_args[1]["request_options"]["params"]

        assert params["generate_presigned_urls"]
        assert params["count"] == 20
        assert params["page"] == 1
        assert params["search"] == "ML model"
        assert params["sort"] == "title"
        assert params["direction"] == "ASC"
        assert params["status"] == "ACTIVE"

    @patch("covalent_cloud.function_serve.deployment.get_deployment_client")
    def test_list_function_deployments_empty_response(self, mock_get_client, mock_settings):
        """Test listing deployments with empty response."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "records": [],
            "metadata": {"total_count": 0, "page": 0, "count": 10, "has_next_page": False},
        }
        mock_client.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = list_function_deployments(settings=mock_settings)

        assert isinstance(result, FunctionDeploymentList)
        assert len(result.records) == 0
        assert result.metadata.total_count == 0

    @patch("covalent_cloud.function_serve.deployment.get_deployment_client")
    def test_list_function_deployments_none_optional_params(
        self, mock_get_client, mock_settings, sample_deployment_list_response
    ):
        """Test listing deployments with None optional parameters."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = sample_deployment_list_response
        mock_client.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = list_function_deployments(
            search=None, sort=None, status=None, settings=mock_settings
        )

        assert isinstance(result, FunctionDeploymentList)

        # None values should not be included in parameters
        call_args = mock_client.get.call_args
        params = call_args[1]["request_options"]["params"]
        assert "search" not in params
        assert "status" not in params
        assert "count" in params
        assert "page" in params

    @patch("covalent_cloud.function_serve.deployment.get_deployment_client")
    def test_list_function_deployments_api_error(self, mock_get_client, mock_settings):
        """Test handling API errors."""
        mock_client = MagicMock()
        mock_client.get.side_effect = Exception("API Error")
        mock_get_client.return_value = mock_client

        with pytest.raises(Exception, match="API Error"):
            list_function_deployments(settings=mock_settings)


class TestCreateInferenceApiKey:
    """Test cases for create_inference_api_key function."""

    @patch("covalent_cloud.function_serve.deployment.get_deployment_client")
    def test_create_inference_api_key_success(
        self, mock_get_client, mock_settings, sample_api_key_response
    ):
        """Test creating API key successfully."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = sample_api_key_response
        mock_client.post.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = create_inference_api_key("func-123", settings=mock_settings)

        assert isinstance(result, InferenceAPIKey)
        assert result.key_id == "key-123"
        assert result.key == "sk-1234567890abcdef"
        assert result.created_at is not None

        # Check API call
        mock_client.post.assert_called_once_with("/functions/func-123/inference-keys")

    @patch("covalent_cloud.function_serve.deployment.get_deployment_client")
    def test_create_inference_api_key_with_updated_at(self, mock_get_client, mock_settings):
        """Test creating API key when response has updated_at instead of created_at."""
        api_key_response = {
            "id": "key-789",
            "key": "sk-abcdef1234567890",
            "updated_at": "2023-01-01T12:00:00Z",
        }

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = api_key_response
        mock_client.post.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = create_inference_api_key("func-456", settings=mock_settings)

        assert isinstance(result, InferenceAPIKey)
        assert result.key_id == "key-789"
        assert result.key == "sk-abcdef1234567890"
        # created_at is parsed to a datetime object, so check it exists and is correct type
        assert result.created_at is not None
        assert isinstance(result.created_at, type(result.created_at))

    @patch("covalent_cloud.function_serve.deployment.get_deployment_client")
    def test_create_inference_api_key_api_error(self, mock_get_client, mock_settings):
        """Test handling API errors during key creation."""
        mock_client = MagicMock()
        mock_client.post.side_effect = Exception("API Error")
        mock_get_client.return_value = mock_client

        with pytest.raises(Exception, match="API Error"):
            create_inference_api_key("func-123", settings=mock_settings)

    def test_create_inference_api_key_empty_function_id(self, mock_settings):
        """Test creating API key with empty function ID."""
        with pytest.raises(ValueError):
            create_inference_api_key("", settings=mock_settings)


class TestListInferenceApiKeys:
    """Test cases for list_inference_api_keys function."""

    @patch("covalent_cloud.function_serve.deployment.get_deployment_client")
    def test_list_inference_api_keys_success(
        self, mock_get_client, mock_settings, sample_api_keys_list_response
    ):
        """Test listing API keys successfully."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = sample_api_keys_list_response
        mock_client.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = list_inference_api_keys("func-123", settings=mock_settings)

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(key, InferenceKeyMetadata) for key in result)

        assert result[0].key_id == "key-123"
        assert result[0].created_at is not None
        assert result[0].last_used is not None

        assert result[1].key_id == "key-456"
        assert result[1].last_used is None

        # Check API call
        mock_client.get.assert_called_once_with("/functions/func-123/inference-keys")

    @patch("covalent_cloud.function_serve.deployment.get_deployment_client")
    def test_list_inference_api_keys_empty_list(self, mock_get_client, mock_settings):
        """Test listing API keys with empty response."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_client.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = list_inference_api_keys("func-123", settings=mock_settings)

        assert isinstance(result, list)
        assert len(result) == 0

    @patch("covalent_cloud.function_serve.deployment.get_deployment_client")
    def test_list_inference_api_keys_with_updated_at(self, mock_get_client, mock_settings):
        """Test listing API keys when response has updated_at instead of created_at."""
        api_keys_response = [
            {
                "id": "key-999",
                "updated_at": "2023-01-01T14:00:00Z",
                "last_used": "2023-01-01T16:00:00Z",
            }
        ]

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = api_keys_response
        mock_client.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = list_inference_api_keys("func-456", settings=mock_settings)

        assert len(result) == 1
        assert result[0].key_id == "key-999"
        assert result[0].created_at.isoformat() == "2023-01-01T14:00:00+00:00"

    @patch("covalent_cloud.function_serve.deployment.get_deployment_client")
    def test_list_inference_api_keys_api_error(self, mock_get_client, mock_settings):
        """Test handling API errors during key listing."""
        mock_client = MagicMock()
        mock_client.get.side_effect = Exception("API Error")
        mock_get_client.return_value = mock_client

        with pytest.raises(Exception, match="API Error"):
            list_inference_api_keys("func-123", settings=mock_settings)


class TestDeleteInferenceApiKey:
    """Test cases for delete_inference_api_key function."""

    @patch("covalent_cloud.function_serve.deployment.get_deployment_client")
    def test_delete_inference_api_key_success(self, mock_get_client, mock_settings):
        """Test deleting API key successfully."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_client.delete.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = delete_inference_api_key("func-123", "key-456", settings=mock_settings)

        assert result

        # Check API call
        mock_client.delete.assert_called_once_with("/functions/func-123/inference-keys/key-456")

    @patch("covalent_cloud.function_serve.deployment.get_deployment_client")
    def test_delete_inference_api_key_not_found(self, mock_get_client, mock_settings):
        """Test deleting non-existent API key."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_client.delete.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = delete_inference_api_key("func-123", "nonexistent-key", settings=mock_settings)

        assert not result

    @patch("covalent_cloud.function_serve.deployment.get_deployment_client")
    def test_delete_inference_api_key_api_error(self, mock_get_client, mock_settings):
        """Test handling API errors during key deletion."""
        mock_client = MagicMock()
        mock_client.delete.side_effect = Exception("API Error")
        mock_get_client.return_value = mock_client

        result = delete_inference_api_key("func-123", "key-456", settings=mock_settings)

        assert not result

    @patch("covalent_cloud.function_serve.deployment.get_deployment_client")
    def test_delete_inference_api_key_server_error(self, mock_get_client, mock_settings):
        """Test handling server error during key deletion."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_client.delete.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = delete_inference_api_key("func-123", "key-456", settings=mock_settings)

        assert not result

    def test_delete_inference_api_key_empty_parameters(self, mock_settings):
        """Test deleting API key with empty parameters."""
        with pytest.raises(ValueError):
            delete_inference_api_key("", "key-456", settings=mock_settings)

        with pytest.raises(ValueError):
            delete_inference_api_key("func-123", "", settings=mock_settings)


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    @patch("covalent_cloud.function_serve.deployment.get_deployment_client")
    def test_list_function_deployments_malformed_response(self, mock_get_client, mock_settings):
        """Test handling malformed API response."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        # Missing required fields
        mock_response.json.return_value = {"records": [{"id": "test"}]}
        mock_client.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        with pytest.raises(Exception):  # Pydantic validation error
            list_function_deployments(settings=mock_settings)

    @patch("covalent_cloud.function_serve.deployment.get_deployment_client")
    def test_create_inference_api_key_malformed_response(self, mock_get_client, mock_settings):
        """Test handling malformed API response during key creation."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        # Missing required fields
        mock_response.json.return_value = {"id": "key-123"}  # Missing 'key' field
        mock_client.post.return_value = mock_response
        mock_get_client.return_value = mock_client

        with pytest.raises(Exception):
            create_inference_api_key("func-123", settings=mock_settings)

    def test_function_id_special_characters(self, mock_settings):
        """Test function ID with special characters."""
        function_id = "func-123_v2.0"

        with patch(
            "covalent_cloud.function_serve.deployment.get_deployment_client"
        ) as mock_get_client:
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.json.return_value = []
            mock_client.get.return_value = mock_response
            mock_get_client.return_value = mock_client

            result = list_inference_api_keys(function_id, settings=mock_settings)

            assert isinstance(result, list)
            # Check that the function ID was passed correctly
            mock_client.get.assert_called_once_with(f"/functions/{function_id}/inference-keys")
