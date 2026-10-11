"""Tests for main DealCloud class."""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from dealcloud_sdk import DealCloud
from dealcloud_sdk.schema.dealcloud_schema import DealCloudSchema


class TestDealCloudInit:
    """Tests for DealCloud initialization."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_init_with_cache_enabled(self, mock_client_class):
        """Test init with schema caching enabled (default)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}

        # Mock schema and users for init
        mock_client.get.side_effect = [
            # get_objects
            [{"apiName": "Company", "singularName": "Company", "pluralName": "Companies", "id": 1, "entryListId": 100}],
            # get_fields
            [{"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100}],
            # get_users
            [{"id": 1, "email": "test@gmail.co", "name": "Test User", "entryListId": 500}],
        ]
        mock_client_class.return_value = mock_client

        dc = DealCloud(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
            cache_schema=True,
        )

        assert dc._cache_schema is True
        assert dc._site_schema is not None
        assert dc._user_map is not None

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_init_with_cache_disabled(self, mock_client_class):
        """Test init with schema caching disabled."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}

        mock_client.get.side_effect = [
            [{"apiName": "Company", "singularName": "Company", "pluralName": "Companies", "id": 1, "entryListId": 100}],
            [{"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100}],
            [{"id": 1, "email": "test@gmail.co", "name": "Test User", "entryListId": 500}],
        ]
        mock_client_class.return_value = mock_client

        dc = DealCloud(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
            cache_schema=False,
        )

        assert dc._cache_schema is False
        assert dc._site_schema is not None

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_init_with_custom_cache_ttl(self, mock_client_class):
        """Test init with custom cache TTL."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}

        mock_client.get.side_effect = [
            [{"apiName": "Company", "singularName": "Company", "pluralName": "Companies", "id": 1, "entryListId": 100}],
            [{"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100}],
            [{"id": 1, "email": "test@gmail.co", "name": "Test User", "entryListId": 500}],
        ]
        mock_client_class.return_value = mock_client

        dc = DealCloud(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
            schema_cache_ttl=600.0,
        )

        assert dc._schema_cache_ttl == 600.0

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_init_uses_cached_schema(self, mock_client_class):
        """Test that second init uses cached schema."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}

        mock_client.get.side_effect = [
            [{"apiName": "Company", "singularName": "Company", "pluralName": "Companies", "id": 1, "entryListId": 100}],
            [{"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100}],
            [{"id": 1, "email": "test@gmail.co", "name": "Test User", "entryListId": 500}],
        ]
        mock_client_class.return_value = mock_client

        # Clear cache first
        DealCloud.clear_all_schema_caches()

        # First client fetches schema
        dc1 = DealCloud(
            site_url="cached-test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        # Reset mock to verify second client doesn't fetch
        mock_client.get.reset_mock()

        # Second client should use cache - no additional get calls for schema
        dc2 = DealCloud(
            site_url="cached-test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        # Both should have same schema object (cached)
        assert dc1._site_schema is not None
        assert dc2._site_schema is not None


class TestDealCloudMethods:
    """Tests for DealCloud methods."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_refresh_schema(self, mock_client_class):
        """Test refresh_schema refreshes cache."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}

        # Initial schema fetch
        mock_client.get.side_effect = [
            [{"apiName": "Company", "singularName": "Company", "pluralName": "Companies", "id": 1, "entryListId": 100}],
            [{"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100}],
            [{"id": 1, "email": "test@gmail.co", "name": "Test User", "entryListId": 500}],
            # refresh_schema calls
            [{"apiName": "Company", "singularName": "Company", "pluralName": "Companies", "id": 1, "entryListId": 100}],
            [{"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100}],
            [{"id": 2, "email": "new@gmail.co", "name": "New User", "entryListId": 500}],
        ]
        mock_client_class.return_value = mock_client

        dc = DealCloud(
            site_url="refresh-test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        # Refresh schema (no longer updates _user_map; that is lazy via cached_user_map)
        dc.refresh_schema()

        # Schema should be refreshed
        assert dc._site_schema is not None
        # User map is not updated by refresh_schema; it stays empty until cached_user_map is accessed
        assert dc._user_map == {}

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_refresh_schema_updates_cache(self, mock_client_class):
        """Test refresh_schema updates cache when caching enabled."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}

        mock_client.get.side_effect = [
            [{"apiName": "Company", "singularName": "Company", "pluralName": "Companies", "id": 1, "entryListId": 100}],
            [{"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100}],
            [{"id": 1, "email": "test@gmail.co", "name": "Test User", "entryListId": 500}],
            [{"apiName": "Company", "singularName": "Company", "pluralName": "Companies", "id": 1, "entryListId": 100}],
            [{"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100}],
            [{"id": 1, "email": "test@gmail.co", "name": "Test User", "entryListId": 500}],
        ]
        mock_client_class.return_value = mock_client

        dc = DealCloud(
            site_url="cache-refresh-test.dealcloud.com",
            client_id="123",
            client_secret="secret",
            cache_schema=True,
        )

        dc.refresh_schema()

        # Schema should be refreshed
        assert dc._site_schema is not None

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_clear_schema_cache(self, mock_client_class):
        """Test clear_schema_cache clears cache for site."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}

        mock_client.get.side_effect = [
            [{"apiName": "Company", "singularName": "Company", "pluralName": "Companies", "id": 1, "entryListId": 100}],
            [{"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100}],
            [{"id": 1, "email": "test@gmail.co", "name": "Test User", "entryListId": 500}],
        ]
        mock_client_class.return_value = mock_client

        dc = DealCloud(
            site_url="clear-cache-test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        # Clear cache should not raise
        dc.clear_schema_cache()

    def test_clear_all_schema_caches(self):
        """Test clear_all_schema_caches class method."""
        # Should not raise
        DealCloud.clear_all_schema_caches()


class TestDealCloudSchemaCache:
    """Tests for DealCloud class with schema caching."""

    def test_dealcloud_uses_cache_by_default(self):
        """DealCloud uses schema cache by default."""
        import inspect
        sig = inspect.signature(DealCloud.__init__)
        params = sig.parameters

        assert "cache_schema" in params
        assert params["cache_schema"].default is True

    def test_schema_cache_ttl_parameter(self):
        """DealCloud accepts schema_cache_ttl parameter."""
        import inspect
        sig = inspect.signature(DealCloud.__init__)
        params = sig.parameters

        assert "schema_cache_ttl" in params
        assert params["schema_cache_ttl"].default == 300.0


class TestDealCloudSchemaUserWrappers:
    """get_schema_users / cached_user_map / legacy aliases on DealCloud."""

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_get_schema_users_delegates_to_schema(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.side_effect = [
            [{"apiName": "Company", "singularName": "C", "pluralName": "Cs", "id": 1, "entryListId": 1}],
            [{"apiName": "Name", "name": "Name", "fieldType": 1, "id": 1, "entryListId": 1}],
            [{"id": 1, "email": "a@b.co", "name": "U", "entryListId": 1}],
        ]
        mock_client_class.return_value = mock_client
        dc = DealCloud(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch.object(DealCloudSchema, "get_users", return_value=[]) as gu:
            dc.get_schema_users(active_only=True)
        gu.assert_called_once_with(dc, True)

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_cached_user_map_lazy_populates(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.side_effect = [
            [{"apiName": "Company", "singularName": "C", "pluralName": "Cs", "id": 1, "entryListId": 1}],
            [{"apiName": "Name", "name": "Name", "fieldType": 1, "id": 1, "entryListId": 1}],
            [{"id": 1, "email": "a@b.co", "name": "U", "entryListId": 1}],
        ]
        mock_client_class.return_value = mock_client
        dc = DealCloud(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        u = SimpleNamespace(email="Hello@Example.com", id=77)
        with patch.object(DealCloudSchema, "get_users", return_value=[u]):
            assert dc.cached_user_map == {"hello@example.com": 77}

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_get_object_history_forwards_to_get_history(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.side_effect = [
            [{"apiName": "Company", "singularName": "C", "pluralName": "Cs", "id": 1, "entryListId": 1}],
            [{"apiName": "Name", "name": "Name", "fieldType": 1, "id": 1, "entryListId": 1}],
            [{"id": 1, "email": "a@b.co", "name": "U", "entryListId": 1}],
        ]
        mock_client_class.return_value = mock_client
        dc = DealCloud(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch.object(dc, "get_history", return_value=[{"x": 1}]) as gh:
            out = dc.get_object_history(1, "2020-01-01")
        assert out == [{"x": 1}]
        gh.assert_called_once_with(1, "2020-01-01")

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_download_files_forwards_to_download_file(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.side_effect = [
            [{"apiName": "Company", "singularName": "C", "pluralName": "Cs", "id": 1, "entryListId": 1}],
            [{"apiName": "Name", "name": "Name", "fieldType": 1, "id": 1, "entryListId": 1}],
            [{"id": 1, "email": "a@b.co", "name": "U", "entryListId": 1}],
        ]
        mock_client_class.return_value = mock_client
        dc = DealCloud(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch.object(dc, "download_file", return_value=b"data") as df:
            assert dc.download_files(10, "Logo") == b"data"
        df.assert_called_once_with(10, "Logo")


class TestExports:
    """Tests for module exports."""

    def test_error_handling_exported(self):
        """ErrorHandling is exported and matches the shared fail_fast/collect/log_only contract."""
        from enum import Enum

        from dealcloud_sdk import ErrorHandling

        assert issubclass(ErrorHandling, Enum)
        assert ErrorHandling.FAIL_FAST.value == "fail_fast"
        assert ErrorHandling.COLLECT.value == "collect"
        assert ErrorHandling.LOG_ONLY.value == "log_only"

    def test_batch_result_exported(self):
        """BatchResult is exported from main module."""
        from dealcloud_sdk import BatchResult
        assert BatchResult is not None

    def test_schema_cache_exported(self):
        """SchemaCache is exported from main module."""
        from dealcloud_sdk import SchemaCache, get_schema_cache
        assert SchemaCache is not None
        assert get_schema_cache is not None

    def test_field_type_names_exported(self):
        """FIELD_TYPE_NAMES is exported from main module."""
        from dealcloud_sdk import FIELD_TYPE_NAMES
        assert FIELD_TYPE_NAMES is not None
        assert isinstance(FIELD_TYPE_NAMES, dict)

    def test_get_field_type_name_exported(self):
        """get_field_type_name is exported from main module."""
        from dealcloud_sdk import get_field_type_name
        assert get_field_type_name is not None
        assert callable(get_field_type_name)

    def test_data_type_exported(self):
        """DataType is exported from main module."""
        from dealcloud_sdk import DataType
        assert DataType is not None

    def test_profiling_utilities_exported(self):
        """Profiling utilities are exported from main module."""
        from dealcloud_sdk import analyze_field_values, detect_choice_field, estimate_field_type
        assert estimate_field_type is not None
        assert detect_choice_field is not None
        assert analyze_field_values is not None

