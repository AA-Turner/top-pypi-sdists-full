"""Run a local Slack OAuth v2 flow to obtain a bot token.

Usage:
    pysae-ai-tools slack get-token \
        --client-id <CLIENT_ID> \
        --client-secret <CLIENT_SECRET>

Starts an ephemeral HTTP server on http://localhost:<port>/callback, opens the
Slack authorize URL in the default browser, captures the returned ``code``, and
exchanges it for a bot token via ``oauth.v2.access``.

Defaults mirror the bot scopes enabled on the "AI Tools Bot" Slack app, so a token
minted here matches the app's installed scopes one-for-one (history + posting for
slack-ask-review / release-status, ``files:write`` for release-file / upload-file,
``channels:join`` for the #mep self-join, plus the DM/mpim scopes the app carries).
Override with ``--scopes`` if the app's scope set changes.

Output (JSON, one line on stdout):
    {"access_token": "xoxb-...", "bot_user_id": "U...", "team": {...}, "scope": "..."}

The token is long-lived and can be stored in AWS Secrets Manager for later use
by the ask-review script.
"""

import http.server
import json
import secrets
import socket
import threading
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import Annotated

import typer

from ..common.browser import open_and_announce
from .client import SLACK_API_BASE

SLACK_AUTHORIZE_URL = "https://slack.com/oauth/v2/authorize"
SLACK_OAUTH_ACCESS_URL = f"{SLACK_API_BASE}/oauth.v2.access"

# Bot scopes enabled on the "AI Tools Bot" Slack app. Kept in sync with the app's
# OAuth config so a freshly minted token never lacks a scope the app advertises.
# (users:read.email is intentionally excluded — not enabled on the app, unused here.)
DEFAULT_SCOPES = ",".join(
    [
        "app_mentions:read",
        "channels:history",
        "channels:join",
        "channels:read",
        "chat:write",
        "files:read",
        "files:write",
        "groups:history",
        "groups:read",
        "im:history",
        "im:read",
        "im:write",
        "mpim:history",
        "mpim:read",
        "mpim:write",
        "users:read",
    ]
)
DEFAULT_PORT = 8765
CALLBACK_PATH = "/callback"


@dataclass
class CallbackResult:
    code: str = ""
    state: str = ""
    error: str = ""
    received: threading.Event = field(default_factory=threading.Event)


def _make_handler(result: CallbackResult) -> type[http.server.BaseHTTPRequestHandler]:
    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: object) -> None:
            """Silence default stderr access log."""

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

            body = (
                b"<html><body style='font-family:sans-serif;padding:2em'>"
                b"<h2>Slack OAuth flow complete</h2>"
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


def _port_available(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind(("127.0.0.1", port))
        except OSError:
            return False
    return True


def _exchange_code(client_id: str, client_secret: str, code: str, redirect_uri: str) -> dict[str, object]:
    data = urllib.parse.urlencode(
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
        }
    ).encode()
    req = urllib.request.Request(SLACK_OAUTH_ACCESS_URL, data=data)
    with urllib.request.urlopen(req, timeout=15) as resp:
        payload: dict[str, object] = json.loads(resp.read())
    if not payload.get("ok"):
        error = payload.get("error", "unknown")
        raise RuntimeError(f"Slack oauth.v2.access error: {error}")
    return payload


cli = typer.Typer()


@cli.command()
def main(
    client_id: Annotated[str, typer.Option("--client-id", envvar="SLACK_CLIENT_ID", help="Slack App Client ID")],
    client_secret: Annotated[
        str, typer.Option("--client-secret", envvar="SLACK_CLIENT_SECRET", help="Slack App Client Secret")
    ],
    scopes: Annotated[str, typer.Option("--scopes", help="Comma-separated bot scopes")] = DEFAULT_SCOPES,
    user_scopes: Annotated[
        str,
        typer.Option(
            "--user-scopes",
            help="Comma-separated user scopes (triggers user-token flow in addition to bot)",
        ),
    ] = "",
    user_only: Annotated[
        bool,
        typer.Option(
            "--user-only",
            help="Skip bot scopes — request only a user token. Requires --user-scopes.",
        ),
    ] = False,
    port: Annotated[int, typer.Option("--port", help="Local port for OAuth redirect")] = DEFAULT_PORT,
    timeout: Annotated[int, typer.Option("--timeout", help="Seconds to wait for the browser redirect")] = 180,
    no_browser: Annotated[
        bool, typer.Option("--no-browser", help="Print the authorize URL instead of opening a browser")
    ] = False,
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Print the full Slack response as JSON instead of just the token"),
    ] = False,
) -> None:
    """Obtain a Slack bot and/or user token via the OAuth v2 flow."""
    if user_only and not user_scopes:
        typer.echo("--user-only requires --user-scopes", err=True)
        raise typer.Exit(1)
    if not _port_available(port):
        typer.echo(f"Port {port} already in use — pick another with --port", err=True)
        raise typer.Exit(1)

    redirect_uri = f"http://localhost:{port}{CALLBACK_PATH}"
    state = secrets.token_urlsafe(16)

    authorize_params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "state": state,
    }
    if not user_only:
        authorize_params["scope"] = scopes
    if user_scopes:
        authorize_params["user_scope"] = user_scopes
    authorize_url = f"{SLACK_AUTHORIZE_URL}?" + urllib.parse.urlencode(authorize_params)

    result = CallbackResult()
    server = http.server.HTTPServer(("127.0.0.1", port), _make_handler(result))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        typer.echo(f"Redirect URI declared in the Slack App must include: {redirect_uri}", err=True)
        if no_browser:
            typer.echo(f"Open this URL in your browser:\n{authorize_url}", err=True)
        else:
            open_and_announce(authorize_url, what="Slack authorization page")

        if not result.received.wait(timeout=timeout):
            typer.echo(f"Timed out after {timeout}s waiting for the OAuth callback", err=True)
            raise typer.Exit(1)
    finally:
        server.shutdown()
        server.server_close()

    if result.error:
        typer.echo(f"Slack returned an error: {result.error}", err=True)
        raise typer.Exit(1)
    if result.state != state:
        typer.echo("State mismatch — possible CSRF, aborting", err=True)
        raise typer.Exit(1)
    if not result.code:
        typer.echo("No authorization code returned", err=True)
        raise typer.Exit(1)

    try:
        payload = _exchange_code(client_id, client_secret, result.code, redirect_uri)
    except (RuntimeError, urllib.error.URLError) as e:
        typer.echo(f"Token exchange failed: {e}", err=True)
        raise typer.Exit(1) from e

    access_token = payload.get("access_token", "")
    refresh_token = payload.get("refresh_token", "")
    expires_in = payload.get("expires_in", 0)
    authed_user = payload.get("authed_user", {})

    if json_output:
        print(
            json.dumps(
                {
                    "access_token": access_token,
                    "scope": payload.get("scope", ""),
                    "bot_user_id": payload.get("bot_user_id", ""),
                    "team": payload.get("team", {}),
                    "refresh_token": refresh_token,
                    "expires_in": expires_in,
                    "authed_user": authed_user,
                }
            )
        )
    else:
        user_token = authed_user.get("access_token", "") if isinstance(authed_user, dict) else ""
        token = str(access_token or user_token)
        if not token:
            typer.echo("No token returned by Slack", err=True)
            raise typer.Exit(1)
        print(token)

    if isinstance(authed_user, dict) and authed_user.get("id"):
        typer.echo(
            f"\nUser authenticated: id={authed_user.get('id')} (user scopes: {authed_user.get('scope', '')})",
            err=True,
        )
    if refresh_token:
        typer.echo(
            f"\nToken rotation is ENABLED on this app — access_token expires in {expires_in}s.\n"
            "Store both `access_token` and `refresh_token`, and refresh via oauth.v2.access\n"
            "with grant_type=refresh_token before expiry.",
            err=True,
        )
    else:
        typer.echo(
            "\nLong-lived token obtained (rotation disabled). Store it in AWS Secrets Manager, e.g.:\n"
            "  aws secretsmanager create-secret --name pysae/slack/ask-review-bot --secret-string <token>",
            err=True,
        )


if __name__ == "__main__":
    cli()
