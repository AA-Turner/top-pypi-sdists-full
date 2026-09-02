"""
Role-Based Access Control (RBAC) middleware and decorators.

Single source of truth for authentication and authorization in InnoDay.
All routers import get_current_user and verify_org_membership from here.
"""

import re
from functools import wraps
from typing import Callable, Optional

from fastapi import Depends, HTTPException, Request, status
from sqlmodel import Session, func, select

from src.database import get_session
from src.database.rls import enforce_for_user
from src.domain.organization import (
    Organization,
    OrganizationMembership,
    OrganizationRole,
    role_satisfies,
)
from src.domain.user import User
from src.middleware.token_auth import (
    UnverifiedEmailError,
    resolve_user_from_request,
)

#: Path parameters that hold an organization reference, in precedence order.
_ORG_PARAMS = ("organization_id", "org_id")
#: ...and a project reference. Every `{project_id}` in the API sits under a
#: literal `/projects/` segment, so the name is unambiguous.
_PROJECT_PARAMS = ("project_id",)
#: ...and a ticket reference, so a board key (`BPAI-402`) works anywhere the
#: numeric id does. Normalised here for the reason this function exists: the
#: handlers keep `ticket_id: int` and are unchanged, because the value is
#: rewritten before FastAPI binds it.
_TICKET_PARAMS = ("ticket_id",)

_UUID = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I
)


def normalize_path_refs(request: Request, org: Organization, session: Session) -> None:
    """Replace alias path parameters with the UUIDs they resolve to.

    **Why this exists.** `resolve_organization`/`resolve_project` accept a UUID,
    an alias or a name, so every org-scoped route *reads* as alias-tolerant. It
    is not. The guard resolves the entity for **authorization** and hands back an
    `Organization`, but the handler's own `org_id` / `project_id` argument is
    still bound from the raw path, and 105 handlers go on to filter with it:

        select(Release).where(Release.organization_id == org_id)   # raw param

    Those columns hold UUIDs. Given an alias the filter matches nothing, and the
    route answers **HTTP 200 with an empty list** -- proven on
    `GET /organizations/{org}/releases`, which reported PF as having no releases
    at all while it had three. A confidently wrong answer, worse than the 404 a
    stricter route would have given. Where the ref is used for a lookup instead
    of a filter (`scopes`, `tickets`) the same cause surfaces as a spurious 404.

    **Why here rather than in the handlers.** Editing 105 handlers fixes today's
    routes and nothing else; the next handler written will use the raw param
    again, because using it is the obvious thing and nothing pushes back. Doing
    it in the guard makes correct the default and needs no author to remember.

    **The ordering this relies on, and how it is pinned.** FastAPI's
    `solve_dependencies` resolves sub-dependencies *before* it binds the
    handler's own path parameters, so mutating `request.scope["path_params"]`
    here is visible to the handler. That is real but undocumented behaviour --
    `tests/test_resolved_entity_paths.py` drives it through `TestClient` end to
    end, so an upstream change that reorders the two turns the suite red rather
    than silently restoring the empty-list bug.

    Normalising the **org** costs nothing: it was resolved a line above either
    way. The **project** costs one indexed lookup, and only when the value is not
    already a UUID -- which, for every CLI-issued request since #634, it is. The
    **ticket** is the same trade: a digits-only id short-circuits, and only a board
    key like `BPAI-402` pays for a lookup.

    **This reaches path parameters only.** A `project_id` arriving as a query
    parameter or a body field needs `resolve_project_ref` called by hand, and
    `tests/test_project_refs_are_resolved.py` fails when one does not -- otherwise
    the "nothing pushes back" problem above just moves to those sites, which is
    where it was found ten times over.
    """
    params = request.scope.get("path_params")
    if not isinstance(params, dict):  # pragma: no cover -- always set by routing
        return

    for name in _ORG_PARAMS:
        if name in params:
            params[name] = org.id

    for name in _PROJECT_PARAMS:
        if params.get(name):
            # Through `resolve_project_ref` rather than beside it: one gate on
            # what counts as an already-resolved reference, so a path param and a
            # query param cannot come to disagree about it.
            params[name] = resolve_project_ref(params[name], org.id, session)

    for name in _TICKET_PARAMS:
        if params.get(name):
            # Costs nothing for the common case: `resolve_ticket_ref`
            # short-circuits a digits-only value without touching the database,
            # which is every request the CLI issued before board keys were
            # accepted. Only a board key pays for one indexed lookup.
            params[name] = resolve_ticket_ref(params[name], org.id, session)


def resolve_project_ref(
    ref: Optional[str], org_id: str, session: Session
) -> Optional[str]:
    """Alias, name or id -> project id. `None` in, `None` out.

    For project references that arrive somewhere `normalize_path_refs` cannot
    reach -- a **query parameter** or a **request body field** -- since neither
    is a path param. `?project_id=PF` on `GET .../releases` filtered a UUID
    column by an alias and returned an empty list; `{"project_id": "PF"}` on
    `POST .../releases` reached a **foreign key**: on Postgres
    `releases_project_id_fkey` is validated and not deferrable, so the write was
    refused and the request answered **500** (measured -- see the note in
    `tests/db_helpers.py` on why the SQLite suite sees it persist instead).

    Also the single gate `normalize_path_refs` uses, so the two cannot drift on
    what a valid reference is.

    **It inherits `resolve_project`'s errors, and that is the intent.** An
    unresolvable ref is a **404** and an ambiguous *name* a **409**, on a list
    route as much as on a lookup -- so `?project_id=NOPE` now says so instead of
    answering `200 []`, which is the whole point of the change. Documented under
    "An alias in a URL" in CLAUDE.md, because it is a visible change of contract
    on `GET .../releases` and `GET .../boards`.
    """
    if ref is None:
        return None

    ref = str(ref).strip()
    if not ref:
        return ref

    if _UUID.match(ref):
        # The **stripped** value, deliberately, not the one that arrived. The gate
        # strips before matching, so `<uuid>%20` used to satisfy the short-circuit
        # and then filter a UUID column by `"<uuid> "` -- reaching the empty list
        # this function exists to prevent, through the fast path meant to be free.
        return ref

    # Imported here: `src.routers.projects` imports this module, so a
    # module-level import would close the cycle.
    from src.routers.projects import resolve_project

    return resolve_project(ref, org_id, session).id


_TICKET_ID = re.compile(r"^\d+$")


def resolve_ticket_ref(ref: str, org_id: str, session: Session) -> int:
    """InnoDay ticket id, or a board key like ``BPAI-402`` -> ticket id.

    **The id a person has in hand is almost never the one the API took.**
    ``Ticket.id`` is an auto-increment integer; the board's own key lives in a
    different column (``external_ticket_id``). Every ticket route typed
    ``ticket_id: int``, and nothing outside `board_sync_service` ever looked up an
    external key -- so working from a Linear issue, a branch name or a standup
    note meant listing tickets just to translate ``BPAI-402`` into ``1380`` before
    you could touch it.

    Modelled on `resolve_project_ref`, deliberately: same "reference or id" shape,
    same errors, so the two cannot drift on what a valid reference is. A
    digits-only value is an id and short-circuits -- board keys always carry a
    non-digit (``ALIAS-nnn``), so the two vocabularies cannot collide.

    Matching on the external key is case-insensitive, because the same issue is
    written ``BPAI-402`` in Linear and ``bpai-402`` in a branch name, and a
    reference a human would call identical must not depend on which they copied.

    Unresolvable is a **404** and an ambiguous key a **409**, mirroring
    `resolve_project_ref`. Soft-deleted tickets are excluded: a cancelled row must
    not answer for a key somebody is trying to act on.
    """
    ref = str(ref).strip()
    if not ref:
        raise not_found("Ticket", ref)

    if _TICKET_ID.match(ref):
        return int(ref)

    # Imported here to match `resolve_project_ref`'s reason: routers import this
    # module, so a module-level domain import risks closing a cycle.
    from src.domain.ticket import Ticket

    matches = session.exec(
        select(Ticket).where(
            Ticket.organization_id == org_id,
            func.lower(Ticket.external_ticket_id) == ref.lower(),
            Ticket.deleted_at.is_(None),
        )
    ).all()

    if not matches:
        raise not_found("Ticket", ref)
    if len(matches) > 1:
        # A board key is unique per board, not per org, so two boards in one org
        # can both carry an "ABC-1". Refusing beats acting on whichever row the
        # database happened to return first.
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Ticket '{ref}' is ambiguous -- {len(matches)} tickets in this "
                "organization carry that key. Use the numeric ticket id."
            ),
        )
    return matches[0].id


def resolve_organization(org_ref: str, session: Session) -> Organization:
    """Look up an organization by UUID or alias. Raises 404 if not found."""
    org = (
        session.get(Organization, org_ref)
        or session.exec(
            select(Organization).where(Organization.alias == org_ref)
        ).first()
    )
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization '{org_ref}' not found",
        )
    return org


async def get_current_user(
    request: Request,
    session: Session = Depends(get_session),
) -> User:
    """Resolve the current user, raising 401 if unauthenticated.

    Tries, in order (see src.middleware.token_auth):
      1. Authorization: Bearer idt_/ido_/idr_/innoday_...  (CLI token)
      2. Authorization: Bearer <JWT>        (Supabase, verified via JWKS)
    (A third path once trusted an X-User-ID header verbatim — removed.
     X-Team-Secret is a separate deployment gate, never identity.)
    """
    try:
        user = resolve_user_from_request(request, session)
    except UnverifiedEmailError as exc:
        # A real credential, but the address was never proven. 403 (not 401) with
        # the reason, so the CLI can tell the user to check their email instead of
        # reporting a bad token.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    # From here on the session runs as `innoday_app` with this user's claim, so
    # RLS backs up the membership checks below. No-op unless INNODAY_RLS_ENFORCE
    # is set. Must come after resolution: the token lookup itself has to read
    # `cli_tokens`/`users` before any claim exists.
    enforce_for_user(session, user.id)
    return user


async def get_optional_user(
    request: Request,
    session: Session = Depends(get_session),
) -> Optional[User]:
    """Resolve the current user via any auth source, or None if unauthenticated."""
    try:
        return resolve_user_from_request(request, session)
    except UnverifiedEmailError:
        # Optional-auth callers treat "no user" as anonymous; an unverified
        # credential must not be more privileged than none.
        return None


def verify_org_membership(
    user_id: str,
    organization_id: str,
    session: Session,
    required_role: Optional[OrganizationRole] = None,
) -> OrganizationMembership:
    """
    Verify user is an active member of the organization.

    Platform members (is_platform_member=True) bypass org membership checks.
    """
    user = session.exec(select(User).where(User.id == user_id)).first()
    if user and user.is_platform_member:
        # Platform staff have cross-org access — synthesise a membership
        return OrganizationMembership(
            user_id=user_id,
            organization_id=organization_id,
            role=OrganizationRole.ADMIN,
            is_active=True,
        )

    membership = session.exec(
        select(OrganizationMembership).where(
            OrganizationMembership.user_id == user_id,
            OrganizationMembership.organization_id == organization_id,
            OrganizationMembership.is_active == True,
        )
    ).first()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a member of this organization",
        )

    # `required_role` is a MINIMUM, not an exact match. It used to be `!=`, which meant
    # a route asking for DEVELOPER refused an ADMIN — see ORGANIZATION_ROLE_RANK.
    if required_role and not role_satisfies(membership.role, required_role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Requires {required_role.value} role or higher",
        )

    return membership


def require_org_role(
    minimum: Optional[OrganizationRole] = None,
) -> Callable:
    """FastAPI dependency: authenticated caller who is a member of the path's org.

    Replaces the hand-rolled `resolve_organization(...)` +
    `verify_org_membership(...)` pair that every org-scoped endpoint repeated. As a
    dependency it cannot be forgotten the way a two-line preamble can -- omitting it
    is visible in the signature.

    Reads the org from whichever path parameter the route declares
    (`organization_id` or `org_id` -- both spellings are in use) and returns the
    resolved `Organization`. Platform members bypass membership via
    `verify_org_membership`, which synthesises an ADMIN membership for them.

    Usage:
        org: Organization = Depends(require_org_role())
        org: Organization = Depends(require_org_role(OrganizationRole.ADMIN))
    """

    async def _dep(
        request: Request,
        current_user: User = Depends(get_current_user),
        session: Session = Depends(get_session),
    ) -> Organization:
        params = request.path_params
        # `_ORG_PARAMS`, not the two names inline: they were spelled out here as
        # well, two lines from the tuple that declares them, so adding a third
        # spelling would have normalised it (below) without this line ever
        # finding it -- every route using that name would then hit the deliberate
        # 500 below instead.
        raw = next((params[name] for name in _ORG_PARAMS if params.get(name)), None)
        if not raw:
            # A programming error, not a client error: the route asked for an org
            # guard but declares no org path parameter.
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="require_org_role used on a route with no organization path param",
            )
        org = resolve_organization(str(raw), session)
        verify_org_membership(current_user.id, org.id, session, required_role=minimum)
        normalize_path_refs(request, org, session)
        return org

    return _dep


def not_found(resource: str, ref: str) -> HTTPException:
    """Return a 404 HTTPException with a standard detail message."""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource} '{ref}' not found",
    )


def conflict(resource: str, ref: str) -> HTTPException:
    """Return a 409 HTTPException for duplicate resource."""
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"{resource} '{ref}' already exists",
    )


# `get_org_member` stood here -- a dependency factory returning
# `(org, membership, user, session)`, whose docstring showed how to write an
# org-scoped endpoint with it. No route and no test ever used it, and it could not
# have normalised anything: it took `org_id: str`, not the `Request` whose
# `path_params` must be rewritten. So this module's one piece of documentation
# that read as a recommendation pointed at the pattern `normalize_path_refs`
# exists to retire. Deleted rather than warned about -- a caveat beside a usage
# example is still an invitation. Use `Depends(require_org_role(...))`.


async def get_authenticated_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Require authenticated user or raise 401."""
    return current_user


async def get_admin_user(
    current_user: User = Depends(get_authenticated_user),
) -> User:
    """
    Require admin user or raise 403.
    """
    if not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required"
        )
    return current_user


def require_admin(func):
    """
    Decorator to require admin role for endpoint access.

    Usage:
        @require_admin
        async def admin_only_endpoint(current_user: User = Depends(get_admin_user)):
            # This endpoint requires admin access
            pass
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        # The admin check is handled by the get_admin_user dependency
        return await func(*args, **kwargs)

    return wrapper


def require_auth(func):
    """
    Decorator to require authentication for endpoint access.

    Usage:
        @require_auth
        async def authenticated_endpoint(current_user: User = Depends(get_authenticated_user)):
            # This endpoint requires authentication
            pass
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        # The auth check is handled by the get_authenticated_user dependency
        return await func(*args, **kwargs)

    return wrapper


class RBACPermissions:
    """
    Role-based access control permissions checker.
    """

    @staticmethod
    def can_manage_licenses(user: User) -> bool:
        """Check if user can manage licenses."""
        return user.is_admin()

    @staticmethod
    def can_manage_users(user: User) -> bool:
        """Check if user can manage other users."""
        return user.is_admin()

    @staticmethod
    def can_configure_system(user: User) -> bool:
        """Check if user can configure system settings."""
        return user.is_admin()

    @staticmethod
    def can_view_analytics(user: User) -> bool:
        """Check if user can view system analytics."""
        return user.is_admin()

    @staticmethod
    def can_manage_integrations(user: User) -> bool:
        """Check if user can manage integrations."""
        return user.is_admin()


def check_permission(permission_func):
    """
    Decorator factory for custom permission checks.

    Usage:
        @check_permission(RBACPermissions.can_manage_licenses)
        async def license_endpoint(current_user: User = Depends(get_authenticated_user)):
            # This endpoint requires license management permission
            pass
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract current_user from kwargs
            current_user = kwargs.get("current_user")
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required",
                )

            if not permission_func(current_user):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions",
                )

            return await func(*args, **kwargs)

        return wrapper

    return decorator
