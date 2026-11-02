"""parse free-form flag values: key=value pairs, JSON, literal/@file/stdin text, and say when a removed notes flag was dropped."""

from __future__ import annotations
import json
import sys
from pathlib import Path
from typing import Any

import typer
from ...sdk.reads.notes_cap import FILE_NOTES_REMOVED


# -- helpers ----------------------------------------------------------------
def _kv_pairs(items: list[str] | None, *, cast_float: bool = False) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for item in items or []:
        if "=" not in item:
            raise typer.BadParameter(f"expected key=value, got: {item!r}")
        key, _, raw = item.partition("=")
        if cast_float:
            try:
                out[key] = float(raw)
            except ValueError as exc:
                raise typer.BadParameter(f"metric {key!r} must be numeric, got {raw!r}") from exc
        else:
            try:
                out[key] = json.loads(raw)
            except json.JSONDecodeError:
                out[key] = raw
    return out


def _json_value(raw: str | None) -> dict | None:
    if raw is None:
        return None
    if raw.startswith("@"):
        from pathlib import Path

        raw = Path(raw[1:]).read_text()
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise typer.BadParameter("expected a JSON object")
    return value


def _text_value(raw: str | None) -> str | None:
    """Free text for a `--notes` flag: literal, `@file`, or `-` for stdin.

    A caveat is prose, and prose arrives from a heredoc or a file at least as
    often as from a quoted argument -- `notes write` already reads both, and a
    run's note is the same kind of text. Passing `""` is preserved, not treated
    as absent: that is how the SDK clears a note.
    """
    if raw is None:
        return None
    if raw == "-":
        return sys.stdin.read()
    if raw.startswith("@"):
        return Path(raw[1:]).read_text()
    return raw


def _warn_notes_ignored(what: str, removed: str) -> None:
    """One stderr line saying a removed notes field was dropped, not sent.

    The write itself goes ahead: a script or an agent on an older skill that
    still passes it must not lose its upload or its group over a field the
    server no longer keeps. The value is never read (no `@file`, no stdin)."""
    print(f"warning: {what} is ignored: {removed}", file=sys.stderr)


def _warn_file_notes_ignored(what: str) -> None:
    _warn_notes_ignored(what, FILE_NOTES_REMOVED)
