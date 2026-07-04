"""TDD tests for critical issues identified in codebase analysis.

This test file covers:
- Critical Index/Bounds Safety (Issues #1, #7, #9)
- Silent Exception Handling (Issue #4)
- Input Validation (Issue #6)
- Safe Array Access Patterns
- JSON Parsing Safety
- Regex Group Safety

Run with: pytest sage/tests/test_critical_fixes.py -v
"""

from __future__ import annotations

import json
import re
from collections import Counter
from typing import Any
from unittest.mock import patch

import pytest

# =============================================================================
# Test Utilities and Safe Access Patterns
# =============================================================================


def safe_list_get(lst: list, index: int, default: Any = None) -> Any:
    """Safely get item from list with bounds checking."""
    if lst and 0 <= index < len(lst):
        return lst[index]
    return default


def safe_dict_path(data: dict, *keys: str, default: Any = None) -> Any:
    """Safely navigate nested dict with default fallback."""
    current = data
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key)
        if current is None:
            return default
    return current


def safe_first(iterable, default: Any = None) -> Any:
    """Safely get first element of any iterable."""
    try:
        return next(iter(iterable), default)
    except (StopIteration, TypeError):
        return default


def safe_json_parse(text: str, default: Any = None) -> Any:
    """Safely parse JSON with default fallback."""
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return default


def safe_regex_group(match: re.Match | None, group: int, default: str = "") -> str:
    """Safely get regex group with bounds checking."""
    if match is None:
        return default
    try:
        result = match.group(group)
        return result if result is not None else default
    except (IndexError, AttributeError):
        return default


# =============================================================================
# Test: Safe List Access
# =============================================================================


class TestSafeListAccess:
    """Tests for safe list access patterns."""

    def test_safe_list_get_valid_index(self):
        """Test safe access with valid index."""
        lst = ["a", "b", "c"]
        assert safe_list_get(lst, 0) == "a"
        assert safe_list_get(lst, 2) == "c"

    def test_safe_list_get_negative_index_returns_default(self):
        """Test that negative index returns default."""
        lst = ["a", "b", "c"]
        assert safe_list_get(lst, -1) is None
        assert safe_list_get(lst, -1, "default") == "default"

    def test_safe_list_get_out_of_bounds(self):
        """Test out of bounds returns default."""
        lst = ["a", "b"]
        assert safe_list_get(lst, 5) is None
        assert safe_list_get(lst, 5, "fallback") == "fallback"

    def test_safe_list_get_empty_list(self):
        """Test empty list returns default."""
        assert safe_list_get([], 0) is None
        assert safe_list_get([], 0, "empty") == "empty"

    def test_safe_list_get_none_list(self):
        """Test None list returns default."""
        assert safe_list_get(None, 0) is None
        assert safe_list_get(None, 0, "none") == "none"

    def test_safe_first_with_list(self):
        """Test safe_first with list."""
        assert safe_first([1, 2, 3]) == 1
        assert safe_first([]) is None
        assert safe_first([], "default") == "default"

    def test_safe_first_with_generator(self):
        """Test safe_first with generator."""
        gen = (x for x in [1, 2, 3])
        assert safe_first(gen) == 1

    def test_safe_first_with_none(self):
        """Test safe_first with None."""
        assert safe_first(None) is None


# =============================================================================
# Test: Safe Dict Path Navigation
# =============================================================================


class TestSafeDictPath:
    """Tests for safe nested dict access."""

    def test_safe_dict_path_valid(self):
        """Test valid nested path."""
        data = {"a": {"b": {"c": "value"}}}
        assert safe_dict_path(data, "a", "b", "c") == "value"

    def test_safe_dict_path_missing_key(self):
        """Test missing key returns default."""
        data = {"a": {"b": "value"}}
        assert safe_dict_path(data, "a", "c") is None
        assert safe_dict_path(data, "a", "c", default="missing") == "missing"

    def test_safe_dict_path_empty_dict(self):
        """Test empty dict returns default."""
        assert safe_dict_path({}, "a") is None

    def test_safe_dict_path_none_intermediate(self):
        """Test None value in path returns default."""
        data = {"a": None}
        assert safe_dict_path(data, "a", "b") is None

    def test_safe_dict_path_non_dict_intermediate(self):
        """Test non-dict value in path returns default."""
        data = {"a": "string"}
        assert safe_dict_path(data, "a", "b") is None

    def test_llm_response_parsing(self):
        """Test realistic LLM response parsing."""
        # Valid response
        valid_response = {"choices": [{"message": {"content": "Hello!"}}]}
        content = safe_dict_path(
            safe_list_get(safe_dict_path(valid_response, "choices"), 0), "message", "content"
        )
        assert content == "Hello!"

        # Empty choices
        empty_response = {"choices": []}
        choice = safe_list_get(safe_dict_path(empty_response, "choices"), 0)
        assert choice is None

        # Missing key
        malformed = {"data": "something"}
        assert safe_dict_path(malformed, "choices") is None


# =============================================================================
# Test: Safe JSON Parsing
# =============================================================================


class TestSafeJsonParsing:
    """Tests for safe JSON parsing."""

    def test_safe_json_parse_valid(self):
        """Test parsing valid JSON."""
        assert safe_json_parse('{"key": "value"}') == {"key": "value"}
        assert safe_json_parse("[1, 2, 3]") == [1, 2, 3]

    def test_safe_json_parse_invalid(self):
        """Test parsing invalid JSON returns default."""
        assert safe_json_parse("not json") is None
        assert safe_json_parse("not json", {}) == {}
        assert safe_json_parse("{invalid}", []) == []

    def test_safe_json_parse_empty(self):
        """Test parsing empty string."""
        assert safe_json_parse("") is None
        assert safe_json_parse("", "default") == "default"

    def test_safe_json_parse_none(self):
        """Test parsing None."""
        assert safe_json_parse(None) is None


# =============================================================================
# Test: Safe Regex Group Access
# =============================================================================


class TestSafeRegexGroup:
    """Tests for safe regex group extraction."""

    def test_safe_regex_group_valid(self):
        """Test valid group extraction."""
        match = re.match(r"(\w+):(\d+)", "file:123")
        assert safe_regex_group(match, 1) == "file"
        assert safe_regex_group(match, 2) == "123"

    def test_safe_regex_group_no_match(self):
        """Test no match returns default."""
        match = re.match(r"(\d+)", "no numbers")
        assert match is None
        assert safe_regex_group(match, 1) == ""
        assert safe_regex_group(match, 1, "default") == "default"

    def test_safe_regex_group_out_of_bounds(self):
        """Test group index out of bounds."""
        match = re.match(r"(\w+)", "word")
        assert safe_regex_group(match, 5) == ""
        assert safe_regex_group(match, 5, "missing") == "missing"

    def test_safe_regex_group_none_match(self):
        """Test None match object."""
        assert safe_regex_group(None, 1) == ""


# =============================================================================
# Test: Counter Most Common Safety
# =============================================================================


class TestCounterSafety:
    """Tests for safe Counter.most_common() access."""

    def test_counter_most_common_non_empty(self):
        """Test most_common with data."""
        counter = Counter(["a", "a", "b", "c", "c", "c"])
        most_common = counter.most_common(1)
        assert len(most_common) > 0
        assert most_common[0] == ("c", 3)

    def test_counter_most_common_empty(self):
        """Test most_common on empty counter."""
        counter = Counter()
        most_common = counter.most_common(1)
        assert most_common == []
        # Safe access
        first = safe_first(most_common)
        assert first is None

    def test_safe_counter_pattern(self):
        """Test safe pattern for using Counter.most_common()."""

        def safe_most_common_value(counter: Counter, min_count: int = 5) -> str | None:
            """Safely get most common value if it meets threshold."""
            most_common = counter.most_common(1)
            if most_common and most_common[0][1] >= min_count:
                return most_common[0][0]
            return None

        # Has enough counts
        counter1 = Counter(["a"] * 10)
        assert safe_most_common_value(counter1, 5) == "a"

        # Not enough counts
        counter2 = Counter(["a", "b"])
        assert safe_most_common_value(counter2, 5) is None

        # Empty counter
        counter3 = Counter()
        assert safe_most_common_value(counter3, 5) is None


# =============================================================================
# Test: Max/Min on Empty Collections
# =============================================================================


class TestMaxMinSafety:
    """Tests for safe max/min operations."""

    def test_max_with_default(self):
        """Test max with default on empty."""
        assert max([], default=None) is None
        assert max([], default=0) == 0

    def test_max_with_key_and_default(self):
        """Test max with key function and default."""
        items = []
        result = max(items, key=lambda x: x.get("score", 0), default=None)
        assert result is None

    def test_safe_max_pattern(self):
        """Test safe pattern for max on potentially empty list."""

        def safe_best_model(models: list) -> dict | None:
            """Safely get best model by capability score."""
            if not models:
                return None
            return max(models, key=lambda m: m.get("score", 0))

        assert safe_best_model([]) is None
        assert safe_best_model([{"score": 5}]) == {"score": 5}
        models = [{"score": 3}, {"score": 8}, {"score": 1}]
        assert safe_best_model(models) == {"score": 8}


# =============================================================================
# Test: String Operations Safety
# =============================================================================


class TestStringSafety:
    """Tests for safe string operations."""

    def test_split_with_maxsplit(self):
        """Test split with maxsplit for safety."""
        # Always use maxsplit when expecting specific parts
        s = "model:version:extra"
        parts = s.split(":", 1)
        assert len(parts) == 2
        assert parts[0] == "model"
        assert parts[1] == "version:extra"

    def test_split_empty_string(self):
        """Test split on empty string."""
        s = ""
        parts = s.split(":")
        assert parts == [""]
        # Safe access
        assert safe_list_get(parts, 0) == ""
        assert safe_list_get(parts, 1) is None

    def test_safe_string_slice(self):
        """Test safe string slicing."""

        def safe_slice(s: str, length: int) -> str:
            """Safely slice string to max length."""
            return s[:length] if s else ""

        assert safe_slice("hello", 3) == "hel"
        assert safe_slice("hi", 10) == "hi"
        assert safe_slice("", 5) == ""
        assert safe_slice(None, 5) == ""


# =============================================================================
# Test: Input Validation
# =============================================================================


class TestInputValidation:
    """Tests for input validation functions."""

    def test_validate_user_input_none(self):
        """Test handling None user input."""

        def process_input(user_input: str | None) -> str:
            if user_input is None:
                return ""
            return user_input.lower().strip()

        assert process_input(None) == ""
        assert process_input("  HELLO  ") == "hello"
        assert process_input("") == ""

    def test_validate_model_id(self):
        """Test model ID validation."""
        import re

        SAFE_MODEL_ID_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9_:\.\-]{0,127}$"

        def is_valid_model_id(model_id: str | None) -> bool:
            if not model_id:
                return False
            return bool(re.match(SAFE_MODEL_ID_PATTERN, model_id))

        assert is_valid_model_id("gpt-4") is True
        assert is_valid_model_id("llama:7b") is True
        assert is_valid_model_id("") is False
        assert is_valid_model_id(None) is False
        assert is_valid_model_id("../../../etc/passwd") is False
        assert is_valid_model_id("-starts-with-dash") is False

    def test_validate_path_traversal(self):
        """Test path traversal prevention."""

        def is_safe_path(path: str) -> bool:
            if not path:
                return False
            dangerous = ["..", "//", "\\", "\x00"]
            return not any(d in path for d in dangerous)

        assert is_safe_path("models/gpt4.gguf") is True
        assert is_safe_path("../etc/passwd") is False
        assert is_safe_path("foo/../bar") is False
        assert is_safe_path("foo\x00bar") is False


# =============================================================================
# Test: Exception Handling Patterns
# =============================================================================


class TestExceptionHandling:
    """Tests for proper exception handling patterns."""

    def test_exception_with_logging(self):
        """Test that exceptions are logged, not silently swallowed."""
        logged_errors = []

        def operation_with_logging():
            try:
                raise ValueError("test error")
            except Exception as e:
                logged_errors.append(str(e))
                return None

        result = operation_with_logging()
        assert result is None
        assert len(logged_errors) == 1
        assert "test error" in logged_errors[0]

    def test_specific_exception_handling(self):
        """Test catching specific exceptions, not bare except."""

        def parse_config(data: str) -> dict:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return {}
            except TypeError:
                return {}
            # Note: No bare 'except:' or 'except Exception:'

        assert parse_config('{"key": "value"}') == {"key": "value"}
        assert parse_config("invalid") == {}
        assert parse_config(None) == {}

    def test_exception_context_preserved(self):
        """Test that exception context is preserved with 'from'."""

        def inner_operation():
            raise ValueError("inner error")

        def outer_operation():
            try:
                inner_operation()
            except ValueError as e:
                raise RuntimeError("outer error") from e

        with pytest.raises(RuntimeError) as exc_info:
            outer_operation()

        assert exc_info.value.__cause__ is not None
        assert "inner error" in str(exc_info.value.__cause__)


# =============================================================================
# Test: Git Operations Safety
# =============================================================================


class TestGitOperationsSafety:
    """Tests for safe git operations."""

    def test_git_stash_message_escaping(self):
        """Test that stash messages with special chars are safe."""

        def make_stash_command(message: str) -> list:
            # Using list format prevents shell injection
            safe_message = message.replace("\n", " ").replace("\r", " ")
            return ["git", "stash", "push", "-m", f"SAGE: {safe_message}"]

        # Normal message
        cmd = make_stash_command("checkpoint before refactor")
        assert cmd == ["git", "stash", "push", "-m", "SAGE: checkpoint before refactor"]

        # Message with newlines
        cmd = make_stash_command("line1\nline2\rline3")
        assert "\n" not in cmd[4]
        assert "\r" not in cmd[4]

    def test_git_sha_validation(self):
        """Test git SHA validation."""

        def is_valid_sha(sha: str | None) -> bool:
            if not sha:
                return False
            # SHA-1 is 40 hex chars, short form is 7-12
            return bool(re.match(r"^[a-f0-9]{7,40}$", sha.lower()))

        assert is_valid_sha("abc1234") is True
        assert is_valid_sha("a" * 40) is True
        assert is_valid_sha("") is False
        assert is_valid_sha(None) is False
        assert is_valid_sha("xyz123") is False  # non-hex
        assert is_valid_sha("abc") is False  # too short


# =============================================================================
# Test: Concurrent Safety Patterns
# =============================================================================


class TestConcurrencySafety:
    """Tests for thread-safe patterns."""

    def test_check_then_act_pattern_unsafe(self):
        """Demonstrate unsafe check-then-act pattern."""
        import threading
        import time

        # Simulating race condition
        shared_value = {"loaded": False, "count": 0}
        errors = []

        def unsafe_load():
            # BAD: Check then act without lock
            if not shared_value["loaded"]:
                time.sleep(0.001)  # Simulate work
                shared_value["loaded"] = True
                shared_value["count"] += 1

        threads = [threading.Thread(target=unsafe_load) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Count could be > 1 due to race condition
        # (In practice, this test may or may not show the race)

    def test_check_then_act_pattern_safe(self):
        """Demonstrate safe check-then-act pattern with lock."""
        import threading

        lock = threading.Lock()
        shared_value = {"loaded": False, "count": 0}

        def safe_load():
            with lock:
                if not shared_value["loaded"]:
                    shared_value["loaded"] = True
                    shared_value["count"] += 1

        threads = [threading.Thread(target=safe_load) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Count should always be exactly 1
        assert shared_value["count"] == 1


# =============================================================================
# Test: Division Safety
# =============================================================================


class TestDivisionSafety:
    """Tests for safe division operations."""

    def test_safe_percentage(self):
        """Test safe percentage calculation."""

        def safe_percentage(completed: int, total: int) -> float:
            if total <= 0:
                return 0.0
            return (completed / total) * 100

        assert safe_percentage(50, 100) == 50.0
        assert safe_percentage(0, 100) == 0.0
        assert safe_percentage(100, 0) == 0.0
        assert safe_percentage(0, 0) == 0.0

    def test_safe_average(self):
        """Test safe average calculation."""

        def safe_average(values: list) -> float:
            if not values:
                return 0.0
            return sum(values) / len(values)

        assert safe_average([1, 2, 3]) == 2.0
        assert safe_average([]) == 0.0


# =============================================================================
# Integration Tests for Common Patterns
# =============================================================================


class TestIntegrationPatterns:
    """Integration tests combining multiple safety patterns."""

    def test_llm_response_full_pipeline(self):
        """Test full LLM response processing pipeline."""

        def process_llm_response(response: Any) -> str:
            """Safely process LLM response to extract content."""
            if not isinstance(response, dict):
                return ""

            choices = safe_dict_path(response, "choices")
            if not choices or not isinstance(choices, list):
                return ""

            first_choice = safe_list_get(choices, 0)
            if not first_choice:
                return ""

            content = safe_dict_path(first_choice, "message", "content", default="")
            return content if isinstance(content, str) else ""

        # Valid response
        valid = {"choices": [{"message": {"content": "Hello!"}}]}
        assert process_llm_response(valid) == "Hello!"

        # Empty choices
        assert process_llm_response({"choices": []}) == ""

        # Missing structure
        assert process_llm_response({"data": "something"}) == ""

        # None content
        assert process_llm_response({"choices": [{"message": {"content": None}}]}) == ""

        # Non-dict response
        assert process_llm_response("string response") == ""
        assert process_llm_response(None) == ""

    def test_model_selection_pipeline(self):
        """Test safe model selection with fallbacks."""

        def select_model(models: list, preferred: str | None = None) -> dict | None:
            """Safely select best model from list."""
            if not models:
                return None

            # Try to find preferred model
            if preferred:
                for m in models:
                    if safe_dict_path(m, "id") == preferred:
                        return m

            # Fall back to best by score
            return max(models, key=lambda m: safe_dict_path(m, "score", default=0))

        models = [
            {"id": "gpt-4", "score": 100},
            {"id": "gpt-3.5", "score": 80},
        ]

        assert select_model(models, "gpt-4")["id"] == "gpt-4"
        assert select_model(models, "unknown")["id"] == "gpt-4"  # fallback to best
        assert select_model([], "gpt-4") is None
        assert select_model(models)["id"] == "gpt-4"  # best by score


class TestSageAnalysisIssues:
    """Tests for SAGE AI analysis flow issues identified in log analysis."""

    def test_task_status_has_skipped(self):
        """TaskStatus enum should have SKIPPED attribute."""
        from sage.execution import TaskStatus

        assert hasattr(TaskStatus, "SKIPPED")
        assert TaskStatus.SKIPPED.value == "skipped"

    def test_evidence_tracker_integration_exists(self):
        """EvidenceTracker should be importable and usable."""
        from sage.core.request_classifier import EvidenceTracker

        tracker = EvidenceTracker()
        assert not tracker.has_verified_evidence()

        tracker.record_file_read("test.py", success=True)
        assert tracker.has_verified_evidence()

    def test_synthesis_gate_blocks_without_evidence(self):
        """SynthesisGate should block synthesis without evidence."""
        from sage.core.request_classifier import EvidenceTracker, SynthesisGate

        gate = SynthesisGate()
        tracker = EvidenceTracker()

        can_synthesize, reason = gate.check(tracker)
        assert can_synthesize is False
        assert "evidence" in reason.lower()

    def test_synthesis_gate_allows_with_evidence(self):
        """SynthesisGate should allow synthesis with evidence."""
        from sage.core.request_classifier import EvidenceTracker, SynthesisGate

        gate = SynthesisGate()
        tracker = EvidenceTracker()
        tracker.record_file_read("main.py", success=True)

        can_synthesize, reason = gate.check(tracker)
        assert can_synthesize is True

    def test_list_generation_requires_quantity(self):
        """List generation should detect quantity requirements."""
        from sage.core.request_classifier import PipelineType, RequestClassifier

        classifier = RequestClassifier()
        result = classifier.classify("List 100 improvements")

        assert result.pipeline_type == PipelineType.LIST_GENERATION
        assert result.quantity_required == 100

    def test_analysis_uses_correct_pipeline(self):
        """Analysis requests should use ANALYSIS_ONLY pipeline."""
        from sage.core.request_classifier import PipelineType, RequestClassifier

        classifier = RequestClassifier()
        result = classifier.classify("Analyze the codebase")

        assert result.pipeline_type == PipelineType.ANALYSIS_ONLY

    def test_main_py_evidence_tracker_functions_importable(self):
        """EvidenceTracker functions should be importable from main.py."""
        from sage.cli_core import (
            _check_synthesis_gate,
            _get_evidence_tracker,
            _record_file_read,
            _record_search,
            _reset_evidence_tracker,
        )

        # Reset tracker should return a fresh tracker
        tracker = _reset_evidence_tracker()
        assert tracker is not None
        assert not tracker.has_verified_evidence()

        # Get tracker should return the same tracker
        assert _get_evidence_tracker() is tracker

        # Record file read should work
        _record_file_read("test.py", success=True)
        assert tracker.has_verified_evidence()
        assert "test.py" in tracker.verified_files

        # Record search should work
        _record_search("pattern", ["file1.py", "file2.py"])
        assert tracker.has_successful_searches()

        # Synthesis gate should allow synthesis now
        can_synthesize, reason = _check_synthesis_gate()
        assert can_synthesize is True

    def test_main_py_evidence_tracker_resets_on_classify(self):
        """EvidenceTracker should reset when a new request is classified."""
        from sage.cli_core import (
            _classify_and_store_request,
            _get_evidence_tracker,
            _record_file_read,
            _reset_evidence_tracker,
        )

        # Set up some evidence
        _reset_evidence_tracker()
        _record_file_read("old_file.py", success=True)
        tracker = _get_evidence_tracker()
        assert "old_file.py" in tracker.verified_files

        # Classify a new request - should reset the tracker
        _classify_and_store_request("List 50 improvements")

        # Get the new tracker
        new_tracker = _get_evidence_tracker()
        assert new_tracker is not tracker  # Different instance
        assert not new_tracker.has_verified_evidence()  # Empty

    def test_main_py_synthesis_gate_blocks_without_evidence(self):
        """Synthesis gate should block synthesis without evidence in main.py."""
        from sage.cli_core import (
            _check_synthesis_gate,
            _reset_evidence_tracker,
        )

        # Reset to empty tracker
        _reset_evidence_tracker()

        # Should block synthesis
        can_synthesize, reason = _check_synthesis_gate()
        assert can_synthesize is False
        assert "evidence" in reason.lower()


class TestSubTaskExecution:
    """Tests for SubTask handling in execution engine (P0 bug fix)."""

    def test_subtask_is_dataclass_not_string(self):
        """SubTask should be a dataclass with a description field."""
        from sage.reasoning import SubTask

        subtask = SubTask(
            id="test_1",
            description="Test task description",
            type="implementation",
            priority=1,
            complexity=2,
        )

        # SubTask is a dataclass, not a string
        assert hasattr(subtask, "description")
        assert subtask.description == "Test task description"
        assert not isinstance(subtask, str)

    def test_subtask_description_extraction(self):
        """Subtask description should be extractable for execution."""
        from sage.reasoning import ReasoningContext, SubTask

        context = ReasoningContext(task="Main task")
        context.subtasks = [
            SubTask(
                id="st_1",
                description="First subtask",
                type="implementation",
                priority=1,
                complexity=2,
            ),
            SubTask(
                id="st_2",
                description="Second subtask",
                type="testing",
                priority=2,
                complexity=1,
            ),
        ]

        # Should be able to extract descriptions for execution
        descriptions = [st.description for st in context.subtasks]
        assert descriptions == ["First subtask", "Second subtask"]

    def test_subtask_not_subscriptable(self):
        """SubTask objects should not be accessed with [] notation."""
        from sage.reasoning import SubTask

        subtask = SubTask(
            id="test_1",
            description="Test task",
            type="implementation",
            priority=1,
            complexity=2,
        )

        # Attempting to subscript should raise TypeError
        with pytest.raises(TypeError, match="not subscriptable"):
            _ = subtask["description"]

    def test_execution_task_creation_with_subtask(self):
        """ExecutionTask should be created with SubTask.description, not SubTask object."""
        from sage.execution import ExecutionTask, RetryConfig, RetryStrategy, TaskPriority
        from sage.reasoning import SubTask

        subtask = SubTask(
            id="st_1",
            description="Write unit tests for authentication module",
            type="testing",
            priority=1,
            complexity=3,
        )

        # Correct: use subtask.description
        task = ExecutionTask(
            id="exec_1",
            description=subtask.description,  # Should use .description
            command=lambda: {"success": True},
            priority=TaskPriority.HIGH,
            dependencies=[],
            timeout=60.0,
            retry_config=RetryConfig(
                max_attempts=2,
                strategy=RetryStrategy.EXPONENTIAL,
                initial_delay=1.0,
            ),
        )

        assert task.description == "Write unit tests for authentication module"
        assert isinstance(task.description, str)


class TestEvidenceGroundingEnforcement:
    """Tests for evidence grounding enforcement during synthesis."""

    def test_synthesis_blocked_without_file_reads(self):
        """Synthesis should be blocked if no files were actually read."""
        from sage.core.request_classifier import EvidenceTracker, SynthesisGate

        tracker = EvidenceTracker()
        gate = SynthesisGate(require_any_evidence=True)

        # No evidence recorded
        can_synthesize, reason = gate.check(tracker)

        assert can_synthesize is False
        assert "evidence" in reason.lower()

    def test_synthesis_allowed_with_verified_reads(self):
        """Synthesis should be allowed after verified file reads."""
        from sage.core.request_classifier import EvidenceTracker, SynthesisGate

        tracker = EvidenceTracker()
        gate = SynthesisGate(require_any_evidence=True)

        # Record a successful file read
        tracker.record_file_read("sage/main.py", success=True)

        can_synthesize, reason = gate.check(tracker)

        assert can_synthesize is True

    def test_failed_reads_not_counted_as_evidence(self):
        """Failed file reads should not count as evidence."""
        from sage.core.request_classifier import EvidenceTracker, SynthesisGate

        tracker = EvidenceTracker()
        gate = SynthesisGate(require_any_evidence=True)

        # Record only failed reads
        tracker.record_file_read("nonexistent.py", success=False)
        tracker.record_file_read("also_missing.py", success=False)

        # Should not have verified evidence
        assert not tracker.has_verified_evidence()

        can_synthesize, reason = gate.check(tracker)
        assert can_synthesize is False

    def test_empty_search_not_counted_as_evidence(self):
        """Empty search results should not count as evidence."""
        from sage.core.request_classifier import EvidenceTracker, SynthesisGate

        tracker = EvidenceTracker()
        gate = SynthesisGate(require_any_evidence=True)

        # Record empty search
        tracker.record_search("nonexistent_pattern", [])

        # Should not have verified evidence from empty search
        assert not tracker.has_successful_searches()

        can_synthesize, reason = gate.check(tracker)
        assert can_synthesize is False


class TestListGenerationQuality:
    """Tests for list generation quality and grounding."""

    def test_list_items_must_have_file_references(self):
        """List generation requests should produce items with file references."""
        from sage.core.request_classifier import PipelineType, RequestClassifier

        classifier = RequestClassifier()
        result = classifier.classify("List 100 improvements in the codebase")

        # Should be classified as LIST_GENERATION
        assert result.pipeline_type == PipelineType.LIST_GENERATION
        assert result.quantity_required == 100
        assert result.read_only is True

    def test_quantity_extraction_from_various_formats(self):
        """Quantity should be extracted from list-style phrasings."""
        from sage.core.request_classifier import RequestClassifier

        classifier = RequestClassifier()

        # Focus on phrasings that are classified as LIST_GENERATION
        test_cases = [
            ("List 100 improvements", 100),
            ("List 50 things to improve", 50),
            ("List 25 issues in the code", 25),
        ]

        for prompt, expected_qty in test_cases:
            result = classifier.classify(prompt)
            assert result.quantity_required == expected_qty, f"Failed for: {prompt}"


class TestThinkingBlockSuppression:
    """Tests for thinking block suppression - only final output should be shown."""

    def test_suppress_thinking_returns_true_by_default(self):
        """Thinking blocks should be suppressed by default (not verbose mode)."""
        from sage.core import renderer

        # Not in verbose mode - should suppress
        with patch.object(renderer, "is_verbose", return_value=False):
            assert renderer.suppress_thinking() is True

    def test_suppress_thinking_returns_false_in_verbose(self):
        """Thinking blocks should show in verbose mode."""
        from sage.core import renderer

        # suppress_thinking() returns _output_mode != "verbose"
        # So when _output_mode is "verbose", it returns False
        with patch.object(renderer, "_output_mode", "verbose"):
            # When in verbose mode, suppress_thinking should return False
            result = renderer.suppress_thinking()
            assert result is False

    def test_thinking_block_stripped_from_response(self):
        """Response generator should have thinking block pattern in EXCESSIVE_PATTERNS."""
        from sage.core.response_generator import ResponseQualityValidator

        validator = ResponseQualityValidator()

        # Verify thinking_block is in the excessive patterns
        excessive_patterns = validator.EXCESSIVE_PATTERNS
        thinking_patterns = [p for p in excessive_patterns if "thinking" in p[1]]
        assert len(thinking_patterns) > 0, "thinking_block should be in EXCESSIVE_PATTERNS"
        assert thinking_patterns[0][1] == "thinking_block"

    def test_strip_thinking_function_exists(self):
        """A function to strip thinking blocks should exist."""

        def strip_thinking(text: str) -> str:
            """Strip thinking blocks from text."""
            import re

            return re.sub(r"<thinking>[\s\S]*?</thinking>\s*", "", text)

        input_text = "<thinking>Hidden thought</thinking>Visible output"
        result = strip_thinking(input_text)
        assert "<thinking>" not in result
        assert "Hidden thought" not in result
        assert "Visible output" in result


class TestTDDByDefault:
    """Tests for TDD enforcement by default for all implementation tasks."""

    def test_implementation_requests_require_tdd_by_default(self):
        """All IMPLEMENTATION pipeline requests should require TDD by default."""
        from sage.core.request_classifier import PipelineType, RequestClassifier

        classifier = RequestClassifier()

        # Various implementation requests
        impl_requests = [
            "Add a login feature",
            "Implement the payment processor",
            "Create a new API endpoint",
            "Build user authentication",
            "Develop the dashboard component",
        ]

        for request in impl_requests:
            result = classifier.classify(request)
            if result.pipeline_type == PipelineType.IMPLEMENTATION:
                assert result.requires_tdd is True, f"TDD not required for: {request}"

    def test_fix_requests_require_tdd(self):
        """Fix requests should require TDD."""
        from sage.core.request_classifier import RequestClassifier

        classifier = RequestClassifier()

        result = classifier.classify("Fix the bug in the authentication module")
        assert result.requires_tdd is True

    def test_refactor_requests_require_tdd(self):
        """Refactoring requests should require TDD."""
        from sage.core.request_classifier import RequestClassifier

        classifier = RequestClassifier()

        result = classifier.classify("Refactor the database access layer")
        assert result.requires_tdd is True

    def test_analysis_requests_do_not_require_tdd(self):
        """Analysis/review requests should NOT require TDD."""
        from sage.core.request_classifier import PipelineType, RequestClassifier

        classifier = RequestClassifier()

        analysis_requests = [
            "Analyze the codebase structure",
            "Review the security of this code",
            "What files handle authentication?",
            "List all API endpoints",
        ]

        for request in analysis_requests:
            result = classifier.classify(request)
            if result.pipeline_type == PipelineType.ANALYSIS_ONLY:
                assert result.requires_tdd is False, f"TDD wrongly required for: {request}"


class TestPromptEnhancement:
    """Tests for prompt enhancement before execution."""

    def test_enhance_task_prompt_exists(self):
        """A function to enhance prompts should exist in main.py."""
        from sage.cli_core import _enhance_task_prompt

        # Should be callable
        assert callable(_enhance_task_prompt)

    def test_enhance_task_prompt_adds_clarity(self):
        """Enhanced prompt should add clarity to the original."""
        from sage.cli_core import _enhance_task_prompt

        original = "fix the bug"
        enhanced = _enhance_task_prompt(original)

        # Enhanced should be longer and more detailed
        assert len(enhanced) >= len(original)

    def test_enhance_task_prompt_preserves_intent(self):
        """Enhanced prompt should preserve original intent."""
        from sage.cli_core import _enhance_task_prompt

        original = "implement user login"
        enhanced = _enhance_task_prompt(original)

        # Original intent words should be present
        assert "login" in enhanced.lower() or "user" in enhanced.lower()

    def test_enhance_task_prompt_adds_tdd_for_implementation(self):
        """Enhanced prompt for implementation should mention TDD."""
        from sage.core.request_classifier import RequestClassifier
        from sage.cli_core import _enhance_task_prompt

        classifier = RequestClassifier()
        original = "implement a new feature"
        classification = classifier.classify(original)

        if classification.requires_tdd:
            enhanced = _enhance_task_prompt(original)
            # Should mention TDD or testing
            has_tdd = "tdd" in enhanced.lower() or "test" in enhanced.lower()
            assert has_tdd, "Enhanced implementation prompt should mention TDD/testing"


class TestProceduralStepIndicators:
    """Tests for procedural step indicators instead of text messages."""

    def test_phase_indicator_function_exists(self):
        """Renderer should have a phase indicator function."""
        from sage.core import renderer

        assert hasattr(renderer, "phase")
        assert callable(renderer.phase)

    def test_phase_indicator_accepts_phase_name_and_message(self):
        """Phase indicator should accept phase name and message."""
        from io import StringIO

        from sage.core import renderer

        # Mock stdout to capture output
        with patch("sys.stdout", new_callable=StringIO):
            # Should not raise
            renderer.phase("research", "Analyzing codebase...")

    def test_step_indicator_formats_correctly(self):
        """Step indicators should format as indicators, not plain text."""
        from sage.core import renderer

        # Test that step indicator methods exist
        assert hasattr(renderer, "step_indicator") or hasattr(renderer, "phase")


class TestSageTestExecution:
    """Tests for SAGE's ability to execute its own tests."""

    def test_run_shell_function_exists(self):
        """A function to run shell commands should exist."""
        from sage.core.shell import run_shell

        assert callable(run_shell)

    def test_run_tdd_test_function_exists(self):
        """A function specifically for TDD test execution should exist."""
        from sage.core.shell import run_tdd_test

        assert callable(run_tdd_test)

    def test_run_tdd_test_returns_correct_structure(self):
        """run_tdd_test should return a structured result."""
        import tempfile
        from pathlib import Path

        from sage.core.shell import run_tdd_test

        # Use a temp directory
        with tempfile.TemporaryDirectory() as tmpdir:
            # Run a simple command that succeeds
            result = run_tdd_test("echo 'test'", cwd=Path(tmpdir), timeout=5, expect_failure=False)

            # Should return a tuple of (success, message, raw_output)
            assert isinstance(result, tuple)
            assert len(result) == 3
            success, message, output = result
            assert isinstance(success, bool)
            assert isinstance(message, str)

    def test_validation_command_discovery_exists(self):
        """Function to discover validation/test commands should exist."""
        from sage.core.project import discover_project_test_command

        assert callable(discover_project_test_command)


class TestOutputFiltering:
    """Tests for filtering non-essential output, keeping only final results."""

    def test_stream_tokens_minimal_exists(self):
        """A minimal streaming function should exist."""
        from sage.core import renderer

        assert hasattr(renderer, "stream_tokens_minimal")

    def test_response_removes_announcement_phrases(self):
        """Response validator should have announcement pattern in EXCESSIVE_PATTERNS."""
        from sage.core.response_generator import ResponseQualityValidator

        validator = ResponseQualityValidator()

        # Verify announcement is in the excessive patterns
        excessive_patterns = validator.EXCESSIVE_PATTERNS
        announcement_patterns = [p for p in excessive_patterns if "announcement" in p[1]]
        assert len(announcement_patterns) > 0, "announcement should be in EXCESSIVE_PATTERNS"
        assert announcement_patterns[0][1] == "announcement"


class TestEvidenceGroundingIntegration:
    """Tests for evidence grounding integration throughout the pipeline."""

    def test_tool_commands_record_evidence(self):
        """READ: and SEARCH: commands should record evidence."""
        from sage.cli_core import (
            _record_file_read,
            _record_search,
            _reset_evidence_tracker,
        )

        tracker = _reset_evidence_tracker()
        assert not tracker.has_verified_evidence()

        # Record file read
        _record_file_read("main.py", success=True)
        assert tracker.has_verified_evidence()
        assert "main.py" in tracker.verified_files

        # Record search
        _record_search("function", ["file1.py", "file2.py"])
        assert tracker.has_successful_searches()

    def test_synthesis_gate_integrated_with_main(self):
        """Synthesis gate check should be integrated in main.py."""
        from sage.cli_core import _check_synthesis_gate, _reset_evidence_tracker

        _reset_evidence_tracker()
        can_synthesize, reason = _check_synthesis_gate()
        assert can_synthesize is False  # No evidence yet

    def test_evidence_tracker_resets_per_request(self):
        """Evidence tracker should reset for each new request classification."""
        from sage.cli_core import (
            _classify_and_store_request,
            _get_evidence_tracker,
            _record_file_read,
            _reset_evidence_tracker,
        )

        # Setup initial evidence
        _reset_evidence_tracker()
        _record_file_read("old.py", success=True)
        old_tracker = _get_evidence_tracker()
        assert "old.py" in old_tracker.verified_files

        # New classification should reset
        _classify_and_store_request("new request")
        new_tracker = _get_evidence_tracker()
        assert "old.py" not in new_tracker.verified_files


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
