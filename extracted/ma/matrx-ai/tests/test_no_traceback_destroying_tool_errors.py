"""A tool must NEVER stringify a caught exception into a ToolError and throw
the traceback away.

THE BUG THIS EXISTS TO PREVENT (2026-07-13, real, cost hours):

    except Exception as exc:
        return ToolResult(success=False, error=ToolError(
            error_type="search_failed",
            message=f"RAG search failed: {exc}",     # <-- stack destroyed here
        ))

Every `rag_search` call was failing with

    RAG search failed: invalid input for query argument $5: 0 (expected str, got int)

and the server log showed NOTHING — no file, no line, no stack, nowhere. The
exception was caught and flattened to a string before anything could record it,
so the two durable sinks (.matrx-debug/ and chat.tool_trace) faithfully stored a
one-line message about a bug they could not locate. The actual defect was in
matrx-orm's Case/When (an anchorless CASE param that Postgres silently types as
`text`), and finding it required reproducing the call by hand.

THE RULE: in an `except` block, build the ToolError with
``ToolError.from_exception(exc, error_type=..., message=...)``. It keeps every
kwarg you already pass and additionally captures ``exc.__traceback__``. Or just
let the exception propagate — ``ToolExecutor.execute`` catches it and records the
traceback for you. Either is correct. Stringifying is not.

(Layer 2 of the defense is in ToolExecutor: a FAIL result now SCREAMS to the
console, and says so explicitly when the traceback is missing. This test is
layer 1 — it stops the antipattern from being written at all.)
"""
from __future__ import annotations

import pathlib
import re

IMPLEMENTATIONS = pathlib.Path(__file__).resolve().parents[1] / "matrx_ai" / "tools" / "implementations"

_EXCEPT_RE = re.compile(r"except\s+\w*(?:Exception|Error)\w*\s+as\s+(\w+)\s*:")

# How many lines after the `except` line to consider part of the handler.
_BLOCK_LINES = 16


def _offending_sites() -> list[str]:
    sites: list[str] = []
    for path in sorted(IMPLEMENTATIONS.rglob("*.py")):
        lines = path.read_text().splitlines()
        for i, line in enumerate(lines):
            m = _EXCEPT_RE.search(line)
            if not m:
                continue
            var = m.group(1)
            block = "\n".join(lines[i : i + _BLOCK_LINES])

            # Does this handler interpolate the exception into an error message?
            if not re.search(rf'message=f"[^"]*\{{{var}\}}', block):
                continue
            # ...and does it preserve the stack by any sanctioned route?
            preserved = (
                "from_exception" in block
                or "traceback=" in block
                or f"exc={var}" in block  # threaded into a local _fail(...) helper
            )
            if not preserved:
                sites.append(f"{path.relative_to(IMPLEMENTATIONS)}:{i + 1}")
    return sites


def test_no_tool_stringifies_an_exception_and_destroys_the_traceback():
    offenders = _offending_sites()
    assert not offenders, (
        "These tool error handlers interpolate a caught exception into a ToolError "
        "message but never preserve its traceback — the stack is destroyed before "
        "any sink can record it, which is exactly how the 2026-07-13 rag_search "
        "outage stayed invisible:\n\n"
        + "\n".join(f"  - {s}" for s in offenders)
        + "\n\nFix: use ToolError.from_exception(exc, error_type=..., message=...) "
        "(it takes the same kwargs and captures exc.__traceback__), or let the "
        "exception propagate to ToolExecutor, which records the traceback for you."
    )
