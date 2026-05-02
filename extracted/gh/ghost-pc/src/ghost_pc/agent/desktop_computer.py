"""ADK BaseComputer implementation for Windows desktop control.

Maps ADK's abstract computer interface to real Windows desktop actions
using BetterCam for screen capture and Win32 SendInput for input injection.

Enhanced with 4-layer UI understanding:
1. UIA inspection (structured accessibility tree)
2. Set-of-Mark screenshot annotation (numbered labels)
3. OCR fallback (for custom-rendered UIs)
4. Vision (Gemini Computer Use model)
"""

from __future__ import annotations

import asyncio
import io
import logging
from typing import Any, Literal

from google.adk.tools.computer_use.base_computer import (
    BaseComputer,
    ComputerEnvironment,
    ComputerState,
)

logger = logging.getLogger(__name__)

# Delay after actions to let the UI update before taking a screenshot
POST_ACTION_DELAY = 0.4

# Minimum number of useful UIA controls to consider inspection successful
MIN_USEFUL_CONTROLS = 3


class DesktopComputer(BaseComputer):
    """Controls a real Windows desktop via BetterCam + SendInput.

    ADK's ComputerUseToolset introspects this class, wraps each method
    as a tool, and feeds them to the Gemini Computer Use model.
    Coordinates received are in actual screen pixel space — ADK handles
    the conversion from the model's coordinate grid.
    """

    def __init__(self, screen_width: int, screen_height: int) -> None:
        self._screen_width = screen_width
        self._screen_height = screen_height
        # Shared state dict reference — set by the agent runner to inject
        # UIA/OCR data into session state for the model
        self._state: dict[str, Any] | None = None
        # Gemini Computer Use requires a url in every ComputerState response.
        # Use empty string so the field is always present — Gemini CU
        # validates that ALL tool responses include a url/current_url field.
        self._current_url: str = ""

    def bind_state(self, state: dict[str, Any]) -> None:
        """Bind a session state dict for storing transient UI data."""
        self._state = state

    def _clamp(self, x: int, y: int) -> tuple[int, int]:
        """Clamp coordinates to screen dimensions."""
        cx = max(0, min(x, self._screen_width - 1))
        cy = max(0, min(y, self._screen_height - 1))
        return cx, cy

    # --- Required abstract methods ---

    async def screen_size(self) -> tuple[int, int]:
        return (self._screen_width, self._screen_height)

    async def environment(self) -> ComputerEnvironment:
        return ComputerEnvironment.ENVIRONMENT_UNSPECIFIED

    async def current_state(self) -> ComputerState:
        """Capture screen with optional UIA/OCR augmentation.

        Flow:
        1. Capture screenshot (BetterCam) — 4ms
        2. Get foreground window HWND + process name — 1ms
        3. UIA inspect that window — 5-50ms
        4. If UIA found useful controls:
           a. Annotate screenshot with SoM labels
           b. Build control text list
           c. Store in temp:uia_controls
        5. If UIA found nothing useful:
           a. Run OCR on screenshot — 10-80ms
           b. Store in temp:ocr_results
        6. Downscale + encode PNG — 10ms
        7. Return ComputerState with (possibly annotated) screenshot
        """
        # Step 1: Capture raw screenshot as PNG bytes
        screenshot_png = await asyncio.to_thread(
            _capture_png, self._screen_width, self._screen_height
        )

        # Steps 2-5: UI understanding augmentation
        screenshot_png = await self._augment_screenshot(screenshot_png)

        # Gemini Computer Use requires a url field (even for desktop).
        # Track the last navigated URL so the model can reference it.
        return ComputerState(screenshot=screenshot_png, url=self._current_url)

    async def _augment_screenshot(self, screenshot_png: bytes) -> bytes:
        """Add UIA/OCR data to the screenshot and session state."""
        try:
            from ghost_pc.desktop.uia_inspector import (
                get_foreground_hwnd,
                get_foreground_process_name,
                inspect_window,
            )

            # Step 2: Get foreground window info
            hwnd = await asyncio.to_thread(get_foreground_hwnd)
            process_name = await asyncio.to_thread(get_foreground_process_name)

            if self._state is not None:
                self._state["temp:active_app"] = process_name or ""

            # Step 3: UIA inspection
            controls = await asyncio.to_thread(inspect_window, hwnd)

            # Filter to useful interactive controls
            useful = [
                c
                for c in controls
                if c["name"] or c["control_type"] in ("Button", "Edit", "ComboBox", "CheckBox")
            ]

            if len(useful) >= MIN_USEFUL_CONTROLS:
                # Step 4a: Annotate screenshot with SoM labels
                try:
                    from ghost_pc.desktop.som import annotate_screenshot

                    annotated_png, control_text = annotate_screenshot(
                        screenshot_png,
                        useful,
                        screen_width=self._screen_width,
                        screen_height=self._screen_height,
                    )
                    screenshot_png = annotated_png

                    # Step 4b-c: Store in state
                    if self._state is not None:
                        self._state["temp:uia_controls"] = control_text
                        self._state["temp:controls_map"] = useful
                        self._state["temp:ocr_results"] = ""
                except Exception as e:
                    logger.debug("SoM annotation failed: %s", e)
                    # Store text-only fallback
                    if self._state is not None:
                        from ghost_pc.desktop.som import build_control_text

                        self._state["temp:uia_controls"] = build_control_text(useful)
                        self._state["temp:controls_map"] = useful
            else:
                # Step 5: UIA didn't find enough — try OCR
                if self._state is not None:
                    self._state["temp:uia_controls"] = ""
                    self._state["temp:controls_map"] = []

                try:
                    from ghost_pc.desktop.ocr import extract_text

                    ocr_results = await extract_text(screenshot_png)
                    if ocr_results and self._state is not None:
                        ocr_text = "\n".join(
                            f"'{r['text']}' at ({r['bbox'][0]},{r['bbox'][1]})"
                            for r in ocr_results[:100]
                        )
                        self._state["temp:ocr_results"] = ocr_text
                except Exception as e:
                    logger.debug("OCR failed: %s", e)

        except ImportError:
            logger.debug("UI understanding modules not available")
            if self._state is not None:
                self._state["temp:controls_map"] = []
        except Exception as e:
            logger.debug("Screenshot augmentation failed: %s", e)
            if self._state is not None:
                self._state["temp:controls_map"] = []

        return screenshot_png

    async def click_at(self, x: int, y: int) -> ComputerState:
        from ghost_pc.desktop.input import click

        x, y = self._clamp(x, y)
        await asyncio.to_thread(click, x, y)
        await asyncio.sleep(POST_ACTION_DELAY)
        return await self.current_state()

    async def hover_at(self, x: int, y: int) -> ComputerState:
        from ghost_pc.desktop.input import move_mouse

        x, y = self._clamp(x, y)
        await asyncio.to_thread(move_mouse, x, y)
        await asyncio.sleep(0.1)
        return await self.current_state()

    async def type_text_at(
        self,
        x: int,
        y: int,
        text: str,
        press_enter: bool = True,
        clear_before_typing: bool = True,
    ) -> ComputerState:
        from ghost_pc.desktop.input import click, hotkey, press_key, type_text

        x, y = self._clamp(x, y)
        await asyncio.to_thread(click, x, y)
        await asyncio.sleep(0.15)

        if clear_before_typing:
            await asyncio.to_thread(hotkey, "ctrl", "a")
            await asyncio.sleep(0.05)
            await asyncio.to_thread(press_key, "backspace")
            await asyncio.sleep(0.05)

        await asyncio.to_thread(type_text, text)
        await asyncio.sleep(0.1)

        if press_enter:
            await asyncio.to_thread(press_key, "enter")
            await asyncio.sleep(0.1)

        await asyncio.sleep(POST_ACTION_DELAY)
        return await self.current_state()

    async def scroll_document(
        self, direction: Literal["up", "down", "left", "right"]
    ) -> ComputerState:
        from ghost_pc.desktop.input import press_key, scroll

        if direction in ("up", "down"):
            await asyncio.to_thread(press_key, "pageup" if direction == "up" else "pagedown")
        else:
            # Use actual horizontal scroll at screen center instead of home/end
            cx, cy = self._screen_width // 2, self._screen_height // 2
            await asyncio.to_thread(scroll, cx, cy, direction, 5)

        await asyncio.sleep(POST_ACTION_DELAY)
        return await self.current_state()

    async def scroll_at(
        self,
        x: int,
        y: int,
        direction: Literal["up", "down", "left", "right"],
        magnitude: int,
    ) -> ComputerState:
        from ghost_pc.desktop.input import scroll

        x, y = self._clamp(x, y)
        amount = max(1, magnitude // 200)
        await asyncio.to_thread(scroll, x, y, direction, amount)
        await asyncio.sleep(POST_ACTION_DELAY)
        return await self.current_state()

    async def wait(self, seconds: int) -> ComputerState:
        await asyncio.sleep(seconds)
        return await self.current_state()

    # -- Browser methods disabled: desktop-first mode --
    # The Gemini CU model calls these automatically, so we override them
    # to no-op instead of opening Chrome. This forces the model to use
    # desktop tools (open_application, switch_to_window, etc.) instead.

    async def go_back(self) -> ComputerState:
        return await self.current_state()

    async def go_forward(self) -> ComputerState:
        return await self.current_state()

    async def search(self) -> ComputerState:
        return await self.current_state()

    async def navigate(self, url: str) -> ComputerState:
        return await self.current_state()

    async def key_combination(self, keys: list[str]) -> ComputerState:
        from ghost_pc.desktop.input import hotkey

        normalized = [_normalize_key(k) for k in keys]
        await asyncio.to_thread(hotkey, *normalized)
        await asyncio.sleep(POST_ACTION_DELAY)
        return await self.current_state()

    async def drag_and_drop(
        self, x: int, y: int, destination_x: int, destination_y: int
    ) -> ComputerState:
        from ghost_pc.desktop.input import drag

        x, y = self._clamp(x, y)
        destination_x, destination_y = self._clamp(destination_x, destination_y)
        await asyncio.to_thread(drag, x, y, destination_x, destination_y)
        await asyncio.sleep(POST_ACTION_DELAY)
        return await self.current_state()

    async def open_web_browser(self) -> ComputerState:
        # Browser use disabled — desktop-first mode
        return await self.current_state()

    # --- Optional overrides ---

    async def initialize(self) -> None:
        logger.info(
            "DesktopComputer initialized (%dx%d)",
            self._screen_width,
            self._screen_height,
        )

    async def close(self) -> None:
        logger.info("DesktopComputer closed")


# --- Helpers ---

# Map ADK key names (Playwright-style) to our Win32 key names
_KEY_MAP: dict[str, str] = {
    "Control": "ctrl",
    "Shift": "shift",
    "Alt": "alt",
    "Meta": "win",
    "Enter": "enter",
    "Backspace": "backspace",
    "Delete": "delete",
    "Escape": "escape",
    "Tab": "tab",
    "Space": "space",
    "ArrowUp": "up",
    "ArrowDown": "down",
    "ArrowLeft": "left",
    "ArrowRight": "right",
    "PageUp": "pageup",
    "PageDown": "pagedown",
    "Home": "home",
    "End": "end",
    "Insert": "insert",
    "F1": "f1",
    "F2": "f2",
    "F3": "f3",
    "F4": "f4",
    "F5": "f5",
    "F6": "f6",
    "F7": "f7",
    "F8": "f8",
    "F9": "f9",
    "F10": "f10",
    "F11": "f11",
    "F12": "f12",
}


def _normalize_key(key: str) -> str:
    """Convert ADK/Playwright-style key names to our Win32 key names."""
    if key in _KEY_MAP:
        return _KEY_MAP[key]
    if len(key) == 1:
        return key
    return _KEY_MAP.get(key.title(), key.lower())


def _capture_png(width: int, height: int) -> bytes:
    """Capture screen, downscale to target resolution, and encode as PNG.

    ADK expects PNG format screenshots. Uses Pillow for encoding and
    resizing. BetterCam provides BGRA numpy arrays. The frame cache in
    capture.py ensures we always get a frame (never None after first grab).
    """
    try:
        from ghost_pc.desktop.capture import grab_screenshot

        frame = grab_screenshot()
        if frame is None:
            return _blank_png(width, height)

        from PIL import Image

        # BetterCam returns BGRA — take R,G,B channels (indices 2,1,0) for Pillow
        rgb_frame = frame[:, :, 2::-1]
        img = Image.fromarray(rgb_frame)

        # Downscale if captured resolution exceeds target
        if img.width > width or img.height > height:
            img = img.resize((width, height), Image.Resampling.LANCZOS)

        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=False, compress_level=1)
        return buf.getvalue()

    except Exception as e:
        logger.warning("Screen capture failed: %s", e)
        return _blank_png(width, height)


def _blank_png(width: int, height: int) -> bytes:
    """Generate a minimal blank PNG as fallback."""
    from PIL import Image

    img = Image.new("RGB", (width, height), (30, 30, 30))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
