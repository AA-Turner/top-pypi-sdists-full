"""Safety detection logic for destructive operations.

Pure functions — no I/O, no side effects. Easily testable.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field


@dataclass
class SafetyVerdict:
    needs_approval: bool
    reason: str
    tool_name: str
    details: dict[str, str] = field(default_factory=dict)
    hard_denied: bool = False
    is_hard_blocked: bool = False
    hard_block_description: str = ""
    bypass_immune: bool = False


_DEFAULT_DESTRUCTIVE_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\brm\b"),
    re.compile(r"\brmdir\b"),
    re.compile(r"\bgit\s+push\s+--force\b"),
    re.compile(r"\bgit\s+push\s+-f\b"),
    re.compile(r"\bgit\s+reset\s+--hard\b"),
    re.compile(r"\bgit\s+clean\b"),
    re.compile(r"\bgit\s+checkout\s+\.\s*$"),
    re.compile(r"\bdrop\s+table\b", re.IGNORECASE),
    re.compile(r"\bdrop\s+database\b", re.IGNORECASE),
    re.compile(r"\btruncate\b", re.IGNORECASE),
    re.compile(r">\s*/dev/(?!null\b)"),
    re.compile(r"\bchmod\s+777\b"),
    re.compile(r"\bkill\s+-9\b"),
]

_DEFAULT_SENSITIVE_PATHS: list[str] = [
    ".env",
    ".ssh",
    ".gnupg",
    ".aws/credentials",
    ".config/gcloud",
]


def _normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def check_bash_command(
    command: str,
    custom_patterns: list[str] | None = None,
) -> SafetyVerdict:
    if not command or not command.strip():
        return SafetyVerdict(needs_approval=False, reason="", tool_name="bash")

    normalized = _normalize_whitespace(command)

    for pattern in _DEFAULT_DESTRUCTIVE_PATTERNS:
        if pattern.search(normalized):
            return SafetyVerdict(
                needs_approval=True,
                reason=f"Destructive command detected: {command}",
                tool_name="bash",
                details={"command": command, "matched_pattern": pattern.pattern},
            )

    if custom_patterns:
        for raw_pattern in custom_patterns:
            try:
                compiled = re.compile(raw_pattern, re.IGNORECASE)
                if compiled.search(normalized):
                    return SafetyVerdict(
                        needs_approval=True,
                        reason=f"Custom pattern matched: {command}",
                        tool_name="bash",
                        details={"command": command, "matched_pattern": raw_pattern},
                    )
            except re.error:
                if raw_pattern.lower() in normalized.lower():
                    return SafetyVerdict(
                        needs_approval=True,
                        reason=f"Custom pattern matched: {command}",
                        tool_name="bash",
                        details={"command": command, "matched_pattern": raw_pattern},
                    )

    return SafetyVerdict(needs_approval=False, reason="", tool_name="bash")


_DEFAULT_BYPASS_IMMUNE_PATHS: list[str] = [
    ".git/hooks",
    ".anteroom/config.yaml",
    ".bashrc",
    ".bash_profile",
    ".zshrc",
    ".profile",
    ".ssh/",
    ".gnupg/",
    ".aws/credentials",
    ".config/gcloud/",
    ".netrc",
    ".kube/config",
    ".config/gh/hosts.yml",
]

# Patterns in bash commands that indicate a write to a target path.
_BASH_WRITE_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r">{1,2}\s*(\S+)"),  # > or >> redirect
    re.compile(r"\btee\s+(?:-[a-zA-Z]*\s+)*(\S+)"),  # tee [flags] path
    re.compile(r"\bmv\s+\S+\s+(\S+)"),  # mv src dest
    re.compile(r"\bcp\s+\S+\s+(\S+)"),  # cp src dest
]


def _path_matches_immune(
    path: str,
    working_dir: str,
    immune_paths: list[str],
) -> str | None:
    """Return the matched immune path pattern if *path* targets one, else None."""
    if not path or not immune_paths:
        return None

    if os.path.isabs(path):
        resolved = os.path.normpath(path)
    else:
        resolved = os.path.normpath(os.path.join(working_dir, path))

    home = os.path.expanduser("~")
    path_normalized = os.path.normpath(path)
    path_parts = path_normalized.replace("\\", "/").split("/")

    for immune in immune_paths:
        expanded = os.path.expanduser(immune) if immune.startswith("~") else immune

        if os.path.isabs(expanded):
            immune_resolved = os.path.normpath(expanded)
        else:
            immune_resolved = os.path.normpath(os.path.join(home, expanded))

        if resolved == immune_resolved or resolved.startswith(immune_resolved + os.sep):
            return immune

        # Component matching for relative paths (same approach as check_write_path).
        immune_stripped = immune.lstrip("~").lstrip("/").lstrip("\\")
        immune_norm = os.path.normpath(immune_stripped).replace("\\", "/")
        # Trailing-slash immune entries (e.g. ".ssh/") mean "anything under this dir".
        # After normpath the slash is gone so we treat them as prefix matches.
        is_dir_pattern = immune.rstrip("/\\") != immune
        immune_parts = immune_norm.split("/")
        for i in range(len(path_parts)):
            segment = path_parts[i : i + len(immune_parts)]
            if segment == immune_parts:
                if is_dir_pattern or len(path_parts) == i + len(immune_parts):
                    return immune
                # Exact-file pattern but path extends deeper — still a match
                # (e.g. immune=".anteroom/config.yaml" matches that file exactly).
                if not is_dir_pattern and len(path_parts) == i + len(immune_parts):
                    return immune
                # For dir patterns, any deeper path matches.
                if is_dir_pattern:
                    return immune
                # For exact file patterns that matched components, accept.
                return immune

    return None


def check_bypass_immune_path(
    tool_name: str,
    arguments: dict[str, str],
    working_dir: str,
    immune_paths: list[str] | None = None,
) -> SafetyVerdict | None:
    """Check if a tool call targets a bypass-immune path.

    Returns a SafetyVerdict with ``bypass_immune=True`` if the call targets an
    immune path, or ``None`` if no immune path is matched.  The verdict has
    ``needs_approval=True`` but ``hard_denied=False`` — the user can approve,
    but the prompt cannot be skipped by AUTO mode or allowed_tools.
    """
    paths_to_check = list(_DEFAULT_BYPASS_IMMUNE_PATHS) if immune_paths is None else list(immune_paths)
    if not paths_to_check:
        return None

    target_path: str | None = None

    if tool_name == "write_file":
        target_path = arguments.get("path", "")
    elif tool_name == "edit_file":
        target_path = arguments.get("file_path", "") or arguments.get("path", "")

    if tool_name in ("write_file", "edit_file") and target_path:
        matched = _path_matches_immune(target_path, working_dir, paths_to_check)
        if matched is not None:
            return SafetyVerdict(
                needs_approval=True,
                reason=f"Write to bypass-immune path: {target_path}",
                tool_name=tool_name,
                details={"path": target_path, "matched_immune": matched},
                bypass_immune=True,
            )

    if tool_name == "bash":
        command = arguments.get("command", "")
        if command:
            for pattern in _BASH_WRITE_PATTERNS:
                for m in pattern.finditer(command):
                    candidate = m.group(1)
                    matched = _path_matches_immune(candidate, working_dir, paths_to_check)
                    if matched is not None:
                        return SafetyVerdict(
                            needs_approval=True,
                            reason=f"Bash write to bypass-immune path: {candidate}",
                            tool_name="bash",
                            details={"command": command, "target_path": candidate, "matched_immune": matched},
                            bypass_immune=True,
                        )

    return None


def check_write_path(
    path: str,
    working_dir: str,
    sensitive_paths: list[str] | None = None,
) -> SafetyVerdict:
    if not path:
        return SafetyVerdict(needs_approval=False, reason="", tool_name="write_file")

    all_sensitive = list(_DEFAULT_SENSITIVE_PATHS)
    if sensitive_paths:
        all_sensitive.extend(sensitive_paths)

    if os.path.isabs(path):
        resolved = os.path.normpath(path)
    else:
        resolved = os.path.normpath(os.path.join(working_dir, path))

    home = os.path.expanduser("~")

    # Normalize path for component matching (works regardless of actual home dir)
    path_normalized = os.path.normpath(path)
    path_parts = path_normalized.replace("\\", "/").split("/")

    for sensitive in all_sensitive:
        expanded = os.path.expanduser(sensitive) if sensitive.startswith("~") else sensitive

        if os.path.isabs(expanded):
            sensitive_resolved = os.path.normpath(expanded)
        else:
            sensitive_resolved = os.path.normpath(os.path.join(home, expanded))

        if resolved == sensitive_resolved or resolved.startswith(sensitive_resolved + os.sep):
            return SafetyVerdict(
                needs_approval=True,
                reason=f"Write to sensitive path: {path}",
                tool_name="write_file",
                details={"path": path, "matched_sensitive": sensitive},
            )

        # Component matching: handles cases where the input path is relative (e.g.
        # .ssh/id_rsa) but the resolved absolute path doesn't match because the
        # working_dir differs from the user's home directory. Strip ~/  prefix from
        # sensitive patterns so "~/.ssh" matches ".ssh" in any path context.
        sensitive_stripped = sensitive.lstrip("~").lstrip("/").lstrip("\\")
        sensitive_normalized = os.path.normpath(sensitive_stripped).replace("\\", "/")
        sensitive_parts = sensitive_normalized.split("/")
        for i in range(len(path_parts)):
            segment = path_parts[i : i + len(sensitive_parts)]
            if segment == sensitive_parts:
                return SafetyVerdict(
                    needs_approval=True,
                    reason=f"Write to sensitive path: {path}",
                    tool_name="write_file",
                    details={"path": path, "matched_sensitive": sensitive},
                )

    return SafetyVerdict(needs_approval=False, reason="", tool_name="write_file")
