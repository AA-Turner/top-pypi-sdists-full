"""App-specific knowledge base for GhostPC.

Maps process names to keyboard shortcuts, UI tips, search shortcuts,
and protocol handlers. Injected into the model's dynamic instruction
so it can use shortcuts instead of clicking through menus.
"""

from __future__ import annotations

from typing import TypedDict


class AppKnowledge(TypedDict, total=False):
    """Knowledge about a specific application."""

    display_name: str
    shortcuts: dict[str, str]  # action → key combo
    ui_tips: list[str]
    search_shortcut: str
    protocol: str  # URI scheme (e.g., "discord://")
    protocol_examples: list[str]


APP_KNOWLEDGE: dict[str, AppKnowledge] = {
    "discord.exe": {
        "display_name": "Discord",
        "shortcuts": {
            "Quick Switcher (search)": "Ctrl+K",
            "Search": "Ctrl+F",
            "Toggle Mute": "Ctrl+Shift+M",
            "Toggle Deafen": "Ctrl+Shift+D",
            "Create/Join Server": "Ctrl+Shift+N",
            "Navigate channels up": "Alt+Up",
            "Navigate channels down": "Alt+Down",
            "Mark as Read": "Escape",
            "Upload File": "Ctrl+Shift+U",
        },
        "ui_tips": [
            "Use Ctrl+K to search for channels, DMs, or servers instantly.",
            "Server list is on the far left; channels on the left panel.",
            "Right-click a channel for options like mute, notifications, etc.",
        ],
        "search_shortcut": "Ctrl+K",
        "protocol": "discord://",
        "protocol_examples": [
            "discord://discord.com/channels/@me  (open DMs)",
        ],
    },
    "spotify.exe": {
        "display_name": "Spotify",
        "shortcuts": {
            "Search": "Ctrl+L",
            "Play/Pause": "Space",
            "Next Track": "Ctrl+Right",
            "Previous Track": "Ctrl+Left",
            "Volume Up": "Ctrl+Up",
            "Volume Down": "Ctrl+Down",
            "Toggle Shuffle": "Ctrl+S",
            "Toggle Repeat": "Ctrl+R",
            "Like Song": "Alt+Shift+B",
        },
        "ui_tips": [
            "Use Ctrl+L to jump directly to the search bar.",
            "Playback controls are at the bottom bar.",
            "Left sidebar has Home, Search, and Your Library.",
        ],
        "search_shortcut": "Ctrl+L",
        "protocol": "spotify://",
        "protocol_examples": [
            "spotify://track/<id>  (play a specific track)",
            "spotify://playlist/<id>  (open a playlist)",
        ],
    },
    "slack.exe": {
        "display_name": "Slack",
        "shortcuts": {
            "Quick Switcher": "Ctrl+K",
            "Search": "Ctrl+F",
            "New Message": "Ctrl+N",
            "Toggle Sidebar": "Ctrl+Shift+D",
            "Channel Info": "Ctrl+Shift+I",
            "Set Status": "Ctrl+Shift+Y",
            "Upload File": "Ctrl+U",
            "Threads": "Ctrl+Shift+T",
        },
        "ui_tips": [
            "Use Ctrl+K to quickly jump to any channel or DM.",
            "Workspace switcher is in the top-left corner.",
            "Use @ to mention someone, # to link a channel.",
        ],
        "search_shortcut": "Ctrl+K",
        "protocol": "slack://",
        "protocol_examples": [
            "slack://channel?team=<team>&id=<channel>  (open a channel)",
        ],
    },
    "code.exe": {
        "display_name": "VS Code",
        "shortcuts": {
            "Command Palette": "Ctrl+Shift+P",
            "Quick Open (file)": "Ctrl+P",
            "Search in Files": "Ctrl+Shift+F",
            "Toggle Terminal": "Ctrl+`",
            "Toggle Sidebar": "Ctrl+B",
            "Go to Line": "Ctrl+G",
            "Find": "Ctrl+F",
            "Find and Replace": "Ctrl+H",
            "Save": "Ctrl+S",
            "Close Tab": "Ctrl+W",
            "Split Editor": "Ctrl+\\",
            "Toggle Word Wrap": "Alt+Z",
        },
        "ui_tips": [
            "Use Ctrl+Shift+P for ANY action — command palette is the fastest way.",
            "Ctrl+P opens quick file search — type filename to jump to it.",
            "The integrated terminal (Ctrl+`) avoids needing a separate window.",
        ],
        "search_shortcut": "Ctrl+P",
        "protocol": "vscode://",
        "protocol_examples": [
            "vscode://file/<path>  (open a file in VS Code)",
        ],
    },
    "explorer.exe": {
        "display_name": "File Explorer",
        "shortcuts": {
            "Address Bar": "Ctrl+L",
            "Search": "Ctrl+E",
            "New Folder": "Ctrl+Shift+N",
            "Rename": "F2",
            "Delete": "Delete",
            "Properties": "Alt+Enter",
            "Select All": "Ctrl+A",
            "Refresh": "F5",
            "Go Up": "Alt+Up",
            "Go Back": "Alt+Left",
        },
        "ui_tips": [
            "Ctrl+L focuses the address bar — type a path to navigate directly.",
            "F2 renames the selected file/folder.",
            "Terminal commands are often faster for file operations.",
        ],
        "search_shortcut": "Ctrl+E",
    },
    "notepad.exe": {
        "display_name": "Notepad",
        "shortcuts": {
            "New": "Ctrl+N",
            "Open": "Ctrl+O",
            "Save": "Ctrl+S",
            "Save As": "Ctrl+Shift+S",
            "Find": "Ctrl+F",
            "Find and Replace": "Ctrl+H",
            "Go to Line": "Ctrl+G",
            "Select All": "Ctrl+A",
            "Zoom In": "Ctrl++",
            "Zoom Out": "Ctrl+-",
        },
        "ui_tips": [
            "Ctrl+F opens Find dialog, Ctrl+H opens Find and Replace.",
            "Windows 11 Notepad supports tabs — Ctrl+N opens a new tab.",
        ],
        "search_shortcut": "Ctrl+F",
    },
    "winword.exe": {
        "display_name": "Microsoft Word",
        "shortcuts": {
            "Save": "Ctrl+S",
            "Find": "Ctrl+F",
            "Find and Replace": "Ctrl+H",
            "Bold": "Ctrl+B",
            "Italic": "Ctrl+I",
            "Underline": "Ctrl+U",
            "Undo": "Ctrl+Z",
            "Redo": "Ctrl+Y",
            "Print": "Ctrl+P",
            "Select All": "Ctrl+A",
        },
        "ui_tips": [
            "Use Ctrl+F for quick text search within the document.",
            "The Ribbon has tabs: Home, Insert, Design, Layout, etc.",
            "Ctrl+S saves immediately; don't rely on autosave for important work.",
        ],
        "search_shortcut": "Ctrl+F",
    },
    "excel.exe": {
        "display_name": "Microsoft Excel",
        "shortcuts": {
            "Save": "Ctrl+S",
            "Find": "Ctrl+F",
            "Find and Replace": "Ctrl+H",
            "Go to Cell": "Ctrl+G",
            "Insert Row": "Ctrl+Shift++",
            "Delete Row": "Ctrl+-",
            "AutoSum": "Alt+=",
            "New Sheet": "Shift+F11",
            "Format Cells": "Ctrl+1",
            "Select Column": "Ctrl+Space",
            "Select Row": "Shift+Space",
        },
        "ui_tips": [
            "Click the Name Box (left of formula bar) and type a cell reference to jump to it.",
            "Ctrl+F finds text in cells; Ctrl+H replaces.",
            "Use the formula bar to edit cell contents precisely.",
        ],
        "search_shortcut": "Ctrl+F",
    },
    "teams.exe": {
        "display_name": "Microsoft Teams",
        "shortcuts": {
            "Search": "Ctrl+E",
            "Command Bar": "Ctrl+/",
            "Go to Chat": "Ctrl+2",
            "Go to Teams": "Ctrl+3",
            "Go to Calendar": "Ctrl+4",
            "Toggle Mute": "Ctrl+Shift+M",
            "Toggle Video": "Ctrl+Shift+O",
            "Raise Hand": "Ctrl+Shift+K",
            "New Chat": "Ctrl+N",
        },
        "ui_tips": [
            "Use Ctrl+E to search for people, messages, and files.",
            "Ctrl+/ shows all available keyboard shortcuts.",
            "Left sidebar: Activity, Chat, Teams, Calendar, Files.",
        ],
        "search_shortcut": "Ctrl+E",
    },
    "outlook.exe": {
        "display_name": "Microsoft Outlook",
        "shortcuts": {
            "New Email": "Ctrl+N",
            "Search": "Ctrl+E",
            "Reply": "Ctrl+R",
            "Reply All": "Ctrl+Shift+R",
            "Forward": "Ctrl+F",
            "Send": "Ctrl+Enter",
            "Switch to Mail": "Ctrl+1",
            "Switch to Calendar": "Ctrl+2",
            "Switch to Contacts": "Ctrl+3",
        },
        "ui_tips": [
            "Use Ctrl+E to search across all mail.",
            "Ctrl+N creates a new email from any view.",
            "Navigation pane on the left: Mail, Calendar, People, Tasks.",
        ],
        "search_shortcut": "Ctrl+E",
    },
}


def get_app_hints(process_name: str) -> str | None:
    """Get formatted knowledge hints for the active application.

    Args:
        process_name: The process name (e.g., "discord.exe").

    Returns:
        Formatted instruction text, or None if no knowledge available.
    """
    knowledge = APP_KNOWLEDGE.get(process_name.lower())
    if not knowledge:
        return None

    parts: list[str] = []
    display = knowledge.get("display_name", process_name)
    parts.append(f"Active app: {display}")

    shortcuts = knowledge.get("shortcuts")
    if shortcuts:
        shortcut_lines = [f"  {action}: {key}" for action, key in shortcuts.items()]
        parts.append("Shortcuts:\n" + "\n".join(shortcut_lines))

    search = knowledge.get("search_shortcut")
    if search:
        parts.append(f"Quick search: {search}")

    tips = knowledge.get("ui_tips")
    if tips:
        parts.append("Tips:\n" + "\n".join(f"  - {t}" for t in tips))

    protocol = knowledge.get("protocol")
    if protocol:
        examples = knowledge.get("protocol_examples", [])
        proto_text = f"Protocol: {protocol}"
        if examples:
            proto_text += "\n" + "\n".join(f"  {ex}" for ex in examples)
        parts.append(proto_text)

    return "\n".join(parts)
