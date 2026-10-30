from typing import Any, Callable, cast

import httpx
from httpx._utils import get_environment_proxies

from mistralai.workflows._mistral_http import HttpBackend
from mistralai.workflows.core.config.config import HttpRoute, config


def verify(route: HttpRoute | None = None) -> bool | str:
    if not config.http.route_verify(route):
        return False
    return config.common.ca_bundle or True


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


def _sync_http_transport(*, proxy: str | None, verify: bool | str, http: HttpBackend = httpx) -> httpx.HTTPTransport:
    return http.HTTPTransport(**_transport_kwargs(proxy=proxy, verify=verify, http=http))


def _async_http_transport(
    *, proxy: str | None, verify: bool | str, http: HttpBackend = httpx
) -> httpx.AsyncHTTPTransport:
    return http.AsyncHTTPTransport(**_transport_kwargs(proxy=proxy, verify=verify, http=http))


def _transport_kwargs(*, proxy: str | None, verify: bool | str, http: HttpBackend = httpx) -> dict[str, Any]:
    kwargs: dict[str, Any] = {"verify": verify, "limits": limits(http)}
    if proxy is not None:
        kwargs["proxy"] = proxy
    if config.http.retries:
        kwargs["retries"] = config.http.retries
    return kwargs
