"""Tests for orchestration robustness - P0 fixes for SAGE AI.

Tests verify:
- Nested AI response fields are handled safely (items 1-5)
- Orchestration failures are handled gracefully with structured details
- Fallback paths work correctly
"""

from unittest.mock import MagicMock

from sage.core.ai_orchestration import (
    AIComplexityAssessor,
    AIDecompositionEngine,
    AIPlanGenerator,
    AIPlanRefiner,
    OrchestrationError,
    OrchestrationFailure,
    _ensure_dict,
    _safe_nested_get,
)


class TestSafeNestedGet:
    """Test _safe_nested_get handles all edge cases."""

    def test_returns_value_from_dict(self):
        """Should return value when parent is a dict with the key."""
        data = {"plan": {"steps": [1, 2, 3]}}
        result = _safe_nested_get(data, "plan", default={})
        assert result == {"steps": [1, 2, 3]}

    def test_returns_default_when_key_missing(self):
        """Should return default when key doesn't exist."""
        data = {"other": "value"}
        result = _safe_nested_get(data, "plan", default={"steps": []})
        assert result == {"steps": []}

    def test_handles_list_as_parent(self):
        """Should return default when parent is a list, not a dict."""
        data = ["item1", "item2"]
        result = _safe_nested_get(data, "plan", default={})
        assert result == {}

    def test_handles_string_as_parent(self):
        """Should return default when parent is a string."""
        data = "raw text response"
        result = _safe_nested_get(data, "plan", default={})
        assert result == {}

    def test_handles_none_as_parent(self):
        """Should return default when parent is None."""
        result = _safe_nested_get(None, "plan", default={})
        assert result == {}

    def test_handles_nested_path(self):
        """Should traverse nested paths safely."""
        data = {"response": {"plan": {"steps": [1, 2]}}}
        result = _safe_nested_get(data, "response.plan.steps", default=[])
        assert result == [1, 2]

    def test_handles_missing_intermediate_key(self):
        """Should return default when intermediate key is missing."""
        data = {"response": {}}
        result = _safe_nested_get(data, "response.plan.steps", default=[])
        assert result == []

    def test_normalizes_list_to_dict_with_items(self):
        """Should normalize list values to dict when expecting dict."""
        data = {"plan": ["step1", "step2"]}
        result = _safe_nested_get(data, "plan", default={}, normalize_list=True)
        assert isinstance(result, dict)
        assert "items" in result or "steps" in result

    def test_preserves_list_when_expected(self):
        """Should preserve list values when list is expected."""
        data = {"steps": ["step1", "step2"]}
        result = _safe_nested_get(data, "steps", default=[], expect_list=True)
        assert result == ["step1", "step2"]


class TestEnsureDictEnhancements:
    """Test _ensure_dict handles all AI response variants."""

    def test_handles_dict_response(self):
        """Should return dict unchanged."""
        response = {"key": "value"}
        assert _ensure_dict(response) == {"key": "value"}

    def test_handles_list_response(self):
        """Should wrap list in dict."""
        response = ["item1", "item2"]
        result = _ensure_dict(response)
        assert isinstance(result, dict)
        assert "items" in result or "subtasks" in result

    def test_handles_string_json_response(self):
        """Should parse JSON string."""
        response = '{"key": "value"}'
        result = _ensure_dict(response)
        assert result == {"key": "value"}

    def test_handles_string_non_json_response(self):
        """Should wrap non-JSON string."""
        response = "plain text response"
        result = _ensure_dict(response)
        assert "raw_text" in result

    def test_handles_none_response(self):
        """Should return empty dict for None."""
        assert _ensure_dict(None) == {}

    def test_handles_nested_list_in_json_string(self):
        """Should handle JSON array string."""
        response = '["item1", "item2"]'
        result = _ensure_dict(response)
        assert isinstance(result, dict)


class TestOrchestrationFailureHandling:
    """Test orchestration errors are structured and actionable."""

    def test_orchestration_error_has_phase(self):
        """OrchestrationError should include phase information."""
        error = OrchestrationError(
            phase="planning", message="Failed to parse plan", raw_type="list", expected_type="dict"
        )
        assert error.phase == "planning"
        assert "parse" in error.message.lower()

    def test_orchestration_error_has_raw_type(self):
        """OrchestrationError should include the type that was received."""
        error = OrchestrationError(
            phase="decomposition",
            message="Unexpected response type",
            raw_type="str",
            expected_type="dict",
        )
        assert error.raw_type == "str"
        assert error.expected_type == "dict"

    def test_orchestration_failure_is_structured(self):
        """OrchestrationFailure should be a structured result, not exception."""
        failure = OrchestrationFailure(
            phase="complexity",
            error="Model returned invalid JSON",
            fallback_used=True,
            fallback_result={"level": "medium", "score": 5},
        )
        assert failure.phase == "complexity"
        assert failure.fallback_used is True
        assert failure.fallback_result["level"] == "medium"


class TestDecompositionEngineRobustness:
    """Test AIDecompositionEngine handles malformed responses."""

    def test_handles_list_response(self):
        """Should handle when AI returns a list instead of dict."""
        mock_send = MagicMock(return_value=["task1", "task2", "task3"])
        engine = AIDecompositionEngine(mock_send)

        result = engine.decompose("Build a web app")

        assert result.success is True
        assert len(result.subtasks) >= 1

    def test_handles_string_response(self):
        """Should handle when AI returns raw text."""
        mock_send = MagicMock(return_value="Step 1: Do this\nStep 2: Do that")
        engine = AIDecompositionEngine(mock_send)

        result = engine.decompose("Build a web app")

        assert result.success is True
        # Should have at least the original task as fallback
        assert len(result.subtasks) >= 1

    def test_handles_nested_list_in_subtasks(self):
        """Should flatten nested lists in subtasks."""
        mock_send = MagicMock(return_value={"subtasks": [["nested", "list"], "normal"]})
        engine = AIDecompositionEngine(mock_send)

        result = engine.decompose("Build a web app")

        assert result.success is True
        # Should handle or flatten nested lists
        assert all(isinstance(t, str) for t in result.subtasks)

    def test_handles_none_response(self):
        """Should handle None response gracefully."""
        mock_send = MagicMock(return_value=None)
        engine = AIDecompositionEngine(mock_send)

        result = engine.decompose("Build a web app")

        assert result.success is True  # Graceful degradation
        assert result.subtasks == ["Build a web app"]  # Falls back to original task


class TestComplexityAssessorRobustness:
    """Test AIComplexityAssessor handles malformed responses."""

    def test_handles_dict_with_wrong_keys(self):
        """Should use defaults when expected keys are missing."""
        mock_send = MagicMock(return_value={"wrong": "keys"})
        assessor = AIComplexityAssessor(mock_send)

        result = assessor.assess("Complex task")

        assert result.level in ("low", "medium", "high")
        assert 1 <= result.score <= 10

    def test_handles_complexity_as_list(self):
        """Should handle when complexity field is a list."""
        mock_send = MagicMock(return_value={"complexity": ["factor1", "factor2"], "score": 8})
        assessor = AIComplexityAssessor(mock_send)

        result = assessor.assess("Task")

        # Should not crash, should use defaults
        assert result.level in ("low", "medium", "high")

    def test_handles_score_as_string(self):
        """Should handle when score is a string instead of int."""
        mock_send = MagicMock(return_value={"complexity": "high", "score": "8"})
        assessor = AIComplexityAssessor(mock_send)

        result = assessor.assess("Task")

        assert isinstance(result.score, int)


class TestPlanGeneratorRobustness:
    """Test AIPlanGenerator handles malformed responses."""

    def test_handles_plan_as_list(self):
        """Should handle when plan field is a list instead of dict."""
        mock_send = MagicMock(return_value={"plan": ["step1", "step2", "step3"]})
        generator = AIPlanGenerator(mock_send)

        result = generator.generate("Create a feature")

        assert result.success is True
        assert isinstance(result.steps, list)

    def test_handles_steps_in_wrong_location(self):
        """Should find steps even when not nested under plan."""
        mock_send = MagicMock(return_value={"steps": [{"step": 1, "action": "Do thing"}]})
        generator = AIPlanGenerator(mock_send)

        result = generator.generate("Create a feature")

        assert len(result.steps) >= 1

    def test_handles_empty_plan(self):
        """Should handle empty plan gracefully."""
        mock_send = MagicMock(return_value={"plan": {}})
        generator = AIPlanGenerator(mock_send)

        result = generator.generate("Task")

        assert result.success is True
        assert result.steps == []


class TestPlanRefinerRobustness:
    """Test AIPlanRefiner handles malformed responses."""

    def test_handles_refined_plan_as_list(self):
        """Should handle when refined_plan is a list."""
        mock_send = MagicMock(return_value={"refined_plan": ["step1", "step2"]})
        refiner = AIPlanRefiner(mock_send)

        result = refiner.refine({"steps": []}, {"feedback": "add more"})

        assert result.success is True


class TestFailClosedBehavior:
    """Test that orchestration fails closed on parse errors."""

    def test_decomposition_records_parse_failure(self):
        """Should record structured failure when parsing fails."""

        def bad_send(prompt):
            raise ValueError("Model error")

        engine = AIDecompositionEngine(bad_send)
        result = engine.decompose("Task")

        # Should not raise, but should record failure
        assert result.success is False or result.error is not None

    def test_complexity_records_parse_failure(self):
        """Should record structured failure for complexity parse errors."""

        def bad_send(prompt):
            return {"invalid": object()}  # Non-serializable

        assessor = AIComplexityAssessor(bad_send)
        result = assessor.assess("Task")

        # Should use safe defaults, not crash
        assert result.level in ("low", "medium", "high")


class TestDeterministicFallback:
    """Test deterministic fallback paths when AI orchestration fails."""

    def test_decomposition_fallback_uses_original_task(self):
        """Fallback should use original task as single subtask."""
        mock_send = MagicMock(return_value=None)
        engine = AIDecompositionEngine(mock_send)

        result = engine.decompose("Build web app")

        assert result.subtasks == ["Build web app"]
        assert result.granularity == "medium"

    def test_complexity_fallback_uses_medium(self):
        """Fallback should use medium complexity as safe default."""
        mock_send = MagicMock(return_value=None)
        assessor = AIComplexityAssessor(mock_send)

        result = assessor.assess("Task")

        assert result.level == "medium"
        assert result.score == 5

    def test_plan_fallback_returns_empty_steps(self):
        """Fallback should return empty steps list."""
        mock_send = MagicMock(return_value=None)
        generator = AIPlanGenerator(mock_send)

        result = generator.generate("Task")

        assert result.steps == []
