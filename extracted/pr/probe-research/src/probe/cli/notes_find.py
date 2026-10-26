"""`probe notes find`: the paragraphs of a note that mention some words.

An agent about to change one fact in a long note needs the paragraph that holds
it, word for word, not the whole note: reading a whole 22K-84K-character note
before every edit was most of what one team's daemon helpers did (daemon cost
round 7, 2026-10-25). Each match is printed verbatim under its section heading
with its line numbers, so it can be quoted as the `old` text of an edit.

Pure text in, text out: the command (`main.notes_find`) fetches the current
version and prints what `report` returns.
"""

from __future__ import annotations

from dataclasses import dataclass

#: At most this many matching paragraphs, and this many characters of them, are
#: printed; the rest are counted.
MAX_PARAGRAPHS = 8
MAX_CHARS = 8_000


@dataclass(frozen=True)
class Paragraph:
    """One block of a note between blank lines (a heading is its own block)."""

    heading: str
    first_line: int
    last_line: int
    text: str


def paragraphs(text: str) -> list[Paragraph]:
    """`text`'s blocks, in order, each with the nearest heading above it (`#`
    lines; "" before the first) and its 1-based line range."""
    out: list[Paragraph] = []
    heading = ""
    block: list[str] = []
    start = 0

    def close(end: int) -> None:
        if block:
            out.append(Paragraph(heading=heading, first_line=start, last_line=end, text="\n".join(block)))
            block.clear()

    for number, line in enumerate(text.split("\n"), start=1):
        if not line.strip():
            close(number - 1)
            continue
        if line.lstrip().startswith("#"):
            close(number - 1)
            heading = line.strip().lstrip("#").strip()
            out.append(Paragraph(heading=heading, first_line=number, last_line=number, text=line))
            continue
        if not block:
            start = number
        block.append(line)
    close(len(text.split("\n")))
    return out


def matches(text: str, words: list[str]) -> tuple[list[Paragraph], int]:
    """The paragraphs of `text` that mention any of `words` (case-insensitive),
    those mentioning more of them first, then in note order; and how many
    paragraphs `text` has."""
    wanted = [w.lower() for w in words if w.strip()]
    found: list[tuple[int, int, Paragraph]] = []
    blocks = paragraphs(text)
    for index, block in enumerate(blocks):
        lowered = block.text.lower()
        hits = sum(1 for word in wanted if word in lowered)
        if hits:
            found.append((-hits, index, block))
    found.sort(key=lambda item: (item[0], item[1]))
    return [block for _, _, block in found], len(blocks)


def report(label: str, version: object, text: str, words: list[str]) -> str:
    """What `probe notes find` prints for `words` in `text`, the note `label` at
    `version`."""
    quoted = " ".join(f'"{w}"' for w in words)
    found, total = matches(text, words)
    head = f"{label} · v{version} · {len(text):,} characters"
    if not found:
        return f"{head} · no paragraph mentions {quoted}"
    lines = [f"{head} · {len(found)} of {total} paragraphs mention {quoted}"]
    shown = 0
    used = 0
    for block in found:
        if shown >= MAX_PARAGRAPHS or (shown and used + len(block.text) > MAX_CHARS):
            break
        where = f"lines {block.first_line}-{block.last_line}" if block.last_line > block.first_line \
            else f"line {block.first_line}"
        lines.append(f"\n[{block.heading or 'top'} · {where}]\n{block.text}")
        shown += 1
        used += len(block.text)
    if shown < len(found):
        lines.append(f"\n[... {len(found) - shown} more matching paragraphs: add words to narrow]")
    return "\n".join(lines)
