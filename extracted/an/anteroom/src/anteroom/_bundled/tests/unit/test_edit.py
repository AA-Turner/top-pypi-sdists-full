"""Tests for tools/edit.py — edit_file tool."""

from __future__ import annotations

import pytest

from anteroom.tools.edit import handle, set_working_dir


@pytest.fixture(autouse=True)
def _set_working_dir(tmp_path):
    set_working_dir(str(tmp_path))
    yield


class TestEditFileErrors:
    async def test_file_not_found(self, tmp_path) -> None:
        result = await handle(
            path=str(tmp_path / "nonexistent.py"),
            old_text="foo",
            new_text="bar",
        )
        assert "error" in result
        assert "not found" in result["error"].lower()

    async def test_old_text_not_found(self, tmp_path) -> None:
        f = tmp_path / "test.py"
        f.write_text("hello world", encoding="utf-8")
        result = await handle(
            path=str(f),
            old_text="nonexistent text",
            new_text="replacement",
        )
        assert "error" in result
        assert "not found" in result["error"]

    async def test_ambiguous_match(self, tmp_path) -> None:
        f = tmp_path / "test.py"
        f.write_text("foo\nbar\nfoo\n", encoding="utf-8")
        result = await handle(
            path=str(f),
            old_text="foo",
            new_text="baz",
        )
        assert "error" in result
        assert "2 times" in result["error"]

    async def test_replace_all_with_multiple_matches(self, tmp_path) -> None:
        f = tmp_path / "test.py"
        f.write_text("foo\nbar\nfoo\n", encoding="utf-8")
        result = await handle(
            path=str(f),
            old_text="foo",
            new_text="baz",
            replace_all=True,
        )
        assert result["status"] == "ok"
        assert result["replacements"] == 2
        assert f.read_text(encoding="utf-8") == "baz\nbar\nbaz\n"

    async def test_successful_single_replacement(self, tmp_path) -> None:
        f = tmp_path / "test.py"
        f.write_text("hello world\n", encoding="utf-8")
        result = await handle(
            path=str(f),
            old_text="hello",
            new_text="goodbye",
        )
        assert result["status"] == "ok"
        assert result["replacements"] == 1
        assert f.read_text(encoding="utf-8") == "goodbye world\n"
        assert "_old_content" in result
        assert "_new_content" in result
