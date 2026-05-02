"""UI Automation (UIA) inspector for extracting accessible UI controls.

Uses pywinauto's UIA backend to extract the accessibility tree from
the active window. Returns structured control info that the agent
can use for reliable interaction (clicking by name instead of coordinates).

Windows-only. Falls back gracefully on other platforms.
"""

from __future__ import annotations

import logging
import sys
from typing import Any, TypedDict

logger = logging.getLogger(__name__)

# Maximum controls to return (keep LLM context manageable)
MAX_CONTROLS = 500


class ControlInfo(TypedDict):
    """Structured info about a single UI control."""

    index: int
    name: str
    control_type: str
    rect: tuple[int, int, int, int]  # (left, top, right, bottom)
    enabled: bool
    automation_id: str
    value: str


def inspect_window(hwnd: int | None = None) -> list[ControlInfo]:
    """Extract all interactive UI controls from a window using UIA.

    Args:
        hwnd: Window handle to inspect. If None, uses the foreground window.

    Returns:
        List of ControlInfo dicts with name, type, bounding box, etc.
        Limited to MAX_CONTROLS elements for performance.
    """
    if sys.platform != "win32":
        return []

    try:
        from pywinauto import Desktop
        from pywinauto.controls.uiawrapper import UIAWrapper

        desktop = Desktop(backend="uia")

        if hwnd:
            try:
                window = desktop.window(handle=hwnd)
            except Exception:
                window = desktop.top_window()
        else:
            window = desktop.top_window()

        if not window:
            return []

        wrapper: UIAWrapper = window.wrapper_object()
        controls: list[ControlInfo] = []

        # Walk the control tree, depth-limited
        _walk_controls(wrapper, controls, depth=0, max_depth=8)

        return controls[:MAX_CONTROLS]

    except ImportError:
        logger.debug("pywinauto not installed — UIA inspection unavailable")
        return []
    except Exception as e:
        logger.debug("UIA inspection failed: %s", e)
        return []


def find_control_by_name(
    name: str,
    hwnd: int | None = None,
) -> ControlInfo | None:
    """Find a single control by its accessible name (case-insensitive partial match).

    Args:
        name: Control name to search for (partial, case-insensitive).
        hwnd: Optional window handle to search within.

    Returns:
        The first matching ControlInfo, or None.
    """
    controls = inspect_window(hwnd)
    name_lower = name.lower()
    for ctrl in controls:
        if name_lower in ctrl["name"].lower():
            return ctrl
    return None


def get_foreground_hwnd() -> int | None:
    """Get the handle of the foreground window."""
    if sys.platform != "win32":
        return None
    try:
        import ctypes

        return ctypes.windll.user32.GetForegroundWindow()
    except Exception:
        return None


def get_foreground_process_name() -> str:
    """Get the process name of the foreground window."""
    if sys.platform != "win32":
        return ""
    try:
        import ctypes
        from ctypes import wintypes

        user32 = ctypes.windll.user32
        hwnd = user32.GetForegroundWindow()
        if not hwnd:
            return ""

        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

        import psutil

        proc = psutil.Process(pid.value)
        return proc.name()
    except Exception:
        return ""


def _walk_controls(
    wrapper: Any,
    result: list[ControlInfo],
    depth: int,
    max_depth: int,
) -> None:
    """Recursively walk the UIA control tree."""
    if depth > max_depth or len(result) >= MAX_CONTROLS:
        return

    try:
        children = wrapper.children()
    except Exception:
        return

    for child in children:
        if len(result) >= MAX_CONTROLS:
            break

        try:
            name = child.window_text() or ""
            control_type = child.element_info.control_type or ""
            rect = child.rectangle()
            enabled = child.is_enabled()
            auto_id = getattr(child.element_info, "automation_id", "") or ""

            # Get value for text inputs
            value = ""
            try:
                value = child.get_value() if hasattr(child, "get_value") else ""
            except Exception:
                pass

            # Filter: skip invisible/tiny controls and nameless non-interactive ones
            width = rect.right - rect.left
            height = rect.bottom - rect.top
            if width <= 0 or height <= 0:
                continue

            # Only include controls that are potentially useful
            interactive_types = {
                "Button",
                "Edit",
                "ComboBox",
                "CheckBox",
                "RadioButton",
                "MenuItem",
                "TabItem",
                "ListItem",
                "TreeItem",
                "Hyperlink",
                "Slider",
                "Spinner",
                "Text",
                "Image",
                "Menu",
                "MenuBar",
                "ToolBar",
                "StatusBar",
                "DataItem",
                "Document",
                "Pane",
                "Window",
                "Group",
                "List",
                "Table",
                "Header",
                "HeaderItem",
                "ScrollBar",
            }

            # Include if it has a name or is an interactive type
            if name or control_type in interactive_types:
                result.append(
                    ControlInfo(
                        index=len(result),
                        name=name,
                        control_type=control_type,
                        rect=(rect.left, rect.top, rect.right, rect.bottom),
                        enabled=enabled,
                        automation_id=auto_id,
                        value=value or "",
                    )
                )

            # Recurse into children
            _walk_controls(child, result, depth + 1, max_depth)

        except Exception:
            continue
