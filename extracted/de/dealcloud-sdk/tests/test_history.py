"""Tests for DealCloudHistory class."""

import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch

from dealcloud_sdk.history.dealcloud_history import (
    DealCloudHistory,
    DateTimeBehavior,
    _normalize_date_time_behavior,
)


class TestDealCloudHistoryInit:
    """Tests for DealCloudHistory initialization."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_init_sets_history_url(self, mock_client_class):
        """Test that init sets history URL."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        history = DealCloudHistory(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        assert history._history_url == "https://test.dealcloud.com/api/rest/v4/data/entrydata"


class TestDealCloudHistoryGetObjectHistory:
    """Tests for get_history method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_history_basic(self, mock_client_class):
        """Test get_history basic."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"entryId": 1, "changeDate": "2024-01-15T10:30:00Z"},
            {"entryId": 2, "changeDate": "2024-01-15T11:00:00Z"},
        ]
        mock_client_class.return_value = mock_client
        
        history = DealCloudHistory(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = history.get_history(
            "Company",
            modified_since=datetime(2024, 1, 1),
        )
        
        assert len(result) == 2
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_history_with_all_filters(self, mock_client_class):
        """Test get_history with all filter params."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = []
        mock_client_class.return_value = mock_client
        
        history = DealCloudHistory(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        start = datetime(2024, 1, 1)
        history.get_history(
            "Company",
            modified_since=start,
            end_date=datetime(2024, 1, 31),
            entry_ids=[1, 2],
            field_ids=[10],
            user_ids=[100],
            limit=500,
            skip=50,
        )
        
        call_args = mock_client.get.call_args
        call_url = call_args[0][0]
        call_kwargs = call_args[1] if len(call_args) > 1 else {}
        call_params = call_kwargs.get("params", {})
        assert "entries/history" in call_url or "entries/allHistory" in call_url
        assert "modifiedSince" in call_params
        # API spec only defines modifiedSince; extra params are not sent
        assert set(call_params.keys()) <= {"modifiedSince"}


class TestDealCloudHistoryGetHistoricalData:
    """Tests for get_historical_data method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_historical_data_basic(self, mock_client_class):
        """Test get_historical_data basic."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = [
            {"EntryId": 1, "Name": "Company A (historical)"},
        ]
        mock_client_class.return_value = mock_client
        
        history = DealCloudHistory(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        as_of = datetime(2024, 3, 31)
        result = history.get_historical_data("Company", [1, 2], as_of_date=as_of)

        mock_client.post.assert_called_once()
        call_url = mock_client.post.call_args[0][0]
        payload = mock_client.post.call_args[1].get("json", {})
        assert "getHistoricalData" in call_url
        assert payload.get("entryTypeId") == "Company"
        assert payload.get("entries") == [1, 2]
        assert "fromDate" in payload
        assert result == [{"EntryId": 1, "Name": "Company A (historical)"}]
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_historical_data_with_fields(self, mock_client_class):
        """Test get_historical_data with specific fields."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = []
        mock_client_class.return_value = mock_client
        
        history = DealCloudHistory(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        as_of = datetime(2024, 3, 31)
        history.get_historical_data("Company", [1], as_of_date=as_of, fields=["Name", "Status"])

        call_url = mock_client.post.call_args[0][0]
        payload = mock_client.post.call_args[1]["json"]
        assert "getHistoricalData" in call_url
        assert payload["entryTypeId"] == "Company"
        assert payload["entries"] == [1]
        assert "fromDate" in payload
        assert payload["fields"] == ["Name", "Status"]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_historical_data_date_time_behavior_enum(self, mock_client_class):
        """Test get_historical_data accepts DateTimeBehavior enum."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.post.return_value = []
        mock_client_class.return_value = mock_client

        history = DealCloudHistory(
            site_url="test.dealcloud.com", client_id="x", client_secret="y"
        )
        as_of = datetime(2024, 1, 1)
        history.get_historical_data("Company", [1], as_of_date=as_of, date_time_behavior=DateTimeBehavior.LOCAL)

        params = mock_client.post.call_args[1].get("params", {})
        assert params.get("dateTimeBehavior") == 1

        history.get_historical_data("Company", [1], as_of_date=as_of, date_time_behavior=DateTimeBehavior.UTC)
        params = mock_client.post.call_args[1].get("params", {})
        assert params.get("dateTimeBehavior") == 0

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_historical_data_date_time_behavior_string(self, mock_client_class):
        """Test get_historical_data accepts 'UTC' and 'Local' (case-insensitive)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.post.return_value = []
        mock_client_class.return_value = mock_client

        history = DealCloudHistory(
            site_url="test.dealcloud.com", client_id="x", client_secret="y"
        )
        as_of = datetime(2024, 1, 1)

        history.get_historical_data("Company", [1], as_of_date=as_of, date_time_behavior="Local")
        assert mock_client.post.call_args[1].get("params", {}).get("dateTimeBehavior") == 1

        history.get_historical_data("Company", [1], as_of_date=as_of, date_time_behavior="LOCAL")
        assert mock_client.post.call_args[1].get("params", {}).get("dateTimeBehavior") == 1

        history.get_historical_data("Company", [1], as_of_date=as_of, date_time_behavior="UTC")
        assert mock_client.post.call_args[1].get("params", {}).get("dateTimeBehavior") == 0

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_historical_data_date_time_behavior_invalid_raises(self, mock_client_class):
        """Test get_historical_data raises on invalid date_time_behavior."""
        mock_client_class.return_value = MagicMock()
        history = DealCloudHistory(
            site_url="test.dealcloud.com", client_id="x", client_secret="y"
        )
        as_of = datetime(2024, 1, 1)

        with pytest.raises(ValueError, match="must be 0 or 1"):
            history.get_historical_data("Company", [1], as_of_date=as_of, date_time_behavior=2)
        with pytest.raises(ValueError, match="'UTC' or 'Local'"):
            history.get_historical_data("Company", [1], as_of_date=as_of, date_time_behavior="invalid")


class TestNormalizeDateTimeBehavior:
    """Direct tests for _normalize_date_time_behavior."""

    def test_int_zero_or_one_returns_int(self):
        assert _normalize_date_time_behavior(0) == 0
        assert _normalize_date_time_behavior(1) == 1

    def test_invalid_type_raises_type_error(self):
        with pytest.raises(TypeError, match="DateTimeBehavior"):
            _normalize_date_time_behavior(1.5)


class TestDealCloudHistoryUrlAndHistoricalResponse:
    """history_url property and non-rows API responses."""

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_history_url_property(self, mock_client_class):
        mock_client_class.return_value = MagicMock()
        mock_client_class.return_value._get_auth_headers_sync.return_value = {}
        history = DealCloudHistory(
            site_url="test.dealcloud.com", client_id="a", client_secret="b"
        )
        assert history.history_url.endswith("/entrydata")

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_get_historical_data_wrap_into_arrays_false_omits_param(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.post.return_value = {"rows": []}
        mock_client_class.return_value = mock_client
        history = DealCloudHistory(
            site_url="test.dealcloud.com", client_id="a", client_secret="b"
        )
        history.get_historical_data(
            "Company", [1], as_of_date=datetime(2024, 1, 1), wrap_into_arrays=False
        )
        call_kw = mock_client.post.call_args[1]
        params = call_kw.get("params")
        assert params is None or "wrapIntoArrays" not in (params or {})

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_get_historical_data_returns_raw_when_no_rows_key(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.post.return_value = [{"EntryId": 1}]
        mock_client_class.return_value = mock_client
        history = DealCloudHistory(
            site_url="test.dealcloud.com", client_id="a", client_secret="b"
        )
        out = history.get_historical_data(
            "Company", [1], as_of_date=datetime(2024, 1, 1)
        )
        assert out == [{"EntryId": 1}]


class TestDealCloudHistoryGetObjectHistoryDeletedOnly:
    """Tests for get_history(deleted_only=True)."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_history_deleted_only_returns_only_deleted(self, mock_client_class):
        """Test get_history(deleted_only=True) returns only entries with isDeleted true."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"isDeleted": False, "id": 1, "name": "Active", "entryListId": 100},
            {"isDeleted": True, "id": 999, "name": "Deleted Co", "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client

        history = DealCloudHistory(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = history.get_history(
            "Company", modified_since=datetime(2024, 1, 1), deleted_only=True
        )

        assert len(result) == 1
        assert result[0]["isDeleted"] is True
        assert result[0]["id"] == 999

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_history_requires_modified_since(self, mock_client_class):
        """Test get_history raises when modified_since not provided."""
        mock_client_class.return_value = MagicMock()
        history = DealCloudHistory(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with pytest.raises(ValueError, match="modified_since is required"):
            history.get_history("Company", deleted_only=True)

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_history_deleted_only_calls_history_endpoint(self, mock_client_class):
        """Test get_history(deleted_only=True) calls history endpoint with modifiedSince."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.get.return_value = []
        mock_client_class.return_value = mock_client

        history = DealCloudHistory(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        history.get_history(
            "Company", modified_since=datetime(2024, 1, 1), deleted_only=True
        )

        mock_client.get.assert_called_once()
        call_url = mock_client.get.call_args[0][0]
        call_params = mock_client.get.call_args[1].get("params", {})
        assert "entries/history" in call_url or "entries/allHistory" in call_url
        assert "modifiedSince" in call_params

