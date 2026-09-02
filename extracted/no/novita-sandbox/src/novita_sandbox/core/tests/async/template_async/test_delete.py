import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from novita_sandbox.core import AsyncTemplate
from novita_sandbox.core.exceptions import SandboxException


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_async_delete_success():
    """Test successful async template deletion"""
    pass


@pytest.mark.asyncio
async def test_async_delete_empty_template_id():
    """Test async delete with empty template_id"""
    with pytest.raises(ValueError, match="template_id cannot be empty"):
        await AsyncTemplate.delete(template_id="")


@pytest.mark.asyncio
async def test_async_delete_none_template_id():
    """Test async delete with None template_id"""
    with pytest.raises(ValueError, match="template_id cannot be empty"):
        await AsyncTemplate.delete(template_id=None)


@pytest.mark.asyncio
@patch("novita_sandbox.core.template_async.main.AsyncApiClient")
async def test_async_delete_with_mock_success(mock_async_api_client_class):
    """Test async delete with mocked API client - success case"""
    mock_client = MagicMock()
    mock_async_api_client_class.return_value.__aenter__ = AsyncMock(return_value=mock_client)
    mock_async_api_client_class.return_value.__aexit__ = AsyncMock(return_value=None)

    mock_response = MagicMock()
    mock_response.status_code = 204
    mock_response.parsed = None

    with patch("novita_sandbox.core.template_async.main.delete_templates_template_id.asyncio_detailed", new_callable=AsyncMock, return_value=mock_response):
        await AsyncTemplate.delete(template_id="test-template-id")


@pytest.mark.asyncio
@patch("novita_sandbox.core.template_async.main.AsyncApiClient")
async def test_async_delete_with_mock_401_error(mock_async_api_client_class):
    """Test async delete with mocked API client - 401 unauthorized"""
    mock_client = MagicMock()
    mock_async_api_client_class.return_value.__aenter__ = AsyncMock(return_value=mock_client)
    mock_async_api_client_class.return_value.__aexit__ = AsyncMock(return_value=None)

    mock_response = MagicMock()
    mock_response.status_code = 401

    with patch("novita_sandbox.core.template_async.main.delete_templates_template_id.asyncio_detailed", new_callable=AsyncMock, return_value=mock_response):
        with patch("novita_sandbox.core.template_async.main.handle_api_exception") as mock_handle:
            mock_handle.return_value = SandboxException("Unauthorized")

            with pytest.raises(SandboxException):
                await AsyncTemplate.delete(template_id="test-template-id")


@pytest.mark.asyncio
@patch("novita_sandbox.core.template_async.main.AsyncApiClient")
async def test_async_delete_with_mock_500_error(mock_async_api_client_class):
    """Test async delete with mocked API client - 500 server error"""
    mock_client = MagicMock()
    mock_async_api_client_class.return_value.__aenter__ = AsyncMock(return_value=mock_client)
    mock_async_api_client_class.return_value.__aexit__ = AsyncMock(return_value=None)

    mock_response = MagicMock()
    mock_response.status_code = 500

    with patch("novita_sandbox.core.template_async.main.delete_templates_template_id.asyncio_detailed", new_callable=AsyncMock, return_value=mock_response):
        with patch("novita_sandbox.core.template_async.main.handle_api_exception") as mock_handle:
            mock_handle.return_value = SandboxException("Server error")

            with pytest.raises(SandboxException):
                await AsyncTemplate.delete(template_id="test-template-id")


@pytest.mark.asyncio
@patch("novita_sandbox.core.template_async.main.AsyncApiClient")
async def test_async_delete_with_custom_api_key(mock_async_api_client_class):
    """Test async delete with custom API key"""
    mock_client = MagicMock()
    mock_async_api_client_class.return_value.__aenter__ = AsyncMock(return_value=mock_client)
    mock_async_api_client_class.return_value.__aexit__ = AsyncMock(return_value=None)

    mock_response = MagicMock()
    mock_response.status_code = 204
    mock_response.parsed = None

    with patch("novita_sandbox.core.template_async.main.delete_templates_template_id.asyncio_detailed", new_callable=AsyncMock, return_value=mock_response):
        await AsyncTemplate.delete(template_id="test-template-id", api_key="custom-api-key")
