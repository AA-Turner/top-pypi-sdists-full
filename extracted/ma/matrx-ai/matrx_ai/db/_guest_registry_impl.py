"""
Guest Registry — resolve a stable auth.users UUID for fingerprint-identified visitors.

On every guest request the auth middleware calls ``resolve_guest_uuid()``.
This function looks up ``guest_executions`` by fingerprint.  If a row exists
and already has an ``auth_user_id``, that UUID is returned immediately (fast
path — no auth API call needed).  If the row is new or ``auth_user_id`` is
missing, the function calls the Supabase Admin API to create a real anonymous
``auth.users`` record, then stores the returned UUID on the row.

The resulting UUID satisfies every FK constraint in the cx_ table family:
    cx_conversation.created_by  → auth.users(id) (via platform._stamp_actor when unset)
    cx_message.created_by     → auth.users(id)
    cx_user_request.created_by → auth.users(id)
    cx_tool_call.created_by   → auth.users(id)
    cx_agent_memory.created_by → auth.users(id)

Session continuity: subsequent requests with the same fingerprint get the
same UUID.  No sign-up required.

Sign-up conversion: when the guest creates an account, call
``link_guest_to_user(fingerprint, real_user_id)``.  All existing cx_ rows
already point to ``auth_user_id`` which is the anonymous user's UUID.
Supabase can promote an anonymous user to a real one in-place, so the UUID
never changes — no data migration is needed.

Blocked guests: a row with ``is_blocked`` whose ``blocked_until`` is unset or
still in the future raises ``GuestBlockedError`` before any counter update or
anonymous-user creation — the host maps it to a final 403 at its auth boundary.

One identity per fingerprint (2026-09-29): every write of ``auth_user_id`` is one
atomic claim — a conditional update that sets it only while it is still NULL,
then re-reads the winner. Concurrent first requests for one fingerprint may each
mint an anonymous user, but all of them return the same identity; a losing
minted user is logged loudly and recorded (``system_error`` kind
``guest_identity_race_loser``), never returned and never deleted.

Error resilience: all other DB and auth errors are caught and re-raised as
``GuestIdentityUnavailableError``.  A locally-generated UUID is forbidden:
it is not an ``auth.users`` identity and only moves the failure into the first
personal-organization or ownership write downstream.
"""

from __future__ import annotations

import inspect
import re
from datetime import UTC, datetime
from typing import Any

from matrx_utils import vcprint

from matrx_ai.db._registry import get_instance

_gm = get_instance("guest_executions_manager")
_lm = get_instance("guest_execution_log_manager")


class GuestIdentityUnavailableError(RuntimeError):
    """The guest resolver could not produce a real ``auth.users`` identity."""


class GuestBlockedError(RuntimeError):
    """This fingerprint's guest registry row is blocked; no identity is issued.

    A sibling of ``GuestIdentityUnavailableError``, deliberately NOT a subclass:
    unavailable is a retryable outage (503), blocked is a final refusal (403).
    A subclass would let every ``except GuestIdentityUnavailableError`` turn a
    block into "retry in a moment".
    """

    def __init__(self, fingerprint: str, blocked_until: datetime | None = None) -> None:
        until = f" until {blocked_until.isoformat()}" if blocked_until else ""
        super().__init__(f"Guest fingerprint {fingerprint[:12]}… is blocked{until}.")
        self.blocked_until = blocked_until


async def _create_anon_auth_user() -> str:
    """Create a Supabase anonymous auth.users record and return its UUID.

    Calls GoTrue's ``POST /auth/v1/signup`` endpoint with an empty body —
    GoTrue mints an ``is_anonymous=true`` row when the "Anonymous Sign-Ins"
    provider is enabled in the project's Auth settings.

    Why raw httpx instead of ``client.auth.sign_in_anonymously()``:
    the supabase-py async client is a process-wide singleton initialised
    with the service-role secret key. The SDK's ``sign_in_anonymously``
    calls ``_save_session`` + ``_notify_all_subscribers('SIGNED_IN', …)``
    on success, which would mutate the singleton's auth state — every
    concurrent admin/RPC/Realtime call on that client would then ride the
    guest's JWT instead of service-role. Calling the HTTP endpoint
    directly produces the same user row without any client-side side
    effects.

    Raises on any error — callers are responsible for catching.
    """
    import os

    import httpx

    url = os.environ.get("SUPABASE_MATRIX_URL")
    key = os.environ.get("SUPABASE_MATRIX_SECRET_KEY")
    if not url or not key:
        raise RuntimeError(
            "SUPABASE_MATRIX_URL / SUPABASE_MATRIX_SECRET_KEY env vars must "
            "be set for guest anonymous sign-in."
        )

    signup_url = f"{url.rstrip('/')}/auth/v1/signup"
    async with httpx.AsyncClient(timeout=10.0) as http:
        resp = await http.post(
            signup_url,
            headers={"apikey": key, "Content-Type": "application/json"},
            # Empty body + provider enabled = anonymous user. Any payload
            # with email/phone would create a non-anonymous user instead.
            json={},
        )
        if resp.status_code >= 400:
            # Surface the GoTrue error body to the caller so log lines like
            # ``anonymous_provider_disabled`` are visible instead of just
            # an opaque HTTPStatusError.
            raise RuntimeError(f"GoTrue signup failed ({resp.status_code}): {resp.text}")
        body = resp.json()
        user_id = (body.get("user") or {}).get("id")
        if not user_id:
            raise RuntimeError(f"GoTrue signup returned no user.id: {body!r}")
        return str(user_id)


# Non-human callers — mirrors matrx-frontend lib/product-analytics/user-acquisition.ts
# BOT_USER_AGENT, plus our own agent browser (``Claude/x.y``). A bot is STAMPED,
# never refused: our agents run guest-flow tests in headless Chrome.
_BOT_USER_AGENT = re.compile(
    r"\b([a-z0-9_-]*bot|crawler|spider|slurp|bingpreview|facebookexternalhit|headlesschrome"
    r"|lighthouse|semrush|ahrefs|bytespider)\b"
    r"|\b(curl|wget|python-requests|python-httpx|aiohttp|httpie|okhttp|axios|go-http-client"
    r"|libwww-perl|java|apache-httpclient|node-fetch|got|undici)\b"
    r"|\bclaude/[\d.]+"
    r"|^node$",
    re.IGNORECASE,
)
_BROWSER_FAMILIES = (("edge", r"Edg/"), ("firefox", r"Firefox/"), ("chrome", r"Chrome/"), ("safari", r"Safari/"))


def classify_guest_user_agent(user_agent: str | None) -> tuple[str, str]:
    """``(traffic_kind, ua_family)`` — ``traffic_kind`` is ``bot`` or ``browser``.

    ``ua_family`` names the matched bot token (lower-cased) or the browser
    family; ``unknown`` when no user agent was sent (counted as ``bot``: every
    real browser sends one).
    """
    if not user_agent:
        return "bot", "unknown"
    match = _BOT_USER_AGENT.search(user_agent)
    if match:
        token = (match.group(0) or "").lower()
        return "bot", token.split("/", 1)[0] or "unknown"
    for family, pattern in _BROWSER_FAMILIES:
        if re.search(pattern, user_agent):
            return "browser", family
    return "browser", "other"


def _mint_stamp(user_agent: str | None, minted_route: str | None) -> dict[str, Any]:
    traffic_kind, ua_family = classify_guest_user_agent(user_agent)
    return {
        "traffic_kind": traffic_kind,
        "ua_family": ua_family,
        "minted_route": minted_route,
        "minted_at": datetime.now(UTC).isoformat(),
    }


def _merged_metadata(row: Any, stamp: dict[str, Any]) -> dict[str, Any]:
    """The row's metadata with the mint stamp merged in — other keys kept."""
    current = getattr(row, "metadata", None)
    merged = dict(current) if isinstance(current, dict) else {}
    merged.update(stamp)
    return merged


async def guest_has_identity(fingerprint: str) -> bool:
    """True when this fingerprint already owns an ``auth.users`` identity.

    Read-only: mints nothing, moves no counter. The auth middleware asks this
    before a READ request (GET/HEAD/OPTIONS) so a visitor who has never done
    anything that needs an account — a crawler, a link preview, a page load —
    is answered anonymously instead of getting an anonymous user and an
    organization of their own. Raises ``GuestIdentityUnavailableError`` when
    the registry cannot be read (never answers a guess).
    """
    try:
        rows = await _gm.filter_all_guest_executions(fingerprint=fingerprint)
    except Exception as exc:
        raise GuestIdentityUnavailableError(
            "Guest registry could not be read."
        ) from exc
    return bool(rows and getattr(rows[0], "auth_user_id", None))


async def resolve_guest_uuid(
    fingerprint: str,
    ip_address: str | None = None,
    user_agent: str | None = None,
    minted_route: str | None = None,
) -> str:
    """Return the stable auth.users UUID for this fingerprint.

    Resolving is NOT executing: no counter or execution timestamp moves here
    (they move only in the execution gate / ``record_guest_execution``). A
    request that MINTS stamps ``metadata`` with ``traffic_kind`` / ``ua_family``
    / ``minted_route`` / ``minted_at`` (merged; other keys kept).

    Flow:
      1. Look up guest_executions by fingerprint.
      2. If found and actively blocked     → raise ``GuestBlockedError`` (no writes).
      3. If found with auth_user_id set  → return auth_user_id (fast path).
      4. If found but auth_user_id is null → mint, then CLAIM the row atomically.
      5. If not found                      → mint, create the row; a lost insert
                                             race CLAIMS the racer's row or adopts
                                             its identity.

    Exactly one identity per fingerprint is ever returned: a request whose
    minted user loses the claim returns the winner's.

    Raises ``GuestBlockedError`` when the row is blocked and ``blocked_until`` is
    unset or in the future — a final refusal, never wrapped as unavailable.
    Raises ``GuestIdentityUnavailableError`` when the registry or anonymous
    sign-in cannot produce a real ``auth.users`` row.  Callers must stop at the
    authentication boundary on either; a synthetic UUID is not an identity.
    """
    try:
        existing = await _gm.filter_all_guest_executions(fingerprint=fingerprint)

        if existing:
            row = existing[0]
            now = datetime.now(UTC)
            auth_user_id: str | None = getattr(row, "auth_user_id", None)
            if auth_user_id:
                auth_user_id = str(auth_user_id)
            row_id = str(row.id)

            # A blocked guest is refused HERE — before its counters move and
            # before an anonymous auth user is minted or backfilled for it.
            # Same rule as public.check_guest_execution_limit: the block holds
            # while blocked_until is unset or still in the future.
            blocked_until = getattr(row, "blocked_until", None)
            if getattr(row, "is_blocked", False) and (
                blocked_until is None or _as_aware_utc(blocked_until) > now
            ):
                vcprint(
                    f"[GuestRegistry] Blocked guest refused before identity "
                    f"fingerprint={fingerprint[:12]}… until={blocked_until or 'indefinite'}",
                    color="yellow",
                )
                raise GuestBlockedError(fingerprint, blocked_until)

            if auth_user_id:
                # Identity resolve only — no write. Counters move on real
                # executions, never on every request that carries a fingerprint.
                vcprint(
                    f"[GuestRegistry] Returning existing guest: "
                    f"{auth_user_id[:8]}… fingerprint={fingerprint[:12]}…",
                    color="cyan",
                )
                return auth_user_id

            # Row exists but auth_user_id was never populated (an acquisition
            # first-touch row, or a legacy row) — mint, then CLAIM atomically.
            minted = await _create_anon_auth_user()
            winner = await _claim_identity(
                row_id,
                minted,
                metadata=_merged_metadata(row, _mint_stamp(user_agent, minted_route)),
            )
            if winner != minted:
                await _record_race_loser(fingerprint, loser=minted, winner=winner, branch="backfill")
                return winner
            vcprint(
                f"[GuestRegistry] Backfilled auth_user_id for existing guest: "
                f"{minted[:8]}… fingerprint={fingerprint[:12]}…",
                color="green",
            )
            return minted

        # First visit — create both the anon auth user and the guest_executions row.
        auth_user_id = await _create_anon_auth_user()
        try:
            await _gm.create_guest_executions(
                fingerprint=fingerprint,
                auth_user_id=auth_user_id,
                ip_address=ip_address,
                user_agent=user_agent,
                metadata=_mint_stamp(user_agent, minted_route),
            )
        except Exception:
            # A concurrent request committed the unique fingerprint row while
            # this one was minting. If that row already holds an identity it
            # wins; if it holds none (a concurrent acquisition first-touch, or
            # a racer that has not claimed yet), claim it atomically. Either
            # way exactly one identity is returned. No row = a real failure.
            winners = await _gm.filter_all_guest_executions(fingerprint=fingerprint)
            if not winners:
                raise
            racer = winners[0]
            winner = await _claim_identity(
                str(racer.id),
                auth_user_id,
                metadata=_merged_metadata(racer, _mint_stamp(user_agent, minted_route)),
            )
            if winner != auth_user_id:
                await _record_race_loser(
                    fingerprint, loser=auth_user_id, winner=winner, branch="first_visit"
                )
            return winner
        vcprint(
            f"[GuestRegistry] Created new guest: "
            f"{auth_user_id[:8]}… fingerprint={fingerprint[:12]}…",
            color="green",
        )
        return auth_user_id

    except GuestBlockedError:
        # A refusal, not an outage — never re-wrap it as "unavailable".
        raise
    except Exception as exc:
        vcprint(
            f"[GuestRegistry] Guest identity unavailable — request refused before auth: {exc}",
            color="red",
        )
        raise GuestIdentityUnavailableError(
            "Guest identity could not be resolved to an auth.users row."
        ) from exc


async def _claim_identity(row_id: str, minted: str, **fields: object) -> str:
    """Atomically set ``auth_user_id`` on ``row_id`` ONLY while it is still NULL.

    One conditional UPDATE (``... WHERE id = $1 AND auth_user_id IS NULL``) —
    Postgres serialises concurrent claims on the row, so exactly one wins.
    Returns the identity the row holds afterwards: ``minted`` when this call
    won, the earlier winner's otherwise. Raises when the row vanished.
    """
    result = await _gm.update_where(
        {"id": row_id, "auth_user_id__isnull": True},
        auth_user_id=minted,
        **fields,
    )
    if getattr(result, "rows_affected", 0):
        return minted
    rows = await _gm.filter_all_guest_executions(id=row_id)
    holder = getattr(rows[0], "auth_user_id", None) if rows else None
    if not holder:
        raise RuntimeError(
            f"guest row {row_id} could not be claimed and holds no identity (row gone?)"
        )
    return str(holder)


async def _record_race_loser(fingerprint: str, *, loser: str, winner: str, branch: str) -> None:
    """A concurrent request won this fingerprint; ``loser`` is never served.

    Loud by contract: a WARNING line plus one ``system_error`` row (kind
    ``guest_identity_race_loser``) naming the orphaned anonymous ``auth.users``
    id so it can be found. Not deleted here (archive, never delete); no
    guest_executions row points to it.
    """
    vcprint(
        f"[GuestRegistry] Concurrent mint lost ({branch}): anonymous user {loser[:8]}… is an "
        f"orphan; returning winner {winner[:8]}… fingerprint={fingerprint[:12]}…",
        color="yellow",
        log_level="WARNING",
    )
    try:
        from matrx_ai._ext import get_ext, has_ext

        if not has_ext("record_error"):
            return
        pending = get_ext("record_error")(
            RuntimeError("guest identity race: minted anonymous user lost the claim"),
            kind="guest_identity_race_loser",
            error_type="guest_identity_race_loser",
            error_text=(
                f"Two first requests for one guest fingerprint minted two anonymous users; "
                f"{loser} lost the atomic claim and is served to nobody."
            ),
            payload={
                "orphan_auth_user_id": loser,
                "winner_auth_user_id": winner,
                "branch": branch,
                "effect": "orphan anonymous auth.users row (and its signup organization); no guest row points to it",
            },
            route="matrx_ai.db.guest_registry.resolve_guest_uuid",
        )
        if inspect.isawaitable(pending):
            await pending
    except Exception as capture_exc:  # capture never fails the guest's request
        vcprint(
            f"[GuestRegistry] race-loser capture FAILED for orphan {loser}: {capture_exc!r}",
            color="red",
        )


def _as_aware_utc(value: datetime) -> datetime:
    return value if value.tzinfo is not None else value.replace(tzinfo=UTC)


async def log_guest_execution(
    fingerprint: str,
    resource_type: str,
    resource_id: str | None = None,
    resource_name: str | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
) -> None:
    """Fire-and-forget: write a guest_execution_log row.

    Looks up ``guest_executions.id`` (the table PK) from the fingerprint —
    that is the FK required by ``guest_execution_log.guest_id``.  The caller
    only needs to supply the fingerprint; the internal guest_executions.id is
    resolved here.

    Errors are logged, never raised.
    """
    try:
        existing = await _gm.filter_all_guest_executions(fingerprint=fingerprint)
        if not existing:
            vcprint(
                f"[GuestRegistry] log_guest_execution: no guest row for fingerprint={fingerprint[:12]}…",
                color="yellow",
            )
            return
        guest_executions_id = str(existing[0].id)
        await _lm.create_guest_execution_log(
            guest_id=guest_executions_id,
            fingerprint=fingerprint,
            resource_type=resource_type,
            resource_id=resource_id,
            resource_name=resource_name,
            ip_address=ip_address,
            user_agent=user_agent,
        )
    except Exception as exc:
        vcprint(
            f"[GuestRegistry] Failed to log execution for fingerprint={fingerprint[:12]}…: {exc}",
            color="yellow",
        )


async def link_guest_to_user(fingerprint: str, real_user_id: str) -> bool:
    """Stamp converted_to_user_id on the guest_executions row at sign-up.

    ``real_user_id`` is the new permanent auth.users UUID after the guest
    creates an account.  The anonymous user (``auth_user_id``) can be promoted
    by Supabase in-place, so the UUID that ``cx_conversation`` etc. already
    hold never needs changing.

    Returns True if the row was found and updated, False otherwise.
    """
    try:
        existing = await _gm.filter_all_guest_executions(fingerprint=fingerprint)
        if not existing:
            vcprint(
                f"[GuestRegistry] link_guest_to_user: no row for fingerprint={fingerprint[:12]}…",
                color="yellow",
            )
            return False
        row = existing[0]
        await _gm.update_guest_executions(
            str(row.id),
            converted_to_user_id=real_user_id,
            converted_at=datetime.now(UTC),
        )
        vcprint(
            f"[GuestRegistry] Linked guest {str(row.id)[:8]}… → user {real_user_id[:8]}…",
            color="green",
        )
        return True
    except Exception as exc:
        vcprint(
            f"[GuestRegistry] Failed to link guest to user {real_user_id[:8]}…: {exc}",
            color="yellow",
        )
        return False
