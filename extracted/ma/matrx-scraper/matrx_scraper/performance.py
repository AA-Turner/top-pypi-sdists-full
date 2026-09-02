"""Performance data — PageSpeed Insights + Google Search Console.

Two integrations, same shape:
  * `PsiClient`    — public PageSpeed Insights v5 API (Lighthouse + CrUX)
  * `GscClient`    — Search Console searchAnalytics.query (per-page metrics)

Both are slow + rate-limited. Always cache through `scraper.psi_metrics` /
`scraper.gsc_metrics`. Refresh on demand from the page-detail UI.

Configuration (env vars, resolved in order — first match wins)
--------------------------------------------------------------
PSI key:
    GOOGLE_PSI_API_KEY               # explicit override
    GOOGLE_SEARCH_API_KEY            # standard Google Cloud key — works for PSI
                                     # if PageSpeed Insights API is enabled
                                     # on the same Cloud project
    AME_GOOGLE_SEARCH_API_KEY        # alternate aidream-account key
    (none)                           # PSI works keyless but throttled to ~25/day/IP

GSC auth — three paths, tried in order. First one that works wins:

    [A] Service account (PREFERRED — server-to-server, no consent flow):
        FIREBASE_SERVICE_ACCOUNT     # inline JSON OR file path to a service
                                     # account key. The SA must be added as a
                                     # user on the Search Console property
                                     # (Search Console → Settings → Users &
                                     # permissions → add the SA's email with
                                     # at least "Restricted" access).
        GOOGLE_SERVICE_ACCOUNT       # alternate name, same shape

    [B] OAuth refresh-token flow:
        GSC_CLIENT_ID + GSC_CLIENT_SECRET             # explicit override
        GOOGLE_OAUTH_CLIENT_SECRETS                   # JSON blob OR file path
        GOOGLE_CLIENT_ID + GOOGLE_CLIENT_SECRET       # canonical pair
        + GSC_REFRESH_TOKEN                           # mint via gsc_bootstrap.py

    [C] (none) — endpoint returns `not_configured`.

GSC default site URL (e.g. "sc-domain:aimatrx.com" or "https://aimatrx.com/"):
    GSC_DEFAULT_SITE_URL             # optional — we'll auto-infer
                                     # `sc-domain:<host>` if you don't set it.

Both clients no-op gracefully when their env is missing — the endpoints
return a structured `not_configured` payload so the UI can prompt the admin.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from enum import StrEnum
from typing import Any
from urllib.parse import urlparse

import httpx

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Env resolution helpers — keep all the "first env that's set wins" logic in
# one place so the docstring above and the runtime stay in sync.
# ---------------------------------------------------------------------------


def _first_env(*names: str) -> str | None:
    for n in names:
        v = os.environ.get(n)
        if v and v.strip():
            return v.strip()
    return None


def _resolve_psi_api_key() -> str | None:
    return _first_env(
        "GOOGLE_PSI_API_KEY",
        "GOOGLE_SEARCH_API_KEY",
        "AME_GOOGLE_SEARCH_API_KEY",
    )


def _looks_like_oauth_client_id(v: str | None) -> bool:
    """A real Google OAuth client ID ends with .apps.googleusercontent.com.
    The aidream env has GOOGLE_CLIENT_ID set to the GCP project NUMBER on
    some installs — reject those."""
    return bool(v) and v.endswith(".apps.googleusercontent.com")


def _parse_client_secrets_blob(raw: str) -> tuple[str | None, str | None]:
    """Parse a Google client_secrets payload — either an inline JSON string
    or a path to a JSON file. Looks for both `installed` and `web` blocks."""
    payload: dict | None = None
    raw = raw.strip()
    if raw.startswith("{"):
        try:
            payload = json.loads(raw)
        except Exception:
            logger.info("GOOGLE_OAUTH_CLIENT_SECRETS looked like JSON but didn't parse")
            payload = None
    if payload is None:
        try:
            with open(raw, encoding="utf-8") as f:
                payload = json.load(f)
        except Exception:
            logger.info("GOOGLE_OAUTH_CLIENT_SECRETS path read failed: %s", raw)
            return None, None
    if not isinstance(payload, dict):
        return None, None
    for key in ("installed", "web"):
        block = payload.get(key) or {}
        cid = block.get("client_id")
        csec = block.get("client_secret")
        if cid and csec:
            return cid, csec
    return None, None


def _resolve_service_account_info() -> dict | None:
    """Resolve a Google service-account key from env. Either inline JSON or
    a file path; returns the parsed dict or None.

    `FIREBASE_SERVICE_ACCOUNT` is the canonical aidream slot — the same key
    used for Firebase Admin works for any Google API the SA has been
    authorised on (we only need GSC's `webmasters.readonly` scope).
    """
    for name in ("FIREBASE_SERVICE_ACCOUNT", "GOOGLE_SERVICE_ACCOUNT"):
        raw = _first_env(name)
        if not raw:
            continue
        raw = raw.strip()
        try:
            if raw.startswith("{"):
                payload = json.loads(raw)
            else:
                with open(raw, encoding="utf-8") as f:
                    payload = json.load(f)
        except Exception:
            logger.exception("Failed to parse %s", name)
            continue
        if isinstance(payload, dict) and payload.get("type") == "service_account":
            return payload
    return None


def _resolve_oauth_client() -> tuple[str | None, str | None]:
    """Return (client_id, client_secret) from the first source that has both.

    Order:
      1. GSC_CLIENT_ID / GSC_CLIENT_SECRET           (explicit override)
      2. GOOGLE_OAUTH_CLIENT_SECRETS                 (JSON blob OR file path —
         this is what the aidream .env actually has, with the real OAuth
         client inside `web` / `installed`. Tried before GOOGLE_CLIENT_ID
         because GOOGLE_CLIENT_ID is sometimes the GCP project number, not
         a real OAuth client.)
      3. GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET     (only if client_id has the
         canonical .apps.googleusercontent.com suffix)
    """
    cid = _first_env("GSC_CLIENT_ID")
    csec = _first_env("GSC_CLIENT_SECRET")
    if cid and csec:
        return cid, csec

    secrets = _first_env("GOOGLE_OAUTH_CLIENT_SECRETS")
    if secrets:
        cid, csec = _parse_client_secrets_blob(secrets)
        if cid and csec:
            return cid, csec

    cid = _first_env("GOOGLE_CLIENT_ID")
    csec = _first_env("GOOGLE_CLIENT_SECRET")
    if _looks_like_oauth_client_id(cid) and csec:
        return cid, csec
    return None, None


# ---------------------------------------------------------------------------
# PageSpeed Insights v5
# ---------------------------------------------------------------------------

PSI_ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"


@dataclass
class PsiSnapshot:
    url: str
    strategy: str  # 'mobile' | 'desktop'
    performance: float | None = None
    accessibility: float | None = None
    best_practices: float | None = None
    seo: float | None = None
    lcp_ms: int | None = None
    inp_ms: int | None = None
    cls: float | None = None
    fcp_ms: int | None = None
    tbt_ms: int | None = None
    si_ms: int | None = None
    ttfb_ms: int | None = None
    crux_lcp_ms: int | None = None
    crux_inp_ms: int | None = None
    crux_cls: float | None = None
    crux_fcp_ms: int | None = None
    raw: dict[str, Any] = field(default_factory=dict)
    error_message: str | None = None
    fetched_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    http_status: int | None = None
    response_headers: dict[str, str] = field(default_factory=dict)
    request_count: int = 0


class PsiClient:
    """PageSpeed Insights v5 — public API.

    Without an API key the endpoint works but is rate-limited to ~25/day per
    source IP. With `GOOGLE_PSI_API_KEY` set, gets ~25k/day.
    """

    def __init__(self, *, api_key: str | None = None, timeout: float = 90.0) -> None:
        self.api_key = api_key or _resolve_psi_api_key()
        self.timeout = timeout

    async def fetch(self, url: str, *, strategy: str = "mobile") -> PsiSnapshot:
        if strategy not in ("mobile", "desktop"):
            raise ValueError(f"strategy must be mobile|desktop, got {strategy!r}")

        params: list[tuple[str, str]] = [
            ("url", url),
            ("strategy", strategy),
            ("category", "PERFORMANCE"),
            ("category", "ACCESSIBILITY"),
            ("category", "BEST_PRACTICES"),
            ("category", "SEO"),
        ]
        if self.api_key:
            params.append(("key", self.api_key))

        snap = PsiSnapshot(url=url, strategy=strategy)
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                snap.request_count = 1
                resp = await client.get(PSI_ENDPOINT, params=params)
                snap.http_status = resp.status_code
                snap.response_headers = dict(resp.headers)
                if resp.status_code >= 400:
                    response_text: str | None = None
                    try:
                        error_payload = await _decode_response_json(resp)
                    except ValueError:
                        response_text = await _decode_response_text(resp)
                        error_payload = {
                            "http_error": {
                                "status": resp.status_code,
                                "body": response_text[:2_000],
                                "body_truncated": len(response_text) > 2_000,
                            }
                        }
                    snap.raw = (
                        error_payload
                        if isinstance(error_payload, dict)
                        else {"http_error": {"status": resp.status_code, "body": error_payload}}
                    )
                    provider_message = _google_api_error_message(error_payload)
                    expired_key = self.api_key and _is_expired_psi_key_response(
                        resp,
                        error_payload,
                    )
                    if expired_key:
                        logger.error(
                            "PSI API key was rejected as expired; the platform credential "
                            "must be rotated"
                        )
                        # This is the PLATFORM quota key, not any user's
                        # Google OAuth connection — say so, or the error
                        # reads as an auth problem on OAuth surfaces.
                        snap.error_message = (
                            "The platform PageSpeed Insights API key is "
                            "expired — an operator must renew the Google API "
                            "key in the Google Cloud console and update the "
                            "server environment. This is NOT your Google "
                            "account connection; no re-authorization on your "
                            "side will fix it."
                        )
                    else:
                        if response_text is None:
                            response_text = await _decode_response_text(resp)
                        snap.error_message = (
                            f"PSI HTTP {resp.status_code}: "
                            f"{provider_message or response_text[:300]}"
                        )
                    return snap
                payload = await _decode_response_json(resp)
        except Exception as exc:
            snap.error_message = f"{type(exc).__name__}: {exc}"
            snap.raw = {
                "transport_error": {
                    "type": type(exc).__name__,
                    "message": str(exc),
                }
            }
            return snap

        if not isinstance(payload, dict):
            snap.error_message = "PSI returned a malformed HTTP 200 response"
            snap.raw = {
                "malformed_response": {
                    "reason": "response body must be a JSON object",
                    "body": payload,
                }
            }
            return snap

        snap.raw = payload
        if not isinstance(payload.get("lighthouseResult"), dict):
            snap.error_message = "PSI returned HTTP 200 without lighthouseResult"
            return snap
        try:
            categories = (payload.get("lighthouseResult") or {}).get("categories") or {}
            snap.performance = _safe_float(_dig(categories, "performance", "score"))
            snap.accessibility = _safe_float(_dig(categories, "accessibility", "score"))
            snap.best_practices = _safe_float(_dig(categories, "best-practices", "score"))
            snap.seo = _safe_float(_dig(categories, "seo", "score"))

            audits = (payload.get("lighthouseResult") or {}).get("audits") or {}
            snap.lcp_ms = _audit_ms(audits, "largest-contentful-paint")
            snap.fcp_ms = _audit_ms(audits, "first-contentful-paint")
            snap.tbt_ms = _audit_ms(audits, "total-blocking-time")
            snap.si_ms = _audit_ms(audits, "speed-index")
            snap.ttfb_ms = _audit_ms(audits, "server-response-time")
            snap.cls = _audit_value(audits, "cumulative-layout-shift")
            # INP — added to Lighthouse 11+; may be absent on older runs
            snap.inp_ms = _audit_ms(audits, "interaction-to-next-paint")

            # CrUX field data — real-user p75 metrics over the last 28 days.
            loading = payload.get("loadingExperience") or {}
            metrics = loading.get("metrics") or {}
            snap.crux_lcp_ms = _crux_int(metrics, "LARGEST_CONTENTFUL_PAINT_MS")
            snap.crux_inp_ms = _crux_int(metrics, "INTERACTION_TO_NEXT_PAINT") or _crux_int(
                metrics, "EXPERIMENTAL_INTERACTION_TO_NEXT_PAINT"
            )
            snap.crux_cls = _crux_float_cls(metrics, "CUMULATIVE_LAYOUT_SHIFT_SCORE")
            snap.crux_fcp_ms = _crux_int(metrics, "FIRST_CONTENTFUL_PAINT_MS")
        except Exception:
            logger.exception("PSI parse failed for %s (%s)", url, strategy)
            # Keep raw — we still want the partial data for debugging.

        return snap


def _parse_response_json(response: httpx.Response) -> Any:
    return response.json()


async def _decode_response_json(response: httpx.Response) -> Any:
    return await asyncio.to_thread(_parse_response_json, response)


async def _decode_response_json_or_none(response: httpx.Response) -> Any | None:
    try:
        return await _decode_response_json(response)
    except (TypeError, ValueError):
        return None


def _parse_response_text(response: httpx.Response) -> str:
    return response.text


async def _decode_response_text(response: httpx.Response) -> str:
    return await asyncio.to_thread(_parse_response_text, response)


def _is_expired_psi_key_response(response: httpx.Response, payload: Any) -> bool:
    if response.status_code != 400:
        return False
    if not isinstance(payload, dict):
        return False
    error = payload.get("error")
    if not isinstance(error, dict):
        return False
    message = error.get("message")
    return isinstance(message, str) and "api key expired" in message.casefold()


def _google_api_error_message(payload: Any) -> str | None:
    if not isinstance(payload, dict):
        return None
    error = payload.get("error")
    if not isinstance(error, dict):
        return None
    message = error.get("message")
    return message.strip() if isinstance(message, str) and message.strip() else None


def _dig(d: dict, *keys: str) -> Any:
    cur: Any = d
    for k in keys:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(k)
    return cur


def _safe_float(v: Any) -> float | None:
    if v is None:
        return None
    try:
        return float(v)
    except Exception:
        return None


def _audit_ms(audits: dict, key: str) -> int | None:
    a = audits.get(key) or {}
    v = a.get("numericValue")
    if v is None:
        return None
    try:
        return int(round(float(v)))
    except Exception:
        return None


def _audit_value(audits: dict, key: str) -> float | None:
    a = audits.get(key) or {}
    v = a.get("numericValue")
    return _safe_float(v)


def _crux_int(metrics: dict, key: str) -> int | None:
    m = metrics.get(key) or {}
    p = m.get("percentile")
    if p is None:
        return None
    try:
        return int(p)
    except Exception:
        return None


def _crux_float_cls(metrics: dict, key: str) -> float | None:
    """CrUX returns CLS as percentile * 100 (integer). Convert back to float."""
    m = metrics.get(key) or {}
    p = m.get("percentile")
    if p is None:
        return None
    try:
        return float(p) / 100.0
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Google Search Console
# ---------------------------------------------------------------------------

GSC_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
GSC_QUERY_ENDPOINT = (
    "https://searchconsole.googleapis.com/webmasters/v3/sites/{site}/searchAnalytics/query"
)


@dataclass
class GscQueryRow:
    query: str
    clicks: int
    impressions: int
    ctr: float
    position: float


class GscErrorCode(StrEnum):
    NOT_CONFIGURED = "gsc_not_configured"
    PROPERTY_NOT_AUTHORIZED = "gsc_property_not_authorized"
    AUTHENTICATION_FAILED = "gsc_authentication_failed"
    REQUEST_FAILED = "gsc_request_failed"
    UNEXPECTED_ERROR = "gsc_unexpected_error"


@dataclass
class GscPageSnapshot:
    url: str
    site_url: str
    period_start: date
    period_end: date
    clicks: int = 0
    impressions: int = 0
    ctr: float = 0.0
    position: float | None = None
    top_queries: list[GscQueryRow] = field(default_factory=list)
    error_code: str | None = None
    error_message: str | None = None
    fetched_at: datetime = field(default_factory=lambda: datetime.now(UTC))


GSC_SCOPE = "https://www.googleapis.com/auth/webmasters.readonly"


def _classify_gsc_http_error(
    response: httpx.Response,
    *,
    payload: Any,
    response_text: str,
    operation: str,
    site_url: str,
) -> tuple[GscErrorCode, str]:
    google_status: str | None = None
    if isinstance(payload, dict):
        error = payload.get("error")
        if isinstance(error, dict) and isinstance(error.get("status"), str):
            google_status = error["status"]

    if response.status_code == 403 and google_status in (None, "PERMISSION_DENIED"):
        return (
            GscErrorCode.PROPERTY_NOT_AUTHORIZED,
            f"Search Console property {site_url!r} is not authorized for this credential. "
            "Grant the credential access in Search Console, then retry.",
        )
    if response.status_code == 401:
        return (
            GscErrorCode.AUTHENTICATION_FAILED,
            "Search Console rejected the credential. Reconnect it, then retry.",
        )
    detail = response_text[:200]
    return (
        GscErrorCode.REQUEST_FAILED,
        f"GSC {operation} HTTP {response.status_code}: {detail}",
    )


class GscClient:
    """Search Console — searchAnalytics.query.

    Two auth modes:
      * Service account (preferred): use the SA email + private key from a
        FIREBASE_SERVICE_ACCOUNT-style JSON. The SA must be added as a user
        on the Search Console property.
      * OAuth refresh token: uses an OAuth client + a per-admin refresh
        token (provisioned once via gsc_bootstrap.py).

    Service-account mode is preferred because no human-mediated OAuth
    consent is needed and the SA can be granted access to any GSC property
    via the standard "Users & permissions" UI.
    """

    def __init__(
        self,
        *,
        client_id: str | None = None,
        client_secret: str | None = None,
        refresh_token: str | None = None,
        default_site_url: str | None = None,
        service_account_info: dict | None = None,
        timeout: float = 30.0,
    ) -> None:
        # Service-account path — preferred. Resolved unless an explicit
        # OAuth pair was passed in.
        if service_account_info is not None:
            self.service_account_info: dict | None = service_account_info
        elif client_id and client_secret:
            self.service_account_info = None
        else:
            self.service_account_info = _resolve_service_account_info()

        # OAuth path — fallback when SA isn't available.
        if client_id and client_secret:
            self.client_id = client_id
            self.client_secret = client_secret
        else:
            cid, csec = _resolve_oauth_client()
            self.client_id = client_id or cid
            self.client_secret = client_secret or csec
        self.refresh_token = refresh_token or _first_env("GSC_REFRESH_TOKEN")
        self.default_site_url = default_site_url or _first_env("GSC_DEFAULT_SITE_URL")
        self.timeout = timeout
        self._access_token: str | None = None
        self._access_token_expires_at: float = 0.0
        self._token_lock = asyncio.Lock()

    @property
    def auth_mode(self) -> str | None:
        if self.service_account_info:
            return "service_account"
        if self.client_id and self.client_secret and self.refresh_token:
            return "oauth_refresh_token"
        return None

    @property
    def is_configured(self) -> bool:
        return self.auth_mode is not None

    async def access_token(self) -> str:
        """Public accessor for the cached short-lived access token.

        Consumers that call Search Console endpoints the snapshot helpers do
        not cover (daily search-analytics paging, submitted-sitemaps listing —
        see ``web_crawl.gsc_sync``) mint through this instead of reaching into
        the private ``_access`` refresh machinery.
        """

        return await self._access()

    async def _access(self) -> str:
        async with self._token_lock:
            now = time.time()
            if self._access_token and now < (self._access_token_expires_at - 60):
                return self._access_token
            mode = self.auth_mode
            if mode is None:
                raise RuntimeError(
                    "GSC client is not configured — set FIREBASE_SERVICE_ACCOUNT "
                    "(preferred) or GSC_REFRESH_TOKEN + an OAuth client."
                )
            if mode == "service_account":
                token, ttl = await self._mint_via_service_account()
            else:
                token, ttl = await self._mint_via_refresh_token()
            self._access_token = token
            self._access_token_expires_at = now + ttl
            return token

    async def _mint_via_refresh_token(self) -> tuple[str, int]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(
                GSC_TOKEN_ENDPOINT,
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "refresh_token": self.refresh_token,
                    "grant_type": "refresh_token",
                },
            )
            if resp.status_code >= 400:
                response_text = await _decode_response_text(resp)
                raise RuntimeError(
                    f"GSC token refresh failed: HTTP {resp.status_code} {response_text[:200]}"
                )
            payload = await _decode_response_json(resp)
        return payload["access_token"], int(payload.get("expires_in", 3600))

    async def _mint_via_service_account(self) -> tuple[str, int]:
        """Sign a JWT with the SA's private key and exchange for an access
        token. Runs the (CPU-bound) JWT sign + thin HTTP exchange in a
        thread so the event loop isn't blocked.
        """
        info = self.service_account_info or {}
        client_email = info.get("client_email")
        private_key = info.get("private_key")
        if not client_email or not private_key:
            raise RuntimeError("service account JSON missing client_email/private_key fields")
        token_uri = info.get("token_uri") or GSC_TOKEN_ENDPOINT

        def _sign() -> str:
            import jwt as _jwt  # PyJWT — already in the venv

            now_s = int(time.time())
            assertion_payload = {
                "iss": client_email,
                "scope": GSC_SCOPE,
                "aud": token_uri,
                "iat": now_s,
                "exp": now_s + 3600,
            }
            return _jwt.encode(assertion_payload, private_key, algorithm="RS256")

        assertion = await asyncio.to_thread(_sign)
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(
                token_uri,
                data={
                    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                    "assertion": assertion,
                },
            )
            if resp.status_code >= 400:
                response_text = await _decode_response_text(resp)
                raise RuntimeError(
                    f"GSC service-account token exchange failed: "
                    f"HTTP {resp.status_code} {response_text[:200]}"
                )
            payload = await _decode_response_json(resp)
        return payload["access_token"], int(payload.get("expires_in", 3600))

    def _resolve_site_url(self, page_url: str, site_url: str | None) -> str:
        if site_url:
            return site_url
        if self.default_site_url:
            return self.default_site_url
        # Best-effort guess: sc-domain: form covers https + http + subdomains
        host = urlparse(page_url).netloc
        if not host:
            raise ValueError(f"cannot infer GSC site_url from {page_url!r}")
        return f"sc-domain:{host}"

    async def page_snapshot(
        self,
        url: str,
        *,
        site_url: str | None = None,
        days: int = 28,
        top_n_queries: int = 20,
    ) -> GscPageSnapshot:
        end = date.today() - timedelta(days=2)  # GSC has a 1-2 day delay
        start = end - timedelta(days=days)
        snap = GscPageSnapshot(
            url=url,
            site_url=site_url or self.default_site_url or "",
            period_start=start,
            period_end=end,
        )
        if not self.is_configured:
            snap.error_code = GscErrorCode.NOT_CONFIGURED
            snap.error_message = "not_configured"
            return snap

        try:
            site = self._resolve_site_url(url, site_url)
            snap.site_url = site
            access_token = await self._access()
            from urllib.parse import quote

            endpoint = GSC_QUERY_ENDPOINT.format(site=quote(site, safe=""))
            headers = {"Authorization": f"Bearer {access_token}"}

            # First request — totals for THIS page
            totals_body = {
                "startDate": start.isoformat(),
                "endDate": end.isoformat(),
                "dimensions": ["page"],
                "rowLimit": 1,
                "dimensionFilterGroups": [
                    {"filters": [{"dimension": "page", "operator": "equals", "expression": url}]}
                ],
            }
            # Second request — top queries for THIS page
            queries_body = {
                "startDate": start.isoformat(),
                "endDate": end.isoformat(),
                "dimensions": ["query"],
                "rowLimit": top_n_queries,
                "dimensionFilterGroups": [
                    {"filters": [{"dimension": "page", "operator": "equals", "expression": url}]}
                ],
                "orderBy": [{"field": "clicks", "descending": True}],
            }
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                totals_resp, queries_resp = await asyncio.gather(
                    client.post(endpoint, headers=headers, json=totals_body),
                    client.post(endpoint, headers=headers, json=queries_body),
                )
            if totals_resp.status_code >= 400:
                error_payload, response_text = await asyncio.gather(
                    _decode_response_json_or_none(totals_resp),
                    _decode_response_text(totals_resp),
                )
                snap.error_code, snap.error_message = _classify_gsc_http_error(
                    totals_resp,
                    payload=error_payload,
                    response_text=response_text,
                    operation="totals",
                    site_url=site,
                )
                return snap
            totals = await _decode_response_json(totals_resp)
            rows = totals.get("rows") or []
            if rows:
                r = rows[0]
                snap.clicks = int(r.get("clicks", 0) or 0)
                snap.impressions = int(r.get("impressions", 0) or 0)
                snap.ctr = float(r.get("ctr", 0) or 0)
                snap.position = float(r.get("position")) if r.get("position") is not None else None

            if queries_resp.status_code < 400:
                qpayload = await _decode_response_json(queries_resp)
                qrows = qpayload.get("rows") or []
                snap.top_queries = [
                    GscQueryRow(
                        query=(r.get("keys") or [""])[0],
                        clicks=int(r.get("clicks", 0) or 0),
                        impressions=int(r.get("impressions", 0) or 0),
                        ctr=float(r.get("ctr", 0) or 0),
                        position=float(r.get("position", 0) or 0),
                    )
                    for r in qrows
                    if r.get("keys")
                ]
            else:
                error_payload, response_text = await asyncio.gather(
                    _decode_response_json_or_none(queries_resp),
                    _decode_response_text(queries_resp),
                )
                snap.error_code, snap.error_message = _classify_gsc_http_error(
                    queries_resp,
                    payload=error_payload,
                    response_text=response_text,
                    operation="top-queries",
                    site_url=site,
                )
        except Exception as exc:
            snap.error_code = GscErrorCode.UNEXPECTED_ERROR
            snap.error_message = f"{type(exc).__name__}: {exc}"
            logger.exception("GSC page_snapshot failed for %s", url)

        return snap


# ---------------------------------------------------------------------------
# Storage helpers — DEFERRED TO HOST.
#
# Hosts that want to persist snapshots (e.g. aidream's
# scraper.psi_metrics / scraper.gsc_metrics tables) implement
# upsert/get helpers in their own service layer and pass a connection pool
# to them. The package itself stays DB-agnostic so it works equally well
# in a CLI, a notebook, or any other consumer that doesn't have Postgres.
# ---------------------------------------------------------------------------


__all__ = [
    "PsiClient",
    "PsiSnapshot",
    "GscClient",
    "GscErrorCode",
    "GscPageSnapshot",
    "GscQueryRow",
    "PSI_ENDPOINT",
    "GSC_TOKEN_ENDPOINT",
    "GSC_QUERY_ENDPOINT",
    "GSC_SCOPE",
]
