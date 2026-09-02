"""The ``/ui`` routes: sign in, the dashboard, the profile, and CLI tokens.

Route order is load-bearing. ``/ui/{org_ref}`` matches a bare org alias, so every
literal page name must be registered *before* it or an org aliased "login" would
shadow the sign-in page. Starlette matches in declaration order, and
``RESERVED_UI_SEGMENTS`` is the belt to that braces -- so a reserved segment 404s
even if the declaration order is ever disturbed.

Unknown org and not-a-member both answer **404, not 403**: telling a non-member
"this org exists but you may not see it" leaks the org list to anyone who can
guess aliases.
"""

import hmac
import logging
import os
import time
from datetime import date, datetime, timedelta, timezone
from typing import Dict, List, Optional
from urllib.parse import quote, unquote

from fastapi import APIRouter, Depends, Form, Query, Request
from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
    RedirectResponse,
    Response,
)
from sqlalchemy import func
from sqlmodel import Session, select

from src.database import get_session
from src.domain.cli_token import CLIToken
from src.domain.organization import (
    Organization,
    OrganizationMembership,
    OrganizationRole,
    role_satisfies,
)
from src.domain.project import Project, ProjectRepository, RepositoryLayer
from src.domain.release import Release
from src.domain.scrum import ScrumKind
from src.domain.signup_request import SignupRequest, SignupRequestStatus
from src.domain.ticket import Ticket, TicketStatus
from src.domain.user import User
from src.domain.user_identity import IdentityPlatform, MatchSource, UserIdentity
from src.page_paths import (
    AUTH_CALLBACK_PATH,
    JOIN_PATH,
    LOGIN_PATH,
    LOGOUT_PATH,
    RESERVED_UI_SEGMENTS,
    SESSION_PATH,
    UI_PREFIX,
    dashboard_path,
    project_path,
    team_path,
    workflow_path,
)
from src.routers.webui import render, workflow
from src.routers.webui.data import (
    DEFAULT_STATUSES,
    MAX_EXTRA_TOPICS,
    admin_count,
    alias_is_available,
    can_open,
    contributors_by_project,
    done_unreleased_for,
    done_unreleased_totals_for,
    live_summaries_for,
    member_organizations,
    my_done_recently_for,
    my_pull_requests,
    my_tickets,
    profile_rows,
    project_cards,
    project_tickets,
    project_tickets_for,
    project_timeline,
    release_board,
    scrum_activity_today,
    summary_panel,
    team_members,
    topic_preview,
    unmapped_counts_for,
    unowned_todo_for,
    viewer_has_any_handle,
    viewer_has_identity,
)
from src.routers.webui.session import (
    COOKIE_NAME,
    SESSION_TOKEN_NAME,
    clear_session,
    issue_session,
    revoke_session,
    user_from_request,
)
from src.services import scrum_service
from src.services.release_pipeline import promote_backlog_in, retarget
from src.services.release_planning import release_being_cut
from src.services.summary_service import unmapped_handles
from src.services.supabase_invite import (
    google_sign_in_url,
    magic_link_configured,
    send_magic_link,
)
from src.services.user_provisioning import (
    UserProvisioningError,
    provision_user,
    resend_invite,
)
from src.utils.time_windows import format_target_date

logger = logging.getLogger(__name__)

router = APIRouter(prefix=UI_PREFIX, tags=["web-ui"], include_in_schema=False)


def _route(path: str) -> str:
    """A ``page_paths`` constant expressed relative to this router's prefix.

    The decorators are written in terms of the constants rather than repeating the
    literals, so ``LOGIN_PATH`` and the route that serves it cannot drift apart.
    That drift is not a visible failure -- it is a link in an email that 404s
    (issue #414), which is the whole reason ``src/page_paths.py`` exists.
    """
    return path.removeprefix(UI_PREFIX)


# Supabase's built-in mailer is capped at 2 sends/hour project-wide and that
# figure is not raisable, so an unauthenticated POST that triggers email is a real
# way to burn the org's entire front door. One request per address per interval.
# In-process, therefore per worker -- a floor, not a guarantee.
_OTP_COOLDOWN_SECONDS = 60
# Above this many tracked addresses, sweep the expired ones before adding more.
_OTP_TRACKING_LIMIT = 1024

# Lifetime of a token minted from the dashboard. Long enough not to be a chore,
# short enough that an abandoned laptop's token is not indefinite.
TOKEN_EXPIRY_DAYS = 90

# How many of a project's tickets the Tickets tab shows. A browse, not an
# accounting -- unlike "your tickets", which is uncapped because a person has to
# be able to trust it is the whole list. The pane says when it has truncated.
PROJECT_TICKET_LIMIT = 200

# The Releases tab's two caps. The backlog is a planning pool, so a long tail of
# stale unversioned tickets is noise rather than information; the history is what
# issue #523 asked for in as many words ("the last 10 releases").
RELEASE_BACKLOG_LIMIT = 100
RELEASE_HISTORY_LIMIT = 10

# One bucket per email-sending route, so a person throttled on sign-in can still
# ask for access. Same shape, so the sweep below serves both.
_last_request: Dict[str, Dict[str, float]] = {"otp": {}, "join": {}}


def _throttled(bucket: str, address: str) -> bool:
    """Whether this address asked too recently. Records the attempt if not.

    In-process, therefore per worker -- a floor, not a guarantee. It exists
    because both callers send email on an unauthenticated POST, and email is a
    finite, shared, per-project resource: an unthrottled send is a way to burn
    the whole team's front door.
    """
    seen = _last_request[bucket]
    now = time.monotonic()
    last = seen.get(address)
    if last is not None and now - last < _OTP_COOLDOWN_SECONDS:
        return True

    # Without this the dict grows one key per distinct address forever, and both
    # routes are reachable by anyone -- so "distinct addresses seen" is
    # attacker-controlled.
    if len(seen) > _OTP_TRACKING_LIMIT:
        for stale in [a for a, t in seen.items() if now - t >= _OTP_COOLDOWN_SECONDS]:
            del seen[stale]

    seen[address] = now
    return False


def _html(markup: str, status_code: int = 200) -> HTMLResponse:
    # no-store: these pages are per-user and one of them renders a secret exactly
    # once. A shared cache holding either would be a disclosure.
    return HTMLResponse(
        markup, status_code=status_code, headers={"Cache-Control": "no-store"}
    )


def _to_login() -> RedirectResponse:
    return RedirectResponse(LOGIN_PATH, status_code=303)


def _not_found() -> HTMLResponse:
    """The single 404 body. Unknown org and not-a-member share it deliberately:
    a distinguishable 403 would confirm an org exists to someone who only
    guessed its alias."""
    return _html("<h1>404 &mdash; not found</h1>", status_code=404)


def _cookies_secure(request: Request) -> bool:
    """Whether to mark the session cookie Secure.

    A Secure cookie is never sent over plain http, so hardcoding it would make
    local development silently fail to hold a session. Behind Railway's proxy the
    scheme arrives in ``X-Forwarded-Proto``.
    """
    forwarded = request.headers.get("x-forwarded-proto", "")
    scheme = forwarded.split(",")[0].strip() or request.url.scheme
    return scheme == "https"


# --------------------------------------------------------------------------- #
# Flash notices
#
# A POST that changes something answers 303, and the page it lands on says what
# happened. The notice therefore has to survive one redirect.
#
# It rides in a **cookie**, not a query string. The text includes an exception's
# own message on the failure path, and a query parameter is a value the caller
# chooses -- reflecting one back into the page would mean rendering caller-
# controlled text on every load of a URL anyone can hand out. ``esc()`` would
# neutralise the markup, but nothing stops a crafted link from putting an
# arbitrary sentence in InnoDay's voice on InnoDay's page.
#
# Deleted the moment it is read, so a notice appears exactly once and a refresh
# shows the page rather than yesterday's result.
# --------------------------------------------------------------------------- #

_FLASH_COOKIE = "innoday_flash"
# Long enough to survive the redirect, short enough that a notice never outlives
# the action that produced it -- a tab restored tomorrow must not announce a sync.
_FLASH_MAX_AGE = 30
# Well inside the ~4KB per-cookie limit, with room for the name and attributes.
_FLASH_MAX_CHARS = 500


def _set_flash(response: Response, request: Request, message: str, ok: bool) -> None:
    """Attach a one-shot notice to a redirect.

    Truncated, because the failure path interpolates an exception's own message
    and those have no length bound. A browser silently drops a cookie past its
    ~4KB limit, so an untruncated notice would not be a long notice -- it would
    be no notice, on exactly the path where the user most needs one.
    """
    if len(message) > _FLASH_MAX_CHARS:
        message = message[: _FLASH_MAX_CHARS - 1] + "\u2026"
    # Percent-encoded, because a Set-Cookie header is **latin-1** and this text
    # is not: the success message contains an em-dash, so an unencoded value
    # raised UnicodeEncodeError on every *successful* sync -- the common path.
    # Encoding also neutralises `;` and newlines, either of which would
    # otherwise let a message truncate its own cookie or inject an attribute.
    response.set_cookie(
        _FLASH_COOKIE,
        quote(f"{'1' if ok else '0'}:{message}", safe=""),
        max_age=_FLASH_MAX_AGE,
        httponly=True,
        secure=_cookies_secure(request),
        samesite="lax",
        path=UI_PREFIX,
    )


def _take_flash(request: Request) -> Optional[tuple]:
    """Read the pending notice as ``(message, ok)``, or None.

    Reading does not clear it -- only a *response* can do that, so the caller
    pairs this with ``_clear_flash`` on whatever it returns. Split apart because
    the render helpers build their response after the notice is needed.
    """
    raw = request.cookies.get(_FLASH_COOKIE)
    if not raw:
        return None
    raw = unquote(raw)
    flag, _, message = raw.partition(":")
    if not message:
        return None
    return (message, flag == "1")


def _clear_flash(response: Response) -> None:
    """Drop a consumed notice. ``path`` must match the one it was set with."""
    response.delete_cookie(_FLASH_COOKIE, path=UI_PREFIX)


_UNDO_COOKIE = "innoday_undo"


def _set_undo(
    response: Response, request: Request, ticket_id, previous: str, was: str
) -> None:
    """Attach a one-shot undo to a redirect: which ticket, and what to restore.

    A cookie rather than a query parameter, for the same reason the notice beside
    it is: a crafted link could otherwise hand someone an "Undo" button that
    writes a version of the sender's choosing. The values here are structured and
    re-validated server-side, but a URL that offers a write is a URL worth not
    minting.

    ``previous`` is what the form said the ticket held before, and ``was`` what it
    actually held. They differ only if something changed the ticket between the
    page rendering and the button being pressed -- ``was`` wins, so undo restores
    what was really replaced rather than what a stale page believed.
    """
    if str(was) == str(previous) and not was:
        # Nothing was displaced, so there is nothing to put back.
        return
    response.set_cookie(
        _UNDO_COOKIE,
        quote(f"{ticket_id}:{was}", safe=""),
        max_age=_FLASH_MAX_AGE,
        httponly=True,
        secure=_cookies_secure(request),
        samesite="lax",
        path=UI_PREFIX,
    )


def _take_undo(request: Request) -> Optional[tuple]:
    """The pending undo as ``(ticket_id, version)``, or None."""
    raw = request.cookies.get(_UNDO_COOKIE)
    if not raw:
        return None
    ticket_id, _, version = unquote(raw).partition(":")
    if not ticket_id:
        return None
    return (ticket_id, version)


def _clear_undo(response: Response) -> None:
    response.delete_cookie(_UNDO_COOKIE, path=UI_PREFIX)


def _redirect_with_flash(
    request: Request, location: str, message: str, ok: bool
) -> RedirectResponse:
    """The standard answer to a POST that changed something: 303 plus a notice."""
    response = RedirectResponse(location, status_code=303)
    _set_flash(response, request, message, ok)
    return response


def _origin_or(return_to: Optional[str], fallback: str) -> str:
    """Where to send the browser back to after a POST.

    The form states it in a hidden ``return_to`` field, because the server
    cannot otherwise know: ``Referer`` is optional, strippable, and absent under
    common privacy settings, so a handler that trusted it would silently land
    people on the dashboard some of the time and nowhere reproducible.

    **Validated to a path inside this router before use.** An unchecked value out
    of a request body is an open redirect, and "it came from our own form" is a
    property of the form we rendered, not of the request that arrived. Anything
    that fails the check falls back rather than erroring -- a wrong destination
    is worth a redirect to a right one, not a 400 in the middle of a sync that
    already succeeded.

    The ``//`` test rejects ``/ui//evil.example.com``: browsers read a leading
    double slash as protocol-relative, so that is an absolute URL wearing a
    prefix this router would otherwise accept.
    """
    candidate = (return_to or "").strip()
    if not candidate.startswith(UI_PREFIX + "/"):
        return fallback
    if "//" in candidate or "\\" in candidate:
        return fallback
    return candidate


def _looks_unconfirmed(result) -> bool:
    """Whether a failed magic link means "never confirmed" rather than "broken".

    GoTrue reports it as `422 signup_disabled`, which reads like a
    misconfiguration and is really "this person has an identity and never
    clicked their link". Matched on the error text as well as the status because
    the status alone is reused for other validation failures, and re-inviting on
    one of those would email somebody for no reason.
    """
    if result.configured is False:
        return False
    text = (result.error or "").lower()
    return result.status_code == 422 and "signup" in text


def _supabase_configured() -> bool:
    """Whether this deployment can send a sign-in link at all."""
    return magic_link_configured()


def _app_url(request: Request) -> str:
    """Public base URL for building the magic-link redirect."""
    configured = os.getenv("APP_URL")
    if configured:
        return configured.rstrip("/")
    return str(request.base_url).rstrip("/")


# --------------------------------------------------------------------------- #
# Sign in / out
# --------------------------------------------------------------------------- #


@router.get(_route(LOGIN_PATH))
async def login_form(
    request: Request, session: Session = Depends(get_session)
) -> Response:
    """The sign-in card, or a bounce to the dashboard if already signed in."""
    if not _supabase_configured():
        return _html(render.unconfigured_page())
    if user_from_request(request, session) is not None:
        return RedirectResponse(UI_PREFIX, status_code=303)
    return _html(render.login_page(google_url=google_sign_in_url(_app_url(request))))


@router.post(_route(LOGIN_PATH))
async def request_sign_in_link(
    request: Request,
    email: str = Form(...),
    session: Session = Depends(get_session),
) -> Response:
    """Email an existing user a sign-in link.

    Renders the same confirmation whatever happens -- unknown address, throttled,
    upstream failure. Any difference between those responses is an oracle for
    which addresses have accounts.

    **The address is matched against InnoDay's own users table before Supabase is
    called at all.** The admin endpoint that sends the link creates an
    ``auth.users`` row for an address it doesn't recognise rather than refusing,
    so handing it unvalidated input from a public form would let a stranger
    provision an identity -- and then, by following the link, a mirror InnoDay
    user, since ``_user_from_supabase_jwt`` creates one on first sight. Our own
    table is the allowlist, and checking it costs one indexed lookup.
    """
    if not _supabase_configured():
        return _html(render.unconfigured_page())

    address = email.strip().lower()
    if not address:
        return _html(
            render.login_page(
                error="Enter an email address.",
                google_url=google_sign_in_url(_app_url(request)),
            )
        )

    if _throttled("otp", address):
        return _html(render.login_sent_page(address))

    known = session.exec(select(User).where(func.lower(User.email) == address)).first()
    if known is None:
        # Same page as a success. Signing up is invite-only (src/routers/invites.py),
        # and this route must never be the thing that creates an account.
        logger.info("webui sign-in link requested for an unknown address")
        return _html(render.login_sent_page(address))

    result = send_magic_link(
        address, redirect_to=_app_url(request) + AUTH_CALLBACK_PATH
    )

    # **The dead end this exists to remove.** `/auth/v1/otp` cannot reach someone
    # whose identity exists but was never confirmed: with `[auth] enable_signup =
    # false` GoTrue routes their magic link through its *signup* path and answers
    # `422 signup_disabled`. Before this, the page still said "check your email"
    # and no email ever came -- so from their side the platform was silently,
    # permanently broken, and the only way out was an operator noticing a log
    # line. `resend_invite` is the admin path, which works with signup disabled.
    #
    # The fallback runs only for an address already matched against our own users
    # table above, so it cannot provision anyone. And both branches render the
    # same page as an unknown address does -- otherwise "which of these got a
    # different answer" becomes an oracle for who has an account.
    if not result.sent and _looks_unconfirmed(result):
        logger.info("webui sign-in fell back to a fresh invite for a known user")
        error = resend_invite(address)
        if error:
            logger.warning("webui sign-in invite fallback failed: %s", error)
    elif not result.sent:
        # Logged, not shown. The person still sees "check your email" -- but a
        # silent failure here is exactly how a login page can be broken for
        # everyone while looking like it works, so it must reach the operator.
        logger.warning(
            "webui sign-in link not sent (configured=%s status=%s error=%s)",
            result.configured,
            result.status_code,
            result.error,
        )

    return _html(render.login_sent_page(address))


@router.post(_route(SESSION_PATH))
async def establish_session(
    request: Request,
    session: Session = Depends(get_session),
) -> Response:
    """Exchange a verified Supabase JWT for a session cookie.

    Called by the ``/ui/auth/callback`` page, which is the only place the token
    exists -- Supabase returns it in the URL *fragment*, which browsers never send
    to a server, so the page has to read it in JS and post it back here.

    The JWT is verified through the same JWKS path every other route uses; an
    unverified one resolves no user and gets a 401.
    """
    from src.middleware.token_auth import _user_from_supabase_jwt

    payload = await request.json()
    access_token = (payload or {}).get("access_token")
    if not access_token:
        return Response(status_code=400)

    try:
        user = _user_from_supabase_jwt(access_token, session)
    except Exception:
        user = None
    if user is None:
        return Response(status_code=401)

    response = Response(status_code=204)
    issue_session(response, session, user, secure=_cookies_secure(request))
    return response


@router.post(_route(LOGOUT_PATH))
async def logout(request: Request, session: Session = Depends(get_session)) -> Response:
    """Revoke this browser's session token and clear the cookie."""
    raw_token = request.cookies.get(COOKIE_NAME)
    if raw_token:
        revoke_session(session, raw_token)
    response = _to_login()
    clear_session(response)
    return response


# --------------------------------------------------------------------------- #
# Request access
# --------------------------------------------------------------------------- #


def _team_secret_ok(supplied: str) -> bool:
    """Constant-time check against the deployment's team secret.

    Returns False when the secret is unset rather than letting everyone through.
    A deployment with no `TEAM_ACCESS_SECRET` is one where this page has no gate
    at all, and "no gate configured" must never read as "gate passed" -- that is
    the failure mode where a local default silently ships to production.
    """
    secret = os.getenv("TEAM_ACCESS_SECRET", "")
    if not secret:
        return False
    return hmac.compare_digest(supplied, secret)


@router.get(_route(JOIN_PATH))
async def join_form(request: Request) -> Response:
    """Ask for access, holding the team secret.

    Deliberately not linked from the sign-in card. It is for people who cannot
    sign in yet, and pointing everyone else at it only invites guesses.
    """
    if not os.getenv("TEAM_ACCESS_SECRET"):
        return _html(render.join_unavailable_page())
    return _html(render.join_page())


@router.post(_route(JOIN_PATH))
async def request_access(
    request: Request,
    email: str = Form(...),
    team_secret: str = Form(...),
    full_name: str = Form(""),
    note: str = Form(""),
    session: Session = Depends(get_session),
) -> Response:
    """Two outcomes, and the difference is the whole design.

    **Already has an account** -- send a fresh invite immediately. Someone
    already decided to let this person in; they are only stuck because their
    Supabase identity was never confirmed, and `[auth] enable_signup = false`
    makes the ordinary sign-in path answer 422 for exactly that state. Nothing
    to approve, so nothing is queued.

    **No account** -- queue a request. The team secret is shared, static, and
    attributable to nobody, so holding it is evidence of proximity to the team,
    not of authorisation. A platform member turns it into an account.

    These two answers differ, which does tell a holder of the team secret
    whether an address has an account. That is an acceptable trade: they already
    hold a team credential, and telling someone "your request is with an admin"
    when in fact an email is on its way would be a worse failure.
    """
    if not os.getenv("TEAM_ACCESS_SECRET"):
        return _html(render.join_unavailable_page())

    address = email.strip().lower()
    if not address:
        return _html(render.join_page(error="Enter an email address."))

    if not _team_secret_ok(team_secret):
        # One message for a wrong secret, whatever the address. Anything else
        # turns this form into an oracle for valid secrets.
        logger.warning("webui join attempted with an invalid team secret")
        return _html(
            render.join_page(error="That team secret is not right.", email=address)
        )

    if _throttled("join", address):
        return _html(render.join_submitted_page(address, queued=False))

    known = session.exec(select(User).where(func.lower(User.email) == address)).first()
    if known is not None:
        error = resend_invite(address)
        if error:
            logger.warning("webui join re-invite failed for a known user: %s", error)
        return _html(render.join_submitted_page(address, queued=False))

    existing = session.exec(
        select(SignupRequest).where(
            func.lower(SignupRequest.email) == address,
            SignupRequest.status == SignupRequestStatus.PENDING,
        )
    ).first()
    if existing is None:
        session.add(
            SignupRequest(
                email=address,
                full_name=(full_name.strip() or address.split("@")[0])[:100],
                note=(note.strip() or None),
            )
        )
        session.commit()
        logger.info("webui signup request queued")

    return _html(render.join_submitted_page(address, queued=True))


# --------------------------------------------------------------------------- #
# Dashboard
# --------------------------------------------------------------------------- #


@router.get("")
async def dashboard_root(
    request: Request, session: Session = Depends(get_session)
) -> Response:
    """Send a signed-in user to the workflow page for their default org.

    **This lands on the workflow launcher, not the dashboard.** Signing in used
    to open a page that answers "how are things?" -- counts, sync freshness, next
    release -- when the question someone arrives with is "what do I want to do?".
    The dashboard has not moved and is still `/ui/{org}`; what changed is which
    of the two is the front door.

    Which *org* is still `users.default_organization_id`, unchanged: the star in
    the org switcher sets it, and without it someone in four orgs landed on
    whichever sorted first by name every time.
    """
    user = user_from_request(request, session)
    if user is None:
        return _to_login()

    orgs = member_organizations(session, user)
    if not orgs:
        return _html(render.no_orgs_page(user))

    chosen = next(
        (o for o in orgs if o.id == user.default_organization_id),
        orgs[0],
    )
    return RedirectResponse(workflow_path(chosen.alias or chosen.id), status_code=303)


def _resolve_org(org_ref: str, session: Session, user: User) -> Optional[Organization]:
    """An org this user may open, by alias (any case) or UUID -- else ``None``.

    The alias comparison lowercases **both sides**. Only the auto-derived path,
    ``Organization.generate_alias``, lowercases; an alias supplied explicitly to
    ``POST /api/v1/organizations`` is stored verbatim, so aliases like ``PF`` do
    exist. Matching a lowercased URL segment against the stored value directly
    would make such an org unreachable at *every* spelling of its own URL --
    including the one this app builds for it after sign-in.

    Reserved segments never resolve, so a page name can't be shadowed by an alias.
    """
    if org_ref.lower() in RESERVED_UI_SEGMENTS:
        return None

    org = session.exec(
        select(Organization).where(func.lower(Organization.alias) == org_ref.lower())
    ).first() or session.get(Organization, org_ref)

    if org is None or not org.is_active:
        return None
    if not can_open(session, user, org.id):
        return None
    return org


def _active_cli_tokens(session: Session, user_id: str):
    """The user's live tokens, excluding browser sessions.

    Session rows are hidden because nobody created them on purpose, and offering
    "revoke" beside the session you are currently using is a trap.
    """
    return list(
        session.exec(
            select(CLIToken)
            .where(
                CLIToken.user_id == user_id,
                CLIToken.revoked_at == None,  # noqa: E711
                CLIToken.name != SESSION_TOKEN_NAME,
            )
            .order_by(CLIToken.created_at)
        ).all()
    )


def _pending_signup_requests(session: Session, user: User) -> list:
    """The access queue -- empty for anyone who cannot act on it.

    Queried per render rather than cached: it is one indexed lookup, and a stale
    queue would show an approver a request another admin already handled.
    """
    if not user.is_platform_member:
        return []
    return list(
        session.exec(
            select(SignupRequest)
            .where(SignupRequest.status == SignupRequestStatus.PENDING)
            .order_by(SignupRequest.created_at)
        ).all()
    )


def _render_dashboard(
    session: Session,
    user: User,
    org: Organization,
    *,
    new_token: Optional[str] = None,
    notice: Optional[tuple] = None,
    personal_for: Optional[str] = None,
    request: Optional[Request] = None,
) -> HTMLResponse:
    """Render the dashboard. ``notice`` is an optional ``(message, ok)`` banner.

    ``personal_for`` is the project id whose scrum panel should show "Yours"
    instead of the team roll-up -- the ``?you=`` parameter. Per project rather
    than page-wide, so switching one card's panel leaves the rest alone.
    """
    # `project_cards` already selected every project in this org; re-selecting
    # them here ran the identical query twice per dashboard load. The card
    # carries the row it was built from for exactly this.
    # An explicit notice wins: a caller that has just done something is saying
    # what happened, and the cookie is only how a *redirected* caller says it.
    if notice is None and request is not None:
        notice = _take_flash(request)

    cards = project_cards(session, org.id)
    project_ids = [card.id for card in cards]
    unmapped = unmapped_counts_for(session, project_ids)
    # Two queries for every card's summaries, not two per card. `project_cards`
    # and `unmapped_counts_for` above were both batched for this reason; the
    # panel reads were the one thing in this function that still scaled with the
    # number of projects (#501).
    summaries = live_summaries_for(session, project_ids, user.id)
    # Two queries for every card's contributors, not two per card -- same reason
    # the three lookups above it are batched.
    people = contributors_by_project(session, project_ids)
    panels = {
        card.id: summary_panel(
            session,
            card.project,
            user,
            prefer_personal=(card.id == personal_for),
            unmapped_counts=unmapped,
            prefetched=summaries,
        )
        for card in cards
        if card.project is not None
    }
    response = _html(
        render.dashboard_page(
            user=user,
            org=org,
            orgs=member_organizations(session, user),
            cards=cards,
            tokens=_active_cli_tokens(session, user.id),
            new_token=new_token,
            notice=notice,
            panels=panels,
            contributors=people,
            signup_requests=_pending_signup_requests(session, user),
        )
    )
    # Whether or not there was one: clearing an absent cookie is a no-op, and
    # the alternative is a branch that has to stay in step with the caller that
    # read it.
    _clear_flash(response)
    _clear_undo(response)
    return response


# --------------------------------------------------------------------------- #
# Profile
#
# Declared BEFORE `/{org_ref}` for the reason at the top of this module. These
# are two-segment paths, so Starlette would not in fact confuse them with a bare
# alias today -- but "literal routes come first" is the rule that keeps that
# true, and the day someone adds a `/ui/profile` shortcut is the day an org
# aliased "profile" silently shadows it. `RESERVED_UI_SEGMENTS` is the second
# guard, and refuses the alias outright.
# --------------------------------------------------------------------------- #


def _render_profile(
    session: Session,
    user: User,
    org: Organization,
    *,
    notice: Optional[tuple] = None,
) -> HTMLResponse:
    return _html(
        render.profile_page(
            user=user,
            org=org,
            orgs=member_organizations(session, user),
            rows=profile_rows(session, user, org.id),
            notice=notice,
        )
    )


@router.get("/{org_ref}/profile")
async def profile(
    org_ref: str, request: Request, session: Session = Depends(get_session)
) -> Response:
    """Your GitHub login, and which board handle is you on each project."""
    user = user_from_request(request, session)
    if user is None:
        return _to_login()

    org = _resolve_org(org_ref, session, user)
    if org is None:
        return _not_found()

    return _render_profile(session, user, org)


@router.post("/{org_ref}/profile/github")
async def set_github_username(
    org_ref: str,
    request: Request,
    github_username: str = Form(default=""),
    session: Session = Depends(get_session),
) -> Response:
    """Set (or clear) ``users.github_username``.

    Goes through ``User.update_integration_status`` -- the same method
    ``PUT /api/v1/users/{id}/integrations`` calls -- rather than assigning the
    column here. One writer, so the two surfaces cannot drift on what
    "connected" means.

    Always the caller's own row. The page has no notion of editing someone
    else's profile, and a `user_id` form field would be an authorisation
    question that does not need to exist.
    """
    user = user_from_request(request, session)
    if user is None:
        return _to_login()

    org = _resolve_org(org_ref, session, user)
    if org is None:
        return _not_found()

    handle = github_username.strip().lstrip("@")
    row = session.get(User, user.id)
    row.update_integration_status(
        service="github", connected=bool(handle), username=handle or None
    )
    session.add(row)
    session.commit()

    return _render_profile(
        session,
        row,
        org,
        notice=(
            (f"GitHub login set to {handle}.", True)
            if handle
            else ("GitHub login cleared.", True)
        ),
    )


@router.post("/{org_ref}/profile/identities")
async def claim_board_handle(
    org_ref: str,
    request: Request,
    project_id: str = Form(...),
    platform: str = Form(...),
    handle: str = Form(default=""),
    session: Session = Depends(get_session),
) -> Response:
    """Claim a board handle on one project, for the signed-in user.

    Delegates the rule to ``IdentityResolutionService.claim_identity`` rather
    than re-deriving it: a handle already linked to someone else **in this
    organisation** is refused, in every one of its projects, because a handle
    identifies one human. Another org's claim on the same string is not a
    conflict and never was one -- see ``find_conflicting_claim``. The message
    names the *conflict* and never the person: "who else is on this board?" is
    not a question a claim form should answer, and it would be an enumeration
    oracle for anyone who can guess display names.

    An existing project-scoped claim by this same user is replaced, which is
    what "override" means on the page. The conflict check runs **before** the
    delete, so a rejected claim leaves the current mapping intact rather than
    clearing it on the way to failing.
    """
    from src.services.identity_resolution import (
        HandleAlreadyClaimedError,
        IdentityResolutionService,
    )

    user = user_from_request(request, session)
    if user is None:
        return _to_login()

    org = _resolve_org(org_ref, session, user)
    if org is None:
        return _not_found()

    project = session.get(Project, project_id)
    if project is None or project.organization_id != org.id:
        return _not_found()

    try:
        chosen = IdentityPlatform(platform)
    except ValueError:
        return _html("<h1>400 &mdash; unknown platform</h1>", status_code=400)

    wanted = handle.strip()
    if not wanted:
        return _render_profile(
            session, user, org, notice=("Enter the name the board uses.", False)
        )

    conflict = IdentityResolutionService.find_conflicting_claim(
        session,
        user_id=user.id,
        platform=chosen,
        handle=wanted,
        organization_id=org.id,
        project_id=project.id,
    )
    if conflict is not None:
        return _render_profile(
            session,
            user,
            org,
            notice=("That handle is already linked to another user", False),
        )

    # Only now that the claim is known to be accepted: one handle per person per
    # project, so the previous one goes.
    for stale in session.exec(
        select(UserIdentity).where(
            UserIdentity.user_id == user.id,
            UserIdentity.project_id == project.id,
            UserIdentity.platform == chosen,
            UserIdentity.handle != wanted,
        )
    ).all():
        session.delete(stale)
    session.flush()

    try:
        IdentityResolutionService.claim_identity(
            session,
            user_id=user.id,
            platform=chosen,
            handle=wanted,
            organization_id=org.id,
            project_id=project.id,
            match_source=MatchSource.MANUAL,
        )
    except HandleAlreadyClaimedError:
        # Belt to the check above's braces: another request could have claimed
        # it in between. Roll back rather than leaving the delete committed.
        session.rollback()
        return _render_profile(
            session,
            user,
            org,
            notice=("That handle is already linked to another user", False),
        )

    session.commit()
    return _render_profile(
        session,
        user,
        org,
        notice=(f"{project.alias}: you are {wanted} on this board.", True),
    )


# --------------------------------------------------------------------------- #
# Dashboard (parameterized -- must stay last of the GETs)
# --------------------------------------------------------------------------- #


def _resolve_project(
    session: Session, org: Organization, project_alias: str
) -> Optional[Project]:
    """One project by its alias within this org, or None.

    Alias rather than UUID because ``Project.alias`` is unique *per organization*
    (``uq_project_org_alias``) and the org is the segment above it -- so the pair
    is exactly as unambiguous as an id, and reads as what people call the thing.
    Case-insensitive: aliases are stored uppercase because they are ticket
    prefixes, while the URL carries them lowercased.
    """
    return session.exec(
        select(Project).where(
            Project.organization_id == org.id,
            func.lower(Project.alias) == project_alias.lower(),
        )
    ).first()


def _render_project(
    session: Session,
    user: User,
    org: Organization,
    project: Project,
    *,
    tab: str,
    request: Optional[Request] = None,
    bump: Optional[str] = None,
    statuses: Optional[List[str]] = None,
    release: Optional[str] = None,
) -> HTMLResponse:
    """One project page. ``tab`` is already validated by the route that calls it."""
    # Which statuses the Tickets tab is filtered to. `None` means "no filter in
    # the URL", which is every status -- an unfiltered address must not hide work.
    # An explicit empty list is a real ask with an empty answer, kept distinct.
    selected_values = (
        [s.value for s in DEFAULT_STATUSES]
        if statuses is None
        else [v for v in statuses if v in {s.value for s in DEFAULT_STATUSES}]
    )
    chosen_statuses = [TicketStatus(v) for v in selected_values]

    # The board is needed by two tabs now: Releases renders it, and Tickets uses
    # its two slots for the release chips and for what the plan button targets.
    board = (
        release_board(
            session,
            project.id,
            backlog_limit=RELEASE_BACKLOG_LIMIT,
            history_limit=RELEASE_HISTORY_LIMIT,
        )
        if tab in ("releases", "tickets")
        else None
    )
    # Planning adds to the **next** release -- "drag into next sprint". The
    # current one is being cut; adding to it mid-flight is a different decision
    # and not one a hover arrow should make.
    plan_target = board.planned.release.version if board and board.planned else None
    query = ""
    if request is not None and request.url.query:
        query = f"?{request.url.query}"
    # `project_cards` builds every card in the org and this page needs one. That
    # is a real cost and a deliberate one: the function is already batched, this
    # is a single page load, and a second single-project variant would be another
    # thing to keep correct alongside it.
    cards = project_cards(session, org.id)
    card = next((c for c in cards if c.id == project.id), None)
    if card is None:
        return _not_found()

    panel = summary_panel(session, project, user, prefer_personal=True)
    identity = next(
        (
            row
            for row in profile_rows(session, user, org.id)
            if row.project_id == project.id
        ),
        None,
    )
    has_identity = viewer_has_identity(session, user, project)
    handles_mapped = viewer_has_any_handle(session, user)

    # Only the pane on show is queried. The tabs are separate URLs precisely so
    # that "the project's 200 tickets" is not a cost paid by someone reading
    # their own five.
    response = _html(
        render.project_page(
            user=user,
            org=org,
            orgs=member_organizations(session, user),
            card=card,
            tab=tab,
            panel=panel,
            identity=identity,
            tickets=my_tickets(session, project.id, user.id) if tab == "you" else (),
            pull_requests=(
                my_pull_requests(session, project.id, user) if tab == "you" else ()
            ),
            has_identity=has_identity,
            handles_mapped=handles_mapped,
            open_tickets=card.in_progress + card.in_review,
            all_tickets=(
                project_tickets(
                    session,
                    project.id,
                    limit=PROJECT_TICKET_LIMIT,
                    statuses=chosen_statuses,
                    release=release,
                )
                if tab == "tickets"
                else ()
            ),
            selected_statuses=selected_values,
            release_filter=release,
            plan_target=plan_target,
            return_to=str(request.url.path) + query if request is not None else None,
            ticket_limit=PROJECT_TICKET_LIMIT,
            release_board=board,
            release_history_limit=RELEASE_HISTORY_LIMIT,
            proposed_bump=bump if tab == "releases" else None,
            # Two tabs render controls that need it -- Releases (date, version
            # line, plan buttons) and Tickets (plan button) -- so the membership
            # lookup is paid on those and skipped elsewhere. DEVELOPER, not
            # ADMIN: see `_may_edit_release` for why the date and the version
            # line now hold the same bar as the API's release update.
            can_edit_release=(
                _may_edit_release(session, org, user)
                if tab in ("releases", "tickets")
                else False
            ),
            full_timeline=(
                project_timeline(session, project.id, user.id)
                if tab == "timeline"
                else ()
            ),
            project=project,
            notice=_take_flash(request) if request is not None else None,
            undo=_take_undo(request) if request is not None else None,
        )
    )
    _clear_flash(response)
    _clear_undo(response)
    return response


async def _org_repos(session: Session, org: Organization):
    """Every repository in the org's GitHub account, with its topics.

    **One request for the whole form.** GitHub's org listing already returns each
    repo's `topics` on the standard Accept header, so the topic list, the counts
    and the preview all come out of a single call -- rather than one search per
    topic, which is what discovery does at sync time because it is matching, not
    enumerating.

    Returns `(repos, ok)`. `ok` is False when the org has no usable GitHub
    credential, which is a different thing from an org with no repositories and
    is rendered differently: one is "set this up", the other is "nothing tagged".
    """
    from src.services.github_connect_service import GitHubConnectService

    service = GitHubConnectService(session)
    api = service._client_for_org(org.id)
    if api is None:
        return [], False
    github_org = (org.settings or {}).get("github_org") or org.alias
    try:
        return await api.get_all_organization_repositories(github_org), True
    except Exception as exc:  # noqa: BLE001 - surfaced on the page, not swallowed
        logger.warning("webui new-project repo listing failed for %s: %s", org.id, exc)
        return [], False


def _github_org_name(org: Organization) -> Optional[str]:
    """The GitHub account this org's repos live under.

    Explicit config first: it is not derivable from the alias (`atomic` ->
    `atomicpe`), which is exactly why `organizations.settings['github_org']`
    exists.
    """
    return (org.settings or {}).get("github_org") or org.alias


def _membership(session: Session, org: Organization, user_id: str):
    """One active membership, or None."""
    return session.exec(
        select(OrganizationMembership).where(
            OrganizationMembership.organization_id == org.id,
            OrganizationMembership.user_id == user_id,
            OrganizationMembership.is_active == True,  # noqa: E712
        )
    ).first()


def _has_org_role(
    session: Session, org: Organization, user: User, minimum: OrganizationRole
) -> bool:
    """Whether this viewer meets ``minimum`` in this org.

    One implementation behind the named questions below. Uses the capability
    ranking rather than `role == minimum`: the ranking exists because an equality
    check once locked admins out of nine routes that asked for DEVELOPER. A
    platform member satisfies every bar, which is what `is_platform_member` means.

    The named wrappers stay separate rather than collapsing into calls to this:
    they are what a route reads as, and "may this person edit a release" is a
    question the codebase should be able to answer in one place when the answer
    changes.
    """
    if getattr(user, "is_platform_member", False):
        return True
    membership = _membership(session, org, user.id)
    return membership is not None and role_satisfies(membership.role, minimum)


def _is_org_admin(session: Session, org: Organization, user: User) -> bool:
    """Whether this viewer may manage the team, or destroy something."""
    return _has_org_role(session, org, user, OrganizationRole.ADMIN)


def _may_move_tickets(session: Session, org: Organization, user: User) -> bool:
    """Whether this viewer may change a ticket in this org.

    **The same bar as the API, for the same effect.** Every ticket write in
    `src/routers/tickets.py` requires `DEVELOPER`, and `OrganizationRole.MEMBER`
    is documented as "Read tickets, view summaries". Recording a personal update
    was an inert note when that gate was written; it now writes `status`,
    `completed_at`, `assigned_to` and pushes to a client's board, so the two
    surfaces have to agree. A `/ui` route being page-internal is not a reason to
    hold a lower bar than the API for the same write.
    """
    return _has_org_role(session, org, user, OrganizationRole.DEVELOPER)


def _may_edit_release(session: Session, org: Organization, user: User) -> bool:
    """Whether this viewer may change a release on this project.

    **One rule across the whole release surface: editing is DEVELOPER,
    destroying is ADMIN.** It replaces three different answers to the same
    question, which is how the most consequential control on the page ended up
    being the least protected one:

    | Action | Was | Now |
    |---|---|---|
    | Move the version line (`releases/version`) | *no gate at all* | DEVELOPER |
    | Set a target date (`releases/date`) | ADMIN | DEVELOPER |
    | Plan a ticket into a release | *no gate at all* | DEVELOPER (`_may_move_tickets`) |
    | Create / update over the API | DEVELOPER | DEVELOPER, unchanged |
    | Withdraw / delete | ADMIN | ADMIN, unchanged |

    Retargeting was the worst of the three: it renames the version every
    repository is about to be tagged with *and* rewrites every ticket planned
    into it, and any member of the org could do it. A target date, meanwhile, was
    held to a higher bar than the rename -- so the page protected the label and
    not the thing the label names.

    Distinct from `_may_move_tickets` despite the identical bar today. They are
    different questions about different objects, and collapsing them would mean a
    future change to one silently moving the other.
    """
    return _has_org_role(session, org, user, OrganizationRole.DEVELOPER)


#: What a MEMBER gets from every release control on the Releases tab. One string,
#: because the three controls now hold one bar and telling a person a different
#: story per button is how the bar stopped looking like a rule.
_CANNOT_EDIT_RELEASE = (
    "Changing a release needs the developer role in this organization."
)


#: What a MEMBER gets from the two routes that now mutate tickets. 403 rather
#: than 404: the org is one they can open, and pretending otherwise would
#: contradict the page they are looking at.
_CANNOT_MOVE_TICKETS = {
    "error": (
        "Recording moves needs the developer role in this organization — "
        "a member can read tickets but not change them."
    )
}


def _render_team(
    session: Session,
    user: User,
    org: Organization,
    *,
    request: Optional[Request] = None,
    notice: Optional[tuple] = None,
) -> HTMLResponse:
    can_admin = _is_org_admin(session, org, user)
    # `session.exec` yields scalars for a single-column select, not 1-tuples.
    project_ids = list(
        session.exec(select(Project.id).where(Project.organization_id == org.id)).all()
    )
    if notice is None and request is not None:
        notice = _take_flash(request)
    response = _html(
        render.team_page(
            user=user,
            org=org,
            orgs=member_organizations(session, user),
            members=team_members(session, org.id, user),
            unmapped=unmapped_handles(session, org.id, project_ids),
            can_admin=can_admin,
            last_admin=admin_count(session, org.id) <= 1,
            notice=notice,
        )
    )
    _clear_flash(response)
    _clear_undo(response)
    return response


@router.get("/{org_ref}/team")
async def team(
    org_ref: str,
    request: Request,
    session: Session = Depends(get_session),
) -> Response:
    """The org roster. Everyone may look; only admins may change anything."""
    user = user_from_request(request, session)
    if user is None:
        return _to_login()
    org = _resolve_org(org_ref, session, user)
    if org is None:
        return _not_found()
    return _render_team(session, user, org, request=request)


@router.post("/{org_ref}/team/members/{member_id}/role")
async def set_member_role(
    org_ref: str,
    member_id: str,
    request: Request,
    role: str = Form(...),
    session: Session = Depends(get_session),
) -> Response:
    """Change a member's role.

    **Refuses to demote the last admin.** An org with no admin is an org nobody
    can add one to, and there is no way back from the UI. Checked here rather
    than only hidden in the template: the disabled control is a courtesy, this is
    the guarantee.
    """
    user = user_from_request(request, session)
    if user is None:
        return _to_login()
    org = _resolve_org(org_ref, session, user)
    if org is None:
        return _not_found()
    if not _is_org_admin(session, org, user):
        return _not_found()

    try:
        chosen = OrganizationRole(role.upper())
    except ValueError:
        return _not_found()

    membership = _membership(session, org, member_id)
    if membership is None:
        return _not_found()

    dest = team_path(org.alias or org.id)
    if (
        membership.role == OrganizationRole.ADMIN
        and chosen != OrganizationRole.ADMIN
        and admin_count(session, org.id) <= 1
    ):
        return _redirect_with_flash(
            request, dest, "That is the only admin — promote someone else first.", False
        )

    membership.role = chosen
    session.add(membership)
    session.commit()
    return _redirect_with_flash(
        request, dest, f"Role updated to {chosen.value.lower()}.", True
    )


@router.post("/{org_ref}/team/members/{member_id}/remove")
async def remove_member(
    org_ref: str,
    member_id: str,
    request: Request,
    session: Session = Depends(get_session),
) -> Response:
    """Remove someone from the organization.

    **Deactivates, never deletes.** Their tickets, identities and summaries all
    point at the user row; deleting the membership would leave that work
    attributed to somebody the org no longer lists, which is worse than a row
    marked inactive. Re-inviting reactivates rather than duplicating.
    """
    user = user_from_request(request, session)
    if user is None:
        return _to_login()
    org = _resolve_org(org_ref, session, user)
    if org is None:
        return _not_found()
    if not _is_org_admin(session, org, user):
        return _not_found()

    dest = team_path(org.alias or org.id)
    if member_id == user.id:
        return _redirect_with_flash(request, dest, "You cannot remove yourself.", False)

    membership = _membership(session, org, member_id)
    if membership is None:
        return _not_found()
    if membership.role == OrganizationRole.ADMIN and admin_count(session, org.id) <= 1:
        return _redirect_with_flash(
            request, dest, "That is the only admin — promote someone else first.", False
        )

    membership.is_active = False
    session.add(membership)
    session.commit()
    return _redirect_with_flash(request, dest, "Removed from this organization.", True)


@router.post("/{org_ref}/team/map")
async def map_handle(
    org_ref: str,
    request: Request,
    kind: str = Form(...),
    handle: str = Form(...),
    user_id: str = Form(""),
    session: Session = Depends(get_session),
) -> Response:
    """Say who a board or commit handle belongs to.

    A **commit** handle writes `users.github_username` -- the same column the
    profile page writes, so there is one place a GitHub handle lives. A **board**
    handle writes a `UserIdentity` scoped to nothing in particular (the handle is
    the same across the org's projects), matching what the profile page's
    self-service claim already does.

    Both are reversible from the profile page. A wrong mapping reattributes
    somebody else's work in every summary that follows, so it must not be a
    one-way door.
    """
    user = user_from_request(request, session)
    if user is None:
        return _to_login()
    org = _resolve_org(org_ref, session, user)
    if org is None:
        return _not_found()
    if not _is_org_admin(session, org, user):
        return _not_found()

    dest = team_path(org.alias or org.id)
    handle = handle.strip()
    if not user_id or not handle:
        return _redirect_with_flash(request, dest, "Pick who that handle is.", False)

    target = session.get(User, user_id)
    if target is None or _membership(session, org, user_id) is None:
        return _not_found()

    if kind == "commit":
        target.github_username = handle
        session.add(target)
    else:
        session.add(
            UserIdentity(
                user_id=target.id,
                platform=IdentityPlatform.LINEAR,
                handle=handle,
                match_source=MatchSource.MANUAL,
            )
        )
    session.commit()
    return _redirect_with_flash(
        request, dest, f"{handle} is now {target.full_name or target.email}.", True
    )


@router.get("/{org_ref}/projects/new")
async def new_project_form(
    org_ref: str,
    request: Request,
    session: Session = Depends(get_session),
) -> Response:
    """The create-a-project form.

    Declared **before** ``/{org_ref}/projects/{project_alias}`` so "new" cannot be
    read as a project alias. Starlette matches in declaration order, and that
    ordering is the whole guard -- a project aliased "new" would otherwise shadow
    this page.
    """
    user = user_from_request(request, session)
    if user is None:
        return _to_login()

    org = _resolve_org(org_ref, session, user)
    if org is None:
        return _not_found()

    repos, github_ok = await _org_repos(session, org)
    return _html(
        render.new_project_page(
            user=user,
            org=org,
            orgs=member_organizations(session, user),
            preview=topic_preview(repos, "", []),
            values={},
            chosen=[],
            max_extra=MAX_EXTRA_TOPICS,
            github_org=_github_org_name(org),
            github_ok=github_ok,
        )
    )


@router.post("/{org_ref}/projects/new")
async def create_project_page(
    org_ref: str,
    request: Request,
    name: str = Form(""),
    alias: str = Form(""),
    description: str = Form(""),
    intent: str = Form("preview"),
    topic: List[str] = Form(default=[]),
    session: Session = Depends(get_session),
) -> Response:
    """Preview the repositories a project would pull in, or create it.

    Two intents on one route so the preview can round-trip without JavaScript and
    without losing anything already typed. A GET-based preview would have had to
    carry every field in the query string; a scripted one would have made the
    whole form depend on scripting to be usable at all.
    """
    user = user_from_request(request, session)
    if user is None:
        return _to_login()

    org = _resolve_org(org_ref, session, user)
    if org is None:
        return _not_found()

    name = name.strip()
    alias = alias.strip()
    description = description.strip()
    # Trim to the form's own limit rather than silently honouring more: every
    # topic is another GitHub search on every discovery run.
    chosen = [t.strip().lower() for t in topic if t.strip()][:MAX_EXTRA_TOPICS]

    repos, github_ok = await _org_repos(session, org)

    def _form(error: Optional[str] = None) -> Response:
        return _html(
            render.new_project_page(
                user=user,
                org=org,
                orgs=member_organizations(session, user),
                preview=topic_preview(repos, alias, chosen),
                values={"name": name, "alias": alias, "description": description},
                chosen=chosen,
                max_extra=MAX_EXTRA_TOPICS,
                github_org=_github_org_name(org),
                github_ok=github_ok,
                error=error,
            ),
            status_code=200 if error is None else 400,
        )

    if intent != "create":
        return _form()

    if not name or not alias:
        return _form("A name and an alias are both required.")
    if not alias.replace("-", "").replace("_", "").isalnum():
        return _form("An alias may contain only letters, numbers, - and _.")
    # `new` sits where an alias would in the URL, so a project called that would
    # shadow this very form. The other reserved words are org-level, but an alias
    # matching one produces `/ui/x/projects/login` -- confusing rather than
    # broken, and cheap to refuse.
    if alias.lower() == "new" or alias.lower() in RESERVED_UI_SEGMENTS:
        return _form(f"“{alias}” is reserved. Choose another alias.")
    if not alias_is_available(session, org.id, alias):
        return _form(f"This organization already has a project aliased “{alias}”.")

    from src.services.project_service import ProjectService

    try:
        project = await ProjectService(session).create_project(
            organization_id=org.id,
            name=name,
            # The column is NOT NULL, and an empty description is a worse record
            # than an honest placeholder someone can edit.
            description=description or f"{name} ({alias.upper()})",
            alias=alias.upper(),
        )
    except Exception as exc:  # noqa: BLE001 - shown on the form, not a stack trace
        logger.warning("webui project create failed in %s: %s", org.id, exc)
        return _form(f"Could not create the project: {exc}")

    if chosen:
        # Extra topics are stored per project on the ORG, because that is where
        # `WorkspaceOnboardService.github_topics()` reads them from. Copy-on-write
        # rather than mutating in place: `settings` is a JSON column, and SQLModel
        # does not see an in-place dict edit as a change to persist.
        settings = dict(org.settings or {})
        topics = dict(settings.get("github_topics") or {})
        topics[project.alias] = ",".join(chosen)
        settings["github_topics"] = topics
        org.settings = settings
        session.add(org)
        session.commit()

    return _redirect_with_flash(
        request,
        project_path(org.alias or org.id, project.alias),
        f"{project.alias} created. Run `innoday init "
        f"{(org.alias or org.id).lower()}/{project.alias}` to clone its "
        f"repositories and generate its context.",
        True,
    )


@router.get("/{org_ref}/projects/{project_alias}")
async def project(
    org_ref: str,
    project_alias: str,
    request: Request,
    session: Session = Depends(get_session),
) -> Response:
    """One project's own page. Defaults to the "You" tab."""
    user = user_from_request(request, session)
    if user is None:
        return _to_login()
    return _project_view(session, user, org_ref, project_alias, "you", request)


@router.get("/{org_ref}/projects/{project_alias}/{tab}")
async def project_tab(
    org_ref: str,
    project_alias: str,
    tab: str,
    request: Request,
    bump: Optional[str] = None,
    status: Optional[List[str]] = Query(None),
    release: Optional[str] = None,
    session: Session = Depends(get_session),
) -> Response:
    """A named tab of one project's page.

    ``?bump=major`` on the Releases tab renders a *proposal* -- what the two
    forward slots would become -- and writes nothing. A GET that changed the
    version every repo is about to be tagged with would be a GET that a link
    prefetcher could fire.
    """
    user = user_from_request(request, session)
    if user is None:
        return _to_login()
    return _project_view(session, user, org_ref, project_alias, tab, request, bump=bump)


def _project_view(
    session: Session,
    user: User,
    org_ref: str,
    project_alias: str,
    tab: str,
    request: Request,
    bump: Optional[str] = None,
    statuses: Optional[List[str]] = None,
    release: Optional[str] = None,
) -> Response:
    """Resolve org, project and tab for an already-authenticated viewer.

    An unknown tab 404s rather than falling back to "you": a mistyped URL that
    silently renders a different page is how someone concludes a feature is
    broken when they are simply not on it.
    """
    if tab not in render.PROJECT_TABS:
        return _not_found()

    org = _resolve_org(org_ref, session, user)
    if org is None:
        return _not_found()

    project = _resolve_project(session, org, project_alias)
    if project is None:
        # 404, not 403, and the same 404 an unknown org gets: a distinguishable
        # response would confirm the project exists to someone guessing aliases.
        return _not_found()

    return _render_project(
        session,
        user,
        org,
        project,
        tab=tab,
        request=request,
        bump=bump,
        statuses=statuses,
        release=release,
    )


@router.get("/{org_ref}/workflow")
async def workflow_launcher(
    org_ref: str,
    request: Request,
    project: Optional[str] = None,
    session: Session = Depends(get_session),
) -> Response:
    """The workflow launcher -- what signing in opens.

    A launcher rather than a dashboard: pick a project for context, pick a
    workflow, walk its steps. `GET /ui` redirects here.

    ``?project=<id>`` preselects a project, overriding the starred default. It
    exists so a link can point at "this workflow, this project" -- the rail
    itself switches client-side and costs no round trip, which is why every
    project's work is loaded below rather than just the selected one.

    Registered **before** ``/{org_ref}``: that route matches a bare org alias, so
    a literal segment declared after it would never be reached. ``workflow`` is
    in `RESERVED_UI_SEGMENTS` for the same reason, as the second guard.
    """
    user = user_from_request(request, session)
    if user is None:
        return _to_login()

    org = _resolve_org(org_ref, session, user)
    if org is None:
        return _not_found()

    cards = project_cards(session, org.id)
    project_ids = [card.id for card in cards]

    # The eight table reads below are one query each for the whole page, never
    # one per project -- the rule `_render_dashboard` states, and it matters more
    # here because the rail switches projects without a round trip.
    #
    # The last three serve the personal update. They are org-wide constants like
    # the rest, which is the only shape available to them: a fourth read *inside*
    # the per-project comprehension below would push the route past the linearity
    # `test_workflow_page_query_count_grows_with_project_count` pins (it asserts
    # under four extra SELECTs per project and the route already spends three).
    #
    # `summary_panel` is **not** one of them: the comprehension underneath calls
    # it once per project, so the page's total query count still grows with the
    # number of projects (measured: 21 SELECTs at one project, 63 at fifteen --
    # a constant 21 plus 3 per project, of which the fifth read below is one of
    # the constants).
    # That is the dashboard's shape inherited wholesale, and saying otherwise
    # here would be a docstring asserting a property nothing checks --
    # `test_workflow_page_query_count_grows_with_project_count` pins the real
    # behaviour so the claim and the code cannot drift apart. Batching
    # `summary_panel` is worth doing for both pages at once, not for this one.
    unmapped = unmapped_counts_for(session, project_ids)
    summaries = live_summaries_for(session, project_ids, user.id)
    tickets = project_tickets_for(session, project_ids)
    unreleased = done_unreleased_for(session, project_ids)
    # A fifth read, and a `COUNT` rather than a fetch. `done_unreleased_for` is
    # capped per project, so `len()` of what it returns is the size of a page and
    # not a total -- and the steps below state the number in words.
    unreleased_totals = done_unreleased_totals_for(session, project_ids)
    # "Today" is one UTC calendar date, decided here and passed down, because that
    # is the boundary `Scrum.day` is stamped against -- see `domain.scrum`. Read
    # once for the whole page so every project's tick is answered as of the same
    # instant: two calls to `utcnow()` either side of midnight would tick one
    # project's box and clear another's on one render.
    today = datetime.utcnow()
    activity = scrum_activity_today(session, project_ids, user.id, day=today.date())
    reopen = my_done_recently_for(
        session,
        project_ids,
        user.id,
        # Naive UTC, like the column. Measured back from **today's UTC midnight**
        # rather than from the current instant, so the list a person sees does not
        # quietly shed its oldest row as the afternoon goes on -- the window is a
        # number of days, and a day is the unit `Scrum.day` is keyed on too.
        #
        # `REOPEN_WINDOW_DAYS` is the workflow's own constant rather than
        # `LINGER_DAYS` -- the two agree and mean different things; see the
        # comment on its definition.
        since=(
            today.replace(hour=0, minute=0, second=0, microsecond=0)
            - timedelta(days=workflow.REOPEN_WINDOW_DAYS)
        ),
    )
    unowned = unowned_todo_for(session, project_ids, cap=workflow.TAKE_CAP)
    panels = {
        card.id: summary_panel(
            session,
            card.project,
            user,
            unmapped_counts=unmapped,
            prefetched=summaries,
        )
        for card in cards
        if card.project is not None
    }

    # A platform member can open any org without holding a membership row, and
    # `default_project_id` lives *on* that row -- so for them there is nothing to
    # read and nothing `POST .../default-project` could write. The star is hidden
    # rather than shown-and-refused: it used to render, move optimistically under
    # the click, and only then land on a 404 page.
    membership = _membership(session, org, user.id)
    response = _html(
        workflow.workflow_page(
            user=user,
            org=org,
            orgs=member_organizations(session, user),
            cards=cards,
            panels=panels,
            tickets=tickets,
            unreleased=unreleased,
            unreleased_totals=unreleased_totals,
            reopen=reopen,
            unowned=unowned,
            scrum_activity=activity,
            default_project_id=membership.default_project_id if membership else None,
            can_set_default=membership is not None,
            scrums_url=f"{UI_PREFIX}/{(org.alias or org.id).lower()}/scrums",
            selected_project_id=project,
            notice=_take_flash(request),
        )
    )
    _clear_flash(response)
    return response


@router.post("/{org_ref}/default-project")
async def set_default_project(
    org_ref: str,
    request: Request,
    project_id: str = Form(...),
    session: Session = Depends(get_session),
) -> Response:
    """Choose which project the workflow page opens with, for this org.

    The per-project twin of `set_default_org`, and deliberately stored on
    `OrganizationMembership` rather than on `User`: a project default is only
    meaningful inside one org, and a single column on `users` would follow
    someone into an org where it names a project they cannot see. The membership
    row is already uniquely keyed on ``(user_id, organization_id)``, so it needs
    no new table and no new constraint.

    Unlike `set_default_org`, the target is checked against **this** org rather
    than resolved independently: a project is reachable only through the org
    that owns it, so a project_id from elsewhere is not a different-but-valid
    choice the way another org is -- it is someone naming a row they were not
    shown.
    """
    user = user_from_request(request, session)
    if user is None:
        return _to_login()

    org = _resolve_org(org_ref, session, user)
    if org is None:
        return _not_found()

    target = session.get(Project, project_id)
    if target is None or target.organization_id != org.id:
        return _not_found()

    membership = _membership(session, org, user.id)
    if membership is None:
        return _not_found()

    membership.default_project_id = target.id
    session.add(membership)
    session.commit()

    return _redirect_with_flash(
        request,
        workflow_path(org.alias or org.id),
        f"{target.alias} opens by default",
        True,
    )


# --------------------------------------------------------------------------- #
# The scrum walk's writes
#
# The workflow page records a scrum *while the meeting happens* -- opened when
# the walk starts, one row per ticket as each stop ends, closed at wrap-up. Those
# writes have to land somewhere the page can actually reach, and that is here
# rather than `/api/v1`: a browser cannot send `X-Team-Secret`, injecting the
# shared secret into page JavaScript would leak it, and cookie auth is not
# `Authorization: Bearer`. `team_secret.py` exempts `/ui` for exactly this
# reason, so a same-origin `fetch` carrying the session cookie works and an
# `/api/v1` call from the same page could not.
#
# They answer JSON rather than a redirect because they are `fetch` targets, not
# form posts -- but they are `/ui` routes in every other respect, and are gated
# the same way the pages around them are. The `/api/v1` scrum routes are
# untouched and remain the path for the CLI and MCP.
#
# Registered **before** `/{org_ref}`, like every other literal segment here.
# --------------------------------------------------------------------------- #


def _scrum_error(exc: scrum_service.ScrumError) -> JSONResponse:
    """The refusal as JSON, naming the field when the service named one.

    ``field`` is what lets the page put the message beside the box that caused
    it. Without it the script has only a status code and a sentence, so a
    rejected transcript link is announced in a banner at the top of the page
    while the input that produced it looks untouched -- and every retry fails
    the same way, with the meeting's record never written.

    The status comes from `scrum_service.http_status`, which the `/api/v1`
    router also calls. This module used to keep its own copy of that table,
    identical to the other one: two surfaces disagreeing about whether a stale
    tab may close somebody else's scrum is precisely the bug the shared service
    exists to prevent, and two tables is how they would come to.
    """
    body = {"error": str(exc)}
    field = getattr(exc, "field", None)
    if field:
        body["field"] = field
    return JSONResponse(body, status_code=scrum_service.http_status(exc))


async def _json_body(request: Request) -> Dict:
    """The request body as a dict, or an empty one.

    A body that is absent or is not an object is treated as "nothing supplied"
    rather than as an error: every field these routes read is then missing, and
    the checks below refuse on their own terms with a message that names what
    was wrong.
    """
    try:
        payload = await request.json()
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


#: **All three routes below open with the same two gates, spelled out inline:**
#: `user_from_request` for who the caller is, `_resolve_org` for whether they may
#: open this org at all -- which is `can_open`, i.e. an active or platform
#: membership, the plain-membership bar the `/api/v1` scrum routes are gated at.
#: Written out in each route body rather than hidden behind a helper on purpose:
#: `tests/test_auth_tiers.py` reads these bodies, and a guard it cannot see is a
#: guard nobody is checking. The *comment* saying so lives here once; the code it
#: describes is deliberately in all three.
#:
#: What a `fetch` caller gets instead of a redirect to the sign-in page: it would
#: follow a 303 and hand the page's own HTML back to a `.json()` call.
_UNAUTHENTICATED = {"error": "Not signed in"}
#: 404 rather than 403 for an org the viewer may not open, exactly as the pages
#: answer: a distinguishable response would confirm the org exists to somebody
#: guessing aliases.
_NO_SUCH_ORG = {"error": "Organization not found"}


@router.post("/{org_ref}/scrums")
async def open_scrum_run(
    org_ref: str,
    request: Request,
    session: Session = Depends(get_session),
) -> Response:
    """Open (or resume) a record for one project and hand back its id.

    Called as the first writing step opens, not at the finish. A run interrupted
    half way through is the ordinary case, and the record of *that* run is the one
    most worth having -- so the row exists before the first ticket is discussed.

    ``kind`` says **what** is being recorded: a team walk or one person's daily
    update (`domain.scrum.ScrumKind`). It is forwarded as sent and checked by the
    service, like every other value these routes take -- a rule written here is a
    rule the ``/api/v1`` router does not have. Omitted, it is the team walk, which
    is what every caller that predates the second kind means.

    **Idempotent on the day's record**, and it has to be from here: the page
    retries this call after any rejection, and cancelling a walk resets its record
    and re-opens on the next one. `scrum_service.open_scrum` hands back this
    caller's own record for this project, kind and day rather than starting a
    second, so a dropped response does not split a run across two rows and a
    cancelled attempt does not leave one behind that reads as abandoned. 201
    either way -- a client that lost the first answer cannot tell the two apart,
    which is the point.

    **A closed team scrum is not resumed; it gets a new row, and that is also a
    201.** A team may hold two stand-ups in one day, so the second one is a second
    meeting with minutes of its own. "Scrums stay final" is enforced by the finish
    route refusing a second *close*, not here. A personal update is the other way
    round: the day's row comes back closed or not, because correcting it is the
    point (`scrum_service.open_scrum`).

    **This route never answers 409.** `ScrumAlreadyClosed` is the only refusal
    mapped to it and nothing on this path raises one -- the reachable answers are
    401, 404, 422, 403 and 201. Worth stating because the engine's `err.fromOpen`
    guard is justified by that being true, and a docstring here claiming otherwise
    is the one a reader would find first.
    """
    # The two gates, as described above `_UNAUTHENTICATED`.
    user = user_from_request(request, session)
    if user is None:
        return JSONResponse(_UNAUTHENTICATED, status_code=401)
    org = _resolve_org(org_ref, session, user)
    if org is None:
        return JSONResponse(_NO_SUCH_ORG, status_code=404)

    body = await _json_body(request)
    project = session.get(Project, str(body.get("project_id") or ""))
    if project is None or project.organization_id != org.id:
        # Checked against the org this URL resolved to, never against the id in
        # the body: a project from elsewhere is somebody naming a row they were
        # not shown, not a different-but-valid choice.
        return JSONResponse({"error": "Project not found"}, status_code=404)

    try:
        scrum = scrum_service.open_scrum(
            session,
            organization_id=org.id,
            project_id=project.id,
            run_by_user_id=user.id,
            kind=body.get("kind", ScrumKind.SCRUM.value),
        )
    except scrum_service.ScrumError as exc:
        return _scrum_error(exc)

    return JSONResponse({"scrum_id": scrum.id}, status_code=201)


@router.post("/{org_ref}/scrums/{scrum_id}/visits")
async def record_scrum_visit(
    org_ref: str,
    scrum_id: str,
    request: Request,
    session: Session = Depends(get_session),
) -> Response:
    """Record one stop on the walk, as that stop ends.

    One call per ticket and never a batch: collecting the walk client-side and
    posting it at the finish would mean a dropped connection lost the whole
    meeting instead of one ticket.
    """
    # The two gates, as described above `_UNAUTHENTICATED`.
    user = user_from_request(request, session)
    if user is None:
        return JSONResponse(_UNAUTHENTICATED, status_code=401)
    org = _resolve_org(org_ref, session, user)
    if org is None:
        return JSONResponse(_NO_SUCH_ORG, status_code=404)

    # Forwarded as sent, and checked by the service -- not parsed here. The two
    # surfaces have to agree about what a visit may contain, and a rule written
    # in this route is a rule the `/api/v1` router does not have (and the other
    # way round: this route used to truncate an over-long status where the API
    # answered 422 for the same value).
    body = await _json_body(request)
    try:
        scrum = scrum_service.writable_scrum(session, scrum_id, org.id, user.id)
        visit = scrum_service.record_visit(
            session,
            scrum=scrum,
            ticket_id=body.get("ticket_id"),
            position=body.get("position"),
            seconds=body.get("seconds"),
            status_at_visit=body.get("status_at_visit"),
            comment=body.get("comment"),
            moved_to=body.get("moved_to"),
        )
    except scrum_service.ScrumError as exc:
        return _scrum_error(exc)

    return JSONResponse({"visit_id": visit.id}, status_code=201)


@router.post("/{org_ref}/scrums/{scrum_id}/picks")
async def replace_scrum_picks(
    org_ref: str,
    scrum_id: str,
    request: Request,
    session: Session = Depends(get_session),
) -> Response:
    """Set a personal update's picks to exactly what was sent.

    **A whole set, not one pick, and that is the whole reason this route exists
    beside `/visits`.** A per-ticket endpoint can express "add this"; it cannot
    express "and nothing else", so it cannot express somebody *un-ticking* a box.
    With only `/visits`, re-entering the workflow to withdraw a pick left the
    withdrawn pick in the record while the page said the record held what you
    asked for -- a save reported that did not happen, on requirement 6's own path.

    It also makes the write **idempotent**: the page re-sends its complete
    selection on each picker step, so a retry after a partial failure converges
    instead of doubling every pick that had already landed.

    Updates only. A team scrum's visits are stops on a walk, written one at a time
    as the meeting happens so an interrupted run still leaves a trace; replacing
    that set wholesale would delete the first half of a meeting because somebody
    retried the second. `scrum_service.replace_picks` refuses the wrong kind.

    Answers the count it actually stored, so the page can paint a number it was
    told rather than one it assumed.
    """
    # The two gates, as described above `_UNAUTHENTICATED`.
    user = user_from_request(request, session)
    if user is None:
        return JSONResponse(_UNAUTHENTICATED, status_code=401)
    org = _resolve_org(org_ref, session, user)
    if org is None:
        return JSONResponse(_NO_SUCH_ORG, status_code=404)

    # **The third gate, and it is new to this route.** Recording a pick used to be
    # an inert note; submitting now applies it -- `Ticket.status`, `completed_at`,
    # `assigned_to`, and a push to the client's board. That is a ticket mutation,
    # and the API's equivalent requires DEVELOPER.
    if not _may_move_tickets(session, org, user):
        return JSONResponse(_CANNOT_MOVE_TICKETS, status_code=403)

    body = await _json_body(request)
    try:
        scrum = scrum_service.writable_scrum(session, scrum_id, org.id, user.id)
        visits = scrum_service.replace_picks(
            session,
            scrum=scrum,
            sent=body.get("picks", []),
            # Which boxes the page could *see*. Absent means "every visit this
            # record holds", which is the old whole-set behaviour and what any
            # other caller gets; see `replace_picks`.
            offered=body.get("offered"),
        )
    except scrum_service.ScrumError as exc:
        return _scrum_error(exc)

    return JSONResponse({"scrum_id": scrum.id, "recorded": len(visits)})


@router.post("/{org_ref}/scrums/{scrum_id}/finish")
async def finish_scrum_run(
    org_ref: str,
    scrum_id: str,
    request: Request,
    session: Session = Depends(get_session),
) -> Response:
    """Close the scrum: end time, the page's own clock, transcript, notes.

    A separate path rather than the same one that opened it, because closing is
    not idempotent -- `scrum_service.apply_wrap_up` refuses a second close, so a
    stale tab cannot blank minutes that are already final.

    The 409 that refusal produces is *not* a failure to the page, and the script
    treats it as the done state: it is what a retry gets when the response to a
    finish that already committed was dropped in transit, and the scrum really is
    closed. The row this call would have written is the row that is already
    there.
    """
    # The two gates, as described above `_UNAUTHENTICATED`.
    user = user_from_request(request, session)
    if user is None:
        return JSONResponse(_UNAUTHENTICATED, status_code=401)
    org = _resolve_org(org_ref, session, user)
    if org is None:
        return JSONResponse(_NO_SUCH_ORG, status_code=404)

    body = await _json_body(request)
    # Only the keys actually supplied are forwarded, so a wrap-up that fills in
    # the notes cannot blank a transcript URL it never mentioned -- the same
    # `exclude_unset` contract the PATCH route has.
    sent = {
        key: body[key]
        for key in (
            "ended_at",
            "total_seconds",
            "transcript_url",
            "updated_summary_id",
            "lingering_count",
            "notes_markdown",
        )
        if key in body
    }

    try:
        scrum = scrum_service.writable_scrum(session, scrum_id, org.id, user.id)
        scrum = scrum_service.apply_wrap_up(session, scrum=scrum, sent=sent)
    except scrum_service.ScrumError as exc:
        return _scrum_error(exc)

    answer = {
        "scrum_id": scrum.id,
        "visits": scrum_service.visit_count(session, scrum.id),
    }

    # **Closing a personal update is what applies its moves.** The picks are an
    # answer somebody is still editing -- un-ticking a box is the whole reason
    # `replace_picks` reconciles rather than appends -- so moving on each pick
    # would apply changes the person then withdrew. Submitting is the moment they
    # stop editing, and the moves run over what the record holds *then*.
    #
    # After `apply_wrap_up`, not before: the wrap-up is the caller's own data and
    # a refusal to it is a refusal to the whole request, whereas a board being
    # down is not. Ordering it this way keeps the 422s the page paints beside a
    # field separate from the board failures it paints in the banner.
    #
    # A team scrum's visits record what was observed, not what was asked for, so
    # nothing here touches one.
    if scrum.kind == ScrumKind.UPDATE.value:
        # Gated here as well as on `/picks`, and not only for symmetry: a record
        # made while somebody held DEVELOPER must not still apply after they were
        # demoted. Closing the scrum itself is deliberately *not* gated -- a
        # MEMBER may record their own update, they simply may not move tickets
        # with it -- so this refuses the moves and keeps the wrap-up.
        if _may_move_tickets(session, org, user):
            answer.update(
                await scrum_service.apply_recorded_moves(
                    session, scrum=scrum, actor=user
                )
            )
        else:
            answer.update(
                {
                    "applied": False,
                    "moved": 0,
                    "pushed": False,
                    "errors": [_CANNOT_MOVE_TICKETS["error"]],
                    "notices": [],
                }
            )

        # **And the comments, gated on the same check** -- a comment is a board
        # write. The first version of this exempted them on the grounds that
        # "saying something is not changing something", and rested that on the
        # delivery being unreachable for a MEMBER anyway (`/picks` refuses them,
        # so they record nothing to deliver). Both halves were wrong together:
        # the reachable case is somebody **demoted between recording and
        # submitting**, which is the exact case the gate above was written for --
        # their status move was just refused, and in the same response their
        # comment would have been pushed to the client's board. `_may_move_tickets`
        # exists because a `/ui` route being page-internal is not a reason to hold
        # a lower bar than the API for the same write, and that argument does not
        # stop at `Ticket.status`.
        #
        # After the moves, deliberately. A comment usually explains the move
        # ("bringing this back, QA found a regression"), so it should not land on
        # the board ahead of the change it is about.
        if _may_move_tickets(session, org, user):
            answer.update(
                await scrum_service.deliver_recorded_comments(
                    session, scrum=scrum, actor=user
                )
            )
        else:
            answer.update(
                {
                    "commented": 0,
                    # `None`, not `False`. The three-valued convention this
                    # feature defends everywhere means "nothing was sent" --
                    # `False` says a push was attempted and did not land, and
                    # nothing was attempted here. (The moves' branch above spends
                    # `False` on the same refusal; that is pre-existing, and
                    # response-only rather than persisted, so it is left as it is
                    # rather than changed in passing.)
                    "comments_pushed": None,
                    "comment_errors": [_CANNOT_MOVE_TICKETS["error"]],
                    "comment_notices": [],
                }
            )

    return JSONResponse(answer)


@router.get("/{org_ref}")
async def dashboard(
    org_ref: str,
    request: Request,
    you: Optional[str] = None,
    session: Session = Depends(get_session),
) -> Response:
    """One organization: its projects, their repos and next launches, your tokens.

    ``?you=<project_id>`` switches that project's scrum panel to the viewer's
    personal summary. A query parameter rather than a second page: it is the
    same dashboard, and a URL that survives a bookmark is the whole benefit of
    a server-rendered toggle.
    """
    user = user_from_request(request, session)
    if user is None:
        return _to_login()

    org = _resolve_org(org_ref, session, user)
    if org is None:
        return _not_found()

    return _render_dashboard(session, user, org, personal_for=you, request=request)


@router.post("/{org_ref}/tokens")
async def create_token(
    org_ref: str,
    request: Request,
    session: Session = Depends(get_session),
) -> Response:
    """Mint a CLI token, replacing any previous one, and show it exactly once.

    **Replaces rather than adds.** One person, one CLI token: a list of five means
    "which of these is my laptop using?" is unanswerable without revoking them all
    and starting over, and the raw values are unrecoverable so there is no way to
    tell. Creating a new one revokes the old, which is also what someone who has
    lost a token actually wants.

    Name and expiry are derived, not asked. Both were free-text inputs on a form
    whose only real question is "do you want a token" -- and a name nobody chooses
    carefully is worse than a dated one, which at least sorts and explains itself.

    The raw value is rendered rather than redirected to: a redirect would carry the
    secret in a URL, which lands in history and in logs.
    """
    user = user_from_request(request, session)
    if user is None:
        return _to_login()

    org = _resolve_org(org_ref, session, user)
    if org is None:
        return _not_found()

    now = datetime.now(timezone.utc)
    for existing in _active_cli_tokens(session, user.id):
        existing.revoked_at = now
        session.add(existing)
    session.commit()

    from src.routers.auth import default_org_alias, mint_cli_token

    _row, raw_token = mint_cli_token(
        session,
        user_id=user.id,
        name=f"web-{now:%Y-%m-%d}",
        expires_days=TOKEN_EXPIRY_DAYS,
        kind="pat",
        org_alias=default_org_alias(session, user),
    )
    return _render_dashboard(session, user, org, new_token=raw_token)


@router.post("/{org_ref}/projects/{project_alias}/tickets/plan")
async def plan_ticket_into_release(
    org_ref: str,
    project_alias: str,
    request: Request,
    ticket_id: str = Form(...),
    release: str = Form(""),
    previous: str = Form(""),
    return_to: str = Form(""),
    session: Session = Depends(get_session),
) -> Response:
    """Move one ticket into a release -- or back out of it, which is the undo.

    One route serves both directions. ``release=""`` clears the field, so "undo"
    is the same POST with the ticket's previous value, and the notice it lands on
    carries a button that does exactly that. No history to keep and nothing to
    expire: the previous value travels in the form that offers to restore it.

    Writes ``ticket.release`` -- free text, no foreign key -- so this is a plain
    field update rather than a relation. It deliberately does **not** validate
    against the project's releases: the button only ever offers a real version,
    and refusing an unrecognised one here would also refuse the undo that puts a
    ticket back on a version since renamed.
    """
    user = user_from_request(request, session)
    if user is None:
        return _to_login()

    org = _resolve_org(org_ref, session, user)
    if org is None:
        return _not_found()
    project = _resolve_project(session, org, project_alias)
    if project is None:
        return _not_found()

    destination = _origin_or(
        return_to, f"{project_path(org.alias or org.id, project.alias)}/tickets"
    )
    # Writing `ticket.release` is a ticket write, and every ticket write on the
    # API requires DEVELOPER. The page held no bar at all.
    if not _may_move_tickets(session, org, user):
        return _redirect_with_flash(request, destination, _CANNOT_EDIT_RELEASE, False)

    ticket = session.get(Ticket, int(ticket_id)) if ticket_id.isdigit() else None
    # Scoped to this project, not merely to the id: the id arrives in a form and
    # a ticket from another project would otherwise be editable through it.
    if ticket is None or ticket.project_id != project.id:
        return _redirect_with_flash(
            request, destination, "That ticket is not on this project.", False
        )

    was = ticket.release or ""
    ticket.release = release or None

    # Only the in-progress slot promotes: adding to the *next* release is
    # deferring work, and moving its status would say the opposite. The rule
    # itself lives in `release_pipeline` -- the release router asserts the same
    # invariant when a rotation promotes a whole release into this slot.
    promoted = False
    if release:
        cutting = release_being_cut(
            list(
                session.exec(
                    select(Release).where(
                        Release.project_id == project.id,
                        Release.deleted_at.is_(None),
                    )
                ).all()
            )
        )
        if cutting is not None and cutting.version == release:
            session.add(ticket)
            session.flush()
            promoted = bool(promote_backlog_in(session, project.id, release))

    # `touch()` is what puts the ticket at the top of its release: the slot lists
    # order by `updated_at`, so "newest planned first" needs nothing else.
    ticket.touch()
    session.add(ticket)
    session.commit()

    ref = ticket.external_ticket_id or f"#{ticket.id}"
    if release:
        message = f"{ref} planned into {release}."
        if promoted:
            message = f"{ref} planned into {release}, and moved to todo."
    else:
        message = f"{ref} removed from {was}." if was else f"{ref} has no release."

    response = _redirect_with_flash(request, destination, message, True)
    # The undo travels with the notice, as a form the next page renders.
    _set_undo(response, request, ticket.id, previous, was)
    return response


@router.post("/{org_ref}/projects/{project_alias}/releases/version")
async def set_release_version(
    org_ref: str,
    project_alias: str,
    request: Request,
    bump: str = Form(...),
    session: Session = Depends(get_session),
) -> Response:
    """Move the project's two forward slots onto a different version line.

    POST rather than a link, and reached only from the confirm step: this renames
    the version every repository is about to be tagged with and rewrites every
    ticket planned into it. ``retarget`` does both in this request's transaction,
    so they land together or not at all.

    Refusals come back as a flash on the same tab rather than an error page --
    "v2.0.0 already exists on this project" is something to act on, not a
    failure to recover from.
    """
    user = user_from_request(request, session)
    if user is None:
        return _to_login()

    org = _resolve_org(org_ref, session, user)
    if org is None:
        return _not_found()

    project = _resolve_project(session, org, project_alias)
    if project is None:
        return _not_found()

    destination = f"{project_path(org.alias or org.id, project.alias)}/releases"
    if not _may_edit_release(session, org, user):
        return _redirect_with_flash(request, destination, _CANNOT_EDIT_RELEASE, False)

    result = retarget(session, project.id, bump)
    if result.ok:
        session.commit()
    else:
        session.rollback()

    return _redirect_with_flash(request, destination, result.message, result.ok)


@router.post("/{org_ref}/projects/{project_alias}/releases/date")
async def set_release_target_date(
    org_ref: str,
    project_alias: str,
    request: Request,
    version: str = Form(...),
    target_date: str = Form(""),
    session: Session = Depends(get_session),
) -> Response:
    """Set (or clear) the day a release is aimed at. Org admins only.

    **Admin-gated where its neighbours are not**, and deliberately. The bump
    control above rearranges InnoDay's own bookkeeping; a target date is a date
    the team and the client read as a commitment, so who may set one is a
    different question from who may plan a ticket into a sprint. Same rule as the
    team page (`_is_org_admin`), so there is one notion of "admin" on this surface.

    An empty submission clears the date rather than being rejected. A wrong date
    on a shared page is worse than none, so getting back to "not decided yet" has
    to be as easy as setting it -- the same reasoning the unmapped-handle panel
    gives for making mapping reversible.

    The version is matched, not trusted: it names a row *within this project*, so
    a forged value can only ever miss.
    """
    user = user_from_request(request, session)
    if user is None:
        return _to_login()

    org = _resolve_org(org_ref, session, user)
    if org is None:
        return _not_found()

    project = _resolve_project(session, org, project_alias)
    if project is None:
        return _not_found()

    destination = f"{project_path(org.alias or org.id, project.alias)}/releases"
    if not _may_edit_release(session, org, user):
        return _redirect_with_flash(request, destination, _CANNOT_EDIT_RELEASE, False)

    release = session.exec(
        select(Release).where(
            Release.project_id == project.id,
            Release.version == version,
            Release.deleted_at.is_(None),
        )
    ).first()
    if release is None:
        return _redirect_with_flash(
            request, destination, f"{version} is not a release on this project.", False
        )

    raw = (target_date or "").strip()
    if not raw:
        release.target_date = None
        message = f"{release.version} has no target date."
    else:
        try:
            release.target_date = date.fromisoformat(raw)
        except ValueError:
            # `<input type="date">` submits ISO or nothing, so this is a
            # hand-made request rather than a mistake -- but it still gets a
            # sentence rather than a 422 page, since the tab is already open.
            return _redirect_with_flash(
                request,
                destination,
                f"{raw!r} is not a date (expected YYYY-MM-DD).",
                False,
            )
        message = (
            f"{release.version} is aimed at {format_target_date(release.target_date)}."
        )

    session.add(release)
    session.commit()
    return _redirect_with_flash(request, destination, message, True)


@router.post("/{org_ref}/repos/{repo_id}/layer")
async def set_repo_layer(
    org_ref: str,
    repo_id: str,
    request: Request,
    layer: str = Form(...),
    return_to: str = Form(""),
    session: Session = Depends(get_session),
) -> Response:
    """Reclassify a repository within this project.

    Writes ``ProjectRepository.layer`` -- the *per-project* classification, not
    ``Repository.layer``. The same repo can legitimately be the UI layer of one
    project and a library to another, so the org-wide value is left alone as the
    fallback it is.

    The submitted value is checked against the enum rather than trusted: it arrives
    from a form, and an unknown string would either raise on the enum cast or, on
    SQLite, persist a layer nothing can render.
    """
    user = user_from_request(request, session)
    if user is None:
        return _to_login()

    org = _resolve_org(org_ref, session, user)
    if org is None:
        return _not_found()

    try:
        chosen = RepositoryLayer(layer)
    except ValueError:
        return _html("<h1>400 &mdash; unknown layer</h1>", status_code=400)

    # Scope the update through the org's own projects, so a repo id from another
    # tenant cannot be reclassified by guessing it.
    link = session.exec(
        select(ProjectRepository)
        .join(Project, Project.id == ProjectRepository.project_id)
        .where(
            ProjectRepository.repository_id == repo_id,
            ProjectRepository.is_active == True,  # noqa: E712
            Project.organization_id == org.id,
        )
    ).first()
    if link is None:
        return _not_found()

    link.layer = chosen
    session.add(link)
    session.commit()

    return RedirectResponse(
        _origin_or(return_to, dashboard_path(org.alias or org.id)), status_code=303
    )


@router.post("/{org_ref}/projects/{project_id}/sync")
async def sync_project(
    org_ref: str,
    project_id: str,
    request: Request,
    return_to: str = Form(""),
    session: Session = Depends(get_session),
) -> Response:
    """Re-discover this project's repositories from GitHub, now.

    Awaited rather than backgrounded. It calls GitHub, so it can take a few
    seconds -- but the whole point of pressing sync is to see the result, and a
    route that returned instantly while the page still showed the old timestamp
    would be indistinguishable from one that did nothing. A slow response is the
    honest signal here.

    Reuses ``GitHubConnectService.sync_project_repositories``, the same call
    ``POST /api/v1/organizations/{org}/projects/{id}/repositories/sync`` makes --
    the topic-resolution rules, the soft-delete of repos that lost the label, and
    the layer defaults all live there and are not worth a second implementation.

    A failure (no GitHub credential for the org, an expired token, GitHub down)
    comes back as a message on the dashboard rather than a stack trace: the fix is
    almost always org configuration, and the person pressing the button is the one
    who can do it.
    """
    user = user_from_request(request, session)
    if user is None:
        return _to_login()

    org = _resolve_org(org_ref, session, user)
    if org is None:
        return _not_found()

    project = session.get(Project, project_id)
    if project is None or project.organization_id != org.id:
        return _not_found()

    # `_reportable_sync_error` is imported deliberately rather than reimplemented:
    # the notice below and `Project.github_error_message` are the same disclosure,
    # and a second copy of the classification would drift from the one the service
    # applies. It is private because nothing outside this pair should be quoting
    # exceptions at people.
    from src.services.github_connect_service import (
        GitHubConnectService,
        _reportable_sync_error,
    )

    try:
        result = await GitHubConnectService(session).sync_project_repositories(
            organization_id=org.id, project_id=project_id
        )
    except Exception as exc:  # noqa: BLE001 - surfaced to the operator, not swallowed
        # Sanitised, not `str(exc)`. The service already narrows this exact
        # exception before storing it, and interpolating the raw one here undid
        # that a file over: an aborted-transaction `OperationalError` or an
        # `IntegrityError` stringifies to SQL, bound parameters and connection
        # detail, which the notice then rendered in full to whoever pressed Sync.
        # The unabridged exception stays in the log line below, where it belongs.
        logger.warning("webui project sync failed for %s: %s", project_id, exc)
        return _redirect_with_flash(
            request,
            _origin_or(return_to, dashboard_path(org.alias or org.id)),
            f"Sync failed for {project.alias}: {_reportable_sync_error(exc)}",
            False,
        )

    # These three read keys `sync_project_repositories` actually returns. The
    # previous version read `added`, `removed` and `total_repositories`, none of
    # which the result dict has ever contained -- so every press of Sync flashed
    # "synced \u2014 ? repositories" with both counts suppressed as falsy, whatever
    # had really changed. The real shape is `repositories_synced` at the top level
    # and a nested `changes` dict; see the return at the end of
    # `GitHubConnectService.sync_project_repositories`.
    #
    # Note the two mixed types, which is why one is `len()` and the other is not:
    # `changes["new_repositories"]` is a list of repo names, while
    # `reactivated_repositories` and `deactivated_repositories` are ints.
    #
    # New and reactivated are summed under one "added" because they are the same
    # event to the person reading this: a repo that was not on the project's list
    # before the press is on it now. Which of the two it was is a detail of
    # whether InnoDay had seen the repo previously, and the page the redirect
    # lands on shows the resulting list either way.
    changes = result.get("changes") or {}
    added = len(changes.get("new_repositories") or []) + (
        changes.get("reactivated_repositories") or 0
    )
    removed = changes.get("deactivated_repositories") or 0
    total = result.get("repositories_synced", "?")
    return _redirect_with_flash(
        request,
        _origin_or(return_to, dashboard_path(org.alias or org.id)),
        f"{project.alias} synced \u2014 {total} repositories"
        + (f", {added} added" if added else "")
        + (f", {removed} removed" if removed else ""),
        True,
    )


@router.post("/{org_ref}/default-org")
async def set_default_org(
    org_ref: str,
    request: Request,
    organization_id: str = Form(...),
    session: Session = Depends(get_session),
) -> Response:
    """Choose which organization bare ``/ui`` opens.

    Writes ``users.default_organization_id`` -- the field ``GET /ui`` already
    consults, and which was previously only settable through the API or by hand.
    Without it, someone in four orgs landed on whichever sorted first by name
    every single time.

    Membership of the *target* is checked separately from the org in the path:
    they are different organizations by design (you set your default from
    whichever dashboard you happen to be on), so authorising one says nothing
    about the other.
    """
    user = user_from_request(request, session)
    if user is None:
        return _to_login()

    here = _resolve_org(org_ref, session, user)
    if here is None:
        return _not_found()

    target = session.get(Organization, organization_id)
    if target is None or not can_open(session, user, target.id):
        return _not_found()

    row = session.get(User, user.id)
    row.default_organization_id = target.id
    session.add(row)
    session.commit()

    return RedirectResponse(dashboard_path(here.alias or here.id), status_code=303)


@router.post("/{org_ref}/signup-requests/{request_id}/{decision}")
async def decide_signup_request(
    org_ref: str,
    request_id: str,
    decision: str,
    request: Request,
    session: Session = Depends(get_session),
) -> Response:
    """Approve or deny a request for platform access. Platform members only.

    **Not org-scoped, despite the org in the path.** Platform access is not an
    org's to grant, and an org ADMIN is not a platform member. The org segment is
    here only so the redirect lands back on the dashboard the approver was
    looking at; authorisation is `is_platform_member` and nothing else.

    Approving provisions through `provision_user`, the same service
    `POST /api/v1/users` uses -- so an approved person gets a Supabase identity
    before a `users` row exists, and a failure to provision leaves neither.
    """
    user = user_from_request(request, session)
    if user is None:
        return _to_login()

    org = _resolve_org(org_ref, session, user)
    if org is None:
        return _not_found()

    if not user.is_platform_member:
        # 404, not 403: a non-platform member should not learn that a queue of
        # people waiting for access exists, let alone that this one is in it.
        return _not_found()

    if decision not in ("approve", "deny"):
        return _html("<h1>400 &mdash; unknown decision</h1>", status_code=400)

    pending = session.get(SignupRequest, request_id)
    if pending is None or not pending.is_pending():
        # Already decided by someone else, most likely. Not an error worth a
        # page -- just show the queue as it now stands.
        return RedirectResponse(dashboard_path(org.alias or org.id), status_code=303)

    if decision == "deny":
        pending.decide(SignupRequestStatus.DENIED, user.id)
        session.add(pending)
        session.commit()
        return _render_dashboard(
            session, user, org, notice=(f"Denied access for {pending.email}.", True)
        )

    try:
        provisioned = provision_user(
            session, email=pending.email, full_name=pending.full_name
        )
    except UserProvisioningError as exc:
        # The request stays PENDING: a failure to provision is not a decision,
        # and silently marking it approved would strand someone with no account
        # and no way to ask again.
        logger.warning("signup approval failed for %s: %s", pending.email, exc)
        return _render_dashboard(
            session, user, org, notice=(f"Could not create the account: {exc}", False)
        )

    pending.decide(SignupRequestStatus.APPROVED, user.id)
    pending.created_user_id = provisioned.user.id
    session.add(pending)
    session.commit()

    return _render_dashboard(
        session,
        user,
        org,
        notice=(f"{pending.email} approved \u2014 invite sent.", True),
    )
