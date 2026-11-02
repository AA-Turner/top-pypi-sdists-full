"""Desktop platform profile and keyboard normalization."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, replace
from enum import Enum

from use_computer.agents.types import Platform

# Anthropic CUA outputs key names that don't match computer-server's expected names.
_KEY_ALIASES = {
    "Escape": "esc",
    "escape": "esc",
    "ESCAPE": "esc",
    "ESC": "esc",
    "Return": "enter",
    "return": "enter",
    "RETURN": "enter",
    "Enter": "enter",
    "enter": "enter",
    "ENTER": "enter",
    "Command": "cmd",
    "command": "cmd",
    "COMMAND": "cmd",
    "Cmd": "cmd",
    "cmd": "cmd",
    "CMD": "cmd",
    "super": "cmd",
    "SUPER": "cmd",
    "meta": "cmd",
    "META": "cmd",
    "Super_L": "cmd",
    "Meta_L": "cmd",
    "Control": "ctrl",
    "control": "ctrl",
    "CONTROL": "ctrl",
    "Ctrl": "ctrl",
    "ctrl": "ctrl",
    "CTRL": "ctrl",
    "Shift": "shift",
    "shift": "shift",
    "SHIFT": "shift",
    "Alt": "alt",
    "alt": "alt",
    "ALT": "alt",
    "Option": "alt",
    "option": "alt",
    "OPTION": "alt",
    "Backspace": "backspace",
    "backspace": "backspace",
    "BACKSPACE": "backspace",
    "Delete": "delete",
    "delete": "delete",
    "DELETE": "delete",
    "Tab": "tab",
    "tab": "tab",
    "TAB": "tab",
    "Space": "space",
    "space": "space",
    "SPACE": "space",
    "ArrowUp": "up",
    "ARROWUP": "up",
    "Up": "up",
    "up": "up",
    "UP": "up",
    "ArrowDown": "down",
    "ARROWDOWN": "down",
    "Down": "down",
    "down": "down",
    "DOWN": "down",
    "ArrowLeft": "left",
    "ARROWLEFT": "left",
    "Left": "left",
    "left": "left",
    "LEFT": "left",
    "ArrowRight": "right",
    "ARROWRIGHT": "right",
    "Right": "right",
    "right": "right",
    "RIGHT": "right",
    "Page_Up": "pageup",
    "PAGE_UP": "pageup",
    "PAGEUP": "pageup",
    "Page_Down": "pagedown",
    "PAGE_DOWN": "pagedown",
    "PAGEDOWN": "pagedown",
}


class OpenAIComputerEnvironment(str, Enum):
    MAC = "mac"


@dataclass(frozen=True)
class DesktopProfile:
    platform: Platform
    os_type: str
    notes: str = ""
    key_aliases: Mapping[str, str] | None = None
    openai_environment: OpenAIComputerEnvironment = OpenAIComputerEnvironment.MAC

    @property
    def article(self) -> str:
        return "an" if self.os_type[0].lower() in {"a", "e", "i", "o", "u"} else "a"


_DESKTOP_PROFILES = {
    Platform.MACOS: DesktopProfile(
        platform=Platform.MACOS,
        os_type="macOS",
        openai_environment=OpenAIComputerEnvironment.MAC,
    ),
}


def desktop_profile(
    platform: Platform | str = Platform.MACOS,
    *,
    os_type: str | None = None,
    platform_notes: str | None = None,
    openai_environment: OpenAIComputerEnvironment | str | None = None,
) -> DesktopProfile:
    parsed = Platform.parse(platform)
    base = _DESKTOP_PROFILES[parsed]
    environment = (
        OpenAIComputerEnvironment(openai_environment)
        if openai_environment is not None
        else base.openai_environment
    )
    return replace(
        base,
        os_type=os_type or base.os_type,
        notes=platform_notes if platform_notes is not None else base.notes,
        openai_environment=environment,
    )


def normalize_key(key: str, aliases: Mapping[str, str] | None = None) -> str:
    """Map agent key names to computer-server key names."""
    aliases = aliases if aliases is not None else _KEY_ALIASES
    if "+" in key:
        return "+".join(aliases.get(k, k) for k in key.split("+"))
    return aliases.get(key, key)
