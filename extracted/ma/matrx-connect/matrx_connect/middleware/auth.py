"""Auth middleware — pure ASGI, no BaseHTTPMiddleware.

Auth resolution order per request:
1. Bearer mx_* -> injected API-key resolver -> service or personal identity
2. Other bearer -> verified Supabase JWT, configured current-session authority,
                   organization admission and resolved admin tier
   Any presented/refused authorization ends here; no guest/cookie fallback.
3. Fingerprint -> injected guest resolver -> real guest user
4. File cookie -> verified source binding/current authority on enabled hosts,
                  legacy HMAC-only identity otherwise; eligible GET bytes only
5. None of the above -> anonymous. Static admin credentials are never admitted.

Sets both:
  - request.state.context  -> consumed by FastAPI Depends(context_dep)
  - ContextVar             -> consumed by get_app_context() anywhere in the stack
"""

from __future__ import annotations

import asyncio
import copy
import hashlib
import logging
import re
import time
import uuid
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from dataclasses import dataclass
from typing import Any, Protocol
from urllib.parse import unquote

import jwt
from matrx_utils import AsyncSingleFlight, get_inflight_registry, vcprint
from starlette.requests import HTTPConnection, Request
from starlette.types import ASGIApp, Receive, Scope, Send

from matrx_connect.client_ip import client_ip
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_connect.emitters.stream_emitter import StreamEmitter
from matrx_connect.routing import AuthenticatedResourceRoute
from .authority_retry import DEFAULT_SESSION_ATTEMPT_SECONDS, FreshFlight, call_authority
from .file_session import FileSessionCredential, classify_bound_file_session_value
from .session_authority import (
    CredentialAuthorityUnavailable,
    CurrentSessionDecision,
    SessionAuthorityUnavailable,
    credential_unavailable_response,
)


def _is_uuid(value: str) -> bool:
    if not value:
        return False
    try:
        uuid.UUID(value)
        return True
    except (ValueError, AttributeError, TypeError):
        return False


#: admission marker → the machine reason a refusal reports. One code per
#: SITUATION, because a caller that cannot tell them apart cannot know whether
#: retrying is worth anything (only `organization_unverifiable` is).
_ADMISSION_REASON_CODES = {
    "none": "organization_required",
    "denied": "organization_forbidden",
    "unknown": "organization_not_found",
    "archived": "organization_archived",
    "malformed": "organization_id_invalid",
    "unverifiable": "organization_unverifiable",
}

#: Every code the organization admission gate can refuse with — for consumers
#: that classify a refusal (e.g. the local transport's 400 → 403 mapping), so
#: they read the gate's table instead of keeping a copy that drifts.
ADMISSION_REFUSAL_CODES: frozenset[str] = frozenset(_ADMISSION_REASON_CODES.values())


class GuestResolver(Protocol):
    """``(fingerprint, ip, user_agent, *, route) -> auth.users id``.

    ``route`` is ``"<METHOD> <path>"`` of the request that is resolving the
    guest, so a host that mints an identity can record WHICH request minted it.
    """

    def __call__(
        self,
        fingerprint: str,
        ip_address: str | None,
        user_agent: str | None,
        *,
        route: str | None = None,
    ) -> Awaitable[str]: ...


@dataclass(frozen=True)
class ApiKeyIdentity:
    """Resolved identity for an ``Authorization: Bearer mx_...`` API key.

    Produced by the host-injected ``ApiKeyResolver``. ``user_id`` is the key's
    REAL service-identity ``auth.users`` row (guest-lane pattern — never a
    synthetic id), and ``organization_id`` is the ONE organization the key is
    bound to; the middleware admits it as the request organization.
    """

    user_id: str
    organization_id: str
    key_id: str | None = None
    key_name: str | None = None
    #: ``service`` — the key IS its own minted service identity, bound to ONE organization
    #: (``X-Organization-Id`` must equal it). ``personal`` — the key IS the person who made it
    #: (TABLE-API-1, 2026-09-29): ``organization_id`` is only the organization the key was
    #: deliberately configured to work in, and every request's organization goes through the
    #: SAME membership resolver a signed-in person's does (the header, else that configured
    #: organization), so a lapsed membership is refused on the next request.
    kind: str = "service"
    #: Trusted expiry of the resolved key, in UTC epoch seconds; None means
    #: the key row has no expiry. This is never taken from a request header.
    expires_at: int | None = None


class ApiKeyRefused(Exception):
    """A key that IS one of ours, presented correctly, that no longer works — revoked or expired.

    Raised by the host resolver so the caller is told WHY in words ("This key was revoked 2 hours
    ago"), instead of the generic "sign in" a stranger's token gets. The request still proceeds
    unauthenticated and the route's own gate answers 401 — carrying this sentence
    (``metadata["credential_refused"]``, read by ``require_authenticated``).
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


# Host-injected async callback ``(bearer_token) -> ApiKeyIdentity | None``.
# Receives the FULL ``mx_...`` bearer string; the host owns parsing, the
# hashed-at-rest lookup, constant-time comparison, status/expiry checks, and
# caching. Returning None (or raising) rejects the credential — the request
# proceeds anonymously and the route's own auth requirement produces the 401.
ApiKeyResolver = Callable[[str], Awaitable[ApiKeyIdentity | None]]

# Host-injected ``(ctx) -> async context manager | None``, entered around the
# WHOLE admitted request (HTTP and websocket) once the caller's identity is
# settled. This is the request boundary — the one place that knows WHO is
# calling before any handler runs — so a host uses it to declare, ONCE, the
# provenance every write in the request inherits (a signed-in person is a
# ``human`` actor; an API key is ``code`` named by the key). A handler that
# knows better (an AI writer) nests its own declaration inside and wins.
# Returning None declares nothing for this request (an anonymous caller).
RequestScopeHook = Callable[[AppContext], "AbstractAsyncContextManager[Any] | None"]

# Bearer tokens with this prefix are API keys, never JWTs. ONE Authorization
# header for every credential kind; the middleware disambiguates by shape.
API_KEY_BEARER_PREFIX = "mx_"


# The ONLY paths an authenticated caller may reach with no organization.
# Liveness, the OpenAPI surface, the sign-in flow, and the identity probe a
# client calls BEFORE it can know which organization it acts in. A host adds
# to this via ``organization_exempt_paths``; it never removes the gate.
DEFAULT_ORG_EXEMPT_PATHS: tuple[str, ...] = (
    "/health",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/auth/",
)


def compile_organization_exempt_pattern(entry: str) -> re.Pattern[str]:
    """Compile one EXEMPT ROUTE entry (``organization_exempt_routes``) to an
    exact matcher.

    A host composes these from its own route table (aidream:
    ``Depends(organization_free)`` + ``compose_organization_free_routes``).
    A route entry must match ONE route and nothing else — the ``_paths`` list
    is prefixes, and prefix semantics on a composed ROUTE is a data-isolation
    bug, not an inconvenience: ``/mandates/coverage`` as a prefix silently
    exempted the org-scoped ``/mandates/coverage/states`` it shares a stem
    with, which is how this rule was earned (2026-09-12, caught in composition
    testing before it shipped).

    So a route entry matches ONE path and nothing else:

    * each ``{...}`` consumes exactly one non-empty segment (never a ``/``),
    * the match is anchored at both ends — no prefix semantics, ever, so
      ``/mandates/abc/references/extra`` does NOT match,
    * literal text is escaped, so ``/mandatesX/abc/references`` does NOT match.

    A trailing slash on the entry is ignored, matching the prefix matcher's
    ``rstrip("/")``.
    """
    trimmed = entry.rstrip("/")
    compiled: list[str] = []
    index = 0
    while index < len(trimmed):
        char = trimmed[index]
        if char == "{":
            close = trimmed.find("}", index)
            if close == -1:
                raise ValueError(
                    f"organization-exempt entry {entry!r} has an unclosed '{{' — "
                    "an exempt entry that cannot be compiled must never be "
                    "silently treated as a prefix"
                )
            compiled.append("[^/]+")
            index = close + 1
            continue
        compiled.append(re.escape(char))
        index += 1
    return re.compile("".join(compiled) + r"\Z")


def _matches_organization_exempt(
    path: str,
    prefixes: tuple[str, ...],
    patterns: tuple[re.Pattern[str], ...],
) -> bool:
    """The ONE organization-exemption matching rule.

    ``prefixes`` are segment-bounded prefixes; ``patterns`` are compiled EXACT
    routes. Nothing else matches.
    """
    for prefix in prefixes:
        trimmed = prefix.rstrip("/")
        if not trimmed:
            continue
        if path == trimmed or path.startswith(trimmed + "/"):
            return True
    return any(pattern.match(path) for pattern in patterns)


def is_organization_exempt_path(
    path: str,
    exempt_paths: tuple[str, ...],
    exempt_routes: tuple[str, ...] = (),
) -> bool:
    """Ask the REAL matcher whether ``path`` is exempt.

    For hosts and guard tests: same rule, same code, no middleware instance.
    ``exempt_paths`` are prefixes; ``exempt_routes`` are exact routes.
    """
    return _matches_organization_exempt(
        path,
        tuple(exempt_paths),
        tuple(compile_organization_exempt_pattern(entry) for entry in exempt_routes),
    )


def compile_authenticated_resource_pattern(entry: AuthenticatedResourceRoute) -> re.Pattern[str]:
    """Compile one validated resource-bootstrap declaration as an exact path."""
    parts: list[str] = []
    for segment in entry.path.split("/")[1:]:
        if segment.startswith("{") and segment.endswith("}"):
            parts.append(r"[^/]+")
        else:
            parts.append(re.escape(segment))
    return re.compile(r"/" + "/".join(parts) + r"\Z")


def _unsafe_encoded_path(raw_path: bytes | str | None) -> bool:
    """Refuse encoded separator/normalization paths before exact matching."""
    if raw_path is None:
        return False
    raw = raw_path.decode("ascii", "surrogateescape") if isinstance(raw_path, bytes) else raw_path
    candidate = raw
    for _ in range(4):
        lower = candidate.lower()
        if "%2f" in lower or "%5c" in lower:
            return True
        decoded = unquote(candidate)
        if decoded == candidate:
            break
        candidate = decoded
    return any(segment in {".", ".."} for segment in candidate.split("/"))


def is_authenticated_resource_route(
    method: str,
    path: str,
    declarations: tuple[AuthenticatedResourceRoute, ...],
    *,
    raw_path: bytes | str | None = None,
) -> bool:
    """Match only a declared HTTP method and its exact segment-bounded path."""
    if _unsafe_encoded_path(raw_path):
        return False
    return any(
        entry.method == method and compile_authenticated_resource_pattern(entry).match(path)
        for entry in declarations
    )


class OrganizationNotFound(Exception):
    """Raised by an organization resolver for a well-formed id that names no
    organization.

    It exists so the admission refusal can tell "you are not a member of that
    organization" (ask to be added) apart from "no such organization" (the id
    is wrong or the organization is gone) — two permanent failures with two
    different repairs, which one shared "try again" sentence hid from every
    caller until 2026-09-08 (V-CORRECTNESS F1). A resolver that does not raise
    it simply reports "denied", exactly as before.

    Caught by name in ``_resolve_organization`` BEFORE the generic handler, so
    it is never mistaken for a resolver outage.
    """


class OrganizationArchived(Exception):
    """Raised by an organization resolver for an organization that exists but
    is ARCHIVED.

    An archived organization is closed (ACCESS LADDER T-33, 2026-09-28): its
    members keep their rows so a restore gives everything back, but membership
    reaches nothing inside it — the database's ``iam.has_org_access_for`` joins
    ``archived_at is null``. Admission states the same rule so a request never
    gets past the front door into an organization the database will refuse.
    The repair is neither "ask to be added" nor "pick again": it is "restore
    the organization", so it is its own situation with its own sentence.

    Caught by name BEFORE the generic handler and before the admin lane: an
    archived organization admits no request, a platform admin's included.
    """


class ApiKeyOrganizationMismatch(Exception):
    """Raised when ``X-Organization-Id`` disagrees with the API key's bound
    organization. The middleware answers 409, mirroring
    ``require_organization_context`` — an API key is unambiguous about its
    org, so a contradicting header is a caller bug, never a scope choice."""

    def __init__(self, claimed: str, admitted: str) -> None:
        self.claimed = claimed
        self.admitted = admitted
        super().__init__(f"X-Organization-Id {claimed!r} != API key organization {admitted!r}")
AdminResolver = Callable[[str], Awaitable[bool]]
# Resolves the caller's admin TIER (admin.admins.level) → the level string
# ("super_admin" | "senior_admin" | "developer") or None for a non-admin.
# Preferred over AdminResolver: is_admin is derived as ``level is not None``, and
# the tier is carried onto AppContext.admin_level. A host that only supplies the
# boolean AdminResolver still works (admin_level stays None).
AdminLevelResolver = Callable[[str], Awaitable[str | None]]
# Callback signature: ``(user_id, claimed_org_id) -> verified_org_id | None``.
# Returning None means "the claimed org is not valid for this user; fall back
# to personal scope".  When the host does not supply a resolver, the
# middleware trusts the claim as-is (acceptable for dev; production hosts
# should always inject a resolver that consults iam.memberships).
OrgResolver = Callable[[str, str | None], Awaitable[str | None]]
# THE ADMIN LANE (Arman, 2026-09-25/26: admin keeps full access inside the
# admin apps only; "no one acts as themselves in admin"). Signature:
# ``(user_id, claimed_org_id) -> bool``. Consulted ONLY when the membership
# resolver refused a claimed organization AND the request carries
# ``x-matrx-admin-lane: 1``. The HOST decides — it must verify the caller as a
# platform admin against its canonical admin registry (never the header, never
# the token cache) and admit only its own platform tenant, and it records the
# admission in its audit trail. Without the header this is never called, so
# admission is byte-for-byte unchanged.
AdminLaneAdmission = Callable[[str, str], Awaitable[bool]]
ADMIN_LANE_HEADER = "x-matrx-admin-lane"
# THE RECORD-GRANT LANE (W-66, 2026-10-01). Signature:
# ``(user_id, claimed_org_id, method, path) -> bool``. Sharing works at every
# level and access never depends on membership (access ladder): a person given
# a record by share may act ON THAT RECORD, in the record's own organization,
# without being a member of it. Consulted ONLY for an HTTP request whose
# membership admission refused the claimed organization and that the admin lane
# did not admit. The HOST decides, narrowly: it recognizes the exact record
# routes it serves (never a prefix, never "any route"), verifies the caller's
# grant on THAT record through its canonical access function, and admits only
# when the claimed organization IS the record's own organization. A path with
# an encoded separator or dot segment never reaches the hook. Without a hook
# this is never called and admission is byte-for-byte unchanged. A hook that
# raises is "unverifiable" (503), never an admission.
RecordGrantAdmission = Callable[[str, str, str, str], Awaitable[bool]]


class AdminLaneAuditUnavailable(Exception):
    """Raised by a host ``admin_lane_admission`` hook that VERIFIED the admin but
    could not write the audit record it requires. The admission is refused (no
    unaudited admission), and the refusal says so in plain words — never "you are
    not a member", which would be a lie about an admin whose access is fine."""


#: Why an admin-lane admission could not be DECIDED (as opposed to refused).
#: Carried on ``ctx.metadata[ADMISSION_FAILURE_KEY]`` beside
#: ``organization_admission="unverifiable"`` so the refusal names the real cause.
ADMISSION_FAILURE_KEY = "organization_admission_failure"
ADMIN_LANE_AUDIT_UNAVAILABLE = "admin_lane_audit_unavailable"
ADMIN_LANE_UNVERIFIABLE = "admin_lane_unverifiable"
_ADMIN_LANE_FAILURES = frozenset({ADMIN_LANE_AUDIT_UNAVAILABLE, ADMIN_LANE_UNVERIFIABLE})


def _admission_failure(ctx: AppContext) -> str | None:
    metadata = ctx.metadata if isinstance(getattr(ctx, "metadata", None), dict) else {}
    failure = metadata.get(ADMISSION_FAILURE_KEY)
    return failure if failure in _ADMIN_LANE_FAILURES else None
JWKS_REFRESH_COOLDOWN_SECONDS = 30.0

# Burst-window for the file-session-cookie drift detector: within this window,
# repeated CRITICAL alarms for the same (process, reason) are counted, not
# logged — the next alarm after the window carries the suppressed count. Keeps
# a broken fleet (EVERY private render mismatching) from flooding the logs
# while guaranteeing the signal recurs until fixed.
COOKIE_DRIFT_LOG_WINDOW_SECONDS = 300.0


@dataclass(frozen=True)
class VerifiedToken:
    """Result of verifying a Supabase JWT — identity + admin status, no
    transport coupling. Returned by ``AuthMiddleware.verify_token_raw`` so the
    HTTP middleware and out-of-band resource servers (e.g. the MCP OAuth
    TokenVerifier) share one verification primitive instead of re-deriving the
    crypto, JWKS client, token cache, and admin resolver."""

    user_id: str
    is_admin: bool
    email: str | None
    claims: dict[str, Any]
    token: str
    # Admin tier ("super_admin" | "senior_admin" | "developer") or None for a
    # non-admin. is_admin == (admin_level is not None).
    admin_level: str | None = None
    # Transport-neutral JWT lifecycle metadata. Resource-server adapters must
    # not re-decode the raw token merely to recover these verified claims.
    expires_at: int | None = None
    issuer: str | None = None
    session_decision: CurrentSessionDecision | None = None


_READ_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})


class AuthMiddleware:
    """Pure ASGI auth middleware with pluggable guest and admin resolution.

    Parameters
    ----------
    app : ASGIApp
        The next ASGI app in the stack.
    jwt_secret : str
        Secret for decoding Supabase JWTs.
    admin_token : str
        Ignored compatibility argument; static admin-token authentication is forbidden.
    admin_user_id : str
        Ignored compatibility argument; it grants no identity or admin authority.
    resolve_guest : GuestResolver | None
        Async callback ``(fingerprint, ip, user_agent) -> user_id`` for
        fingerprint-based auth. If None, the host has NO guest lane: a
        fingerprint header is ignored for identity and the request stays
        anonymous (it never becomes a user id).
    is_admin_resolver : AdminResolver | None
        Async callback ``(user_id) -> bool`` that checks the DB admins table.
        Called for every JWT-authenticated request. ORM-level caching means
        this is effectively free after the first hit per user.
    resolve_active_organization : OrgResolver | None
        Async callback ``(user_id, claimed_org_id) -> verified_org_id | None``
        that confirms the caller is a member of the claimed organization.
        Sources for ``claimed_org_id`` (highest priority first):
          1. ``X-Organization-Id`` request header.
          2. ``organization_id`` / ``org_id`` claim on the JWT.
        If the resolver returns None (or no resolver is provided and no
        claim is present), the request stays in personal scope.
    quiet_paths : tuple[str, ...]
        Path prefixes for which the verbose ``[AuthMiddleware] Request`` log
        block is suppressed. The auth resolution still runs normally; only
        the per-request console print is skipped. Use for noisy probes like
        ``("/health",)``.
    token_cache_ttl_seconds : float
        TTL for the per-token validation cache. On a cache hit the JWT
        decode AND the admin-DB lookup are both skipped — only the cheap
        SHA256(token) lookup and an ``AppContext.with_overrides`` call run.
        Bounded staleness is intentional: a token revoked mid-window is
        accepted for at most this many seconds; an admin flag change has the
        same lag. Defaults to 5.0s, which collapses the burst of HTTP Range
        requests pdf.js fires for a single document open (5–6 hits within
        ~200ms) down to one real validation. Set to 0 to disable caching.
    token_cache_max_size : int
        Maximum number of cached token entries. Bounds memory in case of a
        large burst of distinct tokens. Defaults to 1024 — well above the
        per-worker active-token count under realistic load and small enough
        to fit comfortably in memory.
    """

    def __init__(
        self,
        app: ASGIApp,
        *,
        jwt_secret: str = "",
        jwks_url: str | None = None,
        jwt_algorithms: tuple[str, ...] = ("HS256",),
        resolve_guest: GuestResolver | None = None,
        # Optional read-only companion to ``resolve_guest``: ``(fingerprint) ->
        # bool`` "does this fingerprint already own an identity?". When given,
        # a READ request (GET/HEAD/OPTIONS) from a fingerprint with NO identity
        # yet stays anonymous instead of minting an account — accounts are
        # created only by a request that does something (POST/PUT/PATCH/DELETE).
        has_guest_identity: Callable[[str], Awaitable[bool]] | None = None,
        # Optional ``(method, path, query_string) -> bool``: True when this request is
        # INCIDENTAL (a signing-link page open, a token mint that needs a real user, a
        # stateless utility). Such a request is treated like a READ: a fingerprint that
        # already owns an identity resolves as usual, one that does not stays
        # anonymous. Only takes effect together with ``has_guest_identity``.
        guest_mint_exempt: Callable[[str, str, str], bool] | None = None,
        resolve_api_key: ApiKeyResolver | None = None,
        is_admin_resolver: AdminResolver | None = None,
        admin_level_resolver: AdminLevelResolver | None = None,
        resolve_active_organization: OrgResolver | None = None,
        # See ``AdminLaneAdmission``. None = there is no admin lane on this host.
        admin_lane_admission: AdminLaneAdmission | None = None,
        # See ``RecordGrantAdmission``. None = no record-grant lane on this host.
        record_grant_admission: RecordGrantAdmission | None = None,
        # The longest a request waits for the membership lookup. Past it the
        # request is answered 503 "could not verify your organization" instead
        # of hanging behind a database that stopped answering (2026-09-25:
        # files.matrxserver.com requests hung 30–45 s, then forever). The
        # shared lookup keeps running; only this caller stops waiting.
        organization_resolve_timeout: float = 5.0,
        jwt_audience: str | None = "authenticated",
        guest_fingerprint_secret: str = "",
        quiet_paths: tuple[str, ...] = (),
        # Paths an AUTHENTICATED caller may reach without an organization —
        # liveness, the sign-in surface, and the identity probe a client uses
        # BEFORE it can know its organization. Prefix match. Every entry is a
        # hole in the admission contract, so a host declares its own list
        # explicitly and keeps it short enough to read aloud.
        organization_exempt_paths: tuple[str, ...] = DEFAULT_ORG_EXEMPT_PATHS,
        # EXACT route paths — one entry exempts exactly one route, parameters
        # (``{id}``) allowed, NEVER a prefix. This is what a host composes from
        # its own route table, so a route can be exempt while the siblings
        # sharing its stem stay gated. Prefixes live in the list above.
        organization_exempt_routes: tuple[str, ...] = (),
        # Exact method/path declarations whose handler performs typed
        # resource authorization after normal authentication.  This is a
        # distinct, authenticated bootstrap lane — never organization-free.
        authenticated_resource_routes: tuple[AuthenticatedResourceRoute, ...] = (),
        # Entered around every ADMITTED request after identity is settled —
        # see ``RequestScopeHook``. The host declares request-wide facts here
        # (actor provenance above all); no route has to remember to.
        request_scope: RequestScopeHook | None = None,
        log_requests: bool = True,
        resolve_current_session: Callable[[VerifiedToken], Awaitable[bool | CurrentSessionDecision]] | None = None,
        resolve_file_session: Callable[[FileSessionCredential], Awaitable[bool]] | None = None,
        require_file_session_source: bool = False,
        session_resolve_timeout: float = DEFAULT_SESSION_ATTEMPT_SECONDS,
        token_cache_ttl_seconds: float = 5.0,
        token_cache_max_size: int = 1024,
        # First-party token issuers whose JWTs are NOT user-login tokens and
        # are verified per-route instead (scoped capability tokens — see
        # ``matrx_connect.scoped_tokens``). A bearer whose unverified ``iss``
        # matches falls through this middleware SILENTLY (anonymous context,
        # no ERROR log); the route that owns the audience verifies it
        # explicitly. This is a log-noise/fall-through control only — it
        # never grants anything.
        passthrough_issuers: tuple[str, ...] = (),
        # Removed in 2026-05: `admin_token` / `admin_user_id` static escape
        # hatch is no longer accepted. For local dev / agent auth, the host
        # exposes a dev-login endpoint that mints real Supabase JWTs. Leave
        # the kwargs accepted-but-ignored for one release so unrelated
        # callers don't crash on import; they emit a loud warning.
        admin_token: str | None = None,
        admin_user_id: str | None = None,
    ) -> None:
        if admin_token or admin_user_id:
            import sys as _sys

            print(
                "[matrx-connect AuthMiddleware] admin_token / admin_user_id "
                "are no longer accepted — drop them from your AuthMiddleware "
                "wiring. Use a Supabase JWT (real user login or dev-login "
                "endpoint) instead.",
                file=_sys.stderr,
            )
        self.app = app
        # JWKS WINS. A host that can fetch the issuer's public keys has no need
        # of a shared secret, and keeping one around is not free: the key is
        # chosen from the TOKEN's own `alg` header, so any HS256 secret present
        # is a second, independent way to authenticate as anyone.
        #
        # That is not hypothetical. On 2026-08-22 every Matrx server was found
        # holding the RETIRED Supabase project's JWT secret (never rotated at
        # the migration), which made a decommissioned project's key a trusted
        # signing key for production auth — confirmed live against
        # /auth/whoami. Real logins were unaffected the whole time, because they
        # are ES256 through JWKS, which is exactly why nobody noticed.
        #
        # So: if we can verify asymmetrically, we ONLY verify asymmetrically.
        # A stale or wrong secret in some env file cannot grant anything.
        if jwks_url and jwt_secret:
            import sys as _sys

            print(
                "[matrx-connect AuthMiddleware] jwks_url is set, so the HS256 "
                "jwt_secret is IGNORED — asymmetric verification is the only "
                "accepted path. Remove the secret from this host's environment.",
                file=_sys.stderr,
            )
            jwt_secret = ""
        self._jwt_secret = jwt_secret
        self._request_scope = request_scope
        # JWKS support — when ``jwks_url`` is set, asymmetric tokens
        # (RS256/ES256) are validated by fetching the signing key from
        # the JWKS document. The PyJWKClient caches keys in-process and
        # transparently refreshes on unknown ``kid``. Hosts that use
        # Supabase's asymmetric JWT signing must set this; hosts on
        # legacy HS256 shared-secret signing leave it at None.
        #
        # ``jwt_algorithms`` is the algorithm allow-list passed to
        # jwt.decode(). Default is HS256-only for backwards compat. To
        # accept asymmetric tokens, callers pass e.g.
        # ``jwt_algorithms=("RS256", "ES256")``. When JWKS is configured,
        # HS256 remains rejected even if a stale allow-list entry survives.
        self._jwks_url = jwks_url or None
        self._jwt_algorithms = tuple(jwt_algorithms) or ("HS256",)
        self._passthrough_issuers = frozenset(i for i in passthrough_issuers if i)
        self._jwks_client = None  # lazily built on first asymmetric token
        self._resolve_guest = resolve_guest
        self._has_guest_identity = has_guest_identity
        self._guest_mint_exempt = guest_mint_exempt
        self._resolve_api_key = resolve_api_key
        self._is_admin_resolver = is_admin_resolver
        # When supplied, this resolves the admin TIER and takes precedence over
        # is_admin_resolver (is_admin is derived from it). See AdminLevelResolver.
        self._admin_level_resolver = admin_level_resolver
        self._resolve_active_organization = resolve_active_organization
        self._admin_lane_admission = admin_lane_admission
        self._record_grant_admission = record_grant_admission
        self._organization_resolve_timeout = float(organization_resolve_timeout)
        self._jwt_audience = jwt_audience or None
        self._quiet_paths = tuple(quiet_paths)
        self._organization_exempt_paths = tuple(organization_exempt_paths)
        self._organization_exempt_routes = tuple(organization_exempt_routes)
        # The two kinds are split ONCE, here, by which list they came from —
        # never by inspecting the string. That is what keeps a composed route
        # from ever acquiring prefix semantics by accident.
        self._organization_exempt_patterns = tuple(
            compile_organization_exempt_pattern(entry)
            for entry in self._organization_exempt_routes
        )
        self._authenticated_resource_routes = tuple(authenticated_resource_routes)
        if any(type(entry) is not AuthenticatedResourceRoute for entry in self._authenticated_resource_routes):
            raise ValueError("authenticated_resource_routes must contain AuthenticatedResourceRoute entries")
        # When the host already logs every incoming request (e.g. aidream's
        # RequestLogMiddleware), the per-request ``[AUTH][INFO] Request`` block
        # is a redundant duplicate. Hosts disable it via ``log_requests=False``;
        # the auth-outcome lines (``JWT accepted`` / ``Admin confirmed``) are
        # unaffected. Standalone consumers keep it on by default.
        self._log_requests = bool(log_requests)
        # HMAC secret used to sign + verify the guest_fingerprint cookie.
        # Empty in dev → an ephemeral random secret is generated at first
        # use, which invalidates all guest sessions on restart.
        #
        # ``secret_is_ephemeral`` is the honesty flag: True means this process
        # invented its own secret, so cookies it mints die on every OTHER
        # process/container and at the next restart. It is registered beside
        # the secret so the /files/session mint response can carry
        # ``secret_source`` and clients can scream instead of failing silently.
        self.secret_is_ephemeral: bool = not guest_fingerprint_secret
        if not guest_fingerprint_secret:
            import secrets

            # 🚨 Per-PROCESS secret: guest fingerprints and mx_files_session
            # cookies minted here are invalid in every OTHER process/container
            # and after every restart. Acceptable for a single dev process
            # only — in any multi-instance deployment this breaks all private
            # file renders (the 2026-08-30 production outage). Hosts must
            # inject a stable value.
            import logging

            logging.getLogger("matrx_connect.auth").warning(
                "AuthMiddleware: no guest_fingerprint_secret injected — using "
                "an EPHEMERAL per-process secret. Fingerprint + file-session "
                "cookies will not survive restarts and will FAIL across "
                "multiple instances. Inject a stable secret."
            )
            guest_fingerprint_secret = secrets.token_urlsafe(48)
        self._guest_fp_secret = guest_fingerprint_secret.encode("utf-8")
        # The browser file-session cookie (durable private render lane) signs
        # with the same server secret, domain-separated. Register it so the
        # POST /files/session mint route can sign without a second secret.
        from .session_cookie import register_session_cookie_secret

        register_session_cookie_secret(
            self._guest_fp_secret, ephemeral=self.secret_is_ephemeral
        )
        # Drift-detector rate-limit state: reason -> (last_emit_monotonic,
        # suppressed_since_last_emit). See _report_cookie_drift.
        self._drift_log_state: dict[str, tuple[float, int]] = {}
        # Short-lived in-memory cache: SHA256(token) -> validation result.
        # Skips JWT decode + admin DB lookup for repeat hits within
        # ``_token_cache_ttl`` seconds. Negative or zero TTL disables it.
        self._resolve_current_session = resolve_current_session
        self._resolve_file_session = resolve_file_session
        self._require_file_session_source = require_file_session_source or resolve_file_session is not None
        self._session_resolve_timeout = max(0.001, session_resolve_timeout)
        # A resolver that asks a remote authority declares how long one try needs (its own deadline
        # plus headroom); the outer attempt never cuts it short of that (2026-10-21, Files at 3 s vs
        # aidream's 5 s attempts).
        for resolver in (resolve_current_session, resolve_file_session):
            needed = getattr(resolver, "attempt_seconds", None)
            if isinstance(needed, (int, float)) and not isinstance(needed, bool) and needed > self._session_resolve_timeout:
                self._session_resolve_timeout = float(needed)
        self._token_cache_ttl: float = max(0.0, float(token_cache_ttl_seconds))
        self._token_cache_max_size: int = max(0, int(token_cache_max_size))
        # value layout: cache expiry, identity, claims, and verified JWT
        # lifecycle metadata used by out-of-band resource servers.
        self._token_cache: dict[
            str,
            tuple[
                float,
                str,
                bool,
                str | None,
                dict[str, Any],
                str | None,
                int | None,
                str | None,
            ],
        ] = {}
        self._token_flights: AsyncSingleFlight[str, VerifiedToken | None] = AsyncSingleFlight()
        self._org_flights: AsyncSingleFlight[tuple[str, str | None], str | None] = (
            AsyncSingleFlight()
        )
        self._jwks_flights: AsyncSingleFlight[str, object] = AsyncSingleFlight()
        # Current login / file-session source checks: shared only by callers who all asked
        # before the lookup started (authority_retry.FreshFlight) — never a cached answer.
        self._session_flights: FreshFlight[str, object] = FreshFlight()
        self._jwks_lookup_lock = asyncio.Lock()
        self._jwks_keys: dict[str, object] = {}
        self._jwks_last_refresh = 0.0

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        if scope["type"] == "websocket":
            await self._admit_websocket(scope, receive, send)
            return

        request = Request(scope, receive)

        from matrx_connect.chat_timing import clear_inbound_stamp, stamp_inbound_request
        from matrx_connect.request_latency import arm_request_latency

        from matrx_connect.chat_timing import arm_chat_timing

        stamp_inbound_request(path=request.url.path)
        arm_request_latency(path=request.url.path, headers=request.headers)
        arm_chat_timing(path=request.url.path)

        raw_auth: str | None = request.headers.get("authorization")
        redacted_auth: str | None = None
        if raw_auth:
            parts = raw_auth.split(None, 1)
            if len(parts) == 2:
                scheme, tok = parts
                redacted_auth = (
                    f"{scheme} {tok[:6]}...{tok[-4:]}" if len(tok) > 10 else f"{scheme} [redacted]"
                )
            else:
                redacted_auth = "[redacted]"

        # Both header names are accepted; X-Fingerprint-ID is the canonical
        # one in aidream and X-Guest-Fingerprint is accepted as an alias so
        # cloud_files frontends can use the more descriptive name.
        fingerprint_in = request.headers.get("x-fingerprint-id") or request.headers.get(
            "x-guest-fingerprint"
        )

        # Never log the raw fingerprint (it's an unauthenticated identity
        # claim). Log a short prefix-hash for correlation only.
        import hashlib

        fp_redacted: str | None = None
        if fingerprint_in:
            fp_redacted = "fp:" + hashlib.sha256(fingerprint_in.encode("utf-8")).hexdigest()[:12]

        if self._log_requests and not any(
            request.url.path.startswith(p) for p in self._quiet_paths
        ):
            vcprint(
                {
                    "method": request.method,
                    "path": request.url.path,
                    "query": str(request.url.query) or None,
                    "client": client_ip(request),
                    "authorization": redacted_auth,
                    "fingerprint_id": fp_redacted,
                },
                title="[AUTH][INFO] Request",
                color="blue",
                log_level="INFO",
            )

        try:
            ctx = await self._build_context(request)
        except CredentialAuthorityUnavailable as error:
            await credential_unavailable_response(error)(scope, receive, send)
            clear_inbound_stamp()
            return
        except ApiKeyOrganizationMismatch:
            from starlette.responses import JSONResponse

            # Mirrors require_organization_context's 409 contract exactly —
            # same status, same error code, same envelope shape.
            response = JSONResponse(
                status_code=409,
                content={
                    "detail": {
                        "error": "organization_context_mismatch",
                        "message": (
                            "X-Organization-Id does not match the organization "
                            "this API key is bound to"
                        ),
                    }
                },
            )
            await response(scope, receive, send)
            clear_inbound_stamp()
            return

        organization_rejection = self._organization_admission_failure(request, ctx)
        if organization_rejection is not None:
            await organization_rejection(scope, receive, send)
            clear_inbound_stamp()
            return

        request.state.context = ctx

        token = set_app_context(ctx)
        # Register this request in the process-wide in-flight registry so that
        # off-loop probes (the event-loop watchdog monitor thread, future
        # stuck-request sweepers) can correlate an anomaly to the request(s)
        # that were live when it fired — the watchdog samples from another
        # thread and otherwise has no access to who/what was running.
        inflight = get_inflight_registry()
        inflight_token = inflight.register(
            method=request.method,
            path=request.url.path,
            request_id=ctx.request_id,
            user_id=ctx.user_id,
        )
        try:
            async with self._request_scoped(ctx):
                await self.app(scope, receive, send)
        finally:
            inflight.unregister(inflight_token)
            clear_app_context(token)
            clear_inbound_stamp()

    def _is_organization_exempt(self, path: str) -> bool:
        """Match an exemption at a SEGMENT boundary, never as raw text.

        A bare ``startswith`` made ``/health`` exempt ``/healthcare/patients``:
        an exemption list that silently widens itself is worse than no list,
        because it reads as narrow. A plain entry matches the path exactly, or
        the path continues with ``/``; a ``{parameter}`` entry matches ONE
        route exactly and is never a prefix.

        The matching RULE lives in ``_matches_organization_exempt`` so the
        module-level ``is_organization_exempt_path`` (what hosts and guard
        tests ask) can never drift from what the request path actually does.
        """
        return _matches_organization_exempt(
            path,
            self._organization_exempt_paths,
            self._organization_exempt_patterns,
        )

    def _is_authenticated_resource_route(self, request: Request) -> bool:
        return is_authenticated_resource_route(
            request.method,
            request.url.path,
            self._authenticated_resource_routes,
            raw_path=request.scope.get("raw_path"),
        )

    def _organization_admission_reason(
        self, request: Request | HTTPConnection, ctx: AppContext
    ) -> str | None:
        """The one rule: identity present + no organization + not exempt.

        Shared by the HTTP path (``_organization_admission_failure``, which
        wraps this in a 400 JSON response) and the WebSocket path
        (``_admit_websocket``, which wraps this in an ASGI ``websocket.close``)
        so there is exactly one place the admission RULE is stated — only the
        transport-specific refusal shape differs.

        Returns a short machine reason string, or None to admit the request.
        """
        if not getattr(ctx, "user_id", None):
            # No identity at all — the route's own auth requirement answers
            # this with a 401 (or, for WS, its own handshake refusal).
            # Telling an anonymous caller "organization required" would send
            # them to fix the wrong thing.
            return None
        if getattr(ctx, "auth_type", None) in ("fingerprint", "cookie"):
            # Lanes that CANNOT name an organization are admitted, not gated.
            # A fingerprint guest has no iam.memberships row to verify — guest
            # work is guest-scoped by construction, and demanding a header
            # they can never legitimately send turns every anonymous surface
            # into a 400. The file-session cookie lane is stricter still: it
            # authenticates <img>/<video> byte GETs, and a browser tag cannot
            # attach ANY header — gating it silently killed every private
            # media render. The organization admission rule is for callers
            # with tenant membership (JWT / API key), who can and must state
            # the organization they act in.
            return None
        if getattr(ctx, "organization_id", None):
            return None
        if isinstance(request, Request) and self._is_authenticated_resource_route(request):
            return None
        if self._is_organization_exempt(request.url.path):
            return None
        # The machine reason NAMES the situation. It used to be the single
        # string "organization_required" for four different worlds, which is
        # what made the sentence below wrong in three of them.
        failure = _admission_failure(ctx)
        if failure and getattr(ctx, "organization_admission", None) == "unverifiable":
            return failure
        return _ADMISSION_REASON_CODES.get(
            getattr(ctx, "organization_admission", "none") or "none",
            "organization_required",
        )

    @staticmethod
    def _organization_admission_words(ctx: AppContext) -> tuple[str, str, str]:
        """(code, message, user_message) for THIS request's admission failure.

        🚨 V-CORRECTNESS F1 (2026-09-07). One sentence answered four different
        situations: no header at all, a real organization the caller is not in,
        an id for no organization, and a value that is not an id. Three of the
        four were told "This request carried an identity but no organization …
        Choose the organization you're working in" — advice that is
        unactionable for somebody who DID choose one — and a permanent
        non-membership was told to "try again" exactly like a transient
        resolver outage. The information to say the right thing was already on
        the context: this campaign added `organization_admission` and
        `claimed_organization_id` and then never read either. This is the read.

        Every sentence names what is wrong AND what to do about it, and the
        `user_message` is the one a person sees — never the generic fallback.
        """
        admission = getattr(ctx, "organization_admission", "none") or "none"
        claimed = getattr(ctx, "claimed_organization_id", None)
        # The id itself rides the envelope's `claimed_organization_id`, never the sentence: a
        # message is words a person reads (TABLE-API-1 / VERIFIER-31 D2).
        named = "the organization in X-Organization-Id" if claimed else "an organization"

        if admission == "denied":
            return (
                "organization_forbidden",
                f"This request named {named} and you are not a member of it. "
                "Membership is checked on every request and is never inferred; "
                "nothing here is retryable until it changes.",
                "You are not a member of that organization, so this cannot run in "
                "it. Switch to an organization you belong to, or ask one of its "
                "administrators to add you.",
            )
        if admission == "unknown":
            return (
                "organization_not_found",
                f"This request named {named}, and no such organization exists.",
                "That organization doesn't exist — it may have been deleted, or the "
                "link you followed is out of date. Pick your organization again.",
            )
        if admission == "archived":
            return (
                "organization_archived",
                f"This request named {named}, and that organization is archived. "
                "An archived organization admits no request until its owner "
                "restores it; nothing is retryable until then.",
                "That organization is archived. Restore it to keep working in it, "
                "or switch to another organization.",
            )
        if admission == "malformed":
            return (
                "organization_id_invalid",
                "The X-Organization-Id this request sent is not an organization id. "
                "Nothing was looked up.",
                "The organization this request named isn't a valid one. Reload the "
                "page and choose your organization again.",
            )
        failure = _admission_failure(ctx) if admission == "unverifiable" else None
        if failure == ADMIN_LANE_AUDIT_UNAVAILABLE:
            return (
                ADMIN_LANE_AUDIT_UNAVAILABLE,
                f"Your platform-admin access to {named} was verified, but the admin "
                "audit log could not record this admission, and admin work never runs "
                "unrecorded, so it was refused. Your membership and access are not the "
                "problem; the audit log is.",
                "The admin audit log is unavailable right now. Your admin access is "
                "fine, but admin work is never done without a record, and the record "
                "could not be written. Try again in a moment; if it keeps happening, "
                "tell support the admin audit log is failing.",
            )
        if failure == ADMIN_LANE_UNVERIFIABLE:
            return (
                ADMIN_LANE_UNVERIFIABLE,
                f"This request asked to act in {named} as a platform admin, and the "
                "platform could not confirm your admin access (the admin check "
                "failed). Nothing was decided about you.",
                "We couldn't confirm your admin access just now. This is on us, not "
                "on you. Try again in a moment; if it keeps happening, tell support "
                "the admin access check is failing.",
            )
        if admission == "unverifiable":
            return (
                "organization_unverifiable",
                f"This request named {named} and the platform could not verify your "
                "membership (the membership lookup failed). It is NOT demoted to "
                "no-organization: resolving anyway would silently run in a different "
                "scope than the one you asked for.",
                "We couldn't confirm your organization just now — this is on us, not "
                "on you. Try again in a moment; if it keeps happening, tell support "
                "the membership lookup is failing.",
            )
        return (
            "organization_required",
            "This request carried an identity but no organization. Send the "
            "X-Organization-Id header naming the organization you are acting "
            "in; the server verifies your membership and never chooses one "
            "for you.",
            "Choose the organization you're working in, then try again.",
        )

    def _organization_admission_failure(self, request: Request, ctx: AppContext):
        """Refuse an authenticated request that names no organization.

        Identity has always been undeniable on this platform because it is
        resolved HERE, at the top, and nothing routes without it. Organization
        was not: it was resolved only when a caller happened to send one, and
        each route was left to invent its own late check — which is why the
        same missing organization surfaced as a 400 deep inside one feature, a
        silently mis-tenanted write in the next, and nothing at all in a third.

        An organization is a per-request fact, exactly like the bearer token,
        and it is admitted on the same line. A request carrying an identity but
        no organization does not reach feature code.

        It is deliberately NOT resolved for the caller here: a server that
        picks an organization when the caller forgot one is how work lands in
        the wrong tenant (see common-docs/systems/architecture/database/projects/no-db-assigned-org/PLAN.md). The
        caller states it; the middleware verifies membership; nobody guesses.

        Returns a Starlette response to send, or None to admit the request.
        """
        if self._organization_admission_reason(request, ctx) is None:
            return None
        path = request.url.path

        from starlette.responses import JSONResponse

        code, message, user_message = self._organization_admission_words(ctx)

        vcprint(
            f"[AUTH][REJECT] {request.method} {path} — {code} "
            f"(user={ctx.user_id}, claimed="
            f"{getattr(ctx, 'claimed_organization_id', None)})",
            color="yellow",
            # This is an intentional 400 caller denial, not an application
            # failure.  ERROR feeds the production repair safety net and
            # turns normal control flow into a false incident family.
            log_level="WARNING",
        )
        # 🚨 THE REASON MUST BE WHERE A CLIENT READS IT (2026-09-14).
        #
        # `require_organization_context` raises `HTTPException(400, detail={...})`
        # and the app's error handler HOISTS that detail dict's keys to the
        # ROOT of the response — `{error, message, user_message, details,
        # request_id, ...extras}`. This middleware sits ABOVE the exception
        # handlers, so it builds its own response; it used to build the
        # PRE-hoist shape, `{"detail": {...}}`, and called that "the same
        # envelope". It is not the same WIRE shape, and a client reading
        # `body.user_message` / `body.message` off the root found neither:
        # every organization admission refusal arrived at a person as "The
        # server refused this request and sent no reason with it" — the exact
        # sentence matrx-frontend prints when a body carries no readable
        # reason (GET /seo/brands/{id}/strategy for a brand in another org,
        # ops.app_log 2026-09-14 22:48). The words were always computed; they
        # simply never reached the screen.
        #
        # So the envelope is emitted HOISTED, matching what the error handler
        # produces for the identical refusal raised from a route. The STATUS
        # stays 400 for every shape: it is the same admission gate and existing
        # clients branch on it. `code` still says which of the five situations
        # this is, so a client can retry the retryable one and only that one.
        #
        # EXCEPT `unverifiable` (2026-09-25): that is not the caller's mistake,
        # it is the server failing to look the membership up. A 400 tells the
        # client "your request is wrong, do not retry"; 503 + Retry-After is
        # the honest status. No client branched on 400 for this code.
        # The admin-lane failures ride the same marker: the server could not
        # decide, so they are 503 + Retry-After too, with their own words.
        unverifiable = getattr(ctx, "organization_admission", None) == "unverifiable"
        return JSONResponse(
            status_code=503 if unverifiable else 400,
            headers={"Retry-After": "5"} if unverifiable else None,
            content={
                "error": code,
                "code": code,
                "message": message,
                "user_message": user_message,
                "details": None,
                "organization_admission": getattr(ctx, "organization_admission", "none"),
                "claimed_organization_id": getattr(ctx, "claimed_organization_id", None),
                "request_id": getattr(ctx, "request_id", None) or "",
            },
        )

    async def _admit_websocket(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Give the WebSocket lane the SAME identity + organization admission
        as the HTTP lane, instead of the no-op early return this branch used
        to be (it built no ``AppContext`` at all — no identity check, no
        organization check, for ANY WebSocket connection, on every host).

        Admission is based on whatever the handshake itself carries: a
        ``Authorization`` bearer token, an ``mx_...`` API key, a guest
        fingerprint header, or ``X-Organization-Id`` — exactly the lanes
        ``_build_context`` already resolves for HTTP, reused here via a bare
        ``HTTPConnection`` (headers/cookies/query only; nothing here ever
        calls ``receive()`` for a message body).

        * No identity at handshake → admitted through unchanged. Several WS
          endpoints (e.g. google_specialized's realtime sockets) authenticate
          via a message sent AFTER ``websocket.accept()``, which this gate
          cannot see — that is each handler's OWN admission to make, and nothing
          here removes the need for it. This gate only closes the lane for
          identity carried at handshake time.
        * Identity present, verified organization present, or the path is
          exempt → admitted.
        * Identity present, no organization, not exempt → refused: the
          connection is closed at handshake with a clear reason, never handed
          to the app and never left to hang.
        """
        connection = HTTPConnection(scope, receive)

        try:
            ctx = await self._build_context(connection)
        except CredentialAuthorityUnavailable as error:
            await self._close_websocket_handshake(
                receive, send, code=1013, reason=error.code
            )
            return
        except ApiKeyOrganizationMismatch:
            await self._close_websocket_handshake(
                receive, send, code=4409, reason="organization_context_mismatch"
            )
            return

        reason = self._organization_admission_reason(connection, ctx)
        if reason is not None:
            vcprint(
                f"[AUTH][REJECT] WS {scope.get('path')} — {reason} (user={ctx.user_id}, "
                f"claimed={getattr(ctx, 'claimed_organization_id', None)})",
                color="yellow",
                # Same expected caller denial as the HTTP 400 above.
                log_level="WARNING",
            )
            # The close reason is the only channel a handshake refusal has, so
            # it carries the SAME code the HTTP lane returns — a socket closed
            # with "organization_required" when the truth is "you are not a
            # member" is the F1 defect wearing a different transport.
            await self._close_websocket_handshake(receive, send, code=4400, reason=reason)
            return

        scope.setdefault("state", {})
        scope["state"]["context"] = ctx

        token = set_app_context(ctx)
        try:
            async with self._request_scoped(ctx):
                await self.app(scope, receive, send)
        finally:
            clear_app_context(token)

    def _is_incidental_request(self, request: Request | HTTPConnection) -> bool:
        if self._guest_mint_exempt is None:
            return False
        url = request.url
        return bool(
            self._guest_mint_exempt(
                getattr(request, "method", "POST"), url.path, url.query or ""
            )
        )

    @asynccontextmanager
    async def _request_scoped(self, ctx: AppContext) -> AsyncIterator[None]:
        """The host's request-wide declaration for this admitted caller.

        Entered INSIDE the app-context ContextVar and in the request's own
        task, so anything the hook declares through a ContextVar is visible to
        every handler, dependency and ORM call the request makes — and gone
        the moment the request ends. A hook that returns None, or no hook at
        all, is a no-op scope: matrx-connect standalone declares nothing.
        """
        cm = self._request_scope(ctx) if self._request_scope is not None else None
        if cm is None:
            yield
            return
        async with cm:
            yield

    @staticmethod
    async def _close_websocket_handshake(
        receive: Receive, send: Send, *, code: int, reason: str
    ) -> None:
        """Refuse a WebSocket at handshake, per ASGI: the server's first
        event to the app is ``websocket.connect``; the app answers with
        either ``websocket.accept`` or ``websocket.close`` before anything
        else. This middleware never called ``self.app`` for a refused
        connection, so it must consume that ``connect`` event itself and
        answer ``close`` directly — never silently drop the socket (that
        reads as a hang, not a refusal) and never forward a refused
        connection to the app.
        """
        connect_event = await receive()
        if connect_event.get("type") != "websocket.connect":
            # Protocol violation upstream — nothing we can cleanly close.
            return
        await send({"type": "websocket.close", "code": code, "reason": reason})

    async def _build_context(self, request: Request | HTTPConnection) -> AppContext:
        # Build the AppContext via successive ``with_overrides`` so the final
        # object is fully constructed before we ever set the ContextVar.
        # AppContext is frozen in Phase 1+; the helpers below all return new
        # instances.

        # Honor client-supplied X-Request-Id when present so the request
        # correlation token round-trips through realtime echoes (the FE
        # uses it to dedupe its own optimistic writes from server-side
        # broadcasts of the same row).
        #
        # The header MUST be a valid UUID: request_id becomes the
        # cx_user_request primary key (a UUID column) downstream, so a
        # non-UUID value silently produced NO request row at all and orphaned
        # the conversation (it appeared stuck forever, no completion, no
        # error). Anything that isn't a UUID — or is absent — gets a fresh
        # server-minted UUID instead. Reusing ONE valid request_id across
        # multiple conversations is now fully CORRECT (not a collision): a
        # cx_user_request is one backend API call with NO conversation, and
        # each conversation it touches gets its own cx_request row — that IS
        # the request↔conversation bridge.
        client_request_id = (request.headers.get("x-request-id") or "").strip()
        request_id = client_request_id if _is_uuid(client_request_id) else str(uuid.uuid4())

        # Hold every frame until the response body opens the wire. Request
        # PREPARATION (tool merge, MCP attachment, sandbox arming) runs long
        # before the NDJSON body exists; a frame published there used to
        # advance the wire sequence and make the journal attach raise from
        # inside the response generator, which reached the browser as an HTTP
        # 200 with an EMPTY body (prod 2026-09-13). Armed here — the one place
        # every HTTP request's emitter is born — so no call site anywhere can
        # reopen that door.
        request_emitter = StreamEmitter(debug=False)
        request_emitter.hold_wire_until_open()

        ctx = AppContext(
            ip_address=client_ip(request),
            user_agent=request.headers.get("user-agent"),
            emitter=request_emitter,
            request_id=request_id,
            route=request.url.path,
        )

        authorization: str | None = request.headers.get("authorization")
        fingerprint_id: str | None = request.headers.get("x-fingerprint-id") or request.headers.get(
            "x-guest-fingerprint"
        )

        if authorization:
            # The API-key lane (`Authorization: Bearer mx_...`). ONE header for
            # every credential kind — disambiguated here by shape, exactly once.
            # When the lane claims the request it returns a context (accepted or
            # anonymous-after-rejection) and nothing downstream ever branches on
            # "is this an API key" again.
            api_key_ctx = await self._admit_api_key(authorization, request, ctx)
            if api_key_ctx is not None:
                return api_key_ctx

            enriched = await self._validate_token(authorization, fingerprint_id, ctx)
            if enriched is not None:
                return await self._resolve_organization(request, enriched)

            # A credential was PRESENTED and REFUSED (expired, bad signature,
            # wrong scheme). The caller is a signed-in client whose session
            # lapsed — never a guest. Falling through to the fingerprint lane
            # minted an anonymous auth.users row (and its organization) for
            # every expired-token request a browser sent with both headers:
            # 172 of them on one admin-only GET in 30 days (2026-09-30).
            # Answer anonymously so the route says 401 and the client refreshes.
            # Guard: tests/test_rejected_bearer_never_enters_guest_lane.py.
            return ctx

        # 🚨 THE GUEST LANE EXISTS ONLY WHERE A HOST WIRED A RESOLVER. A
        # fingerprint is an unauthenticated, caller-chosen string; only
        # ``resolve_guest`` can turn it into a real ``auth.users`` identity.
        # Until 2026-09-26 a host with no resolver (the standalone matrx-files
        # and matrx-seo services, the hosted box) got ``user_id = fingerprint``
        # — so ``X-Guest-Fingerprint: <any user's uuid>`` with NO token read
        # that user's private files, and any non-uuid fingerprint 500'd with
        # InvalidTextRepresentationError. Without a resolver the header is
        # ignored for identity and the request stays anonymous (routes that
        # need a user answer 401). Guard:
        # tests/test_fingerprint_without_resolver_is_anonymous.py.
        mint_allowed = True
        if (
            fingerprint_id
            and self._resolve_guest
            and self._has_guest_identity is not None
            and (
                getattr(request, "method", "POST") in _READ_METHODS
                or self._is_incidental_request(request)
            )
        ):
            # A read (or an incidental write) from a fingerprint that never did
            # anything meaningful: no account.
            mint_allowed = await self._has_guest_identity(fingerprint_id)

        if fingerprint_id and self._resolve_guest and mint_allowed:
            user_id = await self._resolve_guest(
                fingerprint_id,
                ctx.ip_address,
                ctx.user_agent,
                route=f"{getattr(request, 'method', 'WS')} {request.url.path}",
            )

            # Sign the (fingerprint, user_id) pair so callers can verify
            # later (e.g. /files/migrate-guest-to-user proves the caller
            # was the guest at this UUID before they signed up).
            new_metadata = dict(ctx.metadata)
            try:
                new_metadata["guest_fingerprint_signature"] = self._sign_fingerprint(
                    fingerprint_id,
                    user_id,
                )
            except Exception:
                pass

            return ctx.with_overrides(
                auth_type="fingerprint",
                fingerprint_id=fingerprint_id,
                user_id=user_id,
                metadata=new_metadata,
            )

        # ------------------------------------------------------------------
        # Browser file-session cookie — the durable private render lane.
        # Accepted ONLY on GET byte-serving routes (COOKIE_AUTH_PATH_RE):
        # an <img>/<video> tag cannot send Authorization headers, and this
        # cookie can never authorize anything but reading bytes the user
        # already has access to. Source-enabled hosts also check current
        # authority; see middleware/file_session.py.
        # ------------------------------------------------------------------
        # ``.method`` only exists on a full HTTP ``Request``; a WebSocket
        # handshake is admitted through this same builder via a bare
        # ``HTTPConnection`` (see ``_admit_websocket``), which has no
        # ``.method`` at all — the file-session cookie lane is HTTP-GET-only
        # by design, so it is simply unreachable for a WS connection.
        if getattr(request, "method", None) == "GET":
            from .session_cookie import (
                COOKIE_AUTH_PATH_RE,
                SESSION_COOKIE_NAME,
            )

            if COOKIE_AUTH_PATH_RE.match(request.url.path):
                cookie_user = await self._file_cookie_user(
                    request.cookies.get(SESSION_COOKIE_NAME)
                )
                if cookie_user:
                    return ctx.with_overrides(
                        auth_type="cookie",
                        user_id=cookie_user,
                        is_authenticated=True,
                    )

        return ctx

    async def _file_cookie_user(self, value: str | None) -> str | None:
        """Authenticate a byte cookie; source decisions are fresh and never cached."""
        if value and value.startswith("v2."):
            credential, reason = classify_bound_file_session_value(value, self._guest_fp_secret)
            if reason == "signature_mismatch":
                self._report_cookie_drift(reason)
            if credential is None:
                return None
            if self._resolve_file_session is None:
                raise SessionAuthorityUnavailable("file-session authority not configured")
            try:
                resolve_file = self._resolve_file_session
                flight_key = "file:" + self._hash_token(value)
                active = await call_authority(
                    lambda: self._session_flights.do(
                        flight_key,
                        lambda: resolve_file(credential),
                        limit_seconds=self._session_resolve_timeout,
                    ),
                    attempt_timeout=self._session_resolve_timeout,
                    label="File-session authority",
                )
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                logging.getLogger(__name__).warning(
                    "File-session authority unavailable (%s)", type(exc).__name__
                )
                raise SessionAuthorityUnavailable("file-session authority unavailable") from exc
            return credential.user_id if active is True else None
        if self._require_file_session_source:
            return None
        from .session_cookie import classify_session_cookie_value

        user, reason = classify_session_cookie_value(value, self._guest_fp_secret)
        if reason == "signature_mismatch":
            self._report_cookie_drift(reason)
        return user

    async def _admin_lane_verdict(
        self, request: Request | HTTPConnection, ctx: AppContext, claimed: str
    ) -> bool | str:
        """True only when the request rides the admin lane AND the host's
        admission hook verifies it. The header alone never admits anything.

        False is a REFUSAL (not on the lane, not an admin, not the tenant). A
        string is a check that could not be DECIDED — the hook raised or timed
        out — naming why (``ADMIN_LANE_AUDIT_UNAVAILABLE`` /
        ``ADMIN_LANE_UNVERIFIABLE``). Never an admission, and never reported as
        "not a member"."""
        if self._admin_lane_admission is None or not ctx.user_id:
            return False
        if (ctx.auth_type == "token" and self._resolve_current_session is not None
                and not ctx.is_admin):
            # A host's role-only tenant hook cannot restore administrator power
            # that this request's fresh session/MFA authority has withheld.
            return False
        if (request.headers.get(ADMIN_LANE_HEADER) or "").strip() != "1":
            return False
        try:
            admission = self._admin_lane_admission
            admitted = await call_authority(
                lambda: admission(str(ctx.user_id), claimed),
                attempt_timeout=self._organization_resolve_timeout,
                label="Admin-lane authority",
                decisions=(AdminLaneAuditUnavailable,),
            )
        except Exception as exc:  # noqa: BLE001 — a failed check is a refusal, never an admission
            failure = (
                ADMIN_LANE_AUDIT_UNAVAILABLE
                if isinstance(exc, AdminLaneAuditUnavailable)
                else ADMIN_LANE_UNVERIFIABLE
            )
            vcprint(
                f"[AUTH][ERROR] admin-lane admission check FAILED for org={claimed} "
                f"user={ctx.user_id}: {type(exc).__name__}: {exc} — refused ({failure}).",
                color="red",
                log_level="ERROR",
            )
            return failure
        if admitted:
            vcprint(
                f"[AUTH][INFO] organization admitted by the ADMIN LANE: org={claimed} user={ctx.user_id}",
                color="green",
                log_level="INFO",
            )
        return bool(admitted)

    async def _record_grant_verdict(
        self, request: Request | HTTPConnection, ctx: AppContext, claimed: str
    ) -> bool | None:
        """True when the host's record-grant hook admits this exact request.

        False is a refusal (no hook, not HTTP, unsafe path, or the host said
        no). None is a check that could not be DECIDED (the hook raised or
        timed out) — never an admission, and never reported as "not a member".
        """
        if self._record_grant_admission is None or not ctx.user_id:
            return False
        if not isinstance(request, Request):
            return False
        if _unsafe_encoded_path(request.scope.get("raw_path")):
            return False
        try:
            grant = self._record_grant_admission
            admitted = await call_authority(
                lambda: grant(str(ctx.user_id), claimed, request.method.upper(), request.url.path),
                attempt_timeout=self._organization_resolve_timeout,
                label="Record-grant authority",
            )
        except Exception as exc:  # noqa: BLE001 — a failed check is never an admission
            vcprint(
                f"[AUTH][ERROR] record-grant admission check FAILED for org={claimed} "
                f"user={ctx.user_id} {request.method} {request.url.path}: "
                f"{type(exc).__name__}: {exc} — refused (unverifiable).",
                color="red",
                log_level="ERROR",
            )
            return None
        if admitted:
            vcprint(
                f"[AUTH][INFO] organization admitted by a RECORD GRANT: org={claimed} "
                f"user={ctx.user_id} {request.method} {request.url.path}",
                color="green",
                log_level="INFO",
            )
        return bool(admitted)

    async def _resolve_organization(self, request: Request | HTTPConnection, ctx: AppContext) -> AppContext:
        """Pin a verified organization_id onto an authenticated AppContext.

        Resolution order:
          1. ``X-Organization-Id`` header (explicit user choice).
          2. JWT claim ``organization_id`` or ``org_id`` (stashed on
             ``ctx.metadata['jwt_claims']`` by ``_validate_token``).
        If a resolver was injected, it is the source of truth: it returns
        the verified org_id (or None to deny). Without a resolver, the
        claim is trusted as-is — acceptable in dev, never in production.
        """
        if not ctx.is_authenticated or not ctx.user_id:
            return ctx

        claimed: str | None = request.headers.get("x-organization-id") or None
        if not claimed:
            claims = ctx.metadata.get("jwt_claims") if isinstance(ctx.metadata, dict) else None
            if isinstance(claims, dict):
                raw = claims.get("organization_id") or claims.get("org_id")
                if isinstance(raw, str) and raw:
                    claimed = raw

        if claimed is None and self._resolve_active_organization is None:
            return ctx

        # A value that is not an organization id at all is answered HERE, before
        # any lookup: sending it to the resolver produces a database type error,
        # which the handler below would honestly but uselessly report as
        # "could not verify — try again" for something that will never verify.
        if claimed is not None:
            if not _is_uuid(str(claimed).strip()):
                vcprint(
                    f"[AUTH][REJECT] organization admission MALFORMED: {claimed!r} is "
                    f"not an organization id (user={ctx.user_id})",
                    color="yellow",
                    log_level="WARNING",
                )
                return ctx.with_overrides(
                    organization_admission="malformed",
                    claimed_organization_id=str(claimed),
                )

        if self._resolve_active_organization is not None:
            try:
                # Bounded: the singleflight task is shielded, so a timeout here
                # stops only THIS caller waiting; a TimeoutError is a failure to
                # verify ("unverifiable", 503 below), never a quiet no-org.
                # Transient misses are retried within a bounded budget (authority_retry);
                # not-found / archived are DECISIONS and raise at once.
                verified = await call_authority(
                    lambda: self._org_flights.do(
                        (ctx.user_id, claimed),
                        lambda: self._resolve_active_organization(ctx.user_id, claimed),
                    ),
                    attempt_timeout=self._organization_resolve_timeout,
                    label="Organization membership authority",
                    decisions=(OrganizationNotFound, OrganizationArchived),
                )
            except OrganizationNotFound:
                # A well-formed id for an organization that does not exist. As
                # permanent as a denial and as un-retryable, but a DIFFERENT
                # repair — telling this caller "ask an admin to add you" would
                # send them to fix the wrong thing.
                vcprint(
                    f"[AUTH][REJECT] organization admission UNKNOWN: no organization "
                    f"{claimed} (user={ctx.user_id})",
                    color="yellow",
                    log_level="WARNING",
                )
                return ctx.with_overrides(
                    organization_admission="unknown",
                    claimed_organization_id=claimed,
                )
            except OrganizationArchived:
                # The organization exists and is closed. Refused for everyone —
                # member, owner and platform admin alike — exactly as the
                # database refuses it (iam.has_org_access_for).
                vcprint(
                    f"[AUTH][REJECT] organization admission ARCHIVED: organization "
                    f"{claimed} is archived (user={ctx.user_id})",
                    color="yellow",
                    log_level="WARNING",
                )
                return ctx.with_overrides(
                    organization_admission="archived",
                    claimed_organization_id=claimed,
                )
            except Exception as exc:  # noqa: BLE001 — resolver failures must never 500 the request
                # 🚨 NOT A SILENT NO-ORG. The request DID name an organization and
                # the platform could not tell whether the caller belongs to it.
                # Downstream, "no org" is not a smaller answer — it is a
                # DIFFERENT one (the mandate ladder resolves user -> ACTIVE org
                # -> system, so a swallowed failure here changes which agent
                # runs). The context now carries the difference; consumers that
                # scope by organization refuse on it.
                vcprint(
                    f"[AUTH][ERROR] organization admission UNVERIFIABLE for "
                    f"org={claimed} user={ctx.user_id}: {type(exc).__name__}: {exc} — "
                    "the request is NOT demoted to no-org; organization-scoped "
                    "features will refuse until the resolver answers again.",
                    color="red",
                    log_level="ERROR",
                )
                return ctx.with_overrides(
                    organization_admission="unverifiable",
                    claimed_organization_id=claimed,
                )
        else:
            verified = claimed

        if not verified:
            lane = await self._admin_lane_verdict(request, ctx, str(claimed)) if claimed else False
            if isinstance(lane, str):
                # The admin lane could not DECIDE. Retryable server-side
                # failure ("unverifiable", 503), with the real cause named —
                # an admin whose audit log is down is not "not a member".
                metadata = dict(ctx.metadata) if isinstance(ctx.metadata, dict) else {}
                metadata[ADMISSION_FAILURE_KEY] = lane
                return ctx.with_overrides(
                    organization_admission="unverifiable",
                    claimed_organization_id=claimed,
                    metadata=metadata,
                )
            if lane is True:
                # THE ADMIN LANE: the host verified a platform admin, on the
                # admin lane, naming its platform tenant. The tenant is VERIFIED
                # (every tenant-scoped consumer reads "verified"); the lane that
                # admitted it rides on metadata so it is never mistaken for a
                # membership.
                metadata = dict(ctx.metadata) if isinstance(ctx.metadata, dict) else {}
                metadata["organization_admitted_by"] = "admin_lane"
                return ctx.with_overrides(
                    organization_id=str(claimed),
                    organization_admission="verified",
                    claimed_organization_id=claimed,
                    metadata=metadata,
                )
            if claimed:
                grant = await self._record_grant_verdict(request, ctx, str(claimed))
                if grant is None:
                    return ctx.with_overrides(
                        organization_admission="unverifiable",
                        claimed_organization_id=claimed,
                    )
                if grant is True:
                    # THE RECORD-GRANT LANE: the host verified a share grant on
                    # the exact record this route acts on, whose own
                    # organization is the claimed one. The tenant is VERIFIED;
                    # how it was admitted rides on metadata so it is never
                    # mistaken for a membership.
                    metadata = dict(ctx.metadata) if isinstance(ctx.metadata, dict) else {}
                    metadata["organization_admitted_by"] = "record_grant"
                    return ctx.with_overrides(
                        organization_id=str(claimed),
                        organization_admission="verified",
                        claimed_organization_id=claimed,
                        metadata=metadata,
                    )
                # A proved non-member. An ANSWER, not a failure — and still not
                # the same thing as naming no organization at all.
                vcprint(
                    f"[AUTH][INFO] organization admission DENIED for org={claimed} "
                    f"user={ctx.user_id} (not an active member)",
                    color="yellow",
                    log_level="INFO",
                )
                return ctx.with_overrides(
                    organization_admission="denied",
                    claimed_organization_id=claimed,
                )
            return ctx

        if (request.headers.get(ADMIN_LANE_HEADER) or "").strip() == "1":
            # A MEMBER of the platform tenant who is also a platform admin, on the
            # admin lane: membership already admitted the org, but the request is
            # still ADMIN work and must read as the lane (admin-reach doors ask
            # ``organization_admitted_by == "admin_lane"``). The host hook
            # re-verifies tenant + admin registry and audits, exactly as for a
            # non-member. A refusal or an undecided check leaves the plain
            # membership admission untouched — never a demotion.
            lane = await self._admin_lane_verdict(request, ctx, str(verified))
            if lane is True:
                metadata = dict(ctx.metadata) if isinstance(ctx.metadata, dict) else {}
                metadata["organization_admitted_by"] = "admin_lane"
                return ctx.with_overrides(
                    organization_id=verified,
                    organization_admission="verified",
                    claimed_organization_id=claimed,
                    metadata=metadata,
                )

        return ctx.with_overrides(
            organization_id=verified,
            organization_admission="verified",
            claimed_organization_id=claimed,
        )

    async def _admit_api_key(
        self,
        authorization: str,
        request: HTTPConnection,
        ctx: AppContext,
    ) -> AppContext | None:
        """The API-key admission lane (design: API-KEY-LANE-DESIGN.md, C16).

        Returns None when the request is not an API-key request (no resolver
        configured, non-bearer scheme, or the token lacks the ``mx_`` prefix) —
        the JWT lane then proceeds untouched. When the lane claims the request:

        * resolver success → authenticated context: ``user_id`` is the key's
          service identity, ``auth_type="api_key"``, and the key's organization
          is the admitted org. ``X-Organization-Id``, when present, must EQUAL
          it (409 via ``ApiKeyOrganizationMismatch``); when absent the key's
          org is admitted — fail-closed while sparing machine callers a
          redundant header.
        * typed current-authority outage → retryable HTTP503 / WebSocket1013.
        * resolver rejection/unexpected failure → the anonymous context, with the same
          compact INFO control-flow logging a rejected JWT gets (no token
          material ever logged). The route's own auth gate produces the 401.
        """
        if self._resolve_api_key is None:
            return None
        try:
            scheme, token_value = authorization.split(None, 1)
        except ValueError:
            return None
        if scheme.lower() != "bearer" or not token_value.startswith(API_KEY_BEARER_PREFIX):
            return None

        identity: ApiKeyIdentity | None
        try:
            identity = await self._resolve_api_key(token_value)
        except ApiKeyRefused as refused:
            vcprint("[AUTH][INFO] API key refused: " + refused.message, color="yellow", log_level="INFO")
            refused_metadata = dict(ctx.metadata)
            refused_metadata["credential_refused"] = refused.message
            return ctx.with_overrides(metadata=refused_metadata)
        except CredentialAuthorityUnavailable:
            raise
        except Exception as exc:  # noqa: BLE001 — unexpected resolver failure retains denial compatibility
            vcprint(
                f"[AUTH][WARN] API key resolver failed: {type(exc).__name__}",
                color="yellow",
                log_level="WARNING",
            )
            identity = None

        if identity is None:
            vcprint(
                "[AUTH][INFO] API key rejected",
                color="yellow",
                log_level="INFO",
            )
            return ctx

        if identity.kind == "personal":
            return await self._admit_personal_key(request, ctx, identity)

        claimed = (request.headers.get("x-organization-id") or "").strip()
        if claimed and claimed.lower() != str(identity.organization_id).lower():
            raise ApiKeyOrganizationMismatch(claimed, str(identity.organization_id))

        vcprint(
            f"[AUTH][INFO] API key accepted: user={identity.user_id} "
            f"org={identity.organization_id} key={identity.key_id or '?'}",
            color="green",
            log_level="INFO",
        )

        new_metadata = dict(ctx.metadata)
        new_metadata["api_key_id"] = identity.key_id
        new_metadata["api_key_expires_at"] = identity.expires_at
        if identity.key_name:
            new_metadata["api_key_name"] = identity.key_name

        return ctx.with_overrides(
            user_id=identity.user_id,
            auth_type="api_key",
            is_authenticated=True,
            organization_id=str(identity.organization_id),
            organization_admission="verified",
            claimed_organization_id=str(identity.organization_id),
            metadata=new_metadata,
        )

    async def _admit_personal_key(
        self, request: HTTPConnection, ctx: AppContext, identity: ApiKeyIdentity
    ) -> AppContext:
        """A personal key IS the person — admitted exactly as their own sign-in would be.

        The identity is the person's own ``auth.users`` row. The organization is NOT the
        key's to decide: it goes through :meth:`_resolve_organization`, the one resolver a
        signed-in person's request crosses — ``X-Organization-Id`` when sent, else the
        organization this key was deliberately configured with (carried as the claim a JWT
        would carry). Membership is verified there on every request, so a person removed
        from an organization is refused on the next call even while the key row is cached.

        The admin tier is deliberately NOT resolved: full admin access lives inside the
        admin apps, signed in (Arman, 2026-09-26/29); a key reaches everything the person
        can do as an ordinary member.
        """
        vcprint(
            f"[AUTH][INFO] personal API key accepted: user={identity.user_id} "
            f"key={identity.key_id or '?'}",
            color="green",
            log_level="INFO",
        )
        new_metadata = dict(ctx.metadata)
        new_metadata["api_key_id"] = identity.key_id
        new_metadata["api_key_kind"] = "personal"
        new_metadata["api_key_expires_at"] = identity.expires_at
        if identity.key_name:
            new_metadata["api_key_name"] = identity.key_name
        # The claims an RLS session is opened with. `organization_id` is the key's configured
        # organization — the same claim slot a JWT's organization rides in — so the resolver
        # below treats it exactly like a presented claim: verified, never trusted.
        new_metadata["jwt_claims"] = {
            "sub": identity.user_id,
            "role": "authenticated",
            "aud": "authenticated",
            "organization_id": str(identity.organization_id),
        }
        admitted = ctx.with_overrides(
            user_id=identity.user_id,
            auth_type="api_key",
            is_authenticated=True,
            metadata=new_metadata,
        )
        return await self._resolve_organization(request, admitted)

    def _report_cookie_drift(self, reason: str) -> None:
        """CRITICAL alarm for the mx_files_session drift detector, rate-limited
        per (process, reason) burst-window.

        First occurrence logs immediately; further occurrences within
        ``COOKIE_DRIFT_LOG_WINDOW_SECONDS`` are counted silently; the next
        occurrence after the window logs again carrying the suppressed count.
        The token ``MX_COOKIE_SIGNATURE_MISMATCH`` is machine-greppable.
        """
        import logging

        now = time.monotonic()
        last, suppressed = self._drift_log_state.get(reason, (None, 0))
        if last is not None and now - last < COOKIE_DRIFT_LOG_WINDOW_SECONDS:
            self._drift_log_state[reason] = (last, suppressed + 1)
            return
        suppressed_note = (
            f" ({suppressed} further occurrence(s) suppressed in the last burst window)"
            if suppressed
            else ""
        )
        source = "EPHEMERAL per-process fallback" if self.secret_is_ephemeral else "injected"
        logging.getLogger("matrx_connect.auth").critical(
            "MX_COOKIE_SIGNATURE_MISMATCH: a structurally valid, UNEXPIRED "
            "mx_files_session cookie failed HMAC verification%s. This is secret "
            "drift — the cookie was minted by a process holding a DIFFERENT "
            "guest_fingerprint_secret (or it was tampered with); it is never a "
            "normal anonymous request, and every private file render for this "
            "client is 401ing. This process's secret is %s. Remedy: inject ONE "
            "stable guest_fingerprint_secret into AuthMiddleware on EVERY "
            "instance/container (the 2026-08-30 private-file outage class).",
            suppressed_note,
            source,
        )
        self._drift_log_state[reason] = (now, 0)

    def _sign_fingerprint(self, fingerprint: str, user_id: str) -> str:
        """HMAC-SHA256 signature of (fingerprint, user_id). 32-byte hex."""
        import hmac as _hmac

        msg = f"{fingerprint}|{user_id}".encode()
        return _hmac.new(self._guest_fp_secret, msg, hashlib.sha256).hexdigest()

    @staticmethod
    def _hash_token(token: str) -> str:
        # Full SHA256 hex; never store the raw token. Collisions are
        # computationally infeasible.
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def _token_cache_lookup(
        self,
        token: str,
    ) -> (
        tuple[
            str,
            bool,
            str | None,
            dict[str, Any],
            str | None,
            int | None,
            str | None,
        ]
        | None
    ):
        """Return identity, claims, and JWT lifecycle metadata for a fresh
        entry. Expired entries are evicted on access."""
        if self._token_cache_ttl <= 0 or not self._token_cache:
            return None
        key = self._hash_token(token)
        entry = self._token_cache.get(key)
        if entry is None:
            return None
        (
            cache_expires_at,
            user_id,
            is_admin,
            email,
            jwt_claims,
            admin_level,
            jwt_expires_at,
            issuer,
        ) = entry
        if time.monotonic() >= cache_expires_at:
            self._token_cache.pop(key, None)
            return None
        return (
            user_id,
            is_admin,
            email,
            jwt_claims,
            admin_level,
            jwt_expires_at,
            issuer,
        )

    def _token_cache_insert(
        self,
        token: str,
        *,
        user_id: str,
        is_admin: bool,
        admin_level: str | None,
        email: str | None,
        jwt_claims: dict[str, Any],
        jwt_exp: int | None,
        jwt_issuer: str | None,
    ) -> None:
        """Store a successful validation. TTL is capped by the JWT's own
        ``exp`` so a cached entry can never outlive the token itself."""
        if self._token_cache_ttl <= 0 or self._token_cache_max_size <= 0:
            return
        now_mono = time.monotonic()
        ttl = self._token_cache_ttl
        if jwt_exp is not None:
            remaining = float(jwt_exp) - time.time()
            if remaining <= 0:
                return  # token already expired — don't pollute the cache
            ttl = min(ttl, remaining)
        # Opportunistic sweep when full: drop expired entries first, then
        # the oldest by expiry. Cheap because the cache is tiny.
        if len(self._token_cache) >= self._token_cache_max_size:
            expired_keys = [k for k, v in self._token_cache.items() if v[0] <= now_mono]
            for k in expired_keys:
                self._token_cache.pop(k, None)
            if len(self._token_cache) >= self._token_cache_max_size:
                # Drop the oldest entries until we're back under the cap.
                ordered = sorted(self._token_cache.items(), key=lambda kv: kv[1][0])
                drop_n = len(self._token_cache) - self._token_cache_max_size + 1
                for k, _ in ordered[:drop_n]:
                    self._token_cache.pop(k, None)
        self._token_cache[self._hash_token(token)] = (
            now_mono + ttl,
            user_id,
            is_admin,
            email,
            copy.deepcopy(jwt_claims),
            admin_level,
            jwt_exp,
            jwt_issuer,
        )

    def verify_fingerprint_signature(
        self,
        fingerprint: str,
        user_id: str,
        signature: str,
    ) -> bool:
        import hmac as _hmac

        expected = self._sign_fingerprint(fingerprint, user_id)
        return _hmac.compare_digest(expected, signature or "")

    async def _validate_token(
        self,
        authorization: str,
        fingerprint_id: str | None,
        ctx: AppContext,
    ) -> AppContext | None:
        try:
            scheme, token_value = authorization.split(None, 1)
            if scheme.lower() != "bearer":
                vcprint(
                    f"[AUTH][WARN] Non-bearer scheme rejected: {scheme!r}",
                    color="yellow",
                    log_level="WARNING",
                )
                return None
        except ValueError:
            vcprint(
                "[AUTH][WARN] Malformed authorization header", color="yellow", log_level="WARNING"
            )
            return None

        # NOTE (2026-05): static admin-token escape hatch removed. The only
        # accepted auth is a Supabase-signed JWT validated below. For local
        # dev / agent auth, hosts expose a dev-login endpoint that mints
        # real JWTs for real user_ids — see aidream/api/routers/dev_login.py.

        verified = await self.verify_token_raw(token_value)
        if verified is None:
            return None

        new_metadata = dict(ctx.metadata)
        new_metadata["jwt_claims"] = verified.claims
        # exp is deliberately omitted from the selective claims projection.
        # Carry its verified value separately for credentials derived from
        # this exact login; never re-decode the raw bearer without verification.
        new_metadata["jwt_expires_at"] = verified.expires_at
        if verified.session_decision is not None:
            decision = verified.session_decision
            new_metadata["admin_admission"] = {
                "admitted": decision.admin_admitted,
                "mfa_required": decision.mfa_required,
                "reason": decision.reason,
                "current_admin_level": decision.current_admin_level,
            }
        return ctx.with_overrides(
            user_id=verified.user_id,
            auth_type="token",
            is_authenticated=True,
            # A Supabase anonymous user (guest token) is a verified JWT like any
            # other; only account-only work tells it apart (ctx.has_account).
            is_anonymous=verified.claims.get("is_anonymous") is True,
            is_admin=verified.is_admin,
            admin_level=verified.admin_level,
            email=verified.email,
            token=verified.token,
            fingerprint_id=fingerprint_id,
            metadata=new_metadata,
        )

    async def verify_token_raw(self, token_value: str) -> VerifiedToken | None:
        """Verify one token, coalescing concurrent cache misses by token hash."""
        cached = self._token_cache_lookup(token_value)
        if cached is not None:
            result = self._verified_from_cache(token_value, cached)
        else:
            result = await self._token_flights.do(
                self._hash_token(token_value),
                lambda: self._verify_token_raw_inner(token_value),
            )
        if result is None:
            return None
        # Current authority is NEVER cached with crypto/admin identity. Each
        # admission checks after the cache/single-flight, including warm hits.
        decision: CurrentSessionDecision | None = None
        if self._resolve_current_session is not None:
            try:
                resolve_session = self._resolve_current_session
                flight_key = "login:" + self._hash_token(token_value)
                authority = await call_authority(
                    lambda: self._session_flights.do(
                        flight_key,
                        lambda: resolve_session(result),
                        limit_seconds=self._session_resolve_timeout,
                    ),
                    attempt_timeout=self._session_resolve_timeout,
                    label="Current-session authority",
                )
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                logging.getLogger(__name__).warning(
                    "Current-session authority unavailable (%s)", type(exc).__name__
                )
                raise SessionAuthorityUnavailable("session authority unavailable") from exc
            if isinstance(authority, CurrentSessionDecision):
                decision = authority
            elif authority is True:
                # A boolean authority proved login, not current membership/MFA.
                # It must never preserve a cached administrator grant.
                decision = CurrentSessionDecision(True, None, False, None, "login_only")
            else:
                return None
            if not decision.active:
                return None
        # Each caller owns its claims mapping; a mutation in one request must
        # never leak through the shared flight or completed-result cache.
        return VerifiedToken(
            user_id=result.user_id,
            is_admin=decision.admin_admitted if decision is not None else result.is_admin,
            email=result.email,
            claims=copy.deepcopy(result.claims),
            token=result.token,
            admin_level=(decision.current_admin_level if decision.admin_admitted else None)
            if decision is not None else result.admin_level,
            expires_at=result.expires_at,
            issuer=result.issuer,
            session_decision=decision,
        )

    @staticmethod
    def _verified_from_cache(
        token_value: str,
        cached: tuple[
            str,
            bool,
            str | None,
            dict[str, Any],
            str | None,
            int | None,
            str | None,
        ],
    ) -> VerifiedToken:
        (
            user_id,
            is_admin,
            email,
            jwt_claims,
            admin_level,
            expires_at,
            issuer,
        ) = cached
        return VerifiedToken(
            user_id=user_id,
            is_admin=is_admin,
            email=email,
            claims=copy.deepcopy(jwt_claims),
            token=token_value,
            admin_level=admin_level,
            expires_at=expires_at,
            issuer=issuer,
        )

    async def _verify_token_raw_inner(self, token_value: str) -> VerifiedToken | None:
        """Verify a raw Supabase JWT (no ``Bearer`` prefix) and resolve admin
        status. Returns a ``VerifiedToken`` on success, ``None`` on any failure.

        This is the single token-verification primitive: the HTTP
        ``_validate_token`` path and any out-of-band resource server (the MCP
        OAuth TokenVerifier) both call it, so the crypto, the lazy JWKS client,
        the token cache, and the admin resolver live in exactly one place.
        """
        if not self._jwt_secret and not self._jwks_url:
            vcprint(
                "[AUTH][ERROR] Neither jwt_secret nor jwks_url is set — "
                "JWT tokens cannot be validated.",
                color="red",
                log_level="ERROR",
            )
            return None

        # JWT structural pre-check.
        # A Supabase JWT is exactly three base64url segments separated by
        # dots (header.payload.signature). When the bearer token doesn't
        # match that shape, it isn't claiming to be a JWT — it's a
        # different bearer scheme that the host's downstream routers
        # authenticate themselves (e.g. AI Dream's sandbox-bridge service
        # token + ``X-Matrx-User-Id`` header pair, or any future
        # machine-to-machine integration that shares the
        # ``Authorization: Bearer …`` header). Skipping the decode
        # silently here prevents misleading
        # ``JWT validation FAILED: Not enough segments`` ERROR-level
        # noise on every such request, while still letting the request
        # fall through to whatever auth the route itself enforces.
        # Real JWT integrity / signature / audience / expiry failures
        # still surface loudly below — those are tokens that ARE
        # claiming to be JWTs and are genuinely broken.
        if token_value.count(".") != 2:
            return None

        # Scoped-capability tokens from a registered first-party issuer are
        # not user-login tokens — they are verified by the route that owns
        # their audience (matrx_connect.scoped_tokens). Fall through
        # silently instead of failing loudly on the audience check.
        if self._passthrough_issuers:
            try:
                unverified = jwt.decode(token_value, options={"verify_signature": False})
                if unverified.get("iss") in self._passthrough_issuers:
                    return None
            except jwt.InvalidTokenError:
                pass  # not even decodable — let the normal path report it

        # Hot path: a fresh cache entry skips the JWT decode AND the admin
        # DB lookup. pdf.js fires 5–6 HTTP Range requests against
        # /files/{id}/download in ~200ms for a single document open, each
        # carrying the same Bearer token — the cache collapses them to one
        # real validation.
        cached = self._token_cache_lookup(token_value)
        if cached is not None:
            return self._verified_from_cache(token_value, cached)

        try:
            # Peek at the unverified header to pick the verification key.
            # Symmetric (HS256) → shared secret; asymmetric (RS256/ES256)
            # → JWKS signing key resolved by ``kid``.
            try:
                unverified_header = jwt.get_unverified_header(token_value)
            except jwt.InvalidTokenError as exc:
                vcprint(
                    f"[AUTH][ERROR] JWT header parse FAILED: {type(exc).__name__}: {exc}",
                    color="red",
                    log_level="ERROR",
                )
                return None
            alg = unverified_header.get("alg", "HS256")

            allowed = list(self._jwt_algorithms)
            if alg not in allowed:
                vcprint(
                    f"[AUTH][ERROR] JWT alg={alg!r} not in allow-list {allowed}; rejecting.",
                    color="red",
                    log_level="ERROR",
                )
                return None

            decode_key: object
            if alg == "HS256":
                if not self._jwt_secret:
                    vcprint(
                        "[AUTH][WARN] HS256 token rejected because jwt_secret "
                        "is not configured; rejecting.",
                        color="yellow",
                        log_level="WARNING",
                    )
                    return None
                decode_key = self._jwt_secret
            else:
                # Asymmetric — use JWKS.
                if not self._jwks_url:
                    vcprint(
                        f"[AUTH][ERROR] {alg} token received but jwks_url "
                        "is not configured; rejecting.",
                        color="red",
                        log_level="ERROR",
                    )
                    return None
                if self._jwks_client is None:
                    # Lazy build; PyJWKClient handles HTTP fetch + cache.
                    self._jwks_client = jwt.PyJWKClient(self._jwks_url)
                try:
                    kid_value = unverified_header.get("kid")
                    if not isinstance(kid_value, str) or not kid_value:
                        vcprint(
                            f"[AUTH][ERROR] {alg} token missing required kid; rejecting.",
                            color="red",
                            log_level="ERROR",
                        )
                        return None
                    kid = kid_value
                    signing_key = await self._jwks_flights.do(
                        kid,
                        lambda: self._get_signing_key(kid),
                    )
                except (jwt.PyJWKClientError, jwt.PyJWKClientConnectionError) as exc:
                    # An absent signing key is an authentication rejection, not
                    # an application crash. This is expected for stale sessions
                    # after a key rotation and for tokens issued by an unrelated
                    # project. Keep it visible for security/operator correlation,
                    # but out of the ERROR-only application-failure safety net.
                    vcprint(
                        f"[AUTH][WARN] JWKS key lookup rejected token for "
                        f"alg={alg}: {type(exc).__name__}: {exc}",
                        color="yellow",
                        log_level="WARNING",
                    )
                    return None
                decode_key = signing_key.key

            decode_kwargs: dict = {"algorithms": [alg]}
            if self._jwt_audience:
                decode_kwargs["audience"] = self._jwt_audience
            else:
                decode_kwargs["options"] = {"verify_aud": False}
            decoded = jwt.decode(
                token_value,
                decode_key,
                **decode_kwargs,
            )
            user_id = decoded.get("sub", "")
            vcprint(f"[AUTH][INFO] JWT accepted: user={user_id}", color="green", log_level="INFO")

            # Resolve admin status. The tier resolver is preferred (it also
            # yields the level); is_admin is derived as ``level is not None``.
            # A host that only wired the boolean resolver still works.
            is_admin = False
            admin_level: str | None = None
            if self._admin_level_resolver and user_id:
                try:
                    admin_level = await self._admin_level_resolver(user_id)
                    is_admin = admin_level is not None
                except Exception as exc:
                    vcprint(
                        f"[AUTH][WARN] Admin tier check failed for user={user_id}: {exc}",
                        color="yellow",
                        log_level="WARNING",
                    )
            elif self._is_admin_resolver and user_id:
                try:
                    is_admin = await self._is_admin_resolver(user_id)
                except Exception as exc:
                    vcprint(
                        f"[AUTH][WARN] Admin check failed for user={user_id}: {exc}",
                        color="yellow",
                        log_level="WARNING",
                    )

            if is_admin:
                vcprint(
                    f"[AUTH][INFO] Admin confirmed from DB: user={user_id} "
                    f"level={admin_level or 'unknown'}",
                    color="green",
                    log_level="INFO",
                )

            # Stash the raw claims on metadata under a known key so
            # downstream resolvers (organization_id, custom scopes) can read
            # them without re-decoding. Strip the signature/exp metadata from
            # the snapshot — claims-only.
            jwt_claims = {
                k: v
                for k, v in decoded.items()
                if k not in ("iat", "exp", "nbf", "jti", "iss", "sub")
            }
            email = decoded.get("email")
            # Insert into the validation cache so subsequent requests with
            # the same Bearer token within the TTL window short-circuit the
            # JWT decode + admin DB lookup. ``exp`` is the JWT's own
            # expiry (if present) — the insert caps TTL at remaining
            # lifetime so a cached entry never outlives the token.
            self._token_cache_insert(
                token_value,
                user_id=user_id,
                is_admin=is_admin,
                admin_level=admin_level,
                email=email,
                jwt_claims=jwt_claims,
                jwt_exp=decoded.get("exp"),
                jwt_issuer=decoded.get("iss"),
            )

            return VerifiedToken(
                user_id=user_id,
                is_admin=is_admin,
                email=email,
                claims=copy.deepcopy(jwt_claims),
                token=token_value,
                admin_level=admin_level,
                expires_at=decoded.get("exp"),
                issuer=decoded.get("iss"),
            )
        except jwt.ExpiredSignatureError:
            # Expiry is normal session lifecycle, not a signature/integrity
            # incident. The HTTP boundary emits one compact 401 outcome; logging
            # a second red traceback-sized alarm here made routine refreshes look
            # like uncaught server failures. Out-of-band verifiers simply return
            # rejection and let their transport produce its normal challenge.
            return None
        except jwt.InvalidTokenError as e:
            vcprint(
                f"[AUTH][ERROR] JWT validation FAILED: {type(e).__name__}: {e}",
                color="red",
                log_level="ERROR",
            )
            return None

    async def _get_signing_key(self, kid: str) -> object:
        # PyJWKClient performs synchronous HTTP and owns mutable caches. Keep it
        # off the event loop, serialize access, and allow at most one forced
        # refresh per cooldown. Random unknown kids therefore cannot trigger an
        # outbound JWKS request each.
        async with self._jwks_lookup_lock:
            cached = self._jwks_keys.get(kid)
            if cached is not None:
                return cached

            now = time.monotonic()
            if not self._jwks_keys:
                if (
                    self._jwks_last_refresh
                    and now - self._jwks_last_refresh < JWKS_REFRESH_COOLDOWN_SECONDS
                ):
                    raise jwt.PyJWKClientError("JWKS refresh is cooling down")
                # Set before I/O so a failed fetch is negatively cached for the
                # cooldown instead of every queued token retrying the network.
                self._jwks_last_refresh = now
                signing_keys = await asyncio.to_thread(self._jwks_client.get_signing_keys)
                self._jwks_keys.update({key.key_id: key for key in signing_keys if key.key_id})
            elif now - self._jwks_last_refresh >= JWKS_REFRESH_COOLDOWN_SECONDS:
                # A failed forced refresh is still a refresh attempt. Record it
                # before outbound I/O so queued unknown kids cannot each retry
                # the same failing endpoint. Keep the last known-good keys
                # unless the fetch succeeds.
                self._jwks_last_refresh = now
                signing_keys = await asyncio.to_thread(
                    self._jwks_client.get_signing_keys,
                    True,
                )
                self._jwks_keys = {key.key_id: key for key in signing_keys if key.key_id}

            signing_key = self._jwks_keys.get(kid)
            if signing_key is None:
                raise jwt.PyJWKClientError(f'Unable to find a signing key that matches: "{kid}"')
            return signing_key
