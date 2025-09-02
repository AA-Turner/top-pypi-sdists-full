import ipaddress
import ssl
from collections.abc import Sequence
from typing import (
    Any,
    Literal,
)

import aiohttp
import certifi

from .validations import (
    validate_local_request,
    validate_url,
)


def get_secure_connector(
    *,
    allow_local_network: bool,
    allow_localhost: bool,
) -> type[aiohttp.TCPConnector]:
    class SecureTCPConnector(aiohttp.TCPConnector):
        async def _resolve_host(
            self,
            host: str,
            port: int,
            traces: Sequence[aiohttp.tracing.Trace] | None = None,
        ) -> list[aiohttp.abc.ResolveResult]:
            hosts = await super()._resolve_host(host, port, traces)
            resolved_ips = [ipaddress.ip_address(host["host"]) for host in hosts]
            validate_local_request(
                resolved_ips,
                allow_local_network=allow_local_network,
                allow_localhost=allow_localhost,
            )
            return hosts

    return SecureTCPConnector


async def request(
    url: str,
    *,
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_local_network: bool = False,
    allow_localhost: bool = False,
    ascii_only: bool = False,
    dns_rebind_protection: bool = True,
    enforce_sanitization: bool = False,
    headers: dict[str, str] | None = None,
    json: Any | None = None,
    ports: list[int] | None = None,
    schemes: list[str] | None = None,
    timeout: int = 10,
) -> aiohttp.ClientResponse:
    validate_url(
        url,
        ascii_only=ascii_only,
        enforce_sanitization=enforce_sanitization,
        ports=ports or [],
        schemes=schemes or [],
    )
    connector = (
        get_secure_connector(
            allow_local_network=allow_local_network,
            allow_localhost=allow_localhost,
        )
        if dns_rebind_protection
        else aiohttp.TCPConnector
    )
    connection = connector(
        ssl=ssl.create_default_context(cafile=certifi.where()),
    )

    async with aiohttp.ClientSession(
        connector=connection,
        headers=headers,
    ) as session:
        async with session.request(
            method,
            url,
            allow_redirects=not dns_rebind_protection,
            json=json,
            timeout=aiohttp.ClientTimeout(total=timeout),
        ) as response:
            await response.read()
            return response
