"""Tests for DealCloud factory functions."""

import json
import os
import tempfile
import pytest

from dealcloud_sdk.factories.from_env import (
    dc_from_environment_variables,
    read_env_config,
    normalize_site_url,
)
from dealcloud_sdk.factories.from_json import dc_from_json_config, _is_dotnet_format
from dealcloud_sdk.factories.from_yaml import dc_from_yaml_config
from dealcloud_sdk.models.factory_models import DealCloudConfig, DealCloudFactoryArgs


class TestNormalizeSiteUrl:
    """Tests for site_url normalization (scheme/path stripped to host only)."""

    def test_https_with_path_returns_host_only(self):
        assert normalize_site_url("https://site.intapp.com/auth") == "site.intapp.com"

    def test_http_with_path_returns_host_only(self):
        assert normalize_site_url("http://client.dealcloud.com/api") == "client.dealcloud.com"

    def test_plain_host_unchanged(self):
        assert normalize_site_url("site.intapp.com") == "site.intapp.com"

    def test_https_no_path_returns_host_only(self):
        assert normalize_site_url("https://site.intapp.com") == "site.intapp.com"


class TestFromEnv:
    """Tests for environment variable factory."""
    
    def test_read_env_config_success(self, monkeypatch):
        """Test read_env_config with existing variable."""
        monkeypatch.setenv("TEST_VAR", "test_value")
        result = read_env_config("TEST_VAR")
        assert result == "test_value"
    
    def test_read_env_config_missing(self):
        """Test read_env_config with missing variable."""
        with pytest.raises(KeyError) as exc_info:
            read_env_config("NONEXISTENT_VAR_12345")
        assert "NONEXISTENT_VAR_12345" in str(exc_info.value)
    
    def test_dc_from_environment_variables(self, monkeypatch):
        """Test dc_from_environment_variables."""
        monkeypatch.setenv("DC_SITE_URL", "test.dealcloud.com")
        monkeypatch.setenv("DC_CLIENT_ID", "12345")
        monkeypatch.setenv("DC_API_KEY", "secret123")

        config = dc_from_environment_variables()
        assert config.site_url == "test.dealcloud.com"
        assert config.client_id == "12345"
        assert config.client_secret == "secret123"

    def test_dc_from_environment_variables_normalizes_site_url(self, monkeypatch):
        """Site URL with https:// and path is stored as host only."""
        monkeypatch.setenv("DC_SITE_URL", "https://site.intapp.com/auth")
        monkeypatch.setenv("DC_CLIENT_ID", "12345")
        monkeypatch.setenv("DC_API_KEY", "secret123")

        config = dc_from_environment_variables()
        assert config.site_url == "site.intapp.com"
    
    def test_dc_from_environment_variables_custom_names(self, monkeypatch):
        """Test dc_from_environment_variables with custom names."""
        monkeypatch.setenv("CUSTOM_SITE", "custom.dealcloud.com")
        monkeypatch.setenv("CUSTOM_ID", "54321")
        monkeypatch.setenv("CUSTOM_SECRET", "customsecret")
        
        config = dc_from_environment_variables(
            site_url_env_name="CUSTOM_SITE",
            client_id_env_name="CUSTOM_ID",
            client_secret_env_name="CUSTOM_SECRET",
        )
        assert config.site_url == "custom.dealcloud.com"
        assert config.client_id == "54321"
    
    def test_dc_from_environment_variables_returns_factory_args_when_only_credentials(self, monkeypatch):
        """Test that only credentials returns DealCloudFactoryArgs for backward compatibility."""
        monkeypatch.setenv("DC_SITE_URL", "test.dealcloud.com")
        monkeypatch.setenv("DC_CLIENT_ID", "12345")
        monkeypatch.setenv("DC_API_KEY", "secret123")
        
        config = dc_from_environment_variables()
        assert isinstance(config, DealCloudFactoryArgs)
        assert not isinstance(config, DealCloudConfig)
    
    def test_dc_from_environment_variables_returns_config_with_timeout(self, monkeypatch):
        """Test that setting timeout returns DealCloudConfig."""
        monkeypatch.setenv("DC_SITE_URL", "test.dealcloud.com")
        monkeypatch.setenv("DC_CLIENT_ID", "12345")
        monkeypatch.setenv("DC_API_KEY", "secret123")
        monkeypatch.setenv("DC_SDK_CONNECTOR_TIMEOUT_SECONDS", "120")
        
        config = dc_from_environment_variables()
        assert isinstance(config, DealCloudConfig)
        assert config.connectorTimeoutSeconds == 120
        assert config.siteUrl == "test.dealcloud.com"
        assert config.clientId == "12345"
        assert config.clientSecret == "secret123"
    
    def test_dc_from_environment_variables_with_query_settings(self, monkeypatch):
        """Test environment variables for query settings."""
        monkeypatch.setenv("DC_SITE_URL", "test.dealcloud.com")
        monkeypatch.setenv("DC_CLIENT_ID", "12345")
        monkeypatch.setenv("DC_API_KEY", "secret123")
        monkeypatch.setenv("DC_SDK_QUERY_PAGE_SIZE", "2000")
        monkeypatch.setenv("DC_SDK_QUERY_CELL_PAGINATION_LIMIT", "5000")
        monkeypatch.setenv("DC_SDK_QUERY_DELETE_PAGE_SIZE", "15000")
        
        config = dc_from_environment_variables()
        assert isinstance(config, DealCloudConfig)
        assert config.querySettings.pageSize == 2000
        assert config.querySettings.cellPaginationLimit == 5000
        assert config.querySettings.deletePageSize == 15000
    
    def test_dc_from_environment_variables_with_concurrency_limits(self, monkeypatch):
        """Test environment variables for concurrency limits."""
        monkeypatch.setenv("DC_SITE_URL", "test.dealcloud.com")
        monkeypatch.setenv("DC_CLIENT_ID", "12345")
        monkeypatch.setenv("DC_API_KEY", "secret123")
        monkeypatch.setenv("DC_SDK_CONCURRENCY_LIMIT_READ", "4")
        monkeypatch.setenv("DC_SDK_CONCURRENCY_LIMIT_DELETE", "3")
        monkeypatch.setenv("DC_SDK_CONCURRENCY_LIMIT_CREATE", "5")
        
        config = dc_from_environment_variables()
        assert isinstance(config, DealCloudConfig)
        assert config.concurrencyLimits.read == 4
        assert config.concurrencyLimits.delete == 3
        assert config.concurrencyLimits.create == 5
    
    def test_dc_from_environment_variables_with_retry_settings(self, monkeypatch):
        """Test environment variables for retry settings."""
        monkeypatch.setenv("DC_SITE_URL", "test.dealcloud.com")
        monkeypatch.setenv("DC_CLIENT_ID", "12345")
        monkeypatch.setenv("DC_API_KEY", "secret123")
        monkeypatch.setenv("DC_SDK_RETRY_TOO_MANY_REQUESTS", "10")
        monkeypatch.setenv("DC_SDK_RETRY_INTERNAL_SERVER_ERROR", "3")
        monkeypatch.setenv("DC_SDK_RETRY_SERVICE_UNAVAILABLE", "4")
        monkeypatch.setenv("DC_SDK_RETRY_BAD_GATEWAY", "2")
        monkeypatch.setenv("DC_SDK_RETRY_GATEWAY_TIMEOUT", "3")
        monkeypatch.setenv("DC_SDK_RETRY_BACKOFF_FACTOR", "2.5")
        monkeypatch.setenv("DC_SDK_RETRY_MAX_BACKOFF_SECONDS", "600.0")
        
        config = dc_from_environment_variables()
        assert isinstance(config, DealCloudConfig)
        assert config.responseRetrySettings.tooManyRequests == 10
        assert config.responseRetrySettings.internalServerError == 3
        assert config.responseRetrySettings.serviceUnavailable == 4
        assert config.responseRetrySettings.badGateway == 2
        assert config.responseRetrySettings.gatewayTimeout == 3
        assert config.responseRetrySettings.backoffFactor == 2.5
        assert config.responseRetrySettings.maxBackoffSeconds == 600.0
    
    def test_dc_from_environment_variables_partial_settings(self, monkeypatch):
        """Test that partial optional settings still return DealCloudConfig."""
        monkeypatch.setenv("DC_SITE_URL", "test.dealcloud.com")
        monkeypatch.setenv("DC_CLIENT_ID", "12345")
        monkeypatch.setenv("DC_API_KEY", "secret123")
        monkeypatch.setenv("DC_SDK_QUERY_PAGE_SIZE", "500")
        
        config = dc_from_environment_variables()
        assert isinstance(config, DealCloudConfig)
        assert config.querySettings.pageSize == 500
        # Other query settings should use defaults
        assert config.querySettings.cellPaginationLimit == 9000  # default
        assert config.querySettings.deletePageSize == 5000  # default
    
    def test_dc_from_environment_variables_invalid_int(self, monkeypatch):
        """Test that invalid integer values raise ValueError."""
        monkeypatch.setenv("DC_SITE_URL", "test.dealcloud.com")
        monkeypatch.setenv("DC_CLIENT_ID", "12345")
        monkeypatch.setenv("DC_API_KEY", "secret123")
        monkeypatch.setenv("DC_SDK_QUERY_PAGE_SIZE", "not_an_int")
        
        with pytest.raises(ValueError) as exc_info:
            dc_from_environment_variables()
        assert "must be an integer" in str(exc_info.value)
    
    def test_dc_from_environment_variables_invalid_float(self, monkeypatch):
        """Test that invalid float values raise ValueError."""
        monkeypatch.setenv("DC_SITE_URL", "test.dealcloud.com")
        monkeypatch.setenv("DC_CLIENT_ID", "12345")
        monkeypatch.setenv("DC_API_KEY", "secret123")
        monkeypatch.setenv("DC_SDK_RETRY_BACKOFF_FACTOR", "not_a_float")
        
        with pytest.raises(ValueError) as exc_info:
            dc_from_environment_variables()
        assert "must be a float" in str(exc_info.value)


class TestDotnetFormatDetection:
    """Tests for .NET SDK format detection."""
    
    def test_is_dotnet_format_with_timeout(self):
        """Test _is_dotnet_format detects connectorTimeoutSeconds."""
        data = {
            "siteUrl": "test.dealcloud.com",
            "clientId": "12345",
            "clientSecret": "secret",
            "connectorTimeoutSeconds": 100,
        }
        assert _is_dotnet_format(data) is True
    
    def test_is_dotnet_format_with_retry_settings(self):
        """Test _is_dotnet_format detects responseRetrySettings."""
        data = {
            "siteUrl": "test.dealcloud.com",
            "clientId": "12345",
            "clientSecret": "secret",
            "responseRetrySettings": {"tooManyRequests": 5},
        }
        assert _is_dotnet_format(data) is True
    
    def test_is_dotnet_format_with_query_settings(self):
        """Test _is_dotnet_format detects querySettings."""
        data = {
            "siteUrl": "test.dealcloud.com",
            "clientId": "12345",
            "clientSecret": "secret",
            "querySettings": {"pageSize": 500},
        }
        assert _is_dotnet_format(data) is True
    
    def test_is_dotnet_format_with_concurrency_limits(self):
        """Test _is_dotnet_format detects concurrencyLimits."""
        data = {
            "siteUrl": "test.dealcloud.com",
            "clientId": "12345",
            "clientSecret": "secret",
            "concurrencyLimits": {"read": 2},
        }
        assert _is_dotnet_format(data) is True
    
    def test_is_dotnet_format_legacy_format(self):
        """Test _is_dotnet_format returns False for legacy format."""
        data = {
            "site_url": "test.dealcloud.com",
            "client_id": "12345",
            "client_secret": "secret",
        }
        assert _is_dotnet_format(data) is False
    
    def test_is_dotnet_format_camelcase_credentials_only(self):
        """Test _is_dotnet_format returns False for camelCase credentials only."""
        data = {
            "siteUrl": "test.dealcloud.com",
            "clientId": "12345",
            "clientSecret": "secret",
        }
        assert _is_dotnet_format(data) is False


class TestFromJson:
    """Tests for JSON factory."""
    
    def test_dc_from_json_config_flat(self):
        """Test dc_from_json_config with flat structure."""
        config_data = {
            "site_url": "test.dealcloud.com",
            "client_id": "12345",
            "client_secret": "secret123",
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = dc_from_json_config(temp_path)
            assert isinstance(config, DealCloudFactoryArgs)
            assert config.site_url == "test.dealcloud.com"
            assert config.client_id == "12345"
            assert config.client_secret == "secret123"
        finally:
            os.unlink(temp_path)
    
    def test_dc_from_json_config_invalid_path_raises(self):
        """Test dc_from_json_config with invalid nested path."""
        config_data = {
            "site_url": "test.dealcloud.com",
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name
        
        try:
            with pytest.raises(KeyError, match="Path 'invalid.path' not found"):
                dc_from_json_config(temp_path, json_path_to_credentials="invalid.path")
        finally:
            os.unlink(temp_path)
    
    def test_dc_from_json_config_camel_case(self):
        """Test dc_from_json_config with camelCase (.NET style)."""
        config_data = {
            "siteUrl": "test.dealcloud.com",
            "clientId": "12345",
            "clientSecret": "secret123",
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = dc_from_json_config(temp_path)
            assert config.site_url == "test.dealcloud.com"
            assert config.client_id == "12345"
        finally:
            os.unlink(temp_path)
    
    def test_dc_from_json_config_nested(self):
        """Test dc_from_json_config with nested structure."""
        config_data = {
            "app": {
                "dealcloud": {
                    "site_url": "test.dealcloud.com",
                    "client_id": "12345",
                    "client_secret": "secret123",
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = dc_from_json_config(temp_path, json_path_to_credentials="app.dealcloud")
            assert config.site_url == "test.dealcloud.com"
            assert config.client_id == "12345"
        finally:
            os.unlink(temp_path)

    def test_dc_from_json_config_normalizes_site_url(self):
        """Legacy JSON with https:// and path stores host only."""
        config_data = {
            "site_url": "https://site.intapp.com/auth",
            "client_id": "12345",
            "client_secret": "secret123",
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name
        try:
            config = dc_from_json_config(temp_path)
            assert config.site_url == "site.intapp.com"
        finally:
            os.unlink(temp_path)


class TestFromJsonDotnetFormat:
    """Tests for JSON factory with .NET SDK format."""
    
    def test_dc_from_json_config_dotnet_full(self):
        """Test dc_from_json_config with full .NET SDK format."""
        config_data = {
            "siteUrl": "test.dealcloud.com",
            "clientId": "12345",
            "clientSecret": "secret123",
            "connectorTimeoutSeconds": 100,
            "querySettings": {
                "pageSize": 500,
                "cellPaginationLimit": 5000,
                "deletePageSize": 8000,
            },
            "concurrencyLimits": {
                "read": 4,
                "delete": 2,
                "create": 3,
            },
            "responseRetrySettings": {
                "tooManyRequests": 10,
                "internalServerError": 3,
                "serviceUnavailable": 3,
                "backoffFactor": 3.0,
            },
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = dc_from_json_config(temp_path)
            
            # Should return DealCloudConfig, not DealCloudFactoryArgs
            assert isinstance(config, DealCloudConfig)
            
            # Check credentials
            assert config.siteUrl == "test.dealcloud.com"
            assert config.clientId == "12345"
            assert config.clientSecret == "secret123"
            
            # Check timeout
            assert config.connectorTimeoutSeconds == 100
            
            # Check query settings
            assert config.querySettings.pageSize == 500
            assert config.querySettings.cellPaginationLimit == 5000
            assert config.querySettings.deletePageSize == 8000
            
            # Check concurrency limits
            assert config.concurrencyLimits.read == 4
            assert config.concurrencyLimits.delete == 2
            assert config.concurrencyLimits.create == 3
            
            # Check retry settings
            assert config.responseRetrySettings.tooManyRequests == 10
            assert config.responseRetrySettings.internalServerError == 3
            assert config.responseRetrySettings.serviceUnavailable == 3
            assert config.responseRetrySettings.backoffFactor == 3.0
        finally:
            os.unlink(temp_path)
    
    def test_dc_from_json_config_dotnet_partial(self):
        """Test dc_from_json_config with partial .NET SDK format (defaults)."""
        config_data = {
            "siteUrl": "test.dealcloud.com",
            "clientId": "12345",
            "clientSecret": "secret123",
            "connectorTimeoutSeconds": 120,  # Just timeout, rest defaults
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = dc_from_json_config(temp_path)
            
            assert isinstance(config, DealCloudConfig)
            assert config.connectorTimeoutSeconds == 120
            
            # Defaults should be applied
            assert config.querySettings.pageSize == 1000
            assert config.concurrencyLimits.read == 2
            assert config.responseRetrySettings.tooManyRequests == 5
        finally:
            os.unlink(temp_path)
    
    def test_dc_from_json_config_dotnet_with_retry_only(self):
        """Test dc_from_json_config with only responseRetrySettings."""
        config_data = {
            "siteUrl": "test.dealcloud.com",
            "clientId": "12345",
            "clientSecret": "secret123",
            "responseRetrySettings": {
                "tooManyRequests": 15,
                "backoffFactor": 4.0,
            },
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = dc_from_json_config(temp_path)
            
            assert isinstance(config, DealCloudConfig)
            assert config.responseRetrySettings.tooManyRequests == 15
            assert config.responseRetrySettings.backoffFactor == 4.0
            # Defaults for others
            assert config.responseRetrySettings.internalServerError == 2
        finally:
            os.unlink(temp_path)

    def test_dc_from_json_config_dotnet_normalizes_site_url(self):
        """Dotnet JSON with https:// and path stores host only."""
        config_data = {
            "siteUrl": "https://site.intapp.com/auth",
            "clientId": "12345",
            "clientSecret": "secret",
            "connectorTimeoutSeconds": 100,
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name
        try:
            config = dc_from_json_config(temp_path)
            assert isinstance(config, DealCloudConfig)
            assert config.siteUrl == "site.intapp.com"
        finally:
            os.unlink(temp_path)

    def test_dc_from_json_config_dotnet_snake_case_credentials(self):
        """Test dc_from_json_config with .NET format but snake_case credentials."""
        config_data = {
            "site_url": "test.dealcloud.com",
            "client_id": "12345",
            "client_secret": "secret123",
            "connectorTimeoutSeconds": 100,  # This triggers .NET format detection
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = dc_from_json_config(temp_path)
            
            # Should normalize snake_case to camelCase
            assert isinstance(config, DealCloudConfig)
            assert config.siteUrl == "test.dealcloud.com"
            assert config.clientId == "12345"
            assert config.clientSecret == "secret123"
        finally:
            os.unlink(temp_path)
    
    def test_dc_from_json_config_dotnet_nested(self):
        """Test dc_from_json_config with nested .NET SDK format."""
        config_data = {
            "environments": {
                "production": {
                    "siteUrl": "prod.dealcloud.com",
                    "clientId": "prod-123",
                    "clientSecret": "prod-secret",
                    "connectorTimeoutSeconds": 120,
                    "responseRetrySettings": {
                        "tooManyRequests": 15,
                    },
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = dc_from_json_config(temp_path, json_path_to_credentials="environments.production")
            
            assert isinstance(config, DealCloudConfig)
            assert config.siteUrl == "prod.dealcloud.com"
            assert config.connectorTimeoutSeconds == 120
            assert config.responseRetrySettings.tooManyRequests == 15
        finally:
            os.unlink(temp_path)
    
    def test_dc_from_json_config_retry_count_by_status(self):
        """Test that retry settings convert to status code map."""
        config_data = {
            "siteUrl": "test.dealcloud.com",
            "clientId": "12345",
            "clientSecret": "secret123",
            "responseRetrySettings": {
                "tooManyRequests": 10,
                "internalServerError": 3,
                "serviceUnavailable": 4,
                "badGateway": 2,
                "gatewayTimeout": 5,
            },
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = dc_from_json_config(temp_path)
            
            # Test conversion to status code map
            status_map = config.responseRetrySettings.to_retry_count_by_status()
            assert status_map[429] == 10  # tooManyRequests
            assert status_map[500] == 3   # internalServerError
            assert status_map[502] == 2   # badGateway
            assert status_map[503] == 4   # serviceUnavailable
            assert status_map[504] == 5   # gatewayTimeout
        finally:
            os.unlink(temp_path)


class TestFromYaml:
    """Tests for YAML factory."""
    
    @pytest.fixture(autouse=True)
    def check_yaml(self):
        """Check if PyYAML is available."""
        pytest.importorskip("yaml")
    
    def test_dc_from_yaml_config_flat(self):
        """Test dc_from_yaml_config with flat structure."""
        import yaml
        
        config_data = {
            "site_url": "test.dealcloud.com",
            "client_id": "12345",
            "client_secret": "secret123",
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = dc_from_yaml_config(temp_path)
            assert config.site_url == "test.dealcloud.com"
            assert config.client_id == "12345"
            assert config.client_secret == "secret123"
        finally:
            os.unlink(temp_path)

    def test_dc_from_yaml_config_normalizes_site_url(self):
        """Legacy YAML with https:// and path stores host only."""
        import yaml
        config_data = {
            "site_url": "https://site.intapp.com/auth",
            "client_id": "12345",
            "client_secret": "secret123",
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            temp_path = f.name
        try:
            config = dc_from_yaml_config(temp_path)
            assert config.site_url == "site.intapp.com"
        finally:
            os.unlink(temp_path)

    def test_dc_from_yaml_config_camel_case(self):
        """Test dc_from_yaml_config with camelCase keys."""
        import yaml
        
        config_data = {
            "siteUrl": "test.dealcloud.com",
            "clientId": "12345",
            "clientSecret": "secret123",
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = dc_from_yaml_config(temp_path)
            assert config.site_url == "test.dealcloud.com"
            assert config.client_id == "12345"
            assert config.client_secret == "secret123"
        finally:
            os.unlink(temp_path)
    
    def test_dc_from_yaml_config_nested(self):
        """Test dc_from_yaml_config with nested structure."""
        import yaml
        
        config_data = {
            "dealcloud": {
                "site_url": "test.dealcloud.com",
                "client_id": "12345",
                "client_secret": "secret123",
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = dc_from_yaml_config(temp_path, yaml_path_to_credentials="dealcloud")
            assert config.site_url == "test.dealcloud.com"
            assert config.client_id == "12345"
        finally:
            os.unlink(temp_path)
    
    def test_dc_from_yaml_config_deep_nested(self):
        """Test dc_from_yaml_config with deeply nested structure."""
        import yaml
        
        config_data = {
            "app": {
                "config": {
                    "dealcloud": {
                        "site_url": "deep.dealcloud.com",
                        "client_id": "99999",
                        "client_secret": "deepsecret",
                    }
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = dc_from_yaml_config(temp_path, yaml_path_to_credentials="app.config.dealcloud")
            assert config.site_url == "deep.dealcloud.com"
            assert config.client_id == "99999"
        finally:
            os.unlink(temp_path)
    
    def test_dc_from_yaml_config_invalid_path(self):
        """Test dc_from_yaml_config with invalid nested path."""
        import yaml
        
        config_data = {
            "site_url": "test.dealcloud.com",
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            temp_path = f.name
        
        try:
            with pytest.raises(KeyError) as exc_info:
                dc_from_yaml_config(temp_path, yaml_path_to_credentials="invalid.path")
            assert "Path 'invalid.path' not found" in str(exc_info.value)
        finally:
            os.unlink(temp_path)


class TestFromYamlDotnetFormat:
    """Tests for YAML factory with .NET SDK format."""
    
    @pytest.fixture(autouse=True)
    def check_yaml(self):
        """Check if PyYAML is available."""
        pytest.importorskip("yaml")
    
    def test_dc_from_yaml_config_dotnet_full(self):
        """Test dc_from_yaml_config with full .NET SDK format."""
        import yaml
        
        config_data = {
            "siteUrl": "test.dealcloud.com",
            "clientId": "12345",
            "clientSecret": "secret123",
            "connectorTimeoutSeconds": 100,
            "querySettings": {
                "pageSize": 500,
                "cellPaginationLimit": 5000,
                "deletePageSize": 8000,
            },
            "concurrencyLimits": {
                "read": 4,
                "delete": 2,
                "create": 3,
            },
            "responseRetrySettings": {
                "tooManyRequests": 10,
                "internalServerError": 3,
                "backoffFactor": 3.0,
            },
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = dc_from_yaml_config(temp_path)
            
            # Should return DealCloudConfig
            assert isinstance(config, DealCloudConfig)
            
            # Check credentials
            assert config.siteUrl == "test.dealcloud.com"
            assert config.clientId == "12345"
            
            # Check timeout
            assert config.connectorTimeoutSeconds == 100
            
            # Check query settings
            assert config.querySettings.pageSize == 500
            
            # Check concurrency limits
            assert config.concurrencyLimits.read == 4
            
            # Check retry settings
            assert config.responseRetrySettings.tooManyRequests == 10
            assert config.responseRetrySettings.backoffFactor == 3.0
        finally:
            os.unlink(temp_path)
    
    def test_dc_from_yaml_config_dotnet_partial(self):
        """Test dc_from_yaml_config with partial .NET SDK format."""
        import yaml
        
        config_data = {
            "siteUrl": "test.dealcloud.com",
            "clientId": "12345",
            "clientSecret": "secret123",
            "connectorTimeoutSeconds": 150,
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = dc_from_yaml_config(temp_path)
            
            assert isinstance(config, DealCloudConfig)
            assert config.connectorTimeoutSeconds == 150
            # Defaults applied
            assert config.querySettings.pageSize == 1000
        finally:
            os.unlink(temp_path)

    def test_dc_from_yaml_config_dotnet_normalizes_site_url(self):
        """Dotnet YAML with https:// and path stores host only."""
        import yaml
        config_data = {
            "siteUrl": "https://site.intapp.com/auth",
            "clientId": "12345",
            "clientSecret": "secret",
            "connectorTimeoutSeconds": 100,
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            temp_path = f.name
        try:
            config = dc_from_yaml_config(temp_path)
            assert isinstance(config, DealCloudConfig)
            assert config.siteUrl == "site.intapp.com"
        finally:
            os.unlink(temp_path)

    def test_dc_from_yaml_config_dotnet_snake_case(self):
        """Test dc_from_yaml_config with mixed snake_case credentials."""
        import yaml
        
        config_data = {
            "site_url": "test.dealcloud.com",
            "client_id": "12345",
            "client_secret": "secret123",
            "responseRetrySettings": {
                "tooManyRequests": 8,
            },
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = dc_from_yaml_config(temp_path)
            
            # Should normalize to camelCase
            assert isinstance(config, DealCloudConfig)
            assert config.siteUrl == "test.dealcloud.com"
            assert config.clientId == "12345"
            assert config.responseRetrySettings.tooManyRequests == 8
        finally:
            os.unlink(temp_path)
    
    def test_dc_from_yaml_returns_factory_args_for_legacy(self):
        """Test that legacy YAML format returns DealCloudFactoryArgs."""
        import yaml
        
        config_data = {
            "site_url": "test.dealcloud.com",
            "client_id": "12345",
            "client_secret": "secret123",
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = dc_from_yaml_config(temp_path)
            
            # Should return DealCloudFactoryArgs for legacy format
            assert isinstance(config, DealCloudFactoryArgs)
            assert config.site_url == "test.dealcloud.com"
        finally:
            os.unlink(temp_path)


class TestJsonHelpers:
    """Tests for JSON helper functions."""
    
    def test_get_nested_value_direct(self):
        """Test _get_nested_value with empty path returns original data."""
        from dealcloud_sdk.factories.from_json import _get_nested_value
        
        data = {"key": "value"}
        result = _get_nested_value(data, "")
        assert result == data
    
    def test_get_nested_value_single_level(self):
        """Test _get_nested_value with single level path."""
        from dealcloud_sdk.factories.from_json import _get_nested_value
        
        data = {"config": {"key": "value"}}
        result = _get_nested_value(data, "config")
        assert result == {"key": "value"}
    
    def test_get_nested_value_multi_level(self):
        """Test _get_nested_value with multi-level path."""
        from dealcloud_sdk.factories.from_json import _get_nested_value
        
        data = {"a": {"b": {"c": "found"}}}
        result = _get_nested_value(data, "a.b")
        assert result == {"c": "found"}
    
    def test_get_nested_value_not_found(self):
        """Test _get_nested_value with invalid path raises KeyError."""
        from dealcloud_sdk.factories.from_json import _get_nested_value
        
        data = {"a": {"b": "value"}}
        with pytest.raises(KeyError, match="Path 'a.c' not found"):
            _get_nested_value(data, "a.c")
    
    def test_get_nested_value_non_dict_in_path(self):
        """Test _get_nested_value when path traverses non-dict value."""
        from dealcloud_sdk.factories.from_json import _get_nested_value
        
        data = {"a": "not_a_dict"}
        with pytest.raises(KeyError, match="Path 'a.b' not found"):
            _get_nested_value(data, "a.b")


class TestYamlImportError:
    """Tests for YAML import error handling."""
    
    def test_yaml_import_error_handling(self, tmp_path):
        """Test dc_from_yaml_config raises ImportError when yaml unavailable."""
        import sys
        import builtins
        
        # Create a test yaml file
        config_file = tmp_path / "config.yaml"
        config_file.write_text("site_url: test.dealcloud.com\n")
        
        # Save original import
        real_import = builtins.__import__
        
        def mock_import(name, *args, **kwargs):
            if name == 'yaml':
                raise ImportError("No module named 'yaml'")
            return real_import(name, *args, **kwargs)
        
        # Reload module with mocked import
        if 'dealcloud_sdk.factories.from_yaml' in sys.modules:
            del sys.modules['dealcloud_sdk.factories.from_yaml']
        
        builtins.__import__ = mock_import
        try:
            # Re-import to get fresh module
            from dealcloud_sdk.factories.from_yaml import dc_from_yaml_config
            
            with pytest.raises(ImportError) as exc_info:
                dc_from_yaml_config(str(config_file))
            
            assert "PyYAML is required" in str(exc_info.value)
        finally:
            builtins.__import__ = real_import
            # Restore module
            if 'dealcloud_sdk.factories.from_yaml' in sys.modules:
                del sys.modules['dealcloud_sdk.factories.from_yaml']


class TestYamlHelpers:
    """Tests for YAML helper functions."""
    
    def test_get_nested_value_direct(self):
        """Test _get_nested_value with empty path."""
        from dealcloud_sdk.factories.from_yaml import _get_nested_value
        
        data = {"key": "value"}
        result = _get_nested_value(data, "")
        assert result == data
    
    def test_get_nested_value_single_level(self):
        """Test _get_nested_value with single level path."""
        from dealcloud_sdk.factories.from_yaml import _get_nested_value
        
        data = {"config": {"key": "value"}}
        result = _get_nested_value(data, "config")
        assert result == {"key": "value"}
    
    def test_get_nested_value_multi_level(self):
        """Test _get_nested_value with multi-level path."""
        from dealcloud_sdk.factories.from_yaml import _get_nested_value
        
        data = {"a": {"b": {"c": "found"}}}
        result = _get_nested_value(data, "a.b")
        assert result == {"c": "found"}
    
    def test_get_nested_value_not_found(self):
        """Test _get_nested_value with invalid path."""
        from dealcloud_sdk.factories.from_yaml import _get_nested_value
        
        data = {"a": {"b": "value"}}
        with pytest.raises(KeyError):
            _get_nested_value(data, "a.c")


