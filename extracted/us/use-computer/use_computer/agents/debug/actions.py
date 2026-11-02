"""Debug-agent action dispatch."""

from __future__ import annotations

from typing import Any

from use_computer.agents.debug.models import REAL_EXEC_SLEEP_SEC, REAL_TYPE_LEN, ReplayAction
from use_computer.agents.types import Platform


def desktop_replay_platform(sandbox: Any) -> str:
    return "macos"


async def dispatch_desktop_replay_action(sandbox: Any, action: ReplayAction) -> None:
    fn = action.function
    args = action.args
    if fn in ("left_click", "click"):
        await sandbox.mouse.click(
            float(args["x"]),
            float(args["y"]),
            button=args.get("button", "left"),
            double=bool(args.get("double", False)),
        )
    elif fn == "double_click":
        await sandbox.mouse.click(float(args["x"]), float(args["y"]), button="left", double=True)
    elif fn == "right_click":
        await sandbox.mouse.click(float(args["x"]), float(args["y"]), button="right")
    elif fn in ("type_text", "type"):
        await sandbox.keyboard.type(args.get("text", ""))
    elif fn in ("press_key", "key", "press"):
        await sandbox.keyboard.press(args.get("key") or args.get("text", ""))
    elif fn == "hotkey":
        keys = args.get("keys") or args.get("key", "")
        if isinstance(keys, list):
            keys = "+".join(str(key) for key in keys)
        await sandbox.keyboard.hotkey(keys)
    elif fn == "scroll":
        await sandbox.mouse.scroll(
            float(args.get("x", 0)),
            float(args.get("y", 0)),
            args.get("direction", "down"),
            int(args.get("amount", 3)),
        )
    elif fn in ("move", "move_cursor"):
        await sandbox.mouse.move(float(args["x"]), float(args["y"]))
    elif fn == "drag":
        await sandbox.mouse.drag(
            float(args.get("startX") or args.get("from_x") or args.get("x1") or 0),
            float(args.get("startY") or args.get("from_y") or args.get("y1") or 0),
            float(args.get("endX") or args.get("to_x") or args.get("x2") or 0),
            float(args.get("endY") or args.get("to_y") or args.get("y2") or 0),
        )
    else:
        raise ValueError(f"unsupported desktop replay action: {fn!r}")


async def run_desktop_debug_action(sandbox: Any, action: str, platform: Platform) -> None:
    if action == "click":
        await sandbox.mouse.click(960, 540)
    elif action == "rclick":
        await sandbox.mouse.click(960, 540, button="right")
    elif action == "scroll":
        await sandbox.mouse.scroll(960, 540, direction="down", amount=3)
    elif action == "move":
        await sandbox.mouse.move(500, 500)
    elif action == "drag":
        await sandbox.mouse.drag(200, 200, 800, 800)
    elif action == "type":
        await sandbox.keyboard.type("x" * REAL_TYPE_LEN)
    elif action == "press":
        await sandbox.keyboard.press("return")
    elif action == "hotkey":
        await sandbox.keyboard.hotkey(_select_all_hotkey(platform))
    else:
        raise ValueError(f"unknown debug action: {action}")


async def run_realistic_exec(sandbox: Any, step: int) -> None:
    command = f"printf 'step_{step}'; sleep {REAL_EXEC_SLEEP_SEC:.1f}"
    await run_desktop_exec(sandbox, command)


async def run_desktop_exec(sandbox: Any, command: str) -> Any:
    return await sandbox.exec_ssh(command)


def _select_all_hotkey(platform: Platform) -> str:
    return "cmd+a"
