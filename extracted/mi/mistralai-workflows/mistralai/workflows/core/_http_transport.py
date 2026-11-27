import os
import ssl
from typing import Any, Callable, cast

import httpx
from httpx._utils import get_environment_proxies

from mistralai.workflows._mistral_http import HttpBackend
from mistralai.workflows.core.config.config import HttpRoute, config


def sync_client_options(http: HttpBackend = httpx) -> dict[str, Any]:
    transport = sync_transport(http)
    return {
        # httpx only reads the client-level `verify` when it builds the default transport itself.
        "verify": verify() if transport is None else True,
        "transport": transport,
        "mounts": sync_mounts(http),
        "limits": limits(http),
    }


def async_client_options(http: HttpBackend = httpx) -> dict[str, Any]:
    transport = async_transport(http)
    return {
        "verify": verify() if transport is None else True,
        "transport": transport,
        "mounts": async_mounts(http),
        "limits": limits(http),
    }


def verify(route: HttpRoute | None = None) -> ssl.SSLContext | bool:
    verifies = config.http.route_verify(route)
    client_identity = config.common.mtls_client_identity
    if client_identity is None and not (verifies and config.common.ca_bundle):
        return verifies
    context = _verifying_ssl_context() if verifies else httpx.create_ssl_context(verify=False)
    if client_identity is not None:
        context.load_cert_chain(*client_identity)
    return context


def _verifying_ssl_context() -> ssl.SSLContext:
    ca_bundle = config.common.ca_bundle
    if ca_bundle is None:
        return httpx.create_ssl_context()
    if os.path.isdir(ca_bundle):
        return ssl.create_default_context(capath=ca_bundle)
    return ssl.create_default_context(cafile=ca_bundle)


def limits(http: HttpBackend = httpx) -> httpx.Limits:
    return http.Limits(
        max_connections=config.http.max_connections,
        max_keepalive_connections=config.http.max_keepalive_connections,
    )


def sync_transport(http: HttpBackend = httpx) -> httpx.BaseTransport | None:
    if config.http.transport_factory is not None:
        return cast(httpx.BaseTransport, config.http.transport_factory(http.Client))
    if not _needs_transport():
        return None
    return _sync_http_transport(proxy=config.http.proxy, verify=verify(), http=http)


def async_transport(http: HttpBackend = httpx) -> httpx.AsyncBaseTransport | None:
    if config.http.transport_factory is not None:
        return cast(httpx.AsyncBaseTransport, config.http.transport_factory(http.AsyncClient))
    if not _needs_transport():
        return None
    return _async_http_transport(proxy=config.http.proxy, verify=verify(), http=http)


def sync_mounts(http: HttpBackend = httpx) -> dict[str, httpx.BaseTransport | None] | None:
    return _mounts(lambda **kwargs: _sync_http_transport(http=http, **kwargs))


def async_mounts(http: HttpBackend = httpx) -> dict[str, httpx.AsyncBaseTransport | None] | None:
    return _mounts(lambda **kwargs: _async_http_transport(http=http, **kwargs))


def _mounts(make_transport: Callable[..., Any]) -> dict[str, Any] | None:
    if config.http.routes:
        return {
            pattern: make_transport(proxy=config.http.route_proxy(route), verify=verify(route))
            for pattern, route in config.http.routes.items()
        }
    if _needs_transport() and not _sdk_resolves_proxies():
        resolved_verify = verify()
        return {
            pattern: None if url is None else make_transport(proxy=url, verify=resolved_verify)
            for pattern, url in get_environment_proxies().items()
        }
    return None


def _needs_transport() -> bool:
    return bool(config.http.proxy or config.http.routes or config.http.retries)


def _sdk_resolves_proxies() -> bool:
    return bool(config.http.proxy or config.http.routes or config.http.transport_factory)


def _sync_http_transport(
    *, proxy: str | None, verify: ssl.SSLContext | bool, http: HttpBackend = httpx
) -> httpx.HTTPTransport:
    return http.HTTPTransport(**_transport_kwargs(proxy=proxy, verify=verify, http=http))


def _async_http_transport(
    *, proxy: str | None, verify: ssl.SSLContext | bool, http: HttpBackend = httpx
) -> httpx.AsyncHTTPTransport:
    return http.AsyncHTTPTransport(**_transport_kwargs(proxy=proxy, verify=verify, http=http))


def _transport_kwargs(*, proxy: str | None, verify: ssl.SSLContext | bool, http: HttpBackend = httpx) -> dict[str, Any]:
    kwargs: dict[str, Any] = {"verify": verify, "limits": limits(http)}
    if proxy is not None:
        kwargs["proxy"] = proxy
    if config.http.retries:
        kwargs["retries"] = config.http.retries
    return kwargs
