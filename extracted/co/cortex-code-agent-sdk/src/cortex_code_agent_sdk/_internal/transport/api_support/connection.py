"""Connection and HTTP helpers for direct Agent API transport."""

from __future__ import annotations

import re
import select
import urllib.error
import urllib.request
from collections.abc import Callable
from contextlib import suppress
from ipaddress import ip_address
from typing import Any
from urllib.parse import urlsplit

from ....types import AgentApiOptions, CortexCodeAgentOptions
from .settings import _is_truthy, _merged_env
from .types import _DirectConnection, _HttpResponse


def _clean_rest_url(rest_url: str) -> tuple[str, str]:
    protocol = "http" if rest_url.startswith("http://") else "https"
    parsed = urlsplit(
        rest_url if re.match(r"^https?://", rest_url) else f"{protocol}://{rest_url}"
    )
    if protocol == "http" and not _is_loopback_hostname(parsed.hostname):
        raise ValueError(
            "API mode api.rest_url must use https for non-local Snowflake hosts"
        )
    hostname = parsed.hostname.replace("_", "-") if parsed.hostname else ""
    netloc = hostname
    if parsed.port is not None:
        netloc = f"{netloc}:{parsed.port}"
    clean_rest_url = netloc + parsed.path.rstrip("/")
    return clean_rest_url, protocol


def _is_loopback_hostname(hostname: str | None) -> bool:
    if hostname is None:
        return False
    normalized = hostname.strip("[]").lower()
    if normalized == "localhost":
        return True
    try:
        return ip_address(normalized).is_loopback
    except ValueError:
        return False


def _resolve_connection(options: CortexCodeAgentOptions) -> _DirectConnection:
    env = _merged_env(options)
    if _is_truthy(env.get("CORTEX_AGENT_USE_LOCAL_ORCHESTRATOR")) or env.get(
        "CORTEX_AGENT_LOCAL_PORT"
    ):
        host = env.get("CORTEX_AGENT_LOCAL_HOST", "localhost")
        port = env.get("CORTEX_AGENT_LOCAL_PORT", "2031")
        return _DirectConnection(
            agent_url=f"http://{host}:{port}/api/v2/cortex/agent:run",
            rest_url=f"{host}:{port}",
            token="fake-token",
            protocol="http",
            is_local=True,
        )

    api = options.api or AgentApiOptions()
    rest_url = api.rest_url
    token_provider = api.token_provider
    if rest_url and token_provider:
        clean_rest_url, protocol = _clean_rest_url(rest_url)
        token = _read_token(
            "api.token_provider.get_token",
            token_provider.get_token(),
        )
        connection = _DirectConnection(
            agent_url=f"{protocol}://{clean_rest_url}/api/v2/cortex/agent:run",
            rest_url=clean_rest_url,
            token=token,
            protocol=protocol,
            is_local=False,
        )

        def refresh(reason: str) -> None:
            connection.token = _read_token(
                "api.token_provider.refresh_token",
                token_provider.refresh_token(reason),
            )

        connection.refresh = refresh
        return connection

    return _resolve_snowflake_connector_connection(options)


def _read_token(source: str, token: str) -> str:
    if not isinstance(token, str) or not token:
        raise RuntimeError(f"{source} must return a non-empty Snowflake session token")
    return token


def _resolve_snowflake_connector_connection(
    options: CortexCodeAgentOptions,
) -> _DirectConnection:
    try:
        import snowflake.connector
    except ImportError as exc:
        raise RuntimeError(
            "No Snowflake connection provided for API mode. Pass "
            "CortexCodeAgentOptions(api=AgentApiOptions(rest_url=..., token_provider=...)) "
            "or install snowflake-connector-python and pass "
            "CortexCodeAgentOptions(connection=...)."
        ) from exc

    connect_kwargs: dict[str, Any] = {}
    if options.connection:
        connect_kwargs["connection_name"] = options.connection

    try:
        active_connector_connection = snowflake.connector.connect(**connect_kwargs)
    except Exception as exc:
        target = f" connection {options.connection!r}" if options.connection else ""
        raise RuntimeError(
            f"Failed to resolve Snowflake{target} for API mode. Pass "
            "CortexCodeAgentOptions(api=AgentApiOptions(rest_url=..., token_provider=...)) "
            "or configure a Snowflake connection in connections.toml/config.toml."
        ) from exc

    connection = _direct_connection_from_connector(active_connector_connection)

    def close() -> None:
        with suppress(Exception):
            active_connector_connection.close()

    def refresh(_reason: str) -> None:
        nonlocal active_connector_connection
        replacement_connection = snowflake.connector.connect(**connect_kwargs)
        refreshed = _direct_connection_from_connector(replacement_connection)
        previous_connection = active_connector_connection
        active_connector_connection = replacement_connection
        connection.agent_url = refreshed.agent_url
        connection.rest_url = refreshed.rest_url
        connection.token = refreshed.token
        connection.protocol = refreshed.protocol
        connection.user = refreshed.user
        with suppress(Exception):
            previous_connection.close()

    connection.close = close
    connection.refresh = refresh
    return connection


def _direct_connection_from_connector(connector_connection: Any) -> _DirectConnection:
    rest = getattr(connector_connection, "rest", None)
    token = getattr(rest, "token", None)
    server_url = getattr(rest, "server_url", None)
    if not isinstance(token, str) or not token:
        with suppress(Exception):
            connector_connection.close()
        raise RuntimeError("Snowflake connector did not return a session token.")
    if not isinstance(server_url, str) or not server_url:
        with suppress(Exception):
            connector_connection.close()
        raise RuntimeError("Snowflake connector did not return a REST URL.")

    clean_rest_url, protocol = _clean_rest_url(server_url)
    user = getattr(connector_connection, "user", None)
    return _DirectConnection(
        agent_url=f"{protocol}://{clean_rest_url}/api/v2/cortex/agent:run",
        rest_url=clean_rest_url,
        token=token,
        protocol=protocol,
        is_local=False,
        user=user if isinstance(user, str) else None,
    )


def _http_request(
    url: str,
    method: str,
    headers: dict[str, str],
    body: bytes | None,
) -> _HttpResponse:
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode()
            status = int(getattr(response, "status", response.getcode()))
            reason = str(getattr(response, "reason", ""))
            return _HttpResponse(status=status, reason=reason, body=response_body)
    except urllib.error.HTTPError as error:
        return _HttpResponse(
            status=error.code,
            reason=error.reason,
            body=error.read().decode(errors="replace"),
        )


def _http_stream_request(
    url: str,
    headers: dict[str, str],
    should_stop: Callable[[], bool],
    on_response: Callable[[Any | None], None] | None = None,
) -> _HttpResponse:
    request = urllib.request.Request(url, headers=headers, method="GET")
    try:
        try:
            with urllib.request.urlopen(request) as response:
                if on_response is not None:
                    on_response(response)
                status = int(getattr(response, "status", response.getcode()))
                reason = str(getattr(response, "reason", ""))
                if not hasattr(response, "readline"):
                    return _HttpResponse(
                        status=status,
                        reason=reason,
                        body=response.read().decode(errors="replace"),
                    )

                lines: list[str] = []
                while True:
                    if should_stop():
                        lines.append(
                            'event: response.done\ndata: {"status":"cancelled"}\n\n'
                        )
                        break
                    sock = _response_socket(response)
                    if sock is not None:
                        while not should_stop():
                            readable, _, _ = select.select([sock], [], [], 1)
                            if readable:
                                break
                        if should_stop():
                            lines.append(
                                'event: response.done\n'
                                'data: {"status":"cancelled"}\n\n'
                            )
                            break
                    try:
                        line = response.readline()
                    except OSError:
                        if should_stop():
                            lines.append(
                                'event: response.done\n'
                                'data: {"status":"cancelled"}\n\n'
                            )
                            break
                        raise
                    if not line:
                        break
                    lines.append(line.decode(errors="replace"))
                return _HttpResponse(status=status, reason=reason, body="".join(lines))
        except urllib.error.HTTPError as error:
            return _HttpResponse(
                status=error.code,
                reason=error.reason,
                body=error.read().decode(errors="replace"),
            )
    finally:
        if on_response is not None:
            on_response(None)


def _response_socket(response: Any) -> Any | None:
    fp = getattr(response, "fp", None)
    raw = getattr(fp, "raw", None)
    return getattr(raw, "_sock", None)
