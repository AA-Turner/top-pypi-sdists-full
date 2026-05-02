"""Custom tools for the GhostPC agent.

These are plain Python functions that ADK auto-wraps into FunctionTools.
They handle desktop actions that aren't part of the standard ComputerUse
toolset (terminal, app launching, screenshot sharing, UIA interaction, etc.).

ADK discovers tools by their function signature and docstring.
A `tool_context: ToolContext` parameter is auto-injected for state access.
"""

from __future__ import annotations

from google.adk.tools.tool_context import ToolContext


async def run_terminal(command: str, tool_context: ToolContext) -> dict:
    """Run a PowerShell/terminal command and return the output.

    Use this for any shell commands: git, npm, pip, file operations, etc.
    The command runs on the user's Windows PC.
    Output is truncated to 3000 chars to fit context.

    Args:
        command: The PowerShell command to execute.
    """
    from ghost_pc.desktop.terminal import run_command

    result = await run_command(command)
    output = str(result["stdout"] or result["stderr"] or result.get("error", ""))

    # Truncate long output to fit model context
    if len(output) > 3000:
        output = output[:3000] + "\n... (truncated)"

    return {
        "status": "ok" if result["returncode"] == 0 else "error",
        "output": output,
        "returncode": result["returncode"],
    }


async def open_application(name: str) -> dict:
    """Launch a native Windows desktop application by name.

    Smart behavior: if the app is already running, focuses its window
    instead of opening a duplicate. Discovers installed apps automatically,
    so any app installed on the PC works — not just the common ones.

    Common names: notepad, calculator, explorer, powershell, terminal,
    vscode, spotify, slack, discord, teams, word, excel, figma, obsidian.
    Do NOT use this to open browsers — browser use is disabled.

    Args:
        name: The application name (e.g., 'discord', 'notepad', 'vscode').
    """
    from ghost_pc.desktop.apps import open_app

    return await open_app(name)


async def send_screenshot_to_user(
    caption: str = "Here's your screen",
    tool_context: ToolContext | None = None,
) -> dict:
    """Take a screenshot and send it to the user on WhatsApp.

    Use this when the user asks to see their screen, or after completing
    a visual task to show the result.

    Args:
        caption: Caption to include with the screenshot.
    """
    if tool_context:
        # Signal the orchestrator to capture and send a screenshot.
        # The after_tool_callback in action_loop.py picks this up.
        tool_context.state["screenshot_requested"] = True
        tool_context.state["screenshot_caption"] = caption
    return {"status": "ok", "action": "screenshot will be sent to user"}


async def task_complete(summary: str) -> dict:
    """Signal that the requested task is finished.

    Call this when you've completed what the user asked for.
    Include a brief summary of what was done.

    Args:
        summary: Brief summary of what was accomplished.
    """
    return {"status": "complete", "summary": summary}


async def read_clipboard() -> dict:
    """Read the current text content from the Windows clipboard.

    Use this when the user says "what's copied" or "paste what I have".
    """
    from ghost_pc.desktop.clipboard import get_clipboard_text

    text = get_clipboard_text()
    if text is None:
        return {"status": "empty", "content": ""}
    return {"status": "ok", "content": text}


async def write_clipboard(text: str) -> dict:
    """Copy text to the Windows clipboard.

    Use this when the user says "copy this" or when you need to
    prepare text for pasting somewhere.

    Args:
        text: The text to copy to clipboard.
    """
    from ghost_pc.desktop.clipboard import set_clipboard_text

    success = set_clipboard_text(text)
    return {"status": "ok" if success else "error"}


async def list_files(path: str) -> dict:
    """List files and folders in a directory.

    Use this to explore the user's filesystem. Common paths:
    ~/Desktop, ~/Documents, ~/Downloads.

    Args:
        path: Directory path to list.
    """
    from ghost_pc.desktop.filesystem import list_directory

    return list_directory(path)


async def find_files(directory: str, pattern: str) -> dict:
    """Search for files matching a pattern in a directory.

    Args:
        directory: Root directory to search in.
        pattern: Glob pattern (e.g., "*.pdf", "report*", "*.docx").
    """
    from ghost_pc.desktop.filesystem import search_files

    return search_files(directory, pattern)


async def read_text_file(path: str) -> dict:
    """Read the contents of a text file.

    Args:
        path: Path to the text file.
    """
    from ghost_pc.desktop.filesystem import read_file

    return read_file(path)


# --- Click variants ---


async def double_click_at(x: int, y: int) -> dict:
    """Double-click at screen coordinates.

    Use this to open files, folders, desktop icons, or any element
    that requires a double-click. The model should infer when a
    double-click is needed (e.g. opening a desktop shortcut, launching
    a file in Explorer, selecting a word in a text editor).

    Args:
        x: X pixel coordinate on screen.
        y: Y pixel coordinate on screen.
    """
    import asyncio

    from ghost_pc.desktop.input import double_click

    await asyncio.to_thread(double_click, x, y)
    return {"status": "ok", "action": "double_click", "x": x, "y": y}


async def right_click_at(x: int, y: int) -> dict:
    """Right-click at screen coordinates to open a context menu.

    Use this when you need to access right-click context menus
    (e.g. "Copy", "Paste", "Properties", "New > Folder", rename
    options, desktop right-click for display settings, etc.).

    Args:
        x: X pixel coordinate on screen.
        y: Y pixel coordinate on screen.
    """
    import asyncio

    from ghost_pc.desktop.input import click

    await asyncio.to_thread(click, x, y, "right")
    return {"status": "ok", "action": "right_click", "x": x, "y": y}


# --- Window management ---


async def get_open_windows() -> dict:
    """List all currently visible windows with their titles.

    Use this to find which applications are open, or to get the
    exact window title before focusing/minimizing/closing a window.
    """
    import asyncio

    from ghost_pc.desktop.apps import list_windows

    windows = await asyncio.to_thread(list_windows)
    return {
        "status": "ok",
        "windows": [{"title": w["title"], "hwnd": w["hwnd"]} for w in windows],
        "count": len(windows),
    }


async def switch_to_window(title: str) -> dict:
    """Bring a window to the foreground by searching its title.

    Matches partial titles (case-insensitive). For example,
    "chrome" will match "Google Chrome - New Tab".

    Args:
        title: Partial window title to search for.
    """
    import asyncio

    from ghost_pc.desktop.apps import focus_window

    found = await asyncio.to_thread(focus_window, title)
    if found:
        return {"status": "ok", "action": f"focused window matching '{title}'"}
    return {"status": "error", "message": f"No window found matching '{title}'"}


async def manage_window(action: str, title: str | None = None) -> dict:
    """Minimize, maximize, or close a window.

    If no title is given, acts on the currently active window.

    Args:
        action: One of "minimize", "maximize", or "close".
        title: Optional partial window title. If omitted, targets the active window.
    """
    import asyncio

    from ghost_pc.desktop.apps import close_window, maximize_window, minimize_window

    actions = {
        "minimize": minimize_window,
        "maximize": maximize_window,
        "close": close_window,
    }
    fn = actions.get(action)
    if fn is None:
        return {
            "status": "error",
            "message": f"Unknown action: {action}. Use minimize/maximize/close.",
        }

    success = await asyncio.to_thread(fn, title)
    target = f"window '{title}'" if title else "active window"
    if success:
        return {"status": "ok", "action": f"{action}d {target}"}
    return {"status": "error", "message": f"No window found matching '{title}'"}


# --- UIA interaction tools (Phase 3) ---


async def inspect_ui() -> dict:
    """Get the full UIA control tree of the active window.

    Returns a structured list of all interactive UI elements with their
    names, types, positions, and states. Use this to discover what controls
    are available before using uia_click or uia_type.
    """
    import asyncio

    try:
        from ghost_pc.desktop.uia_inspector import inspect_window

        controls = await asyncio.to_thread(inspect_window)
        if not controls:
            return {"status": "ok", "controls": [], "count": 0, "note": "No controls found"}

        # Format for the model
        formatted = []
        for ctrl in controls[:100]:  # Limit to 100 for context
            entry: dict[str, str | int | bool] = {
                "index": ctrl["index"],
                "name": ctrl["name"],
                "type": ctrl["control_type"],
                "enabled": ctrl["enabled"],
            }
            if ctrl.get("value"):
                entry["value"] = ctrl["value"][:100]
            formatted.append(entry)

        return {"status": "ok", "controls": formatted, "count": len(controls)}
    except ImportError:
        return {"status": "unavailable", "error": "pywinauto not installed"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def uia_click(control_name: str) -> dict:
    """Click a UI control by its accessible name.

    More reliable than pixel clicking — finds the control via UIA
    accessibility tree and clicks its center coordinates.
    Use when you can see a labeled control in the UIA data or inspect_ui output.

    Args:
        control_name: The name (or partial name) of the control to click.
    """
    import asyncio

    try:
        from ghost_pc.desktop.input import click
        from ghost_pc.desktop.uia_inspector import find_control_by_name

        ctrl = await asyncio.to_thread(find_control_by_name, control_name)
        if ctrl is None:
            return {
                "status": "error",
                "message": f"No control found matching '{control_name}'",
            }

        if not ctrl["enabled"]:
            return {
                "status": "error",
                "message": f"Control '{control_name}' is disabled",
            }

        left, top, right, bottom = ctrl["rect"]
        center_x = (left + right) // 2
        center_y = (top + bottom) // 2

        await asyncio.to_thread(click, center_x, center_y)
        return {
            "status": "ok",
            "action": (
                f"clicked '{ctrl['name']}' ({ctrl['control_type']}) at ({center_x},{center_y})"
            ),
        }
    except ImportError:
        return {"status": "unavailable", "error": "pywinauto not installed"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def uia_type(control_name: str, text: str) -> dict:
    """Type text into a named input field.

    Finds the control via UIA, clicks it to focus, and types the text.

    Args:
        control_name: The name of the input field to type into.
        text: The text to type.
    """
    import asyncio

    try:
        from ghost_pc.desktop.input import click, type_text
        from ghost_pc.desktop.uia_inspector import find_control_by_name

        ctrl = await asyncio.to_thread(find_control_by_name, control_name)
        if ctrl is None:
            return {
                "status": "error",
                "message": f"No control found matching '{control_name}'",
            }

        left, top, right, bottom = ctrl["rect"]
        center_x = (left + right) // 2
        center_y = (top + bottom) // 2

        # Click to focus, then type
        await asyncio.to_thread(click, center_x, center_y)
        await asyncio.sleep(0.1)
        await asyncio.to_thread(type_text, text)

        return {
            "status": "ok",
            "action": f"typed '{text[:50]}' into '{ctrl['name']}' at ({center_x},{center_y})",
        }
    except ImportError:
        return {"status": "unavailable", "error": "pywinauto not installed"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def uia_get_value(control_name: str) -> dict:
    """Read the current value/text of a UI control.

    Works for text fields, labels, combo boxes, etc.

    Args:
        control_name: The name of the control to read.
    """
    import asyncio

    try:
        from ghost_pc.desktop.uia_inspector import find_control_by_name

        ctrl = await asyncio.to_thread(find_control_by_name, control_name)
        if ctrl is None:
            return {
                "status": "error",
                "message": f"No control found matching '{control_name}'",
            }

        return {
            "status": "ok",
            "name": ctrl["name"],
            "type": ctrl["control_type"],
            "value": ctrl.get("value", ""),
            "enabled": ctrl["enabled"],
        }
    except ImportError:
        return {"status": "unavailable", "error": "pywinauto not installed"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


# --- System control tools (Phase 4) ---


async def set_volume(level: int) -> dict:
    """Set the system volume level (0-100).

    Args:
        level: Volume level from 0 (mute) to 100 (maximum).
    """
    try:
        from ghost_pc.desktop.system import set_system_volume

        return await set_system_volume(level)
    except ImportError:
        return {"status": "unavailable", "error": "pycaw not installed"}


async def get_system_info() -> dict:
    """Get system information: CPU usage, RAM, disk space, battery status.

    Use this when the user asks about their computer's performance or status.
    """
    try:
        from ghost_pc.desktop.system import get_system_status

        return await get_system_status()
    except ImportError:
        return {"status": "unavailable", "error": "psutil not installed"}


async def list_processes(sort_by: str = "cpu") -> dict:
    """List running processes sorted by resource usage.

    Args:
        sort_by: Sort by "cpu" or "memory".
    """
    try:
        from ghost_pc.desktop.system import list_running_processes

        return await list_running_processes(sort_by)
    except ImportError:
        return {"status": "unavailable", "error": "psutil not installed"}


async def kill_process(name: str) -> dict:
    """Kill a process by name.

    Args:
        name: Process name (e.g., "chrome.exe", "notepad.exe").
    """
    try:
        from ghost_pc.desktop.system import terminate_process

        return await terminate_process(name)
    except ImportError:
        return {"status": "unavailable", "error": "psutil not installed"}


async def set_reminder(
    description: str,
    delay_minutes: int,
    tool_context: ToolContext,
) -> dict:
    """Set a reminder that will notify the user after a delay.

    Use this when the user says "remind me in X minutes to do Y" or similar.
    The reminder will be sent as a WhatsApp message when the time comes.

    Args:
        description: What to remind the user about.
        delay_minutes: Minutes from now to send the reminder (1-1440).
    """
    delay_minutes = max(1, min(1440, delay_minutes))
    # Signal the orchestrator to schedule the reminder
    tool_context.state["temp:set_reminder"] = {
        "description": description,
        "delay_minutes": delay_minutes,
    }
    return {
        "status": "ok",
        "message": f"Reminder set for {delay_minutes} minutes from now: {description}",
    }


async def click_label(label: int, tool_context: ToolContext) -> dict:
    """Click on a numbered SoM label from the annotated screenshot.

    Each screenshot is annotated with numbered labels (#0, #1, #2, ...) on
    interactive UI controls. Use this tool to click a label by its number —
    this is more precise than guessing pixel coordinates.

    Prefer this over click_at when labeled controls are visible.

    Args:
        label: The label number shown on the screenshot (e.g., 0, 1, 5).
    """
    import asyncio

    controls_map: list[dict] = tool_context.state.get("temp:controls_map", [])
    if not controls_map:
        return {
            "status": "error",
            "message": "No labeled controls available. Use click_at(x, y) instead.",
        }

    if label < 0 or label >= len(controls_map):
        return {
            "status": "error",
            "message": (
                f"Label #{label} out of range. "
                f"Valid labels: #0 to #{len(controls_map) - 1}."
            ),
        }

    ctrl = controls_map[label]
    left, top, right, bottom = ctrl["rect"]
    center_x = (left + right) // 2
    center_y = (top + bottom) // 2

    from ghost_pc.desktop.input import click

    await asyncio.to_thread(click, center_x, center_y)
    return {
        "status": "ok",
        "action": (
            f"clicked label #{label}: {ctrl['control_type']} "
            f"'{ctrl['name']}' at ({center_x},{center_y})"
        ),
    }


async def type_into_label(
    label: int,
    text: str,
    tool_context: ToolContext,
    press_enter: bool = False,
    clear_first: bool = True,
) -> dict:
    """Click a labeled control to focus it, then type text into it.

    Use this for input fields, search boxes, text areas, etc. that have
    a SoM label number on the annotated screenshot.

    Args:
        label: The label number of the input field.
        text: The text to type into the field.
        press_enter: Whether to press Enter after typing (default: False).
        clear_first: Whether to select-all and clear before typing (default: True).
    """
    import asyncio

    controls_map: list[dict] = tool_context.state.get("temp:controls_map", [])
    if not controls_map:
        return {
            "status": "error",
            "message": "No labeled controls available. Use type_text_at(x, y, text) instead.",
        }

    if label < 0 or label >= len(controls_map):
        return {
            "status": "error",
            "message": (
                f"Label #{label} out of range. "
                f"Valid labels: #0 to #{len(controls_map) - 1}."
            ),
        }

    ctrl = controls_map[label]
    left, top, right, bottom = ctrl["rect"]
    center_x = (left + right) // 2
    center_y = (top + bottom) // 2

    from ghost_pc.desktop.input import click, hotkey, press_key, type_text

    # Click to focus the control
    await asyncio.to_thread(click, center_x, center_y)
    await asyncio.sleep(0.15)

    if clear_first:
        await asyncio.to_thread(hotkey, "ctrl", "a")
        await asyncio.sleep(0.05)
        await asyncio.to_thread(press_key, "backspace")
        await asyncio.sleep(0.05)

    await asyncio.to_thread(type_text, text)

    if press_enter:
        await asyncio.sleep(0.05)
        await asyncio.to_thread(press_key, "enter")

    return {
        "status": "ok",
        "action": (
            f"typed '{text[:50]}' into label #{label}: {ctrl['control_type']} "
            f"'{ctrl['name']}' at ({center_x},{center_y})"
        ),
    }


async def send_desktop_notification(title: str, message: str) -> dict:
    """Show a Windows toast notification on the desktop.

    Use this after completing a task or to alert the user about something.

    Args:
        title: Notification title.
        message: Notification body text.
    """
    try:
        from ghost_pc.desktop.system import show_toast_notification

        return await show_toast_notification(title, message)
    except ImportError:
        return {"status": "unavailable", "error": "windows-toasts not installed"}
