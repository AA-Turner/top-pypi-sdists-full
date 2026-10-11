"""Tests for DealCloudMerge class."""

import pytest
from unittest.mock import MagicMock, patch

from dealcloud_sdk.merge.dealcloud_merge import DealCloudMerge


class TestDealCloudMergeInit:
    """Tests for DealCloudMerge initialization."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_init_sets_merge_url(self, mock_client_class):
        """Test that init sets merge URL."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        merge = DealCloudMerge(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        assert merge._merge_url == "https://test.dealcloud.com/api/rest/v4/data/merge"

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_merge_url_property(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        merge = DealCloudMerge(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        assert merge.merge_url == merge._merge_url


class TestDealCloudMergeEntries:
    """Tests for merge_entries method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_merge_entries_basic(self, mock_client_class):
        """Test merge_entries basic."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {
            "winnerId": 123,
            "success": True,
            "relationshipsTransferred": 5,
        }
        mock_client_class.return_value = mock_client
        
        merge = DealCloudMerge(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = merge.merge_entries("Company", 123, [456, 789])
        
        assert result["winnerId"] == 123
        assert result["success"] is True
        mock_client.post.assert_called_once()
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_merge_entries_with_overrides(self, mock_client_class):
        """Test merge_entries with field_overrides."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"success": True}
        mock_client_class.return_value = mock_client
        
        merge = DealCloudMerge(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        merge.merge_entries(
            "Company",
            123,
            [456],
            field_overrides={"Status": [1]},
        )
        
        call_kwargs = mock_client.post.call_args
        payload = call_kwargs[1]["json"]
        assert isinstance(payload, list) and len(payload) == 1
        item = payload[0]
        assert "fieldOverrides" in item
        assert item["fieldOverrides"] == {"Status": [1]}
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_merge_entries_no_delete(self, mock_client_class):
        """Test merge_entries with delete_losers=False."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"success": True}
        mock_client_class.return_value = mock_client
        
        merge = DealCloudMerge(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        merge.merge_entries("Company", 123, [456], delete_losers=False)
        
        call_kwargs = mock_client.post.call_args
        payload = call_kwargs[1]["json"]
        assert isinstance(payload, list) and len(payload) == 1
        assert payload[0]["deleteLoserEntries"] is False
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_merge_entries_no_transfer_relationships(self, mock_client_class):
        """Test merge_entries with transfer_relationships=False."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"success": True}
        mock_client_class.return_value = mock_client
        
        merge = DealCloudMerge(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        merge.merge_entries("Company", 123, [456], transfer_relationships=False)
        
        call_kwargs = mock_client.post.call_args
        payload = call_kwargs[1]["json"]
        assert isinstance(payload, list) and len(payload) == 1
        assert payload[0]["transferRelationships"] is False

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_merge_entries_overwrite_empty_values_query_param(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"success": True}
        mock_client_class.return_value = mock_client
        merge = DealCloudMerge(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        merge.merge_entries("Company", 1, [2, 3], overwrite_empty_values=True)
        mock_client.post.assert_called_once()
        assert mock_client.post.call_args[1]["params"] == {
            "overwriteEmptyValues": True,
        }
