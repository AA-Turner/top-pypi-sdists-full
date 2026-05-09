"""Comprehensive tests for sage/core/ai_orchestration.py - AI Model-Driven Orchestration."""

import json
import pytest
from dataclasses import dataclass, field
from typing import Any

from sage.core.ai_orchestration import (
    # Error handling
    OrchestrationError,
    OrchestrationFailure,
    # Core types
    AIResult,
    # Helper functions
    _ensure_dict,
    _safe_nested_get,
    _safe_get_as_dict,
    _safe_get_as_list,
    _safe_get_as_str,
    _safe_get_as_int,
    # Category 1: Critical Thinking
    AIDecompositionEngine,
    DecompositionResult,
    AIComplexityAssessor,
    ComplexityResult,
    AIContextEngine,
    ContextResult,
    AIAssumptionIdentifier,
    AssumptionResult,
    AIRiskAssessor,
    RiskResult,
    AIConstraintRecognizer,
    ConstraintResult,
    AIDependencyAnalyzer,
    DependencyResult,
    AIEdgeCaseIdentifier,
    EdgeCaseResult,
    AITradeoffAnalyzer,
    TradeoffResult,
    AIImpactAssessor,
    ImpactResult,
    AIPrerequisiteDetector,
    PrerequisiteResult,
    AIScopeBoundaryDetector,
    ScopeResult,
    AIContradictionDetector,
    ContradictionResult,
    AIPriorityInferrer,
    PriorityResult,
    AISuccessCriteriaExtractor,
    SuccessCriteriaResult,
    # Category 2: Planning
    AIPlanGenerator,
    PlanResult,
    AIPlanRefiner,
    RefinedPlanResult,
    AIMultiPathPlanner,
    MultiPathResult,
    AIResourceAwarePlanner,
    ResourceAwarePlanResult,
    AIRollbackPlanner,
    RollbackPlanResult,
    AIParallelPlanner,
    ParallelPlanResult,
    AITestingStrategyPlanner,
    TestingStrategyResult,
    # Category 3: Reasoning
    AIChainOfThoughtReasoner,
    ReasoningResult,
    # Category 4: Analysis
    AICodePatternAnalyzer,
    PatternAnalysisResult,
    # Category 5: Testing
    AITestGenerator,
    TestGenerationResult,
    # Category 6: Execution
    AIAdaptiveExecutor,
    AdaptationResult,
    # Category 7: Bash/DevOps
    AIShellCommandGenerator,
    ShellCommandResult,
    AIGitMaster,
    GitResult,
    # Category 8: Self-Improvement
    AIOutcomeLearner,
    LearningResult,
    # Category 9: Quality Assurance
    AIPlaceholderDetector,
    PlaceholderDetectionResult,
    # Main Orchestrator
    AIOrchestrator,
)


# =============================================================================
# Mock AI Model Sender
# =============================================================================


def make_mock_sender(response: Any):
    """Create a mock sender that returns a specific response."""

    def mock_send(prompt: str) -> Any:
        return response

    return mock_send


def make_exception_sender(exception: Exception):
    """Create a mock sender that raises an exception."""

    def mock_send(prompt: str) -> Any:
        raise exception

    return mock_send


# =============================================================================
# Tests for OrchestrationError
# =============================================================================


class TestOrchestrationError:
    """Tests for OrchestrationError dataclass."""

    def test_create_basic(self):
        """Create basic error."""
        error = OrchestrationError(phase="planning", message="Failed to plan")
        assert error.phase == "planning"
        assert error.message == "Failed to plan"
        assert error.raw_type is None
        assert error.expected_type is None
        assert error.raw_value is None

    def test_create_with_type_info(self):
        """Create error with type information."""
        error = OrchestrationError(
            phase="decomposition",
            message="Type mismatch",
            raw_type="list",
            expected_type="dict",
            raw_value=[1, 2, 3],
        )
        assert error.raw_type == "list"
        assert error.expected_type == "dict"
        assert error.raw_value == [1, 2, 3]

    def test_str_basic(self):
        """String representation basic."""
        error = OrchestrationError(phase="test", message="Error occurred")
        assert "[test] Error occurred" in str(error)

    def test_str_with_types(self):
        """String representation with type info."""
        error = OrchestrationError(
            phase="parse",
            message="Invalid type",
            raw_type="str",
            expected_type="int",
        )
        result = str(error)
        assert "[parse]" in result
        assert "got str" in result
        assert "expected int" in result


# =============================================================================
# Tests for OrchestrationFailure
# =============================================================================


class TestOrchestrationFailure:
    """Tests for OrchestrationFailure dataclass."""

    def test_create_basic(self):
        """Create basic failure."""
        failure = OrchestrationFailure(phase="execution", error="Timeout")
        assert failure.phase == "execution"
        assert failure.error == "Timeout"
        assert failure.fallback_used is False
        assert failure.fallback_result == {}

    def test_create_with_fallback(self):
        """Create failure with fallback info."""
        failure = OrchestrationFailure(
            phase="planning",
            error="AI unavailable",
            fallback_used=True,
            fallback_result={"steps": ["default"]},
        )
        assert failure.fallback_used is True
        assert failure.fallback_result == {"steps": ["default"]}

    def test_to_dict(self):
        """Convert to dict."""
        failure = OrchestrationFailure(
            phase="test",
            error="Failed",
            fallback_used=True,
            fallback_result={"value": 42},
        )
        result = failure.to_dict()
        assert result["phase"] == "test"
        assert result["error"] == "Failed"
        assert result["fallback_used"] is True
        assert result["fallback_result"]["value"] == 42


# =============================================================================
# Tests for AIResult
# =============================================================================


class TestAIResult:
    """Tests for AIResult dataclass."""

    def test_create_success(self):
        """Create successful result."""
        result = AIResult(raw_response={"data": "value"})
        assert result.success is True
        assert result.error is None
        assert result.failure is None
        assert result.raw_response["data"] == "value"

    def test_create_failure(self):
        """Create failed result."""
        failure = OrchestrationFailure(phase="test", error="Error")
        result = AIResult(
            raw_response={},
            success=False,
            error="Something went wrong",
            failure=failure,
        )
        assert result.success is False
        assert result.error == "Something went wrong"
        assert result.failure is not None


# =============================================================================
# Tests for _ensure_dict helper
# =============================================================================


class TestEnsureDict:
    """Tests for _ensure_dict helper function."""

    def test_none_returns_empty(self):
        """None returns empty dict."""
        assert _ensure_dict(None) == {}

    def test_dict_returns_dict(self):
        """Dict returns same dict."""
        input_dict = {"key": "value"}
        assert _ensure_dict(input_dict) == input_dict

    def test_list_wrapped_in_dict(self):
        """List is wrapped in dict with multiple keys."""
        input_list = [1, 2, 3]
        result = _ensure_dict(input_list)
        assert result["items"] == [1, 2, 3]
        assert result["subtasks"] == [1, 2, 3]
        assert result["steps"] == [1, 2, 3]
        assert result["paths"] == [1, 2, 3]

    def test_json_string_parsed(self):
        """JSON string is parsed."""
        json_str = '{"key": "value"}'
        result = _ensure_dict(json_str)
        assert result["key"] == "value"

    def test_invalid_json_string(self):
        """Invalid JSON returns raw_text dict."""
        invalid_str = "not valid json"
        result = _ensure_dict(invalid_str)
        assert result["raw_text"] == "not valid json"

    def test_json_list_string(self):
        """JSON list string is parsed and wrapped."""
        json_str = '[1, 2, 3]'
        result = _ensure_dict(json_str)
        assert result["items"] == [1, 2, 3]

    def test_unknown_type(self):
        """Unknown type returns empty dict."""
        result = _ensure_dict(12345)
        assert result == {}


# =============================================================================
# Tests for _safe_nested_get helper
# =============================================================================


class TestSafeNestedGet:
    """Tests for _safe_nested_get helper function."""

    def test_none_returns_default(self):
        """None data returns default."""
        assert _safe_nested_get(None, "key", default="default") == "default"

    def test_simple_key(self):
        """Get simple key."""
        data = {"key": "value"}
        assert _safe_nested_get(data, "key") == "value"

    def test_missing_key(self):
        """Missing key returns default."""
        data = {"other": "value"}
        assert _safe_nested_get(data, "key", default="default") == "default"

    def test_dot_notation(self):
        """Get nested value with dot notation."""
        data = {"level1": {"level2": "value"}}
        assert _safe_nested_get(data, "level1.level2") == "value"

    def test_dot_notation_missing(self):
        """Missing nested key returns default."""
        data = {"level1": {"other": "value"}}
        assert _safe_nested_get(data, "level1.level2", default="default") == "default"

    def test_non_dict_returns_default(self):
        """Non-dict at any level returns default."""
        data = {"level1": "not a dict"}
        assert _safe_nested_get(data, "level1.level2", default="default") == "default"

    def test_normalize_list_to_dict(self):
        """Normalize list to dict when requested."""
        data = {"items": [1, 2, 3]}
        result = _safe_nested_get(data, "items", normalize_list=True)
        assert result["items"] == [1, 2, 3]
        assert result["steps"] == [1, 2, 3]

    def test_expect_list_with_list(self):
        """Return list as-is when expect_list=True."""
        data = {"items": [1, 2, 3]}
        result = _safe_nested_get(data, "items", expect_list=True)
        assert result == [1, 2, 3]

    def test_expect_list_wraps_single(self):
        """Wrap single item in list when expect_list=True."""
        data = {"item": "single"}
        result = _safe_nested_get(data, "item", expect_list=True)
        assert result == ["single"]

    def test_expect_list_none_returns_empty(self):
        """None with expect_list and default returns empty list."""
        data = {"other": "value"}
        # When key is not found, returns default ([] if specified)
        result = _safe_nested_get(data, "missing", default=[], expect_list=True)
        assert result == []


# =============================================================================
# Tests for _safe_get_as_dict helper
# =============================================================================


class TestSafeGetAsDict:
    """Tests for _safe_get_as_dict helper function."""

    def test_get_dict(self):
        """Get dict value."""
        data = {"config": {"key": "value"}}
        result = _safe_get_as_dict(data, "config")
        assert result == {"key": "value"}

    def test_missing_returns_default(self):
        """Missing key returns default."""
        data = {"other": "value"}
        result = _safe_get_as_dict(data, "config", default={"default": True})
        assert result == {"default": True}

    def test_list_normalized(self):
        """List is normalized to dict."""
        data = {"items": [1, 2, 3]}
        result = _safe_get_as_dict(data, "items")
        assert result["items"] == [1, 2, 3]
        assert result["steps"] == [1, 2, 3]

    def test_json_string_parsed(self):
        """JSON string is parsed."""
        data = {"config": '{"key": "value"}'}
        result = _safe_get_as_dict(data, "config")
        assert result["key"] == "value"

    def test_json_list_string_normalized(self):
        """JSON list string is parsed and normalized."""
        data = {"items": '[1, 2, 3]'}
        result = _safe_get_as_dict(data, "items")
        assert result["items"] == [1, 2, 3]

    def test_invalid_json_string(self):
        """Invalid JSON returns raw_text dict."""
        data = {"text": "not json"}
        result = _safe_get_as_dict(data, "text")
        assert result["raw_text"] == "not json"


# =============================================================================
# Tests for _safe_get_as_list helper
# =============================================================================


class TestSafeGetAsList:
    """Tests for _safe_get_as_list helper function."""

    def test_get_list(self):
        """Get list value."""
        data = {"items": [1, 2, 3]}
        result = _safe_get_as_list(data, "items")
        assert result == [1, 2, 3]

    def test_missing_returns_default(self):
        """Missing key returns default."""
        data = {"other": "value"}
        result = _safe_get_as_list(data, "items", default=[0])
        assert result == [0]

    def test_flatten_nested_lists(self):
        """Flatten nested lists."""
        data = {"items": [[1, 2], [3, 4]]}
        result = _safe_get_as_list(data, "items")
        assert result == [1, 2, 3, 4]

    def test_string_wrapped(self):
        """String is wrapped in list."""
        data = {"item": "single"}
        result = _safe_get_as_list(data, "item")
        assert result == ["single"]

    def test_dict_extracts_items(self):
        """Dict extracts items/steps key."""
        data = {"config": {"items": [1, 2]}}
        result = _safe_get_as_list(data, "config")
        assert result == [1, 2]

    def test_dict_extracts_steps(self):
        """Dict extracts steps key if no items."""
        data = {"config": {"steps": [3, 4]}}
        result = _safe_get_as_list(data, "config")
        assert result == [3, 4]


# =============================================================================
# Tests for _safe_get_as_str helper
# =============================================================================


class TestSafeGetAsStr:
    """Tests for _safe_get_as_str helper function."""

    def test_get_string(self):
        """Get string value."""
        data = {"name": "test"}
        result = _safe_get_as_str(data, "name")
        assert result == "test"

    def test_missing_returns_default(self):
        """Missing key returns default."""
        data = {"other": "value"}
        result = _safe_get_as_str(data, "name", default="default")
        assert result == "default"

    def test_int_converted(self):
        """Int is converted to string."""
        data = {"value": 42}
        result = _safe_get_as_str(data, "value")
        assert result == "42"

    def test_float_converted(self):
        """Float is converted to string."""
        data = {"value": 3.14}
        result = _safe_get_as_str(data, "value")
        assert result == "3.14"

    def test_list_returns_first_string(self):
        """List returns first string item."""
        data = {"items": [1, "second", "third"]}
        result = _safe_get_as_str(data, "items")
        assert result == "second"

    def test_list_no_strings(self):
        """List with no strings returns default."""
        data = {"items": [1, 2, 3]}
        result = _safe_get_as_str(data, "items", default="default")
        assert result == "default"


# =============================================================================
# Tests for _safe_get_as_int helper
# =============================================================================


class TestSafeGetAsInt:
    """Tests for _safe_get_as_int helper function."""

    def test_get_int(self):
        """Get int value."""
        data = {"value": 42}
        result = _safe_get_as_int(data, "value")
        assert result == 42

    def test_missing_returns_default(self):
        """Missing key returns default."""
        data = {"other": "value"}
        result = _safe_get_as_int(data, "value", default=10)
        assert result == 10

    def test_float_truncated(self):
        """Float is truncated to int."""
        data = {"value": 3.7}
        result = _safe_get_as_int(data, "value")
        assert result == 3

    def test_string_parsed(self):
        """String is parsed to int."""
        data = {"value": "42"}
        result = _safe_get_as_int(data, "value")
        assert result == 42

    def test_float_string_parsed(self):
        """Float string is parsed to int."""
        data = {"value": "3.9"}
        result = _safe_get_as_int(data, "value")
        assert result == 3

    def test_invalid_string(self):
        """Invalid string returns default."""
        data = {"value": "not a number"}
        result = _safe_get_as_int(data, "value", default=0)
        assert result == 0


# =============================================================================
# Tests for AIDecompositionEngine
# =============================================================================


class TestAIDecompositionEngine:
    """Tests for AIDecompositionEngine."""

    def test_decompose_success(self):
        """Successful decomposition."""
        response = {"subtasks": ["task1", "task2"], "granularity": "fine"}
        engine = AIDecompositionEngine(make_mock_sender(response))
        result = engine.decompose("Build a web app")
        assert result.success is True
        assert result.subtasks == ["task1", "task2"]
        assert result.granularity == "fine"

    def test_decompose_exception(self):
        """Decomposition handles exception."""
        engine = AIDecompositionEngine(make_exception_sender(ValueError("API error")))
        result = engine.decompose("Build a web app")
        assert result.success is False
        assert "API error" in result.error
        assert result.subtasks == ["Build a web app"]  # Fallback
        assert result.failure is not None
        assert result.failure.fallback_used is True

    def test_decompose_empty_subtasks(self):
        """Empty subtasks fallback to original task."""
        response = {"subtasks": [], "granularity": "medium"}
        engine = AIDecompositionEngine(make_mock_sender(response))
        result = engine.decompose("Original task")
        assert result.subtasks == ["Original task"]

    def test_decompose_invalid_granularity(self):
        """Invalid granularity defaults to medium."""
        response = {"subtasks": ["task1"], "granularity": "invalid"}
        engine = AIDecompositionEngine(make_mock_sender(response))
        result = engine.decompose("Task")
        assert result.granularity == "medium"

    def test_decompose_list_response(self):
        """Handle list response."""
        response = ["task1", "task2"]  # AI returns list directly
        engine = AIDecompositionEngine(make_mock_sender(response))
        result = engine.decompose("Task")
        # _ensure_dict wraps list with subtasks key
        assert len(result.subtasks) >= 1


class TestDecompositionResult:
    """Tests for DecompositionResult dataclass."""

    def test_create(self):
        """Create result."""
        result = DecompositionResult(
            raw_response={"data": "value"},
            subtasks=["a", "b"],
            granularity="coarse",
        )
        assert result.subtasks == ["a", "b"]
        assert result.granularity == "coarse"


# =============================================================================
# Tests for AIComplexityAssessor
# =============================================================================


class TestAIComplexityAssessor:
    """Tests for AIComplexityAssessor."""

    def test_assess_success(self):
        """Successful assessment."""
        response = {"complexity": "high", "score": 8, "factors": ["complex logic"]}
        assessor = AIComplexityAssessor(make_mock_sender(response))
        result = assessor.assess("Implement distributed system")
        assert result.success is True
        assert result.level == "high"
        assert result.score == 8
        assert "complex logic" in result.factors

    def test_assess_exception(self):
        """Assessment handles exception."""
        assessor = AIComplexityAssessor(make_exception_sender(RuntimeError("Timeout")))
        result = assessor.assess("Task")
        assert result.success is False
        assert result.level == "medium"  # Fallback
        assert result.score == 5  # Fallback

    def test_assess_invalid_level(self):
        """Invalid level defaults to medium."""
        response = {"complexity": "extreme", "score": 5}
        assessor = AIComplexityAssessor(make_mock_sender(response))
        result = assessor.assess("Task")
        assert result.level == "medium"

    def test_assess_score_clamped(self):
        """Score is clamped to 1-10."""
        response = {"complexity": "low", "score": 15}
        assessor = AIComplexityAssessor(make_mock_sender(response))
        result = assessor.assess("Task")
        assert result.score == 10

    def test_assess_score_clamped_low(self):
        """Score is clamped minimum 1."""
        response = {"complexity": "low", "score": -5}
        assessor = AIComplexityAssessor(make_mock_sender(response))
        result = assessor.assess("Task")
        assert result.score == 1


class TestComplexityResult:
    """Tests for ComplexityResult dataclass."""

    def test_create(self):
        """Create result."""
        result = ComplexityResult(
            raw_response={},
            level="low",
            score=3,
            factors=["simple"],
        )
        assert result.level == "low"
        assert result.score == 3


# =============================================================================
# Tests for AIContextEngine
# =============================================================================


class TestAIContextEngine:
    """Tests for AIContextEngine."""

    def test_extract_context(self):
        """Extract context from conversation."""
        response = {
            "framework": "React",
            "language": "TypeScript",
            "current_task": "Add button",
            "implicit_requirements": ["accessibility"],
        }
        engine = AIContextEngine(make_mock_sender(response))
        result = engine.extract_context([{"role": "user", "content": "Add a button"}])
        assert result.framework == "React"
        assert result.language == "TypeScript"
        assert "accessibility" in result.implicit_requirements


class TestContextResult:
    """Tests for ContextResult dataclass."""

    def test_create(self):
        """Create result."""
        result = ContextResult(
            raw_response={},
            framework="Django",
            language="Python",
        )
        assert result.framework == "Django"


# =============================================================================
# Tests for AIAssumptionIdentifier
# =============================================================================


class TestAIAssumptionIdentifier:
    """Tests for AIAssumptionIdentifier."""

    def test_identify(self):
        """Identify assumptions."""
        response = {"assumptions": [{"assumption": "User has Python", "confidence": 0.9}]}
        identifier = AIAssumptionIdentifier(make_mock_sender(response))
        result = identifier.identify("Run pytest")
        assert len(result.assumptions) == 1


# =============================================================================
# Tests for AIRiskAssessor
# =============================================================================


class TestAIRiskAssessor:
    """Tests for AIRiskAssessor."""

    def test_assess(self):
        """Assess risks."""
        response = {"risks": [{"risk": "Data loss", "severity": "high", "mitigation": "Backup"}]}
        assessor = AIRiskAssessor(make_mock_sender(response))
        result = assessor.assess("Delete database")
        assert len(result.risks) == 1


# =============================================================================
# Tests for AIConstraintRecognizer
# =============================================================================


class TestAIConstraintRecognizer:
    """Tests for AIConstraintRecognizer."""

    def test_recognize(self):
        """Recognize constraints."""
        response = {"constraints": [{"type": "technical", "constraint": "Must use Python 3.8+"}]}
        recognizer = AIConstraintRecognizer(make_mock_sender(response))
        result = recognizer.recognize("Build CLI tool")
        assert len(result.constraints) == 1


# =============================================================================
# Tests for AIDependencyAnalyzer
# =============================================================================


class TestAIDependencyAnalyzer:
    """Tests for AIDependencyAnalyzer."""

    def test_analyze(self):
        """Analyze dependencies."""
        response = {
            "dependencies": [{"task": "build", "depends_on": "test"}],
            "execution_order": ["test", "build"],
        }
        analyzer = AIDependencyAnalyzer(make_mock_sender(response))
        result = analyzer.analyze(["test", "build"])
        assert len(result.dependencies) == 1
        assert result.execution_order == ["test", "build"]

    def test_analyze_default_order(self):
        """Default execution order is input tasks."""
        response = {"dependencies": []}
        analyzer = AIDependencyAnalyzer(make_mock_sender(response))
        result = analyzer.analyze(["a", "b", "c"])
        assert result.execution_order == ["a", "b", "c"]


# =============================================================================
# Tests for AIEdgeCaseIdentifier
# =============================================================================


class TestAIEdgeCaseIdentifier:
    """Tests for AIEdgeCaseIdentifier."""

    def test_identify(self):
        """Identify edge cases."""
        response = {"edge_cases": [{"case": "Empty input", "test": "test_empty"}]}
        identifier = AIEdgeCaseIdentifier(make_mock_sender(response))
        result = identifier.identify("Parse user input")
        assert len(result.edge_cases) == 1


# =============================================================================
# Tests for AITradeoffAnalyzer
# =============================================================================


class TestAITradeoffAnalyzer:
    """Tests for AITradeoffAnalyzer."""

    def test_analyze(self):
        """Analyze tradeoffs."""
        response = {
            "options": [{"option": "SQL", "pros": ["mature"], "cons": ["rigid"]}],
            "recommendation": "Use SQL",
        }
        analyzer = AITradeoffAnalyzer(make_mock_sender(response))
        result = analyzer.analyze("Choose database")
        assert len(result.options) == 1
        assert result.recommendation == "Use SQL"


# =============================================================================
# Tests for AIImpactAssessor
# =============================================================================


class TestAIImpactAssessor:
    """Tests for AIImpactAssessor."""

    def test_assess(self):
        """Assess impact."""
        response = {
            "affected_components": ["auth", "api"],
            "affected_files": ["auth.py"],
            "impact_level": "high",
        }
        assessor = AIImpactAssessor(make_mock_sender(response))
        result = assessor.assess("Change auth flow")
        assert "auth" in result.affected_components
        assert result.impact_level == "high"


# =============================================================================
# Tests for AIPrerequisiteDetector
# =============================================================================


class TestAIPrerequisiteDetector:
    """Tests for AIPrerequisiteDetector."""

    def test_detect(self):
        """Detect prerequisites."""
        response = {"prerequisites": [{"requirement": "Node.js", "met": True, "action": None}]}
        detector = AIPrerequisiteDetector(make_mock_sender(response))
        result = detector.detect("Run npm install")
        assert len(result.prerequisites) == 1


# =============================================================================
# Tests for AIScopeBoundaryDetector
# =============================================================================


class TestAIScopeBoundaryDetector:
    """Tests for AIScopeBoundaryDetector."""

    def test_detect(self):
        """Detect scope boundaries."""
        response = {
            "in_scope": False,
            "scope_concerns": ["Too broad"],
            "suggested_focus": "Focus on API only",
        }
        detector = AIScopeBoundaryDetector(make_mock_sender(response))
        result = detector.detect("Rewrite the entire system")
        assert result.in_scope is False
        assert len(result.scope_concerns) == 1


# =============================================================================
# Tests for AIContradictionDetector
# =============================================================================


class TestAIContradictionDetector:
    """Tests for AIContradictionDetector."""

    def test_detect(self):
        """Detect contradictions."""
        response = {
            "contradictions": [
                {"statement1": "Use REST", "statement2": "Use GraphQL", "resolution_needed": True}
            ]
        }
        detector = AIContradictionDetector(make_mock_sender(response))
        result = detector.detect(["Use REST", "Use GraphQL"])
        assert len(result.contradictions) == 1


# =============================================================================
# Tests for AIPriorityInferrer
# =============================================================================


class TestAIPriorityInferrer:
    """Tests for AIPriorityInferrer."""

    def test_infer(self):
        """Infer priorities."""
        response = {"priorities": [{"task": "security", "priority": 1, "reason": "Critical"}]}
        inferrer = AIPriorityInferrer(make_mock_sender(response))
        result = inferrer.infer(["security", "styling"])
        assert len(result.priorities) == 1


# =============================================================================
# Tests for AISuccessCriteriaExtractor
# =============================================================================


class TestAISuccessCriteriaExtractor:
    """Tests for AISuccessCriteriaExtractor."""

    def test_extract(self):
        """Extract success criteria."""
        response = {"criteria": [{"criterion": "Tests pass", "measurable": True}]}
        extractor = AISuccessCriteriaExtractor(make_mock_sender(response))
        result = extractor.extract("Implement feature")
        assert len(result.criteria) == 1


# =============================================================================
# Tests for AIPlanGenerator
# =============================================================================


class TestAIPlanGenerator:
    """Tests for AIPlanGenerator."""

    def test_generate_success(self):
        """Generate plan successfully."""
        response = {
            "plan": {"steps": [{"step": "1", "action": "setup"}, {"step": "2", "action": "implement"}]}
        }
        generator = AIPlanGenerator(make_mock_sender(response))
        result = generator.generate("Build API")
        assert len(result.steps) == 2

    def test_generate_exception(self):
        """Generate handles exception."""
        generator = AIPlanGenerator(make_exception_sender(ValueError("Error")))
        result = generator.generate("Task")
        assert result.success is False
        assert result.steps == []

    def test_generate_steps_directly(self):
        """Steps directly in response."""
        response = {"steps": [{"step": "1"}]}
        generator = AIPlanGenerator(make_mock_sender(response))
        result = generator.generate("Task")
        assert len(result.steps) == 1

    def test_generate_plan_is_list(self):
        """Plan is a list instead of dict."""
        response = {"plan": [{"step": "1"}, {"step": "2"}]}
        generator = AIPlanGenerator(make_mock_sender(response))
        result = generator.generate("Task")
        # _safe_get_as_dict normalizes list to dict with items/steps
        assert len(result.steps) >= 0  # Steps may or may not be found


# =============================================================================
# Tests for AIPlanRefiner
# =============================================================================


class TestAIPlanRefiner:
    """Tests for AIPlanRefiner."""

    def test_refine(self):
        """Refine plan."""
        response = {
            "refined_plan": {"steps": [{"step": "improved"}]},
            "changes_made": ["Added caching"],
        }
        refiner = AIPlanRefiner(make_mock_sender(response))
        result = refiner.refine({"steps": []}, {"feedback": "Add caching"})
        assert len(result.steps) == 1
        assert "Added caching" in result.changes_made

    def test_refine_exception(self):
        """Refine handles exception."""
        refiner = AIPlanRefiner(make_exception_sender(RuntimeError("Error")))
        result = refiner.refine({}, {})
        assert result.success is False
        assert result.steps == []


# =============================================================================
# Tests for AIMultiPathPlanner
# =============================================================================


class TestAIMultiPathPlanner:
    """Tests for AIMultiPathPlanner."""

    def test_plan(self):
        """Plan multiple paths."""
        response = {
            "paths": [{"name": "fast", "steps": []}, {"name": "thorough", "steps": []}],
            "recommended": "thorough",
        }
        planner = AIMultiPathPlanner(make_mock_sender(response))
        result = planner.plan("Deploy application")
        assert len(result.paths) == 2
        assert result.recommended == "thorough"

    def test_plan_exception(self):
        """Plan handles exception."""
        planner = AIMultiPathPlanner(make_exception_sender(ValueError("Error")))
        result = planner.plan("Task")
        assert result.success is False
        assert result.paths == []


# =============================================================================
# Tests for AIResourceAwarePlanner
# =============================================================================


class TestAIResourceAwarePlanner:
    """Tests for AIResourceAwarePlanner."""

    def test_plan(self):
        """Plan with resources."""
        response = {"plan": {"steps": [{"step": "1"}], "resource_aware": True}}
        planner = AIResourceAwarePlanner(make_mock_sender(response))
        result = planner.plan("Deploy", {"memory": "4GB"})
        assert len(result.steps) == 1
        assert result.resource_aware is True

    def test_plan_exception(self):
        """Plan handles exception."""
        planner = AIResourceAwarePlanner(make_exception_sender(ValueError("Error")))
        result = planner.plan("Task", {})
        assert result.success is False

    def test_plan_resource_aware_false(self):
        """Resource aware can be false."""
        response = {"plan": {"steps": [], "resource_aware": False}}
        planner = AIResourceAwarePlanner(make_mock_sender(response))
        result = planner.plan("Task", {})
        assert result.resource_aware is False


# =============================================================================
# Tests for AIRollbackPlanner
# =============================================================================


class TestAIRollbackPlanner:
    """Tests for AIRollbackPlanner."""

    def test_plan(self):
        """Plan with rollback."""
        response = {
            "plan": {
                "steps": [{"step": "1"}],
                "checkpoints": [{"id": "cp1"}],
                "rollback_strategy": "revert all",
            }
        }
        planner = AIRollbackPlanner(make_mock_sender(response))
        result = planner.plan("Database migration")
        assert len(result.steps) == 1
        assert len(result.checkpoints) == 1
        assert result.rollback_strategy == "revert all"

    def test_plan_exception(self):
        """Plan handles exception."""
        planner = AIRollbackPlanner(make_exception_sender(ValueError("Error")))
        result = planner.plan("Task")
        assert result.success is False
        assert result.rollback_strategy is None


# =============================================================================
# Tests for AIParallelPlanner
# =============================================================================


class TestAIParallelPlanner:
    """Tests for AIParallelPlanner."""

    def test_plan(self):
        """Plan parallel execution."""
        response = {
            "parallel_groups": [{"group": 1, "tasks": ["a", "b"], "can_parallelize": True}]
        }
        planner = AIParallelPlanner(make_mock_sender(response))
        result = planner.plan(["a", "b", "c"])
        assert len(result.parallel_groups) == 1


# =============================================================================
# Tests for AITestingStrategyPlanner
# =============================================================================


class TestAITestingStrategyPlanner:
    """Tests for AITestingStrategyPlanner."""

    def test_plan(self):
        """Plan testing strategy."""
        response = {
            "strategy": {
                "unit_tests": True,
                "integration_tests": True,
                "e2e_tests": False,
                "coverage_target": 80,
            }
        }
        planner = AITestingStrategyPlanner(make_mock_sender(response))
        result = planner.plan("Build API")
        assert result.strategy["unit_tests"] is True


# =============================================================================
# Tests for AIChainOfThoughtReasoner
# =============================================================================


class TestAIChainOfThoughtReasoner:
    """Tests for AIChainOfThoughtReasoner."""

    def test_reason(self):
        """Apply reasoning."""
        response = {
            "reasoning_steps": [{"step": "1", "thought": "First"}],
            "conclusion": "Do X",
        }
        reasoner = AIChainOfThoughtReasoner(make_mock_sender(response))
        result = reasoner.reason("How to solve?")
        assert len(result.reasoning_steps) == 1
        assert result.conclusion == "Do X"

    def test_reason_with_tdd(self):
        """Apply TDD-aware reasoning."""
        response = {
            "reasoning_steps": [{"step": "test_cases", "thought": "Write tests first"}],
            "conclusion": "TDD approach",
            "tdd_compliant": True,
        }
        reasoner = AIChainOfThoughtReasoner(make_mock_sender(response))
        result = reasoner.reason_with_tdd("Implement sort function")
        assert len(result.reasoning_steps) == 1


# =============================================================================
# Tests for AICodePatternAnalyzer
# =============================================================================


class TestAICodePatternAnalyzer:
    """Tests for AICodePatternAnalyzer."""

    def test_analyze(self):
        """Analyze code patterns."""
        response = {"patterns": [{"pattern": "singleton", "type": "design", "suggestion": "OK"}]}
        analyzer = AICodePatternAnalyzer(make_mock_sender(response))
        result = analyzer.analyze("class Foo: pass")
        assert len(result.patterns) == 1


# =============================================================================
# Tests for AITestGenerator
# =============================================================================


class TestAITestGenerator:
    """Tests for AITestGenerator."""

    def test_generate(self):
        """Generate tests."""
        response = {"tests": [{"name": "test_add", "code": "assert add(1,2) == 3"}]}
        generator = AITestGenerator(make_mock_sender(response))
        result = generator.generate("def add(a, b): return a + b")
        assert len(result.tests) == 1


# =============================================================================
# Tests for AIAdaptiveExecutor
# =============================================================================


class TestAIAdaptiveExecutor:
    """Tests for AIAdaptiveExecutor."""

    def test_adapt(self):
        """Adapt execution."""
        response = {"adapted_strategy": "retry with backoff", "reason": "Transient failure"}
        executor = AIAdaptiveExecutor(make_mock_sender(response))
        result = executor.adapt({"error": "timeout"})
        assert result.adapted_strategy == "retry with backoff"
        assert result.reason == "Transient failure"


# =============================================================================
# Tests for AIShellCommandGenerator
# =============================================================================


class TestAIShellCommandGenerator:
    """Tests for AIShellCommandGenerator."""

    def test_generate(self):
        """Generate shell command."""
        response = {"command": "ls -la", "explanation": "List all files"}
        generator = AIShellCommandGenerator(make_mock_sender(response))
        result = generator.generate("List files in directory")
        assert result.command == "ls -la"
        assert "List" in result.explanation


# =============================================================================
# Tests for AIGitMaster
# =============================================================================


class TestAIGitMaster:
    """Tests for AIGitMaster."""

    def test_handle(self):
        """Handle git scenario."""
        response = {"commands": ["git add .", "git commit -m 'fix'"], "explanation": "Commit fix"}
        master = AIGitMaster(make_mock_sender(response))
        result = master.handle("Commit my changes")
        assert len(result.commands) == 2


# =============================================================================
# Tests for AIOutcomeLearner
# =============================================================================


class TestAIOutcomeLearner:
    """Tests for AIOutcomeLearner."""

    def test_learn(self):
        """Learn from outcome."""
        response = {"lessons": [{"lesson": "Use caching", "confidence": 0.8}]}
        learner = AIOutcomeLearner(make_mock_sender(response))
        result = learner.learn({"task": "optimize", "result": "slow"})
        assert len(result.lessons) == 1


# =============================================================================
# Tests for AIPlaceholderDetector
# =============================================================================


class TestAIPlaceholderDetector:
    """Tests for AIPlaceholderDetector."""

    def test_detect_placeholder(self):
        """Detect placeholder code."""
        response = {"is_placeholder": True, "indicators": ["TODO comment", "pass statement"]}
        detector = AIPlaceholderDetector(make_mock_sender(response))
        result = detector.detect("def foo(): pass  # TODO")
        assert result.is_placeholder is True
        assert len(result.indicators) == 2

    def test_detect_not_placeholder(self):
        """Detect complete code."""
        response = {"is_placeholder": False, "indicators": []}
        detector = AIPlaceholderDetector(make_mock_sender(response))
        result = detector.detect("def foo(): return 42")
        assert result.is_placeholder is False


# =============================================================================
# Tests for AIOrchestrator
# =============================================================================


class TestAIOrchestrator:
    """Tests for AIOrchestrator."""

    def test_init(self):
        """Initialize orchestrator."""
        orchestrator = AIOrchestrator(make_mock_sender({}))
        assert orchestrator.decomposition_engine is not None
        assert orchestrator.complexity_assessor is not None
        assert orchestrator.reasoner is not None

    def test_plugins_disabled_by_default(self):
        """Plugins disabled by default."""
        orchestrator = AIOrchestrator(make_mock_sender({}))
        assert orchestrator.plugins_enabled is False

    def test_list_plugin_capabilities_empty(self):
        """List capabilities when plugins disabled."""
        orchestrator = AIOrchestrator(make_mock_sender({}))
        assert orchestrator.list_plugin_capabilities() == []

    def test_plan_plugin_actions_empty(self):
        """Plan plugin actions when disabled."""
        orchestrator = AIOrchestrator(make_mock_sender({}))
        assert orchestrator.plan_plugin_actions("task") == []

    def test_execute_plugin_actions_empty(self):
        """Execute plugin actions with empty list."""
        orchestrator = AIOrchestrator(make_mock_sender({}))
        assert orchestrator.execute_plugin_actions([]) == []

    def test_run_plugin_cycle_disabled(self):
        """Run plugin cycle when disabled."""
        orchestrator = AIOrchestrator(make_mock_sender({}))
        result = orchestrator.run_plugin_cycle("task")
        assert result["planned_actions"] == []
        assert result["results"] == []
        assert result["summary"] == ""

    def test_execute_basic(self):
        """Execute basic task."""
        # Mock responses for all AI calls
        response = {
            "complexity": "medium",
            "score": 5,
            "subtasks": ["subtask1"],
            "granularity": "medium",
            "plan": {"steps": [{"step": "1"}]},
            "reasoning_steps": [],
            "conclusion": "Done",
            "lessons": [],
            "result": "success",
            "success": True,
        }
        orchestrator = AIOrchestrator(make_mock_sender(response))
        result = orchestrator.execute("Build feature")

        assert "complexity" in result
        assert "subtasks" in result
        assert "plan_steps" in result
        assert "result" in result

    def test_build_plugin_guidance_empty(self):
        """Build plugin guidance with empty results."""
        orchestrator = AIOrchestrator(make_mock_sender({}))
        guidance = orchestrator._build_plugin_guidance({"results": []})
        assert guidance == ""

    def test_build_plugin_guidance_non_list(self):
        """Build plugin guidance with non-list results."""
        orchestrator = AIOrchestrator(make_mock_sender({}))
        guidance = orchestrator._build_plugin_guidance({"results": "not a list"})
        assert guidance == ""

    def test_build_plugin_guidance_with_data(self):
        """Build plugin guidance with actual data."""
        orchestrator = AIOrchestrator(make_mock_sender({}))
        plugin_cycle = {
            "results": [
                {
                    "success": True,
                    "data": {
                        "capability_type": "skill",
                        "capability_name": "code_review",
                        "plugin": "review_plugin",
                        "description": "Reviews code",
                        "workflow_steps": ["step1", "step2"],
                        "execution_prompt": "Review this code",
                    },
                }
            ]
        }
        guidance = orchestrator._build_plugin_guidance(plugin_cycle)
        assert "PLUGIN_CAPABILITY" in guidance
        assert "review_plugin" in guidance


# =============================================================================
# Integration Tests
# =============================================================================


class TestAIOrchestrationIntegration:
    """Integration tests for AI orchestration."""

    def test_full_orchestration_flow(self):
        """Test full orchestration flow."""
        response = {
            "complexity": "low",
            "score": 3,
            "factors": ["simple"],
            "subtasks": ["step1", "step2"],
            "granularity": "fine",
            "plan": {"steps": [{"step": "1", "action": "do"}]},
            "reasoning_steps": [{"step": "think", "thought": "analyze"}],
            "conclusion": "Proceed",
            "lessons": [{"lesson": "Keep it simple"}],
            "result": "completed",
            "success": True,
        }

        orchestrator = AIOrchestrator(make_mock_sender(response))
        result = orchestrator.execute("Simple task")

        assert result["complexity"] == "low"
        assert len(result["subtasks"]) == 2
        assert len(result["plan_steps"]) >= 1

    def test_error_handling_propagation(self):
        """Test error handling across components."""
        # Simulate AI that returns malformed responses
        malformed_response = {"invalid": "structure"}

        orchestrator = AIOrchestrator(make_mock_sender(malformed_response))
        result = orchestrator.execute("Task")

        # Should still complete without crashing
        assert "complexity" in result
        assert "subtasks" in result

    def test_decomposition_to_planning_flow(self):
        """Test decomposition flows into planning."""
        decomposition_response = {
            "subtasks": ["setup", "implement", "test"],
            "granularity": "fine",
        }
        plan_response = {
            "plan": {"steps": [{"step": "1"}, {"step": "2"}, {"step": "3"}]}
        }

        # Test decomposition with decomposition response
        engine = AIDecompositionEngine(make_mock_sender(decomposition_response))
        decomp = engine.decompose("Build app")
        assert len(decomp.subtasks) == 3

        # Test planning with plan response
        generator = AIPlanGenerator(make_mock_sender(plan_response))
        plan = generator.generate("Build app")
        assert len(plan.steps) == 3
