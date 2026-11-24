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
import uuid
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from typing import Any

from matrx_utils import AsyncSingleFlight, get_inflight_registry, vcprint
from starlette.requests import HTTPConnection, Request
from starlette.types import ASGIApp, Receive, Scope, Send

from matrx_connect.client_ip import client_ip
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_connect.emitters.stream_emitter import StreamEmitter
from matrx_connect.routing import AuthenticatedResourceRoute
from ..authority_retry import DEFAULT_SESSION_ATTEMPT_SECONDS, FreshFlight
from ..file_session import FileSessionCredential
from ..session_authority import (
    CredentialAuthorityUnavailable,
    CurrentSessionDecision,
    credential_unavailable_response,
)

# Every name the former single-module ``middleware/auth.py`` defined, re-exported unchanged.
from .types import (
    _is_uuid as _is_uuid,
    _ADMISSION_REASON_CODES as _ADMISSION_REASON_CODES,
    ADMISSION_REFUSAL_CODES as ADMISSION_REFUSAL_CODES,
    GuestResolver as GuestResolver,
    ApiKeyIdentity as ApiKeyIdentity,
    ApiKeyRefused as ApiKeyRefused,
    ApiKeyResolver as ApiKeyResolver,
    RequestScopeHook as RequestScopeHook,
    API_KEY_BEARER_PREFIX as API_KEY_BEARER_PREFIX,
    DEFAULT_ORG_EXEMPT_PATHS as DEFAULT_ORG_EXEMPT_PATHS,
    compile_organization_exempt_pattern as compile_organization_exempt_pattern,
    _matches_organization_exempt as _matches_organization_exempt,
    is_organization_exempt_path as is_organization_exempt_path,
    compile_authenticated_resource_pattern as compile_authenticated_resource_pattern,
    _unsafe_encoded_path as _unsafe_encoded_path,
    is_authenticated_resource_route as is_authenticated_resource_route,
    OrganizationNotFound as OrganizationNotFound,
    OrganizationArchived as OrganizationArchived,
    ApiKeyOrganizationMismatch as ApiKeyOrganizationMismatch,
    AdminResolver as AdminResolver,
    AdminLevelResolver as AdminLevelResolver,
    OrgResolver as OrgResolver,
    AdminLaneAdmission as AdminLaneAdmission,
    ADMIN_LANE_HEADER as ADMIN_LANE_HEADER,
    RecordGrantAdmission as RecordGrantAdmission,
    AdminLaneAuditUnavailable as AdminLaneAuditUnavailable,
    ADMISSION_FAILURE_KEY as ADMISSION_FAILURE_KEY,
    ADMIN_LANE_AUDIT_UNAVAILABLE as ADMIN_LANE_AUDIT_UNAVAILABLE,
    ADMIN_LANE_UNVERIFIABLE as ADMIN_LANE_UNVERIFIABLE,
    _ADMIN_LANE_FAILURES as _ADMIN_LANE_FAILURES,
    _admission_failure as _admission_failure,
    JWKS_REFRESH_COOLDOWN_SECONDS as JWKS_REFRESH_COOLDOWN_SECONDS,
    COOKIE_DRIFT_LOG_WINDOW_SECONDS as COOKIE_DRIFT_LOG_WINDOW_SECONDS,
    VerifiedToken as VerifiedToken,
    _READ_METHODS as _READ_METHODS,
)
from .api_key import ApiKeyLane
from .file_cookie import FileCookieLane
from .gate import OrganizationGate
from .guest import GuestLane
from .jwt import JwtLane, refused_token_context
from .organization import OrganizationLane
from .token_cache import TokenCacheLane
from .websocket import WebSocketAdmission


def request_id_from_header(value: str | None) -> str:
    """The request's id: the client's ``X-Request-ID`` when it is a UUID, else a fresh one.

    A client that mints the id before it sends (the new chat's Stop, P1-CHAT) can cancel the run by it at the
    press, before the response headers come back; ``POST /ai/cancel/{id}`` holds a cancel for a run not open yet."""
    candidate = (value or "").strip()
    return candidate if _is_uuid(candidate) else str(uuid.uuid4())


class AuthMiddleware(
    ApiKeyLane,
    JwtLane,
    TokenCacheLane,
    OrganizationLane,
    GuestLane,
    FileCookieLane,
    OrganizationGate,
    WebSocketAdmission,
):
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
        If the resolver returns None, or no resolver is provided and no
        claim is present, no organization is admitted: ``organization_id``
        stays unset, ``organization_admission`` names why, and the
        organization gate refuses it on a non-exempt path (a named reason
        such as ``organization_required``, HTTP 400 / WebSocket 4400) —
        never a personal-scope fallback.
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
        # EXACT route paths that are NEVER exempt, even under an exempt prefix
        # above: a route whose work must be filed in an organization.
        organization_required_routes: tuple[str, ...] = (),
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
        self._organization_required_patterns = tuple(
            compile_organization_exempt_pattern(entry) for entry in organization_required_routes
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
        from ..session_cookie import register_session_cookie_secret

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
        request_id = request_id_from_header(request.headers.get("x-request-id"))

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
            # The refusal says WHY when the token told us (expired, session ended): still anonymous, still a 401.
            return refused_token_context(ctx)

        guest_ctx = await self._guest_lane(request, ctx, fingerprint_id)
        if guest_ctx is not None:
            return guest_ctx

        cookie_ctx = await self._file_cookie_lane(request, ctx)
        if cookie_ctx is not None:
            return cookie_ctx

        return ctx
