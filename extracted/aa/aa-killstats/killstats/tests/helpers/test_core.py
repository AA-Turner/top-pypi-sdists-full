"""Unit tests for helpers.core module."""

# Standard Library
from unittest.mock import Mock, patch

# AA Killstats
from killstats.helpers.core import (
    get_redis_client,
)
from killstats.tests import AuthTestCase

MODULE_PATH = "killstats.helpers.core"


class TestCoreHelpers(AuthTestCase):
    def test_get_redis_client_should_return_django_redis_connection(self):
        # Test Data
        mock_conn = Mock()

        # Test Action
        with patch(
            f"{MODULE_PATH}.django_redis.get_redis_connection",
            return_value=mock_conn,
        ) as mock_get_conn:
            client = get_redis_client()

        # Expected Result
        self.assertEqual(client, mock_conn)
        mock_get_conn.assert_called_once_with("default")

    def test_get_redis_client_should_fallback_to_caches_on_attribute_error(
        self,
    ):
        # Test Data
        mock_master_client = Mock()
        mock_cache = Mock()
        mock_cache.get_master_client.return_value = mock_master_client

        # Test Action
        with (
            patch(
                f"{MODULE_PATH}.django_redis.get_redis_connection",
                side_effect=AttributeError,
            ),
            patch(f"{MODULE_PATH}.caches", {"default": mock_cache}),
        ):
            client = get_redis_client()

        # Expected Result
        self.assertEqual(client, mock_master_client)
        mock_cache.get_master_client.assert_called_once()
