"""
Environment variable substitution for runlayer.yaml files.

Supports standard Docker Compose / shell-style variable syntax:
- ${VAR} - Required variable (error if not set)
- ${VAR:-default} - Use default if unset or empty
- ${VAR-default} - Use default only if unset (not if empty)
- $$VAR - Preserved as-is for backend processing

References inside `#` comments are left alone: comments are located with the
YAML scanner and passed through verbatim, so a literal `${VAR}` in a comment
does not count as a required variable and the document is never reformatted.
"""

import os
from pathlib import Path
from typing import Dict

import yaml
from dotenv import dotenv_values

from runlayer_cli import regex_safe


def load_env_vars(
    env_file_path: str | None = None, search_dir: Path | None = None
) -> Dict[str, str]:
    """
    Load environment variables from os.environ and optionally from a .env file.

    If env_file_path is provided, load variables from that file.
    Otherwise, automatically look for .env file in search_dir (or current directory).
    Variables from .env file override os.environ values.

    Args:
        env_file_path: Optional explicit path to .env file (overrides auto-discovery)
        search_dir: Optional directory to search for .env file (defaults to current directory)

    Returns:
        Dictionary of environment variable name -> value

    Raises:
        FileNotFoundError: If env_file_path is provided but file doesn't exist
    """
    # Start with current environment variables
    env_vars = dict(os.environ)

    # Determine which .env file to load
    env_path = None

    if env_file_path:
        # Explicit path provided
        env_path = Path(env_file_path)
        if not env_path.exists():
            raise FileNotFoundError(f"Environment file not found: {env_file_path}")
    else:
        # Auto-discover .env file
        search_directory = search_dir if search_dir else Path.cwd()
        potential_env_file = search_directory / ".env"
        if potential_env_file.exists():
            env_path = potential_env_file

    # Load .env file if found (overrides os.environ)
    if env_path:
        # Load .env file into a dict (doesn't modify os.environ)
        dotenv_vars = dotenv_values(env_path, encoding="utf-8-sig")

        # Merge dotenv_vars into env_vars (dotenv file overrides os.environ)
        # Filter out None values (unset variables in .env file)
        env_vars.update({k: v for k, v in dotenv_vars.items() if v is not None})

    return env_vars


def _append_hash_spans(spans: list[tuple[int, int]], text: str, offset: int) -> None:
    """Record `#`-to-end-of-line spans in text that can hold only whitespace and comments."""
    for line in text.splitlines(keepends=True):
        hash_at = line.find("#")
        if hash_at != -1:
            spans.append((offset + hash_at, offset + len(line)))
        offset += len(line)


def _comment_spans(yaml_content: str) -> list[tuple[int, int]]:
    """Absolute (start, end) of every `#` comment, in document order."""
    spans: list[tuple[int, int]] = []
    pos = 0
    for token in yaml.scan(yaml_content):
        start = token.start_mark.index
        # Between tokens the scanner skips only whitespace and comments.
        _append_hash_spans(spans, yaml_content[pos:start], pos)
        if isinstance(token, yaml.ScalarToken) and token.style in ("|", ">"):
            # A block scalar's header line (indicators + optional comment) is
            # folded into the token, so its comment is not in any gap.
            header = yaml_content[start : token.end_mark.index].splitlines(
                keepends=True
            )[:1]
            _append_hash_spans(spans, "".join(header), start)
        pos = max(pos, token.end_mark.index)
    return spans


def substitute_env_vars(yaml_content: str, env_vars: Dict[str, str]) -> str:
    """
    Replace environment variable references in YAML content.

    Supports:
    - ${VAR} - Required variable (error if not set)
    - ${VAR:-default} - Use default if unset or empty
    - ${VAR-default} - Use default only if unset (not if empty)
    - $$VAR - Preserved as-is (double dollar sign)

    Args:
        yaml_content: Raw YAML content as string
        env_vars: Dictionary of environment variable name -> value

    Returns:
        YAML content with variables substituted

    Raises:
        ValueError: If a required variable (${VAR}) is not found
    """
    # Pattern to match ${VAR:-default} or ${VAR-default} or ${VAR}
    # This regex captures:
    # - Group 1: Variable name
    # - Group 2: Default value operator (:- or -) or empty
    # - Group 3: Default value (if present)
    # We use a non-capturing group to match the optional colon before dash
    pattern = r"\$\{([A-Z_][A-Z0-9_]*)(?:(:-)|(-))?([^}]*)\}"

    def replace_var(match: regex_safe.Match) -> str:
        var_name = match.group(1)
        # Group 2 is ':-' if present, Group 3 is '-' if present, or None
        default_op_colon = match.group(2)  # ':-' or None
        default_op_dash = match.group(3)  # '-' or None
        default_value = match.group(4) if match.group(4) else ""

        # Determine the operator type
        if default_op_colon:
            default_op = ":-"
        elif default_op_dash:
            default_op = "-"
        else:
            default_op = ""

        # Check if variable exists in env_vars
        var_value = env_vars.get(var_name)

        # Handle different cases
        if var_value is not None:
            # Variable exists
            if default_op == ":-":
                # ${VAR:-default} - use default if empty
                return var_value if var_value else default_value
            elif default_op == "-":
                # ${VAR-default} - use default only if unset (not if empty)
                return var_value  # Variable exists, use it even if empty
            else:
                # ${VAR} - required, use value
                return var_value
        else:
            # Variable doesn't exist
            if default_op:
                # Has default, use it
                return default_value
            else:
                # No default, required variable missing
                raise ValueError(
                    f"Required environment variable '{var_name}' is not set. "
                    f"Set it in your environment or use --env-file to load from a file."
                )

    def substitute(text: str) -> str:
        return regex_safe.sub(pattern, replace_var, text)

    # Skip `#` comments. The scanner only skips whitespace and comments
    # between tokens, so any `#` in an inter-token gap starts a comment;
    # `#` inside tokens (quoted strings, URLs) is content. Everything but
    # the comment spans is substituted as before, comments pass verbatim.
    try:
        comment_spans = _comment_spans(yaml_content)
    except yaml.YAMLError:
        return substitute(yaml_content)

    parts = []
    pos = 0
    for start, end in comment_spans:
        parts.append(substitute(yaml_content[pos:start]))
        parts.append(yaml_content[start:end])
        pos = end
    parts.append(substitute(yaml_content[pos:]))
    result = "".join(parts)

    # Note: We don't need to handle $$VAR separately because:
    # - $$VAR becomes $VAR in the string (single $)
    # - Our regex only matches ${...} patterns, not $VAR
    # - If someone writes $${VAR}, it becomes ${VAR} which we handle
    # - If someone writes $$VAR (no braces), it stays as $$VAR

    return result
