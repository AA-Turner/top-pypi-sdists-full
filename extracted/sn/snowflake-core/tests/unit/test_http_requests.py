import os
import types

from ssl import CERT_REQUIRED
from unittest import mock

import pytest

import snowflake.core._http_requests


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
    ),
)
def test_resolve_url(inputs, expected_output):
    assert snowflake.core._http_requests.resolve_url(*inputs) == expected_output


@pytest.fixture(autouse=True)
def _reset_connection_pool():
    # Ensure singleton pool does not leak across tests
    http = snowflake.core._http_requests
    original = http.CONNECTION_POOL
    http.CONNECTION_POOL = None
    try:
        yield
    finally:
        http.CONNECTION_POOL = original


@mock.patch.dict(os.environ, {"HTTPS_PROXY": ""}, clear=False)
@mock.patch.object(snowflake.core._http_requests.urllib3, "ProxyManager")
@mock.patch.object(snowflake.core._http_requests.urllib3, "PoolManager")
def test_create_connection_pool_uses_proxy_from_configuration(pool_mock, proxy_mock):
    http = snowflake.core._http_requests

    configuration = types.SimpleNamespace(
        verify_ssl=True,
        ssl_ca_cert=None,
        cert_file=None,
        key_file=None,
        assert_hostname=None,
        retries=None,
        socket_options=None,
        connection_pool_maxsize=None,
        proxy="https://proxy.local:8443",
        proxy_headers={"X-Proxy": "1"},
    )

    pool = http.create_connection_pool(configuration)
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
@mock.patch.object(snowflake.core._http_requests.urllib3, "ProxyManager")
@mock.patch.object(snowflake.core._http_requests.urllib3, "PoolManager")
def test_create_connection_pool_uses_proxy_from_env(pool_mock, proxy_mock):
    http = snowflake.core._http_requests

    configuration = types.SimpleNamespace(
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

    pool = http.create_connection_pool(configuration)
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


@mock.patch.dict(os.environ, {"HTTPS_PROXY": ""}, clear=False)
@mock.patch.object(snowflake.core._http_requests.urllib3, "ProxyManager")
@mock.patch.object(snowflake.core._http_requests.urllib3, "PoolManager")
def test_create_connection_pool_without_proxy(pool_mock, proxy_mock):
    http = snowflake.core._http_requests

    configuration = types.SimpleNamespace(
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

    pool = http.create_connection_pool(configuration)
    assert isinstance(pool, http.SFPoolManager)
    proxy_mock.assert_not_called()
    pool_mock.assert_called_once_with(
        num_pools=4, maxsize=4, cert_reqs=CERT_REQUIRED, ca_certs=None, cert_file=None, key_file=None
    )
