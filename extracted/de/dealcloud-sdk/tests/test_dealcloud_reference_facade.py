"""Tests for DealCloudData reference/delta delegation methods."""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from dealcloud_sdk.data.dealcloud_data import DealCloudData
from dealcloud_sdk.data.models import ReferenceFormat


def _fields_response():
    return [
        {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
    ]


@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
class TestReferenceFacades:
    def test_get_reference_fields_delegates_to_read(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = _fields_response()
        mock_client_class.return_value = mock_client
        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch("dealcloud_sdk.data.read.get_reference_fields", return_value=[]) as m:
            dc.get_reference_fields("Company")
        m.assert_called_once_with(dc, "Company")

    def test_private_get_reference_fields_delegates_to_references(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = _fields_response()
        mock_client_class.return_value = mock_client
        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch(
            "dealcloud_sdk.data.references.get_reference_fields", return_value=[]
        ) as m:
            dc._get_reference_fields("Company")
        m.assert_called_once_with(dc, "Company")

    def test_fetch_entry_names_and_private_delegate(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = _fields_response()
        mock_client_class.return_value = mock_client
        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch(
            "dealcloud_sdk.data.references.fetch_entry_names",
            return_value={1: "A"},
        ) as m:
            assert dc.fetch_entry_names("Co", [1]) == {1: "A"}
            assert dc._fetch_entry_names("Co", [1], name_field="Title") == {1: "A"}
        m.assert_any_call(dc, "Co", [1], "Name")
        m.assert_any_call(dc, "Co", [1], "Title")

    def test_resolve_and_apply_reference_private_delegate(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = _fields_response()
        mock_client_class.return_value = mock_client
        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch(
            "dealcloud_sdk.data.references.resolve_reference_value", return_value=9
        ) as m1:
            assert dc._resolve_reference_value({"id": 1}, ReferenceFormat.ID) == 9
        m1.assert_called_once()
        with patch(
            "dealcloud_sdk.data.references.apply_reference_format",
            return_value=[{"x": 1}],
        ) as m2:
            assert dc._apply_reference_format([{}], "O", ReferenceFormat.ID) == [{"x": 1}]
        m2.assert_called_once()

    def test_apply_reference_format_defaults_to_id(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = _fields_response()
        mock_client_class.return_value = mock_client
        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch(
            "dealcloud_sdk.data.references.apply_reference_format",
            return_value=[{"ok": True}],
        ) as m:
            out = dc.apply_reference_format([{"EntryId": 1}], "Company")
        assert out == [{"ok": True}]
        assert m.call_args[0][3] == ReferenceFormat.ID

    def test_apply_reference_format_explicit_format_skips_none_default(
        self, mock_client_class
    ):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = _fields_response()
        mock_client_class.return_value = mock_client
        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch(
            "dealcloud_sdk.data.references.apply_reference_format",
            return_value=[{"ok": True}],
        ) as m:
            out = dc.apply_reference_format(
                [{"EntryId": 1}], "Company", ReferenceFormat.NAME
            )
        assert out == [{"ok": True}]
        assert m.call_args[0][3] == ReferenceFormat.NAME

    def test_prefetch_reference_names_private(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = _fields_response()
        mock_client_class.return_value = mock_client
        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        cache = MagicMock()
        with patch(
            "dealcloud_sdk.data.references.prefetch_reference_names"
        ) as m:
            dc._prefetch_reference_names([], {"F": "Target"}, cache)
        m.assert_called_once_with(dc, [], {"F": "Target"}, cache)


@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
class TestGetTotalRecordCount:
    def test_returns_total_records_from_client(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {"totalRecords": 42, "rows": []}
        mock_client_class.return_value = mock_client
        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        assert dc.get_total_record_count("Company") == 42


@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
class TestDeltaSyncFacades:
    def test_get_modified_entries_delegates(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        since = datetime(2024, 1, 1)
        with patch(
            "dealcloud_sdk.data.delta_sync.get_modified_entries",
            return_value=[],
        ) as m:
            dc.get_modified_entries("Company", since)
        m.assert_called_once_with(dc, "Company", since, True)

    @pytest.mark.asyncio
    async def test_aget_modified_entries_delegates(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        since = datetime(2024, 1, 1)
        with patch(
            "dealcloud_sdk.data.delta_sync.aget_modified_entries",
            new_callable=AsyncMock,
            return_value=[],
        ) as m:
            await dc.aget_modified_entries("Company", since)
        m.assert_awaited_once_with(dc, "Company", since, True)

    def test_sync_delta_delegates(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        since = datetime(2024, 1, 1)
        fake = MagicMock()
        with patch(
            "dealcloud_sdk.data.delta_sync.sync_delta", return_value=fake
        ) as m:
            out = dc.sync_delta("Company", since, fields=["Name"], output="pandas")
        assert out is fake
        m.assert_called_once_with(
            dc, "Company", since, ["Name"], "pandas", None, 500
        )
