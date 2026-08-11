import os
import types

from decimal import Decimal
from ssl import CERT_REQUIRED
from unittest import mock

import pytest

import snowflake.core._http_requests as http


@pytest.mark.parametrize(
    ("inputs", "expected_output"),
    (
        # Simplest case
        (("simple_url", {}, {}, ""), "simple_url"),
        # Embedding case
        (("databases/{database}", {"database": "asd"}, {}, ""), "databases/asd"),
        # Collections formats
        (
            ("items/{items}", {"items": ["bread", "butter", "cheese", "cold_cuts"]}, {"items": "csv"}, ""),
            "items/bread%2Cbutter%2Ccheese%2Ccold_cuts",
        ),
        # Safe quoting (same as last one, but don't change ',' into '%2C')
        (
            ("items/{items}", {"items": ["bread", "butter", "cheese", "cold_cuts"]}, {"items": "csv"}, ",/"),
            "items/bread,butter,cheese,cold_cuts",
        ),
        # Quoted identifier containing ".." — dots wrapped in percent-encoded quotes, not a dot-segment
        (
            (
                "databases/{database}/schemas/{schema}/tables/{name}",
                {"database": "db", "schema": "public", "name": '".."'},
                {},
                "",
            ),
            "databases/db/schemas/public/tables/%22..%22",
        ),
        # Quoted identifier containing "." — dot wrapped in percent-encoded quotes, not a dot-segment
        (
            ("databases/{database}", {"database": '"."'}, {}, ""),
            "databases/%22.%22",
        ),
    ),
)
def test_resolve_url(inputs, expected_output):
    assert http.resolve_url(*inputs) == expected_output


@pytest.mark.parametrize(
    ("dot_segment", "param_name"),
    (
        (".", "database"),
        ("..", "database"),
        (".", "schema"),
        ("..", "schema"),
        (".", "name"),
        ("..", "name"),
    ),
)
def test_resolve_url_rejects_dot_segments(dot_segment, param_name):
    path = "databases/{database}/schemas/{schema}/tables/{name}"
    params = {"database": "db", "schema": "public", "name": "t"}
    params[param_name] = dot_segment
    with pytest.raises(ValueError, match="may not be '\\.' or '\\.\\.'"):
        http.resolve_url(path, params, {}, "")


@pytest.mark.parametrize("dot_segment", [".", ".."])
def test_path_traversal_rejected_in_table_name(tables, dot_segment):
    with pytest.raises(ValueError, match="may not be"):
        tables[dot_segment].drop()


@pytest.mark.parametrize("dot_segment", [".", ".."])
def test_path_traversal_rejected_in_schema_name(db, dot_segment):
    with pytest.raises(ValueError, match="may not be"):
        db.schemas[dot_segment].tables["mytable"].drop()


@pytest.mark.parametrize("dot_segment", [".", ".."])
def test_path_traversal_rejected_in_database_name(dbs, dot_segment):
    with pytest.raises(ValueError, match="may not be"):
        dbs[dot_segment].schemas["public"].tables["mytable"].drop()


@pytest.fixture(autouse=True)
def _reset_connection_pool():
    # Ensure singleton pool does not leak across tests
    original = http.CONNECTION_POOL
    http.CONNECTION_POOL = None
    try:
        yield
    finally:
        http.CONNECTION_POOL = original


@mock.patch.object(http.urllib3, "ProxyManager")
@mock.patch.object(http.urllib3, "PoolManager")
def test_create_connection_pool_uses_proxy_from_configuration(pool_mock, proxy_mock):
    pool = http.create_connection_pool(
        _make_configuration(proxy="https://proxy.local:8443", proxy_headers={"X-Proxy": "1"})
    )
    assert isinstance(pool, http.SFPoolManager)
    proxy_mock.assert_called_once_with(
        num_pools=4,
        maxsize=4,
        cert_reqs=CERT_REQUIRED,
        ca_certs=None,
        cert_file=None,
        key_file=None,
        proxy_url="https://proxy.local:8443",
        proxy_headers={"X-Proxy": "1"},
    )
    pool_mock.assert_not_called()


@mock.patch.dict(os.environ, {"HTTPS_PROXY": "https://env-proxy:3128"}, clear=False)
@mock.patch.object(http.urllib3, "ProxyManager")
@mock.patch.object(http.urllib3, "PoolManager")
def test_create_connection_pool_uses_proxy_from_env(pool_mock, proxy_mock):
    pool = http.create_connection_pool(_make_configuration())
    assert isinstance(pool, http.SFPoolManager)
    proxy_mock.assert_called_once_with(
        num_pools=4,
        maxsize=4,
        cert_reqs=CERT_REQUIRED,
        ca_certs=None,
        cert_file=None,
        key_file=None,
        proxy_url="https://env-proxy:3128",
        proxy_headers={},
    )
    pool_mock.assert_not_called()


@mock.patch.object(http.urllib3, "ProxyManager")
@mock.patch.object(http.urllib3, "PoolManager")
def test_create_connection_pool_without_proxy(pool_mock, proxy_mock):
    pool = http.create_connection_pool(_make_configuration())
    assert isinstance(pool, http.SFPoolManager)
    proxy_mock.assert_not_called()
    pool_mock.assert_called_once_with(
        num_pools=4, maxsize=4, cert_reqs=CERT_REQUIRED, ca_certs=None, cert_file=None, key_file=None
    )


@mock.patch.dict(os.environ, {"https_proxy": "https://lower-proxy:3128"}, clear=False)
@mock.patch.object(http.urllib3, "ProxyManager")
@mock.patch.object(http.urllib3, "PoolManager")
def test_create_connection_pool_uses_proxy_from_lowercase_env(pool_mock, proxy_mock):
    http.create_connection_pool(_make_configuration())
    proxy_mock.assert_called()
    _, kwargs = proxy_mock.call_args
    assert kwargs["proxy_url"] == "https://lower-proxy:3128"
    pool_mock.assert_not_called()


@mock.patch.dict(os.environ, {"SSL_CERT_FILE": "/etc/ssl/cert_file.pem"}, clear=False)
@mock.patch.object(http.urllib3, "ProxyManager")
@mock.patch.object(http.urllib3, "PoolManager")
def test_create_connection_pool_uses_ssl_cert_file_from_env(pool_mock, proxy_mock):
    http.create_connection_pool(_make_configuration())
    pool_mock.assert_called()
    _, kwargs = pool_mock.call_args
    assert kwargs["ca_certs"] == "/etc/ssl/cert_file.pem"
    proxy_mock.assert_not_called()


@mock.patch.dict(os.environ, {"ssl_cert_file": "/etc/ssl/lower_cert_file.pem"}, clear=False)
@mock.patch.object(http.urllib3, "ProxyManager")
@mock.patch.object(http.urllib3, "PoolManager")
def test_create_connection_pool_uses_ssl_cert_file_from_lowercase_env(pool_mock, proxy_mock):
    http.create_connection_pool(_make_configuration())
    pool_mock.assert_called()
    _, kwargs = pool_mock.call_args
    assert kwargs["ca_certs"] == "/etc/ssl/lower_cert_file.pem"
    proxy_mock.assert_not_called()


@mock.patch.object(http.urllib3, "ProxyManager")
@mock.patch.object(http.urllib3, "PoolManager")
def test_create_connection_pool_uses_ssl_ca_cert_from_configuration(pool_mock, proxy_mock):
    http.create_connection_pool(_make_configuration(ssl_ca_cert="/custom/ca.pem"))
    pool_mock.assert_called()
    _, kwargs = pool_mock.call_args
    assert kwargs["ca_certs"] == "/custom/ca.pem"
    proxy_mock.assert_not_called()


def test_sanitize_for_serialization():
    assert http.sanitize_for_serialization(Decimal("1.23")) == "1.23"


def _make_configuration(**overrides):
    base = dict(
        verify_ssl=True,
        ssl_ca_cert=None,
        cert_file=None,
        key_file=None,
        assert_hostname=None,
        retries=None,
        socket_options=None,
        connection_pool_maxsize=None,
        proxy=None,
        proxy_headers=None,
    )
    base.update(overrides)
    return types.SimpleNamespace(**base)
