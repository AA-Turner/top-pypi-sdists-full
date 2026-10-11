"""Tests for DealCloudBase class."""

import json
import os
import tempfile
import pytest
from unittest.mock import MagicMock, patch, PropertyMock

from intapp_rest_client.exceptions import HttpError

from dealcloud_sdk.base.dealcloud_base import DealCloudBase
from dealcloud_sdk.dealcloud import DealCloud
from dealcloud_sdk.models.factory_models import (
    DealCloudConfig,
    QuerySettings,
    ConcurrencyLimits,
    ResponseRetrySettings,
)
from dealcloud_sdk.utils.process_response_errors import DealCloudRateLimitError


class TestDealCloudBaseInit:
    """Tests for DealCloudBase initialization."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_init_with_params(self, mock_client_class):
        """Test initialization with individual parameters."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        base = DealCloudBase(
            site_url="test.dealcloud.com",
            client_id="12345",
            client_secret="secret123",
        )
        
        assert base._site == "test.dealcloud.com"
        assert base._client_id == "12345"
        assert base._client_secret == "secret123"
        assert base._url_root == "https://test.dealcloud.com/api/rest/v4"
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_init_with_config(self, mock_client_class):
        """Test initialization with DealCloudConfig object."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        config = DealCloudConfig(
            siteUrl="config.dealcloud.com",
            clientId="config123",
            clientSecret="configsecret",
            connectorTimeoutSeconds=200,
        )
        
        base = DealCloudBase(config=config)
        
        assert base._site == "config.dealcloud.com"
        assert base._client_id == "config123"
        assert base._config == config
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_init_missing_params_raises_error(self, mock_client_class):
        """Test that missing parameters raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            DealCloudBase()
        assert "Must provide either config or site_url/client_id/client_secret" in str(exc_info.value)
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_init_partial_params_raises_error(self, mock_client_class):
        """Test that partial parameters raises ValueError."""
        with pytest.raises(ValueError):
            DealCloudBase(site_url="test.dealcloud.com")
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_init_builds_correct_urls(self, mock_client_class):
        """Test URL building during init."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        base = DealCloudBase(
            site_url="mysite.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        assert base._url_root == "https://mysite.dealcloud.com/api/rest/v4"
        assert base._url_root_v1 == "https://mysite.dealcloud.com/api/rest/v1"
        assert base._schema_url == "https://mysite.dealcloud.com/api/rest/v4/schema"
        assert base._data_url == "https://mysite.dealcloud.com/api/rest/v4/data"

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_init_sets__logger_from_logger_when_missing(self, mock_client_class):
        """Compatibility: copy .logger to ._logger when client only exposes .logger."""

        class ClientWithLoggerOnly:
            def __init__(self):
                self.logger = MagicMock()

            def _get_auth_headers_sync(self):
                return {}

        client = ClientWithLoggerOnly()
        mock_client_class.return_value = client

        DealCloudBase(
            site_url="log.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        assert client._logger is client.logger

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_url_properties_return_correct_values(self, mock_client_class):
        """Test public URL properties (api_url, schema_url, data_url, etc.)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        base = DealCloudBase(
            site_url="mysite.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        assert base.site_url == "mysite.dealcloud.com"
        assert base.api_url == "https://mysite.dealcloud.com/api/rest/v4"
        assert base.api_url_v1 == "https://mysite.dealcloud.com/api/rest/v1"
        assert base.schema_url == "https://mysite.dealcloud.com/api/rest/v4/schema"
        assert base.data_url == "https://mysite.dealcloud.com/api/rest/v4/data"
        assert base.entrydata_url == "https://mysite.dealcloud.com/api/rest/v4/data/entrydata"
        assert base.rows_url == "https://mysite.dealcloud.com/api/rest/v4/data/entrydata/rows"
        assert base.query_url == "https://mysite.dealcloud.com/api/rest/v4/data/entrydata/rows/query"
        assert base.views_url == "https://mysite.dealcloud.com/api/rest/v4/data/rows/view"
        assert base.auth_scope
        assert base.refresh_id_maps is True
        assert isinstance(base.retry_status_codes, dict)
        assert base.concurrency_limits is None
        assert base.query_settings is None
        assert base.client is not None
        assert base.cached_schema is None
        assert base.cached_user_map == {}
        assert base.cached_id_map == {}


class TestDealCloudBaseProperties:
    """Tests for DealCloudBase properties."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_page_size_default(self, mock_client_class):
        """Test default page_size when no config."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        base = DealCloudBase(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        assert base.page_size == 1000
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_page_size_from_config(self, mock_client_class):
        """Test page_size from config."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        config = DealCloudConfig(
            siteUrl="test.dealcloud.com",
            clientId="123",
            clientSecret="secret",
            querySettings=QuerySettings(pageSize=500),
        )
        
        base = DealCloudBase(config=config)
        
        assert base.page_size == 500
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_cell_pagination_limit_default(self, mock_client_class):
        """Test default cell_pagination_limit."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        base = DealCloudBase(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        assert base.cell_pagination_limit == 9000
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_cell_pagination_limit_from_config(self, mock_client_class):
        """Test cell_pagination_limit from config."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        config = DealCloudConfig(
            siteUrl="test.dealcloud.com",
            clientId="123",
            clientSecret="secret",
            querySettings=QuerySettings(cellPaginationLimit=5000),
        )
        
        base = DealCloudBase(config=config)
        
        assert base.cell_pagination_limit == 5000
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_page_size_default(self, mock_client_class):
        """Test default delete_page_size."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        base = DealCloudBase(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        assert base.delete_page_size == 10000
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_page_size_from_config(self, mock_client_class):
        """Test delete_page_size from config."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        config = DealCloudConfig(
            siteUrl="test.dealcloud.com",
            clientId="123",
            clientSecret="secret",
            querySettings=QuerySettings(deletePageSize=5000),
        )
        
        base = DealCloudBase(config=config)
        
        assert base.delete_page_size == 5000

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_page_size_exceeds_max_capped_to_10000(self, mock_client_class):
        """Test delete_page_size > 10000 is capped and warns (e.g. from raw config)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        base = DealCloudBase(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        # Simulate config with deletePageSize > 10000 (e.g. from env/JSON before validation)
        base._query_settings = MagicMock(deletePageSize=15000)

        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            got = base.delete_page_size
            assert got == 10000
            assert any("10000" in str(m.message) for m in w)
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_concurrency_defaults(self, mock_client_class):
        """Test default concurrency limits."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        base = DealCloudBase(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        assert base.read_concurrency == 4
        assert base.delete_concurrency == 4
        assert base.create_concurrency == 4
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_concurrency_from_config(self, mock_client_class):
        """Test concurrency limits from config."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        config = DealCloudConfig(
            siteUrl="test.dealcloud.com",
            clientId="123",
            clientSecret="secret",
            concurrencyLimits=ConcurrencyLimits(read=4, delete=2, create=3),
        )
        
        base = DealCloudBase(config=config)
        
        assert base.read_concurrency == 4
        assert base.delete_concurrency == 2
        assert base.create_concurrency == 3


class TestDealCloudBaseFactoryMethods:
    """Tests for factory methods."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_from_env(self, mock_client_class, monkeypatch):
        """Test from_env factory method."""
        monkeypatch.setenv("DC_SITE_URL", "env.dealcloud.com")
        monkeypatch.setenv("DC_CLIENT_ID", "env123")
        monkeypatch.setenv("DC_API_KEY", "envsecret")
        
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        base = DealCloudBase.from_env()
        
        assert base._site == "env.dealcloud.com"
        assert base._client_id == "env123"

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_from_env_uses_dealcloud_config_when_optional_settings_in_env(
        self, mock_client_class, monkeypatch
    ):
        """When optional DC_SDK_* vars are set, factory receives DealCloudConfig (not only to_config)."""
        monkeypatch.setenv("DC_SITE_URL", "env.dealcloud.com")
        monkeypatch.setenv("DC_CLIENT_ID", "env123")
        monkeypatch.setenv("DC_API_KEY", "envsecret")
        monkeypatch.setenv("DC_SDK_QUERY_PAGE_SIZE", "500")

        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client_class.return_value = mock_client

        base = DealCloudBase.from_env()
        assert base._site == "env.dealcloud.com"
        assert base._config is not None
        assert base._config.querySettings is not None
        assert base._config.querySettings.pageSize == 500
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_from_env_custom_names(self, mock_client_class, monkeypatch):
        """Test from_env with custom environment variable names."""
        monkeypatch.setenv("CUSTOM_URL", "custom.dealcloud.com")
        monkeypatch.setenv("CUSTOM_ID", "custom123")
        monkeypatch.setenv("CUSTOM_SECRET", "customsecret")
        
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        base = DealCloudBase.from_env(
            site_url_env_name="CUSTOM_URL",
            client_id_env_name="CUSTOM_ID",
            client_secret_env_name="CUSTOM_SECRET",
        )
        
        assert base._site == "custom.dealcloud.com"
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_from_json(self, mock_client_class, tmp_path):
        """Test from_json factory method."""
        config = {
            "site_url": "json.dealcloud.com",
            "client_id": "json123",
            "client_secret": "jsonsecret",
        }
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps(config))
        
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        base = DealCloudBase.from_json(str(config_file))
        
        assert base._site == "json.dealcloud.com"

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_from_json_full_dotnet_format_warns(self, mock_client_class, tmp_path):
        """Full JSON config via from_json issues DeprecationWarning; use from_config for new code."""
        config = {
            "siteUrl": "dotnet.dealcloud.com",
            "clientId": "1",
            "clientSecret": "s",
            "connectorTimeoutSeconds": 50,
        }
        path = tmp_path / "full.json"
        path.write_text(json.dumps(config))
        mock_client_class.return_value = MagicMock()
        mock_client_class.return_value._get_auth_headers_sync.return_value = {}

        with pytest.warns(DeprecationWarning, match="from_config"):
            base = DealCloudBase.from_json(str(path))

        assert base._site == "dotnet.dealcloud.com"
        assert base._config is not None

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_from_yaml_full_dotnet_format_warns(self, mock_client_class, tmp_path):
        pytest.importorskip("yaml")
        import yaml

        config = {
            "siteUrl": "yamldotnet.dealcloud.com",
            "clientId": "1",
            "clientSecret": "s",
            "connectorTimeoutSeconds": 60,
        }
        path = tmp_path / "full.yaml"
        path.write_text(yaml.safe_dump(config))
        mock_client_class.return_value = MagicMock()
        mock_client_class.return_value._get_auth_headers_sync.return_value = {}

        with pytest.warns(DeprecationWarning, match="from_config"):
            base = DealCloudBase.from_yaml(str(path))

        assert base._site == "yamldotnet.dealcloud.com"
        assert base._config is not None

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_from_yaml_legacy_format_uses_positional_constructor(self, mock_client_class, tmp_path):
        pytest.importorskip("yaml")
        import yaml

        path = tmp_path / "legacy.yaml"
        path.write_text(
            yaml.safe_dump(
                {
                    "site_url": "legacyyaml.dealcloud.com",
                    "client_id": "9",
                    "client_secret": "sec",
                }
            )
        )
        mock_client_class.return_value = MagicMock()
        mock_client_class.return_value._get_auth_headers_sync.return_value = {}

        base = DealCloudBase.from_yaml(str(path))
        assert base._site == "legacyyaml.dealcloud.com"
        assert base._client_id == "9"

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_from_config_yaml_extension(self, mock_client_class, tmp_path):
        pytest.importorskip("yaml")
        import yaml

        config = {
            "siteUrl": "ycfg.dealcloud.com",
            "clientId": "1",
            "clientSecret": "s",
            "connectorTimeoutSeconds": 40,
        }
        path = tmp_path / "cfg.yaml"
        path.write_text(yaml.safe_dump(config))
        mock_client_class.return_value = MagicMock()
        mock_client_class.return_value._get_auth_headers_sync.return_value = {}

        base = DealCloudBase.from_config(str(path))
        assert base._site == "ycfg.dealcloud.com"
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_from_config_json(self, mock_client_class, tmp_path):
        """Test from_config with JSON file."""
        config = {
            "siteUrl": "fullconfig.dealcloud.com",
            "clientId": "full123",
            "clientSecret": "fullsecret",
            "connectorTimeoutSeconds": 150,
        }
        config_file = tmp_path / "fullconfig.json"
        config_file.write_text(json.dumps(config))
        
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        base = DealCloudBase.from_config(str(config_file))
        
        assert base._site == "fullconfig.dealcloud.com"
        assert base._config is not None
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_from_config_object(self, mock_client_class):
        """Test from_config_object factory method."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        config = DealCloudConfig(
            siteUrl="object.dealcloud.com",
            clientId="obj123",
            clientSecret="objsecret",
        )
        
        base = DealCloudBase.from_config_object(config)
        
        assert base._site == "object.dealcloud.com"
        assert base._config == config


class TestDealCloudBaseContextManager:
    """Tests for context manager methods."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_context_manager_enter(self, mock_client_class):
        """Test context manager __enter__."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        base = DealCloudBase(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        with base as b:
            assert b is base
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_context_manager_exit_closes(self, mock_client_class):
        """Test context manager __exit__ calls close."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        base = DealCloudBase(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        with base:
            pass
        
        mock_client.close.assert_called_once()
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_close_method(self, mock_client_class):
        """Test close method."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        base = DealCloudBase(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        base.close()
        
        mock_client.close.assert_called_once()


class TestDealCloudBasePlaceholders:
    """Tests for placeholder methods."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_schema_placeholder(self, mock_client_class):
        """Test get_schema placeholder returns None."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        base = DealCloudBase(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        assert base.get_schema() is None
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_users_placeholder(self, mock_client_class):
        """Test get_users placeholder returns None."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        base = DealCloudBase(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        assert base.get_users() is None


class TestDealCloudBaseRetryConfig:
    """Tests for retry configuration."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_retry_settings_from_config(self, mock_client_class):
        """Test retry settings are applied from config."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        config = DealCloudConfig(
            siteUrl="test.dealcloud.com",
            clientId="123",
            clientSecret="secret",
            responseRetrySettings=ResponseRetrySettings(
                tooManyRequests=10,
                internalServerError=5,
                backoffFactor=3.0,
            ),
        )
        
        base = DealCloudBase(config=config)
        
        # Check retry map was built correctly
        assert base._status_retry_map[429] == 10
        assert base._status_retry_map[500] == 5


class Test429RateLimitHandling:
    """Tests for 429 rate limit error handling and transformation."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_schema_get_objects_raises_dealcloud_rate_limit_error_on_429(self, mock_client_class):
        """When client raises HttpError(429), schema path (with_error_handling) raises DealCloudRateLimitError."""
        DealCloud.clear_all_schema_caches()
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.side_effect = HttpError(
            429,
            "Too many requests",
            response_body={"message": "Rate limit exceeded"},
            headers={"Retry-After": "30"},
        )
        mock_client_class.return_value = mock_client

        with pytest.raises(DealCloudRateLimitError) as exc_info:
            DealCloud(
                site_url="test.dealcloud.com",
                client_id="123",
                client_secret="secret",
                cache_schema=False,
            )
        # DealCloud.__init__ calls get_schema() -> get_objects(), so 429 is raised and transformed there
        assert exc_info.value.status_code == 429
        assert exc_info.value.retry_after == 30

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_schema_get_currencies_429_raises_rate_limit_error(self, mock_client_class):
        """When client raises 429 on schema GET, DealCloudRateLimitError is raised (e.g. during init get_schema)."""
        DealCloud.clear_all_schema_caches()
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.side_effect = HttpError(
            429,
            "Too many requests",
            response_body={},
            headers={},
        )
        mock_client_class.return_value = mock_client

        with pytest.raises(DealCloudRateLimitError) as exc_info:
            DealCloud(
                site_url="test.dealcloud.com",
                client_id="123",
                client_secret="secret",
                cache_schema=False,
            )
        assert exc_info.value.status_code == 429
        assert exc_info.value.retry_after is None


class TestDealCloudSdkVersionHeader:
    """Tests for SDK version header."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_sdk_version_header_passed_to_rest_client(self, mock_client_class):
        """Test X-Dealcloud-Sdk-Version header is passed to RestClient."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        DealCloudBase(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        # Check that RestClient was called with headers containing SDK version
        call_kwargs = mock_client_class.call_args[1]
        assert "headers" in call_kwargs
        assert "X-Dealcloud-Sdk-Version" in call_kwargs["headers"]
        assert call_kwargs["headers"]["X-Dealcloud-Sdk-Version"].startswith("dealcloud-sdk.")
    
    def test_sdk_version_module_exports(self):
        """Test SDK version module exports correct values."""
        from dealcloud_sdk._version import SDK_VERSION, PACKAGE_NAME, __version__
        
        assert PACKAGE_NAME == "dealcloud-sdk"
        assert SDK_VERSION.startswith("dealcloud-sdk.")
        assert __version__ in SDK_VERSION
    
    def test_sdk_version_exported_from_package(self):
        """Test SDK version is exported from main package."""
        from dealcloud_sdk import SDK_VERSION, PACKAGE_NAME, __version__
        
        assert PACKAGE_NAME == "dealcloud-sdk"
        assert SDK_VERSION.startswith("dealcloud-sdk.")
        assert __version__ is not None



