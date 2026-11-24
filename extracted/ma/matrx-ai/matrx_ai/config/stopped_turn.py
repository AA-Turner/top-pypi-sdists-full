"""A STOPPED REPLY THAT ENDS INSIDE AN OPEN REGION IS CLOSED ON THE WIRE (2026-11-14).

The person presses Stop while the reply is inside a ```python block. The saved reply ends mid-fence (plus the
stop marker the executor appends) and is kept exactly like that: it is what the person saw. When they say
"continue", the model is sent that turn as history; with the fence still open it carries on INSIDE the code,
never opens a fence of its own, and its later closing ``` is read by the one splitter as an opener, inverting
every fence after it.

So, on the WIRE copy only (``send_boundary._close_stopped_turns``, the only caller; the saved row never changes),
a stopped assistant turn whose text ends inside an open fenced block, display math, or raw svg / html root has
the region closed before the stop marker, and one host-written sentence tells the model the reply was cut there
and that it may restate the cut block in full. Pure text functions; no I/O.
"""

from __future__ import annotations

import re

from matrx_ai.processing.blocks.fence_nesting import (
    classify_inner_fence_line,
    fence_nests_inner_fences,
    parse_fence_opener,
    trim_fence_line,
)

#: The words the executor appends to a stopped partial (``orchestrator/executor.py`` ``_STOP_MARKERS``).
STOP_MARKER_RE = re.compile(r"\n*\[⚠️ Response (?:stopped|interrupted)[^\]\n]*before completion\.\]\s*$")

STOPPED_IN_REGION_NOTE = (
    "\n\n[Note from the system: that reply was stopped partway through {what}, which was closed above only so "
    "it reads cleanly. When you continue, begin cleanly: do not carry on inside it as if still open; if you "
    "need the cut part, restate it in full, opening its own {opener}.]"
)

_CLOSERS = {"$$": "$$", "\\[": "\\]", "<svg": "</svg>", "<html": "</html>", "<!doctype html": "</html>"}


def _open_fence(text: str) -> tuple[int, str | None] | None:
    """``(ticks, language)`` of the fence still open at the end of ``text``, or None."""
    open_state: tuple[int, str | None, bool, int] | None = None  # ticks, lang, nests, depth
    for line in text.split("\n"):
        if open_state is None:
            opened = parse_fence_opener(line)
            if opened is not None and not line.lstrip(" ").startswith("    "):
                ticks, lang = opened
                open_state = (ticks, lang or None, fence_nests_inner_fences(lang), 0)
            continue
        ticks, lang, nests, depth = open_state
        kind = classify_inner_fence_line(trim_fence_line(line), ticks, nests, depth)
        if kind == "close-outer":
            open_state = None
        elif kind == "close-nested":
            open_state = (ticks, lang, nests, depth - 1)
        elif kind == "open-nested":
            open_state = (ticks, lang, nests, depth + 1)
    return None if open_state is None else (open_state[0], open_state[1])


def _open_extra(text: str) -> str | None:
    """The closing delimiter of a display-math / svg / html root still open at the end of ``text``, or None."""
    from matrx_ai.processing.blocks.markdown_regions import _MD, blocked_lines, maybe_extras, merge_regions

    raw = text.encode("utf-8")
    if not maybe_extras(raw):
        return None
    tokens = _MD.parse(text)
    md = [
        ("code" if t.type == "fence" else "table", t.map[0], t.map[1], None)
        for t in tokens
        if t.map is not None and t.type in ("fence", "table_open")
    ]
    lines = raw.splitlines(True)
    for kind, first, _end, _lang, closed in reversed(merge_regions(lines, md, blocked_lines(tokens, lines))):
        if kind in ("math", "svg", "html") and not closed:
            head = lines[first].decode("utf-8", "replace").lstrip().lower()
            for opener, closer in _CLOSERS.items():
                if opener in head:
                    return closer
        break
    return None


def close_stopped_text(text: str) -> str | None:
    """``text`` of a STOPPED reply with its open region closed and the note added, or None when nothing is open.

    The stop marker (when the text carries one) stays last of the original words; the closer goes before it.
    """
    marker = STOP_MARKER_RE.search(text)
    body, tail = (text[: marker.start()], text[marker.start() :]) if marker else (text, "")
    fence = _open_fence(body)
    if fence is not None:
        ticks, lang = fence
        closer = "\n" + "`" * ticks
        what = f"a {lang} code block" if lang else "a code block"
        opener = "`" * ticks + (lang or "")
        return body.rstrip("\n") + closer + tail + STOPPED_IN_REGION_NOTE.format(what=what, opener=f"fence ({opener})")
    extra = _open_extra(body)
    if extra is not None:
        return (
            body.rstrip("\n")
            + ("\n" if extra == "$$" or extra == "\\]" else "")
            + extra
            + tail
            + STOPPED_IN_REGION_NOTE.format(what="an open block", opener="delimiters")
        )
    return None


def is_stopped_turn(message: object) -> bool:
    """A stopped partial: ``metadata.stopped`` on the row, or the executor's stop marker ending its last text."""
    metadata = getattr(message, "metadata", None)
    return isinstance(metadata, dict) and bool(metadata.get("stopped"))


__all__ = ["STOPPED_IN_REGION_NOTE", "STOP_MARKER_RE", "close_stopped_text", "is_stopped_turn"]
