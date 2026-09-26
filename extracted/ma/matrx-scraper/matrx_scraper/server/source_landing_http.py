"""The hosted scraper service's landing hook — ``POST {AIDREAM_URL}/api/sources/land``.

SOURCE-CONVERGENCE §3 "reached two ways": producers that run in THIS service (page-capture,
quick-scrape, search-and-scrape, batch, desktop's ``/content/save``) reach aidream's landing door
over authenticated HTTP. The service may not import aidream, so the hook is registered with
``configure_ext(source_landing=...)`` in the lifespan (``server/app.py``) — only when the process
has no hook yet (aidream, hosting the same routers in-process, wires its own first and that one
stays authoritative).

HOW IT AUTHENTICATES — the two ways the hosted service already talks to aidream, nothing new:

1. **The caller's own login.** A request admitted on a Supabase JWT (desktop, the extension, the
   web app, or aidream forwarding the person's token — ``services/scraper_client/transport.py``)
   carries that token on its context. It is forwarded as-is to ``/api/sources/land`` with the
   admitted ``X-Organization-Id``, so aidream sees the same person the scraper did.
2. **The platform bridge.** A request admitted on the shared service token (an aidream cron, an
   agent run with no person token) has no JWT to forward. The hook then calls the bridge twin
   ``/api/sources/internal/land`` with ``AIDREAM_SERVICE_TOKEN`` + ``X-Matrx-User-Id`` +
   ``X-Organization-Id`` — the same bridge the GSC credential resolution already uses
   (``web_crawl/gsc_sync.py``), whose far side verifies the person's membership in that
   organization before installing the context.

Neither configured → every landing fails LOUDLY on that page's result with the remedy (set
``AIDREAM_URL`` and ``AIDREAM_SERVICE_TOKEN`` on this deployment); nothing is dropped quietly.
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any

import httpx

from matrx_scraper.source_landing import SourceLandingFailed

logger = logging.getLogger("matrx_scraper.server.source_landing_http")

#: A landing is a few database writes and maybe one S3 upload.
LANDING_TIMEOUT_SECONDS = 60.0

_NOT_CONFIGURED_REMEDY = "set_AIDREAM_URL_and_AIDREAM_SERVICE_TOKEN_on_the_scraper_service"


def _context() -> Any:
    try:
        from matrx_connect import try_get_app_context

        return try_get_app_context()
    except Exception:  # noqa: BLE001 — no context is answered below by name
        return None


def _person_token(ctx: Any) -> str:
    """The caller's Supabase JWT, when this request was admitted on one (never the service
    secret: a service-admitted context has no verified JWT claims)."""
    if ctx is None:
        return ""
    metadata = getattr(ctx, "metadata", None) or {}
    token = str(getattr(ctx, "token", "") or "")  # orm-getattr-ok: AppContext, not an ORM model
    if token and isinstance(metadata, dict) and metadata.get("jwt_claims"):
        return token
    return ""


def _refusal(response: Any) -> SourceLandingFailed:
    """The platform's refusal, in its own words.

    aidream's error handler sends a refusal's fields at the TOP LEVEL of the body (``code``,
    ``message``, ``remedy``, beside the envelope's ``error``); a bare FastAPI app nests them under
    ``detail``. Both are read, the top level first, so no refusal collapses into one generic
    sentence."""
    try:
        body: Any = response.json()
    except Exception:  # noqa: BLE001 — a non-JSON refusal is still reported, verbatim
        body = response.text[:300]
    payload: Any = body
    if isinstance(body, dict) and isinstance(body.get("detail"), dict) and not body.get("code"):
        payload = body["detail"]
    if isinstance(payload, dict) and (payload.get("code") or payload.get("error") or payload.get("message")):
        return SourceLandingFailed(
            str(payload.get("code") or payload.get("error") or f"http_{response.status_code}"),
            str(payload.get("message") or f"The platform refused this Source ({response.status_code})."),
            remedy=str(payload.get("remedy") or ""),
        )
    return SourceLandingFailed(
        f"http_{response.status_code}",
        f"The platform refused to save this page as a Source (HTTP {response.status_code}: {str(body)[:200]}).",
        remedy="scrape_it_again",
    )


def make_http_landing_hook(
    *, aidream_url: str, service_token: str
) -> Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]:
    """Build the hook. Missing configuration is reported per landing, loudly, with the remedy."""
    base = (aidream_url or "").strip().rstrip("/")
    bridge_token = (service_token or "").strip()
    if not base:
        logger.error(
            "AIDREAM_URL is not set on the scraper service — every page it scrapes will be "
            "answered WITHOUT becoming a Source, and each result will say so. Remedy: set "
            "AIDREAM_URL (and AIDREAM_SERVICE_TOKEN for unattended calls) on this deployment."
        )

    async def _land(landing: dict[str, Any]) -> dict[str, Any]:
        if not base:
            raise SourceLandingFailed(
                "landing_not_configured",
                "This page was read but not saved as a Source: the scraper service does not know "
                "where the platform is (AIDREAM_URL is not set).",
                remedy=_NOT_CONFIGURED_REMEDY,
            )
        ctx = _context()
        organization_id = str(landing.get("organization_id") or "")
        headers = {"Accept": "application/json", "X-Organization-Id": organization_id}
        jwt = _person_token(ctx)
        if jwt:
            url = f"{base}/api/sources/land"
            headers["Authorization"] = f"Bearer {jwt}"
        elif bridge_token:
            url = f"{base}/api/sources/internal/land"
            headers["Authorization"] = f"Bearer {bridge_token}"
            headers["X-Matrx-User-Id"] = str((landing.get("provenance") or {}).get("user_id") or "")
        else:
            raise SourceLandingFailed(
                "landing_not_authorized",
                "This page was read but not saved as a Source: this request carried no person's "
                "login to forward, and the scraper service has no platform service token "
                "(AIDREAM_SERVICE_TOKEN is not set).",
                remedy=_NOT_CONFIGURED_REMEDY,
            )
        try:
            async with httpx.AsyncClient(timeout=LANDING_TIMEOUT_SECONDS) as http:
                response = await http.post(url, json=landing, headers=headers)
        except httpx.HTTPError as exc:
            raise SourceLandingFailed(
                "landing_unreachable",
                f"This page was read but the platform could not be reached to save it as a Source "
                f"({type(exc).__name__}).",
                remedy="scrape_it_again",
            ) from exc
        if response.status_code >= 400:
            raise _refusal(response)
        return response.json()

    return _land


__all__ = ["LANDING_TIMEOUT_SECONDS", "make_http_landing_hook"]
