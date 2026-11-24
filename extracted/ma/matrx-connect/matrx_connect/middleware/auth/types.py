"""Shared auth types, errors, constants and organization-exempt path helpers.

Moved verbatim from the former ``middleware/auth.py`` (PF-AUTH S2); re-exported
from ``matrx_connect.middleware.auth``."""

from __future__ import annotations

import functools
import re
import uuid
from collections.abc import Awaitable, Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import Any, Protocol
from urllib.parse import unquote


from matrx_connect.context.app_context import AppContext
from matrx_connect.routing import AuthenticatedResourceRoute
from ..session_authority import (
    CurrentSessionDecision,
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
    #: The limits the key's maker set (which tables, read or write; calls per minute / per day), as the host
    #: resolver read them from the key row. ``None`` = no limits: the key reaches what its identity reaches.
    #: Carried opaquely into ``metadata["api_key_limits"]``; the host enforces it.
    limits: dict | None = None
    #: A personal key's staff level on the host's MCP server (``mcp.full_access`` | ``developer`` |
    #: ``senior_admin`` | ``super_admin``), as the key row says; None = a member there. The host caps
    #: it by the person's current level on every admission. This middleware never reads it: REST
    #: admission of a key carries no admin tier.
    mcp_level: str | None = None


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


@functools.cache
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

    Memoized (a pure function of ``entry``; a compiled pattern is immutable; a refused entry
    raises every time): ``is_organization_exempt_path`` compiles the whole route table on EVERY
    call, and ``re``'s own 512-entry cache cannot hold a ~1,000-route table, so the API contract
    emitter spent ~300 s re-parsing the same regexes (3.3 M compiles, 2026-11-17).
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
    required: tuple[re.Pattern[str], ...] = (),
) -> bool:
    """The ONE organization-exemption matching rule.

    ``prefixes`` are segment-bounded prefixes; ``patterns`` are compiled EXACT
    routes. Nothing else matches. ``required`` are compiled EXACT routes that are
    never exempt, whatever prefix covers them: a route under an exempt prefix whose
    work must be filed in an organization (a streamed run the runtime journals —
    ``/admin/rag/search-lab/diagnose/stream``, 2026-11-16) declares it, so the gate,
    the API contract and the client all say "required" for it.
    """
    if any(pattern.match(path) for pattern in required):
        return False
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
    required_routes: tuple[str, ...] = (),
) -> bool:
    """Ask the REAL matcher whether ``path`` is exempt.

    For hosts and guard tests: same rule, same code, no middleware instance.
    ``exempt_paths`` are prefixes; ``exempt_routes`` are exact routes;
    ``required_routes`` are exact routes that are never exempt.
    """
    return _matches_organization_exempt(
        path,
        tuple(exempt_paths),
        tuple(compile_organization_exempt_pattern(entry) for entry in exempt_routes),
        tuple(compile_organization_exempt_pattern(entry) for entry in required_routes),
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
# Returning None means "the claimed org is not valid for this user": no
# organization is admitted (``organization_admission="denied"``) and the
# organization gate refuses it on a non-exempt path — there is no personal fallback
# (policies/context-is-carried-never-rebuilt.md).  When the host does not supply a resolver, the
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
