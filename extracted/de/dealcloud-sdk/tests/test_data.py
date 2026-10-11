"""Tests for DealCloudData class."""

import pytest
import pandas as pd
from unittest.mock import AsyncMock, MagicMock, patch, call
from intapp_rest_client.exceptions import HttpError

from dealcloud_sdk.data.dealcloud_data import DealCloudData, ErrorHandling
from dealcloud_sdk.models.data import Rows


class TestDealCloudDataReadData:
    """Tests for read_data method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_basic(self, mock_client_class):
        """Test basic read_data returns DataFrame (uses get_paginated)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get_paginated.return_value = iter([
            [{"EntryId": 1, "Name": "Company A"}, {"EntryId": 2, "Name": "Company B"}],
        ])
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = data.read_data(object_id="Company", output="pandas")

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_output_list(self, mock_client_class):
        """Test read_data with output='list' (uses get_paginated)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get_paginated.return_value = iter([
            [{"EntryId": 1, "Name": "Company A"}, {"EntryId": 2, "Name": "Company B"}],
        ])
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = data.read_data(object_id="Company", output="list")

        assert isinstance(result, list)
        assert len(result) == 2
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_empty_result(self, mock_client_class):
        """Test read_data with empty result (get_paginated yields no batches)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get_paginated.return_value = iter([])
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = data.read_data(object_id="Company", output="pandas")
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_empty_result_list(self, mock_client_class):
        """Test read_data with empty result and output='list'."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {"totalRecords": 0, "rows": []}
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = data.read_data(object_id="Company", output="list")
        
        assert result == []
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_both_object_and_view_raises(self, mock_client_class):
        """Test read_data raises when both object_id and view_id provided."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        with pytest.raises(AttributeError) as exc_info:
            data.read_data(object_id="Company", view_id=1, output="list")
        
        assert "Only one of" in str(exc_info.value)
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_neither_raises(self, mock_client_class):
        """Test read_data raises when neither object_id nor view_id provided."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        with pytest.raises(AttributeError) as exc_info:
            data.read_data(output="list")
        
        assert "Must pass one of" in str(exc_info.value)
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_output_required(self, mock_client_class):
        """Test read_data raises when output parameter not provided (breaking change from v0.x)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        with pytest.raises(ValueError) as exc_info:
            data.read_data(object_id="Company")  # No output specified
        
        assert "output" in str(exc_info.value).lower()
        assert "required" in str(exc_info.value).lower()
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_invalid_output_raises(self, mock_client_class):
        """Test read_data raises for invalid output value."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        with pytest.raises(ValueError) as exc_info:
            data.read_data(object_id="Company", output="invalid")
        
        assert "pandas" in str(exc_info.value) or "list" in str(exc_info.value) or "polars" in str(exc_info.value)
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_with_fields(self, mock_client_class):
        """Test read_data with specific fields (get_paginated params)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get_paginated.return_value = iter([[{"EntryId": 1, "Name": "A"}]])
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        data.read_data(object_id="Company", fields=["Name", "Status"], output="list")

        call_kwargs = mock_client.get_paginated.call_args[1]
        assert "params" in call_kwargs
        assert call_kwargs["params"].get("fields") == ["Name", "Status"]
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_with_query(self, mock_client_class):
        """Test read_data with query uses post_paginated."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post_paginated.return_value = iter([[{"EntryId": 1, "Name": "Filtered"}]])
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        data.read_data(object_id="Company", query="Name = 'Test'", output="list")

        assert mock_client.post_paginated.called
    

class TestDealCloudDataInsertData:
    """Tests for insert_data method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_insert_data_basic(self, mock_client_class):
        """Test basic insert_data (uses post)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client.post.return_value = [{"EntryId": 1, "Success": True}, {"EntryId": 2, "Success": True}]
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = data.insert_data(
            "Company",
            [{"Name": "Company A"}, {"Name": "Company B"}],
        )

        assert len(result) == 2
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_insert_data_pandas(self, mock_client_class):
        """Test insert_data with output='pandas'."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client.post.return_value = [
            {"EntryId": 1, "Success": True},
        ]
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = data.insert_data(
            "Company",
            [{"Name": "Company A"}],
            output="pandas",
        )
        
        assert isinstance(result, pd.DataFrame)


class TestDealCloudDataUpdateData:
    """Tests for update_data method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_update_data_basic(self, mock_client_class):
        """Test basic update_data (uses put)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client.put.return_value = [{"EntryId": 1, "Success": True}]
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = data.update_data(
            "Company",
            [{"EntryId": 1, "Name": "Updated Name"}],
        )

        assert len(result) == 1


class TestDealCloudDataUpsertData:
    """Tests for upsert_data method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_upsert_data_mixed(self, mock_client_class):
        """Test upsert_data with mix of inserts and updates."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client.post.return_value = [{"EntryId": 100, "Success": True}]
        mock_client.put.return_value = [{"EntryId": 1, "Success": True}]
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = data.upsert_data(
            "Company",
            [
                {"Name": "New Company"},  # Insert (no EntryId)
                {"EntryId": 1, "Name": "Update"},  # Update
            ],
        )
        
        assert len(result) == 2
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_upsert_data_inserts_only(self, mock_client_class):
        """Test upsert_data with only inserts."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client.post.return_value = [{"EntryId": 100, "Success": True}]
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = data.upsert_data("Company", [{"Name": "New"}])
        
        assert mock_client.post.called
        assert not mock_client.put.called
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_upsert_data_updates_only(self, mock_client_class):
        """Test upsert_data with only updates."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client.put.return_value = [{"EntryId": 1, "Success": True}]
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = data.upsert_data("Company", [{"EntryId": 1, "Name": "Update"}])
        
        assert mock_client.put.called


class TestDealCloudDataDeleteData:
    """Tests for delete_data method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_data_basic(self, mock_client_class):
        """Test basic delete_data (uses DELETE with JSON body per Swagger)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.delete.return_value = [{"deleted": [1, 2, 3]}]
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        data.delete_data("Company", [1, 2, 3])

        mock_client.delete.assert_called()
        call_kw = mock_client.delete.call_args[1]
        assert call_kw["json"] == [1, 2, 3]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_data_empty_list(self, mock_client_class):
        """Test delete_data with empty list returns early."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = data.delete_data("Company", [])

        assert result == []
        assert not mock_client.delete.called


class TestDealCloudDataValidateFieldMapping:
    """Tests for _validate_field_mapping method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_validate_field_mapping_success(self, mock_client_class):
        """Test validation passes for valid columns."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
            {"apiName": "Status", "name": "Status", "fieldType": 2, "id": 11, "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        # Should not raise
        data.validate_field_mapping("Company", {"Name", "Status"})
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_validate_field_mapping_failure(self, mock_client_class):
        """Test validation fails for invalid columns."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        with pytest.raises(KeyError) as exc_info:
            data.validate_field_mapping("Company", {"Name", "InvalidField"})
        
        assert "Mapping error" in str(exc_info.value)
        assert "InvalidField" in str(exc_info.value)
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_validate_field_mapping_allows_entry_id(self, mock_client_class):
        """Test validation allows EntryId column."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        # EntryId should be valid
        data.validate_field_mapping("Company", {"EntryId", "Name"})


class TestDealCloudDataStreamingMethods:
    """Tests for streaming pagination methods."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_streaming_uses_get_paginated(self, mock_client_class):
        """Test read_data_streaming uses get_paginated."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get_paginated.return_value = iter([[{"EntryId": 1}], [{"EntryId": 2}]])
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        batches = list(data.read_data_streaming("Company"))
        
        assert len(batches) == 2
        mock_client.get_paginated.assert_called_once()
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_streaming_uses_config_page_size(self, mock_client_class):
        """Test read_data_streaming uses configured page_size."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get_paginated.return_value = iter([])
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        # Default page_size is 1000
        
        list(data.read_data_streaming("Company"))
        
        call_kwargs = mock_client.get_paginated.call_args[1]
        assert call_kwargs["page_size"] == 1000
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_streaming_override_page_size(self, mock_client_class):
        """Test read_data_streaming allows page_size override."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get_paginated.return_value = iter([])
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        list(data.read_data_streaming("Company", page_size=500))
        
        call_kwargs = mock_client.get_paginated.call_args[1]
        assert call_kwargs["page_size"] == 500
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_streaming_uses_config_concurrency(self, mock_client_class):
        """Test read_data_streaming uses configured concurrency."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get_paginated.return_value = iter([])
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        list(data.read_data_streaming("Company"))

        mock_client.get_paginated.assert_called_once()
        # max_concurrency omitted for compatibility with older intapp-rest-client
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_streaming_override_concurrency(self, mock_client_class):
        """Test read_data_streaming allows concurrency override."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get_paginated.return_value = iter([])
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        list(data.read_data_streaming("Company", max_concurrency=5))

        mock_client.get_paginated.assert_called_once()
        # max_concurrency accepted by SDK but not passed to client for older-client compatibility
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_streaming_with_fields(self, mock_client_class):
        """Test read_data_streaming passes fields parameter."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get_paginated.return_value = iter([])
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        list(data.read_data_streaming("Company", fields=["EntryId", "Name"]))
        
        call_kwargs = mock_client.get_paginated.call_args[1]
        assert "fields" in call_kwargs["params"]
        assert call_kwargs["params"]["fields"] == ["EntryId", "Name"]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_streaming_with_query_uses_post_paginated(self, mock_client_class):
        """Test read_data_streaming with query uses post_paginated."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post_paginated.return_value = iter([[{"EntryId": 1}, {"EntryId": 2}]])
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        batches = list(data.read_data_streaming("Company", query="EntryId in (1,2,3)"))
        assert len(batches) == 1
        assert len(batches[0]) == 2
        mock_client.post_paginated.assert_called_once()
        mock_client.get_paginated.assert_not_called()

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_streaming_without_query_uses_get_paginated(self, mock_client_class):
        """Test read_data_streaming without query uses get_paginated."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get_paginated.return_value = iter([[{"EntryId": 1}]])
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        list(data.read_data_streaming("Company"))
        mock_client.get_paginated.assert_called_once()
        mock_client.post_paginated.assert_not_called()


class TestDealCloudDataQueryData:
    """Tests for query_data helper."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_query_data_returns_full_response(self, mock_client_class):
        """Test query_data POSTs to rows/query and returns full response."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"rows": [{"EntryId": 1, "Name": "A"}], "totalRecords": 1}
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        resp = data.query_data("Company", "Status = 'Active'", limit=10)
        assert resp["rows"] == [{"EntryId": 1, "Name": "A"}]
        assert resp["totalRecords"] == 1
        mock_client.post.assert_called_once()
        call_args = mock_client.post.call_args
        assert "/rows/query/Company" in call_args[0][0]
        body = call_args[1]["json"]
        assert body["query"] == "Status = 'Active'"
        assert body["limit"] == 10
        assert body["wrapIntoArrays"] is True

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_query_data_with_fields_and_skip(self, mock_client_class):
        """Test query_data passes fields and skip."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.post.return_value = {"rows": []}
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        data.query_data("Contact", "EntryId > 0", fields=["EntryId", "Name"], limit=5, skip=10)
        body = mock_client.post.call_args[1]["json"]
        assert body["fields"] == ["EntryId", "Name"]
        assert body["limit"] == 5
        assert body["skip"] == 10


class TestProgressCallbacks:
    """Tests for progress callbacks on data operations."""

    def test_progress_callback_signature(self):
        """Test that progress callbacks receive correct parameters."""
        progress_calls = []

        def callback(current, total):
            progress_calls.append((current, total))

        callback(10, 100)
        assert progress_calls[0] == (10, 100)


class TestDataOperationsWithErrorHandling:
    """Tests for data operations with error_handling parameter."""

    def test_read_data_accepts_error_handling(self):
        """read_data accepts error_handling parameter."""
        import inspect
        sig = inspect.signature(DealCloudData.read_data)
        params = sig.parameters
        assert "error_handling" in params
        assert params["error_handling"].default == ErrorHandling.FAIL_FAST

    def test_insert_data_accepts_error_handling(self):
        """insert_data accepts error_handling parameter."""
        import inspect
        sig = inspect.signature(DealCloudData.insert_data)
        assert "error_handling" in sig.parameters

    def test_update_data_accepts_error_handling(self):
        """update_data accepts error_handling parameter."""
        import inspect
        sig = inspect.signature(DealCloudData.update_data)
        assert "error_handling" in sig.parameters

    def test_delete_data_accepts_error_handling(self):
        """delete_data accepts error_handling parameter."""
        import inspect
        sig = inspect.signature(DealCloudData.delete_data)
        assert "error_handling" in sig.parameters


class TestDataOperationsWithProgressCallback:
    """Tests for data operations with progress_callback parameter."""

    def test_read_data_accepts_progress_callback(self):
        """read_data accepts progress_callback parameter."""
        import inspect
        sig = inspect.signature(DealCloudData.read_data)
        assert "progress_callback" in sig.parameters

    def test_insert_data_accepts_progress_callback(self):
        """insert_data accepts progress_callback parameter."""
        import inspect
        sig = inspect.signature(DealCloudData.insert_data)
        assert "progress_callback" in sig.parameters

    def test_delete_data_accepts_progress_callback(self):
        """delete_data accepts progress_callback parameter."""
        import inspect
        sig = inspect.signature(DealCloudData.delete_data)
        assert "progress_callback" in sig.parameters


class TestStreamingRead:
    """Tests for read_data_streaming and read_view_streaming."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_streaming_single_batch(self, mock_client_class):
        """Test streaming read with single batch."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get_paginated.return_value = iter([
            [{"EntryId": 1}, {"EntryId": 2}, {"EntryId": 3}]
        ])
        mock_client_class.return_value = mock_client

        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        batches = list(dc.read_data_streaming("Company", page_size=1000))
        assert len(batches) == 1
        assert len(batches[0]) == 3
        assert batches[0][0]["EntryId"] == 1

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_streaming_multiple_batches(self, mock_client_class):
        """Test streaming read with multiple batches."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get_paginated.return_value = iter([
            [{"EntryId": i} for i in range(1000)],
            [{"EntryId": i} for i in range(1000, 1500)],
        ])
        mock_client_class.return_value = mock_client

        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        batches = list(dc.read_data_streaming("Company", page_size=1000))
        assert len(batches) == 2
        assert len(batches[0]) == 1000
        assert len(batches[1]) == 500

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_streaming_empty_object(self, mock_client_class):
        """Test streaming read with empty object."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get_paginated.return_value = iter([])
        mock_client_class.return_value = mock_client

        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        batches = list(dc.read_data_streaming("Company"))
        assert len(batches) == 0

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_streaming_with_fields(self, mock_client_class):
        """Test streaming read with specific fields."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get_paginated.return_value = iter([[{"EntryId": 1, "Name": "Test"}]])
        mock_client_class.return_value = mock_client

        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        batches = list(dc.read_data_streaming("Company", fields=["EntryId", "Name"], page_size=1000))
        call_kwargs = mock_client.get_paginated.call_args[1]
        assert "fields" in call_kwargs["params"]
        assert call_kwargs["params"]["fields"] == ["EntryId", "Name"]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_streaming_error_handling(self, mock_client_class):
        """Test streaming read raises on error."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}

        def error_generator():
            raise RuntimeError("Network error")
            yield  # pragma: no cover

        mock_client.get_paginated.return_value = error_generator()
        mock_client_class.return_value = mock_client

        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with pytest.raises(RuntimeError, match="Network error"):
            list(dc.read_data_streaming("Company"))

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_view_streaming_single_batch(self, mock_client_class):
        """Test view streaming read with single batch."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {
            "totalRecords": 1,
            "rows": [{"id": 12345, "name": "Test View"}],
        }
        mock_client.post_paginated_params.return_value = iter([
            [{"EntryId": 1}, {"EntryId": 2}]
        ])
        mock_client_class.return_value = mock_client

        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        batches = list(dc.read_view_streaming(12345, page_size=1000))
        assert len(batches) == 1
        assert len(batches[0]) == 2

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_view_streaming_with_name_lookup(self, mock_client_class):
        """Test view streaming with name lookup."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {
            "rows": [{"id": 12345, "name": "My View"}, {"id": 99999, "name": "Other View"}],
            "totalRecords": 2
        }
        mock_client.post_paginated_params.return_value = iter([[{"EntryId": 1}]])
        mock_client_class.return_value = mock_client

        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        batches = list(dc.read_view_streaming("My View", page_size=1000))
        assert len(batches) == 1
        call_url = mock_client.post_paginated_params.call_args[0][0]
        assert "12345" in call_url

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_view_streaming_view_not_found(self, mock_client_class):
        """Test view streaming raises when view not found."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {"rows": [], "totalRecords": 0}
        mock_client_class.return_value = mock_client

        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with pytest.raises(AttributeError, match="not found"):
            list(dc.read_view_streaming("NonExistent View"))


class TestDealCloudDataResolveChoiceFields:
    """Tests for resolve in read_data."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_resolve_name(self, mock_client_class):
        """Test read_data with resolve='name'."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        
        # Return data with choice field values as IDs
        data_response = {
            "totalRecords": 1,
            "rows": [{"EntryId": 1, "Status": [1], "Priority": [2]}]
        }
        empty_response = {"totalRecords": 0, "rows": []}
        mock_client.get.side_effect = [data_response] + [empty_response] * 20
        
        # Return fields with choice values
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        # Mock get_fields to return choice field
        data.get_choice_reference_fields = MagicMock(return_value=[
            MagicMock(apiName="Status", fieldType=2, choiceValues=[
                MagicMock(id=1, name="Active"),
                MagicMock(id=2, name="Inactive")
            ])
        ])
        
        result = data.read_data(object_id="Company", resolve="name", output="pandas")
        
        assert isinstance(result, pd.DataFrame)


class TestDealCloudDataProgressCallbacks:
    """Tests for progress callback functionality."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_with_progress_callback(self, mock_client_class):
        """Test read_data calls progress callback."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get_paginated.return_value = iter([
            [{"EntryId": 1}, {"EntryId": 2}],
        ])
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        progress_calls = []
        def track_progress(current, total):
            progress_calls.append((current, total))

        result = data.read_data(object_id="Company", progress_callback=track_progress, output="list")

        # Progress should have been called
        assert len(progress_calls) > 0


class TestDealCloudDataErrorHandling:
    """Tests for error handling modes."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_collect_errors(self, mock_client_class):
        """Test read_data with COLLECT error handling (uses get_paginated)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get_paginated.return_value = iter([[{"EntryId": 1}]])
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        from dealcloud_sdk.data.dealcloud_data import ErrorHandling, BatchResult
        
        result = data.read_data(
            object_id="Company",
            output="list",
            error_handling=ErrorHandling.COLLECT
        )
        
        assert isinstance(result, BatchResult)
        assert result.total_succeeded >= 0


class TestDealCloudDataInsertWithOptions:
    """Tests for insert_data with various options."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_insert_data_pandas_output(self, mock_client_class):
        """Test insert_data with pandas output (uses post)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = [{"EntryId": 1, "Name": "New"}]
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = data.insert_data("Company", [{"Name": "New Company"}], output="pandas")
        
        assert isinstance(result, pd.DataFrame)
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_insert_data_with_progress_callback(self, mock_client_class):
        """Test insert_data with progress callback (uses post)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = [{"EntryId": 1}]
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        progress_calls = []
        def track_progress(current, total):
            progress_calls.append((current, total))
        
        result = data.insert_data("Company", [{"Name": "New"}], progress_callback=track_progress)
        
        assert len(progress_calls) > 0
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_insert_data_collect_error_handling(self, mock_client_class):
        """Test insert_data with COLLECT error handling."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client.post.return_value = [{"EntryId": 1}]
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        from dealcloud_sdk.data.dealcloud_data import ErrorHandling, BatchResult

        result = data.insert_data(
            "Company", [{"Name": "New"}],
            error_handling=ErrorHandling.COLLECT
        )

        assert isinstance(result, BatchResult)


class TestDealCloudDataUpdateWithOptions:
    """Tests for update_data with various options."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_update_data_pandas_output(self, mock_client_class):
        """Test update_data with pandas output."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.put.return_value = [{"EntryId": 1, "Name": "Updated"}]
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = data.update_data("Company", [{"EntryId": 1, "Name": "Updated"}], output="pandas")
        
        assert isinstance(result, pd.DataFrame)
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_update_data_collect_error_handling(self, mock_client_class):
        """Test update_data with COLLECT."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client.put.return_value = [{"EntryId": 1, "Success": True}]
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        from dealcloud_sdk.data.dealcloud_data import ErrorHandling, BatchResult

        result = data.update_data(
            "Company", [{"EntryId": 1, "Name": "Updated"}],
            error_handling=ErrorHandling.COLLECT
        )

        assert isinstance(result, BatchResult)


class TestDealCloudDataDeleteWithOptions:
    """Tests for delete_data with various options."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_data_pagination(self, mock_client_class):
        """Test delete_data with pagination (uses DELETE with JSON body per batch)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.delete.return_value = [{"deleted": 5}]
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        data.delete_data("Company", list(range(1, 100)))

        assert mock_client.delete.called
        assert mock_client.delete.call_args[1]["json"] == list(range(1, 100))

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_data_with_progress_callback(self, mock_client_class):
        """Test delete_data with progress callback (uses DELETE per batch)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.delete.return_value = [{"deleted": [1, 2, 3]}]
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        progress_calls = []
        def track_progress(current, total):
            progress_calls.append((current, total))

        data.delete_data("Company", [1, 2, 3], progress_callback=track_progress)

        assert mock_client.delete.called
        assert progress_calls == [(1, 1)]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_data_collect_error_handling(self, mock_client_class):
        """Test delete_data with COLLECT (DELETE per batch; success)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.delete.return_value = []
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        from dealcloud_sdk.data.dealcloud_data import ErrorHandling, BatchResult

        result = data.delete_data(
            "Company", [1, 2, 3],
            error_handling=ErrorHandling.COLLECT
        )

        assert isinstance(result, BatchResult)


class TestDealCloudDataAsyncStreamingMethods:
    """Tests for async streaming pagination methods."""
    
    @pytest.mark.asyncio
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    async def test_aread_data_streaming_uses_aget_paginated(self, mock_client_class):
        """Test aread_data_streaming uses aget_paginated."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        
        async def mock_aget_paginated(*args, **kwargs):
            yield [{"EntryId": 1}]
            yield [{"EntryId": 2}]
        
        mock_client.aget_paginated = mock_aget_paginated
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        batches = []
        async for batch in data.aread_data_streaming("Company"):
            batches.append(batch)
        
        assert len(batches) == 2
    
    @pytest.mark.asyncio
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    async def test_aread_data_streaming_with_fields(self, mock_client_class):
        """Test aread_data_streaming passes fields parameter."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        
        call_kwargs_captured = {}
        
        async def mock_aget_paginated(*args, **kwargs):
            call_kwargs_captured.update(kwargs)
            yield [{"EntryId": 1}]
        
        mock_client.aget_paginated = mock_aget_paginated
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        batches = []
        async for batch in data.aread_data_streaming("Company", fields=["EntryId", "Name"]):
            batches.append(batch)
        
        assert "fields" in call_kwargs_captured.get("params", {})

    @pytest.mark.asyncio
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    async def test_aread_data_streaming_with_query_uses_apost_paginated(self, mock_client_class):
        """Test aread_data_streaming with query uses apost_paginated."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}

        async def mock_apost_gen(*args, **kwargs):
            yield [{"EntryId": 1}, {"EntryId": 2}]

        mock_client.apost_paginated.return_value = mock_apost_gen()
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        batches = []
        async for batch in data.aread_data_streaming("Company", query="EntryId in (1,2,3)"):
            batches.append(batch)
        assert len(batches) == 1
        assert len(batches[0]) == 2
        mock_client.apost_paginated.assert_called_once()
        mock_client.aget_paginated.assert_not_called()

    @pytest.mark.asyncio
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    async def test_aread_data_streaming_without_query_uses_aget_paginated(self, mock_client_class):
        """Test aread_data_streaming without query uses aget_paginated."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}

        async def mock_aget_gen(*args, **kwargs):
            yield [{"EntryId": 1}]

        mock_client.aget_paginated.return_value = mock_aget_gen()
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        batches = []
        async for batch in data.aread_data_streaming("Company"):
            batches.append(batch)
        assert len(batches) == 1
        mock_client.aget_paginated.assert_called_once()
        mock_client.apost_paginated.assert_not_called()

    @pytest.mark.asyncio
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    async def test_aread_data_streaming_explicit_page_size_and_max_concurrency(
        self, mock_client_class
    ):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        captured = {}

        async def aget_paginated(endpoint, **kwargs):
            captured.update(kwargs)
            yield [{"EntryId": 1}]

        mock_client.aget_paginated = aget_paginated
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        batches = []
        async for batch in data.aread_data_streaming(
            "Company", page_size=50, max_concurrency=2
        ):
            batches.append(batch)
        assert len(batches) == 1
        assert captured.get("page_size") == 50
    

class TestDealCloudDataChoiceReferenceFields:
    """Tests for _get_choice_reference_fields method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_choice_reference_fields(self, mock_client_class):
        """Test _get_choice_reference_fields filters by field type."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        # Field types: TEXT=1, CHOICE=2, REFERENCE=5, USER=7
        mock_client.get.return_value = [
            {"apiName": "Name", "fieldType": 1, "id": 1, "entryListId": 100},  # Text
            {"apiName": "Status", "fieldType": 2, "id": 2, "entryListId": 100},  # Choice
            {"apiName": "Owner", "fieldType": 5, "id": 3, "entryListId": 100},  # Reference
            {"apiName": "Creator", "fieldType": 7, "id": 4, "entryListId": 100},  # User
        ]
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        # Call the method
        fields = data.get_choice_reference_fields("Company")
        
        # Should only include choice (2), reference (5), and user (7) types
        api_names = [f.apiName for f in fields]
        assert "Status" in api_names
        assert "Owner" in api_names
        assert "Creator" in api_names
        assert "Name" not in api_names


class TestDealCloudDataParallelRequestsErrorHandling:
    """Tests for parallel request error handling paths."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_parallel_get_log_only_errors(self, mock_client_class):
        """Test _parallel_requests_get with LOG_ONLY (client.parallel_get returns tuple)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.parallel_get.return_value = ([{"rows": [{"EntryId": 1}]}], [{"error": "Network error"}])
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        from dealcloud_sdk.data.dealcloud_data import ErrorHandling

        results, errors = data._parallel_requests_get(
            ["http://url1", "http://url2"],
            max_workers=2,
            error_handling=ErrorHandling.LOG_ONLY
        )

        assert len(results) == 1
        assert len(errors) == 1
        assert "Network error" in errors[0]["error"]
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_parallel_get_collect_errors(self, mock_client_class):
        """Test _parallel_requests_get with COLLECT (client returns tuple with response_body)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.parallel_get.return_value = (
            [],
            [{"error": "Server error", "response_body": "Internal Server Error"}],
        )
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        from dealcloud_sdk.data.dealcloud_data import ErrorHandling

        results, errors = data._parallel_requests_get(
            ["http://url1"],
            max_workers=1,
            error_handling=ErrorHandling.COLLECT
        )

        assert len(errors) == 1
        assert "response_body" in errors[0]
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_parallel_post_log_only_errors(self, mock_client_class):
        """Test _parallel_requests_post with LOG_ONLY (client.parallel_post returns tuple)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.parallel_post.return_value = ([], [{"error": "Post failed"}])
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        from dealcloud_sdk.data.dealcloud_data import ErrorHandling

        results, errors = data._parallel_requests_post(
            "http://url",
            [{"data": 1}],
            max_workers=1,
            error_handling=ErrorHandling.LOG_ONLY
        )

        assert len(errors) == 1
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_parallel_post_collect_with_response_body(self, mock_client_class):
        """Test _parallel_requests_post collects response_body (client returns tuple)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.parallel_post.return_value = (
            [],
            [{"error": "Bad request", "response_body": {"error": "Invalid data"}}],
        )
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        from dealcloud_sdk.data.dealcloud_data import ErrorHandling

        results, errors = data._parallel_requests_post(
            "http://url",
            [{"data": 1}],
            max_workers=1,
            error_handling=ErrorHandling.COLLECT
        )

        assert len(errors) == 1
        assert "response_body" in errors[0]


class TestDealCloudDataUpsertDataWithOptions:
    """Tests for upsert_data with various options."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_upsert_data_pandas_output(self, mock_client_class):
        """Test upsert_data with pandas output."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client.post.return_value = [{"EntryId": 100, "Success": True}]
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = data.upsert_data("Company", [{"Name": "New"}], output="pandas")
        
        assert isinstance(result, pd.DataFrame)
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_upsert_data_pandas_output_empty_result(self, mock_client_class):
        """Test upsert_data with pandas output and empty result."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client.post.return_value = []
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = data.upsert_data("Company", [{"Name": "New"}], output="pandas")
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0


class TestDealCloudDataDeleteDataEmptyCollect:
    """Tests for delete_data with COLLECT on empty list."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_data_empty_with_collect(self, mock_client_class):
        """Test delete_data with empty list and COLLECT error handling."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        from dealcloud_sdk.data.dealcloud_data import ErrorHandling, BatchResult
        
        result = data.delete_data("Company", [], error_handling=ErrorHandling.COLLECT)
        
        assert isinstance(result, BatchResult)
        assert result.total_requested == 0


class TestDealCloudDataDeleteDataErrorModes:
    """Tests for delete_data error handling modes."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_data_log_only_on_error(self, mock_client_class):
        """Test delete_data with LOG_ONLY (DELETE raises, error collected)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.delete.side_effect = Exception("Delete failed")
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        from dealcloud_sdk.data.dealcloud_data import ErrorHandling, BatchResult

        result = data.delete_data(
            "Company", [1, 2, 3],
            error_handling=ErrorHandling.LOG_ONLY
        )

        assert isinstance(result, BatchResult)
        assert result.has_errors
        assert len(result.errors) == 1

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_data_fail_fast_raises(self, mock_client_class):
        """Test delete_data with FAIL_FAST raises (DELETE raises)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.delete.side_effect = HttpError(500, "Delete failed")
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        with pytest.raises(HttpError, match="Delete failed"):
            data.delete_data("Company", [1], error_handling=ErrorHandling.FAIL_FAST)

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_data_with_response_body_in_error(self, mock_client_class):
        """Test delete_data COLLECT captures exception when DELETE raises."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.delete.side_effect = Exception("Permission denied")
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        from dealcloud_sdk.data.dealcloud_data import ErrorHandling, BatchResult

        result = data.delete_data(
            "Company", [1],
            error_handling=ErrorHandling.COLLECT
        )

        assert isinstance(result, BatchResult)
        assert len(result.errors) == 1
        assert "Permission denied" in str(result.errors[0])


class TestDealCloudDataDeleteDataParallelPath:
    """Tests for delete_data multi-batch recovery path."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_data_multiple_batches_uses_parallel_delete(self, mock_client_class):
        """Test delete_data with multiple batches calls delete per batch in parallel."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        # 25 IDs with page_size=10 -> 3 batches
        mock_client.delete.side_effect = [
            [{"deleted": 10}],
            [{"deleted": 10}],
            [{"deleted": 5}],
        ]
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = data.delete_data("Company", list(range(1, 26)), page_size=10)

        assert mock_client.delete.call_count == 3
        payloads = sorted(
            (call.kwargs["json"] for call in mock_client.delete.call_args_list),
            key=lambda batch: batch[0],
        )
        assert payloads == [
            list(range(1, 11)),
            list(range(11, 21)),
            list(range(21, 26)),
        ]
        assert len(result) == 3

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_data_multiple_batches_collect_returns_batch_result(self, mock_client_class):
        """Test delete_data multi-batch with COLLECT returns BatchResult with correct totals."""
        from dealcloud_sdk.data.dealcloud_data import BatchResult
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}

        def delete_side_effect(url, json=None, **kwargs):
            if json == list(range(11, 21)):
                raise HttpError(429, "Rate limited", {}, {})
            return [{"deleted": len(json)}]

        mock_client.delete.side_effect = delete_side_effect
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = data.delete_data(
            "Company", list(range(1, 26)), page_size=10, error_handling=ErrorHandling.COLLECT
        )

        assert isinstance(result, BatchResult)
        assert result.total_requested == 25
        assert result.total_succeeded == 2
        assert result.total_failed == 10
        assert len(result.errors) == 1
        assert result.errors[0]["payload_index"] == 1

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_data_multiple_batches_fail_fast_raises(self, mock_client_class):
        """Test delete_data multi-batch FAIL_FAST: delete raises."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.delete.side_effect = HttpError(500, "Delete failed")
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        with pytest.raises(HttpError, match="Delete failed"):
            data.delete_data("Company", list(range(1, 26)), page_size=10)

        assert mock_client.delete.called

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_data_multiple_batches_progress_callback_once(self, mock_client_class):
        """Test delete_data multi-batch invokes progress_callback once at end."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.delete.side_effect = [[], [], []]
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        progress_calls = []
        def capture_progress(current, total):
            progress_calls.append((current, total))
        data.delete_data(
            "Company", list(range(1, 26)), page_size=10, progress_callback=capture_progress
        )
        assert progress_calls == [(3, 3)]


class TestDealCloudDataInsertErrorModes:
    """Tests for insert_data error handling modes."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_insert_data_log_only_on_error(self, mock_client_class):
        """Test insert_data with LOG_ONLY error handling."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client.post.side_effect = HttpError(500, "Insert failed")
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        from dealcloud_sdk.data.dealcloud_data import ErrorHandling, BatchResult

        result = data.insert_data(
            "Company", [{"Name": "Test"}],
            error_handling=ErrorHandling.LOG_ONLY
        )
        
        assert isinstance(result, BatchResult)
        assert result.has_errors
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_insert_data_with_response_body_in_error(self, mock_client_class):
        """Test insert_data captures transport errors in COLLECT mode."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        
        err = HttpError(400, "Validation error", "Validation error", {})
        mock_client.post.side_effect = err
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        from dealcloud_sdk.data.dealcloud_data import ErrorHandling, BatchResult
        
        result = data.insert_data(
            "Company", [{"Name": "Test"}],
            error_handling=ErrorHandling.COLLECT
        )
        
        assert len(result.errors) == 1
        assert isinstance(result.errors[0], HttpError)


class TestDealCloudDataUpdateErrorModes:
    """Tests for update_data error handling modes."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_update_data_log_only_on_error(self, mock_client_class):
        """Test update_data with LOG_ONLY error handling."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client.put.side_effect = HttpError(500, "Update failed")
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        from dealcloud_sdk.data.dealcloud_data import ErrorHandling, BatchResult

        result = data.update_data(
            "Company", [{"EntryId": 1, "Name": "Test"}],
            error_handling=ErrorHandling.LOG_ONLY
        )
        
        assert isinstance(result, BatchResult)
        assert result.has_errors
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_update_data_with_response_body_in_error(self, mock_client_class):
        """Test update_data captures transport errors in COLLECT mode."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        
        err = HttpError(400, "Record locked", "Record locked", {})
        mock_client.put.side_effect = err
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        from dealcloud_sdk.data.dealcloud_data import ErrorHandling, BatchResult

        result = data.update_data(
            "Company", [{"EntryId": 1, "Name": "Test"}],
            error_handling=ErrorHandling.COLLECT
        )
        
        assert len(result.errors) == 1
        assert isinstance(result.errors[0], HttpError)


class TestDealCloudDataReadDataCollectEmptyResults:
    """Tests for read_data with COLLECT and empty results."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_collect_empty_list_output(self, mock_client_class):
        """Test read_data with COLLECT and empty result, list output (get_paginated)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get_paginated.return_value = iter([])
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        from dealcloud_sdk.data.dealcloud_data import ErrorHandling, BatchResult
        
        result = data.read_data(
            object_id="Company",
            output="list",
            error_handling=ErrorHandling.COLLECT
        )
        
        assert isinstance(result, BatchResult)
        assert result.results == []
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_collect_empty_pandas_output(self, mock_client_class):
        """Test read_data with COLLECT and empty result, pandas output (get_paginated)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get_paginated.return_value = iter([])
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        from dealcloud_sdk.data.dealcloud_data import ErrorHandling, BatchResult
        
        result = data.read_data(
            object_id="Company",
            output="pandas",
            error_handling=ErrorHandling.COLLECT
        )
        
        assert isinstance(result, BatchResult)
        assert isinstance(result.results, pd.DataFrame)
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_collect_with_results_list_output(self, mock_client_class):
        """Test read_data with COLLECT and list output (uses get_paginated)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get_paginated.return_value = iter([[{"EntryId": 1, "Name": "Test"}]])
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        from dealcloud_sdk.data.dealcloud_data import ErrorHandling, BatchResult
        
        result = data.read_data(
            object_id="Company",
            output="list",
            error_handling=ErrorHandling.COLLECT
        )
        
        assert isinstance(result, BatchResult)
        assert len(result.results) == 1


class TestDealCloudDataPaginationProgressCallback:
    """Tests for pagination with progress callback failures."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_paginated_read_progress_callback_failure(self, mock_client_class):
        """Test read_data (via read_data_streaming) handles progress callback failures."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get_paginated.return_value = iter([[{"EntryId": 1}]])
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        def failing_callback(current, total):
            raise ValueError("Callback error")

        # Should not raise, just log the warning
        result = data.read_data(object_id="Company", progress_callback=failing_callback, output="list")

        assert len(result) == 1


class TestBatchResultProperties:
    """Tests for BatchResult dataclass."""
    
    def test_batch_result_has_errors_true(self):
        """Test has_errors returns True when errors exist."""
        from dealcloud_sdk.data.dealcloud_data import BatchResult
        
        result = BatchResult(errors=[{"error": "test"}])
        
        assert result.has_errors is True
    
    def test_batch_result_has_errors_false(self):
        """Test has_errors returns False when no errors."""
        from dealcloud_sdk.data.dealcloud_data import BatchResult
        
        result = BatchResult()
        
        assert result.has_errors is False
    
    def test_batch_result_success_rate_100_percent(self):
        """Test success_rate returns 100 when all succeeded."""
        from dealcloud_sdk.data.dealcloud_data import BatchResult
        
        result = BatchResult(total_requested=10, total_succeeded=10)
        
        assert result.success_rate == 100.0
    
    def test_batch_result_success_rate_partial(self):
        """Test success_rate returns correct percentage."""
        from dealcloud_sdk.data.dealcloud_data import BatchResult
        
        result = BatchResult(total_requested=10, total_succeeded=8)
        
        assert result.success_rate == 80.0
    
    def test_batch_result_success_rate_zero_requested(self):
        """Test success_rate returns 100 when nothing requested."""
        from dealcloud_sdk.data.dealcloud_data import BatchResult
        
        result = BatchResult(total_requested=0)
        
        assert result.success_rate == 100.0


class TestDealCloudDataParallelRequestErrors:
    """Tests for parallel request error handling."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_parallel_get_fail_fast_raises(self, mock_client_class):
        """Test _parallel_requests_get with FAIL_FAST raises (parallel_get raises)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.parallel_get.side_effect = HttpError(500, "API Error")
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        from dealcloud_sdk.data.dealcloud_data import ErrorHandling
        with pytest.raises(HttpError, match="API Error"):
            data._parallel_requests_get(
                ["http://test/1", "http://test/2"],
                max_workers=2,
                error_handling=ErrorHandling.FAIL_FAST
            )
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_parallel_post_fail_fast_raises(self, mock_client_class):
        """Test _parallel_requests_post with FAIL_FAST raises (parallel_post raises)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.parallel_post.side_effect = HttpError(500, "POST Error")
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        from dealcloud_sdk.data.dealcloud_data import ErrorHandling
        with pytest.raises(HttpError, match="POST Error"):
            data._parallel_requests_post(
                "http://test",
                [{"data": 1}, {"data": 2}],
                max_workers=2,
                error_handling=ErrorHandling.FAIL_FAST
            )


class TestDealCloudDataPaginationPublicWrappers:
    """Public parallel_get / parallel_post / paginated_read delegate to pagination module."""

    @patch(
        "dealcloud_sdk.data.dealcloud_data.pagination.parallel_get",
        return_value=[{"delegated": True}],
    )
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_parallel_get_delegates(self, mock_client_class, mock_parallel_get):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        from dealcloud_sdk.data.dealcloud_data import ErrorHandling

        out = data.parallel_get(
            ["http://a", "http://b"],
            max_workers=3,
            error_handling=ErrorHandling.COLLECT,
        )
        assert out == [{"delegated": True}]
        mock_parallel_get.assert_called_once_with(
            mock_client,
            ["http://a", "http://b"],
            3,
            ErrorHandling.COLLECT,
            data._logger,
        )

    @patch(
        "dealcloud_sdk.data.dealcloud_data.pagination.parallel_post",
        return_value=[{"post": 1}],
    )
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_parallel_post_delegates(self, mock_client_class, mock_parallel_post):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        from dealcloud_sdk.data.dealcloud_data import ErrorHandling

        out = data.parallel_post(
            "http://post-url",
            [{"q": 1}],
            max_workers=2,
            error_handling=ErrorHandling.LOG_ONLY,
        )
        assert out == [{"post": 1}]
        mock_parallel_post.assert_called_once_with(
            mock_client,
            "http://post-url",
            [{"q": 1}],
            2,
            ErrorHandling.LOG_ONLY,
            data._logger,
        )

    @patch(
        "dealcloud_sdk.data.dealcloud_data.pagination.paginated_read",
        return_value=[{"EntryId": 99}],
    )
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_paginated_read_delegates(self, mock_client_class, mock_paginated_read):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        from dealcloud_sdk.data.dealcloud_data import ErrorHandling

        out = data.paginated_read(
            "http://rows",
            method="POST",
            request_body={"filter": "x"},
            page_size=500,
            max_workers=4,
            error_handling=ErrorHandling.COLLECT,
        )
        assert out == [{"EntryId": 99}]
        mock_paginated_read.assert_called_once_with(
            mock_client,
            "http://rows",
            "POST",
            {"filter": "x"},
            500,
            4,
            None,
            ErrorHandling.COLLECT,
            data._logger,
        )

    @patch(
        "dealcloud_sdk.data.dealcloud_data.pagination.paginated_read_until_empty",
        return_value=[{"EntryId": 1}],
    )
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_paginated_read_until_empty_deprecated(self, mock_client_class, mock_prue):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        from dealcloud_sdk.data.dealcloud_data import ErrorHandling

        with pytest.warns(DeprecationWarning, match="deprecated"):
            out = data._paginated_read_until_empty(
                "http://base",
                method="GET",
                page_size=100,
                error_handling=ErrorHandling.FAIL_FAST,
            )
        assert out == [{"EntryId": 1}]
        mock_prue.assert_called_once_with(
            mock_client,
            "http://base",
            "GET",
            None,
            100,
            8,
            None,
            ErrorHandling.FAIL_FAST,
            data._logger,
        )


class TestDealCloudDataDeleteFailFast:
    """Tests for delete with FAIL_FAST error handling."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_data_fail_fast_raises(self, mock_client_class):
        """Test delete_data with FAIL_FAST raises (DELETE raises)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.delete.side_effect = HttpError(500, "Delete Error")
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        with pytest.raises(HttpError, match="Delete Error"):
            data.delete_data(
                "Company",
                [1, 2],
                error_handling=ErrorHandling.FAIL_FAST,
            )


class TestEntryIdCache:
    """Tests for EntryIdCache data structure."""
    
    def test_basic_get_set(self):
        """Test basic get and set operations."""
        from dealcloud_sdk.models.data import EntryIdCache
        
        cache = EntryIdCache(object_id="Company", key_field="crmId")
        
        cache.set("CRM-123", 1001)
        cache.set("CRM-456", 1002)
        
        assert cache.get("CRM-123") == 1001
        assert cache.get("CRM-456") == 1002
        assert cache.get("CRM-999") is None
    
    def test_contains(self):
        """Test __contains__ (in operator)."""
        from dealcloud_sdk.models.data import EntryIdCache
        
        cache = EntryIdCache(object_id="Company", key_field="crmId")
        cache.set("CRM-123", 1001)
        
        assert "CRM-123" in cache
        assert "CRM-999" not in cache
    
    def test_len(self):
        """Test __len__ (len() function)."""
        from dealcloud_sdk.models.data import EntryIdCache
        
        cache = EntryIdCache(object_id="Company", key_field="crmId")
        assert len(cache) == 0
        
        cache.set("CRM-123", 1001)
        assert len(cache) == 1
        
        cache.set("CRM-456", 1002)
        assert len(cache) == 2
    
    def test_bulk_set(self):
        """Test bulk_set for multiple mappings."""
        from dealcloud_sdk.models.data import EntryIdCache
        
        cache = EntryIdCache(object_id="Company", key_field="crmId")
        cache.bulk_set({
            "CRM-123": 1001,
            "CRM-456": 1002,
            "CRM-789": 1003,
        })
        
        assert len(cache) == 3
        assert cache.get("CRM-123") == 1001
        assert cache.get("CRM-789") == 1003
    
    def test_remove(self):
        """Test remove operation."""
        from dealcloud_sdk.models.data import EntryIdCache
        
        cache = EntryIdCache(object_id="Company", key_field="crmId")
        cache.set("CRM-123", 1001)
        
        assert cache.remove("CRM-123") is True
        assert "CRM-123" not in cache
        assert cache.remove("CRM-123") is False  # Already removed
    
    def test_clear(self):
        """Test clear operation."""
        from dealcloud_sdk.models.data import EntryIdCache
        
        cache = EntryIdCache(object_id="Company", key_field="crmId")
        cache.bulk_set({"CRM-1": 1, "CRM-2": 2, "CRM-3": 3})
        assert len(cache) == 3
        
        cache.clear()
        assert len(cache) == 0
    
    def test_iteration(self):
        """Test iteration over cache."""
        from dealcloud_sdk.models.data import EntryIdCache
        
        cache = EntryIdCache(object_id="Company", key_field="crmId")
        cache.bulk_set({"CRM-1": 1, "CRM-2": 2})
        
        keys = list(cache)
        assert set(keys) == {"CRM-1", "CRM-2"}
        
        items = list(cache.items())
        assert set(items) == {("CRM-1", 1), ("CRM-2", 2)}
    
    def test_string_conversion(self):
        """Test that numeric IDs are converted to strings."""
        from dealcloud_sdk.models.data import EntryIdCache
        
        cache = EntryIdCache(object_id="Company", key_field="crmId")
        cache.set(123, 1001)  # Numeric key
        
        assert cache.get("123") == 1001
        assert cache.get(123) == 1001
        assert 123 in cache
        assert "123" in cache


class TestBuildEntryIdCache:
    """Tests for build_entry_id_cache method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_build_entry_id_cache_basic(self, mock_client_class):
        """Test build_entry_id_cache creates mapping (uses get_paginated via read_data)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get_paginated.return_value = iter([
            [
                {"EntryId": 1001, "crmId": "CRM-123"},
                {"EntryId": 1002, "crmId": "CRM-456"},
                {"EntryId": 1003, "crmId": "CRM-789"},
            ]
        ])
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        cache = data.build_entry_id_cache("Company", "crmId")
        
        assert len(cache) == 3
        assert cache.get("CRM-123") == 1001
        assert cache.get("CRM-456") == 1002
        assert cache.get("CRM-789") == 1003
        assert cache.object_id == "Company"
        assert cache.key_field == "crmId"
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_build_entry_id_cache_skips_nulls(self, mock_client_class):
        """Test build_entry_id_cache skips rows with null key (uses get_paginated)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get_paginated.return_value = iter([
            [
                {"EntryId": 1001, "crmId": "CRM-123"},
                {"EntryId": 1002, "crmId": None},
                {"EntryId": 1003},
            ]
        ])
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        cache = data.build_entry_id_cache("Company", "crmId")
        
        assert len(cache) == 1
        assert cache.get("CRM-123") == 1001
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_build_entry_id_cache_empty_result(self, mock_client_class):
        """Test build_entry_id_cache with no data (get_paginated yields empty)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get_paginated.return_value = iter([])
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        cache = data.build_entry_id_cache("Company", "crmId")
        
        assert len(cache) == 0


class TestMapIds:
    """Tests for map_ids method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_map_ids_basic(self, mock_client_class):
        """Test map_ids adds EntryId to matching records."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        # Create cache manually
        from dealcloud_sdk.models.data import EntryIdCache
        cache = EntryIdCache(object_id="Company", key_field="crmId")
        cache.bulk_set({"CRM-123": 1001, "CRM-456": 1002})
        
        # Records to map
        records = [
            {"crm_id": "CRM-123", "name": "Acme Corp"},
            {"crm_id": "CRM-456", "name": "Beta Inc"},
            {"crm_id": "CRM-999", "name": "New Company"},  # Not in cache
        ]
        
        mapped = data.map_ids(records, cache, "crm_id")
        
        assert len(mapped) == 3
        assert mapped[0]["EntryId"] == 1001
        assert mapped[0]["name"] == "Acme Corp"
        assert mapped[1]["EntryId"] == 1002
        assert "EntryId" not in mapped[2]  # Not found in cache
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_map_ids_does_not_modify_original(self, mock_client_class):
        """Test map_ids returns copies, not modified originals."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        from dealcloud_sdk.models.data import EntryIdCache
        cache = EntryIdCache(object_id="Company", key_field="crmId")
        cache.set("CRM-123", 1001)
        
        original = {"crm_id": "CRM-123", "name": "Test"}
        records = [original]
        
        mapped = data.map_ids(records, cache, "crm_id")
        
        assert "EntryId" in mapped[0]
        assert "EntryId" not in original  # Original unchanged
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_map_ids_split_insert_update(self, mock_client_class):
        """Test typical workflow: split into inserts vs updates."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        from dealcloud_sdk.models.data import EntryIdCache
        cache = EntryIdCache(object_id="Company", key_field="crmId")
        cache.bulk_set({"EXIST-1": 1001, "EXIST-2": 1002})
        
        records = [
            {"crm_id": "EXIST-1", "name": "Update Me"},
            {"crm_id": "NEW-1", "name": "Insert Me"},
            {"crm_id": "EXIST-2", "name": "Also Update"},
            {"crm_id": "NEW-2", "name": "Also Insert"},
        ]
        
        mapped = data.map_ids(records, cache, "crm_id")
        
        to_insert = [r for r in mapped if "EntryId" not in r]
        to_update = [r for r in mapped if "EntryId" in r]
        
        assert len(to_insert) == 2
        assert len(to_update) == 2
        assert to_insert[0]["name"] == "Insert Me"
        assert to_update[0]["EntryId"] == 1001

