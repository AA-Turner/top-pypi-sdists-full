"""One-shot CLI to mint a Google Search Console refresh token.

Usage
-----
1. Make sure your OAuth client allows the local-loopback redirect URI
   (`http://localhost:8765`). In Google Cloud Console → APIs & Services →
   Credentials, click your OAuth client and add `http://localhost:8765` to
   Authorized redirect URIs (you may already have it). For the Installed-app
   ("Desktop") OAuth client type, this is implicit.

2. Run this script with whichever Python has matrx-scraper installed:
       python -m matrx_scraper.gsc_bootstrap

3. A browser window opens. Sign in as the Google account that has access to
   the Search Console properties you want to query.

4. Grant the requested scope (read-only Search Console).

5. The script captures the OAuth callback, exchanges the code for tokens,
   prints the refresh token, and writes a `.env` line you can paste:

       GSC_REFRESH_TOKEN=1//0gA3...

6. Drop that into `.env`, restart the API, and the dashboard's Refresh
   button under Search Console will start working.

Why this is a one-time thing
----------------------------
GSC's OAuth flow gives you a *refresh token* once you've consented. The
server uses it to mint short-lived access tokens automatically — you don't
need to re-consent unless the user revokes the grant, the password is
changed, or 6 months pass without use.

Notes
-----
* This script depends on `google-auth-oauthlib`, which is in the venv via
  the matrx-utils transitive set. We don't need additional installs.
* The script only uses `https://www.googleapis.com/auth/webmasters.readonly`
  — read-only access to your Search Console data. It cannot modify anything.
"""

from __future__ import annotations

import http.server
import json
import os
import socketserver
import sys
import threading
import urllib.parse
import webbrowser
from pathlib import Path

# Where the operator's `.env` lives is a property of the PROJECT this CLI is
# run from — never of the package's own install path. Resolving it from
# ``__file__`` (as this did until 2026-08-09, with ``parents[3]`` meaning "the
# aidream repo root") is a repo-layout assumption: in any pip install that
# points at a random parent of site-packages, and in any consumer that is not
# aidream it points at someone else's tree. Walk up from the working directory
# instead, exactly like every other dotenv-aware CLI.


def _find_env_file() -> Path | None:
    cwd = Path.cwd().resolve()
    for candidate in (cwd, *cwd.parents):
        env = candidate / ".env"
        if env.is_file():
            return env
    return None


ENV_PATH = _find_env_file()


# Load .env so we can pick up GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET if the
# user already has them. We do this manually (rather than via dotenv.load_dotenv)
# so the script runs with no host settings layer importable at all.


def _load_env_file() -> None:
    if ENV_PATH is None or not ENV_PATH.exists():
        return
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k and v and k not in os.environ:
            os.environ[k] = v


_load_env_file()


# Re-use the resolver from performance.py so the precedence is identical.
from matrx_scraper.performance import _resolve_oauth_client  # noqa: E402

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
LOCAL_PORT = 8765
REDIRECT_URI = f"http://localhost:{LOCAL_PORT}"
AUTH_URI = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URI = "https://oauth2.googleapis.com/token"


def _build_auth_url(client_id: str) -> str:
    params = {
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",  # request a refresh token
        "prompt": "consent",  # always include refresh_token even on re-auth
        "include_granted_scopes": "true",
    }
    return f"{AUTH_URI}?{urllib.parse.urlencode(params)}"


class _CallbackServer(socketserver.TCPServer):
    allow_reuse_address = True
    code_holder: dict[str, str] = {}


class _CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        code = params.get("code", [None])[0]
        error = params.get("error", [None])[0]

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        if error:
            body = f"<h1>OAuth error</h1><pre>{error}</pre>"
        elif code:
            body = "<h1>Got it ✓</h1><p>You can close this tab. The CLI is finishing up.</p>"
            self.server.code_holder["code"] = code  # type: ignore[attr-defined]
        else:
            body = "<h1>No code in callback. Try again.</h1>"
        self.wfile.write(body.encode("utf-8"))

    def log_message(self, *args, **kwargs) -> None:  # noqa: D401
        return  # silence the dev-server logging


def _exchange_code_for_tokens(client_id: str, client_secret: str, code: str) -> dict:
    import urllib.request

    body = urllib.parse.urlencode(
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        TOKEN_URI,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _list_sites(access_token: str) -> list[dict]:
    """Best-effort listing of Search Console properties so the user can pick
    `GSC_DEFAULT_SITE_URL`. Failures are non-fatal."""
    import urllib.request

    req = urllib.request.Request(
        "https://searchconsole.googleapis.com/webmasters/v3/sites",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        print(f"[warn] couldn't list sites: {exc}", file=sys.stderr)
        return []
    return payload.get("siteEntry") or []


def main() -> int:
    client_id, client_secret = _resolve_oauth_client()
    if not client_id or not client_secret:
        print(
            "ERROR — no OAuth client found in env.\n\n"
            "Set one of:\n"
            "  GOOGLE_CLIENT_ID + GOOGLE_CLIENT_SECRET   (preferred — already there)\n"
            "  GSC_CLIENT_ID    + GSC_CLIENT_SECRET      (explicit override)\n"
            "  GOOGLE_OAUTH_CLIENT_SECRETS=/path/to/client_secrets.json\n",
            file=sys.stderr,
        )
        return 1

    print(f"Using OAuth client: {client_id[:20]}…")
    print()
    print("Step 1: opening Google's consent screen.")
    print(f"  Redirect URI: {REDIRECT_URI}")
    print(f"  Scope:        {SCOPES[0]}")
    print()
    print("If your OAuth client doesn't have http://localhost:8765 as an")
    print("authorized redirect URI yet, add it in Google Cloud Console first")
    print("(APIs & Services → Credentials → your OAuth 2.0 Client ID).")
    print()

    auth_url = _build_auth_url(client_id)
    print("If a browser doesn't open, paste this URL manually:")
    print(f"  {auth_url}")
    print()

    server = _CallbackServer(("127.0.0.1", LOCAL_PORT), _CallbackHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        webbrowser.open(auth_url)
        print("Waiting for callback…")
        # Poll for the code with a hard cap.
        import time

        deadline = time.time() + 300
        while "code" not in server.code_holder:
            if time.time() > deadline:
                print("Timed out waiting for OAuth callback.", file=sys.stderr)
                return 2
            time.sleep(0.25)
    finally:
        server.shutdown()

    code = server.code_holder["code"]
    print()
    print("Step 2: exchanging code for tokens…")
    try:
        tokens = _exchange_code_for_tokens(client_id, client_secret, code)
    except Exception as exc:
        print(f"Token exchange failed: {exc}", file=sys.stderr)
        return 3

    refresh_token = tokens.get("refresh_token")
    access_token = tokens.get("access_token")
    if not refresh_token:
        print(
            "Google didn't return a refresh_token. This usually means you've "
            "already consented before. Revoke the grant at "
            "https://myaccount.google.com/permissions and re-run.",
            file=sys.stderr,
        )
        return 4

    print("Step 3: enumerating your Search Console properties…")
    sites = _list_sites(access_token) if access_token else []
    print()
    print("---------------------------------------------------------------")
    print("DONE. Add the following to your .env (or wherever the API reads")
    print("its env from), then restart the API:")
    print()
    print(f"GSC_REFRESH_TOKEN={refresh_token}")
    if sites:
        # Pick the first usable site as a sensible default suggestion.
        usable = [
            s
            for s in sites
            if s.get("permissionLevel") in ("siteOwner", "siteFullUser", "siteRestrictedUser")
        ]
        if usable:
            preferred = usable[0]["siteUrl"]
            print(f"GSC_DEFAULT_SITE_URL={preferred}")
    print("---------------------------------------------------------------")
    if sites:
        print()
        print("Properties this token can read:")
        for s in sites:
            print(f"  - {s.get('siteUrl', '?'):40s}  ({s.get('permissionLevel', '?')})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
