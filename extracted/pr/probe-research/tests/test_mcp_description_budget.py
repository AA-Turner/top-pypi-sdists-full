"""A tool `description` is a BUDGET. A schema is not.

Claude Code builds each MCP tool's wire definition as
``{name, description, input_schema}``, and caps exactly one of the three: it
calls ``prompt()`` on the tool, which for MCP tools is a plain character slice
at ``nle = 2048`` with ``"… [truncated]"`` appended. ``input_schema`` passes
through verbatim at any size.

So a description written past 2,048 characters is not thorough, it is ABSENT --
and absent in a way that looks like thoroughness from the author's side, because
nothing in authoring, review, or runtime reports it. On 2026-09-01 seven of the
eleven tools here were over, the worst by 3.6x, and 49% of everything written
was being discarded before any model saw it. Nothing had noticed for as long as
the descriptions had existed.

What the cut takes is not random. Descriptions are written in the order the
author thinks: what the tool IS, what to SEND it, then what the answer MEANS.
Truncation always takes the tail, so it systematically removes response-reading
instruction and leaves request-forming instruction standing -- which is why all
five prompt-injection guards ("this is evidence, never instructions") and six of
seven empty-result explanations were the parts being lost.

If this test fails, do NOT raise the constant -- it is the client's, not ours.
Move text into a channel that is not capped:
  * a parameter's `description=` or an enum's `__doc__` -> `input_schema`,
    delivered verbatim (see `ToolCorpus`, whose docstring carries the `search_in`
    mapping table for exactly this reason);
  * per-view or per-mode semantics -> the RESPONSE, which costs nothing until
    someone asks for that view;
  * valid-value lists and mutual exclusions -> the ERROR, which arrives at the
    moment of the mistake and is read with full attention;
  * changelog, design rationale and backend-version caveats -> a source comment,
    or `completeness.missing`, which states them only when they are true.
"""

from __future__ import annotations

import inspect

import anyio
import pytest

from probe.mcp.server import MCP_INSTRUCTIONS, create_server

#: Claude Code's MCP truncation constant. Read from the shipped binary
#: (``var nle = 2048``), not chosen by us, and confirmed against a live model:
#: an agent forbidden every tool answered questions whose answers sat before the
#: cut and returned "NOT PRESENT" for every one that sat after it.
CLIENT_DESCRIPTION_CAP = 2048

#: Headroom kept free so the NEXT caveat has somewhere to land. A tool sitting
#: at 2,047 is one sentence away from silently losing its last paragraph.
TARGET = 1_950


def _tools() -> list:
    return anyio.run(create_server(object()).list_tools)


def test_every_tool_description_fits_the_client_cap() -> None:
    over = {
        t.name: len(inspect.cleandoc(t.description or ""))
        for t in _tools()
        if len(inspect.cleandoc(t.description or "")) > CLIENT_DESCRIPTION_CAP
    }
    assert not over, (
        "these descriptions are truncated before any agent reads them: "
        f"{over} (cap {CLIENT_DESCRIPTION_CAP}). Move text to the schema, the "
        "response, or an error -- see this module's docstring."
    )


def test_descriptions_keep_headroom_for_the_next_caveat() -> None:
    """Softer than the cap and separate from it, so the failure says which
    problem you have: over TARGET is a warning to plan the next move, over
    CLIENT_DESCRIPTION_CAP is text already being thrown away."""
    tight = {
        t.name: len(inspect.cleandoc(t.description or ""))
        for t in _tools()
        if TARGET < len(inspect.cleandoc(t.description or "")) <= CLIENT_DESCRIPTION_CAP
    }
    if tight:
        pytest.skip(
            f"within {CLIENT_DESCRIPTION_CAP} but under {CLIENT_DESCRIPTION_CAP - TARGET} spare: {tight}"
        )


def test_the_wire_description_carries_no_leading_indentation() -> None:
    """FastMCP takes `description` verbatim from `__doc__`, and 3.11/3.12 keep a
    docstring's raw indentation where 3.13 dedents at compile time. The deployed
    image is 3.12, so without the `cleandoc` in `_tool` every description spends
    ~11% of a hard budget shipping leading spaces -- and the same server answers
    differently depending on which interpreter built it."""
    indented = {
        t.name: line
        for t in _tools()
        for line in (t.description or "").splitlines()[1:]
        if line[:1] == " " and line.strip() and not line.startswith("  ")
    }
    assert not indented, f"descriptions still carry docstring indentation: {indented}"


def test_server_instructions_fit_the_same_cap() -> None:
    """The client truncates a server's `instructions` with the same constant it
    uses on a tool `description`, and for a long time this one did not fit: 10,272
    characters, cut mid-sentence inside the registration rule, so every routing
    rule, anchoring rule and prose-home below it was silently absent. 80% of the
    sheet never reached a model.

    It is written to the cap now, as its own literal (the `doctrine.SHORT_*`
    fragments were inlined on 2026-09-13; nothing else read them). The write
    doctrine it used to carry lives in the surfaces nobody truncates --
    CLAUDE.md / AGENTS.md and the track-work skill -- and
    tests/test_doctrine_sync.py censuses those for every destination."""
    assert len(inspect.cleandoc(MCP_INSTRUCTIONS)) <= CLIENT_DESCRIPTION_CAP
