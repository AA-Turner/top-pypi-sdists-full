"""Regression: read_file on .ipynb strips outputs to keep context small.

Caught from operator's 2026-05-19 observation: Google_Trends_Analysis/
main.ipynb returned 64,073 chars and ballooned the session to 31K
tokens vs the 7-9K baseline. Notebook JSON has lots of redundant
output/metadata that the model rarely needs to read code.
"""
from __future__ import annotations

import asyncio
import json
from pathlib import Path

from drydock.core.tools.base import BaseToolState
from drydock.core.tools.builtins.read_file import (
    ReadFile,
    ReadFileArgs,
    ReadFileResult,
    ReadFileToolConfig,
)


def _make_tool() -> ReadFile:
    return ReadFile(config=ReadFileToolConfig(), state=BaseToolState())


def _run(tool: ReadFile, args: ReadFileArgs) -> ReadFileResult:
    async def go() -> ReadFileResult:
        result: ReadFileResult | None = None
        async for ev in tool.run(args):
            if isinstance(ev, ReadFileResult):
                result = ev
        assert result is not None
        return result
    return asyncio.run(go())


def _make_notebook(path: Path, n_cells: int = 3, output_bytes: int = 5000) -> None:
    cells = []
    for i in range(n_cells):
        cells.append({
            "cell_type": "code",
            "source": [f"x = {i}\n", f"print(x * 2)\n"],
            "execution_count": i + 1,
            "outputs": [
                {
                    "output_type": "stream",
                    "name": "stdout",
                    # huge fake output — would inflate the read
                    "text": "blah " * (output_bytes // 5),
                },
            ],
            "metadata": {},
        })
    notebook = {
        "cells": cells,
        "metadata": {"kernelspec": {"name": "python3"}},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path.write_text(json.dumps(notebook))


def test_notebook_output_stripped(tmp_path: Path) -> None:
    nb = tmp_path / "demo.ipynb"
    _make_notebook(nb, n_cells=3, output_bytes=10000)
    raw_size = nb.stat().st_size
    assert raw_size > 30000, "test notebook should be large to demonstrate the win"

    out = _run(_make_tool(), ReadFileArgs(path=str(nb)))
    # Returned content should be much smaller than the raw notebook
    assert len(out.content) < raw_size // 3, (
        f"slim notebook should be at least 3× smaller; "
        f"got {len(out.content)} vs raw {raw_size}"
    )
    # No raw output bytes in the slim form
    assert "blah blah blah" not in out.content
    # But cell source IS there
    assert "x = 0" in out.content
    assert "print(x * 2)" in out.content


def test_notebook_header_lists_cell_count(tmp_path: Path) -> None:
    nb = tmp_path / "demo.ipynb"
    _make_notebook(nb, n_cells=7)
    out = _run(_make_tool(), ReadFileArgs(path=str(nb)))
    assert "7 cells" in out.content


def test_notebook_outputs_summarized_per_cell(tmp_path: Path) -> None:
    nb = tmp_path / "demo.ipynb"
    _make_notebook(nb, n_cells=2)
    out = _run(_make_tool(), ReadFileArgs(path=str(nb)))
    # Each cell with outputs gets a "— outputs: [N stream]" annotation
    assert "outputs:" in out.content
    assert "stream" in out.content


def test_malformed_notebook_falls_back_to_plain(tmp_path: Path) -> None:
    """If the .ipynb isn't valid JSON, do a plain UTF-8 read instead of
    erroring out."""
    nb = tmp_path / "broken.ipynb"
    nb.write_text("{not valid json}")
    out = _run(_make_tool(), ReadFileArgs(path=str(nb)))
    # Falls back to plain content — at least the bytes are there
    assert "not valid json" in out.content


def test_non_ipynb_unchanged(tmp_path: Path) -> None:
    """Make sure the notebook path doesn't fire on regular files."""
    f = tmp_path / "foo.py"
    f.write_text("def hello(): return 1\n")
    out = _run(_make_tool(), ReadFileArgs(path=str(f)))
    assert out.content == "def hello(): return 1\n"
