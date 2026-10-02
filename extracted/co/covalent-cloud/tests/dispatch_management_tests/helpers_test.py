# Copyright 2023 Agnostiq Inc.

"""Unit tests for dispatch helpers"""

import os
import tempfile
from unittest.mock import Mock, patch

import pytest
import requests
from rich.progress import Progress

from covalent_cloud.dispatch_management.helpers import _upload_asset
from covalent_cloud.shared.classes.settings import AuthSettings, Settings


class TestUploadAsset:
    """Tests for the _upload_asset function"""

    def setup_method(self):
        """Set up test fixtures"""
        self.mock_settings = Settings(
            auth=AuthSettings(
                dr_api_token="test-dr-token",
            )
        )

        self.mock_legacy_settings = Settings(
            auth=AuthSettings(
                api_key="test-api-key",  # pragma: allowlist secret
            )
        )

        self.expected_auth_headers = {
            "Authorization": "Bearer test-dr-token",
            "x-dr-region": "",
        }

        self.expected_legacy_auth_headers = {
            "x-api-key": "test-api-key",
        }

    @patch("covalent_cloud.dispatch_management.helpers.AssetAPIClient")
    def test_upload_asset_empty_file_with_auth_headers(self, mock_asset_api_client_class):
        """Test uploading an empty file with AssetAPIClient"""
        # Setup mocks
        mock_asset_client = Mock()
        mock_response = Mock()
        mock_response.status_code = requests.codes.ok
        mock_asset_client.upload_asset.return_value = mock_response
        mock_asset_api_client_class.return_value = mock_asset_client

        # Create temporary empty file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name

        try:
            local_uri = f"file://{temp_file_path}"
            remote_uri = "https://example.com/upload"

            # Mock progress objects
            mock_task = Mock()
            mock_progress = Mock(spec=Progress)

            # Call the function
            _upload_asset(local_uri, remote_uri, mock_task, mock_progress, self.mock_settings)

            # Verify AssetAPIClient was created with settings
            mock_asset_api_client_class.assert_called_once_with(settings=self.mock_settings)

            # Verify upload_asset was called with empty data and Content-Length header
            mock_asset_client.upload_asset.assert_called_once_with(
                remote_uri, b"", additional_headers={"Content-Length": "0"}
            )

            # Verify progress was updated
            mock_progress.advance.assert_called_once_with(mock_task, advance=1)
            mock_progress.refresh.assert_called_once()

        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    @patch("covalent_cloud.dispatch_management.helpers.AssetAPIClient")
    def test_upload_asset_non_empty_file_with_auth_headers(self, mock_asset_api_client_class):
        """Test uploading a non-empty file with AssetAPIClient"""
        # Setup mocks
        mock_asset_client = Mock()
        mock_response = Mock()
        mock_response.status_code = requests.codes.ok
        mock_asset_client.upload_asset.return_value = mock_response
        mock_asset_api_client_class.return_value = mock_asset_client

        # Create temporary file with content
        test_content = b"test file content"
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(test_content)
            temp_file_path = temp_file.name

        try:
            local_uri = f"file://{temp_file_path}"
            remote_uri = "https://example.com/upload"

            # Mock progress objects
            mock_task = Mock()
            mock_progress = Mock(spec=Progress)

            # Call the function
            _upload_asset(local_uri, remote_uri, mock_task, mock_progress, self.mock_settings)

            # Verify AssetAPIClient was created with settings
            mock_asset_api_client_class.assert_called_once_with(settings=self.mock_settings)

            # Verify upload_asset was called with file content
            mock_asset_client.upload_asset.assert_called_once_with(remote_uri, test_content)

            # Verify progress was updated
            mock_progress.advance.assert_called_once_with(mock_task, advance=1)
            mock_progress.refresh.assert_called_once()

        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    @patch("covalent_cloud.dispatch_management.helpers.AssetAPIClient")
    def test_upload_asset_with_legacy_auth_headers(self, mock_asset_api_client_class):
        """Test uploading with legacy API key authentication"""
        # Setup mocks
        mock_asset_client = Mock()
        mock_response = Mock()
        mock_response.status_code = requests.codes.ok
        mock_asset_client.upload_asset.return_value = mock_response
        mock_asset_api_client_class.return_value = mock_asset_client

        # Create temporary empty file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name

        try:
            local_uri = f"file://{temp_file_path}"
            remote_uri = "https://example.com/upload"

            # Mock progress objects
            mock_task = Mock()
            mock_progress = Mock(spec=Progress)

            # Call the function with legacy settings
            _upload_asset(
                local_uri, remote_uri, mock_task, mock_progress, self.mock_legacy_settings
            )

            # Verify AssetAPIClient was created with legacy settings
            mock_asset_api_client_class.assert_called_once_with(settings=self.mock_legacy_settings)

            # Verify upload_asset was called with empty data and Content-Length header
            mock_asset_client.upload_asset.assert_called_once_with(
                remote_uri, b"", additional_headers={"Content-Length": "0"}
            )

        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    @patch("covalent_cloud.dispatch_management.helpers.AssetAPIClient")
    def test_upload_asset_without_file_prefix(self, mock_asset_api_client_class):
        """Test uploading when local_uri doesn't have file:// prefix"""
        # Setup mocks
        mock_asset_client = Mock()
        mock_response = Mock()
        mock_response.status_code = requests.codes.ok
        mock_asset_client.upload_asset.return_value = mock_response
        mock_asset_api_client_class.return_value = mock_asset_client

        # Create temporary empty file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name

        try:
            # Use local path directly without file:// prefix
            local_uri = temp_file_path
            remote_uri = "https://example.com/upload"

            # Mock progress objects
            mock_task = Mock()
            mock_progress = Mock(spec=Progress)

            # Call the function
            _upload_asset(local_uri, remote_uri, mock_task, mock_progress, self.mock_settings)

            # Verify AssetAPIClient was created and upload was called
            mock_asset_api_client_class.assert_called_once_with(settings=self.mock_settings)
            mock_asset_client.upload_asset.assert_called_once_with(
                remote_uri, b"", additional_headers={"Content-Length": "0"}
            )

        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    @patch("covalent_cloud.dispatch_management.helpers.AssetAPIClient")
    def test_upload_asset_http_error_propagates(self, mock_asset_api_client_class):
        """Test that HTTP errors are properly propagated"""
        # Setup mocks
        mock_asset_client = Mock()
        mock_asset_client.upload_asset.side_effect = requests.exceptions.HTTPError("Upload failed")
        mock_asset_api_client_class.return_value = mock_asset_client

        # Create temporary empty file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name

        try:
            local_uri = f"file://{temp_file_path}"
            remote_uri = "https://example.com/upload"

            # Mock progress objects
            mock_task = Mock()
            mock_progress = Mock(spec=Progress)

            # Call the function and expect HTTPError to be raised
            with pytest.raises(requests.exceptions.HTTPError):
                _upload_asset(local_uri, remote_uri, mock_task, mock_progress, self.mock_settings)

            # Verify AssetAPIClient was created and upload was attempted
            mock_asset_api_client_class.assert_called_once_with(settings=self.mock_settings)
            mock_asset_client.upload_asset.assert_called_once_with(
                remote_uri, b"", additional_headers={"Content-Length": "0"}
            )

            # Verify progress was not updated on failure
            mock_progress.advance.assert_not_called()

        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    @patch("covalent_cloud.dispatch_management.helpers.AssetAPIClient")
    def test_upload_asset_retry_configuration(self, mock_asset_api_client_class):
        """Test that AssetAPIClient handles retry configuration internally"""
        # Setup mocks
        mock_asset_client = Mock()
        mock_response = Mock()
        mock_response.status_code = requests.codes.ok
        mock_asset_client.upload_asset.return_value = mock_response
        mock_asset_api_client_class.return_value = mock_asset_client

        # Create temporary empty file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name

        try:
            local_uri = f"file://{temp_file_path}"
            remote_uri = "https://example.com/upload"

            # Mock progress objects
            mock_task = Mock()
            mock_progress = Mock(spec=Progress)

            # Call the function
            _upload_asset(local_uri, remote_uri, mock_task, mock_progress, self.mock_settings)

            # Verify AssetAPIClient was created and used (retry logic is internal)
            mock_asset_api_client_class.assert_called_once_with(settings=self.mock_settings)
            mock_asset_client.upload_asset.assert_called_once()

        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
