"""File-read and shell-command enforcement via local pattern matching."""

from __future__ import annotations

import os

from runlayer_cli import regex_safe
from runlayer_cli.hook import messages

_ENV_FILE_NAMES = {".env", ".envrc"}
_ENV_FILE_PREFIXES = (".env.",)
_ENV_FILE_SUFFIXES = (".env",)

_MCP_CONFIG_NAMES = {
    "mcp.json",
    "mcp_config.json",
    ".mcp.json",
    "mcp-config.json",
    "mcp.yaml",
    "mcp.yml",
    ".claude.json",
    "claude_desktop_config.json",
}

_SHELL_SPLIT_RE = regex_safe.compile(r"[|;&<>\n`]")
_SUBSHELL_RE = regex_safe.compile(r"\$\(")


class FilePolicyViolation(Exception):
    """Raised when a file access violates policy."""

    def __init__(self, user_msg: str, agent_msg: str) -> None:
        self.user_msg = user_msg
        self.agent_msg = agent_msg
        super().__init__(user_msg)


def check_file_read(file_path: str) -> None:
    """Raise FilePolicyViolation if *file_path* matches a protected pattern."""
    if not file_path:
        return

    basename = os.path.basename(file_path)
    lower_basename = basename.lower()

    if (
        lower_basename in _ENV_FILE_NAMES
        or any(lower_basename.startswith(p) for p in _ENV_FILE_PREFIXES)
        or any(lower_basename.endswith(s) for s in _ENV_FILE_SUFFIXES)
    ):
        user_msg, agent_msg = messages.file_access_env(file_path)
        raise FilePolicyViolation(user_msg, agent_msg)

    if lower_basename in _MCP_CONFIG_NAMES:
        user_msg, agent_msg = messages.file_access_mcp_config(file_path)
        raise FilePolicyViolation(user_msg, agent_msg)

    if lower_basename == "settings.json":
        # Normalize backslashes so Windows paths (C:\\Users\\u\\.claude\\settings.json)
        # match the same forward-slash pattern used on POSIX. Mirrors the
        # _normalized_dir approach in clients.py for cross-platform matching.
        lower_path = file_path.lower().replace("\\", "/")
        if "/.claude/settings.json" in lower_path:
            user_msg, agent_msg = messages.file_access_claude_settings(file_path)
            raise FilePolicyViolation(user_msg, agent_msg)


def check_bash_command(command: str) -> None:
    """Scan a shell command string for references to protected files."""
    if not command:
        return

    sanitized = _SHELL_SPLIT_RE.sub(" ", command)
    sanitized = _SUBSHELL_RE.sub("  ", sanitized)
    sanitized = sanitized.replace(")", " ")

    for word in sanitized.split():
        if not word or word.startswith("-") or word[0].isdigit():
            continue
        if word in ("''", '""'):
            continue
        word = word.strip('"').strip("'")
        check_file_read(word)
