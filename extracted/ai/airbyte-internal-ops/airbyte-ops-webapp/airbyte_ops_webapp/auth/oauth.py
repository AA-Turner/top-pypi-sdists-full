"""OAuth helpers for the connector version manager webapp."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request

from fastmcp import FastMCP
from prefab_ui.actions.custom import CallHandler
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse

from airbyte_ops_webapp.state import (
    OAUTH_CLIENT_ID_ENV_VAR,
    OAUTH_CLIENT_SECRET_ENV_VAR,
    OAUTH_ENABLED_ENV_VAR,
    OAUTH_ISSUER_ENV_VAR,
    OAUTH_PUBLIC_URL_ENV_VAR,
    OAUTH_REDIRECT_URI_ENV_VAR,
)

DEFAULT_OAUTH_CLIENT_ID = "airbyte-ops-webapp-client"
DEFAULT_OAUTH_ISSUER = "https://cloud.airbyte.com/auth/realms/airbyte"
DEFAULT_OAUTH_LOCAL_REDIRECT_URI = "http://localhost:3000/oauth/callback"
OAUTH_CALLBACK_PATH = "/oauth/callback"
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
        "token_exchange_endpoint": OAUTH_TOKEN_PATH,
    }


def register_oauth_routes(mcp: FastMCP) -> None:
    mcp.custom_route(OAUTH_CALLBACK_PATH, methods=["GET"], name="ops_oauth_callback")(
        oauth_callback_response
    )
    mcp.custom_route(OAUTH_TOKEN_PATH, methods=["POST"], name="ops_oauth_token")(
        oauth_token_response
    )


def hydrate_oauth_action() -> CallHandler:
    return CallHandler("hydrateOAuth")


def logout_oauth_action() -> CallHandler:
    return CallHandler("logoutOAuth")


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


class OAuthTokenExchangeError(RuntimeError):
    def __init__(self, status_code: int, error: str, description: str) -> None:
        super().__init__(description)
        self.status_code = status_code
        self.error = error
        self.description = description


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

    request_body = urllib.parse.urlencode(token_request).encode()
    request = urllib.request.Request(
        str(config["token_endpoint"]),
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
    "hydrateOAuth": r"""(...args) => {
      const state = args[0]?.state || args[0] || {};
      const token = sessionStorage.getItem("airbyte_ops_webapp_access_token") || "";
      const expiresAt = Number(sessionStorage.getItem("airbyte_ops_webapp_expires_at") || "0");
      const email = sessionStorage.getItem("airbyte_ops_webapp_user_email") || "";
      if (!token) {
        return {
          auth_bearer_token: state.auth_bearer_token || "",
          admin_user_email: state.admin_user_email || "",
          oauth_authenticated: false,
          oauth_user_email: "",
          oauth_status: state.oauth_status || "",
        };
      }
      if (expiresAt && expiresAt < Date.now() + 30000) {
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
        auth_bearer_token: token,
        admin_user_email: email || state.admin_user_email,
        oauth_authenticated: true,
        oauth_user_email: email,
        oauth_status: email ? `Signed in as ${email}` : "Signed in with Keycloak",
      };
    }""",
    "startOAuth": r"""async (...args) => {
      const state = args[0]?.state || args[0] || {};
      const config = state.oauth_config || {};
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
      const navigationLocation = window.top?.location || window.location;
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
    "logoutOAuth": r"""() => {
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
    sessionStorage.setItem("airbyte_ops_webapp_access_token", tokenResponse.access_token);
    sessionStorage.setItem("airbyte_ops_webapp_user_email", email);
    sessionStorage.setItem(
      "airbyte_ops_webapp_expires_at",
      String(Date.now() + Number(tokenResponse.expires_in || 180) * 1000),
    );
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
