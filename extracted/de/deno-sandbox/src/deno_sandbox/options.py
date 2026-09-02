from __future__ import annotations

import os

from typing import Optional, TypedDict
from typing_extensions import NotRequired

from httpx import URL

from .errors import MissingApiToken

DEFAULT_SANDBOX_BASE_DOMAIN = "sandbox-api.deno.net"
DEFAULT_REGION = "ord"


class Options(TypedDict):
    token: NotRequired[str | None]
    regions: NotRequired[list[str] | None]


class InternalOptions(TypedDict):
    sandbox_ws_url: URL
    sandbox_url: URL
    console_url: URL
    token: str
    regions: list[str]
    sandbox_base_domain: str | None


def get_sandbox_ws_url(options: InternalOptions, region: str | None = None) -> URL:
    """Build a region-specific sandbox WebSocket URL.

    If the user set DENO_SANDBOX_ENDPOINT, that endpoint is always used
    (region is ignored for URL construction). Otherwise the URL is built
    from the base domain and the requested region.
    """
    base_domain = options["sandbox_base_domain"]
    if base_domain is None:
        # User provided an explicit endpoint — use it as-is.
        return options["sandbox_ws_url"]

    resolved_region = region if region is not None else DEFAULT_REGION
    return URL(f"wss://{resolved_region}.{base_domain}")


def get_internal_options(options: Optional[Options] = None) -> InternalOptions:
    explicit_endpoint = os.environ.get("DENO_SANDBOX_ENDPOINT")

    if explicit_endpoint is not None:
        sandbox_url = URL(explicit_endpoint)
        sandbox_base_domain: str | None = None
    else:
        base_domain = os.environ.get(
            "DENO_SANDBOX_BASE_DOMAIN", DEFAULT_SANDBOX_BASE_DOMAIN
        )
        sandbox_url = URL(f"https://{DEFAULT_REGION}.{base_domain}")
        sandbox_base_domain = base_domain

    token = (
        options is not None
        and options.get("token")
        or os.environ.get("DENO_DEPLOY_TOKEN", None)
    )

    if token is None:
        raise MissingApiToken({"message": "DENO_DEPLOY_TOKEN is not set"})

    scheme = sandbox_url.scheme.replace("http", "ws")
    sandbox_ws_url = URL(f"{scheme}://{sandbox_url.netloc.decode()}")

    console_url = URL(
        os.environ.get("DENO_DEPLOY_ENDPOINT", "https://console.deno.com")
    )

    regions = (
        options is not None
        and options.get("regions")
        or os.environ.get("DENO_AVAILABLE_REGIONS", "ams1,ord").split(",")
    )

    return InternalOptions(
        console_url=console_url,
        sandbox_ws_url=sandbox_ws_url,
        sandbox_url=sandbox_url,
        token=token,
        regions=regions,
        sandbox_base_domain=sandbox_base_domain,
    )
