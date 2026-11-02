"""Browser-based login flow: custom login UI → Cognito USER_PASSWORD_AUTH → API key.

Endpoints:
  GET  /auth/login?session_id=<id>   — render custom login page
  POST /auth/authenticate            — authenticate via Cognito InitiateAuth
  GET  /auth/session/<session_id>    — agent polls for the provisioned API key
  GET  /auth/logout                  — clear the session cookie and revoke its key
  GET  /auth/forgot                  — ask for a reset code by email
  POST /auth/forgot                  — Cognito ForgotPassword (uniform response)
  GET  /auth/reset                   — enter a code already received
  POST /auth/reset                   — Cognito ConfirmForgotPassword, then sign in
"""

from __future__ import annotations

import hashlib
import html
import logging
import time
from urllib.parse import parse_qsl, urlencode

import boto3
from jose import jwt
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

from cube_cloud.auth import api_keys, session_cookie
from cube_cloud.auth.api_keys import create_key
from cube_cloud.browser_proxy.http_proxy import (
    RequestBodyTooLarge, read_request_body_capped,
)
from cube_cloud.browser_proxy.rate_limit import SlidingWindowRateLimiter
from cube_cloud.config import settings

logger = logging.getLogger(__name__)

SESSION_TTL = 300  # 5 minutes (well above agent's 2-minute poll window)


# ---------------------------------------------------------------------------
# DynamoDB session helpers (replaces in-memory _sessions dict)
# ---------------------------------------------------------------------------


def _store_session(session_id: str, api_key: str) -> None:
    """Store a login session in DynamoDB with a TTL."""
    table = settings.login_sessions_table
    client = boto3.client("dynamodb", region_name=settings.aws_region)
    expiry = int(time.time()) + SESSION_TTL
    client.put_item(
        TableName=table,
        Item={
            "session_id": {"S": session_id},
            "api_key": {"S": api_key},
            "expiry": {"N": str(expiry)},
        },
    )


def _retrieve_session(session_id: str) -> str | None:
    """Retrieve and delete a login session from DynamoDB (one-time use).

    Returns the api_key if found, or None.
    """
    table = settings.login_sessions_table
    client = boto3.client("dynamodb", region_name=settings.aws_region)
    resp = client.get_item(
        TableName=table,
        Key={"session_id": {"S": session_id}},
    )
    item = resp.get("Item")
    if not item:
        return None

    api_key = item["api_key"]["S"]

    # One-time use: delete after retrieval
    client.delete_item(
        TableName=table,
        Key={"session_id": {"S": session_id}},
    )
    return api_key


# ---------------------------------------------------------------------------
# Cognito helpers (USER_PASSWORD_AUTH)
# ---------------------------------------------------------------------------


def _initiate_auth(email: str, password: str) -> dict:
    """Call Cognito InitiateAuth with USER_PASSWORD_AUTH flow."""
    client = boto3.client("cognito-idp", region_name=settings.aws_region)
    try:
        resp = client.initiate_auth(
            ClientId=settings.cognito_app_client_id,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": email, "PASSWORD": password},
        )
    except client.exceptions.NotAuthorizedException:
        return {"error": "Incorrect email or password."}
    except client.exceptions.UserNotFoundException:
        return {"error": "Incorrect email or password."}
    except client.exceptions.UserNotConfirmedException:
        return {"error": "Account not confirmed. Please contact your administrator."}
    except Exception as e:
        logger.error("InitiateAuth failed: %s", e)
        return {"error": "Authentication failed. Please try again."}

    if resp.get("ChallengeName") == "NEW_PASSWORD_REQUIRED":
        return {"challenge": "NEW_PASSWORD_REQUIRED", "session": resp["Session"]}

    auth_result = resp.get("AuthenticationResult", {})
    return {"id_token": auth_result.get("IdToken", "")}


def _respond_to_challenge(session: str, email: str, new_password: str) -> dict:
    """Respond to NEW_PASSWORD_REQUIRED challenge."""
    client = boto3.client("cognito-idp", region_name=settings.aws_region)
    try:
        resp = client.respond_to_auth_challenge(
            ClientId=settings.cognito_app_client_id,
            ChallengeName="NEW_PASSWORD_REQUIRED",
            Session=session,
            ChallengeResponses={
                "USERNAME": email,
                "NEW_PASSWORD": new_password,
            },
        )
    except client.exceptions.InvalidPasswordException as e:
        msg = str(e)
        # Extract the useful part of the error message
        if ":" in msg:
            msg = msg.split(":", 1)[1].strip()
        return {"error": msg}
    except Exception as e:
        logger.error("RespondToAuthChallenge failed: %s", e)
        return {"error": "Failed to set password. Please try again."}

    auth_result = resp.get("AuthenticationResult", {})
    return {"id_token": auth_result.get("IdToken", "")}


def _forgot_password(email: str) -> dict:
    """Ask Cognito to email a password-reset code.

    Returns ``{}`` for every outcome the caller must render IDENTICALLY, and
    ``{"throttled": True}`` only when Cognito refused on rate. The swallowing is
    the whole point rather than laziness: with the pool's
    ``prevent_user_existence_errors`` at LEGACY (deliberate — see
    infra/terraform/cognito.tf) Cognito distinguishes "no such user"
    (``UserNotFoundException``), "no verified email" (``InvalidParameterException``)
    and "still on a temporary password" (``NotAuthorizedException``). Those are
    three facts about someone else's account, and an unauthenticated caller must
    not be able to read any of them off the page. Keeping LEGACY is what leaves
    the distinction in OUR logs, where it is a support tool instead of an oracle.

    Only the exception CLASS is logged. Never the message — Cognito echoes the
    username into several of them — and never the address.
    """
    client = boto3.client("cognito-idp", region_name=settings.aws_region)
    try:
        client.forgot_password(
            ClientId=settings.cognito_app_client_id,
            Username=email,
        )
    except Exception as e:  # noqa: BLE001 - EVERY outcome renders alike
        # Cognito's own throttle is swallowed along with the rest, and that is
        # deliberate. Under LEGACY a non-existent username raises
        # UserNotFoundException before any per-user counter is consulted, so
        # LimitExceededException can only ever be reached for an address that
        # HAS an account -- surfacing it as its own page made "did it throttle"
        # an existence oracle, bypassing the byte-identical property this whole
        # function exists to provide. Our own per-email budget (config.py) is
        # what tells a user they are going too fast, and it is spent by
        # repetition alone, whether or not the account exists.
        logger.info("ForgotPassword declined: %s", type(e).__name__)
    return {}


def _confirm_forgot_password(email: str, code: str, new_password: str) -> dict:
    """Redeem a reset code. Returns ``{}`` on success or ``{"error": msg}``.

    Unlike :func:`_forgot_password` this one DOES report failures, because the
    code and the password are the caller's own input and telling them their own
    typing was wrong discloses nothing. The one exception is
    ``UserNotFoundException``, folded into the code-mismatch message: reported
    separately it would turn this page into the enumeration oracle the previous
    step was careful not to be.
    """
    client = boto3.client("cognito-idp", region_name=settings.aws_region)
    try:
        client.confirm_forgot_password(
            ClientId=settings.cognito_app_client_id,
            Username=email,
            ConfirmationCode=code,
            Password=new_password,
        )
    except (client.exceptions.CodeMismatchException,
            client.exceptions.UserNotFoundException,
            client.exceptions.ExpiredCodeException):
        # ONE message for all three, and the third is the reason why. Splitting
        # "expired" out reads as a kindness and is an account-existence oracle:
        # under LEGACY an unknown address raises UserNotFoundException, while a
        # REAL account with no outstanding code raises ExpiredCodeException. So
        # submitting any code for any address answered "does this account
        # exist" — caught live on dev, where the two wordings differed; the unit
        # test that was supposed to cover this compared UserNotFound against
        # CodeMismatch only and never against ExpiredCode.
        #
        # The merged wording stays true and actionable in every case: the page
        # carries a "Send a new code" link directly beneath it.
        return {"error": "That code is not correct or has expired. "
                         "Send a new code and try again."}
    except client.exceptions.InvalidPasswordException as e:
        # Same idiom as _respond_to_challenge: surface Cognito's own policy text,
        # which is more specific than anything we could restate here.
        msg = str(e)
        if ":" in msg:
            msg = msg.split(":", 1)[1].strip()
        return {"error": msg}
    # NOTE: no `PasswordHistoryPolicyViolationException` clause. It needs the
    # Essentials/Plus feature tier AND a configured PasswordHistorySize, and the
    # pool sets neither, so it cannot fire -- while `client.exceptions.<Name>`
    # raises AttributeError for a shape the resolved botocore does not carry,
    # and Python evaluates `except` expressions at RAISE time. On an older
    # botocore that would make the generic handler below unreachable and turn an
    # unrelated Cognito error into a 500. The generic handler covers it anyway.
    except (client.exceptions.TooManyFailedAttemptsException,
            client.exceptions.LimitExceededException,
            client.exceptions.TooManyRequestsException):
        return {"error": "Too many attempts. Please wait a while and try again."}
    except Exception as e:  # noqa: BLE001
        logger.error("ConfirmForgotPassword failed: %s", type(e).__name__)
        return {"error": "Could not reset the password. Please try again."}
    return {}


# ---------------------------------------------------------------------------
# Shared CSS design system
# ---------------------------------------------------------------------------

_GLASSMORPHISM_CSS = """\
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
    min-height: 100vh;
    display: flex;
    color: #fff;
    /* Scrollable, and centred by the card's own `margin: auto` rather than by
       `align-items`/`justify-content` here. This used to be `overflow: hidden`
       with flex centring, which was fine while every page in this flow was
       short. The reset page is not: it carries an email, a code, two password
       fields and the "no code?" note, and on a laptop-height window that put
       the submit button and the help address below a fold nobody could scroll
       to. Centring via auto margins is the fix rather than a nicety -- a
       flex-centred item that overflows its scroll container has its TOP edge
       clipped and unreachable, so simply turning overflow back on would have
       moved the unreachable half rather than removed it.

       `.bg` is `position: fixed`, so it adds no height and does not scroll
       away. */
    overflow-y: auto;
    padding: 24px 16px;
}

.bg {
    position: fixed;
    inset: 0;
    background-size: cover;
    background-position: center;
    z-index: -2;
}

.bg::after {
    content: '';
    position: absolute;
    inset: 0;
    background: rgba(0, 0, 0, 0.55);
    z-index: -1;
}

.glass-card {
    margin: auto;
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    padding: 48px 40px;
    width: 100%;
    max-width: 420px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.logo {
    text-align: center;
    margin-bottom: 32px;
}

.logo h1 {
    font-size: 24px;
    font-weight: 600;
    letter-spacing: -0.5px;
}

.logo span {
    color: #6b8afd;
}

.logo p {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.5);
    margin-top: 4px;
}

h2 {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 8px;
    letter-spacing: -0.3px;
}

.subtitle {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.5);
    margin-bottom: 28px;
}

.form-group {
    margin-bottom: 18px;
}

.form-group label {
    display: block;
    font-size: 13px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.7);
    margin-bottom: 6px;
}

.form-group input {
    width: 100%;
    padding: 12px 14px;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 10px;
    color: #fff;
    font-size: 15px;
    font-family: inherit;
    outline: none;
    transition: border-color 0.2s, background 0.2s;
}

.form-group input:focus {
    border-color: #6b8afd;
    background: rgba(255, 255, 255, 0.1);
}

.form-group input::placeholder {
    color: rgba(255, 255, 255, 0.3);
}

.btn {
    width: 100%;
    padding: 13px;
    background: #6b8afd;
    color: #fff;
    border: none;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition: background 0.2s, box-shadow 0.2s;
    margin-top: 8px;
}

.btn:hover {
    background: #5a7bf0;
    box-shadow: 0 4px 20px rgba(107, 138, 253, 0.35);
}

.error-box {
    background: rgba(255, 59, 48, 0.15);
    border: 1px solid rgba(255, 59, 48, 0.3);
    border-radius: 10px;
    padding: 12px 14px;
    margin-bottom: 20px;
    font-size: 13px;
    color: #ff6b6b;
}

/* Good news, not bad. `.error-box` is red, and the one message that must use
   this instead is "Password updated — please sign in": by the time it renders,
   the reset has already SUCCEEDED and only the automatic sign-in fell over.
   Rendering that in the red box would tell the user their password change
   failed, which is both false and the one thing likeliest to make them try
   again and lock themselves out. */
.notice-box {
    background: rgba(52, 199, 89, 0.15);
    border: 1px solid rgba(52, 199, 89, 0.3);
    border-radius: 10px;
    padding: 12px 14px;
    margin-bottom: 20px;
    font-size: 13px;
    color: #6ee7a0;
}

.hint {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.4);
    margin-top: 6px;
}

.alt-action {
    font-size: 13px;
    text-align: center;
    margin-top: 16px;
}

.alt-action a {
    color: #6b8afd;
    text-decoration: none;
}

.alt-action a:hover {
    text-decoration: underline;
}

.help-footer {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.4);
    text-align: center;
    margin-top: 28px;
    padding-top: 18px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.help-footer a {
    color: #6b8afd;
    text-decoration: none;
}

.help-footer a:hover {
    text-decoration: underline;
}
"""

# The address every unauthenticated surface points people at. Hardcoded rather
# than plumbed through Settings + Terraform: it is stable, and the console SPA
# has to carry its own copy across the language boundary regardless (see
# console/web/src/App.tsx). Tests on both sides pin the literal.
HELP_EMAIL = "help@edgescaleai.com"

_HELP_FOOTER = (
    f'<p class="help-footer">Questions or feedback? '
    f'<a href="mailto:{HELP_EMAIL}">{HELP_EMAIL}</a></p>'
)

# The confirm-password check, shared by the two pages that ask for a new
# password (`_new_password_page` and `_reset_page`). A convenience only — both
# handlers re-check server-side, because this runs in the user's browser and is
# therefore not a validation. It relies on the ids `new_password` and
# `confirm_password`, so both pages must keep them.
_CONFIRM_MATCH_SCRIPT = """
    <script>
    function validatePasswords() {
        var pw = document.getElementById('new_password').value;
        var cpw = document.getElementById('confirm_password').value;
        if (pw !== cpw) {
            alert('Passwords do not match.');
            return false;
        }
        return true;
    }
    </script>"""

# The Edgescale mark, in every `<head>` on this flow and in the console shell
# (console/web/index.html) — one file, referenced by path, rather than a data URI
# duplicated per page.
#
# Served by the `/static` mount, which is in `APIKeyMiddleware.EXEMPT_PREFIXES`.
# That is a requirement, not a convenience: these pages render *before* anyone has
# a credential, so an authenticated icon would simply fail to load on the one
# surface every user sees first.
#
# A shared constant for the same reason as `_HELP_FOOTER`: four builders below,
# and a favicon on three of them looks like a bug rather than a decision.
_FAVICON = (
    '<link rel="icon" type="image/svg+xml" href="/static/favicon.svg">\n'
    '    <link rel="alternate icon" type="image/png" sizes="32x32" '
    'href="/static/favicon.png">'
)


# ---------------------------------------------------------------------------
# HTML page builders
# ---------------------------------------------------------------------------


def _carry(session_id: str, next_url: str) -> str:
    """Query string carrying the entry mode across a link between these pages.

    Both values are re-validated by whatever handler receives them, so this is
    only about not LOSING them: a user who detours through the reset pages must
    still land where they were going — the console, an app subdomain, or the
    agent's close-the-tab page — rather than on the default.

    `urlencode` first (the values are raw), then the caller escapes the whole
    href for the attribute. Doing it the other way round double-encodes.
    """
    params = [(k, v) for k, v in (("session_id", session_id), ("next", next_url)) if v]
    return f"?{urlencode(params)}" if params else ""


def _signin_href(target: str = "") -> str:
    """An escaped `/auth/login` href that lands the user in the console, or "".

    Returns "" when the console is not served on this stack, because a bare
    `/auth/login` 400s there — the same trap `infra/terraform/cognito.tf` records
    against the invite email's link. A dead link on a page someone reaches when
    they are already lost is worse than no link, so callers omit the whole
    element rather than rendering one that cannot work.

    Every destination goes through sign-in rather than straight to `/console`,
    and that is not laziness: the agent (`session_id`) flow deliberately sets no
    session cookie, so a direct link would 302 the user to this same page having
    promised them the console. Routing through it openly costs one sign-in and
    never dead-ends.
    """
    if not settings.console_enabled:
        return ""
    destination = target or session_cookie.CONSOLE_PREFIX
    return html.escape(f"/auth/login{_carry('', destination)}", quote=True)


def _login_page(session_id: str, error: str = "", next_url: str = "",
                notice: str = "") -> str:
    # All reflected values are escaped — this page renders on the apex origin
    # that mints credentials, so attribute-breakout there is a credential-theft
    # XSS. (next_url has passed validate_next; the rest are raw user input.)
    error_html = f'<div class="error-box">{html.escape(error)}</div>' if error else ""
    notice_html = f'<div class="notice-box">{html.escape(notice)}</div>' if notice else ""
    forgot_href = html.escape(f"/auth/forgot{_carry(session_id, next_url)}", quote=True)
    session_id = html.escape(session_id, quote=True)
    next_field = f'<input type="hidden" name="next" value="{html.escape(next_url, quote=True)}">' if next_url else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {_FAVICON}
    <title>Sign In — Edgeport</title>
    <style>{_GLASSMORPHISM_CSS}</style>
</head>
<body>
    <div class="bg" style="background-image: url('/static/underground-mining-excavator-operations.png');"></div>
    <div class="glass-card">
        <div class="logo">
            <h1>Edgescale<span>AI</span></h1>
            <p>Edgeport</p>
        </div>
        {notice_html}
        {error_html}
        <form method="POST" action="/auth/authenticate">
            <input type="hidden" name="session_id" value="{session_id}">
            {next_field}
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" placeholder="you@company.com" required autofocus>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" placeholder="Enter your password" required>
            </div>
            <button type="submit" class="btn">Sign In</button>
        </form>
        <p class="alt-action"><a href="{forgot_href}">Forgot your password?</a></p>
        {_HELP_FOOTER}
    </div>
</body>
</html>"""


def _new_password_page(session_id: str, email: str, challenge_session: str, error: str = "", next_url: str = "") -> str:
    error_html = f'<div class="error-box">{html.escape(error)}</div>' if error else ""
    session_id = html.escape(session_id, quote=True)
    email = html.escape(email, quote=True)
    challenge_session = html.escape(challenge_session, quote=True)
    next_field = f'<input type="hidden" name="next" value="{html.escape(next_url, quote=True)}">' if next_url else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {_FAVICON}
    <title>Set Your Password — Edgeport</title>
    <style>{_GLASSMORPHISM_CSS}</style>
</head>
<body>
    <div class="bg" style="background-image: url('/static/underground-mining-excavator-operations.png');"></div>
    <div class="glass-card">
        <div class="logo">
            <h1>Edgescale<span>AI</span></h1>
            <p>Edgeport</p>
        </div>
        <h2>Set Your Password</h2>
        <p class="subtitle">Choose a new password for your account.</p>
        {error_html}
        <form method="POST" action="/auth/authenticate">
            <input type="hidden" name="session_id" value="{session_id}">
            <input type="hidden" name="email" value="{email}">
            <input type="hidden" name="challenge_session" value="{challenge_session}">
            {next_field}
            <div class="form-group">
                <label for="new_password">New Password</label>
                <input type="password" id="new_password" name="new_password" placeholder="Choose a strong password" required autofocus>
                <p class="hint">At least 12 characters with uppercase, lowercase, and numbers.</p>
            </div>
            <div class="form-group">
                <label for="confirm_password">Confirm Password</label>
                <input type="password" id="confirm_password" name="confirm_password" placeholder="Confirm your password" required>
            </div>
            <button type="submit" class="btn" onclick="return validatePasswords()">Continue</button>
        </form>
        {_HELP_FOOTER}
    </div>{_CONFIRM_MATCH_SCRIPT}
</body>
</html>"""


def _forgot_page(session_id: str, error: str = "", next_url: str = "") -> str:
    """Step 1 of self-service reset: ask for the address to send a code to."""
    error_html = f'<div class="error-box">{html.escape(error)}</div>' if error else ""
    login_href = html.escape(f"/auth/login{_carry(session_id, next_url)}", quote=True)
    session_id = html.escape(session_id, quote=True)
    next_field = f'<input type="hidden" name="next" value="{html.escape(next_url, quote=True)}">' if next_url else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {_FAVICON}
    <title>Reset Password — Edgeport</title>
    <style>{_GLASSMORPHISM_CSS}</style>
</head>
<body>
    <div class="bg" style="background-image: url('/static/underground-mining-excavator-operations.png');"></div>
    <div class="glass-card">
        <div class="logo">
            <h1>Edgescale<span>AI</span></h1>
            <p>Edgeport</p>
        </div>
        <h2>Reset Your Password</h2>
        <p class="subtitle">Enter your email address and we will send you a reset code.</p>
        {error_html}
        <form method="POST" action="/auth/forgot">
            <input type="hidden" name="session_id" value="{session_id}">
            {next_field}
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" placeholder="you@company.com" required autofocus>
            </div>
            <button type="submit" class="btn">Send reset code</button>
        </form>
        <p class="alt-action"><a href="{login_href}">Back to sign in</a></p>
        {_HELP_FOOTER}
    </div>
</body>
</html>"""


def _reset_page(session_id: str, email: str = "", error: str = "",
                next_url: str = "") -> str:
    """Step 2 of self-service reset: redeem the code and choose a password.

    Two things here are load-bearing and easy to "tidy" away.

    The email is a VISIBLE, prefilled input rather than a hidden field, so
    `GET /auth/reset` is a working entry for someone whose code arrived after
    they closed the tab. A hidden field would make the mail useless the moment
    the browser was gone, which is exactly when a code takes a few minutes.

    The "no code?" line is shown to EVERYONE, unconditionally. It is how the
    `FORCE_CHANGE_PASSWORD` population — a user who never completed first login,
    or whose 7-day invite expired — gets pointed somewhere useful, since Cognito
    refuses `ForgotPassword` for them and :func:`_forgot_password` deliberately
    renders that refusal the same as success. Making the line conditional on
    that state would restore precisely the disclosure this flow avoids.
    """
    error_html = f'<div class="error-box">{html.escape(error)}</div>' if error else ""
    forgot_href = html.escape(f"/auth/forgot{_carry(session_id, next_url)}", quote=True)
    login_href = html.escape(f"/auth/login{_carry(session_id, next_url)}", quote=True)
    # Carries the entry mode rather than using `_signin_href`, because someone
    # who abandons a reset mid-flow must land back in the flow they came from --
    # the agent's close-the-tab page, or wherever `next` pointed.
    reset_back = f' &middot; <a href="{login_href}">Back to sign in</a>'
    session_id = html.escape(session_id, quote=True)
    email = html.escape(email, quote=True)
    next_field = f'<input type="hidden" name="next" value="{html.escape(next_url, quote=True)}">' if next_url else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {_FAVICON}
    <title>Enter Your Code — Edgeport</title>
    <style>{_GLASSMORPHISM_CSS}</style>
</head>
<body>
    <div class="bg" style="background-image: url('/static/underground-mining-excavator-operations.png');"></div>
    <div class="glass-card">
        <div class="logo">
            <h1>Edgescale<span>AI</span></h1>
            <p>Edgeport</p>
        </div>
        <h2>Enter Your Code</h2>
        <p class="subtitle">If an account exists for that address, a reset code is on its way. It expires in one hour.</p>
        {error_html}
        <form method="POST" action="/auth/reset">
            <input type="hidden" name="session_id" value="{session_id}">
            {next_field}
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" value="{email}" placeholder="you@company.com" required>
            </div>
            <div class="form-group">
                <label for="code">Reset code</label>
                <input type="text" id="code" name="code" placeholder="From your email" required autofocus
                       autocomplete="one-time-code" inputmode="numeric">
            </div>
            <div class="form-group">
                <label for="new_password">New Password</label>
                <input type="password" id="new_password" name="new_password" placeholder="Choose a strong password" required>
                <p class="hint">At least 12 characters with uppercase, lowercase, and numbers.</p>
            </div>
            <div class="form-group">
                <label for="confirm_password">Confirm Password</label>
                <input type="password" id="confirm_password" name="confirm_password" placeholder="Confirm your password" required>
            </div>
            <button type="submit" class="btn" onclick="return validatePasswords()">Reset password</button>
        </form>
        <p class="alt-action"><a href="{forgot_href}">Send a new code</a>{reset_back}</p>
        <p class="hint" style="text-align:center;">No code after a few minutes? Your account may need an
        administrator to re-send your invitation.</p>
        {_HELP_FOOTER}
    </div>{_CONFIRM_MATCH_SCRIPT}
</body>
</html>"""


def _success_page() -> str:
    """The agent (`session_id`) flow's close-the-tab page.

    The primary instruction stays exactly as it was — the published CLI's whole
    UX is "we opened a tab, now come back to your terminal", and that sentence is
    load-bearing. What is added is a secondary line for the fact that this page
    is, for most people, the very first Edgeport surface they ever see: they have
    an account, and nothing has told them a console or a field guide exists.

    The Field Guide leads because of who is standing here: someone whose first
    successful action was a CLI login. Both links go via `_signin_href`, so they
    disappear on a stack without a console rather than 400ing.
    """
    guide_href = _signin_href(f"{session_cookie.CONSOLE_PREFIX}/guide")
    console_href = _signin_href()
    # Two lines rather than one: at the card's 420px the single-line version
    # wrapped mid-phrase and ran the two links together into something that read
    # as one long link.
    next_steps = f"""
        <p class="hint" style="text-align:center;">New to Edgeport?</p>
        <p class="alt-action" style="margin-top:4px;"><a href="{guide_href}">Read the Cube Field Guide</a>
        &middot; <a href="{console_href}">Open the Console</a></p>""" if console_href else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {_FAVICON}
    <title>Login Successful — Edgeport</title>
    <style>
    {_GLASSMORPHISM_CSS}
    .success-icon {{
        width: 72px;
        height: 72px;
        border-radius: 50%;
        background: rgba(52, 199, 89, 0.15);
        border: 2px solid rgba(52, 199, 89, 0.4);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 24px;
        animation: scaleIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    .checkmark {{
        width: 32px;
        height: 32px;
        stroke: #34c759;
        stroke-width: 3;
        fill: none;
        stroke-linecap: round;
        stroke-linejoin: round;
    }}
    .checkmark path {{
        stroke-dasharray: 48;
        stroke-dashoffset: 48;
        animation: draw 0.5s 0.3s ease forwards;
    }}
    @keyframes scaleIn {{
        from {{ transform: scale(0); opacity: 0; }}
        to {{ transform: scale(1); opacity: 1; }}
    }}
    @keyframes draw {{
        to {{ stroke-dashoffset: 0; }}
    }}
    .success-text {{
        text-align: center;
    }}
    .success-text h2 {{
        margin-bottom: 12px;
    }}
    .success-text p {{
        color: rgba(255, 255, 255, 0.5);
        font-size: 14px;
        line-height: 1.5;
    }}
    </style>
</head>
<body>
    <div class="bg" style="background-image: url('/static/underground-mining-excavator-operations.png');"></div>
    <div class="glass-card">
        <div class="logo">
            <h1>Edgescale<span>AI</span></h1>
            <p>Edgeport</p>
        </div>
        <div class="success-icon">
            <svg class="checkmark" viewBox="0 0 32 32">
                <path d="M6 17l7 7 13-13"/>
            </svg>
        </div>
        <div class="success-text">
            <h2>Login Successful!</h2>
            <p>You can close this tab and return to your terminal.</p>
        </div>{next_steps}
        {_HELP_FOOTER}
    </div>
</body>
</html>"""


def _logout_page() -> str:
    """Signed-out confirmation.

    "Sign in again to continue" told the user what to do without giving them any
    way to do it — the page is a dead end otherwise, since there is no navigation
    anywhere on this flow. The link is omitted rather than pointed at a bare
    `/auth/login` on a console-less stack, where that 400s.
    """
    signin_href = _signin_href()
    signin_link = (f'<p class="alt-action"><a href="{signin_href}">Sign in again</a></p>'
                   if signin_href else "")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {_FAVICON}
    <title>Signed Out — Edgeport</title>
    <style>{_GLASSMORPHISM_CSS}</style>
</head>
<body>
    <div class="bg" style="background-image: url('/static/underground-mining-excavator-operations.png');"></div>
    <div class="glass-card">
        <div class="logo">
            <h1>Edgescale<span>AI</span></h1>
            <p>Edgeport</p>
        </div>
        <div class="success-text" style="text-align:center;">
            <h2>Signed Out</h2>
            <p class="subtitle">Your session has ended.</p>
        </div>
        {signin_link}
        {_HELP_FOOTER}
    </div>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Route handlers
# ---------------------------------------------------------------------------


def _entry_mode(session_id: str, raw_next: str) -> tuple[str, str]:
    """Resolve the (session_id, safe_next) pair every page in this flow carries.

    `next` is run through the open-redirect guard HERE, on each hop, GET and
    POST alike — a form field is exactly as forgeable as a query param, so a
    value is never trusted past the guard just because an earlier page already
    checked it. A rejected value falls back to the console default rather than
    being reflected or redirected to.

    One helper because six handlers now need the identical three lines, and the
    reset pages must default and validate exactly the way the sign-in pages do
    or a user detouring through them lands somewhere else.
    """
    safe_next = session_cookie.validate_next(raw_next) or ""
    if not session_id and not safe_next and settings.console_enabled:
        safe_next = session_cookie.CONSOLE_PREFIX
    return session_id, safe_next


# Shown to someone whose password is right but who belongs to no Cognito group,
# i.e. to no profile. Nothing about which state they are in: there is only one.
_NO_PROFILE = (
    "This account is not assigned to a profile yet, so it cannot sign in. "
    "Ask an administrator to add it to one."
)


class NoProfileError(Exception):
    """The ID token carries no Cognito group, so there is no profile to mint a key for.

    Raised rather than returned as ``None`` so each caller can answer in its own
    voice: the sign-in page says so, while a reset (whose password change is
    already durable) still lands on the "password updated" notice.
    """


def _email_verified(claims: dict) -> bool:
    """Cognito's ``email_verified`` claim is a JSON boolean; accept its string form too."""
    value = claims.get("email_verified")
    return value is True or value == "true"


def _mint_session(id_token: str, session_id: str, safe_next: str) -> Response | None:
    """Turn a successful Cognito authentication into this app's own credential.

    Returns the finished response — a session cookie plus a 303 for the browser
    flow, or the close-the-tab page for the agent flow — or ``None`` when the
    token is missing or unreadable, leaving the caller to render an error in its
    own page's voice.

    One function, two callers (`auth_authenticate` and `auth_reset_submit`), so
    a reset that lands on the console mints the same short-lived key a direct
    sign-in does. A second copy of this is exactly the kind of thing that keeps
    the TTL rule below on one path and not the other.
    """
    if not id_token:
        return None
    try:
        claims = jwt.get_unverified_claims(id_token)
    except Exception as e:  # noqa: BLE001
        logger.error("Failed to decode ID token: %s", type(e).__name__)
        return None

    # Only a VERIFIED address is recorded on the key. The app client is public and sets
    # no write_attributes, so a user can change their own `email` with
    # UpdateUserAttributes, and Cognito lets every client write a required attribute
    # whatever its permissions. The new value stays unverified until the code sent to it
    # is entered. Everything that reads the key's address (feedback's reporter, the
    # telemetry identity, the `test` classification) would otherwise trust a value the
    # user typed. Every path that creates a user sets email_verified=true.
    user_email = claims.get("email") if _email_verified(claims) else None
    if claims.get("email") and user_email is None:
        logger.warning("Sign-in with an unverified email: the key records no address")
    groups = claims.get("cognito:groups") or []
    if not groups:
        # A user in no group used to resolve to `admin`, i.e. every cube, so a
        # half-provisioned account (created, group not yet set) was the most
        # privileged account in the pool. No group now means no access.
        logger.warning("Sign-in refused: the account belongs to no Cognito group")
        raise NoProfileError
    profile = groups[0]

    # CONSOLE keys expire with the cookie that carries them (docs/console-spec.md
    # §4.7). Two flows deliberately keep minting non-expiring keys:
    #   * the agent (`session_id`) flow — that key becomes the developer's
    #     long-lived CLI credential; and
    #   * the browser APP-PROXY flow — it predates the console, and this change is
    #     scoped to not alter its behavior (operator decision 2026-07-30).
    # Hence the discriminator is "is the post-login target the console", not the
    # broader "is this any cookie flow".
    is_console_login = bool(safe_next) and session_cookie.is_console_path(safe_next)
    api_key, _ = create_key(
        profile,
        description=f"Browser login: {user_email or 'unknown'}",
        user_email=user_email,
        ttl_seconds=settings.console_key_ttl_seconds if is_console_login else None,
    )

    # Browser flow: carry the key in the parent-domain session cookie and redirect
    # to the originally-requested target (an app subdomain, or the console). 303
    # forces the follow-up to be a GET (both callers are POST handlers).
    if safe_next:
        resp = RedirectResponse(safe_next, status_code=303)
        session_cookie.set_session_cookie(resp, api_key)
        return resp

    # Agent flow: stash the key for the agent's poll loop, show the close-tab page.
    _store_session(session_id, api_key)
    return HTMLResponse(_success_page())


async def auth_login(request: Request) -> HTMLResponse:
    """Render the custom login page.

    Three entry modes:
      * agent flow — ``?session_id=<id>``; the agent polls for the key afterward.
        **Unchanged** — the published CLI depends on this path and its
        close-the-tab success page.
      * browser flow — ``?next=<target>``; on success we set the session cookie
        and redirect back to ``next``. ``next`` is run through the open-redirect
        guard here so a bad value is never reflected into the form (and never
        becomes a redirect target later). Valid targets are an app-proxy
        subdomain URL or a relative console path.
      * bare ``/auth/login`` — neither parameter. Defaults to the console
        (docs/console-spec.md §4.7), so signing in at the apex lands on the UI
        instead of the 400 this used to return.
    """
    # No session_id and no (valid) next ⇒ this is a person signing in at the apex,
    # and `_entry_mode` defaults them to the console. Note that also catches a
    # next which FAILED the guard: falling back to the console is the safe
    # default, and never bounces the browser to the rejected target. Only when
    # the console is actually served here — otherwise the default is a 404.
    session_id, safe_next = _entry_mode(
        request.query_params.get("session_id", ""),
        request.query_params.get("next", ""),
    )

    if not session_id and not safe_next:
        return JSONResponse(status_code=400, content={"error": "session_id or next is required"})

    if not settings.cognito_app_client_id:
        return JSONResponse(
            status_code=503,
            content={"error": "Browser login not configured. Set the CUBE_API_KEY environment variable with a pre-issued key instead."},
        )

    return HTMLResponse(_login_page(session_id, next_url=safe_next))


async def auth_authenticate(request: Request) -> HTMLResponse:
    """Handle login form POST — authenticate via Cognito USER_PASSWORD_AUTH."""
    form = await request.form()
    # `_field`, not `form.get`, for the same reason the reset handlers coerce: a
    # multipart part arrives as an UploadFile, and `validate_next`'s `"\\" in
    # next_url` then raises TypeError -- an unauthenticated 500 on the sign-in
    # endpoint. Pre-existing rather than new here, but it is the same bug as the
    # one being fixed next door, in the same file.
    email = _field(form, "email")
    password = _field(form, "password")
    challenge_session = _field(form, "challenge_session")
    new_password = _field(form, "new_password")
    session_id, safe_next = _entry_mode(_field(form, "session_id"), _field(form, "next"))

    if not session_id and not safe_next:
        return HTMLResponse(_login_page("", error="Invalid session."), status_code=400)

    # Handle NEW_PASSWORD_REQUIRED challenge response
    if challenge_session and new_password:
        result = _respond_to_challenge(challenge_session, email, new_password)
        if result.get("error"):
            return HTMLResponse(
                _new_password_page(session_id, email, challenge_session, error=result["error"], next_url=safe_next)
            )
    else:
        # Initial authentication
        if not email or not password:
            return HTMLResponse(_login_page(session_id, error="Email and password are required.", next_url=safe_next))

        result = _initiate_auth(email, password)
        if result.get("challenge") == "NEW_PASSWORD_REQUIRED":
            return HTMLResponse(_new_password_page(session_id, email, result["session"], next_url=safe_next))
        if result.get("error"):
            return HTMLResponse(_login_page(session_id, error=result["error"], next_url=safe_next))

    # Success — mint this app's credential from the Cognito ID token.
    try:
        resp = _mint_session(result.get("id_token", ""), session_id, safe_next)
    except NoProfileError:
        return HTMLResponse(_login_page(session_id, error=_NO_PROFILE, next_url=safe_next))
    if resp is None:
        return HTMLResponse(_login_page(session_id, error="Authentication failed. Please try again.", next_url=safe_next))
    return resp


async def auth_session(request: Request) -> JSONResponse:
    """Agent polls this to retrieve the provisioned API key."""
    session_id = request.path_params.get("session_id", "")
    if not session_id:
        return JSONResponse(status_code=400, content={"error": "session_id is required"})

    api_key = _retrieve_session(session_id)
    if not api_key:
        return JSONResponse(content={"status": "pending"})

    return JSONResponse(content={"status": "ready", "api_key": api_key})


async def auth_logout(request: Request) -> HTMLResponse:
    """Clear the browser session cookie AND revoke the key it carried.

    Revocation was deliberately omitted originally, on the reasoning that logout
    only needs to drop the browser's copy. That held while browser login was a
    rare developer action. It does not hold for a bookmarked console people open
    daily: without revocation, every sign-in leaves behind a live credential that
    outlives the session, and "sign out" would not actually end access for anyone
    who had captured the cookie (docs/console-spec.md §4.7).

    Best-effort by design — a revocation failure must still clear the cookie, or a
    DynamoDB blip would leave the user unable to sign out at all.
    """
    resp = HTMLResponse(_logout_page())
    raw_key = request.cookies.get(session_cookie.SESSION_COOKIE_NAME)
    if raw_key:
        try:
            api_keys.revoke_key(api_keys.hash_key(raw_key))
        except Exception as e:  # noqa: BLE001 - never block the cookie clear
            logger.warning("logout: could not revoke session key: %s", e)
    session_cookie.clear_session_cookie(resp)
    return resp


# ---------------------------------------------------------------------------
# Self-service password reset
# ---------------------------------------------------------------------------

# Two budgets, because the abuse shapes differ: per-email bounds mailbox spam
# aimed at one victim, per-IP bounds a spray across many addresses. A single
# shared budget would have to be the tighter of the two, which locks out an
# office behind one NAT.
#
# Both are CAPPED (`max_keys`). Every other caller of this limiter keys on an
# authenticated session hash — a handful of principals — and its docstring says
# in as many words that an uncapped dict is only safe because of that. These
# keys are a submitted address and a client IP, i.e. attacker-varied, so without
# the cap the limiter would be a memory-exhaustion vector rather than a defence.
_reset_email_limiter = SlidingWindowRateLimiter(
    max_requests=settings.password_reset_rate_limit_per_email,
    window_seconds=settings.password_reset_rate_limit_window_seconds,
    max_keys=settings.password_reset_rate_limit_max_keys,
)
_reset_ip_limiter = SlidingWindowRateLimiter(
    max_requests=settings.password_reset_rate_limit_per_ip,
    window_seconds=settings.password_reset_rate_limit_window_seconds,
    max_keys=settings.password_reset_rate_limit_max_keys,
)

_THROTTLED = "Too many reset attempts. Please wait a while and try again."
_PASSWORD_UPDATED = "Password updated. Please sign in with your new password."


def _field(form, name: str) -> str:
    """One form value, as a string, or "".

    Starlette hands back an `UploadFile` for a multipart part, and these are
    unauthenticated endpoints anyone can post multipart to -- so reading a field
    without this turns a hostile request into a 500 the moment anything calls
    `.strip()` on it.
    """
    value = form.get(name, "")
    return value if isinstance(value, str) else ""


def _client_ip(request: Request) -> str:
    """The address the ALB saw, for rate-limit keying.

    The RIGHTMOST `X-Forwarded-For` entry, not the leftmost. Everything to the
    left of it was supplied by the caller and is therefore forgeable, and for a
    limiter a forgeable key is worse than no key at all: it buys both evasion
    (vary the header, get a fresh budget every request) and unbounded growth of
    the key set. `telemetry/events.py::_caller_ip` reads the LEFTMOST on purpose
    — best-effort attribution can live with a spoofed value — so the two
    deliberately disagree, and neither should be "unified" into the other.

    Sound because the public domains are Cloudflare DNS-only CNAMEs straight to
    the ALB (AGENTS.md, Branching & CI/CD), so the entry the ALB appends really
    is the user. If Cloudflare is ever switched to proxied, that entry becomes
    Cloudflare's and every user in the world collapses onto a handful of keys —
    revisit here in the same change.
    """
    xff = request.headers.get("x-forwarded-for", "")
    if xff:
        rightmost = xff.rsplit(",", 1)[-1].strip()
        if rightmost:
            return rightmost
    client = getattr(request, "client", None)
    return getattr(client, "host", None) or "unknown"


def _reset_ip_allowed(request: Request) -> bool:
    """The per-IP budget, checked BEFORE the request body is read.

    Ordering, not decoration: parsing first means the expensive part happens
    ungated on an endpoint anyone can reach. This bounds the NUMBER of bodies one
    caller can make us buffer; `_read_form_capped` bounds the size of each. Both
    are needed -- an earlier revision had only this one and claimed in its own
    docstring to bound buffering, which a single 200 MB body disproved.
    """
    return _reset_ip_limiter.allow(f"ip:{_client_ip(request)}")


def _reset_email_allowed(email: str) -> bool:
    """The per-email budget. Checked after the body, because it needs the body.

    Separate from the IP budget so neither can be exhausted while hiding behind
    the other: both are consulted and both record a hit.

    The key is a HASH, not the address. `max_keys` caps how many keys are
    retained but says nothing about how large one may be, so keying on the raw
    submitted string let a caller park arbitrarily long attacker-chosen strings
    in the limiter for a full window -- the same exhaustion the cap was added to
    prevent, scaled by key size instead of key count. A fixed-width digest also
    means no cleartext address sits in process memory for an hour, which the
    telemetry boundary already treats as the right default.
    """
    digest = hashlib.sha256(email.strip().lower().encode("utf-8")).hexdigest()
    return _reset_email_limiter.allow(f"email:{digest}")


async def _read_form_capped(request: Request) -> dict[str, str] | None:
    """Parse a urlencoded reset form, or None if the body is over the cap.

    `request.form()` is deliberately NOT used. It buffers the whole body with no
    size limit of its own for urlencoded input (`max_part_size` and friends are
    multipart-only), which on an unauthenticated endpoint is a memory-exhaustion
    vector. `read_request_body_capped` is the repo's existing answer to exactly
    this -- it streams and aborts, rather than trusting the client's
    Content-Length, which is only a claim.

    Parsing urlencoded ourselves also means multipart simply yields no fields
    here, which is the right answer for a login form and removes the
    `UploadFile`-shaped surface entirely rather than coercing it after the fact.
    """
    try:
        raw = await read_request_body_capped(
            request, settings.password_reset_max_body_bytes)
    except RequestBodyTooLarge:
        return None
    try:
        return dict(parse_qsl(raw.decode("utf-8"), keep_blank_values=True))
    except UnicodeDecodeError:
        return {}


async def auth_forgot(request: Request) -> HTMLResponse:
    """Render the 'send me a reset code' page."""
    session_id, safe_next = _entry_mode(
        request.query_params.get("session_id", ""),
        request.query_params.get("next", ""),
    )
    if not session_id and not safe_next:
        return JSONResponse(status_code=400, content={"error": "session_id or next is required"})
    if not settings.cognito_app_client_id:
        return JSONResponse(
            status_code=503,
            content={"error": "Browser login not configured. Set the CUBE_API_KEY environment variable with a pre-issued key instead."},
        )
    return HTMLResponse(_forgot_page(session_id, next_url=safe_next))


async def auth_forgot_submit(request: Request) -> HTMLResponse:
    """Request a reset code — and answer IDENTICALLY whatever Cognito said.

    This is the security property of the whole feature, so it is worth stating
    plainly: past the two guard clauses below, exactly one page is returned. No
    branch on the Cognito outcome may reach the rendered HTML, because each of
    those outcomes is a fact about someone else's account (see
    :func:`_forgot_password`).

    The throttle branch is the one visible difference, and it does not leak:
    our own per-email budget is spent by repetition alone, whether or not the
    address exists, and it is deliberately tighter than Cognito's per-USER
    budget — which would only ever be reached for a real account — so that
    Cognito's throttle stays out of reach as a signal.
    """
    if not _reset_ip_allowed(request):
        return HTMLResponse(_forgot_page("", error=_THROTTLED), status_code=429)

    form = await _read_form_capped(request)
    if form is None:
        return HTMLResponse(_forgot_page("", error="That request was too large."),
                            status_code=413)
    email = _field(form, "email").strip()
    session_id, safe_next = _entry_mode(_field(form, "session_id"), _field(form, "next"))

    if not session_id and not safe_next:
        return HTMLResponse(_forgot_page("", error="Invalid session."), status_code=400)
    if not email:
        return HTMLResponse(_forgot_page(session_id, error="Email is required.", next_url=safe_next))
    if not _reset_email_allowed(email):
        return HTMLResponse(_forgot_page(session_id, error=_THROTTLED, next_url=safe_next))

    _forgot_password(email)
    return HTMLResponse(_reset_page(session_id, email, next_url=safe_next))


async def auth_reset(request: Request) -> HTMLResponse:
    """Render the 'I have a code' page.

    Reachable directly, not only as the POST target above, so a code that
    arrives after the user closed the tab is still usable.
    """
    session_id, safe_next = _entry_mode(
        request.query_params.get("session_id", ""),
        request.query_params.get("next", ""),
    )
    if not session_id and not safe_next:
        return JSONResponse(status_code=400, content={"error": "session_id or next is required"})
    if not settings.cognito_app_client_id:
        return JSONResponse(
            status_code=503,
            content={"error": "Browser login not configured. Set the CUBE_API_KEY environment variable with a pre-issued key instead."},
        )
    return HTMLResponse(_reset_page(session_id, next_url=safe_next))


async def auth_reset_submit(request: Request) -> Response:
    """Redeem the code, set the password, and sign the user straight in.

    The ordering matters on the failure paths. Once `ConfirmForgotPassword`
    returns, the new password is DURABLE — so from that line on, nothing may
    render as an error. The automatic sign-in is a convenience layered on top of
    a change that already succeeded; if it falls over for any reason, the user
    is sent to the sign-in page with a NOTICE saying the password was updated,
    never an error box implying it was not. Telling someone their reset failed
    when it did not is the one message most likely to make them try again and
    burn their remaining attempts.
    """
    if not _reset_ip_allowed(request):
        return HTMLResponse(_reset_page("", error=_THROTTLED), status_code=429)

    form = await _read_form_capped(request)
    if form is None:
        return HTMLResponse(_reset_page("", error="That request was too large."),
                            status_code=413)
    email = _field(form, "email").strip()
    code = _field(form, "code").strip()
    new_password = _field(form, "new_password")
    confirm_password = _field(form, "confirm_password")
    session_id, safe_next = _entry_mode(_field(form, "session_id"), _field(form, "next"))

    if not session_id and not safe_next:
        return HTMLResponse(_reset_page("", error="Invalid session."), status_code=400)
    if not (email and code and new_password):
        return HTMLResponse(_reset_page(session_id, email, next_url=safe_next,
                                        error="Email, code, and a new password are all required."))
    # Re-checked here because the page's `validatePasswords()` runs in the
    # user's browser and so is a convenience, not a validation.
    if new_password != confirm_password:
        return HTMLResponse(_reset_page(session_id, email, next_url=safe_next,
                                        error="Passwords do not match."))
    if not _reset_email_allowed(email):
        return HTMLResponse(_reset_page(session_id, email, next_url=safe_next, error=_THROTTLED))

    result = _confirm_forgot_password(email, code, new_password)
    if result.get("error"):
        return HTMLResponse(_reset_page(session_id, email, next_url=safe_next, error=result["error"]))

    # --- the password is now changed and durable; no error pages past here ---
    #
    # The try/except is part of that rule, not defensive noise. Enforcing it only
    # against RETURN values left the exception path open: `create_key` or
    # `_store_session` hitting a DynamoDB blip propagated out as a 500, after the
    # password had already changed -- which is exactly the "your reset failed"
    # message the rule exists to prevent, in its worst form.
    try:
        auth = _initiate_auth(email, new_password)
        resp = _mint_session(auth.get("id_token", ""), session_id, safe_next)
    except NoProfileError:
        # Not a failure of the reset. The user meets `_NO_PROFILE` when they sign in.
        resp = None
    except Exception as e:  # noqa: BLE001
        logger.error("Reset succeeded but session minting failed: %s", type(e).__name__)
        resp = None
    if resp is None:
        logger.info("Reset succeeded but auto sign-in did not; sending user to sign in.")
        return HTMLResponse(_login_page(session_id, next_url=safe_next, notice=_PASSWORD_UPDATED))
    return resp
