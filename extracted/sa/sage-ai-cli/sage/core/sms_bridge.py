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

    def _get(self, path: str) -> dict:
        r = httpx.get(f"{self._base}{path}", headers=self._headers, timeout=10)
        r.raise_for_status()
        return r.json()

    def _post(self, path: str, body: dict) -> dict:
        r = httpx.post(f"{self._base}{path}", json=body, headers=self._headers, timeout=10)
        r.raise_for_status()
        return r.json()

    def _delete(self, path: str) -> dict:
        r = httpx.delete(f"{self._base}{path}", headers=self._headers, timeout=10)
        r.raise_for_status()
        return r.json()

    def list_computers(self) -> list[dict]:
        return self._get("/sms/computers").get("computers", [])

    def remove_computer(self, computer_id: str) -> dict:
        return self._delete(f"/sms/computers/{computer_id}")

    def list_contacts(self) -> list[dict]:
        return self._get("/sms/contacts").get("contacts", [])

    def add_contact(self, email: str, label: str = "") -> dict:
        resp = self._post("/sms/contacts", {"email": email, "label": label})
        return resp.get("contact", resp)

    def remove_contact(self, email: str) -> dict:
        from urllib.parse import quote
        return self._delete(f"/sms/contacts/{quote(email, safe='')}")

    def contact_emails(self) -> list[str]:
        return [c["email"] for c in self.list_contacts() if c.get("email")]

    def announce(self, computer_name: str) -> None:
        """Notify all registered contacts that this computer is online."""
        try:
            self._post("/sms/announce", {"computer_name": computer_name})
        except Exception as exc:
            logger.warning("announce failed: %s", exc)

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

def _send_imessage(apple_id: str, text: str) -> bool:
    """Send an iMessage from this Mac via the Messages app (osascript).

    Works when the Mac is signed into an Apple ID with iMessage enabled.
    The recipient's apple_id can be their iCloud email or phone number.
    """
    if sys.platform != "darwin":
        return False
    # Escape for AppleScript string literals
    safe_text = text.replace("\\", "\\\\").replace('"', '\\"')
    safe_id   = apple_id.replace("\\", "\\\\").replace('"', '\\"')
    script = (
        'tell application "Messages"\n'
        '    set theService to first service whose service type = iMessage\n'
        f'    set theBuddy to buddy "{safe_id}" of theService\n'
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


def _strip_ansi(text: str) -> str:
    text = re.sub(r'\x1b\[[0-9;]*[mGKHFABCDEJst]', '', text)
    return re.sub(r'\x1b\][^\x07]*\x07', '', text).strip()


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

    def _log(self, msg: str) -> None:
        ts = time.strftime("%H:%M:%S")
        line = f"[{ts}][{self.cfg.computer_name}] {msg}"
        print(line)
        self._log_fp.write(line + "\n")

    def _run_sage_task(self, task: str) -> str:
        model_flags = ["--model", self.cfg.model] if self.cfg.model else []
        for cmd in (
            [sys.executable, "-m", "sage", "ask"] + model_flags + ["--raw", task],
            ["sage", "ask"] + model_flags + ["--raw", task],
        ):
            try:
                result = subprocess.run(
                    cmd, cwd=str(self.working_dir),
                    capture_output=True, text=True, timeout=180,
                    env={**os.environ, "NO_COLOR": "1", "TERM": "dumb"},
                )
                out = _strip_ansi((result.stdout or "") + (result.stderr or "")).strip()
                return out or "Task completed."
            except FileNotFoundError:
                continue
            except subprocess.TimeoutExpired:
                return "⏱ Timed out (>3 min). Check your terminal."
            except Exception as exc:
                return f"Error: {exc}"
        return "Error: sage command not found"

    def _handle_task(self, ws, msg: dict) -> None:
        """Process a task from the backend (runs in a thread)."""
        task_id = msg.get("task_id", "")
        task    = msg.get("task", "").strip()
        sender  = msg.get("from", "")
        lower   = task.lower()

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
            output = self._run_sage_task(task)

        # Send result back via WebSocket (thread-safe via httpx sync)
        try:
            import websocket as _ws_lib
            ws.send(json.dumps({"type": "result", "task_id": task_id, "output": output}))
        except Exception as exc:
            self._log(f"Failed to send result: {exc}")

    def _announce_online(self) -> None:
        """Notify all linked accounts that the bridge is online.

        - Syncs Google/Apple provider emails as contacts (idempotent)
        - Sends via SAGE email bridge to all registered contacts
        - On macOS, also sends an iMessage directly via the Messages app
          to any linked Apple ID
        """
        try:
            be = SAGEBackend(self._token, self._api_base)

            # Auto-register provider emails so they receive the announcement
            be.sync_provider_contacts()

            # Send via SAGE email bridge (covers Gmail + phone gateways)
            be.announce(self.cfg.computer_name)
            self._log("Announced online to contacts")

            # Also send via iMessage on macOS for instant delivery to Apple ID
            if sys.platform == "darwin":
                providers = be.get_linked_providers()
                msg = (
                    f"✅ [{self.cfg.computer_name}] SAGE is online.\n"
                    f"Text me any task and I'll run it on your Mac.\n"
                    f"Reply @help for commands."
                )
                for p in providers:
                    if p.get("provider_id") == "apple.com" and p.get("email"):
                        if _send_imessage(p["email"], msg):
                            self._log(f"iMessage sent to {p['email']}")
                        else:
                            self._log(f"iMessage failed (Messages app may not be open)")
                        break
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

                # Wait for ready
                resp = json.loads(ws.recv())
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

                last_heartbeat = time.time()

                while not self._stop.is_set():
                    ws.settimeout(5)
                    try:
                        raw = ws.recv()
                        msg = json.loads(raw)
                        msg_type = msg.get("type", "")

                        if msg_type == "task":
                            threading.Thread(
                                target=self._handle_task,
                                args=(ws, msg),
                                daemon=True,
                            ).start()

                        elif msg_type == "pong":
                            pass  # heartbeat acknowledged

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
