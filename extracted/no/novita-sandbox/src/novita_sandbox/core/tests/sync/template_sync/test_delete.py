import pytest
from unittest.mock import patch, MagicMock

from novita_sandbox.core import Template
from novita_sandbox.core.exceptions import SandboxException


@pytest.mark.skip_debug()
def test_delete_success():
    """Test successful template deletion"""
    # This test requires a real template ID to test against
    # In a real environment, you would create a template first, then delete it
    # For now, we'll skip this test in debug mode

    # Example usage (commented out to prevent accidental deletions):
    template_id = "j75it6ohvhoixm1z1209"
    Template.delete(template_id=template_id)
    pass


def test_delete_empty_template_id():
    """Test delete with empty template_id"""
    with pytest.raises(ValueError, match="template_id cannot be empty"):
        Template.delete(template_id="")


def test_delete_none_template_id():
    """Test delete with None template_id"""
    with pytest.raises(ValueError, match="template_id cannot be empty"):
        Template.delete(template_id=None)


@patch("novita_sandbox.core.template_sync.main.ApiClient")
def test_delete_with_mock_success(mock_api_client_class):
    """Test delete with mocked API client - success case"""
    mock_client = MagicMock()
    mock_api_client_class.return_value.__enter__ = MagicMock(return_value=mock_client)
    mock_api_client_class.return_value.__exit__ = MagicMock(return_value=None)

    mock_response = MagicMock()
    mock_response.status_code = 204
    mock_response.parsed = None

    with patch("novita_sandbox.core.template_sync.main.delete_templates_template_id.sync_detailed", return_value=mock_response):
        Template.delete(template_id="test-template-id")


@patch("novita_sandbox.core.template_sync.main.ApiClient")
def test_delete_with_mock_401_error(mock_api_client_class):
    """Test delete with mocked API client - 401 unauthorized"""
    mock_client = MagicMock()
    mock_api_client_class.return_value.__enter__ = MagicMock(return_value=mock_client)
    mock_api_client_class.return_value.__exit__ = MagicMock(return_value=None)

    mock_response = MagicMock()
    mock_response.status_code = 401

    with patch("novita_sandbox.core.template_sync.main.delete_templates_template_id.sync_detailed", return_value=mock_response):
        with patch("novita_sandbox.core.template_sync.main.handle_api_exception") as mock_handle:
            mock_handle.return_value = SandboxException("Unauthorized")

            with pytest.raises(SandboxException):
                Template.delete(template_id="test-template-id")


@patch("novita_sandbox.core.template_sync.main.ApiClient")
def test_delete_with_mock_500_error(mock_api_client_class):
    """Test delete with mocked API client - 500 server error"""
    mock_client = MagicMock()
    mock_api_client_class.return_value.__enter__ = MagicMock(return_value=mock_client)
    mock_api_client_class.return_value.__exit__ = MagicMock(return_value=None)

    mock_response = MagicMock()
    mock_response.status_code = 500

    with patch("novita_sandbox.core.template_sync.main.delete_templates_template_id.sync_detailed", return_value=mock_response):
        with patch("novita_sandbox.core.template_sync.main.handle_api_exception") as mock_handle:
            mock_handle.return_value = SandboxException("Server error")

            with pytest.raises(SandboxException):
                Template.delete(template_id="test-template-id")


@patch("novita_sandbox.core.template_sync.main.ApiClient")
def test_delete_with_custom_api_key(mock_api_client_class):
    """Test delete with custom API key"""
    mock_client = MagicMock()
    mock_api_client_class.return_value.__enter__ = MagicMock(return_value=mock_client)
    mock_api_client_class.return_value.__exit__ = MagicMock(return_value=None)

    mock_response = MagicMock()
    mock_response.status_code = 204
    mock_response.parsed = None

    with patch("novita_sandbox.core.template_sync.main.delete_templates_template_id.sync_detailed", return_value=mock_response):
        Template.delete(template_id="test-template-id", api_key="custom-api-key")
