"""TLS helpers for Runlayer CLI HTTP clients.

Layered on top of the global ``truststore.inject_into_ssl()`` patch applied
by ``runlayer_cli.truststore_init`` at each entrypoint. Injection covers
libraries we don't control (urllib, aiohttp, third-party SDKs); the helpers
here add an explicit per-client ``truststore.SSLContext`` so the
``--ca-bundle`` / ``RUNLAYER_CA_BUNDLE`` / ``SSL_CERT_FILE`` /
``REQUESTS_CA_BUNDLE`` overrides layer on top of system trust.

Direct construction of ``truststore.SSLContext`` here bypasses any
monkeypatching, so the env-var bundle fallback works regardless of injection
order.
"""

import os
import ssl
import warnings
from typing import Any

import httpx
import truststore

RUNLAYER_CA_BUNDLE_ENV = "RUNLAYER_CA_BUNDLE"
SSL_CERT_FILE_ENV = "SSL_CERT_FILE"
SSL_CERT_DIR_ENV = "SSL_CERT_DIR"
REQUESTS_CA_BUNDLE_ENV = "REQUESTS_CA_BUNDLE"
_CA_BUNDLE_ENV_VARS = (
    RUNLAYER_CA_BUNDLE_ENV,
    SSL_CERT_FILE_ENV,
    REQUESTS_CA_BUNDLE_ENV,
)


def get_ca_bundle_path() -> str | None:
    """Return the configured extra CA bundle path, if any."""
    for env_var in _CA_BUNDLE_ENV_VARS:
        value = os.environ.get(env_var)
        if value:
            return value
    return None


def get_ca_bundle_dir() -> str | None:
    """Return the configured OpenSSL-style CA bundle directory, if any."""
    value = os.environ.get(SSL_CERT_DIR_ENV)
    if value:
        return value
    return None


def set_ca_bundle_path(ca_bundle: str | None) -> None:
    """Set the Runlayer-specific CA bundle override for this process."""
    if ca_bundle:
        os.environ[RUNLAYER_CA_BUNDLE_ENV] = ca_bundle


def build_verify() -> ssl.SSLContext | bool:
    """Build httpx's verify value for Runlayer TLS trust rules."""
    ca_bundle = get_ca_bundle_path()
    ca_bundle_dir = get_ca_bundle_dir()
    context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    if ca_bundle or ca_bundle_dir:
        try:
            context.load_verify_locations(cafile=ca_bundle, capath=ca_bundle_dir)
        except OSError as exc:
            warnings.warn(
                f"Ignoring invalid TLS CA bundle: {exc}",
                RuntimeWarning,
                stacklevel=2,
            )
    return context


def http_client(**kwargs: Any) -> httpx.Client:
    """Create an httpx client that uses Runlayer TLS trust rules."""
    kwargs.setdefault("verify", build_verify())
    return httpx.Client(**kwargs)


def async_http_client(
    headers: dict[str, str] | None = None,
    timeout: httpx.Timeout | None = None,
    auth: httpx.Auth | None = None,
    follow_redirects: bool = True,
    **kwargs: Any,
) -> httpx.AsyncClient:
    """Create an async httpx client that uses Runlayer TLS trust rules."""
    if headers is not None:
        kwargs["headers"] = headers
    if timeout is None:
        from mcp.shared._httpx_utils import (  # noqa: PLC0415 - keep aiwatch mcp-free
            MCP_DEFAULT_SSE_READ_TIMEOUT,
            MCP_DEFAULT_TIMEOUT,
        )

        kwargs["timeout"] = httpx.Timeout(
            MCP_DEFAULT_TIMEOUT,
            read=MCP_DEFAULT_SSE_READ_TIMEOUT,
        )
    else:
        kwargs["timeout"] = timeout
    if auth is not None:
        kwargs["auth"] = auth
    kwargs["follow_redirects"] = follow_redirects
    kwargs.setdefault("verify", build_verify())
    return httpx.AsyncClient(**kwargs)
