"""Comprehensive tests for sage/core/self_improvement.py - Self-Improvement System."""

import time
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from sage.core.self_improvement import (
    # Enums
    ProficiencyLevel,
    FailureSeverity,
    # Dataclasses
    CapabilityResult,
    HallucinationResult,
    RootCauseResult,
    FailureChain,
    FailureCategory,
    FixResult,
    FixStrategy,
    ValidationResult,
    DiagnosisResult,
    LanguageAssessmentResult,
    DebuggingAssessmentResult,
    ProblemSolvingResult,
    AccuracyResult,
    AssessmentResult,
    MonitoringResult,
    DiagnosisRunResult,
    RepairResult,
    ModificationResult,
    ImprovementPlan,
    # Classes - Category 1.1: Capability Assessment
    SelfAssessmentEngine,
    CapabilityInventory,
    SkillProficiency,
    CapabilityGapDetector,
    ImprovementPriorityQueue,
    SuccessRateTracker,
    FailurePatternAnalyzer,
    CapabilityDependencyGraph,
    CapabilityVersioning,
    LanguageProficiencyAssessor,
    DebuggingSkillAssessor,
    ProblemSolvingAssessor,
    AccuracyAssessor,
    # Classes - Category 1.2: Self-Monitoring
    PerformanceMonitor,
    ErrorRateTracker,
    HallucinationDetector,
    ConfidenceCalibrator,
    TaskCompletionMonitor,
    QualityScoreTracker,
    CodeQualityMonitor,
    InstructionFollowingMonitor,
    # Classes - Category 1.3: Self-Diagnosis
    RootCauseAnalyzer,
    FailureCategorizer,
    PatternBasedDiagnosis,
    SymptomToCauseMapper,
    OverallHealthDiagnosis,
    # Classes - Category 1.4: Self-Repair
    AutoFixSystem,
    FixStrategySelector,
    RollbackMechanism,
    FixValidation,
    FixLearningSystem,
    # Orchestrator
    SelfImprovementOrchestrator,
)


# =============================================================================
# Tests for Enums
# =============================================================================


class TestProficiencyLevel:
    """Tests for ProficiencyLevel enum."""

    def test_novice(self):
        assert ProficiencyLevel.NOVICE.value == "novice"

    def test_beginner(self):
        assert ProficiencyLevel.BEGINNER.value == "beginner"

    def test_intermediate(self):
        assert ProficiencyLevel.INTERMEDIATE.value == "intermediate"

    def test_advanced(self):
        assert ProficiencyLevel.ADVANCED.value == "advanced"

    def test_expert(self):
        assert ProficiencyLevel.EXPERT.value == "expert"


class TestFailureSeverity:
    """Tests for FailureSeverity enum."""

    def test_low(self):
        assert FailureSeverity.LOW.value == "low"

    def test_medium(self):
        assert FailureSeverity.MEDIUM.value == "medium"

    def test_high(self):
        assert FailureSeverity.HIGH.value == "high"

    def test_critical(self):
        assert FailureSeverity.CRITICAL.value == "critical"


# =============================================================================
# Tests for Dataclasses
# =============================================================================


class TestCapabilityResult:
    """Tests for CapabilityResult dataclass."""

    def test_create(self):
        result = CapabilityResult(name="python", score=0.85, confidence=0.9)
        assert result.name == "python"
        assert result.score == 0.85
        assert result.confidence == 0.9

    def test_defaults(self):
        result = CapabilityResult(name="test", score=0.5, confidence=0.5)
        assert result.sub_scores == {}
        assert isinstance(result.timestamp, datetime)


class TestHallucinationResult:
    """Tests for HallucinationResult dataclass."""

    def test_create(self):
        result = HallucinationResult(
            has_hallucinations=True,
            types=["file", "api"],
            confidence=0.8,
        )
        assert result.has_hallucinations is True
        assert "file" in result.types
        assert result.details == []


class TestRootCauseResult:
    """Tests for RootCauseResult dataclass."""

    def test_create(self):
        result = RootCauseResult(
            root_cause="Missing import",
            confidence=0.9,
            suggested_fixes=["Add import statement"],
        )
        assert result.root_cause == "Missing import"
        assert result.chain == []


class TestFailureChain:
    """Tests for FailureChain dataclass."""

    def test_create(self):
        chain = FailureChain(root="ImportError", sequence=[{"type": "ImportError"}])
        assert chain.root == "ImportError"
        assert len(chain.sequence) == 1


class TestFailureCategory:
    """Tests for FailureCategory dataclass."""

    def test_create(self):
        cat = FailureCategory(
            main_category="syntax",
            sub_category="SyntaxError",
            severity="medium",
        )
        assert cat.main_category == "syntax"
        assert cat.tags == []


class TestFixResult:
    """Tests for FixResult dataclass."""

    def test_create_fixed(self):
        result = FixResult(
            fixed=True,
            fixed_code="print('hello')",
            requires_confirmation=False,
            proposed_fix=None,
            confidence=0.9,
        )
        assert result.fixed is True

    def test_create_not_fixed(self):
        result = FixResult(
            fixed=False,
            fixed_code=None,
            requires_confirmation=True,
            proposed_fix="Manual fix needed",
            confidence=0.3,
        )
        assert result.fixed is False
        assert result.requires_confirmation is True


class TestFixStrategy:
    """Tests for FixStrategy dataclass."""

    def test_create(self):
        strategy = FixStrategy(
            name="type_conversion",
            confidence=0.8,
            description="Convert value to correct type",
        )
        assert strategy.name == "type_conversion"
        assert strategy.steps == []


class TestValidationResult:
    """Tests for ValidationResult dataclass."""

    def test_create(self):
        result = ValidationResult(
            is_valid=True,
            syntax_correct=True,
            passes_tests=True,
            has_regression=False,
        )
        assert result.is_valid is True
        assert result.details == {}


class TestDiagnosisResult:
    """Tests for DiagnosisResult dataclass."""

    def test_create(self):
        result = DiagnosisResult(
            matched_pattern="connection refused",
            diagnosis="Database connection failed",
            confidence=0.9,
        )
        assert result.matched_pattern == "connection refused"
        assert result.suggestions == []


class TestLanguageAssessmentResult:
    """Tests for LanguageAssessmentResult dataclass."""

    def test_create(self):
        result = LanguageAssessmentResult(
            language="python",
            score=0.85,
            sub_scores={"syntax": 0.9},
        )
        assert result.language == "python"


class TestDebuggingAssessmentResult:
    """Tests for DebuggingAssessmentResult dataclass."""

    def test_create(self):
        result = DebuggingAssessmentResult(
            score=0.75,
            sub_scores={"error_identification": 0.8},
        )
        assert result.score == 0.75


class TestProblemSolvingResult:
    """Tests for ProblemSolvingResult dataclass."""

    def test_create(self):
        result = ProblemSolvingResult(
            score=0.8,
            sub_scores={"decomposition": 0.82},
        )
        assert result.score == 0.8


class TestAccuracyResult:
    """Tests for AccuracyResult dataclass."""

    def test_create(self):
        result = AccuracyResult(
            score=0.9,
            total_attempts=100,
            correct_attempts=90,
        )
        assert result.score == 0.9


class TestAssessmentResult:
    """Tests for AssessmentResult dataclass."""

    def test_create(self):
        result = AssessmentResult(
            capabilities_evaluated=10,
            average_score=0.75,
            weakest_capabilities=["security"],
        )
        assert result.capabilities_evaluated == 10


class TestMonitoringResult:
    """Tests for MonitoringResult dataclass."""

    def test_create(self):
        result = MonitoringResult(
            metrics_collected=50,
            alerts_triggered=2,
        )
        assert result.metrics_collected == 50


class TestDiagnosisRunResult:
    """Tests for DiagnosisRunResult dataclass."""

    def test_create(self):
        result = DiagnosisRunResult(
            issues_found=3,
            critical_issues=1,
        )
        assert result.issues_found == 3


class TestRepairResult:
    """Tests for RepairResult dataclass."""

    def test_create(self):
        result = RepairResult(
            fixes_attempted=5,
            fixes_successful=4,
        )
        assert result.fixes_attempted == 5


class TestModificationResult:
    """Tests for ModificationResult dataclass."""

    def test_create(self):
        result = ModificationResult(
            checkpoint_id="abc123",
            can_rollback=True,
            applied=True,
        )
        assert result.checkpoint_id == "abc123"


class TestImprovementPlan:
    """Tests for ImprovementPlan dataclass."""

    def test_create(self):
        plan = ImprovementPlan(
            target_score=0.9,
            steps=["Analyze", "Improve", "Validate"],
        )
        assert plan.target_score == 0.9


# =============================================================================
# Tests for SelfAssessmentEngine
# =============================================================================


class TestSelfAssessmentEngine:
    """Tests for SelfAssessmentEngine class."""

    def test_init(self):
        engine = SelfAssessmentEngine()
        assert "python_coding" in engine.capabilities
        assert engine.capabilities["python_coding"] == 0.85

    def test_evaluate_capability(self):
        engine = SelfAssessmentEngine()
        result = engine.evaluate_capability("python_coding")
        assert result.name == "python_coding"
        assert result.score == 0.85

    def test_evaluate_unknown_capability(self):
        engine = SelfAssessmentEngine()
        result = engine.evaluate_capability("unknown_skill")
        assert result.score == 0.5  # Default

    def test_evaluate_all(self):
        engine = SelfAssessmentEngine()
        results = engine.evaluate_all()
        assert len(results) == len(engine.capabilities)

    def test_get_capability_history(self):
        engine = SelfAssessmentEngine()
        engine.evaluate_capability("python_coding")
        history = engine.get_capability_history("python_coding")
        assert len(history) == 1

    def test_get_improvement_recommendations(self):
        engine = SelfAssessmentEngine()
        recommendations = engine.get_improvement_recommendations()
        # Should recommend improving capabilities below 0.7
        assert isinstance(recommendations, list)

    def test_set_capability_score(self):
        engine = SelfAssessmentEngine()
        engine.set_capability_score("test_cap", 0.5)
        assert engine.capabilities["test_cap"] == 0.5


# =============================================================================
# Tests for CapabilityInventory
# =============================================================================


class TestCapabilityInventory:
    """Tests for CapabilityInventory class."""

    def test_init(self):
        inventory = CapabilityInventory()
        assert inventory.has("python")

    def test_add(self):
        inventory = CapabilityInventory()
        inventory.add("new_skill", category="custom", description="A new skill")
        assert inventory.has("new_skill")

    def test_remove(self):
        inventory = CapabilityInventory()
        inventory.add("to_remove", category="test")
        inventory.remove("to_remove")
        assert not inventory.has("to_remove")

    def test_list_all(self):
        inventory = CapabilityInventory()
        all_caps = inventory.list_all()
        assert "python" in all_caps

    def test_get_categories(self):
        inventory = CapabilityInventory()
        categories = inventory.get_categories()
        assert "programming_languages" in categories

    def test_search(self):
        inventory = CapabilityInventory()
        results = inventory.search("python")
        assert "python" in results

    def test_export_json(self):
        inventory = CapabilityInventory()
        json_str = inventory.export_json()
        assert "python" in json_str

    def test_import_json(self):
        inventory = CapabilityInventory()
        inventory.import_json('{"imported_skill": {"category": "test"}}')
        assert inventory.has("imported_skill")


# =============================================================================
# Tests for SkillProficiency
# =============================================================================


class TestSkillProficiency:
    """Tests for SkillProficiency class."""

    def test_init(self):
        proficiency = SkillProficiency()
        assert proficiency is not None

    def test_calculate_default(self):
        proficiency = SkillProficiency()
        score = proficiency.calculate("unknown")
        assert score == 0.5

    def test_record_and_calculate(self):
        proficiency = SkillProficiency()
        proficiency.record("python", 0.8)
        score = proficiency.calculate("python")
        assert score == 0.8

    def test_get_level_novice(self):
        proficiency = SkillProficiency()
        assert proficiency.get_level(0.1) == "novice"

    def test_get_level_beginner(self):
        proficiency = SkillProficiency()
        assert proficiency.get_level(0.3) == "beginner"

    def test_get_level_intermediate(self):
        proficiency = SkillProficiency()
        assert proficiency.get_level(0.5) == "intermediate"

    def test_get_level_advanced(self):
        proficiency = SkillProficiency()
        assert proficiency.get_level(0.7) == "advanced"

    def test_get_level_expert(self):
        proficiency = SkillProficiency()
        assert proficiency.get_level(0.9) == "expert"

    def test_get_trend_stable(self):
        proficiency = SkillProficiency()
        assert proficiency.get_trend("unknown") == "stable"

    def test_get_trend_improving(self):
        proficiency = SkillProficiency()
        proficiency.record("python", 0.5)
        proficiency.record("python", 0.6)
        proficiency.record("python", 0.7)
        assert proficiency.get_trend("python") == "improving"

    def test_get_trend_declining(self):
        proficiency = SkillProficiency()
        proficiency.record("python", 0.8)
        proficiency.record("python", 0.7)
        proficiency.record("python", 0.6)
        assert proficiency.get_trend("python") == "declining"

    def test_compare(self):
        proficiency = SkillProficiency()
        proficiency.record("python", 0.8)
        proficiency.record("javascript", 0.6)
        comparison = proficiency.compare(["python", "javascript"])
        assert comparison[0]["skill"] == "python"


# =============================================================================
# Tests for CapabilityGapDetector
# =============================================================================


class TestCapabilityGapDetector:
    """Tests for CapabilityGapDetector class."""

    def test_init(self):
        detector = CapabilityGapDetector()
        assert detector is not None

    def test_detect_missing(self):
        detector = CapabilityGapDetector()
        missing = detector.detect_missing(
            current=["python", "javascript"],
            required=["python", "javascript", "rust"],
        )
        assert "rust" in missing

    def test_detect_weak(self):
        detector = CapabilityGapDetector()
        detector.set_scores({"python": 0.8, "rust": 0.3})
        weak = detector.detect_weak(threshold=0.5)
        assert "rust" in weak
        assert "python" not in weak

    def test_prioritize_gaps(self):
        detector = CapabilityGapDetector()
        detector.set_scores({"python": 0.8, "rust": 0.3})
        detector.set_importance({"python": 0.9, "rust": 0.9})
        prioritized = detector.prioritize_gaps()
        # Rust should have higher priority (lower score = bigger gap)
        assert prioritized[0]["capability"] == "rust"

    def test_generate_report(self):
        detector = CapabilityGapDetector()
        detector.set_scores({"python": 0.8, "rust": 0.3})
        report = detector.generate_report()
        assert "summary" in report
        assert "gaps" in report


# =============================================================================
# Tests for ImprovementPriorityQueue
# =============================================================================


class TestImprovementPriorityQueue:
    """Tests for ImprovementPriorityQueue class."""

    def test_init(self):
        queue = ImprovementPriorityQueue()
        assert queue.is_empty()

    def test_add_and_size(self):
        queue = ImprovementPriorityQueue()
        queue.add("improve_python", priority=1)
        assert queue.size() == 1
        assert not queue.is_empty()

    def test_pop(self):
        queue = ImprovementPriorityQueue()
        queue.add("item1", priority=2)
        queue.add("item2", priority=1)
        item = queue.pop()
        assert item["item"] == "item2"  # Higher priority (lower number)

    def test_pop_empty(self):
        queue = ImprovementPriorityQueue()
        assert queue.pop() is None

    def test_peek(self):
        queue = ImprovementPriorityQueue()
        queue.add("item1", priority=1)
        item = queue.peek()
        assert item["item"] == "item1"
        assert queue.size() == 1  # Still in queue

    def test_peek_empty(self):
        queue = ImprovementPriorityQueue()
        assert queue.peek() is None

    def test_update_priority(self):
        queue = ImprovementPriorityQueue()
        queue.add("item1", priority=2)
        queue.add("item2", priority=1)
        queue.update_priority("item1", 0)
        item = queue.pop()
        assert item["item"] == "item1"

    def test_save_and_load(self, tmp_path):
        path = tmp_path / "queue.json"
        queue = ImprovementPriorityQueue(storage_path=path)
        queue.add("item1", priority=1)
        queue.save()

        queue2 = ImprovementPriorityQueue(storage_path=path)
        queue2.load()
        assert queue2.size() == 1


# =============================================================================
# Tests for SuccessRateTracker
# =============================================================================


class TestSuccessRateTracker:
    """Tests for SuccessRateTracker class."""

    def test_init(self):
        tracker = SuccessRateTracker()
        assert tracker is not None

    def test_record_success(self):
        tracker = SuccessRateTracker()
        tracker.record_success("coding", "task1")
        assert tracker.get_success_count("coding") == 1

    def test_record_failure(self):
        tracker = SuccessRateTracker()
        tracker.record_failure("coding", "task1", reason="Timeout")
        assert tracker.get_failure_count("coding") == 1

    def test_get_success_rate(self):
        tracker = SuccessRateTracker()
        tracker.record_success("coding", "task1")
        tracker.record_failure("coding", "task2")
        rate = tracker.get_success_rate("coding")
        assert rate == 0.5

    def test_get_success_rate_no_records(self):
        tracker = SuccessRateTracker()
        assert tracker.get_success_rate("unknown") == 0.0

    def test_get_rates_by_category(self):
        tracker = SuccessRateTracker()
        tracker.record_success("task1", "id1", category="coding")
        tracker.record_failure("task2", "id2", category="coding")
        rates = tracker.get_rates_by_category()
        assert "coding" in rates

    def test_get_trend(self):
        tracker = SuccessRateTracker()
        for i in range(10):
            tracker.record_success("coding", f"task{i}")
        assert tracker.get_trend("coding") in ["improving", "stable", "declining"]

    def test_get_trend_insufficient_data(self):
        tracker = SuccessRateTracker()
        tracker.record_success("coding", "task1")
        assert tracker.get_trend("coding") == "insufficient_data"


# =============================================================================
# Tests for FailurePatternAnalyzer
# =============================================================================


class TestFailurePatternAnalyzer:
    """Tests for FailurePatternAnalyzer class."""

    def test_init(self):
        analyzer = FailurePatternAnalyzer()
        assert analyzer is not None

    def test_record_failure(self):
        analyzer = FailurePatternAnalyzer()
        analyzer.record_failure("task1", "timeout", {"size": "large"})
        patterns = analyzer.get_common_patterns()
        assert len(patterns) == 1
        assert patterns[0]["pattern"] == "timeout"

    def test_get_common_patterns_sorted(self):
        analyzer = FailurePatternAnalyzer()
        analyzer.record_failure("task1", "timeout")
        analyzer.record_failure("task2", "timeout")
        analyzer.record_failure("task3", "memory_error")
        patterns = analyzer.get_common_patterns()
        assert patterns[0]["pattern"] == "timeout"

    def test_find_correlations(self):
        analyzer = FailurePatternAnalyzer()
        # Add failures with common context
        for i in range(5):
            analyzer.record_failure(f"task{i}", "timeout", {"env": "production"})
        correlations = analyzer.find_correlations()
        assert len(correlations) >= 1

    def test_get_prevention_suggestions_known(self):
        analyzer = FailurePatternAnalyzer()
        suggestions = analyzer.get_prevention_suggestions("timeout")
        assert len(suggestions) > 0

    def test_get_prevention_suggestions_unknown(self):
        analyzer = FailurePatternAnalyzer()
        suggestions = analyzer.get_prevention_suggestions("unknown_error")
        assert "Review error details" in suggestions[0]

    def test_get_timeline(self):
        analyzer = FailurePatternAnalyzer()
        analyzer.record_failure("task1", "timeout")
        timeline = analyzer.get_timeline("timeout")
        assert len(timeline) == 1


# =============================================================================
# Tests for CapabilityDependencyGraph
# =============================================================================


class TestCapabilityDependencyGraph:
    """Tests for CapabilityDependencyGraph class."""

    def test_init(self):
        graph = CapabilityDependencyGraph()
        assert graph is not None

    def test_add_dependency(self):
        graph = CapabilityDependencyGraph()
        graph.add_dependency("react", "javascript")
        deps = graph.get_dependencies("react")
        assert "javascript" in deps

    def test_circular_dependency_detection(self):
        graph = CapabilityDependencyGraph()
        graph.add_dependency("a", "b")
        graph.add_dependency("b", "c")
        with pytest.raises(ValueError):
            graph.add_dependency("c", "a")

    def test_get_all_dependencies(self):
        graph = CapabilityDependencyGraph()
        graph.add_dependency("react", "javascript")
        graph.add_dependency("javascript", "programming_basics")
        all_deps = graph.get_all_dependencies("react")
        assert "javascript" in all_deps
        assert "programming_basics" in all_deps

    def test_generate_learning_path(self):
        graph = CapabilityDependencyGraph()
        graph.add_dependency("react", "javascript")
        graph.add_dependency("javascript", "programming_basics")
        path = graph.generate_learning_path("react")
        # Should be in order: basics first
        assert path.index("programming_basics") < path.index("javascript")

    def test_to_visualization_format(self):
        graph = CapabilityDependencyGraph()
        graph.add_dependency("react", "javascript")
        viz = graph.to_visualization_format()
        assert "nodes" in viz
        assert "edges" in viz


# =============================================================================
# Tests for CapabilityVersioning
# =============================================================================


class TestCapabilityVersioning:
    """Tests for CapabilityVersioning class."""

    def test_init(self):
        versioning = CapabilityVersioning()
        assert versioning is not None

    def test_snapshot(self):
        versioning = CapabilityVersioning()
        versioning.snapshot("v1.0", {"python": 0.8})
        stored = versioning.get_version("v1.0")
        assert stored["python"] == 0.8

    def test_get_version_unknown(self):
        versioning = CapabilityVersioning()
        assert versioning.get_version("unknown") == {}

    def test_compare(self):
        versioning = CapabilityVersioning()
        versioning.snapshot("v1.0", {"python": 0.7})
        versioning.snapshot("v2.0", {"python": 0.8})
        comparison = versioning.compare("v1.0", "v2.0")
        assert comparison["python"]["change"] == pytest.approx(0.1)


# =============================================================================
# Tests for Language/Debugging/ProblemSolving/Accuracy Assessors
# =============================================================================


class TestLanguageProficiencyAssessor:
    """Tests for LanguageProficiencyAssessor class."""

    def test_assess(self):
        assessor = LanguageProficiencyAssessor()
        result = assessor.assess("python")
        assert result.language == "python"
        assert result.score == 0.85

    def test_assess_unknown(self):
        assessor = LanguageProficiencyAssessor()
        result = assessor.assess("cobol")
        assert result.score == 0.5

    def test_assess_all(self):
        assessor = LanguageProficiencyAssessor()
        results = assessor.assess_all(["python", "javascript"])
        assert len(results) == 2

    def test_compare_languages(self):
        assessor = LanguageProficiencyAssessor()
        comparison = assessor.compare_languages(["python", "rust"])
        assert comparison["ranking"][0]["language"] == "python"


class TestDebuggingSkillAssessor:
    """Tests for DebuggingSkillAssessor class."""

    def test_assess(self):
        assessor = DebuggingSkillAssessor()
        result = assessor.assess()
        assert result.score == 0.75
        assert "error_identification" in result.sub_scores


class TestProblemSolvingAssessor:
    """Tests for ProblemSolvingAssessor class."""

    def test_assess(self):
        assessor = ProblemSolvingAssessor()
        result = assessor.assess()
        assert result.score == 0.80
        assert "decomposition" in result.sub_scores


class TestAccuracyAssessor:
    """Tests for AccuracyAssessor class."""

    def test_assess_no_results(self):
        assessor = AccuracyAssessor()
        result = assessor.assess()
        assert result.score == 0.0
        assert result.total_attempts == 0

    def test_assess_with_results(self):
        assessor = AccuracyAssessor()
        assessor.record_result(True)
        assessor.record_result(True)
        assessor.record_result(False)
        result = assessor.assess()
        assert result.correct_attempts == 2
        assert result.total_attempts == 3


# =============================================================================
# Tests for PerformanceMonitor
# =============================================================================


class TestPerformanceMonitor:
    """Tests for PerformanceMonitor class."""

    def test_init(self):
        monitor = PerformanceMonitor()
        assert not monitor.is_running()

    def test_start_stop(self):
        monitor = PerformanceMonitor()
        monitor.start()
        assert monitor.is_running()
        monitor.stop()
        assert not monitor.is_running()

    def test_track(self):
        monitor = PerformanceMonitor()
        monitor.track("latency", 100)
        stats = monitor.get_stats("latency")
        assert stats["count"] == 1
        assert stats["mean"] == 100

    def test_threshold_alert(self):
        monitor = PerformanceMonitor()
        alerts = []
        monitor.on_alert(lambda a: alerts.append(a))
        monitor.set_threshold("latency", max_value=50)
        monitor.track("latency", 100)  # Exceeds threshold
        assert len(alerts) == 1

    def test_get_stats_empty(self):
        monitor = PerformanceMonitor()
        stats = monitor.get_stats("unknown")
        assert stats["count"] == 0

    def test_aggregate(self):
        monitor = PerformanceMonitor()
        monitor.track("latency", 100)
        monitor.track("latency", 200)
        agg = monitor.aggregate("latency")
        assert agg["sum"] == 300
        assert agg["count"] == 2


# =============================================================================
# Tests for ErrorRateTracker
# =============================================================================


class TestErrorRateTracker:
    """Tests for ErrorRateTracker class."""

    def test_init(self):
        tracker = ErrorRateTracker()
        assert tracker.total_errors() == 0

    def test_record_error(self):
        tracker = ErrorRateTracker()
        tracker.record_error("timeout")
        assert tracker.total_errors() == 1

    def test_record_success(self):
        tracker = ErrorRateTracker()
        tracker.record_success()
        assert tracker.total_errors() == 0

    def test_get_error_rate(self):
        tracker = ErrorRateTracker()
        tracker.record_error("timeout")
        tracker.record_success()
        rate = tracker.get_error_rate()
        assert rate == 0.5

    def test_get_error_rate_empty(self):
        tracker = ErrorRateTracker()
        assert tracker.get_error_rate() == 0.0

    def test_get_breakdown(self):
        tracker = ErrorRateTracker()
        tracker.record_error("timeout")
        tracker.record_error("timeout")
        tracker.record_error("memory")
        breakdown = tracker.get_breakdown()
        assert breakdown["timeout"] == 2
        assert breakdown["memory"] == 1


# =============================================================================
# Tests for HallucinationDetector
# =============================================================================


class TestHallucinationDetector:
    """Tests for HallucinationDetector class."""

    def test_init(self):
        detector = HallucinationDetector()
        assert detector is not None

    def test_check_no_hallucinations(self):
        detector = HallucinationDetector()
        result = detector.check("This is a normal response")
        assert result.has_hallucinations is False

    def test_check_with_fake_api(self):
        detector = HallucinationDetector()
        result = detector.check(
            "Use the superSplit method", context={"language": "python"}
        )
        assert result.has_hallucinations is True
        assert "api" in result.types

    def test_get_common_patterns(self):
        detector = HallucinationDetector()
        patterns = detector.get_common_patterns()
        assert len(patterns) > 0


# =============================================================================
# Tests for ConfidenceCalibrator
# =============================================================================


class TestConfidenceCalibrator:
    """Tests for ConfidenceCalibrator class."""

    def test_init(self):
        calibrator = ConfidenceCalibrator()
        assert calibrator.sample_count() == 0

    def test_record(self):
        calibrator = ConfidenceCalibrator()
        calibrator.record(0.9, True)
        assert calibrator.sample_count() == 1

    def test_get_calibration_score_insufficient(self):
        calibrator = ConfidenceCalibrator()
        calibrator.record(0.9, True)
        assert calibrator.get_calibration_score() == 0.0

    def test_get_calibration_score(self):
        calibrator = ConfidenceCalibrator()
        # Add enough records
        for _ in range(10):
            calibrator.record(0.9, True)
        score = calibrator.get_calibration_score()
        assert 0 <= score <= 1.0

    def test_is_overconfident(self):
        calibrator = ConfidenceCalibrator()
        # Record high confidence but mostly wrong
        for _ in range(10):
            calibrator.record(0.95, False)
        assert calibrator.is_overconfident() is True

    def test_get_recommendations_overconfident(self):
        calibrator = ConfidenceCalibrator()
        for _ in range(10):
            calibrator.record(0.95, False)
        recommendations = calibrator.get_recommendations()
        assert len(recommendations) > 0


# =============================================================================
# Tests for TaskCompletionMonitor
# =============================================================================


class TestTaskCompletionMonitor:
    """Tests for TaskCompletionMonitor class."""

    def test_init(self):
        monitor = TaskCompletionMonitor()
        assert monitor.get_completion_count() == 0

    def test_start_and_complete_task(self):
        monitor = TaskCompletionMonitor()
        monitor.start_task("task1")
        monitor.complete_task("task1")
        assert monitor.get_completion_count() == 1

    def test_abandon_task(self):
        monitor = TaskCompletionMonitor()
        monitor.start_task("task1")
        monitor.abandon_task("task1", reason="Too complex")
        assert monitor.get_completion_count() == 0

    def test_get_completion_rate(self):
        monitor = TaskCompletionMonitor()
        monitor.start_task("task1")
        monitor.complete_task("task1")
        monitor.start_task("task2")
        monitor.abandon_task("task2")
        rate = monitor.get_completion_rate()
        assert rate == 0.5

    def test_get_completion_rate_empty(self):
        monitor = TaskCompletionMonitor()
        assert monitor.get_completion_rate() == 0.0

    def test_get_average_completion_time(self):
        monitor = TaskCompletionMonitor()
        monitor.start_task("task1")
        time.sleep(0.01)
        monitor.complete_task("task1")
        avg_time = monitor.get_average_completion_time()
        assert avg_time > 0


# =============================================================================
# Tests for QualityScoreTracker
# =============================================================================


class TestQualityScoreTracker:
    """Tests for QualityScoreTracker class."""

    def test_init(self):
        tracker = QualityScoreTracker()
        assert tracker is not None

    def test_record(self):
        tracker = QualityScoreTracker()
        tracker.record("code", 0.85)
        latest = tracker.get_latest("code")
        assert latest["score"] == 0.85

    def test_get_latest_none(self):
        tracker = QualityScoreTracker()
        assert tracker.get_latest("unknown") is None

    def test_get_trend_insufficient(self):
        tracker = QualityScoreTracker()
        tracker.record("code", 0.8)
        assert tracker.get_trend("code") == "insufficient_data"

    def test_get_trend_improving(self):
        tracker = QualityScoreTracker()
        for i in range(5):
            tracker.record("code", 0.7 + i * 0.05)
        assert tracker.get_trend("code") == "improving"


# =============================================================================
# Tests for CodeQualityMonitor
# =============================================================================


class TestCodeQualityMonitor:
    """Tests for CodeQualityMonitor class."""

    def test_analyze(self):
        monitor = CodeQualityMonitor()
        code = '''def hello():
    """Say hello."""
    print("hello")
'''
        result = monitor.analyze(code)
        assert "complexity" in result
        assert "maintainability" in result
        assert result["maintainability"] == 0.8  # Has docstring

    def test_analyze_no_docstring(self):
        monitor = CodeQualityMonitor()
        code = "def hello():\n    print('hello')"
        result = monitor.analyze(code)
        assert result["maintainability"] == 0.6

    def test_detect_smells_too_many_params(self):
        monitor = CodeQualityMonitor()
        code = "def func(a, b, c, d, e, f, g, h, i, j):\n    pass"
        smells = monitor.detect_smells(code)
        assert any(s["type"] == "too_many_parameters" for s in smells)


# =============================================================================
# Tests for InstructionFollowingMonitor
# =============================================================================


class TestInstructionFollowingMonitor:
    """Tests for InstructionFollowingMonitor class."""

    def test_init(self):
        monitor = InstructionFollowingMonitor()
        assert monitor.get_compliance_rate() == 1.0  # Default

    def test_record_instruction_compliant(self):
        monitor = InstructionFollowingMonitor()
        monitor.record_instruction(
            "Use Python 3", "def foo(): ...", compliant=True
        )
        assert monitor.get_compliance_rate() == 1.0

    def test_record_instruction_non_compliant(self):
        monitor = InstructionFollowingMonitor()
        monitor.record_instruction(
            "Use Python 3",
            "print 'hello'",
            compliant=False,
            violation_type="syntax",
        )
        assert monitor.get_compliance_rate() == 0.0

    def test_get_common_violations(self):
        monitor = InstructionFollowingMonitor()
        monitor.record_instruction(
            "inst1", "resp1", compliant=False, violation_type="format"
        )
        monitor.record_instruction(
            "inst2", "resp2", compliant=False, violation_type="format"
        )
        violations = monitor.get_common_violations()
        assert violations[0]["type"] == "format"


# =============================================================================
# Tests for RootCauseAnalyzer
# =============================================================================


class TestRootCauseAnalyzer:
    """Tests for RootCauseAnalyzer class."""

    def test_analyze_known_error(self):
        analyzer = RootCauseAnalyzer()
        result = analyzer.analyze({"type": "NameError", "message": "name 'x' is not defined"})
        assert "Undefined" in result.root_cause
        assert result.confidence == 0.8

    def test_analyze_unknown_error(self):
        analyzer = RootCauseAnalyzer()
        result = analyzer.analyze({"type": "CustomError", "message": "Something went wrong"})
        assert result.confidence == 0.5

    def test_trace_chain(self):
        analyzer = RootCauseAnalyzer()
        errors = [
            {"type": "ImportError", "message": "No module named 'foo'"},
            {"type": "NameError", "message": "name 'foo' is not defined"},
        ]
        chain = analyzer.trace_chain(errors)
        assert chain.root == "ImportError"

    def test_trace_chain_empty(self):
        analyzer = RootCauseAnalyzer()
        chain = analyzer.trace_chain([])
        assert chain.root == "Unknown"


# =============================================================================
# Tests for FailureCategorizer
# =============================================================================


class TestFailureCategorizer:
    """Tests for FailureCategorizer class."""

    def test_categorize_syntax(self):
        categorizer = FailureCategorizer()
        result = categorizer.categorize({"type": "SyntaxError"})
        assert result.main_category == "syntax"
        assert result.severity == "medium"

    def test_categorize_runtime(self):
        categorizer = FailureCategorizer()
        result = categorizer.categorize({"type": "ZeroDivisionError"})
        assert result.main_category == "runtime"
        assert result.severity == "high"

    def test_categorize_system(self):
        categorizer = FailureCategorizer()
        result = categorizer.categorize({"type": "MemoryError"})
        assert result.main_category == "system"
        assert result.severity == "critical"

    def test_categorize_from_context_test_failed(self):
        categorizer = FailureCategorizer()
        result = categorizer.categorize_from_context({
            "test_failed": True,
            "expected_output": "a",
            "actual_output": "b",
        })
        assert result.main_category == "logic"


# =============================================================================
# Tests for PatternBasedDiagnosis
# =============================================================================


class TestPatternBasedDiagnosis:
    """Tests for PatternBasedDiagnosis class."""

    def test_diagnose_known_pattern(self):
        diagnosis = PatternBasedDiagnosis()
        result = diagnosis.diagnose({
            "message": "Connection refused on port 5432"
        })
        assert result.diagnosis is not None
        assert "PostgreSQL" in result.diagnosis

    def test_diagnose_unknown_pattern(self):
        diagnosis = PatternBasedDiagnosis()
        result = diagnosis.diagnose({"message": "Random error occurred"})
        assert result.diagnosis is None
        assert result.confidence == 0.0

    def test_learn_pattern(self):
        diagnosis = PatternBasedDiagnosis()
        diagnosis.learn_pattern(
            "custom error pattern",
            "Custom diagnosis",
            "Custom fix",
        )
        result = diagnosis.diagnose({"message": "custom error pattern occurred"})
        assert result.diagnosis == "Custom diagnosis"


# =============================================================================
# Tests for SymptomToCauseMapper
# =============================================================================


class TestSymptomToCauseMapper:
    """Tests for SymptomToCauseMapper class."""

    def test_map_single_symptom(self):
        mapper = SymptomToCauseMapper()
        causes = mapper.map(["slow_response"])
        assert "high CPU usage" in causes

    def test_map_multiple_symptoms(self):
        mapper = SymptomToCauseMapper()
        causes = mapper.map(["slow_response", "high_memory"])
        assert len(causes) > 1

    def test_map_with_probability(self):
        mapper = SymptomToCauseMapper()
        causes = mapper.map_with_probability(["connection_timeout"])
        assert causes[0]["probability"] > 0


# =============================================================================
# Tests for OverallHealthDiagnosis
# =============================================================================


class TestOverallHealthDiagnosis:
    """Tests for OverallHealthDiagnosis class."""

    def test_check(self):
        diagnosis = OverallHealthDiagnosis()
        result = diagnosis.check()
        assert "overall_score" in result
        assert "status" in result

    def test_generate_report(self):
        diagnosis = OverallHealthDiagnosis()
        report = diagnosis.generate_report()
        assert "summary" in report
        assert "generated_at" in report


# =============================================================================
# Tests for AutoFixSystem
# =============================================================================


class TestAutoFixSystem:
    """Tests for AutoFixSystem class."""

    def test_init(self):
        fixer = AutoFixSystem()
        assert not fixer.safe_mode

    def test_fix_missing_parenthesis(self):
        fixer = AutoFixSystem()
        code = "print('hello'"
        result = fixer.fix(code, {
            "type": "SyntaxError",
            "message": "unexpected EOF while parsing",
        })
        assert result.fixed is True
        assert ")" in result.fixed_code

    def test_fix_missing_import(self):
        fixer = AutoFixSystem()
        code = "data = json.loads('{}')"
        result = fixer.fix(code, {
            "type": "NameError",
            "message": "name 'json' is not defined",
        })
        assert result.fixed is True
        assert "import json" in result.fixed_code

    def test_fix_safe_mode(self):
        fixer = AutoFixSystem(safe_mode=True)
        code = "print('hello'"
        result = fixer.fix(code, {
            "type": "SyntaxError",
            "message": "unexpected EOF",
        })
        assert result.fixed is False
        assert result.requires_confirmation is True

    def test_fix_unknown_error(self):
        fixer = AutoFixSystem()
        result = fixer.fix("code", {"type": "WeirdError", "message": "weird"})
        assert result.fixed is False


# =============================================================================
# Tests for FixStrategySelector
# =============================================================================


class TestFixStrategySelector:
    """Tests for FixStrategySelector class."""

    def test_select_known_error(self):
        selector = FixStrategySelector()
        strategy = selector.select({"type": "TypeError"})
        assert strategy.name == "type_conversion"

    def test_select_unknown_error(self):
        selector = FixStrategySelector()
        strategy = selector.select({"type": "WeirdError"})
        assert strategy.name == "manual_review"

    def test_get_all_strategies(self):
        selector = FixStrategySelector()
        strategies = selector.get_all_strategies({"type": "TypeError"})
        assert len(strategies) >= 1

    def test_get_ranked_strategies(self):
        selector = FixStrategySelector()
        strategies = selector.get_ranked_strategies({"type": "TypeError"})
        # Should be sorted by confidence descending
        if len(strategies) > 1:
            assert strategies[0].confidence >= strategies[1].confidence


# =============================================================================
# Tests for RollbackMechanism
# =============================================================================


class TestRollbackMechanism:
    """Tests for RollbackMechanism class."""

    def test_create_checkpoint(self):
        rollback = RollbackMechanism()
        checkpoint_id = rollback.create_checkpoint({"value": 1})
        assert len(checkpoint_id) == 8

    def test_rollback(self):
        rollback = RollbackMechanism()
        checkpoint_id = rollback.create_checkpoint({"value": 1})
        state = rollback.rollback(checkpoint_id)
        assert state["value"] == 1

    def test_rollback_unknown_checkpoint(self):
        rollback = RollbackMechanism()
        with pytest.raises(ValueError):
            rollback.rollback("unknown")

    def test_list_checkpoints(self):
        rollback = RollbackMechanism()
        rollback.create_checkpoint({"v": 1})
        rollback.create_checkpoint({"v": 2})
        checkpoints = rollback.list_checkpoints()
        assert len(checkpoints) == 2


# =============================================================================
# Tests for FixValidation
# =============================================================================


class TestFixValidation:
    """Tests for FixValidation class."""

    def test_validate_syntax_correct(self):
        validator = FixValidation()
        result = validator.validate(
            "print('hello'",
            "print('hello')",
        )
        assert result.syntax_correct is True

    def test_validate_syntax_incorrect(self):
        validator = FixValidation()
        result = validator.validate(
            "print('hello'",
            "print('hello'",  # Missing close paren
        )
        assert result.syntax_correct is False
        assert result.is_valid is False

    def test_validate_with_tests(self):
        validator = FixValidation()
        result = validator.validate(
            "def add(a, b): return a + b",
            "def add(a, b): return a + b",
            test_cases=[{"expected": 3}],
        )
        assert result.passes_tests is True


# =============================================================================
# Tests for FixLearningSystem
# =============================================================================


class TestFixLearningSystem:
    """Tests for FixLearningSystem class."""

    def test_record_fix(self):
        learner = FixLearningSystem()
        learner.record_fix("TypeError", "int+str", "convert_type", success=True)
        assert len(learner._fix_history) == 1

    def test_suggest_fix(self):
        learner = FixLearningSystem()
        learner.record_fix("TypeError", "int+str", "convert_type", success=True)
        suggestion = learner.suggest_fix("TypeError", "int+str")
        assert suggestion == "convert_type"

    def test_suggest_fix_no_history(self):
        learner = FixLearningSystem()
        suggestion = learner.suggest_fix("UnknownError", "pattern")
        assert suggestion == []

    def test_get_success_rate(self):
        learner = FixLearningSystem()
        learner.record_fix("TypeError", "pattern", "fix1", success=True)
        learner.record_fix("TypeError", "pattern", "fix1", success=False)
        rate = learner.get_success_rate("fix1")
        assert rate == 0.5


# =============================================================================
# Tests for SelfImprovementOrchestrator
# =============================================================================


class TestSelfImprovementOrchestrator:
    """Tests for SelfImprovementOrchestrator class."""

    def test_init(self):
        orchestrator = SelfImprovementOrchestrator()
        assert orchestrator.assessment_engine is not None
        assert orchestrator.performance_monitor is not None

    def test_run_assessment(self):
        orchestrator = SelfImprovementOrchestrator()
        result = orchestrator.run_assessment()
        assert result.capabilities_evaluated > 0
        assert 0 <= result.average_score <= 1

    def test_run_monitoring_check(self):
        orchestrator = SelfImprovementOrchestrator()
        result = orchestrator.run_monitoring_check()
        assert isinstance(result, MonitoringResult)

    def test_run_diagnosis(self):
        orchestrator = SelfImprovementOrchestrator()
        result = orchestrator.run_diagnosis()
        assert isinstance(result, DiagnosisRunResult)

    def test_run_repair(self):
        orchestrator = SelfImprovementOrchestrator()
        result = orchestrator.run_repair()
        assert isinstance(result, RepairResult)

    def test_generate_improvement_plan(self):
        orchestrator = SelfImprovementOrchestrator()
        plan = orchestrator.generate_improvement_plan()
        assert "priorities" in plan
        assert "timeline" in plan

    def test_create_modification_checkpoint(self):
        orchestrator = SelfImprovementOrchestrator()
        checkpoint_id = orchestrator.create_modification_checkpoint()
        assert len(checkpoint_id) == 8

    def test_apply_safe_modification(self):
        orchestrator = SelfImprovementOrchestrator()
        result = orchestrator.apply_safe_modification(
            "capability_weights",
            {"test_cap": 0.9},
        )
        assert result.applied is True
        assert result.can_rollback is True

    def test_record_improvement(self):
        orchestrator = SelfImprovementOrchestrator()
        orchestrator.record_improvement("accuracy", before=0.7, after=0.8)
        metrics = orchestrator.get_improvement_metrics()
        assert "accuracy" in metrics
        assert metrics["accuracy"]["improvement"] == pytest.approx(0.1)

    def test_detect_capability_gaps(self):
        orchestrator = SelfImprovementOrchestrator()
        gaps = orchestrator.detect_capability_gaps(threshold=0.9)
        assert len(gaps) > 0  # Many capabilities are below 0.9

    def test_plan_capability_improvement(self):
        orchestrator = SelfImprovementOrchestrator()
        plan = orchestrator.plan_capability_improvement("security")
        assert plan.target_score > 0.6
        assert len(plan.steps) > 0

    def test_execute_improvement(self):
        orchestrator = SelfImprovementOrchestrator()
        plan = ImprovementPlan(target_score=0.8, steps=["step1"])
        result = orchestrator.execute_improvement(plan, safe_mode=True)
        assert result.applied is False  # Safe mode prevents application

    def test_continuous_monitoring(self):
        orchestrator = SelfImprovementOrchestrator()
        orchestrator.start_continuous_monitoring(interval_seconds=0.01)
        time.sleep(0.05)
        orchestrator.stop_continuous_monitoring()
        report = orchestrator.get_monitoring_report()
        assert report["event_count"] >= 1

    def test_record_user_feedback(self):
        orchestrator = SelfImprovementOrchestrator()
        orchestrator.record_user_feedback(
            "task1",
            "correction",
            {"expected": "a", "got": "b"},
        )
        learnings = orchestrator.get_learnings()
        assert len(learnings) == 1
        assert learnings[0]["type"] == "correction"
