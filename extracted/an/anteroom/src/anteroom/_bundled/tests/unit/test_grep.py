"""Tests for tools/grep.py — grep tool edge cases."""

from __future__ import annotations

import pytest

from anteroom.tools.grep import handle, set_working_dir


@pytest.fixture(autouse=True)
def _set_working_dir(tmp_path):
    set_working_dir(str(tmp_path))
    yield


class TestGrepEdgeCases:
    async def test_invalid_regex_returns_error(self, tmp_path) -> None:
        result = await handle(pattern="[invalid")
        assert "error" in result
        assert "Invalid regex" in result["error"]

    async def test_max_results_limit(self, tmp_path) -> None:
        f = tmp_path / "big.txt"
        lines = ["match_line\n"] * 300
        f.write_text("".join(lines), encoding="utf-8")
        result = await handle(pattern="match_line", path=str(tmp_path))
        assert result["truncated"] is True
        assert result["total_matches"] == 200

    async def test_binary_file_skipped(self, tmp_path) -> None:
        """Files larger than _MAX_FILE_SIZE are skipped."""
        f = tmp_path / "large.bin"
        f.write_bytes(b"x" * 5_000_001)
        result = await handle(pattern="x", path=str(f))
        assert result["total_matches"] == 0

    async def test_search_single_file(self, tmp_path) -> None:
        f = tmp_path / "test.py"
        f.write_text("hello world\ngoodbye world\n", encoding="utf-8")
        result = await handle(pattern="hello", path=str(f))
        assert result["total_matches"] == 1
        assert len(result["matches"]) == 1
        assert result["matches"][0]["line_number"] == 1

    async def test_case_insensitive_search(self, tmp_path) -> None:
        f = tmp_path / "test.py"
        f.write_text("Hello World\n", encoding="utf-8")
        result = await handle(pattern="hello", path=str(f), case_insensitive=True)
        assert result["total_matches"] == 1

    async def test_path_not_found(self, tmp_path) -> None:
        result = await handle(pattern="test", path=str(tmp_path / "nonexistent"))
        assert "error" in result
