"""OAuth helpers for the connector version manager webapp."""

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

from airbyte_ops_webapp.auth.mock_session import (
    mock_oauth_login,
    mock_oauth_logout,
    mock_oauth_session_state,
)
from airbyte_ops_webapp.state import (
    OAUTH_CLIENT_ID_ENV_VAR,
    OAUTH_CLIENT_SECRET_ENV_VAR,
    OAUTH_ENABLED_ENV_VAR,
    OAUTH_ISSUER_ENV_VAR,
    OAUTH_PUBLIC_URL_ENV_VAR,
    OAUTH_REDIRECT_URI_ENV_VAR,
    mock_only_enabled,
)

DEFAULT_OAUTH_CLIENT_ID = "airbyte-ops-webapp-client"
DEFAULT_OAUTH_ISSUER = "https://cloud.airbyte.com/auth/realms/airbyte"
DEFAULT_OAUTH_LOCAL_REDIRECT_URI = "http://localhost:3000/oauth/callback"
OAUTH_CALLBACK_PATH = "/oauth/callback"
OAUTH_SESSION_COOKIE_NAME = "airbyte_ops_webapp_session"
OAUTH_SESSION_PATH = "/oauth/session"
OAUTH_TOKEN_PATH = "/oauth/token"


def oauth_config() -> dict[str, str | bool]:
    issuer = os.getenv(OAUTH_ISSUER_ENV_VAR, DEFAULT_OAUTH_ISSUER).strip().rstrip("/")
    return {
        "enabled": _oauth_enabled(),
        "issuer": issuer,
        "client_id": os.getenv(
            OAUTH_CLIENT_ID_ENV_VAR, DEFAULT_OAUTH_CLIENT_ID
        ).strip(),
        "redirect_uri": _oauth_redirect_uri(),
        "authorization_endpoint": f"{issuer}/protocol/openid-connect/auth",
        "token_endpoint": f"{issuer}/protocol/openid-connect/token",
        "session_endpoint": OAUTH_SESSION_PATH,
        "token_exchange_endpoint": OAUTH_TOKEN_PATH,
    }


def register_oauth_routes(mcp: FastMCP) -> None:
    mcp.custom_route(OAUTH_CALLBACK_PATH, methods=["GET"], name="ops_oauth_callback")(
        oauth_callback_response
    )
    mcp.custom_route(OAUTH_TOKEN_PATH, methods=["POST"], name="ops_oauth_token")(
        oauth_token_response
    )
    mcp.custom_route(
        OAUTH_SESSION_PATH,
        methods=["GET", "POST", "DELETE"],
        name="ops_oauth_session",
    )(oauth_session_response)


def hydrate_oauth_action() -> Fetch:
    return Fetch.get(
        OAUTH_SESSION_PATH,
        on_success=[
            SetState("auth_bearer_token", RESULT.auth_bearer_token),
            SetState(
                "admin_user_email", RESULT.admin_user_email | STATE.admin_user_email
            ),
            SetState("oauth_authenticated", RESULT.oauth_authenticated),
            SetState("oauth_user_email", RESULT.oauth_user_email),
            SetState("oauth_status", RESULT.oauth_status),
        ],
        on_error=[
            SetState("auth_bearer_token", STATE.auth_bearer_token),
            SetState("admin_user_email", STATE.admin_user_email),
            SetState("oauth_authenticated", STATE.oauth_authenticated),
            SetState("oauth_user_email", STATE.oauth_user_email),
            SetState("oauth_status", "Unable to refresh OAuth session. Sign in again."),
        ],
    )


def mock_login_oauth_action() -> Fetch:
    """Return a Fetch action that simulates OAuth login in mock mode."""
    return Fetch.post(
        OAUTH_SESSION_PATH,
        body={"mock": True},
        on_success=[
            SetState("auth_bearer_token", RESULT.auth_bearer_token),
            SetState("admin_user_email", RESULT.admin_user_email),
            SetState("oauth_authenticated", RESULT.oauth_authenticated),
            SetState("oauth_user_email", RESULT.oauth_user_email),
            SetState("oauth_status", RESULT.oauth_status),
        ],
    )


def mock_logout_oauth_action() -> Fetch:
    """Return a Fetch action that simulates OAuth logout in mock mode."""
    return Fetch.delete(
        OAUTH_SESSION_PATH,
        on_success=[
            SetState("auth_bearer_token", RESULT.auth_bearer_token),
            SetState("admin_user_email", RESULT.admin_user_email),
            SetState("oauth_authenticated", RESULT.oauth_authenticated),
            SetState("oauth_user_email", RESULT.oauth_user_email),
            SetState("oauth_status", RESULT.oauth_status),
        ],
    )


def logout_oauth_action() -> Fetch:
    """Return a Fetch action that logs out of Airbyte and updates UI state."""
    return Fetch.delete(
        OAUTH_SESSION_PATH,
        on_success=[
            SetState("oauth_authenticated", False),
            SetState("oauth_user_email", ""),
            SetState("auth_bearer_token", ""),
            SetState("oauth_status", "Signed out of Airbyte."),
        ],
        on_error=[
            SetState("oauth_status", "Airbyte logout failed. Please try again."),
        ],
    )


async def oauth_callback_response(_request: Request) -> HTMLResponse:
    config = oauth_config()
    return HTMLResponse(
        _oauth_callback_html(config),
        headers={"Content-Security-Policy": _oauth_callback_csp(config)},
    )


async def oauth_token_response(request: Request) -> JSONResponse:
    payload = await request.json()
    code = str(payload.get("code", "")).strip() if isinstance(payload, dict) else ""
    code_verifier = (
        str(payload.get("code_verifier", "")).strip()
        if isinstance(payload, dict)
        else ""
    )
    if not code or not code_verifier:
        return _json_no_store_response(
            {
                "error": "invalid_request",
                "error_description": "OAuth token exchange requires code and code_verifier.",
            },
            status_code=400,
        )

    try:
        return _json_no_store_response(_exchange_oauth_token(code, code_verifier))
    except OAuthTokenExchangeError as error:
        return _json_no_store_response(
            {
                "error": error.error,
                "error_description": error.description,
            },
            status_code=error.status_code,
        )


async def oauth_session_response(request: Request) -> JSONResponse:
    if mock_only_enabled():
        return _mock_oauth_session_response(request)
    if request.method == "DELETE":
        return _delete_session_response()
    if request.method == "GET":
        return _get_session_response(request)
    try:
        payload = await request.json()
    except json.JSONDecodeError:
        return _json_no_store_response(
            {
                "error": "invalid_request",
                "error_description": "OAuth session request body must be valid JSON.",
            },
            status_code=400,
        )
    return _create_session_response(request, payload)


def _mock_oauth_session_response(request: Request) -> JSONResponse:
    """Handle OAuth session requests in mock mode using in-memory state."""
    if request.method == "DELETE":
        return _json_no_store_response(mock_oauth_logout())
    if request.method == "POST":
        return _json_no_store_response(mock_oauth_login())
    return _json_no_store_response(mock_oauth_session_state())


class OAuthTokenExchangeError(RuntimeError):
    def __init__(self, status_code: int, error: str, description: str) -> None:
        super().__init__(description)
        self.status_code = status_code
        self.error = error
        self.description = description


class OAuthSessionSecretError(RuntimeError):
    pass


def _json_no_store_response(
    content: dict[str, object],
    *,
    status_code: int = 200,
) -> JSONResponse:
    return JSONResponse(
        content,
        status_code=status_code,
        headers={"Cache-Control": "no-store"},
    )


def _create_session_response(
    request: Request,
    payload: object,
) -> JSONResponse:
    if not isinstance(payload, dict):
        return _json_no_store_response(
            {
                "error": "invalid_request",
                "error_description": "OAuth session request body must be an object.",
            },
            status_code=400,
        )
    access_token = _required_string_payload_value(payload, "access_token")
    if not access_token:
        return _json_no_store_response(
            {
                "error": "invalid_request",
                "error_description": "OAuth session requires an access token.",
            },
            status_code=400,
        )
    session_payload = _oauth_session_payload(payload)
    if _oauth_session_payload_expires_at(session_payload) <= _now_ms():
        return _json_no_store_response(
            {
                "error": "invalid_request",
                "error_description": "OAuth session expiration is invalid.",
            },
            status_code=400,
        )

    response = _json_no_store_response(_oauth_session_state(session_payload))
    try:
        _set_session_cookie(request, response, session_payload)
    except OAuthSessionSecretError:
        return _session_secret_error_response()
    return response


def _set_session_cookie(
    request: Request,
    response: JSONResponse,
    session_payload: dict[str, object],
) -> None:
    expires_at = _oauth_session_cookie_expires_at(session_payload)
    response.set_cookie(
        OAUTH_SESSION_COOKIE_NAME,
        _encode_oauth_session(session_payload),
        httponly=True,
        max_age=max(0, int((expires_at - _now_ms()) / 1000)),
        path="/",
        samesite="lax",
        secure=_request_is_secure(request),
    )


def _get_session_response(request: Request) -> JSONResponse:
    try:
        session_payload = _decode_oauth_session(
            request.cookies.get(OAUTH_SESSION_COOKIE_NAME, "")
        )
    except OAuthSessionSecretError:
        return _session_secret_error_response()
    if session_payload is None:
        return _json_no_store_response(_signed_out_oauth_state())
    if _oauth_session_payload_expires_at(session_payload) <= _now_ms() + 30_000:
        return _refresh_session_response(request, session_payload)
    return _json_no_store_response(_oauth_session_state(session_payload))


def _delete_session_response() -> JSONResponse:
    response = _json_no_store_response(_signed_out_oauth_state("Signed out."))
    _clear_session_cookie(response)
    return response


def _refresh_session_response(
    request: Request,
    session_payload: dict[str, object],
) -> JSONResponse:
    refresh_token = str(session_payload.get("refresh_token", ""))
    refresh_expires_at = _int_payload_value(session_payload.get("refresh_expires_at"))
    if not refresh_token or (refresh_expires_at and refresh_expires_at <= _now_ms()):
        response = _json_no_store_response(
            _signed_out_oauth_state("OAuth session expired. Sign in again.")
        )
        _clear_session_cookie(response)
        return response

    try:
        token_response = _refresh_oauth_token(refresh_token)
    except OAuthTokenExchangeError:
        response = _json_no_store_response(
            _signed_out_oauth_state("OAuth session expired. Sign in again.")
        )
        _clear_session_cookie(response)
        return response

    refreshed_access_token = _required_string_payload_value(
        token_response,
        "access_token",
    )
    if not refreshed_access_token:
        response = _json_no_store_response(
            _signed_out_oauth_state("OAuth session expired. Sign in again.")
        )
        _clear_session_cookie(response)
        return response

    refreshed_token_payload = {
        "access_token": refreshed_access_token,
        "email": session_payload.get("email"),
        "expires_in": token_response.get("expires_in"),
        "refresh_token": token_response.get("refresh_token") or refresh_token,
        "refresh_expires_in": token_response.get("refresh_expires_in"),
    }
    if not token_response.get("refresh_expires_in"):
        refreshed_token_payload["refresh_expires_at"] = refresh_expires_at
    refreshed_payload = _oauth_session_payload(refreshed_token_payload)
    response = _json_no_store_response(_oauth_session_state(refreshed_payload))
    try:
        _set_session_cookie(request, response, refreshed_payload)
    except OAuthSessionSecretError:
        return _session_secret_error_response()
    return response


def _clear_session_cookie(response: JSONResponse) -> None:
    response.delete_cookie(OAUTH_SESSION_COOKIE_NAME, path="/", samesite="lax")


def _session_secret_error_response() -> JSONResponse:
    return _json_no_store_response(
        {
            "error": "server_error",
            "error_description": "OAuth session secret is not configured.",
        },
        status_code=500,
    )


def _signed_out_oauth_state(oauth_status: str = "") -> dict[str, object]:
    return {
        "auth_bearer_token": "",
        "oauth_authenticated": False,
        "oauth_user_email": "",
        "oauth_status": oauth_status,
    }


def _oauth_session_state(session_payload: dict[str, object]) -> dict[str, object]:
    email = str(session_payload.get("email", ""))
    token = str(session_payload.get("access_token", ""))
    return {
        "auth_bearer_token": token,
        "admin_user_email": email,
        "oauth_authenticated": True,
        "oauth_user_email": email,
        "oauth_status": (email and f"Signed in as {email}")
        or "Signed in with Keycloak",
    }


def _oauth_session_payload(payload: dict[str, object]) -> dict[str, object]:
    session_payload = {
        "access_token": _optional_string_payload_value(payload, "access_token"),
        "email": _optional_string_payload_value(payload, "email"),
        "expires_at": _oauth_session_expires_at(payload),
    }
    refresh_token = _optional_string_payload_value(payload, "refresh_token")
    if refresh_token:
        session_payload["refresh_token"] = refresh_token
        session_payload["refresh_expires_at"] = _oauth_session_refresh_expires_at(
            payload
        )
    return session_payload


def _oauth_session_expires_at(payload: dict[str, object]) -> int:
    expires_at = _int_payload_value(payload.get("expires_at"))
    if expires_at > 0:
        return expires_at
    expires_in = _int_payload_value(payload.get("expires_in"))
    if expires_in <= 0:
        expires_in = 180
    return _now_ms() + expires_in * 1000


def _oauth_session_refresh_expires_at(payload: dict[str, object]) -> int:
    refresh_expires_at = _int_payload_value(payload.get("refresh_expires_at"))
    if refresh_expires_at > 0:
        return refresh_expires_at
    refresh_expires_in = _int_payload_value(payload.get("refresh_expires_in"))
    if refresh_expires_in > 0:
        return _now_ms() + refresh_expires_in * 1000
    return _oauth_session_expires_at(payload)


def _oauth_session_payload_expires_at(session_payload: dict[str, object]) -> int:
    return _int_payload_value(session_payload.get("expires_at"))


def _oauth_session_cookie_expires_at(session_payload: dict[str, object]) -> int:
    return max(
        _oauth_session_payload_expires_at(session_payload),
        _int_payload_value(session_payload.get("refresh_expires_at")),
    )


def _int_payload_value(value: object) -> int:
    if isinstance(value, bool):
        return 0
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.isdigit():
            return int(stripped)
    return 0


def _required_string_payload_value(payload: dict[str, object], key: str) -> str | None:
    value = payload.get(key)
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    return stripped or None


def _optional_string_payload_value(payload: dict[str, object], key: str) -> str:
    return _required_string_payload_value(payload, key) or ""


def _encode_oauth_session(session_payload: dict[str, object]) -> str:
    payload_json = json.dumps(
        session_payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return _oauth_session_cipher().encrypt(payload_json).decode()


def _decode_oauth_session(cookie_value: str) -> dict[str, object] | None:
    if not cookie_value:
        return None
    try:
        decoded_payload = json.loads(
            _oauth_session_cipher().decrypt(cookie_value.encode())
        )
    except (InvalidToken, json.JSONDecodeError):
        return None
    if not isinstance(decoded_payload, dict):
        return None
    if not _required_string_payload_value(decoded_payload, "access_token"):
        return None
    return decoded_payload


def _oauth_session_cipher() -> Fernet:
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"airbyte-ops-webapp-oauth-session",
        info=b"fernet-key",
    ).derive(_oauth_session_secret())
    key = base64.urlsafe_b64encode(derived_key)
    return Fernet(key)


def _oauth_session_secret() -> bytes:
    value = os.getenv(OAUTH_CLIENT_SECRET_ENV_VAR, "").strip()
    if not value:
        raise OAuthSessionSecretError(
            f"{OAUTH_CLIENT_SECRET_ENV_VAR} is required for OAuth session cookies."
        )
    return value.encode()


def _request_is_secure(request: Request) -> bool:
    forwarded_proto = request.headers.get("x-forwarded-proto", "")
    first_forwarded_proto = forwarded_proto.split(",", 1)[0].strip().lower()
    return request.url.scheme == "https" or first_forwarded_proto == "https"


def _now_ms() -> int:
    return int(time.time() * 1000)


def _exchange_oauth_token(code: str, code_verifier: str) -> dict[str, object]:
    config = oauth_config()
    token_request = {
        "grant_type": "authorization_code",
        "client_id": str(config["client_id"]),
        "code": code,
        "redirect_uri": str(config["redirect_uri"]),
        "code_verifier": code_verifier,
    }
    client_secret = os.getenv(OAUTH_CLIENT_SECRET_ENV_VAR, "").strip()
    if client_secret:
        token_request["client_secret"] = client_secret

    return _send_oauth_token_request(token_request, str(config["token_endpoint"]))


def _refresh_oauth_token(refresh_token: str) -> dict[str, object]:
    config = oauth_config()
    token_request = {
        "grant_type": "refresh_token",
        "client_id": str(config["client_id"]),
        "refresh_token": refresh_token,
    }
    client_secret = os.getenv(OAUTH_CLIENT_SECRET_ENV_VAR, "").strip()
    if client_secret:
        token_request["client_secret"] = client_secret

    return _send_oauth_token_request(token_request, str(config["token_endpoint"]))


def _send_oauth_token_request(
    token_request: dict[str, str],
    token_endpoint: str,
) -> dict[str, object]:
    request_body = urllib.parse.urlencode(token_request).encode()
    request = urllib.request.Request(
        token_endpoint,
        data=request_body,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return _parse_oauth_token_json(response.read())
    except urllib.error.HTTPError as error:
        error_body = _parse_oauth_error_json(error.read())
        raise OAuthTokenExchangeError(
            error.code,
            str(error_body.get("error", "token_exchange_failed")),
            str(
                error_body.get(
                    "error_description",
                    error_body.get("error", "OAuth token exchange failed."),
                )
            ),
        ) from None
    except urllib.error.URLError as error:
        raise OAuthTokenExchangeError(
            502,
            "token_exchange_failed",
            str(error.reason),
        ) from None


def _parse_oauth_token_json(body: bytes) -> dict[str, object]:
    value = json.loads(body)
    if not isinstance(value, dict):
        raise OAuthTokenExchangeError(
            502,
            "invalid_token_response",
            "OAuth token response was not a JSON object.",
        )
    return value


def _parse_oauth_error_json(body: bytes) -> dict[str, object]:
    try:
        value = json.loads(body)
    except json.JSONDecodeError:
        return {"error": "token_exchange_failed"}
    if isinstance(value, dict):
        return value
    return {"error": "token_exchange_failed"}


def _oauth_enabled() -> bool:
    return os.getenv(OAUTH_ENABLED_ENV_VAR, "true").strip().lower() not in {
        "0",
        "false",
        "no",
    }


def _oauth_redirect_uri() -> str:
    configured_redirect_uri = os.getenv(OAUTH_REDIRECT_URI_ENV_VAR, "").strip()
    if configured_redirect_uri:
        return configured_redirect_uri

    public_url = os.getenv(OAUTH_PUBLIC_URL_ENV_VAR, "").strip().rstrip("/")
    if public_url:
        return f"{public_url}{OAUTH_CALLBACK_PATH}"

    return DEFAULT_OAUTH_LOCAL_REDIRECT_URI


def _oauth_callback_csp(config: dict[str, str | bool]) -> str:
    return (
        "default-src 'none'; "
        "base-uri 'none'; "
        "connect-src 'self'; "
        "form-action 'none'; "
        "frame-ancestors 'none'; "
        "script-src 'unsafe-inline'"
    )


OAUTH_JS_ACTIONS = {
    "hydrateOAuth": r"""async (...args) => {
      const state = args[0]?.state || args[0] || {};
      const config = state.oauth_config || {};
      try {
        const response = await fetch(config.session_endpoint || "/oauth/session", {
          credentials: "same-origin",
          headers: { "Accept": "application/json" },
        });
        if (response.ok) {
          const session = await response.json();
          if (session.oauth_authenticated) {
            return {
              ...session,
              admin_user_email: session.admin_user_email || state.admin_user_email,
            };
          }
          if (session.oauth_status) {
            return {
              ...session,
              admin_user_email: state.admin_user_email || "",
            };
          }
        }
      } catch {
      }
      const legacyToken = sessionStorage.getItem("airbyte_ops_webapp_access_token") || "";
      const legacyExpiresAt = Number(sessionStorage.getItem("airbyte_ops_webapp_expires_at") || "0");
      const legacyEmail = sessionStorage.getItem("airbyte_ops_webapp_user_email") || "";
      if (!legacyToken) {
        return {
          auth_bearer_token: state.auth_bearer_token || "",
          admin_user_email: state.admin_user_email || "",
          oauth_authenticated: false,
          oauth_user_email: "",
          oauth_status: state.oauth_status || "",
        };
      }
      if (legacyExpiresAt && legacyExpiresAt < Date.now() + 30000) {
        sessionStorage.removeItem("airbyte_ops_webapp_access_token");
        sessionStorage.removeItem("airbyte_ops_webapp_expires_at");
        sessionStorage.removeItem("airbyte_ops_webapp_user_email");
        return {
          auth_bearer_token: "",
          oauth_authenticated: false,
          oauth_user_email: "",
          oauth_status: "OAuth session expired. Sign in again.",
        };
      }
      return {
        auth_bearer_token: legacyToken,
        admin_user_email: legacyEmail || state.admin_user_email,
        oauth_authenticated: true,
        oauth_user_email: legacyEmail,
        oauth_status: legacyEmail ? `Signed in as ${legacyEmail}` : "Signed in with Keycloak",
      };
    }""",
    "startOAuth": r"""async (...args) => {
      const state = args[0]?.state || args[0] || {};
      const config = state.oauth_config || {};
      const navigationLocation = window.top?.location || window.location;
      let browserCrypto = globalThis.crypto;
      if (!browserCrypto?.subtle) {
        try {
          browserCrypto = window.top?.crypto || browserCrypto;
        } catch {
          browserCrypto = globalThis.crypto;
        }
      }
      if (!browserCrypto?.getRandomValues || !browserCrypto?.subtle) {
        return { oauth_status: "Browser WebCrypto is unavailable; use localhost or HTTPS." };
      }
      const randomBytes = new Uint8Array(32);
      browserCrypto.getRandomValues(randomBytes);
      const base64Url = (bytes) => btoa(String.fromCharCode(...bytes))
        .replace(/\+/g, "-")
        .replace(/\//g, "_")
        .replace(/=+$/, "");
      const verifierBytes = new Uint8Array(64);
      browserCrypto.getRandomValues(verifierBytes);
      const codeVerifier = base64Url(verifierBytes);
      const digest = await browserCrypto.subtle.digest(
        "SHA-256",
        new TextEncoder().encode(codeVerifier),
      );
      const codeChallenge = base64Url(new Uint8Array(digest));
      const oauthState = base64Url(randomBytes);
      const nonceBytes = new Uint8Array(32);
      browserCrypto.getRandomValues(nonceBytes);
      const nonce = base64Url(nonceBytes);
      sessionStorage.setItem("airbyte_ops_webapp_code_verifier", codeVerifier);
      sessionStorage.setItem("airbyte_ops_webapp_state", oauthState);
      sessionStorage.setItem("airbyte_ops_webapp_nonce", nonce);
      sessionStorage.setItem("airbyte_ops_webapp_return_to", navigationLocation.href);
      const params = new URLSearchParams({
        client_id: config.client_id,
        redirect_uri: config.redirect_uri,
        response_type: "code",
        scope: "openid email profile",
        state: oauthState,
        nonce,
        code_challenge: codeChallenge,
        code_challenge_method: "S256",
      });
      navigationLocation.assign(`${config.authorization_endpoint}?${params.toString()}`);
      return { oauth_status: "Redirecting to Keycloak..." };
    }""",
    "logoutOAuth": r"""async (...args) => {
      const state = args[0]?.state || args[0] || {};
      const config = state.oauth_config || {};
      try {
        await fetch(config.session_endpoint || "/oauth/session", {
          method: "DELETE",
          credentials: "same-origin",
          headers: { "Accept": "application/json" },
        });
      } catch {
      }
      sessionStorage.removeItem("airbyte_ops_webapp_access_token");
      sessionStorage.removeItem("airbyte_ops_webapp_expires_at");
      sessionStorage.removeItem("airbyte_ops_webapp_user_email");
      sessionStorage.removeItem("airbyte_ops_webapp_code_verifier");
      sessionStorage.removeItem("airbyte_ops_webapp_state");
      sessionStorage.removeItem("airbyte_ops_webapp_nonce");
      sessionStorage.removeItem("airbyte_ops_webapp_return_to");
      return {
        auth_bearer_token: "",
        oauth_authenticated: false,
        oauth_user_email: "",
        oauth_status: "Signed out.",
      };
    }""",
}


def _oauth_callback_html(config: dict[str, str | bool]) -> str:
    config_json = json.dumps(config).replace("</", r"<\/")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Airbyte Ops OAuth Callback</title>
</head>
<body>
  <p id="status">Completing Airbyte sign-in...</p>
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
    const url = new URL(value || "/", window.location.origin);
    return url.origin === window.location.origin ? url.toString() : "/";
  }} catch {{
    return "/";
  }}
}};
(async () => {{
  try {{
    const params = new URLSearchParams(window.location.search);
    const error = params.get("error");
    if (error) {{
      throw new Error(`${{error}}: ${{params.get("error_description") || "Keycloak rejected the request"}}`);
    }}
    const code = params.get("code");
    const returnedState = params.get("state");
    const expectedState = sessionStorage.getItem("airbyte_ops_webapp_state");
    const expectedNonce = sessionStorage.getItem("airbyte_ops_webapp_nonce");
    const codeVerifier = sessionStorage.getItem("airbyte_ops_webapp_code_verifier");
    if (!code || !returnedState || !expectedState || returnedState !== expectedState || !codeVerifier || !expectedNonce) {{
      throw new Error("OAuth callback state is invalid or incomplete.");
    }}
    const body = {{
      code,
      code_verifier: codeVerifier,
    }};
    const response = await fetch(config.token_exchange_endpoint, {{
      method: "POST",
      headers: {{ "Content-Type": "application/json" }},
      body: JSON.stringify(body),
    }});
    const tokenResponse = await response.json();
    if (!response.ok || !tokenResponse.access_token) {{
      throw new Error(tokenResponse.error_description || tokenResponse.error || "Token exchange failed.");
    }}
    if (!tokenResponse.id_token) {{
      throw new Error("OAuth token response did not include an ID token.");
    }}
    const claims = decodeJwtPayload(tokenResponse.id_token);
    if (claims.nonce !== expectedNonce) {{
      throw new Error("OAuth callback nonce is invalid.");
    }}
    const email = claims.email || claims.preferred_username || claims.sub || "";
    const sessionResponse = await fetch(config.session_endpoint, {{
      method: "POST",
      credentials: "same-origin",
      headers: {{ "Content-Type": "application/json" }},
      body: JSON.stringify({{
        access_token: tokenResponse.access_token,
        email,
        expires_in: tokenResponse.expires_in || 180,
        refresh_token: tokenResponse.refresh_token || "",
        refresh_expires_in: tokenResponse.refresh_expires_in || "",
      }}),
    }});
    const sessionBody = await sessionResponse.json();
    if (!sessionResponse.ok || !sessionBody.oauth_authenticated) {{
      throw new Error(sessionBody.error_description || sessionBody.error || "OAuth session setup failed.");
    }}
    sessionStorage.removeItem("airbyte_ops_webapp_code_verifier");
    sessionStorage.removeItem("airbyte_ops_webapp_state");
    sessionStorage.removeItem("airbyte_ops_webapp_nonce");
    const returnTo = sameOriginReturnTo(sessionStorage.getItem("airbyte_ops_webapp_return_to"));
    sessionStorage.removeItem("airbyte_ops_webapp_return_to");
    window.location.replace(returnTo);
  }} catch (error) {{
    statusEl.textContent = error instanceof Error ? error.message : String(error);
  }}
}})();
  </script>
</body>
</html>"""
