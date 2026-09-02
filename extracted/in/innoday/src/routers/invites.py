"""Organization invite + self-registration endpoints (auth P3, PF-350, §5.3-5.4).

    POST   /api/v1/organizations/{org_id}/invites       send an invite   [admin/owner|platform]
    GET    /api/v1/organizations/{org_id}/invites       list invites     [admin/owner|platform]
    DELETE /api/v1/organizations/{org_id}/invites/{id}  revoke invite    [admin/owner|platform]
    POST   /api/v1/invites/{token}/accept               accept an invite [authed invitee]
    POST   /api/v1/organizations/{org_id}/join          self-register    [authed; org opt-in]

Authorization for sending/listing/revoking uses ``User.is_org_admin`` /
``is_org_owner``, which already short-circuit True for platform users (rbac.py)
— so req 6 ("platform users AND org admins can send invites") falls out of the
existing model without special-casing here.
"""

import logging
import os
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select

from src.database import get_session
from src.domain.organization import (
    Organization,
    OrganizationMembership,
    OrganizationRole,
)
from src.domain.organization_invite import (
    InviteStatus,
    OrganizationInvite,
    generate_invite_token,
    hash_invite_token,
)
from src.domain.user import User
from src.middleware.rbac import get_current_user, resolve_organization
from src.page_paths import INVITE_ACCEPT_PATH, SESSION_PATH, UI_PREFIX
from src.routers._brand_pages import brand_page
from src.services.supabase_invite import send_supabase_invite

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["invites"])


def _app_url() -> str:
    return os.getenv("APP_URL", "http://localhost:8000").rstrip("/")


class InviteCreate(BaseModel):
    email: EmailStr
    # DEVELOPER for the same reason as MembershipCreate: you invite someone
    # because you want them working in the org, and MEMBER cannot.
    role: OrganizationRole = OrganizationRole.DEVELOPER


class InviteInfo(BaseModel):
    id: str
    organization_id: str
    email: str
    role: OrganizationRole
    status: InviteStatus
    invited_by: str
    expires_at: datetime
    created_at: datetime
    # Present only in the create response when email delivery isn't configured
    # (dev convenience) — the raw accept link so the flow is testable.
    accept_url: Optional[str] = None


def _require_org_admin(user: User, org: Organization) -> None:
    """Caller must be org ADMIN/owner OR a platform user (§4)."""
    if not user.is_org_admin(org.id):
        raise HTTPException(
            status_code=403,
            detail="Only organization admins/owners or platform users may manage invites",
        )


@router.post("/organizations/{org_id}/invites", response_model=InviteInfo)
async def create_invite(
    org_id: str,
    body: InviteCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Send an invite. Owner role is never invite-grantable (§3.6)."""
    org = resolve_organization(org_id, session)
    _require_org_admin(current_user, org)

    if body.role not in (
        OrganizationRole.MEMBER,
        OrganizationRole.ADMIN,
        OrganizationRole.DEVELOPER,
    ):
        raise HTTPException(status_code=400, detail="Invalid invite role")

    email = body.email.lower()

    # Already a member?
    existing_member = session.exec(
        select(OrganizationMembership)
        .join(User, OrganizationMembership.user_id == User.id)
        .where(
            OrganizationMembership.organization_id == org.id,
            User.email == email,
            OrganizationMembership.is_active == True,  # noqa: E712
        )
    ).first()
    if existing_member:
        raise HTTPException(status_code=409, detail="User is already a member")

    # Revoke any prior live invite for this (org, email) so there is one live
    # invite at a time (partial-unique-while-PENDING semantic, §3.2).
    prior = session.exec(
        select(OrganizationInvite).where(
            OrganizationInvite.organization_id == org.id,
            OrganizationInvite.email == email,
            OrganizationInvite.status == InviteStatus.PENDING,
        )
    ).all()
    for p in prior:
        p.revoke()
        session.add(p)

    raw_token = generate_invite_token()
    invite = OrganizationInvite(
        organization_id=org.id,
        email=email,
        role=body.role,
        invited_by=current_user.id,
        token_hash=hash_invite_token(raw_token),
    )
    session.add(invite)
    session.commit()
    session.refresh(invite)

    accept_url = f"{_app_url()}{INVITE_ACCEPT_PATH}?token={raw_token}"
    dispatch = send_supabase_invite(
        email=email,
        redirect_to=accept_url,
        metadata={"org_id": org.id, "role": body.role.value},
    )
    if dispatch.supabase_invite_id:
        invite.supabase_invite_id = dispatch.supabase_invite_id
        session.add(invite)
        session.commit()
        session.refresh(invite)

    resp = InviteInfo(
        id=invite.id,
        organization_id=invite.organization_id,
        email=invite.email,
        role=invite.role,
        status=invite.status,
        invited_by=invite.invited_by,
        expires_at=invite.expires_at,
        created_at=invite.created_at,
    )
    # Surface the raw accept link whenever an email did NOT actually go out —
    # either Supabase isn't configured (dev), or it is but the dispatch failed
    # (transient error / bad key). Without this, a Supabase error would strand
    # the invite: no email sent and no link for the admin to hand over.
    email_sent = dispatch.configured and dispatch.supabase_invite_id is not None
    if not email_sent:
        resp.accept_url = accept_url
    return resp


@router.get("/organizations/{org_id}/invites", response_model=List[InviteInfo])
async def list_invites(
    org_id: str,
    status_filter: Optional[InviteStatus] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    org = resolve_organization(org_id, session)
    _require_org_admin(current_user, org)

    query = select(OrganizationInvite).where(
        OrganizationInvite.organization_id == org.id
    )
    if status_filter:
        query = query.where(OrganizationInvite.status == status_filter)
    rows = session.exec(query).all()
    return [
        InviteInfo(
            id=r.id,
            organization_id=r.organization_id,
            email=r.email,
            role=r.role,
            status=r.status,
            invited_by=r.invited_by,
            expires_at=r.expires_at,
            created_at=r.created_at,
        )
        for r in rows
    ]


@router.delete("/organizations/{org_id}/invites/{invite_id}")
async def revoke_invite(
    org_id: str,
    invite_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    org = resolve_organization(org_id, session)
    _require_org_admin(current_user, org)

    invite = session.get(OrganizationInvite, invite_id)
    if not invite or invite.organization_id != org.id:
        raise HTTPException(status_code=404, detail="Invite not found")
    invite.revoke()
    session.add(invite)
    session.commit()
    return {"message": "Invite revoked", "id": invite_id}


@router.post("/invites/{token}/accept")
async def accept_invite(
    token: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Accept an invite. The caller is the authenticated invitee (Supabase JWT
    or CLI token). Creates the membership row and marks the invite ACCEPTED.

    The invitee becomes an ORDINARY member — never a platform user (§5.4).
    """
    invite = session.exec(
        select(OrganizationInvite).where(
            OrganizationInvite.token_hash == hash_invite_token(token)
        )
    ).first()
    if not invite:
        raise HTTPException(status_code=404, detail="Invite not found")
    if not invite.is_acceptable():
        raise HTTPException(
            status_code=400,
            detail=f"Invite is not acceptable (status={invite.status.value})",
        )

    # The accepting user's email should match the invited email.
    if current_user.email.lower() != invite.email.lower():
        raise HTTPException(
            status_code=403,
            detail="This invite was issued to a different email address",
        )

    # Idempotent: if already a member, just mark accepted.
    membership = session.exec(
        select(OrganizationMembership).where(
            OrganizationMembership.user_id == current_user.id,
            OrganizationMembership.organization_id == invite.organization_id,
        )
    ).first()
    if not membership:
        membership = OrganizationMembership(
            user_id=current_user.id,
            organization_id=invite.organization_id,
            role=invite.role,
            is_active=True,
            invited_by=invite.invited_by,  # finally meaningful (§3.2)
        )
        session.add(membership)
        # Set the invitee's home org if they have none yet.
        if not current_user.default_organization_id:
            current_user.default_organization_id = invite.organization_id
            session.add(current_user)
    else:
        membership.is_active = True
        session.add(membership)

    # Accepting proves control of the invited address: the invite token was
    # only ever emailed there, and the email match above was already enforced.
    # Reconcile verification state here (#414) so the CLI-token path reaches it
    # too -- the magic-link flow arrives with a Supabase JWT, which
    # _user_from_supabase_jwt already marks verified, but a CLI-token invitee
    # would otherwise stay unverified forever and be locked out the moment
    # REQUIRE_VERIFIED_EMAIL is switched on.
    if not current_user.email_verified:
        current_user.mark_email_verified()
        session.add(current_user)
        logger.info("Marked %s email-verified on invite acceptance", current_user.email)

    invite.mark_accepted()
    session.add(invite)
    session.commit()

    return {
        "message": "Invite accepted",
        "organization_id": invite.organization_id,
        "role": invite.role.value,
    }


@router.post("/organizations/{org_id}/join")
async def self_register(
    org_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Self-register into an org that has ``allow_self_registration`` on (§5.2).

    Platform users never need this (they already reach every org, no row);
    calling it is a no-op success for them.
    """
    org = resolve_organization(org_id, session)

    if current_user.is_platform_member:
        return {
            "message": "Platform users already have access to all organizations",
            "organization_id": org.id,
        }

    if not org.allow_self_registration:
        raise HTTPException(
            status_code=403,
            detail="This organization does not allow self-registration; an invite is required",
        )

    existing = session.exec(
        select(OrganizationMembership).where(
            OrganizationMembership.user_id == current_user.id,
            OrganizationMembership.organization_id == org.id,
        )
    ).first()
    if existing:
        if not existing.is_active:
            existing.is_active = True
            session.add(existing)
            session.commit()
        return {"message": "Already a member", "organization_id": org.id}

    membership = OrganizationMembership(
        user_id=current_user.id,
        organization_id=org.id,
        role=OrganizationRole.MEMBER,
        is_active=True,
    )
    session.add(membership)
    if not current_user.default_organization_id:
        current_user.default_organization_id = org.id
        session.add(current_user)
    session.commit()

    return {"message": "Joined organization", "organization_id": org.id}


# NB: these page-serving routes are intentionally NOT on the /api/v1 prefix.
# They are browser pages, so they live on the app's other half, /ui -- see
# src/page_paths.py for why the two segment by path. Their pre-/ui
# addresses are still served as 301s (registered in src/api/app.py).
page_router = APIRouter(prefix=UI_PREFIX, tags=["invites"])


@page_router.get("/invite/accept", response_class=HTMLResponse)
async def invite_accept_page(request: Request):
    """Pixelfuel-branded invite-accept landing page (reached from the email link).

    The invitee arrives already Supabase-authenticated (the magic link confirms
    their session); this page reads that session's Bearer token and POSTs it to
    /api/v1/invites/{token}/accept. Standalone/dev use falls back to a token in
    localStorage('innoday_token')."""
    token = request.query_params.get("token", "")
    return HTMLResponse(_render_accept_page(token))


@page_router.get("/auth/callback", response_class=HTMLResponse)
async def auth_callback_page() -> HTMLResponse:
    """Where a Supabase invite / magic link lands (``APP_URL`` + this path).

    Three code paths already pointed Supabase's ``redirect_to`` here —
    ``POST /users``, ``seed_platform_user``, and the identity backfill script —
    but **nothing served it**. A live probe of the dev deployment returned
    ``401``: not a 404, because ``TeamSecretMiddleware`` rejected the request
    before routing (the path was missing from ``EXEMPT_PATHS``, unlike
    ``/ui/invite/accept``). A browser arriving from an email has no team secret, so
    every invite recipient would have hit that wall.

    Supabase confirms the address at its own ``/auth/v1/verify`` before
    redirecting, so ``auth.users.email_confirmed_at`` was being set — but
    InnoDay's ``users.email_verified_at`` never was, because that only happens
    when a Supabase JWT reaches the API. The invite looked like it worked and
    left the person still locked out.

    The access token arrives in the URL **fragment**
    (``#access_token=…&refresh_token=…``), which is never sent to the server —
    only JS can read it. So this page parses the fragment, POSTs the token to
    ``/api/v1/auth/confirm-email`` to mirror verification, and stores it under
    ``innoday_token`` so the invite-accept page composes with this one.

    It then POSTs the same token to ``/ui/session`` to trade it for a session
    cookie and continues to the dashboard. That is what makes this page the
    landing spot for *both* audiences: an invitee finishing verification, and
    someone who just asked for a sign-in link at ``/ui/login``. Both need exactly
    this token exchanged for a session, so neither needs its own callback.

    Only a *success* redirects — an expired link or a failed confirmation stays
    put with its message on screen, because a page that bounces away before the
    error can be read is indistinguishable from one that silently did nothing.
    """
    return HTMLResponse(_render_auth_callback_page())


def _render_auth_callback_page() -> str:
    """Branded landing page for the IdP redirect (shell in _brand_pages).

    Paths are substituted rather than f-string-interpolated: the script is dense
    with JS braces, and doubling every one of them to satisfy an f-string is how
    a working page becomes a syntax error nobody notices until an invite bounces.
    """
    card = """    <div class="brand">Pixelfuel · InnoDay</div>
    <h1>Signing you in</h1>
    <p>One moment — linking your account.</p>
    <div class="msg" id="msg"></div>"""
    script = """
  const msg = document.getElementById('msg');
  function show(text, cls) { msg.textContent = text; msg.className = 'msg ' + cls; }

  // Supabase returns the session in the URL fragment, not the query string, so
  // it never reaches the server. On an error it uses `error_description`.
  const frag = new URLSearchParams((window.location.hash || '').replace(/^#/, ''));
  const token = frag.get('access_token');
  const errorText = frag.get('error_description') || frag.get('error');

  // Trade the verified JWT for a session cookie, then continue to the dashboard.
  // Failing this is not fatal: the address is still confirmed, so say so and
  // offer the sign-in page rather than reporting the whole link as broken.
  async function startSession(bearer, confirmedMessage) {
    try {
      const r = await fetch('__SESSION_PATH__', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ access_token: bearer }),
      });
      if (r.ok) {
        show(confirmedMessage + ' Taking you to your dashboard…', 'ok');
        window.setTimeout(() => { window.location.replace('__UI_PREFIX__'); }, 900);
        return;
      }
    } catch (e) { /* fall through to the message below */ }
    show(confirmedMessage + ' Open the sign-in page to continue.', 'ok');
  }

  if (errorText) {
    show(errorText + ' — the link may have expired. Ask for a new one.', 'err');
  } else if (!token) {
    show('No sign-in details found in this link. Open the most recent email, or ask for a new one.', 'err');
  } else {
    // Keep it where the invite-accept page looks, so the two pages compose.
    try { window.localStorage.setItem('innoday_token', token); } catch (e) {}
    fetch('/api/v1/auth/confirm-email', {
      method: 'POST',
      headers: { 'Authorization': 'Bearer ' + token },
    }).then(async (r) => {
      const data = await r.json().catch(() => ({}));
      if (r.ok && data.verified) {
        startSession(token, 'Email confirmed for ' + data.email + '.');
      } else if (r.ok) {
        show('Signed in as ' + (data.email || 'your account') + ', but the confirmation did not register. Please contact your administrator.', 'err');
      } else {
        show(data.detail || 'Could not confirm this account.', 'err');
      }
    }).catch((e) => show('Network error: ' + e.message, 'err'));
  }"""
    script = script.replace("__SESSION_PATH__", SESSION_PATH).replace(
        "__UI_PREFIX__", UI_PREFIX
    )
    return brand_page("InnoDay · Signing you in", card, script)


def _render_accept_page(token: str) -> str:
    """Pixelfuel-branded invite-accept page (shared shell in _brand_pages)."""
    card = """    <div class="brand">Pixelfuel · InnoDay</div>
    <h1>Accept your invitation</h1>
    <p>Join your team's workspace. Confirm below to finish.</p>
    <button id="accept">Accept invitation</button>
    <div class="msg" id="msg"></div>"""
    # token is embedded as a JS string literal via Python's repr.
    script = f"""
  const token = {token!r};
  const msg = document.getElementById('msg');
  document.getElementById('accept').addEventListener('click', async () => {{
    const bearer = window.localStorage.getItem('innoday_token') || '';
    try {{
      const r = await fetch('/api/v1/invites/' + encodeURIComponent(token) + '/accept', {{
        method:'POST',
        headers: bearer ? {{'Authorization':'Bearer '+bearer}} : {{}},
      }});
      const data = await r.json();
      if (r.ok) {{ msg.textContent = 'Accepted! You can now `innoday login` from the CLI.'; msg.className='msg ok'; }}
      else {{ msg.textContent = (data.detail||'Could not accept invite'); msg.className='msg err'; }}
    }} catch (e) {{ msg.textContent = 'Network error: ' + e.message; msg.className='msg err'; }}
  }});"""
    return brand_page("InnoDay · Accept invitation", card, script)
