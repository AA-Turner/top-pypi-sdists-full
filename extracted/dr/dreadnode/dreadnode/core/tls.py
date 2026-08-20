"""Native host trust for Dreadnode-owned platform connections."""

import ssl
import typing as t

import requests
import truststore
from requests.adapters import HTTPAdapter

if t.TYPE_CHECKING:
    from requests.adapters import _HostParams, _PoolKwargs

TLS_TRUST_DOCS_URL = "https://docs.dreadnode.io/self-hosting/client-tls-trust/"


def create_platform_ssl_context() -> ssl.SSLContext:
    """Create a verified TLS context backed by the host OS trust store."""
    return truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)


class NativeTrustAdapter(HTTPAdapter):
    """Use an explicit SSL context while preserving Requests pool semantics."""

    def __init__(self, ssl_context: ssl.SSLContext) -> None:
        self.ssl_context = ssl_context
        super().__init__()

    def build_connection_pool_key_attributes(
        self,
        request: requests.PreparedRequest,
        verify: bool | str,
        cert: str | tuple[str, str] | None = None,
    ) -> "tuple[_HostParams, _PoolKwargs]":
        host_params, pool_kwargs = super().build_connection_pool_key_attributes(
            request,
            verify,
            cert,
        )
        if request.url and request.url.lower().startswith("https://") and verify is not False:
            pool_kwargs.pop("ca_certs", None)
            pool_kwargs.pop("ca_cert_dir", None)
            pool_kwargs["ssl_context"] = self.ssl_context
            pool_kwargs["cert_reqs"] = "CERT_REQUIRED"
        return host_params, pool_kwargs


def create_platform_http_session(
    ssl_context: ssl.SSLContext | None = None,
) -> requests.Session:
    """Create a Requests session using native trust for HTTPS destinations."""
    session = requests.Session()
    session.mount("https://", NativeTrustAdapter(ssl_context or create_platform_ssl_context()))
    return session


def format_tls_error(error: BaseException | str, error_type: str | None = None) -> str | None:
    """Return an actionable message when an error chain contains a TLS verification failure."""
    parts = [error_type or "", str(error)]
    if isinstance(error, BaseException):
        seen: set[int] = set()
        current: BaseException | None = error
        while current is not None and id(current) not in seen:
            seen.add(id(current))
            parts.extend((current.__class__.__name__, str(current)))
            current = current.__cause__ or current.__context__

    lowered = " ".join(parts).lower()
    if not any(
        marker in lowered
        for marker in (
            "certificate_verify_failed",
            "certificate verify failed",
            "sslcertverificationerror",
            "hostname mismatch",
            "certificate name does not match input",
            "certificate has expired",
            "certificate is not yet valid",
        )
    ):
        return None

    if any(
        marker in lowered
        for marker in (
            "hostname mismatch",
            "certificate name does not match input",
            "doesn't match",
            "not valid for",
            "ip address mismatch",
        )
    ):
        reason = "hostname mismatch"
        action = "Fix the server certificate SAN configuration."
    elif any(marker in lowered for marker in ("expired", "not yet valid", "not valid yet")):
        reason = "certificate validity or system clock"
        action = "Renew the certificate or correct the client clock."
    elif any(
        marker in lowered
        for marker in (
            "unable to get local issuer",
            "unable to verify the first certificate",
            "self-signed certificate",
            "unknown ca",
            "unknown issuer",
        )
    ):
        reason = "unknown issuer or incomplete chain"
        action = "Install or repair the organization CA chain in the OS trust store."
    else:
        reason = "certificate verification failed"
        action = "Check the server certificate and the host OS trust store."

    return f"TLS certificate verification failed: {reason}. {action} See {TLS_TRUST_DOCS_URL}"
