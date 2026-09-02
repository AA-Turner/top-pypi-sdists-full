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

Error resilience: all DB and auth errors are caught and re-raised as
``GuestIdentityUnavailableError``.  A locally-generated UUID is forbidden:
it is not an ``auth.users`` identity and only moves the failure into the first
personal-organization or ownership write downstream.
"""

from __future__ import annotations

from datetime import UTC, datetime

from matrx_utils import vcprint

from matrx_ai.db._registry import get_instance

_gm = get_instance("guest_executions_manager")
_lm = get_instance("guest_execution_log_manager")


class GuestIdentityUnavailableError(RuntimeError):
    """The guest resolver could not produce a real ``auth.users`` identity."""


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


async def resolve_guest_uuid(
    fingerprint: str,
    ip_address: str | None = None,
    user_agent: str | None = None,
) -> str:
    """Return the stable auth.users UUID for this fingerprint.

    Flow:
      1. Look up guest_executions by fingerprint.
      2. If found with auth_user_id set  → return auth_user_id (fast path).
      3. If found but auth_user_id is null → create anon auth user, patch row.
      4. If not found                      → create anon auth user, create row.

    Raises ``GuestIdentityUnavailableError`` when the registry or anonymous
    sign-in cannot produce a real ``auth.users`` row.  Callers must stop at the
    authentication boundary; a synthetic UUID is not an identity.
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

            if getattr(row, "is_blocked", False):
                vcprint(
                    f"[GuestRegistry] Blocked guest fingerprint={fingerprint[:12]}…",
                    color="red",
                )

            if auth_user_id:
                await _gm.update_guest_executions(
                    row_id,
                    first_execution_at=getattr(row, "first_execution_at", None) or now,
                    last_execution_at=now,
                    total_executions=getattr(row, "total_executions", 0) + 1,
                )
                vcprint(
                    f"[GuestRegistry] Returning existing guest: "
                    f"{auth_user_id[:8]}… fingerprint={fingerprint[:12]}…",
                    color="cyan",
                )
                return auth_user_id

            # Row exists but auth_user_id was never populated — create anon user now.
            auth_user_id = await _create_anon_auth_user()
            await _gm.update_guest_executions(
                row_id,
                auth_user_id=auth_user_id,
                first_execution_at=getattr(row, "first_execution_at", None) or now,
                last_execution_at=now,
                total_executions=getattr(row, "total_executions", 0) + 1,
            )
            vcprint(
                f"[GuestRegistry] Backfilled auth_user_id for existing guest: "
                f"{auth_user_id[:8]}… fingerprint={fingerprint[:12]}…",
                color="green",
            )
            return auth_user_id

        # First visit — create both the anon auth user and the guest_executions row.
        auth_user_id = await _create_anon_auth_user()
        try:
            await _gm.create_guest_executions(
                fingerprint=fingerprint,
                auth_user_id=auth_user_id,
                ip_address=ip_address,
                user_agent=user_agent,
                total_executions=1,
            )
        except Exception:
            # A concurrent first request may have committed the unique
            # fingerprint row while this request was creating its anonymous
            # auth identity. Adopt that winner instead of refusing a valid
            # guest as unavailable. Any non-race failure still propagates.
            winners = await _gm.filter_all_guest_executions(fingerprint=fingerprint)
            winner_auth_user_id = (
                getattr(winners[0], "auth_user_id", None) if winners else None
            )
            if not winner_auth_user_id:
                raise
            return str(winner_auth_user_id)
        vcprint(
            f"[GuestRegistry] Created new guest: "
            f"{auth_user_id[:8]}… fingerprint={fingerprint[:12]}…",
            color="green",
        )
        return auth_user_id

    except Exception as exc:
        vcprint(
            f"[GuestRegistry] Guest identity unavailable — request refused before auth: {exc}",
            color="red",
        )
        raise GuestIdentityUnavailableError(
            "Guest identity could not be resolved to an auth.users row."
        ) from exc


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
