import os
import pytest
import requests
from unittest.mock import Mock, patch
from spring_config_client.client import SpringConfigClient, _interpolate


# Mock response data with obfuscated details
MOCK_CONFIG_RESPONSE = {
    "name": "example-service-app",
    "profiles": [
        "production"
    ],
    "label": None,
    "version": "abc123def456789012345678901234567890abcd",
    "state": "",
    "propertySources": [
        {
            "name": "https://example.com/configs.git/example-service-app/application-production.properties",
            "source": {
                "MY_VAR_FOR_PROD": "prod",
                "ANOTHER_ONE_WITH_TEMPLATE": "${SOME_LOCAL_VAR}-prod"
            }
        },
        {
            "name": "https://example.com/configs.git/application-production.properties",
            "source": {
                "logging.level.root": "WARN",
                "logging.level.com.example": "INFO",
                "management.endpoints.web.exposure.include": "health,info,metrics"
            }
        },
        {
            "name": "https://example.com/configs.git/example-service-app/application.properties",
            "source": {
                "TEST_ENV_VAR": "test"
            }
        },
        {
            "name": "https://example.com/configs.git/application.properties",
            "source": {
                "spring.jpa.hibernate.ddl-auto": "validate",
                "spring.jpa.show-sql": "false",
                "spring.jpa.properties.hibernate.format_sql": "false",
                "spring.jpa.properties.hibernate.jdbc.batch_size": "20",
                "logging.pattern.console": "%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n",
                "logging.level.root": "INFO",
                "logging.level.org.springframework": "INFO",
                "logging.level.org.hibernate": "WARN",
                "management.endpoints.web.exposure.include": "health,info,refresh,metrics",
                "management.endpoint.health.show-details": "always",
                "management.metrics.export.prometheus.enabled": "true",
                "server.shutdown": "graceful",
                "server.compression.enabled": "true",
                "server.tomcat.connection-timeout": "20s",
                "server.tomcat.threads.max": "200",
                "server.tomcat.threads.min-spare": "10"
            }
        }
    ]
}


class TestInterpolation:
    """Tests for the _interpolate function"""

    def test_interpolate_with_existing_env_var(self):
        """Test that environment variables are correctly interpolated"""
        os.environ['TEST_VAR'] = 'test_value'
        result = _interpolate('prefix-${TEST_VAR}-suffix')
        assert result == 'prefix-test_value-suffix'
        del os.environ['TEST_VAR']

    def test_interpolate_without_env_var(self):
        """Test that missing environment variables are left as-is"""
        result = _interpolate('${NON_EXISTENT_VAR}')
        assert result == '${NON_EXISTENT_VAR}'

    def test_interpolate_multiple_vars(self):
        """Test interpolation with multiple variables"""
        os.environ['VAR1'] = 'value1'
        os.environ['VAR2'] = 'value2'
        result = _interpolate('${VAR1}-middle-${VAR2}')
        assert result == 'value1-middle-value2'
        del os.environ['VAR1']
        del os.environ['VAR2']

    def test_interpolate_no_vars(self):
        """Test that strings without variables are unchanged"""
        result = _interpolate('plain string')
        assert result == 'plain string'


class TestSpringConfigClient:
    """Tests for the SpringConfigClient class"""

    def test_init_with_defaults(self):
        """Test client initialization with default values"""
        client = SpringConfigClient(
            server_url='http://config-server:8888',
            app_name='test-app'
        )
        assert client.server_url == 'http://config-server:8888'
        assert client.app_name == 'test-app'
        assert client.profile == 'default'
        assert client.auth is None
        assert client.timeout == 10

    def test_init_with_auth(self):
        """Test client initialization with authentication"""
        client = SpringConfigClient(
            server_url='http://config-server:8888',
            app_name='test-app',
            username='admin',
            password='secret'
        )
        assert client.auth == ('admin', 'secret')

    def test_init_strips_trailing_slash(self):
        """Test that trailing slashes are removed from server URL"""
        client = SpringConfigClient(
            server_url='http://config-server:8888/',
            app_name='test-app'
        )
        assert client.server_url == 'http://config-server:8888'

    @patch('spring_config_client.client.requests.get')
    def test_fetch_and_load_success(self, mock_get):
        """Test successful configuration fetch and load"""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = MOCK_CONFIG_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Create client and fetch config
        client = SpringConfigClient(
            server_url='http://config-server:8888',
            app_name='example-service-app',
            profile='production'
        )

        # Clear any existing test env vars
        for key in list(os.environ.keys()):
            if key.startswith('TEST_') or key in ['MY_VAR_FOR_PROD', 'ANOTHER_ONE_WITH_TEMPLATE']:
                del os.environ[key]

        result = client.fetch_and_load()

        # Verify request was made correctly
        mock_get.assert_called_once_with(
            'http://config-server:8888/example-service-app/production',
            auth=None,
            timeout=10
        )

        # Verify merged configuration
        assert 'MY_VAR_FOR_PROD' in result
        assert result['MY_VAR_FOR_PROD'] == 'prod'
        assert 'TEST_ENV_VAR' in result
        assert result['TEST_ENV_VAR'] == 'test'
        assert 'spring.jpa.hibernate.ddl-auto' in result

        # Verify environment variables were set
        assert os.environ['MY_VAR_FOR_PROD'] == 'prod'
        assert os.environ['TEST_ENV_VAR'] == 'test'
        assert os.environ['logging.level.root'] == 'WARN'  # Should be overridden by production profile

    @patch('spring_config_client.client.requests.get')
    def test_fetch_and_load_with_interpolation(self, mock_get):
        """Test that environment variable interpolation works during fetch"""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = MOCK_CONFIG_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Set environment variable for interpolation
        os.environ['SOME_LOCAL_VAR'] = 'local_value'

        client = SpringConfigClient(
            server_url='http://config-server:8888',
            app_name='example-service-app',
            profile='production'
        )

        result = client.fetch_and_load()

        # Verify interpolation occurred
        assert os.environ['ANOTHER_ONE_WITH_TEMPLATE'] == 'local_value-prod'

        # Cleanup
        del os.environ['SOME_LOCAL_VAR']

    @patch('spring_config_client.client.requests.get')
    def test_fetch_and_load_with_auth(self, mock_get):
        """Test fetch with authentication credentials"""
        mock_response = Mock()
        mock_response.json.return_value = MOCK_CONFIG_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = SpringConfigClient(
            server_url='http://config-server:8888',
            app_name='example-service-app',
            profile='production',
            username='admin',
            password='secret'
        )

        client.fetch_and_load()

        # Verify auth was passed
        mock_get.assert_called_once_with(
            'http://config-server:8888/example-service-app/production',
            auth=('admin', 'secret'),
            timeout=10
        )

    @patch('spring_config_client.client.requests.get')
    def test_fetch_and_load_connection_error(self, mock_get):
        """Test handling of connection errors"""
        mock_get.side_effect = requests.ConnectionError('Connection refused')

        client = SpringConfigClient(
            server_url='http://config-server:8888',
            app_name='example-service-app'
        )

        with pytest.raises(requests.ConnectionError):
            client.fetch_and_load()

    @patch('spring_config_client.client.requests.get')
    def test_fetch_and_load_http_error(self, mock_get):
        """Test handling of HTTP errors"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError('404 Not Found')
        mock_get.return_value = mock_response

        client = SpringConfigClient(
            server_url='http://config-server:8888',
            app_name='nonexistent-app'
        )

        with pytest.raises(requests.HTTPError):
            client.fetch_and_load()

    @patch('spring_config_client.client.requests.get')
    def test_property_source_priority(self, mock_get):
        """Test that property sources are merged with correct priority"""
        # Create a config with overlapping properties
        mock_config = {
            "name": "test-app",
            "profiles": ["production"],
            "propertySources": [
                {
                    "name": "high-priority",
                    "source": {
                        "shared.property": "high-priority-value",
                        "unique.high": "high"
                    }
                },
                {
                    "name": "low-priority",
                    "source": {
                        "shared.property": "low-priority-value",
                        "unique.low": "low"
                    }
                }
            ]
        }

        mock_response = Mock()
        mock_response.json.return_value = mock_config
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = SpringConfigClient(
            server_url='http://config-server:8888',
            app_name='test-app'
        )

        result = client.fetch_and_load()

        # First source should override second (higher priority)
        assert result['shared.property'] == 'high-priority-value'
        assert result['unique.high'] == 'high'
        assert result['unique.low'] == 'low'

    @patch('spring_config_client.client.requests.get')
    def test_custom_timeout(self, mock_get):
        """Test that custom timeout is used"""
        mock_response = Mock()
        mock_response.json.return_value = MOCK_CONFIG_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = SpringConfigClient(
            server_url='http://config-server:8888',
            app_name='test-app',
            timeout=30
        )

        client.fetch_and_load()

        # Verify custom timeout was used
        mock_get.assert_called_once_with(
            'http://config-server:8888/test-app/default',
            auth=None,
            timeout=30
        )