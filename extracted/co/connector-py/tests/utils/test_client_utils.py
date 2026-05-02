import json

import httpx
import pytest
from connector.error import ConnectorError
from connector.utils.client_utils import create_client_response
from connector_sdk_types.generated import ConnectorErrorCode
from pydantic import BaseModel


class SampleDTO(BaseModel):
    id: str
    name: str
    active: bool = True


class TestCreateClientResponse:
    """Test cases for the create_client_response function."""

    def test_successful_response_parsing(self):
        """Test that a successful response with valid JSON is parsed correctly."""
        mock_response = httpx.Response(
            200,
            json={"id": "123", "name": "test_user", "active": True},
            request=httpx.Request("GET", "https://example.com/api/users"),
        )

        result = create_client_response(mock_response, SampleDTO)

        assert isinstance(result, SampleDTO)
        assert result.id == "123"
        assert result.name == "test_user"
        assert result.active is True

    def test_json_decode_error_raises_connector_error(self):
        """Test that JSONDecodeError is caught and converted to ConnectorError with proper message format."""
        invalid_json = "{ invalid json }"
        status_code = 200
        url = "https://example.com/api/users"
        mock_response = httpx.Response(
            status_code,
            text=invalid_json,
            request=httpx.Request("GET", url),
        )

        with pytest.raises(ConnectorError) as exc_info:
            create_client_response(mock_response, SampleDTO)

        assert exc_info.value.error_code == ConnectorErrorCode.INVALID_RESPONSE
        assert f"[{status_code}]" in exc_info.value.message
        assert url in exc_info.value.message
        assert invalid_json in exc_info.value.message
        assert isinstance(exc_info.value.__cause__, json.JSONDecodeError)

    def test_json_decode_error_with_query_params_in_url(self):
        """Test that URL with query parameters is handled correctly."""
        invalid_json = "error"
        mock_response = httpx.Response(
            200,
            text=invalid_json,
            request=httpx.Request("GET", "https://example.com/api/users?page=1&limit=10"),
        )

        with pytest.raises(ConnectorError) as exc_info:
            create_client_response(mock_response, SampleDTO)

        assert "https://example.com/api/users?page=1&limit=10" in exc_info.value.message
        assert exc_info.value.error_code == ConnectorErrorCode.INVALID_RESPONSE

    def test_json_decode_error_with_empty_response(self):
        """Test that empty response text is handled correctly."""
        mock_response = httpx.Response(
            200,
            text="",
            request=httpx.Request("GET", "https://example.com/api/users"),
        )

        with pytest.raises(ConnectorError) as exc_info:
            create_client_response(mock_response, SampleDTO)

        assert "[200][https://example.com/api/users]: " in exc_info.value.message
        assert exc_info.value.error_code == ConnectorErrorCode.INVALID_RESPONSE
