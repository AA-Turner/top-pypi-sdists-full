"""search_replace must REJECT edits that break Python syntax for a
file that parsed clean before the edit.

The Selenium-Login-Bot trace 2026-05-18 showed Gemma 4 loop 14+ times
editing the same file, each edit committed despite the post-edit
"⚠ SYNTAX ERROR ... tabs and spaces" warning. The warning was advisory
only — the file was modified and the model retried indefinitely. Now
the edit is rolled back and the model gets a REJECTED result so it
reads the file and fixes the indentation deliberately.
"""
from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from drydock.core.tools.base import BaseToolState
from drydock.core.tools.builtins.search_replace import (
    SearchReplace,
    SearchReplaceArgs,
    SearchReplaceConfig,
    SearchReplaceResult,
)


def _run(tool, args):
    async def go():
        out = []
        async for ev in tool.run(args):
            out.append(ev)
        return out
    return asyncio.run(go())


def _make_tool() -> SearchReplace:
    cfg = SearchReplaceConfig()
    return SearchReplace(config=cfg, state=BaseToolState())


def test_rollback_when_edit_breaks_syntax(tmp_path: Path) -> None:
    """The classic case: tabs+spaces mismatch from the REPLACE block."""
    src = tmp_path / "broken.py"
    src.write_text("def foo():\n    return 1\n")
    original = src.read_text()

    # The REPLACE uses a TAB where the original uses 4 spaces — this
    # is exactly the mismatch that bit Selenium Login Bot.
    content = (
        "<<<<<<< SEARCH\n"
        "def foo():\n"
        "    return 1\n"
        "=======\n"
        "def foo():\n"
        "\treturn 1\n"
        " return 1\n"
        ">>>>>>> REPLACE\n"
    )
    args = SearchReplaceArgs(file_path=str(src), content=content)
    tool = _make_tool()

    events = _run(tool, args)
    results = [e for e in events if isinstance(e, SearchReplaceResult)]
    assert results, "tool emitted no result"
    r = results[-1]

    # The file must be unchanged on disk.
    assert src.read_text() == original
    # The result must signal rejection.
    assert r.blocks_applied == 0
    assert r.lines_changed == 0
    assert "REJECTED" in r.content
    assert any("REJECTED" in w for w in r.warnings)


def test_ship_when_modified_content_is_clean(tmp_path: Path) -> None:
    src = tmp_path / "ok.py"
    src.write_text("def foo():\n    return 1\n")

    content = (
        "<<<<<<< SEARCH\n"
        "def foo():\n"
        "    return 1\n"
        "=======\n"
        "def foo():\n"
        "    return 2\n"
        ">>>>>>> REPLACE\n"
    )
    args = SearchReplaceArgs(file_path=str(src), content=content)
    tool = _make_tool()

    _run(tool, args)
    # File was actually modified.
    assert "return 2" in src.read_text()


def test_ship_when_original_was_already_broken(tmp_path: Path) -> None:
    """If the file ALREADY had a SyntaxError before our edit, allow
    the edit through — the model may be editing to FIX it. Blocking
    here would stall recovery."""
    src = tmp_path / "broken_already.py"
    src.write_text("def foo(:\n    pass\n")  # invalid

    content = (
        "<<<<<<< SEARCH\n"
        "def foo(:\n"
        "    pass\n"
        "=======\n"
        "def foo(:\n"
        "    return 1\n"  # still broken after, but original was too
        ">>>>>>> REPLACE\n"
    )
    args = SearchReplaceArgs(file_path=str(src), content=content)
    tool = _make_tool()

    _run(tool, args)
    # Edit went through.
    assert "return 1" in src.read_text()


def test_rollback_does_not_apply_to_non_python(tmp_path: Path) -> None:
    src = tmp_path / "x.md"
    src.write_text("# Title\n")
    content = (
        "<<<<<<< SEARCH\n"
        "# Title\n"
        "=======\n"
        "# Title v2\n"
        ">>>>>>> REPLACE\n"
    )
    args = SearchReplaceArgs(file_path=str(src), content=content)
    tool = _make_tool()
    _run(tool, args)
    assert "v2" in src.read_text()
