"""Auth0 OAuth flows for the Pysae API CLI client.

The dedicated ``pysae-ai-tools`` Auth0 client is a public *native* app, so all
flows use PKCE (no client secret):

- :func:`login_authorization_code` — interactive browser login. Spins an
  ephemeral localhost server on one of :data:`CALLBACK_PORTS`, opens the Auth0
  authorize URL, captures the ``code`` and exchanges it for tokens.
- :func:`login_device_code` — headless/no-local-browser login (RFC 8628).
  Prints a short user code + verification URL and polls until authorized.
- :func:`refresh` — exchanges a refresh token for a fresh access token,
  honouring rotating refresh tokens.
"""

import base64
import hashlib
import http.server
import secrets
import threading
import time
import urllib.parse
import webbrowser
from collections.abc import Callable
from dataclasses import dataclass, field

import httpx

from .config import CALLBACK_PATH, CALLBACK_PORTS, OAUTH_SCOPE, Auth0Env
from .tokens import TokenSet

_HTTP_TIMEOUT = 30.0


class OAuthError(RuntimeError):
    """Raised when an OAuth exchange fails."""


def _pkce_pair() -> tuple[str, str]:
    """Return ``(verifier, challenge)`` for PKCE S256."""
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(64)).rstrip(b"=").decode("ascii")
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return verifier, challenge


# ---------------------------------------------------------------------------
# Authorization code + PKCE (interactive browser)
# ---------------------------------------------------------------------------


@dataclass
class _CallbackResult:
    code: str = ""
    state: str = ""
    error: str = ""
    error_description: str = ""
    received: threading.Event = field(default_factory=threading.Event)


def _make_handler(result: _CallbackResult) -> type[http.server.BaseHTTPRequestHandler]:
    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: object) -> None:  # noqa: A002
            """Silence the default stderr access log."""

        def do_GET(self) -> None:
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path != CALLBACK_PATH:
                self.send_response(404)
                self.end_headers()
                return
            params = urllib.parse.parse_qs(parsed.query)
            result.code = params.get("code", [""])[0]
            result.state = params.get("state", [""])[0]
            result.error = params.get("error", [""])[0]
            result.error_description = params.get("error_description", [""])[0]
            body = (
                b"<html><body style='font-family:sans-serif;padding:2em'>"
                b"<h2>Pysae API login complete</h2>"
                b"<p>You can close this tab and return to the terminal.</p>"
                b"</body></html>"
            )
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            result.received.set()

    return Handler


def _bind_callback_server(result: _CallbackResult) -> tuple[http.server.HTTPServer, int]:
    """Bind the first available callback port; raise if none are free."""
    for port in CALLBACK_PORTS:
        try:
            server = http.server.HTTPServer(("127.0.0.1", port), _make_handler(result))
        except OSError:
            continue
        return server, port
    raise OAuthError(f"none of the callback ports {CALLBACK_PORTS} are free — close whatever is using them and retry")


def login_authorization_code(
    env: Auth0Env,
    client_id: str,
    *,
    timeout: int = 300,
    open_browser: bool = True,
    on_url: Callable[[str], None] | None = None,
) -> TokenSet:
    """Run the interactive authorization-code + PKCE flow and return tokens."""
    verifier, challenge = _pkce_pair()
    state = secrets.token_urlsafe(24)
    result = _CallbackResult()
    server, port = _bind_callback_server(result)
    redirect_uri = f"http://localhost:{port}{CALLBACK_PATH}"

    authorize_url = (
        env.authorize_endpoint
        + "?"
        + urllib.parse.urlencode(
            {
                "client_id": client_id,
                "response_type": "code",
                "redirect_uri": redirect_uri,
                "scope": OAUTH_SCOPE,
                "audience": env.audience,
                "code_challenge": challenge,
                "code_challenge_method": "S256",
                "state": state,
                "prompt": "login",
            }
        )
    )

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        if on_url is not None:
            on_url(authorize_url)
        if open_browser:
            webbrowser.open(authorize_url)
        if not result.received.wait(timeout=timeout):
            raise OAuthError(f"timed out after {timeout}s waiting for the browser redirect")
    finally:
        server.shutdown()
        server.server_close()

    if result.error:
        raise OAuthError(f"Auth0 returned an error: {result.error} — {result.error_description}")
    if result.state != state:
        raise OAuthError("state mismatch — possible CSRF, aborting")
    if not result.code:
        raise OAuthError("no authorization code returned")

    payload = _token_request(
        env,
        {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "code": result.code,
            "redirect_uri": redirect_uri,
            "code_verifier": verifier,
        },
    )
    return TokenSet.from_response(payload)


# ---------------------------------------------------------------------------
# Device code (headless / no local browser)
# ---------------------------------------------------------------------------


@dataclass
class DeviceCode:
    device_code: str
    user_code: str
    verification_uri: str
    verification_uri_complete: str
    interval: int
    expires_in: int


def start_device_code(env: Auth0Env, client_id: str) -> DeviceCode:
    """Request a device code from Auth0 (RFC 8628 step 1)."""
    with httpx.Client(timeout=_HTTP_TIMEOUT) as client:
        resp = client.post(
            env.device_endpoint,
            data={"client_id": client_id, "scope": OAUTH_SCOPE, "audience": env.audience},
        )
    data = resp.json() if resp.content else {}
    if resp.status_code != 200:
        raise OAuthError(_describe(data, resp.status_code))
    return DeviceCode(
        device_code=str(data["device_code"]),
        user_code=str(data["user_code"]),
        verification_uri=str(data.get("verification_uri", "")),
        verification_uri_complete=str(data.get("verification_uri_complete", "")),
        interval=int(data.get("interval", 5)),
        expires_in=int(data.get("expires_in", 600)),
    )


def poll_device_code(env: Auth0Env, client_id: str, device: DeviceCode) -> TokenSet:
    """Poll the token endpoint until the user authorizes (RFC 8628 step 3)."""
    deadline = time.time() + device.expires_in
    interval = device.interval
    while time.time() < deadline:
        time.sleep(interval)
        with httpx.Client(timeout=_HTTP_TIMEOUT) as client:
            resp = client.post(
                env.token_endpoint,
                data={
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                    "device_code": device.device_code,
                    "client_id": client_id,
                },
            )
        data = resp.json() if resp.content else {}
        if resp.status_code == 200:
            return TokenSet.from_response(data)
        error = str(data.get("error", ""))
        if error == "authorization_pending":
            continue
        if error == "slow_down":
            interval += 5
            continue
        raise OAuthError(_describe(data, resp.status_code))
    raise OAuthError("device code expired before authorization completed")


# ---------------------------------------------------------------------------
# Refresh
# ---------------------------------------------------------------------------


def refresh(env: Auth0Env, client_id: str, current: TokenSet) -> TokenSet:
    """Exchange the refresh token for a fresh access token."""
    if not current.refresh_token:
        raise OAuthError("no refresh token stored — run `pysae api auth login` again")
    payload = _token_request(
        env,
        {
            "grant_type": "refresh_token",
            "client_id": client_id,
            "refresh_token": current.refresh_token,
        },
    )
    return TokenSet.from_response(payload, previous=current)


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------


def _token_request(env: Auth0Env, data: dict[str, str]) -> dict[str, object]:
    with httpx.Client(timeout=_HTTP_TIMEOUT) as client:
        resp = client.post(env.token_endpoint, data=data)
    payload = resp.json() if resp.content else {}
    if resp.status_code != 200:
        raise OAuthError(_describe(payload, resp.status_code))
    return payload if isinstance(payload, dict) else {}


def _describe(payload: object, status: int) -> str:
    if isinstance(payload, dict) and payload.get("error"):
        desc = payload.get("error_description") or ""
        return f"Auth0 {payload['error']}: {desc}".strip()
    return f"Auth0 token endpoint returned HTTP {status}"
