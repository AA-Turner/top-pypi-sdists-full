"""A desktop agent for the Pi screen: the HTTP API that the `computer` MCP server calls,
served on this machine and driven over VNC (pi5-2 has no desktop agent and no input tool).

* The frame is scaled down to at most :data:`DEFAULT_MAX_WIDTH` and the clicks are scaled back up: the
  Claude API shrinks a 1920x1080 image, so the model would otherwise click in the wrong place.
* ``/bash`` refuses all but the client's screensaver call. ``--disallowedTools`` is the first wall.
* :meth:`PiDesktop.secret_lock` and :class:`ScreenGate`: no frame while a secret may show (a TOTP QR code
  is the seed). Once a secret showed, the screen stays sealed until the command ends.
* No DevTools: no right click and no DevTools keys (the Application tab shows the session cookies).
"""

from __future__ import annotations

import base64
import io
import json
import queue
import threading
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import TYPE_CHECKING, Any, Protocol

from pydantic import BaseModel, ValidationError

from plato.sims.ubuntu_vm.client import _DISABLE_SCREENSAVER_CMD
from plato.sims.ubuntu_vm.models import (
    Action,
    BashRequest,
    ComputerRequest,
    Resolution,
    ScrollDirection,
    StatusResponse,
    ToolResult,
)

if TYPE_CHECKING:
    from PIL.Image import Image

# The width of the screen the model sees. 1280 keeps a 16:9 frame under the
# Claude API's image size limit, so the API does not shrink it again.
DEFAULT_MAX_WIDTH = 1280
VNC_CONNECT_TIMEOUT_S = 30.0
# Input timing: a short hover before a press (hover handlers), the gap between the
# clicks of a double click, the pause between typed characters, the drag steps.
HOVER_S = 0.05
MULTI_CLICK_GAP_S = 0.08
TYPE_GAP_S = 0.01
DRAG_STEPS = 10
DRAG_STEP_S = 0.02
MAX_WAIT_S = 30.0
DISPLAY_NAME = "pi-vnc"

BASH_REFUSED = "bash is not available on this desktop: use the screen tools"
SCREEN_LOCKED = "the screen is hidden while code reads a secret: take a screenshot again in a few seconds"
SCREEN_SEALED = (
    "the screen is hidden because a secret shows on it, and it stays hidden: code takes over now. "
    "End your run with the result line"
)
DEVTOOLS_REFUSED = "this key or click opens DevTools or a context menu, and it is not available on this desktop"
SCREEN_MASKING = "code masked a new value on the screen: take a screenshot again"
PASTE_REFUSED = "pasting is not available on this desktop: code reads and types every value"
# How long a screenshot waits for the page check on the other thread. No answer: no frame.
GATE_ASK_S = 5.0
MASK_SETTLE_S = 0.5

# RFB pointer buttons (the button-mask bits are button - 1).
BUTTON_LEFT = 1
BUTTON_MIDDLE = 2
BUTTON_RIGHT = 3
_SCROLL_BUTTON = {
    ScrollDirection.up: 4,
    ScrollDirection.down: 5,
    ScrollDirection.left: 6,
    ScrollDirection.right: 7,
}
_CLICK_BUTTON = {
    Action.left_click: BUTTON_LEFT,
    Action.middle_click: BUTTON_MIDDLE,
    Action.right_click: BUTTON_RIGHT,
}

# X keysyms (RFB key events carry X keysyms). Names as xdotool takes them, lower case.
SHIFT = 0xFFE1
_KEYSYMS: dict[str, int] = {
    "shift": SHIFT,
    "shift_l": SHIFT,
    "shift_r": 0xFFE2,
    "ctrl": 0xFFE3,
    "control": 0xFFE3,
    "control_l": 0xFFE3,
    "control_r": 0xFFE4,
    "alt": 0xFFE9,
    "alt_l": 0xFFE9,
    "alt_r": 0xFFEA,
    "meta": 0xFFE7,
    "super": 0xFFEB,
    "super_l": 0xFFEB,
    "super_r": 0xFFEC,
    "cmd": 0xFFEB,
    "win": 0xFFEB,
    "return": 0xFF0D,
    "enter": 0xFF0D,
    "kp_enter": 0xFF8D,
    "tab": 0xFF09,
    "iso_left_tab": 0xFE20,
    "escape": 0xFF1B,
    "esc": 0xFF1B,
    "backspace": 0xFF08,
    "delete": 0xFFFF,
    "del": 0xFFFF,
    "insert": 0xFF63,
    "home": 0xFF50,
    "end": 0xFF57,
    "page_up": 0xFF55,
    "prior": 0xFF55,
    "pageup": 0xFF55,
    "page_down": 0xFF56,
    "next": 0xFF56,
    "pagedown": 0xFF56,
    "left": 0xFF51,
    "up": 0xFF52,
    "right": 0xFF53,
    "down": 0xFF54,
    "space": 0x20,
    "minus": 0x2D,
    "plus": 0x2B,
    "equal": 0x3D,
    "comma": 0x2C,
    "period": 0x2E,
    "slash": 0x2F,
    "backslash": 0x5C,
    "semicolon": 0x3B,
    "apostrophe": 0x27,
    "grave": 0x60,
    "bracketleft": 0x5B,
    "bracketright": 0x5D,
    "menu": 0xFF67,
    "caps_lock": 0xFFE5,
    "print": 0xFF61,
    **{f"f{n}": 0xFFBE + n - 1 for n in range(1, 13)},
}
# Characters that need Shift on a US layout (the Pi's keymap).
_SHIFTED = set('~!@#$%^&*()_+{}|:"<>?ABCDEFGHIJKLMNOPQRSTUVWXYZ')
_CTRL = {_KEYSYMS["control_l"], _KEYSYMS["control_r"]}
_SHIFTS = {SHIFT, _KEYSYMS["shift_r"]}


def opens_devtools(keysyms: list[int]) -> bool:
    """F12, ctrl+shift+i/j/c (DevTools), ctrl+u (page source), the menu key and
    shift+F10 (the context menu with "Inspect")."""
    keys = set(keysyms)
    ctrl, shift = bool(keys & _CTRL), bool(keys & _SHIFTS)
    if _KEYSYMS["f12"] in keys or _KEYSYMS["menu"] in keys:
        return True
    if shift and _KEYSYMS["f10"] in keys:
        return True
    letters = {k | 0x20 for k in keys if 0x41 <= k <= 0x5A or 0x61 <= k <= 0x7A}
    if ctrl and shift and letters & {ord("i"), ord("j"), ord("c")}:
        return True
    return ctrl and ord("u") in letters


def pastes(keysyms: list[int]) -> bool:
    """ctrl+v, ctrl+shift+v and shift+insert: a copied value would show in the address bar."""
    keys = set(keysyms)
    letters = {k | 0x20 for k in keys if 0x41 <= k <= 0x5A or 0x61 <= k <= 0x7A}
    return bool(keys & _CTRL and ord("v") in letters) or bool(keys & _SHIFTS and _KEYSYMS["insert"] in keys)


class ScreenGate:
    """A check, run on the thread that owns the page, before a frame goes out.

    The HTTP thread calls :meth:`ask` after it captured a frame; the page thread
    calls :meth:`serve` in its wait loop, which answers each ask and also checks on
    its own. ``secret_visible`` runs only on the page thread (Playwright's sync API
    belongs to one thread). The check runs AFTER the capture: a QR code is in the
    page before it is on the screen, so a frame that shows it always fails the
    check. Once the check says a secret shows, the gate stays latched."""

    refused = SCREEN_SEALED
    blocks_paste = False

    def __init__(self, secret_visible: Callable[[], bool]) -> None:
        self._check = secret_visible
        self._asks: queue.Queue[tuple[threading.Event, list[bool]]] = queue.Queue()
        self.latched = False

    def ask(self, timeout_s: float = GATE_ASK_S, started_at: float | None = None) -> bool:
        """True when the frame may go out. No answer in time: False. ``started_at``: when
        the frame's capture began (:class:`MaskGate` uses it)."""
        if self.latched:
            return False
        done, box = threading.Event(), [False]
        self._asks.put((done, box))
        if not done.wait(timeout_s):
            self.latched = True  # the page thread did not answer: no more frames
            return False
        return box[0]

    def serve(self, wait_s: float) -> None:
        """Answer the asks that came, waiting up to ``wait_s`` for one; with none,
        check once anyway (so input stops soon after a secret shows)."""
        try:
            first = self._asks.get(timeout=wait_s)
        except queue.Empty:
            first = None
        pending = [first] if first is not None else []
        while True:
            try:
                pending.append(self._asks.get_nowait())
            except queue.Empty:
                break
        ok = self._run_check()
        for done, box in pending:
            box[0] = ok
            done.set()

    def _run_check(self) -> bool:
        if not self.latched:
            try:
                self.latched = bool(self._check())
            except Exception:
                self.latched = True  # no answer from the page: assume the secret shows
        return not self.latched

    def close(self) -> None:
        """Refuse every ask still waiting (the page thread stops serving)."""
        while True:
            try:
                done, box = self._asks.get_nowait()
            except queue.Empty:
                return
            box[0] = False
            done.set()


class MaskGate(ScreenGate):
    """A gate that never latches: ``masked_since_last`` (run on the page thread) masks every
    secret-like value on the page and says whether it masked one that was not masked at the
    last check. Such a frame may show the value, so it is refused, and the next one goes out.
    It also refuses paste keys, so a copied value never reaches the address bar."""

    refused = SCREEN_MASKING
    blocks_paste = True

    def __init__(self, masked_since_last: Callable[[], bool]) -> None:
        super().__init__(masked_since_last)
        # When a check last masked a new value. The screen shows a change a little after
        # the page has it, so a frame captured up to MASK_SETTLE_S before that is refused too.
        self.changed_at: float | None = None

    def ask(self, timeout_s: float = GATE_ASK_S, started_at: float | None = None) -> bool:
        done, box = threading.Event(), [False]
        self._asks.put((done, box))
        done.wait(timeout_s)
        changed = self.changed_at
        if started_at is not None and changed is not None and changed >= started_at - MASK_SETTLE_S:
            return False
        return box[0]

    def _run_check(self) -> bool:
        try:
            masked = bool(self._check())
        except Exception:
            masked = True  # no answer from the page (a navigation): this frame does not go out
        if masked:
            self.changed_at = time.monotonic()
        return not masked


class ScreenSize(BaseModel):
    width: int
    height: int


class VncClient(Protocol):
    """The VNC operations the adapter needs. Coordinates are framebuffer pixels."""

    def size(self) -> ScreenSize: ...

    def capture(self) -> Image: ...

    def pointer(self, x: int, y: int, buttons: int) -> None: ...

    def key(self, keysym: int, down: bool) -> None: ...

    def close(self) -> None: ...


class UnknownKey(ValueError):
    pass


def char_keysym(ch: str) -> int:
    """The X keysym for one typed character."""
    if ch == "\n":
        return _KEYSYMS["return"]
    if ch == "\t":
        return _KEYSYMS["tab"]
    code = ord(ch)
    if 0x20 <= code <= 0x7E or 0xA0 <= code <= 0xFF:
        return code
    return 0x01000000 | code  # X11 Unicode keysym


def combo_keysyms(combo: str) -> list[int]:
    """``ctrl+shift+t`` as keysyms, in press order. A single character keeps its case
    (``A`` adds Shift, as xdotool does)."""
    out: list[int] = []
    for part in combo.split("+"):
        if not part:
            raise UnknownKey(f"empty key name in {combo!r}")
        known = _KEYSYMS.get(part.lower())
        if known is not None:
            out.append(known)
        elif len(part) == 1:
            if part in _SHIFTED and SHIFT not in out:
                out.append(SHIFT)
            out.append(ord(part.lower()) if part.isalpha() else char_keysym(part))
        else:
            raise UnknownKey(f"unknown key name {part!r}")
    return out


class PiDesktop:
    """One VNC screen as a desktop agent. Thread-safe: one action at a time."""

    def __init__(
        self,
        vnc: VncClient,
        *,
        max_width: int = DEFAULT_MAX_WIDTH,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self._vnc = vnc
        self._sleep = sleep
        self._lock = threading.RLock()
        self._secret_depth = 0
        self._sealed = False
        self.gate: ScreenGate | None = None
        size = vnc.size()
        self.screen = size
        if size.width > max_width:
            self.view = ScreenSize(width=max_width, height=round(size.height * max_width / size.width))
        else:
            self.view = size
        self._x = self.view.width // 2
        self._y = self.view.height // 2
        self._buttons = 0

    @property
    def sealed(self) -> bool:
        gate = self.gate
        return self._sealed or (gate is not None and gate.latched)

    @property
    def locked(self) -> bool:
        return self._secret_depth > 0 or self.sealed

    def seal(self) -> None:
        """No frame and no input from now on: a secret showed on the screen."""
        with self._lock:
            self._sealed = True

    @contextmanager
    def secret_lock(self) -> Iterator[None]:
        """No frame and no input while code reads a secret from the page. Waits for an
        action in progress to end first."""
        with self._lock:
            self._secret_depth += 1
        try:
            yield
        finally:
            with self._lock:
                self._secret_depth -= 1

    def status(self) -> StatusResponse:
        return StatusResponse(
            status="ok",
            display=DISPLAY_NAME,
            resolution=Resolution(width=self.view.width, height=self.view.height),
        )

    def bash(self, req: BashRequest) -> ToolResult:
        if req.command == _DISABLE_SCREENSAVER_CMD:
            return ToolResult(output="")
        return ToolResult(error=BASH_REFUSED)

    def computer(self, req: ComputerRequest) -> ToolResult:
        with self._lock:
            if self.locked:
                return ToolResult(error=SCREEN_SEALED if self.sealed else SCREEN_LOCKED)
            started = time.monotonic()
            try:
                result = self._act(req)
            except UnknownKey as e:
                return ToolResult(error=str(e))
            gate = self.gate
            if result.base64_image is not None and gate is not None and not gate.ask(started_at=started):
                return ToolResult(error=gate.refused)
            return result

    def _no_paste(self) -> bool:
        gate = self.gate
        return gate is not None and gate.blocks_paste

    def _to_screen(self, x: int, y: int) -> tuple[int, int]:
        sx = round(x * self.screen.width / self.view.width)
        sy = round(y * self.screen.height / self.view.height)
        return min(max(sx, 0), self.screen.width - 1), min(max(sy, 0), self.screen.height - 1)

    def _move(self, x: int, y: int) -> None:
        self._x = min(max(x, 0), self.view.width - 1)
        self._y = min(max(y, 0), self.view.height - 1)
        self._vnc.pointer(*self._to_screen(self._x, self._y), self._buttons)

    def _button(self, button: int, down: bool) -> None:
        bit = 1 << (button - 1)
        self._buttons = self._buttons | bit if down else self._buttons & ~bit
        self._vnc.pointer(*self._to_screen(self._x, self._y), self._buttons)

    def _click(self, button: int, times: int) -> None:
        for n in range(times):
            if n:
                self._sleep(MULTI_CLICK_GAP_S)
            self._button(button, True)
            self._button(button, False)

    def _keys(self, keysyms: list[int], hold_s: float = 0.0) -> None:
        for k in keysyms:
            self._vnc.key(k, True)
        if hold_s:
            self._sleep(hold_s)
        for k in reversed(keysyms):
            self._vnc.key(k, False)

    def _maybe_move(self, req: ComputerRequest) -> None:
        if req.coordinate is not None:
            if len(req.coordinate) != 2:
                raise UnknownKey("coordinate must be [x, y]")
            self._move(req.coordinate[0], req.coordinate[1])
            self._sleep(HOVER_S)

    def _act(self, req: ComputerRequest) -> ToolResult:
        action = req.action
        if action == Action.screenshot:
            return ToolResult(base64_image=self._frame())
        if action == Action.cursor_position:
            return ToolResult(output=f"X={self._x}\nY={self._y}")
        if action == Action.mouse_move:
            if req.coordinate is None:
                return ToolResult(error="mouse_move needs a coordinate")
            self._maybe_move(req)
        elif action == Action.right_click:
            return ToolResult(error=DEVTOOLS_REFUSED)  # the context menu has "Inspect"
        elif action == Action.middle_click and self._no_paste():
            return ToolResult(error=PASTE_REFUSED)  # X pastes the primary selection
        elif action in _CLICK_BUTTON:
            self._maybe_move(req)
            self._click(_CLICK_BUTTON[action], 1)
        elif action in (Action.double_click, Action.triple_click):
            self._maybe_move(req)
            self._click(BUTTON_LEFT, 2 if action == Action.double_click else 3)
        elif action == Action.left_mouse_down:
            self._button(BUTTON_LEFT, True)
        elif action == Action.left_mouse_up:
            self._button(BUTTON_LEFT, False)
        elif action == Action.left_click_drag:
            if req.coordinate is None or len(req.coordinate) != 2:
                return ToolResult(error="left_click_drag needs the end coordinate")
            x0, y0 = self._x, self._y
            x1, y1 = req.coordinate
            self._button(BUTTON_LEFT, True)
            for i in range(1, DRAG_STEPS + 1):
                self._move(round(x0 + (x1 - x0) * i / DRAG_STEPS), round(y0 + (y1 - y0) * i / DRAG_STEPS))
                self._sleep(DRAG_STEP_S)
            self._button(BUTTON_LEFT, False)
        elif action == Action.type:
            for ch in req.text or "":
                sym = char_keysym(ch)
                self._keys([SHIFT, sym] if ch in _SHIFTED else [sym])
                self._sleep(TYPE_GAP_S)
        elif action == Action.key:
            if not (req.text or "").strip():
                return ToolResult(error="key needs a key name")
            combos = [combo_keysyms(c) for c in (req.text or "").split()]  # xdotool: space-separated
            if any(opens_devtools(c) for c in combos):
                return ToolResult(error=DEVTOOLS_REFUSED)
            if self._no_paste() and any(pastes(c) for c in combos):
                return ToolResult(error=PASTE_REFUSED)
            for keysyms in combos:
                self._keys(keysyms)
        elif action == Action.hold_key:
            if not (req.text or "").strip():
                return ToolResult(error="hold_key needs a key name")
            keysyms = combo_keysyms((req.text or "").strip())
            if opens_devtools(keysyms):
                return ToolResult(error=DEVTOOLS_REFUSED)
            if self._no_paste() and pastes(keysyms):
                return ToolResult(error=PASTE_REFUSED)
            self._keys(keysyms, hold_s=min(req.duration or 0.5, MAX_WAIT_S))
        elif action == Action.scroll:
            self._maybe_move(req)
            button = _SCROLL_BUTTON[req.scroll_direction or ScrollDirection.down]
            for _ in range(max(1, min(req.scroll_amount or 3, 50))):
                self._click(button, 1)
        elif action == Action.wait:
            self._sleep(min(max(req.duration or 1.0, 0.0), MAX_WAIT_S))
        else:  # pragma: no cover - the Action enum has no other member
            return ToolResult(error=f"action {action.value} is not supported")
        return ToolResult(output="ok")

    def _frame(self) -> str:
        from PIL import Image as PILImage

        img = self._vnc.capture()
        if (img.width, img.height) != (self.view.width, self.view.height):
            img = img.resize((self.view.width, self.view.height), PILImage.Resampling.LANCZOS)
        buf = io.BytesIO()
        img.convert("RGB").save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()


class DesktopHttpServer:
    """``/status``, ``/computer`` and ``/bash`` for one :class:`PiDesktop`, on 127.0.0.1."""

    def __init__(self, desktop: PiDesktop, host: str = "127.0.0.1", port: int = 0) -> None:
        self.desktop = desktop
        self._httpd = ThreadingHTTPServer((host, port), _handler(desktop))
        self._httpd.daemon_threads = True
        self._thread: threading.Thread | None = None

    @property
    def port(self) -> int:
        return int(self._httpd.server_address[1])

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.port}"

    def start(self) -> str:
        if self._thread is None:
            self._thread = threading.Thread(target=self._httpd.serve_forever, name="pi-desktop-http", daemon=True)
            self._thread.start()
        return self.url

    def close(self) -> None:
        if self._thread is not None:
            self._httpd.shutdown()
            self._thread.join(timeout=5)
            self._thread = None
        self._httpd.server_close()


def _handler(desktop: PiDesktop) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, format: str, *args: Any) -> None:  # noqa: A002 - the base class name
            return  # no request log: a typed text is in the request body

        def _send(self, status: int, body: BaseModel | dict[str, Any]) -> None:
            data = (
                body.model_dump_json(exclude_none=True) if isinstance(body, BaseModel) else json.dumps(body)
            ).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self) -> None:  # noqa: N802 - http.server names
            if self.path.split("?")[0] == "/status":
                self._send(200, desktop.status())
            else:
                self._send(404, {"detail": "not found"})

        def do_POST(self) -> None:  # noqa: N802 - http.server names
            route = self.path.split("?")[0]
            length = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(length) if length else b""
            try:
                if route == "/computer":
                    self._send(200, desktop.computer(ComputerRequest.model_validate_json(raw)))
                elif route == "/bash":
                    self._send(200, desktop.bash(BashRequest.model_validate_json(raw)))
                else:
                    self._send(404, {"detail": "not found"})
            except ValidationError as e:
                self._send(422, {"detail": f"bad request: {e.error_count()} error(s)"})
            except Exception as e:  # the VNC link broke: tell the client, keep serving
                self._send(500, {"detail": f"desktop error: {type(e).__name__}"})

    return Handler


class VncdotoolClient:
    """:class:`VncClient` on ``vncdotool``'s threaded API. ZRLE encoding: a full
    1920x1080 frame in raw pixels is 8 MB, too slow over the office link."""

    def __init__(self, proxy: Any) -> None:
        self._proxy = proxy

    def size(self) -> ScreenSize:
        proto = self._proxy.protocol
        return ScreenSize(width=int(proto.width), height=int(proto.height))

    def capture(self) -> Image:
        self._proxy.refreshScreen(False)  # a full update: an incremental one waits for a change
        screen = self._proxy.protocol.screen
        if screen is None:
            raise RuntimeError("the VNC server sent no frame")
        return screen.copy()

    def pointer(self, x: int, y: int, buttons: int) -> None:
        self._proxy.platoPointer(x, y, buttons)

    def key(self, keysym: int, down: bool) -> None:
        self._proxy.platoKey(keysym, down)

    def close(self) -> None:
        try:
            self._proxy.disconnect()
        except Exception:
            pass


def connect_vncdotool(host: str, port: int, timeout_s: float = VNC_CONNECT_TIMEOUT_S) -> VncClient:
    """Connect to a VNC server with security type None (wayvnc with ``enable_auth=false``)."""
    try:
        from vncdotool import api, rfb
        from vncdotool.client import VNCDoToolClient, VNCDoToolFactory
    except ImportError as e:  # the `pi` extra is not installed
        raise RuntimeError("vncdotool is not installed: install plato-sdk-v2[pi]") from e

    class _ZrleClient(VNCDoToolClient):
        encoding = rfb.Encoding.ZRLE

        # The threaded proxy chains each call on the protocol object: a method must
        # return it. The raw pointerEvent and keyEvent return None, which breaks every
        # later call, and keyDown takes key names, not keysyms. These two return self.
        def platoPointer(self, x: int, y: int, buttons: int) -> Any:  # noqa: N802 - vncdotool's naming
            self.x, self.y, self.buttons = x, y, buttons
            self.pointerEvent(x, y, buttons)
            return self

        def platoKey(self, keysym: int, down: bool) -> Any:  # noqa: N802 - vncdotool's naming
            self.keyEvent(keysym, down)
            return self

    class _ZrleFactory(VNCDoToolFactory):
        protocol = _ZrleClient

    proxy = api.connect(f"{host}::{port}", None, _ZrleFactory, api.ThreadedVNCClientProxy, timeout_s)
    client = VncdotoolClient(proxy)
    try:
        # The first proxied call waits for the RFB handshake; it fails on a dead tunnel.
        proxy.refreshScreen(False)
        client.size()
    except BaseException:
        client.close()
        raise
    return client
