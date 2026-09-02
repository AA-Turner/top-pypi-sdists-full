import json
import sys
from pathlib import Path
from typing import Any

from .script_generators.atomic_write import atomic_write

_PLUGIN_NAME = "agentic-devtools"

# Plugin identifier in the "plugin-name@marketplace-name" format required by the
# GitHub Copilot repository-settings schema for enabledPlugins.
_PLUGIN_KEY = f"{_PLUGIN_NAME}@agentic-devtools"

# Marketplace name and its source descriptor as required by the GitHub Copilot
# repository-settings schema for extraKnownMarketplaces.
_MARKETPLACE_NAME = "agentic-devtools"
_MARKETPLACE_SOURCE = {"source": "github", "repo": "swai-factory/agentic-devtools-plugin"}


def _reject_non_finite_json_constants(raw_constant: str) -> Any:
    raise ValueError(f"non-finite JSON constant is not supported: {raw_constant}")


_STRICT_JSON_DECODER = json.JSONDecoder(parse_constant=_reject_non_finite_json_constants)


def _json_values_match(existing: Any, expected: Any) -> bool:
    if type(existing) is not type(expected):
        return False
    if isinstance(existing, dict):
        if existing.keys() != expected.keys():
            return False
        return all(_json_values_match(existing[key], expected[key]) for key in existing)
    if isinstance(existing, list):
        if len(existing) != len(expected):
            return False
        return all(
            _json_values_match(existing_item, expected_item) for existing_item, expected_item in zip(existing, expected)
        )
    return existing == expected


def _skip_whitespace(content: str, index: int) -> int:
    while index < len(content) and content[index] in " \t\r\n":
        index += 1
    return index


def _line_indent(content: str, index: int) -> str:
    line_start = content.rfind("\n", 0, index) + 1
    indent = content[line_start:index]
    return indent if not indent.strip() else ""


def _render_value(value: Any, member_indent: str, newline: str) -> str:
    rendered = json.dumps(value, indent=4)
    lines = rendered.splitlines()
    if len(lines) == 1:
        return rendered
    return lines[0] + "".join(f"{newline}{member_indent}{line}" for line in lines[1:])


def _parse_top_level_members(content: str) -> tuple[dict[str, tuple[Any, int, int, int]], int]:
    index = _skip_whitespace(content, 0)
    if index >= len(content) or content[index] != "{":
        raise ValueError("settings.json is not a JSON object")

    index += 1
    members: dict[str, tuple[Any, int, int, int]] = {}

    while True:
        index = _skip_whitespace(content, index)
        if index >= len(content):
            raise ValueError("unterminated JSON object")
        if content[index] == "}":
            return members, index

        key_start = index
        key, key_end = _STRICT_JSON_DECODER.raw_decode(content, index)
        if not isinstance(key, str):
            raise ValueError("top-level key is not a string")

        index = _skip_whitespace(content, key_end)
        if index >= len(content) or content[index] != ":":
            raise ValueError("malformed JSON object entry")

        index += 1
        value_start = _skip_whitespace(content, index)
        value, value_end = _STRICT_JSON_DECODER.raw_decode(content, value_start)
        members[key] = (value, key_start, value_start, value_end)

        index = _skip_whitespace(content, value_end)
        if index < len(content) and content[index] == ",":
            index = _skip_whitespace(content, index + 1)
            if index >= len(content) or content[index] != '"':
                raise ValueError("malformed JSON object terminator")
            continue
        if index < len(content) and content[index] == "}":
            return members, index
        raise ValueError("malformed JSON object terminator")


def _merge_expected_entries(
    existing_json_object: str, expected_entries: dict[str, Any], newline: str
) -> tuple[str, bool]:
    members, _ = _parse_top_level_members(existing_json_object)
    updated_content = existing_json_object
    replacements: list[tuple[int, int, str]] = []
    changed = False

    for entry_key, entry_val in expected_entries.items():
        member = members.get(entry_key)
        if member is None:
            continue

        existing_value, key_start, value_start, value_end = member
        if _json_values_match(existing_value, entry_val):
            continue

        entry_indent = _line_indent(existing_json_object, key_start) or "    "
        replacements.append((value_start, value_end, _render_value(entry_val, entry_indent, newline)))
        changed = True

    for value_start, value_end, replacement in sorted(replacements, reverse=True):
        updated_content = updated_content[:value_start] + replacement + updated_content[value_end:]

    updated_members, closing_brace = _parse_top_level_members(updated_content)
    object_indent = "    "
    if updated_members:
        first_member = min(updated_members.values(), key=lambda member: member[1])
        object_indent = _line_indent(updated_content, first_member[1]) or "    "

    missing_entries = [
        f"{object_indent}{json.dumps(entry_key)}: {_render_value(entry_val, object_indent, newline)}"
        for entry_key, entry_val in expected_entries.items()
        if entry_key not in updated_members
    ]
    if missing_entries:
        insertion = (
            "".join(f",{newline}{pair}" for pair in missing_entries)
            if updated_members
            else newline + f",{newline}".join(missing_entries) + newline
        )
        updated_content = updated_content[:closing_brace] + insertion + updated_content[closing_brace:]
        changed = True

    return updated_content, changed


def ensure_copilot_settings(git_root: Path) -> bool:
    """Ensure .github/copilot/settings.json exists and has the plugin settings.

    Creates the file when absent, merges when present.
    Only touches the two plugin-related top-level keys; every other top-level
    key is preserved byte-for-byte.
    Returns True if the file was modified or created, False if no changes were needed.
    """
    copilot_dir = git_root / ".github" / "copilot"
    settings_file = copilot_dir / "settings.json"

    plugin_settings: dict[str, Any] = {
        "enabledPlugins": {_PLUGIN_KEY: True},
        "extraKnownMarketplaces": {_MARKETPLACE_NAME: {"source": _MARKETPLACE_SOURCE}},
    }

    if not settings_file.exists():
        try:
            atomic_write(settings_file, json.dumps(plugin_settings, indent=4) + "\n")
            return True
        except OSError as exc:
            print(f"  ⚠ Failed to create {settings_file.relative_to(git_root)} — {exc}", file=sys.stderr)
            return False

    # File exists, merge it.
    try:
        content = settings_file.read_bytes().decode("utf-8")
        if not content.strip():
            data: dict[str, Any] = {}
            content = "{}"
        else:
            data = json.loads(content, parse_constant=_reject_non_finite_json_constants)

        if not isinstance(data, dict):
            print(f"  ⚠ {settings_file.relative_to(git_root)} is not a JSON object, skipping merge.", file=sys.stderr)
            return False
    except Exception as exc:
        print(f"  ⚠ Failed to read {settings_file.relative_to(git_root)} — {exc}", file=sys.stderr)
        return False

    try:
        members, _ = _parse_top_level_members(content)
    except ValueError as exc:
        print(f"  ⚠ Failed to parse {settings_file.relative_to(git_root)} for merge — {exc}", file=sys.stderr)
        return False

    newline = "\r\n" if "\r\n" in content else "\n"
    changed = False
    replacements: list[tuple[int, int, str]] = []
    for k, v in plugin_settings.items():
        member = members.get(k)
        if member is None:
            changed = True
            continue

        existing, key_start, value_start, value_end = member
        if isinstance(existing, dict):
            merged, member_changed = _merge_expected_entries(content[value_start:value_end], v, newline)
            if member_changed:
                replacements.append((value_start, value_end, merged))
                changed = True
        else:
            indent = _line_indent(content, key_start) or "    "
            replacements.append((value_start, value_end, _render_value(v, indent, newline)))
            changed = True

    if not changed:
        return False

    updated_content = content
    for value_start, value_end, replacement in sorted(replacements, reverse=True):
        updated_content = updated_content[:value_start] + replacement + updated_content[value_end:]

    try:
        updated_members, closing_brace = _parse_top_level_members(updated_content)
    except ValueError as exc:
        print(f"  ⚠ Failed to parse {settings_file.relative_to(git_root)} after merge — {exc}", file=sys.stderr)
        return False

    top_level_indent = "    "
    if updated_members:
        first_member = min(updated_members.values(), key=lambda member: member[1])
        top_level_indent = _line_indent(updated_content, first_member[1]) or "    "

    missing_pairs = [
        f"{top_level_indent}{json.dumps(key)}: {_render_value(value, top_level_indent, newline)}"
        for key, value in plugin_settings.items()
        if key not in updated_members
    ]
    if missing_pairs:
        if updated_members:
            insertion = "".join(f",{newline}{pair}" for pair in missing_pairs)
        else:
            insertion = newline + f",{newline}".join(missing_pairs) + newline
        updated_content = updated_content[:closing_brace] + insertion + updated_content[closing_brace:]

    try:
        atomic_write(settings_file, updated_content)
        return True
    except OSError as exc:
        print(f"  ⚠ Failed to write {settings_file.relative_to(git_root)} — {exc}", file=sys.stderr)
        return False
