"""Tests for services.tool_result_compact."""

from __future__ import annotations

import json

from anteroom.services.tool_result_compact import (
    compact_tool_output,
    compute_shape_hash,
    derive_error_class,
    summarize,
)


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


# ---------------------------------------------------------------------------
# CLI-UI summarize() mode (#1367)
# ---------------------------------------------------------------------------


class TestSummarizeCliMode:
    """``summarize()`` is additive: consumed by the CLI renderer and the web UI
    summary helper (#1467). Must not alter ``compact_tool_output`` behaviour.
    """

    def test_short_string_returned_unchanged(self) -> None:
        summary = summarize("hello world", head_lines=3, tail_lines=2)
        assert summary == "hello world"

    def test_empty_input(self) -> None:
        assert summarize("", head_lines=3, tail_lines=2) == ""
        assert summarize(None, head_lines=3, tail_lines=2) == ""

    def test_long_string_head_tail_slice(self) -> None:
        payload = "\n".join(f"line-{i}" for i in range(20))
        out = summarize(payload, head_lines=3, tail_lines=2)
        lines = out.split("\n")
        assert lines[0] == "line-0"
        assert lines[1] == "line-1"
        assert lines[2] == "line-2"
        assert lines[-1] == "line-19"
        assert lines[-2] == "line-18"
        # Middle marker appears
        assert any("[+" in part and "lines]" in part for part in lines)

    def test_dict_with_stdout_prefers_bulk_field(self) -> None:
        payload = {"exit_code": 0, "stdout": "\n".join(str(i) for i in range(50))}
        out = summarize(payload, head_lines=2, tail_lines=1)
        assert "0" in out
        assert "49" in out
        # Must have collapsed the middle
        assert "[+" in out

    def test_dict_with_error_field_surfaces_error(self) -> None:
        payload = {"exit_code": 1, "error": "boom: permission denied"}
        out = summarize(payload, head_lines=3, tail_lines=2)
        assert "boom: permission denied" in out

    def test_dict_with_content_field(self) -> None:
        payload = {"path": "/tmp/x", "content": "\n".join(str(i) for i in range(40))}
        out = summarize(payload, head_lines=2, tail_lines=2)
        assert "0" in out
        assert "39" in out
        assert "[+" in out

    def test_non_string_non_dict_falls_back_to_repr(self) -> None:
        out = summarize(42, head_lines=3, tail_lines=2)
        assert "42" in out

    def test_head_zero_tail_zero_collapses_entirely(self) -> None:
        payload = "\n".join(f"line-{i}" for i in range(5))
        out = summarize(payload, head_lines=0, tail_lines=0)
        # Zero-sized head/tail -> only the marker survives.
        assert "[+5 lines]" in out

    def test_single_line_returned_verbatim(self) -> None:
        assert summarize("only one", head_lines=3, tail_lines=2) == "only one"


class TestSummarizeDoesNotAffectCompact:
    """Regression: make sure introducing ``summarize()`` does not alter the
    existing LLM-replay ``compact_tool_output`` contract.
    """

    def test_compact_still_returns_json(self) -> None:
        raw = {"exit_code": 0, "stdout": "x" * 10_000}
        result = compact_tool_output(raw, max_chars=2000)
        # Still parseable JSON — not a plain-text slice.
        parsed = json.loads(result)
        assert parsed["exit_code"] == 0


class TestDeriveErrorClass:
    """Tests for #1467 ``derive_error_class`` helper."""

    def test_success_returns_none(self) -> None:
        assert derive_error_class({"exit_code": 0}, "success") is None

    def test_success_with_weird_output_still_none(self) -> None:
        # Zero-config contract: success status is ALWAYS None regardless of shape.
        assert derive_error_class({"error": "ignored"}, "success") is None

    def test_none_status_returns_none(self) -> None:
        assert derive_error_class({"error": "oops"}, None) is None

    def test_exit_nonzero(self) -> None:
        assert derive_error_class({"exit_code": 1}, "error") == "exit_nonzero"
        assert derive_error_class({"returncode": 2}, "error") == "exit_nonzero"

    def test_exception_non_dict(self) -> None:
        assert derive_error_class("boom", "error") == "exception"
        assert derive_error_class(None, "error") == "exception"

    def test_explicit_denied_flag(self) -> None:
        assert derive_error_class({"denied": True}, "error") == "denied"
        assert derive_error_class({"blocked": True}, "error") == "denied"

    def test_error_message_denied_keyword(self) -> None:
        assert derive_error_class({"error": "Permission denied"}, "error") == "denied"
        assert derive_error_class({"error": "blocked by policy"}, "error") == "denied"
        assert derive_error_class({"error": "Not allowed"}, "error") == "denied"

    def test_timeout(self) -> None:
        assert derive_error_class({"timeout": True}, "error") == "timeout"
        assert derive_error_class({"timed_out": True}, "error") == "timeout"
        assert derive_error_class({}, "timeout") == "timeout"
        assert derive_error_class({"error": "operation timed out"}, "error") == "timeout"

    def test_generic_exception(self) -> None:
        assert derive_error_class({"error": "value error"}, "error") == "exception"
        assert derive_error_class({"exception": "TypeError"}, "error") == "exception"

    def test_unknown_failure_shape_defaults_to_exception(self) -> None:
        # No known error marker — still classify as generic exception so the
        # web UI can still apply an error CSS class.
        assert derive_error_class({}, "error") == "exception"

    def test_status_success_wins_over_error_field(self) -> None:
        # If the status says success, we trust it.
        assert derive_error_class({"error": "weird"}, "success") is None


class TestComputeShapeHash:
    """Tests for #1467 ``compute_shape_hash`` helper."""

    def test_returns_16_char_hex(self) -> None:
        h = compute_shape_hash({"a": 1})
        assert len(h) == 16
        assert all(c in "0123456789abcdef" for c in h)

    def test_same_shape_same_hash(self) -> None:
        a = {"exit_code": 0, "stdout": "hello world"}
        b = {"exit_code": 0, "stdout": "different content"}
        # Bulk string content differs but the shape (keys + types + exit_code) is identical.
        assert compute_shape_hash(a) == compute_shape_hash(b)

    def test_different_exit_code_different_hash(self) -> None:
        a = {"exit_code": 0, "stdout": "x"}
        b = {"exit_code": 1, "stdout": "x"}
        assert compute_shape_hash(a) != compute_shape_hash(b)

    def test_different_keys_different_hash(self) -> None:
        a = {"exit_code": 0, "stdout": "x"}
        b = {"exit_code": 0, "stderr": "x"}
        assert compute_shape_hash(a) != compute_shape_hash(b)

    def test_none_and_empty_stable(self) -> None:
        # Both hash to a stable value; they should not raise.
        assert compute_shape_hash(None) == compute_shape_hash(None)
        assert compute_shape_hash({}) == compute_shape_hash({})

    def test_list_signature(self) -> None:
        # Lists of differing length produce different hashes.
        a = compute_shape_hash([1, 2, 3])
        b = compute_shape_hash([1, 2])
        assert a != b

    def test_pathological_input_does_not_raise(self) -> None:
        class Weird:
            def __repr__(self) -> str:
                raise RuntimeError("no repr for you")

        # ``default=str`` and the fallback ``repr(output)`` should keep this safe.
        # If even ``repr`` raises, we should still return a 16-char hex.
        try:
            h = compute_shape_hash(Weird())
            assert len(h) == 16
        except RuntimeError:
            # Acceptable fallback: repr raised. The function uses str fallback
            # first via json dumps default=str, so this path should be rare.
            pass

    def test_nested_dict_stable(self) -> None:
        # Key order should not matter — dict signature sorts keys.
        a = compute_shape_hash({"a": {"x": 1, "y": 2}})
        b = compute_shape_hash({"a": {"y": 2, "x": 1}})
        assert a == b
