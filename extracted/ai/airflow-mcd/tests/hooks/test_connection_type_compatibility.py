"""
Tests for connection type backward compatibility between Airflow versions.

These tests ensure that both the new RFC3986-compliant connection type (mcd-gateway)
and the legacy connection type (mcd_gateway) work correctly across Airflow versions.
"""
import json
from unittest import TestCase
from unittest.mock import patch, Mock

from airflow.models import Connection
from pycarlo.core import Session

from airflow_mcd.hooks import SessionHook, GatewaySessionHook
from airflow_mcd.hooks.constants import (
    MCD_GATEWAY_CONNECTION_TYPE,
    MCD_GATEWAY_CONNECTION_TYPE_LEGACY,
    MCD_GATEWAY_SCOPE,
    MCD_GATEWAY_HOSTS,
)

SAMPLE_ID = 'test_id'
SAMPLE_TOKEN = 'test_token'


class ConnectionTypeCompatibilityTest(TestCase):
    """Test connection type compatibility across Airflow versions."""

    def test_constants_defined(self):
        """Verify that both connection type constants are defined."""
        self.assertEqual(MCD_GATEWAY_CONNECTION_TYPE, "mcd-gateway")
        self.assertEqual(MCD_GATEWAY_CONNECTION_TYPE_LEGACY, "mcd_gateway")

    def test_is_gateway_connection_with_new_type(self):
        """Test that the new RFC3986-compliant connection type is recognized."""
        hook = SessionHook(mcd_session_conn_id='test')
        
        # Test with new connection type (mcd-gateway)
        result = hook._is_gateway_connection(
            connection_type=MCD_GATEWAY_CONNECTION_TYPE,
            host=None
        )
        self.assertTrue(result, "New connection type (mcd-gateway) should be recognized as gateway")

    def test_is_gateway_connection_with_legacy_type(self):
        """Test that the legacy connection type is still recognized for backward compatibility."""
        hook = SessionHook(mcd_session_conn_id='test')
        
        # Test with legacy connection type (mcd_gateway)
        result = hook._is_gateway_connection(
            connection_type=MCD_GATEWAY_CONNECTION_TYPE_LEGACY,
            host=None
        )
        self.assertTrue(result, "Legacy connection type (mcd_gateway) should be recognized as gateway")

    def test_is_gateway_connection_with_http_fallback(self):
        """Test that HTTP connections with gateway hosts are recognized."""
        hook = SessionHook(mcd_session_conn_id='test')
        
        # Test with HTTP type but gateway host
        for host in MCD_GATEWAY_HOSTS:
            result = hook._is_gateway_connection(
                connection_type='http',
                host=f'https://{host}/path'
            )
            self.assertTrue(result, f"HTTP connection with host {host} should be recognized as gateway")

    def test_is_gateway_connection_with_non_gateway_type(self):
        """Test that non-gateway connection types are not recognized."""
        hook = SessionHook(mcd_session_conn_id='test')
        
        # Test with regular mcd type
        result = hook._is_gateway_connection(
            connection_type='mcd',
            host=None
        )
        self.assertFalse(result, "Regular mcd connection type should not be recognized as gateway")

    @patch('airflow_mcd.hooks.session_hook.Session')
    @patch.object(SessionHook, 'get_connection')
    def test_get_conn_with_new_gateway_type(self, get_connection_mock, session_mock):
        """Test that connections with new gateway type get proper scope."""
        hook = SessionHook(mcd_session_conn_id='test')
        
        # Mock connection with new gateway type
        get_connection_mock.return_value = Connection(
            conn_type=MCD_GATEWAY_CONNECTION_TYPE,
            host=f'https://{MCD_GATEWAY_HOSTS[0]}',
            login=SAMPLE_ID,
            password=SAMPLE_TOKEN
        )
        expected_session = Session(
            mcd_id=SAMPLE_ID,
            mcd_token=SAMPLE_TOKEN,
            endpoint=f'https://{MCD_GATEWAY_HOSTS[0]}/graphql',
            scope=MCD_GATEWAY_SCOPE
        )
        session_mock.return_value = expected_session

        result = hook.get_conn()
        
        self.assertEqual(result, expected_session)
        session_mock.assert_called_once_with(
            endpoint=f'https://{MCD_GATEWAY_HOSTS[0]}/graphql',
            mcd_id=SAMPLE_ID,
            mcd_token=SAMPLE_TOKEN,
            scope=MCD_GATEWAY_SCOPE
        )

    @patch('airflow_mcd.hooks.session_hook.Session')
    @patch.object(SessionHook, 'get_connection')
    def test_get_conn_with_legacy_gateway_type(self, get_connection_mock, session_mock):
        """Test that connections with legacy gateway type still work and get proper scope."""
        hook = SessionHook(mcd_session_conn_id='test')
        
        # Mock connection with legacy gateway type
        get_connection_mock.return_value = Connection(
            conn_type=MCD_GATEWAY_CONNECTION_TYPE_LEGACY,
            host=f'https://{MCD_GATEWAY_HOSTS[0]}',
            login=SAMPLE_ID,
            password=SAMPLE_TOKEN
        )
        expected_session = Session(
            mcd_id=SAMPLE_ID,
            mcd_token=SAMPLE_TOKEN,
            endpoint=f'https://{MCD_GATEWAY_HOSTS[0]}/graphql',
            scope=MCD_GATEWAY_SCOPE
        )
        session_mock.return_value = expected_session

        result = hook.get_conn()
        
        self.assertEqual(result, expected_session)
        session_mock.assert_called_once_with(
            endpoint=f'https://{MCD_GATEWAY_HOSTS[0]}/graphql',
            mcd_id=SAMPLE_ID,
            mcd_token=SAMPLE_TOKEN,
            scope=MCD_GATEWAY_SCOPE
        )

    def test_gateway_hook_uses_new_connection_type(self):
        """Test that GatewaySessionHook uses the new RFC3986-compliant connection type."""
        # This ensures new connections created through the UI will use the new type
        self.assertEqual(
            GatewaySessionHook.conn_type,
            MCD_GATEWAY_CONNECTION_TYPE,
            "GatewaySessionHook should use the new RFC3986-compliant connection type"
        )

    @patch('airflow_mcd.hooks.session_hook.Session')
    @patch.object(GatewaySessionHook, 'get_connection')
    def test_gateway_hook_accepts_both_connection_types(self, get_connection_mock, session_mock):
        """Test that GatewaySessionHook works with both new and legacy connection types."""
        
        for conn_type in [MCD_GATEWAY_CONNECTION_TYPE, MCD_GATEWAY_CONNECTION_TYPE_LEGACY]:
            with self.subTest(conn_type=conn_type):
                hook = GatewaySessionHook(mcd_session_conn_id='test')
                
                get_connection_mock.return_value = Connection(
                    conn_type=conn_type,
                    host=f'https://{MCD_GATEWAY_HOSTS[0]}',
                    login=SAMPLE_ID,
                    password=SAMPLE_TOKEN
                )
                expected_session = Session(
                    mcd_id=SAMPLE_ID,
                    mcd_token=SAMPLE_TOKEN,
                    endpoint=f'https://{MCD_GATEWAY_HOSTS[0]}/graphql',
                    scope=MCD_GATEWAY_SCOPE
                )
                session_mock.return_value = expected_session

                result = hook.get_conn()
                
                self.assertEqual(result, expected_session)
                # Both connection types should result in gateway scope being set
                session_mock.assert_called_with(
                    endpoint=f'https://{MCD_GATEWAY_HOSTS[0]}/graphql',
                    mcd_id=SAMPLE_ID,
                    mcd_token=SAMPLE_TOKEN,
                    scope=MCD_GATEWAY_SCOPE
                )
                
                # Reset mocks for next iteration
                get_connection_mock.reset_mock()
                session_mock.reset_mock()

    def test_connection_type_does_not_contain_underscore(self):
        """Test that the primary connection type is RFC3986 compliant (no underscores)."""
        self.assertNotIn(
            '_',
            MCD_GATEWAY_CONNECTION_TYPE,
            "New connection type should not contain underscores (RFC3986 compliance)"
        )

    def test_legacy_connection_type_contains_underscore(self):
        """Test that the legacy connection type is identified correctly."""
        self.assertIn(
            '_',
            MCD_GATEWAY_CONNECTION_TYPE_LEGACY,
            "Legacy connection type should contain underscore for backward compatibility"
        )


class ProviderInfoTest(TestCase):
    """Test that provider info is correctly configured."""

    def test_provider_info_structure(self):
        """Test that get_provider_info returns the expected structure."""
        from airflow_mcd import get_provider_info
        
        provider_info = get_provider_info()
        
        self.assertIn('connection-types', provider_info)
        self.assertIn('hook-class-names', provider_info)
        self.assertEqual(provider_info['package-name'], 'airflow-mcd')

    def test_gateway_connection_registered_with_new_type(self):
        """Test that the gateway connection is registered with the new RFC3986-compliant type."""
        from airflow_mcd import get_provider_info
        
        provider_info = get_provider_info()
        connection_types = provider_info['connection-types']
        
        # Find the gateway connection registration
        gateway_connections = [
            ct for ct in connection_types
            if 'GatewaySessionHook' in ct['hook-class-name']
        ]
        
        # Should have exactly one gateway connection registered
        self.assertEqual(
            len(gateway_connections),
            1,
            "Should have exactly one gateway connection registered to avoid UI confusion"
        )
        
        # It should use the new connection type
        gateway_conn = gateway_connections[0]
        self.assertEqual(
            gateway_conn['connection-type'],
            MCD_GATEWAY_CONNECTION_TYPE,
            "Gateway connection should be registered with new RFC3986-compliant type"
        )

    def test_legacy_connection_type_not_registered(self):
        """Test that the legacy connection type is not registered in provider info."""
        from airflow_mcd import get_provider_info
        
        provider_info = get_provider_info()
        connection_types = provider_info['connection-types']
        
        # Legacy type should not be in the registered connection types
        legacy_registrations = [
            ct for ct in connection_types
            if ct['connection-type'] == MCD_GATEWAY_CONNECTION_TYPE_LEGACY
        ]
        
        self.assertEqual(
            len(legacy_registrations),
            0,
            "Legacy connection type should not be registered to avoid duplicate UI entries"
        )

