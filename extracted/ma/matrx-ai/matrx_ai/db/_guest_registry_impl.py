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

Minting is bounded per client IP (2026-10-03): before GoTrue is called for a
NEW identity, ``_enforce_mint_ceiling`` checks an in-process per-IP log of
identities minted inside the ``auth.guest_identity`` window (knobs read through
the host's ``guest_mint_limit_reader``; the log is seeded from the table in the
background, never read on the mint path) and raises ``GuestMintRateLimitedError``
(429) at the ceiling. Only rows carrying the mint stamp (``metadata.minted_at``,
written since 2026-10-01 together with the real-client-IP fix) are counted, so
historic rows holding a Cloudflare edge address never bucket strangers
together. Bots are counted like everyone else; they are labelled, not refused.
Returning guests never reach the check.

Error resilience: all other DB and auth errors are caught and re-raised as
``GuestIdentityUnavailableError``.  A locally-generated UUID is forbidden:
it is not an ``auth.users`` identity and only moves the failure into the first
personal-organization or ownership write downstream.
"""

from __future__ import annotations

import inspect
import re
import time
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime, timedelta
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


class GuestMintRateLimitedError(RuntimeError):
    """This client IP reached the ``auth.guest_identity`` new-identity ceiling (429).

    A final refusal for this request, never a subclass of
    ``GuestIdentityUnavailableError`` (which means "retry in a moment"). Only a
    NEW identity is refused; a returning guest never reaches the check.
    """

    def __init__(self, ip_address: str | None, *, ceiling: int, window_minutes: int) -> None:
        super().__init__(
            f"Too many new guest identities from this network ({ceiling} per "
            f"{window_minutes} min)."
        )
        self.ip_address = ip_address
        self.ceiling = ceiling
        self.window_minutes = window_minutes
        self.retry_after_seconds = window_minutes * 60


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


def _mint_stamp(
    user_agent: str | None,
    minted_route: str | None,
    ip_address: str | None = None,
    agent_traffic: str | None = None,
) -> dict[str, Any]:
    traffic_kind, ua_family = classify_guest_user_agent(user_agent)
    stamp: dict[str, Any] = {}
    if agent_traffic:
        # The marker (matrx_ai.agent_traffic) is a statement, not a guess: it
        # outranks the user-agent heuristic, which is still recorded beside it.
        traffic_kind = "agent"
        stamp["agent_tool"] = agent_traffic
    return {
        **stamp,
        "traffic_kind": traffic_kind,
        "ua_family": ua_family,
        "minted_route": minted_route,
        "minted_ip": ip_address,
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
    agent_traffic: str | None = None,
    on_agent_minted: Callable[[str, str], Awaitable[None]] | None = None,
) -> str:
    """Return the stable auth.users UUID for this fingerprint.

    ``agent_traffic`` is the agent-traffic marker's value (``matrx_ai.agent_traffic``) when the
    request carried it: the mint stamp then says ``traffic_kind = "agent"``, and
    ``on_agent_minted(user_id, tool)`` runs for an identity THIS call minted and won (the host
    tags it with a test-fixture expiry). The hook never fails the request: an error is logged
    loudly and the identity is still returned.

    Resolving is NOT executing: no counter or execution timestamp moves here
    (they move only in the execution gate / ``record_guest_execution``). A
    request that MINTS stamps ``metadata`` with ``traffic_kind`` / ``ua_family``
    / ``minted_route`` / ``minted_at`` (merged; other keys kept).

    Flow:
      1. Look up guest_executions by fingerprint.
      2. If found and actively blocked     → raise ``GuestBlockedError`` (no writes).
      3. If found with auth_user_id set  → return auth_user_id (fast path).
      4. If found but auth_user_id is null → ceiling check, mint, CLAIM atomically.
      5. If not found                      → ceiling check, mint, create the row; a lost insert
                                             race CLAIMS the racer's row or adopts
                                             its identity.

    Exactly one identity per fingerprint is ever returned: a request whose
    minted user loses the claim returns the winner's.

    Raises ``GuestMintRateLimitedError`` when a NEW identity would pass the
    per-client-IP ceiling — nothing is minted; final for this request.
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
            await _enforce_mint_ceiling(ip_address)
            minted = await _create_anon_auth_user()
            winner = await _claim_identity(
                row_id,
                minted,
                metadata=_merged_metadata(row, _mint_stamp(user_agent, minted_route, ip_address, agent_traffic)),
            )
            if winner != minted:
                await _record_race_loser(fingerprint, loser=minted, winner=winner, branch="backfill")
                # The orphan is still an account our agent minted: tag it so the sweep removes it.
                await _after_agent_mint(minted, agent_traffic, on_agent_minted)
                return winner
            await _after_agent_mint(minted, agent_traffic, on_agent_minted)
            vcprint(
                f"[GuestRegistry] Backfilled auth_user_id for existing guest: "
                f"{minted[:8]}… fingerprint={fingerprint[:12]}…",
                color="green",
            )
            return minted

        # First visit — create both the anon auth user and the guest_executions row.
        await _enforce_mint_ceiling(ip_address)
        auth_user_id = await _create_anon_auth_user()
        try:
            await _gm.create_guest_executions(
                fingerprint=fingerprint,
                auth_user_id=auth_user_id,
                ip_address=ip_address,
                user_agent=user_agent,
                metadata=_mint_stamp(user_agent, minted_route, ip_address, agent_traffic),
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
                metadata=_merged_metadata(racer, _mint_stamp(user_agent, minted_route, ip_address, agent_traffic)),
            )
            if winner != auth_user_id:
                await _record_race_loser(
                    fingerprint, loser=auth_user_id, winner=winner, branch="first_visit"
                )
            # Winner or orphan, this call minted it: tag it so the sweep can remove it.
            await _after_agent_mint(auth_user_id, agent_traffic, on_agent_minted)
            return winner
        await _after_agent_mint(auth_user_id, agent_traffic, on_agent_minted)
        vcprint(
            f"[GuestRegistry] Created new guest: "
            f"{auth_user_id[:8]}… fingerprint={fingerprint[:12]}…",
            color="green",
        )
        return auth_user_id

    except (GuestBlockedError, GuestMintRateLimitedError):
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


async def _after_agent_mint(
    user_id: str,
    agent_traffic: str | None,
    hook: Callable[[str, str], Awaitable[None]] | None,
) -> None:
    """Hand an identity our agent just minted to the host's tagger. Never raises."""
    if not agent_traffic or hook is None:
        return
    try:
        await hook(user_id, agent_traffic)
    except Exception as exc:  # labelling never fails the guest's request
        vcprint(
            f"[GuestRegistry] agent-minted guest {user_id} was NOT tagged for expiry "
            f"(tool={agent_traffic}): {exc!r}",
            color="red",
            log_level="ERROR",
        )


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


#: Per client IP: wall-clock timestamps of the guest identities this process
#: knows were minted from it (seeded from the table in the background, plus
#: every mint this process admitted since). Read on the mint path; never a
#: database read there (USAGE-GATE.md rule 1, 2026-10-03).
_mint_log: dict[str, list[float]] = {}
#: When each IP's seed STARTED (epoch seconds); an IP is re-seeded once its
#: seed is older than the window, which is how another process's mints arrive.
_seeded_at: dict[str, float] = {}
_seed_tasks: dict[str, Any] = {}


def reset_mint_ceiling_state() -> None:
    """Tests: forget every IP this process has counted."""
    _mint_log.clear()
    _seeded_at.clear()
    _seed_tasks.clear()


async def _seed_mint_log(ip_address: str, window_minutes: int, started: float) -> None:
    """Background: the identities minted from ``ip_address`` inside the window.

    Counts rows holding an ``auth_user_id`` AND the mint stamp
    (``metadata ? 'minted_at'``), so pre-stamp rows (which hold Cloudflare edge
    addresses) never count. The read is bounded ABOVE by ``started``: rows minted
    before it come from the table, mints this process admits from ``started`` on
    come from the local log — so one mint is never counted twice.
    """
    until = datetime.fromtimestamp(started, UTC)
    since = until - timedelta(minutes=window_minutes)
    try:
        rows = await _gm.filter_all_guest_executions(
            ip_address=ip_address,
            auth_user_id__isnull=False,
            metadata__json_has_key="minted_at",
            created_at__gte=since,
            created_at__lt=until,
        )
    except Exception as exc:  # noqa: BLE001 — unseeded = local count only, announced
        _seeded_at.pop(ip_address, None)
        vcprint(
            f"[GuestRegistry] mint-ceiling seed for ip={ip_address} failed "
            f"({type(exc).__name__}: {exc}); counting this process's mints only until it reads.",
            color="red",
            log_level="ERROR",
        )
        return
    seeded = [
        _as_aware_utc(r.created_at).timestamp()
        for r in rows
        if getattr(r, "created_at", None) is not None
    ]
    later_local = [t for t in _mint_log.get(ip_address, []) if t >= started]
    _mint_log[ip_address] = sorted(seeded + later_local)


def _schedule_seed(ip_address: str, window_minutes: int, now: float) -> None:
    from matrx_utils import detached_task

    task = _seed_tasks.get(ip_address)
    if task is not None and not task.done():
        return
    seeded = _seeded_at.get(ip_address)
    if seeded is not None and (now - seeded) < window_minutes * 60:
        return
    _seeded_at[ip_address] = now
    task = detached_task(
        _seed_mint_log(ip_address, window_minutes, now), name=f"guest-mint-seed-{ip_address}"
    )
    _seed_tasks[ip_address] = task
    task.add_done_callback(lambda _t, ip=ip_address: _seed_tasks.pop(ip, None))


async def _enforce_mint_ceiling(ip_address: str | None) -> None:
    """Refuse a NEW guest identity once this client IP has minted its share.

    The host's reader answers the ``auth.guest_identity`` knobs for this address,
    or ``None`` when the address is not a countable client (loopback, unknown, a
    proxy edge) — then the mint proceeds and the skip is announced at WARNING.
    The count is an IN-PROCESS log per IP: seeded from the table in the
    BACKGROUND the first time an IP mints (and again once the seed is older than
    the window, which brings in other processes' mints), plus every mint this
    process admits. No database read decides a mint; the first mint from an
    unseen IP is decided on what this process already knows. Bots count like
    everyone else.
    """
    from matrx_ai._ext import get_guest_mint_limit_reader

    reader = get_guest_mint_limit_reader()
    if reader is None:
        raise RuntimeError(
            "no guest_mint_limit_reader is bound — refusing to mint an unlimited guest "
            "identity. Remedy: the host must configure_ext(guest_mint_limit_reader=...)."
        )
    limits = await reader(ip_address)
    if limits is None or not ip_address:
        vcprint(
            f"[GuestRegistry] Guest mint ceiling NOT applied: ip={ip_address!r} is not a "
            f"countable client address (loopback, unknown or a proxy edge)",
            color="yellow",
            log_level="WARNING",
        )
        return
    ceiling, window_minutes = int(limits[0]), int(limits[1])
    now = time.time()
    _schedule_seed(ip_address, window_minutes, now)
    horizon = now - window_minutes * 60
    log = [t for t in _mint_log.get(ip_address, []) if t >= horizon]
    _mint_log[ip_address] = log
    if len(log) >= ceiling:
        vcprint(
            f"[GuestRegistry] Guest mint ceiling reached: ip={ip_address} minted={len(log)} "
            f"ceiling={ceiling}/{window_minutes}min — new identity refused before GoTrue",
            color="yellow",
            log_level="WARNING",
        )
        raise GuestMintRateLimitedError(
            ip_address, ceiling=ceiling, window_minutes=window_minutes
        )
    log.append(now)


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
