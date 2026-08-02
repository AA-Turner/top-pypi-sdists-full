"""Native cross-platform desktop notifications via ``desktop-notifier``.

No shell-out: uses the OS-native backends (D-Bus on Linux, UNUserNotifications on
macOS, WinRT toast on Windows). If the library or a backend is unavailable, the
notification is silently skipped — the hook never fails because of it.

Plain notifications dispatch in-process and the OS keeps showing them after we exit.
Action-button notifications need a live event loop to receive the click, so they run
in a short-lived detached worker (``notify_worker``) that we fire and forget.
"""

import platform
import subprocess
import sys
from pathlib import Path
from typing import Any

from .icon import icon_path

try:
    from desktop_notifier import Attachment, DesktopNotifierSync, Icon

    _AVAILABLE = True
except ImportError:
    _AVAILABLE = False

# Notification lifetime in ms (mapped to desktop-notifier's seconds; ≤0 = OS default).
# The hook overrides this from its --notify-timeout flag at startup.
DEFAULT_TIMEOUT_MS = 15000

_notifier: Any = None


def _get_notifier() -> Any:
    global _notifier
    if _notifier is None:
        _notifier = DesktopNotifierSync(app_name="Claude")
    return _notifier


def resolve_icon(icon: str | None) -> Any:
    """Build a desktop_notifier ``Icon`` from a path or a themed name (None if unavailable)."""
    if not _AVAILABLE:
        return None
    resolved = icon or icon_path()
    if not resolved:
        return None
    path = Path(resolved)
    return Icon(path=path) if path.exists() else Icon(name=resolved)


def timeout_seconds(timeout_ms: int | None) -> int:
    ms = DEFAULT_TIMEOUT_MS if timeout_ms is None else timeout_ms
    return -1 if ms <= 0 else max(1, round(ms / 1000))


def media_kwargs(icon: str | None) -> dict[str, Any]:
    """Map the Claude logo to the right desktop-notifier field per platform.

    On Linux, GNOME renders the big icon from the ``image-path`` hint (set via
    ``attachment``), not from ``app_icon`` — so pass the logo as an attachment there.
    On macOS/Windows the native ``icon`` is the app logo.
    """
    if not _AVAILABLE:
        return {}
    resolved = icon or icon_path()
    if resolved and platform.system() == "Linux":
        path = Path(resolved)
        if path.exists():
            return {"attachment": Attachment(path=path)}
    return {"icon": resolve_icon(icon)}


def send(title: str, body: str, icon: str | None = None, timeout_ms: int | None = None) -> None:
    """Show a plain native notification, best-effort (no-op if the library is missing)."""
    if not _AVAILABLE:
        return
    try:
        _get_notifier().send(
            title=title,
            message=body,
            timeout=timeout_seconds(timeout_ms),
            **media_kwargs(icon),
        )
    except Exception:  # noqa: BLE001 — best-effort; a notification must never break the hook
        pass


def send_action(
    title: str,
    body: str,
    label: str,
    action: str,
    icon: str | None = None,
    timeout_ms: int | None = None,
    until_iso: str = "",
) -> None:
    """Show a notification with an action button (``action`` ∈ unblock/block).

    Runs in a detached ``notify_worker`` process that stays alive until the
    notification expires so the button callback can fire and toggle the override.
    """
    if not _AVAILABLE:
        return
    ms = DEFAULT_TIMEOUT_MS if timeout_ms is None else timeout_ms
    args = [
        sys.executable,
        "-m",
        "pysae_ai_tools.usage.notify_worker",
        title,
        body,
        icon or icon_path() or "",
        str(ms),
        label,
        action,
        until_iso,
    ]
    try:
        subprocess.Popen(
            args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )
    except (OSError, ValueError):
        pass
