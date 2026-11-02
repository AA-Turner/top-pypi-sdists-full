"""The closed vocabulary of trust labels.

Every label is `family:specific`. Rules return a `Trust` member, which *is* a
string everywhere it's used — display, counting, comparison, `--hide` matching —
so callers can treat it as the `family:specific` token it spells, while the enum
gives one place to see every label and catches typos at the source.
"""

from __future__ import annotations

from enum import StrEnum


class Trust(StrEnum):
    LOCKFILE = "generated:lockfile"
    EMPTY_FILE = "file:added-empty"
    FILE_RENAMED = "file:renamed"
    WHITESPACE = "formatting:whitespace"
    LINE_LENGTH = "formatting:line-length"
    STYLE = "formatting:style"
    SPACING = "formatting:spacing"
    COMMENTS_ADDED = "comments:added"
    COMMENTS_REMOVED = "comments:removed"
    COMMENTS_MODIFIED = "comments:modified"
    IMPORTS_ADDED = "imports:added"
    IMPORTS_REMOVED = "imports:removed"
    IMPORTS_MODIFIED = "imports:modified"
    IMPORTS_REORDERED = "imports:reordered"
    TYPE_ANNOTATIONS_MODIFIED = "type-annotations:modified"

    @property
    def family(self) -> str:
        """The part before the colon, e.g. `formatting` for `formatting:style`."""
        return self.value.split(":", 1)[0]


# Every family a `--hide` filter can name.
TRUST_FAMILIES = frozenset(label.family for label in Trust)
