"""
A name the platform sent - a file of a listing, a member of a download - as a path under the folder it is written into,
never outside it.

In one sentence: the name's parts, split at "/" and at "\\" (a separator to Windows) → refused when the name is empty or
absolute, or a part steps up (".."), names a drive ("C:") or holds a control character → else the folder joined with
them.

WHY on the user's machine as well as on the platform: the platform refuses such names where they enter it
, and what a download names is written on the user's machine, which must not need that
to hold. Before, `seq volume get` and `seq policy data export` joined a listed "../x" or "/x" to the folder as it came,
and the export opened - so emptied - such a file before its download was refused.

"""
from __future__ import annotations

import pathlib
import re

_DRIVE = re.compile(r"[A-Za-z]:")
_CONTROL = re.compile(r"[\x00-\x1f\x7f]")


def parts_of(name: object) -> list[str] | None:
    """The parts of a relative name, or None for a name that would leave the folder it is written under."""
    if not isinstance(name, str) or not name or _CONTROL.search(name) or name[0] in "/\\":
        return None
    parts = [p for p in re.split(r"[/\\]", name) if p not in ("", ".")]
    if not parts or any(p == ".." or _DRIVE.match(p) for p in parts):
        return None
    return parts


def under(folder: str | pathlib.Path, name: object) -> pathlib.Path:
    """`name`, a relative path the platform sent, under `folder`; InvalidRequest for one that is not."""
    parts = parts_of(name)
    if parts is None:
        from sequence_ai.errors import InvalidRequest

        raise InvalidRequest(f"the platform named a file {str(name)[:200]!r}, which would be written outside {folder}: "
                             "nothing was written")
    return pathlib.Path(folder).joinpath(*parts)
