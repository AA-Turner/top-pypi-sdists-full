# Copyright 2024 Agnostiq Inc.

"""Integration tests for asset upload authentication"""

import os
import tempfile
from unittest.mock import Mock, patch

import requests

from covalent_cloud.dispatch_management.helpers import _upload_asset
from covalent_cloud.function_serve.assets import AssetsMediator
from covalent_cloud.function_serve.common import ServeAssetType
from covalent_cloud.function_serve.models import ServeAsset
from covalent_cloud.shared.classes.settings import AuthSettings, Settings


class TestAssetUploadAuthIntegration:
    """Integration tests to verify auth headers are included in asset uploads"""

    def setup_method(self):
        """Set up test fixtures"""
        self.mock_settings = Settings(
            auth=AuthSettings(
                dr_api_token="integration-test-token",
            )
        )

        self.expected_auth_headers = {
            "Authorization": "Bearer integration-test-token",
            "x-dr-region": "",
        }

    @patch("covalent_cloud.dispatch_management.helpers.AssetAPIClient")
    def test_dispatch_upload_includes_auth_headers_integration(self, mock_asset_api_client_class):
        """Integration test: verify dispatch_management _upload_asset works with AssetAPIClient"""
        # Mock the AssetAPIClient
        mock_asset_client = Mock()
        mock_response = Mock()
        mock_response.status_code = requests.codes.ok
        mock_asset_client.upload_asset.return_value = mock_response
        mock_asset_api_client_class.return_value = mock_asset_client

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(b"test file content")
            temp_file_path = temp_file.name

        try:
            # Call the actual _upload_asset function
            _upload_asset(
                f"file://{temp_file_path}",
                "https://test-upload-endpoint.com/file",
                Mock(),
                Mock(),
                self.mock_settings,
            )

            # Verify AssetAPIClient was used correctly
            mock_asset_api_client_class.assert_called_once_with(settings=self.mock_settings)
            mock_asset_client.upload_asset.assert_called_once()

            # Verify the upload was called with correct file data
            call_args = mock_asset_client.upload_asset.call_args
            assert call_args[0][0] == "https://test-upload-endpoint.com/file"  # URL
            assert call_args[0][1] == b"test file content"  # Data

        finally:
            # Clean up
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    @patch("covalent_cloud.function_serve.assets.AssetAPIClient")
    def test_function_serve_upload_includes_auth_headers_integration(
        self, mock_asset_api_client_class
    ):
        """Integration test: verify function_serve asset upload works with AssetAPIClient"""
        # Mock the AssetAPIClient
        mock_asset_client = Mock()
        mock_response = Mock()
        mock_asset_client.upload_asset.return_value = mock_response
        mock_asset_client.get_upload_headers.return_value = self.expected_auth_headers
        mock_asset_api_client_class.return_value = mock_asset_client

        # Create a test asset (non-S3 URL should get auth headers)
        test_asset = ServeAsset(
            type=ServeAssetType.JSON,
            serialized_object=b'{"integration": "test"}',
            url="https://test-upload-endpoint.com/serve-asset",
        )

        original_url = test_asset.url
        original_data = test_asset.serialized_object

        # Call the actual AssetsMediator.upload_asset function
        with patch("covalent_cloud.function_serve.assets.settings", self.mock_settings):
            AssetsMediator.upload_asset(test_asset, self.mock_settings)

        # Verify AssetAPIClient was used correctly
        mock_asset_api_client_class.assert_called_once_with(settings=self.mock_settings)
        mock_asset_client.upload_asset.assert_called_once_with(original_url, original_data)

        # Verify asset fields were cleared
        assert test_asset.url is None
        assert test_asset.serialized_object is None

    def test_auth_headers_consistent_between_modules(self):
        """Integration test: verify both modules use AssetAPIClient consistently"""
        from covalent_cloud.shared.classes.api import AssetAPIClient

        # Test that both modules would get the same headers for the same URL
        client = AssetAPIClient(self.mock_settings)

        test_url = "https://test.com/upload"
        headers1 = client.get_headers(test_url)
        headers2 = client.get_headers(test_url)

        # Headers should be consistent
        assert headers1 == headers2, f"Inconsistent headers: {headers1} vs {headers2}"

        # Should contain auth info for non-S3 URLs
        has_bearer_auth = "Authorization" in headers1 and headers1["Authorization"].startswith(
            "Bearer"
        )
        has_api_key_auth = "x-api-key" in headers1  # pragma: allowlist secret
        assert has_bearer_auth or has_api_key_auth, f"Missing auth headers: {headers1}"

        # Test S3 URL gets no headers
        s3_url = "https://bucket.s3.amazonaws.com/key?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Signature=abc"
        s3_headers = client.get_headers(s3_url)
        assert s3_headers == {}, f"S3 URL should have no auth headers but got: {s3_headers}"

    def test_auth_header_types_with_different_settings(self):
        """Integration test: verify different settings produce appropriate auth headers"""
        from covalent_cloud.shared.classes.api import AssetAPIClient

        # Test modern DR token settings
        dr_settings = Settings(auth=AuthSettings(dr_api_token="dr-test-token"))

        # Test legacy API key settings
        api_key_settings = Settings(auth=AuthSettings(api_key="api-key-test"))

        test_url = "https://test.com/upload"

        # Test DR token produces Bearer auth
        dr_client = AssetAPIClient(dr_settings)
        dr_headers = dr_client.get_headers(test_url)
        assert "Authorization" in dr_headers
        assert dr_headers["Authorization"].startswith("Bearer")
        assert "dr-test-token" in dr_headers["Authorization"]

        # Test API key auth (may produce either x-api-key or Bearer token depending on system config)
        api_key_client = AssetAPIClient(api_key_settings)
        api_key_headers = api_key_client.get_headers(test_url)

        # Should contain either Bearer token or API key auth
        has_bearer_auth = "Authorization" in api_key_headers and api_key_headers[
            "Authorization"
        ].startswith("Bearer")
        has_api_key_auth = "x-api-key" in api_key_headers  # pragma: allowlist secret

        assert (
            has_bearer_auth or has_api_key_auth
        ), f"API key settings should produce auth headers but got: {api_key_headers}"

    @patch("covalent_cloud.function_serve.assets.AssetAPIClient")
    def test_s3_presigned_url_no_auth_headers_function_serve(self, mock_asset_api_client_class):
        """Test that S3 presigned URLs don't get auth headers in function serve uploads"""
        # Setup mocks
        mock_asset_client = Mock()
        mock_response = Mock()
        mock_asset_client.is_s3_presigned_url.return_value = True
        mock_asset_client.get_upload_headers.return_value = {}  # No auth headers for S3
        mock_asset_client.upload_asset.return_value = mock_response
        mock_asset_api_client_class.return_value = mock_asset_client

        # Create a test asset with S3 URL
        test_asset = ServeAsset(
            type=ServeAssetType.JSON,
            serialized_object=b'{"test": "s3_data"}',
            url="https://my-bucket.s3.amazonaws.com/path/to/file?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Signature=abc123",
        )

        original_url = test_asset.url
        original_data = test_asset.serialized_object

        # Call the function
        with patch("covalent_cloud.function_serve.assets.settings", self.mock_settings):
            AssetsMediator.upload_asset(test_asset, self.mock_settings)

        # Verify AssetAPIClient detected S3 URL and didn't add auth headers
        mock_asset_client.upload_asset.assert_called_once_with(original_url, original_data)
        mock_asset_api_client_class.assert_called_once_with(settings=self.mock_settings)

    @patch("covalent_cloud.dispatch_management.helpers.AssetAPIClient")
    def test_s3_presigned_url_no_auth_headers_dispatch(self, mock_asset_api_client_class):
        """Test that S3 presigned URLs don't get auth headers in dispatch uploads"""
        # Setup mocks
        mock_asset_client = Mock()
        mock_response = Mock()
        mock_response.status_code = requests.codes.ok
        mock_asset_client.is_s3_presigned_url.return_value = True
        mock_asset_client.get_upload_headers.return_value = {}  # No auth headers for S3
        mock_asset_client.upload_asset.return_value = mock_response
        mock_asset_api_client_class.return_value = mock_asset_client

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(b"test s3 content")
            temp_file_path = temp_file.name

        try:
            # S3 presigned URL
            s3_url = "https://my-bucket.s3.us-east-1.amazonaws.com/uploads/test?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Signature=def456"

            # Call the upload function
            _upload_asset(f"file://{temp_file_path}", s3_url, Mock(), Mock(), self.mock_settings)

            # Verify AssetAPIClient was used and upload was called
            mock_asset_api_client_class.assert_called_once_with(settings=self.mock_settings)
            mock_asset_client.upload_asset.assert_called_once()
            # Verify the call was made with the S3 URL
            call_args = mock_asset_client.upload_asset.call_args
            assert call_args[0][0] == s3_url

        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_s3_url_detection_patterns(self):
        """Test that various S3 URL patterns are correctly detected"""
        from covalent_cloud.shared.classes.api import AssetAPIClient

        client = AssetAPIClient(self.mock_settings)

        # S3 URLs that should be detected as presigned
        s3_presigned_urls = [
            "https://bucket.s3.amazonaws.com/key?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Signature=abc",
            "https://bucket.s3.us-west-2.amazonaws.com/key?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=def",
            "https://bucket.s3-us-west-1.amazonaws.com/key?X-Amz-Signature=ghi",
            "https://s3.eu-central-1.amazonaws.com/bucket/key?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Signature=jkl",
        ]

        # Non-S3 URLs that should NOT be detected as S3
        non_s3_urls = [
            "https://example.com/upload",
            "https://my-cdn.cloudfront.net/file",
            "https://storage.googleapis.com/bucket/file",
            "https://bucket.s3.amazonaws.com/key",  # No presigned params
            "https://not-s3.com/key?X-Amz-Signature=fake",  # Not S3 hostname
        ]

        # Test S3 presigned URL detection
        for url in s3_presigned_urls:
            assert client.is_s3_presigned_url(
                url
            ), f"Expected {url} to be detected as S3 presigned URL"
            assert client.get_headers(url) == {}, f"Expected no auth headers for S3 URL: {url}"

        # Test non-S3 URL detection
        for url in non_s3_urls:
            assert not client.is_s3_presigned_url(
                url
            ), f"Expected {url} to NOT be detected as S3 presigned URL"
            headers = client.get_headers(url)
            assert len(headers) > 0, f"Expected auth headers for non-S3 URL: {url}"

    def test_non_s3_url_still_gets_auth_headers(self):
        """Test that non-S3 URLs still get auth headers as before"""
        from covalent_cloud.shared.classes.api import AssetAPIClient

        client = AssetAPIClient(self.mock_settings)

        # Test non-S3 URL
        non_s3_url = "https://my-custom-storage.example.com/upload/asset"
        headers = client.get_headers(non_s3_url)

        # Should contain auth headers
        has_bearer_auth = "Authorization" in headers and headers["Authorization"].startswith(
            "Bearer"
        )
        has_api_key_auth = "x-api-key" in headers  # pragma: allowlist secret
        assert (
            has_bearer_auth or has_api_key_auth
        ), f"Non-S3 URL should have auth headers but got: {headers}"

        # Verify it's not detected as S3
        assert not client.is_s3_presigned_url(
            non_s3_url
        ), "Non-S3 URL was incorrectly detected as S3"
