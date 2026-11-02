"""Approved-server request identity — the opt-in "this call is one of our servers" path.

This is the ONE canonical primitive for server-to-server auth across the Matrx
family (aidream → scraper-service, the sandbox bridge, the media-healer). Before
this, the same shape was hand-rolled in three places.

**It is NOT part of `AuthMiddleware`, and must never be.** The middleware accepts
ONLY a real user-login token (a Supabase-signed JWT) — that contract stays. This
module is a set of EXPLICIT, per-route dependencies a host applies to specific
routers when a sibling SERVER (not a person) needs to call them.

The handshake, in plain terms:
  1. The caller proves it is **one of our servers** — it presents a shared secret
     only our servers hold (compared in constant time).
  2. When the call acts **for a person**, it names that person via the
     ``X-Matrx-User-Id`` header. The request is then scoped to THAT real user.
  3. It names the **organization** the work belongs to via ``X-Organization-Id``
     — on every call, with or without an acting user. A hop between our own
     servers carries actor AND organization and is admitted the same way as any
     other request; if it is not included, the request is denied.

**Never a fixed admin.** The acting user is exactly what the caller names, or
empty for ephemeral, no-write calls. It is NEVER defaulted to an admin/system
user — that fixed-user mis-attribution is the exact 2026-05 scraper incident
(``docs/archive/2026/scraper__SCRAPER_SECURITY_BUGS.md``). An endpoint that writes user-owned
rows enforces its own owner and raises on a missing user, so a userless service
call to such an endpoint fails loudly rather than mis-attributing.
"""

from __future__ import annotations

import hmac
from collections.abc import Awaitable, Callable
from uuid import UUID

from fastapi import HTTPException, Request, status

from matrx_connect.context.app_context import AppContext, set_app_context
from matrx_connect.org_hold import (
    ORGANIZATION_MALFORMED,
    ORGANIZATION_MISMATCH,
    OrganizationRequired,
)

USER_HEADER = "X-Matrx-User-Id"
ORGANIZATION_HEADER = "X-Organization-Id"


def _presented_secret(request: Request, secret_header: str) -> str:
    raw = request.headers.get(secret_header) or ""
    if secret_header.lower() == "authorization":
        return raw.split(" ", 1)[1].strip() if raw[:7].lower() == "bearer " else ""
    return raw.strip()


def _validate_user(value: str, header: str) -> None:
    try:
        UUID(value)
    except (ValueError, TypeError) as exc:  # noqa: TRY003
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{header} must be a UUID",
        ) from exc


def verify_approved_server(
    request: Request,
    *,
    secret: str,
    secret_header: str = "authorization",
    require_user: bool = False,
    user_header: str = USER_HEADER,
) -> str:
    """Verify the caller is an approved server; return the acting ``user_id``.

    - ``secret`` — the shared approved-server secret (empty ⇒ always 401; the path
      is effectively disabled). A caller that wants a distinct "not configured"
      signal (503) should check that itself BEFORE calling this.
    - ``secret_header`` — where the secret is presented: ``"authorization"`` (a
      ``Bearer`` value) or a custom header name (e.g. ``"x-cloud-files-bypass"``).
    - ``require_user`` — if True, ``user_header`` MUST carry a valid UUID (400
      otherwise). If False, the header is optional but still shape-validated when
      present; returns ``""`` when absent.

    Pure — never mutates request state. Raises 401 on a bad/absent secret.
    """
    presented = _presented_secret(request, secret_header)
    if not secret or not presented or not hmac.compare_digest(presented, secret):
        # A refusal that does not name the contract sends the caller to whatever
        # doc they already have — and a stale one cost a real afternoon on
        # 2026-09-17, when an `X-API-Key` scheme retired long ago was still
        # documented as the scraper's auth and the 401 said only
        # "credentials required". Naming HOW to present the secret is a
        # contract, never a secret; the value itself is never echoed.
        expected = (
            "Authorization: Bearer <token>"
            if secret_header.lower() == "authorization"
            else f"{secret_header}: <token>"
        )
        message = f"Approved-server credentials required — present them as `{expected}`."
        if not presented and request.headers.get("x-api-key"):
            message += (
                " This service does not accept `X-API-Key`; that scheme is retired. "
                "Any document still describing it is out of date."
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "service_credentials_required",
                "message": message,
                "expected_header": secret_header,
            },
        )
    acting = (request.headers.get(user_header) or "").strip()
    if require_user and not acting:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{user_header} header required",
        )
    if acting:
        _validate_user(acting, user_header)
    return acting


def _organization_from_headers(request: Request, *, required: bool) -> str | None:
    """Read ``X-Organization-Id`` off the wire, UUID-validated.

    ``required=True`` refuses a call that names no organization (400
    ``organization_required``); a malformed one is ALWAYS refused (400
    ``organization_malformed``), required or not — a value that is not an
    organization id is never worth admitting and never worth "try again".
    """
    raw = (request.headers.get(ORGANIZATION_HEADER) or "").strip()
    if not raw:
        if not required:
            return None
        # THE ONE HOLD — not a bespoke 400. The caller gets the typed envelope
        # and (once the host's error handler enriches it) the list of
        # organizations this person may actually act in.
        raise OrganizationRequired(
            what=(
                f"This service call named no organization. Send {ORGANIZATION_HEADER}; "
                "the server never chooses one for you."
            ),
            set_on="request",
            user_id=(request.headers.get(USER_HEADER) or "").strip() or None,
        )
    try:
        return str(UUID(raw))
    except (ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": ORGANIZATION_MALFORMED,
                "code": ORGANIZATION_MALFORMED,
                "message": f"{ORGANIZATION_HEADER} must be an organization id (a UUID).",
            },
        ) from exc


def require_authenticated_or_service(
    secret: str | Callable[[], str],
    *,
    require_user: bool = False,
    secret_header: str = "authorization",
    service_only: bool = False,
    organization_optional: bool = False,
    organization_optional_reason: str = "",
) -> Callable[[Request], Awaitable[None]]:
    """Router dependency: admit EITHER a real user login (AuthMiddleware already
    set ``is_authenticated``) OR an approved-server call. On the service path it
    stamps the named acting user AND the named organization into the request
    context, so downstream code is scoped exactly as a login would be.
    ``secret`` may be a value or a zero-arg getter (read lazily so app-build
    order never matters).

    **Structurally below the organization gate.** ``AuthMiddleware`` admits an
    organization on the SAME line as identity, but this dependency runs AFTER
    the middleware, as a FastAPI ``Depends`` — a service call that lands here
    was anonymous when the gate ran, so the gate never saw it, and this
    function used to mint a NEW authenticated context (a real ``user_id``)
    with no organization at all. That is the exact class of bug the gate
    exists to close, just reached from underneath it.

    **THE ORGANIZATION IS ON THE WIRE OR THE CALL IS REFUSED.** A hop between
    our own servers carries actor AND organization and is admitted the same
    way as any other request (``common-docs/policies/context-is-carried-never-rebuilt.md``
    rule 1; Arman: "if it's not included, the request is denied"). So EVERY
    service-authenticated call — the ones naming an acting user
    (``X-Matrx-User-Id``) and the "pure service", no-actor ones alike —
    requires an explicit, well-formed ``X-Organization-Id``. Until
    2026-09-17 the no-actor path skipped the requirement entirely: a userless
    service call was admitted with NO organization at all, and each receiving
    route then took the tenant from a request-BODY field, so a route that
    forgot the field had no tenant and nothing screamed.

    ``secret_header`` names where the shared secret is presented — ``Bearer`` on
    ``authorization`` by default, or a custom header for a caller that already
    has one (the media healer's ``X-Cloud-Files-Bypass``). It is the same value
    ``verify_approved_server`` takes; a door does not need a second primitive
    just because its secret rides a different header.

    ``service_only=True`` says a user login is NOT an admission here: the door is
    server-to-server, and a real person's JWT gets the same 401 a stranger does.
    Without it this dependency returns early for any authenticated request, which
    on a route that was previously secret-gated would hand every signed-in user a
    door that used to be ours alone.

    The header is trusted as presented: this primitive has no membership table
    of its own to verify a SERVER's claim against, so the admission it installs
    is ``organization_admission="none"`` — the honest marker, never "verified".
    A route that also receives an organization in its body compares the two and
    refuses a disagreement (409), exactly as aidream's
    ``organization_for_request`` does.

    **The ONE lawful exemption** is a route that genuinely touches no tenant
    data, declared at mount time with ``organization_optional=True`` AND an
    ``organization_optional_reason`` saying why — a silent opt-out is banned,
    an explicit, read-aloud reason is not. Even then a header that IS present
    is validated and installed, so an honest caller is never discarded.
    """
    if organization_optional and not organization_optional_reason:
        raise ValueError(
            "organization_optional=True requires organization_optional_reason — "
            "a silent opt-out is exactly the fallback this gate exists to ban"
        )

    async def _require_authenticated_or_service(request: Request) -> None:
        ctx: AppContext | None = getattr(request.state, "context", None)
        if ctx is not None and ctx.is_authenticated and not service_only:
            # AuthMiddleware already admitted this request, organization
            # included — nothing new for the service lane to check.
            return
        resolved = secret() if callable(secret) else secret
        acting = verify_approved_server(
            request,
            secret=resolved,
            secret_header=secret_header,
            require_user=require_user,
        )

        organization_id = _organization_from_headers(
            request, required=not organization_optional
        )

        if ctx is None:
            # AuthMiddleware always installs request.state.context, so this
            # branch is unreachable in a wired host — and the old stand-in,
            # ``AppContext()``, could not even be built (the constructor takes
            # an emitter), so it would have been a TypeError dressed as a 500.
            # A door with no context refuses by name instead of minting one.
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "request_context_missing",
                    "message": (
                        "require_authenticated_or_service ran on a request with no "
                        "AppContext installed. The host must mount AuthMiddleware "
                        "(matrx_connect.middleware.auth) before this router."
                    ),
                },
            )
        base = ctx
        new_ctx = base.with_overrides(
            user_id=acting,
            is_authenticated=True,
            auth_type="token",
            organization_id=organization_id,
            organization_admission="none",
        )
        request.state.context = new_ctx
        set_app_context(new_ctx)

    return _require_authenticated_or_service


def confirm_request_organization(ctx: AppContext, claimed: str | None = None) -> str:
    """The organization this request acts in — the context's, and only the context's.

    The receiving half of the wire contract above, for a route whose request
    BODY also carries an ``organization_id``. The admitted organization (from
    ``X-Organization-Id``, installed on the context) is the authority; a body
    value may CONFIRM it and never replaces it:

    * no organization on the context → ``400 organization_required``; the route
      never falls back to the body, a default, or a personal organization;
    * a body value that disagrees → ``409 organization_context_mismatch``, the
      same answer aidream's ``organization_for_request`` gives.

    Kept here, beside the admission that installs the value, so every host
    (matrx-scraper included) reads one rule rather than hand-rolling a second.
    """
    ctx_org = str(getattr(ctx, "organization_id", "") or "").strip() or None
    claimed_raw = str(claimed or "").strip() or None
    if ctx_org is None:
        # THE ONE HOLD — the caller carries an identity, so the host's error
        # handler can name the organizations it may choose from.
        raise OrganizationRequired(
            what=(
                "This request carried an identity but no organization. Send the "
                f"{ORGANIZATION_HEADER} header naming the organization you are "
                "acting in."
            ),
            set_on="request",
            user_id=str(getattr(ctx, "user_id", "") or "").strip() or None,
        )
    verified = _canonical_organization(ctx_org, field="context organization_id")
    if claimed_raw is not None and (
        _canonical_organization(claimed_raw, field="organization_id") != verified
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": ORGANIZATION_MISMATCH,
                "code": ORGANIZATION_MISMATCH,
                "message": (
                    "The request body names a different organization than the one this "
                    "request was admitted for. The admitted organization is the only one "
                    "a request acts in; a body value can confirm it, never replace it."
                ),
                "claimed_organization_id": claimed_raw,
                "organization_id": verified,
            },
        )
    return verified


def _canonical_organization(value: object, *, field: str) -> str:
    try:
        return str(UUID(str(value).strip()))
    except (ValueError, TypeError, AttributeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "organization_id_invalid",
                "code": "organization_id_invalid",
                "message": f"{field} is not an organization id.",
            },
        ) from exc


__all__ = [
    "ORGANIZATION_HEADER",
    "USER_HEADER",
    "confirm_request_organization",
    "require_authenticated_or_service",
    "verify_approved_server",
]
