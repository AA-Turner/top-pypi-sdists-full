import ssl

import httpx
import pytest
from pydantic import SecretStr

from mistralai.workflows.client import _get_async_client, _get_sync_client, get_mistral_client
from mistralai.workflows.core.auth import StaticTokenProvider
from mistralai.workflows.core.config.config import AppConfig, HttpConfig, _loggable_config, config
from mistralai.workflows.core.worker_client import get_worker_client
from mistralai.workflows.hooks.executor_credentials_hook import (
    AsyncExecutorCredentialsHook,
    SyncExecutorCredentialsHook,
)

_CLIENT_FACTORIES = [
    pytest.param(_get_async_client, id="async"),
    pytest.param(_get_sync_client, id="sync"),
]


@pytest.fixture(autouse=True)
def reset_http_config():
    original = config.http
    config.http = HttpConfig()
    yield config.http
    config.http = original


def _client(get_client) -> httpx.Client | httpx.AsyncClient:
    return get_client(server_url="http://localhost")


def _proxy_origin(transport) -> tuple[bytes, bytes, int] | None:
    proxy_url = getattr(transport._pool, "_proxy_url", None)
    if proxy_url is None:
        return None
    return proxy_url.scheme, proxy_url.host, proxy_url.port


def _route_to(client: httpx.Client | httpx.AsyncClient, url: str) -> tuple[bytes, bytes, int] | None:
    return _proxy_origin(client._transport_for_url(httpx.URL(url)))


def _verifies(transport) -> bool:
    return transport._pool._ssl_context.verify_mode is not ssl.CERT_NONE


_CORP_PROXY = (b"http", b"corp-proxy", 3128)
_EU_PROXY = (b"http", b"eu-proxy", 3128)
_ENV_PROXY = (b"http", b"env-proxy", 1111)


class TestDefaults:
    @pytest.mark.parametrize("get_client", _CLIENT_FACTORIES)
    def test_the_environment_proxies_are_still_honoured(self, get_client, monkeypatch):
        monkeypatch.setenv("HTTPS_PROXY", "http://env-proxy:1111")

        assert _route_to(_client(get_client), "https://api.mistral.ai/v1") == _ENV_PROXY

    @pytest.mark.parametrize("get_client", _CLIENT_FACTORIES)
    def test_timeout_defaults_to_sixty_seconds(self, get_client):
        assert _client(get_client).timeout.connect == 60.0


class TestProxy:
    @pytest.mark.parametrize("get_client", _CLIENT_FACTORIES)
    def test_proxy_reaches_the_client_transport(self, get_client):
        config.http.proxy = "http://corp-proxy:3128"

        assert _proxy_origin(_client(get_client)._transport) == _CORP_PROXY

    @pytest.mark.parametrize(
        "hook_cls,attribute",
        [
            pytest.param(AsyncExecutorCredentialsHook, "async_client", id="async"),
            pytest.param(SyncExecutorCredentialsHook, "client", id="sync"),
        ],
    )
    def test_proxy_reaches_the_executor_credentials_clients(self, hook_cls, attribute):
        config.http.proxy = "http://corp-proxy:3128"

        hook = hook_cls(server_url="http://localhost", token_provider=StaticTokenProvider("test-key"))

        httpx_client = getattr(hook._worker_client.sdk_configuration, attribute)
        assert _proxy_origin(httpx_client._transport) == _CORP_PROXY

    async def test_proxy_reaches_the_worker_client(self):
        config.http.proxy = "http://corp-proxy:3128"

        async with get_worker_client(base_url="http://localhost", api_key="test-key") as client:
            httpx_client = client.sdk_configuration.async_client

        assert _proxy_origin(httpx_client._transport) == _CORP_PROXY

    @pytest.mark.parametrize("get_client", _CLIENT_FACTORIES)
    def test_the_sdk_owned_arguments_survive(self, get_client):
        config.http.proxy = "http://corp-proxy:3128"

        client = _client(get_client)

        assert client.headers["user-agent"]
        assert client.event_hooks["request"]
        assert client.follow_redirects is True


class TestTransportOptions:
    @pytest.mark.parametrize("get_client", _CLIENT_FACTORIES)
    def test_retries_reach_the_connection_pool(self, get_client):
        config.http.retries = 3

        assert _client(get_client)._transport._pool._retries == 3

    @pytest.mark.parametrize("get_client", _CLIENT_FACTORIES)
    def test_limits_reach_the_connection_pool(self, get_client):
        config.http.max_connections = 5
        config.http.max_keepalive_connections = 2

        pool = _client(get_client)._transport._pool

        assert pool._max_connections == 5
        assert pool._max_keepalive_connections == 2

    @pytest.mark.parametrize("get_client", _CLIENT_FACTORIES)
    @pytest.mark.parametrize("field, value", [("retries", 3), ("max_connections", 5)])
    def test_they_do_not_cost_the_environment_proxies(self, get_client, monkeypatch, field, value):
        monkeypatch.setenv("HTTPS_PROXY", "http://env-proxy:1111")
        setattr(config.http, field, value)

        assert _route_to(_client(get_client), "https://api.mistral.ai/v1") == _ENV_PROXY

    @pytest.mark.parametrize("get_client", _CLIENT_FACTORIES)
    def test_no_proxy_is_still_honoured_alongside_retries(self, get_client, monkeypatch):
        monkeypatch.setenv("HTTPS_PROXY", "http://env-proxy:1111")
        monkeypatch.setenv("NO_PROXY", "internal.corp")
        config.http.retries = 3

        client = _client(get_client)

        assert _route_to(client, "https://internal.corp/v1") is None
        assert _route_to(client, "https://api.mistral.ai/v1") == _ENV_PROXY

    @pytest.mark.parametrize("get_client", _CLIENT_FACTORIES)
    @pytest.mark.parametrize(
        "field, value, other, other_default",
        [
            ("max_keepalive_connections", 2, "max_connections", 100),
            ("max_connections", 200, "max_keepalive_connections", 20),
        ],
    )
    def test_one_limit_leaves_the_other_at_its_default(self, get_client, field, value, other, other_default):
        setattr(config.http, field, value)

        pool = _client(get_client)._transport._pool

        assert getattr(pool, f"_{field}") == value
        assert getattr(pool, f"_{other}") == other_default

    @pytest.mark.parametrize("get_client", _CLIENT_FACTORIES)
    def test_timeout_is_configurable(self, get_client):
        config.http.timeout = 7.0

        assert _client(get_client).timeout.connect == 7.0

    @pytest.mark.parametrize("get_client", _CLIENT_FACTORIES)
    def test_an_explicit_timeout_still_wins(self, get_client):
        config.http.timeout = 7.0

        assert get_client(timeout=1.0, server_url="http://localhost").timeout.connect == 1.0

    def test_the_mistral_client_honours_it(self):
        config.http.timeout = 7.0

        client = get_mistral_client(api_key="k", server_url="http://localhost")

        assert client.sdk_configuration.client.timeout.connect == 7.0
        assert client.sdk_configuration.async_client.timeout.connect == 7.0

    def test_it_does_not_cap_the_mistral_per_request_timeout(self):
        config.http.timeout = 7.0

        client = get_mistral_client(api_key="k", server_url="http://localhost")

        assert client.sdk_configuration.timeout_ms is None

    def test_an_explicit_timeout_ms_still_wins_over_it(self):
        config.http.timeout = 7.0

        client = get_mistral_client(api_key="k", server_url="http://localhost", timeout_ms=1000)

        assert client.sdk_configuration.client.timeout.connect == 1.0

    def test_the_worker_client_honours_it(self):
        config.http.timeout = 7.0

        client = get_worker_client(base_url="http://localhost", api_key="k")

        assert client.sdk_configuration.async_client.timeout.connect == 7.0
        assert client.sdk_configuration.timeout_ms == 7000

    @pytest.mark.parametrize(
        "hook_cls,attribute",
        [
            pytest.param(AsyncExecutorCredentialsHook, "async_client", id="async"),
            pytest.param(SyncExecutorCredentialsHook, "client", id="sync"),
        ],
    )
    def test_the_executor_credentials_clients_do_not_inherit_it(self, hook_cls, attribute):
        config.http.timeout = 7.0

        hook = hook_cls(server_url="http://localhost", token_provider=StaticTokenProvider("k"))

        assert getattr(hook._worker_client.sdk_configuration, attribute).timeout.connect == 5.0

    @pytest.mark.parametrize("get_client", _CLIENT_FACTORIES)
    def test_the_ca_bundle_reaches_the_transport_we_build(self, get_client, monkeypatch, tmp_path):
        ca_bundle = tmp_path / "ca.pem"
        loaded: list[str | None] = []
        monkeypatch.setattr(
            "ssl.SSLContext.load_verify_locations",
            lambda self, cafile=None, capath=None, cadata=None: loaded.append(cafile),
        )
        monkeypatch.setattr(config.common, "ca_bundle", str(ca_bundle))
        config.http.proxy = "http://corp-proxy:3128"

        _client(get_client)

        assert loaded == [str(ca_bundle)]


class TestRoutes:
    @pytest.fixture(autouse=True)
    def split_horizon(self):
        config.http.proxy = "http://corp-proxy:3128"
        config.http.routes = {
            "all://internal.corp": None,
            "all://*.eu.corp": {"proxy": "http://eu-proxy:3128"},
        }

    @pytest.mark.parametrize("get_client", _CLIENT_FACTORIES)
    def test_each_destination_takes_its_own_route(self, get_client):
        client = _client(get_client)

        assert _route_to(client, "https://internal.corp/v1") is None
        assert _route_to(client, "https://api.eu.corp/v1") == _EU_PROXY
        assert _route_to(client, "https://api.mistral.ai/v1") == _CORP_PROXY

    @pytest.mark.parametrize("get_client", _CLIENT_FACTORIES)
    def test_the_environment_proxies_are_shut_out(self, get_client, monkeypatch):
        monkeypatch.setenv("HTTPS_PROXY", "http://env-proxy:1111")

        client = _client(get_client)

        assert _route_to(client, "https://api.mistral.ai/v1") == _CORP_PROXY

    @pytest.mark.parametrize("get_client", _CLIENT_FACTORIES)
    def test_routes_reach_every_client_the_sdk_builds(self, get_client):
        hook = AsyncExecutorCredentialsHook(server_url="http://localhost", token_provider=StaticTokenProvider("k"))

        httpx_client = hook._worker_client.sdk_configuration.async_client
        assert _route_to(httpx_client, "https://api.eu.corp/v1") == _EU_PROXY

    def test_a_route_gets_its_own_transport_per_client(self):
        first = _client(_get_sync_client)
        second = _client(_get_sync_client)

        first.close()

        assert second._transport_for_url(httpx.URL("https://api.eu.corp")) is not first._transport_for_url(
            httpx.URL("https://api.eu.corp")
        )

    @pytest.mark.parametrize("get_client", _CLIENT_FACTORIES)
    def test_transport_options_apply_to_every_route(self, get_client):
        config.http.max_connections = 5

        client = _client(get_client)

        assert client._transport._pool._max_connections == 5
        assert client._transport_for_url(httpx.URL("https://api.eu.corp"))._pool._max_connections == 5

    @pytest.mark.parametrize("get_client", _CLIENT_FACTORIES)
    def test_retries_only_reach_the_direct_routes(self, get_client):
        config.http.retries = 2

        client = _client(get_client)

        assert client._transport_for_url(httpx.URL("https://internal.corp"))._pool._retries == 2
        assert client._transport_for_url(httpx.URL("https://api.eu.corp"))._pool._retries == 0


class TestVerify:
    @pytest.mark.parametrize("get_client", _CLIENT_FACTORIES)
    def test_turning_it_off_does_not_cost_the_environment_proxies(self, get_client, monkeypatch):
        monkeypatch.setenv("HTTPS_PROXY", "http://env-proxy:1111")
        config.http.verify = False

        client = _client(get_client)

        assert not _verifies(client._transport)
        assert _route_to(client, "https://api.mistral.ai/v1") == _ENV_PROXY

    @pytest.mark.parametrize("get_client", _CLIENT_FACTORIES)
    def test_verification_can_be_turned_off_behind_a_proxy(self, get_client):
        config.http.proxy = "http://mitm:3128"
        config.http.verify = False

        assert not _verifies(_client(get_client)._transport)

    @pytest.mark.parametrize("get_client", _CLIENT_FACTORIES)
    def test_a_route_overrides_the_section_default(self, get_client):
        config.http.proxy = "http://corp-proxy:3128"
        config.http.routes = {"all://mitm.corp": {"verify": False}}

        client = _client(get_client)

        assert _verifies(client._transport)
        intercepted = client._transport_for_url(httpx.URL("https://mitm.corp"))
        assert not _verifies(intercepted)
        assert _proxy_origin(intercepted) == _CORP_PROXY

    def test_disabling_verification_is_reported(self, caplog):
        HttpConfig(verify=False, routes={"all://mitm.corp": {"verify": False}})

        assert "TLS certificate verification is disabled" in caplog.text
        assert "all://mitm.corp" in caplog.text

    @pytest.mark.parametrize("get_client", _CLIENT_FACTORIES)
    def test_the_ca_bundle_is_the_fallback(self, get_client, monkeypatch, tmp_path):
        ca_bundle = tmp_path / "ca.pem"
        loaded: list[str | None] = []
        monkeypatch.setattr(
            "ssl.SSLContext.load_verify_locations",
            lambda self, cafile=None, capath=None, cadata=None: loaded.append(cafile),
        )
        monkeypatch.setattr(config.common, "ca_bundle", str(ca_bundle))

        _client(get_client)

        assert loaded == [str(ca_bundle)]

    @pytest.mark.parametrize("get_client", _CLIENT_FACTORIES)
    def test_verify_wins_over_the_ca_bundle(self, get_client, monkeypatch):
        monkeypatch.setattr(config.common, "ca_bundle", "/tmp/ca.pem")
        config.http.verify = False

        assert not _verifies(_client(get_client)._transport)


class TestTransportFactory:
    @pytest.mark.parametrize("get_client", _CLIENT_FACTORIES)
    def test_the_factory_supplies_the_transport(self, get_client):
        built = []

        def factory(client_cls):
            transport = (
                httpx.AsyncHTTPTransport() if issubclass(client_cls, httpx.AsyncClient) else httpx.HTTPTransport()
            )
            built.append((client_cls, transport))
            return transport

        config.http.transport_factory = factory

        client = _client(get_client)

        assert built[0][0] is type(client)
        assert client._transport is built[0][1]

    def test_each_client_gets_its_own_instance(self):
        config.http.transport_factory = lambda client_cls: httpx.HTTPTransport()

        assert _client(_get_sync_client)._transport is not _client(_get_sync_client)._transport

    @pytest.mark.parametrize("get_client", _CLIENT_FACTORIES)
    def test_routes_still_layer_on_top(self, get_client):
        config.http.transport_factory = lambda client_cls: (
            httpx.AsyncHTTPTransport() if issubclass(client_cls, httpx.AsyncClient) else httpx.HTTPTransport()
        )
        config.http.routes = {"all://*.eu.corp": {"proxy": "http://eu-proxy:3128"}}

        assert _route_to(_client(get_client), "https://api.eu.corp") == _EU_PROXY

    def test_the_factory_stays_out_of_the_config_dump(self):
        config.http.transport_factory = lambda client_cls: httpx.HTTPTransport()

        assert "transport_factory" not in config.http.model_dump()


class TestEnvironment:
    def test_the_options_are_read_from_the_environment(self, monkeypatch):
        monkeypatch.setenv("MISTRAL_WORKFLOWS_HTTP_PROXY", "http://env-proxy:3128")
        monkeypatch.setenv("MISTRAL_WORKFLOWS_HTTP_RETRIES", "2")
        monkeypatch.setenv("MISTRAL_WORKFLOWS_HTTP_VERIFY", "false")

        http_config = HttpConfig()

        assert http_config.proxy == "http://env-proxy:3128"
        assert http_config.retries == 2
        assert http_config.verify is False

    def test_routes_are_read_from_the_environment_as_json(self, monkeypatch):
        monkeypatch.setenv(
            "MISTRAL_WORKFLOWS_HTTP_ROUTES",
            '{"all://internal.corp": null, "all://": {"proxy": "http://mitm:3128", "verify": false}}',
        )

        http_config = HttpConfig()

        assert http_config.routes["all://internal.corp"] is None
        assert http_config.route_proxy(http_config.routes["all://"]) == "http://mitm:3128"
        assert http_config.route_verify(http_config.routes["all://"]) is False

    def test_the_standard_proxy_variables_are_left_to_httpx(self, monkeypatch):
        monkeypatch.setenv("HTTP_PROXY", "http://standard-proxy:3128")

        assert HttpConfig().proxy is None


class TestLoggableConfig:
    """The 'Configuration loaded' log must not leak config.http proxy credentials."""

    def test_proxy_credentials_are_stripped(self):
        cfg = AppConfig()
        cfg.http.proxy = "http://user:S3cret@corp-proxy:3128"
        cfg.http.routes = {"all://*.eu.corp": {"proxy": "http://ruser:rpass@eu-proxy:3128"}}

        data = _loggable_config(cfg)

        assert data["http"]["proxy"] == "http://***@corp-proxy:3128"
        assert data["http"]["routes"]["all://*.eu.corp"]["proxy"] == "http://***@eu-proxy:3128"
        assert "S3cret" not in str(data)
        assert "rpass" not in str(data)

    def test_proxy_without_credentials_is_left_untouched(self):
        cfg = AppConfig()
        cfg.http.proxy = "http://corp-proxy:3128"

        assert _loggable_config(cfg)["http"]["proxy"] == "http://corp-proxy:3128"

    def test_secretstr_fields_stay_masked(self):
        cfg = AppConfig()
        cfg.common.mistral_api_key = SecretStr("supersecret")

        assert "supersecret" not in str(_loggable_config(cfg))
