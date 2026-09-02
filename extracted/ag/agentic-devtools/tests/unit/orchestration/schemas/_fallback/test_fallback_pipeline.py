"""Tests for fallback parsing pipeline."""

import json

from agentic_devtools.orchestration.schemas._fallback import (
    extract_code_fences,
    extract_json_from_prose,
    normalize_single_quotes,
    remove_trailing_commas,
    run_fallback_pipeline,
    strip_bom_and_invisible,
    unwrap_list_to_single,
)
from agentic_devtools.orchestration.schemas.shared.stop_condition import StopCondition


class TestStripBom:
    """Tests for BOM/invisible Unicode stripping."""

    def test_strips_bom(self):
        text = '\ufeff{"reason": "test"}'
        assert strip_bom_and_invisible(text) == '{"reason": "test"}'

    def test_strips_zero_width_spaces(self):
        text = '\u200b{"reason": "test"}\u200b'
        assert strip_bom_and_invisible(text) == '{"reason": "test"}'

    def test_no_change_for_clean_input(self):
        text = '{"reason": "test"}'
        assert strip_bom_and_invisible(text) == text

    def test_preserves_invisible_chars_inside_json_string_values(self):
        text = '{"reason": "keeps\\u00a0internal\\u2028content"}'
        assert strip_bom_and_invisible(text) == text


class TestExtractCodeFences:
    """Tests for markdown code fence extraction."""

    def test_single_json_fence(self):
        text = 'Here:\n```json\n{"reason": "test"}\n```\nDone.'
        blocks = extract_code_fences(text)
        assert len(blocks) == 1
        assert blocks[0] == '{"reason": "test"}'

    def test_multiple_blocks(self):
        text = '```json\n{"a": 1}\n```\n\n```json\n{"b": 2}\n```'
        blocks = extract_code_fences(text)
        assert len(blocks) == 2

    def test_windows_newline_fence(self):
        text = '```json\r\n{"a": 1}\r\n```'
        blocks = extract_code_fences(text)
        assert blocks == ['{"a": 1}']

    def test_no_fences(self):
        text = "No code fences here."
        assert extract_code_fences(text) == []


class TestExtractJsonFromProse:
    """Tests for JSON extraction from surrounding prose."""

    def test_extracts_json_object(self):
        text = 'The result is: {"reason": "found"} and that\'s it.'
        results = extract_json_from_prose(text)
        assert len(results) >= 1
        assert '{"reason": "found"}' in results

    def test_extracts_nested_objects(self):
        text = 'Result: {"outer": {"inner": true}}'
        results = extract_json_from_prose(text)
        assert len(results) >= 1

    def test_unmatched_close_brace_before_object_does_not_block_extraction(self):
        """Unmatched '}' before a valid object must not drive depth negative."""
        text = '} {"reason": "found"}'
        results = extract_json_from_prose(text)
        assert '{"reason": "found"}' in results

    def test_unmatched_close_bracket_before_array_does_not_block_extraction(self):
        """Unmatched ']' before a valid array must not drive depth negative."""
        text = '] ["a", "b"]'
        results = extract_json_from_prose(text)
        assert '["a", "b"]' in results

    def test_valid_object_after_multiple_unmatched_braces(self):
        """Multiple unmatched '}' characters before a valid object are ignored."""
        text = '}} } {"key": "value"}'
        results = extract_json_from_prose(text)
        assert '{"key": "value"}' in results

    def test_braces_inside_string_value_not_counted(self):
        """Braces inside a JSON string value must not affect depth tracking.

        An LLM may emit code snippets inside string fields, e.g.
        ``{"code": "if (x) {return x;}"}``.  The inner ``{`` and ``}`` are
        part of the string value and must not confuse the brace-depth counter.
        """
        text = 'The result: {"code": "if (x) {return x;}"} done.'
        results = extract_json_from_prose(text)
        assert len(results) == 1
        assert results[0] == '{"code": "if (x) {return x;}"}'

    def test_brackets_inside_string_value_not_counted(self):
        """Brackets inside a JSON string value must not affect depth tracking.

        An LLM may emit array-access expressions inside string fields, e.g.
        ``[{"value": "arr[0]"}]``.  The ``[`` and ``]`` inside the string must
        not cause the array-depth counter to miscalculate the span.
        """
        text = 'Result: [{"value": "arr[0]"}] done.'
        results = extract_json_from_prose(text)
        # The full array must be extractable
        assert '[{"value": "arr[0]"}]' in results

    def test_escaped_quote_inside_string_not_treated_as_string_end(self):
        r"""A ``\"`` escape sequence must not be treated as closing the string.

        Given ``{"msg": "say \"hi\""}``, the ``\"`` sequences are part of the
        string value; the string ends only at the unescaped closing ``"``.
        """
        text = r'{"msg": "say \"hi\""}'
        results = extract_json_from_prose(text)
        assert len(results) >= 1
        assert text in results


class TestNormalizeQuotes:
    """Tests for single-quote normalization."""

    def test_replaces_single_with_double(self):
        text = "{'reason': 'test'}"
        result = normalize_single_quotes(text)
        assert result == '{"reason": "test"}'

    def test_preserves_apostrophes_inside_string_content(self):
        text = "{'reason': \"don't mutate\"}"
        result = normalize_single_quotes(text)
        assert result == '{"reason": "don\'t mutate"}'


class TestRemoveTrailingCommas:
    """Tests for trailing comma removal."""

    def test_removes_trailing_comma_before_brace(self):
        text = '{"reason": "test",}'
        assert remove_trailing_commas(text) == '{"reason": "test"}'

    def test_removes_trailing_comma_before_bracket(self):
        text = '["a", "b",]'
        assert remove_trailing_commas(text) == '["a", "b"]'

    def test_no_change_without_trailing_comma(self):
        text = '{"reason": "test"}'
        assert remove_trailing_commas(text) == text

    def test_preserves_comma_before_brace_inside_string_value(self):
        """Comma followed by '}' inside a quoted string must not be removed.

        Regression: the old regex-based implementation would transform
        ``{"code": "return x,}"}`` into ``{"code": "return x"}`` which
        is both invalid JSON and silently corrupt data.
        """
        text = '{"code": "return x,}"}'
        assert remove_trailing_commas(text) == text

    def test_preserves_comma_before_bracket_inside_string_value(self):
        """Comma followed by ']' inside a quoted string must not be removed."""
        text = '{"code": "arr[i,]"}'
        assert remove_trailing_commas(text) == text

    def test_removes_nested_trailing_commas(self):
        """Trailing commas at multiple nesting levels are all removed."""
        text = '{"a": {"b": 1,},}'
        assert remove_trailing_commas(text) == '{"a": {"b": 1}}'

    def test_escaped_quote_inside_string_does_not_end_string(self):
        r"""A ``\"`` escape must not be treated as the end of the string.

        Given ``{"msg": "say \"hi\"",}``, the backslash-escaped quotes are
        part of the string value; the trailing comma after the value must
        still be removed.
        """
        text = r'{"msg": "say \"hi\"",}'
        assert remove_trailing_commas(text) == r'{"msg": "say \"hi\""}'


class TestUnwrapList:
    """Tests for list-to-single-object unwrapping."""

    def test_unwraps_single_element_array(self):
        text = '[{"reason": "test"}]'
        result = unwrap_list_to_single(text)
        assert result is not None
        assert json.loads(result) == {"reason": "test"}

    def test_returns_none_for_multi_element(self):
        text = '[{"a": 1}, {"b": 2}]'
        assert unwrap_list_to_single(text) is None

    def test_returns_none_for_invalid_json(self):
        assert unwrap_list_to_single("not json") is None


class TestFallbackPipeline:
    """Tests for the complete fallback pipeline orchestration."""

    def test_bom_strategy(self):
        raw = "\ufeff" + json.dumps({"reason": "bom"})
        result = run_fallback_pipeline(StopCondition, raw)
        assert result is not None
        assert result.reason == "bom"

    def test_code_fence_strategy(self):
        raw = "```json\n" + json.dumps({"reason": "fence"}) + "\n```"
        result = run_fallback_pipeline(StopCondition, raw)
        assert result is not None
        assert result.reason == "fence"

    def test_prose_extraction_strategy(self):
        raw = "The output is " + json.dumps({"reason": "prose"}) + " done."
        result = run_fallback_pipeline(StopCondition, raw)
        assert result is not None
        assert result.reason == "prose"

    def test_trailing_comma_strategy(self):
        raw = '{"reason": "comma",}'
        result = run_fallback_pipeline(StopCondition, raw)
        assert result is not None
        assert result.reason == "comma"

    def test_trailing_comma_strategy_with_double_quoted_json(self):
        """remove_trailing_commas succeeds when single-quote normalization is a no-op."""
        raw = '{"reason": "comma", "escalation_reason": null,}'
        result = run_fallback_pipeline(StopCondition, raw)
        assert result is not None
        assert result.reason == "comma"

    def test_unwrap_list_strategy(self):
        raw = '[{"reason": "unwrap"}]'
        result = run_fallback_pipeline(StopCondition, raw)
        assert result is not None
        assert result.reason == "unwrap"

    def test_all_fail_returns_none(self):
        result = run_fallback_pipeline(StopCondition, "completely invalid content")
        assert result is None

    def test_multiple_code_fences_warning(self):
        """Line 143-144: Multiple JSON blocks triggers warning."""
        valid = json.dumps({"reason": "first"})
        raw = f"```json\n{valid}\n```\n\n```json\n{valid}\n```"
        result = run_fallback_pipeline(StopCondition, raw)
        assert result is not None
        assert result.reason == "first"

    def test_single_quote_normalization_strategy(self):
        """Lines 166-169: Strategy 4 - single quote normalization succeeds."""
        raw = "{'reason': 'quotes'}"
        result = run_fallback_pipeline(StopCondition, raw)
        assert result is not None
        assert result.reason == "quotes"

    def test_unwrap_on_cleaned_text(self):
        """Lines 184-187: Strategy 6 unwrap succeeds on cleaned variant."""
        from unittest.mock import patch

        inner = json.dumps({"reason": "unwrap-cleaned"})
        raw = f"\ufeff[{inner}]"
        # Patch extract_json_from_prose to return empty so strategy 3 doesn't pre-empt
        with patch(
            "agentic_devtools.orchestration.schemas._fallback.extract_json_from_prose",
            return_value=[],
        ):
            result = run_fallback_pipeline(StopCondition, raw)
        assert result is not None
        assert result.reason == "unwrap-cleaned"

    def test_combined_code_fence_trailing_comma(self):
        """Lines 191-196: Combined strategy removes trailing commas from code fence."""
        raw = '```json\n{"reason": "combined",}\n```'
        result = run_fallback_pipeline(StopCondition, raw)
        assert result is not None
        assert result.reason == "combined"

    def test_array_extraction_nested_brackets(self):
        """Branch 77->79: Nested array brackets increase depth without starting new extraction."""
        results = extract_json_from_prose("outer [[1,2],3] end")
        assert len(results) >= 1
        # The full outer array should be extracted
        assert "[[1,2],3]" in results

    def test_array_extraction_duplicate_skipped(self):
        """Branch 84->86: Same array candidate string appears twice, second is skipped."""
        results = extract_json_from_prose("[1] text [1]")
        # The second [1] is a duplicate and should be skipped
        assert results.count("[1]") == 1

    def test_array_extraction_depth_mismatch(self):
        """Branch 82->75: ']' encountered when depth > 0 (nested bracket) continues loop."""
        # Nested arrays - inner ] doesn't terminate extraction because depth > 0
        results = extract_json_from_prose("text [[1, 2], 3] end")
        assert len(results) >= 1
        assert "[[1, 2], 3]" in results

    def test_single_quote_normalization_no_match(self):
        """Branch 167->172: Single-quote normalization produces different text but it still doesn't validate."""
        # Has single quotes so normalization changes it, but result is NOT valid for StopCondition schema
        raw = "{'not_a_valid_field': 'value'}"
        result = run_fallback_pipeline(StopCondition, raw)
        # Falls through to subsequent strategies; ultimately returns None
        assert result is None

    def test_unwrap_list_fails_validation_continues_loop(self):
        """Branch 185->181: Unwrap succeeds (gets JSON) but validation still fails, continues loop."""
        # Single-element array but content doesn't match StopCondition schema
        raw = '[{"invalid_key": "not a stop condition"}]'
        result = run_fallback_pipeline(StopCondition, raw)
        assert result is None

    def test_combined_strategy_no_trailing_comma_in_block(self):
        """Branch 192->190: Code fence block has no trailing commas, skip combined strategy."""
        # Code fence with valid JSON that just doesn't match the schema
        raw = '```json\n{"bad_field": "value"}\n```'
        result = run_fallback_pipeline(StopCondition, raw)
        assert result is None

    def test_combined_strategy_fix_doesnt_validate(self):
        """Branch 194->190: Code fence trailing comma removed but still doesn't validate."""
        # Has trailing comma but schema validation still fails after fix
        raw = '```json\n{"bad_field": "value",}\n```'
        result = run_fallback_pipeline(StopCondition, raw)
        assert result is None

    def test_combined_prose_trailing_comma_strategy(self):
        """Combined strategy removes trailing commas from prose-extracted JSON."""
        raw = 'The result is: {"reason": "prose-comma",} done.'
        result = run_fallback_pipeline(StopCondition, raw)
        assert result is not None
        assert result.reason == "prose-comma"

    def test_combined_prose_trailing_comma_fix_doesnt_validate(self):
        """Combined prose strategy: trailing comma removed but schema validation still fails."""
        raw = 'The result is: {"bad_field": "value",} done.'
        result = run_fallback_pipeline(StopCondition, raw)
        assert result is None

    def test_combined_prose_no_trailing_comma_in_candidate(self):
        """Combined prose loop skips candidates that have no trailing comma (if fixed == candidate)."""
        # JSON in prose without trailing comma; strategy 3 fails validation; combined prose skips
        raw = 'The output: {"bad_field": "no_comma"} done.'
        result = run_fallback_pipeline(StopCondition, raw)
        assert result is None

    def test_combined_prose_no_candidates_skips_combined(self):
        """Combined prose strategy is skipped when no prose candidates are found."""
        # Plain invalid text with no JSON-like structure at all
        raw = "completely invalid content with no braces"
        result = run_fallback_pipeline(StopCondition, raw)
        assert result is None

    def test_trailing_comma_strategy_no_prose_candidates(self):
        """Strategy 5 is exercised when prose extraction finds no candidates."""
        from unittest.mock import patch

        # Use JSON boolean `true` so literal_eval fails (Python uses True), ensuring strategy 4
        # is a no-op and strategy 5 is the first to fix the trailing comma.
        raw = '{"reason": "strategy5", "is_recoverable": true,}'
        with patch(
            "agentic_devtools.orchestration.schemas._fallback.extract_json_from_prose",
            return_value=[],
        ):
            result = run_fallback_pipeline(StopCondition, raw)
        assert result is not None
        assert result.reason == "strategy5"
        assert result.is_recoverable is True

    def test_combined_code_fence_trailing_comma_no_prose_candidates(self):
        """Combined code-fence strategy is exercised when prose extraction finds no candidates."""
        from unittest.mock import patch

        raw = '```json\n{"reason": "combined",}\n```'
        with patch(
            "agentic_devtools.orchestration.schemas._fallback.extract_json_from_prose",
            return_value=[],
        ):
            result = run_fallback_pipeline(StopCondition, raw)
        assert result is not None
        assert result.reason == "combined"
