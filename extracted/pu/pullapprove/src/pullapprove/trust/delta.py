"""The shared engine for token-delta trust rules (`_style`, `_spacing`,
`_type_annotations`).

The rules answer the same question — "do these paired lines differ *only* in a
way I recognize as trivial?" — and must apply the same default-deny gates to
answer it safely: equal add/remove counts, no indentation change (semantic in
Python), and a clean tokenization of both sides. If any gate is centralized
inconsistently, a rule can start hiding real changes. So the gates live here,
once, and each rule supplies only its distinct comparison of one line pair.
"""

from __future__ import annotations

from collections.abc import Callable

from ..diff import DiffCode, DiffHunk
from .helpers import leading_indent
from .tokens import Token, tokenize

# Compare one paired (old, new) line: True if it differs ONLY in this rule's
# trivial way, False if the rule sees no difference, None to decline (a
# non-trivial change — default-deny). Receives the raw pair alongside its tokens
# because some rules also need the source text (`_spacing`'s gap/tail checks).
ComparePair = Callable[[DiffCode, DiffCode, list[Token], list[Token]], bool | None]


def paired_changed_lines(hunk: DiffHunk) -> list[tuple[DiffCode, DiffCode]] | None:
    """The hunk's changed lines as POSITIONALLY aligned (old, new) pairs, or None
    when they don't align.

    Pairing is per replacement block: each contiguous run of changes must be
    deletions immediately followed by an equal number of additions, and the
    pairs are taken within that block. Counting alone isn't enough — a line
    moved across an intervening context line (a lone `-` here, its `+` after
    the context) changes execution order, so blocks that don't pair up decline
    rather than letting a positional shuffle read as a trivial delta.

    Cached on the hunk: four rules (`_style`, `_spacing`,
    `_inline_comment_change`, `_type_annotations`) each pair the same lines as
    the rule chain walks — the same reasoning as DiffHunk's cached
    `changed_lines`/`added_lines`. The cache returns the SAME list to every
    caller — treat it as read-only.
    """
    try:
        return hunk._paired_changed_lines  # ty: ignore[unresolved-attribute]
    except AttributeError:
        pairs = _pair_changed_lines(hunk)
        hunk._paired_changed_lines = pairs  # ty: ignore[unresolved-attribute]
        return pairs


def _pair_changed_lines(hunk: DiffHunk) -> list[tuple[DiffCode, DiffCode]] | None:
    pairs: list[tuple[DiffCode, DiffCode]] = []
    lines = hunk.lines
    i = 0
    while i < len(lines):
        if lines[i].is_context():
            i += 1
            continue
        deletions: list[DiffCode] = []
        while i < len(lines) and lines[i].is_deletion():
            deletions.append(lines[i])
            i += 1
        additions: list[DiffCode] = []
        while i < len(lines) and lines[i].is_addition():
            additions.append(lines[i])
            i += 1
        if not deletions or len(deletions) != len(additions):
            return None  # an unpaired block — an insertion, removal, or move
        pairs.extend(zip(deletions, additions))
    return pairs or None


def _non_token_text(stripped: str, tokens: list[Token]) -> str:
    """The line's non-token text — the comments the tokenizer silently drops —
    with all whitespace removed.

    The tokenizer skips line and block comments, so two lines that differ ONLY
    in a comment tokenize identically. Without this, a tool directive hidden in
    a comment (`# noqa`, `# type: ignore[…]`, `/* eslint-disable no-eval */`,
    `/* webpackChunkName */`) could ride along invisibly behind a trivial token
    delta (a quote swap, an annotation edit) and be hidden from review. A
    comment change belongs to `_comments` (which declines tool directives), so
    the token-delta rules must decline when this text changes. Whitespace is
    stripped so `_spacing`'s legitimate whitespace moves don't register."""
    parts: list[str] = []
    pos = 0
    for tok in tokens:
        parts.append(stripped[pos : tok.start])
        pos = tok.end
    parts.append(stripped[pos:])
    return "".join("".join(parts).split())


def paired_token_delta(
    pairs: list[tuple[DiffCode, DiffCode]], ext: str, compare: ComparePair
) -> bool:
    """True if the paired lines earn this rule's label: every pair differs only
    in trivial tokens, with at least one that does.

    Applies the gates every token-delta rule shares — no indentation change
    (semantic in Python), a clean tokenization of both sides, and no change to
    the comments the tokenizer drops — and returns False the moment any gate
    fails or `compare` rejects a pair, so an unrecognized change is never
    trusted. `pairs` comes from `paired_changed_lines`, which enforces the
    positional-alignment gate.
    """
    any_changed = False
    for old, new in pairs:
        if leading_indent(old.content) != leading_indent(new.content):
            return False  # indentation is semantic (Python) — a real change
        old_stripped, new_stripped = old.content.strip(), new.content.strip()
        old_tokens = tokenize(old_stripped, ext)
        new_tokens = tokenize(new_stripped, ext)
        if old_tokens is None or new_tokens is None:
            return False  # a multi-line fragment — can't judge in isolation
        if _non_token_text(old_stripped, old_tokens) != _non_token_text(
            new_stripped, new_tokens
        ):
            return False  # a dropped comment/directive changed — _comments' job
        verdict = compare(old, new, old_tokens, new_tokens)
        if verdict is None:
            return False  # a non-trivial token changed — a real edit
        any_changed = any_changed or verdict
    return any_changed
