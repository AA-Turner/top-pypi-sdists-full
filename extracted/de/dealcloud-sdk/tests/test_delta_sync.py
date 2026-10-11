"""Unit tests for dealcloud_sdk.data.delta_sync (get_modified_entries, sync_delta)."""

from datetime import datetime

import pytest
from unittest.mock import MagicMock, AsyncMock, patch

from dealcloud_sdk.data.dealcloud_data import DealCloudData
from dealcloud_sdk.data.delta_sync import (
    get_modified_entries,
    aget_modified_entries,
    sync_delta,
)
from dealcloud_sdk.data.models import ModifiedEntry, DeltaSyncResult


class TestGetModifiedEntries:
    """Tests for get_modified_entries (sync)."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_modified_entries_list_response(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.get.return_value = [
            {"entryId": 1, "modifiedDate": "2024-01-15T10:30:00Z", "isDeleted": False},
            {"entryId": 2, "modifiedDate": "2024-01-15T11:00:00Z", "isDeleted": True},
        ]
        mock_client_class.return_value = mock_client

        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")
        data._client = mock_client
        data._data_url = "https://test.dealcloud.com/api/rest/v4/data"

        result = get_modified_entries(data, "Company", datetime(2024, 1, 1))

        assert len(result) == 2
        assert result[0].entry_id == 1
        assert result[0].is_deleted is False
        assert result[1].entry_id == 2
        assert result[1].is_deleted is True
        mock_client.get.assert_called_once()
        call_args = mock_client.get.call_args
        assert "entrylist" in call_args[0][0] and "history" in call_args[0][0]
        assert call_args[1]["params"]["includeDeleted"] == "true"

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_modified_entries_dict_with_entries_key(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.get.return_value = {
            "entries": [
                {"entryId": 10, "modifiedDate": "2024-06-01T12:00:00Z", "isDeleted": False},
            ]
        }
        mock_client_class.return_value = mock_client

        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")
        data._client = mock_client
        data._data_url = "https://test.dealcloud.com/api/rest/v4/data"

        result = get_modified_entries(data, 12345, "2024-01-01T00:00:00")

        assert len(result) == 1
        assert result[0].entry_id == 10
        mock_client.get.assert_called_once()
        assert "modifiedSince" in mock_client.get.call_args[1]["params"]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_modified_entries_include_deleted_false(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.get.return_value = []
        mock_client_class.return_value = mock_client

        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")
        data._client = mock_client
        data._data_url = "https://test.dealcloud.com/api/rest/v4/data"

        get_modified_entries(data, "Company", datetime(2024, 1, 1), include_deleted=False)

        assert mock_client.get.call_args[1]["params"]["includeDeleted"] == "false"

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_modified_entries_empty_response_returns_empty_list(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.get.return_value = []
        mock_client_class.return_value = mock_client

        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")
        data._client = mock_client
        data._data_url = "https://test.dealcloud.com/api/rest/v4/data"

        result = get_modified_entries(data, "Company", "2024-01-01T00:00:00")

        assert result == []

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_get_modified_entries_unexpected_dict_returns_empty(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.get.return_value = {"notEntries": True}
        mock_client_class.return_value = mock_client

        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")
        data._client = mock_client
        data._data_url = "https://test.dealcloud.com/api/rest/v4/data"

        assert get_modified_entries(data, "Company", datetime(2024, 1, 1)) == []


@pytest.mark.asyncio
class TestAGetModifiedEntries:
    """Tests for aget_modified_entries (async)."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    async def test_aget_modified_entries_list_response(self, mock_client_class):
        mock_client = MagicMock()
        mock_client.aget = AsyncMock(return_value=[
            {"entryId": 1, "modifiedDate": "2024-01-15T10:30:00Z", "isDeleted": False},
        ])
        mock_client_class.return_value = mock_client

        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")
        data._client = mock_client
        data._data_url = "https://test.dealcloud.com/api/rest/v4/data"

        result = await aget_modified_entries(data, "Company", datetime(2024, 1, 1))

        assert len(result) == 1
        assert result[0].entry_id == 1
        mock_client.aget.assert_called_once()

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    async def test_aget_modified_entries_dict_entries(self, mock_client_class):
        mock_client = MagicMock()
        mock_client.aget = AsyncMock(return_value={
            "entries": [{"entryId": 5, "modifiedDate": "2024-01-01T00:00:00Z", "isDeleted": True}],
        })
        mock_client_class.return_value = mock_client

        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")
        data._client = mock_client
        data._data_url = "https://test.dealcloud.com/api/rest/v4/data"

        result = await aget_modified_entries(data, "Company", "2024-01-01")

        assert len(result) == 1
        assert result[0].entry_id == 5
        assert result[0].is_deleted is True

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    async def test_aget_modified_entries_unexpected_dict_returns_empty(self, mock_client_class):
        mock_client = MagicMock()
        mock_client.aget = AsyncMock(return_value={"unexpected": True})
        mock_client_class.return_value = mock_client

        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")
        data._client = mock_client
        data._data_url = "https://test.dealcloud.com/api/rest/v4/data"

        assert await aget_modified_entries(data, "Company", datetime(2024, 1, 1)) == []


class TestSyncDelta:
    """Tests for sync_delta."""

    @patch('dealcloud_sdk.data.delta_sync.get_modified_entries')
    @patch('dealcloud_sdk.data.read.read_data')
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_sync_delta_with_modifications_calls_read_data(
        self, mock_client_class, mock_read_data, mock_get_modified
    ):
        mock_get_modified.return_value = [
            ModifiedEntry(entry_id=1, modified_date=datetime(2024, 1, 15), is_deleted=False),
            ModifiedEntry(entry_id=2, modified_date=datetime(2024, 1, 15), is_deleted=True),
        ]
        mock_read_data.return_value = [{"EntryId": 1, "Name": "Acme"}]

        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")

        result = sync_delta(data, "Company", datetime(2024, 1, 1), output="list")

        assert isinstance(result, DeltaSyncResult)
        assert result.modified_ids == [1]
        assert result.deleted_ids == [2]
        assert result.modified_data == [{"EntryId": 1, "Name": "Acme"}]
        mock_read_data.assert_called_once()
        call_kw = mock_read_data.call_args[1]
        assert "EntryId in (1)" in call_kw["query"]

    @patch('dealcloud_sdk.data.delta_sync.get_modified_entries')
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_sync_delta_no_modifications_returns_empty_data(
        self, mock_client_class, mock_get_modified
    ):
        mock_get_modified.return_value = []

        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")

        result = sync_delta(data, "Company", "2024-01-01T00:00:00", output="list")

        assert result.modified_ids == []
        assert result.deleted_ids == []
        assert result.modified_data == []
        assert result.modified_since is not None

    @patch('dealcloud_sdk.data.delta_sync.get_modified_entries')
    @patch('dealcloud_sdk.data.read.read_data')
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_sync_delta_above_stream_threshold_uses_read_data(
        self, mock_client_class, mock_read_data, mock_get_modified
    ):
        # sync_delta uses read_data for both branches (small and large); stream_threshold
        # only affects which path - both call read_data with query
        mock_get_modified.return_value = [
            ModifiedEntry(entry_id=i, modified_date=datetime(2024, 1, 1), is_deleted=False)
            for i in range(1, 6)
        ]
        mock_read_data.return_value = [{"EntryId": i} for i in range(1, 6)]

        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")

        result = sync_delta(
            data, "Company", datetime(2024, 1, 1),
            output="list", stream_threshold=10
        )

        assert len(result.modified_ids) == 5
        mock_read_data.assert_called_once()

    @patch("dealcloud_sdk.data.delta_sync.get_modified_entries")
    @patch("dealcloud_sdk.data.read.read_data")
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_sync_delta_modified_count_greater_than_stream_threshold(
        self, mock_client_class, mock_read_data, mock_get_modified
    ):
        mock_get_modified.return_value = [
            ModifiedEntry(entry_id=i, modified_date=datetime(2024, 1, 1), is_deleted=False)
            for i in range(1, 8)
        ]
        mock_read_data.return_value = [{"EntryId": i} for i in range(1, 8)]

        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")

        result = sync_delta(
            data,
            "Company",
            datetime(2024, 1, 1),
            output="list",
            stream_threshold=5,
        )

        assert len(result.modified_ids) == 7
        mock_read_data.assert_called_once()
