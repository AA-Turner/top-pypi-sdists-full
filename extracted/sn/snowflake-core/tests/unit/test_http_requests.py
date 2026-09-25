import os
import types

from decimal import Decimal
from ssl import CERT_NONE, CERT_REQUIRED
from unittest import mock

import pytest
import urllib3

import snowflake.core._http_requests as http

from snowflake.core._common import TokenType


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


API_URL = "https://acct.snowflakecomputing.com/api/v2/databases"


@pytest.fixture(autouse=True)
def _reset_managers():
    # Ensure the process-wide managers do not leak across tests
    original = http.MANAGERS.copy()
    http.MANAGERS.clear()
    try:
        yield
    finally:
        http.MANAGERS.clear()
        http.MANAGERS.update(original)


@mock.patch.object(http, "_ProxyManager")
@mock.patch.object(http, "_PoolManager")
def test_create_connection_pool_uses_proxy_from_configuration(pool_mock, proxy_mock):
    pool = http.create_connection_pool(
        _make_configuration(proxy="https://proxy.local:8443", proxy_headers={"X-Proxy": "1"})
    )
    assert isinstance(pool, http.SFPoolManager)
    proxy_mock.assert_called_once_with(proxy_url="https://proxy.local:8443", proxy_headers={"X-Proxy": "1"})
    pool_mock.assert_not_called()


@mock.patch.dict(os.environ, {"HTTPS_PROXY": "https://env-proxy:3128"}, clear=False)
@mock.patch.object(http, "_ProxyManager")
@mock.patch.object(http, "_PoolManager")
def test_create_connection_pool_uses_proxy_from_env(pool_mock, proxy_mock):
    pool = http.create_connection_pool(_make_configuration())
    assert isinstance(pool, http.SFPoolManager)
    proxy_mock.assert_called_once_with(proxy_url="https://env-proxy:3128", proxy_headers={})
    pool_mock.assert_not_called()


@mock.patch.object(http, "_ProxyManager")
@mock.patch.object(http, "_PoolManager")
def test_create_connection_pool_without_proxy(pool_mock, proxy_mock):
    pool = http.create_connection_pool(_make_configuration())
    assert isinstance(pool, http.SFPoolManager)
    proxy_mock.assert_not_called()
    pool_mock.assert_called_once()


@mock.patch.dict(os.environ, {"https_proxy": "https://lower-proxy:3128"}, clear=False)
@mock.patch.object(http, "_ProxyManager")
@mock.patch.object(http, "_PoolManager")
def test_create_connection_pool_uses_proxy_from_lowercase_env(pool_mock, proxy_mock):
    http.create_connection_pool(_make_configuration())
    proxy_mock.assert_called()
    _, kwargs = proxy_mock.call_args
    assert kwargs["proxy_url"] == "https://lower-proxy:3128"
    pool_mock.assert_not_called()


def test_managers_are_keyed_by_proxy():
    direct = http.create_connection_pool(_make_configuration())
    proxied = http.create_connection_pool(_make_configuration(proxy="https://a.proxy:8443"))
    same_proxy = http.create_connection_pool(_make_configuration(proxy="https://a.proxy:8443"))
    other_proxy = http.create_connection_pool(_make_configuration(proxy="https://b.proxy:8443"))

    assert proxied._manager is same_proxy._manager
    assert proxied._manager is not other_proxy._manager
    assert direct._manager is not proxied._manager
    assert proxied._manager.proxy.host == "a.proxy"
    assert direct._manager.proxy is None


def test_pools_are_isolated_by_verify_ssl(pool_for):
    secure = pool_for(_make_configuration(verify_ssl=True))
    insecure = pool_for(_make_configuration(verify_ssl=False))

    assert secure is not insecure
    assert secure.cert_reqs == CERT_REQUIRED
    assert insecure.cert_reqs == CERT_NONE


def test_equivalent_configurations_share_a_pool(pool_for):
    assert pool_for(_make_configuration()) is pool_for(_make_configuration())


@mock.patch.dict(os.environ, {"SSL_CERT_FILE": "/etc/ssl/cert_file.pem"}, clear=False)
def test_pool_uses_ssl_cert_file_from_env(pool_for):
    assert pool_for(_make_configuration()).ca_certs == "/etc/ssl/cert_file.pem"


@mock.patch.dict(os.environ, {"ssl_cert_file": "/etc/ssl/lower_cert_file.pem"}, clear=False)
def test_pool_uses_ssl_cert_file_from_lowercase_env(pool_for):
    assert pool_for(_make_configuration()).ca_certs == "/etc/ssl/lower_cert_file.pem"


def test_pool_uses_ssl_ca_cert_from_configuration(pool_for):
    assert pool_for(_make_configuration(ssl_ca_cert="/custom/ca.pem")).ca_certs == "/custom/ca.pem"


def test_pool_uses_client_certificate_and_assert_hostname_from_configuration(pool_for):
    pool = pool_for(_make_configuration(cert_file="/client.pem", key_file="/client.key", assert_hostname=False))

    assert pool.cert_file == "/client.pem"
    assert pool.key_file == "/client.key"
    assert pool.assert_hostname is False


def test_pool_maxsize_comes_from_configuration(pool_for):
    assert pool_for(_make_configuration(connection_pool_maxsize=17)).pool.maxsize == 17


def test_pool_options_do_not_outlive_a_request(pool_for):
    pool_for(_make_configuration())

    assert http._POOL_KWARGS.get() is None


def test_sanitize_for_serialization():
    assert http.sanitize_for_serialization(Decimal("1.23")) == "1.23"


@pytest.fixture
def pool_for(monkeypatch):
    """Return a helper giving the pool a configuration sends its requests over.

    The pool is the one the manager resolves for a real request, with only the send itself
    stubbed out, so nothing here opens a socket.
    """
    pools = []

    def fake_urlopen(pool, method, target, **kwargs):
        pools.append(pool)
        return types.SimpleNamespace(status=200, headers={}, data=b"{}", get_redirect_location=lambda: None)

    monkeypatch.setattr(urllib3.HTTPSConnectionPool, "urlopen", fake_urlopen)

    def resolve(configuration, url=API_URL):
        http.create_connection_pool(configuration).request(_make_root(), "GET", url)
        return pools[-1]

    return resolve


def _make_root():
    return types.SimpleNamespace(
        _session_token="session-token", token_type=TokenType.SESSION_TOKEN, external_session_id=None
    )


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
