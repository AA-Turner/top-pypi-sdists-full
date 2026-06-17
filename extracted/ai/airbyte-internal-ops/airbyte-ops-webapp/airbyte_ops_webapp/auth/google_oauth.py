"""Google OAuth helpers for BigQuery user-token authentication."""

from __future__ import annotations

import base64
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from fastmcp import FastMCP
from prefab_ui.actions import Fetch, SetState
from prefab_ui.rx import RESULT, STATE
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse

GOOGLE_CLIENT_ID_ENV_VAR = "AIRBYTE_OPS_WEBAPP_GOOGLE_CLIENT_ID"
DEFAULT_GOOGLE_CLIENT_ID = (
    "351139268520-qauoed89jqafh9358lffkmv8nmkt9m95.apps.googleusercontent.com"
)
GOOGLE_CLIENT_SECRET_ENV_VAR = "AIRBYTE_OPS_WEBAPP_GOOGLE_CLIENT_SECRET"
_REFRESH_TOKEN_COOKIE_MAX_AGE = 30 * 86400  # 30 days
GOOGLE_AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
GOOGLE_OAUTH_CALLBACK_PATH = "/google-oauth/callback"
GOOGLE_OAUTH_SESSION_PATH = "/google-oauth/session"
GOOGLE_OAUTH_TOKEN_PATH = "/google-oauth/token"
GOOGLE_SESSION_COOKIE_NAME = "airbyte_ops_webapp_google_session"
GOOGLE_SCOPES = "openid email profile https://www.googleapis.com/auth/bigquery"


def google_oauth_config() -> dict[str, str | bool]:
    """Return Google OAuth configuration for client-side use."""
    return {
        "enabled": _google_oauth_enabled(),
        "client_id": _google_client_id(),
        "redirect_uri": _google_oauth_redirect_uri(),
        "authorization_endpoint": GOOGLE_AUTH_ENDPOINT,
        "token_endpoint": GOOGLE_TOKEN_ENDPOINT,
        "session_endpoint": GOOGLE_OAUTH_SESSION_PATH,
        "token_exchange_endpoint": GOOGLE_OAUTH_TOKEN_PATH,
        "scopes": GOOGLE_SCOPES,
    }


def register_google_oauth_routes(mcp: FastMCP) -> None:
    """Register Google OAuth routes on the FastMCP server."""
    mcp.custom_route(
        GOOGLE_OAUTH_CALLBACK_PATH,
        methods=["GET"],
        name="ops_google_oauth_callback",
    )(google_oauth_callback_response)
    mcp.custom_route(
        GOOGLE_OAUTH_TOKEN_PATH,
        methods=["POST"],
        name="ops_google_oauth_token",
    )(google_oauth_token_response)
    mcp.custom_route(
        GOOGLE_OAUTH_SESSION_PATH,
        methods=["GET", "POST", "DELETE"],
        name="ops_google_oauth_session",
    )(google_oauth_session_response)


def hydrate_google_oauth_action() -> Fetch:
    """Return a Fetch action that hydrates Google OAuth state from the session cookie."""
    return Fetch.get(
        GOOGLE_OAUTH_SESSION_PATH,
        on_success=[
            SetState("google_authenticated", RESULT.google_authenticated),
            SetState("google_user_email", RESULT.google_user_email),
            SetState("google_access_token", RESULT.google_access_token),
            SetState("google_status", RESULT.google_status),
        ],
        on_error=[
            SetState("google_authenticated", STATE.google_authenticated),
            SetState("google_user_email", STATE.google_user_email),
            SetState("google_access_token", STATE.google_access_token),
            SetState("google_status", "Unable to refresh Google session."),
        ],
    )


async def google_oauth_callback_response(_request: Request) -> HTMLResponse:
    """Serve the Google OAuth callback page."""
    config = google_oauth_config()
    return HTMLResponse(
        _google_oauth_callback_html(config),
        headers={"Content-Security-Policy": _google_oauth_callback_csp()},
    )


async def google_oauth_token_response(request: Request) -> JSONResponse:
    """Exchange Google authorization code for tokens server-side."""
    try:
        body = await request.json()
    except (json.JSONDecodeError, ValueError):
        return _json_response({"error": "invalid_request"}, 400)

    if not isinstance(body, dict):
        return _json_response({"error": "invalid_request"}, 400)
    code = body.get("code", "")
    code_verifier = body.get("code_verifier", "")
    if not code or not code_verifier:
        return _json_response({"error": "missing_code_or_verifier"}, 400)

    try:
        token_response = _exchange_google_token(code, code_verifier)
    except GoogleOAuthError as exc:
        return _json_response(
            {"error": exc.error, "error_description": exc.description},
            exc.status_code,
        )

    return _json_response(token_response)


async def google_oauth_session_response(request: Request) -> JSONResponse:
    """Manage the Google OAuth session cookie."""
    if request.method == "DELETE":
        return _delete_google_session_response()

    if request.method == "POST":
        try:
            body = await request.json()
        except (json.JSONDecodeError, ValueError):
            return _json_response({"error": "invalid_request"}, 400)

        if not isinstance(body, dict):
            return _json_response({"error": "invalid_request"}, 400)
        access_token = body.get("access_token", "")
        if not access_token:
            return _json_response({"error": "missing_access_token"}, 400)

        session_payload = _google_session_payload(body)
        state = _google_session_state(session_payload)
        response = _json_response(state)
        try:
            _set_google_session_cookie(request, response, session_payload)
        except GoogleOAuthError:
            return _json_response(
                {
                    "error": "server_error",
                    "error_description": "Session secret missing.",
                },
                500,
            )
        return response

    # GET: hydrate from cookie
    cookie_value = request.cookies.get(GOOGLE_SESSION_COOKIE_NAME, "")
    if not cookie_value:
        return _json_response(_signed_out_google_state())

    try:
        session_payload = _decode_google_session(cookie_value)
    except GoogleOAuthError:
        return _delete_google_session_response()
    if not session_payload:
        return _delete_google_session_response()

    expires_at = _int_value(session_payload.get("expires_at"))
    if expires_at and expires_at <= _now_ms():
        refresh_token = str(session_payload.get("refresh_token", ""))
        if not refresh_token:
            return _delete_google_session_response()
        return _refresh_google_session_response(request, session_payload)

    return _json_response(_google_session_state(session_payload))


def _refresh_google_session_response(
    request: Request,
    session_payload: dict[str, object],
) -> JSONResponse:
    refresh_token = str(session_payload.get("refresh_token", ""))
    if not refresh_token:
        resp = _json_response(_signed_out_google_state("Google session expired."))
        _clear_google_session_cookie(resp)
        return resp

    try:
        token_response = _refresh_google_token(refresh_token)
    except GoogleOAuthError:
        resp = _json_response(_signed_out_google_state("Google session expired."))
        _clear_google_session_cookie(resp)
        return resp

    new_access_token = token_response.get("access_token", "")
    if not new_access_token:
        resp = _json_response(_signed_out_google_state("Google session expired."))
        _clear_google_session_cookie(resp)
        return resp

    refreshed_payload = _google_session_payload(
        {
            "access_token": new_access_token,
            "email": session_payload.get("email"),
            "expires_in": token_response.get("expires_in"),
            "refresh_token": token_response.get("refresh_token") or refresh_token,
        }
    )
    state = _google_session_state(refreshed_payload)
    response = _json_response(state)
    try:
        _set_google_session_cookie(request, response, refreshed_payload)
    except GoogleOAuthError:
        return _json_response(
            {"error": "server_error", "error_description": "Session secret missing."},
            500,
        )
    return response


def _delete_google_session_response() -> JSONResponse:
    response = _json_response(_signed_out_google_state("Signed out of Google."))
    _clear_google_session_cookie(response)
    return response


def _signed_out_google_state(status: str = "") -> dict[str, object]:
    return {
        "google_authenticated": False,
        "google_user_email": "",
        "google_access_token": "",
        "google_status": status,
    }


def _google_session_state(session_payload: dict[str, object]) -> dict[str, object]:
    email = str(session_payload.get("email", ""))
    token = str(session_payload.get("access_token", ""))
    return {
        "google_authenticated": True,
        "google_user_email": email,
        "google_access_token": token,
        "google_status": (email and f"Signed in as {email}") or "Signed in with Google",
    }


def _google_session_payload(payload: dict[str, object]) -> dict[str, object]:
    access_token = str(payload.get("access_token", "") or "")
    email = str(payload.get("email", "") or "")
    expires_in = _int_value(payload.get("expires_in"))
    if expires_in <= 0:
        expires_in = 3600
    expires_at = _now_ms() + expires_in * 1000
    result: dict[str, object] = {
        "access_token": access_token,
        "email": email,
        "expires_at": expires_at,
    }
    refresh_token = str(payload.get("refresh_token", "") or "")
    if refresh_token:
        result["refresh_token"] = refresh_token
    return result


def _exchange_google_token(code: str, code_verifier: str) -> dict[str, object]:
    config = google_oauth_config()
    client_secret = os.getenv(GOOGLE_CLIENT_SECRET_ENV_VAR, "").strip()
    token_request = {
        "grant_type": "authorization_code",
        "client_id": _google_client_id(),
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": str(config["redirect_uri"]),
        "code_verifier": code_verifier,
    }
    return _send_google_token_request(token_request)


def _refresh_google_token(refresh_token: str) -> dict[str, object]:
    client_secret = os.getenv(GOOGLE_CLIENT_SECRET_ENV_VAR, "").strip()
    token_request = {
        "grant_type": "refresh_token",
        "client_id": _google_client_id(),
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    }
    return _send_google_token_request(token_request)


def _send_google_token_request(token_request: dict[str, str]) -> dict[str, object]:
    request_body = urllib.parse.urlencode(token_request).encode()
    req = urllib.request.Request(
        GOOGLE_TOKEN_ENDPOINT,
        data=request_body,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as error:
        try:
            error_body = json.loads(error.read())
        except (json.JSONDecodeError, ValueError):
            error_body = {}
        raise GoogleOAuthError(
            error.code,
            str(error_body.get("error", "token_exchange_failed")),
            str(error_body.get("error_description", "Google token exchange failed.")),
        ) from None
    except urllib.error.URLError as error:
        raise GoogleOAuthError(
            502, "token_exchange_failed", str(error.reason)
        ) from None


# --- Session cookie encryption ---


def _set_google_session_cookie(
    request: Request,
    response: JSONResponse,
    session_payload: dict[str, object],
) -> None:
    encoded = _encode_google_session(session_payload)
    expires_at = _int_value(session_payload.get("expires_at"))
    has_refresh = bool(session_payload.get("refresh_token"))
    if has_refresh:
        max_age = _REFRESH_TOKEN_COOKIE_MAX_AGE
    elif expires_at:
        max_age = max(0, (expires_at - _now_ms()) // 1000)
    else:
        max_age = 3600
    secure = _request_is_secure(request)
    response.set_cookie(
        GOOGLE_SESSION_COOKIE_NAME,
        encoded,
        max_age=max_age,
        path="/",
        httponly=True,
        secure=secure,
        samesite="lax",
    )


def _clear_google_session_cookie(response: JSONResponse) -> None:
    response.delete_cookie(GOOGLE_SESSION_COOKIE_NAME, path="/", samesite="lax")


def _encode_google_session(session_payload: dict[str, object]) -> str:
    payload_json = json.dumps(
        session_payload, sort_keys=True, separators=(",", ":")
    ).encode()
    return _google_session_cipher().encrypt(payload_json).decode()


def _decode_google_session(cookie_value: str) -> dict[str, object] | None:
    if not cookie_value:
        return None
    try:
        decoded = json.loads(_google_session_cipher().decrypt(cookie_value.encode()))
    except (InvalidToken, json.JSONDecodeError):
        return None
    if not isinstance(decoded, dict):
        return None
    if not decoded.get("access_token"):
        return None
    return decoded


def _google_session_cipher() -> Fernet:
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"airbyte-ops-webapp-google-session",
        info=b"fernet-key",
    ).derive(_google_session_secret())
    key = base64.urlsafe_b64encode(derived_key)
    return Fernet(key)


def _google_session_secret() -> bytes:
    value = os.getenv(GOOGLE_CLIENT_SECRET_ENV_VAR, "").strip()
    if not value:
        raise GoogleOAuthError(
            500,
            "server_error",
            f"{GOOGLE_CLIENT_SECRET_ENV_VAR} is required for Google OAuth.",
        )
    return value.encode()


# --- Helpers ---


def _google_client_id() -> str:
    return os.getenv(GOOGLE_CLIENT_ID_ENV_VAR, DEFAULT_GOOGLE_CLIENT_ID).strip()


def _google_oauth_enabled() -> bool:
    return bool(os.getenv(GOOGLE_CLIENT_SECRET_ENV_VAR, "").strip())


def _google_oauth_redirect_uri() -> str:
    public_url = os.getenv("AIRBYTE_OPS_WEBAPP_PUBLIC_URL", "").strip().rstrip("/")
    if public_url:
        return f"{public_url}{GOOGLE_OAUTH_CALLBACK_PATH}"
    return f"http://localhost:3000{GOOGLE_OAUTH_CALLBACK_PATH}"


def _request_is_secure(request: Request) -> bool:
    forwarded_proto = request.headers.get("x-forwarded-proto", "")
    first_proto = forwarded_proto.split(",", 1)[0].strip().lower()
    return request.url.scheme == "https" or first_proto == "https"


def _now_ms() -> int:
    return int(time.time() * 1000)


def _int_value(value: object) -> int:
    if isinstance(value, bool):
        return 0
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return 0


def _json_response(data: dict[str, object], status_code: int = 200) -> JSONResponse:
    response = JSONResponse(data, status_code=status_code)
    response.headers["Cache-Control"] = "no-store"
    return response


def _google_oauth_callback_csp() -> str:
    """Return a Content-Security-Policy header for the Google OAuth callback page."""
    return (
        "default-src 'none'; "
        "base-uri 'none'; "
        "connect-src 'self'; "
        "form-action 'none'; "
        "frame-ancestors 'none'; "
        "script-src 'unsafe-inline'"
    )


class GoogleOAuthError(Exception):
    """Google OAuth operation failed."""

    def __init__(self, status_code: int, error: str, description: str) -> None:
        super().__init__(description)
        self.status_code = status_code
        self.error = error
        self.description = description


# --- JS Actions for Google OAuth ---

GOOGLE_OAUTH_JS_ACTIONS = {
    "hydrateGoogleOAuth": r"""async (...args) => {
      const state = args[0]?.state || args[0] || {};
      const config = state.google_oauth_config || {};
      if (!config.enabled) {
        return {
          google_authenticated: false,
          google_user_email: "",
          google_access_token: "",
          google_status: "Google OAuth not configured.",
        };
      }
      try {
        const response = await fetch(config.session_endpoint || "/google-oauth/session", {
          credentials: "same-origin",
          headers: { "Accept": "application/json" },
        });
        if (response.ok) {
          return await response.json();
        }
      } catch {}
      return {
        google_authenticated: false,
        google_user_email: "",
        google_access_token: "",
        google_status: "",
      };
    }""",
    "startGoogleOAuth": r"""async (...args) => {
      const state = args[0]?.state || args[0] || {};
      const config = state.google_oauth_config || {};
      if (!config.enabled) {
        alert("Google OAuth is not configured on this server. Set the AIRBYTE_OPS_WEBAPP_GOOGLE_CLIENT_SECRET env var and restart.");
        return { google_status: "Google OAuth is not configured on this server." };
      }
      const navigationLocation = window.top?.location || window.location;
      let browserCrypto = globalThis.crypto;
      if (!browserCrypto?.subtle) {
        try { browserCrypto = window.top?.crypto || browserCrypto; } catch { browserCrypto = globalThis.crypto; }
      }
      if (!browserCrypto?.getRandomValues || !browserCrypto?.subtle) {
        return { google_status: "Browser WebCrypto is unavailable; use localhost or HTTPS." };
      }
      const base64Url = (bytes) => btoa(String.fromCharCode(...bytes))
        .replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
      const verifierBytes = new Uint8Array(64);
      browserCrypto.getRandomValues(verifierBytes);
      const codeVerifier = base64Url(verifierBytes);
      const digest = await browserCrypto.subtle.digest("SHA-256", new TextEncoder().encode(codeVerifier));
      const codeChallenge = base64Url(new Uint8Array(digest));
      const stateBytes = new Uint8Array(32);
      browserCrypto.getRandomValues(stateBytes);
      const oauthState = base64Url(stateBytes);
      const nonceBytes = new Uint8Array(32);
      browserCrypto.getRandomValues(nonceBytes);
      const nonce = base64Url(nonceBytes);
      sessionStorage.setItem("google_oauth_code_verifier", codeVerifier);
      sessionStorage.setItem("google_oauth_state", oauthState);
      sessionStorage.setItem("google_oauth_nonce", nonce);
      sessionStorage.setItem("google_oauth_return_to", navigationLocation.href);
      const params = new URLSearchParams({
        client_id: config.client_id,
        redirect_uri: config.redirect_uri,
        response_type: "code",
        scope: config.scopes || "openid email profile https://www.googleapis.com/auth/bigquery",
        state: oauthState,
        nonce,
        code_challenge: codeChallenge,
        code_challenge_method: "S256",
        access_type: "offline",
        prompt: "consent",
      });
      navigationLocation.assign(`${config.authorization_endpoint}?${params.toString()}`);
      return { google_status: "Redirecting to Google..." };
    }""",
    "logoutGoogleOAuth": r"""async (...args) => {
      const state = args[0]?.state || args[0] || {};
      const config = state.google_oauth_config || {};
      try {
        await fetch(config.session_endpoint || "/google-oauth/session", {
          method: "DELETE",
          credentials: "same-origin",
          headers: { "Accept": "application/json" },
        });
      } catch {}
      sessionStorage.removeItem("google_oauth_code_verifier");
      sessionStorage.removeItem("google_oauth_state");
      sessionStorage.removeItem("google_oauth_nonce");
      sessionStorage.removeItem("google_oauth_return_to");
      return {
        google_authenticated: false,
        google_user_email: "",
        google_access_token: "",
        google_status: "Signed out of Google.",
      };
    }""",
}


def _google_oauth_callback_html(config: dict[str, str | bool]) -> str:
    config_json = json.dumps(config).replace("</", r"<\/")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Google OAuth Callback</title>
</head>
<body>
  <p id="status">Completing Google sign-in...</p>
  <script>
const config = {config_json};
const statusEl = document.getElementById("status");
const decodeJwtPayload = (token) => {{
  const payload = token.split(".")[1];
  if (!payload) return {{}};
  const padded = payload.replace(/-/g, "+").replace(/_/g, "/") + "=".repeat((4 - payload.length % 4) % 4);
  return JSON.parse(atob(padded));
}};
const sameOriginReturnTo = (value) => {{
  try {{
    const url = new URL(value || "/authorization", window.location.origin);
    return url.origin === window.location.origin ? url.toString() : "/authorization";
  }} catch {{
    return "/authorization";
  }}
}};
(async () => {{
  try {{
    const params = new URLSearchParams(window.location.search);
    const error = params.get("error");
    if (error) {{
      throw new Error(`${{error}}: ${{params.get("error_description") || "Google rejected the request"}}`);
    }}
    const code = params.get("code");
    const returnedState = params.get("state");
    const expectedState = sessionStorage.getItem("google_oauth_state");
    const expectedNonce = sessionStorage.getItem("google_oauth_nonce");
    const codeVerifier = sessionStorage.getItem("google_oauth_code_verifier");
    if (!code || !returnedState || !expectedState || returnedState !== expectedState || !codeVerifier || !expectedNonce) {{
      throw new Error("Google OAuth callback state is invalid or incomplete.");
    }}
    const response = await fetch(config.token_exchange_endpoint, {{
      method: "POST",
      headers: {{ "Content-Type": "application/json" }},
      body: JSON.stringify({{ code, code_verifier: codeVerifier }}),
    }});
    const tokenResponse = await response.json();
    if (!response.ok || !tokenResponse.access_token) {{
      throw new Error(tokenResponse.error_description || tokenResponse.error || "Token exchange failed.");
    }}
    if (!tokenResponse.id_token) {{
      throw new Error("Google token response did not include an ID token.");
    }}
    const claims = decodeJwtPayload(tokenResponse.id_token);
    if (claims.nonce !== expectedNonce) {{
      throw new Error("Google OAuth callback nonce is invalid.");
    }}
    const email = claims.email || "";
    const sessionResponse = await fetch(config.session_endpoint, {{
      method: "POST",
      credentials: "same-origin",
      headers: {{ "Content-Type": "application/json" }},
      body: JSON.stringify({{
        access_token: tokenResponse.access_token,
        email,
        expires_in: tokenResponse.expires_in || 3600,
        refresh_token: tokenResponse.refresh_token || "",
      }}),
    }});
    const sessionBody = await sessionResponse.json();
    if (!sessionResponse.ok || !sessionBody.google_authenticated) {{
      throw new Error(sessionBody.error_description || sessionBody.error || "Google session setup failed.");
    }}
    sessionStorage.removeItem("google_oauth_code_verifier");
    sessionStorage.removeItem("google_oauth_state");
    sessionStorage.removeItem("google_oauth_nonce");
    const returnTo = sameOriginReturnTo(sessionStorage.getItem("google_oauth_return_to"));
    sessionStorage.removeItem("google_oauth_return_to");
    window.location.replace(returnTo);
  }} catch (error) {{
    statusEl.textContent = error instanceof Error ? error.message : String(error);
  }}
}})();
  </script>
</body>
</html>"""
