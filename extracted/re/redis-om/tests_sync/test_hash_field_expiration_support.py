from unittest import mock

import pytest
from redis.exceptions import RedisError

from redis_om.model.model import supports_hash_field_expiration

from .conftest import py_test_mark_sync


@py_test_mark_sync
@pytest.mark.parametrize(
    ("server_version", "expected"),
    [("7.2.14", False), ("7.4.0", True), ("8.0.0", True)],
)
def test_supports_hash_field_expiration_checks_server_version(server_version, expected):
    conn = mock.Mock()
    conn.info.return_value = {"redis_version": server_version}

    assert supports_hash_field_expiration(conn) is expected
    assert supports_hash_field_expiration(conn) is expected
    conn.info.assert_called_once_with("server")


@py_test_mark_sync
def test_supports_hash_field_expiration_does_not_share_cache_between_connections():
    first_conn = mock.Mock()
    first_conn.info.return_value = {"redis_version": "7.4.0"}
    second_conn = mock.Mock()
    second_conn.info.return_value = {"redis_version": "7.4.0"}

    assert supports_hash_field_expiration(first_conn) is True
    assert supports_hash_field_expiration(second_conn) is True

    first_conn.info.assert_called_once_with("server")
    second_conn.info.assert_called_once_with("server")


@py_test_mark_sync
def test_supports_hash_field_expiration_retries_after_info_error():
    conn = mock.Mock()
    conn.info.side_effect = [
        RedisError("temporary failure"),
        {"redis_version": "7.4.0"},
    ]

    assert supports_hash_field_expiration(conn) is False
    assert supports_hash_field_expiration(conn) is True
    assert supports_hash_field_expiration(conn) is True
    assert conn.info.call_count == 2
