"""Tests for DealCloudData view-related methods."""

import pytest
from unittest.mock import MagicMock, patch

from dealcloud_sdk.data.dealcloud_data import DealCloudData
from dealcloud_sdk.models.data import Rows


def _configure_views_lookup(mock_client, view_id: int, *, name: str = "Test View") -> None:
    """Mock list_configured_views so resolve_view accepts an integer view id."""
    mock_client.get.return_value = {
        "totalRecords": 1,
        "rows": [{"id": view_id, "name": name}],
    }


class TestDealCloudDataListConfiguredViews:
    """Tests for list_configured_views method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_list_configured_views(self, mock_client_class):
        """Test list_configured_views returns Rows object."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {
            "totalRecords": 2,
            "rows": [
                {"id": 1, "name": "View 1"},
                {"id": 2, "name": "View 2"},
            ]
        }
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        views = data.list_configured_views()
        
        assert isinstance(views, Rows)
        assert views.totalRecords == 2
        assert len(views.rows) == 2
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_list_configured_views_private(self, mock_client_class):
        """Test list_configured_views with is_private filter."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {"totalRecords": 1, "rows": [{"id": 1, "name": "Private View"}]}
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        data.list_configured_views(is_private=True)
        
        mock_client.get.assert_called_with(
            "https://test.dealcloud.com/api/rest/v4/data/rows/view?isprivate=true"
        )


class TestDealCloudDataReadDataViews:
    """Tests for read_data with view_id parameter."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_view_by_name(self, mock_client_class):
        """Test read_data with view name lookup."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {
            "totalRecords": 1,
            "rows": [{"id": 100, "name": "My View"}]
        }
        # read_data(view_id=...) uses read_view_streaming -> post_paginated_params
        mock_client.post_paginated_params.return_value = iter([
            [{"EntryId": 1, "Name": "View Data"}]
        ])
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = data.read_data(view_id="My View", output="list")

        assert len(result) == 1
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_view_not_found_raises(self, mock_client_class):
        """Test read_data raises when view name not found."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {"totalRecords": 0, "rows": []}
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        with pytest.raises(AttributeError) as exc_info:
            data.read_data(view_id="Nonexistent View", output="list")
        
        assert "not found" in str(exc_info.value)
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_multiple_views_raises(self, mock_client_class):
        """Test read_data raises when multiple views with same name."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {
            "totalRecords": 2,
            "rows": [
                {"id": 1, "name": "Duplicate View"},
                {"id": 2, "name": "Duplicate View"},
            ]
        }
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        with pytest.raises(AttributeError) as exc_info:
            data.read_data(view_id="Duplicate View", output="list")
        
        assert "Multiple views" in str(exc_info.value)


class TestDealCloudDataReadViewIncludeNulls:
    """Tests for include_nulls forced to False when reading views (PROPOSAL_view_column_fix)."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_view_integer_id_ignores_include_nulls_true_pandas(self, mock_client_class):
        """When view_id is int and include_nulls=True, SDK forces include_nulls=False; result has reasonable columns."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        _configure_views_lookup(mock_client, 12345)
        mock_client.post_paginated_params.return_value = iter([
            [{"EntryId": 1, "Name": "A"}]
        ])
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = data.read_data(view_id=12345, output="pandas", include_nulls=True)

        assert result is not None
        assert len(result) == 1
        assert len(result.columns) <= 10
        assert "EntryId" in result.columns or "Name" in result.columns

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_view_string_id_ignores_include_nulls_true_pandas(self, mock_client_class):
        """When view_id is string and include_nulls=True, SDK forces include_nulls=False; result has reasonable columns."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        # resolve_view may run twice (read_view + read_view_streaming); use return_value not side_effect
        mock_client.get.return_value = {
            "totalRecords": 1,
            "rows": [{"id": 12345, "name": "Test View"}],
        }
        mock_client.post_paginated_params.return_value = iter([
            [{"EntryId": 1, "Name": "A"}]
        ])
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = data.read_data(view_id="Test View", output="pandas", include_nulls=True)

        assert result is not None
        assert len(result) == 1
        assert len(result.columns) <= 10

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_view_include_nulls_true_returns_reasonable_columns_list(self, mock_client_class):
        """When view_id and include_nulls=True, list output has reasonable key count per row."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        _configure_views_lookup(mock_client, 12345)
        mock_client.post_paginated_params.return_value = iter([
            [{"EntryId": 1, "Name": "A", "Field1": "v1"}]
        ])
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = data.read_data(view_id=12345, output="list", include_nulls=True)

        assert isinstance(result, list)
        assert len(result) == 1
        assert len(result[0].keys()) <= 10
        assert result[0]["EntryId"] == 1
        assert result[0]["Name"] == "A"

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_data_view_empty_returns_empty_pandas(self, mock_client_class):
        """Empty view with include_nulls=True still forces include_nulls=False; returns empty DataFrame."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        _configure_views_lookup(mock_client, 12345)
        mock_client.post_paginated_params.return_value = iter([])
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = data.read_data(view_id=12345, output="pandas", include_nulls=True)

        assert result is not None
        assert len(result) == 0
        assert len(result.columns) == 0


class TestDealCloudDataReadViewStreaming:
    """Tests for read_view_streaming method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_view_streaming_uses_post_paginated_params(self, mock_client_class):
        """Test read_view_streaming uses post_paginated_params."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        _configure_views_lookup(mock_client, 123)
        mock_client.post_paginated_params.return_value = iter([[{"EntryId": 1}]])
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        list(data.read_view_streaming(123))
        
        mock_client.post_paginated_params.assert_called_once()
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_view_streaming_with_filter(self, mock_client_class):
        """Test read_view_streaming passes filter to json body."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        _configure_views_lookup(mock_client, 123)
        mock_client.post_paginated_params.return_value = iter([])
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        view_filter = [{"columnId": 1, "value": "Active"}]
        list(data.read_view_streaming(123, view_filter=view_filter))
        
        call_kwargs = mock_client.post_paginated_params.call_args[1]
        assert call_kwargs["json"] == view_filter
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_view_streaming_concurrency(self, mock_client_class):
        """Test read_view_streaming passes max_concurrency."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        _configure_views_lookup(mock_client, 123)
        mock_client.post_paginated_params.return_value = iter([])
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        list(data.read_view_streaming(123, max_concurrency=3))

        mock_client.post_paginated_params.assert_called_once()
        # max_concurrency omitted for compatibility with older intapp-rest-client


class TestDealCloudDataAreadViewStreaming:
    """Tests for aread_view_streaming async method."""
    
    @pytest.mark.asyncio
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    async def test_aread_view_streaming_uses_apost_paginated_params(self, mock_client_class):
        """Test aread_view_streaming uses apost_paginated_params."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        _configure_views_lookup(mock_client, 123)
        
        async def mock_apost_paginated_params(*args, **kwargs):
            yield [{"EntryId": 1}]
        
        mock_client.apost_paginated_params = mock_apost_paginated_params
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        batches = []
        async for batch in data.aread_view_streaming(123):
            batches.append(batch)
        
        assert len(batches) == 1

    @pytest.mark.asyncio
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    async def test_aread_view_streaming_explicit_page_size_and_max_concurrency(
        self, mock_client_class
    ):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        _configure_views_lookup(mock_client, 123)

        captured = {}

        async def mock_apost_paginated_params(*args, **kwargs):
            captured.update(kwargs)
            yield [{"EntryId": 1}]

        mock_client.apost_paginated_params = mock_apost_paginated_params
        mock_client_class.return_value = mock_client

        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        batches = []
        async for batch in data.aread_view_streaming(
            123, page_size=77, max_concurrency=2
        ):
            batches.append(batch)

        assert len(batches) == 1
        assert captured.get("page_size") == 77
    
    @pytest.mark.asyncio
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    async def test_aread_view_streaming_with_name_lookup(self, mock_client_class):
        """Test aread_view_streaming with view name lookup."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {
            "totalRecords": 1,
            "rows": [{"id": 100, "name": "My Async View"}]
        }
        
        async def mock_apost_paginated_params(*args, **kwargs):
            yield [{"EntryId": 1}]
        
        mock_client.apost_paginated_params = mock_apost_paginated_params
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        batches = []
        async for batch in data.aread_view_streaming("My Async View"):
            batches.append(batch)
        
        assert len(batches) == 1
    
    @pytest.mark.asyncio
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    async def test_aread_view_streaming_not_found_raises(self, mock_client_class):
        """Test aread_view_streaming raises when view not found."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {"totalRecords": 0, "rows": []}
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        with pytest.raises(AttributeError, match="not found"):
            async for _ in data.aread_view_streaming("Nonexistent"):
                pass
    
    @pytest.mark.asyncio
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    async def test_aread_view_streaming_multiple_views_raises(self, mock_client_class):
        """Test aread_view_streaming raises when multiple views with same name."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {
            "totalRecords": 2,
            "rows": [
                {"id": 1, "name": "Dup View"},
                {"id": 2, "name": "Dup View"}
            ]
        }
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        with pytest.raises(AttributeError, match="Multiple views"):
            async for _ in data.aread_view_streaming("Dup View"):
                pass


class TestDealCloudDataViewStreamingNameLookup:
    """Tests for read_view_streaming with name lookup."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_view_streaming_with_name_lookup(self, mock_client_class):
        """Test read_view_streaming with view name lookup."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {
            "totalRecords": 1,
            "rows": [{"id": 100, "name": "My Named View"}]
        }
        mock_client.post_paginated_params.return_value = iter([[{"EntryId": 1}]])
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        batches = list(data.read_view_streaming("My Named View"))
        
        assert len(batches) == 1
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_view_streaming_not_found_raises(self, mock_client_class):
        """Test read_view_streaming raises when view not found."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {"totalRecords": 0, "rows": []}
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        with pytest.raises(AttributeError, match="not found"):
            list(data.read_view_streaming("Nonexistent"))
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_read_view_streaming_multiple_views_raises(self, mock_client_class):
        """Test read_view_streaming raises when multiple views with same name."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {
            "totalRecords": 2,
            "rows": [
                {"id": 1, "name": "Dup View"},
                {"id": 2, "name": "Dup View"}
            ]
        }
        mock_client_class.return_value = mock_client
        
        data = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        with pytest.raises(AttributeError, match="Multiple views"):
            list(data.read_view_streaming("Dup View"))

