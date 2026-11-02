"""Static, conservative classification of diff hunks by *trust*.

A hunk is "trusted" when its change is mechanically trivial — lockfile churn,
whitespace, comments, imports, type annotations — so it can be filtered out
during review. `trust_diff` tags every hunk with a `Trust` label (e.g.
`Trust.LOCKFILE`) or `None`. `Trust` is the closed vocabulary of labels; see
`labels.py`.

Every rule is **default-deny**: it recognizes one specific trivial shape and
returns nothing for everything else, so an unrecognized change is shown, never
hidden — a wrong label would hide a real change. The rules recognize their shape
through a few mechanisms: filename (`_lockfile`), all-blank lines (`_empty_file`,
`_whitespace`), a same-content newline reflow (`_line_length`), a same-statement
import set (`_imports`), a comment-only scan (`_comments`), a token-identical
respacing (`_spacing`), and a token-level delta where every changed token is
trivial (`_style`, `_type_annotations`) — those last three share `delta.py`'s
paired-line gates. Classification is a separate pass from parsing — it never
runs on the `match_diff` hot path.

Each rule lives in its own module beside the syntax tables it needs and is a
pure `(file, hunk) -> Trust | None`; this package wires them into `_RULES`. Add a
rule by writing one and appending it here. One rule classifies whole FILES
instead of hunks: `trust_file_label` (renames.py) labels a hunkless pure rename
from its header lines — hunkless files never reach the per-hunk rules at all.

Ported from the `review` project's static classifier (full parity except
`move:code`, which needs cross-file hunk pairing we don't model).
"""

from __future__ import annotations

from collections.abc import Callable, Iterator

from ..diff import DiffFile, DiffHunk, parse_diff
from .annotations import _type_annotations
from .comments import _comments
from .formatting import _empty_file, _line_length, _spacing, _style, _whitespace
from .imports import _imports
from .labels import TRUST_FAMILIES, Trust
from .lockfiles import _lockfile
from .renames import trust_file_label

__all__ = [
    "TRUST_FAMILIES",
    "Trust",
    "trust_diff",
    "trust_file_label",
    "trust_label",
]

# Order matters: cheapest / most-specific first, first match wins. Default-deny
# keeps the rules from fighting — each declines anything outside its shape — but
# ordering still resolves the few honest overlaps: `_whitespace` precedes
# `_line_length`/`_style` (a blank-only change is not a wrap or a quote swap), and
# `_style`/`_spacing` precede `_comments` (a line whose code differs only in a
# quote and whose comment also changed reads as style; a comment-only change
# token-matches under both, declines, and falls through here). `_style` and
# `_spacing` are disjoint — style needs token texts to differ, spacing needs them
# equal — so their relative order is free. Revisit when adding a rule whose shape
# can co-occur with another's.
_RULES: tuple[Callable[[DiffFile, DiffHunk], Trust | None], ...] = (
    _lockfile,
    _empty_file,
    _whitespace,
    _line_length,
    _style,
    _spacing,
    _comments,
    _type_annotations,
    _imports,
)


def trust_label(file: DiffFile, hunk: DiffHunk) -> Trust | None:
    """Return the conservative trust label for a hunk, or None when nothing matches."""
    for rule in _RULES:
        label = rule(file, hunk)
        if label:
            return label
    return None


def trust_diff(diff: Iterator[str] | str) -> list[DiffFile]:
    """Parse a diff and tag every hunk with its trust label.

    Holds the whole parsed `DiffFile` tree — right for a hunk listing (the
    CLI's `trust` command). When only the per-hunk labels are needed, compose
    `iter_file_hunks` with `trust_label` instead: it classifies each hunk the
    moment the diff finishes streaming it, holding one hunk at a time. Every
    rule classifies a hunk from its own lines and the file path alone (never
    sibling hunks), so the per-hunk result is identical either way.
    """
    files = parse_diff(diff)
    for file in files:
        for hunk in file.hunks:
            hunk.trust = trust_label(file, hunk)
    return files
