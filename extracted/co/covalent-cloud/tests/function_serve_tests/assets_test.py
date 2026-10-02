# Copyright 2024 Agnostiq Inc.

"""Unit tests for function serve assets"""

from unittest.mock import Mock, patch

import pytest
import requests

from covalent_cloud.function_serve.assets import AssetsMediator
from covalent_cloud.function_serve.common import ServeAssetType
from covalent_cloud.function_serve.models import ServeAsset
from covalent_cloud.shared.classes.settings import AuthSettings, Settings


class TestAssetsMediator:
    """Tests for the AssetsMediator class"""

    def setup_method(self):
        """Set up test fixtures"""
        self.mock_settings = Settings(
            auth=AuthSettings(
                dr_api_token="test-dr-token",
            )
        )

        self.mock_legacy_settings = Settings(
            auth=AuthSettings(
                api_key="test-api-key",
            )
        )

        self.expected_auth_headers = {
            "Authorization": "Bearer test-dr-token",
            "x-dr-region": "",
        }

        self.expected_legacy_auth_headers = {
            "x-api-key": "test-api-key",
        }

    @patch("covalent_cloud.function_serve.assets.AssetAPIClient")
    def test_upload_asset_with_auth_headers_json_type(self, mock_asset_api_client_class):
        """Test uploading a JSON type asset includes auth headers for non-S3 URLs"""
        # Setup mocks
        mock_asset_client = Mock()
        mock_response = Mock()
        mock_asset_client.upload_asset.return_value = mock_response
        mock_asset_api_client_class.return_value = mock_asset_client

        # Create a test ServeAsset
        test_asset = ServeAsset(
            type=ServeAssetType.JSON,
            serialized_object=b'{"test": "data"}',
            url="https://example.com/upload/test-asset",
        )

        # Store original values before they get cleared
        original_url = test_asset.url
        original_data = test_asset.serialized_object

        # Call the function
        with patch("covalent_cloud.function_serve.assets.settings", self.mock_settings):
            AssetsMediator.upload_asset(test_asset, self.mock_settings)

        # Verify AssetAPIClient was created with settings
        mock_asset_api_client_class.assert_called_once_with(settings=self.mock_settings)

        # Verify upload_asset was called with correct parameters
        mock_asset_client.upload_asset.assert_called_once_with(original_url, original_data)

        # Verify asset fields were cleared after upload
        assert test_asset.url is None
        assert test_asset.serialized_object is None

    @patch("covalent_cloud.function_serve.assets.AssetAPIClient")
    @patch("covalent_cloud.function_serve.assets.ct.TransportableObject")
    def test_upload_asset_with_auth_headers_asset_type(
        self, mock_transportable_object_class, mock_asset_api_client_class
    ):
        """Test uploading an ASSET type includes auth headers for non-S3 URLs"""
        # Setup mocks
        mock_asset_client = Mock()
        mock_response = Mock()
        mock_asset_client.upload_asset.return_value = mock_response
        mock_asset_api_client_class.return_value = mock_asset_client

        # Mock TransportableObject
        mock_transportable_obj = Mock()
        mock_serialized_data = b"serialized_asset_data"
        mock_transportable_obj.serialize.return_value = mock_serialized_data
        mock_transportable_object_class.deserialize.return_value = mock_transportable_obj

        # Create a test ServeAsset
        test_asset = ServeAsset(
            type=ServeAssetType.ASSET,
            serialized_object="mock_serialized_transportable_object",
            url="https://example.com/upload/test-asset",
        )

        # Store original values before they get cleared
        original_url = test_asset.url
        original_serialized_object = test_asset.serialized_object

        # Call the function
        with patch("covalent_cloud.function_serve.assets.settings", self.mock_settings):
            AssetsMediator.upload_asset(test_asset, self.mock_settings)

        # Verify AssetAPIClient was created with settings
        mock_asset_api_client_class.assert_called_once_with(settings=self.mock_settings)

        # Verify TransportableObject was deserialized and serialized
        mock_transportable_object_class.deserialize.assert_called_once_with(
            original_serialized_object
        )
        mock_transportable_obj.serialize.assert_called_once()

        # Verify upload_asset was called with correct parameters
        mock_asset_client.upload_asset.assert_called_once_with(original_url, mock_serialized_data)

        # Verify asset fields were cleared after upload
        assert test_asset.url is None
        assert test_asset.serialized_object is None

    @patch("covalent_cloud.function_serve.assets.AssetAPIClient")
    def test_upload_asset_with_legacy_auth_headers(self, mock_asset_api_client_class):
        """Test uploading with legacy API key authentication"""
        # Setup mocks
        mock_asset_client = Mock()
        mock_response = Mock()
        mock_asset_client.upload_asset.return_value = mock_response
        mock_asset_api_client_class.return_value = mock_asset_client

        # Create a test ServeAsset
        test_asset = ServeAsset(
            type=ServeAssetType.JSON,
            serialized_object=b'{"test": "data"}',
            url="https://example.com/upload/test-asset",
        )

        # Store original values before they get cleared
        original_url = test_asset.url
        original_data = test_asset.serialized_object

        # Call the function with legacy settings
        with patch("covalent_cloud.function_serve.assets.settings", self.mock_legacy_settings):
            AssetsMediator.upload_asset(test_asset, self.mock_legacy_settings)

        # Verify AssetAPIClient was created with legacy settings
        mock_asset_api_client_class.assert_called_once_with(settings=self.mock_legacy_settings)

        # Verify upload_asset was called with correct parameters
        mock_asset_client.upload_asset.assert_called_once_with(original_url, original_data)

        # Verify asset fields were cleared after upload
        assert test_asset.url is None
        assert test_asset.serialized_object is None

    @patch("covalent_cloud.function_serve.assets.AssetAPIClient")
    @patch("covalent_cloud.function_serve.assets.get_deployment_client")
    def test_upload_asset_with_none_url_gets_presigned_url(
        self, mock_get_deployment_client, mock_asset_api_client_class
    ):
        """Test that when URL is None, a presigned URL is obtained from deployment client"""
        # Setup mocks
        mock_asset_client = Mock()
        mock_response = Mock()
        mock_asset_client.upload_asset.return_value = mock_response
        mock_asset_api_client_class.return_value = mock_asset_client

        # Mock deployment client response
        mock_deployment_client = Mock()
        mock_presigned_response = Mock()
        mock_presigned_response.json.return_value = [
            {"url": "https://presigned.url/upload", "id": "asset-id-123"}
        ]
        mock_deployment_client.post.return_value = mock_presigned_response
        mock_get_deployment_client.return_value = mock_deployment_client

        # Create a test ServeAsset with no URL
        test_asset = ServeAsset(
            type=ServeAssetType.JSON,
            serialized_object=b'{"test": "data"}',
            url=None,  # No URL provided
        )

        # Store original data before it gets cleared
        original_data = test_asset.serialized_object

        # Call the function
        with patch("covalent_cloud.function_serve.assets.settings", self.mock_settings):
            AssetsMediator.upload_asset(test_asset, self.mock_settings)

        # Verify deployment client was used to get presigned URL
        mock_get_deployment_client.assert_called_once_with(self.mock_settings)
        mock_deployment_client.post.assert_called_once_with("/assets")
        mock_presigned_response.json.assert_called_once()

        # Verify AssetAPIClient was created and upload was called
        mock_asset_api_client_class.assert_called_once_with(settings=self.mock_settings)
        mock_asset_client.upload_asset.assert_called_once_with(
            "https://presigned.url/upload", original_data
        )

        # Verify asset fields were cleared and updated
        assert test_asset.url is None  # Gets cleared after upload
        assert test_asset.serialized_object is None
        assert test_asset.id == "asset-id-123"  # Should be set from response

    @patch("covalent_cloud.function_serve.assets.AssetAPIClient")
    def test_upload_asset_http_error_propagates(self, mock_asset_api_client_class):
        """Test that HTTP errors are properly propagated"""
        # Setup mocks
        mock_asset_client = Mock()
        mock_asset_client.upload_asset.side_effect = requests.exceptions.HTTPError("Upload failed")
        mock_asset_api_client_class.return_value = mock_asset_client

        # Create a test ServeAsset
        test_asset = ServeAsset(
            type=ServeAssetType.JSON,
            serialized_object=b'{"test": "data"}',
            url="https://example.com/upload/test-asset",
        )

        # Store original values before they might get cleared
        original_url = test_asset.url
        original_data = test_asset.serialized_object

        # Call the function and expect HTTPError to be raised
        with patch("covalent_cloud.function_serve.assets.settings", self.mock_settings):
            with pytest.raises(requests.exceptions.HTTPError):
                AssetsMediator.upload_asset(test_asset, self.mock_settings)

        # Verify AssetAPIClient was created and upload was attempted
        mock_asset_api_client_class.assert_called_once_with(settings=self.mock_settings)
        mock_asset_client.upload_asset.assert_called_once_with(original_url, original_data)

    def test_upload_asset_unsupported_type_raises_error(self):
        """Test that unsupported asset types raise ValueError"""
        # Create a test ServeAsset with unsupported type
        test_asset = ServeAsset(
            type="UNSUPPORTED_TYPE",  # Invalid type
            serialized_object=b'{"test": "data"}',
            url="https://example.com/upload/test-asset",
        )

        # Call the function and expect ValueError to be raised
        with pytest.raises(ValueError, match="Unsupported asset type: 'UNSUPPORTED_TYPE'"):
            AssetsMediator.upload_asset(test_asset, self.mock_settings)

    @patch("covalent_cloud.function_serve.assets.AssetAPIClient")
    def test_upload_asset_retry_configuration(self, mock_asset_api_client_class):
        """Test that AssetAPIClient handles retry configuration internally"""
        # Setup mocks
        mock_asset_client = Mock()
        mock_response = Mock()
        mock_asset_client.upload_asset.return_value = mock_response
        mock_asset_api_client_class.return_value = mock_asset_client

        # Create a test ServeAsset
        test_asset = ServeAsset(
            type=ServeAssetType.JSON,
            serialized_object=b'{"test": "data"}',
            url="https://example.com/upload/test-asset",
        )

        # Call the function
        with patch("covalent_cloud.function_serve.assets.settings", self.mock_settings):
            AssetsMediator.upload_asset(test_asset, self.mock_settings)

        # Verify AssetAPIClient was created and used (retry logic is internal)
        mock_asset_api_client_class.assert_called_once_with(settings=self.mock_settings)
        mock_asset_client.upload_asset.assert_called_once()
