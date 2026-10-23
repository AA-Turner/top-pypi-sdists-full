import os
import re
import ssl
import types

from decimal import Decimal
from ssl import CERT_NONE, CERT_REQUIRED, TLSVersion
from unittest import mock

import pytest
import urllib3

import snowflake.core._http_requests as http

from snowflake.core._common import TokenType
from snowflake.core.exceptions import SnowflakePythonError


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
    http._create_ssl_context.cache_clear()
    try:
        yield
    finally:
        http.MANAGERS.clear()
        http.MANAGERS.update(original)
        http._create_ssl_context.cache_clear()


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


@pytest.mark.parametrize(
    ("value", "expected"),
    (
        ("1.2", TLSVersion.TLSv1_2),
        ("1.3", TLSVersion.TLSv1_3),
        ("TLSv1.2", TLSVersion.TLSv1_2),
        ("TLSv1.3", TLSVersion.TLSv1_3),
        ("tlsv1.3", TLSVersion.TLSv1_3),
        ("TLSV1.3", TLSVersion.TLSv1_3),
        ("  1.3\n", TLSVersion.TLSv1_3),
    ),
)
def test_pool_uses_min_tls_version_from_env(monkeypatch, pool_for, value, expected):
    monkeypatch.setenv("SNOWFLAKE_MIN_TLS_VERSION", value)
    assert pool_for(_make_configuration()).ssl_minimum_version == expected


@pytest.mark.parametrize("value", (None, "", "   "))
def test_unset_min_tls_version_leaves_pool_options_unchanged(monkeypatch, pool_for, value):
    if value is None:
        monkeypatch.delenv("SNOWFLAKE_MIN_TLS_VERSION", raising=False)
    else:
        monkeypatch.setenv("SNOWFLAKE_MIN_TLS_VERSION", value)

    assert "ssl_minimum_version" not in http._pool_kwargs(_make_configuration())
    assert pool_for(_make_configuration()).ssl_minimum_version is None


@pytest.mark.parametrize("value", ("1.1", "TLSv1.1", "1", "tls1.3", "TLSv1_3", "1.2,1.3"))
def test_invalid_min_tls_version_is_rejected_when_creating_a_pool(monkeypatch, value):
    monkeypatch.setenv("SNOWFLAKE_MIN_TLS_VERSION", f" {value} ")
    message = f"Invalid SNOWFLAKE_MIN_TLS_VERSION value {value!r}. Supported values: 1.2, 1.3, tlsv1.2, tlsv1.3."

    with pytest.raises(SnowflakePythonError, match=re.escape(message)):
        http.create_connection_pool(_make_configuration())


def test_min_tls_version_is_read_whenever_a_pool_is_created(monkeypatch):
    monkeypatch.setenv("SNOWFLAKE_MIN_TLS_VERSION", "1.3")
    http.create_connection_pool(_make_configuration())

    monkeypatch.setenv("SNOWFLAKE_MIN_TLS_VERSION", "bogus")
    with pytest.raises(SnowflakePythonError, match="Invalid SNOWFLAKE_MIN_TLS_VERSION value 'bogus'"):
        http.create_connection_pool(_make_configuration())


def test_pools_are_isolated_by_min_tls_version(monkeypatch, pool_for):
    monkeypatch.delenv("SNOWFLAKE_MIN_TLS_VERSION", raising=False)
    default = pool_for(_make_configuration())
    monkeypatch.setenv("SNOWFLAKE_MIN_TLS_VERSION", "1.3")
    tls13 = pool_for(_make_configuration())
    monkeypatch.setenv("SNOWFLAKE_MIN_TLS_VERSION", "TLSv1.3")
    tls13_again = pool_for(_make_configuration())

    assert default is not tls13
    assert tls13 is tls13_again


TLS12_CIPHER = "ECDHE-RSA-AES256-GCM-SHA384"
TLS13_SUITE = "TLS_AES_256_GCM_SHA384"
needs_set_ciphersuites = pytest.mark.skipif(
    not http._HAS_SET_CIPHERSUITES, reason="SSLContext.set_ciphersuites() needs Python 3.15+"
)


@pytest.mark.parametrize(
    ("value", "expected"),
    (
        (TLS12_CIPHER, http._CipherPolicy(tls12=TLS12_CIPHER, tls13=None)),
        (TLS13_SUITE, http._CipherPolicy(tls12=None, tls13=TLS13_SUITE)),
        (
            f" {TLS12_CIPHER} : {TLS13_SUITE} ::ECDHE-ECDSA-AES256-GCM-SHA384:TLS_AES_128_GCM_SHA256\n",
            http._CipherPolicy(
                tls12=f"{TLS12_CIPHER}:ECDHE-ECDSA-AES256-GCM-SHA384", tls13=f"{TLS13_SUITE}:TLS_AES_128_GCM_SHA256"
            ),
        ),
    ),
)
def test_tls_ciphers_are_split_by_tls_version(monkeypatch, value, expected):
    monkeypatch.setattr(http, "_HAS_SET_CIPHERSUITES", True)
    monkeypatch.setenv("SNOWFLAKE_TLS_CIPHERS", value)
    assert http._resolve_tls_ciphers() == expected


@pytest.mark.parametrize("value", (None, "", "   "))
def test_unset_tls_ciphers_leave_pool_options_unchanged(monkeypatch, value):
    if value is None:
        monkeypatch.delenv("SNOWFLAKE_TLS_CIPHERS", raising=False)
    else:
        monkeypatch.setenv("SNOWFLAKE_TLS_CIPHERS", value)

    assert "ssl_context" not in http._pool_kwargs(_make_configuration())


@pytest.mark.parametrize("value", (":", " : :: ", ":\t:"))
def test_tls_ciphers_without_names_are_rejected(monkeypatch, value):
    monkeypatch.setenv("SNOWFLAKE_TLS_CIPHERS", value)

    with pytest.raises(SnowflakePythonError, match="Invalid SNOWFLAKE_TLS_CIPHERS value .*: no cipher names found."):
        http.create_connection_pool(_make_configuration())


def test_tls13_suites_are_rejected_without_set_ciphersuites(monkeypatch):
    monkeypatch.setattr(http, "_HAS_SET_CIPHERSUITES", False)
    monkeypatch.setenv("SNOWFLAKE_TLS_CIPHERS", f"{TLS12_CIPHER}:{TLS13_SUITE}")
    message = (
        f"SNOWFLAKE_TLS_CIPHERS lists TLS 1.3 cipher suites ('{TLS13_SUITE}'), which require Python 3.15 or later."
    )

    with pytest.raises(SnowflakePythonError, match=re.escape(message)):
        http.create_connection_pool(_make_configuration())


def test_ssl_context_restricts_tls12_ciphers(monkeypatch, pool_for):
    monkeypatch.setenv("SNOWFLAKE_TLS_CIPHERS", TLS12_CIPHER)
    context = pool_for(_make_configuration()).conn_kw["ssl_context"]
    # A TLS 1.2 cipher list leaves the TLS 1.3 suites at OpenSSL's default.
    default_tls13 = _get_ciphers(http.create_urllib3_context(), "TLSv1.3")

    assert _get_ciphers(context, "TLSv1.2") == {TLS12_CIPHER}
    assert _get_ciphers(context, "TLSv1.3") == default_tls13


@needs_set_ciphersuites
def test_ssl_context_restricts_tls13_suites(monkeypatch, pool_for):
    monkeypatch.setenv("SNOWFLAKE_TLS_CIPHERS", TLS13_SUITE)
    context = pool_for(_make_configuration()).conn_kw["ssl_context"]
    # A TLS 1.3 cipher list leaves the TLS 1.2 ciphers at OpenSSL's default.
    default_tls12 = _get_ciphers(http.create_urllib3_context(), "TLSv1.2")

    assert _get_ciphers(context, "TLSv1.3") == {TLS13_SUITE}
    assert _get_ciphers(context, "TLSv1.2") == default_tls12


def test_ssl_context_applies_min_tls_version(monkeypatch, pool_for):
    monkeypatch.setenv("SNOWFLAKE_TLS_CIPHERS", TLS12_CIPHER)
    monkeypatch.setenv("SNOWFLAKE_MIN_TLS_VERSION", "1.3")

    assert pool_for(_make_configuration()).conn_kw["ssl_context"].minimum_version == TLSVersion.TLSv1_3


def test_unusable_tls12_ciphers_are_rejected(monkeypatch):
    monkeypatch.setenv("SNOWFLAKE_TLS_CIPHERS", "BOGUS:ALSO-BOGUS")

    with pytest.raises(ssl.SSLError):
        http.create_connection_pool(_make_configuration())


@needs_set_ciphersuites
def test_unusable_tls13_suites_are_rejected(monkeypatch):
    monkeypatch.setenv("SNOWFLAKE_TLS_CIPHERS", "TLS_BOGUS")

    with pytest.raises(ssl.SSLError):
        http.create_connection_pool(_make_configuration())


def test_ssl_contexts_are_shared_only_between_equal_tls_options(monkeypatch, pool_for):
    monkeypatch.setenv("SNOWFLAKE_TLS_CIPHERS", TLS12_CIPHER)
    first = pool_for(_make_configuration())
    equal = pool_for(_make_configuration())
    other_ca = pool_for(_make_configuration(ssl_ca_cert="/custom/ca.pem"))
    insecure = pool_for(_make_configuration(verify_ssl=False))
    other_hostname = pool_for(_make_configuration(assert_hostname=False))
    monkeypatch.setenv("SNOWFLAKE_TLS_CIPHERS", "ECDHE-ECDSA-AES256-GCM-SHA384")
    other_ciphers = pool_for(_make_configuration())

    assert first is equal
    for other in (other_ca, insecure, other_hostname, other_ciphers):
        assert other is not first
        assert other.conn_kw["ssl_context"] is not first.conn_kw["ssl_context"]


@pytest.mark.parametrize(
    "overrides",
    (
        {"retries": urllib3.Retry(3)},
        {"socket_options": [(6, 1, 1)]},
        {"connection_pool_maxsize": 8},
    ),
)
def test_ssl_contexts_are_shared_across_non_tls_options(monkeypatch, pool_for, overrides):
    monkeypatch.setenv("SNOWFLAKE_TLS_CIPHERS", TLS12_CIPHER)
    first = pool_for(_make_configuration())
    other = pool_for(_make_configuration(**overrides))

    assert other is not first
    assert other.conn_kw["ssl_context"] is first.conn_kw["ssl_context"]


@pytest.mark.parametrize(
    ("variable", "value", "message"),
    (
        ("SNOWFLAKE_MIN_TLS_VERSION", "1.1", "Invalid SNOWFLAKE_MIN_TLS_VERSION value '1.1'"),
        ("SNOWFLAKE_TLS_CIPHERS", ":", "no cipher names found"),
    ),
)
def test_validate_tls_settings_rejects_unusable_values(monkeypatch, variable, value, message):
    monkeypatch.setenv(variable, value)

    with pytest.raises(SnowflakePythonError, match=message):
        http._validate_tls_settings()


def _get_ciphers(context, protocol):
    names = {cipher["name"] for cipher in context.get_ciphers() if cipher["protocol"] == "TLSv1.3"}
    if protocol == "TLSv1.3":
        return names
    return {cipher["name"] for cipher in context.get_ciphers()} - names


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
