"""Tests for DealCloudReports (Template Reports API)."""

import pytest
from unittest.mock import MagicMock, patch

from dealcloud_sdk.reports.dealcloud_reports import DealCloudReports


class TestDealCloudReportsInit:
    """Tests for initialization (inherits _data_url from base)."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_report_templates_url(self, mock_client_class):
        """Test get_report_templates calls GET data/reports/template."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [{"id": 1, "name": "Report A"}]
        mock_client_class.return_value = mock_client

        reports = DealCloudReports(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = reports.get_report_templates()

        assert result == [{"id": 1, "name": "Report A"}]
        mock_client.get.assert_called_once_with(
            "https://test.dealcloud.com/api/rest/v4/data/reports/template"
        )

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_report_templates_with_params(self, mock_client_class):
        """Test get_report_templates with page and id params."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = []
        mock_client_class.return_value = mock_client

        reports = DealCloudReports(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        reports.get_report_templates(page_size=10, page_number=1, id=5)

        mock_client.get.assert_called_once_with(
            "https://test.dealcloud.com/api/rest/v4/data/reports/template?pageSize=10&pageNumber=1&id=5"
        )

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_generate_report(self, mock_client_class):
        """Test generate_report calls POST data/reports/generate with templateId."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {
            "requestID": "550e8400-e29b-41d4-a716-446655440000",
            "status": "Queued",
        }
        mock_client_class.return_value = mock_client

        reports = DealCloudReports(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = reports.generate_report(template_id=42)

        assert result["requestID"] == "550e8400-e29b-41d4-a716-446655440000"
        mock_client.post.assert_called_once_with(
            "https://test.dealcloud.com/api/rest/v4/data/reports/generate",
            json={"templateId": 42},
        )

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_generate_report_with_options(self, mock_client_class):
        """Test generate_report with optional body fields."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"requestID": "uuid", "status": "Queued"}
        mock_client_class.return_value = mock_client

        reports = DealCloudReports(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        reports.generate_report(
            template_id=1,
            remove_empty_table=True,
            entries=[10, 20],
            user_ids=[100],
        )

        mock_client.post.assert_called_once_with(
            "https://test.dealcloud.com/api/rest/v4/data/reports/generate",
            json={
                "templateId": 1,
                "removeEmptyTable": True,
                "entryIds": [10, 20],
                "userIds": [100],
            },
        )

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_report_status(self, mock_client_class):
        """Test get_report_status calls GET data/reports/{requestId}."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {"status": "Completed", "reportUrl": "https://..."}
        mock_client_class.return_value = mock_client

        reports = DealCloudReports(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = reports.get_report_status("550e8400-e29b-41d4-a716-446655440000")

        assert result["status"] == "Completed"
        mock_client.get.assert_called_once_with(
            "https://test.dealcloud.com/api/rest/v4/data/reports/550e8400-e29b-41d4-a716-446655440000"
        )
