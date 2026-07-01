"""Client for the GR web service backend (Backsearch / Backfetch).

The SDK owns input validation, policy decisions, output formatting, and a
``domain_info`` preflight that doubles as the in-process SSRF-equivalent. The
backend owns HTTP egress, HTML->text extraction, and the search index.

The backend is a *backdated* corpus: every ``/fetch`` and ``/search`` call
carries an ``as_of`` date, and the index only returns documents that existed
on or before that date. This is what makes the tools "Back"-tools — they let
an agent see the web as it was at a chosen cutoff, which is how we keep
rollouts free of post-cutoff leakage.

Endpoint contract::

  POST <fetch>/fetch         body {url, as_of}   -> {url, text, host, ..., redirect?}
  POST <search>/search       body {query, as_of, k, mode, allowed_domains?, blocked_domains?}
                                                 -> {mode, hits[], candidates, timing}
  GET  <policy>/policy/domain_info?domain=<host> -> {can_fetch: bool, reason?: str}

Backend tokens and URLs are read from environment variables (see
``WebServiceConfig.from_env``). Defaults point at the live GR LBs.

The HTTP layer is pluggable via :class:`WebTransport` so callers (and tests)
can swap the default aiohttp transport for a fake. The SDK already depends on
aiohttp, so no new runtime dependency is introduced.
"""

from __future__ import annotations

import json as _json
import os
import time
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Mapping, Optional, Protocol

# Cache allowed-decisions only; never cache `blocked` or `failed` — policy
# updates would take five minutes to propagate otherwise.
DOMAIN_INFO_CACHE_TTL_S = 5 * 60
REQUEST_TIMEOUT_S = 60.0

# Live GR backend defaults — overridable via OPENREWARD_WEB_*_URL env vars.
_DEFAULT_FETCH_URL = "https://search.openreward.ai/fetch"
_DEFAULT_SEARCH_URL = "https://search.openreward.ai/search"
_DEFAULT_DOMAIN_INFO_URL = "https://search.openreward.ai/policy/domain_info"

_TRUTHY = ("1", "true", "yes", "on")


# --------------------------------------------------------------------------- #
# Errors                                                                      #
# --------------------------------------------------------------------------- #


class WebServiceError(Exception):
    """Base for backend-side failures (HTTP non-2xx / malformed)."""

    error_type = "WEB_SERVICE_ERROR"

    def __init__(
        self,
        status: int,
        body_snippet: str,
        *,
        detail: Optional[str] = None,
        error_code: Optional[int] = None,
    ):
        # When the backend returns its structured error envelope
        # ({"result": false, "message", "errorCode"}), `detail` carries the
        # human-readable message; surface that instead of the raw JSON body.
        super().__init__(
            f"Web service request failed (HTTP {status}): {detail or body_snippet}"
        )
        self.status = status
        self.body_snippet = body_snippet
        self.detail = detail
        self.error_code = error_code


class WebTransportError(WebServiceError):
    """Network/transport failure before any HTTP status was seen."""

    error_type = "WEB_TRANSPORT_ERROR"

    def __init__(self, cause: str):
        super().__init__(0, f"transport error: {cause}")
        self.cause = cause


class DomainBlockedError(Exception):
    error_type = "DOMAIN_BLOCKED"

    def __init__(self, host: str, reason: Optional[str] = None):
        msg = f"Domain blocked by policy: {host}"
        if reason:
            msg += f" ({reason})"
        super().__init__(msg)
        self.host = host
        self.reason = reason


class DomainCheckFailedError(Exception):
    error_type = "DOMAIN_CHECK_FAILED"

    def __init__(self, host: str, cause: str):
        super().__init__(f"Could not verify domain policy for {host}: {cause}")
        self.host = host
        self.cause = cause


class EgressBlockedError(Exception):
    error_type = "EGRESS_BLOCKED"

    def __init__(self, host: str):
        super().__init__(f"Access to {host} is blocked by the network egress proxy.")
        self.host = host


# --------------------------------------------------------------------------- #
# Config                                                                      #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class WebServiceConfig:
    api_key: str
    fetch_url: str = _DEFAULT_FETCH_URL
    search_url: str = _DEFAULT_SEARCH_URL
    domain_info_url: str = _DEFAULT_DOMAIN_INFO_URL
    skip_preflight: bool = False
    preapproved_hosts: frozenset[str] = field(default_factory=frozenset)
    # Default backdating cutoff (ISO ``YYYY-MM-DD``). ``None`` -> backend sees
    # today. Per-call ``as_of`` always overrides this.
    default_as_of: Optional[str] = None

    @classmethod
    def from_env(cls) -> Optional["WebServiceConfig"]:
        """Build from env vars. The key is read from ``OPENREWARD_API_KEY`` (the
        backdated web service authenticates with the same OpenReward key).
        Returns ``None`` if no key is set — callers should surface a clear "not
        configured" error to the agent rather than crashing."""
        api_key = os.getenv("OPENREWARD_API_KEY", "").strip()
        if not api_key:
            return None
        skip_preflight = os.getenv("OPENREWARD_WEB_SKIP_PREFLIGHT", "").lower() in _TRUTHY
        hosts_raw = os.getenv("OPENREWARD_WEB_PREAPPROVED_HOSTS", "")
        preapproved = frozenset(
            h.strip().lower() for h in hosts_raw.split(",") if h.strip()
        )
        as_of = os.getenv("OPENREWARD_WEB_AS_OF", "").strip() or None
        return cls(
            api_key=api_key,
            fetch_url=os.getenv("OPENREWARD_WEB_FETCH_URL", _DEFAULT_FETCH_URL),
            search_url=os.getenv("OPENREWARD_WEB_SEARCH_URL", _DEFAULT_SEARCH_URL),
            domain_info_url=os.getenv("OPENREWARD_WEB_DOMAIN_INFO_URL", _DEFAULT_DOMAIN_INFO_URL),
            skip_preflight=skip_preflight,
            preapproved_hosts=preapproved,
            default_as_of=as_of,
        )


# --------------------------------------------------------------------------- #
# Transport (pluggable HTTP layer)                                            #
# --------------------------------------------------------------------------- #


@dataclass
class RawResponse:
    status: int
    headers: Mapping[str, str]
    text: str


class WebTransport(Protocol):
    """Minimal async HTTP surface the client needs. Swap for a fake in tests."""

    async def request(
        self,
        method: str,
        url: str,
        *,
        params: Optional[Mapping[str, str]] = None,
        json: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> RawResponse: ...

    async def aclose(self) -> None: ...


class AiohttpTransport:
    """Default transport, backed by the aiohttp dependency the SDK already ships."""

    def __init__(self, timeout: float = REQUEST_TIMEOUT_S):
        self._timeout = timeout
        self._session: Any = None

    async def _ensure_session(self) -> Any:
        if self._session is None:
            import aiohttp

            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self._timeout)
            )
        return self._session

    async def request(
        self,
        method: str,
        url: str,
        *,
        params: Optional[Mapping[str, str]] = None,
        json: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> RawResponse:
        import aiohttp

        session = await self._ensure_session()
        try:
            async with session.request(
                method, url, params=params, json=json, headers=headers
            ) as resp:
                text = await resp.text()
                return RawResponse(status=resp.status, headers=dict(resp.headers), text=text)
        except aiohttp.ClientError as e:
            raise WebTransportError(str(e)) from e

    async def aclose(self) -> None:
        if self._session is not None:
            await self._session.close()
            self._session = None


# --------------------------------------------------------------------------- #
# Client                                                                      #
# --------------------------------------------------------------------------- #


@dataclass
class FetchResponse:
    url: str
    text: str
    host: Optional[str] = None
    title: Optional[str] = None
    crawl_date: Optional[str] = None
    publish_date: Optional[str] = None
    html: Optional[str] = None
    redirect: Optional[dict[str, Any]] = None  # {"to": str, "status": int}

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "FetchResponse":
        redirect = data.get("redirect")
        return cls(
            url=str(data.get("url", "")),
            text=str(data.get("text", "")),
            host=data.get("host"),
            title=data.get("title"),
            crawl_date=data.get("crawl_date"),
            publish_date=data.get("publish_date"),
            html=data.get("html"),
            redirect=redirect if isinstance(redirect, dict) else None,
        )


class WebServiceClient:
    """Async client for the GR web backend. Cheap to construct; reuse one per
    session if you can. Use as an async context manager to release the
    transport, or call :meth:`aclose`."""

    def __init__(
        self,
        config: WebServiceConfig,
        *,
        transport: Optional[WebTransport] = None,
    ):
        self._config = config
        # `_allowed_until[host]` is the monotonic time after which a cached
        # ALLOW decision is stale. We only cache allows.
        self._allowed_until: dict[str, float] = {}
        self._transport: WebTransport = transport or AiohttpTransport()

    async def aclose(self) -> None:
        await self._transport.aclose()

    async def __aenter__(self) -> "WebServiceClient":
        return self

    async def __aexit__(self, *exc) -> None:
        await self.aclose()

    # ----- public methods ------------------------------------------------- #

    def _resolve_as_of(self, as_of: Optional[str]) -> str:
        return as_of or self._config.default_as_of or _today_iso()

    async def fetch(self, *, url: str, as_of: Optional[str] = None) -> FetchResponse:
        body = {"url": url, "as_of": self._resolve_as_of(as_of)}
        data = await self._post_json(self._config.fetch_url, body)
        return FetchResponse.from_json(data)

    async def search(
        self,
        *,
        query: str,
        as_of: Optional[str] = None,
        k: int = 8,
        mode: str = "hybrid",
        allowed_domains: Optional[list[str]] = None,
        blocked_domains: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "query": query,
            "as_of": self._resolve_as_of(as_of),
            "k": k,
            "mode": mode,
        }
        if allowed_domains:
            body["allowed_domains"] = list(allowed_domains)
        if blocked_domains:
            body["blocked_domains"] = list(blocked_domains)
        return await self._post_json(self._config.search_url, body)

    async def domain_info(self, host: str) -> dict[str, Any]:
        h = host.lower()
        deadline = self._allowed_until.get(h)
        if deadline is not None and deadline > time.monotonic():
            return {"can_fetch": True}
        try:
            resp = await self._transport.request(
                "GET",
                self._config.domain_info_url,
                params={"domain": h},
                headers=self._headers(),
            )
        except WebTransportError as e:
            raise DomainCheckFailedError(h, e.cause) from e
        data = self._parse_json_response(resp)
        if data.get("can_fetch"):
            self._allowed_until[h] = time.monotonic() + DOMAIN_INFO_CACHE_TTL_S
        # Never cache `blocked` or `failed` — re-check next call.
        return data

    # ----- internals ------------------------------------------------------ #

    def _headers(self) -> dict[str, str]:
        # Authenticate with `X-API-Key`, matching the rest of the SDK
        # (openreward/api/_session/http.py) and what search.openreward.ai expects.
        return {
            "X-API-Key": self._config.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "OpenReward/0.1 (general-reasoning web-tools)",
        }

    async def _post_json(self, url: str, body: dict[str, Any]) -> dict[str, Any]:
        resp = await self._transport.request("POST", url, json=body, headers=self._headers())
        return self._parse_json_response(resp)

    def _parse_json_response(self, resp: RawResponse) -> dict[str, Any]:
        text = resp.text
        # Structured egress-block detection.
        if (
            resp.status == 403
            and resp.headers.get("x-proxy-error") == "blocked-by-allowlist"
        ):
            raise EgressBlockedError(_extract_host_from_body(text) or "unknown")
        if resp.status >= 400:
            detail, code = _parse_error_envelope(text)
            raise WebServiceError(resp.status, text[:500], detail=detail, error_code=code)
        try:
            data = _json.loads(text)
        except ValueError:
            raise WebServiceError(resp.status, f"non-JSON response: {text[:200]}")
        if not isinstance(data, dict):
            raise WebServiceError(resp.status, f"expected JSON object, got: {text[:200]}")
        return data


# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #


def _today_iso() -> str:
    return date.today().isoformat()


def validate_as_of(as_of: Optional[str]) -> Optional[str]:
    """Validate an ``as_of`` cutoff string. Returns it unchanged, or raises
    ``ValueError`` if it is not an ISO ``YYYY-MM-DD`` date. ``None`` passes."""
    if as_of is None:
        return None
    try:
        date.fromisoformat(as_of)
    except ValueError as e:
        raise ValueError(
            f'Invalid as_of date "{as_of}" — expected ISO format YYYY-MM-DD'
        ) from e
    return as_of


def _extract_host_from_body(body: str) -> Optional[str]:
    try:
        parsed = _json.loads(body)
    except (ValueError, TypeError):
        return None
    if isinstance(parsed, dict):
        host = parsed.get("domain")
        if isinstance(host, str):
            return host
    return None


def _parse_error_envelope(body: str) -> tuple[Optional[str], Optional[int]]:
    """Pull (message, errorCode) out of the backend's error envelope.

    The search/fetch services return {"result": false, "message": str,
    "errorCode": int} on 4xx (e.g. an unparseable search query -> 400). Returns
    (None, None) when the body isn't that shape, so callers fall back to the raw
    snippet.
    """
    try:
        parsed = _json.loads(body)
    except (ValueError, TypeError):
        return None, None
    if not isinstance(parsed, dict):
        return None, None
    message = parsed.get("message")
    code = parsed.get("errorCode")
    return (
        message if isinstance(message, str) else None,
        code if isinstance(code, int) else None,
    )
