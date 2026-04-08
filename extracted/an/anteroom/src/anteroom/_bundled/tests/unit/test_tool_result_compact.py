"""Tests for services.tool_result_compact."""

from __future__ import annotations

import json

from anteroom.services.tool_result_compact import compact_tool_output


class TestSmallResultUnchanged:
    def test_small_dict_passes_through(self) -> None:
        raw = {"exit_code": 0, "stdout": "hello"}
        result = compact_tool_output(raw, max_chars=5000)
        parsed = json.loads(result)
        assert parsed == raw

    def test_empty_dict(self) -> None:
        result = compact_tool_output({}, max_chars=2000)
        assert result == "{}"


class TestOversizedStdoutTruncated:
    def test_large_stdout_is_truncated(self) -> None:
        raw = {"exit_code": 0, "path": "/tmp/test", "stdout": "x" * 100_000}
        result = compact_tool_output(raw, max_chars=2000)
        assert len(result) <= 3000  # allows for truncation suffix overhead
        parsed = json.loads(result)
        assert parsed["exit_code"] == 0
        assert parsed["path"] == "/tmp/test"
        assert "truncated" in parsed["stdout"]
        assert "100000 chars total" in parsed["stdout"]


class TestStripsInternalKeys:
    def test_underscore_keys_removed(self) -> None:
        raw = {
            "exit_code": 0,
            "stdout": "ok",
            "_old_content": "big old content" * 1000,
            "_new_content": "big new content" * 1000,
        }
        result = compact_tool_output(raw, max_chars=5000)
        parsed = json.loads(result)
        assert "_old_content" not in parsed
        assert "_new_content" not in parsed
        assert parsed["exit_code"] == 0
        assert parsed["stdout"] == "ok"


class TestNonDictInput:
    def test_string_input(self) -> None:
        result = compact_tool_output("hello world", max_chars=2000)
        assert json.loads(result) == "hello world"

    def test_int_input(self) -> None:
        result = compact_tool_output(42, max_chars=2000)
        assert json.loads(result) == 42

    def test_none_input(self) -> None:
        result = compact_tool_output(None, max_chars=2000)
        assert json.loads(result) is None

    def test_long_string_truncated(self) -> None:
        long_str = "a" * 5000
        result = compact_tool_output(long_str, max_chars=100)
        assert len(result) <= 100
        # Result must always be parseable JSON
        parsed = json.loads(result)
        assert isinstance(parsed, str)
        assert "truncated" in parsed
        assert parsed.startswith("a")

    def test_long_string_with_special_chars_stays_valid_json(self) -> None:
        # Quotes, backslashes, and newlines must be escaped properly
        nasty = ('"\\\n' * 1000) + "tail"
        result = compact_tool_output(nasty, max_chars=200)
        assert len(result) <= 200
        json.loads(result)  # must not raise

    def test_list_input(self) -> None:
        result = compact_tool_output([1, 2, 3], max_chars=2000)
        assert json.loads(result) == [1, 2, 3]


class TestStructuredFieldsPreserved:
    def test_exit_code_survives_truncation(self) -> None:
        raw = {"exit_code": 1, "error": "segfault", "stdout": "x" * 50_000, "stderr": "y" * 50_000}
        result = compact_tool_output(raw, max_chars=500)
        parsed = json.loads(result)
        assert parsed["exit_code"] == 1
        assert parsed["error"] == "segfault"

    def test_url_and_file_preserved(self) -> None:
        raw = {
            "url": "https://example.com",
            "file": "/tmp/out.txt",
            "returncode": 0,
            "content": "z" * 50_000,
        }
        result = compact_tool_output(raw, max_chars=500)
        parsed = json.loads(result)
        assert parsed["url"] == "https://example.com"
        assert parsed["file"] == "/tmp/out.txt"
        assert parsed["returncode"] == 0

    def test_path_preserved(self) -> None:
        raw = {"path": "/home/user/file.py", "output": "o" * 50_000}
        result = compact_tool_output(raw, max_chars=300)
        parsed = json.loads(result)
        assert parsed["path"] == "/home/user/file.py"


class TestEdgeCases:
    def test_zero_max_chars(self) -> None:
        # Clamped to a 2-char floor; output is still valid JSON
        result = compact_tool_output("x", max_chars=0)
        assert isinstance(result, str)
        json.loads(result)
        assert len(result) <= 2

    def test_very_small_max_chars(self) -> None:
        result = compact_tool_output({"stdout": "hello"}, max_chars=5)
        assert isinstance(result, str)
        # Always parseable JSON, never exceeds budget
        json.loads(result)
        assert len(result) <= 5

    def test_tiny_budget_does_not_leak_string_tail(self) -> None:
        # Regression: text[:max_chars - 3] used a negative slice for max_chars
        # in 1..2, which wrapped around and exposed the tail of the string.
        secret = "a" * 100 + "SENSITIVE"
        for budget in (2, 3, 4, 10, 20):
            result = compact_tool_output(secret, max_chars=budget)
            assert len(result) <= budget
            assert "SENSITIVE" not in result
            # Every fallback path must produce valid JSON
            json.loads(result)

    def test_oversize_marker_is_valid_json(self) -> None:
        # Regression: previous fallback raw-sliced JSON, producing malformed output.
        # All fallback paths must return valid JSON.
        raw = {"exit_code": 0, "error": "x" * 200, "path": "y" * 200, "stdout": "z" * 5000}
        result = compact_tool_output(raw, max_chars=20)
        json.loads(result)  # must not raise
        assert len(result) <= 20

    def test_non_string_bulk_value(self) -> None:
        raw = {"exit_code": 0, "output": {"nested": "dict", "more": [1, 2, 3]}}
        result = compact_tool_output(raw, max_chars=2000)
        parsed = json.loads(result)
        assert parsed["exit_code"] == 0
        assert "output" in parsed
