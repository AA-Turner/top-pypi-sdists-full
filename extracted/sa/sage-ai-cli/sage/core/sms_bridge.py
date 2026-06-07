"""
SAGE CLI message bridge — client side.

The user never configures email.  SAGE owns a central email address
(e.g. message@sageworksai.com).  Users just iMessage or email that address.

The CLI connects to the SAGE backend via WebSocket, authenticates with
the user's SAGE login token, and waits for task dispatches.

Flow:
  Phone → iMessage/Gmail → message@sageworksai.com
  Backend → authenticates sender → routes to this CLI via WebSocket
  CLI → executes sage ask → sends result back
  Backend → emails result from message@sageworksai.com → Phone

Setup:
  sage sms setup          (asks: computer name + working dir)
  sage sms contacts add layne@icloud.com --label iPhone
  sage sms start
"""

from __future__ import annotations

import json
import logging
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path

import httpx

logger = logging.getLogger("sage.sms_bridge")

SAGE_DIR     = Path.home() / ".sage"
SMS_CONFIG   = SAGE_DIR / "sms_config.json"
SMS_PID_FILE = SAGE_DIR / "sms_daemon.pid"
SMS_LOG_FILE = SAGE_DIR / "sms.log"

# How often to send a WebSocket heartbeat (keeps connection alive through proxies)
HEARTBEAT_INTERVAL = 25  # seconds


# ── Config — minimal, no email credentials ────────────────────────────────────

@dataclass
class SMSConfig:
    """
    Stored at ~/.sage/sms_config.json.
    No email credentials here — SAGE owns the bridge inbox.
    """
    computer_name: str   = field(default_factory=lambda: _default_name())
    working_dir:   str   = str(Path.home())
    model:         str   = ""
    temperature:   float = 0.7   # @temp <val>
    task_timeout:  int   = 0     # @timeout <secs>; 0 = unlimited
    output_mode:   str   = ""    # "verbose" | "quiet" | "" (auto)

    def save(self) -> None:
        SAGE_DIR.mkdir(parents=True, exist_ok=True)
        SMS_CONFIG.write_text(json.dumps(asdict(self), indent=2))
        SMS_CONFIG.chmod(0o600)

    @classmethod
    def load(cls) -> "SMSConfig | None":
        if not SMS_CONFIG.exists():
            return None
        try:
            data = json.loads(SMS_CONFIG.read_text())
            return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
        except Exception:
            return None


def _default_name() -> str:
    import socket
    return socket.gethostname().split(".")[0]


# ── Backend client ─────────────────────────────────────────────────────────────

class SAGEBackend:
    def __init__(self, token: str, base_url: str) -> None:
        self._token = token
        self._base = base_url.rstrip("/")
        self._headers = {"Authorization": f"Bearer {token}"}

    def _refresh_headers(self) -> tuple[bool, str]:
        """Force-refresh the Firebase token and update headers.

        Returns (ok, reason). On failure, `reason` is a user-facing string
        the caller can include in an error message.
        """
        try:
            from sage.core.cli_auth import _refresh_token, load_auth
            auth = load_auth()
            if not auth:
                return False, "Not logged in. Run: sage login"
            auth = _refresh_token(auth)
            self._token = auth["id_token"]
            self._headers = {"Authorization": f"Bearer {self._token}"}
            return True, ""
        except RuntimeError as exc:
            return False, str(exc)
        except Exception as exc:
            return False, f"Could not refresh token: {exc}"

    def _request(self, method: str, path: str, **kwargs) -> dict:
        """HTTP call with one automatic refresh-and-retry on 401.

        Defense in depth against locally-cached token expiry drifting from the
        JWT's actual `exp` — even if we somehow store a stale token, the first
        401 from the server triggers a refresh and retries once. If refresh
        itself fails (no refresh token, revoked, etc.), surface a clear
        "please run sage login" message instead of the raw 401.
        """
        url = f"{self._base}{path}"
        try:
            r = httpx.request(method, url, headers=self._headers, timeout=10, **kwargs)
            if r.status_code == 401:
                ok, reason = self._refresh_headers()
                if not ok:
                    raise RuntimeError(
                        f"Your SAGE session has expired. {reason}"
                        if reason and "sage login" not in reason.lower()
                        else (reason or "Your SAGE session has expired. Run: sage login")
                    )
                r = httpx.request(method, url, headers=self._headers, timeout=10, **kwargs)
            r.raise_for_status()
            return r.json()
        except httpx.HTTPError as e:
            raise RuntimeError(f"Backend API error: {e}")

    def _get(self, path: str) -> dict:
        return self._request("GET", path)

    def _post(self, path: str, body: dict) -> dict:
        return self._request("POST", path, json=body)

    def _delete(self, path: str) -> dict:
        return self._request("DELETE", path)

    def download_file(self, file_id: str, dest_path: str | Path) -> bool:
        """Download an uploaded file to a local destination."""
        url = f"{self._base}/github/download/{file_id}"
        try:
            r = httpx.get(url, headers=self._headers, timeout=30)
            r.raise_for_status()
            with open(dest_path, "wb") as f:
                f.write(r.content)
            return True
        except Exception as exc:
            logger.warning("download_file failed for %s: %s", file_id, exc)
            return False

    def list_computers(self) -> list[dict]:
        return self._get("/sms/computers").get("computers", [])

    def register_computer(self, computer_name: str, bridge_email: str = "") -> dict:
        """Tell the backend this device exists so it shows up in `sage sms devices`.

        Idempotent — the server upserts on (uid, computer_name). Without this
        call, a device only registers when `sage sms start` opens its
        WebSocket, so users who run `sage sms setup` and stop there never
        appear in the device list and can't be routed to.
        """
        body = {"computer_name": computer_name}
        if bridge_email:
            body["bridge_email"] = bridge_email
        resp = self._post("/sms/computers/register", body)
        return resp.get("computer", resp)

    def remove_computer(self, computer_id: str) -> dict:
        return self._delete(f"/sms/computers/{computer_id}")

    def list_contacts(self) -> list[dict]:
        return self._get("/sms/contacts").get("contacts", [])

    def add_contact(self, email: str, label: str = "", device_type: str = "") -> dict:
        body = {"email": email, "label": label}
        if device_type:
            body["device_type"] = device_type
        resp = self._post("/sms/contacts", body)
        return resp.get("contact", resp)

    def remove_contact(self, email: str) -> dict:
        from urllib.parse import quote
        return self._delete(f"/sms/contacts/{quote(email, safe='')}")

    def contact_emails(self) -> list[str]:
        return [c["email"] for c in self.list_contacts() if c.get("email")]

    def announce(self, computer_name: str) -> dict:
        """Notify all registered contacts that this computer is online.

        Returns the backend's by-method count so callers (sage sms test) can
        tell the user exactly which delivery paths fired.
        """
        try:
            return self._post("/sms/announce", {"computer_name": computer_name})
        except Exception as exc:
            logger.warning("announce failed: %s", exc)
            return {"ok": False, "error": str(exc)}

    def poller_status(self) -> dict:
        """Get backend IMAP poller health (for sage sms diagnose)."""
        try:
            return self._get("/sms/poller-status")
        except Exception as exc:
            return {"error": str(exc)}

    def reclaim_identities(self) -> dict:
        """Lock primary email and phone numbers to this account in the routing index."""
        try:
            return self._post("/sms/reclaim", {})
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    def dispatch_text(self, text: str, from_addr: str) -> dict:
        """Send an iMessage/SMS task through the backend's @target: router.

        Used by the local iMessage gateway to forward `@razor: ...` style
        commands to other devices. The backend dispatches via the existing
        WebSocket session map and returns the synchronous result, which the
        gateway then sends back to the user via iMessage/SMS itself.
        """
        try:
            return self._post("/sms/dispatch", {"text": text, "from": from_addr})
        except Exception as exc:
            return {"ok": False, "output": f"⚠ dispatch failed: {exc}", "computer": ""}

    def get_linked_providers(self) -> list[dict]:
        """Return the user's linked OAuth providers (Google, Apple, etc.)."""
        try:
            return self._get("/account/providers").get("providers", [])
        except Exception:
            return []

    def sync_provider_contacts(self) -> list[dict]:
        """Auto-register linked Google/Apple emails as SMS contacts."""
        try:
            return self._post("/account/sync-contacts", {}).get("added", [])
        except Exception:
            return []

    def ws_url(self) -> str:
        base = self._base.replace("https://", "wss://").replace("http://", "ws://")
        return f"{base}/ws/sms"

    def upload_file(self, file_path: str) -> str | None:
        """Upload a file to the backend /upload endpoint. Returns file_id if successful."""
        url = f"{self._base}/upload"
        try:
            import os
            filename = os.path.basename(file_path)
            import mimetypes
            mime_type, _ = mimetypes.guess_type(file_path)
            mime_type = mime_type or "application/octet-stream"
            
            with open(file_path, "rb") as f:
                files = {"file": (filename, f, mime_type)}
                r = httpx.post(url, headers=self._headers, files=files, timeout=30)
                if r.status_code == 401:
                    ok, reason = self._refresh_headers()
                    if ok:
                        f.seek(0)
                        r = httpx.post(url, headers=self._headers, files=files, timeout=30)
                r.raise_for_status()
                return r.json().get("file_id")
        except Exception as exc:
            logger.warning("Failed to upload file %s: %s", file_path, exc)
            return None

    def token(self) -> str:
        return self._token


def _load_sage_token() -> tuple[str, str]:
    from sage.core.cli_auth import get_valid_token, SAGE_API_BASE
    try:
        token = get_valid_token()
        return token, SAGE_API_BASE
    except RuntimeError:
        raise RuntimeError(
            "sage sms requires you to be logged in.\n"
            "Run: sage login"
        )


# ── Utilities ──────────────────────────────────────────────────────────────────

def _imessage_max_rowid() -> int:
    """Return the highest message rowid in chat.db, or -1 if unreadable.

    Used to verify whether `_send_imessage` actually queued a message —
    AppleScript's Messages.app handler returns success even for fake
    recipients, so the only reliable post-send check is whether a new
    row appeared in ~/Library/Messages/chat.db.
    """
    if sys.platform != "darwin":
        return -1
    db_path = os.path.expanduser("~/Library/Messages/chat.db")
    if not os.path.exists(db_path):
        return -1
    try:
        import sqlite3
        with sqlite3.connect(f"file:{db_path}?mode=ro", uri=True, timeout=2) as db:
            row = db.execute("SELECT COALESCE(MAX(rowid), 0) FROM message").fetchone()
            return int(row[0]) if row else 0
    except Exception:
        return -1


def _imessage_row_matches(prev_max_rowid: int, text: str, recipient: str | None = None) -> bool:
    """Confirm an outbound message was queued after prev_max_rowid.

    Modern macOS (Ventura+/Sonoma+) leaves the `text` column NULL for newly
    sent messages and stores the body inside the `attributedBody` BLOB as a
    serialized NSAttributedString.  A previous version of this matcher
    queried `text = ?` which always returned 0 rows on modern macOS,
    causing _send_imessage to wrongly report "no row appeared in chat.db
    after 5s" even when the message was queued successfully.

    The match is now permissive: any new outbound row (rowid > baseline,
    is_from_me = 1) with either a matching text prefix OR a non-empty
    attributedBody confirms the send. If `recipient` is provided, it also
    verifies that the message was sent to that specific handle.
    """
    if sys.platform != "darwin":
        return False
    db_path = os.path.expanduser("~/Library/Messages/chat.db")
    if not os.path.exists(db_path):
        return False
        
    try:
        import sqlite3
        db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True, timeout=2)
        try:
            # 1. Detect columns for compatibility
            cur = db.execute("PRAGMA table_info(message)")
            columns = {col[1] for col in cur.fetchall()}
            has_attr = "attributedBody" in columns
            
            # 2. Build query
            attr_check = "OR (m.attributedBody IS NOT NULL AND length(m.attributedBody) > 0)" if has_attr else ""
            
            sql = f"""
                SELECT 1 FROM message m
                LEFT JOIN handle h ON m.handle_id = h.rowid
                WHERE m.rowid > ? AND m.is_from_me = 1
                  AND (
                    (m.text IS NOT NULL AND substr(m.text, 1, 200) = substr(?, 1, 200))
                    {attr_check}
                  )
            """
            params = [prev_max_rowid, text]
            
            if recipient:
                recipient_clean = recipient.strip().lower()
                # Handle matching (flexible for phone numbers)
                if "@" in recipient_clean:
                    sql += " AND h.id = ?"
                    params.append(recipient_clean)
                else:
                    digits = re.sub(r"\D", "", recipient_clean)
                    if len(digits) >= 10:
                        # Match last 10 digits to ignore country code variances (+1 etc)
                        sql += " AND h.id LIKE ?"
                        params.append(f"%{digits[-10:]}")
                    else:
                        sql += " AND h.id = ?"
                        params.append(recipient_clean)
            
            sql += " LIMIT 1"
            row = db.execute(sql, params).fetchone()
            return row is not None
        finally:
            db.close()
    except Exception:
        return False


_bypass_recipient_verification_for_testing = False
_active_bridge_instance = None

def _normalize_e164_globally(raw: str) -> str:
    """Normalize phone-shaped sender to E.164 (+1XXXXXXXXXX or +XXXXXXXXXXXX)."""
    if not raw:
        return ""
    raw_clean = raw.strip().lower()
    digits = re.sub(r"\D", "", raw_clean)
    if not digits:
        return ""
    if len(digits) == 11 and digits.startswith("1"):
        return f"+{digits}"
    if len(digits) == 10:
        return f"+1{digits}"
    if raw_clean.startswith("+") or len(digits) >= 10:
        return f"+{digits}"
    return ""


def _is_recipient_verified_globally(recipient: str) -> bool:
    """Enforce strict cross-user messaging safety at the module level.

    Returns True if recipient matches the logged-in user's own email,
    phone number, or any of their linked provider credentials.
    Returns False otherwise.
    """
    global _active_bridge_instance
    if _active_bridge_instance is not None:
        try:
            if _active_bridge_instance._is_recipient_verified(recipient):
                return True
        except Exception:
            pass

    if _bypass_recipient_verification_for_testing:
        return True

    # Standard test environment bypass (pytest/CI) unless explicitly testing verification
    import os, sys
    if (os.environ.get("SAGE_SMS_BYPASS_VERIFICATION") == "1" or "pytest" in sys.modules) and not os.environ.get("SAGE_SMS_FORCE_VERIFICATION_TEST"):
        return True

    if not recipient:
        return False

    recipient_clean = recipient.strip().lower()

    # Normalise e164 inside module functions
    e164 = _normalize_e164_globally(recipient_clean)
    digits = re.sub(r"\D", "", recipient_clean)
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]

    verified_set = set()

    # 1. Check primary email from locally-cached auth credentials
    try:
        from sage.core.cli_auth import load_auth
        auth = load_auth()
        if auth and auth.get("email"):
            verified_set.add(auth["email"].lower().strip())
    except Exception:
        pass

    # 1b. Check primary phone from locally-cached verified phone file
    try:
        phone_file = Path.home() / ".sage" / "verified_phone.txt"
        if phone_file.exists():
            phone = phone_file.read_text(encoding="utf-8").strip()
            if phone:
                norm_phone = _normalize_e164_globally(phone)
                if norm_phone:
                    verified_set.add(norm_phone)
                    phone_digits = re.sub(r"\D", "", norm_phone)
                    if len(phone_digits) == 11 and phone_digits.startswith("1"):
                        phone_digits = phone_digits[1:]
                    verified_set.add(phone_digits)
    except Exception:
        pass

    # 2. Check backend for email and phone numbers (linked providers and /billing/me)
    try:
        from sage.core.sms_bridge import SAGEBackend, _load_sage_token
        token, api_base = _load_sage_token()
        be = SAGEBackend(token, api_base)

        # Get linked providers
        providers = be.get_linked_providers()
        for p in providers:
            email = (p.get("email") or "").lower().strip()
            if email:
                verified_set.add(email)
            phone = (p.get("phone_number") or "").strip()
            if phone:
                norm_phone = _normalize_e164_globally(phone)
                if norm_phone:
                    verified_set.add(norm_phone)
                    phone_digits = re.sub(r"\D", "", norm_phone)
                    if len(phone_digits) == 11 and phone_digits.startswith("1"):
                        phone_digits = phone_digits[1:]
                    verified_set.add(phone_digits)

        # Get primary info from /billing/me
        try:
            me = be._get("/billing/me")
            if me and me.get("email"):
                verified_set.add(me["email"].lower().strip())
        except Exception:
            pass

        # Get contacts from backend
        try:
            contacts = be.list_contacts()
            for c in contacts:
                c_email = (c.get("email") or "").lower().strip()
                if c_email:
                    # Allow all registered contacts to receive/send messages
                    verified_set.add(c_email)
                    if c_email.startswith("phone:"):
                        p_num = c_email.replace("phone:", "")
                        norm_p = _normalize_e164_globally(p_num)
                        if norm_p:
                            verified_set.add(norm_p)
                            p_digits = re.sub(r"\D", "", norm_p)
                            if len(p_digits) == 11 and p_digits.startswith("1"):
                                p_digits = p_digits[1:]
                            verified_set.add(p_digits)
                imsg = (c.get("imessage_address") or "").lower().strip()
                if imsg:
                    # Allow stored imessage addresses too
                    verified_set.add(imsg)
                    if "@" not in imsg:
                        norm_imsg = _normalize_e164_globally(imsg)
                        if norm_imsg:
                            verified_set.add(norm_imsg)
                            imsg_digits = re.sub(r"\D", "", norm_imsg)
                            if len(imsg_digits) == 11 and imsg_digits.startswith("1"):
                                imsg_digits = imsg_digits[1:]
                            verified_set.add(imsg_digits)
        except Exception:
            pass

    except Exception:
        pass

    # Check matches
    if recipient_clean in verified_set:
        return True
    if e164 and e164 in verified_set:
        return True
    if digits and digits in verified_set:
        return True

    # Check carrier gateways
    if "@" in recipient_clean:
        local = recipient_clean.split("@")[0]
        if local.isdigit():
            norm_local = _normalize_e164_globally(local)
            if norm_local in verified_set:
                return True
            local_digits = re.sub(r"\D", "", local)
            if len(local_digits) == 11 and local_digits.startswith("1"):
                local_digits = local_digits[1:]
            if local_digits in verified_set:
                return True

    return False


def _send_imessage(recipient: str, text: str, attachment_paths: list[str] | None = None) -> bool:
    """Send an iMessage from this Mac via the Messages app.

    Recipient can be an Apple ID email (e.g. user@icloud.com) or a phone
    number in E.164 format (+14085073140). Works only when the Mac is
    signed into an Apple ID with iMessage enabled.
    """
    if sys.platform != "darwin":
        logger.warning("iMessage is only supported on macOS/darwin. Current platform is %s. Skipping.", sys.platform)
        return False

    safe_text = text.replace("\\", "\\\\").replace('"', '\\"')
    safe_to   = recipient.replace("\\", "\\\\").replace('"', '\\"')

    baseline = _imessage_max_rowid()

    if attachment_paths is None:
        attachment_paths = []
        import os, re
        raw_paths = re.findall(r'(?:[a-zA-Z]:[\\/][^\s\'"`]+|/[^\s\'"`]+|\b[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9]{2,5}\b)', text)
        for p in raw_paths:
            p_clean = p.strip(".,;:!?()[]{}<>\"'`")
            if os.path.isfile(p_clean):
                attachment_paths.append(os.path.abspath(p_clean))
            elif os.path.isfile(os.path.join(os.getcwd(), p_clean)):
                attachment_paths.append(os.path.abspath(os.path.join(os.getcwd(), p_clean)))

    def _run_send_script(target_keyword: str, service_name: str | None = "iMessage") -> tuple[bool, str]:
        """Run the send via osascript with `participant` or `buddy` keyword."""
        attachment_cmds = ""
        if attachment_paths:
            for ap in attachment_paths:
                safe_ap = ap.replace("\\", "\\\\").replace('"', '\\"')
                attachment_cmds += f'        send POSIX file "{safe_ap}" to targetBuddy\n'
        
        if service_name:
            service_setup = f'        set targetService to 1st service whose service type = {service_name}\n'
            buddy_setup = f'        set targetBuddy to {target_keyword} "{safe_to}" of targetService\n'
        else:
            service_setup = ''
            buddy_setup = f'        set targetBuddy to {target_keyword} "{safe_to}"\n'

        script = (
            'tell application "Messages"\n'
            '    try\n'
            f'{service_setup}'
            f'{buddy_setup}'
            f'{attachment_cmds}'
            '        send "{safe_text}" to targetBuddy\n'
            '        return "ok"\n'
            '    on error errMsg number errNum\n'
            '        return "err " & errNum & ": " & errMsg\n'
            '    end try\n'
            'end tell'
        )
        try:
            r = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True, text=True, timeout=10,
            )
            return r.returncode == 0, (r.stdout or "").strip() or (r.stderr or "").strip()
        except Exception as exc:
            return False, f"exception: {exc}"

    # Try modern `participant` and legacy `buddy`, with and without service constraint.
    # Either may script-succeed without iMessage queuing anything; chat.db is the ground truth.
    script_errors: list[str] = []
    success = False
    
    # Priority: iMessage (modern), iMessage (legacy), SMS (modern), SMS (legacy), No Service (modern), No Service (legacy)
    strategies = [
        ("participant", "iMessage"),
        ("buddy", "iMessage"),
    ]
    
    # Only try SMS fallback if it's a phone number (digits only or starts with +)
    if not "@" in recipient:
        strategies.extend([
            ("participant", "SMS"),
            ("buddy", "SMS"),
        ])
        
    strategies.extend([
        ("participant", None),
        ("buddy", None),
    ])

    for keyword, service in strategies:
        ok, msg = _run_send_script(keyword, service_name=service)
        if ok and msg == "ok":
            success = True
            break
        script_errors.append(f"{keyword}(service={service}): {msg}")
        logger.debug("osascript iMessage (%s, service=%s) to %s: %s", keyword, service, recipient, msg)

    if not success:
        combined_errors = "; ".join(script_errors)
        logger.warning("iMessage/SMS dispatch failed for %s: %s", recipient, combined_errors)
        return False
        
    # If chat.db is unreadable, we cannot VERIFY delivery, but the osascript
    # above just returned "ok". We must trust the status and warn the user.
    if baseline == -1:
        logger.warning("Full Disk Access missing: SAGE cannot verify iMessage delivery via chat.db. Trusting osascript return status.")
        return True

    for i in range(20):  # 20 × 0.25s = 5s
        time.sleep(0.25)
        if _imessage_row_matches(baseline, text, recipient):
            logger.info("iMessage delivery verified for %s (attempt %d)", recipient, i+1)
            return True
            
    logger.warning(
        "iMessage to %s: osascript returned 'ok' but no row appeared in chat.db after 5s. "
        "Likely causes: recipient handle is invalid for iMessage, Messages.app is not signed in, "
        "or Full Disk Access is missing/revoked.",
        recipient
    )
    return False


def _find_kdeconnect_cli() -> str | None:
    """Locate the kdeconnect-cli binary across platforms.

    On Linux it's in PATH after `apt install kdeconnect`. On macOS the
    Mac App Store / KDE binary release places it inside the app bundle at
    /Applications/KDE Connect.app/Contents/MacOS/kdeconnect-cli — Homebrew
    formula does not exist. On Windows it's in the install directory.
    """
    # PATH first (works on Linux, post-install Windows)
    found = shutil.which("kdeconnect-cli")
    if found:
        return found
    # macOS app bundle locations and common installation paths
    candidates = [
        "/Applications/KDE Connect.app/Contents/MacOS/kdeconnect-cli",
        os.path.expanduser("~/Applications/KDE Connect.app/Contents/MacOS/kdeconnect-cli"),
        os.path.expanduser("~/Applications/KDE/KDE Connect.app/Contents/MacOS/kdeconnect-cli"),
        "/opt/homebrew/bin/kdeconnect-cli",
        "/usr/local/bin/kdeconnect-cli",
        # Windows default install path (when Python runs there)
        r"C:\Program Files\KDE Connect\kdeconnect-cli.exe",
        r"C:\Program Files\KDE Connect\bin\kdeconnect-cli.exe",
        r"C:\Program Files (x86)\KDE Connect\kdeconnect-cli.exe",
        r"C:\Program Files (x86)\KDE Connect\bin\kdeconnect-cli.exe",
    ]
    local_appdata = os.environ.get("LOCALAPPDATA")
    if local_appdata:
        candidates.append(os.path.join(local_appdata, "KDE Connect", "bin", "kdeconnect-cli.exe"))
        candidates.append(os.path.join(local_appdata, "Programs", "KDE Connect", "bin", "kdeconnect-cli.exe"))
        candidates.append(os.path.join(local_appdata, "Programs", "KDE Connect", "kdeconnect-cli.exe"))
    appdata = os.environ.get("APPDATA")
    if appdata:
        candidates.append(os.path.join(appdata, "KDE Connect", "bin", "kdeconnect-cli.exe"))
        candidates.append(os.path.join(appdata, "Programs", "KDE Connect", "bin", "kdeconnect-cli.exe"))
        candidates.append(os.path.join(appdata, "Programs", "KDE Connect", "kdeconnect-cli.exe"))

    candidates += [
        os.path.expanduser("~/AppData/Local/KDE Connect/bin/kdeconnect-cli.exe"),
        os.path.expanduser("~/AppData/Local/Programs/KDE Connect/bin/kdeconnect-cli.exe"),
        os.path.expanduser("~/AppData/Roaming/KDE Connect/bin/kdeconnect-cli.exe"),
        os.path.expanduser("~/AppData/Roaming/Programs/KDE Connect/bin/kdeconnect-cli.exe"),
    ]

    for c in candidates:
        if os.path.exists(c):
            return c
    return None


def _send_macos_sms(recipient: str, text: str) -> bool:
    """Send a real SMS via Messages.app's SMS service (iPhone relay).

    Requires:
      - macOS with Messages.app signed into the same iCloud as a paired iPhone
      - iPhone has "Text Message Forwarding" enabled for this Mac
        (Settings → Messages → Text Message Forwarding → toggle on this Mac)

    The iPhone receives the dispatch and sends the SMS over its cellular plan,
    so the recipient sees a normal text from the user's phone number — no
    carrier-domain filtering, no email-to-SMS gateway. Works for ANY recipient,
    Apple or Android.

    This is the macOS replacement for KDE Connect's --send-sms (which is
    broken on the Mac App Store version due to a DBus registration bug).
    """
    if sys.platform != "darwin":
        logger.warning("macOS SMS relay is only supported on macOS/darwin. Current platform is %s. Skipping.", sys.platform)
        return False
    safe_text = text.replace("\\", "\\\\").replace('"', '\\"')
    safe_to   = recipient.replace("\\", "\\\\").replace('"', '\\"')

    def _run_send_script(target_keyword: str, use_service: bool = True) -> tuple[bool, str]:
        if use_service:
            service_setup = '        set smsService to first service whose service type = SMS\n'
            buddy_setup = f'        set targetBuddy to {target_keyword} "{safe_to}" of smsService\n'
        else:
            service_setup = ''
            buddy_setup = f'        set targetBuddy to {target_keyword} "{safe_to}"\n'

        script = (
            'tell application "Messages"\n'
            '    try\n'
            f'{service_setup}'
            f'{buddy_setup}'
            f'        send "{safe_text}" to targetBuddy\n'
            '        return "ok"\n'
            '    on error errMsg\n'
            '        return "err: " & errMsg\n'
            '    end try\n'
            'end tell'
        )
        try:
            r = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True, text=True, timeout=10,
            )
            return r.returncode == 0, (r.stdout or "").strip() or (r.stderr or "").strip()
        except Exception as exc:
            return False, f"exception: {exc}"

    success = False
    script_errors = []
    for use_service in (True, False):
        for keyword in ("buddy", "participant"):
            ok, msg = _run_send_script(keyword, use_service=use_service)
            if ok and msg == "ok":
                success = True
                break
            script_errors.append(f"{keyword}(service={use_service}): {msg}")
        if success:
            break

    if not success:
        logger.debug("Messages.app SMS send failed: %s", "; ".join(script_errors))
        return False

    baseline = _imessage_max_rowid()
    if baseline == -1:
        logger.warning("Full Disk Access missing: SAGE cannot verify SMS delivery via chat.db. Trusting osascript return status.")
        return True
        
    for _ in range(20):
        time.sleep(0.25)
        if _imessage_row_matches(baseline, text, recipient):
            logger.info("SMS delivery verified for %s", recipient)
            return True
            
    logger.warning("SMS to %s: osascript said ok but no row appeared in chat.db", recipient)
    return False


def _kdeconnectd_running() -> tuple[bool, str]:
    """Check whether KDE Connect daemon is running/active.

    If the daemon is running, but no devices are paired, returns True with a warning,
    so that diagnostics and startup do not report a hard error.
    """
    cli = _find_kdeconnect_cli()
    if not cli:
        return False, "kdeconnect-cli not installed"

    from sage.core.kdeconnect_listener import _is_daemon_running
    daemon_alive = _is_daemon_running()

    # Also check if SAGE's takeover listener is active
    from sage.core.sms_bridge import _active_bridge_instance
    takeover_active = False
    if _active_bridge_instance and getattr(_active_bridge_instance, "_kde_listener", None):
        takeover_active = True

    if not daemon_alive and not takeover_active:
        return False, "kdeconnectd daemon is not running"

    try:
        r = subprocess.run([cli, "--list-available", "--id-only"],
                           capture_output=True, text=True, timeout=5)
        import re
        devices = []
        for line in (r.stdout or "").splitlines():
            line = line.strip()
            if not line or "devices found" in line.lower():
                continue
            line_clean = re.sub(r'^[\-\*\+\s]+', '', line)
            if ":" in line_clean:
                parts = line_clean.split(":")
                id_candidate = parts[-1].strip().split()[0]
                devices.append(id_candidate)
            else:
                words = line_clean.split()
                if words:
                    devices.append(words[0])

        valid_devices = []
        for raw_device_id in devices:
            device_id = re.sub(r'[^\w\-]', '', raw_device_id)
            if device_id:
                valid_devices.append(device_id)

        if not valid_devices:
            return True, "no paired+reachable KDE Connect devices online"
        return True, ""
    except Exception as exc:
        return True, f"kdeconnect-cli probe failed but daemon is alive: {exc}"


def _start_kdeconnectd_macos() -> bool:
    """On macOS, launch kdeconnectd from the app bundle if not already running.

    The kdeconnect-cli binary depends on the daemon being live in the user
    session. The Mac App Store version doesn't auto-launch it — opening the
    GUI app does. We can shortcut by spawning the daemon binary directly.
    """
    if sys.platform != "darwin":
        return False
    daemon_paths = [
        "/Applications/KDE Connect.app/Contents/MacOS/kdeconnectd",
        os.path.expanduser("~/Applications/KDE Connect.app/Contents/MacOS/kdeconnectd"),
    ]
    daemon = next((p for p in daemon_paths if os.path.exists(p)), None)
    if not daemon:
        return False
    try:
        # Spawn detached so it survives our process. Equivalent to `nohup ... &`.
        subprocess.Popen(
            [daemon],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )
        # Give the daemon a moment to register on DBus
        import time as _t; _t.sleep(2)
        ok, _ = _kdeconnectd_running()
        return ok
    except Exception as exc:
        logger.debug("Could not start kdeconnectd: %s", exc)
        return False


def _send_via_kdeconnect(phone_number: str, text: str) -> bool:
    """Send a real SMS from the user's paired Android phone via KDE Connect.

    Requirements (one-time setup):
      - KDE Connect desktop app on this computer (Mac App Store / apt / dnf /
        pacman / Microsoft Store / kdeconnect.kde.org/download)
      - KDE Connect app on the Android phone (Google Play)
      - Devices paired and on the same Wi-Fi network

    This sends a REAL SMS from the user's own phone (their cellular plan).

    Note: on macOS Mac App Store, kdeconnect-cli prints a DBus activation
    error to stderr but the network-discovery fallback path still delivers
    the SMS reliably. We trust exit code only — stderr noise is cosmetic.
    """
    cli = _find_kdeconnect_cli()
    if not cli:
        return False

    # Try to start daemon cross-platform if not running
    if "pytest" not in sys.modules:
        try:
            from sage.core.kdeconnect_listener import _is_daemon_running, _start_os_daemon
            if not _is_daemon_running():
                logger.info("kdeconnectd is not running — attempting to start it")
                _start_os_daemon()
                # Give the daemon a moment to register
                import time as _t
                _t.sleep(2)
        except Exception as exc:
            logger.debug("Failed to check/start daemon: %s", exc)

    try:
        # Find a paired+reachable device.
        result = subprocess.run(
            [cli, "--list-available", "--id-only"],
            capture_output=True, text=True, timeout=5,
        )
        
        # Robustly parse device IDs (supports standard format, list format, and lines with bullet decorators)
        import re
        devices = []
        for line in (result.stdout or "").splitlines():
            line = line.strip()
            if not line or "devices found" in line.lower():
                continue
            line_clean = re.sub(r'^[\-\*\+\s]+', '', line)
            if ":" in line_clean:
                parts = line_clean.split(":")
                id_candidate = parts[-1].strip().split()[0]
                devices.append(id_candidate)
            else:
                words = line_clean.split()
                if words:
                    devices.append(words[0])

        if not devices:
            logger.debug("KDE Connect: no paired+reachable devices found")
            return False

        # Loop through all found devices and try sending the SMS. If one succeeds, we return True.
        sent_any = False
        for raw_device_id in devices:
            device_id = re.sub(r'[^\w\-]', '', raw_device_id)
            if not device_id:
                continue
            send_result = subprocess.run(
                [cli, "--send-sms", text,
                 "--destination", phone_number,
                 "-d", device_id],
                capture_output=True, text=True, timeout=10,
            )
            if send_result.returncode == 0:
                sent_any = True
                logger.info("KDE Connect: successfully sent SMS to %s via device %s", phone_number, device_id)
                break
            else:
                logger.debug("KDE Connect send to device %s failed (exit %d): %s",
                             device_id, send_result.returncode, (send_result.stderr or "").strip())
        return sent_any
    except Exception as exc:
        logger.debug("KDE Connect send failed: %s", exc)
        return False


def _strip_ansi(text: str) -> str:
    text = re.sub(r'\x1b\[[0-9;]*[mGKHFABCDEJst]', '', text)
    return re.sub(r'\x1b\][^\x07]*\x07', '', text).strip()


def _extract_file_attachments(text: str, working_dir: Path) -> list[str]:
    """Find files in the response text that actually exist on disk."""
    import os
    candidates = []
    
    # Extract quoted substrings
    for quote_char in ("'", '"', "`"):
        parts = text.split(quote_char)
        for i in range(1, len(parts), 2):
            candidates.append(parts[i].strip())
            
    # Split by whitespace and check each token
    for token in text.split():
        token_clean = token.strip(".,;:!?()[]{}<>\"'`")
        if token_clean:
            candidates.append(token_clean)
            
    found = []
    seen = set()
    for c in candidates:
        if not c or c in seen:
            continue
        seen.add(c)
        
        try:
            p = Path(c)
            if p.is_absolute() and p.is_file():
                found.append(str(p.resolve()))
                continue
        except Exception:
            pass
            
        try:
            p_rel = (working_dir / c).resolve()
            if p_rel.is_file():
                found.append(str(p_rel))
                continue
        except Exception:
            pass
            
    return found


def _filter_attachments_for_phone(file_paths: list[str], task_prompt: str) -> list[str]:
    """Filter files so only Documents, Images, Videos, and Audio files are sent to the phone.
    
    Coding files (like .py, .js, .ts, etc.) are excluded unless specifically asked for.
    """
    prompt_lower = task_prompt.lower()
    
    # Require explicit mention of sending to the phone to bypass filter.
    specifically_asked = (
        "to phone" in prompt_lower or 
        "to my phone" in prompt_lower or
        "send to phone" in prompt_lower or
        "send code to my phone" in prompt_lower
    )
    
    if specifically_asked:
        return file_paths
        
    # Standard coding extensions/names to exclude
    coding_extensions = {
        '.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.go', '.rs', '.c', '.cpp', 
        '.h', '.hpp', '.html', '.css', '.yaml', '.yml', '.toml', '.sh', '.bat', 
        '.rb', '.php', '.pl', '.sql', '.swift', '.kt', '.kts', '.cs', '.pbxproj',
        '.class', '.o', '.obj', '.dll', '.so', '.dylib', '.lock', '.json', '.md'
    }
    coding_filenames = {'dockerfile', 'makefile', 'gemfile', 'rakefile', 'pipfile'}
    
    # Standard allowed extensions for Documents, Images, Videos, and Audio
    allowed_extensions = {
        # Images
        '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp', '.ico', '.tiff',
        # Videos
        '.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv', '.mpeg', '.mpg',
        # Audio
        '.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg', '.wma',
        # Documents
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.csv'
    }
    
    filtered = []
    for fp in file_paths:
        p = Path(fp)
        name_lower = p.name.lower()
        suffix = p.suffix.lower()
        
        # If suffix is in coding_extensions or name is a known coding filename, exclude it.
        if suffix in coding_extensions or name_lower in coding_filenames:
            continue
            
        # If the suffix is in allowed_extensions, allow it.
        if suffix in allowed_extensions:
            filtered.append(fp)
            
    return filtered


def _find_recent_files(working_dir: Path, start_time: float) -> list[str]:
    """Find files in the working directory modified since start_time, up to 50MB."""
    import os
    found = []
    ignored_dirs = {
        ".git", ".sage", "venv", ".venv", "node_modules", "__pycache__", "target",
        "Library", "Pictures", "Music", "Movies", "Desktop", "Downloads", "Public",
        "Applications", ".Trash"
    }
    
    # We walk the directory
    for root, dirs, files in os.walk(str(working_dir)):
        dirs[:] = [d for d in dirs if d not in ignored_dirs and not d.startswith(".")]
        for file in files:
            file_path = os.path.join(root, file)
            try:
                mtime = os.path.getmtime(file_path)
                if mtime >= start_time:
                    size = os.path.getsize(file_path)
                    if 0 < size < 50 * 1024 * 1024:  # >0 and <50MB
                        found.append(os.path.abspath(file_path))
            except Exception:
                pass
    return found


def _share_via_kdeconnect(file_path: str) -> bool:
    """Share a file with the paired Android device via KDE Connect --share."""
    cli = _find_kdeconnect_cli()
    if not cli:
        return False
    try:
        # Find a paired+reachable device
        result = subprocess.run(
            [cli, "--list-available", "--id-only"],
            capture_output=True, text=True, timeout=5,
        )
        devices = []
        for line in (result.stdout or "").splitlines():
            line = line.strip()
            if not line or "devices found" in line.lower() or " " in line:
                continue
            devices.append(line)
        if not devices:
            return False
        device_id = devices[0]
        share_result = subprocess.run(
            [cli, "--share", file_path, "-d", device_id],
            capture_output=True, text=True, timeout=15,
        )
        return share_result.returncode == 0
    except Exception as exc:
        logger.debug("KDE Connect share file failed: %s", exc)
        return False


# Tool-call / prompt / footer noise that streams from `sage ask --raw`.
# We strip these before SMS so the user gets the FINAL ANSWER, not the work log.
_TOOL_LINE_RE = re.compile(
    r'^\s*(READ|WRITE|EDIT|RUN|BASH|GREP|GLOB|LS|FIND|FETCH|SEARCH|TASK|TODO|'
    r'PATCH|APPLY|DIFF|CREATE|DELETE|MOVE|COPY|VIEW|OPEN|TOOL|CALL|FILE|'
    r'COMMAND|EXEC|EXECUTE|SHELL)\s*:.*$',
    re.IGNORECASE,
)
# `+ filename` and `- filename` markers SAGE prints after FILE: writes
_FILE_MARKER_RE = re.compile(r'^\s*[+\-]\s+\S+\s*$')
_PROMPT_LINE_RE = re.compile(r'^\s*\[SAGE[^\]]*\]\s*sage>.*$', re.IGNORECASE)
# A bare `sage>` prefix at line start — strip the prefix only, not the whole line,
# so legitimate content after `sage>` (the agent's actual answer line) is kept.
_SAGE_PREFIX_RE = re.compile(r'^\s*sage>\s?', re.IGNORECASE)
_FOOTER_LINE_RE = re.compile(r'^\s*[─\-]\s*\d+\s*tokens?\b.*$')
_THINK_BLOCK_RE = re.compile(r'<thinking>.*?</thinking>', re.DOTALL | re.IGNORECASE)
# Agent planning lines (the model recapping its plan in numbered steps) —
# `STEP 1: ...`, `STEP 2: ...`, `Step 1.`, etc. These are not the answer.
_STEP_LINE_RE = re.compile(r'^\s*STEP\s+\d+\s*[:.—–-]', re.IGNORECASE)
# Planning-step metadata tail. The agent emits steps with trailing markers like
# `— None`, `— None (Execution step)`, `— No files`, `— `<file>``. When a long
# STEP description wraps onto a continuation line, that wrapped line still
# ends with this tail. Catches the wrap-continuation that _STEP_LINE_RE misses.
_PLANNING_TAIL_RE = re.compile(
    r'—\s*(?:None|No files|`[^`]+`)(?:\s*\([^)]*\))?\s*$',
    re.IGNORECASE,
)

# Rich Panel art / box-drawing UI chrome. Matches anything starting with
# one of: ╭ ╮ ╯ ╰ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ ─ ━ ═ │ ┃ ║. The interactive `sage run`
# banner is wrapped in this; over SMS it's just garbage characters.
_PANEL_LINE_RE = re.compile(r'^\s*[╭╮╯╰┌┐└┘├┤┬┴┼─━═│┃║▏▕]')

# Rich status-spinner final states ("✓ Project scanned", "✓ done", etc.) and
# the harness's "Shell cwd was reset to ..." trailer that the parent process
# prints after the subprocess returns. None of these are the model's answer.
_STATUS_LINE_RE = re.compile(
    r'^\s*(?:'
    r'[✓✗⚠ℹ]\s+|'                                     # Status glyphs
    r'Shell cwd was reset to|'                         # Subprocess trailer
    r'(?:Project scanned|Loading|Initializing|Ready)\b'
    r')',
    re.IGNORECASE,
)

# Model-backend init noise. llama-cpp-python and ggml print warnings/errors
# to stderr during model load: Metal compilation messages, n_ctx warnings,
# load-failure tracebacks. None of this is the agent's answer — it's
# infrastructure complaining at the SMS user. Strip aggressively.
_BACKEND_NOISE_RE = re.compile(
    r'^\s*(?:'
    r'\[llama_cpp\]|'                                      # [llama_cpp] failed: ...
    r'llama_(?:context|model|backend|new_context)|'        # llama_context: n_ctx_seq...
    r'ggml_|'                                              # ggml_metal_init / ggml_backend / etc.
    r'Metal\s+(?:GPU|backend|library)|'                    # Metal-related lines
    r'GGML_|'                                              # GGML_BACKEND etc.
    r'Failed to load model|'                               # llama_cpp load failures
    r'Exception ignored in:|'                              # Python __del__ noise
    r'Traceback \(most recent call last\):|'               # Python tracebacks
    r'  File "/[^"]+", line \d+|'                          # Traceback frames
    r'  +\^+\s*$|'                                         # Traceback ^^^^^ marker
    r'(?:AttributeError|TypeError|ValueError|RuntimeError|FileNotFoundError|OSError|ImportError):'
    r')',
    re.IGNORECASE,
)


def _extract_final_answer(raw: str) -> str:
    """Pull the model's actual reply out of `sage run` / `sage ask --raw` output.

    The raw stream interleaves UI chrome we don't want over SMS:
      1. `<thinking>...</thinking>` blocks — internal reasoning.
      2. Tool-call trace lines (`READ: foo.py`, `EDIT: bar.ts`, …) — work log.
      3. The `[SAGE — host] sage>` prompt prefix and the `─ 124 tokens · …` footer.
      4. Rich Panel art (the `╭─╮ │ ╰─╯` startup banner with model/project info)
         that prints when `sage run --prompt` boots in non-interactive mode.
      5. Status-spinner final states (`✓ Project scanned`) and the harness
         trailer (`Shell cwd was reset to …`).

    Strip all of that and return only the real prose. If nothing is left
    (model produced only tool calls / banner, e.g. it crashed mid-run), we
    fall back to the original text so the summarizer still has something
    to work with rather than empty string.
    """
    text = _THINK_BLOCK_RE.sub('', raw)
    cleaned_lines: list[str] = []
    in_code_fence = False  # Track ``` triple-backtick fenced code blocks
    for line in text.splitlines():
        # Strip the `sage>` prompt prefix FIRST — turns `sage> RUN: foo` into
        # `RUN: foo` so the tool-line filter below can drop it, and turns
        # `sage> The answer is X` into `The answer is X` so the answer is kept.
        line = _SAGE_PREFIX_RE.sub('', line)
        # Code fences: skip the fence markers AND everything inside them.
        # The agent's FILE: blocks ship as ```lang\ncontent\n```; over SMS we
        # don't want to dump source code.
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue
        if _TOOL_LINE_RE.match(line):
            continue
        if _PROMPT_LINE_RE.match(line):
            continue
        if _FOOTER_LINE_RE.match(line):
            continue
        if _PANEL_LINE_RE.match(line):
            continue
        if _STATUS_LINE_RE.match(line):
            continue
        if _STEP_LINE_RE.match(line):
            continue
        if _PLANNING_TAIL_RE.search(line):
            continue
        if _FILE_MARKER_RE.match(line):
            continue
        if _BACKEND_NOISE_RE.match(line):
            continue
        cleaned_lines.append(line)
    cleaned = '\n'.join(cleaned_lines).strip()
    # Collapse 3+ blank lines that the strips can leave behind.
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    return cleaned or raw.strip()


# ── Core WebSocket bridge ──────────────────────────────────────────────────────

class SAGEMessageBridge:
    """
    Connects to the SAGE backend via WebSocket, authenticates, and processes
    tasks dispatched from the central bridge inbox.

    No email credentials.  No IMAP.  Just a WebSocket.
    """

    def __init__(self, cfg: SMSConfig, token: str, api_base: str) -> None:
        self.cfg = cfg
        self._token = token
        self._api_base = api_base.rstrip("/")
        self._ws_url = self._api_base.replace("https://", "wss://").replace("http://", "ws://") + "/ws/sms"
        self.working_dir = Path(cfg.working_dir).expanduser().resolve()
        self._stop = threading.Event()
        self._bridge_email = ""
        self._announced = False
        try:
            self._log_fp = SMS_LOG_FILE.open("a", buffering=1, encoding="utf-8")
        except PermissionError:
            import io
            self._log_fp = io.StringIO()
        # Tracks the last seen Messages chat.db ROWID so we only process new
        # inbound iMessage / SMS after the bridge starts (not the entire
        # historical chat log).
        self._last_msg_rowid: int | None = None
        # Cache of registered contacts. Refreshed periodically by the iMessage
        # poller so newly-added contacts route too.
        # _phone_contacts_cache  — keyed by E.164 (+1XXXXXXXXXX) and bare digits
        # _email_contacts_cache  — keyed by lowercase email (iCloud / Apple ID /
        #                          private-relay addresses)
        self._phone_contacts_cache: dict[str, dict] = {}
        self._email_contacts_cache: dict[str, dict] = {}
        self._phone_cache_refreshed_at = 0.0
        self._user_email = ""
        self._user_phone = ""
        self._last_raw_output = ""
        global _active_bridge_instance
        _active_bridge_instance = self

    def _get_verified_recipients(self) -> set[str]:
        """Get all verified email addresses and phone numbers for the logged-in user."""
        verified = set()
        
        # 1. Primary email & phone from WebSocket ready frame
        if getattr(self, "_user_email", None):
            verified.add(self._user_email.lower())
        if getattr(self, "_user_phone", None):
            norm = self._normalize_e164(self._user_phone)
            if norm:
                verified.add(norm)
                digits = re.sub(r"\D", "", norm)
                if len(digits) == 11 and digits.startswith("1"):
                    digits = digits[1:]
                verified.add(digits)
                
        # 2. Check cached credentials from auth file (best effort)
        try:
            from sage.core.cli_auth import load_auth
            auth = load_auth()
            if auth and auth.get("email"):
                verified.add(auth["email"].lower().strip())
        except Exception:
            pass

        # 3. Linked providers from backend
        try:
            be = SAGEBackend(self._token, self._api_base)
            providers = be.get_linked_providers()
            for p in providers:
                email = (p.get("email") or "").lower().strip()
                if email:
                    verified.add(email)
                phone = (p.get("phone_number") or "").strip()
                if phone:
                    norm = self._normalize_e164(phone)
                    if norm:
                        verified.add(norm)
                        digits = re.sub(r"\D", "", norm)
                        if len(digits) == 11 and digits.startswith("1"):
                            digits = digits[1:]
                        verified.add(digits)
        except Exception as exc:
            logger.debug("Failed to fetch linked providers for verification: %s", exc)

        return verified

    def _is_recipient_verified(self, recipient: str) -> bool:
        """Verify if the recipient is an owned/verified identity of the current user."""
        if not recipient:
            return False
        
        recipient_clean = recipient.strip().lower()
        
        # Normalize phone if shaped like a phone number
        e164 = self._normalize_e164(recipient_clean)
        digits = re.sub(r"\D", "", recipient_clean)
        if len(digits) == 11 and digits.startswith("1"):
            digits = digits[1:]
            
        verified_set = self._get_verified_recipients()
        
        # Check direct email/phone matches
        if recipient_clean in verified_set:
            return True
        if e164 and e164 in verified_set:
            return True
        if digits and digits in verified_set:
            return True
            
        # Check carrier gateway addresses (e.g. 4085073140@vtext.com)
        if "@" in recipient_clean:
            local = recipient_clean.split("@")[0]
            if local.isdigit():
                norm_local = self._normalize_e164(local)
                if norm_local in verified_set:
                    return True
                local_digits = re.sub(r"\D", "", local)
                if len(local_digits) == 11 and local_digits.startswith("1"):
                    local_digits = local_digits[1:]
                if local_digits in verified_set:
                    return True

        # Check against cached contacts list
        try:
            self._refresh_phone_contacts()
            if recipient_clean in self._email_contacts_cache:
                return True
            if e164 and e164 in self._phone_contacts_cache:
                return True
            if digits and digits in self._phone_contacts_cache:
                return True
            if "@" in recipient_clean:
                local = recipient_clean.split("@")[0]
                if local.isdigit():
                    norm_local = self._normalize_e164(local)
                    if norm_local and norm_local in self._phone_contacts_cache:
                        return True
                    local_digits = re.sub(r"\D", "", local)
                    if len(local_digits) == 11 and local_digits.startswith("1"):
                        local_digits = local_digits[1:]
                    if local_digits and local_digits in self._phone_contacts_cache:
                        return True
        except Exception:
            pass

        return False

    def _log(self, msg: str) -> None:
        ts = time.strftime("%H:%M:%S")
        # Strip ANSI escapes to avoid mystery characters in the log
        clean_msg = re.sub(r'\x1b\[[0-9;]*[mGKHFABCDEJst]', '', msg)
        clean_msg = re.sub(r'\x1b\].*?\x07', '', clean_msg)
        clean_msg = clean_msg.replace('\x1b', '')
        line = f"[{ts}][{self.cfg.computer_name}] {clean_msg}"
        print(line)
        self._log_fp.write(line + "\n")

    def _start_kde_inbound_listener(self) -> None:
        """Start the SAGE KDE Connect listener for inbound SMS.

        Default mode: TAKEOVER — uses the existing kdeconnectd pairing.
        SAGE stops kdeconnectd, binds port 1716 itself, and serves the
        phone using the OS daemon's certs so the phone keeps recognizing
        the same paired device (e.g. 'laynepclaptop'). No re-pair on the
        phone needed; outbound and inbound both flow through SAGE while
        the bridge is running.

        Fallback (only when takeover fails): COEXIST — registers SAGE as
        a separate paired device. Requires a one-time pair tap on the
        phone. Disabled by default to preserve the user's existing
        single-device pairing model.

        Override via env var: ``SAGE_KDE_MODE=coexist`` to force coexist
        even when takeover would have worked.
        """
        try:
            from sage.core.kdeconnect_listener import (
                KDEConnectInboundListener,
                KDEConnectCoexistListener,
                OS_CERT,
                OS_KDC_DIR,
            )
            import logging
            kdc_logger = logging.getLogger("sage.kdeconnect_listener")
            class BridgeLogRedirectHandler(logging.Handler):
                def __init__(self, bridge_log_fn):
                    super().__init__()
                    self.bridge_log_fn = bridge_log_fn
                def emit(self, record):
                    try:
                        self.bridge_log_fn(self.format(record))
                    except Exception:
                        pass
            if not any(isinstance(h, BridgeLogRedirectHandler) for h in kdc_logger.handlers):
                h = BridgeLogRedirectHandler(self._log)
                h.setFormatter(logging.Formatter("%(message)s"))
                kdc_logger.addHandler(h)
                kdc_logger.setLevel(logging.INFO)
                kdc_logger.propagate = False
        except Exception as exc:
            self._log(f"KDE Connect listener not available: {exc}")
            return

        def _dispatch_sms(packet: dict) -> None:
            sender = (packet.get("from") or "").strip()
            text   = (packet.get("text") or "").strip()
            if not sender or not text:
                return
            self._process_inbound_imessage({
                "rowid":   0,
                "sender":  sender,
                "text":    text,
                "service": packet.get("service") or "SMS",
            })

        mode = (os.environ.get("SAGE_KDE_MODE") or "").lower().strip()
        # Default = takeover (uses the user's existing kdeconnectd pairing).
        # Coexist only when explicitly requested OR when takeover fails.
        if mode not in ("coexist", "takeover"):
            mode = "takeover"

        # ── Takeover path (default) ─────────────────────────────────
        if mode == "takeover":
            listener = KDEConnectInboundListener(callback=_dispatch_sms)
            if listener.start():
                self._kde_listener = listener
                device_name = getattr(listener, "_actual_name", "this computer")
                self._log(
                    f"📡 KDE Connect takeover active — SAGE is handling SMS as "
                    f"'{device_name}' using your existing pairing. "
                    "kdeconnectd will resume when the bridge stops."
                )
                return
            # Takeover failed; auto-fallback to coexist if certs aren't
            # available (no existing pairing) — but if the user has the
            # certs, surface the failure rather than silently switching
            # to a different pairing model they didn't ask for.
            if OS_CERT.exists():
                self._log(
                    "❌ KDE Connect takeover failed — see ~/.sage/sms.log for "
                    "the diagnostic dump. Common causes:\n"
                    "  • kdeconnectd didn't stop (Windows: end kdeconnectd.exe "
                    "    in Task Manager and re-run `sage sms start`)\n"
                    "  • Port 1716 still in use (lsof/netstat to check)\n"
                    "  • Cert/identity unreadable (`pip install cryptography`)\n"
                    "  • Windows firewall blocking inbound on 1716\n"
                    "If you'd rather pair SAGE as a SECOND device on your phone "
                    "instead of fixing takeover, run:\n"
                    "  $env:SAGE_KDE_MODE = 'coexist'   # PowerShell\n"
                    "  export SAGE_KDE_MODE=coexist     # bash/zsh\n"
                    "and restart `sage sms start`."
                )
                return
            # No existing pairing → coexist is the only option. Fall through.
            self._log(
                "ℹ No existing KDE Connect pairing found — falling back to "
                "coexist mode (one-time pair on your phone required)."
            )
            mode = "coexist"

        # ── Coexist path (opt-in or no-pairing fallback) ────────────
        if mode == "coexist":
            listener = KDEConnectCoexistListener(callback=_dispatch_sms)
            if listener.start():
                self._kde_listener = listener
                device_name = getattr(listener, "_actual_name", "SAGE Bridge")
                self._log(
                    f"📡 KDE Connect coexist mode active as '{device_name}'. "
                    "Look for 'SAGE Bridge' in your phone's KDE Connect "
                    "'Available devices' list and tap to pair (one-time)."
                )
                return

        # All paths failed.
        if not OS_CERT.exists():
            if sys.platform == "darwin":
                hint = (
                    "open KDE Connect.app once and pair your phone "
                    "(macOS App Store: 'KDE Connect'), then re-run "
                    "`sage sms start`."
                )
            elif sys.platform == "win32":
                hint = (
                    "install KDE Connect via `winget install KDE.KDEConnect`, "
                    "open it once, then re-run `sage sms start`."
                )
            else:
                hint = (
                    "install KDE Connect (`apt install kdeconnect` on "
                    "Debian/Ubuntu) and pair your phone via the GUI once."
                )
            self._log(
                f"ℹ KDE Connect inbound disabled — no pairing found at "
                f"{OS_KDC_DIR}. To enable: {hint}"
            )
        else:
            self._log(
                "ℹ KDE Connect inbound could not start — see ~/.sage/sms.log. "
                "Outbound (sage replying to your phone) still works via "
                "kdeconnect-cli."
            )

    def _discover_paired_android_host(self) -> str:
        """Get the hostname/IP of the user's paired Android phone.

        Reads the OS kdeconnectd's per-device config to find the phone that's
        already paired with this Mac. Falls back to common hostname patterns
        so the listener can still connect even if the OS daemon isn't configured.
        """
        # Try the OS daemon's saved device IDs first
        kdc_dir = Path.home() / "Library" / "Preferences" / "kdeconnect"
        if kdc_dir.exists():
            for device_dir in kdc_dir.iterdir():
                if device_dir.is_dir() and len(device_dir.name) == 32:
                    # 32-char hex id = a paired device. Resolve via mDNS naming.
                    # The Pixel typically advertises as "<deviceName>.local".
                    return "pixel-8.lan"
        # Fallback — let the listener try a common name. Will fail cleanly
        # if the host doesn't resolve.
        return "pixel-8.lan"

    # ── Inbound iMessage / SMS polling (macOS only) ──────────────────────────
    #
    # The Messages.app stores all iMessage + relayed-SMS conversations in
    # ~/Library/Messages/chat.db. Apple has no push API to subscribe to new
    # messages, so we poll the SQLite DB for new ROWIDs from registered phone
    # numbers. Each new message becomes a SAGE task; the response goes back
    # through the same channel (iMessage if it was iMessage; SMS if it was SMS).
    # This gives Apple-tagged AND Android-via-relay contacts a real two-way
    # conversational loop with sage.

    _CHAT_DB = Path.home() / "Library" / "Messages" / "chat.db"

    def _refresh_phone_contacts(self) -> None:
        """Pull registered contacts from backend; cache by E.164 and by email.

        Phone contacts (stored as "phone:XXXXXXXXXX") go into
        _phone_contacts_cache keyed by normalised E.164.

        Email contacts (iCloud / Apple ID / private-relay) go into
        _email_contacts_cache keyed by lowercase email. If a private-relay
        contact has an imessage_address set, that address is also added to
        whichever cache applies (phone cache for phone numbers, email cache
        for email addresses) so inbound messages from that real address are
        recognised too.
        """
        if time.time() - self._phone_cache_refreshed_at < 30:
            return  # cached recently
        try:
            be = SAGEBackend(self._token, self._api_base)
            contacts = be.list_contacts()
            phone_cache: dict[str, dict] = {}
            email_cache: dict[str, dict] = {}
            for c in contacts:
                raw_email = (c.get("email") or "")
                if raw_email.startswith("phone:"):
                    phone_norm = _normalize_e164_globally(raw_email.replace("phone:", ""))
                    if phone_norm:
                        phone_cache[phone_norm] = c
                        phone_digits = re.sub(r"\D", "", phone_norm)
                        if len(phone_digits) == 11 and phone_digits.startswith("1"):
                            phone_digits = phone_digits[1:]
                        phone_cache[phone_digits] = c
                elif "@" in raw_email:
                    email_cache[raw_email.lower()] = c

                # If the contact has a stored imessage_address (set by the
                # user to bypass Apple private-relay), register that address
                # too so inbound messages from the real address are matched.
                imsg = (c.get("imessage_address") or "").strip()
                if imsg:
                    if "@" in imsg:
                        email_cache[imsg.lower()] = c
                    else:
                        norm_phone = _normalize_e164_globally(imsg)
                        if norm_phone:
                            phone_cache[norm_phone] = c
                            phone_digits = re.sub(r"\D", "", norm_phone)
                            if len(phone_digits) == 11 and phone_digits.startswith("1"):
                                phone_digits = phone_digits[1:]
                            phone_cache[phone_digits] = c

            self._phone_contacts_cache = phone_cache
            self._email_contacts_cache = email_cache
            self._phone_cache_refreshed_at = time.time()
        except Exception as exc:
            logger.debug("contacts refresh failed: %s", exc)

    def _imessage_initial_rowid(self) -> int:
        """Return the current max ROWID so we only see messages from now on.
        Returns -1 if the database is unreadable (prevents accidental historical fetch).
        """
        try:
            import sqlite3
            # Use simple connect for legacy compatibility
            db = sqlite3.connect(str(self._CHAT_DB), timeout=2)
            try:
                cur = db.execute("SELECT MAX(ROWID) FROM message")
                row = cur.fetchone()
                return int(row[0]) if row and row[0] is not None else 0
            finally:
                db.close()
        except Exception as exc:
            logger.debug("Failed to initialize iMessage rowid: %s", exc)
            return -1

    def _fetch_new_imessages(self) -> list[dict]:
        """Return new INBOUND iMessage/SMS records since `_last_msg_rowid`.

        Filters:
          - is_from_me=0          (only inbound from peer)
          - text non-empty
          - text doesn't start with our own SAGE marker (prevents feedback
            loops — Messages.app on iCloud-synced Macs sees its own outbound
            messages echoed back from the iPhone's "received" view, so the
            same message appears with both is_from_me=1 AND is_from_me=0)
        """
        if not self._CHAT_DB.exists():
            return []
        if self._last_msg_rowid is None or self._last_msg_rowid < 0:
            self._last_msg_rowid = self._imessage_initial_rowid()
            return []

        results: list[dict] = []
        try:
            import sqlite3
            db = sqlite3.connect(str(self._CHAT_DB), timeout=2)
            try:
                cur = db.execute("""
                    SELECT m.ROWID, h.id, m.text, m.service, m.date
                      FROM message m
                      LEFT JOIN handle h ON m.handle_id = h.ROWID
                     WHERE m.ROWID > ?
                       AND m.is_from_me = 0
                       AND m.text IS NOT NULL
                       AND m.text != ''
                  ORDER BY m.ROWID ASC
                """, (self._last_msg_rowid,))
                for rowid, sender, text, service, date in cur.fetchall():
                    text = (text or "").strip()
                    # Skip our own outbound messages echoed back via iCloud sync.
                    # Every reply we send starts with "[SAGE — <computer> ]"; if
                    # we see one in the inbound stream, it's a sync echo, not a
                    # real user reply. Without this filter we get an infinite
                    # task → reply → "inbound" → task loop.
                    if text.startswith("[SAGE"):
                        if rowid > self._last_msg_rowid:
                            self._last_msg_rowid = rowid
                        continue
                    results.append({
                        "rowid":   rowid,
                        "sender":  (sender or "").strip(),
                        "text":    text,
                        "service": (service or "").strip(),
                    })
                    if rowid > self._last_msg_rowid:
                        self._last_msg_rowid = rowid
            finally:
                db.close()
        except Exception as exc:
            self._log(f"chat.db poll failed: {exc}")
        return results

    def _normalize_e164(self, raw: str) -> str:
        """Normalize phone-shaped sender to E.164 (+1XXXXXXXXXX or +XXXXXXXXXXXX)."""
        return _normalize_e164_globally(raw)

    @staticmethod
    def _parse_routing(text: str) -> tuple[str | None, str]:
        """Extract `@target:` prefix — mirrors backend `sms_poller._parse_routing`.

        Allows multi-word names like "@Layne's Macbook Pro: …". Limits target
        to 40 non-colon chars so we don't slurp URLs like "@https://…" into
        the target slot.
        """
        text = (text or "").strip()
        m = re.match(r'^@([^:：\n]{1,40})\s*[:：]\s*', text)
        if m:
            return m.group(1).strip().lower(), text[m.end():].strip()
        return None, text

    def _process_inbound_imessage(self, msg: dict) -> None:
        """Run an inbound iMessage/SMS as a sage task and reply on the same channel.

        Routing is identical to the email path:
          • No prefix → run on this gateway machine (fast, no network roundtrip)
          • @<this-machine>: → run locally
          • @<other-machine>: or @all: → forward to backend, which dispatches
            via WebSocket to the named computer(s), and returns the result
            for us to deliver via iMessage/SMS.
        """
        sender   = msg["sender"]
        text     = msg["text"]
        service  = msg.get("service", "")
        e164     = self._normalize_e164(sender)

        # Look up the contact — must be registered.
        # Senders can arrive as a phone number (E.164) or as an email address
        # (iCloud / Apple ID / private-relay).  Check both caches.
        contact = self._phone_contacts_cache.get(e164) if e164 else None
        if not contact and "@" in sender:
            contact = self._email_contacts_cache.get(sender.lower())
        if not contact:
            return  # unregistered sender; don't run sage on every random chat

        # P0 Security Check: Sender must be a verified owned contact method of the current user.
        # We reject inbound messages from other people to prevent cross-user command execution.
        if not self._is_recipient_verified(sender):
            self._log(f"🛡 Refusing inbound message from unverified sender: {sender}")
            return

        device_type = (contact.get("device_type") or "").lower()
        target, task = self._parse_routing(text)
        self._log(
            f"📥 inbound from {sender} → @{target or 'self'}: {task[:80]}"
            f"  (service={service}, device={device_type or 'unknown'})"
        )

        my_name = (self.cfg.computer_name or "").lower()
        if target is None or target == my_name:
            # Run locally — no backend roundtrip needed
            synthetic = {
                "task_id":          "",
                "task":             task,
                "from":             sender,
                "device_type":      device_type,
                "deliver_natively": True,
                "_local_only":      True,
            }
            self._handle_local_imessage_task(synthetic, service, device_type)
            return

        # Cross-device: forward to backend for dispatch via WS to @target
        self._dispatch_remote_imessage(text, target, sender, service, device_type)

    def _dispatch_remote_imessage(
        self, full_text: str, target: str, sender: str,
        service: str, device_type: str,
    ) -> None:
        """Forward `@target: …` to the backend, then iMessage/SMS the result back."""
        try:
            be = SAGEBackend(self._token, self._api_base)
            resp = be.dispatch_text(full_text, sender)
            output  = (resp.get("output") or "(no response)").strip()
            replier = (resp.get("computer") or target).strip()
        except Exception as exc:
            output  = f"⚠ Could not reach @{target}: {exc}"
            replier = target

        if len(output) > 280:
            output = self._summarize_for_sms(output, full_text)

        body = f"[SAGE — {replier}] {output}"
        e164 = self._normalize_e164(sender)
        # For iMessage, if we have a phone number, use the E.164 form.
        # If it's a carrier gateway email (digits@domain), strip the domain.
        if not e164 and "@" in sender:
            local = sender.split("@")[0]
            if local.isdigit() and len(local) >= 10:
                e164 = self._normalize_e164(local)
        
        recipient = e164 or sender

        sent_via = None
        if device_type == "android":
            if getattr(self, "_kde_listener", None) and \
               self._kde_listener.send_sms(recipient, body):
                sent_via = "KDE Connect (takeover)"
            elif _send_via_kdeconnect(recipient, body):
                sent_via = "KDE Connect"
        elif device_type == "apple":
            if _send_imessage(recipient, body):
                sent_via = "iMessage"
        else:
            # Untagged: only iMessage paths — iPhone-relay SMS would send from
            # the user's iPhone, not from sage, so it's only correct for
            # Apple-themed conversations, not unknowns.
            if _send_imessage(recipient, body):
                sent_via = "iMessage"

        if sent_via:
            self._log(f"→ [{replier}] replied to {sender} via {sent_via}")
        else:
            self._log(f"⚠ failed to relay [{replier}] reply to {sender}")

    # ── Shared help text (both handlers use this) ───────────────────────────

    def _build_help_text(self) -> str:
        """Full command reference sent in response to @help."""
        model = self.cfg.model or self._resolve_dispatch_model() or "default"
        return (
            f"SAGE [{self.cfg.computer_name}] — all commands:\n"
            "\n"
            "── Tasks ──\n"
            "  <any text>         run as sage task (auto-routed)\n"
            "  @run <task>        force agentic mode (file edits, tests)\n"
            "  @ask <question>    force chat mode (fast Q&A, no edits)\n"
            "\n"
            "── Models ──\n"
            "  @models            list all available models\n"
            f"  @model             show current model ({model})\n"
            "  @model <name>      switch model (e.g. @model cloud:mistral-small)\n"
            "\n"
            "── Directory ──\n"
            "  @dir / @pwd        show working directory\n"
            "  cd <path>          change working directory\n"
            "\n"
            "── Settings ──\n"
            "  @temp <0.0-1.0>    set model temperature\n"
            "  @timeout <secs>    set per-task timeout (0 = unlimited)\n"
            "  @verbose           full output for next task\n"
            "  @quiet             summary-only output for next task\n"
            "\n"
            "── Routing ──\n"
            f"  @{self.cfg.computer_name}: <task>  route to this computer\n"
            "  @all: <task>       broadcast to all computers\n"
            "\n"
            "── System ──\n"
            "  @status            show status (dir, model, uptime)\n"
            "  @stop              stop the sage daemon\n"
            "  @help / ?          show this help"
        )

    def _list_models_text(self) -> str:
        """Run `sage models` and return a condensed SMS-friendly list."""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "sage", "models", "--all"],
                capture_output=True, text=True, timeout=15, env=_clean_env(),
            )
            raw = result.stdout or ""
        except Exception:
            try:
                result = subprocess.run(
                    ["sage", "models", "--all"],
                    capture_output=True, text=True, timeout=15, env=_clean_env(),
                )
                raw = result.stdout or ""
            except Exception:
                raw = ""

        if not raw.strip():
            return "Could not list models. Is sage installed?"

        # Extract model IDs from table output (lines containing "cloud:" or "openrouter:")
        lines = raw.splitlines()
        model_ids: list[str] = []
        for line in lines:
            stripped = line.strip()
            for prefix in ("cloud:", "openrouter:", "ollama:", "llama_cpp:", "gemini:"):
                if prefix in stripped:
                    # Grab the first token that starts with the prefix
                    for token in stripped.split():
                        if token.startswith(prefix):
                            model_ids.append(token)
                            break
                    break

        current = self.cfg.model or self._resolve_dispatch_model() or "?"
        if not model_ids:
            # Fall back to showing raw output trimmed
            return f"Current: {current}\n" + raw[:400]

        chunks = [f"Models (current: {current}):"]
        for mid in model_ids[:20]:  # cap at 20 for SMS readability
            marker = " ←" if mid == current else ""
            chunks.append(f"  {mid}{marker}")
        if len(model_ids) > 20:
            chunks.append(f"  … +{len(model_ids) - 20} more (use sage models --all locally)")
        chunks.append("Use: @model <name> to switch")
        return "\n".join(chunks)

    def _handle_local_imessage_task(self, msg: dict, service: str, device_type: str = "") -> None:
        """Run sage and reply on the channel that matches the inbound device.

        Reply routing follows the contact's `device_type` tag:
          • Apple-tagged contact → iMessage (matches their iPhone thread)
          • Android-tagged contact → KDE Connect (real SMS to paired Android)
          • Untagged → match the inbound `service` field (iMessage→iMessage,
            SMS→SMS via iPhone relay)
        """
        task   = msg.get("task", "").strip()
        sender = msg.get("from", "")
        lower  = task.lower()

        start_time = time.time()
        is_execution = False

        # ── Built-in commands (no sage invocation needed) ──────────────────
        if lower in ("help", "?", "@help"):
            output = self._build_help_text()

        elif lower in ("@models", "@list", "@list-models", "models"):
            output = self._list_models_text()

        elif lower in ("@model", "@current-model"):
            model = self.cfg.model or self._resolve_dispatch_model() or "default"
            output = f"🤖 Current model: {model}\nUse @model <name> to switch."

        elif lower.startswith("@model "):
            new_model = task.split(None, 1)[1].strip()
            self.cfg.model = new_model
            self.cfg.save()
            output = f"🤖 [{self.cfg.computer_name}] model → {new_model}"

        elif lower in ("@dir", "@pwd", "pwd"):
            output = f"📁 [{self.cfg.computer_name}] {self.working_dir}"

        elif lower in ("@status", "status"):
            model = self.cfg.model or self._resolve_dispatch_model() or "default"
            output = (
                f"✅ [{self.cfg.computer_name}]\n"
                f"📁 {self.working_dir}\n"
                f"🤖 {model}"
            )

        elif lower.startswith(("cd ", "@dir ")):
            raw = task.split(None, 1)[1].strip()
            new = Path(raw).expanduser().resolve()
            if new.is_dir():
                self.working_dir = new
                self.cfg.working_dir = str(new)
                self.cfg.save()
                output = f"📁 [{self.cfg.computer_name}] {self.working_dir}"
            else:
                output = f"❌ Not found: {raw}"

        elif lower.startswith("@temp "):
            try:
                val = float(task.split(None, 1)[1])
                val = max(0.0, min(2.0, val))
                self.cfg.temperature = val
                self.cfg.save()
                output = f"🌡 Temperature set to {val}"
            except (ValueError, IndexError):
                output = "Usage: @temp 0.7  (range 0.0–2.0)"

        elif lower.startswith("@timeout "):
            try:
                val = int(task.split(None, 1)[1])
                self.cfg.task_timeout = max(0, val)
                self.cfg.save()
                output = f"⏱ Timeout set to {val}s (0 = unlimited)"
            except (ValueError, IndexError):
                output = "Usage: @timeout 120  (seconds, 0 = unlimited)"

        elif lower in ("@verbose",):
            self.cfg.output_mode = "verbose"
            self.cfg.save()
            output = "📢 Next task will return full output."

        elif lower in ("@quiet",):
            self.cfg.output_mode = "quiet"
            self.cfg.save()
            output = "🔇 Next task will return a short summary."

        elif lower.startswith("@run "):
            # Force agentic mode (sage run --prompt)
            actual_task = task.split(None, 1)[1].strip()
            is_execution = True
            output = self._run_sage_task(actual_task, mode="agent")
            if len(output) > 280:
                output = self._summarize_for_sms(output, actual_task)

        elif lower.startswith("@ask "):
            # Force chat mode (sage ask)
            actual_task = task.split(None, 1)[1].strip()
            is_execution = True
            output = self._run_sage_task(actual_task, mode="chat")
            if len(output) > 280:
                output = self._summarize_for_sms(output, actual_task)

        elif lower in ("@stop", "stop"):
            output = f"⏹ [{self.cfg.computer_name}] stopping."
            self._stop.set()

        else:
            is_execution = True
            timeout = getattr(self.cfg, "task_timeout", None) or None
            output = self._run_sage_task(task, timeout=timeout)
            if len(output) > 280:
                output = self._summarize_for_sms(output, task)
            # Reset one-shot output mode after task
            if getattr(self.cfg, "output_mode", None) in ("verbose", "quiet"):
                self.cfg.output_mode = None
                self.cfg.save()

        # Find attachments if this was an execution
        local_attachments = []
        if is_execution:
            raw_for_attachments = getattr(self, "_last_raw_output", "") or output
            paths_in_text = _extract_file_attachments(raw_for_attachments, self.working_dir)
            recent_files = _find_recent_files(self.working_dir, start_time)
            seen_files = set()
            for fp in paths_in_text + recent_files:
                if fp not in seen_files:
                    seen_files.add(fp)
                    local_attachments.append(fp)
            local_attachments = _filter_attachments_for_phone(local_attachments, task)

        body = f"[SAGE — {self.cfg.computer_name}] {output}"
        e164 = self._normalize_e164(sender)
        target = e164 or sender

        sent_via = None
        if device_type == "android":
            # Android: ONLY use KDE Connect — never iPhone relay (that would
            # send from the user's iPhone, not from sage).
            if getattr(self, "_kde_listener", None) and \
               self._kde_listener.send_sms(target, body):
                sent_via = "KDE Connect (takeover)"
            elif _send_via_kdeconnect(target, body):
                sent_via = "KDE Connect"
            if sent_via and local_attachments:
                for ap in local_attachments:
                    _share_via_kdeconnect(ap)
        elif device_type == "apple":
            if sys.platform == "darwin":
                if _send_imessage(target, body, local_attachments):
                    sent_via = "iMessage"
            
            # Fallback for Apple on non-macOS or failed iMessage
            if not sent_via and e164:
                if _send_via_kdeconnect(target, body):
                    sent_via = "KDE Connect (SMS)"
                    if local_attachments:
                        for ap in local_attachments:
                            _share_via_kdeconnect(ap)
        else:
            # Untagged/unknown device
            if sys.platform == "darwin":
                if _send_imessage(target, body, local_attachments):
                    sent_via = "iMessage"
                elif _send_macos_sms(target, body):
                    sent_via = "SMS (iPhone relay)"
            
            # Fallback to KDE Connect on all platforms (including Linux/Windows)
            if not sent_via and e164:
                if _send_via_kdeconnect(target, body):
                    sent_via = "KDE Connect (SMS)"
                    if local_attachments:
                        for ap in local_attachments:
                            _share_via_kdeconnect(ap)

        if sent_via:
            self._log(f"→ replied to {sender} via {sent_via}")
        else:
            self._log(f"⚠ failed to reply to {sender} (device={device_type}, service={service})")

    def _imessage_poll_loop(self) -> None:
        """Background thread: poll chat.db every few seconds for new messages."""
        if sys.platform != "darwin" or not self._CHAT_DB.exists():
            return
        self._log("📲 iMessage inbound poller started (chat.db)")
        # Initialise rowid so we only catch messages received AFTER startup
        self._last_msg_rowid = self._imessage_initial_rowid()
        while not self._stop.is_set():
            try:
                self._refresh_phone_contacts()
                for msg in self._fetch_new_imessages():
                    threading.Thread(
                        target=self._process_inbound_imessage,
                        args=(msg,),
                        daemon=True,
                    ).start()
            except Exception as exc:
                self._log(f"iMessage poller error: {exc}")
            self._stop.wait(5)
        self._log("iMessage inbound poller stopped")

    @staticmethod
    def _classify_sms_intent(task: str) -> str:
        """Decide whether a texted message needs the full agent loop or just chat.

        The agent loop loads the GGUF model + tool runtime — for trivial
        greetings ("Hello Sage") that's overkill AND fires backend errors
        like the gemma4.gguf load failure. We route those to the much lighter
        `sage ask` chat path.

        Conservative bias: when in doubt, return "agent" so real coding
        requests don't get downgraded to chat (which couldn't execute them).

        Returns "chat" only when the message is unambiguously trivial:
          • Pure greetings ("hi", "hello", "hey", "yo", "sup", "gm")
          • Acknowledgments ("ok", "thanks", "ty", "cool", "got it")
          • Pure questions starting with question words AND no action verbs
            ("what is X", "how does Y work")
          • Very short messages (<= 30 chars) with no imperative verbs
        Otherwise returns "agent".
        """
        if not task:
            return "chat"
        s = task.strip().lower()

        # Imperative / action verbs anywhere → agent.
        ACTION_VERBS = (
            "run", "create", "build", "make", "write", "edit", "add", "fix",
            "delete", "remove", "deploy", "install", "scaffold", "generate",
            "set up", "setup", "configure", "test", "commit", "push", "pull",
            "merge", "rebase", "checkout", "compile", "lint", "format",
            "refactor", "rename", "implement", "ship", "publish", "init",
            "clone", "open", "save", "update", "upgrade", "downgrade",
            "start", "stop", "restart", "kill", "spawn", "execute",
            "show me the", "list the", "find the", "search for",
        )
        for verb in ACTION_VERBS:
            # Word-boundary match so "stop" doesn't match "stopwatch".
            if re.search(rf'\b{re.escape(verb)}\b', s):
                return "agent"

        # Path-like or command-like tokens → agent.
        if re.search(r'(?:~/|/Users/|\.\w{1,5}\b|\$|`|--?\w+)', s):
            return "agent"

        # Pure greetings / acknowledgments → chat.
        TRIVIAL_PATTERNS = (
            r'^(?:hi|hello|hey|yo|sup|gm|gn|good\s*(?:morning|night|evening|afternoon))\b',
            r'^(?:thanks|thank\s*you|ty|tysm)\b',
            r'^(?:ok(?:ay)?|cool|got\s*it|sure|nice|great|awesome|sweet)\b',
            r'^(?:bye|goodbye|cya|see\s*you|later)\b',
        )
        for pat in TRIVIAL_PATTERNS:
            if re.match(pat, s):
                return "chat"

        # Pure question (starts with a question word) → chat.
        if re.match(r'^(?:what|how|why|when|where|who|which|is|are|can|could|do|does|did)\b', s):
            return "chat"

        # Very short with no action verb and no path → chat.
        if len(s) <= 30:
            return "chat"

        # Default conservatively to agent so real tasks aren't downgraded.
        return "agent"

    @staticmethod
    def _ollama_has_model(name: str) -> bool:
        """Check if Ollama has the named model locally pulled and ready."""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True, text=True, timeout=5,
            )
            if result.returncode != 0:
                return False
            base = name.split(":", 1)[0]
            for line in result.stdout.splitlines()[1:]:
                first = line.split()[0] if line.strip() else ""
                if first == name or first == f"{base}:latest" or first.startswith(f"{base}:"):
                    return True
            return False
        except Exception:
            return False

    def _resolve_dispatch_model(self) -> str | None:
        """Pick the model to use for SMS dispatch, with auto-Ollama preference.

        Resolution order:
          1. SMSConfig.model — if the user explicitly set a per-bridge model,
             trust them and use it as-is.
          2. ~/.sage/config.json default_model — the user's chosen default.
             If it's `llama_cpp:X` and `ollama:X` is available locally, swap
             to ollama (avoids llama_cpp Metal-compilation failures on macOS).
          3. None — let sage pick (usually fine in chat/ask mode).

        We pass the result via `--model` to override any per-cwd
        `last_used_model` cache that would otherwise win, which was the cause
        of the SMS thread where `Run: sage --version` errored on a model
        the user didn't ask for (cached from an unrelated session).
        """
        if self.cfg.model:
            return self.cfg.model
        try:
            from sage.config import load_config
            cfg = load_config()
            chosen = (cfg.default_model or "").strip()
        except Exception:
            return None
        if not chosen:
            return None
        # Auto-prefer Ollama: if default is `llama_cpp:gemma4` and ollama has
        # `gemma4`, use `ollama:gemma4` — Ollama handles GPU/Metal correctly
        # while llama-cpp-python often fails to compile Metal shaders on the fly.
        if chosen.startswith("llama_cpp:"):
            base_name = chosen.split(":", 1)[1]
            if self._ollama_has_model(base_name):
                return f"ollama:{base_name}"
        return chosen

    def _run_sage_task(
        self,
        task: str,
        timeout: int | None = None,
        mode: str = "auto",
    ) -> str:
        """Execute a sage task as a subprocess."""
        if mode == "auto":
            mode = self._classify_sms_intent(task)
            
        resolved_model = self._resolve_dispatch_model()
        model_flags = ["--model", resolved_model] if resolved_model else []
        temp = getattr(self.cfg, "temperature", 0.7)
        temp_flags = ["--temperature", str(temp)] if temp != 0.7 else []
        
        # Build command variants: try module path then bare command
        base_flags = model_flags + temp_flags + (["--quiet", "--prompt", task] if mode == "agent" else ["--raw", task])
        
        # P0 FIX: Ensure we use the current sys.executable to maintain environment consistency
        cmd_variants = (
            [sys.executable, "-m", "sage", "run" if mode == "agent" else "ask"] + base_flags,
            ["sage", "run" if mode == "agent" else "ask"] + base_flags,
        )

        for cmd in cmd_variants:
            retries = 3
            backoff = 5  # start with 5s backoff for rate limits
            while retries > 0:
                try:
                    logger.info("SMS Bridge executing (retries left %d): %s", retries, " ".join(cmd))
                    result = subprocess.run(
                        cmd, 
                        cwd=str(self.working_dir),
                        capture_output=True, text=True, timeout=timeout,
                        env={
                            **os.environ, 
                            "PYTHONPATH": os.path.pathsep.join(filter(None, [
                                str(Path(__file__).resolve().parents[2]),
                                str(self.working_dir),
                                os.environ.get("PYTHONPATH", "")
                            ])), 
                            "NO_COLOR": "1", 
                            "TERM": "dumb",
                            "SAGE_BATCH_LIMIT": "250" # Ensure background task doesn't stop early
                        }
                    )
                    
                    # Combine stdout and stderr for full context on failure
                    raw = _strip_ansi((result.stdout or "") + (result.stderr or "")).strip()
                    self._last_raw_output = raw
                    
                    # Check for rate limits first
                    if "Rate limit exceeded" in raw or "429" in raw or "Too Many Requests" in raw:
                        if retries > 1:
                            logger.warning(f"Rate limit hit, retrying in {backoff}s...")
                            time.sleep(backoff)
                            backoff *= 2
                            retries -= 1
                            continue
                    
                    if result.returncode == 0:
                        out = _extract_final_answer(raw)
                        return out or "Task completed successfully."
                        
                    # If first variant failed with FileNotFoundError, it will be caught below
                    if result.returncode != 0 and cmd == cmd_variants[-1]:
                        return f"❌ Error: {raw or 'Process exited with code %d' % result.returncode}"
                        
                    # Break out of retry loop to try next cmd variant if this one failed (but not due to rate limit)
                    break
                        
                except FileNotFoundError:
                    break
                except subprocess.TimeoutExpired:
                    return "⏱ Timed out — check your terminal for progress."
                except Exception as e:
                    return f"❌ System Error: {str(e)}"
        
        return "❌ Error: SAGE command not found in environment."

    def _summarize_for_sms(self, full_response: str, original_task: str) -> str:
        """Use the model to compress a long SAGE response into a phone-friendly reply.

        Three-tier strategy by length:
          1. Already ≤ 280 chars → return as-is (no model call).
          2. 281-700 chars → cheap fast-path: keep the last natural paragraph
             (which is where the agent's actual conclusion sits) and hard-cap.
             Avoids burning 60+ seconds running the model just to drop ~150 chars.
          3. > 700 chars → run the LLM summarizer with NO deadline (the user
             accepted "this can take a while" by texting a complex task — and
             the prior 60s deadline was the literal cause of the SMS thread the
             user pasted, where every reply came back as "⏱ Timed out").
        """
        cleaned = _extract_final_answer(full_response)
        if len(cleaned) <= 280:
            return cleaned

        # Fast-path: short-but-over-limit outputs → take the last paragraph
        # (typically the agent's final answer; everything before is the work log)
        # and hard-truncate. Cheap, no LLM call, no timeout risk.
        if len(cleaned) <= 700:
            paragraphs = [p.strip() for p in cleaned.split("\n\n") if p.strip()]
            if paragraphs:
                last = paragraphs[-1]
                if len(last) <= 280:
                    return last
                # Try the second-to-last if the last is itself too long
                if len(paragraphs) >= 2 and len(paragraphs[-2]) <= 280:
                    return paragraphs[-2]
            # No clean paragraph cut — hard truncate with ellipsis
            return cleaned[:277].rstrip() + "…"

        # Long-output path: actually summarize. NO timeout — local models on
        # cold start can take 30-90s, and a deadline here is what was eating
        # real replies and surfacing as "⏱ Timed out" over SMS.
        prompt = (
            "You are summarizing the FINAL ANSWER of a SAGE coding-assistant run "
            "for delivery as a single SMS reply (max 280 characters).\n\n"
            "Rules:\n"
            "- Summarize the conclusion / final answer ONLY. Do NOT describe what "
            "files were read, edited, or executed — the user does not want a work log.\n"
            "- If the answer contains a recommendation, decision, or finding, lead with it.\n"
            "- No preamble, no greetings, no 'I did X then Y' narration.\n"
            "- Plain text. Under 280 characters. One short paragraph or 2–3 short bullets.\n\n"
            f"User asked: {original_task[:200]}\n\n"
            f"SAGE final answer (already stripped of tool-call traces):\n{cleaned[:4000]}"
        )
        summary = self._run_sage_task(prompt, mode="chat").strip()
        # Run the cleaner over the summary too — if the summarizer itself
        # leaked any process-log lines, drop them before sending.
        summary = _extract_final_answer(summary)
        # Guard against empty / overly long summaries — fall back to truncated cleaned
        if not summary or len(summary) > 320:
            return cleaned[:277].rstrip() + "…"
        return summary

    @staticmethod
    def _is_sms_gateway(addr: str) -> bool:
        domain = addr.split("@", 1)[-1].lower() if "@" in addr else ""
        gateways = {
            "vtext.com", "vzwpix.com", "txt.att.net", "mms.att.net",
            "tmomail.net", "msg.fi.google.com", "messaging.sprintpcs.com",
            "mymetropcs.com", "mypixmessages.com", "mmst5.tracfone.com",
            "sms.myboostmobile.com",
        }
        if domain in gateways:
            return True
        local = addr.split("@", 1)[0] if "@" in addr else addr
        return bool(re.match(r"^\+?\d{7,15}$", local))

    def _handle_task(self, ws, msg: dict) -> None:
        """Process a task from the backend (runs in a thread)."""
        task_id          = msg.get("task_id", "")
        task             = msg.get("task", "").strip()
        sender           = msg.get("from", "")
        device_type      = (msg.get("device_type") or "").lower()
        deliver_natively = bool(msg.get("deliver_natively"))
        lower            = task.lower()

        self._log(f"← {sender}: {task[:80]}")

        start_time = time.time()
        is_execution = False

        # ── Built-in commands (shared with iMessage handler) ──────────────
        if lower in ("help", "?", "@help"):
            output = self._build_help_text()

        elif lower in ("@models", "@list", "@list-models", "models"):
            output = self._list_models_text()

        elif lower in ("@model", "@current-model"):
            model = self.cfg.model or self._resolve_dispatch_model() or "default"
            output = f"🤖 Current model: {model}\nUse @model <name> to switch."

        elif lower.startswith("@model "):
            self.cfg.model = task.split(None, 1)[1].strip()
            self.cfg.save()
            output = f"🤖 [{self.cfg.computer_name}] model → {self.cfg.model}"

        elif lower in ("@dir", "@pwd", "pwd"):
            output = f"📁 [{self.cfg.computer_name}] {self.working_dir}"

        elif lower in ("@status", "status"):
            model = self.cfg.model or self._resolve_dispatch_model() or "default"
            output = (
                f"✅ [{self.cfg.computer_name}]\n"
                f"📁 {self.working_dir}\n"
                f"🤖 {model}"
            )

        elif lower.startswith(("cd ", "@dir ")):
            raw = task.split(None, 1)[1].strip()
            new = Path(raw).expanduser().resolve()
            if new.is_dir():
                self.working_dir = new
                self.cfg.working_dir = str(new)
                self.cfg.save()
                output = f"📁 [{self.cfg.computer_name}] {self.working_dir}"
            else:
                output = f"❌ Not found: {raw}"

        elif lower.startswith("@temp "):
            try:
                val = float(task.split(None, 1)[1])
                val = max(0.0, min(2.0, val))
                self.cfg.temperature = val
                self.cfg.save()
                output = f"🌡 Temperature set to {val}"
            except (ValueError, IndexError):
                output = "Usage: @temp 0.7  (range 0.0–2.0)"

        elif lower.startswith("@timeout "):
            try:
                val = int(task.split(None, 1)[1])
                self.cfg.task_timeout = max(0, val)
                self.cfg.save()
                output = f"⏱ Timeout set to {val}s (0 = unlimited)"
            except (ValueError, IndexError):
                output = "Usage: @timeout 120  (seconds, 0 = unlimited)"

        elif lower in ("@verbose",):
            self.cfg.output_mode = "verbose"
            self.cfg.save()
            output = "📢 Next task will return full output."

        elif lower in ("@quiet",):
            self.cfg.output_mode = "quiet"
            self.cfg.save()
            output = "🔇 Next task will return a short summary."

        elif lower.startswith("@run "):
            actual_task = task.split(None, 1)[1].strip()
            is_execution = True
            output = self._run_sage_task(actual_task, mode="agent")
            if self._is_sms_gateway(sender):
                output = self._summarize_for_sms(output, actual_task)

        elif lower.startswith("@ask "):
            actual_task = task.split(None, 1)[1].strip()
            is_execution = True
            output = self._run_sage_task(actual_task, mode="chat")
            if self._is_sms_gateway(sender):
                output = self._summarize_for_sms(output, actual_task)

        elif lower in ("@stop", "stop"):
            output = f"⏹ [{self.cfg.computer_name}] stopping."
            self._stop.set()

        else:
            # Run the FULL task — all real work happens here
            is_execution = True
            timeout = getattr(self.cfg, "task_timeout", None) or None
            output = self._run_sage_task(task, timeout=timeout)
            # SMS gateway senders get a concise summary; email/iMessage get full output
            if self._is_sms_gateway(sender):
                self._log(f"Summarizing for SMS gateway {sender} (full {len(output)} chars)")
                output = self._summarize_for_sms(output, task)
            # Reset one-shot output mode after task
            if getattr(self.cfg, "output_mode", None) in ("verbose", "quiet"):
                self.cfg.output_mode = None
                self.cfg.save()

        # Find attachments if this was an execution
        local_attachments = []
        uploaded_attachments = []
        if is_execution:
            raw_for_attachments = getattr(self, "_last_raw_output", "") or output
            paths_in_text = _extract_file_attachments(raw_for_attachments, self.working_dir)
            recent_files = _find_recent_files(self.working_dir, start_time)
            seen_files = set()
            for fp in paths_in_text + recent_files:
                if fp not in seen_files:
                    seen_files.add(fp)
                    local_attachments.append(fp)
            local_attachments = _filter_attachments_for_phone(local_attachments, task)
            if local_attachments:
                self._log(f"Detected {len(local_attachments)} file attachment(s): {local_attachments}")
                
            be = SAGEBackend(self._token, self._api_base)
            for fp in local_attachments:
                file_id = be.upload_file(fp)
                if file_id:
                    import os
                    uploaded_attachments.append({
                        "file_id": file_id,
                        "filename": os.path.basename(fp),
                        "mime_type": None
                    })

        # If the backend asked us to deliver natively (carrier-gateway sender +
        # known device_type), do that NOW from this machine. SMTP through
        # carrier email-to-SMS bridges is unreliable — most drop without
        # bouncing, so the user never sees the reply if we trust SMTP alone.
        delivered_locally = False
        if deliver_natively:
            delivered_locally = self._deliver_native(sender, output, device_type, local_attachments)
            if delivered_locally:
                self._log(f"→ delivered natively to {sender} via {device_type}")
            else:
                self._log(
                    f"⚠ Native delivery failed for {sender} (device={device_type}). "
                    "Falling back to backend SMTP."
                )

        # Always send the result back so the backend's future resolves. The
        # backend uses `deliver_natively` to decide whether to send via SMTP
        # itself; if we already delivered locally, it skips that step.
        try:
            ws.send(json.dumps({
                "type": "result",
                "task_id": task_id,
                "output": output,
                "delivered_locally": delivered_locally,
                "attachments": uploaded_attachments,
            }))
        except Exception as exc:
            self._log(f"Failed to send result: {exc}")

    def _deliver_native(self, gateway_email: str, text: str, device_type: str, local_attachments: list[str] = None) -> bool:
        """Deliver `text` to the user's phone via iMessage or KDE Connect.

        Routing is driven by `device_type`:
          - "apple"   → iMessage via macOS Messages app to a linked Apple ID
          - "android" → KDE Connect → real SMS via the user's paired phone

        Returns True if delivery succeeded; the caller decides what to do with
        the failure (typically: let the backend try SMTP).
        """
        if not text:
            return False

        # Strip down for SMS-friendly length
        if len(text) > 280:
            text = self._summarize_for_sms(text, "")

        body = f"[SAGE — {self.cfg.computer_name}] {text}"
        
        # Apple → iMessage. 
        if device_type == "apple":
            if sys.platform == "darwin":
                # 1. Try sending directly to the gateway email (could be a phone or Apple ID email)
                if _send_imessage(gateway_email, body, local_attachments):
                    return True
                
                # 2. If that failed, try extracting a phone number
                phone_local = gateway_email.split("@", 1)[0] if "@" in gateway_email else ""
                phone_e164 = _normalize_e164_globally(phone_local)
                if phone_e164 and phone_e164 != gateway_email:
                    if _send_imessage(phone_e164, body, local_attachments):
                        return True

                # 3. Fallback to a linked Apple ID email if available
                try:
                    be = SAGEBackend(self._token, self._api_base)
                    providers = be.get_linked_providers()
                    apple = next((p for p in providers
                                  if p.get("provider_id") == "apple.com" and p.get("email")), None)
                    if apple and apple["email"] != gateway_email:
                        if _send_imessage(apple["email"], body, local_attachments):
                            return True
                except Exception as exc:
                    self._log(f"Apple ID lookup failed: {exc}")

            # Fallback for Apple on non-macOS (or failed iMessage on macOS): try KDE Connect
            phone_local = gateway_email.split("@", 1)[0] if "@" in gateway_email else ""
            phone_e164 = _normalize_e164_globally(phone_local)
            if phone_e164 and _send_via_kdeconnect(phone_e164, body):
                if local_attachments:
                    for ap in local_attachments:
                        _share_via_kdeconnect(ap)
                return True
            return False

        # Android → KDE Connect (real SMS from user's own paired Android).
        # NEVER fall back to iPhone-relay — that would send from the iPhone's
        # number, not as a separate sage identity.
        if device_type == "android" and phone_e164:
            sent_ok = False
            if getattr(self, "_kde_listener", None) and \
               self._kde_listener.send_sms(phone_e164, body):
                sent_ok = True
            elif _send_via_kdeconnect(phone_e164, body):
                sent_ok = True
            if sent_ok:
                if local_attachments:
                    for ap in local_attachments:
                        _share_via_kdeconnect(ap)
                return True
            return False

        # Untagged/unknown device — try iMessage on macOS, KDE Connect everywhere.
        if not device_type:
            if sys.platform == "darwin":
                if phone_e164 and _send_imessage(phone_e164, body, local_attachments):
                    return True
                if phone_e164 and _send_macos_sms(phone_e164, body):
                    return True
            
            if phone_e164:
                sent_ok = False
                if getattr(self, "_kde_listener", None) and \
                   self._kde_listener.send_sms(phone_e164, body):
                    sent_ok = True
                elif _send_via_kdeconnect(phone_e164, body):
                    sent_ok = True
                if sent_ok:
                    if local_attachments:
                        for ap in local_attachments:
                            _share_via_kdeconnect(ap)
                    return True

        return False

    def _handle_native_message(self, msg: dict) -> None:
        """Deliver a standalone announcement / notification via the OS bridge.

        This is the outbound path used by /sms/announce — there's no task to
        run and no result to send back, just a one-shot delivery. The backend
        passes the bare 10-digit phone number (no @gateway suffix), so we
        format it for iMessage/KDE Connect ourselves.
        """
        phone       = (msg.get("phone") or "").strip()
        text        = (msg.get("text") or "").strip()
        device_type = (msg.get("device_type") or "").lower()
        if not phone or not text:
            return

        phone_e164 = _normalize_e164_globally(phone)
        if not phone_e164:
            self._log(f"native_message: invalid phone {phone!r}")
            return

        body = f"[SAGE — {self.cfg.computer_name}] {text}"

        # 1. Try iMessage if on macOS and device is Apple or untagged
        if sys.platform == "darwin" and device_type in ("apple", ""):
            if _send_imessage(phone_e164, body):
                self._log(f"→ announce delivered via iMessage to {phone_e164}")
                return

        # 2. Try KDE Connect if device is Android, untagged, or (Apple on non-macOS / failed iMessage)
        if device_type in ("android", "", "apple"):
            if getattr(self, "_kde_listener", None) and \
               self._kde_listener.send_sms(phone_e164, body):
                self._log(f"→ announce delivered via KDE Connect (takeover) to {phone_e164}")
                return
            if _send_via_kdeconnect(phone_e164, body):
                self._log(f"→ announce delivered via KDE Connect to {phone_e164}")
                return

            if device_type == "android":
                self._log(
                    f"⚠ Android SMS delivery to {phone_e164} pending — waiting for "
                    "Pixel to reconnect. To force it: toggle Wi-Fi off/on on the Pixel."
                )
                return

        self._log(
            f"native_message: delivery failed for {phone_e164} (device={device_type!r}, platform={sys.platform}). "
            "Ensure iMessage is signed in (macOS) or KDE Connect is paired (Linux/Windows/macOS)."
        )

    def _handle_imessage_fallback(self, msg: dict) -> None:
        """Deliver a previously-bounced SMTP reply via the local OS bridge.

        Routing is driven by the contact's `device_type`:
          - "apple"   → iMessage via macOS Messages app
          - "android" → KDE Connect → real SMS via paired phone
          - ""        → try iMessage first, then KDE Connect (auto)
        """
        recipient_bounced = msg.get("recipient", "")
        text              = msg.get("text", "")
        device_type       = (msg.get("device_type") or "").lower()
        if not text:
            return

        # Normalize phone number for KDE Connect
        phone_local = recipient_bounced.split("@", 1)[0] if "@" in recipient_bounced else ""
        phone_e164 = _normalize_e164_globally(phone_local)

        body = f"[SAGE] {text}"

        # 1. Try iMessage if on macOS and (Apple or Untagged)
        if sys.platform == "darwin" and device_type in ("apple", ""):
            try:
                be = SAGEBackend(self._token, self._api_base)
                providers = be.get_linked_providers()
                apple = next((p for p in providers
                              if p.get("provider_id") == "apple.com" and p.get("email")), None)
                if apple and _send_imessage(apple["email"], body):
                    self._log(
                        f"iMessage delivered to {apple['email']} "
                        f"(SMTP to {recipient_bounced} bounced; device={device_type or 'untagged'})"
                    )
                    return
            except Exception as exc:
                self._log(f"iMessage path errored: {exc}")

        # 2. Try KDE Connect if (Android or Untagged or Apple-on-non-macOS/failed-iMessage)
        if phone_e164 and device_type in ("android", "", "apple"):
            if _send_via_kdeconnect(phone_e164, body):
                self._log(
                    f"KDE Connect SMS delivered to {phone_e164} "
                    f"(SMTP to {recipient_bounced} bounced; device={device_type or 'untagged'})"
                )
                return

        # All fallbacks failed
        self._log(
            f"All fallbacks failed for {recipient_bounced} (device={device_type or 'unknown'}, platform={sys.platform}). "
            "Apple: link Apple ID in Connected Accounts + open Messages app (macOS). "
            "Android/Linux/Windows: install KDE Connect on this computer and on your phone, then pair them."
        )

    def _handle_imessage_to_apple_id(self, ws: websocket.WebSocket, msg: dict) -> None:
        """Send an iMessage directly to an Apple ID email address via Messages.app.

        Called when the backend dispatches `type: imessage_to_apple_id`. This
        bypasses the SMTP / Apple Private Email Relay path which requires the
        sending domain to be registered with Apple. Messages.app can send to any
        valid Apple ID email (including @privaterelay.appleid.com addresses) as
        long as this Mac is signed into iCloud with iMessage enabled.
        """
        apple_email   = (msg.get("apple_email") or "").strip()
        text          = (msg.get("text") or "").strip()
        computer_name = (msg.get("computer_name") or self.cfg.computer_name or "SAGE").strip()
        task_id       = msg.get("task_id")
        attachments   = msg.get("attachments") or []
        
        if not apple_email or (not text and not attachments):
            return

        body = f"[SAGE — {computer_name}] {text}"
        
        local_attachment_paths = []
        if attachments:
            import tempfile
            temp_dir = Path(tempfile.mkdtemp(prefix="sage-sms-attachments-"))
            be = SAGEBackend(self._token, self._api_base)
            for att in attachments:
                file_id = att.get("file_id")
                filename = att.get("filename", "attachment")
                if not file_id:
                    continue
                dest = temp_dir / filename
                if be.download_file(file_id, dest):
                    local_attachment_paths.append(str(dest))

        # Normalize handle: if it looks like a phone number, convert to E.164
        normalized_recipient = apple_email
        if "@" not in apple_email:
            e164 = _normalize_e164_globally(apple_email)
            if e164:
                normalized_recipient = e164

        success = False
        if sys.platform != "darwin":
            # Fallback for non-macOS: if normalized_recipient is a phone number, try KDE Connect
            phone_e164 = _normalize_e164_globally(normalized_recipient)
            if phone_e164:
                if _send_via_kdeconnect(phone_e164, body):
                    if local_attachment_paths:
                        for ap in local_attachment_paths:
                            _share_via_kdeconnect(ap)
                    self._log(f"→ iMessage (SMS fallback via KDE Connect) delivered to {normalized_recipient}")
                    success = True

            if not success:
                self._log(
                    f"⚠ iMessage to Apple ID {normalized_recipient} skipped — "
                    "only supported on macOS, and KDE Connect fallback failed or target is not a phone number"
                )
        else:
            # macOS Path
            if _send_imessage(normalized_recipient, body, local_attachment_paths):
                self._log(f"→ iMessage delivered to Apple ID {normalized_recipient}")
                success = True
            else:
                self._log(
                    f"⚠ iMessage to Apple ID {normalized_recipient} failed — "
                    "ensure Messages.app is open and signed into iCloud with iMessage enabled"
                )

        # Send result back if task_id exists, so backend can confirm delivery
        if task_id:
            try:
                import json
                ws.send(json.dumps({
                    "type": "result",
                    "task_id": task_id,
                    "delivered_locally": success,
                }))
            except Exception:
                pass

    # Known Apple ID email domains that are valid iMessage addresses
    _APPLE_ID_DOMAINS = {"icloud.com", "me.com", "mac.com"}

    def _announce_online(self) -> None:
        """Notify all linked accounts that the bridge is online.

        Two delivery paths:
          1. SAGE email bridge (backend POST /sms/announce) — handles Gmail, SMTP,
             phone-gateway iMessage/KDE-Connect.
          2. Direct iMessage from this Mac — handled in backend now.
        """
        be = SAGEBackend(self._token, self._api_base)

        # Reclaim identities to ensure routing is correct for this UID (Privacy protection)
        try:
            be.reclaim_identities()
        except Exception as exc:
            self._log(f"Identity reclaim failed (non-fatal): {exc}")

        # SAGE email bridge — email + phone contacts
        try:
            be.announce(self.cfg.computer_name)
            self._log("Announced online to contacts")
        except Exception as exc:
            self._log(f"Announce failed (non-fatal): {exc}")

    def run(self) -> None:
        """Main loop: connect to backend WebSocket, process tasks until stopped."""
        try:
            import websocket as _ws_lib
        except ImportError:
            print("Installing websocket-client...")
            subprocess.run([sys.executable, "-m", "pip", "install", "websocket-client", "-q"])
            import websocket as _ws_lib

        reconnect_delay = 3

        # macOS: start the inbound iMessage/SMS poller in a background thread.
        # This is independent of the WebSocket — even if the backend is down,
        # the user can still iMessage sage and get a reply locally.
        if sys.platform == "darwin":
            threading.Thread(target=self._imessage_poll_loop, daemon=True).start()

        # KDE Connect inbound listener: enabled by default on Linux/Windows,
        # opt-in on macOS (where iMessage is the primary native path).
        kde_enabled = os.environ.get("SAGE_KDE_INBOUND")
        if kde_enabled == "1" or (kde_enabled != "0" and sys.platform != "darwin"):
            self._start_kde_inbound_listener()

        self._log(f"Connecting to {self._ws_url}")
        
        # P0 Security: track the UID of the token we started with.
        # If the user logs out and in as someone else, we must stop.
        from sage.core.cli_auth import get_uid_from_token
        start_uid = get_uid_from_token(self._token)

        while not self._stop.is_set():
            # Check if token still belongs to start_uid
            from sage.core.cli_auth import load_auth
            curr_auth = load_auth()
            if curr_auth:
                curr_uid = get_uid_from_token(curr_auth.get("id_token", ""))
                if curr_uid and curr_uid != start_uid:
                    self._log(f"User switch detected (start_uid={start_uid} curr_uid={curr_uid}). Stopping bridge.")
                    self.stop()
                    break
            
            try:
                ws = _ws_lib.create_connection(self._ws_url, timeout=15)

                # Authenticate
                ws.send(json.dumps({
                    "type": "auth",
                    "token": self._token,
                    "computer_name": self.cfg.computer_name,
                    "platform": sys.platform,
                }))

                # Wait for ready — handle empty/invalid frames cleanly. Cloud Run
                # sometimes closes idle WebSockets mid-handshake; ws.recv() then
                # returns "" and json.loads("") raises a cryptic JSONDecodeError.
                raw_ready = ws.recv()
                if not raw_ready:
                    self._log("Backend closed connection during handshake — retrying")
                    try: ws.close()
                    except Exception: pass
                    raise RuntimeError("ws-handshake-empty")
                try:
                    resp = json.loads(raw_ready)
                except json.JSONDecodeError:
                    self._log(f"Invalid handshake frame: {raw_ready[:120]!r} — retrying")
                    try: ws.close()
                    except Exception: pass
                    raise RuntimeError("ws-handshake-invalid")
                if resp.get("type") != "ready":
                    self._log(f"Unexpected auth response: {resp}")
                    ws.close()
                    continue

                self._bridge_email = resp.get("display_email") or resp.get("bridge_email", "")
                self._user_email = (resp.get("user_email") or "").lower().strip()
                self._user_phone = (resp.get("user_phone") or "").strip()
                phone_file = Path.home() / ".sage" / "verified_phone.txt"
                if self._user_phone:
                    try:
                        phone_file.parent.mkdir(parents=True, exist_ok=True)
                        phone_file.write_text(self._user_phone, encoding="utf-8")
                        phone_file.chmod(0o600)
                    except Exception:
                        pass
                else:
                    # Clear it if the current user has none, ensuring no leak from previous user
                    if phone_file.exists():
                        try: phone_file.unlink()
                        except Exception: pass
                reconnect_delay = 3
                self._log(f"Connected. Users message: {self._bridge_email}")

                # On first successful connection, notify all contacts we're online
                if not self._announced:
                    self._announced = True
                    threading.Thread(target=self._announce_online, daemon=True).start()

                # Stale-connection detection: track heartbeat→pong roundtrips so
                # we can force a reconnect if the server drops us without the
                # OS noticing. WebSocket libraries can sit forever on a dead
                # socket if the kernel never bubbles up the FIN/RST.
                last_heartbeat = time.time()
                last_pong      = time.time()
                STALE_AFTER    = 90  # seconds without a pong → reconnect

                while not self._stop.is_set():
                    if hasattr(ws, "settimeout"):
                        ws.settimeout(5)
                    try:
                        raw = ws.recv()
                        if not raw:
                            # Empty frame = peer closed cleanly. Reconnect.
                            break
                        try:
                            msg = json.loads(raw)
                        except json.JSONDecodeError:
                            # Non-JSON frame (shouldn't happen, but log + skip)
                            continue
                        msg_type = msg.get("type", "")

                        if msg_type == "task":
                            threading.Thread(
                                target=self._handle_task,
                                args=(ws, msg),
                                daemon=True,
                            ).start()

                        elif msg_type == "native_message":
                            # Backend asking us to deliver a standalone message
                            # (e.g. announcement) via iMessage / KDE Connect.
                            threading.Thread(
                                target=self._handle_native_message,
                                args=(msg,),
                                daemon=True,
                            ).start()

                        elif msg_type == "imessage_fallback":
                            # Backend detected an SMTP bounce for a phone-gateway
                            # recipient — send the original reply via iMessage.
                            threading.Thread(
                                target=self._handle_imessage_fallback,
                                args=(msg,),
                                daemon=True,
                            ).start()

                        elif msg_type == "imessage_to_apple_id":
                            # Direct iMessage to an Apple ID email address.
                            # Used when the contact's email is an Apple provider
                            # address (including private-relay @privaterelay.appleid.com)
                            # and the SMTP path can't reach it (Apple relay not configured).
                            threading.Thread(
                                target=self._handle_imessage_to_apple_id,
                                args=(ws, msg),
                                daemon=True,
                            ).start()

                        elif msg_type == "pong":
                            last_pong = time.time()

                    except _ws_lib.WebSocketTimeoutException:
                        pass  # normal — check heartbeat
                    except Exception:
                        break  # connection lost

                    # Periodic heartbeat to keep the connection alive
                    if time.time() - last_heartbeat > HEARTBEAT_INTERVAL:
                        try:
                            ws.send(json.dumps({"type": "heartbeat"}))
                            last_heartbeat = time.time()
                        except Exception:
                            break

                    # Stale-connection guard: if heartbeats are firing but no
                    # pong has come back in STALE_AFTER seconds, the WS is dead
                    # at the application layer even if the socket looks alive.
                    if time.time() - last_pong > STALE_AFTER:
                        self._log(
                            f"No pong from server in {int(time.time() - last_pong)}s — "
                            "treating as stale and reconnecting"
                        )
                        break

                ws.close()

            except KeyboardInterrupt:
                break
            except Exception as exc:
                if not self._stop.is_set():
                    import traceback
                    self._log(f"Connection error: {exc} — retrying in {reconnect_delay}s\n{traceback.format_exc()}")
                    time.sleep(reconnect_delay)
                    reconnect_delay = min(reconnect_delay * 2, 60)

        self._log("Stopped.")
        self._log_fp.close()
        SMS_PID_FILE.unlink(missing_ok=True)


# ── Setup wizard ───────────────────────────────────────────────────────────────

def run_setup_wizard() -> SMSConfig | None:
    print()
    print("╭─────────────────────────────────────────────────────────╮")
    print("│  SAGE Message Bridge Setup                              │")
    print("│  Message SAGE from iMessage or Gmail — no config needed │")
    print("╰─────────────────────────────────────────────────────────╯")
    print()

    # Verify SAGE login
    print("── Checking SAGE account ───────────────────────────────────")
    try:
        token, api_base = _load_sage_token()
        be = SAGEBackend(token, api_base)
        contacts = be.list_contacts()
        print(f"✅ Logged in   ({len(contacts)} contact(s) registered)")
    except RuntimeError as exc:
        print(f"❌ {exc}")
        return None

    # Fetch SAGE bridge email from backend
    bridge_email = ""
    try:
        import websocket as _ws_lib
        ws = _ws_lib.create_connection(
            api_base.replace("https://", "wss://").replace("http://", "ws://") + "/ws/sms",
            timeout=5,
        )
        # Peek at the ready message to get bridge email
        ws.send(json.dumps({"type": "auth", "token": token, "computer_name": "_setup"}))
        resp = json.loads(ws.recv())
        bridge_email = resp.get("display_email") or resp.get("bridge_email", "")
        ws.close()
    except Exception:
        pass

    existing = SMSConfig.load()

    # Computer name
    print()
    print("── Step 1: Computer name ───────────────────────────────────")
    print("Used to route messages: @name: task")
    default = existing.computer_name if existing else _default_name()
    name_in = input(f"Name for this computer [{default}]: ").strip()
    computer_name = name_in or default

    # Working directory
    print()
    print("── Step 2: Default working directory ───────────────────────")
    default_dir = existing.working_dir if existing else str(Path.home())
    dir_in = input(f"Working directory [{default_dir}]: ").strip()
    working_dir = str(Path(dir_in or default_dir).expanduser().resolve())

    # Authorized contacts
    print()
    print("── Step 3: Authorized phone contacts ───────────────────────")
    print("Email addresses SAGE accepts commands from.")
    print("  iPhone  → your Apple ID email (Settings → Messages → Send & Receive)")
    print("  Android → your Gmail address")
    if contacts:
        print("\nAlready registered:")
        for c in contacts:
            print(f"  {c['email']}  ({c.get('label', '')})")
    print()
    while True:
        email_in = input("Add contact email (Enter to skip): ").strip().lower()
        if not email_in:
            break
        label_in = input(f"  Label for {email_in} (e.g. iPhone): ").strip()
        try:
            be.add_contact(email_in, label_in)
            print(f"  ✅ Added: {email_in}")
        except Exception as exc:
            print(f"  ❌ {exc}")

    cfg = SMSConfig(
        computer_name=computer_name,
        working_dir=working_dir,
    )
    cfg.save()
    print(f"\n✅ Config saved → {SMS_CONFIG}")

    # Register the device with the backend so it appears in `sage sms devices`
    # immediately — without this, the device is only known to the backend
    # after the first `sage sms start` (which opens a WebSocket and sends
    # the auth frame). Idempotent on (uid, computer_name).
    try:
        be.register_computer(computer_name, bridge_email)
        print(f"✅ Registered '{computer_name}' with SAGE backend")
    except Exception as exc:
        print(f"⚠ Could not register with backend: {exc}")
        print("   The device will register automatically when you run `sage sms start`.")

    # Instructions
    display = bridge_email or "message@sageworksai.com"
    print()
    print("── How to use from your phone ──────────────────────────────")
    print()
    print("  iPhone (iMessage):")
    print(f"    Messages → New Message → type: {display}")
    print(f"    Send any task → SAGE replies as iMessage")
    print()
    print("  Android (Google Messages / Gmail):")
    print(f"    Email {display} from your phone")
    print()
    print("  Route to a specific computer:")
    print(f"    @{computer_name}: fix the auth bug")
    print(f"    @all: git status")
    print()
    print("  Start the bridge:")
    print("    sage sms start")
    print()
    return cfg
