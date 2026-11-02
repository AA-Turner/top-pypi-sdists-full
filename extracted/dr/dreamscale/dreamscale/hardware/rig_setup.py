"""One LAN setup page for every robot: cameras from live previews, then the robot's own
hardware panel, saved to its rig file.

Setup opens camera readers to preview them and never moves motors. The page edits a
draft; only Save (on the page, or Enter in the terminal) writes the rig file, and Ctrl-C
discards the draft. What differs between robots (roles and their wording, hardware
state, what is left before saving, and steps after it) is a RigSetupProfile.
"""

from __future__ import annotations

import hmac
import html
import io
import json
import queue
import re
import secrets
import select
import socket
import sys
import threading
import time
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from PIL import Image

from .camera_sources import (
    CameraReaders,
    CameraSpec,
    FrameUnavailable,
    _rsusb,
    dependency_help,
    discover_cameras,
    one_per_camera,
    realsense_access_help,
    realsense_inventory,
    usb_cameras_present,
    usb_link_mbps,
)


class RigSetupProfile:
    """What one robot adds to the shared setup page. Override what differs."""

    name = "robot"           # embodiment name: the page picks its hardware panel by it
    label = "robot"          # "YAM", "Franka", "SO-101"
    # (role, label, hint) per camera role, in the order the page assigns them.
    roles: tuple[tuple[str, str, str], ...] = ()
    required_roles: tuple[str, ...] = ()
    cli_command = ""         # the terminal fallback, without --config
    config_cls = None        # its RigFile subclass

    def load(self, path):
        raise NotImplementedError

    def save(self, config, path):
        raise NotImplementedError

    def from_dict(self, value):
        return self.config_cls.from_dict(value)

    def remaining_hardware(self, config) -> str | None:
        return None

    def present(self, config):
        """The draft as the page shows it."""
        return config

    def changed(self, draft, saved) -> bool:
        return draft.to_dict() != saved.to_dict()

    def hardware_state(self, draft, saved) -> dict:
        return {}

    def prepare_save(self, config):
        """The draft about to be written (YAM pins arms to today's adapters)."""
        return config

    def routes(self) -> dict:
        """Extra GET endpoints: path -> callable(server) returning JSON."""
        return {}

    def after_save(self, path, *, print_fn, interactive):
        pass

    def next_command(self, option: str) -> str:
        return f"dreamscale doctor {self.name}{option}"


def listed(items) -> str:
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def on_page(error: str) -> str:
    """A preview's error as this page says it: Rescan is how it restarts cameras."""
    text = re.sub(
        r"\b([Rr])estart(?: cameras)?\.$",
        lambda match: ("P" if match[1] == "R" else "p") + "ress Rescan.",
        error.strip() or "Camera unavailable.",
    )
    if "Rescan" in text:
        return text
    return text + ("" if text.endswith((".", "?", "!")) else ".") + " Press Rescan to try again."


def lan_address() -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as probe:
        try:
            probe.connect(("192.0.2.1", 9))
            return probe.getsockname()[0]
        except OSError:
            return "127.0.0.1"


def remaining(profile: RigSetupProfile, config) -> str | None:
    """What is left before the rig can be saved, or None when it is complete."""
    labels = {role: label.lower() for role, label, _ in profile.roles}
    views = [labels[role] for role in profile.required_roles if role not in config.roles]
    if views:
        return f"Assign the {listed(views)} camera{'s' if len(views) > 1 else ''}."
    return profile.remaining_hardware(config)


class _Preview:
    """One camera's preview readers, opened on a background thread."""

    def __init__(self, spec: CameraSpec):
        self.spec = spec
        self.readers = None
        self.error: str | None = None
        self.retired = False
        self.thread: threading.Thread | None = None


class SetupServer:
    """Serve the setup page, a live preview of every camera, and an unsaved draft.

    start() returns a reachable token URL; close() closes server and readers.
    Pass readers_factory(specs) to inject timestamped fake/custom sources; it is
    called with one camera at a time, so a camera that fails does not hide the
    others. A camera's old readers close before its replacement opens. By default
    every preview checks RealSense cameras against the scan's one enumeration.
    save() writes the draft and sets finished; outcome is then "saved", or
    "discarded" once the terminal cancels. run_setup() is blocking.

    Plugging in or unplugging a camera rescans by itself: a watcher polls
    cameras_present() (any cheap, hashable snapshot) and scans once a change
    has settled. Each scan bumps scans, which the page polls to refresh. A scan
    reopens every preview that failed to open or has stopped delivering frames,
    so a camera that was replugged comes back on Rescan.
    """

    def __init__(
        self,
        profile: RigSetupProfile,
        config_path: Path,
        *,
        host="0.0.0.0",
        port=8765,
        readers_factory=None,
        discover=None,
        cameras_present=usb_cameras_present,
        watch_interval_s=1.0,
    ):
        self.profile = profile
        self.config_path = Path(config_path)
        self.saved = profile.load(self.config_path)
        self.config = self.saved  # the page's draft; written only by save()
        self.outcome: str | None = None
        self.token = secrets.token_urlsafe(32)
        self.readers_factory = readers_factory or self._readers
        self.discover = discover or self._discover
        self._realsense: list | None = None
        self.candidates: dict[str, CameraSpec] = {}
        self.previews: dict[str, _Preview] = {}
        self._openers: dict[str, threading.Thread] = {}
        self.discovery_error: str | None = None
        self.cameras_present = cameras_present
        self.watch_interval_s = watch_interval_s
        self.scans = 0
        self._scanning = threading.Lock()
        self._stop_watching = threading.Event()
        self._watcher: threading.Thread | None = None
        self.finished = threading.Event()
        self.next_command = profile.next_command("")
        self.lock = threading.RLock()
        self._closing = False
        self.server = ThreadingHTTPServer((host, port), self._handler())
        self.server.daemon_threads = True
        self.thread = None
        address = lan_address() if host == "0.0.0.0" else host
        self.origin = f"http://{address}:{self.server.server_port}"
        self.allowed_hosts = {f"{address}:{self.server.server_port}"}
        self.url = f"{self.origin}/#token={self.token}"

    def start(self):
        present = self.cameras_present()
        self.scan()
        with self.lock:
            self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.thread.start()
            self._watcher = threading.Thread(target=self._watch, args=(present,), daemon=True)
            self._watcher.start()
            return self.url

    def _watch(self, scanned):
        """Rescan when the cameras present change and hold still for one poll."""
        last = scanned
        while not self._stop_watching.wait(self.watch_interval_s):
            try:
                present = self.cameras_present()
                if present != scanned and present == last:
                    self.scan()
                    scanned = present
                last = present
            except Exception:
                pass  # a failed scan shows as discovery_error; keep watching

    def scan(self):
        """Find cameras again and (re)open previews that are new, failed or stopped."""
        with self._scanning:
            self._scan()
            with self.lock:
                self.scans += 1

    def _scan(self):
        if _rsusb():
            # RSUSB cannot enumerate a camera another process is streaming, so
            # RealSense previews close first and reopen from this scan.
            with self.lock:
                openers = []
                for camera_id, preview in list(self.previews.items()):
                    if preview.spec.backend == "realsense":
                        self._retire(camera_id)
                        openers.append(preview.thread)
            for opener in openers:
                # A camera still opening closes itself once its open returns.
                if opener is not None:
                    opener.join()
        try:
            found, error = self.discover(), None
        except (ValueError, RuntimeError, OSError) as exc:
            found, error = [], str(exc)
        with self.lock:
            if self._closing:
                raise ValueError("Setup is closing. Start a new setup session.")
            self.discovery_error = error
            self.candidates = {
                s.id: s
                for s in one_per_camera(self.config.cameras, found, link_speed=usb_link_mbps)
            }
            for camera_id, preview in list(self.previews.items()):
                if (
                    self.candidates.get(camera_id) != preview.spec
                    or preview.error
                    or self._stopped(preview)
                ):
                    self._retire(camera_id)
            for spec in self.candidates.values():
                if spec.id not in self.previews:
                    self._open_preview(spec)

    def _discover(self):
        realsense = realsense_inventory() if dependency_help("realsense") is None else []
        with self.lock:
            self._realsense = realsense
        return discover_cameras(realsense=realsense)

    def _readers(self, specs: list[CameraSpec]):
        with self.lock:
            realsense = self._realsense
        return CameraReaders(specs, realsense=realsense)

    def _open_preview(self, spec: CameraSpec):
        preview = _Preview(spec)
        self.previews[spec.id] = preview
        # A camera's previous readers must release the device before reopening.
        previous = self._openers.get(spec.physical_id)
        preview.thread = threading.Thread(
            target=self._run_preview, args=(preview, previous), daemon=True
        )
        self._openers[spec.physical_id] = preview.thread
        preview.thread.start()

    def _run_preview(self, preview: _Preview, previous: threading.Thread | None):
        if previous is not None:
            previous.join()
        with self.lock:
            if preview.retired or self._closing:
                return
        readers = self.readers_factory([preview.spec])
        try:
            readers.open()
        except Exception as exc:
            try:
                readers.close()
            except Exception:
                pass
            with self.lock:
                preview.error = str(exc) or "Camera did not start."
            return
        with self.lock:
            if not (preview.retired or self._closing):
                preview.readers = readers
                return
        readers.close()

    @staticmethod
    def _stopped(preview: _Preview) -> bool:
        """Whether open readers no longer deliver frames: unplugged, reset or stalled.

        Readers that opened keep their camera's spec, and a replugged camera comes
        back with the same one, so only asking them tells a dead preview apart.
        """
        if preview.readers is None:
            return False  # still opening; its open fails or succeeds on its own
        try:
            preview.readers.latest(preview.spec.id)
        except FrameUnavailable:
            return False  # waiting for its first frame
        except Exception:
            return True
        return False

    def _retire(self, camera_id: str):
        preview = self.previews.pop(camera_id, None)
        if preview is None:
            return
        preview.retired = True
        readers, preview.readers = preview.readers, None
        if readers is not None:
            readers.close()

    def frame(self, camera_id: str):
        with self.lock:
            preview = self.previews.get(camera_id)
            if preview is None:
                raise KeyError("This camera is not connected.")
            if preview.error:
                raise ValueError(preview.error)
            if preview.readers is None:
                raise FrameUnavailable("Starting camera…")
            return preview.readers.latest(camera_id)

    def state(self):
        profile = self.profile
        with self.lock:
            draft, saved = self.config, self.saved
        hardware = profile.hardware_state(draft, saved)
        with self.lock:
            return {
                "robot": {"name": profile.name, "label": profile.label},
                "roles": [
                    {"role": role, "label": label, "hint": hint,
                     "required": role in profile.required_roles}
                    for role, label, hint in profile.roles
                ],
                "config": profile.present(self.config).to_dict(),
                "changed": profile.changed(self.config, self.saved),
                "remaining": remaining(profile, self.config),
                "next": self.next_command,
                "scans": self.scans,
                "cameras": [asdict(s) for s in self.candidates.values()],
                "discovery_error": self.discovery_error,
                "dependencies": [
                    text
                    for text in (
                        dependency_help("uvc"),
                        dependency_help("realsense"),
                        realsense_access_help(),
                    )
                    if text
                ],
                **hardware,
            }

    def update(self, config):
        """Replace the draft. Nothing is written until save()."""
        with self.lock:
            if self._closing:
                raise ValueError("Setup is closing.")
            unknown = [s.id for s in config.cameras if s.id not in self.candidates]
            if unknown:
                raise ValueError("Choose cameras shown on this page.")
            self.config = config.validate()
            self._show(config.cameras)

    def _show(self, cameras):
        for spec in cameras:
            if spec.id in self.candidates and self.candidates[spec.id] != spec:
                # A new rotation applies inside capture; reopen to show it.
                self.candidates[spec.id] = spec
                self._retire(spec.id)
                self._open_preview(spec)

    def discard(self):
        """Drop the draft and go back to the saved rig."""
        with self.lock:
            if self._closing:
                raise ValueError("Setup is closing.")
            self.config = self.saved
            self._show(self.saved.cameras)

    def save(self):
        """Write the complete draft, as the robot's profile prepares it."""
        with self.lock:
            draft = self.config
        prepared = self.profile.prepare_save(draft)
        with self.lock:
            if self._closing or self.outcome:
                raise ValueError("Setup is closing.")
            config = prepared
            problem = remaining(self.profile, config)
            if problem:
                raise ValueError("Not saved yet. " + problem)
            self.profile.save(config.validate(complete=True), self.config_path)
            self.saved = self.config = config
            self.outcome = "saved"
            self.finished.set()

    def close(self):
        # Close the mutation gate before shutting down the listening socket.
        # A request may still be blocked reading its body on a daemon thread.
        with self.lock:
            self._closing = True
        self._stop_watching.set()
        if self._watcher is not None:
            self._watcher.join(timeout=20)  # a scan in progress finishes first
        if self.thread is not None:
            self.server.shutdown()
            self.thread.join(timeout=3)
            self.thread = None
        self.server.server_close()
        with self.lock:
            for camera_id in list(self.previews):
                self._retire(camera_id)
            openers = list(self._openers.values())
        for opener in openers:
            # A camera still opening closes itself once its open returns.
            opener.join(timeout=20)

    def page(self) -> bytes:
        """The shared page, named for this robot before its script runs."""
        label = html.escape(self.profile.label)
        text = files("dreamscale.hardware").joinpath("rig_setup.html").read_text()
        for generic, named in (("Set up your robot", f"Set up your {label}"),
                               ("Robot setup", f"{label} setup")):
            text = text.replace(generic, named)
        return text.encode()

    def _handler(self):
        owner = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_):
                pass  # URLs and tokens must not leak into console logs.

            def reply(self, status, value, content_type="application/json"):
                body = value if isinstance(value, bytes) else json.dumps(value).encode()
                self.send_response(status)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                self.send_header("X-Content-Type-Options", "nosniff")
                self.send_header("Referrer-Policy", "no-referrer")
                self.send_header(
                    "Content-Security-Policy",
                    "default-src 'self'; "
                    "script-src 'self' 'unsafe-inline'; "
                    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
                    "font-src https://fonts.gstatic.com; "
                    "img-src 'self' blob: data:; frame-ancestors 'none'",
                )
                self.end_headers()
                self.wfile.write(body)

            def authorized(self):
                token = self.headers.get("Authorization", "").removeprefix("Bearer ")
                return (
                    self.headers.get("Host") in owner.allowed_hosts
                    and self.headers.get("Origin", owner.origin) == owner.origin
                    and hmac.compare_digest(token, owner.token)
                )

            def closing(self):
                if owner._closing:
                    self.reply(503, {"error": "Setup is closing."})
                return owner._closing

            def do_GET(self):
                parsed = urlsplit(self.path)
                if parsed.path == "/":
                    self.reply(200, owner.page(), "text/html; charset=utf-8")
                    return
                if not self.authorized():
                    self.reply(403, {"error": "Open the setup link printed in your terminal."})
                    return
                if self.closing():
                    return
                if parsed.path == "/api/state":
                    self.reply(200, owner.state())
                elif parsed.path == "/api/session":
                    self.reply(200, {"outcome": owner.outcome, "scans": owner.scans})
                elif parsed.path in owner.profile.routes():
                    try:
                        self.reply(200, owner.profile.routes()[parsed.path](owner))
                    except (ValueError, RuntimeError, OSError) as exc:
                        self.reply(409, {"error": str(exc)})
                elif parsed.path == "/api/frame":
                    camera_id = parse_qs(parsed.query).get("id", [""])[0]
                    try:
                        frame = owner.frame(camera_id)
                    except FrameUnavailable as exc:
                        self.reply(409, {"error": str(exc), "starting": True})
                        return
                    except (ValueError, RuntimeError, KeyError) as exc:
                        self.reply(409, {"error": on_page(str(exc).strip("'\""))})
                        return
                    encoded = io.BytesIO()
                    Image.fromarray(frame.rgb).save(encoded, format="JPEG", quality=85)
                    self.reply(200, encoded.getvalue(), "image/jpeg")
                else:
                    self.reply(404, {"error": "Unknown setup endpoint."})

            def do_POST(self):
                if not self.authorized():
                    self.reply(403, {"error": "Open the setup link printed in your terminal."})
                    return
                try:
                    length = int(self.headers.get("Content-Length", "0"))
                    if not 0 < length <= 65536:
                        raise ValueError("Setup request must be 1–65536 bytes.")
                    if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
                        raise ValueError("Send JSON configuration.")
                    self.connection.settimeout(3)
                    value = json.loads(self.rfile.read(length))
                    if self.closing():
                        return
                    if self.path == "/api/config":
                        owner.update(owner.profile.from_dict(value))
                        self.reply(200, owner.state())
                    elif self.path == "/api/scan" and value == {}:
                        owner.scan()
                        self.reply(200, owner.state())
                    elif self.path == "/api/discard" and value == {}:
                        owner.discard()
                        self.reply(200, owner.state())
                    elif self.path == "/api/save" and value == {}:
                        owner.save()
                        self.reply(200, {"next": owner.next_command})
                    else:
                        self.reply(404, {"error": "Unknown setup endpoint."})
                except (ValueError, TypeError, OSError) as exc:
                    if owner._closing:
                        self.reply(503, {"error": "Setup is closing."})
                    else:
                        self.reply(400, {"error": str(exc)})

        return Handler


def run_setup(
    profile: RigSetupProfile,
    config_path: Path,
    *,
    default_path: Path,
    host="0.0.0.0",
    port=8765,
    readers_factory=None,
    discover=None,
    print_url=print,
    input_fn=input,
    server_factory=None,
):
    """Blocking CLI entry point: Save on the page or Enter here saves; Ctrl-C discards.

    After a save the robot's profile finishes what the page can't (YAM brings up its CAN
    buses, with sudo asking for a password in this terminal).
    """
    from shlex import quote

    server = (server_factory or SetupServer)(
        profile, config_path, host=host, port=port, readers_factory=readers_factory,
        discover=discover,
    )
    option = (
        "" if Path(config_path) == Path(default_path)
        else f" --config {quote(str(config_path))}"
    )
    server.next_command = profile.next_command(option)
    existed = Path(config_path).exists()
    lines: queue.Queue = queue.Queue()
    terminal = input_fn is input and sys.stdin.isatty()
    reading = threading.Event()
    reading.set()

    def read_enter():
        # Without a terminal (EOF) the page's Save button is the only way to save.
        try:
            if terminal:
                # Poll, so this thread lets go of the terminal before sudo reads a password.
                while reading.is_set():
                    if select.select([sys.stdin], [], [], 0.25)[0]:
                        if not sys.stdin.readline():
                            return
                        lines.put("")
                return
            while True:
                lines.put(input_fn(""))
        except (EOFError, OSError, ValueError):
            pass

    try:
        print_url(f"Open {profile.label} setup on your laptop: {server.start()}")
        print_url(
            "If the page does not load, put both devices on the same network and allow the "
            f"setup port, or press Ctrl-C and run: {profile.cli_command}{option}"
        )
        print_url("Press Enter here to save, or Ctrl-C to discard.")
        threading.Thread(target=read_enter, daemon=True).start()
        while not server.finished.is_set():
            try:
                lines.get(timeout=0.25)
            except queue.Empty:
                continue
            try:
                server.save()
            except ValueError as exc:
                print_url(f"{exc} Finish on the page, then press Enter.")
    except KeyboardInterrupt:
        server.outcome = server.outcome or "discarded"
    finally:
        reading.clear()
        try:
            # Let an open page see how setup ended before the server goes away.
            time.sleep(1.2)
        except KeyboardInterrupt:
            pass
        server.close()
    if server.outcome == "saved":
        profile.after_save(config_path, print_fn=print_url, interactive=terminal)
        print_url(f"Saved {config_path}. Next: {server.next_command}")
    elif existed:
        print_url(f"Discarded your changes. {config_path} is unchanged.")
    else:
        print_url("Discarded. Nothing was saved.")
    return profile.load(config_path)
