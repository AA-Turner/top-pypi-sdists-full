"""CLI authentication — Firebase email/password, token storage, auto-refresh."""

from __future__ import annotations

import json
import os
import stat
import threading
import time
from pathlib import Path
from typing import Optional

import httpx

_auth_lock = threading.Lock()

FIREBASE_API_KEY = os.environ.get(
    "VITE_FIREBASE_API_KEY",
    "AIzaSyAX_tX1pr822FLr_jTBxwmUF-w-cUZ-UAE",  # public web key
)
IDENTITY_TOOLKIT = "https://identitytoolkit.googleapis.com/v1"
SECURE_TOKEN_URL = "https://securetoken.googleapis.com/v1/token"

AUTH_DIR = Path.home() / ".sage"
AUTH_FILE = AUTH_DIR / "auth.json"

SAGE_API_BASE = os.environ.get("SAGE_API_BASE", "https://sageworksai.com")


# ── Token storage ─────────────────────────────────────────────────────────────

def save_auth(data: dict) -> None:
    AUTH_DIR.mkdir(parents=True, exist_ok=True)
    # Write to temp file first, then atomic rename — prevents partial writes.
    # Use Path.replace() not .rename(): on Windows, .rename() raises
    # FileExistsError if the target exists, while .replace() atomically
    # overwrites on every platform (POSIX semantics).
    tmp = AUTH_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    tmp.chmod(stat.S_IRUSR | stat.S_IWUSR)  # 600 — owner read/write only
    tmp.replace(AUTH_FILE)


def load_auth() -> dict | None:
    if not AUTH_FILE.exists():
        return None
    try:
        return json.loads(AUTH_FILE.read_text())
    except Exception:
        return None


def clear_auth() -> None:
    if AUTH_FILE.exists():
        AUTH_FILE.unlink()


# ── Token operations ──────────────────────────────────────────────────────────

def _jwt_exp(token: str) -> float:
    """Extract the `exp` claim from a JWT without verifying the signature.

    The JWT's own `exp` is the authoritative expiry — this is what the server
    checks. Any locally-stored `expires_at` can drift from it (Firebase's token
    refresh sometimes returns a token whose `exp` doesn't equal `now + expires_in`),
    so trusting `expires_at` alone causes false-negative refreshes that surface
    as 401s on the next API call.
    """
    try:
        import base64
        parts = token.split(".")
        if len(parts) < 2:
            return 0
        payload = parts[1] + "=" * (-len(parts[1]) % 4)
        claims = json.loads(base64.urlsafe_b64decode(payload))
        return float(claims.get("exp", 0))
    except Exception:
        return 0


def get_uid_from_token(token: str) -> str:
    """Extract the `sub` (uid) claim from a Firebase JWT without verifying the signature."""
    try:
        import base64
        parts = token.split(".")
        if len(parts) < 2:
            return ""
        payload = parts[1] + "=" * (-len(parts[1]) % 4)
        claims = json.loads(base64.urlsafe_b64decode(payload))
        return str(claims.get("sub", ""))
    except Exception:
        return ""


def _is_expired(auth: dict, buffer_seconds: int = 300) -> bool:
    """Return True if the stored token is within `buffer_seconds` of expiry.

    Trusts the JWT's `exp` claim over the locally-cached `expires_at` field
    when both are available, since they can drift apart over time.
    """
    token = auth.get("id_token", "")
    jwt_exp = _jwt_exp(token) if token else 0
    expires_at = auth.get("expires_at", 0)
    # If we have a real `exp`, prefer it. Otherwise fall back to expires_at.
    effective = jwt_exp or expires_at
    return time.time() >= (effective - buffer_seconds)


def _refresh_token(auth: dict) -> dict:
    if os.environ.get("SAGE_TESTING") == "1":
        auth["id_token"] = "test-token"
        auth["refresh_token"] = "test-refresh-token"
        return auth
    refresh = auth.get("refresh_token", "")
    if not refresh:
        raise RuntimeError("No refresh token available. Please run: sage login")
    try:
        r = httpx.post(
            f"{SECURE_TOKEN_URL}?key={FIREBASE_API_KEY}",
            json={"grant_type": "refresh_token", "refresh_token": refresh},
            timeout=15,
        )
    except httpx.HTTPError as exc:
        # Network failure (offline, DNS, timeout) — tell the user, don't crash.
        raise RuntimeError(
            f"Could not reach the SAGE auth server to refresh your session ({exc}). "
            "Check your internet connection and try again."
        ) from exc

    if r.status_code == 400:
        # Refresh token revoked, expired, or invalid. Wipe the bad credential
        # so the next login starts clean instead of looping on the same bad
        # token, then surface an actionable RuntimeError. Common causes:
        # backend rotated the key, user signed in elsewhere, or session
        # exceeded Firebase's max refresh window.
        try:
            error_body = r.json().get("error", {})
            firebase_msg = error_body.get("message") if isinstance(error_body, dict) else None
        except Exception:
            firebase_msg = None
        clear_auth()
        detail = f" ({firebase_msg})" if firebase_msg else ""
        raise RuntimeError(
            "Your SAGE session has expired or been revoked" + detail + ".\n"
            "Please run: sage login"
        )
    try:
        r.raise_for_status()
    except httpx.HTTPError as exc:
        raise RuntimeError(f"Could not refresh session: {exc}")
    data = r.json()
    new_id_token = data["id_token"]
    auth["id_token"] = new_id_token
    auth["refresh_token"] = data["refresh_token"]
    # Pin expires_at to the JWT's own `exp` so the local cache always matches
    # the token the server will check. Falls back to `now + expires_in` only
    # if the JWT is somehow undecodable.
    jwt_exp = _jwt_exp(new_id_token)
    auth["expires_at"] = jwt_exp or (time.time() + int(data.get("expires_in", 3600)))
    save_auth(auth)
    return auth


def get_valid_token() -> str:
    """Return a valid Firebase ID token, refreshing if needed. Raises if not logged in."""
    if os.environ.get("SAGE_TESTING") == "1":
        return "test-token"
    with _auth_lock:
        auth = load_auth()
        if auth is None:
            raise RuntimeError(
                "Not logged in. Run: sage login\n"
                "Server models and CLI require a paid plan. Browser AI is always free."
            )
        if _is_expired(auth):
            auth = _refresh_token(auth)
        return auth["id_token"]


def get_auth_headers() -> dict:
    """Return Authorization + X-CLI headers for backend requests."""
    token = get_valid_token()
    return {"Authorization": f"Bearer {token}", "X-CLI": "true"}


# ── Login — browser-based OAuth (supports Google, Apple, email/password) ──────

def login() -> dict:
    """Open the SAGE website in the browser for authentication.

    Supports all sign-in methods: Google, Apple, and email/password.
    The CLI spins up a local callback server, then opens the browser.
    After the user logs in on the website, the token is sent back here.
    """
    import secrets
    import socket
    import threading
    import webbrowser
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from urllib.parse import parse_qs, urlparse

    # Pick a random free port
    with socket.socket() as _s:
        _s.bind(("127.0.0.1", 0))
        port = _s.getsockname()[1]

    state = secrets.token_urlsafe(20)
    result: dict = {}
    stop_event = threading.Event()

    class _Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)

            def _p(k):
                return params.get(k, [None])[0]

            # CSRF check
            if _p("state") != state:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"<h1>Bad state - please retry sage login</h1>")
                return

            result["token"]   = _p("token")
            result["refresh"] = _p("refresh") or ""
            result["email"]   = _p("email") or ""
            result["uid"]     = _p("uid") or ""

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"""<!doctype html>
<html><head><title>SAGE CLI Auth</title>
<style>body{font-family:sans-serif;background:#0d0d17;color:#e8e8f0;
display:flex;align-items:center;justify-content:center;height:100vh;margin:0;text-align:center}
h2{color:#4ade80;font-size:24px;margin-bottom:8px}p{color:#888}</style>
</head><body>
<div><div style="font-size:48px;margin-bottom:16px">&#10003;</div>
<h2>Logged in successfully!</h2>
<p>You can close this tab and return to your terminal.</p></div>
</body></html>""")
            stop_event.set()

        def log_message(self, *args):
            pass  # suppress access log noise

    server = HTTPServer(("127.0.0.1", port), _Handler)
    server.timeout = 1.0  # short poll so we can check stop_event

    auth_url = f"{SAGE_API_BASE}/?cli_port={port}&state={state}"

    print()
    print("  Opening your browser to log in to SAGE AI...")
    print()
    print(f"  URL: {auth_url}")
    print()
    print("  Waiting for authentication (press Ctrl-C to cancel)…")

    webbrowser.open(auth_url)

    # Poll until the callback arrives or 5-minute timeout
    deadline = time.time() + 300
    while not stop_event.is_set() and time.time() < deadline:
        server.handle_request()

    server.server_close()

    if not result.get("token"):
        raise RuntimeError("Authentication timed out. Run `sage login` again.")

    # Detect account switch
    existing = load_auth()
    if existing and existing.get("uid") != result["uid"]:
        # User switched accounts! Stop any running bridge daemon.
        try:
            from sage.core.sms_bridge import SMS_PID_FILE
            from sage.main import _sms_terminate_process
            if SMS_PID_FILE.exists():
                pid = int(SMS_PID_FILE.read_text().strip())
                _sms_terminate_process(pid)
                if SMS_PID_FILE.exists(): SMS_PID_FILE.unlink()
        except Exception:
            pass

    auth = {
        "uid":           result["uid"],
        "email":         result["email"],
        "id_token":      result["token"],
        "refresh_token": result["refresh"],
        "expires_at":    time.time() + 3600,
    }

    # Verify with backend and get tier
    try:
        res = httpx.post(
            f"{SAGE_API_BASE}/auth/verify",
            json={"token": auth["id_token"]},
            timeout=10,
        )
        if res.is_success:
            auth["tier"] = res.json().get("tier", "free")
    except Exception:
        auth["tier"] = "unknown"

    save_auth(auth)
    return auth


def logout() -> None:
    clear_auth()
    
    # Terminate any running SMS bridge daemon before deleting its PID file
    try:
        from sage.core.sms_bridge import SMS_PID_FILE
        if SMS_PID_FILE.exists():
            pid_str = SMS_PID_FILE.read_text().strip()
            if pid_str.isdigit():
                from sage.main import _sms_terminate_process
                _sms_terminate_process(int(pid_str))
    except Exception:
        pass

    # Deep clean local identity data
    targets = [
        "verified_phone.txt",
        "sms_daemon.pid",
        "sms.log",
        "contacts.json",
        "last_seen_contacts.txt"
    ]
    for t in targets:
        p = Path.home() / ".sage" / t
        if p.exists():
            try:
                p.unlink()
            except Exception:
                pass
    
    # Also clear session history if it exists
    history_dir = Path.home() / ".sage" / "history"
    if history_dir.exists() and history_dir.is_dir():
        try:
            import shutil
            shutil.rmtree(history_dir)
        except Exception:
            pass


def whoami() -> dict | None:
    if os.environ.get("SAGE_TESTING") == "1":
        return {"email": "test@sageworksai.com", "tier": "admin"}
    auth = load_auth()
    if auth is None:
        return None
    if _is_expired(auth):
        try:
            auth = _refresh_token(auth)
        except Exception:
            return None
    return {"email": auth.get("email"), "tier": auth.get("tier", "unknown")}


def check_cli_access() -> None:
    """Raise RuntimeError if user is not logged in or on free tier."""
    if os.environ.get("SAGE_TESTING") == "1":
        return
    auth = load_auth()
    if auth is None:
        raise RuntimeError(
            "CLI requires a paid SAGE account.\n"
            "  1. Sign up at https://sageworksai.com\n"
            "  2. Subscribe to Starter or higher ($8/mo)\n"
            "  3. Run: sage login\n"
            "Browser AI at the website is always free."
        )
    tier = auth.get("tier", "free")
    if tier == "free":
        raise RuntimeError(
            "Your account is on the Free plan — CLI requires Starter or higher.\n"
            "Upgrade at: https://sageworksai.com (Billing tab)\n"
            "Browser AI at the website is always free."
        )


def track_usage(message_type: str = "cli", response_text: str = "") -> None:
    """Report one CLI AI response to the SAGE backend for token-based tracking.

    Fire-and-forget: never raises, never blocks. Called after each
    successful AI response in sage run.
    """
    try:
        token = get_valid_token()
        tokens = max(1, len(response_text) // 4) if response_text else 500
        httpx.post(
            f"{SAGE_API_BASE}/billing/track",
            json={"type": message_type, "tokens": tokens, "text": response_text[:100]},
            headers={"Authorization": f"Bearer {token}"},
            timeout=5,
        )
    except Exception:
        pass  # tracking failure must never interrupt the user's session


def check_token_quota() -> None:
    """Check if the user still has tokens remaining. Raises with upgrade message if not."""
    if os.environ.get("SAGE_TESTING") == "1":
        return
    try:
        token = get_valid_token()
        r = httpx.get(
            f"{SAGE_API_BASE}/billing/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=8,
        )
        if not r.is_success:
            return  # can't check — allow and let the backend enforce
        data = r.json()
        tokens_used = data.get("tokens_used", 0)
        token_limit = data.get("token_limit", 0)
        tier = data.get("tier", "free")
        if token_limit > 0 and tokens_used >= token_limit:
            remaining = token_limit - tokens_used
            overage_rates = {"starter": 0.001, "pro": 0.0008, "premium": 0.0005}
            rate = overage_rates.get(tier, 0.001)
            raise RuntimeError(
                f"⚠  Token limit reached: {tokens_used:,} / {token_limit:,} tokens used this month.\n"
                f"   Overage rate: ${rate}/1K tokens — usage continues and you will be billed.\n"
                f"   Upgrade for more tokens: {SAGE_API_BASE} (Billing tab)"
            )
    except RuntimeError:
        raise
    except Exception:
        pass  # quota check failure is non-fatal
