"""Unipile HTTP client for HeyLead — all LinkedIn operations go through here.

Handles all LinkedIn operations for HeyLead's scope:
- Hosted auth link creation (setup flow)
- Account listing / polling / verification
- Profile fetching
- People search
- Invitation sending
- Chat/message fetching

Uses direct httpx calls — no Unipile SDK dependency.
"""

from __future__ import annotations

import asyncio
import json
import logging
import re
from datetime import datetime, timedelta, timezone
from typing import Any

import httpx

from .. import config
from ..constants import UNIPILE_POLL_INTERVAL_SECONDS, UNIPILE_POLL_TIMEOUT_SECONDS
from .api_metrics import api_metrics
from .voyager_health import voyager_health

logger = logging.getLogger(__name__)

_TIMEOUT = httpx.Timeout(30.0, connect=30.0, read=30.0, write=60.0)

# Retry configuration for transient failures (send operations only)
_MAX_RETRIES = 3
_RETRY_BACKOFF = [2, 4, 8]  # seconds
_RETRYABLE_STATUS_CODES = {502, 503, 504}

# Unipile source.status values that mean the LinkedIn session is broken
# and the account must be re-authenticated. CREDENTIALS is the common one
# (cookies expired); CHECKPOINT means a 2FA/captcha is pending user action.
UNHEALTHY_SOURCE_STATUSES = frozenset({
    "CREDENTIALS",
    "CHECKPOINT",
    "RECONNECT_NEEDED",
    "DISCONNECTED",
    "ERROR",
    "FAILED",
    "EXPIRED",
    "STOPPED",
})


def interpret_account_status(data: dict[str, Any]) -> tuple[bool, str]:
    """Return (is_connected, message) for a Unipile account payload.

    Unipile's real health signal lives in ``sources[].status`` (the messaging
    source for LinkedIn). The legacy top-level ``status`` field is rarely
    populated, so earlier versions of this check missed CREDENTIALS expiry
    entirely and reported zombie accounts as connected.
    """
    sources = data.get("sources") or []
    for src in sources:
        status = str(src.get("status") or "").upper()
        if status in UNHEALTHY_SOURCE_STATUSES:
            return False, f"LinkedIn session needs reconnection (status: {status})"
    legacy = str(
        data.get("status") or data.get("state") or data.get("connection_status") or ""
    ).lower()
    if legacy in ("disconnected", "error", "failed", "expired"):
        return False, f"Account status: {legacy}"
    return True, "Connected"


# ──────────────────────────────────────────────
# Exceptions
# ──────────────────────────────────────────────

class UnipileError(Exception):
    """Base error for Unipile API failures."""


class UnipileAuthError(UnipileError):
    """Raised when the Unipile account is disconnected or auth fails."""

    def __init__(self, message: str = "") -> None:
        self.message = message or (
            "🔑 LinkedIn account disconnected.\n\n"
            "Run setup_profile again to reconnect your LinkedIn account."
        )
        super().__init__(self.message)


# ──────────────────────────────────────────────
# Error classification for 401/403 responses
# ──────────────────────────────────────────────

def _classify_http_auth_error(status_code: int, body_text: str) -> dict[str, Any]:
    """Classify a 401/403 HTTP response into auth vs permission error.

    Returns dict with error/auth_error/blocked/permanent keys to merge into result.
    """
    lower = body_text.lower() if body_text else ""
    if "subscription_required" in lower or "subscription required" in lower:
        return {"error": "LinkedIn Premium required for this action.", "permanent": True}
    if "not connected" in lower or "not_connected" in lower:
        return {"error": "Cannot message — not a connection.", "permanent": True}
    if status_code == 401:
        return {"error": "LinkedIn account disconnected.", "auth_error": True, "blocked": True}
    # Generic 403 — permission error, not necessarily disconnected
    return {"error": f"Permission denied by LinkedIn.", "permanent": True}


# ──────────────────────────────────────────────
# Error classification for 422 DM responses
# ──────────────────────────────────────────────

def _classify_422_dm_error(body_text: str) -> dict[str, Any]:
    """Classify a 422 response from Unipile DM endpoints.

    Handles known Unipile error types:
    - no_connection_with_recipient: prospect not a 1st-degree connection
    - user_unreachable: recipient disabled incoming messages
    - invalid_recipient: profile locked or bad ID
    - temporary_provider_limit: LinkedIn rate limit (retryable)
    """
    lower = body_text.lower() if body_text else ""
    if "temporary provider limit" in lower or "temporary_provider_limit" in lower:
        return {
            "error": "Unipile returned 422: temporary_provider_limit",
            "blocked": True,
            "rate_limited_422": True,
        }
    if "no_connection_with_recipient" in lower or "not to be first degree" in lower:
        return {
            "error": "Cannot message — not a 1st-degree connection.",
            "permanent": True,
        }
    if "user_unreachable" in lower or "does not allow incoming" in lower:
        return {
            "error": "Recipient does not allow incoming messages.",
            "permanent": True,
        }
    if "invalid_recipient" in lower or "profile is not locked" in lower:
        return {
            "error": "Recipient profile is locked or invalid.",
            "permanent": True,
        }
    if "cannot_resend_yet" in lower or "cannot resend yet" in lower:
        return {"success": True}
    # Unknown 422 — mark permanent to stop retries
    return {
        "error": f"Unipile returned 422: {body_text[:200]}",
        "permanent": True,
    }


# ──────────────────────────────────────────────
# Invitation type filtering
# ──────────────────────────────────────────────

# Non-connection invitation types to filter out (newsletters, events, etc.)
_NON_CONNECTION_TYPES = frozenset({
    "newsletter", "newsletter_subscription", "subscribe",
    "event", "event_invitation",
})

_NEWSLETTER_CONTENT_PATTERNS = [
    "invited you to subscribe",
    "subscribe to my newsletter",
    "subscribe to their newsletter",
    "check out my newsletter",
    "newsletter subscription",
    "invited you to read",
]


def _is_newsletter_invitation(inv: dict[str, Any]) -> bool:
    """Return True if the invitation is a newsletter/event (not a connection request).

    Uses structured field checks + content heuristic since Unipile's
    invitation type field is not well-documented.
    """
    # Structured field checks
    for field in ("type", "invitation_type", "subtype", "category", "kind"):
        val = str(inv.get(field, "")).lower().strip()
        if val and val in _NON_CONNECTION_TYPES:
            return True

    # Content heuristic — scan text fields for newsletter patterns
    text = " ".join(
        str(inv.get(f, ""))
        for f in ("message", "custom_message", "subject", "title", "description", "text")
    ).lower()
    for pattern in _NEWSLETTER_CONTENT_PATTERNS:
        if pattern in text:
            return True

    # No-sender guard — newsletters are entities, not people
    sender_id = (
        inv.get("provider_id") or inv.get("sender_id") or inv.get("from_member_id")
        or inv.get("inviter_id") or inv.get("from_id") or inv.get("member_id")
        or inv.get("user_id") or inv.get("id") or ""
    )
    sender_name = (
        inv.get("sender_name") or inv.get("display_name") or inv.get("name")
        or inv.get("inviter_name") or inv.get("from_name") or inv.get("full_name")
        or inv.get("first_name", "") or ""
    )
    # Check nested sender/inviter objects
    for nested_key in ("sender", "inviter", "from", "user"):
        nested = inv.get(nested_key)
        if isinstance(nested, dict):
            sender_id = sender_id or nested.get("id") or nested.get("provider_id") or ""
            sender_name = sender_name or nested.get("name") or nested.get("display_name") or ""

    if not sender_id and not sender_name:
        logger.debug("Newsletter filter: no sender in invitation keys=%s", list(inv.keys())[:20])
        return True

    return False


# ──────────────────────────────────────────────
# Client
# ──────────────────────────────────────────────

class UnipileClient:
    """Async Unipile HTTP client for LinkedIn operations.

    Config loaded from ~/.heylead/config.json:
        unipile_api_url: e.g. "https://apiXX.unipile.com:XXXXX"
        unipile_api_key: X-API-KEY header value
    """

    def __init__(self, api_url: str, api_key: str) -> None:
        # Clean URL: remove non-printable chars, ensure https://
        raw = re.sub(r"[^\x20-\x7E]", "", api_url.strip()).rstrip("/")
        if not raw.startswith("http://") and not raw.startswith("https://"):
            raw = f"https://{raw}"
        self.base_url = raw
        self.api_key = api_key.strip()
        self._client = httpx.AsyncClient(timeout=_TIMEOUT)

    def _headers(self) -> dict[str, str]:
        return {
            "accept": "application/json",
            "content-type": "application/json",
            "X-API-KEY": self.api_key,
        }

    async def close(self) -> None:
        await self._client.aclose()

    async def _retry_request(
        self,
        method: str,
        url: str,
        *,
        json: dict | None = None,
        params: dict | None = None,
        data: dict | None = None,
        files: dict | None = None,
    ) -> httpx.Response:
        """HTTP request with retry on transient failures.

        Used for send operations (invitation, message, comment, reaction, posts).
        Setup/auth operations should NOT use this — they fail fast.

        For multipart/form-data uploads (e.g., voice messages), pass ``data``
        and ``files`` instead of ``json``.
        """
        import time as _time

        # Derive a short endpoint label from the URL path for metrics
        endpoint_label = url.rsplit("/", 1)[-1] if "/" in url else url

        last_error: Exception | None = None
        for attempt in range(_MAX_RETRIES):
            t0 = _time.monotonic()
            try:
                if method.upper() == "GET":
                    resp = await self._client.get(url, headers=self._headers(), params=params)
                elif data is not None or files is not None:
                    # Multipart form-data (voice messages, profile edit, attachments).
                    # Do NOT pass Content-Type — httpx sets the boundary automatically.
                    headers = self._headers()
                    headers.pop("content-type", None)
                    headers.pop("Content-Type", None)
                    if method.upper() == "PATCH":
                        resp = await self._client.patch(
                            url, data=data or {}, files=files or {}, headers=headers,
                        )
                    else:
                        resp = await self._client.post(
                            url, data=data or {}, files=files or {}, headers=headers,
                        )
                elif method.upper() == "PATCH":
                    resp = await self._client.patch(url, json=json, headers=self._headers())
                else:
                    resp = await self._client.post(url, json=json, headers=self._headers())

                elapsed = int((_time.monotonic() - t0) * 1000)
                api_metrics.record(
                    endpoint_label,
                    status_code=resp.status_code,
                    duration_ms=elapsed,
                    error=resp.text[:200] if resp.status_code >= 400 else "",
                )

                if resp.status_code in _RETRYABLE_STATUS_CODES and attempt < _MAX_RETRIES - 1:
                    delay = _RETRY_BACKOFF[attempt]
                    logger.info(f"Retry {method} {url} (HTTP {resp.status_code}, attempt {attempt + 1}, {delay}s)")
                    await asyncio.sleep(delay)
                    continue
                return resp

            except (httpx.TimeoutException, httpx.ConnectError) as e:
                elapsed = int((_time.monotonic() - t0) * 1000)
                api_metrics.record(
                    endpoint_label, status_code=0, duration_ms=elapsed, error=str(e),
                )
                last_error = e
                if attempt < _MAX_RETRIES - 1:
                    delay = _RETRY_BACKOFF[attempt]
                    logger.info(f"Retry {method} {url} ({type(e).__name__}, attempt {attempt + 1}, {delay}s)")
                    await asyncio.sleep(delay)
                else:
                    raise
        raise last_error or httpx.TimeoutException("All retries exhausted")

    # ── Auth / Account Management ──

    async def create_hosted_auth_link(self, success_redirect_url: str = "") -> str:
        """Create a hosted auth link for LinkedIn OAuth.

        Returns the URL the user should open in their browser.
        """
        # expiresOn: 24h from now, ISO 8601 with exactly 3ms digits
        future = datetime.now(timezone.utc) + timedelta(hours=24)
        expires_on = future.strftime("%Y-%m-%dT%H:%M:%S") + f".{future.microsecond // 1000:03d}Z"

        payload: dict[str, Any] = {
            "expiresOn": expires_on,
            "api_url": self.base_url,
            "type": "create",
            "providers": ["LINKEDIN"],
        }

        if success_redirect_url:
            payload["success_redirect_url"] = success_redirect_url

        url = f"{self.base_url}/api/v1/hosted/accounts/link"
        try:
            resp = await self._client.post(url, json=payload, headers=self._headers())
            resp.raise_for_status()
            result = resp.json()
            auth_url = result.get("url")
            if not auth_url:
                raise UnipileError(f"Unipile response missing 'url': {result}")
            return auth_url
        except httpx.HTTPStatusError as e:
            detail = ""
            try:
                detail = str(e.response.json())
            except Exception:
                detail = e.response.text[:300]
            raise UnipileError(f"Failed to create auth link: {e.response.status_code} — {detail}") from e

    async def list_accounts(self) -> list[dict[str, Any]]:
        """List all accounts from Unipile."""
        url = f"{self.base_url}/api/v1/accounts"
        try:
            resp = await self._client.get(url, headers=self._headers())
            if resp.status_code >= 400:
                logger.warning("list_accounts: status=%d body=%s", resp.status_code, resp.text[:500])
                resp.raise_for_status()
            data = resp.json()

            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                return data.get("items") or data.get("accounts") or data.get("data") or []
            return []
        except Exception as e:
            logger.warning("list_accounts: %s", e)
            raise

    async def find_linkedin_account(self) -> tuple[str | None, str]:
        """Find a LinkedIn account among connected Unipile accounts.

        Returns (account_id, message).
        """
        try:
            accounts = await self.list_accounts()
        except Exception as e:
            return None, f"Failed to list accounts: {e}"

        if not accounts:
            return None, "No accounts found in Unipile."

        def _is_linkedin(acc: dict) -> bool:
            provider = acc.get("provider") or acc.get("provider_type") or acc.get("type") or ""
            return "LINKEDIN" in str(provider).upper()

        linkedin_accounts = [a for a in accounts if _is_linkedin(a)]
        if not linkedin_accounts:
            providers = [a.get("provider") for a in accounts]
            return None, f"No LinkedIn accounts found. Providers: {providers}"

        account = linkedin_accounts[0]
        account_id = (
            account.get("id")
            or account.get("account_id")
            or account.get("accountId")
            or account.get("uuid")
        )
        if account_id:
            return str(account_id), "Found LinkedIn account"
        return None, "LinkedIn account found but no ID field"

    async def verify_account(self, account_id: str) -> tuple[bool, str]:
        """Check if a Unipile account is still connected.

        Returns (is_connected, message).
        """
        try:
            url = f"{self.base_url}/api/v1/accounts/{account_id}"
            resp = await self._client.get(url, headers=self._headers())
            if resp.status_code == 404:
                return False, "Account not found in Unipile"
            resp.raise_for_status()
            data = resp.json()

            is_ok, msg = interpret_account_status(data)
            if not is_ok:
                return False, msg

            provider = (data.get("provider") or data.get("type") or "").upper()
            if provider and "LINKEDIN" not in provider:
                return False, f"Account is not LinkedIn (provider: {provider})"

            return True, "Connected"
        except Exception as e:
            return False, f"Verification error: {e}"

    async def poll_for_account(
        self,
        timeout_seconds: int = UNIPILE_POLL_TIMEOUT_SECONDS,
        interval: int = UNIPILE_POLL_INTERVAL_SECONDS,
    ) -> tuple[str | None, str]:
        """Poll for a LinkedIn account to appear after OAuth.

        Loops every `interval` seconds until timeout.
        Returns (account_id, message).
        """
        elapsed = 0
        while elapsed < timeout_seconds:
            account_id, msg = await self.find_linkedin_account()
            if account_id:
                # Verify it's actually connected
                connected, status = await self.verify_account(account_id)
                if connected:
                    return account_id, "LinkedIn account connected!"
            await asyncio.sleep(interval)
            elapsed += interval

        return None, f"Timed out after {timeout_seconds}s waiting for LinkedIn connection."

    async def get_existing_account_ids(self) -> set[str]:
        """Snapshot all current account IDs (used to detect new accounts)."""
        try:
            accounts = await self.list_accounts()
        except Exception:
            return set()
        ids: set[str] = set()
        for acc in accounts:
            aid = acc.get("id") or acc.get("account_id") or acc.get("accountId") or acc.get("uuid")
            if aid:
                ids.add(str(aid))
        return ids

    async def poll_for_new_account(
        self,
        known_ids: set[str],
        timeout_seconds: int = UNIPILE_POLL_TIMEOUT_SECONDS,
        interval: int = UNIPILE_POLL_INTERVAL_SECONDS,
    ) -> tuple[str | None, str]:
        """Poll for a NEW LinkedIn account that wasn't in known_ids.

        This ensures we only pick up the account the current user just connected,
        not pre-existing accounts from other users on the same Unipile workspace.

        Returns (account_id, message).
        """
        elapsed = 0
        while elapsed < timeout_seconds:
            try:
                accounts = await self.list_accounts()
            except Exception:
                await asyncio.sleep(interval)
                elapsed += interval
                continue

            for acc in accounts:
                aid = acc.get("id") or acc.get("account_id") or acc.get("accountId") or acc.get("uuid")
                if not aid or str(aid) in known_ids:
                    continue
                provider = acc.get("provider") or acc.get("provider_type") or acc.get("type") or ""
                if "LINKEDIN" not in str(provider).upper():
                    continue
                # Found a new LinkedIn account
                account_id = str(aid)
                connected, status = await self.verify_account(account_id)
                if connected:
                    return account_id, "LinkedIn account connected!"

            await asyncio.sleep(interval)
            elapsed += interval

        return None, f"Timed out after {timeout_seconds}s waiting for LinkedIn connection."

    # ── Profile ──

    async def get_own_profile(self, account_id: str) -> dict[str, Any]:
        """Fetch the authenticated user's LinkedIn profile.

        Returns a normalized profile dict matching HeyLead's format.
        """
        url = f"{self.base_url}/api/v1/users/me?account_id={account_id}"
        resp = await self._client.get(url, headers=self._headers())

        if resp.status_code in (401, 403):
            logger.warning("get_own_profile: auth error status=%d body=%s", resp.status_code, resp.text[:500])
            raise UnipileAuthError()
        if resp.status_code != 200:
            logger.warning("get_own_profile: status=%d body=%s", resp.status_code, resp.text[:500])
        resp.raise_for_status()

        data = resp.json()
        if isinstance(data, list) and data:
            data = data[0]

        # Normalize to HeyLead profile format
        first_name = data.get("first_name") or data.get("firstName") or ""
        last_name = data.get("last_name") or data.get("lastName") or ""
        headline = data.get("headline") or data.get("occupation") or ""
        public_id = data.get("public_identifier") or data.get("publicIdentifier") or ""
        provider_id = data.get("provider_id") or data.get("id") or ""

        # Use direct URL from Unipile if available, else construct from public_id
        profile_url = (
            data.get("profile_url")
            or data.get("public_profile_url")
            or data.get("url")
            or ""
        )
        if not profile_url and public_id:
            profile_url = f"https://www.linkedin.com/in/{public_id}"

        # Parse title + company from headline ("Title at Company")
        title = headline
        company = ""
        if " at " in headline:
            parts = headline.rsplit(" at ", 1)
            title = parts[0]
            company = parts[1]

        # Try to get from experience if available
        experience = data.get("experience") or data.get("positions") or []
        if isinstance(experience, list) and experience:
            current = experience[0]
            if isinstance(current, dict):
                title = current.get("title") or current.get("role") or title
                company = current.get("company") or current.get("company_name") or company

        # Extract location
        location = data.get("location") or ""
        if isinstance(location, dict):
            location = location.get("name") or location.get("default") or str(location)

        # Extract skills
        skills_raw = data.get("skills") or []
        skills: list[str] = []
        if isinstance(skills_raw, list):
            for s in skills_raw:
                if isinstance(s, str):
                    skills.append(s)
                elif isinstance(s, dict):
                    skills.append(s.get("name") or s.get("skill") or str(s))

        # Profile picture URL (for photo backup before replacement)
        profile_picture_url = (
            data.get("profile_picture_url")
            or data.get("picture_url")
            or data.get("displayPictureUrl")
            or ""
        )

        return {
            "name": f"{first_name} {last_name}".strip(),
            "first_name": first_name,
            "last_name": last_name,
            "headline": headline,
            "title": title,
            "company": company,
            "location": location,
            "summary": data.get("summary") or data.get("about") or "",
            "industry": data.get("industry") or "",
            "public_id": public_id,
            "provider_id": str(provider_id),
            "profile_url": profile_url,
            "profile_picture_url": profile_picture_url,
            "connections": data.get("connections_count") or data.get("network_info", {}).get("connections_count", 0),
            "is_relationship": data.get("is_relationship", False),
            "network_distance": data.get("network_distance", ""),
            "skills": skills,
            "experience": experience if isinstance(experience, list) else [],
            "posts": [],  # Populated separately via get_posts()
        }

    async def get_posts(
        self, account_id: str, provider_id: str = "", limit: int = 10,
    ) -> list[dict[str, str]]:
        """Fetch recent LinkedIn posts for the user.

        Returns list of {"text": "...", "urn": "..."}.
        """
        identifier = provider_id or account_id
        url = f"{self.base_url}/api/v1/users/{identifier}/posts?account_id={account_id}&limit={limit}"

        try:
            resp = await self._client.get(url, headers=self._headers())
            if resp.status_code in (404, 400):
                logger.info(f"Posts endpoint returned {resp.status_code}, trying fallback")
                return []
            resp.raise_for_status()
            data = resp.json()

            items = []
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict):
                items = data.get("items") or data.get("data") or data.get("posts") or []

            posts: list[dict[str, str]] = []
            for item in items[:limit]:
                text = ""
                if isinstance(item, dict):
                    text = item.get("text") or item.get("body") or item.get("content") or ""
                elif isinstance(item, str):
                    text = item
                if text:
                    urn = ""
                    if isinstance(item, dict):
                        urn = item.get("id") or item.get("urn") or item.get("social_id") or ""
                    posts.append({"text": str(text), "urn": str(urn)})

            return posts
        except Exception as e:
            logger.warning(f"Failed to fetch posts: {e}")
            return []

    # ── Search ──

    async def search_people(
        self,
        account_id: str,
        keywords: str = "",
        title: str = "",
        location: str = "",
        count: int = 25,
        *,
        # Structured search filters (Gap 1 — from ICP enriched codes)
        industry_codes: list[str] | None = None,
        location_codes: list[str] | None = None,
        title_keywords: list[str] | None = None,
        seniority: list[str] | None = None,
        company_headcount: dict[str, int] | None = None,
        company_types: list[str] | None = None,
        department_codes: list[str] | None = None,
        tenure: dict[str, int] | None = None,
        # Sales Navigator support (Gap 2)
        use_sales_navigator: bool = False,
        # Role codes for Sales Navigator
        role_codes: list[str] | None = None,
        # Pagination cursor (Gap 3)
        cursor: str | None = None,
        # Sales Navigator advanced filters
        spotlight: dict[str, bool] | None = None,
        annual_revenue: dict[str, int] | None = None,
        company_headcount_growth: str | None = None,
        network_distance: list[int] | None = None,
    ) -> tuple[list[dict[str, Any]], str | None]:
        """Search LinkedIn for people matching criteria via Unipile.

        Supports both Classic and Sales Navigator search with structured filters.
        Returns (results, next_cursor) tuple for pagination.
        """
        search_query = keywords
        if title and title.lower() not in keywords.lower():
            search_query = f"{title} {keywords}"

        url = f"{self.base_url}/api/v1/linkedin/search?account_id={account_id}"

        # ── Build payload based on search mode ──
        if use_sales_navigator:
            payload = self._build_navigator_payload(
                keywords=search_query,
                count=count,
                industry_codes=industry_codes,
                location_codes=location_codes,
                role_codes=role_codes,
                seniority=seniority,
                company_headcount=company_headcount,
                company_types=company_types,
                department_codes=department_codes,
                tenure=tenure,
                spotlight=spotlight,
                annual_revenue=annual_revenue,
                company_headcount_growth=company_headcount_growth,
            )
        else:
            payload = self._build_classic_payload(
                keywords=search_query,
                count=count,
                industry_codes=industry_codes,
                location_codes=location_codes,
                title_keywords=title_keywords,
            )

        if cursor:
            payload["cursor"] = cursor
        if network_distance:
            payload["network_distance"] = network_distance

        try:
            resp = await self._client.post(url, json=payload, headers=self._headers())
            if resp.status_code in (401, 403):
                logger.warning("search_people: status=%d body=%s", resp.status_code, resp.text[:500])
                raise UnipileAuthError()
            if resp.status_code >= 400:
                logger.warning("search_people: status=%d body=%s", resp.status_code, resp.text[:500])
                resp.raise_for_status()
            data = resp.json()

            items = data.get("items") or data.get("results") or data.get("data") or []
            if isinstance(data, list):
                items = data

            # Extract pagination cursor
            next_cursor = None
            if isinstance(data, dict):
                next_cursor = data.get("cursor") or data.get("next_cursor") or data.get("paging", {}).get("cursor")

            results = self._parse_search_results(items)
            return results, next_cursor
        except UnipileAuthError:
            raise
        except Exception as e:
            logger.warning(f"Unipile search error: {e}")
            return [], None

    def _build_classic_payload(
        self,
        keywords: str,
        count: int,
        industry_codes: list[str] | None = None,
        location_codes: list[str] | None = None,
        title_keywords: list[str] | None = None,
    ) -> dict[str, Any]:
        """Build a Classic LinkedIn search payload with structured filters."""
        payload: dict[str, Any] = {
            "api": "classic",
            "category": "people",
            "limit": min(count, 50),
        }

        if keywords:
            payload["keywords"] = keywords

        # Structured filters (LinkedIn internal codes)
        if industry_codes:
            payload["industry"] = industry_codes
        if location_codes:
            payload["location"] = location_codes
        if title_keywords:
            # Classic uses advanced_keywords.title with OR logic
            payload["advanced_keywords"] = {
                "title": " OR ".join(title_keywords),
            }

        return payload

    def _build_navigator_payload(
        self,
        keywords: str,
        count: int,
        industry_codes: list[str] | None = None,
        location_codes: list[str] | None = None,
        role_codes: list[str] | None = None,
        seniority: list[str] | None = None,
        company_headcount: dict[str, int] | None = None,
        company_types: list[str] | None = None,
        department_codes: list[str] | None = None,
        tenure: dict[str, int] | None = None,
        spotlight: dict[str, bool] | None = None,
        annual_revenue: dict[str, int] | None = None,
        company_headcount_growth: str | None = None,
    ) -> dict[str, Any]:
        """Build a Sales Navigator search payload with full structured filters."""
        payload: dict[str, Any] = {
            "api": "sales_navigator",
            "category": "people",
            "limit": min(count, 100),  # Navigator supports up to 100 per page
        }

        if keywords:
            payload["keywords"] = keywords

        # Include/exclude patterns for Navigator
        if industry_codes:
            payload["industry"] = {"include": industry_codes}
        if location_codes:
            payload["location"] = {"include": location_codes}
        if role_codes:
            payload["role"] = {"include": role_codes}
        if seniority:
            payload["seniority"] = {"include": seniority}
        if company_headcount:
            payload["company_headcount"] = [company_headcount]
        if company_types:
            payload["company_type"] = company_types
        if department_codes:
            payload["function"] = {"include": department_codes}
        if tenure:
            payload["tenure"] = [tenure]
        if spotlight:
            payload["spotlight"] = spotlight
        if annual_revenue:
            payload["annual_revenue"] = annual_revenue
        if company_headcount_growth:
            payload["company_headcount_growth"] = company_headcount_growth

        return payload

    @staticmethod
    def _parse_search_results(items: list) -> list[dict[str, Any]]:
        """Parse Unipile search result items into normalized prospect dicts."""
        results: list[dict[str, Any]] = []
        for item in items:
            if not isinstance(item, dict):
                continue

            name_parts = []
            if item.get("first_name") or item.get("firstName"):
                name_parts.append(item.get("first_name") or item.get("firstName") or "")
            if item.get("last_name") or item.get("lastName"):
                name_parts.append(item.get("last_name") or item.get("lastName") or "")
            name = " ".join(name_parts).strip() or item.get("name") or ""

            if not name:
                continue

            headline = item.get("headline") or ""
            pub_id = item.get("public_identifier") or item.get("publicIdentifier") or ""
            prov_id = item.get("provider_id") or item.get("id") or item.get("member_urn") or ""

            # Parse title + company from headline
            parsed_title = headline
            parsed_company = ""
            if " at " in headline:
                parts = headline.rsplit(" at ", 1)
                parsed_title = parts[0]
                parsed_company = parts[1]

            loc = item.get("location") or ""
            if isinstance(loc, dict):
                loc = loc.get("name") or loc.get("default") or ""

            profile_url = item.get("profile_url") or item.get("public_profile_url") or ""
            if not profile_url and pub_id:
                profile_url = f"https://www.linkedin.com/in/{pub_id}"

            results.append({
                "name": name,
                "title": parsed_title,
                "company": parsed_company,
                "headline": headline,
                "location": str(loc),
                "linkedin_url": profile_url,
                "public_id": pub_id,
                "provider_id": str(prov_id),
            })
        return results

    # ── Sales Navigator Detection (Gap 2) ──

    async def detect_sales_navigator(self, account_id: str) -> bool:
        """Check if the LinkedIn account has Sales Navigator access.

        Two-step: metadata check (fast negative) then actual search verification.
        Unipile caches premiumFeatures from initial connection — may be stale.
        """
        # Step 1: fast negative from metadata
        url = f"{self.base_url}/api/v1/accounts/{account_id}"
        try:
            resp = await self._client.get(url, headers=self._headers())
            if resp.status_code != 200:
                logger.warning("detect_sales_navigator: metadata check status=%d", resp.status_code)
                return False
            data = resp.json()
            cp = data.get("connection_params") or {}
            im = cp.get("im") or {}
            features = im.get("premiumFeatures") or []
            if "sales_navigator" not in features:
                return False
        except Exception as e:
            logger.warning("detect_sales_navigator: metadata check failed: %s", e)
            return False

        # Step 2: verify with actual Sales Nav search
        search_url = f"{self.base_url}/api/v1/linkedin/search?account_id={account_id}"
        payload = {
            "api": "sales_navigator",
            "category": "people",
            "keywords": "test",
            "limit": 1,
        }
        try:
            resp = await self._client.post(search_url, json=payload, headers=self._headers())
            return resp.status_code == 200
        except Exception as e:
            logger.warning("detect_sales_navigator: search verify failed: %s", e)
            return False

    # ── Post Search ──

    async def search_posts(
        self,
        account_id: str,
        keywords: str,
        limit: int = 25,
        *,
        cursor: str | None = None,
    ) -> tuple[list[dict[str, Any]], str | None]:
        """Search LinkedIn posts by keywords via Unipile.

        Finds posts containing specific topics — useful for intent-based
        targeting (e.g., find prospects who posted about "data migration").

        Args:
            account_id: The Unipile account ID.
            keywords: Search keywords to find posts about.
            limit: Max results per page.
            cursor: Pagination cursor from a previous call.

        Returns:
            (results, next_cursor) — list of post dicts + cursor for next page.
        """
        url = f"{self.base_url}/api/v1/linkedin/search?account_id={account_id}"
        payload: dict[str, Any] = {
            "api": "classic",
            "category": "posts",
            "keywords": keywords,
            "limit": min(limit, 50),
        }
        if cursor:
            payload["cursor"] = cursor

        try:
            resp = await self._client.post(url, json=payload, headers=self._headers())
            if resp.status_code in (401, 403):
                raise UnipileAuthError()
            resp.raise_for_status()
            data = resp.json()

            items = data.get("items") or data.get("results") or data.get("data") or []
            if isinstance(data, list):
                items = data

            next_cursor = None
            if isinstance(data, dict):
                next_cursor = data.get("cursor") or data.get("next_cursor") or data.get("paging", {}).get("cursor")

            posts: list[dict[str, Any]] = []
            for item in items:
                if not isinstance(item, dict):
                    continue
                # Extract author info
                author = item.get("author") or {}
                if isinstance(author, str):
                    author = {"name": author}
                # Extract attachments for media type detection
                attachments = item.get("attachments") or []
                media_type = "text"
                if attachments and isinstance(attachments, list):
                    for att in attachments:
                        att_type = (att.get("type") or "").lower() if isinstance(att, dict) else ""
                        if "video" in att_type:
                            media_type = "video"
                            break
                        elif "image" in att_type:
                            media_type = "image"
                        elif "document" in att_type or "pdf" in att_type:
                            media_type = "document"
                        elif "article" in att_type or "link" in att_type:
                            media_type = "article"
                elif item.get("poll"):
                    media_type = "poll"

                posts.append({
                    "post_id": item.get("id") or item.get("post_id") or "",
                    "text": item.get("text") or item.get("body") or item.get("content") or "",
                    "author_name": author.get("name") or author.get("display_name") or "",
                    "author_id": str(author.get("provider_id") or author.get("id") or ""),
                    "author_headline": author.get("headline") or "",
                    "author_url": author.get("profile_url") or author.get("public_profile_url") or "",
                    "reactions_count": item.get("reactions_count") or item.get("reaction_counter") or item.get("likes") or 0,
                    "comments_count": item.get("comments_count") or item.get("comment_counter") or item.get("comments") or 0,
                    "impressions_count": item.get("impressions_counter") or item.get("impressions_count") or item.get("views_count") or 0,
                    "reposts_count": item.get("repost_counter") or item.get("reposts_count") or item.get("shares_count") or 0,
                    "timestamp": item.get("timestamp") or item.get("created_at") or item.get("parsed_datetime") or "",
                    "share_url": item.get("share_url") or "",
                    "is_repost": bool(item.get("is_repost")),
                    "is_edited": bool(item.get("is_edited")),
                    "visibility": item.get("visibility") or "",
                    "media_type": media_type,
                    "is_company": bool(author.get("is_company")),
                    "author_company": author.get("company") or "",
                })
            return posts, next_cursor
        except UnipileAuthError:
            raise
        except Exception as e:
            logger.warning(f"Unipile post search error: {e}")
            return [], None

    # ── Company Search ──

    async def search_companies(
        self,
        account_id: str,
        keywords: str,
        limit: int = 25,
        *,
        cursor: str | None = None,
    ) -> tuple[list[dict[str, Any]], str | None]:
        """Search LinkedIn companies by keywords via Unipile.

        Discovers target companies matching ICP criteria.

        Args:
            account_id: The Unipile account ID.
            keywords: Search keywords (industry, company name, etc.).
            limit: Max results per page.
            cursor: Pagination cursor from a previous call.

        Returns:
            (results, next_cursor) — list of company dicts + cursor for next page.
        """
        url = f"{self.base_url}/api/v1/linkedin/search?account_id={account_id}"
        payload: dict[str, Any] = {
            "api": "classic",
            "category": "companies",
            "keywords": keywords,
            "limit": min(limit, 50),
        }
        if cursor:
            payload["cursor"] = cursor

        try:
            resp = await self._client.post(url, json=payload, headers=self._headers())
            if resp.status_code in (401, 403):
                raise UnipileAuthError()
            resp.raise_for_status()
            data = resp.json()

            items = data.get("items") or data.get("results") or data.get("data") or []
            if isinstance(data, list):
                items = data

            next_cursor = None
            if isinstance(data, dict):
                next_cursor = data.get("cursor") or data.get("next_cursor") or data.get("paging", {}).get("cursor")

            companies: list[dict[str, Any]] = []
            for item in items:
                if not isinstance(item, dict):
                    continue
                companies.append({
                    "company_id": item.get("id") or item.get("company_id") or "",
                    "name": item.get("name") or item.get("title") or "",
                    "industry": item.get("industry") or "",
                    "size": item.get("size") or item.get("company_size") or "",
                    "employee_count": item.get("employee_count") or item.get("employeeCount") or 0,
                    "description": item.get("description") or item.get("tagline") or "",
                    "website": item.get("website") or "",
                    "logo_url": item.get("logo_url") or item.get("logo") or "",
                    "linkedin_url": item.get("url") or item.get("linkedin_url") or item.get("public_profile_url") or "",
                    "location": item.get("location") or item.get("headquarters") or "",
                })
            return companies, next_cursor
        except UnipileAuthError:
            raise
        except Exception as e:
            logger.warning(f"Unipile company search error: {e}")
            return [], None

    # ── Job Search (Intent Signals) ──

    async def search_jobs(
        self,
        account_id: str,
        keywords: str,
        limit: int = 25,
        *,
        cursor: str | None = None,
    ) -> tuple[list[dict[str, Any]], str | None]:
        """Search LinkedIn job postings by keywords via Unipile.

        Finds companies hiring for specific roles — a strong buying-intent signal.
        E.g., companies hiring "data engineer" may need data tools.

        Args:
            account_id: The Unipile account ID.
            keywords: Search keywords (job title, skill, etc.).
            limit: Max results per page.
            cursor: Pagination cursor from a previous call.

        Returns:
            (results, next_cursor) — list of job dicts + cursor for next page.
        """
        url = f"{self.base_url}/api/v1/linkedin/search?account_id={account_id}"
        payload: dict[str, Any] = {
            "api": "classic",
            "category": "jobs",
            "keywords": keywords,
            "limit": min(limit, 50),
        }
        if cursor:
            payload["cursor"] = cursor

        try:
            resp = await self._client.post(url, json=payload, headers=self._headers())
            if resp.status_code in (401, 403):
                raise UnipileAuthError()
            resp.raise_for_status()
            data = resp.json()

            items = data.get("items") or data.get("results") or data.get("data") or []
            if isinstance(data, list):
                items = data

            next_cursor = None
            if isinstance(data, dict):
                next_cursor = data.get("cursor") or data.get("next_cursor") or data.get("paging", {}).get("cursor")

            jobs: list[dict[str, Any]] = []
            for item in items:
                if not isinstance(item, dict):
                    continue
                company = item.get("company") or {}
                if isinstance(company, str):
                    company = {"name": company}
                jobs.append({
                    "job_id": item.get("id") or item.get("job_id") or "",
                    "title": item.get("title") or item.get("name") or "",
                    "company_name": company.get("name") or item.get("company_name") or "",
                    "company_id": str(company.get("id") or company.get("provider_id") or ""),
                    "company_url": company.get("url") or company.get("linkedin_url") or "",
                    "location": item.get("location") or "",
                    "description": (item.get("description") or item.get("body") or "")[:500],
                    "posted_at": item.get("posted_at") or item.get("timestamp") or item.get("created_at") or "",
                    "applicants": item.get("applicants") or item.get("applicant_count") or 0,
                    "linkedin_url": item.get("url") or item.get("linkedin_url") or "",
                })
            return jobs, next_cursor
        except UnipileAuthError:
            raise
        except Exception as e:
            logger.warning(f"Unipile job search error: {e}")
            return [], None

    # ── Full Profile Enrichment (Gap 4) ──

    async def get_profile(
        self,
        account_id: str,
        identifier: str,
        use_sales_navigator: bool = False,
    ) -> dict[str, Any]:
        """Fetch full LinkedIn profile with all sections (experience, skills, etc.).

        Unlike get_own_profile() which fetches the authenticated user's profile,
        this fetches ANY user's profile by their public_id or provider_id.

        Args:
            account_id: The Unipile account ID.
            identifier: The user's public_identifier or provider_id.
            use_sales_navigator: If True, use Sales Navigator API for richer data.

        Returns:
            Full profile dict with all available LinkedIn sections.
        """
        url = f"{self.base_url}/api/v1/users/{identifier}"
        params: dict[str, str] = {
            "account_id": account_id,
            "linkedin_sections": "*",  # Request ALL sections
        }
        if use_sales_navigator:
            params["linkedin_api"] = "sales_navigator"

        try:
            resp = await self._retry_request("GET", url, params=params)
            if resp.status_code in (404, 400):
                logger.info("get_profile: status=%d identifier=%s body=%s", resp.status_code, identifier[:20], resp.text[:300])
                return {}
            if resp.status_code in (401, 403):
                logger.warning("get_profile: status=%d identifier=%s body=%s", resp.status_code, identifier[:20], resp.text[:500])
                raise UnipileAuthError()
            if resp.status_code >= 400:
                logger.warning("get_profile: status=%d identifier=%s body=%s", resp.status_code, identifier[:20], resp.text[:500])
                resp.raise_for_status()
            data = resp.json()

            if isinstance(data, list) and data:
                data = data[0]
            if not isinstance(data, dict):
                return {}

            # Normalize to HeyLead's profile format
            first_name = data.get("first_name") or data.get("firstName") or ""
            last_name = data.get("last_name") or data.get("lastName") or ""
            headline = data.get("headline") or data.get("occupation") or ""

            parsed_title = headline
            parsed_company = ""
            if " at " in headline:
                parts = headline.rsplit(" at ", 1)
                parsed_title = parts[0]
                parsed_company = parts[1]

            experience = data.get("experience") or data.get("positions") or []
            if isinstance(experience, list) and experience:
                current = experience[0]
                if isinstance(current, dict):
                    parsed_title = current.get("title") or current.get("role") or parsed_title
                    parsed_company = current.get("company") or current.get("company_name") or parsed_company

            loc = data.get("location") or ""
            if isinstance(loc, dict):
                loc = loc.get("name") or loc.get("default") or str(loc)

            skills_raw = data.get("skills") or []
            skills: list[str] = []
            if isinstance(skills_raw, list):
                for s in skills_raw:
                    if isinstance(s, str):
                        skills.append(s)
                    elif isinstance(s, dict):
                        skills.append(s.get("name") or s.get("skill") or str(s))

            pub_id = data.get("public_identifier") or data.get("publicIdentifier") or ""
            prov_id = data.get("provider_id") or data.get("id") or ""

            # Use direct URL from Unipile if available, else construct from public_id
            prof_url = (
                data.get("profile_url")
                or data.get("public_profile_url")
                or data.get("url")
                or ""
            )
            if not prof_url and pub_id:
                prof_url = f"https://www.linkedin.com/in/{pub_id}"

            return {
                "name": f"{first_name} {last_name}".strip(),
                "first_name": first_name,
                "last_name": last_name,
                "headline": headline,
                "title": parsed_title,
                "company": parsed_company,
                "location": str(loc),
                "summary": data.get("summary") or data.get("about") or "",
                "industry": data.get("industry") or "",
                "public_id": pub_id,
                "provider_id": str(prov_id),
                "profile_url": prof_url,
                "connections": data.get("connections_count") or data.get("network_info", {}).get("connections_count", 0),
                "is_relationship": data.get("is_relationship", False),
                "network_distance": data.get("network_distance", ""),
                "skills": skills,
                "experience": experience if isinstance(experience, list) else [],
                "education": data.get("education") or [],
                "certifications": data.get("certifications") or [],
                "publications": data.get("publications") or [],
                "languages": data.get("languages") or [],
                "volunteer": data.get("volunteer_experience") or data.get("volunteer") or [],
                "honors": data.get("honors_awards") or data.get("honors") or [],
            }
        except UnipileAuthError:
            raise
        except Exception as e:
            logger.warning(f"Profile fetch error for {identifier}: {e}")
            return {}

    # ── Relation Pre-check (Gap 5) ──

    async def check_existing_relation(
        self,
        account_id: str,
        provider_id: str,
    ) -> dict[str, Any]:
        """Check if we already have a relation with a prospect.

        Checks for:
        - Existing connection
        - Pending invitation
        - Existing chat/conversation

        Returns:
            {"connected": bool, "pending_invite": bool, "has_chat": bool, "chat_id": str}
        """
        result = {
            "connected": False,
            "pending_invite": False,
            "has_chat": False,
            "chat_id": "",
        }

        # Check pending invitations
        try:
            inv_url = f"{self.base_url}/api/v1/users/invite/sent?account_id={account_id}"
            resp = await self._client.get(inv_url, headers=self._headers())
            if resp.status_code == 200:
                inv_data = resp.json()
                invitations = inv_data.get("items") or inv_data.get("data") or []
                if isinstance(inv_data, list):
                    invitations = inv_data
                for inv in invitations:
                    if not isinstance(inv, dict):
                        continue
                    inv_prov_id = (
                        inv.get("invited_user_id")
                        or inv.get("provider_id") or inv.get("id")
                        or inv.get("to_member_id") or ""
                    )
                    if str(inv_prov_id) == str(provider_id):
                        result["pending_invite"] = True
                        break
        except Exception as e:
            logger.debug(f"Invitation check skipped: {e}")

        # Check existing chat (indicates connection)
        try:
            chat_id = await self.find_chat_for_user(account_id, provider_id)
            if chat_id:
                result["has_chat"] = True
                result["chat_id"] = chat_id
                result["connected"] = True
        except Exception as e:
            logger.debug(f"Chat check skipped: {e}")

        return result

    async def find_chat_for_user(
        self,
        account_id: str,
        prospect_linkedin_id: str,
    ) -> str | None:
        """Find the chat_id for a conversation with a specific prospect.

        Two-phase lookup:
        1. Scan recent chats (up to 3 pages × 50) for a matching attendee.
        2. Fallback: POST /api/v1/chats with attendees_ids (no text) — Unipile
           returns the existing chat or creates one, giving us the chat_id.
        """
        # ── Phase 1: scan recent chats (paginated, up to 3 pages) ──
        cursor: str | None = None
        MAX_PAGES = 3

        try:
            for _page in range(MAX_PAGES):
                url = f"{self.base_url}/api/v1/chats?account_id={account_id}&limit=50"
                if cursor:
                    url += f"&cursor={cursor}"
                resp = await self._client.get(url, headers=self._headers())
                if resp.status_code != 200:
                    break
                data = resp.json()

                items = data.get("items") or data.get("chats") or data.get("data") or []
                if isinstance(data, list):
                    items = data

                for chat in items:
                    if not isinstance(chat, dict):
                        continue
                    chat_id = chat.get("id") or chat.get("chat_id") or ""
                    if not chat_id:
                        continue
                    att_pid = chat.get("attendee_provider_id") or ""
                    if str(att_pid) == str(prospect_linkedin_id):
                        return str(chat_id)
                    attendees = chat.get("attendees") or []
                    for att in attendees:
                        if not isinstance(att, dict):
                            continue
                        for key in ("provider_id", "public_identifier", "id"):
                            att_id = att.get(key, "")
                            if att_id and str(att_id) == str(prospect_linkedin_id):
                                return str(chat_id)

                # Advance cursor for next page
                next_cursor = None
                if isinstance(data, dict):
                    next_cursor = data.get("cursor") or data.get("next_cursor") or data.get("paging", {}).get("cursor")
                if not next_cursor or not items:
                    break
                cursor = next_cursor

        except Exception as e:
            logger.warning(f"find_chat_for_user scan failed: {e}")

        # ── Phase 2: fallback via POST /chats (Unipile resolves/creates chat) ──
        try:
            post_url = f"{self.base_url}/api/v1/chats"
            payload = {
                "account_id": account_id,
                "attendees_ids": [prospect_linkedin_id],
            }
            resp = await self._client.post(post_url, json=payload, headers=self._headers())
            if resp.status_code in (200, 201):
                data = resp.json()
                chat_id = data.get("chat_id") or data.get("id") or ""
                if chat_id:
                    logger.info(
                        "find_chat_for_user resolved via POST /chats: %s",
                        chat_id[:30],
                    )
                    return str(chat_id)
            else:
                logger.warning(
                    "find_chat_for_user POST /chats fallback failed: status=%d body=%s",
                    resp.status_code, resp.text[:300],
                )
        except Exception as e:
            logger.warning(f"find_chat_for_user POST fallback failed: {e}")

        return None

    # ── Search Parameters ──

    async def get_search_params(
        self, account_id: str, type: str, keywords: str,
    ) -> list[dict[str, str]]:
        """Look up LinkedIn search parameter codes via Unipile.

        Args:
            account_id: The Unipile account ID.
            type: Parameter type (LOCATION, INDUSTRY, JOB_TITLE, DEPARTMENT, etc.)
            keywords: Search keywords to look up codes for.

        Returns:
            List of {name, code} dicts.
        """
        url = f"{self.base_url}/api/v1/linkedin/search/parameters"
        params = {
            "account_id": account_id,
            "type": type,
            "keywords": keywords,
        }
        try:
            resp = await self._client.get(url, headers=self._headers(), params=params)
            resp.raise_for_status()
            data = resp.json()
            items = data.get("items") or []
            return [
                {"name": item.get("title", ""), "code": str(item.get("id", ""))}
                for item in items
                if item.get("title") and item.get("id")
            ]
        except Exception as e:
            logger.warning(f"Search params lookup failed: {e}")
            return []

    # ── Messaging ──

    async def send_invitation(
        self,
        account_id: str,
        provider_id: str,
        message: str = "",
    ) -> dict[str, Any]:
        """Send a LinkedIn connection invitation via Unipile.

        Returns {"success": bool, "error": str, "blocked": bool, "auth_error": bool}.
        """
        result: dict[str, Any] = {"success": False, "error": "", "blocked": False, "auth_error": False}

        url = f"{self.base_url}/api/v1/users/invite"
        payload: dict[str, Any] = {
            "account_id": account_id,
            "provider_id": provider_id,
        }
        if message:
            payload["message"] = message[:200]

        try:
            resp = await self._retry_request("POST", url, json=payload)

            if resp.status_code in (200, 201):
                result["success"] = True
                try:
                    body = resp.json()
                    result["invitation_id"] = body.get("invitation_id") or body.get("id") or ""
                    result["response_status"] = body.get("status") or ""
                except Exception:
                    pass
            elif resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After", "")
                wait_msg = f" Retry after {retry_after}s." if retry_after else ""
                result["error"] = f"Rate limited by LinkedIn. Will retry later.{wait_msg}"
                result["blocked"] = True
                if retry_after:
                    try:
                        result["retry_after_seconds"] = int(retry_after)
                    except ValueError:
                        pass
            elif resp.status_code in (401, 403):
                result.update(_classify_http_auth_error(resp.status_code, resp.text[:500]))
            elif resp.status_code == 409:
                result["error"] = "Already connected or invitation pending."
            elif resp.status_code == 422:
                body = resp.text[:500]
                body_lower = body.lower()
                if "temporary provider limit" in body_lower or "temporary_provider_limit" in body_lower:
                    result["error"] = "Unipile returned 422: temporary_provider_limit"
                    result["blocked"] = True
                    result["rate_limited_422"] = True
                elif "cannot_resend_yet" in body_lower or "cannot resend yet" in body_lower:
                    result["success"] = True
                elif "already_invited_recently" in body_lower or "already invited" in body_lower:
                    # Invite was already sent — treat as success so outreach is marked "invited"
                    result["success"] = True
                else:
                    result["error"] = f"Unipile returned 422: {body[:200]}"
            else:
                body = resp.text[:200]
                result["error"] = f"Unipile returned {resp.status_code}: {body}"

        except httpx.TimeoutException:
            result["error"] = "Request timed out after retries. Check your internet connection."
        except Exception as e:
            result["error"] = f"Send failed: {e}"

        if result.get("success"):
            logger.info("send_invitation: success provider_id=%s", provider_id)
        elif result.get("error"):
            logger.warning("send_invitation: %s provider_id=%s", result["error"], provider_id)
        return result

    # ── DM Messaging ──

    async def send_message(
        self,
        account_id: str,
        chat_id: str,
        text: str,
    ) -> dict[str, Any]:
        """Send a DM message in an existing LinkedIn chat/conversation.

        Args:
            account_id: The Unipile account ID.
            chat_id: The chat/conversation ID to send the message in.
            text: The message text to send.

        Returns:
            {"success": bool, "error": str}
        """
        result: dict[str, Any] = {"success": False, "error": ""}
        url = f"{self.base_url}/api/v1/chats/{chat_id}/messages"
        payload = {
            "account_id": account_id,
            "text": text,
        }
        try:
            resp = await self._retry_request("POST", url, json=payload)
            if resp.status_code in (200, 201):
                result["success"] = True
                try:
                    body = resp.json()
                    result["message_id"] = body.get("message_id") or body.get("id") or ""
                except Exception:
                    pass
            elif resp.status_code in (401, 403):
                result.update(_classify_http_auth_error(resp.status_code, resp.text[:500]))
            elif resp.status_code == 422:
                result.update(_classify_422_dm_error(resp.text[:500]))
            elif resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After", "")
                wait_msg = f" Retry after {retry_after}s." if retry_after else ""
                result["error"] = f"Rate limited by LinkedIn.{wait_msg}"
                result["blocked"] = True
                if retry_after:
                    try:
                        result["retry_after_seconds"] = int(retry_after)
                    except ValueError:
                        pass
            else:
                body = resp.text[:200]
                result["error"] = f"Unipile returned {resp.status_code}: {body}"
        except httpx.TimeoutException:
            result["error"] = "Request timed out after retries."
        except Exception as e:
            result["error"] = f"Send failed: {e}"
        if result.get("success"):
            logger.info("send_message: success chat_id=%s", chat_id)
        elif result.get("error"):
            logger.warning("send_message: %s chat_id=%s", result["error"], chat_id)
        return result

    async def send_new_message(
        self,
        account_id: str,
        provider_id: str,
        text: str,
    ) -> dict[str, Any]:
        """Start a new DM conversation with a connected LinkedIn user.

        Creates a new chat via POST /api/v1/chats and sends the first message.
        Use this when no existing chat exists (e.g., first follow-up after
        connection acceptance).

        Args:
            account_id: The Unipile account ID.
            provider_id: LinkedIn provider_id of the recipient.
            text: The message text to send.

        Returns:
            {"success": bool, "error": str, "chat_id": str}
        """
        result: dict[str, Any] = {"success": False, "error": "", "chat_id": ""}
        url = f"{self.base_url}/api/v1/chats"
        payload = {
            "account_id": account_id,
            "attendees_ids": [provider_id],
            "text": text,
        }
        try:
            resp = await self._retry_request("POST", url, json=payload)
            if resp.status_code in (200, 201):
                data = resp.json()
                result["success"] = True
                result["chat_id"] = data.get("chat_id") or data.get("id") or ""
            elif resp.status_code in (401, 403):
                result.update(_classify_http_auth_error(resp.status_code, resp.text[:500]))
            elif resp.status_code == 422:
                result.update(_classify_422_dm_error(resp.text[:500]))
            elif resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After", "")
                wait_msg = f" Retry after {retry_after}s." if retry_after else ""
                result["error"] = f"Rate limited by LinkedIn.{wait_msg}"
                result["blocked"] = True
                if retry_after:
                    try:
                        result["retry_after_seconds"] = int(retry_after)
                    except ValueError:
                        pass
            else:
                body = resp.text[:200]
                result["error"] = f"Unipile returned {resp.status_code}: {body}"
        except httpx.TimeoutException:
            result["error"] = "Request timed out after retries."
        except Exception as e:
            result["error"] = f"Send new message failed: {e}"
        if result.get("success"):
            logger.info("send_new_message: success provider_id=%s", provider_id)
        elif result.get("error"):
            logger.warning("send_new_message: %s provider_id=%s", result["error"], provider_id)
        return result

    # ── Voice Messages ──

    async def send_voice_message(
        self,
        account_id: str,
        chat_id: str,
        audio_path: str,
        text: str = "",
    ) -> dict[str, Any]:
        """Send a voice message in an existing LinkedIn chat via multipart upload.

        Args:
            account_id: The Unipile account ID.
            chat_id: The chat/conversation ID.
            audio_path: Local path to the MP3 audio file.
            text: Optional accompanying text message.

        Returns:
            {"success": bool, "error": str}
        """
        result: dict[str, Any] = {"success": False, "error": ""}
        url = f"{self.base_url}/api/v1/chats/{chat_id}/messages"
        form_data = {"account_id": account_id}
        if text:
            form_data["text"] = text
        try:
            with open(audio_path, "rb") as f:
                files = {"voice_message": ("voice.mp3", f, "audio/mpeg")}
                resp = await self._retry_request(
                    "POST", url, data=form_data, files=files,
                )
            if resp.status_code in (200, 201):
                result["success"] = True
                try:
                    body = resp.json()
                    result["message_id"] = body.get("message_id") or body.get("id") or ""
                except Exception:
                    pass
            elif resp.status_code in (401, 403):
                result.update(_classify_http_auth_error(resp.status_code, resp.text[:500]))
            elif resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After", "")
                wait_msg = f" Retry after {retry_after}s." if retry_after else ""
                result["error"] = f"Rate limited by LinkedIn.{wait_msg}"
                result["blocked"] = True
                if retry_after:
                    try:
                        result["retry_after_seconds"] = int(retry_after)
                    except ValueError:
                        pass
            else:
                body = resp.text[:200]
                result["error"] = f"Unipile returned {resp.status_code}: {body}"
        except FileNotFoundError:
            result["error"] = f"Audio file not found: {audio_path}"
        except httpx.TimeoutException:
            result["error"] = "Request timed out after retries."
        except Exception as e:
            result["error"] = f"Voice send failed: {e}"
        if result.get("success"):
            logger.info("send_voice_message: success chat_id=%s", chat_id)
        elif result.get("error"):
            logger.warning("send_voice_message: %s chat_id=%s", result["error"], chat_id)
        return result

    async def send_new_voice_message(
        self,
        account_id: str,
        provider_id: str,
        audio_path: str,
        text: str = "",
    ) -> dict[str, Any]:
        """Start a new DM with a voice message via multipart upload.

        Creates a new chat via POST /api/v1/chats and sends a voice note.
        Use when no existing chat exists (e.g., first follow-up after connection).

        Args:
            account_id: The Unipile account ID.
            provider_id: LinkedIn provider_id of the recipient.
            audio_path: Local path to the MP3 audio file.
            text: Optional accompanying text message.

        Returns:
            {"success": bool, "error": str, "chat_id": str}
        """
        result: dict[str, Any] = {"success": False, "error": "", "chat_id": ""}
        url = f"{self.base_url}/api/v1/chats"
        form_data = {
            "account_id": account_id,
            "attendees_ids": provider_id,
        }
        if text:
            form_data["text"] = text
        try:
            with open(audio_path, "rb") as f:
                files = {"voice_message": ("voice.mp3", f, "audio/mpeg")}
                resp = await self._retry_request(
                    "POST", url, data=form_data, files=files,
                )
            if resp.status_code in (200, 201):
                data = resp.json()
                result["success"] = True
                result["chat_id"] = data.get("chat_id") or data.get("id") or ""
            elif resp.status_code in (401, 403):
                result.update(_classify_http_auth_error(resp.status_code, resp.text[:500]))
            elif resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After", "")
                wait_msg = f" Retry after {retry_after}s." if retry_after else ""
                result["error"] = f"Rate limited by LinkedIn.{wait_msg}"
                result["blocked"] = True
                if retry_after:
                    try:
                        result["retry_after_seconds"] = int(retry_after)
                    except ValueError:
                        pass
            else:
                body = resp.text[:200]
                result["error"] = f"Unipile returned {resp.status_code}: {body}"
        except FileNotFoundError:
            result["error"] = f"Audio file not found: {audio_path}"
        except httpx.TimeoutException:
            result["error"] = "Request timed out after retries."
        except Exception as e:
            result["error"] = f"Send new voice message failed: {e}"
        if result.get("success"):
            logger.info("send_new_voice_message: success provider_id=%s", provider_id)
        elif result.get("error"):
            logger.warning("send_new_voice_message: %s provider_id=%s", result["error"], provider_id)
        return result

    async def get_chat_messages(
        self,
        account_id: str,
        chat_id: str,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Fetch messages from a specific LinkedIn chat/conversation.

        Args:
            account_id: The Unipile account ID.
            chat_id: The chat/conversation ID.
            limit: Max number of messages to return.

        Returns:
            List of message dicts with sender_id, text, timestamp.
        """
        url = f"{self.base_url}/api/v1/chats/{chat_id}/messages?account_id={account_id}&limit={limit}"
        try:
            resp = await self._client.get(url, headers=self._headers())
            if resp.status_code in (401, 403):
                raise UnipileAuthError()
            resp.raise_for_status()
            data = resp.json()

            items = data.get("items") or data.get("messages") or data.get("data") or []
            if isinstance(data, list):
                items = data

            messages: list[dict[str, Any]] = []
            for msg in items[:limit]:
                if not isinstance(msg, dict):
                    continue
                text = msg.get("text") or msg.get("body") or msg.get("content") or ""
                # Extract URLs from attachments (LinkedIn link previews may not be in text)
                for att in (msg.get("attachments") or []):
                    if isinstance(att, dict):
                        att_url = att.get("url") or att.get("link") or att.get("href") or ""
                        if att_url and att_url not in text:
                            text = f"{text} {att_url}".strip()
                sender_id = msg.get("sender_id") or msg.get("sender", {}).get("provider_id", "")
                sender_name = msg.get("sender_name") or msg.get("sender", {}).get("display_name", "")
                ts_raw = msg.get("timestamp") or msg.get("created_at") or msg.get("date") or ""
                timestamp = 0
                if isinstance(ts_raw, (int, float)):
                    timestamp = int(ts_raw)
                elif isinstance(ts_raw, str) and ts_raw:
                    try:
                        timestamp = int(datetime.fromisoformat(ts_raw.replace("Z", "+00:00")).timestamp())
                    except (ValueError, TypeError):
                        pass
                message_id = str(msg.get("id") or msg.get("message_id") or "")
                messages.append({
                    "message_id": message_id,
                    "sender_id": str(sender_id),
                    "sender_name": str(sender_name),
                    "text": text,
                    "timestamp": timestamp,
                })
            return messages
        except UnipileAuthError:
            raise
        except Exception as e:
            logger.warning(f"Failed to fetch chat messages: {e}")
            return []

    async def verify_message_sent(
        self,
        account_id: str,
        chat_id: str,
        expected_text: str,
    ) -> bool:
        """Read back conversation to verify our message was actually delivered.

        Checks the most recent messages in the chat for a match against
        the expected text (first 50 chars). Returns True if found.
        """
        try:
            messages = await self.get_chat_messages(account_id, chat_id, limit=3)
            snippet = expected_text[:50]
            for msg in messages:
                if snippet in (msg.get("text") or ""):
                    return True
            return False
        except Exception as e:
            logger.warning("DM verification failed for chat %s: %s", chat_id, e)
            return False

    # ── User Posts (for any user, not just self) ──

    async def get_followers(
        self,
        account_id: str,
        limit: int = 100,
        company_id: str = "",
    ) -> list[dict[str, Any]]:
        """Fetch followers of the authenticated LinkedIn account.

        GET /api/v1/users/followers

        Note: This returns followers of the connected account. For company
        page followers, the company page admin must have connected their account.

        Returns:
            List of follower dicts with provider_id, name, headline, profile_url.
        """
        url = f"{self.base_url}/api/v1/users/followers?account_id={account_id}&limit={limit}"
        try:
            resp = await self._retry_request("GET", url)
            if resp.status_code in (404, 400):
                logger.info("Followers endpoint returned %d", resp.status_code)
                return []
            resp.raise_for_status()
            data = resp.json()

            items = []
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict):
                items = data.get("items") or data.get("data") or data.get("followers") or []

            followers: list[dict[str, Any]] = []
            for item in items[:limit]:
                if not isinstance(item, dict):
                    continue
                provider_id = item.get("provider_id") or item.get("id") or ""
                name = item.get("name") or item.get("full_name") or ""
                if not provider_id and not name:
                    continue
                followers.append({
                    "provider_id": str(provider_id),
                    "name": str(name),
                    "headline": str(item.get("headline") or ""),
                    "profile_url": str(item.get("profile_url") or item.get("public_identifier") or ""),
                })
            return followers
        except UnipileError:
            # Re-raise rate limit / auth errors so circuit breaker can see them
            raise
        except Exception as e:
            logger.warning("Failed to fetch followers: %s", e)
            return []

    async def get_user_posts(
        self,
        account_id: str,
        identifier: str,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """Fetch recent posts for any LinkedIn user (by provider_id or public_id).

        Unlike get_posts() which is for the authenticated user's own posts,
        this fetches posts for any user identified by their provider_id.

        Args:
            account_id: The Unipile account ID.
            identifier: The user's provider_id or public_identifier.
            limit: Max number of posts to return.

        Returns:
            List of post dicts with id, text, date, metrics.
        """
        url = f"{self.base_url}/api/v1/users/{identifier}/posts?account_id={account_id}&limit={limit}"
        try:
            resp = await self._retry_request("GET", url)
            if resp.status_code in (404, 400):
                logger.info(f"User posts endpoint returned {resp.status_code}")
                return []
            if resp.status_code == 422:
                logger.info(f"User posts endpoint returned 422 for {identifier}")
                return [{"_status_code": 422}]
            resp.raise_for_status()
            data = resp.json()

            items = []
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict):
                items = data.get("items") or data.get("data") or data.get("posts") or []

            posts: list[dict[str, Any]] = []
            for item in items[:limit]:
                if not isinstance(item, dict):
                    continue
                text = item.get("text") or item.get("body") or item.get("content") or ""
                if not text:
                    continue
                post_id = item.get("id") or item.get("urn") or item.get("social_id") or ""
                post_date = item.get("date") or item.get("created_at") or item.get("parsed_datetime") or ""
                metrics = item.get("metrics") or item.get("social_counts") or {}
                if not isinstance(metrics, dict):
                    metrics = {}

                # Merge top-level counters into metrics if not already present
                for counter_key, metric_key in [
                    ("reaction_counter", "reactions_count"),
                    ("comment_counter", "comments_count"),
                    ("impressions_counter", "impressions_count"),
                    ("repost_counter", "reposts_count"),
                ]:
                    val = item.get(counter_key) or item.get(metric_key)
                    if val and metric_key not in metrics:
                        metrics[metric_key] = val

                post_data: dict[str, Any] = {
                    "id": str(post_id),
                    "text": str(text),
                    "date": str(post_date),
                    "metrics": metrics,
                    "share_url": item.get("share_url") or "",
                    "is_repost": bool(item.get("is_repost")),
                    "is_edited": bool(item.get("is_edited")),
                    "visibility": item.get("visibility") or "",
                }

                # Forward raw item fields for expanded extraction downstream
                for fwd_key in ("image", "images", "video", "video_url", "article",
                                "article_url", "document", "document_url", "poll",
                                "reshared", "repost", "shared_post", "original_post_id",
                                "attachments"):
                    if item.get(fwd_key) is not None:
                        post_data[fwd_key] = item[fwd_key]

                posts.append(post_data)
            return posts
        except Exception as e:
            logger.warning(f"Failed to fetch user posts: {e}")
            return []

    # ── Post Engagement ──

    async def send_post_comment(
        self,
        account_id: str,
        post_id: str,
        text: str,
        outreach_id: str = "",
        post_text: str = "",
    ) -> dict[str, Any]:
        """Send a comment on a LinkedIn post.

        Args:
            account_id: The Unipile account ID.
            post_id: The post ID/URN to comment on.
            text: The comment text.

        Returns:
            {"success": bool, "error": str}
        """
        result: dict[str, Any] = {"success": False, "error": ""}
        url = f"{self.base_url}/api/v1/posts/{post_id}/comments"
        payload = {
            "account_id": account_id,
            "text": text,
        }
        try:
            resp = await self._retry_request("POST", url, json=payload)
            if resp.status_code in (200, 201, 202):
                result["success"] = True
                try:
                    body = resp.json()
                    result["comment_id"] = body.get("comment_id") or body.get("id") or ""
                except Exception:
                    pass
            elif resp.status_code in (401, 403):
                result.update(_classify_http_auth_error(resp.status_code, resp.text[:500]))
            elif resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After", "")
                wait_msg = f" Retry after {retry_after}s." if retry_after else ""
                result["error"] = f"Rate limited by LinkedIn.{wait_msg}"
                result["blocked"] = True
                if retry_after:
                    try:
                        result["retry_after_seconds"] = int(retry_after)
                    except ValueError:
                        pass
            else:
                body = resp.text[:200]
                result["error"] = f"Unipile returned {resp.status_code}: {body}"
        except httpx.TimeoutException:
            result["error"] = "Request timed out after retries."
        except Exception as e:
            result["error"] = f"Comment failed: {e}"
        if result.get("success"):
            logger.info("send_post_comment: success post_id=%s comment_id=%s", post_id, result.get("comment_id", ""))
        elif result.get("error"):
            logger.warning("send_post_comment: %s post_id=%s", result["error"], post_id)
        return result

    async def send_post_reaction(
        self,
        account_id: str,
        post_id: str,
        reaction_type: str = "LIKE",
        outreach_id: str = "",
        post_text: str = "",
    ) -> dict[str, Any]:
        """React to a LinkedIn post (like, celebrate, etc.).

        Args:
            account_id: The Unipile account ID.
            post_id: The post ID/URN to react to.
            reaction_type: Type of reaction (LIKE, CELEBRATE, SUPPORT, etc.)
            outreach_id: Ignored in direct mode (used by backend proxy).
            post_text: Ignored in direct mode (used by backend proxy).

        Returns:
            {"success": bool, "error": str}
        """
        result: dict[str, Any] = {"success": False, "error": ""}
        url = f"{self.base_url}/api/v1/posts/reaction"
        payload = {
            "account_id": account_id,
            "post_id": post_id,
            "reaction_type": reaction_type.lower(),
        }
        try:
            resp = await self._retry_request("POST", url, json=payload)
            if resp.status_code in (200, 201, 202):
                result["success"] = True
                try:
                    body = resp.json()
                    result["reaction_id"] = body.get("reaction_id") or body.get("id") or ""
                except Exception:
                    pass
            elif resp.status_code in (401, 403):
                result.update(_classify_http_auth_error(resp.status_code, resp.text[:500]))
            elif resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After", "")
                wait_msg = f" Retry after {retry_after}s." if retry_after else ""
                result["error"] = f"Rate limited by LinkedIn.{wait_msg}"
                result["blocked"] = True
                if retry_after:
                    try:
                        result["retry_after_seconds"] = int(retry_after)
                    except ValueError:
                        pass
            else:
                body = resp.text[:200]
                result["error"] = f"Unipile returned {resp.status_code}: {body}"
        except httpx.TimeoutException:
            result["error"] = "Request timed out after retries."
        except Exception as e:
            result["error"] = f"Reaction failed: {e}"
        if result.get("success"):
            logger.info("send_post_reaction: success post_id=%s reaction_type=%s", post_id, reaction_type)
        elif result.get("error"):
            logger.warning("send_post_reaction: %s post_id=%s reaction_type=%s", result["error"], post_id, reaction_type)
        return result

    # ── Relations ──

    async def get_relations(
        self,
        account_id: str,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """Fetch the user's LinkedIn connections/relations with pagination.

        Args:
            account_id: The Unipile account ID.
            limit: Max number of relations to return.

        Returns:
            List of relation dicts with provider_id, name, headline.
        """
        all_relations: list[dict[str, Any]] = []
        cursor: str | None = None
        page_size = min(limit, 100)

        try:
            while len(all_relations) < limit:
                url = f"{self.base_url}/api/v1/users/relations?account_id={account_id}&limit={page_size}"
                if cursor:
                    url += f"&cursor={cursor}"

                resp = await self._client.get(url, headers=self._headers())
                if resp.status_code in (401, 403):
                    logger.warning("get_relations: status=%d body=%s", resp.status_code, resp.text[:500])
                    raise UnipileAuthError()
                if resp.status_code >= 400:
                    logger.warning("get_relations: status=%d body=%s", resp.status_code, resp.text[:500])
                    resp.raise_for_status()
                data = resp.json()

                items = data.get("items") or data.get("relations") or data.get("data") or []
                if isinstance(data, list):
                    items = data

                if not items:
                    break

                for item in items:
                    if not isinstance(item, dict):
                        continue
                    provider_id = item.get("provider_id") or item.get("id") or ""
                    name = item.get("display_name") or item.get("name") or ""
                    if not name and (item.get("first_name") or item.get("last_name")):
                        name = f"{item.get('first_name', '')} {item.get('last_name', '')}".strip()
                    headline = item.get("headline") or ""
                    public_id = item.get("public_identifier") or item.get("publicIdentifier") or ""

                    # Extract company/location/profile_url for local search
                    company = item.get("company") or item.get("company_name") or ""
                    if not company and headline and " at " in headline:
                        company = headline.rsplit(" at ", 1)[1].strip()
                    location = item.get("location") or ""
                    if isinstance(location, dict):
                        location = location.get("name") or location.get("default") or ""
                    profile_url = item.get("profile_url") or item.get("public_profile_url") or ""
                    if not profile_url and public_id:
                        profile_url = f"https://www.linkedin.com/in/{public_id}"

                    all_relations.append({
                        "provider_id": str(provider_id),
                        "name": name,
                        "headline": headline,
                        "public_id": public_id,
                        "company": company,
                        "location": str(location),
                        "profile_url": profile_url,
                    })

                cursor = data.get("cursor") if isinstance(data, dict) else None
                if not cursor:
                    break

            return all_relations[:limit]
        except UnipileAuthError:
            raise
        except Exception as e:
            logger.warning(f"Failed to fetch relations: {e}")
            return []

    # ── Company Profile ──

    async def get_company_profile(
        self,
        account_id: str,
        identifier: str,
    ) -> dict[str, Any]:
        """Fetch a LinkedIn company profile via Unipile.

        Args:
            account_id: The Unipile account ID.
            identifier: Company public_id, provider_id, or LinkedIn URL slug.

        Returns:
            Company dict with name, industry, size, employee_count, description, website.
        """
        url = f"{self.base_url}/api/v1/linkedin/company/{identifier}?account_id={account_id}"
        try:
            resp = await self._client.get(url, headers=self._headers())
            if resp.status_code in (404, 400):
                logger.info("get_company_profile: status=%d identifier=%s body=%s", resp.status_code, identifier[:20], resp.text[:300])
                return {}
            if resp.status_code in (401, 403):
                logger.warning("get_company_profile: status=%d identifier=%s body=%s", resp.status_code, identifier[:20], resp.text[:500])
                raise UnipileAuthError()
            if resp.status_code >= 400:
                logger.warning("get_company_profile: status=%d identifier=%s body=%s", resp.status_code, identifier[:20], resp.text[:500])
                resp.raise_for_status()
            data = resp.json()
            if not isinstance(data, dict):
                return {}
            return {
                "name": data.get("name") or data.get("company_name") or "",
                "industry": data.get("industry") or "",
                "size": data.get("company_size") or data.get("size") or "",
                "employee_count": data.get("employee_count") or data.get("employees_count") or 0,
                "description": data.get("description") or data.get("about") or "",
                "website": data.get("website") or data.get("url") or "",
                "headquarters": data.get("headquarters") or data.get("location") or "",
                "founded": data.get("founded") or data.get("founded_year") or "",
                "specialties": data.get("specialties") or [],
                "type": data.get("type") or data.get("company_type") or "",
                "provider_id": str(data.get("provider_id") or data.get("id") or ""),
            }
        except UnipileAuthError:
            raise
        except Exception as e:
            logger.warning(f"Company profile fetch error for {identifier}: {e}")
            return {}

    # ── InMail ──

    async def send_inmail(
        self,
        account_id: str,
        provider_id: str,
        subject: str,
        body: str,
    ) -> dict[str, Any]:
        """Send an InMail to a non-connection via Unipile.

        Uses the standard POST /api/v1/chats endpoint with inmail flag.
        Requires InMail credits (Premium/Sales Nav: ~800/month free).

        Args:
            account_id: The Unipile account ID.
            provider_id: LinkedIn provider_id of the recipient.
            subject: InMail subject line.
            body: InMail message body.

        Returns:
            {"success": bool, "error": str, "chat_id": str}
        """
        result: dict[str, Any] = {"success": False, "error": "", "chat_id": ""}
        url = f"{self.base_url}/api/v1/chats"
        payload = {
            "account_id": account_id,
            "attendees_ids": [provider_id],
            "subject": subject,
            "text": body,
            "inmail": True,
        }
        try:
            resp = await self._retry_request("POST", url, json=payload)
            if resp.status_code in (200, 201):
                data = resp.json()
                result["success"] = True
                result["chat_id"] = data.get("chat_id") or data.get("id") or ""
            elif resp.status_code in (401, 403):
                result.update(_classify_http_auth_error(resp.status_code, resp.text[:500]))
            elif resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After", "")
                wait_msg = f" Retry after {retry_after}s." if retry_after else ""
                result["error"] = f"Rate limited by LinkedIn.{wait_msg}"
                result["blocked"] = True
                if retry_after:
                    try:
                        result["retry_after_seconds"] = int(retry_after)
                    except ValueError:
                        pass
            elif resp.status_code == 402:
                result["error"] = "No InMail credits remaining."
            elif resp.status_code == 422:
                body_text = resp.text[:200]
                result["error"] = f"Cannot send InMail: {body_text}"
            else:
                body_text = resp.text[:200]
                result["error"] = f"Unipile returned {resp.status_code}: {body_text}"
        except httpx.TimeoutException:
            result["error"] = "Request timed out after retries."
        except Exception as e:
            result["error"] = f"InMail send failed: {e}"
        if result.get("success"):
            logger.info("send_inmail: success provider_id=%s", provider_id)
        elif result.get("error"):
            logger.warning("send_inmail: %s provider_id=%s", result["error"], provider_id)
        return result

    async def get_inmail_balance(
        self,
        account_id: str,
    ) -> dict[str, Any]:
        """Get remaining InMail credit balance.

        Args:
            account_id: The Unipile account ID.

        Returns:
            {"credits": int, "error": str}
        """
        result: dict[str, Any] = {"credits": -1, "error": ""}
        url = f"{self.base_url}/api/v1/linkedin/inmail-balance?account_id={account_id}"
        try:
            resp = await self._client.get(url, headers=self._headers())
            if resp.status_code in (200, 201):
                data = resp.json()
                result["credits"] = data.get("balance") or data.get("credits") or data.get("remaining") or 0
            elif resp.status_code in (401, 403):
                result.update(_classify_http_auth_error(resp.status_code, resp.text[:500]))
            elif resp.status_code == 404:
                result["error"] = "InMail balance endpoint not available (may require Premium)."
            else:
                result["error"] = f"Unipile returned {resp.status_code}"
        except Exception as e:
            result["error"] = f"InMail balance check failed: {e}"
        return result

    # ── Skill Endorsement ──

    async def endorse_skill(
        self,
        account_id: str,
        identifier: str,
    ) -> dict[str, Any]:
        """Endorse a LinkedIn profile's skills.

        Uses Unipile's dedicated skill endorsement endpoint.
        Triggers a high-visibility LinkedIn notification to the prospect.

        Args:
            account_id: The Unipile account ID.
            identifier: Profile public_id or provider_id.

        Returns:
            {"success": bool, "error": str}
        """
        result: dict[str, Any] = {"success": False, "error": ""}
        url = f"{self.base_url}/api/v1/linkedin/profile/{identifier}/skill/endorse"
        payload = {"account_id": account_id}
        try:
            resp = await self._retry_request("POST", url, json=payload)
            if resp.status_code in (200, 201, 204):
                result["success"] = True
            elif resp.status_code in (401, 403):
                result.update(_classify_http_auth_error(resp.status_code, resp.text[:500]))
            elif resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After", "")
                wait_msg = f" Retry after {retry_after}s." if retry_after else ""
                result["error"] = f"Rate limited by LinkedIn.{wait_msg}"
                result["blocked"] = True
                if retry_after:
                    try:
                        result["retry_after_seconds"] = int(retry_after)
                    except ValueError:
                        pass
            elif resp.status_code == 404:
                result["error"] = "Profile or skills not found."
            elif resp.status_code == 422:
                result["error"] = "Cannot endorse skills (may require connection)."
            else:
                body = resp.text[:200]
                result["error"] = f"Unipile returned {resp.status_code}: {body}"
        except httpx.TimeoutException:
            result["error"] = "Request timed out after retries."
        except Exception as e:
            result["error"] = f"Skill endorsement failed: {e}"
        if result.get("success"):
            logger.info("endorse_skill: success identifier=%s", identifier)
        elif result.get("error"):
            logger.warning("endorse_skill: %s identifier=%s", result["error"], identifier)
        return result

    # ── Inbound Invitations ──

    async def get_received_invitations(
        self,
        account_id: str,
    ) -> list[dict[str, Any]]:
        """Fetch received (inbound) LinkedIn connection invitations.

        Args:
            account_id: The Unipile account ID.

        Returns:
            List of invitation dicts with id, sender info, message, timestamp.
        """
        # Try newer endpoint first, fall back to legacy
        url = f"{self.base_url}/api/v1/users/invite/received?account_id={account_id}"
        try:
            resp = await self._client.get(url, headers=self._headers())
            if resp.status_code == 404:
                return []
            if resp.status_code in (401, 403):
                raise UnipileAuthError()
            if resp.status_code in (404, 400):
                return []
            resp.raise_for_status()
            data = resp.json()

            # Diagnostic logging — raw response shape
            if isinstance(data, dict):
                items_key = "items" if "items" in data else ("data" if "data" in data else None)
                raw_count = len(data.get(items_key, [])) if items_key else 0
                logger.info("get_received_invitations: keys=%s, items_key=%s, raw_count=%d",
                            list(data.keys()), items_key, raw_count)
                if raw_count > 0 and isinstance(data[items_key][0], dict):
                    logger.debug("get_received_invitations: first item keys=%s",
                                 list(data[items_key][0].keys()))
            elif isinstance(data, list):
                logger.info("get_received_invitations: list count=%d", len(data))

            items = data.get("items") or data.get("data") or []
            if isinstance(data, list):
                items = data

            invitations: list[dict[str, Any]] = []
            for inv in items:
                if not isinstance(inv, dict):
                    continue
                inv_id = inv.get("id") or inv.get("invitation_id") or ""
                if not inv_id:
                    continue

                # TEMP: Log raw invitation for newsletter field discovery
                logger.debug("Raw invitation object: %s", json.dumps(inv, default=str)[:2000])

                # Skip non-connection invitations (newsletters, events, etc.)
                if _is_newsletter_invitation(inv):
                    logger.debug("Filtered non-connection invitation: id=%s", inv_id)
                    continue

                # Sender info — expanded field coverage + nested objects
                sender_name = inv.get("sender_name") or inv.get("display_name") or inv.get("name") or ""
                if not sender_name:
                    fn = inv.get("first_name") or inv.get("firstName") or ""
                    ln = inv.get("last_name") or inv.get("lastName") or ""
                    sender_name = f"{fn} {ln}".strip()
                sender_id = (
                    inv.get("provider_id") or inv.get("sender_id")
                    or inv.get("from_member_id") or inv.get("inviter_id")
                    or inv.get("from_id") or inv.get("member_id") or ""
                )
                # Check nested sender/inviter objects
                for nested_key in ("sender", "inviter", "from", "user"):
                    nested = inv.get(nested_key)
                    if isinstance(nested, dict):
                        sender_id = sender_id or nested.get("id") or nested.get("provider_id") or ""
                        if not sender_name:
                            sender_name = nested.get("name") or nested.get("display_name") or ""
                            if not sender_name:
                                fn = nested.get("first_name") or nested.get("firstName") or ""
                                ln = nested.get("last_name") or nested.get("lastName") or ""
                                sender_name = f"{fn} {ln}".strip()

                headline = inv.get("headline") or ""
                message = inv.get("message") or inv.get("custom_message") or ""

                ts_raw = inv.get("timestamp") or inv.get("created_at") or inv.get("date") or ""
                timestamp = 0
                if isinstance(ts_raw, (int, float)):
                    timestamp = int(ts_raw)
                elif isinstance(ts_raw, str) and ts_raw:
                    try:
                        timestamp = int(datetime.fromisoformat(ts_raw.replace("Z", "+00:00")).timestamp())
                    except (ValueError, TypeError):
                        pass

                # Extract shared_secret for acceptance
                specifics = inv.get("specifics") or {}
                shared_secret = specifics.get("shared_secret") or ""

                invitations.append({
                    "id": str(inv_id),
                    "sender_name": sender_name,
                    "sender_id": str(sender_id),
                    "headline": headline,
                    "message": message,
                    "timestamp": timestamp,
                    "shared_secret": shared_secret,
                })

            logger.info("get_received_invitations: %d raw -> %d after filter", len(items), len(invitations))
            return invitations
        except UnipileAuthError:
            raise
        except Exception as e:
            logger.warning(f"Failed to fetch received invitations: {e}")
            return []

    async def handle_invitation(
        self,
        account_id: str,
        invitation_id: str,
        action: str = "accept",
        *,
        shared_secret: str = "",
    ) -> dict[str, Any]:
        """Accept or decline a received LinkedIn invitation.

        Args:
            account_id: The Unipile account ID.
            invitation_id: The invitation ID to accept/decline.
            action: "accept" or "decline".
            shared_secret: LinkedIn shared secret from the invitation specifics.

        Returns:
            {"success": bool, "error": str}
        """
        result: dict[str, Any] = {"success": False, "error": ""}

        # Build base payload
        base: dict[str, Any] = {"account_id": account_id, "action": action}
        if shared_secret:
            base["shared_secret"] = shared_secret

        # Try multiple endpoint variants
        attempts = [
            (f"{self.base_url}/api/v1/users/invite/received/{invitation_id}",
             {**base, "provider": "LINKEDIN"}),
            (f"{self.base_url}/api/v1/users/invite/received/{invitation_id}", base),
        ]

        try:
            resp = None
            for url, payload in attempts:
                resp = await self._retry_request("POST", url, json=payload)
                if resp.status_code in (200, 201, 204):
                    result["success"] = True
                    try:
                        body = resp.json()
                        result["response_id"] = body.get("id") or body.get("invitation_id") or ""
                    except Exception:
                        pass
                    logger.info("handle_invitation: success invitation_id=%s action=%s", invitation_id, action)
                    return result
                if resp.status_code not in (400, 404, 405):
                    break  # Don't retry on auth/rate-limit errors

            # Handle final error from last attempt
            if resp.status_code in (401, 403):
                result.update(_classify_http_auth_error(resp.status_code, resp.text[:500]))
            elif resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After", "")
                wait_msg = f" Retry after {retry_after}s." if retry_after else ""
                result["error"] = f"Rate limited by LinkedIn.{wait_msg}"
                result["blocked"] = True
                if retry_after:
                    try:
                        result["retry_after_seconds"] = int(retry_after)
                    except ValueError:
                        pass
            elif resp.status_code == 404:
                result["error"] = "Invitation not found or already handled."
            else:
                body = resp.text[:200]
                result["error"] = f"Unipile returned {resp.status_code}: {body}"
        except httpx.TimeoutException:
            result["error"] = "Request timed out after retries."
        except Exception as e:
            result["error"] = f"Handle invitation failed: {e}"
        if result.get("error"):
            logger.warning("handle_invitation: %s invitation_id=%s action=%s", result["error"], invitation_id, action)
        return result

    # ── Withdraw Invitation ──

    async def withdraw_invitation(
        self,
        account_id: str,
        invitation_id: str,
    ) -> dict[str, Any]:
        """Withdraw a sent LinkedIn invitation.

        Args:
            account_id: The Unipile account ID.
            invitation_id: The invitation ID to withdraw.

        Returns:
            {"success": bool, "error": str}
        """
        result: dict[str, Any] = {"success": False, "error": ""}
        url = f"{self.base_url}/api/v1/users/invite/sent/{invitation_id}"
        try:
            resp = await self._client.delete(
                url,
                headers=self._headers(),
                params={"account_id": account_id},
            )
            if resp.status_code in (200, 201, 204):
                result["success"] = True
            elif resp.status_code in (401, 403):
                result.update(_classify_http_auth_error(resp.status_code, resp.text[:500]))
            elif resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After", "")
                wait_msg = f" Retry after {retry_after}s." if retry_after else ""
                result["error"] = f"Rate limited by LinkedIn.{wait_msg}"
                result["blocked"] = True
                if retry_after:
                    try:
                        result["retry_after_seconds"] = int(retry_after)
                    except ValueError:
                        pass
            elif resp.status_code == 404:
                result["error"] = "Invitation not found."
            else:
                body = resp.text[:200]
                result["error"] = f"Unipile returned {resp.status_code}: {body}"
        except Exception as e:
            result["error"] = f"Withdraw failed: {e}"
        if result.get("success"):
            logger.info("withdraw_invitation: success invitation_id=%s", invitation_id)
        elif result.get("error"):
            logger.warning("withdraw_invitation: %s invitation_id=%s", result["error"], invitation_id)
        return result

    # ── Get Pending (Sent) Invitations ──

    async def get_pending_invitations(
        self,
        account_id: str,
    ) -> list[dict[str, Any]]:
        """Fetch all pending sent LinkedIn invitations with cursor pagination.

        Returns:
            List of invitation dicts (id, provider_id, name, timestamp, etc.).
        """
        all_invitations: list[dict[str, Any]] = []
        cursor: str | None = None
        max_pages = 20

        for _ in range(max_pages):
            url = f"{self.base_url}/api/v1/users/invite/sent?account_id={account_id}"
            if cursor:
                url += f"&cursor={cursor}"
            try:
                resp = await self._client.get(url, headers=self._headers())
                if resp.status_code != 200:
                    logger.debug("get_pending_invitations: status %d", resp.status_code)
                    break
                data = resp.json()
                items = data.get("items") or data.get("data") or []
                if isinstance(data, list):
                    items = data
                all_invitations.extend(
                    inv for inv in items if isinstance(inv, dict)
                )
                # Extract next cursor
                next_cursor = None
                if isinstance(data, dict):
                    next_cursor = (
                        data.get("cursor")
                        or data.get("next_cursor")
                        or data.get("paging", {}).get("cursor")
                    )
                if not next_cursor or not items:
                    break
                cursor = next_cursor
            except Exception as e:
                logger.debug("get_pending_invitations error: %s", e)
                break

        logger.info("get_pending_invitations: fetched %d invitations", len(all_invitations))
        return all_invitations

    async def delete_message(
        self,
        account_id: str,
        message_id: str,
    ) -> dict[str, Any]:
        """Delete a LinkedIn message via Unipile.

        LinkedIn only allows deletion within 60 minutes of sending.
        DELETE /api/v1/messages/{message_id}

        Returns:
            {"success": bool, "error": str}
        """
        result: dict[str, Any] = {"success": False, "error": ""}
        url = f"{self.base_url}/api/v1/messages/{message_id}"
        try:
            resp = await self._client.delete(
                url,
                headers=self._headers(),
                params={"account_id": account_id},
            )
            if resp.status_code in (200, 201, 204):
                result["success"] = True
            elif resp.status_code in (401, 403):
                result.update(_classify_http_auth_error(resp.status_code, resp.text[:500]))
            elif resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After", "")
                wait_msg = f" Retry after {retry_after}s." if retry_after else ""
                result["error"] = f"Rate limited by LinkedIn.{wait_msg}"
                result["blocked"] = True
                if retry_after:
                    try:
                        result["retry_after_seconds"] = int(retry_after)
                    except ValueError:
                        pass
            elif resp.status_code == 404:
                result["error"] = "Message not found on LinkedIn."
            else:
                body = resp.text[:200]
                result["error"] = f"Unipile returned {resp.status_code}: {body}"
        except Exception as e:
            result["error"] = f"Delete message failed: {e}"
        if result.get("success"):
            logger.info("delete_message: success message_id=%s", message_id)
        elif result.get("error"):
            logger.warning("delete_message: %s message_id=%s", result["error"], message_id)
        return result

    # ── Messages (comprehensive) ──

    async def list_all_messages(
        self,
        account_id: str,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """Fetch ALL messages across all conversations.

        More comprehensive than get_chats() which only returns the latest
        message per conversation. Returns individual messages allowing
        detection of messages in older conversations.

        GET /api/v1/messages

        Args:
            account_id: The Unipile account ID.
            limit: Max messages to return.

        Returns:
            List of message dicts with sender_id, sender_name, text,
            timestamp, chat_id, message_id.
        """
        url = f"{self.base_url}/api/v1/messages?account_id={account_id}&limit={limit}"
        try:
            resp = await self._client.get(url, headers=self._headers())
            if resp.status_code in (401, 403):
                raise UnipileAuthError()
            if resp.status_code in (404, 400):
                return []
            resp.raise_for_status()
            data = resp.json()

            items = data.get("items") or data.get("messages") or data.get("data") or []
            if isinstance(data, list):
                items = data

            messages: list[dict[str, Any]] = []
            for msg in items[:limit]:
                if not isinstance(msg, dict):
                    continue
                text = msg.get("text") or msg.get("body") or msg.get("content") or ""
                sender_id = msg.get("sender_id") or msg.get("sender", {}).get("provider_id", "")
                sender_name = msg.get("sender_name") or msg.get("sender", {}).get("display_name", "")
                chat_id = msg.get("chat_id") or msg.get("conversation_id") or ""
                message_id = msg.get("id") or msg.get("message_id") or ""
                ts_raw = msg.get("timestamp") or msg.get("created_at") or msg.get("date") or ""
                timestamp = 0
                if isinstance(ts_raw, (int, float)):
                    timestamp = int(ts_raw)
                elif isinstance(ts_raw, str) and ts_raw:
                    try:
                        timestamp = int(datetime.fromisoformat(ts_raw.replace("Z", "+00:00")).timestamp())
                    except (ValueError, TypeError):
                        pass
                messages.append({
                    "sender_id": str(sender_id),
                    "sender_name": str(sender_name),
                    "text": text,
                    "timestamp": timestamp,
                    "chat_id": str(chat_id),
                    "message_id": str(message_id),
                })
            return messages
        except UnipileAuthError:
            raise
        except Exception as e:
            logger.warning("Failed to list all messages: %s", e)
            return []

    async def get_messages_by_sender(
        self,
        account_id: str,
        sender_id: str,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Fetch messages from a specific person.

        GET /api/v1/chat_attendees/{sender_id}/messages

        Useful for viewing full conversation history with an inbound lead
        without needing to resolve their chat_id first.

        Args:
            account_id: The Unipile account ID.
            sender_id: The attendee's provider_id or public_id.
            limit: Max messages to return.

        Returns:
            List of message dicts with sender_id, sender_name, text,
            timestamp, chat_id, message_id.
        """
        url = (
            f"{self.base_url}/api/v1/chat_attendees/{sender_id}/messages"
            f"?account_id={account_id}&limit={limit}"
        )
        try:
            resp = await self._client.get(url, headers=self._headers())
            if resp.status_code in (401, 403):
                raise UnipileAuthError()
            if resp.status_code in (404, 400):
                return []
            resp.raise_for_status()
            data = resp.json()

            items = data.get("items") or data.get("messages") or data.get("data") or []
            if isinstance(data, list):
                items = data

            messages: list[dict[str, Any]] = []
            for msg in items[:limit]:
                if not isinstance(msg, dict):
                    continue
                text = msg.get("text") or msg.get("body") or msg.get("content") or ""
                msg_sender_id = msg.get("sender_id") or msg.get("sender", {}).get("provider_id", "")
                sender_name = msg.get("sender_name") or msg.get("sender", {}).get("display_name", "")
                chat_id = msg.get("chat_id") or msg.get("conversation_id") or ""
                message_id = msg.get("id") or msg.get("message_id") or ""
                ts_raw = msg.get("timestamp") or msg.get("created_at") or msg.get("date") or ""
                timestamp = 0
                if isinstance(ts_raw, (int, float)):
                    timestamp = int(ts_raw)
                elif isinstance(ts_raw, str) and ts_raw:
                    try:
                        timestamp = int(datetime.fromisoformat(ts_raw.replace("Z", "+00:00")).timestamp())
                    except (ValueError, TypeError):
                        pass
                messages.append({
                    "sender_id": str(msg_sender_id),
                    "sender_name": str(sender_name),
                    "text": text,
                    "timestamp": timestamp,
                    "chat_id": str(chat_id),
                    "message_id": str(message_id),
                })
            return messages
        except UnipileAuthError:
            raise
        except Exception as e:
            logger.warning("Failed to get messages by sender %s: %s", sender_id, e)
            return []

    async def add_message_reaction(
        self,
        account_id: str,
        message_id: str,
        reaction: str = "\U0001f44d",
    ) -> dict[str, Any]:
        """React to a LinkedIn DM message.

        POST /api/v1/messages/{message_id}/reaction

        Lightweight acknowledgment before sending a full reply.
        LinkedIn supports emoji reactions on messages.

        Args:
            account_id: The Unipile account ID.
            message_id: The message ID to react to.
            reaction: Emoji reaction (default: thumbs up).

        Returns:
            {"success": bool, "error": str}
        """
        result: dict[str, Any] = {"success": False, "error": ""}
        url = f"{self.base_url}/api/v1/messages/{message_id}/reaction"
        payload = {
            "account_id": account_id,
            "reaction": reaction,
        }
        try:
            resp = await self._retry_request("POST", url, json=payload)
            if resp.status_code in (200, 201, 204):
                result["success"] = True
            elif resp.status_code in (401, 403):
                result.update(_classify_http_auth_error(resp.status_code, resp.text[:500]))
            elif resp.status_code == 429:
                result["error"] = "Rate limited by LinkedIn."
                result["blocked"] = True
            elif resp.status_code == 404:
                result["error"] = "Message not found."
            else:
                body = resp.text[:200]
                result["error"] = f"Unipile returned {resp.status_code}: {body}"
        except Exception as e:
            result["error"] = f"Add reaction failed: {e}"
        if result.get("success"):
            logger.info("add_message_reaction: success message_id=%s", message_id)
        elif result.get("error"):
            logger.warning("add_message_reaction: %s message_id=%s", result["error"], message_id)
        return result

    # ── Follow ──

    async def follow_profile(
        self,
        account_id: str,
        provider_id: str,
    ) -> dict[str, Any]:
        """Follow a LinkedIn profile to warm up before connecting.

        Uses Unipile's raw route (POST /linkedin) to call LinkedIn's
        voyager API for following. Triggers a "X started following you"
        notification on the prospect's end.

        Args:
            account_id: The Unipile account ID.
            provider_id: The prospect's LinkedIn provider_id.

        Returns:
            {"success": bool, "error": str}
        """
        if not voyager_health.is_healthy("follow"):
            logger.info("follow_profile: skipped — Voyager 'follow' endpoint unhealthy")
            return {"success": False, "error": "Voyager follow endpoint unavailable", "voyager_down": True}
        result: dict[str, Any] = {"success": False, "error": ""}
        url = f"{self.base_url}/api/v1/linkedin"
        payload = {
            "account_id": account_id,
            "method": "POST",
            "request_url": (
                "https://www.linkedin.com/voyager/api/feed/dash/followingStates/"
                f"urn:li:fsd_followingState:urn:li:fsd_profile:{provider_id}"
            ),
            "body": {
                "patch": {
                    "$set": {
                        "following": True,
                    }
                }
            },
            "encoding": False,
        }
        try:
            resp = await self._retry_request("POST", url, json=payload)
            if resp.status_code in (200, 201):
                result["success"] = True
                voyager_health.record("follow", success=True)
            elif resp.status_code in (401, 403):
                result.update(_classify_http_auth_error(resp.status_code, resp.text[:500]))
            elif resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After", "")
                wait_msg = f" Retry after {retry_after}s." if retry_after else ""
                result["error"] = f"Rate limited by LinkedIn.{wait_msg}"
                result["blocked"] = True
                if retry_after:
                    try:
                        result["retry_after_seconds"] = int(retry_after)
                    except ValueError:
                        pass
            elif resp.status_code == 404:
                result["error"] = "Profile not found."
                result["permanent"] = True
            elif resp.status_code == 422:
                result["error"] = f"Cannot follow: {resp.text[:200]}"
                result["permanent"] = True
            elif resp.status_code == 400:
                body = resp.text[:200]
                result["error"] = f"Bad request (rejected by provider): {body}"
                voyager_health.record("follow", success=False)
            else:
                body = resp.text[:200]
                result["error"] = f"Unipile returned {resp.status_code}: {body}"
        except httpx.TimeoutException:
            result["error"] = "Request timed out after retries."
        except Exception as e:
            result["error"] = f"Follow failed: {e}"
            voyager_health.record("follow", success=False)
        if result.get("success"):
            logger.info("follow_profile: success provider_id=%s", provider_id)
        elif result.get("error"):
            logger.warning("follow_profile: %s provider_id=%s", result["error"], provider_id)
        return result

    async def check_follow_status(
        self,
        account_id: str,
        provider_id: str,
    ) -> dict[str, Any]:
        """Check if we follow a LinkedIn profile via Voyager raw route.

        Uses followingStates endpoint to verify a follow action actually landed.
        Returns: {"following": bool, "error": str}
        """
        result: dict[str, Any] = {"following": False, "error": ""}
        if not provider_id:
            result["error"] = "No provider_id"
            return result

        if not voyager_health.is_healthy("check_follow"):
            logger.info("check_follow_status: skipped — Voyager endpoint unhealthy")
            result["error"] = "Voyager check-follow endpoint unavailable"
            result["voyager_down"] = True
            return result

        url = f"{self.base_url}/api/v1/linkedin"
        payload = {
            "account_id": account_id,
            "method": "GET",
            "request_url": (
                "https://www.linkedin.com/voyager/api/feed/dash/followingStates/"
                f"urn:li:fsd_followingState:urn:li:fsd_profile:{provider_id}"
            ),
            "encoding": False,
        }
        try:
            resp = await self._client.post(url, json=payload, headers=self._headers())
            if resp.status_code in (401, 403):
                raise UnipileAuthError()
            if resp.status_code == 404:
                result["error"] = "followingStates endpoint returned 404"
                voyager_health.record("check_follow", success=False)
                return result
            if resp.status_code == 400:
                voyager_health.record("check_follow", success=False)
                result["error"] = "Voyager check-follow returned 400"
                return result
            resp.raise_for_status()
            data = resp.json()
            body = data.get("body") or data.get("data") or data
            if isinstance(body, str):
                import json as _json
                try:
                    body = _json.loads(body)
                except (ValueError, TypeError):
                    pass
            if isinstance(body, dict):
                result["following"] = bool(body.get("following", False))
            voyager_health.record("check_follow", success=True)
            return result
        except UnipileAuthError:
            raise
        except Exception as e:
            logger.warning("check_follow_status failed for %s: %s", provider_id[:12], e)
            result["error"] = str(e)
            voyager_health.record("check_follow", success=False)
            return result

    async def view_profile(
        self,
        account_id: str,
        provider_id: str,
    ) -> dict[str, Any]:
        """View a LinkedIn profile to trigger "X viewed your profile" notification.

        Uses Unipile's GET /users/{id} with notify=true to register
        an actual profile view on LinkedIn's side.

        Args:
            account_id: The Unipile account ID.
            provider_id: The prospect's LinkedIn provider_id or public_id.

        Returns:
            {"success": bool, "error": str}
        """
        result: dict[str, Any] = {"success": False, "error": ""}
        url = f"{self.base_url}/api/v1/users/{provider_id}"
        params = {
            "account_id": account_id,
            "linkedin_sections": "*",
            "notify": "true",
        }
        try:
            resp = await self._retry_request("GET", url, params=params)
            if resp.status_code in (200, 201):
                result["success"] = True
            elif resp.status_code in (401, 403):
                result.update(_classify_http_auth_error(resp.status_code, resp.text[:500]))
            elif resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After", "")
                wait_msg = f" Retry after {retry_after}s." if retry_after else ""
                result["error"] = f"Rate limited by LinkedIn.{wait_msg}"
                result["blocked"] = True
                if retry_after:
                    try:
                        result["retry_after_seconds"] = int(retry_after)
                    except ValueError:
                        pass
            elif resp.status_code == 404:
                result["error"] = "Profile not found."
            else:
                body = resp.text[:200]
                result["error"] = f"Unipile returned {resp.status_code}: {body}"
        except httpx.TimeoutException:
            result["error"] = "Request timed out after retries."
        except Exception as e:
            result["error"] = f"Profile view failed: {e}"
        if result.get("success"):
            logger.info("view_profile: success provider_id=%s", provider_id)
        elif result.get("error"):
            logger.warning("view_profile: %s provider_id=%s", result["error"], provider_id)
        return result

    # ── Profile Editing (via Unipile PATCH /api/v1/users/me/edit) ──

    async def _edit_profile(
        self,
        account_id: str,
        *,
        headline: str | None = None,
        summary: str | None = None,
        picture: bytes | None = None,
        picture_content_type: str = "image/jpeg",
        cover_picture: bytes | None = None,
        cover_picture_content_type: str = "image/jpeg",
        custom_link: dict[str, str] | None = None,
        location_id: str | None = None,
        skills: list[str] | None = None,
        experience: dict | None = None,
        education: dict | None = None,
        picture_settings: dict | None = None,
        cover_picture_settings: dict | None = None,
        open_to_work: dict | None = None,
        skills_follow: bool | None = None,
    ) -> dict[str, Any]:
        """Edit own LinkedIn profile via Unipile's dedicated endpoint.

        Uses ``PATCH /api/v1/users/me/edit`` with ``multipart/form-data``.
        Only provided (non-None) fields are included in the request.
        Nested params use bracket notation (``location[id]``, ``custom_link[url]``).
        Returns ``{"success": bool, "error": str}``.
        """
        result: dict[str, Any] = {"success": False, "error": ""}
        url = f"{self.base_url}/api/v1/users/me/edit"

        # List of tuples supports repeated keys (needed for skills)
        form_tuples: list[tuple[str, str]] = [
            ("type", "LINKEDIN"),
            ("account_id", account_id),
        ]
        if headline is not None:
            form_tuples.append(("headline", headline))
        if summary is not None:
            form_tuples.append(("summary", summary))
        if custom_link is not None:
            for key, val in custom_link.items():
                form_tuples.append((f"custom_link[{key}]", str(val)))
        if location_id is not None:
            form_tuples.append(("location[id]", location_id))
        if skills is not None:
            for skill in skills:
                form_tuples.append(("experience[skills]", skill))
        if experience is not None:
            for key, val in experience.items():
                if key != "skills":  # skills handled separately
                    form_tuples.append((f"experience[{key}]", str(val)))
        if education is not None:
            for key, val in education.items():
                form_tuples.append((f"education[{key}]", str(val)))
        if picture_settings is not None:
            for key, val in picture_settings.items():
                form_tuples.append((f"picture_settings[{key}]", str(val)))
        if cover_picture_settings is not None:
            for key, val in cover_picture_settings.items():
                form_tuples.append((f"cover_picture_settings[{key}]", str(val)))
        if open_to_work is not None:
            for key, val in open_to_work.items():
                form_tuples.append((f"open_to_work[{key}]", str(val)))
        if skills_follow is not None:
            form_tuples.append(("skills_follow", str(skills_follow).lower()))

        files: dict[str, tuple[str, bytes, str]] | None = None
        if picture is not None:
            ext = "png" if "png" in picture_content_type else "jpg"
            files = {"picture": (f"profile.{ext}", picture, picture_content_type)}
        if cover_picture is not None:
            ext = "png" if "png" in cover_picture_content_type else "jpg"
            files = files or {}
            files["cover_picture"] = (f"cover.{ext}", cover_picture, cover_picture_content_type)

        try:
            resp = await self._retry_request(
                "PATCH", url, data=form_tuples, files=files,
            )
            if resp.status_code in (200, 201):
                result["success"] = True
            else:
                body = resp.text[:200]
                result["error"] = f"Unipile returned {resp.status_code}: {body}"
        except httpx.TimeoutException:
            result["error"] = "Request timed out after retries."
        except Exception as e:
            result["error"] = f"Profile edit failed: {e}"
        if result.get("success"):
            logger.info("_edit_profile: success")
        elif result.get("error"):
            logger.warning("_edit_profile: %s", result["error"])
        return result

    async def update_profile_headline(
        self,
        account_id: str,
        provider_id: str,  # noqa: ARG002 — deprecated, kept for backward compat
        new_headline: str,
    ) -> dict[str, Any]:
        """Update LinkedIn profile headline.

        Uses Unipile's ``PATCH /api/v1/users/me/edit`` endpoint.
        The ``provider_id`` parameter is deprecated and ignored — the endpoint
        edits the authenticated user's own profile using ``account_id`` only.
        """
        return await self._edit_profile(account_id, headline=new_headline)

    async def update_profile_summary(
        self,
        account_id: str,
        provider_id: str,  # noqa: ARG002 — deprecated, kept for backward compat
        new_summary: str,
    ) -> dict[str, Any]:
        """Update LinkedIn profile summary (About section).

        Uses Unipile's ``PATCH /api/v1/users/me/edit`` endpoint.
        The ``provider_id`` parameter is deprecated and ignored.
        """
        return await self._edit_profile(account_id, summary=new_summary)

    async def upload_profile_photo(
        self,
        account_id: str,
        provider_id: str,  # noqa: ARG002 — deprecated, kept for backward compat
        image_bytes: bytes,
        content_type: str = "image/jpeg",
    ) -> dict[str, Any]:
        """Upload a profile photo via Unipile's dedicated edit endpoint.

        Replaces the old two-step Voyager upload with a single multipart request.
        The ``provider_id`` parameter is deprecated and ignored.
        """
        return await self._edit_profile(
            account_id, picture=image_bytes, picture_content_type=content_type,
        )

    async def upload_cover_photo(
        self,
        account_id: str,
        provider_id: str,  # noqa: ARG002 — deprecated, kept for backward compat
        image_bytes: bytes,
        content_type: str = "image/jpeg",
    ) -> dict[str, Any]:
        """Upload a cover/banner photo via Unipile's edit endpoint."""
        return await self._edit_profile(
            account_id, cover_picture=image_bytes, cover_picture_content_type=content_type,
        )

    async def update_custom_link(
        self,
        account_id: str,
        provider_id: str,  # noqa: ARG002
        category: str,
        url: str,
    ) -> dict[str, Any]:
        """Set a custom profile link (website, portfolio, blog, newsletter)."""
        return await self._edit_profile(
            account_id, custom_link={"category": category, "url": url},
        )

    async def update_location(
        self,
        account_id: str,
        provider_id: str,  # noqa: ARG002
        location_id: str,
    ) -> dict[str, Any]:
        """Update profile location by LinkedIn location ID."""
        return await self._edit_profile(account_id, location_id=location_id)

    async def update_skills(
        self,
        account_id: str,
        provider_id: str,  # noqa: ARG002
        skills: list[str],
    ) -> dict[str, Any]:
        """Add skills to the LinkedIn profile."""
        return await self._edit_profile(account_id, skills=skills)

    async def update_skills_follow(
        self,
        account_id: str,
        provider_id: str,  # noqa: ARG002
        skills_follow: bool,
    ) -> dict[str, Any]:
        """Enable or disable following skill-related content."""
        return await self._edit_profile(account_id, skills_follow=skills_follow)

    async def update_experience(
        self,
        account_id: str,
        provider_id: str,  # noqa: ARG002
        experience: dict,
    ) -> dict[str, Any]:
        """Add or edit a professional experience entry."""
        return await self._edit_profile(account_id, experience=experience)

    async def update_education(
        self,
        account_id: str,
        provider_id: str,  # noqa: ARG002
        education: dict,
    ) -> dict[str, Any]:
        """Add or edit an education entry."""
        return await self._edit_profile(account_id, education=education)

    async def update_picture_settings(
        self,
        account_id: str,
        provider_id: str,  # noqa: ARG002
        settings: dict,
    ) -> dict[str, Any]:
        """Update profile picture settings (filter, contrast, brightness)."""
        return await self._edit_profile(account_id, picture_settings=settings)

    async def update_cover_picture_settings(
        self,
        account_id: str,
        provider_id: str,  # noqa: ARG002
        settings: dict,
    ) -> dict[str, Any]:
        """Update cover picture settings (filter, contrast, brightness)."""
        return await self._edit_profile(account_id, cover_picture_settings=settings)

    async def update_open_to_work(
        self,
        account_id: str,
        provider_id: str,  # noqa: ARG002
        settings: dict,
    ) -> dict[str, Any]:
        """Update Open to Work settings (job titles, locations, visibility)."""
        return await self._edit_profile(account_id, open_to_work=settings)

    # ── Profile Viewers ──

    async def get_profile_viewers(
        self,
        account_id: str,
    ) -> list[dict[str, Any]]:
        """Get list of people who viewed your LinkedIn profile.

        Uses Unipile's raw route to call LinkedIn's Voyager GraphQL API.
        Requires LinkedIn Premium / Sales Navigator for full viewer data.

        Args:
            account_id: The Unipile account ID.

        Returns:
            List of viewer dicts with name, title, company, relation, url.
        """
        if not voyager_health.is_healthy("profile_viewers"):
            logger.info("get_profile_viewers: skipped — Voyager endpoint unhealthy")
            return []
        url = f"{self.base_url}/api/v1/linkedin"
        payload = {
            "account_id": account_id,
            "method": "GET",
            "request_url": (
                "https://www.linkedin.com/voyager/api/graphql"
                "?variables=(start:0,query:(),"
                "analyticsEntityUrn:(activityUrn:urn%3Ali%3Adummy%3A-1),"
                "surfaceType:WVMP)"
                "&queryId=voyagerPremiumDashAnalyticsObject"
                ".c31102e906e7098910f44e0cecaa5b5c"
            ),
            "encoding": False,
        }
        try:
            resp = await self._client.post(url, json=payload, headers=self._headers())
            if resp.status_code != 200:
                logger.info(f"Profile viewers returned {resp.status_code}")
                voyager_health.record("profile_viewers", success=False)
                return []
            data = resp.json()
            elements = (
                data.get("data", {})
                .get("data", {})
                .get("premiumDashAnalyticsObjectByAnalyticsEntity", {})
                .get("elements", [])
            )
            viewers: list[dict[str, Any]] = []
            for elem in elements:
                if not isinstance(elem, dict):
                    continue
                name = elem.get("title", {})
                name = name.get("text", name) if isinstance(name, dict) else name
                subtitle = elem.get("subtitle", {})
                subtitle = subtitle.get("text", subtitle) if isinstance(subtitle, dict) else subtitle
                caption = elem.get("caption", {})
                caption = caption.get("text", caption) if isinstance(caption, dict) else caption
                label = elem.get("label", {})
                label = label.get("text", label) if isinstance(label, dict) else label
                viewers.append({
                    "name": name or elem.get("name", ""),
                    "title": subtitle or "",
                    "company": caption or "",
                    "relation": label or elem.get("relation", ""),
                    "url": elem.get("navigationUrl", ""),
                })
            voyager_health.record("profile_viewers", success=bool(viewers))
            return viewers
        except Exception as e:
            logger.warning(f"Failed to fetch profile viewers: {e}")
            voyager_health.record("profile_viewers", success=False)
            return []

    # ── SSI Score ──

    async def get_ssi_score(self, account_id: str) -> dict[str, Any]:
        """Get Social Selling Index (SSI) score via LinkedIn Voyager API.

        SSI measures LinkedIn account health across 4 pillars:
        - Establish professional brand
        - Find the right people
        - Engage with insights
        - Build relationships

        Requires LinkedIn Premium / Sales Navigator for full data.

        Args:
            account_id: The Unipile account ID.

        Returns:
            {"score": 75, "pillars": [...], "industry_rank": ..., "network_rank": ...}
            or empty dict on failure.
        """
        if not voyager_health.is_healthy("ssi"):
            logger.info("get_ssi_score: skipped — Voyager SSI endpoint unhealthy")
            return {}
        url = f"{self.base_url}/api/v1/linkedin"
        payload = {
            "account_id": account_id,
            "method": "GET",
            "request_url": "https://www.linkedin.com/voyager/api/voyagerSalesInsightsMyDashSsiIndicator",
            "encoding": False,
        }
        try:
            resp = await self._client.post(url, json=payload, headers=self._headers())
            if resp.status_code != 200:
                logger.info(f"SSI score returned {resp.status_code}")
                voyager_health.record("ssi", success=False)
                return {}
            data = resp.json()
            raw = data.get("data", data)

            score = raw.get("score") or raw.get("overallScore") or 0
            pillars = []
            elements = raw.get("elements") or raw.get("pillars") or raw.get("categories") or []
            for elem in elements:
                if isinstance(elem, dict):
                    pillars.append({
                        "name": elem.get("name") or elem.get("title") or "",
                        "score": elem.get("score") or elem.get("value") or 0,
                    })

            voyager_health.record("ssi", success=True)
            return {
                "score": score,
                "pillars": pillars,
                "industry_rank": raw.get("industryRank") or raw.get("industry_rank"),
                "network_rank": raw.get("networkRank") or raw.get("network_rank"),
            }
        except Exception as e:
            logger.warning(f"Failed to fetch SSI score: {e}")
            voyager_health.record("ssi", success=False)
            return {}

    # ── Webhooks ──

    async def register_webhook(
        self,
        account_id: str,
        request_url: str,
        events: list[str] | None = None,
    ) -> dict[str, Any]:
        """Register a Unipile webhook for real-time LinkedIn events.

        Args:
            account_id: The Unipile account ID.
            request_url: URL that will receive webhook POST callbacks.
            events: List of event types to subscribe to. If empty, subscribes to all.

        Returns:
            {"success": True, "webhook_id": "..."} or {"success": False, "error": "..."}
        """
        url = f"{self.base_url}/api/v1/webhooks"
        payload: dict[str, Any] = {
            "account_id": account_id,
            "request_url": request_url,
        }
        if events:
            payload["events"] = events

        try:
            resp = await self._client.post(url, json=payload, headers=self._headers())
            body = resp.json()
            if resp.status_code in (200, 201):
                webhook_id = body.get("webhook_id") or body.get("id") or ""
                logger.info("register_webhook: success webhook_id=%s", webhook_id)
                return {"success": True, "webhook_id": webhook_id}
            logger.warning("register_webhook: status=%d body=%s", resp.status_code, resp.text[:200])
            return {"success": False, "error": body.get("error", resp.text)}
        except Exception as e:
            logger.warning("register_webhook: %s", e)
            return {"success": False, "error": str(e)}

    async def list_webhooks(self, account_id: str) -> list[dict[str, Any]]:
        """List all registered webhooks for an account.

        Args:
            account_id: The Unipile account ID.

        Returns:
            List of webhook dicts with id, request_url, events, etc.
        """
        url = f"{self.base_url}/api/v1/webhooks?account_id={account_id}"
        try:
            resp = await self._client.get(url, headers=self._headers())
            if resp.status_code != 200:
                logger.warning("list_webhooks: status=%d", resp.status_code)
                return []
            data = resp.json()
            if isinstance(data, list):
                return data
            return data.get("items") or data.get("webhooks") or data.get("data") or []
        except Exception as e:
            logger.warning("list_webhooks: %s", e)
            return []

    async def delete_webhook(self, webhook_id: str) -> dict[str, Any]:
        """Delete a registered webhook.

        Args:
            webhook_id: The webhook ID to delete.

        Returns:
            {"success": True} or {"success": False, "error": "..."}
        """
        url = f"{self.base_url}/api/v1/webhooks/{webhook_id}"
        try:
            resp = await self._client.delete(url, headers=self._headers())
            if resp.status_code in (200, 204):
                logger.info("delete_webhook: success webhook_id=%s", webhook_id)
                return {"success": True}
            try:
                body = resp.json()
                logger.warning("delete_webhook: status=%d webhook_id=%s", resp.status_code, webhook_id)
                return {"success": False, "error": body.get("error", resp.text)}
            except Exception:
                logger.warning("delete_webhook: status=%d webhook_id=%s", resp.status_code, webhook_id)
                return {"success": False, "error": resp.text}
        except Exception as e:
            logger.warning("delete_webhook: %s webhook_id=%s", e, webhook_id)
            return {"success": False, "error": str(e)}

    # ── Email ──

    async def send_email(
        self,
        account_id: str,
        to_email: str,
        to_name: str,
        subject: str,
        body: str,
        reply_to_provider_id: str = "",
        tracking_label: str = "",
    ) -> dict[str, Any]:
        """Send an email via a connected email account.

        Args:
            account_id: The Unipile email account ID.
            to_email: Recipient email address.
            to_name: Recipient display name.
            subject: Email subject line.
            body: Email body (HTML supported).
            reply_to_provider_id: Provider ID of email being replied to.
            tracking_label: Optional label for open/click tracking.

        Returns:
            {"success": bool, "email_id": str, "error": str}
        """
        result: dict[str, Any] = {"success": False, "email_id": "", "error": ""}
        url = f"{self.base_url}/api/v1/emails"
        payload: dict[str, Any] = {
            "account_id": account_id,
            "to": [{"display_name": to_name, "identifier": to_email}],
            "subject": subject,
            "body": body,
        }
        if reply_to_provider_id:
            payload["reply_to"] = reply_to_provider_id
        if tracking_label:
            payload["tracking_options"] = {
                "opens": True,
                "links": True,
                "label": tracking_label,
            }

        try:
            resp = await self._retry_request("POST", url, json=payload)
            if resp.status_code in (200, 201):
                data = resp.json()
                result["success"] = True
                result["email_id"] = data.get("id") or data.get("email_id") or ""
            elif resp.status_code in (401, 403):
                result["error"] = "Email account disconnected."
            elif resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After", "")
                wait_msg = f" Retry after {retry_after}s." if retry_after else ""
                result["error"] = f"Rate limited.{wait_msg}"
                result["blocked"] = True
                if retry_after:
                    try:
                        result["retry_after_seconds"] = int(retry_after)
                    except ValueError:
                        pass
            elif resp.status_code == 422:
                result["error"] = f"Cannot send email: {resp.text[:200]}"
            else:
                result["error"] = f"Unipile returned {resp.status_code}: {resp.text[:200]}"
        except httpx.TimeoutException:
            result["error"] = "Request timed out after retries."
        except Exception as e:
            result["error"] = f"Email send failed: {e}"
        if result.get("success"):
            logger.info("send_email: success recipient=%s", to_email)
        elif result.get("error"):
            logger.warning("send_email: %s recipient=%s", result["error"], to_email)
        return result

    async def list_emails(
        self,
        account_id: str,
        limit: int = 20,
        folder: str = "",
    ) -> list[dict[str, Any]]:
        """List emails from a connected email account.

        Args:
            account_id: The Unipile email account ID.
            limit: Max emails to return (1-250).
            folder: Optional folder filter (e.g. "INBOX", "SENT").

        Returns:
            List of email dicts.
        """
        url = f"{self.base_url}/api/v1/emails?account_id={account_id}&limit={min(limit, 250)}"
        if folder:
            url += f"&folder={folder}"
        try:
            resp = await self._client.get(url, headers=self._headers())
            if resp.status_code in (401, 403):
                raise UnipileAuthError()
            if resp.status_code not in (200, 201):
                return []
            data = resp.json()
            items = data.get("items") or data.get("data") or []
            if isinstance(data, list):
                items = data

            emails: list[dict[str, Any]] = []
            for item in items:
                if not isinstance(item, dict):
                    continue
                emails.append({
                    "id": item.get("id") or "",
                    "subject": item.get("subject") or "",
                    "from_name": (item.get("from_attendee") or {}).get("display_name", ""),
                    "from_email": (item.get("from_attendee") or {}).get("identifier", ""),
                    "date": item.get("date") or "",
                    "read": bool(item.get("read_date")),
                    "has_attachments": item.get("has_attachments", False),
                    "body_plain": item.get("body_plain") or "",
                    "folders": item.get("folders") or [],
                })
            return emails
        except UnipileAuthError:
            raise
        except Exception as e:
            logger.warning(f"Failed to list emails: {e}")
            return []

    async def get_email(
        self,
        account_id: str,
        email_id: str,
    ) -> dict[str, Any]:
        """Get a single email by ID.

        Args:
            account_id: The Unipile email account ID.
            email_id: The email ID.

        Returns:
            Email dict with full body, attachments, etc.
        """
        url = f"{self.base_url}/api/v1/emails/{email_id}?account_id={account_id}"
        try:
            resp = await self._client.get(url, headers=self._headers())
            if resp.status_code in (401, 403):
                raise UnipileAuthError()
            if resp.status_code not in (200, 201):
                return {}
            return resp.json()
        except UnipileAuthError:
            raise
        except Exception as e:
            logger.warning(f"Failed to get email: {e}")
            return {}

    async def mark_email(
        self,
        account_id: str,
        email_id: str,
        action: str = "setRead",
    ) -> dict[str, Any]:
        """Mark an email as read, unread, archived, etc.

        Args:
            account_id: The Unipile email account ID.
            email_id: The email ID.
            action: "setRead", "setUnread", "archive"

        Returns:
            {"success": bool, "error": str}
        """
        result: dict[str, Any] = {"success": False, "error": ""}
        url = f"{self.base_url}/api/v1/emails/{email_id}"
        payload = {"account_id": account_id, "action": action}
        try:
            resp = await self._retry_request("PATCH", url, json=payload)
            if resp.status_code in (200, 204):
                result["success"] = True
            else:
                result["error"] = f"Unipile returned {resp.status_code}: {resp.text[:200]}"
        except Exception as e:
            result["error"] = f"Mark email failed: {e}"
        if result.get("success"):
            logger.info("mark_email: success email_id=%s action=%s", email_id, action)
        elif result.get("error"):
            logger.warning("mark_email: %s email_id=%s action=%s", result["error"], email_id, action)
        return result

    # ── Chats ──

    async def get_chats(
        self,
        account_id: str,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Fetch recent LinkedIn messages/chats via Unipile.

        The Unipile GET /api/v1/chats endpoint returns chat metadata without
        embedded messages. For chats missing message content, we fetch the
        last message via GET /api/v1/chats/{id}/messages in parallel.

        Returns normalized message list matching HeyLead's format:
        [{"sender_name", "sender_id", "text", "timestamp", "conversation_urn"}]
        """
        url = f"{self.base_url}/api/v1/chats?account_id={account_id}&limit={limit}"

        try:
            resp = await self._client.get(url, headers=self._headers())
            if resp.status_code in (401, 403):
                raise UnipileAuthError()
            resp.raise_for_status()
            data = resp.json()

            items = data.get("items") or data.get("chats") or data.get("data") or []
            if isinstance(data, list):
                items = data

            messages: list[dict[str, Any]] = []

            for chat in items:
                if not isinstance(chat, dict):
                    continue

                chat_id = chat.get("id") or chat.get("chat_id") or ""
                if not chat_id:
                    continue

                # Get the last message (if embedded)
                chat_messages = chat.get("messages") or chat.get("last_messages") or []
                if isinstance(chat_messages, list) and chat_messages:
                    last_msg = chat_messages[-1] if isinstance(chat_messages[-1], dict) else {}
                elif isinstance(chat_messages, dict):
                    last_msg = chat_messages
                else:
                    last_msg = {}

                text = last_msg.get("text") or last_msg.get("body") or last_msg.get("content") or ""
                # Extract URLs from attachments (LinkedIn link previews may not be in text)
                for att in (last_msg.get("attachments") or []):
                    if isinstance(att, dict):
                        att_url = att.get("url") or att.get("link") or att.get("href") or ""
                        if att_url and att_url not in text:
                            text = f"{text} {att_url}".strip()
                if not text:
                    # No embedded message — return lightweight entry with
                    # attendee info so check_replies can match contacts first,
                    # then selectively fetch only relevant chats.
                    att_pid = chat.get("attendee_provider_id") or ""
                    _attendee_ids: list[str] = []
                    for att in (chat.get("attendees") or []):
                        if isinstance(att, dict):
                            att_id = att.get("provider_id") or att.get("id") or ""
                            if att_id:
                                _attendee_ids.append(str(att_id))
                    if att_pid and str(att_pid) not in _attendee_ids:
                        _attendee_ids.append(str(att_pid))

                    ts_raw = chat.get("timestamp") or chat.get("last_activity") or ""
                    _ts = 0
                    if isinstance(ts_raw, (int, float)):
                        _ts = int(ts_raw)
                    elif isinstance(ts_raw, str) and ts_raw:
                        try:
                            from datetime import datetime as dt
                            _ts = int(dt.fromisoformat(ts_raw.replace("Z", "+00:00")).timestamp())
                        except (ValueError, TypeError):
                            pass

                    messages.append({
                        "sender_name": "",
                        "sender_id": "",
                        "text": "",
                        "timestamp": _ts,
                        "conversation_urn": str(chat_id),
                        "attendee_ids": _attendee_ids,
                        "_needs_fetch": True,
                    })
                    continue

                # Identify the sender
                sender_id = last_msg.get("sender_id") or last_msg.get("sender", {}).get("provider_id", "")
                sender_name = last_msg.get("sender_name") or last_msg.get("sender", {}).get("display_name", "")

                # If no sender info in message, try attendees
                attendees = chat.get("attendees") or []
                if not sender_name:
                    for att in attendees:
                        if isinstance(att, dict):
                            att_id = att.get("provider_id") or att.get("id") or ""
                            if att_id and att_id == sender_id:
                                sender_name = att.get("display_name") or att.get("name") or ""
                                break
                            elif not sender_name:
                                sender_name = att.get("display_name") or att.get("name") or ""

                # Extract attendee provider_ids for reply matching
                attendee_ids = []
                for att in attendees:
                    if isinstance(att, dict):
                        att_id = att.get("provider_id") or att.get("id") or ""
                        if att_id:
                            attendee_ids.append(str(att_id))
                # Fallback: Unipile returns attendee_provider_id as a flat field
                att_pid = chat.get("attendee_provider_id") or ""
                if att_pid and str(att_pid) not in attendee_ids:
                    attendee_ids.append(str(att_pid))

                # Parse timestamp
                ts_raw = last_msg.get("timestamp") or last_msg.get("created_at") or last_msg.get("date") or ""
                timestamp = 0
                if isinstance(ts_raw, (int, float)):
                    timestamp = int(ts_raw)
                elif isinstance(ts_raw, str) and ts_raw:
                    try:
                        from datetime import datetime as dt
                        timestamp = int(dt.fromisoformat(ts_raw.replace("Z", "+00:00")).timestamp())
                    except (ValueError, TypeError):
                        pass

                messages.append({
                    "sender_name": sender_name,
                    "sender_id": str(sender_id),
                    "text": text,
                    "timestamp": timestamp,
                    "conversation_urn": str(chat_id),
                    "attendee_ids": attendee_ids,
                })

            # NOTE: Chats without embedded messages are returned as
            # lightweight entries with _needs_fetch=True and attendee_ids.
            # The caller (check_replies) matches these to contacts first,
            # then selectively fetches only relevant chats.

            return messages
        except UnipileAuthError:
            raise
        except Exception as e:
            logger.warning(f"Failed to fetch chats: {e}")
            return []


    async def mark_chat_read(self, chat_id: str) -> dict[str, Any]:
        """Mark a chat as read.

        PATCH /api/v1/chats/{id} with {"action": "setRead"}
        """
        url = f"{self.base_url}/api/v1/chats/{chat_id}"
        try:
            resp = await self._client.patch(url, headers=self._headers(), json={"action": "setRead"})
            resp.raise_for_status()
            logger.info("mark_chat_read: success chat_id=%s", chat_id)
            return resp.json() if resp.text else {"ok": True}
        except Exception as e:
            logger.warning("mark_chat_read: %s chat_id=%s", e, chat_id)
            return {"ok": False, "error": str(e)}

    async def archive_chat(self, chat_id: str) -> dict[str, Any]:
        """Archive a chat conversation.

        PATCH /api/v1/chats/{id} with {"action": "archive"}
        """
        url = f"{self.base_url}/api/v1/chats/{chat_id}"
        try:
            resp = await self._client.patch(url, headers=self._headers(), json={"action": "archive"})
            resp.raise_for_status()
            logger.info("archive_chat: success chat_id=%s", chat_id)
            return resp.json() if resp.text else {"ok": True}
        except Exception as e:
            logger.warning("archive_chat: %s chat_id=%s", e, chat_id)
            return {"ok": False, "error": str(e)}

    async def reconnect_account(self, account_id: str) -> dict[str, Any]:
        """Reconnect a disconnected Unipile account.

        POST /api/v1/accounts/{id}/reconnect
        Returns the account status after reconnect attempt.
        """
        url = f"{self.base_url}/api/v1/accounts/{account_id}/reconnect"
        try:
            resp = await self._client.post(url, headers=self._headers())
            resp.raise_for_status()
            logger.info("reconnect_account: success account_id=%s", account_id)
            return resp.json()
        except Exception as e:
            logger.warning("reconnect_account: %s account_id=%s", e, account_id)
            raise UnipileError(f"Reconnect failed: {e}") from e

    async def handle_checkpoint(self, account_id: str, code: str = "") -> dict[str, Any]:
        """Handle 2FA/checkpoint challenge for an account.

        POST /api/v1/accounts/{id}/checkpoint
        Args:
            account_id: The Unipile account ID.
            code: The 2FA code if available.
        """
        url = f"{self.base_url}/api/v1/accounts/{account_id}/checkpoint"
        body: dict[str, Any] = {}
        if code:
            body["code"] = code
        try:
            resp = await self._client.post(url, headers=self._headers(), json=body)
            resp.raise_for_status()
            logger.info("handle_checkpoint: success account_id=%s", account_id)
            return resp.json()
        except Exception as e:
            logger.warning("handle_checkpoint: %s account_id=%s", e, account_id)
            raise UnipileError(f"Checkpoint failed: {e}") from e

    async def resync_account(self, account_id: str) -> dict[str, Any]:
        """Trigger a resync of account data to refresh stale messaging state.

        GET /api/v1/accounts/{id}/resync
        """
        url = f"{self.base_url}/api/v1/accounts/{account_id}/resync"
        try:
            resp = await self._client.get(url, headers=self._headers())
            resp.raise_for_status()
            logger.info("resync_account: success account_id=%s", account_id)
            return resp.json()
        except Exception as e:
            logger.warning("resync_account: %s account_id=%s", e, account_id)
            raise UnipileError(f"Resync failed: {e}") from e

    # ── LinkedIn Post Creation & Comments ──

    async def create_post(
        self,
        account_id: str,
        text: str,
    ) -> dict[str, Any]:
        """Create a LinkedIn post (text only).

        POST /api/v1/posts
        """
        result: dict[str, Any] = {"success": False, "error": "", "post_id": ""}
        url = f"{self.base_url}/api/v1/posts"
        payload = {
            "account_id": account_id,
            "text": text,
        }
        try:
            resp = await self._retry_request("POST", url, json=payload)
            if resp.status_code in (200, 201):
                data = resp.json()
                result["success"] = True
                result["post_id"] = data.get("id") or data.get("post_id") or ""
            elif resp.status_code in (401, 403):
                result.update(_classify_http_auth_error(resp.status_code, resp.text[:500]))
            elif resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After", "")
                wait_msg = f" Retry after {retry_after}s." if retry_after else ""
                result["error"] = f"Rate limited by LinkedIn.{wait_msg}"
                result["blocked"] = True
                if retry_after:
                    try:
                        result["retry_after_seconds"] = int(retry_after)
                    except ValueError:
                        pass
            else:
                result["error"] = f"Post creation failed ({resp.status_code}): {resp.text[:200]}"
        except httpx.TimeoutException:
            result["error"] = "Request timed out."
        except Exception as e:
            result["error"] = f"Post creation failed: {e}"
        if result.get("success"):
            logger.info("create_post: success post_id=%s", result.get("post_id", ""))
        elif result.get("error"):
            logger.warning("create_post: %s", result["error"])
        return result

    async def get_post_comments(
        self,
        account_id: str,
        post_id: str,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Get comments on a LinkedIn post.

        GET /api/v1/posts/{post_id}/comments
        Unipile requires URN format (urn:li:activity:XXX) for post interactions.
        """
        # Convert numeric post_id to URN format if needed
        if post_id and not post_id.startswith("urn:"):
            post_id = f"urn:li:activity:{post_id}"
        url = f"{self.base_url}/api/v1/posts/{post_id}/comments?account_id={account_id}&limit={limit}"
        try:
            resp = await self._client.get(url, headers=self._headers())
            if resp.status_code in (401, 403):
                raise UnipileAuthError()
            resp.raise_for_status()
            data = resp.json()
            items = data.get("items") or data.get("comments") or data.get("data") or []
            if isinstance(data, list):
                items = data
            comments: list[dict[str, Any]] = []
            for item in items:
                if not isinstance(item, dict):
                    continue
                author = item.get("author") or {}
                if isinstance(author, str):
                    author = {"name": author}
                # Extract reply/reaction counts on the comment itself
                replies = item.get("replies") or []
                reactions = item.get("reactions") or []
                comments.append({
                    "comment_id": item.get("id") or item.get("comment_id") or "",
                    "text": item.get("text") or item.get("body") or item.get("content") or "",
                    "author_name": author.get("name") or "",
                    "author_id": str(author.get("provider_id") or author.get("id") or ""),
                    "author_headline": author.get("headline") or "",
                    "author_company": author.get("company") or "",
                    "author_profile_url": author.get("profile_url") or author.get("username") or "",
                    "timestamp": item.get("timestamp") or item.get("created_at") or "",
                    "reply_count": len(replies) if isinstance(replies, list) else 0,
                    "reaction_count": len(reactions) if isinstance(reactions, list) else 0,
                })
            return comments
        except UnipileAuthError:
            raise
        except Exception as e:
            logger.warning("Failed to get post comments: %s", e)
            return []

    async def get_post_reactions(
        self,
        account_id: str,
        post_id: str,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Get reactions on a LinkedIn post.

        GET /api/v1/posts/{post_id}/reactions
        Unipile requires URN format (urn:li:activity:XXX) for post interactions.
        """
        # Convert numeric post_id to URN format if needed
        if post_id and not post_id.startswith("urn:"):
            post_id = f"urn:li:activity:{post_id}"
        url = f"{self.base_url}/api/v1/posts/{post_id}/reactions?account_id={account_id}&limit={limit}"
        try:
            resp = await self._client.get(url, headers=self._headers())
            if resp.status_code in (401, 403):
                raise UnipileAuthError()
            resp.raise_for_status()
            data = resp.json()
            items = data.get("items") or data.get("reactions") or data.get("data") or []
            if isinstance(data, list):
                items = data
            reactions: list[dict[str, Any]] = []
            for item in items:
                if not isinstance(item, dict):
                    continue
                author = item.get("author") or {}
                if isinstance(author, str):
                    author = {"name": author}
                reactions.append({
                    "author_id": str(author.get("provider_id") or author.get("id") or item.get("provider_id") or ""),
                    "author_name": author.get("name") or item.get("name") or "",
                    "author_headline": author.get("headline") or "",
                    "reaction_type": item.get("reaction_type") or item.get("type") or "",
                    "timestamp": item.get("timestamp") or item.get("created_at") or "",
                })
            return reactions
        except UnipileAuthError:
            raise
        except Exception as e:
            logger.warning("Failed to get post reactions: %s", e)
            return []

    async def reply_to_comment(
        self,
        account_id: str,
        post_id: str,
        comment_id: str,
        text: str,
    ) -> dict[str, Any]:
        """Reply to a specific comment on a LinkedIn post.

        POST /api/v1/posts/{post_id}/comments
        """
        result: dict[str, Any] = {"success": False, "error": ""}
        url = f"{self.base_url}/api/v1/posts/{post_id}/comments"
        payload = {
            "account_id": account_id,
            "text": text,
            "parent_comment_id": comment_id,
        }
        try:
            resp = await self._retry_request("POST", url, json=payload)
            if resp.status_code in (200, 201):
                result["success"] = True
            elif resp.status_code in (401, 403):
                result.update(_classify_http_auth_error(resp.status_code, resp.text[:500]))
            elif resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After", "")
                wait_msg = f" Retry after {retry_after}s." if retry_after else ""
                result["error"] = f"Rate limited by LinkedIn.{wait_msg}"
                result["blocked"] = True
                if retry_after:
                    try:
                        result["retry_after_seconds"] = int(retry_after)
                    except ValueError:
                        pass
            else:
                result["error"] = f"Reply failed ({resp.status_code}): {resp.text[:200]}"
        except httpx.TimeoutException:
            result["error"] = "Request timed out."
        except Exception as e:
            result["error"] = f"Reply failed: {e}"
        if result.get("success"):
            logger.info("reply_to_comment: success comment_id=%s", comment_id)
        elif result.get("error"):
            logger.warning("reply_to_comment: %s comment_id=%s", result["error"], comment_id)
        return result


# ──────────────────────────────────────────────
# Module-level helpers
# ──────────────────────────────────────────────

def get_unipile_client() -> UnipileClient:
    """Create a UnipileClient from config.json settings."""
    cfg = config.load_config()
    api_url = cfg.get("unipile_api_url", "")
    api_key = cfg.get("unipile_api_key", "")
    if not api_url or not api_key:
        raise UnipileError(
            "Unipile not configured.\n\n"
            "Run setup_profile to configure your Unipile API key and URL."
        )
    return UnipileClient(api_url, api_key)


_cached_account_id: str | None = None
_cached_account_id_set: bool = False


def get_account_id() -> str | None:
    """Load the stored Unipile account_id from settings DB.

    Caches in memory after first successful load to avoid sync DB calls
    on the event loop thread in async contexts.
    """
    global _cached_account_id, _cached_account_id_set
    if _cached_account_id_set:
        return _cached_account_id
    from ..db.queries import get_setting
    val = get_setting("unipile_account_id", None)
    _cached_account_id = val
    _cached_account_id_set = True
    return val


def invalidate_account_id_cache() -> None:
    """Clear the cached account_id (call after account switch)."""
    global _cached_account_id, _cached_account_id_set
    _cached_account_id = None
    _cached_account_id_set = False
