"""Detached worker for action-button notifications.

Spawned by ``notify.send_action`` as a fire-and-forget subprocess. It shows a native
notification with one button and stays alive (running the event loop) until the
notification expires, so the button callback can fire and toggle the block override
in-process — no shell-out, no CLI round-trip.

argv: title body icon timeout_ms label action until_iso
"""

import asyncio
import sys
import time

from . import notify, unblock


def _do_action(action: str, until_iso: str) -> None:
    # until_iso doubles as the window id (the window's resets_at) and the time fallback.
    until = unblock.parse_until(until_iso) if until_iso else None
    if until is None:
        until = time.time() + 3600.0
    if action == "unblock":
        unblock.set_unblock(until_iso, until)
    elif action == "block":
        unblock.set_block(until_iso, until)


async def _main(argv: list[str]) -> None:
    title, body, icon, timeout_ms_s, label, action, until_iso = (argv + [""] * 7)[:7]
    from desktop_notifier import Button, DesktopNotifier

    ms = int(timeout_ms_s or "0")
    notifier = DesktopNotifier(app_name="Claude")
    await notifier.send(
        title=title,
        message=body,
        buttons=[Button(title=label, on_pressed=lambda: _do_action(action, until_iso))],
        timeout=notify.timeout_seconds(ms),
        **notify.media_kwargs(icon or None),
    )
    # Stay alive to receive the click (bounded: never linger more than 5 min).
    await asyncio.sleep(min(max(ms / 1000 if ms > 0 else 300.0, 5.0), 300.0))


def main() -> None:
    try:
        asyncio.run(_main(sys.argv[1:]))
    except Exception:  # noqa: BLE001 — best-effort detached helper, never surfaces errors
        pass


if __name__ == "__main__":
    main()
