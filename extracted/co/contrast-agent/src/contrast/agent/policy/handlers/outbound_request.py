# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import http.client
from typing import TYPE_CHECKING
from urllib.parse import SplitResult, urlsplit, urlunsplit

from contrast_fireball import OtelAttributes, SpanType

from contrast.utils.safe_import import safe_import

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from contrast.agent.policy.handlers import EventDict

REDACTED_CREDENTIALS = "REDACTED:REDACTED@"


class _Sentinel: ...


yarl_URL = safe_import("yarl.URL") or _Sentinel


def _clean_url(parsed: SplitResult) -> SplitResult:
    """
    Performs rudimentary masking on the provided URL, redacting the username and
    password, and removing the querystring and fragment. Also removes the port if it is
    implied by the scheme.

    Operates on urllib SplitResult objects. Unlike `urlparse`, `urlsplit` does not have
    special handling for a rarely-used URL feature called "params", which can be applied
    to particular path segments using a semi-colon (;). We're not concerning ourselves
    with this; urlsplit includes those in `path`.
    """
    credentials = (
        REDACTED_CREDENTIALS
        if parsed.username is not None or parsed.password is not None
        else ""
    )

    port = ""
    port_implied = (
        parsed.port is None
        or (parsed.scheme == "http" and parsed.port == 80)
        or (parsed.scheme == "https" and parsed.port == 443)
    )
    if not port_implied:
        assert parsed.port is not None
        port = f":{parsed.port}"

    netloc = f"{credentials}{parsed.hostname or ''}{port}"

    return SplitResult(
        parsed.scheme,
        netloc,
        parsed.path,
        "",  # query
        "",  # fragment
    )


def _build_attrs(url: str) -> OtelAttributes:
    cleaned_parsed_url = _clean_url(urlsplit(url))

    if cleaned_parsed_url.hostname is None:
        raise ValueError(f"Observe failed to extract hostname: {url=}")

    attrs: OtelAttributes = {
        "server.address": cleaned_parsed_url.hostname,
        "url.full": urlunsplit(cleaned_parsed_url),
    }

    if (
        cleaned_parsed_url.port is not None
    ):  # implied ports (80, 443) are removed in _clean_url
        attrs["server.port"] = cleaned_parsed_url.port

    return attrs


def observe_span_attrs_builder(
    event_dict: EventDict,
) -> tuple[SpanType, Callable[[Mapping[str, object], object], OtelAttributes], None]:
    url_param_location = event_dict.get("url", "")

    if not url_param_location:
        raise ValueError("Event must specify 'url' parameter location.")

    def observe_span_attrs(
        args: Mapping[str, object], result: object
    ) -> OtelAttributes:
        url = args[url_param_location]

        # This is a bit rough, but it's probably a good assumption that any url-like
        # argument is str-convertable. Known cases currently include:
        # - yarl.URL (aiohttp)
        # - httpx(2).URL (httpx(2))
        url = str(url)

        if url.startswith("/") and (result_url := getattr(result, "url", None)):
            # httpx(2).Client supports constructing requests with only
            # a relative path when the client itself was created with a
            # base_url. In that case, the "url" argument alone doesn't have a
            # hostname, but the object returned by BaseClient.build_request (an
            # httpx(2).Request) has already merged the relative path with the
            # client's base_url, so it has a usable absolute URL.
            url = str(result_url)

        return _build_attrs(url)

    return SpanType.OutboundServiceCall, observe_span_attrs, None


def http_client_attrs_builder(
    event_dict: EventDict,
) -> tuple[SpanType, Callable[[Mapping[str, object], object], OtelAttributes], None]:
    def http_client_attrs(args: Mapping[str, object], result: object) -> OtelAttributes:
        connection_obj: http.client.HTTPConnection = args["self"]
        incomplete_url: str = args["url"]

        scheme = (
            "https"
            if isinstance(connection_obj, http.client.HTTPSConnection)
            else "http"
        )
        host = connection_obj.host
        port = connection_obj.port
        full_url = f"{scheme}://{host}:{port}{incomplete_url}"

        return _build_attrs(full_url)

    return SpanType.OutboundServiceCall, http_client_attrs, None
