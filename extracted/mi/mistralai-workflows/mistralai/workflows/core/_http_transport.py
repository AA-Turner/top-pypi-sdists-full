from typing import Any, Callable, cast

import httpx
from httpx._utils import get_environment_proxies

from mistralai.workflows.core.config.config import HttpRoute, config


def verify(route: HttpRoute | None = None) -> bool | str:
    if not config.http.route_verify(route):
        return False
    return config.common.ca_bundle or True


def limits() -> httpx.Limits:
    return httpx.Limits(
        max_connections=config.http.max_connections,
        max_keepalive_connections=config.http.max_keepalive_connections,
    )


def sync_transport() -> httpx.HTTPTransport | None:
    if config.http.transport_factory is not None:
        return cast(httpx.HTTPTransport, config.http.transport_factory(httpx.Client))
    if not _needs_transport():
        return None
    return _sync_http_transport(proxy=config.http.proxy, verify=verify())


def async_transport() -> httpx.AsyncHTTPTransport | None:
    if config.http.transport_factory is not None:
        return cast(httpx.AsyncHTTPTransport, config.http.transport_factory(httpx.AsyncClient))
    if not _needs_transport():
        return None
    return _async_http_transport(proxy=config.http.proxy, verify=verify())


def sync_mounts() -> dict[str, httpx.BaseTransport | None] | None:
    return _mounts(_sync_http_transport)


def async_mounts() -> dict[str, httpx.AsyncBaseTransport | None] | None:
    return _mounts(_async_http_transport)


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


def _sync_http_transport(*, proxy: str | None, verify: bool | str) -> httpx.HTTPTransport:
    return httpx.HTTPTransport(**_transport_kwargs(proxy=proxy, verify=verify))


def _async_http_transport(*, proxy: str | None, verify: bool | str) -> httpx.AsyncHTTPTransport:
    return httpx.AsyncHTTPTransport(**_transport_kwargs(proxy=proxy, verify=verify))


def _transport_kwargs(*, proxy: str | None, verify: bool | str) -> dict[str, Any]:
    kwargs: dict[str, Any] = {"verify": verify, "limits": limits()}
    if proxy is not None:
        kwargs["proxy"] = proxy
    if config.http.retries:
        kwargs["retries"] = config.http.retries
    return kwargs
