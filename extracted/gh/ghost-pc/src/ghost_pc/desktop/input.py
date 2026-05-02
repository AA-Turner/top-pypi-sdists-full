"""Mouse and keyboard injection using Win32 SendInput via ctypes.

No admin required for normal desktop applications.
No external dependencies — pure ctypes.
"""

from __future__ import annotations

import sys
import time

if sys.platform == "win32":
    import ctypes
    from ctypes import wintypes

    # --- DPI Awareness Fix ---
    # Without this, all coordinates are wrong on HiDPI displays (150%+ scaling)
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

    # --- Constants ---
    _INPUT_MOUSE = 0
    _INPUT_KEYBOARD = 1

    _MOUSEEVENTF_MOVE = 0x0001
    _MOUSEEVENTF_LEFTDOWN = 0x0002
    _MOUSEEVENTF_LEFTUP = 0x0004
    _MOUSEEVENTF_RIGHTDOWN = 0x0008
    _MOUSEEVENTF_RIGHTUP = 0x0010
    _MOUSEEVENTF_MIDDLEDOWN = 0x0020
    _MOUSEEVENTF_MIDDLEUP = 0x0040
    _MOUSEEVENTF_WHEEL = 0x0800
    _MOUSEEVENTF_HWHEEL = 0x1000
    _MOUSEEVENTF_ABSOLUTE = 0x8000

    _KEYEVENTF_KEYUP = 0x0002
    _KEYEVENTF_UNICODE = 0x0004

    _WHEEL_DELTA = 120

    # --- Structures ---
    class _MOUSEINPUT(ctypes.Structure):
        _fields_ = [
            ("dx", wintypes.LONG),
            ("dy", wintypes.LONG),
            ("mouseData", wintypes.DWORD),
            ("dwFlags", wintypes.DWORD),
            ("time", wintypes.DWORD),
            ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
        ]

    class _KEYBDINPUT(ctypes.Structure):
        _fields_ = [
            ("wVk", wintypes.WORD),
            ("wScan", wintypes.WORD),
            ("dwFlags", wintypes.DWORD),
            ("time", wintypes.DWORD),
            ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
        ]

    class _HARDWAREINPUT(ctypes.Structure):
        _fields_ = [
            ("uMsg", wintypes.DWORD),
            ("wParamL", wintypes.WORD),
            ("wParamH", wintypes.WORD),
        ]

    class _InputUnion(ctypes.Union):
        _fields_ = [("mi", _MOUSEINPUT), ("ki", _KEYBDINPUT), ("hi", _HARDWAREINPUT)]

    class _INPUT(ctypes.Structure):
        _fields_ = [("type", wintypes.DWORD), ("union", _InputUnion)]

    _user32 = ctypes.windll.user32

    # --- Virtual Key Code Map ---
    _VK_MAP: dict[str, int] = {
        "backspace": 0x08,
        "tab": 0x09,
        "enter": 0x0D,
        "return": 0x0D,
        "shift": 0x10,
        "ctrl": 0x11,
        "control": 0x11,
        "alt": 0x12,
        "menu": 0x12,
        "pause": 0x13,
        "capslock": 0x14,
        "escape": 0x1B,
        "esc": 0x1B,
        "space": 0x20,
        "pageup": 0x21,
        "pagedown": 0x22,
        "end": 0x23,
        "home": 0x24,
        "left": 0x25,
        "up": 0x26,
        "right": 0x27,
        "down": 0x28,
        "printscreen": 0x2C,
        "insert": 0x2D,
        "delete": 0x2E,
        "win": 0x5B,
        "windows": 0x5B,
        "lwin": 0x5B,
        "f1": 0x70,
        "f2": 0x71,
        "f3": 0x72,
        "f4": 0x73,
        "f5": 0x74,
        "f6": 0x75,
        "f7": 0x76,
        "f8": 0x77,
        "f9": 0x78,
        "f10": 0x79,
        "f11": 0x7A,
        "f12": 0x7B,
    }

    def _send(inp: _INPUT) -> None:
        _user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

    def _screen_size() -> tuple[int, int]:
        return (_user32.GetSystemMetrics(0), _user32.GetSystemMetrics(1))

    def _resolve_vk(key: str) -> int:
        """Resolve a key name to a virtual key code."""
        key_lower = key.lower().strip()
        if key_lower in _VK_MAP:
            return _VK_MAP[key_lower]
        if len(key) == 1:
            result = _user32.VkKeyScanW(ord(key))
            if result != -1:
                return result & 0xFF
            return ord(key.upper())
        raise ValueError(f"Unknown key: {key!r}")

    def move_mouse(x: int, y: int) -> None:
        """Move mouse to absolute pixel coordinates."""
        sw, sh = _screen_size()
        nx = int(x * 65536 / sw)
        ny = int(y * 65536 / sh)
        inp = _INPUT(type=_INPUT_MOUSE)
        inp.union.mi.dx = nx
        inp.union.mi.dy = ny
        inp.union.mi.dwFlags = _MOUSEEVENTF_MOVE | _MOUSEEVENTF_ABSOLUTE
        _send(inp)

    def mouse_down(x: int, y: int, button: str = "left") -> None:
        """Press mouse button at coordinates without releasing."""
        move_mouse(x, y)
        time.sleep(0.005)
        down_flag = {
            "left": _MOUSEEVENTF_LEFTDOWN,
            "right": _MOUSEEVENTF_RIGHTDOWN,
            "middle": _MOUSEEVENTF_MIDDLEDOWN,
        }.get(button, _MOUSEEVENTF_LEFTDOWN)
        inp = _INPUT(type=_INPUT_MOUSE)
        inp.union.mi.dwFlags = down_flag
        _send(inp)

    def mouse_up(x: int, y: int, button: str = "left") -> None:
        """Release mouse button at coordinates."""
        move_mouse(x, y)
        time.sleep(0.005)
        up_flag = {
            "left": _MOUSEEVENTF_LEFTUP,
            "right": _MOUSEEVENTF_RIGHTUP,
            "middle": _MOUSEEVENTF_MIDDLEUP,
        }.get(button, _MOUSEEVENTF_LEFTUP)
        inp = _INPUT(type=_INPUT_MOUSE)
        inp.union.mi.dwFlags = up_flag
        _send(inp)

    def click(x: int, y: int, button: str = "left") -> None:
        """Click at absolute pixel coordinates."""
        move_mouse(x, y)
        time.sleep(0.01)

        down_flag, up_flag = {
            "left": (_MOUSEEVENTF_LEFTDOWN, _MOUSEEVENTF_LEFTUP),
            "right": (_MOUSEEVENTF_RIGHTDOWN, _MOUSEEVENTF_RIGHTUP),
            "middle": (_MOUSEEVENTF_MIDDLEDOWN, _MOUSEEVENTF_MIDDLEUP),
        }.get(button, (_MOUSEEVENTF_LEFTDOWN, _MOUSEEVENTF_LEFTUP))

        inp = _INPUT(type=_INPUT_MOUSE)
        inp.union.mi.dwFlags = down_flag
        _send(inp)

        inp2 = _INPUT(type=_INPUT_MOUSE)
        inp2.union.mi.dwFlags = up_flag
        _send(inp2)

    def double_click(x: int, y: int) -> None:
        """Double-click at coordinates."""
        click(x, y)
        time.sleep(0.05)
        click(x, y)

    def scroll(x: int, y: int, direction: str = "down", amount: int = 3) -> None:
        """Scroll at coordinates. Direction: up/down/left/right."""
        move_mouse(x, y)
        time.sleep(0.01)

        inp = _INPUT(type=_INPUT_MOUSE)
        if direction in ("up", "down"):
            inp.union.mi.dwFlags = _MOUSEEVENTF_WHEEL
            delta = amount * _WHEEL_DELTA
            val = delta if direction == "up" else (-delta) & 0xFFFFFFFF
            inp.union.mi.mouseData = wintypes.DWORD(val)
        else:
            inp.union.mi.dwFlags = _MOUSEEVENTF_HWHEEL
            delta = amount * _WHEEL_DELTA
            val = delta if direction == "right" else (-delta) & 0xFFFFFFFF
            inp.union.mi.mouseData = wintypes.DWORD(val)
        _send(inp)

    def drag(x1: int, y1: int, x2: int, y2: int, duration: float = 0.5) -> None:
        """Drag from (x1, y1) to (x2, y2)."""
        move_mouse(x1, y1)
        time.sleep(0.05)

        inp = _INPUT(type=_INPUT_MOUSE)
        inp.union.mi.dwFlags = _MOUSEEVENTF_LEFTDOWN
        _send(inp)

        steps = max(10, int(duration * 60))
        for i in range(1, steps + 1):
            t = i / steps
            cx = int(x1 + (x2 - x1) * t)
            cy = int(y1 + (y2 - y1) * t)
            move_mouse(cx, cy)
            time.sleep(duration / steps)

        inp2 = _INPUT(type=_INPUT_MOUSE)
        inp2.union.mi.dwFlags = _MOUSEEVENTF_LEFTUP
        _send(inp2)

    def press_key(key: str) -> None:
        """Press and release a single key."""
        vk = _resolve_vk(key)
        inp = _INPUT(type=_INPUT_KEYBOARD)
        inp.union.ki.wVk = vk
        _send(inp)
        time.sleep(0.02)
        inp2 = _INPUT(type=_INPUT_KEYBOARD)
        inp2.union.ki.wVk = vk
        inp2.union.ki.dwFlags = _KEYEVENTF_KEYUP
        _send(inp2)

    def hotkey(*keys: str) -> None:
        """Press a key combination (e.g., hotkey('ctrl', 'c'))."""
        vk_codes = [_resolve_vk(k) for k in keys]
        for vk in vk_codes:
            inp = _INPUT(type=_INPUT_KEYBOARD)
            inp.union.ki.wVk = vk
            _send(inp)
            time.sleep(0.02)
        for vk in reversed(vk_codes):
            inp = _INPUT(type=_INPUT_KEYBOARD)
            inp.union.ki.wVk = vk
            inp.union.ki.dwFlags = _KEYEVENTF_KEYUP
            _send(inp)
            time.sleep(0.02)

    def type_text(text: str, interval: float = 0.02) -> None:
        """Type a string character by character using Unicode events."""
        for char in text:
            inp = _INPUT(type=_INPUT_KEYBOARD)
            inp.union.ki.wScan = ord(char)
            inp.union.ki.dwFlags = _KEYEVENTF_UNICODE
            _send(inp)

            inp2 = _INPUT(type=_INPUT_KEYBOARD)
            inp2.union.ki.wScan = ord(char)
            inp2.union.ki.dwFlags = _KEYEVENTF_UNICODE | _KEYEVENTF_KEYUP
            _send(inp2)

            if interval > 0:
                time.sleep(interval)

    def denormalize_coords(
        norm_x: int, norm_y: int, screen_width: int, screen_height: int
    ) -> tuple[int, int]:
        """Convert Gemini's 0-999 normalized coords to actual pixel coords."""
        actual_x = int(norm_x / 1000 * screen_width)
        actual_y = int(norm_y / 1000 * screen_height)
        return (actual_x, actual_y)

else:
    # Non-Windows stubs — never executed at runtime, only for type checker

    def move_mouse(x: int, y: int) -> None:
        """Move mouse to absolute pixel coordinates."""

    def mouse_down(x: int, y: int, button: str = "left") -> None:
        """Press mouse button at coordinates without releasing."""

    def mouse_up(x: int, y: int, button: str = "left") -> None:
        """Release mouse button at coordinates."""

    def click(x: int, y: int, button: str = "left") -> None:
        """Click at absolute pixel coordinates."""

    def double_click(x: int, y: int) -> None:
        """Double-click at coordinates."""

    def scroll(x: int, y: int, direction: str = "down", amount: int = 3) -> None:
        """Scroll at coordinates. Direction: up/down/left/right."""

    def drag(x1: int, y1: int, x2: int, y2: int, duration: float = 0.5) -> None:
        """Drag from (x1, y1) to (x2, y2)."""

    def press_key(key: str) -> None:
        """Press and release a single key."""

    def hotkey(*keys: str) -> None:
        """Press a key combination (e.g., hotkey('ctrl', 'c'))."""

    def type_text(text: str, interval: float = 0.02) -> None:
        """Type a string character by character using Unicode events."""

    def denormalize_coords(
        norm_x: int, norm_y: int, screen_width: int, screen_height: int
    ) -> tuple[int, int]:
        """Convert Gemini's 0-999 normalized coords to actual pixel coords."""
        return (0, 0)
