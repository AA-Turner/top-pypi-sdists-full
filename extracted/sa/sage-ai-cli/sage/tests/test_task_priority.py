"""Tests for sage.core.task_priority module."""

import pytest

from sage.core.task_priority import (
    CheckClass,
    FailureSignature,
    PrioritizedTask,
    TaskCategory,
    TaskPrioritizer,
)


class TestTaskCategory:
    """Test TaskCategory enum."""

    def test_priority_order(self):
        """Test that categories are in correct priority order."""
        # Lower value = higher priority
        assert TaskCategory.SECURITY_CRITICAL.value < TaskCategory.TEST_COLLECTION_ERROR.value
        assert TaskCategory.TEST_COLLECTION_ERROR.value < TaskCategory.BUILD_FAILURE.value
        assert TaskCategory.TEST_FAILURE.value < TaskCategory.LINT_ERROR.value
        assert TaskCategory.LINT_ERROR.value < TaskCategory.TYPE_ERROR.value
        assert TaskCategory.SECURITY_WARNING.value < TaskCategory.ENHANCEMENT.value
        assert TaskCategory.ENHANCEMENT.value < TaskCategory.NICE_TO_HAVE.value

    def test_all_categories_have_values(self):
        """Test that all categories have integer values."""
        for cat in TaskCategory:
            assert isinstance(cat.value, int)


class TestCheckClass:
    """Test CheckClass enum."""

    def test_check_classes_exist(self):
        """Test that expected check classes exist."""
        assert CheckClass.COLLECT is not None
        assert CheckClass.TEST is not None
        assert CheckClass.LINT is not None
        assert CheckClass.TYPE is not None
        assert CheckClass.BUILD is not None
        assert CheckClass.SECURITY is not None


class TestFailureSignature:
    """Test FailureSignature dataclass."""

    def test_create_signature(self):
        """Test creating a failure signature."""
        sig = FailureSignature(
            check_class=CheckClass.TEST,
            error_type="AssertionError",
            file_path="test_foo.py",
            line_number=42,
        )
        assert sig.check_class == CheckClass.TEST
        assert sig.error_type == "AssertionError"
        assert sig.file_path == "test_foo.py"
        assert sig.line_number == 42

    def test_signature_hash(self):
        """Test that signatures are hashable."""
        sig1 = FailureSignature(
            check_class=CheckClass.TEST,
            error_type="AssertionError",
            file_path="test_foo.py",
            line_number=42,
        )
        sig2 = FailureSignature(
            check_class=CheckClass.TEST,
            error_type="AssertionError",
            file_path="test_foo.py",
            line_number=42,
        )
        # Same parameters should have same hash
        assert hash(sig1) == hash(sig2)
        # Can be used in sets
        assert len({sig1, sig2}) == 1


class TestPrioritizedTask:
    """Test PrioritizedTask dataclass."""

    def test_create_task(self):
        """Test creating a prioritized task."""
        task = PrioritizedTask(
            id="task_1",
            description="Fix test failure",
            category=TaskCategory.TEST_FAILURE,
            severity=7,
            blast_radius=3,
            user_impact=8,
        )
        assert task.id == "task_1"
        assert task.category == TaskCategory.TEST_FAILURE
        assert task.severity == 7

    def test_priority_score_calculation(self):
        """Test priority score calculation."""
        task = PrioritizedTask(
            id="task_1",
            description="Test task",
            category=TaskCategory.TEST_FAILURE,
            severity=5,
            blast_radius=2,
            user_impact=5,
        )
        score = task.priority_score
        assert isinstance(score, int)

    def test_blocking_task_has_lower_score(self):
        """Test that blocking tasks have lower (better) priority scores."""
        blocking_task = PrioritizedTask(
            id="task_1",
            description="Blocking task",
            category=TaskCategory.BUILD_FAILURE,
            severity=5,
            blast_radius=2,
            user_impact=5,
            is_blocking=True,
        )
        non_blocking_task = PrioritizedTask(
            id="task_2",
            description="Non-blocking task",
            category=TaskCategory.BUILD_FAILURE,
            severity=5,
            blast_radius=2,
            user_impact=5,
            is_blocking=False,
        )
        # Blocking should have lower (better) score
        assert blocking_task.priority_score < non_blocking_task.priority_score

    def test_higher_severity_has_lower_score(self):
        """Test that higher severity has lower (better) priority score."""
        high_severity = PrioritizedTask(
            id="task_1",
            description="High severity",
            category=TaskCategory.TEST_FAILURE,
            severity=10,
            blast_radius=2,
            user_impact=5,
        )
        low_severity = PrioritizedTask(
            id="task_2",
            description="Low severity",
            category=TaskCategory.TEST_FAILURE,
            severity=2,
            blast_radius=2,
            user_impact=5,
        )
        assert high_severity.priority_score < low_severity.priority_score

    def test_security_critical_has_lowest_score(self):
        """Test that CRITICAL security issues have very low scores."""
        security_task = PrioritizedTask(
            id="task_1",
            description="Security critical",
            category=TaskCategory.SECURITY_CRITICAL,
            severity=10,
            blast_radius=10,
            user_impact=10,
            security_severity="CRITICAL",
        )
        normal_task = PrioritizedTask(
            id="task_2",
            description="Normal task",
            category=TaskCategory.TEST_FAILURE,
            severity=10,
            blast_radius=10,
            user_impact=10,
        )
        assert security_task.priority_score < normal_task.priority_score


class TestTaskPrioritizer:
    """Test TaskPrioritizer class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.prioritizer = TaskPrioritizer()

    def test_classify_collection_error(self):
        """Test classifying test collection errors."""
        error = "ERROR collecting tests/test_foo.py"
        check_class, category = self.prioritizer.classify_error(error)
        assert check_class == CheckClass.COLLECT
        assert category == TaskCategory.TEST_COLLECTION_ERROR

    def test_classify_import_error(self):
        """Test classifying import errors."""
        error = "ModuleNotFoundError: No module named 'foo'"
        check_class, category = self.prioritizer.classify_error(error)
        assert check_class == CheckClass.COLLECT
        assert category == TaskCategory.TEST_COLLECTION_ERROR

    def test_classify_build_failure(self):
        """Test classifying build failures."""
        error = "Build failed: npm ERR! code ELIFECYCLE"
        check_class, category = self.prioritizer.classify_error(error)
        assert check_class == CheckClass.BUILD
        assert category == TaskCategory.BUILD_FAILURE

    def test_classify_test_failure(self):
        """Test classifying test failures."""
        error = "FAILED tests/test_foo.py::test_bar - AssertionError"
        check_class, category = self.prioritizer.classify_error(error)
        assert check_class == CheckClass.TEST
        assert category == TaskCategory.TEST_FAILURE

    def test_classify_security_issue(self):
        """Test classifying security issues."""
        error = "CRITICAL vulnerability CVE-2024-1234 detected"
        check_class, category = self.prioritizer.classify_error(error)
        assert check_class == CheckClass.SECURITY
        assert category == TaskCategory.SECURITY_CRITICAL

    def test_classify_lint_error(self):
        """Test classifying lint errors."""
        error = "ruff: E501 line too long"
        check_class, category = self.prioritizer.classify_error(error)
        assert check_class == CheckClass.LINT
        assert category == TaskCategory.LINT_ERROR

    def test_classify_type_error(self):
        """Test classifying type errors."""
        error = "mypy: error: Argument 1 has incompatible type"
        check_class, category = self.prioritizer.classify_error(error)
        assert check_class == CheckClass.TYPE
        assert category == TaskCategory.TYPE_ERROR

    def test_extract_affected_files(self):
        """Test extracting affected files from error output."""
        error = """
tests/test_foo.py:10: in test_bar
    assert x == y
AssertionError
File "src/utils.py", line 42
"""
        files = self.prioritizer.extract_affected_files(error)
        assert "tests/test_foo.py" in files or "test_foo.py" in files
        assert "src/utils.py" in files or "utils.py" in files

    def test_calculate_blast_radius(self):
        """Test blast radius calculation."""
        files = ["foo.py", "bar.py", "baz.py"]
        radius = self.prioritizer.calculate_blast_radius(files)
        assert radius == 3

    def test_calculate_blast_radius_with_dependencies(self):
        """Test blast radius includes dependents."""
        self.prioritizer.update_dependency_graph(
            {
                "foo.py": {"bar.py", "baz.py"},
            }
        )
        files = ["foo.py"]
        radius = self.prioritizer.calculate_blast_radius(files)
        assert radius == 3  # foo.py + bar.py + baz.py

    def test_prioritize_tasks(self):
        """Test task prioritization from error outputs."""
        errors = [
            "ERROR collecting tests/test_foo.py - ImportError",
            "FAILED tests/test_bar.py::test_baz - AssertionError",
        ]
        tasks = self.prioritizer.prioritize_tasks(errors, baseline_green=False)

        assert len(tasks) == 2
        # Collection error should be first (higher priority)
        assert tasks[0].category == TaskCategory.TEST_COLLECTION_ERROR
        assert tasks[1].category == TaskCategory.TEST_FAILURE

    def test_should_allow_improvements_when_green(self):
        """Test that improvements are allowed when baseline is green."""
        assert (
            self.prioritizer.should_allow_improvements(
                baseline_green=True,
                pending_tasks=[],
            )
            is True
        )

    def test_should_block_improvements_when_red(self):
        """Test that improvements are blocked when baseline is red."""
        assert (
            self.prioritizer.should_allow_improvements(
                baseline_green=False,
                pending_tasks=[],
            )
            is False
        )

    def test_should_block_improvements_with_blocking_tasks(self):
        """Test that improvements are blocked when blocking tasks exist."""
        blocking_task = PrioritizedTask(
            id="task_1",
            description="Blocking",
            category=TaskCategory.BUILD_FAILURE,
            severity=10,
            blast_radius=5,
            user_impact=10,
            is_blocking=True,
        )
        assert (
            self.prioritizer.should_allow_improvements(
                baseline_green=True,
                pending_tasks=[blocking_task],
            )
            is False
        )

    def test_should_block_improvements_with_failing_tests(self):
        """Test that improvements are blocked when test failures exist."""
        failing_test = PrioritizedTask(
            id="task_1",
            description="Failing test",
            category=TaskCategory.TEST_FAILURE,
            severity=7,
            blast_radius=2,
            user_impact=5,
        )
        assert (
            self.prioritizer.should_allow_improvements(
                baseline_green=True,
                pending_tasks=[failing_test],
            )
            is False
        )

    def test_record_and_clear_failure(self):
        """Test recording and clearing failures."""
        error = "FAILED tests/test_foo.py::test_bar"

        # Record failure
        self.prioritizer.record_failure(error)
        freq = self.prioritizer._get_failure_frequency(error)
        assert freq == 1

        # Record again
        self.prioritizer.record_failure(error)
        freq = self.prioritizer._get_failure_frequency(error)
        assert freq == 2

        # Clear failure
        self.prioritizer.clear_failure(error)
        freq = self.prioritizer._get_failure_frequency(error)
        assert freq == 0

    def test_is_regression(self):
        """Test regression detection."""
        task = PrioritizedTask(
            id="task_1",
            description="Test",
            category=TaskCategory.TEST_FAILURE,
            severity=7,
            blast_radius=2,
            user_impact=5,
            affected_files=["foo.py"],
        )
        previous_state = {"foo.py": True}  # Was passing
        assert self.prioritizer.is_regression(task, previous_state) is True

        previous_state = {"foo.py": False}  # Was already failing
        assert self.prioritizer.is_regression(task, previous_state) is False

    def test_extract_security_severity(self):
        """Test security severity extraction."""
        assert self.prioritizer._extract_security_severity("CRITICAL vuln") == "CRITICAL"
        assert self.prioritizer._extract_security_severity("HIGH risk") == "HIGH"
        assert self.prioritizer._extract_security_severity("MEDIUM issue") == "MEDIUM"
        assert self.prioritizer._extract_security_severity("LOW priority") == "LOW"
        assert self.prioritizer._extract_security_severity("normal text") is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
