"""The file-level pure-rename rule.

A pure rename — git found byte-identical content at a new path — produces no
hunks, only header metadata, so it never reaches the per-hunk rules. This rule
classifies the file itself, from its header lines alone.

Default-deny like every hunk rule: the ONLY recognized shape is the exact
three metadata lines git emits for a same-content, same-mode rename. A rename
that also changes mode (`old mode`/`new mode` lines), a binary rename with
changes (`index` + `Binary files` lines), a copy (`copy from`/`copy to`), or
anything else adds or substitutes lines and is declined — those changes are
real and must be shown.
"""

from __future__ import annotations

from ..diff import DiffFile
from .labels import Trust


def trust_file_label(file: DiffFile) -> Trust | None:
    """Return the trust label for a hunkless file, or None when nothing matches."""
    if file.hunks:
        return None
    if not file.is_move():
        return None
    # After the `diff --git` line: exactly the pure-rename metadata, nothing
    # else. The paths themselves were already read from the `diff --git` line
    # (is_move above); prefix checks avoid re-parsing the C-quoted forms.
    meta = file.header_lines[1:]
    if len(meta) != 3:
        return None
    if meta[0] != "similarity index 100%":
        return None
    if not meta[1].startswith("rename from "):
        return None
    if not meta[2].startswith("rename to "):
        return None
    return Trust.FILE_RENAMED
