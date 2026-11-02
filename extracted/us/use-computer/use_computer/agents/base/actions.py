"""Desktop action execution for CUA agents."""

from __future__ import annotations

import asyncio
import io
import logging
import time
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import httpx
from PIL import Image, ImageDraw

from use_computer.agents.base.desktop import normalize_key
from use_computer.agents.base.sandbox import ComputerSandbox
from use_computer.agents.types import DesktopAction, DesktopCommand, MouseButton

_log = logging.getLogger("use_computer.agent")


def _extract_coords(
    action: dict[str, Any],
) -> tuple[tuple[int, int] | None, tuple[int, int] | None]:
    """Pull (point, secondary_point) from any action shape we use."""
    point: tuple[int, int] | None = None
    secondary: tuple[int, int] | None = None
    if "coordinate" in action and action["coordinate"]:
        c = action["coordinate"]
        point = (int(c[0]), int(c[1]))
    if "start_coordinate" in action and action["start_coordinate"]:
        s = action["start_coordinate"]
        secondary = (int(s[0]), int(s[1]))
    if point is None and "x" in action and "y" in action:
        try:
            point = (int(float(action["x"])), int(float(action["y"])))
        except (TypeError, ValueError):
            pass
    if "to_x" in action and "to_y" in action:
        try:
            point = (int(float(action["to_x"])), int(float(action["to_y"])))
        except (TypeError, ValueError):
            pass
    if "from_x" in action and "from_y" in action:
        try:
            secondary = (int(float(action["from_x"])), int(float(action["from_y"])))
        except (TypeError, ValueError):
            pass
    return point, secondary


def _annotate_click(png_bytes: bytes, action: dict[str, Any]) -> bytes:
    """Draw a red marker at the click/move/scroll/drag coordinate."""
    point, start = _extract_coords(action)
    if point is None and start is None:
        return png_bytes
    try:
        img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        red = (255, 30, 30, 240)
        radius = 5
        if point and start:
            draw.line([start, point], fill=red, width=2)
            for px, py in (start, point):
                draw.ellipse([px - radius, py - radius, px + radius, py + radius], fill=red)
        else:
            cx, cy = point or start  # type: ignore
            draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=red)
        out = Image.alpha_composite(img, overlay).convert("RGB")
        buf = io.BytesIO()
        out.save(buf, format="PNG")
        return buf.getvalue()
    except Exception as e:
        _log.warning(f"annotate_click failed: {e}")
        return png_bytes


async def execute_action(
    sandbox: ComputerSandbox,
    action: dict[str, Any],
    images_dir: Path,
    step_idx: int,
    key_aliases: Mapping[str, str] | None = None,
) -> tuple[str, bytes | None, str | None]:
    """Execute a computer-use action; returns (result_text, ss_bytes, ss_path)."""
    command = DesktopCommand.from_mapping(action)
    img_name = f"step_{step_idx:03d}.png"
    t0 = time.monotonic()

    if command.action is DesktopAction.SCREENSHOT:
        ss = await _take_screenshot_with_recovery(sandbox, command.label)
        if ss is None:
            return "Screenshot failed after retries", None, None
        (images_dir / img_name).write_bytes(ss)
        _log.info(f"action screenshot: {time.monotonic() - t0:.2f}s, {len(ss)} bytes")
        return "Screenshot taken", ss, f"images/{img_name}"

    try:
        if command.action in {DesktopAction.LEFT_CLICK, DesktopAction.CLICK}:
            await sandbox.mouse.click(
                command.point.x,
                command.point.y,
                button=MouseButton.LEFT.value,
            )
        elif command.action is DesktopAction.RIGHT_CLICK:
            await sandbox.mouse.click(
                command.point.x,
                command.point.y,
                button=MouseButton.RIGHT.value,
            )
        elif command.action is DesktopAction.DOUBLE_CLICK:
            await sandbox.mouse.click(
                command.point.x,
                command.point.y,
                button=MouseButton.LEFT.value,
                double=True,
            )
        elif command.action is DesktopAction.TRIPLE_CLICK:
            await sandbox.mouse.click(
                command.point.x,
                command.point.y,
                button=MouseButton.LEFT.value,
                double=True,
            )
            await asyncio.sleep(0.05)
            await sandbox.mouse.click(
                command.point.x,
                command.point.y,
                button=MouseButton.LEFT.value,
            )
        elif command.action is DesktopAction.MIDDLE_CLICK:
            await sandbox.mouse.click(
                command.point.x,
                command.point.y,
                button=MouseButton.MIDDLE.value,
            )
        elif command.action is DesktopAction.TYPE:
            await sandbox.keyboard.type(command.text)
        elif command.action is DesktopAction.KEY:
            key = normalize_key(command.key or command.text, key_aliases)
            action["key"] = key
            if "+" in key:
                await sandbox.keyboard.hotkey(key)
            else:
                await sandbox.keyboard.press(key)
        elif command.action is DesktopAction.SCROLL:
            await sandbox.mouse.scroll(
                command.point.x,
                command.point.y,
                command.direction.value,
                command.amount,
            )
        elif command.action is DesktopAction.MOVE:
            await sandbox.mouse.move(command.point.x, command.point.y)
        elif command.action is DesktopAction.DRAG:
            await sandbox.mouse.drag(
                command.start_point.x,
                command.start_point.y,
                command.point.x,
                command.point.y,
            )
        elif command.action is DesktopAction.WAIT:
            await asyncio.sleep(command.duration)
        else:
            return f"Unknown action: {command.label}", None, None
    except httpx.HTTPStatusError as e:
        detail = e.response.text.strip().replace("\n", " ")[:240]
        msg = f"Action '{command.label}' failed: HTTP {e.response.status_code} {detail}"
        _log.warning(msg)
        ss = await _take_screenshot_with_recovery(sandbox, command.label)
        if ss is None:
            return msg, None, None
        (images_dir / img_name).write_bytes(ss)
        return msg, ss, f"images/{img_name}"
    except httpx.HTTPError as e:
        msg = f"Action '{command.label}' failed: {type(e).__name__}: {e}"
        _log.warning(msg)
        ss = await _take_screenshot_with_recovery(sandbox, command.label)
        if ss is None:
            return msg, None, None
        (images_dir / img_name).write_bytes(ss)
        return msg, ss, f"images/{img_name}"

    action_elapsed = time.monotonic() - t0
    await asyncio.sleep(2)
    ss = await _take_screenshot_with_recovery(sandbox, command.label)
    if ss is None:
        return (
            f"Action '{command.label}' executed; screenshot failed after retries",
            None,
            None,
        )
    annotated = _annotate_click(ss, action)
    (images_dir / img_name).write_bytes(annotated)
    total_elapsed = time.monotonic() - t0
    screenshot_elapsed = total_elapsed - action_elapsed
    _log.info(
        f"action {command.label}: {action_elapsed:.2f}s + "
        f"screenshot {screenshot_elapsed:.2f}s = {total_elapsed:.2f}s total"
    )
    return f"Action '{command.label}' executed", ss, f"images/{img_name}"


async def _take_screenshot_with_recovery(
    sandbox: ComputerSandbox, action_type: str
) -> bytes | None:
    attempts = 4
    for attempt in range(1, attempts + 1):
        try:
            return await sandbox.screenshot.take_full_screen()
        except httpx.HTTPStatusError as e:
            if attempt == attempts:
                _log.warning(
                    f"screenshot after {action_type} failed after retries: "
                    f"HTTP {e.response.status_code} {e.response.text[:160]}"
                )
                return None
            _log.warning(
                f"screenshot after {action_type} failed: HTTP {e.response.status_code}; "
                f"retrying in 10s ({attempt}/{attempts - 1})"
            )
            await asyncio.sleep(10)
        except httpx.HTTPError as e:
            if attempt == attempts:
                _log.warning(
                    f"screenshot after {action_type} failed after retries: {type(e).__name__}: {e}"
                )
                return None
            _log.warning(
                f"screenshot after {action_type} failed: {type(e).__name__}; "
                f"retrying in 10s ({attempt}/{attempts - 1})"
            )
            await asyncio.sleep(10)
