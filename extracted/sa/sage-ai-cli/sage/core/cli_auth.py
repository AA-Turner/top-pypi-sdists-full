"""CLI authentication — Firebase email/password, token storage, auto-refresh."""

from __future__ import annotations

import json
import logging
import os
import stat
import threading
import time
import base64
from pathlib import Path
from typing import Optional
from cryptography.fernet import Fernet

import httpx

logger = logging.getLogger(__name__)
_auth_lock = threading.Lock()

FIREBASE_API_KEY = os.environ.get(
    "VITE_FIREBASE_API_KEY",
    "AIzaSyAX_tX1pr822FLr_jTBxwmUF-w-cUZ-UAE",  # public web key
)
IDENTITY_TOOLKIT = "https://identitytoolkit.googleapis.com/v1"
SECURE_TOKEN_URL = "https://securetoken.googleapis.com/v1/token"

AUTH_DIR = Path.home() / ".sage"
AUTH_FILE = AUTH_DIR / "auth.json"

def get_api_base() -> str:
    return os.environ.get("SAGE_API_BASE", "https://sageworksai.com")

SAGE_API_BASE = get_api_base()


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
        # Network failure (offline, DNS, timeout) — log warning and fallback to expired token for offline mode
        logger.warning(f"Could not reach auth server ({exc}). Continuing in offline mode with cached session.")
        return auth

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

    If the user already has a valid cached session, returns it immediately
    without opening the browser — this allows `sage login` to succeed
    even when offline.
    """
    # Check for existing valid session first (offline-safe)
    existing = load_auth()
    if existing and existing.get("id_token"):
        # Try to refresh if expired, but don't fail if offline
        if _is_expired(existing):
            try:
                existing = _refresh_token(existing)
            except RuntimeError:
                # Token revoked — need fresh login. Fall through to browser flow.
                existing = None
        if existing and existing.get("id_token"):
            email = existing.get("email", "unknown")
            tier = existing.get("tier", "unknown")
            print(f"\n  ✓ Already logged in as {email} ({tier} plan).")
            print(f"    Run `sage logout` to switch accounts.\n")
            # Best-effort sync
            try:
                sync_on_reconnect()
            except Exception:
                pass
            return existing

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

    auth_url = f"{get_api_base()}/?cli_port={port}&state={state}"

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
            from sage.cli_core import _sms_terminate_process
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
            f"{get_api_base()}/auth/verify",
            json={"token": auth["id_token"]},
            timeout=10,
        )
        if res.is_success:
            auth["tier"] = res.json().get("tier", "free")
    except Exception:
        auth["tier"] = "unknown"

    save_auth(auth)

    # Best-effort device registration (don't block login on failure)
    try:
        import platform as _plat
        import socket as _sock
        device_platform = {
            "Darwin": "macos", "Windows": "windows", "Linux": "linux",
        }.get(_plat.system(), "linux")
        device_name = f"{_sock.gethostname()} — CLI"
        httpx.post(
            f"{get_api_base()}/devices/register",
            json={
                "name": device_name,
                "platform": device_platform,
                "client": "cli",
                "capabilities": ["chat", "terminal", "code_exec"],
            },
            headers={"Authorization": f"Bearer {auth['id_token']}"},
            timeout=5,
        )
    except Exception:
        pass  # device registration is optional — don't break login

    return auth


def logout() -> None:
    clear_auth()
    
    # Terminate any running SMS bridge daemon before deleting its PID file
    try:
        from sage.core.sms_bridge import SMS_PID_FILE
        if SMS_PID_FILE.exists():
            pid_str = SMS_PID_FILE.read_text().strip()
            if pid_str.isdigit():
                from sage.cli_core import _sms_terminate_process
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


# ── Offline Usage Tracking (hardened) ────────────────────────────────────────

import hashlib
import hmac as _hmac_mod
import subprocess as _sp


def _get_machine_id() -> str:
    """Get a stable machine identifier. Uses hardware UUID on macOS/Linux,
    MachineGuid on Windows. Falls back to hostname + username hash if
    hardware ID is unavailable (VMs, containers).
    """
    import platform
    system = platform.system()

    try:
        if system == "Darwin":
            out = _sp.run(
                ["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"],
                capture_output=True, text=True, timeout=5,
            )
            for line in out.stdout.splitlines():
                if "IOPlatformUUID" in line:
                    return line.split('"')[-2]
        elif system == "Linux":
            for path in ("/etc/machine-id", "/sys/class/dmi/id/product_uuid"):
                p = Path(path)
                if p.exists():
                    try:
                        return p.read_text().strip()
                    except PermissionError:
                        continue
        elif system == "Windows":
            out = _sp.run(
                ["reg", "query",
                 "HKLM\\SOFTWARE\\Microsoft\\Cryptography",
                 "/v", "MachineGuid"],
                capture_output=True, text=True, timeout=5,
            )
            for line in out.stdout.splitlines():
                if "MachineGuid" in line:
                    parts = line.strip().split()
                    return parts[-1] if parts else ""
    except Exception:
        pass

    # Fallback: hash of hostname + username — not perfect but stable per-user-per-machine
    import socket, getpass
    return hashlib.sha256(f"{socket.gethostname()}:{getpass.getuser()}".encode()).hexdigest()


def _derive_key(uid: str = "") -> bytes:
    """Derive a Fernet key from the machine ID + user UID.
    
    This ensures:
    1. usage.enc can't be copied to another machine (different machine ID)
    2. usage.enc can't be shared between users (different UID)
    3. The key is deterministic — no .ukey file to delete
    """
    machine_id = _get_machine_id()
    auth = load_auth() or {}
    effective_uid = uid or auth.get("uid", "")
    salt = f"sage-usage-v2:{machine_id}:{effective_uid}"
    key_bytes = hashlib.pbkdf2_hmac("sha256", salt.encode(), b"sage-hardened", 100_000)
    # Fernet needs a url-safe base64-encoded 32-byte key
    return base64.urlsafe_b64encode(key_bytes[:32])


def _get_fernet() -> Fernet:
    return Fernet(_derive_key())


def _usage_hmac(data: bytes) -> bytes:
    """Compute HMAC-SHA256 for integrity verification of usage.enc."""
    machine_id = _get_machine_id()
    key = hashlib.sha256(f"sage-hmac:{machine_id}".encode()).digest()
    return _hmac_mod.new(key, data, hashlib.sha256).digest()


def _get_offline_tokens() -> int:
    usage_path = AUTH_FILE.parent / "usage.enc"
    hmac_path = AUTH_FILE.parent / "usage.hmac"
    watermark_path = AUTH_FILE.parent / "usage.watermark"

    if not usage_path.exists():
        # If the file was deleted but we had a watermark, the user tampered.
        # Return the watermark value so they can't reset to 0.
        if watermark_path.exists():
            try:
                return int(watermark_path.read_text().strip())
            except Exception:
                return 0
        return 0

    try:
        enc_data = usage_path.read_bytes()

        # HMAC integrity check
        if hmac_path.exists():
            stored_hmac = hmac_path.read_bytes()
            expected_hmac = _usage_hmac(enc_data)
            if not _hmac_mod.compare_digest(stored_hmac, expected_hmac):
                logger.warning("usage.enc HMAC mismatch — possible tampering. Using watermark.")
                if watermark_path.exists():
                    return int(watermark_path.read_text().strip())
                return 0

        f = _get_fernet()
        data = f.decrypt(enc_data).decode("utf-8")
        return int(data)
    except Exception:
        # Decryption failed (wrong machine, corrupted) — use watermark
        if watermark_path.exists():
            try:
                return int(watermark_path.read_text().strip())
            except Exception:
                pass
        return 0


def _add_offline_tokens(tokens: int) -> None:
    usage_path = AUTH_FILE.parent / "usage.enc"
    hmac_path = AUTH_FILE.parent / "usage.hmac"
    watermark_path = AUTH_FILE.parent / "usage.watermark"

    current = _get_offline_tokens()
    new_total = current + tokens
    try:
        AUTH_DIR.mkdir(parents=True, exist_ok=True)
        f = _get_fernet()
        enc_data = f.encrypt(str(new_total).encode("utf-8"))
        usage_path.write_bytes(enc_data)
        usage_path.chmod(0o600)

        # Write HMAC for integrity
        hmac_path.write_bytes(_usage_hmac(enc_data))
        hmac_path.chmod(0o600)

        # Update watermark (plaintext max-ever-seen — prevents delete-to-reset)
        watermark_path.write_text(str(new_total), encoding="utf-8")
        watermark_path.chmod(0o600)
    except Exception as exc:
        logger.warning("Failed to save offline usage: %s", exc)


def _clear_offline_tokens() -> None:
    """Clear offline tokens after successful sync. Also clears the watermark
    since the server now has the authoritative count."""
    for name in ("usage.enc", "usage.hmac", "usage.watermark"):
        p = AUTH_FILE.parent / name
        if p.exists():
            p.unlink(missing_ok=True)


def sync_on_reconnect() -> None:
    """Best-effort sync: fetch latest tier + limits from server and cache locally.

    Called on every CLI invocation. If online, updates the cached token_limit,
    tokens_used, and tier in auth.json so offline enforcement uses fresh data.
    If the user upgraded their plan, the new limits take effect immediately.
    Also syncs any pending offline tokens to the server.
    """
    if os.environ.get("SAGE_TESTING") == "1":
        return

    auth = load_auth()
    if auth is None:
        return

    try:
        token = get_valid_token()

        # First, sync any pending offline usage
        offline_tokens = _get_offline_tokens()
        if offline_tokens > 0:
            try:
                r = httpx.post(
                    f"{get_api_base()}/billing/track",
                    json={"type": "cli", "tokens": 0, "offline_tokens": offline_tokens},
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=5,
                )
                if r.is_success:
                    _clear_offline_tokens()
            except Exception:
                pass  # Will try again next invocation

        # Then fetch latest billing info (tier, limits, usage)
        r = httpx.get(
            f"{get_api_base()}/billing/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=8,
        )
        if r.is_success:
            data = r.json()
            auth["token_limit"] = data.get("token_limit", 0)
            auth["tokens_used"] = max(0, data.get("tokens_used", 0) - data.get("overage_paid_tokens", 0))
            auth["tier"] = data.get("tier", "free")
            save_auth(auth)
    except Exception:
        pass  # Offline — will sync next time


def track_usage(message_type: str = "cli", response_text: str = "") -> None:
    """Report one CLI AI response to the SAGE backend for token-based tracking.

    If offline, tracks the usage locally in an encrypted file.
    If online, syncs any pending offline usage along with the current usage.
    """
    tokens = max(1, len(response_text) // 4) if response_text else 500
    try:
        token = get_valid_token()
        offline_tokens = _get_offline_tokens()
        payload = {"type": message_type, "tokens": tokens, "text": response_text[:100]}
        if offline_tokens > 0:
            payload["offline_tokens"] = offline_tokens

        r = httpx.post(
            f"{get_api_base()}/billing/track",
            json=payload,
            headers={"Authorization": f"Bearer {token}"},
            timeout=5,
        )
        r.raise_for_status()
        if offline_tokens > 0:
            _clear_offline_tokens()
    except Exception as exc:
        # Track offline on network failure
        logger.debug("Offline usage tracked (%d tokens). Syncing when online. Error: %s", tokens, exc)
        _add_offline_tokens(tokens)


def check_token_quota() -> None:
    """Check if the user still has tokens remaining. Raises with upgrade message if not."""
    if os.environ.get("SAGE_TESTING") == "1":
        return

    auth = load_auth() or {}

    # Try fetching latest usage online (also syncs plan upgrades)
    try:
        token = get_valid_token()
        r = httpx.get(
            f"{get_api_base()}/billing/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=8,
        )
        if r.is_success:
            data = r.json()
            # Cache the latest limit and usage for offline enforcement
            auth["token_limit"] = data.get("token_limit", 0)
            auth["tokens_used"] = max(0, data.get("tokens_used", 0) - data.get("overage_paid_tokens", 0))
            auth["tier"] = data.get("tier", "free")
            save_auth(auth)
    except Exception:
        pass

    # Enforce quota (works both online and offline using cached + local offline usage)
    token_limit = auth.get("token_limit", 0)
    cached_used = auth.get("tokens_used", 0)
    offline_used = _get_offline_tokens()

    total_used = cached_used + offline_used
    tier = auth.get("tier", "free")

    if token_limit > 0 and total_used >= token_limit:
        raise RuntimeError(
            f"⚠  Token limit reached for {tier} plan.\n"
            f"   Total used: {total_used:,} / {token_limit:,} tokens (including {offline_used:,} offline).\n"
            f"   Usage has been blocked. Please go to your Billing page at {get_api_base()} to pay for overage or upgrade."
        )

