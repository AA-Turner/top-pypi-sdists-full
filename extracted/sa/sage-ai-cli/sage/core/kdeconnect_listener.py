"""
KDE Connect listener for SAGE — transparent takeover (macOS, Linux, Windows).

KDE Connect normally consumes inbound SMS inside its own GUI process and
exposes them to other apps unevenly across platforms (DBus on Linux is
flaky in some builds; the macOS App Store version's DBus registration is
broken; Windows has no DBus at all). To make inbound SMS reach SAGE on
every platform without requiring users to re-pair, SAGE temporarily
takes over the kdeconnectd role:

    1. On bridge start: stop the OS kdeconnectd
    2. Read certs from the platform-specific KDE Connect config dir
       (already paired, so the phone keeps recognizing us)
    3. Bind UDP 1716 + TCP 1716
    4. Wait for the phone's UDP discovery broadcast
    5. TCP-connect to phone:tcpPort using the OS daemon's identity
    6. The phone sees its existing paired desktop and accepts immediately
    7. Receive SMS, dispatch through bridge; send replies over same socket
    8. On bridge stop: restart kdeconnectd

Cross-platform notes:

* Config / cert location is determined by `_kde_config_dir()` per OS.
* Daemon stop/restart routes through `taskkill` on Windows, `pkill` /
  `pgrep` elsewhere.
* Cert CN extraction tries the `cryptography` library first, then falls
  back to the `openssl` CLI, then to a stdlib-only ASN.1 reader. At
  least one of these works on every platform we support.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import socket
import ssl
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Callable

logger = logging.getLogger("sage.kdeconnect_listener")


# ── Platform-specific paths and commands ─────────────────────────────────

def _kde_config_candidates() -> list[Path]:
    """All directories where KDE Connect might have stored its certs.

    Different KDE Connect versions (and packages: snap, flatpak, MS Store,
    homebrew, .deb, .pkg) end up in different roots. Returning every
    plausible location and probing each one means we don't lock the user
    into a single path that might not exist on their setup.
    """
    paths: list[Path] = []
    home = Path.home()

    if sys.platform == "darwin":
        paths += [
            home / "Library" / "Preferences" / "kdeconnect",
            home / "Library" / "Application Support" / "kdeconnect",
        ]
    elif sys.platform == "win32":
        for env in ("LOCALAPPDATA", "APPDATA"):
            base = os.environ.get(env)
            if base:
                paths.append(Path(base) / "kdeconnect")
        # Final fallbacks if env vars aren't set.
        paths += [
            home / "AppData" / "Local" / "kdeconnect",
            home / "AppData" / "Roaming" / "kdeconnect",
        ]
    else:
        # Linux + BSD: XDG_CONFIG_HOME + the most common install layouts
        # used by Debian/Ubuntu, Fedora, Arch, snap, flatpak.
        xdg = os.environ.get("XDG_CONFIG_HOME")
        if xdg:
            paths.append(Path(xdg) / "kdeconnect")
        paths += [
            home / ".config" / "kdeconnect",
            home / ".local" / "share" / "kdeconnect",
            home / "snap" / "kdeconnect" / "current" / ".config" / "kdeconnect",
            home / ".var" / "app" / "org.kde.kdeconnect" / "config" / "kdeconnect",
        ]

    # Deduplicate while preserving order
    seen: set[Path] = set()
    unique: list[Path] = []
    for p in paths:
        if p not in seen:
            seen.add(p)
            unique.append(p)
    return unique


def _resolve_kde_paths() -> tuple[Path, Path, Path]:
    """Find the KDE Connect config dir that actually has the cert + key.

    Returns (config_dir, cert, key). If none exist, returns the first
    candidate (so callers can still report the expected path).
    """
    candidates = _kde_config_candidates()
    for d in candidates:
        cert = d / "certificate.pem"
        key  = d / "privateKey.pem"
        if cert.exists() and key.exists():
            return d, cert, key
    # Nothing found — return the canonical default for messaging.
    default = candidates[0] if candidates else Path.home() / ".config" / "kdeconnect"
    return default, default / "certificate.pem", default / "privateKey.pem"


OS_KDC_DIR, OS_CERT, OS_KEY = _resolve_kde_paths()


def _kde_config_dir() -> Path:
    """Backwards-compat alias — returns the resolved config dir."""
    return OS_KDC_DIR

PROTOCOL_VERSION = 7
KDC_PORT         = 1716

# Tell the phone every packet type SAGE wants to receive. The Android KDE
# Connect app filters its outgoing packets by the peer's `incomingCapabilities`,
# so anything missing here is silently dropped on the phone side. We list
# every SMS-adjacent capability — the phone uses different ones depending on
# its KDE Connect version (older: telephony; newer: sms.messages; and
# sms.attachment_file for MMS).
INCOMING_CAPS = [
    "kdeconnect.sms.messages",
    "kdeconnect.sms.attachment_file",
    "kdeconnect.telephony",
    "kdeconnect.notification",
    "kdeconnect.notification.request",
    "kdeconnect.pair",
]
OUTGOING_CAPS = [
    "kdeconnect.sms.request",
    "kdeconnect.sms.request_conversations",
    "kdeconnect.sms.request_conversation",
    "kdeconnect.sms.request_attachment",
    "kdeconnect.notification.request",
    "kdeconnect.pair",
]


# ── Identity helpers ──────────────────────────────────────────────────────

def _extract_cn_via_cryptography(cert_path: Path) -> str | None:
    """Parse cert CN using the `cryptography` library. Returns None if
    the library isn't installed (we only require it as a soft dependency)."""
    try:
        from cryptography import x509
    except ImportError:
        return None
    try:
        cert = x509.load_pem_x509_certificate(cert_path.read_bytes())
        for attr in cert.subject:
            # NameOID.COMMON_NAME has dotted_string "2.5.4.3"
            if getattr(attr.oid, "dotted_string", "") == "2.5.4.3":
                return str(attr.value)
    except Exception as exc:
        logger.debug("cryptography parse failed for %s: %s", cert_path, exc)
    return None


def _extract_cn_via_openssl(cert_path: Path) -> str | None:
    """Parse cert CN by shelling out to `openssl`. Common on macOS and Linux,
    sometimes available on Windows via Git Bash."""
    if not shutil.which("openssl"):
        return None
    try:
        out = subprocess.run(
            ["openssl", "x509", "-in", str(cert_path), "-noout", "-subject"],
            capture_output=True, text=True, check=True, timeout=5,
        ).stdout.strip()
        # Output forms:
        #   "subject=O=KDE, OU=KDE Connect, CN=<deviceId>"
        #   "subject= O = KDE, OU = ..., CN = <deviceId>"
        for part in out.replace(",", " ").split():
            if part.startswith("CN="):
                return part[3:]
        import re
        m = re.search(r"CN\s*=\s*([^\s,/]+)", out)
        if m:
            return m.group(1)
    except Exception as exc:
        logger.debug("openssl parse failed for %s: %s", cert_path, exc)
    return None


def _extract_cn_via_stdlib(cert_path: Path) -> str | None:
    """Stdlib-only PEM cert CN reader. Used as a last resort on Windows
    boxes that have neither the cryptography library nor openssl in PATH.

    Walks the DER for the OID 2.5.4.3 (commonName) followed by a string
    tag (PrintableString / UTF8String / IA5String) and returns the value.
    Best-effort: returns None on any parse error.
    """
    try:
        import base64
        import re
        pem = cert_path.read_text(encoding="utf-8")
        m = re.search(
            r"-----BEGIN CERTIFICATE-----\s*(.+?)\s*-----END CERTIFICATE-----",
            pem,
            re.DOTALL,
        )
        if not m:
            return None
        der = base64.b64decode("".join(m.group(1).split()))
        cn_oid = bytes([0x06, 0x03, 0x55, 0x04, 0x03])  # 2.5.4.3
        idx = der.find(cn_oid)
        if idx < 0:
            return None
        after = idx + len(cn_oid)
        # X.520 commonName is wrapped in a SET → SEQUENCE → AttributeTypeAndValue
        # so the value tag follows the OID directly: tag, length, bytes.
        if after + 2 > len(der):
            return None
        tag = der[after]
        # PrintableString / UTF8String / IA5String / TeletexString / BMPString
        if tag not in (0x13, 0x0c, 0x16, 0x14, 0x1e):
            return None
        length = der[after + 1]
        cn_bytes = der[after + 2: after + 2 + length]
        return cn_bytes.decode("utf-8", errors="replace") or None
    except Exception as exc:
        logger.debug("stdlib parse failed for %s: %s", cert_path, exc)
    return None


def _read_cert_cn(cert_path: Path) -> str | None:
    """Try every available method for extracting a cert's CN.

    cryptography → openssl → stdlib ASN.1. At least one of these works on
    macOS, Linux, and Windows without forcing users to install extras.
    """
    for fn in (_extract_cn_via_cryptography, _extract_cn_via_openssl,
               _extract_cn_via_stdlib):
        cn = fn(cert_path)
        if cn:
            return cn
    return None


def _read_os_daemon_identity() -> tuple[str, Path, Path] | None:
    """Read OS kdeconnectd's deviceId from its cert CN. Returns (id, cert, key)."""
    if not OS_CERT.exists() or not OS_KEY.exists():
        return None
    cn = _read_cert_cn(OS_CERT)
    if cn:
        return cn, OS_CERT, OS_KEY
    logger.warning(
        "Couldn't extract deviceId from %s — install `pip install cryptography` "
        "or ensure `openssl` is in PATH.",
        OS_CERT,
    )
    return None


def _read_os_daemon_name() -> str:
    """Best-effort device name shown to the phone."""
    if sys.platform == "darwin":
        try:
            out = subprocess.run(
                ["scutil", "--get", "ComputerName"],
                capture_output=True, text=True, timeout=2,
            )
            if out.returncode == 0 and out.stdout.strip():
                return out.stdout.strip()
        except Exception:
            pass
    elif sys.platform == "win32":
        # Windows exposes the computer name via env var; falls back to
        # gethostname which is also fine on Windows.
        name = os.environ.get("COMPUTERNAME", "").strip()
        if name:
            return name
    try:
        return socket.gethostname().split(".")[0]
    except Exception:
        return "Sage"


# ── Wire protocol helpers ────────────────────────────────────────────────

def _identity_packet(device_id: str, name: str, tcp_port: int) -> dict:
    return {
        "id":   int(time.time() * 1000),
        "type": "kdeconnect.identity",
        "body": {
            "deviceId":             device_id,
            "deviceName":           name,
            "deviceType":           "desktop",
            "incomingCapabilities": INCOMING_CAPS,
            "outgoingCapabilities": OUTGOING_CAPS,
            "protocolVersion":      PROTOCOL_VERSION,
            "tcpPort":              tcp_port,
        },
    }


def _send_packet(sock, packet: dict) -> None:
    raw = (json.dumps(packet) + "\n").encode("utf-8")
    sock.sendall(raw)


def _recv_packet(sock, buf: bytearray) -> dict | None:
    while b"\n" not in buf:
        try:
            chunk = sock.recv(4096)
        except OSError as exc:
            if getattr(exc, "errno", None) in (57, 32):
                if not buf: return None
                break
            raise
        if not chunk:
            if not buf: return None
            break
        buf.extend(chunk)
    if b"\n" not in buf:
        return None
    line, _, rest = bytes(buf).partition(b"\n")
    buf[:] = rest
    try:
        return json.loads(line.decode("utf-8"))
    except Exception:
        return None


# ── Daemon lifecycle ──────────────────────────────────────────────────────

_DAEMON_NAMES = (
    ("kdeconnectd.exe", "kdeconnectd")
    if sys.platform == "win32"
    else ("kdeconnectd",)
)


def _find_kdeconnectd() -> str | None:
    """Locate the kdeconnectd binary path so we can restart it on shutdown.

    Per-platform install locations differ; we check the common ones, then
    fall back to PATH (Linux's apt/dnf packages put it on PATH).
    """
    candidates: list[str] = []
    if sys.platform == "darwin":
        candidates += [
            "/Applications/KDE Connect.app/Contents/MacOS/kdeconnectd",
            os.path.expanduser("~/Applications/KDE Connect.app/Contents/MacOS/kdeconnectd"),
        ]
    elif sys.platform == "win32":
        # KDE Connect Windows installer puts it under Program Files; also
        # the Microsoft Store version may live elsewhere — best effort.
        candidates += [
            r"C:\Program Files\KDE Connect\kdeconnectd.exe",
            r"C:\Program Files (x86)\KDE Connect\kdeconnectd.exe",
        ]
        local_appdata = os.environ.get("LOCALAPPDATA")
        if local_appdata:
            candidates.append(os.path.join(local_appdata, "Programs", "KDE Connect", "bin", "kdeconnectd.exe"))
        candidates.append(os.path.expanduser("~/AppData/Local/Programs/KDE Connect/bin/kdeconnectd.exe"))
    else:
        candidates += [
            "/usr/bin/kdeconnectd",
            "/usr/lib/x86_64-linux-gnu/libexec/kdeconnectd",
            "/usr/libexec/kdeconnectd",
            "/usr/lib/kde6/libexec/kdeconnectd",
            "/usr/lib/kdeconnectd",
        ]
    for c in candidates:
        if os.path.exists(c):
            return c
    for name in _DAEMON_NAMES:
        found = shutil.which(name)
        if found:
            return found
    return None


def _is_daemon_running() -> bool:
    """Return True if any kdeconnectd process is currently alive."""
    try:
        if sys.platform == "win32":
            r = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq kdeconnectd.exe"],
                capture_output=True, text=True, timeout=3,
            )
            return "kdeconnectd.exe" in (r.stdout or "").lower()
        # POSIX: pgrep is on every modern macOS and Linux
        r = subprocess.run(
            ["pgrep", "-x", "kdeconnectd"],
            capture_output=True, timeout=3,
        )
        return r.returncode == 0
    except Exception:
        return False


def _free_port_1716() -> int:
    """Force-free TCP/UDP 1716 by killing whatever process holds it.

    More aggressive than `_stop_os_daemon` (which targets the daemon by
    name): finds the PID currently listening on 1716 via OS-specific
    commands and force-kills it, regardless of process name.

    Returns the number of PIDs killed so callers can decide whether to
    retry bind. Always best-effort; failures are silently logged.
    """
    pids: set[int] = set()
    try:
        if sys.platform == "win32":
            # netstat -ano shows the LOCAL_ADDR:PORT and PID. We want
            # entries listening on :1716.
            r = subprocess.run(
                ["netstat", "-ano"],
                capture_output=True, text=True, timeout=5,
            )
            for raw in (r.stdout or "").splitlines():
                line = raw.strip()
                if ":1716 " not in line and not line.endswith(":1716"):
                    continue
                if "LISTENING" not in line.upper() and "UDP" not in line.upper():
                    continue
                parts = line.split()
                if parts and parts[-1].isdigit():
                    pids.add(int(parts[-1]))
        else:
            # POSIX: try lsof, ss, fuser in order. Different distros ship
            # different ones; we only need one to work.
            for cmd_args in (
                ["lsof", "-iTCP:1716", "-sTCP:LISTEN", "-t"],
                ["lsof", "-i", ":1716", "-t"],
                ["fuser", "1716/tcp"],
                ["fuser", "1716/udp"],
            ):
                try:
                    r = subprocess.run(
                        cmd_args, capture_output=True, text=True, timeout=3,
                    )
                    if r.returncode == 0:
                        for tok in (r.stdout or "").split():
                            tok = tok.strip(":")
                            if tok.isdigit():
                                pids.add(int(tok))
                        if pids:
                            break
                except FileNotFoundError:
                    continue
                except Exception:
                    continue
    except Exception as exc:
        logger.debug("Port 1716 lookup failed: %s", exc)
        return 0

    killed = 0
    for pid in pids:
        try:
            if sys.platform == "win32":
                subprocess.run(
                    ["taskkill", "/F", "/PID", str(pid)],
                    capture_output=True, timeout=3,
                )
            else:
                os.kill(pid, 9)
            logger.info("Freed port 1716 by killing PID %d", pid)
            killed += 1
        except Exception as exc:
            logger.debug("Couldn't kill PID %d: %s", pid, exc)

    if killed:
        # Give the OS a beat to actually release the socket
        time.sleep(1.0)
    return killed


def _stop_os_daemon() -> bool:
    """Stop the OS kdeconnectd. Returns True once the process is gone.

    Aggressive on Windows: tries `taskkill /IM` first, then iterates
    every PID `tasklist` reports and force-kills each one with
    `taskkill /F /PID`. KDE Connect Windows occasionally has multiple
    kdeconnectd.exe processes (the daemon plus a watcher), and a single
    /IM kill misses the watcher which then respawns the daemon.
    """
    try:
        if sys.platform == "win32":
            # Pass 1: kill by image name.
            subprocess.run(
                ["taskkill", "/IM", "kdeconnectd.exe", "/F", "/T"],
                capture_output=True, timeout=5,
            )
            # Pass 2: enumerate any survivors and kill by PID. Some
            # Windows builds spawn helper processes that don't go down
            # on /IM alone.
            try:
                r = subprocess.run(
                    ["tasklist", "/FI", "IMAGENAME eq kdeconnectd.exe", "/FO", "CSV", "/NH"],
                    capture_output=True, text=True, timeout=3,
                )
                for line in (r.stdout or "").splitlines():
                    # CSV: "kdeconnectd.exe","1234","Console","1","12,345 K"
                    parts = [p.strip().strip('"') for p in line.split(",")]
                    if len(parts) >= 2 and parts[1].isdigit():
                        subprocess.run(
                            ["taskkill", "/F", "/PID", parts[1]],
                            capture_output=True, timeout=3,
                        )
            except Exception as exc:
                logger.debug("Per-PID kill loop failed: %s", exc)
        else:
            # POSIX: pkill, then SIGKILL stragglers.
            subprocess.run(
                ["pkill", "-x", "kdeconnectd"],
                capture_output=True, timeout=5,
            )
            time.sleep(1)
            subprocess.run(
                ["pkill", "-9", "-x", "kdeconnectd"],
                capture_output=True, timeout=5,
            )

        # Wait for the port to free up — checking process presence rather
        # than a fixed sleep so this is fast on a fast box and patient on
        # a slow one.
        for _ in range(20):
            time.sleep(0.5)
            if not _is_daemon_running():
                return True
        return False
    except Exception as exc:
        logger.warning("Couldn't stop kdeconnectd: %s", exc)
        return False


def _start_os_daemon() -> None:
    """Restart kdeconnectd in the background (used on shutdown)."""
    daemon = _find_kdeconnectd()
    if not daemon:
        logger.info("kdeconnectd not found on this machine — nothing to restart.")
        return
    try:
        if sys.platform == "win32":
            # DETACHED_PROCESS keeps the daemon alive after sage exits;
            # CREATE_NO_WINDOW hides the console window the daemon would
            # otherwise pop up under cmd.exe.
            DETACHED_PROCESS  = 0x00000008
            CREATE_NO_WINDOW  = 0x08000000
            subprocess.Popen(
                [daemon],
                creationflags=DETACHED_PROCESS | CREATE_NO_WINDOW,
                close_fds=True,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            subprocess.Popen(
                [daemon],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                start_new_session=True,
            )
    except Exception as exc:
        logger.warning("Couldn't restart kdeconnectd: %s", exc)


# ── Listener ──────────────────────────────────────────────────────────────

class KDEConnectInboundListener:
    """SAGE's KDE Connect implementation. Replaces kdeconnectd while running.

    Re-uses the OS daemon's existing pairing identity so the user's Pixel
    sees the same Maclan device — no re-pair needed.
    """

    def __init__(self, callback: Callable[[dict], None],
                 sage_device_name: str = "") -> None:
        self.callback = callback
        self.device_name = sage_device_name  # ignored — we use Maclan's name
        self._stop = threading.Event()
        # Active TLS session (one per phone)
        self._sessions: dict[str, ssl.SSLSocket] = {}
        self._sessions_lock = threading.Lock()
        self._takeover_active = False

    def start(self) -> bool:
        """Take over kdeconnectd's role and start listening.

        Safety: if no Pixel TLS session establishes within 90 seconds, we
        auto-revert (restart kdeconnectd) so the user's pairing is never at
        risk for long. Auto-revert applies even if the bridge keeps running.
        """
        # Diagnostic header — these lines land in ~/.sage/sms.log so users
        # can see exactly which paths/files we're using if takeover fails.
        logger.info("KDE Connect takeover starting:")
        logger.info("  config dir : %s (exists=%s)", OS_KDC_DIR, OS_KDC_DIR.exists())
        logger.info("  cert file  : %s (exists=%s)", OS_CERT, OS_CERT.exists())
        logger.info("  key  file  : %s (exists=%s)", OS_KEY, OS_KEY.exists())
        logger.info("  daemon bin : %s", _find_kdeconnectd() or "<not found>")
        logger.info("  daemon up  : %s", _is_daemon_running())

        ident = _read_os_daemon_identity()
        if not ident:
            logger.info(
                "OS kdeconnectd identity not found at %s — pair your phone "
                "via the GUI app once before running `sage sms start`.",
                OS_CERT,
            )
            return False
        self._device_id, self._cert, self._key = ident
        self._actual_name = _read_os_daemon_name()
        logger.info(
            "Identity loaded: deviceId=%s, name=%s",
            self._device_id, self._actual_name,
        )

        if not _stop_os_daemon():
            logger.warning(
                "Couldn't stop kdeconnectd cleanly — port 1716 may be busy. "
                "If TLS handshake fails below, manually stop kdeconnectd "
                "(macOS: quit KDE Connect.app; Linux: `pkill kdeconnectd`; "
                "Windows: end kdeconnectd.exe in Task Manager) and retry."
            )
        else:
            logger.info("kdeconnectd stopped — port 1716 free for SAGE")

        self._takeover_active = True
        self._takeover_started_at = time.time()
        threading.Thread(target=self._run, daemon=True,
                         name="sage-kdeconnect-takeover").start()
        threading.Thread(target=self._safety_watchdog, daemon=True,
                         name="sage-kdeconnect-watchdog").start()
        # Respawn watchdog: Windows (and some Linux setups) auto-restart
        # kdeconnectd after we kill it. If kdeconnectd comes back, the
        # phone's TLS connection goes there instead of SAGE — sage binds
        # 1716 with REUSEADDR but the kernel arbitrates and traffic ends
        # up at the wrong process. Solution: keep killing it.
        # This is the missing piece for the user-reported "outbound works
        # after sage sms start" symptom (which means kdeconnectd is
        # alive, which means takeover never actually took over).
        threading.Thread(target=self._respawn_watchdog, daemon=True,
                         name="sage-kdeconnect-respawn-watchdog").start()
        return True

    def _respawn_watchdog(self) -> None:
        """Re-kill kdeconnectd if it respawns during the takeover.

        Polls every 3 seconds. If kdeconnectd comes back, kills it
        immediately and force-frees port 1716 — without this, Windows's
        kdeconnect-indicator restarts the daemon within seconds and
        steals the phone's traffic from SAGE.
        """
        while not self._stop.is_set() and self._takeover_active:
            time.sleep(3)
            if self._stop.is_set() or not self._takeover_active:
                return
            if _is_daemon_running():
                logger.warning(
                    "kdeconnectd respawned during takeover — re-killing so "
                    "phone traffic stays with SAGE"
                )
                _stop_os_daemon()
                # Belt and suspenders: also force-free the port in case
                # something else has it. Catches the scenario where
                # KDE Connect spawns a helper process under a different
                # name that holds the port.
                _free_port_1716()

    def _safety_watchdog(self) -> None:
        """If no TLS session within 90s, auto-revert to OS daemon."""
        deadline = self._takeover_started_at + 90
        while time.time() < deadline and not self._stop.is_set():
            with self._sessions_lock:
                if self._sessions:
                    logger.info("Watchdog: TLS session(s) established, takeover stable")
                    return
            time.sleep(2)
        if self._stop.is_set():
            return
        with self._sessions_lock:
            sessions = bool(self._sessions)
        if not sessions:
            logger.warning(
                "Watchdog: no TLS session within 90s — auto-reverting to "
                "kdeconnectd to preserve pairing"
            )
            self._stop.set()
            self._takeover_active = False
            _start_os_daemon()

    def stop(self) -> None:
        self._stop.set()
        # Close any active TLS sessions
        with self._sessions_lock:
            for sock in self._sessions.values():
                try: sock.close()
                except Exception: pass
            self._sessions.clear()
        # Restore OS daemon
        if self._takeover_active:
            self._takeover_active = False
            _start_os_daemon()

    def send_sms(self, phone_number: str, text: str) -> bool:
        """Send an SMS through any active session. Returns True if dispatched."""
        with self._sessions_lock:
            if not self._sessions:
                return False
            sock = next(iter(self._sessions.values()))
        try:
            _send_packet(sock, {
                "id": int(time.time() * 1000),
                "type": "kdeconnect.sms.request",
                "body": {
                    "version":           2,
                    "sendSms":           True,
                    "phoneNumber":       phone_number,
                    "messageBody":       text,
                    # Some KDE Connect versions also accept this format:
                    "addresses":         [{"address": phone_number}],
                    "messageText":       text,
                },
            })
            return True
        except Exception as exc:
            logger.warning("send_sms failed: %s", exc)
            return False

    # ── Main loop ────────────────────────────────────────────────────────

    def _run(self) -> None:
        def _try_bind_udp() -> socket.socket | None:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                try:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                except (AttributeError, OSError):
                    pass
                s.bind(("0.0.0.0", KDC_PORT))
                s.settimeout(1)
                return s
            except OSError as exc:
                self._last_bind_err = exc
                return None

        def _try_bind_tcp() -> socket.socket | None:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(("0.0.0.0", KDC_PORT))
                s.listen(4)
                s.settimeout(1)
                return s
            except OSError as exc:
                self._last_bind_err = exc
                return None

        # Bind UDP 1716 — for receiving Pixel discovery broadcasts
        udp = _try_bind_udp()
        if udp is None:
            # First bind failed. Force-free the port (kills WHATEVER process
            # holds it, even if it's not kdeconnectd by name) and retry.
            logger.warning(
                "UDP %d bind failed (%s) — forcing port free and retrying",
                KDC_PORT, self._last_bind_err,
            )
            killed = _free_port_1716()
            if killed:
                udp = _try_bind_udp()
        if udp is None:
            logger.error(
                "❌ Couldn't bind UDP %d after force-free: %s. kdeconnectd "
                "running=%s. Manually stop whatever holds the port and retry "
                "`sage sms start`.\n"
                "  Windows: `Get-NetUDPEndpoint -LocalPort 1716` then `Stop-Process -Id <PID> -Force`\n"
                "  POSIX:   `lsof -iUDP:1716` then `kill -9 <PID>`",
                KDC_PORT, self._last_bind_err, _is_daemon_running(),
            )
            return
        logger.info("✓ Bound UDP %d", KDC_PORT)

        # Bind TCP 1716 — the Pixel reconnects via TCP to our paired peer's
        # known port after a network drop, NOT via UDP broadcast every time.
        # Without this listener, Pixel's reconnect attempts get RST.
        tcp = _try_bind_tcp()
        if tcp is None:
            logger.warning(
                "TCP %d bind failed (%s) — forcing port free and retrying",
                KDC_PORT, self._last_bind_err,
            )
            killed = _free_port_1716()
            if killed:
                tcp = _try_bind_tcp()
        if tcp is None:
            logger.error(
                "❌ Couldn't bind TCP %d after force-free: %s. Phone won't "
                "be able to reconnect to SAGE. Check Windows Firewall: open "
                "'Allow an app through Windows Defender Firewall', tick "
                "Python on both Private and Public.",
                KDC_PORT, self._last_bind_err,
            )
            udp.close()
            return
        logger.info("✓ Bound TCP %d (listening for phone reconnect)", KDC_PORT)

        logger.info(
            "SAGE KDE Connect takeover: identity=%s (%s), UDP+TCP %d",
            self._device_id, self._actual_name, KDC_PORT,
        )

        # Send our identity broadcast — paired phones immediately TCP back.
        self._broadcast_identity_once()

        while not self._stop.is_set():
            # UDP discovery
            try:
                data, addr = udp.recvfrom(4096)
                if addr[0] not in self._self_addresses():
                    self._handle_udp_identity(data, addr[0])
            except socket.timeout:
                pass
            except Exception as exc:
                logger.debug("UDP loop error: %s", exc)
            # TCP accept (Pixel reconnecting)
            try:
                conn, addr = tcp.accept()
                threading.Thread(
                    target=self._handle_inbound_tcp, args=(conn, addr),
                    daemon=True, name=f"sage-kdc-in-{addr[0]}",
                ).start()
            except socket.timeout:
                pass
            except OSError:
                break

        udp.close()
        try: tcp.close()
        except Exception: pass

    def _handle_inbound_tcp(self, sock: socket.socket, addr) -> None:
        """Pixel reconnects via TCP to our well-known port. Detect protocol
        (TLS-immediately for paired devices, plain identity for new) and
        complete the handshake.
        """
        try:
            sock.setblocking(True)
            sock.settimeout(8)

            logger.info("📡 Inbound TCP from %s — peeking first byte...", addr)
            try:
                first = sock.recv(1, socket.MSG_PEEK)
            except OSError as exc:
                logger.warning("Inbound %s peek failed: %s", addr, exc)
                sock.close()
                return
            if not first:
                logger.warning("Inbound %s closed before any data", addr)
                sock.close()
                return

            logger.info("📡 Inbound %s first byte = 0x%02x ('%s')",
                        addr, first[0], chr(first[0]) if 32 <= first[0] < 127 else '?')
            if first[0] == 0x16:
                logger.info("📡 TLS-first protocol — paired Pixel reconnecting")
                self._handle_tls_first_inbound(sock, addr)
                return

            # Plain text path: peer sends identity unencrypted first
            buf = bytearray()
            peer_pkt = _recv_packet(sock, buf)
            if not peer_pkt or peer_pkt.get("type") != "kdeconnect.identity":
                sock.close(); return
            body = peer_pkt.get("body", {}) or {}
            peer_id   = body.get("deviceId", "")
            peer_name = body.get("deviceName", peer_id)
            logger.info("Inbound TCP identity from %s (%s)", peer_name, peer_id)

            try:
                _send_packet(sock, _identity_packet(self._device_id,
                                                    self._actual_name, KDC_PORT))
            except OSError:
                sock.close(); return

            # TCP-server-side: TLS server. CERT_NONE because Android KDE
            # Connect uses self-signed certs and pins peers by SHA256
            # fingerprint out-of-band (during pairing), not via CA chain.
            # CERT_OPTIONAL was the previous setting and silently rejected
            # every real phone with CERTIFICATE_VERIFY_FAILED — Python's
            # CERT_OPTIONAL tries to verify against the system trust
            # store, which never contains a phone's self-signed cert.
            # That single bug was the root cause of inbound SMS never
            # arriving at SAGE on the user's machine.
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ctx.load_cert_chain(certfile=str(self._cert), keyfile=str(self._key))
            ctx.verify_mode = ssl.CERT_NONE
            ctx.minimum_version = ssl.TLSVersion.TLSv1_2
            try:
                tls = ctx.wrap_socket(sock, server_side=True,
                                      do_handshake_on_connect=True)
            except ssl.SSLError as exc:
                logger.warning("TLS handshake from %s failed: %s", peer_name, exc)
                sock.close(); return

            self._run_tls_session(tls, peer_id, peer_name, ssl_buf=bytearray())
        except Exception as exc:
            logger.info("Inbound %s ended: %s", addr, exc)
            try: sock.close()
            except Exception: pass

    def _handle_tls_first_inbound(self, sock: socket.socket, addr) -> None:
        """Paired Pixel reconnect: it sends TLS ClientHello immediately."""
        # CERT_NONE: see comment in _handle_inbound_tcp above. The phone's
        # self-signed cert can't be verified via CA chain; KDE Connect's
        # trust model is fingerprint-pinning at pair time.
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(certfile=str(self._cert), keyfile=str(self._key))
        ctx.verify_mode = ssl.CERT_NONE
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2

        try:
            tls = ctx.wrap_socket(sock, server_side=True,
                                  do_handshake_on_connect=True)
        except ssl.SSLError as exc:
            logger.warning("TLS-first from %s failed: %s", addr, exc)
            sock.close(); return

        # Exchange identity over TLS
        ssl_buf = bytearray()
        try:
            _send_packet(tls, _identity_packet(self._device_id,
                                               self._actual_name, KDC_PORT))
            tls.settimeout(10)
            peer_pkt = _recv_packet(tls, ssl_buf)
        except Exception as exc:
            logger.warning("TLS identity exchange %s failed: %s", addr, exc)
            tls.close(); return

        if not peer_pkt or peer_pkt.get("type") != "kdeconnect.identity":
            logger.warning("TLS-first %s no identity: %s", addr, peer_pkt)
            tls.close(); return
        body = peer_pkt.get("body", {}) or {}
        peer_id   = body.get("deviceId", "")
        peer_name = body.get("deviceName", peer_id)
        logger.info("✓ TLS-first session with %s (%s)", peer_name, peer_id)

        self._run_tls_session(tls, peer_id, peer_name, ssl_buf)

    def _run_tls_session(self, tls: ssl.SSLSocket, peer_id: str,
                         peer_name: str, ssl_buf: bytearray) -> None:
        """After TLS + identity exchange, subscribe to SMS and dispatch packets.
        Already paired — no pair handshake needed.
        """
        with self._sessions_lock:
            self._sessions[peer_id] = tls

        logger.info("✅ TLS session ready with %s — subscribing to SMS", peer_name)

        # Send every subscription request the SMS plugin recognizes. Different
        # KDE Connect Android versions push events on different triggers:
        # * Older builds proactively send `kdeconnect.telephony` for new SMS
        #   regardless of subscription.
        # * 1.4+ sends `kdeconnect.sms.messages` proactively to all paired
        #   devices that listed sms.messages in their incomingCapabilities.
        # * Some builds wait for an explicit `request_conversations` ping
        #   before they start streaming. Sending all three is safe — the
        #   phone will just answer whichever it understands.
        for sub_type in (
            "kdeconnect.sms.request_conversations",
            "kdeconnect.notification.request",  # ask phone for current notifications too
        ):
            try:
                _send_packet(tls, {
                    "id": int(time.time() * 1000),
                    "type": sub_type,
                    "body": {"request": True},
                })
                logger.info("   → sent %s", sub_type)
            except Exception as exc:
                logger.warning("subscribe %s failed: %s", sub_type, exc)

        last_seen = [int(time.time() * 1000)]
        # Generous timeout — KDE Connect's keep-alive is silent for long
        # stretches between SMS. 60s used to cause us to break the loop on
        # idle networks; bump to 5 minutes and rely on socket errors rather
        # than timeouts to detect connection loss.
        tls.settimeout(300)
        try:
            while not self._stop.is_set():
                try:
                    packet = _recv_packet(tls, ssl_buf)
                except socket.timeout:
                    continue
                except Exception as exc:
                    logger.info("Lost %s: %s", peer_name, exc)
                    break
                if packet is None:
                    logger.info("Lost %s: peer closed", peer_name)
                    break
                # Diagnostic: log every packet type we receive so users can
                # tell us what the phone is actually sending. Body keys only
                # (no values) — keeps SMS contents out of logs.
                ptype = packet.get("type", "?")
                bkeys = list((packet.get("body") or {}).keys())
                logger.info("📨 %s ← %s body=%s", ptype, peer_name, bkeys)
                self._handle_packet(packet, peer_name, last_seen)
        finally:
            with self._sessions_lock:
                self._sessions.pop(peer_id, None)
            try: tls.close()
            except Exception: pass

    def _self_addresses(self) -> set[str]:
        out = {"127.0.0.1"}
        try:
            for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
                out.add(info[4][0])
        except Exception:
            pass
        return out

    def _broadcast_targets(self) -> list[str]:
        targets = ["255.255.255.255"]
        try:
            for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
                ip = info[4][0]
                if ip.startswith(("127.", "169.254.")):
                    continue
                parts = ip.split(".")
                if len(parts) == 4:
                    targets.append(".".join(parts[:3]) + ".255")
        except Exception:
            pass
        return list(dict.fromkeys(targets))

    def _broadcast_identity_once(self) -> None:
        """Send a UDP identity broadcast so paired phones notice us coming back."""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        try:
            ident = _identity_packet(self._device_id, self._actual_name, KDC_PORT)
            raw = (json.dumps(ident) + "\n").encode("utf-8")
            for target in self._broadcast_targets():
                try: s.sendto(raw, (target, KDC_PORT))
                except Exception: pass
        finally:
            s.close()

    def _handle_udp_identity(self, data: bytes, source_ip: str) -> None:
        try:
            pkt = json.loads(data.decode("utf-8").strip())
        except Exception:
            return
        if pkt.get("type") != "kdeconnect.identity":
            return
        body = pkt.get("body", {}) or {}
        peer_id = body.get("deviceId", "")
        peer_name = body.get("deviceName", peer_id)
        peer_type = body.get("deviceType", "")
        peer_tcp = int(body.get("tcpPort", 0)) or KDC_PORT
        if peer_type not in ("phone", "tablet", "smartphone"):
            return
        if not peer_id:
            return
        # Skip if we already have a session
        with self._sessions_lock:
            if peer_id in self._sessions:
                return
        logger.info("Discovered phone %s (%s) at %s:%d — connecting",
                    peer_name, peer_id, source_ip, peer_tcp)
        threading.Thread(
            target=self._connect_and_run, args=(source_ip, peer_tcp, peer_id, peer_name),
            daemon=True, name=f"sage-kdc-{peer_name}",
        ).start()

    # ── Per-peer TLS session ─────────────────────────────────────────────

    def _connect_and_run(self, ip: str, port: int, peer_id: str, peer_name: str) -> None:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(15)
            sock.connect((ip, port))
        except Exception as exc:
            logger.warning("TCP connect to %s failed: %s", peer_name, exc)
            return

        # Identity exchange: TCP CLIENT (us) sends first
        try:
            _send_packet(sock, _identity_packet(self._device_id, self._actual_name, KDC_PORT))
            buf = bytearray()
            peer_pkt = _recv_packet(sock, buf)
        except Exception as exc:
            logger.warning("Identity exchange with %s failed: %s", peer_name, exc)
            sock.close()
            return
        if not peer_pkt or peer_pkt.get("type") != "kdeconnect.identity":
            logger.warning("No peer identity from %s: %s", peer_name, peer_pkt)
            sock.close()
            return

        # TLS upgrade: TCP CLIENT = TLS CLIENT
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.load_cert_chain(certfile=str(self._cert), keyfile=str(self._key))
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE  # peer cert pinned out-of-band by KDE Connect
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2

        try:
            tls = ctx.wrap_socket(sock, server_hostname=peer_id or "kdeconnect",
                                  do_handshake_on_connect=True)
        except ssl.SSLError as exc:
            logger.warning("TLS handshake with %s failed: %s — pairing may be broken; "
                           "open KDE Connect.app once to re-pair", peer_name, exc)
            sock.close()
            return

        logger.info("✓ TLS session established with %s", peer_name)
        self._run_tls_session(tls, peer_id, peer_name, ssl_buf=bytearray())

    def _handle_packet(self, packet: dict, peer_name: str, last_seen: list) -> None:
        ptype = packet.get("type", "")
        body  = packet.get("body", {}) or {}

        if ptype == "kdeconnect.telephony":
            # Older KDE Connect Android sends incoming-SMS events as a
            # telephony packet with event=sms.
            if (body.get("event") or "").lower() != "sms":
                return
            sender = (body.get("phoneNumber")
                      or body.get("contactName")
                      or "")
            text   = (body.get("messageBody")
                      or body.get("messageText")
                      or body.get("body")
                      or "")
            if sender and text:
                self._dispatch(sender, text)
            return

        if ptype == "kdeconnect.sms.messages":
            messages = body.get("messages") or []
            if not messages and body.get("body"):
                # Some build variants flatten a single-message push.
                messages = [body]
            last_ts = last_seen[0]
            for m in messages:
                # Drafts are noise — skip them. But accept inbox (1) and
                # sent (2) both, because self-SMS (texting your own number)
                # often only surfaces as type=2 in some Android builds, and
                # the user explicitly asked for that flow to work. Feedback
                # loops from sage's own replies are filtered below by body
                # marker, not by type.
                m_type = m.get("type")
                try:
                    if m_type is not None and int(m_type) == 3:  # draft
                        continue
                except (TypeError, ValueError):
                    pass

                # Date is best-effort — keep the last_seen high-water mark
                # but don't drop messages purely because the date is older
                # (clock skew between phone and PC is common).
                try:
                    date = int(m.get("date", 0))
                except (TypeError, ValueError):
                    date = 0

                # Sender extraction — addresses can be a list of dicts, a
                # list of strings, a single dict, or just a string field.
                sender = _extract_sms_sender(m)
                # Body extraction — try every field name we've seen in the
                # wild.
                text = (m.get("body")
                        or m.get("messageBody")
                        or m.get("messageText")
                        or m.get("text")
                        or "").strip()

                if not sender or not text:
                    logger.debug(
                        "SMS message dropped — sender=%r text-len=%d",
                        sender, len(text),
                    )
                    continue
                # Feedback protection: SAGE's own outbound replies start
                # with "[SAGE — ". When the user texts their own number,
                # KDE Connect re-broadcasts every SMS the phone sees,
                # including sage's reply. Without this filter, sage would
                # see its own reply, treat it as a new task, reply again,
                # and loop forever.
                if text.startswith("[SAGE"):
                    logger.debug(
                        "SMS message dropped — looks like SAGE's own reply (feedback)",
                    )
                    if date > last_seen[0]:
                        last_seen[0] = date
                    continue
                logger.info("📩 SMS from %s (%d chars, type=%s) — dispatching",
                            sender, len(text), m_type)
                self._dispatch(sender, text)
                if date > last_seen[0]:
                    last_seen[0] = date
            return

        if ptype == "kdeconnect.notification":
            # Some Android setups (particularly when the SMS plugin is
            # disabled or lacks RECEIVE_SMS permission) only forward SMS as
            # OS notifications. The notification packet's appName is the
            # user's SMS app (e.g. "Messages", "Google Messages"); title is
            # the sender name/number; text is the message body.
            app    = (body.get("appName") or "").lower()
            title  = (body.get("title") or "").strip()
            text   = (body.get("text") or "").strip()
            ticker = (body.get("ticker") or "").strip()
            sms_apps = ("messages", "messaging", "sms", "mms", "google messages")
            if not any(needle in app for needle in sms_apps):
                return
            if title and text:
                self._dispatch(title, text)
            elif ticker:
                # ticker format is often "Sender: body"
                if ":" in ticker:
                    sender, _, body_text = ticker.partition(":")
                    if sender.strip() and body_text.strip():
                        self._dispatch(sender.strip(), body_text.strip())
            return

    def _dispatch(self, sender: str, text: str) -> None:
        try:
            self.callback({"from": sender, "text": text, "service": "SMS"})
        except Exception as exc:
            logger.warning("SMS callback failed: %s", exc)


def _extract_sms_sender(m: dict) -> str:
    """Return a phone-number string from any KDE Connect SMS message shape.

    Different KDE Connect builds send the address in different places:
      * `addresses`: [{"address": "+1..."}]   (most common, post-1.3)
      * `addresses`: ["+1..."]                (some builds)
      * `address`:   "+1..."                  (single-address shape)
      * `phoneNumber`: "+1..."                (legacy field, telephony plugin)
      * `from`:      "+1..."                  (rare)
    """
    addrs = m.get("addresses")
    if addrs:
        first = addrs[0]
        if isinstance(first, dict):
            v = first.get("address")
            if v:
                return str(v)
        elif isinstance(first, str) and first.strip():
            return first.strip()
    for key in ("address", "phoneNumber", "phone_number", "from"):
        v = m.get(key)
        if v:
            return str(v).strip()
    return ""


# ── Coexistence mode ─────────────────────────────────────────────────────
#
# Runs alongside the OS kdeconnectd as a SEPARATE paired device — no
# takeover, no daemon kill, no port stealing. SAGE generates its own
# cert+key, broadcasts its own identity, and the user pairs once on
# their phone.
#
# This is the cross-platform path that has the highest chance of
# working. The takeover approach above depends on too many things going
# right (pairing certs in a known location, kdeconnectd actually
# stopping when killed, port 1716 freeing up immediately, the phone
# trusting the same identity from a process other than kdeconnectd).
# Coexist sidesteps all of those.

SAGE_KDE_DIR        = Path.home() / ".sage" / "kdeconnect"
SAGE_CERT           = SAGE_KDE_DIR / "certificate.pem"
SAGE_KEY            = SAGE_KDE_DIR / "privateKey.pem"
SAGE_DEVICE_ID_FILE = SAGE_KDE_DIR / "device_id.txt"
SAGE_TRUSTED_FILE   = SAGE_KDE_DIR / "trusted.json"


def _ensure_sage_device_id() -> str:
    """Stable per-machine device id. Generated once, persisted forever."""
    if SAGE_DEVICE_ID_FILE.exists():
        try:
            existing = SAGE_DEVICE_ID_FILE.read_text(encoding="utf-8").strip()
            if existing:
                return existing
        except Exception:
            pass
    import hashlib
    import uuid
    seed = f"sage-bridge-{uuid.getnode():x}-{socket.gethostname()}"
    device_id = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:32]
    SAGE_KDE_DIR.mkdir(parents=True, exist_ok=True)
    SAGE_DEVICE_ID_FILE.write_text(device_id, encoding="utf-8")
    return device_id


def _generate_cert_via_cryptography(device_id: str) -> bool:
    """Generate sage's cert+key using the `cryptography` library."""
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
    except ImportError:
        return False
    from datetime import datetime, timedelta, timezone

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "KDE"),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "KDE Connect"),
        x509.NameAttribute(NameOID.COMMON_NAME, device_id),
    ])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now(timezone.utc) - timedelta(days=1))
        .not_valid_after(datetime.now(timezone.utc) + timedelta(days=3650))
        .sign(key, hashes.SHA256())
    )
    SAGE_CERT.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    SAGE_KEY.write_bytes(
        key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    try:
        os.chmod(SAGE_KEY, 0o600)
    except Exception:
        pass
    return True


def _generate_cert_via_openssl(device_id: str) -> bool:
    """Generate cert+key by shelling out to the `openssl` CLI."""
    if not shutil.which("openssl"):
        return False
    subj = f"/O=KDE/OU=KDE Connect/CN={device_id}"
    try:
        subprocess.run(
            ["openssl", "req", "-x509", "-newkey", "rsa:2048",
             "-keyout", str(SAGE_KEY), "-out", str(SAGE_CERT),
             "-days", "3650", "-nodes", "-subj", subj],
            capture_output=True, check=True, timeout=30,
        )
        try:
            os.chmod(SAGE_KEY, 0o600)
        except Exception:
            pass
        return True
    except Exception as exc:
        logger.warning("openssl cert generation failed: %s", exc)
        return False


def _ensure_sage_certs(device_id: str) -> bool:
    """Make sure sage's KDE Connect cert+key exist; generate if missing.

    Tries `cryptography` lib first (clean, no external dep), falls back
    to `openssl` CLI, finally pip-installs `cryptography` and retries.
    Returns True if cert + key are present and usable.
    """
    if SAGE_CERT.exists() and SAGE_KEY.exists():
        return True
    SAGE_KDE_DIR.mkdir(parents=True, exist_ok=True)

    if _generate_cert_via_cryptography(device_id):
        logger.info("Generated SAGE KDE Connect cert at %s", SAGE_CERT)
        return True
    if _generate_cert_via_openssl(device_id):
        logger.info("Generated SAGE KDE Connect cert via openssl at %s", SAGE_CERT)
        return True

    # Last resort: pip-install cryptography and retry. Quiet to avoid
    # cluttering the user's terminal during normal `sage sms start`.
    logger.info("Installing `cryptography` library for KDE Connect cert generation...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--user", "--quiet", "cryptography"],
            capture_output=True, timeout=120,
        )
    except Exception as exc:
        logger.warning("pip install cryptography failed: %s", exc)
        return False
    if _generate_cert_via_cryptography(device_id):
        logger.info("Generated SAGE KDE Connect cert at %s", SAGE_CERT)
        return True
    logger.error(
        "Could not generate KDE Connect cert. Install one of: "
        "`pip install cryptography` OR ensure `openssl` is in PATH."
    )
    return False


class KDEConnectCoexistListener(KDEConnectInboundListener):
    """Run KDE Connect inbound SMS WITHOUT taking over kdeconnectd.

    SAGE registers as its own paired device ("SAGE Bridge — <hostname>"
    on the phone). The OS app keeps working normally; SMS gets sent to
    every paired device, including SAGE.

    First-time setup: user accepts a pairing prompt on their phone
    (one tap, similar to pairing the desktop app). After that, every
    `sage sms start` reconnects automatically.

    Why this exists: the takeover-based listener was unreliable across
    user setups (silent failures when kdeconnectd doesn't stop cleanly,
    when port 1716 stays bound, when the cert path differs from what we
    expect, when the phone refuses the impersonation handshake).
    Coexist mode trades a one-time pair tap for a much simpler, more
    reliable steady state.
    """

    def __init__(self, callback: Callable[[dict], None],
                 device_name: str = "") -> None:
        super().__init__(callback, device_name)
        self._actual_name = device_name or f"SAGE Bridge — {_read_os_daemon_name()}"
        self._coexist_tcp_port = 0
        self._trusted: set[str] = set()

    def start(self) -> bool:
        logger.info("KDE Connect coexist mode starting:")
        self._device_id = _ensure_sage_device_id()
        logger.info("  device id  : %s", self._device_id)
        logger.info("  device name: %s", self._actual_name)

        if not _ensure_sage_certs(self._device_id):
            logger.error("KDE Connect coexist: cert generation failed — see logs above")
            return False

        self._cert = SAGE_CERT
        self._key  = SAGE_KEY
        logger.info("  cert       : %s", SAGE_CERT)

        self._load_trusted()
        if self._trusted:
            logger.info("  paired with: %s", sorted(self._trusted))
        else:
            logger.info(
                "  paired with: <none yet> — when SAGE Bridge appears on your "
                "phone's KDE Connect 'Available devices' list, tap to pair."
            )

        threading.Thread(target=self._run, daemon=True,
                         name="sage-kdc-coexist").start()
        threading.Thread(target=self._broadcast_loop, daemon=True,
                         name="sage-kdc-bcast").start()
        return True

    def stop(self) -> None:
        # No daemon to restart — coexist never killed it.
        self._stop.set()
        with self._sessions_lock:
            for s in self._sessions.values():
                try: s.close()
                except Exception: pass
            self._sessions.clear()

    # No safety watchdog in coexist mode (we never replaced anything to
    # roll back to). Override the parent's watchdog to a no-op.
    def _safety_watchdog(self) -> None:
        return

    def _load_trusted(self) -> None:
        if not SAGE_TRUSTED_FILE.exists():
            return
        try:
            data = json.loads(SAGE_TRUSTED_FILE.read_text(encoding="utf-8"))
            self._trusted = set(data.get("device_ids", []))
        except Exception as exc:
            logger.debug("Couldn't load trusted devices: %s", exc)

    def _save_trusted(self) -> None:
        try:
            SAGE_KDE_DIR.mkdir(parents=True, exist_ok=True)
            SAGE_TRUSTED_FILE.write_text(
                json.dumps({"device_ids": sorted(self._trusted)}, indent=2),
                encoding="utf-8",
            )
        except Exception as exc:
            logger.warning("Couldn't save trusted devices: %s", exc)

    def _run(self) -> None:
        # Bind TCP — try 1716 first (paired phones reconnect to that port
        # by default), fall back to 1717+ if kdeconnectd already has it.
        tcp = None
        for port in [KDC_PORT, 1717, 1718, 1719, 1720, 0]:
            try:
                tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                if hasattr(socket, "SO_REUSEPORT"):
                    try:
                        tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                    except OSError:
                        pass
                tcp.bind(("0.0.0.0", port))
                tcp.listen(4)
                tcp.settimeout(1)
                break
            except OSError:
                if tcp:
                    try: tcp.close()
                    except Exception: pass
                tcp = None
                continue
        if tcp is None:
            logger.error("KDE Connect coexist: couldn't bind any TCP port")
            return

        self._coexist_tcp_port = tcp.getsockname()[1]
        logger.info("KDE Connect coexist: TCP listening on %d", self._coexist_tcp_port)

        # Try UDP 1716 too (with SO_REUSEPORT/REUSEADDR). If kdeconnectd
        # has it bound exclusively, we just rely on outbound broadcasts —
        # the phone will TCP-connect back to us when it sees our identity.
        udp = None
        try:
            udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if hasattr(socket, "SO_REUSEPORT"):
                try:
                    udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                except OSError:
                    pass
            udp.bind(("0.0.0.0", KDC_PORT))
            udp.settimeout(1)
            logger.info("KDE Connect coexist: UDP 1716 shared with kdeconnectd")
        except OSError as exc:
            logger.info(
                "KDE Connect coexist: UDP 1716 not shareable on this OS (%s) — "
                "using outbound identity broadcasts only",
                exc,
            )
            if udp:
                try: udp.close()
                except Exception: pass
            udp = None

        # Initial broadcast — already-paired phones reconnect immediately.
        self._broadcast_identity_once()

        while not self._stop.is_set():
            if udp:
                try:
                    data, addr = udp.recvfrom(4096)
                    if addr[0] not in self._self_addresses():
                        self._handle_udp_identity(data, addr[0])
                except socket.timeout:
                    pass
                except Exception as exc:
                    logger.debug("UDP loop error: %s", exc)
            else:
                # No UDP path — small wait so we don't busy-spin.
                self._stop.wait(0.2)

            try:
                conn, addr = tcp.accept()
                threading.Thread(
                    target=self._handle_inbound_tcp, args=(conn, addr),
                    daemon=True, name=f"sage-kdc-in-{addr[0]}",
                ).start()
            except socket.timeout:
                pass
            except OSError:
                break

        try: tcp.close()
        except Exception: pass
        if udp:
            try: udp.close()
            except Exception: pass

    def _broadcast_loop(self) -> None:
        """Re-broadcast identity every 60s so phones can find SAGE."""
        while not self._stop.is_set():
            if self._stop.wait(60):
                return
            self._broadcast_identity_once()

    def _broadcast_identity_once(self) -> None:
        """Override to use coexist's actual TCP port instead of KDC_PORT."""
        port = self._coexist_tcp_port or KDC_PORT
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        try:
            ident = _identity_packet(self._device_id, self._actual_name, port)
            raw = (json.dumps(ident) + "\n").encode("utf-8")
            for target in self._broadcast_targets():
                try: s.sendto(raw, (target, KDC_PORT))
                except Exception: pass
        finally:
            s.close()

    def _run_tls_session(self, tls: ssl.SSLSocket, peer_id: str,
                         peer_name: str, ssl_buf: bytearray) -> None:
        """Coexist-mode session — handles the pair handshake before SMS subs.

        On first connection from a device we haven't seen before, we send
        a `kdeconnect.pair` request. The user accepts on their phone, the
        phone sends `pair: true` back, we persist their deviceId, then
        proceed to SMS subscription. Subsequent reconnects skip the pair
        step (already in `_trusted`).
        """
        with self._sessions_lock:
            self._sessions[peer_id] = tls

        is_new = peer_id not in self._trusted
        if is_new:
            logger.info(
                "🔗 Pairing with new device %s (%s) — accept on your phone "
                "(KDE Connect → Devices → SAGE Bridge → Pair)",
                peer_name, peer_id,
            )
            try:
                _send_packet(tls, {
                    "id": int(time.time() * 1000),
                    "type": "kdeconnect.pair",
                    "body": {"pair": True},
                })
            except Exception as exc:
                logger.warning("pair request failed: %s", exc)
        else:
            logger.info("✅ TLS session ready with %s (already paired)", peer_name)

        # Subscribe to SMS — every variant the phone might recognize.
        for sub_type in (
            "kdeconnect.sms.request_conversations",
            "kdeconnect.notification.request",
        ):
            try:
                _send_packet(tls, {
                    "id": int(time.time() * 1000),
                    "type": sub_type,
                    "body": {"request": True},
                })
                logger.info("   → sent %s", sub_type)
            except Exception as exc:
                logger.warning("subscribe %s failed: %s", sub_type, exc)

        last_seen = [int(time.time() * 1000)]
        tls.settimeout(300)
        try:
            while not self._stop.is_set():
                try:
                    packet = _recv_packet(tls, ssl_buf)
                except socket.timeout:
                    continue
                except Exception as exc:
                    logger.info("Lost %s: %s", peer_name, exc)
                    break
                if packet is None:
                    logger.info("Lost %s: peer closed", peer_name)
                    break

                ptype = packet.get("type", "?")
                bkeys = list((packet.get("body") or {}).keys())
                logger.info("📨 %s ← %s body=%s", ptype, peer_name, bkeys)

                # Pair packet — phone accepting (or rejecting) our pair request.
                if ptype == "kdeconnect.pair":
                    paired = bool((packet.get("body") or {}).get("pair", False))
                    if paired:
                        logger.info("✅ Phone accepted pair from %s", peer_name)
                        self._trusted.add(peer_id)
                        self._save_trusted()
                    else:
                        logger.warning(
                            "Phone rejected pair from %s — disconnecting", peer_name,
                        )
                        break
                    continue

                self._handle_packet(packet, peer_name, last_seen)
        finally:
            with self._sessions_lock:
                self._sessions.pop(peer_id, None)
            try: tls.close()
            except Exception: pass
