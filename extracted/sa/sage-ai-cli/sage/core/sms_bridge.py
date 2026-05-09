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
    computer_name: str = field(default_factory=lambda: _default_name())
    working_dir:   str = str(Path.home())
    model:         str = ""

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

    def _get(self, path: str) -> dict:
        return self._request("GET", path)

    def _post(self, path: str, body: dict) -> dict:
        return self._request("POST", path, json=body)

    def _delete(self, path: str) -> dict:
        return self._request("DELETE", path)

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

def _send_imessage(recipient: str, text: str) -> bool:
    """Send an iMessage from this Mac via the Messages app.

    Recipient can be an Apple ID email (e.g. user@icloud.com) or a phone
    number in E.164 format (+14085073140). Works only when the Mac is
    signed into an Apple ID with iMessage enabled. The sender will be the
    Mac's signed-in Apple ID — no way around this without Apple Business
    Chat (which is paid).
    """
    if sys.platform != "darwin":
        return False
    safe_text = text.replace("\\", "\\\\").replace('"', '\\"')
    safe_to   = recipient.replace("\\", "\\\\").replace('"', '\\"')
    script = (
        'tell application "Messages"\n'
        '    set theService to first service whose service type = iMessage\n'
        f'    set theBuddy to buddy "{safe_to}" of theService\n'
        f'    send "{safe_text}" to theBuddy\n'
        'end tell'
    )
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=10,
        )
        return result.returncode == 0
    except Exception as exc:
        logger.debug("osascript iMessage failed: %s", exc)
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
    # macOS app bundle locations
    candidates = [
        "/Applications/KDE Connect.app/Contents/MacOS/kdeconnect-cli",
        os.path.expanduser("~/Applications/KDE Connect.app/Contents/MacOS/kdeconnect-cli"),
        # Windows default install path (when Python runs there)
        r"C:\Program Files\KDE Connect\kdeconnect-cli.exe",
        r"C:\Program Files (x86)\KDE Connect\kdeconnect-cli.exe",
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
        return False
    safe_text = text.replace("\\", "\\\\").replace('"', '\\"')
    safe_to   = recipient.replace("\\", "\\\\").replace('"', '\\"')
    script = (
        'tell application "Messages"\n'
        '    try\n'
        '        set smsService to first service whose service type = SMS\n'
        f'        set theBuddy to buddy "{safe_to}" of smsService\n'
        f'        send "{safe_text}" to theBuddy\n'
        '        return "ok"\n'
        '    on error errMsg\n'
        '        return "err: " & errMsg\n'
        '    end try\n'
        'end tell'
    )
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=10,
        )
        out = (result.stdout or "").strip()
        return result.returncode == 0 and out == "ok"
    except Exception as exc:
        logger.debug("Messages.app SMS send failed: %s", exc)
        return False


def _kdeconnectd_running() -> tuple[bool, str]:
    """Check whether KDE Connect can reach a paired device.

    The Mac App Store build of KDE Connect always prints a DBus activation
    error to stderr ("name org.kde.kdeconnect was not provided by any .service
    files"), but `--send-sms` and `--list-devices` both still WORK — the CLI
    has a network-discovery fallback that bypasses DBus. So we ignore stderr
    entirely and treat "at least one paired+reachable device" as healthy.
    """
    cli = _find_kdeconnect_cli()
    if not cli:
        return False, "kdeconnect-cli not installed"
    try:
        r = subprocess.run([cli, "--list-available", "--id-only"],
                           capture_output=True, text=True, timeout=5)
        devices = [d.strip() for d in (r.stdout or "").splitlines() if d.strip()]
        if not devices:
            return False, "no paired+reachable KDE Connect devices"
        return True, ""
    except Exception as exc:
        return False, f"kdeconnect-cli probe failed: {exc}"


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
    try:
        # Find a paired+reachable device.
        result = subprocess.run(
            [cli, "--list-available", "--id-only"],
            capture_output=True, text=True, timeout=5,
        )
        devices = [d.strip() for d in (result.stdout or "").splitlines() if d.strip()]
        if not devices:
            logger.debug("KDE Connect: no paired+reachable devices")
            return False
        device_id = devices[0]
        send_result = subprocess.run(
            [cli, "--send-sms", text,
             "--destination", phone_number,
             "-d", device_id],
            capture_output=True, text=True, timeout=10,
        )
        # Trust exit code only. The Mac App Store build always emits DBus
        # activation noise to stderr but still delivers; treating that as
        # failure rejects working sends.
        return send_result.returncode == 0
    except Exception as exc:
        logger.debug("KDE Connect send failed: %s", exc)
        return False


def _strip_ansi(text: str) -> str:
    text = re.sub(r'\x1b\[[0-9;]*[mGKHFABCDEJst]', '', text)
    return re.sub(r'\x1b\][^\x07]*\x07', '', text).strip()


# Tool-call / prompt / footer noise that streams from `sage ask --raw`.
# We strip these before SMS so the user gets the FINAL ANSWER, not the work log.
_TOOL_LINE_RE = re.compile(
    r'^\s*(READ|WRITE|EDIT|RUN|BASH|GREP|GLOB|LS|FIND|FETCH|SEARCH|TASK|TODO|'
    r'PATCH|APPLY|DIFF|CREATE|DELETE|MOVE|COPY|VIEW|OPEN|TOOL|CALL)\s*:.*$',
    re.IGNORECASE,
)
_PROMPT_LINE_RE = re.compile(r'^\s*\[SAGE[^\]]*\]\s*sage>.*$', re.IGNORECASE)
_FOOTER_LINE_RE = re.compile(r'^\s*[─\-]\s*\d+\s*tokens?\b.*$')
_THINK_BLOCK_RE = re.compile(r'<thinking>.*?</thinking>', re.DOTALL | re.IGNORECASE)


def _extract_final_answer(raw: str) -> str:
    """Pull the model's actual reply out of `sage ask --raw` output.

    The raw stream interleaves three things we don't want over SMS:
      1. `<thinking>...</thinking>` blocks — internal reasoning.
      2. Tool-call trace lines (`READ: foo.py`, `EDIT: bar.ts`, etc.) — the
         work log, not the answer.
      3. The `[SAGE — host] sage>` prompt prefix and the trailing
         `─ 124 tokens · 10s · …` token footer.

    Strip all of that and return only the real prose. If nothing is left
    (model produced only tool calls, e.g. it ran out of budget mid-research),
    we fall back to the original text so the summarizer still has something
    to work with rather than empty string.
    """
    text = _THINK_BLOCK_RE.sub('', raw)
    cleaned_lines: list[str] = []
    for line in text.splitlines():
        if _TOOL_LINE_RE.match(line):
            continue
        if _PROMPT_LINE_RE.match(line):
            continue
        if _FOOTER_LINE_RE.match(line):
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
        self._log_fp = SMS_LOG_FILE.open("a", buffering=1)
        # Tracks the last seen Messages chat.db ROWID so we only process new
        # inbound iMessage / SMS after the bridge starts (not the entire
        # historical chat log).
        self._last_msg_rowid: int | None = None
        # Cache of registered phone-number contacts keyed by E.164 form. Refreshed
        # periodically by the iMessage poller so newly-added contacts route too.
        self._phone_contacts_cache: dict[str, dict] = {}
        self._phone_cache_refreshed_at: float = 0.0

    def _log(self, msg: str) -> None:
        ts = time.strftime("%H:%M:%S")
        line = f"[{ts}][{self.cfg.computer_name}] {msg}"
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
        """Pull registered phone contacts from the backend, cache by E.164."""
        if time.time() - self._phone_cache_refreshed_at < 30:
            return  # cached recently
        try:
            be = SAGEBackend(self._token, self._api_base)
            contacts = be.list_contacts()
            cache: dict[str, dict] = {}
            for c in contacts:
                email = (c.get("email") or "")
                if not email.startswith("phone:"):
                    continue
                digits = re.sub(r"\D", "", email.replace("phone:", ""))
                if len(digits) == 11 and digits.startswith("1"):
                    digits = digits[1:]
                if len(digits) == 10:
                    cache[f"+1{digits}"] = c
                    cache[digits] = c  # also bare digits, just in case
            self._phone_contacts_cache = cache
            self._phone_cache_refreshed_at = time.time()
        except Exception as exc:
            logger.debug("phone contacts refresh failed: %s", exc)

    def _imessage_initial_rowid(self) -> int:
        """Return the current max ROWID so we only see messages from now on."""
        try:
            import sqlite3
            with sqlite3.connect(f"file:{self._CHAT_DB}?mode=ro", uri=True, timeout=2) as db:
                cur = db.execute("SELECT COALESCE(MAX(ROWID), 0) FROM message")
                return cur.fetchone()[0] or 0
        except Exception:
            return 0

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
        if self._last_msg_rowid is None:
            self._last_msg_rowid = self._imessage_initial_rowid()
            return []

        results: list[dict] = []
        try:
            import sqlite3
            with sqlite3.connect(f"file:{self._CHAT_DB}?mode=ro", uri=True, timeout=2) as db:
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
        except Exception as exc:
            self._log(f"chat.db poll failed: {exc}")
        return results

    def _normalize_e164(self, raw: str) -> str:
        """Normalize phone-shaped sender to +1XXXXXXXXXX."""
        digits = re.sub(r"\D", "", raw or "")
        if len(digits) == 11 and digits.startswith("1"):
            digits = digits[1:]
        if len(digits) == 10:
            return f"+1{digits}"
        if raw and raw.startswith("+"):
            return raw
        return ""

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

        # Look up the contact — must be registered
        contact = self._phone_contacts_cache.get(e164)
        if not contact:
            return  # unregistered sender; don't run sage on every random chat

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

        # Built-in commands run instantly without invoking `sage ask`
        if lower in ("help", "?", "@help"):
            output = (
                f"SAGE [{self.cfg.computer_name}] commands:\n"
                "Any text → sage task\n"
                "@status, @dir, @help, @stop\n"
                "@<computer>: <task> → route to a specific computer"
            )
        elif lower in ("@dir", "@pwd", "pwd"):
            output = f"📁 [{self.cfg.computer_name}] {self.working_dir}"
        elif lower in ("@status", "status"):
            output = (
                f"✅ [{self.cfg.computer_name}]\n"
                f"📁 {self.working_dir}"
            )
        elif lower in ("@stop", "stop"):
            output = f"⏹ [{self.cfg.computer_name}] stopping."
            self._stop.set()
        else:
            output = self._run_sage_task(task)
            if len(output) > 280:
                output = self._summarize_for_sms(output, task)

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
        elif device_type == "apple":
            if _send_imessage(target, body):
                sent_via = "iMessage"
        else:
            if service.lower() == "imessage" and _send_imessage(target, body):
                sent_via = "iMessage"
            elif sys.platform == "darwin" and _send_macos_sms(target, body):
                sent_via = "SMS (iPhone relay)"
            elif _send_imessage(target, body):
                sent_via = "iMessage"

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

    def _run_sage_task(
        self,
        task: str,
        timeout: int | None = None,
        mode: str = "agent",
    ) -> str:
        """Execute a sage task as a subprocess.

        Two dispatch modes:
        - mode="agent" (default, used for real SMS tasks): runs `sage run --prompt`
          which fires the full agent loop — shell, file edits, RUN: blocks, test
          loops, retries. This is what makes texted requests like "create a
          project at ~/foo" or "run the tests" actually execute. Without this,
          the model just chats back ("I cannot run commands").
        - mode="chat" (used for the SMS reply summarizer): runs `sage ask --raw`
          which is a fast one-shot text completion with no tool use. Right for
          pure compression tasks where we don't want the agent reasoning loop.

        No deadline by default — real coding work routinely runs longer than
        any timeout we'd pick, and dropping the reply mid-run is the worst
        possible UX. Callers that genuinely want a deadline pass `timeout`.
        """
        model_flags = ["--model", self.cfg.model] if self.cfg.model else []
        if mode == "agent":
            cmd_variants = (
                [sys.executable, "-m", "sage", "run"] + model_flags + ["--prompt", task],
                ["sage", "run"] + model_flags + ["--prompt", task],
            )
        else:
            cmd_variants = (
                [sys.executable, "-m", "sage", "ask"] + model_flags + ["--raw", task],
                ["sage", "ask"] + model_flags + ["--raw", task],
            )
        for cmd in cmd_variants:
            try:
                result = subprocess.run(
                    cmd, cwd=str(self.working_dir),
                    capture_output=True, text=True, timeout=timeout,
                    env={**os.environ, "NO_COLOR": "1", "TERM": "dumb"},
                )
                raw = _strip_ansi((result.stdout or "") + (result.stderr or "")).strip()
                out = _extract_final_answer(raw)
                return out or "Task completed."
            except FileNotFoundError:
                continue
            except subprocess.TimeoutExpired:
                return "⏱ Timed out — check your terminal for progress."
            except Exception as exc:
                return f"Error: {exc}"
        return "Error: sage command not found"

    def _summarize_for_sms(self, full_response: str, original_task: str) -> str:
        """Use the model to compress a long SAGE response into a phone-friendly reply.

        Falls back to the cleaned full text if the model is unavailable or the
        response is already short enough.
        """
        # _run_sage_task already strips tool-call traces, but if a caller hands
        # us raw output (or a future code path forgets), clean again here so
        # the summarizer never sees `READ: foo` / `[SAGE] sage>` noise.
        cleaned = _extract_final_answer(full_response)
        if len(cleaned) <= 280:
            return cleaned
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
        summary = self._run_sage_task(prompt, timeout=60, mode="chat").strip()
        # Run the cleaner over the summary too — if the summarizer itself
        # leaked any process-log lines, drop them before sending.
        summary = _extract_final_answer(summary)
        # Guard against empty / overly long summaries
        if not summary or len(summary) > 320:
            return cleaned  # backend will hard-truncate
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

        # Built-in commands
        if lower in ("help", "?", "@help"):
            output = (
                f"SAGE [{self.cfg.computer_name}] — commands:\n"
                "Any text   → run as sage task\n"
                f"@{self.cfg.computer_name}: msg → route here\n"
                "@all: msg  → all computers\n"
                "cd <path>  → change directory\n"
                "@dir       → show directory\n"
                "@status    → show status\n"
                "@stop      → stop this daemon"
            )
        elif lower in ("@dir", "@pwd", "pwd"):
            output = f"📁 [{self.cfg.computer_name}] {self.working_dir}"
        elif lower in ("@status", "status"):
            output = (
                f"✅ [{self.cfg.computer_name}]\n"
                f"📁 {self.working_dir}\n"
                f"🤖 {self.cfg.model or 'default model'}"
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
        elif lower.startswith("@model "):
            self.cfg.model = task.split(None, 1)[1].strip()
            self.cfg.save()
            output = f"🤖 [{self.cfg.computer_name}] model → {self.cfg.model}"
        elif lower in ("@stop", "stop"):
            output = f"⏹ [{self.cfg.computer_name}] stopping."
            self._stop.set()
        else:
            # Run the FULL task (sage ask) — all real work happens here
            output = self._run_sage_task(task)
            # If the reply is going to a phone-number SMS gateway, generate a
            # concise summary. The full output is logged locally; the user
            # gets a phone-friendly version back.
            if self._is_sms_gateway(sender):
                self._log(f"Summarizing for SMS gateway {sender} (full {len(output)} chars)")
                output = self._summarize_for_sms(output, task)

        # If the backend asked us to deliver natively (carrier-gateway sender +
        # known device_type), do that NOW from this machine. SMTP through
        # carrier email-to-SMS bridges is unreliable — most drop without
        # bouncing, so the user never sees the reply if we trust SMTP alone.
        delivered_locally = False
        if deliver_natively:
            delivered_locally = self._deliver_native(sender, output, device_type)
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
            }))
        except Exception as exc:
            self._log(f"Failed to send result: {exc}")

    def _deliver_native(self, gateway_email: str, text: str, device_type: str) -> bool:
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
        phone_local = gateway_email.split("@", 1)[0] if "@" in gateway_email else ""
        digits = re.sub(r"\D", "", phone_local)
        phone_e164 = ""
        if len(digits) == 10:
            phone_e164 = f"+1{digits}"
        elif len(digits) == 11 and digits.startswith("1"):
            phone_e164 = f"+{digits}"

        # Apple → iMessage. Use the user's actual phone number (E.164) — the
        # macOS Messages app routes by phone iff iMessage is enabled on this
        # machine and the recipient is registered with iMessage.
        if device_type == "apple":
            if sys.platform == "darwin" and phone_e164:
                if _send_imessage(phone_e164, body):
                    return True
            # Fallback to a linked Apple ID email if available
            try:
                be = SAGEBackend(self._token, self._api_base)
                providers = be.get_linked_providers()
                apple = next(
                    (p for p in providers
                     if p.get("provider_id") == "apple.com" and p.get("email")),
                    None,
                )
                if apple and sys.platform == "darwin":
                    if _send_imessage(apple["email"], body):
                        return True
            except Exception as exc:
                self._log(f"Apple ID lookup failed: {exc}")
            return False

        # Android → KDE Connect (real SMS from user's own paired Android).
        # NEVER fall back to iPhone-relay — that would send from the iPhone's
        # number, not as a separate sage identity.
        if device_type == "android" and phone_e164:
            if getattr(self, "_kde_listener", None) and \
               self._kde_listener.send_sms(phone_e164, body):
                return True
            return _send_via_kdeconnect(phone_e164, body)

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

        digits = re.sub(r"\D", "", phone)
        phone_e164 = ""
        if len(digits) == 10:
            phone_e164 = f"+1{digits}"
        elif len(digits) == 11 and digits.startswith("1"):
            phone_e164 = f"+{digits}"
        if not phone_e164:
            self._log(f"native_message: invalid phone {phone!r}")
            return

        body = f"[SAGE — {self.cfg.computer_name}] {text}"

        if device_type == "apple" and sys.platform == "darwin":
            if _send_imessage(phone_e164, body):
                self._log(f"→ announce delivered via iMessage to {phone_e164}")
                return
            self._log(f"⚠ iMessage delivery failed for {phone_e164}")
            return

        if device_type == "android":
            # Android-tagged contacts get SMS via the user's OWN paired Android
            # phone (KDE Connect). Never via iPhone relay — that would send
            # from the user's iPhone number, not from sage, and the recipient
            # (the Android phone) would just see iPhone messages.
            if getattr(self, "_kde_listener", None) and \
               self._kde_listener.send_sms(phone_e164, body):
                self._log(f"→ announce delivered via KDE Connect (takeover) to {phone_e164}")
                return
            if _send_via_kdeconnect(phone_e164, body):
                self._log(f"→ announce delivered via KDE Connect to {phone_e164}")
                return
            self._log(
                f"⚠ Android SMS delivery to {phone_e164} pending — waiting for "
                "Pixel to reconnect. To force it: toggle Wi-Fi off/on on the Pixel."
            )
            return

        self._log(
            f"native_message: device_type={device_type!r} not handled on this platform "
            f"(sys.platform={sys.platform})"
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

        # Normalize phone number for KDE Connect (E.164 with US country code default)
        phone_local = recipient_bounced.split("@", 1)[0] if "@" in recipient_bounced else ""
        digits = re.sub(r"\D", "", phone_local)
        if len(digits) == 10:
            phone_e164 = f"+1{digits}"
        elif len(digits) == 11 and digits.startswith("1"):
            phone_e164 = f"+{digits}"
        else:
            phone_e164 = ""

        try_apple   = device_type in ("", "apple")
        try_android = device_type in ("", "android")

        # Path 1: macOS iMessage (Apple)
        if try_apple and sys.platform == "darwin":
            try:
                be = SAGEBackend(self._token, self._api_base)
                providers = be.get_linked_providers()
                apple = next((p for p in providers
                              if p.get("provider_id") == "apple.com" and p.get("email")), None)
                if apple and _send_imessage(apple["email"], f"[SAGE] {text}"):
                    self._log(
                        f"iMessage delivered to {apple['email']} "
                        f"(SMTP to {recipient_bounced} bounced; device=apple)"
                    )
                    return
            except Exception as exc:
                self._log(f"iMessage path errored: {exc}")

        # Path 2: KDE Connect → real SMS via paired Android phone
        if try_android and phone_e164:
            if _send_via_kdeconnect(phone_e164, f"[SAGE] {text}"):
                self._log(
                    f"KDE Connect SMS delivered to {phone_e164} "
                    f"(SMTP to {recipient_bounced} bounced; device=android)"
                )
                return

        # All fallbacks failed — explain what they need
        self._log(
            f"All fallbacks failed for {recipient_bounced} (device={device_type or 'unknown'}). "
            "Apple: link Apple ID in Connected Accounts + open Messages app. "
            "Android: install KDE Connect on this Mac and on your phone, then pair them."
        )

    def _announce_online(self) -> None:
        """Notify all linked accounts that the bridge is online via the SAGE
        email bridge — replies always come from messages@sageworksai.com so the
        user sees a single canonical sender regardless of how they opened the
        thread (Gmail, Mail.app, SMS gateway).
        """
        try:
            be = SAGEBackend(self._token, self._api_base)
            # Auto-register linked provider emails as contacts (idempotent)
            be.sync_provider_contacts()
            # Send via SAGE email bridge — backend skips phone-only contacts
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

        # KDE Connect inbound listener (takeover mode): off by default because
        # it stops kdeconnectd to bind UDP+TCP 1716, and any TLS handshake
        # failure can leave the Pixel in a half-paired state. Opt-in via
        # SAGE_KDE_INBOUND=1 once we have a robust handshake. Until then,
        # rely on email + iMessage paths for inbound; KDE Connect outbound
        # (via kdeconnect-cli to the OS daemon) still works fine.
        if os.environ.get("SAGE_KDE_INBOUND") == "1":
            self._start_kde_inbound_listener()

        self._log(f"Connecting to {self._ws_url}")

        while not self._stop.is_set():
            try:
                ws = _ws_lib.create_connection(self._ws_url, timeout=15)

                # Authenticate
                ws.send(json.dumps({
                    "type": "auth",
                    "token": self._token,
                    "computer_name": self.cfg.computer_name,
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
                    self._log(f"Connection error: {exc} — retrying in {reconnect_delay}s")
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
