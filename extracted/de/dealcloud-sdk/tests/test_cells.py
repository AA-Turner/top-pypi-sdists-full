"""Tests for DealCloudCells class."""

import pytest
from unittest.mock import MagicMock, patch, PropertyMock
from intapp_rest_client.exceptions import HttpError

from dealcloud_sdk.cells.dealcloud_cells import DealCloudCells


class TestDealCloudCellsInit:
    """Tests for DealCloudCells initialization."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_init_sets_cells_url(self, mock_client_class):
        """Test that init sets cells URL."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        assert cells._cells_url == "https://test.dealcloud.com/api/rest/v4/data/entrydata"
        assert cells.cells_url == cells._cells_url


class TestDealCloudCellsGetCells:
    """Tests for get_cells method (POST entrydata/get with DataReadRequest array)."""

    @patch('dealcloud_sdk.cells.dealcloud_cells.DealCloudCells.get_fields')
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_cells_basic(self, mock_client_class, mock_get_fields):
        """Test get_cells with entry_ids and fields (POST get)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = [{"entryId": 1, "fieldId": 10, "value": "A"}]
        mock_client_class.return_value = mock_client
        mock_get_fields.return_value = [MagicMock(id=10), MagicMock(id=11)]

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        result = cells.get_cells("Company", entry_ids=[1, 2], fields=[10, 11])

        assert mock_client.post.called
        call_args = mock_client.post.call_args
        assert "entrydata/get" in call_args[0][0]
        body = call_args[1]["json"]
        assert len(body) == 4  # 2 entries x 2 fields
        assert all("entryId" in r and "fieldId" in r for r in body)

    @patch('dealcloud_sdk.cells.dealcloud_cells.DealCloudCells.list_entries')
    @patch('dealcloud_sdk.cells.dealcloud_cells.DealCloudCells.get_fields')
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_cells_with_entry_ids(self, mock_client_class, mock_get_fields, mock_list_entries):
        """Test get_cells with entry_ids builds DataReadRequest and POSTs."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = []
        mock_client_class.return_value = mock_client
        mock_get_fields.return_value = [MagicMock(id=10)]
        mock_list_entries.return_value = []

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        cells.get_cells("Company", entry_ids=[123, 456])

        body = mock_client.post.call_args[1]["json"]
        assert body == [{"entryId": 123, "fieldId": 10}, {"entryId": 456, "fieldId": 10}]

    @patch('dealcloud_sdk.cells.dealcloud_cells.DealCloudCells.list_entries')
    @patch('dealcloud_sdk.cells.dealcloud_cells.DealCloudCells.get_fields')
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_cells_with_fields_int(self, mock_client_class, mock_get_fields, mock_list_entries):
        """Test get_cells with fields as list of int (no entry_ids: list_entries then POST get)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = []
        mock_client_class.return_value = mock_client
        mock_get_fields.return_value = [MagicMock(id=10), MagicMock(id=11)]
        mock_list_entries.return_value = [1, 2]

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        cells.get_cells("Company", fields=[10, 11])

        mock_client.post.assert_called_once()
        body = mock_client.post.call_args[1]["json"]
        assert len(body) == 4

    @patch('dealcloud_sdk.cells.dealcloud_cells.DealCloudCells.get_fields')
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_cells_with_fields_str(self, mock_client_class, mock_get_fields):
        """Test get_cells with fields as list of str (API names) resolves to IDs via get_fields and POSTs."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = []
        mock_client_class.return_value = mock_client
        mock_get_fields.return_value = [
            MagicMock(apiName='Name', id=10),
            MagicMock(apiName='Status', id=11),
        ]

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        cells.get_cells("Company", entry_ids=[1], fields=["Name", "Status"])

        mock_client.post.assert_called_once()
        body = mock_client.post.call_args[1]["json"]
        assert len(body) == 2  # 1 entry x 2 fields

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_cells_empty_entries_returns_empty(self, mock_client_class):
        """Test get_cells with entry_ids=[] returns [] without calling POST."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        result = cells.get_cells("Company", entry_ids=[])

        assert result == []
        mock_client.post.assert_not_called()

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_get_cells_empty_fields_list_returns_empty(self, mock_client_class):
        """fields=[] yields no field IDs and returns [] without POST."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        assert cells.get_cells("Company", entry_ids=[1], fields=[]) == []
        mock_client.post.assert_not_called()

    @patch("dealcloud_sdk.cells.dealcloud_cells.DealCloudCells.get_fields")
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_get_cells_unknown_field_names_yield_no_ids(self, mock_client_class, mock_get_fields):
        """String field names with no matching apiName produce empty field_ids []."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        mock_get_fields.return_value = [MagicMock(apiName="Name", id=10)]

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        assert cells.get_cells("Company", entry_ids=[1], fields=["Missing"]) == []
        mock_client.post.assert_not_called()

    @patch("dealcloud_sdk.cells.dealcloud_cells.DealCloudCells.get_fields")
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_get_cells_single_dict_response_appended(self, mock_client_class, mock_get_fields):
        """When POST returns a single dict (not list), it is appended to results."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"raw": True}
        mock_client_class.return_value = mock_client
        mock_get_fields.return_value = [MagicMock(id=10)]

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        assert cells.get_cells("Company", entry_ids=[1], fields=[10]) == [{"raw": True}]

    @patch('dealcloud_sdk.cells.dealcloud_cells.DealCloudCells.get_fields')
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_cells_query_params_and_currency_code(self, mock_client_class, mock_get_fields):
        """Test get_cells forwards resolve_reference_url, fill_extended_data, wrap_into_arrays, date_time_behavior and currency_code."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = []
        mock_client_class.return_value = mock_client
        mock_get_fields.return_value = [MagicMock(id=10)]

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        cells.get_cells(
            "Company",
            entry_ids=[1],
            fields=[10],
            resolve_reference_url=True,
            fill_extended_data=True,
            wrap_into_arrays=True,
            date_time_behavior=1,
            currency_code="USD",
        )

        mock_client.post.assert_called_once()
        call_kw = mock_client.post.call_args[1]
        params = call_kw.get("params") or {}
        assert params.get("resolveReferenceUrl") is True
        assert params.get("fillExtendedData") is True
        assert params.get("wrapIntoArrays") is True
        assert params.get("dateTimeBehavior") == 1
        body = call_kw["json"]
        assert len(body) == 1
        assert body[0]["currencyCode"] == "USD"
        assert body[0]["entryId"] == 1
        assert body[0]["fieldId"] == 10


class TestDealCloudCellsListEntries:
    """Tests for list_entries (GET .../entries or .../entries/history; limit/skip client-side)."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_list_entries_basic(self, mock_client_class):
        """Test list_entries with NamedEntryVm list (id, name, entryListId)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"id": 1, "name": "A", "entryListId": 0},
            {"id": 2, "name": "B", "entryListId": 0},
        ]
        mock_client_class.return_value = mock_client

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        result = cells.list_entries("Company")

        assert result == [1, 2]
        call_url = mock_client.get.call_args[0][0]
        assert "/entrydata/Company/entries" in call_url and "history" not in call_url

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_list_entries_skips_items_without_id_or_int(self, mock_client_class):
        """Entries that are not dicts with id or ints are ignored."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [{"n": 1}, {"id": 7}, 99, {"id": 8}]
        mock_client_class.return_value = mock_client

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        assert cells.list_entries("Company") == [7, 99, 8]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_list_entries_dict_with_entry_ids(self, mock_client_class):
        """Test list_entries when API returns dict with entryIds (fallback)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {"entryIds": [1, 2, 3]}
        mock_client_class.return_value = mock_client

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        result = cells.list_entries("Company")

        assert result == [1, 2, 3]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_list_entries_list_of_ints(self, mock_client_class):
        """Test list_entries when API returns list of int IDs."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [1, 2, 3]
        mock_client_class.return_value = mock_client

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        result = cells.list_entries("Company")

        assert result == [1, 2, 3]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_list_entries_calls_entries_url(self, mock_client_class):
        """Test list_entries calls GET .../entries with no query params (no pagination in swagger)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [{"id": 1}, {"id": 2}]
        mock_client_class.return_value = mock_client

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        result = cells.list_entries("Company")

        assert result == [1, 2]
        mock_client.get.assert_called_once()
        call_url = mock_client.get.call_args[0][0]
        assert "/entries" in call_url and call_url.rstrip("/").endswith("entries")
        assert "?" not in call_url

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_list_entries_with_limit_and_skip(self, mock_client_class):
        """Test list_entries applies limit and skip client-side."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"id": i, "name": f"E{i}", "entryListId": 0} for i in range(10)
        ]
        mock_client_class.return_value = mock_client

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        result = cells.list_entries("Company", limit=5, skip=2)
        assert result == [2, 3, 4, 5, 6]
        result_limit_only = cells.list_entries("Company", limit=3)
        assert result_limit_only == [0, 1, 2]


class TestDealCloudCellsListEntriesWithFilter:
    """Tests for list_entries_with_filter (POST .../filter; operator -> filterOperation)."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_list_entries_with_filter(self, mock_client_class):
        """Test list_entries_with_filter sends filterOperation (operator mapped)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = [1, 2, 3]
        mock_client_class.return_value = mock_client

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        filters = [{"fieldId": 10, "operator": "equals", "value": "Active"}]
        result = cells.list_entries_with_filter("Company", filters)

        assert result == [1, 2, 3]
        mock_client.post.assert_called_once()
        call_url = mock_client.post.call_args[0][0]
        assert "/entrydata/Company/filter" in call_url
        body = mock_client.post.call_args[1]["json"]
        assert body == [{"fieldId": 10, "filterOperation": "equals", "value": "Active"}]

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_list_entries_with_filter_preserves_existing_filter_operation(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = [9]
        mock_client_class.return_value = mock_client

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        filters = [{"fieldId": 10, "filterOperation": "equals", "value": "x"}]
        assert cells.list_entries_with_filter("Company", filters) == [9]
        assert "operator" not in mock_client.post.call_args[1]["json"][0]

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_list_entries_with_filter_non_list_response_returns_empty(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"unexpected": "object"}
        mock_client_class.return_value = mock_client

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        assert cells.list_entries_with_filter("Company", []) == []


class TestDealCloudCellsWriteCells:
    """Tests for write_cells (storeRequests body; create=post, update/upsert=put with recovery)."""

    @patch('dealcloud_sdk.cells.dealcloud_cells.DealCloudCells.get_field_by_api_name')
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_write_cells_create_mode(self, mock_client_class, mock_get_field):
        """Test write_cells in create mode POSTs storeRequests with row-error recovery."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = [
            {"entryId": -1, "fieldId": 10, "rowId": 1001, "value": "New Company"}
        ]
        mock_client_class.return_value = mock_client
        mock_get_field.return_value = MagicMock(id=10)

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        data = [{"EntryId": -1, "Name": "New Company"}]
        result = cells.write_cells("Company", data, mode="create")

        assert len(result) == 1
        mock_client.post.assert_called_once()
        body = mock_client.post.call_args[1]["json"]
        assert body["storeRequests"] == [{"entryId": -1, "fieldId": 10, "value": "New Company"}]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_write_cells_create_mode_positive_id_raises(self, mock_client_class):
        """Test write_cells create mode raises for positive EntryId."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        data = [{"EntryId": 123, "Name": "Company"}]

        with pytest.raises(ValueError) as exc_info:
            cells.write_cells("Company", data, mode="create")
        assert "create" in str(exc_info.value)
        assert "negative" in str(exc_info.value)

    @patch('dealcloud_sdk.cells.dealcloud_cells.DealCloudCells.get_field_by_api_name')
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_write_cells_update_mode(self, mock_client_class, mock_get_field):
        """Test write_cells in update mode PUTs storeRequests with row-error recovery."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.put.return_value = [
            {"entryId": 123, "fieldId": 10, "rowId": 123, "value": "Updated"}
        ]
        mock_client_class.return_value = mock_client
        mock_get_field.return_value = MagicMock(id=10)

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        data = [{"EntryId": 123, "Name": "Updated"}]
        result = cells.write_cells("Company", data, mode="update")

        assert len(result) == 1
        mock_client.put.assert_called_once()
        body = mock_client.put.call_args[1]["json"]
        assert body["storeRequests"] == [{"entryId": 123, "fieldId": 10, "value": "Updated"}]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_write_cells_update_mode_negative_id_raises(self, mock_client_class):
        """Test write_cells update mode raises for negative EntryId."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        data = [{"EntryId": -1, "Name": "Company"}]

        with pytest.raises(ValueError) as exc_info:
            cells.write_cells("Company", data, mode="update")
        assert "update" in str(exc_info.value)
        assert "positive" in str(exc_info.value)

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_write_cells_update_mode_zero_id_raises(self, mock_client_class):
        """Test write_cells update mode raises for zero EntryId."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        data = [{"EntryId": 0, "Name": "Company"}]

        with pytest.raises(ValueError):
            cells.write_cells("Company", data, mode="update")

    @patch('dealcloud_sdk.cells.dealcloud_cells.DealCloudCells.get_field_by_api_name')
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_write_cells_upsert_mode(self, mock_client_class, mock_get_field):
        """Test write_cells in upsert mode PUTs storeRequests."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.put.return_value = [
            {"entryId": -1, "fieldId": 10, "rowId": 1001, "value": "New"},
            {"entryId": 100, "fieldId": 10, "rowId": 100, "value": "Update"},
        ]
        mock_client_class.return_value = mock_client
        mock_get_field.return_value = MagicMock(id=10)

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        data = [{"EntryId": -1, "Name": "New"}, {"EntryId": 100, "Name": "Update"}]
        result = cells.write_cells("Company", data, mode="upsert")

        assert len(result) == 2
        mock_client.put.assert_called_once()

    @patch("dealcloud_sdk.cells.dealcloud_cells.DealCloudCells.get_field_by_api_name")
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_write_cells_splits_batch_when_exceeding_cell_pagination_limit(
        self, mock_client_class, mock_get_field
    ):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.put.return_value = [{"entryId": 1, "fieldId": 10, "rowId": 1, "value": 1}]
        mock_client_class.return_value = mock_client

        def gf(_obj, name):
            m = MagicMock()
            m.id = 10 if name == "A" else 11
            return m

        mock_get_field.side_effect = gf

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch.object(
            DealCloudCells,
            "cell_pagination_limit",
            new_callable=PropertyMock,
            return_value=2,
        ):
            data = [
                {"EntryId": 1, "A": 1, "B": 1},
                {"EntryId": 2, "A": 1, "B": 1},
            ]
            cells.write_cells("Company", data, mode="upsert")

        assert mock_client.put.call_count == 2
        first_body = mock_client.put.call_args_list[0][1]["json"]["storeRequests"]
        second_body = mock_client.put.call_args_list[1][1]["json"]["storeRequests"]
        assert len(first_body) == 2
        assert len(second_body) == 2

    @patch("dealcloud_sdk.cells.dealcloud_cells.DealCloudCells.get_field_by_api_name")
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_write_cells_skips_unknown_fields_and_none_values(
        self, mock_client_class, mock_get_field
    ):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.put.return_value = [{"entryId": 1, "fieldId": 10, "rowId": 1, "value": 1}]
        mock_client_class.return_value = mock_client

        def gf(_obj, name):
            if name == "Unknown":
                return None
            return MagicMock(id=10)

        mock_get_field.side_effect = gf

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        cells.write_cells(
            "Company",
            [{"EntryId": 1, "Known": 1, "Unknown": 9, "Other": None}],
            mode="upsert",
        )
        body = mock_client.put.call_args[1]["json"]["storeRequests"]
        assert len(body) == 1
        assert body[0]["fieldId"] == 10


class TestDealCloudCellsWriteCellsEdgeCases:
    """Tests for write_cells edge cases."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_write_cells_empty_column_count(self, mock_client_class):
        """Test write_cells with data having no columns returns [] (no storeRequests)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        data = [{}, {}]
        result = cells.write_cells("Company", data, mode="upsert")

        assert result == []
        mock_client.put.assert_not_called()

    @patch('dealcloud_sdk.cells.dealcloud_cells.DealCloudCells.get_field_by_api_name')
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_write_cells_non_list_result(self, mock_client_class, mock_get_field):
        """Test write_cells handles dict results from post (create)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {
            "entryId": -1,
            "fieldId": 10,
            "rowId": 1001,
            "value": "Test",
        }
        mock_client_class.return_value = mock_client
        mock_get_field.return_value = MagicMock(id=10)

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        data = [{"EntryId": -1, "Name": "Test"}]
        result = cells.write_cells("Company", data, mode="create")

        assert len(result) == 1
        assert result[0]["rowId"] == 1001

    @patch('dealcloud_sdk.cells.dealcloud_cells.DealCloudCells.get_field_by_api_name')
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_write_cells_exception_handling(self, mock_client_class, mock_get_field):
        """Test write_cells propagates exceptions from put (update mode)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.put.side_effect = HttpError(500, "API Error")
        mock_client_class.return_value = mock_client
        mock_get_field.return_value = MagicMock(id=10)

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        data = [{"EntryId": 123, "Name": "Test"}]

        with pytest.raises(HttpError, match="API Error"):
            cells.write_cells("Company", data, mode="update")


class TestDealCloudCellsDeleteCells:
    """Tests for delete_cells (DELETE body = array of entry IDs only; field_ids ignored by API)."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_cells_basic(self, mock_client_class):
        """Test delete_cells sends body as list of entry IDs."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.delete.return_value = [{"EntryId": 1, "Success": True}]
        mock_client_class.return_value = mock_client

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        result = cells.delete_cells("Company", [1, 2, 3])

        mock_client.delete.assert_called_once()
        call_kwargs = mock_client.delete.call_args
        assert call_kwargs[1]["json"] == [1, 2, 3]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_cells_field_ids_ignored(self, mock_client_class):
        """Test delete_cells sends only entry IDs (field_ids not sent; API ignores them)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.delete.return_value = []
        mock_client_class.return_value = mock_client

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        cells.delete_cells("Company", [1], field_ids=[10, 11])

        mock_client.delete.assert_called_once()
        kwargs = mock_client.delete.call_args[1]
        assert kwargs is not None and kwargs.get("json") == [1]


class TestDealCloudCellsBacklinkDmsDocument:
    """Tests for backlink_dms_document method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    @patch.object(DealCloudCells, 'get_field_by_api_name')
    @patch.object(DealCloudCells, 'get_field_by_name')
    def test_backlink_dms_document_with_field_ids(self, mock_get_by_name, mock_get_by_api, mock_client_class):
        """Test backlink_dms_document with field IDs."""
        from dealcloud_sdk.models.schema import Field
        
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"EntryId": 12345, "Success": True}
        mock_client_class.return_value = mock_client
        
        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = cells.backlink_dms_document(
            object_id="Documents",
            title_field=374033,  # Field ID
            title_value="My Document",
            binary_field=374040,  # Field ID
            format_type="pdf",
            document_storage_id="sharepoint_id_123"
        )
        
        assert result["EntryId"] == 12345
        mock_client.post.assert_called_once()
        
        # Verify payload structure
        call_args = mock_client.post.call_args
        payload = call_args[1]["json"]
        assert "storeRequests" in payload
        assert "binaryStoreRequests" in payload
        assert len(payload["storeRequests"]) == 1
        assert len(payload["binaryStoreRequests"]) == 1
        assert payload["storeRequests"][0]["fieldId"] == 374033
        assert payload["storeRequests"][0]["value"] == "My Document"
        assert payload["binaryStoreRequests"][0]["fieldId"] == 374040
        assert payload["binaryStoreRequests"][0]["formatType"] == "pdf"
        assert payload["binaryStoreRequests"][0]["documentStorageId"] == "sharepoint_id_123"
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    @patch.object(DealCloudCells, 'get_field_by_api_name')
    @patch.object(DealCloudCells, 'get_field_by_name')
    def test_backlink_dms_document_with_field_api_names(self, mock_get_by_name, mock_get_by_api, mock_client_class):
        """Test backlink_dms_document with field API names."""
        from dealcloud_sdk.models.schema import Field
        
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"EntryId": 12345, "Success": True}
        mock_client_class.return_value = mock_client
        
        # Mock field resolution
        title_field = Field(id=374033, apiName="Name")
        binary_field = Field(id=374040, apiName="Document")
        mock_get_by_api.side_effect = [title_field, binary_field]
        
        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = cells.backlink_dms_document(
            object_id="Documents",
            title_field="Name",  # API name
            title_value="My Document",
            binary_field="Document",  # API name
            format_type="pdf",
            document_storage_id="box_id_456"
        )
        
        assert result["EntryId"] == 12345
        assert mock_get_by_api.call_count == 2
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    @patch.object(DealCloudCells, 'get_field_by_api_name')
    @patch.object(DealCloudCells, 'get_field_by_name')
    def test_backlink_dms_document_with_display_names(self, mock_get_by_name, mock_get_by_api, mock_client_class):
        """Test backlink_dms_document with field display names (tests line 340)."""
        from dealcloud_sdk.models.schema import Field
        
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"EntryId": 12345, "Success": True}
        mock_client_class.return_value = mock_client
        
        # Mock field resolution: API name returns None, display name returns field
        title_field = Field(id=374033, name="Document Name")
        binary_field = Field(id=374040, name="Document File")
        mock_get_by_api.return_value = None  # API name lookup fails
        mock_get_by_name.side_effect = [title_field, binary_field]  # Display name lookup succeeds
        
        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = cells.backlink_dms_document(
            object_id="Documents",
            title_field="Document Name",  # Display name
            title_value="My Document",
            binary_field="Document File",  # Display name
            format_type="pdf",
            document_storage_id="sharepoint_id_789"
        )
        
        assert result["EntryId"] == 12345
        # Verify both API name and display name lookups were attempted
        assert mock_get_by_api.call_count == 2
        assert mock_get_by_name.call_count == 2
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    @patch.object(DealCloudCells, 'get_field_by_api_name')
    @patch.object(DealCloudCells, 'get_field_by_name')
    def test_backlink_dms_document_with_additional_fields(self, mock_get_by_name, mock_get_by_api, mock_client_class):
        """Test backlink_dms_document with additional fields."""
        from dealcloud_sdk.models.schema import Field
        
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"EntryId": 12345, "Success": True}
        mock_client_class.return_value = mock_client
        
        # Mock field resolution for additional fields
        category_field = Field(id=374050, apiName="Category")
        mock_get_by_api.return_value = category_field
        
        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = cells.backlink_dms_document(
            object_id="Documents",
            title_field=374033,
            title_value="My Document",
            binary_field=374040,
            format_type="pdf",
            document_storage_id="sharepoint_id_123",
            additional_fields={"Category": [1]}  # Choice field
        )
        
        assert result["EntryId"] == 12345
        
        # Verify additional field is in storeRequests
        call_args = mock_client.post.call_args
        payload = call_args[1]["json"]
        assert len(payload["storeRequests"]) == 2  # Title + Category
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    @patch.object(DealCloudCells, 'get_field_by_api_name')
    @patch.object(DealCloudCells, 'get_field_by_name')
    def test_backlink_dms_document_field_not_found(self, mock_get_by_name, mock_get_by_api, mock_client_class):
        """Test backlink_dms_document raises error when field not found."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        # Mock field resolution to return None
        mock_get_by_api.return_value = None
        mock_get_by_name.return_value = None
        
        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        with pytest.raises(ValueError) as exc_info:
            cells.backlink_dms_document(
                object_id="Documents",
                title_field="NonExistentField",
                title_value="My Document",
                binary_field=374040,
                format_type="pdf",
                document_storage_id="sharepoint_id_123"
            )
        
        assert "not found" in str(exc_info.value).lower()
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    @patch.object(DealCloudCells, 'get_field_by_api_name')
    @patch.object(DealCloudCells, 'get_field_by_name')
    def test_backlink_dms_document_list_response(self, mock_get_by_name, mock_get_by_api, mock_client_class):
        """Test backlink_dms_document handles list response."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = [{"EntryId": 12345, "Success": True}]
        mock_client_class.return_value = mock_client
        
        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = cells.backlink_dms_document(
            object_id="Documents",
            title_field=374033,
            title_value="My Document",
            binary_field=374040,
            format_type="pdf",
            document_storage_id="sharepoint_id_123"
        )
        
        assert result["EntryId"] == 12345
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    @patch.object(DealCloudCells, 'get_field_by_api_name')
    @patch.object(DealCloudCells, 'get_field_by_name')
    def test_backlink_dms_document_empty_list_response(self, mock_get_by_name, mock_get_by_api, mock_client_class):
        """Test backlink_dms_document handles empty list response."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = []
        mock_client_class.return_value = mock_client
        
        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = cells.backlink_dms_document(
            object_id="Documents",
            title_field=374033,
            title_value="My Document",
            binary_field=374040,
            format_type="pdf",
            document_storage_id="sharepoint_id_123"
        )
        
        assert result == {}
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    @patch.object(DealCloudCells, 'get_field_by_api_name')
    @patch.object(DealCloudCells, 'get_field_by_name')
    def test_backlink_dms_document_dict_response(self, mock_get_by_name, mock_get_by_api, mock_client_class):
        """Test backlink_dms_document handles dict response (non-list)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"EntryId": 12345, "Success": True, "Message": "Created"}
        mock_client_class.return_value = mock_client
        
        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = cells.backlink_dms_document(
            object_id="Documents",
            title_field=374033,
            title_value="My Document",
            binary_field=374040,
            format_type="pdf",
            document_storage_id="sharepoint_id_123"
        )
        
        assert result["EntryId"] == 12345
        assert result["Message"] == "Created"
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    @patch.object(DealCloudCells, 'get_field_by_api_name')
    @patch.object(DealCloudCells, 'get_field_by_name')
    def test_backlink_dms_document_multiple_additional_fields(self, mock_get_by_name, mock_get_by_api, mock_client_class):
        """Test backlink_dms_document with multiple additional fields."""
        from dealcloud_sdk.models.schema import Field
        
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"EntryId": 12345, "Success": True}
        mock_client_class.return_value = mock_client
        
        # Mock field resolution for multiple additional fields
        category_field = Field(id=374050, apiName="Category")
        status_field = Field(id=374051, apiName="Status")
        mock_get_by_api.side_effect = [category_field, status_field]
        
        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = cells.backlink_dms_document(
            object_id="Documents",
            title_field=374033,
            title_value="My Document",
            binary_field=374040,
            format_type="pdf",
            document_storage_id="sharepoint_id_123",
            additional_fields={
                "Category": [1],
                "Status": "Active"
            }
        )
        
        assert result["EntryId"] == 12345
        
        # Verify all fields are in storeRequests
        call_args = mock_client.post.call_args
        payload = call_args[1]["json"]
        assert len(payload["storeRequests"]) == 3  # Title + Category + Status
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    @patch.object(DealCloudCells, 'get_field_by_api_name')
    @patch.object(DealCloudCells, 'get_field_by_name')
    def test_backlink_dms_document_additional_field_not_found(self, mock_get_by_name, mock_get_by_api, mock_client_class):
        """Test backlink_dms_document raises error when additional field not found."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        # Mock field resolution: title and binary fields work, but additional field fails
        mock_get_by_api.return_value = None
        mock_get_by_name.return_value = None
        
        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        with pytest.raises(ValueError) as exc_info:
            cells.backlink_dms_document(
                object_id="Documents",
                title_field=374033,
                title_value="My Document",
                binary_field=374040,
                format_type="pdf",
                document_storage_id="sharepoint_id_123",
                additional_fields={"NonExistentField": "value"}
            )
        
        assert "not found" in str(exc_info.value).lower()
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    @patch.object(DealCloudCells, 'get_field_by_api_name')
    @patch.object(DealCloudCells, 'get_field_by_name')
    def test_resolve_field_id_with_none_id_from_api_name(self, mock_get_by_name, mock_get_by_api, mock_client_class):
        """Test _resolve_field_id when field found by API name but id is None."""
        from dealcloud_sdk.models.schema import Field
        
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        # Mock field with None id
        field_none_id = Field(id=None, apiName="Name")
        field_with_id = Field(id=374033, name="Document Name")
        mock_get_by_api.return_value = field_none_id  # First call returns field with None id
        mock_get_by_name.return_value = field_with_id  # Falls back to display name
        
        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        # Should fall through to display name lookup
        result = cells._resolve_field_id("Documents", "Name")
        assert result == 374033
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    @patch.object(DealCloudCells, 'get_field_by_api_name')
    @patch.object(DealCloudCells, 'get_field_by_name')
    def test_resolve_field_id_with_none_id_from_display_name(self, mock_get_by_name, mock_get_by_api, mock_client_class):
        """Test _resolve_field_id when field found by display name but id is None."""
        from dealcloud_sdk.models.schema import Field
        
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        # Mock field with None id
        field_none_id = Field(id=None, name="Document Name")
        mock_get_by_api.return_value = None
        mock_get_by_name.return_value = field_none_id
        
        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        # Should raise ValueError since id is None
        with pytest.raises(ValueError) as exc_info:
            cells._resolve_field_id("Documents", "Document Name")
        
        assert "not found" in str(exc_info.value).lower()
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_resolve_field_id_with_integer(self, mock_client_class):
        """Test _resolve_field_id with integer field ID (should return as-is)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        # Should return integer as-is without any lookups
        result = cells._resolve_field_id("Documents", 374033)
        assert result == 374033


class TestDealCloudCellsCreateEntryWithStoreRequests:
    """Tests for create_entry_with_store_requests method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_create_entry_with_store_requests_basic(self, mock_client_class):
        """Test create_entry_with_store_requests with basic payload."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"EntryId": 12345, "Success": True}
        mock_client_class.return_value = mock_client
        
        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = cells.create_entry_with_store_requests(
            object_id="Documents",
            store_requests=[
                {"entryId": -1, "fieldId": 374033, "value": "My Document"}
            ],
            binary_store_requests=[
                {
                    "entryId": -1,
                    "fieldId": 374040,
                    "formatType": "pdf",
                    "documentStorageId": "sharepoint_id_123"
                }
            ]
        )
        
        assert result["EntryId"] == 12345
        
        # Verify payload structure
        call_args = mock_client.post.call_args
        payload = call_args[1]["json"]
        assert "storeRequests" in payload
        assert "binaryStoreRequests" in payload
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_create_entry_with_store_requests_only_store(self, mock_client_class):
        """Test create_entry_with_store_requests with only storeRequests."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"EntryId": 12345, "Success": True}
        mock_client_class.return_value = mock_client
        
        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = cells.create_entry_with_store_requests(
            object_id="Documents",
            store_requests=[
                {"entryId": -1, "fieldId": 374033, "value": "My Document"}
            ]
        )
        
        assert result["EntryId"] == 12345
        
        # Verify only storeRequests in payload
        call_args = mock_client.post.call_args
        payload = call_args[1]["json"]
        assert "storeRequests" in payload
        assert "binaryStoreRequests" not in payload
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_create_entry_with_store_requests_only_binary(self, mock_client_class):
        """Test create_entry_with_store_requests with only binaryStoreRequests."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"EntryId": 12345, "Success": True}
        mock_client_class.return_value = mock_client
        
        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = cells.create_entry_with_store_requests(
            object_id="Documents",
            binary_store_requests=[
                {
                    "entryId": -1,
                    "fieldId": 374040,
                    "formatType": "pdf",
                    "documentStorageId": "sharepoint_id_123"
                }
            ]
        )
        
        assert result["EntryId"] == 12345
        
        # Verify only binaryStoreRequests in payload
        call_args = mock_client.post.call_args
        payload = call_args[1]["json"]
        assert "storeRequests" not in payload
        assert "binaryStoreRequests" in payload
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_create_entry_with_store_requests_empty_raises(self, mock_client_class):
        """Test create_entry_with_store_requests raises when both are empty."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        with pytest.raises(ValueError) as exc_info:
            cells.create_entry_with_store_requests(
                object_id="Documents"
            )
        
        assert "at least one" in str(exc_info.value).lower()
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_create_entry_with_store_requests_list_response(self, mock_client_class):
        """Test create_entry_with_store_requests handles list response."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = [{"EntryId": 12345, "Success": True}]
        mock_client_class.return_value = mock_client
        
        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = cells.create_entry_with_store_requests(
            object_id="Documents",
            store_requests=[
                {"entryId": -1, "fieldId": 374033, "value": "My Document"}
            ]
        )
        
        assert result["EntryId"] == 12345
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_create_entry_with_store_requests_empty_list_response(self, mock_client_class):
        """Test create_entry_with_store_requests handles empty list response."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = []
        mock_client_class.return_value = mock_client
        
        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = cells.create_entry_with_store_requests(
            object_id="Documents",
            store_requests=[
                {"entryId": -1, "fieldId": 374033, "value": "My Document"}
            ]
        )
        
        assert result == {}
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_create_entry_with_store_requests_dict_response(self, mock_client_class):
        """Test create_entry_with_store_requests handles dict response (non-list)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"EntryId": 12345, "Success": True, "Message": "Created"}
        mock_client_class.return_value = mock_client
        
        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = cells.create_entry_with_store_requests(
            object_id="Documents",
            store_requests=[
                {"entryId": -1, "fieldId": 374033, "value": "My Document"}
            ]
        )
        
        assert result["EntryId"] == 12345
        assert result["Message"] == "Created"
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_create_entry_with_store_requests_multiple_store_requests(self, mock_client_class):
        """Test create_entry_with_store_requests with multiple store requests."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"EntryId": 12345, "Success": True}
        mock_client_class.return_value = mock_client
        
        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = cells.create_entry_with_store_requests(
            object_id="Documents",
            store_requests=[
                {"entryId": -1, "fieldId": 374033, "value": "Document 1"},
                {"entryId": -1, "fieldId": 374034, "value": "Category A"},
                {"entryId": -1, "fieldId": 374035, "value": "Status Active"}
            ]
        )
        
        assert result["EntryId"] == 12345
        
        # Verify all store requests are in payload
        call_args = mock_client.post.call_args
        payload = call_args[1]["json"]
        assert len(payload["storeRequests"]) == 3
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_create_entry_with_store_requests_multiple_binary_store_requests(self, mock_client_class):
        """Test create_entry_with_store_requests with multiple binary store requests."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"EntryId": 12345, "Success": True}
        mock_client_class.return_value = mock_client
        
        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = cells.create_entry_with_store_requests(
            object_id="Documents",
            binary_store_requests=[
                {
                    "entryId": -1,
                    "fieldId": 374040,
                    "formatType": "pdf",
                    "documentStorageId": "sharepoint_id_1"
                },
                {
                    "entryId": -1,
                    "fieldId": 374041,
                    "formatType": "docx",
                    "documentStorageId": "sharepoint_id_2"
                }
            ]
        )
        
        assert result["EntryId"] == 12345
        
        # Verify all binary store requests are in payload
        call_args = mock_client.post.call_args
        payload = call_args[1]["json"]
        assert len(payload["binaryStoreRequests"]) == 2
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_create_entry_with_store_requests_update_mode(self, mock_client_class):
        """Test create_entry_with_store_requests with update mode (positive entryId)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"EntryId": 12345, "Success": True}
        mock_client_class.return_value = mock_client
        
        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = cells.create_entry_with_store_requests(
            object_id="Documents",
            store_requests=[
                {"entryId": 12345, "fieldId": 374033, "value": "Updated Document"}
            ]
        )
        
        assert result["EntryId"] == 12345
        
        # Verify entryId is positive (update mode)
        call_args = mock_client.post.call_args
        payload = call_args[1]["json"]
        assert payload["storeRequests"][0]["entryId"] == 12345

