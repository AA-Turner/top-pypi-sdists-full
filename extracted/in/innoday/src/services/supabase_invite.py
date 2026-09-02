"""Supabase invite email dispatch (auth P3, PF-350, §5.3).

Wraps ``supabase.auth.admin.inviteUserByEmail`` — the GoTrue admin API that
creates an unconfirmed ``auth.users`` row and emails the invitee a magic link.
This uses the **service_role** key, which bypasses RLS/auth, so it lives ONLY
in backend code and is never exposed to the CLI or browser (security note §6).

Configured via ``SUPABASE_URL`` + ``SUPABASE_SERVICE_KEY``. If either is
missing the dispatch is a graceful no-op returning ``configured=False`` — the
InnoDay-side invite row is still created, and in dev the raw accept link is
returned to the caller so the flow is testable without email delivery.

The Supabase Python client is an optional dependency (``supabase`` extra); the
import is lazy so the backend runs without it installed.
"""

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.parse import quote

from src.page_paths import AUTH_CALLBACK_PATH


@dataclass
class InviteDispatchResult:
    configured: bool
    supabase_invite_id: Optional[str] = None
    error: Optional[str] = None


@dataclass
class IdPConfirmation:
    """What the IdP knows about one identity's email confirmation."""

    supabase_user_id: str
    email: Optional[str]
    email_confirmed_at: Optional[Any]


def fetch_confirmed_identities() -> "tuple[Optional[list], Optional[str]]":
    """Every ``auth.users`` row, for reconciling confirmation state.

    Returns ``(identities, error)`` — exactly one is non-None.

    Needed because InnoDay's ``users.email_verified_at`` is only written when a
    Supabase JWT reaches the API. Supabase sets ``email_confirmed_at`` at its own
    ``/auth/v1/verify`` endpoint the moment someone clicks their link, so the two
    can disagree indefinitely if the person never makes an authenticated call.
    Reading the IdP directly makes the rollout verifiable server-side instead of
    depending on anyone's browser having completed the round trip.
    """
    if not supabase_admin_configured():
        return None, "SUPABASE_URL / SUPABASE_SERVICE_KEY are not both set"

    try:
        from supabase import create_client  # type: ignore
    except Exception as exc:  # pragma: no cover - optional dep
        return None, f"supabase client not installed: {exc}"

    try:
        client = create_client(
            os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
        )
        identities: list = []
        page = 1
        while True:
            batch = client.auth.admin.list_users(page=page, per_page=200)
            if not batch:
                break
            identities.extend(
                IdPConfirmation(
                    supabase_user_id=str(u.id),
                    email=getattr(u, "email", None),
                    email_confirmed_at=getattr(u, "email_confirmed_at", None),
                )
                for u in batch
            )
            if len(batch) < 200:
                break
            page += 1
        return identities, None
    except Exception as exc:  # pragma: no cover - network/SDK variance
        return None, str(exc)


def supabase_admin_configured() -> bool:
    return bool(os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_KEY"))


def google_sign_in_url(app_url: str) -> Optional[str]:
    """Where "Continue with Google" sends the browser, or None if unavailable.

    GoTrue's `/auth/v1/authorize` handles the whole dance and returns the browser
    to `redirect_to` with the session in the URL fragment -- the *same* landing
    the magic link already uses, so `/ui/auth/callback` serves both and needed no
    change. `redirect_to` must be listed in `additional_redirect_urls` or Supabase
    silently substitutes `site_url`, which looks like "Google sent me to the wrong
    place" rather than a config error.

    **None when the provider is not configured**, and the caller hides the button
    rather than rendering one that leads to a 400. That is the same bargain the
    sign-in form already makes when Supabase is absent: say the door is shut, do
    not draw one that does not open.

    Configuration is checked through the *client* key, not the service key: this
    URL is followed by a browser, so it needs the project to exist and the
    provider to be on -- the presence of a server-side admin key says nothing
    about either.
    """
    base = os.getenv("SUPABASE_URL")
    if not base or not os.getenv("SUPABASE_AUTH_EXTERNAL_GOOGLE_CLIENT_ID"):
        return None
    redirect = f"{app_url.rstrip('/')}{AUTH_CALLBACK_PATH}"
    return (
        f"{base.rstrip('/')}/auth/v1/authorize?provider=google"
        f"&redirect_to={quote(redirect, safe='')}"
    )


@dataclass
class MagicLinkResult:
    """Outcome of a sign-in link dispatch. Never carries the link itself."""

    configured: bool
    sent: bool = False
    status_code: Optional[int] = None
    error: Optional[str] = None


def magic_link_configured() -> bool:
    """Whether a sign-in link can be sent: the public endpoint needs the anon key."""
    return bool(os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_KEY"))


def send_magic_link(email: str, redirect_to: str) -> MagicLinkResult:
    """Email an existing user a sign-in link. Best-effort; never raises.

    Uses the **public** ``/auth/v1/otp`` endpoint with the anon key, because it is
    the only one that actually delivers mail. The obvious-looking alternative,
    ``admin/generate_link``, returns 200 and stamps ``recovery_sent_at`` but sends
    nothing -- it exists to hand you a link so *you* can mail it ("generates email
    links and OTPs to be sent via a custom email provider"). Measured against the
    live project: four ``generate_link`` calls produced zero SES delivery
    attempts, while one ``/auth/v1/otp`` produced one. Do not "simplify" this back
    to the admin endpoint; it fails silently and looks identical from the caller.

    ``redirect_to`` is a **query parameter**, not a body field. The REST API
    ignores both ``options.email_redirect_to`` (the supabase-js shape) and a
    top-level body ``redirect_to`` here, falling back to the project's Site URL --
    which is ``https://www.inno.day``, i.e. ``/``, which the team-secret gate
    answers with 401. A wrong redirect is therefore not a cosmetic bug: it hands
    the person an error page at the end of a working sign-in.

    ``create_user: false`` keeps this endpoint from provisioning an identity for
    an unknown address. The caller must *also* confirm the address belongs to a
    real InnoDay user -- see ``webui.routes``. Two guards, because this is a
    public form and either one alone is a single point of failure.

    A 422 ``signup_disabled`` here means the address exists at the IdP but is
    **unconfirmed**: this project sets ``[auth] enable_signup = false``, and
    GoTrue routes a magic link for an unconfirmed user through its signup path.
    Those users need an invite (or an operator confirmation) before they can use
    browser sign-in -- the result carries the code so the caller can log it.
    """
    if not magic_link_configured():
        return MagicLinkResult(configured=False)

    import urllib.parse

    import httpx

    base = os.environ["SUPABASE_URL"].rstrip("/")
    key = os.environ["SUPABASE_KEY"]
    query = urllib.parse.urlencode({"redirect_to": redirect_to})
    try:
        response = httpx.post(
            f"{base}/auth/v1/otp?{query}",
            headers={"apikey": key, "Content-Type": "application/json"},
            json={"email": email, "create_user": False},
            timeout=10,
        )
    except httpx.HTTPError as exc:
        return MagicLinkResult(configured=True, error=str(exc))

    if response.status_code >= 400:
        code = ""
        try:
            code = str(response.json().get("error_code", ""))
        except Exception:
            pass
        return MagicLinkResult(
            configured=True,
            status_code=response.status_code,
            error=code or "http error",
        )

    return MagicLinkResult(configured=True, sent=True, status_code=response.status_code)


def send_supabase_invite(
    email: str,
    redirect_to: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> InviteDispatchResult:
    """Best-effort: email a Supabase invite. Never raises — returns a result.

    On success ``supabase_invite_id`` is the created auth user's id. On any
    failure (not configured, client missing, API error) the InnoDay invite row
    should still stand; the caller falls back to the dev accept link.
    """
    if not supabase_admin_configured():
        return InviteDispatchResult(configured=False)

    try:
        from supabase import create_client  # type: ignore
    except Exception as exc:  # pragma: no cover - optional dep
        return InviteDispatchResult(
            configured=False, error=f"supabase client not installed: {exc}"
        )

    try:
        client = create_client(
            os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
        )
        resp = client.auth.admin.invite_user_by_email(
            email,
            {"redirect_to": redirect_to, "data": metadata or {}},
        )
        user = getattr(resp, "user", None)
        invite_id = getattr(user, "id", None) if user else None
        return InviteDispatchResult(configured=True, supabase_invite_id=invite_id)
    except Exception as exc:  # pragma: no cover - network/SDK variance
        return InviteDispatchResult(configured=True, error=str(exc))
