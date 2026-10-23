"""OAuth for `plato vault app`: PKCE, the one-shot callback listener, the token calls and the checks.

Canva refresh tokens work ONE time. :func:`refresh` takes the store's account lock, re-reads the
record, and stores the new refresh token BEFORE it returns the access token. If that store write
fails, no access token is handed out. Errors never name a token or the reply body.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import threading
import time
from collections.abc import Callable
from enum import StrEnum
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse

import httpx
from pydantic import SecretStr, ValidationError

from plato.cli.vault.app_models import (
    AppCredentials,
    ClientAuth,
    McpCheck,
    PkcePair,
    TokenGrant,
    VendorRecipe,
    VendorUser,
)
from plato.cli.vault.app_store import AppStore, StoreError
from plato.cli.vault.client import NotFound, VaultConsoleError

HTTP_TIMEOUT_S = 30.0
LISTEN_TIMEOUT_S = 300.0
# A connection that sends no request line in this time is closed. Browsers open
# spare connections in advance, and an idle one must not hold up the redirect.
LISTENER_IDLE_S = 5.0
MCP_PROTOCOL_VERSION = "2025-06-18"


class OAuthErrorCode(StrEnum):
    """The vendor's OAuth ``error`` codes that change the advice a command gives."""

    invalid_grant = "invalid_grant"


class OAuthError(VaultConsoleError):
    """A token call or a consent failed. Exit code 5. ``code``: the vendor's OAuth error
    code, when the vendor replied with one. Code compares it, never the message text."""

    exit_code = 5

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code


def http_client() -> httpx.Client:
    """The client every vendor call uses. Tests patch this with a MockTransport client."""
    return httpx.Client(timeout=HTTP_TIMEOUT_S)


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def make_pkce(verifier: str | None = None) -> PkcePair:
    """RFC 7636 S256. The default verifier is 32 random bytes, 43 characters (Canva: 43 to 128)."""
    v = verifier or _b64url(secrets.token_bytes(32))
    if not 43 <= len(v) <= 128:
        raise ValueError("a PKCE verifier must be 43 to 128 characters")
    return PkcePair(verifier=SecretStr(v), challenge=_b64url(hashlib.sha256(v.encode("ascii")).digest()))


def new_state() -> str:
    return secrets.token_urlsafe(24)


def authorize_url(recipe: VendorRecipe, client_id: str, scopes: list[str], pkce: PkcePair, state: str) -> str:
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": recipe.redirect_uri,
        "scope": " ".join(scopes),
        "state": state,
        "code_challenge": pkce.challenge,
        "code_challenge_method": pkce.method,
    }
    return f"{recipe.authorize_url}?{urlencode(params)}"


class CallbackListener:
    """Listens on the redirect URI's host and port for ONE good redirect.

    A wrong ``state`` gets a 400 and the listener keeps waiting: a forged redirect must not end the
    consent. The good redirect gets a 302 to ``/done``, so no later snapshot shows the code. Access
    logging is off, because the default handler writes the code to stderr. Each connection has its
    own thread and a :data:`LISTENER_IDLE_S` timeout, so an idle connection cannot block the redirect.
    """

    def __init__(self, redirect_uri: str, state: str, port: int | None = None) -> None:
        parsed = urlparse(redirect_uri)
        if parsed.hostname != "127.0.0.1":
            raise OAuthError(f"the listener binds 127.0.0.1 only, not {parsed.hostname}")
        self.path = parsed.path or "/"
        self.port = parsed.port if port is None else port
        self._state = state
        self._got = threading.Event()
        self._done = threading.Event()
        self.code: str | None = None
        self.error: str | None = None
        self.refused = 0
        self._take = threading.Lock()
        self._server: ThreadingHTTPServer | None = None
        self._thread: threading.Thread | None = None

    def _handler(self) -> type[BaseHTTPRequestHandler]:
        listener = self

        class Handler(BaseHTTPRequestHandler):
            timeout = LISTENER_IDLE_S

            def log_message(self, format: str, *args: Any) -> None:  # noqa: A002 - the base class's name
                return None

            def _reply(self, status: int, body: str, location: str | None = None) -> None:
                self.send_response(status)
                if location:
                    self.send_header("Location", location)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(body.encode())

            def do_GET(self) -> None:  # noqa: N802 - http.server's name
                url = urlparse(self.path)
                if url.path == "/done":
                    self._reply(200, "<p>Plato vault: done. You can close this tab.</p>")
                    listener._done.set()
                    return
                if url.path != listener.path:
                    self._reply(404, "<p>not found</p>")
                    return
                query = parse_qs(url.query)
                state = (query.get("state") or [""])[0]
                with listener._take:
                    if listener._got.is_set():
                        status = 404
                    elif not hmac.compare_digest(state.encode(), listener._state.encode()):
                        listener.refused += 1
                        status = 400
                    else:
                        if "error" in query:
                            listener.error = query["error"][0]
                        elif query.get("code"):
                            listener.code = query["code"][0]
                        else:
                            listener.error = "no code in the redirect"
                        listener._got.set()
                        status = 302
                if status == 404:
                    self._reply(404, "<p>not found</p>")
                elif status == 400:
                    self._reply(400, "<p>state does not match: refused</p>")
                else:
                    self._reply(302, "", location="/done")

        return Handler

    def __enter__(self) -> CallbackListener:
        try:
            self._server = ThreadingHTTPServer(("127.0.0.1", self.port or 0), self._handler())
            self._server.daemon_threads = True
        except OSError as e:
            raise OAuthError(
                f"cannot listen on 127.0.0.1:{self.port} ({e.strerror}); stop what uses the port and try again"
            ) from None
        self.port = self._server.server_address[1]
        self._thread = threading.Thread(target=self._server.serve_forever, name="vault-app-callback", daemon=True)
        self._thread.start()
        return self

    def wait(self, timeout_s: float = LISTEN_TIMEOUT_S, pump: Callable[[], None] | None = None) -> str:
        """The code. Raises :class:`OAuthError` on a vendor error or a timeout.

        ``pump`` (each driver passes one): a short wait. On the Pi driver, Playwright
        handles events in it: the Pi browser's redirect reaches this listener only through
        a Playwright route, which runs only while this thread is in a Playwright call. On
        ego-browser it only sleeps, so the code can show up to one pump later."""
        if pump is not None:
            end = time.monotonic() + timeout_s
            while not self._got.is_set() and time.monotonic() < end:
                pump()
        if not self._got.wait(0 if pump is not None else timeout_s):
            extra = f" ({self.refused} redirect(s) with a wrong state were refused)" if self.refused else ""
            raise OAuthError(f"no consent redirect came within {timeout_s:.0f} s{extra}")
        if self.error or not self.code:
            raise OAuthError(f"the vendor refused the consent: {self.error}")
        return self.code

    def __exit__(self, *exc: object) -> None:
        if self._got.is_set():
            self._done.wait(2.0)  # let the browser load /done
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()


def _error_code(response: httpx.Response) -> str:
    """The reply's OAuth ``error`` code only; the description can quote the request."""
    try:
        body = response.json()
    except ValueError:
        return "(no JSON body)"
    if not isinstance(body, dict):
        return "(unknown error)"
    code = body.get("error") or body.get("code")
    if isinstance(code, dict):  # {"error": {"code": ..., "message": ...}}
        code = code.get("code")
    return str(code or "(unknown error)")


REFRESH_NO_ANSWER = "A refresh token may be spent now: run `refresh` again, and if it says invalid_grant, run `consent`"
EXCHANGE_NO_ANSWER = (
    "The code works one time only, so it may be spent now: run `consent` again. Do not run `refresh`: "
    "it spends the refresh token of the grant that is stored"
)


def _token_call(
    recipe: VendorRecipe,
    client_id: str,
    client_secret: SecretStr,
    data: dict[str, str],
    http: httpx.Client,
    *,
    no_answer: str = REFRESH_NO_ANSWER,
) -> TokenGrant:
    body = dict(data)
    extra: dict[str, Any] = {}
    if recipe.client_auth == ClientAuth.basic:
        extra["auth"] = httpx.BasicAuth(client_id, client_secret.get_secret_value())
    else:
        body.update(client_id=client_id, client_secret=client_secret.get_secret_value())
    try:
        response = http.post(recipe.token_url, data=body, headers={"Accept": "application/json"}, **extra)
    except httpx.HTTPError as e:
        raise OAuthError(
            f"the token call to {recipe.token_url} got no answer ({type(e).__name__}). {no_answer}"
        ) from None
    if response.status_code != 200:
        code = _error_code(response)
        raise OAuthError(f"the token call failed: HTTP {response.status_code} {code}", code=code)
    try:
        return TokenGrant.model_validate(response.json())
    except (ValueError, ValidationError):
        raise OAuthError("the token reply is not a token grant (HTTP 200, unreadable body)") from None


def exchange_code(
    recipe: VendorRecipe, client_id: str, client_secret: SecretStr, code: str, pkce: PkcePair, http: httpx.Client
) -> TokenGrant:
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": recipe.redirect_uri,
        "code_verifier": pkce.verifier.get_secret_value(),
    }
    return _token_call(recipe, client_id, client_secret, data, http, no_answer=EXCHANGE_NO_ANSWER)


def refresh(
    store: AppStore,
    recipe: VendorRecipe,
    login_key: str,
    account: str,
    http: httpx.Client,
    *,
    min_left_s: float | None = None,
) -> tuple[AppCredentials, bool]:
    """``(record, refreshed)``. With ``min_left_s``, a token with that much time left
    (after the lock, so another process's refresh counts) is reused; without it the
    refresh always runs. The new record is in the store before this returns."""
    with store.lock(login_key, account):
        creds = store.load(login_key, account)
        if creds is None:
            raise NotFound(f"no app credentials for {login_key}/{account} (run `plato vault app create` or `import`)")
        if min_left_s is not None and creds.fresh_for(min_left_s):
            return creds, False
        if creds.refresh_token is None:
            raise OAuthError(f"{login_key}/{account} has no refresh token: run `plato vault app consent` first")
        data = {"grant_type": "refresh_token", "refresh_token": creds.refresh_token.get_secret_value()}
        try:
            grant = _token_call(recipe, creds.client_id, creds.client_secret, data, http)
        except OAuthError as e:
            if e.code == OAuthErrorCode.invalid_grant:
                raise OAuthError(
                    f"{e}: the grant is dead (a refresh token works one time only). "
                    f"Run `plato vault app consent {login_key} -a {account}`",
                    code=e.code,
                ) from None
            raise
        new = creds.with_grant(grant)
        try:
            store.save(new)
        except StoreError as e:
            raise StoreError(
                f"{e}. The vendor already rotated the refresh token, so the grant is lost: "
                f"run `plato vault app consent {login_key} -a {account}`"
            ) from None
        return new, True


def check_user(recipe: VendorRecipe, access_token: SecretStr, http: httpx.Client) -> VendorUser:
    """Canva ``GET users/me``: the grant works and signs in as this user and team. A reply
    with no user id raises: the caller compares that id to find a grant of another account."""
    try:
        response = http.get(
            recipe.user_check_url, headers={"Authorization": f"Bearer {access_token.get_secret_value()}"}
        )
    except httpx.HTTPError as e:
        raise OAuthError(f"the user check got no answer ({type(e).__name__})") from None
    if response.status_code != 200:
        raise OAuthError(f"the user check failed: HTTP {response.status_code} {_error_code(response)}")
    try:
        body = response.json()
    except ValueError:
        raise OAuthError("the user check reply is not JSON") from None
    team_user = body.get("team_user") if isinstance(body, dict) else None
    user_id = team_user.get("user_id") if isinstance(team_user, dict) else None
    if not isinstance(user_id, str) or not user_id:
        raise OAuthError("the user check reply (HTTP 200) has no team_user.user_id")
    team_id = team_user.get("team_id")
    return VendorUser(user_id=user_id, team_id=team_id if isinstance(team_id, str) else None)


def _rpc_reply(response: httpx.Response, rpc_id: int) -> dict | None:
    """The JSON-RPC reply with ``id == rpc_id``, from a JSON body or from the ``data:``
    lines of an SSE body (a server can send notifications before the reply)."""
    if "text/event-stream" in response.headers.get("content-type", ""):
        for line in response.text.splitlines():
            if not line.startswith("data:"):
                continue
            try:
                msg = json.loads(line[5:].strip())
            except ValueError:
                continue
            if isinstance(msg, dict) and msg.get("id") == rpc_id:
                return msg
        return None
    try:
        body = response.json()
    except ValueError:
        return None
    return body if isinstance(body, dict) and body.get("id") == rpc_id else None


def check_mcp(recipe: VendorRecipe, access_token: SecretStr, http: httpx.Client) -> McpCheck:
    """``initialize``, ``notifications/initialized``, then ``tools/list``. A 200 on
    initialize with a 403 on tools/list means the app's "Canva MCP" switch is off."""
    url = recipe.mcp_url
    headers = {
        "Authorization": f"Bearer {access_token.get_secret_value()}",
        "Accept": "application/json, text/event-stream",
        "Content-Type": "application/json",
    }
    init = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": MCP_PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": "plato-vault-app", "version": "1"},
        },
    }
    try:
        first = http.post(url, json=init, headers=headers)
        if first.status_code != 200:
            return McpCheck(url=url, initialize_status=first.status_code)
        session = first.headers.get("mcp-session-id")
        if session:
            headers["Mcp-Session-Id"] = session
        headers["MCP-Protocol-Version"] = MCP_PROTOCOL_VERSION
        http.post(url, json={"jsonrpc": "2.0", "method": "notifications/initialized"}, headers=headers)
        tools = http.post(url, json={"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, headers=headers)
    except httpx.HTTPError as e:
        return McpCheck(url=url, initialize_status=0, error=f"no answer ({type(e).__name__})")
    if tools.status_code != 200:
        return McpCheck(url=url, initialize_status=200, tools_status=tools.status_code)
    reply = _rpc_reply(tools, 2)
    if reply is not None and isinstance(reply.get("error"), dict):
        message = str(reply["error"].get("message") or "error")
        return McpCheck(url=url, initialize_status=200, tools_status=200, error=message)
    result = reply.get("result") if reply else None
    listed = result.get("tools") if isinstance(result, dict) else None
    if not isinstance(listed, list):
        return McpCheck(url=url, initialize_status=200, tools_status=200, error="no tools list in the tools/list reply")
    return McpCheck(url=url, initialize_status=200, tools_status=200, tool_count=len(listed))
