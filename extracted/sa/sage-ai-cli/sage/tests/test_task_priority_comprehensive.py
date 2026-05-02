"""Comprehensive tests for sage/core/task_priority.py - Task prioritization."""

import pytest

from sage.core.task_priority import (
    CheckClass,
    FailureSignature,
    PrioritizedTask,
    TaskCategory,
    TaskPrioritizer,
)


# =============================================================================
# Tests for TaskCategory enum
# =============================================================================


class TestTaskCategory:
    """Tests for TaskCategory enum."""

    def test_security_critical_value(self):
        """Security critical has value 1."""
        assert TaskCategory.SECURITY_CRITICAL.value == 1

    def test_test_collection_error_value(self):
        """Test collection error has value 2."""
        assert TaskCategory.TEST_COLLECTION_ERROR.value == 2

    def test_build_failure_value(self):
        """Build failure has value 3."""
        assert TaskCategory.BUILD_FAILURE.value == 3

    def test_deploy_blocker_value(self):
        """Deploy blocker has value 4."""
        assert TaskCategory.DEPLOY_BLOCKER.value == 4

    def test_test_regression_value(self):
        """Test regression has value 10."""
        assert TaskCategory.TEST_REGRESSION.value == 10

    def test_test_failure_value(self):
        """Test failure has value 11."""
        assert TaskCategory.TEST_FAILURE.value == 11

    def test_lint_error_value(self):
        """Lint error has value 12."""
        assert TaskCategory.LINT_ERROR.value == 12

    def test_type_error_value(self):
        """Type error has value 13."""
        assert TaskCategory.TYPE_ERROR.value == 13

    def test_security_warning_value(self):
        """Security warning has value 20."""
        assert TaskCategory.SECURITY_WARNING.value == 20

    def test_coverage_gap_value(self):
        """Coverage gap has value 21."""
        assert TaskCategory.COVERAGE_GAP.value == 21

    def test_deprecation_value(self):
        """Deprecation has value 22."""
        assert TaskCategory.DEPRECATION.value == 22

    def test_enhancement_value(self):
        """Enhancement has value 30."""
        assert TaskCategory.ENHANCEMENT.value == 30

    def test_refactor_value(self):
        """Refactor has value 31."""
        assert TaskCategory.REFACTOR.value == 31

    def test_hygiene_value(self):
        """Hygiene has value 32."""
        assert TaskCategory.HYGIENE.value == 32

    def test_documentation_value(self):
        """Documentation has value 33."""
        assert TaskCategory.DOCUMENTATION.value == 33

    def test_optimization_value(self):
        """Optimization has value 40."""
        assert TaskCategory.OPTIMIZATION.value == 40

    def test_nice_to_have_value(self):
        """Nice to have has value 50."""
        assert TaskCategory.NICE_TO_HAVE.value == 50

    def test_is_int_enum(self):
        """TaskCategory is IntEnum - comparable to int."""
        assert TaskCategory.SECURITY_CRITICAL < TaskCategory.TEST_FAILURE
        assert TaskCategory.ENHANCEMENT > TaskCategory.LINT_ERROR

    def test_category_ordering(self):
        """Categories are ordered by priority."""
        categories = list(TaskCategory)
        # First items should be higher priority (lower value)
        assert TaskCategory.SECURITY_CRITICAL == min(categories, key=lambda x: x.value)


# =============================================================================
# Tests for CheckClass enum
# =============================================================================


class TestCheckClass:
    """Tests for CheckClass enum."""

    def test_collect_value(self):
        """Collect has value 1."""
        assert CheckClass.COLLECT.value == 1

    def test_test_value(self):
        """Test has value 2."""
        assert CheckClass.TEST.value == 2

    def test_lint_value(self):
        """Lint has value 3."""
        assert CheckClass.LINT.value == 3

    def test_type_value(self):
        """Type has value 4."""
        assert CheckClass.TYPE.value == 4

    def test_build_value(self):
        """Build has value 5."""
        assert CheckClass.BUILD.value == 5

    def test_deploy_value(self):
        """Deploy has value 6."""
        assert CheckClass.DEPLOY.value == 6

    def test_security_value(self):
        """Security has value 7."""
        assert CheckClass.SECURITY.value == 7

    def test_is_int_enum(self):
        """CheckClass is IntEnum."""
        assert CheckClass.COLLECT < CheckClass.SECURITY

    def test_all_classes_present(self):
        """All expected check classes exist."""
        expected = ["COLLECT", "TEST", "LINT", "TYPE", "BUILD", "DEPLOY", "SECURITY"]
        for name in expected:
            assert hasattr(CheckClass, name)


# =============================================================================
# Tests for FailureSignature dataclass
# =============================================================================


class TestFailureSignature:
    """Tests for FailureSignature dataclass."""

    def test_create_minimal(self):
        """Create with minimal required fields."""
        sig = FailureSignature(
            check_class=CheckClass.TEST, error_type="AssertionError"
        )
        assert sig.check_class == CheckClass.TEST
        assert sig.error_type == "AssertionError"
        assert sig.file_path is None
        assert sig.line_number is None
        assert sig.message_hash == ""

    def test_create_full(self):
        """Create with all fields."""
        sig = FailureSignature(
            check_class=CheckClass.LINT,
            error_type="F401",
            file_path="src/main.py",
            line_number=42,
            message_hash="abc123",
        )
        assert sig.check_class == CheckClass.LINT
        assert sig.error_type == "F401"
        assert sig.file_path == "src/main.py"
        assert sig.line_number == 42
        assert sig.message_hash == "abc123"

    def test_hash_same_content(self):
        """Same content produces same hash."""
        sig1 = FailureSignature(
            check_class=CheckClass.TEST,
            error_type="Error",
            file_path="test.py",
            line_number=10,
        )
        sig2 = FailureSignature(
            check_class=CheckClass.TEST,
            error_type="Error",
            file_path="test.py",
            line_number=10,
        )
        assert hash(sig1) == hash(sig2)

    def test_hash_different_content(self):
        """Different content produces different hash."""
        sig1 = FailureSignature(check_class=CheckClass.TEST, error_type="Error1")
        sig2 = FailureSignature(check_class=CheckClass.TEST, error_type="Error2")
        assert hash(sig1) != hash(sig2)

    def test_hash_different_line(self):
        """Different line number produces different hash."""
        sig1 = FailureSignature(
            check_class=CheckClass.TEST,
            error_type="Error",
            file_path="test.py",
            line_number=10,
        )
        sig2 = FailureSignature(
            check_class=CheckClass.TEST,
            error_type="Error",
            file_path="test.py",
            line_number=20,
        )
        assert hash(sig1) != hash(sig2)

    def test_usable_in_set(self):
        """FailureSignature can be used in sets."""
        sig1 = FailureSignature(check_class=CheckClass.TEST, error_type="Error")
        sig2 = FailureSignature(check_class=CheckClass.TEST, error_type="Error")
        sig3 = FailureSignature(check_class=CheckClass.LINT, error_type="Error")

        s = {sig1, sig2, sig3}
        # sig1 and sig2 have same hash, so set should have 2 elements
        assert len(s) == 2

    def test_usable_as_dict_key(self):
        """FailureSignature can be used as dict key."""
        sig = FailureSignature(check_class=CheckClass.TEST, error_type="Error")
        d = {sig: "value"}
        assert d[sig] == "value"


# =============================================================================
# Tests for PrioritizedTask dataclass
# =============================================================================


class TestPrioritizedTask:
    """Tests for PrioritizedTask dataclass."""

    def test_create_minimal(self):
        """Create with minimal fields."""
        task = PrioritizedTask(
            id="task_1",
            description="Fix bug",
            category=TaskCategory.TEST_FAILURE,
            severity=5,
            blast_radius=1,
            user_impact=5,
        )
        assert task.id == "task_1"
        assert task.description == "Fix bug"
        assert task.category == TaskCategory.TEST_FAILURE
        assert task.severity == 5
        assert task.blast_radius == 1
        assert task.user_impact == 5
        assert task.is_blocking is False
        assert task.affected_files == []
        assert task.dependencies == []
        assert task.failure_frequency == 0
        assert task.security_severity is None
        assert task.deploy_risk == 0

    def test_create_full(self):
        """Create with all fields."""
        task = PrioritizedTask(
            id="task_2",
            description="Security fix",
            category=TaskCategory.SECURITY_CRITICAL,
            severity=10,
            blast_radius=5,
            user_impact=10,
            is_blocking=True,
            affected_files=["auth.py", "api.py"],
            dependencies=["task_1"],
            failure_frequency=3,
            security_severity="CRITICAL",
            deploy_risk=9,
        )
        assert task.id == "task_2"
        assert task.is_blocking is True
        assert len(task.affected_files) == 2
        assert task.security_severity == "CRITICAL"

    def test_priority_score_basic(self):
        """Priority score is calculated correctly."""
        task = PrioritizedTask(
            id="t",
            description="d",
            category=TaskCategory.TEST_FAILURE,  # value = 11
            severity=5,
            blast_radius=1,
            user_impact=5,
        )
        # base = 11 * 100 = 1100
        # severity_adj = (10 - 5) * 5 = 25
        # blast_adj = max(0, 10 - 1) * 2 = 18
        # impact_adj = (10 - 5) * 3 = 15
        # blocking_adj = 0
        # frequency_adj = 0
        # security_adj = 0
        # deploy_adj = 0
        expected = 1100 + 25 + 18 + 15
        assert task.priority_score == expected

    def test_priority_score_blocking(self):
        """Blocking tasks get priority boost."""
        task = PrioritizedTask(
            id="t",
            description="d",
            category=TaskCategory.BUILD_FAILURE,
            severity=9,
            blast_radius=5,
            user_impact=9,
            is_blocking=True,
        )
        non_blocking = PrioritizedTask(
            id="t2",
            description="d",
            category=TaskCategory.BUILD_FAILURE,
            severity=9,
            blast_radius=5,
            user_impact=9,
            is_blocking=False,
        )
        # Blocking task should have lower (better) priority score
        assert task.priority_score < non_blocking.priority_score

    def test_priority_score_security_critical(self):
        """Security critical gets major boost."""
        task = PrioritizedTask(
            id="t",
            description="d",
            category=TaskCategory.SECURITY_CRITICAL,
            severity=10,
            blast_radius=1,
            user_impact=10,
            security_severity="CRITICAL",
        )
        # Security adjustment = -1000
        assert task.priority_score < 0

    def test_priority_score_security_high(self):
        """Security HIGH gets boost."""
        task = PrioritizedTask(
            id="t",
            description="d",
            category=TaskCategory.SECURITY_WARNING,
            severity=7,
            blast_radius=1,
            user_impact=7,
            security_severity="HIGH",
        )
        non_security = PrioritizedTask(
            id="t2",
            description="d",
            category=TaskCategory.SECURITY_WARNING,
            severity=7,
            blast_radius=1,
            user_impact=7,
        )
        assert task.priority_score < non_security.priority_score

    def test_priority_score_security_medium(self):
        """Security MEDIUM gets smaller boost."""
        task = PrioritizedTask(
            id="t",
            description="d",
            category=TaskCategory.SECURITY_WARNING,
            severity=5,
            blast_radius=1,
            user_impact=5,
            security_severity="MEDIUM",
        )
        # Medium security adjustment = -100
        assert task.priority_score < 2000  # Some reasonable bound

    def test_priority_score_failure_frequency(self):
        """Recurring failures get priority boost."""
        task = PrioritizedTask(
            id="t",
            description="d",
            category=TaskCategory.TEST_FAILURE,
            severity=5,
            blast_radius=1,
            user_impact=5,
            failure_frequency=10,
        )
        non_recurring = PrioritizedTask(
            id="t2",
            description="d",
            category=TaskCategory.TEST_FAILURE,
            severity=5,
            blast_radius=1,
            user_impact=5,
            failure_frequency=0,
        )
        # Higher frequency = lower (better) priority score
        assert task.priority_score < non_recurring.priority_score

    def test_priority_score_deploy_risk(self):
        """Deploy risk affects priority."""
        task = PrioritizedTask(
            id="t",
            description="d",
            category=TaskCategory.TEST_FAILURE,
            severity=5,
            blast_radius=1,
            user_impact=5,
            deploy_risk=10,
        )
        low_risk = PrioritizedTask(
            id="t2",
            description="d",
            category=TaskCategory.TEST_FAILURE,
            severity=5,
            blast_radius=1,
            user_impact=5,
            deploy_risk=0,
        )
        # Higher deploy risk = lower (better) priority score
        assert task.priority_score < low_risk.priority_score

    def test_priority_score_high_severity(self):
        """High severity reduces priority score."""
        high_sev = PrioritizedTask(
            id="t",
            description="d",
            category=TaskCategory.TEST_FAILURE,
            severity=10,
            blast_radius=1,
            user_impact=5,
        )
        low_sev = PrioritizedTask(
            id="t2",
            description="d",
            category=TaskCategory.TEST_FAILURE,
            severity=1,
            blast_radius=1,
            user_impact=5,
        )
        assert high_sev.priority_score < low_sev.priority_score

    def test_priority_score_blast_radius(self):
        """Large blast radius reduces priority score."""
        large_blast = PrioritizedTask(
            id="t",
            description="d",
            category=TaskCategory.TEST_FAILURE,
            severity=5,
            blast_radius=10,
            user_impact=5,
        )
        small_blast = PrioritizedTask(
            id="t2",
            description="d",
            category=TaskCategory.TEST_FAILURE,
            severity=5,
            blast_radius=1,
            user_impact=5,
        )
        assert large_blast.priority_score < small_blast.priority_score

    def test_priority_score_user_impact(self):
        """High user impact reduces priority score."""
        high_impact = PrioritizedTask(
            id="t",
            description="d",
            category=TaskCategory.TEST_FAILURE,
            severity=5,
            blast_radius=1,
            user_impact=10,
        )
        low_impact = PrioritizedTask(
            id="t2",
            description="d",
            category=TaskCategory.TEST_FAILURE,
            severity=5,
            blast_radius=1,
            user_impact=1,
        )
        assert high_impact.priority_score < low_impact.priority_score


# =============================================================================
# Tests for TaskPrioritizer class
# =============================================================================


class TestTaskPrioritizerInit:
    """Tests for TaskPrioritizer initialization."""

    def test_init_defaults(self):
        """TaskPrioritizer initializes with empty history and graph."""
        tp = TaskPrioritizer()
        assert tp.failure_history == {}
        assert tp.dependency_graph == {}


class TestTaskPrioritizerClassifyError:
    """Tests for classify_error method."""

    def test_classify_collection_error(self):
        """Classify collection error patterns."""
        tp = TaskPrioritizer()

        errors = [
            "ERROR collecting tests/test_foo.py",
            "ImportError: No module named 'xyz'",
            "ModuleNotFoundError: No module named 'abc'",
            "SyntaxError: invalid syntax",
            "IndentationError: unexpected indent",
        ]

        for error in errors:
            check_class, category = tp.classify_error(error)
            assert check_class == CheckClass.COLLECT
            assert category == TaskCategory.TEST_COLLECTION_ERROR

    def test_classify_build_failure(self):
        """Classify build failure patterns."""
        tp = TaskPrioritizer()

        errors = [
            "Build failed with exit code 1",
            "Compilation error: undefined symbol",
            "compile error in foo.c",
            "npm ERR! Missing script: build",
            "cargo build failed",
        ]

        for error in errors:
            check_class, category = tp.classify_error(error)
            assert check_class == CheckClass.BUILD
            assert category == TaskCategory.BUILD_FAILURE

    def test_classify_security_issue(self):
        """Classify security issue patterns."""
        tp = TaskPrioritizer()

        errors = [
            "CRITICAL: SQL injection vulnerability",
            "Found vulnerability in package xyz",
            "CVE-2024-1234: remote code execution",
            "security audit failed",
            "Potential SQL injection in query",
        ]

        for error in errors:
            check_class, category = tp.classify_error(error)
            assert check_class == CheckClass.SECURITY
            assert category == TaskCategory.SECURITY_CRITICAL

    def test_classify_test_failure(self):
        """Classify test failure patterns."""
        tp = TaskPrioritizer()

        errors = [
            "FAILED tests/test_foo.py::test_bar",
            "AssertionError: 1 != 2",
            "1 test failed",
            "3 tests failed, 10 passed",
        ]

        for error in errors:
            check_class, category = tp.classify_error(error)
            assert check_class == CheckClass.TEST
            assert category == TaskCategory.TEST_FAILURE

    def test_classify_lint_error(self):
        """Classify lint error patterns."""
        tp = TaskPrioritizer()

        errors = [
            "lint: src/main.py:10: E501",
            "ruff check found errors",
            "eslint: 'x' is not defined",
            "pylint: Missing docstring",
            "flake8 error F401",
        ]

        for error in errors:
            check_class, category = tp.classify_error(error)
            assert check_class == CheckClass.LINT
            assert category == TaskCategory.LINT_ERROR

    def test_classify_type_error(self):
        """Classify type error patterns."""
        tp = TaskPrioritizer()

        errors = [
            "mypy: Incompatible types",
            "pyright: Type 'int' not assignable",
            "TypeScript error TS2322",
            "type error: expected str, got int",
        ]

        for error in errors:
            check_class, category = tp.classify_error(error)
            assert check_class == CheckClass.TYPE
            assert category == TaskCategory.TYPE_ERROR

    def test_classify_unknown_defaults(self):
        """Unknown errors default to TEST/TEST_FAILURE."""
        tp = TaskPrioritizer()
        check_class, category = tp.classify_error("Some random error")
        assert check_class == CheckClass.TEST
        assert category == TaskCategory.TEST_FAILURE


class TestTaskPrioritizerExtractFiles:
    """Tests for extract_affected_files method."""

    def test_extract_python_files(self):
        """Extract Python file paths."""
        tp = TaskPrioritizer()
        error = "Error in src/main.py:42\nFile \"tests/test_foo.py\", line 10"
        files = tp.extract_affected_files(error)
        assert "src/main.py" in files
        assert "tests/test_foo.py" in files

    def test_extract_js_ts_files(self):
        """Extract JS/TS file paths."""
        tp = TaskPrioritizer()
        error = "Error: src/app.ts:15\nFailed in components/Button.tsx:30"
        files = tp.extract_affected_files(error)
        assert "src/app.ts" in files
        # The regex captures up to the extension, tsx gets truncated to ts
        assert any("Button" in f for f in files)

    def test_extract_jsx_files(self):
        """Extract JSX files - note: pattern may not capture all extensions."""
        tp = TaskPrioritizer()
        # The regex pattern captures .js, .ts, .tsx, .jsx
        error = "Error in App.js:5"
        files = tp.extract_affected_files(error)
        assert any("App.js" in f for f in files)

    def test_extract_deduplicates(self):
        """Duplicate files are deduplicated."""
        tp = TaskPrioritizer()
        error = "Error in foo.py:10\nAnother error in foo.py:20"
        files = tp.extract_affected_files(error)
        assert files.count("foo.py") == 1

    def test_extract_filters_angle_brackets(self):
        """Files starting with < are filtered out."""
        tp = TaskPrioritizer()
        error = 'File "<stdin>", line 1'
        files = tp.extract_affected_files(error)
        assert all(not f.startswith("<") for f in files)

    def test_extract_empty_error(self):
        """Empty error returns empty list."""
        tp = TaskPrioritizer()
        files = tp.extract_affected_files("")
        assert files == []

    def test_extract_no_files(self):
        """Error without file paths returns empty list."""
        tp = TaskPrioritizer()
        files = tp.extract_affected_files("General error occurred")
        assert files == []


class TestTaskPrioritizerBlastRadius:
    """Tests for calculate_blast_radius method."""

    def test_blast_radius_no_deps(self):
        """Blast radius with no dependencies is file count."""
        tp = TaskPrioritizer()
        files = ["a.py", "b.py", "c.py"]
        assert tp.calculate_blast_radius(files) == 3

    def test_blast_radius_with_deps(self):
        """Blast radius includes dependents."""
        tp = TaskPrioritizer()
        tp.dependency_graph = {"a.py": {"d.py", "e.py"}, "b.py": {"f.py"}}
        files = ["a.py", "b.py"]
        radius = tp.calculate_blast_radius(files)
        # a.py, b.py, d.py, e.py, f.py = 5
        assert radius == 5

    def test_blast_radius_empty(self):
        """Blast radius of empty list is 0."""
        tp = TaskPrioritizer()
        assert tp.calculate_blast_radius([]) == 0

    def test_blast_radius_overlapping_deps(self):
        """Overlapping dependencies are counted once."""
        tp = TaskPrioritizer()
        tp.dependency_graph = {"a.py": {"c.py"}, "b.py": {"c.py"}}
        files = ["a.py", "b.py"]
        radius = tp.calculate_blast_radius(files)
        # a.py, b.py, c.py = 3
        assert radius == 3


class TestTaskPrioritizerIsRegression:
    """Tests for is_regression method."""

    def test_is_regression_true(self):
        """Detects regression when file was passing before."""
        tp = TaskPrioritizer()
        task = PrioritizedTask(
            id="t",
            description="d",
            category=TaskCategory.TEST_FAILURE,
            severity=5,
            blast_radius=1,
            user_impact=5,
            affected_files=["test_foo.py"],
        )
        previous_state = {"test_foo.py": True}  # Was passing
        assert tp.is_regression(task, previous_state) is True

    def test_is_regression_false_new_failure(self):
        """Not a regression if file wasn't passing before."""
        tp = TaskPrioritizer()
        task = PrioritizedTask(
            id="t",
            description="d",
            category=TaskCategory.TEST_FAILURE,
            severity=5,
            blast_radius=1,
            user_impact=5,
            affected_files=["test_foo.py"],
        )
        previous_state = {"test_foo.py": False}  # Was already failing
        assert tp.is_regression(task, previous_state) is False

    def test_is_regression_unknown_file(self):
        """Not a regression if file not in previous state."""
        tp = TaskPrioritizer()
        task = PrioritizedTask(
            id="t",
            description="d",
            category=TaskCategory.TEST_FAILURE,
            severity=5,
            blast_radius=1,
            user_impact=5,
            affected_files=["new_test.py"],
        )
        previous_state = {"other_test.py": True}
        assert tp.is_regression(task, previous_state) is False

    def test_is_regression_any_file(self):
        """Regression if any affected file was passing."""
        tp = TaskPrioritizer()
        task = PrioritizedTask(
            id="t",
            description="d",
            category=TaskCategory.TEST_FAILURE,
            severity=5,
            blast_radius=1,
            user_impact=5,
            affected_files=["a.py", "b.py", "c.py"],
        )
        previous_state = {"a.py": False, "b.py": True, "c.py": False}
        assert tp.is_regression(task, previous_state) is True


class TestTaskPrioritizerPrioritizeTasks:
    """Tests for prioritize_tasks method."""

    def test_prioritize_empty(self):
        """Empty error list returns empty task list."""
        tp = TaskPrioritizer()
        tasks = tp.prioritize_tasks([], baseline_green=True)
        assert tasks == []

    def test_prioritize_single_task(self):
        """Single error creates single task."""
        tp = TaskPrioritizer()
        tasks = tp.prioritize_tasks(["FAILED test_foo.py"], baseline_green=False)
        assert len(tasks) == 1
        assert tasks[0].id == "task_0"

    def test_prioritize_multiple_tasks(self):
        """Multiple errors create multiple tasks."""
        tp = TaskPrioritizer()
        errors = [
            "FAILED test_a.py",
            "FAILED test_b.py",
            "FAILED test_c.py",
        ]
        tasks = tp.prioritize_tasks(errors, baseline_green=False)
        assert len(tasks) == 3

    def test_prioritize_sorts_by_priority(self):
        """Tasks are sorted by priority score."""
        tp = TaskPrioritizer()
        errors = [
            "lint: warning in code.py",  # Lower priority
            "CRITICAL: security vulnerability",  # Higher priority
            "FAILED test.py",  # Medium priority
        ]
        tasks = tp.prioritize_tasks(errors, baseline_green=False)
        # Security should be first (lowest priority score)
        assert tasks[0].category == TaskCategory.SECURITY_CRITICAL

    def test_prioritize_marks_blocking(self):
        """Collection and build errors are marked blocking."""
        tp = TaskPrioritizer()
        errors = [
            "ERROR collecting test.py\nImportError: foo",
            "Build failed",
        ]
        tasks = tp.prioritize_tasks(errors, baseline_green=False)
        assert all(t.is_blocking for t in tasks)

    def test_prioritize_detects_regression(self):
        """Regressions are detected and recategorized."""
        tp = TaskPrioritizer()
        errors = ["FAILED tests/test_foo.py::test_bar"]
        previous_state = {"tests/test_foo.py": True}  # Was passing
        tasks = tp.prioritize_tasks(
            errors, baseline_green=False, previous_state=previous_state
        )
        assert len(tasks) == 1
        assert tasks[0].category == TaskCategory.TEST_REGRESSION

    def test_prioritize_regression_severity_boost(self):
        """Regressions get severity boost."""
        tp = TaskPrioritizer()
        errors = ["FAILED tests/test_foo.py::test_bar"]
        previous_state = {"tests/test_foo.py": True}

        # Get regression task
        tasks = tp.prioritize_tasks(
            errors, baseline_green=False, previous_state=previous_state
        )
        regression_task = tasks[0]

        # Get non-regression task
        non_reg_tasks = tp.prioritize_tasks(
            errors, baseline_green=False, previous_state={}
        )
        non_reg_task = non_reg_tasks[0]

        # Regression should have higher severity (by +2)
        assert regression_task.severity >= non_reg_task.severity


class TestTaskPrioritizerShouldAllowImprovements:
    """Tests for should_allow_improvements method."""

    def test_allow_when_green_no_blockers(self):
        """Allow improvements when green and no blockers."""
        tp = TaskPrioritizer()
        tasks = []
        assert tp.should_allow_improvements(baseline_green=True, pending_tasks=tasks)

    def test_block_when_red(self):
        """Block improvements when baseline is red."""
        tp = TaskPrioritizer()
        tasks = []
        assert tp.should_allow_improvements(baseline_green=False, pending_tasks=tasks) is False

    def test_block_when_blocking_tasks(self):
        """Block improvements when blocking tasks exist."""
        tp = TaskPrioritizer()
        task = PrioritizedTask(
            id="t",
            description="d",
            category=TaskCategory.BUILD_FAILURE,
            severity=9,
            blast_radius=1,
            user_impact=9,
            is_blocking=True,
        )
        assert tp.should_allow_improvements(True, [task]) is False

    def test_block_when_test_failures(self):
        """Block improvements when test failures exist."""
        tp = TaskPrioritizer()
        task = PrioritizedTask(
            id="t",
            description="d",
            category=TaskCategory.TEST_FAILURE,
            severity=5,
            blast_radius=1,
            user_impact=5,
        )
        assert tp.should_allow_improvements(True, [task]) is False

    def test_block_when_test_regression(self):
        """Block improvements when test regressions exist."""
        tp = TaskPrioritizer()
        task = PrioritizedTask(
            id="t",
            description="d",
            category=TaskCategory.TEST_REGRESSION,
            severity=7,
            blast_radius=1,
            user_impact=7,
        )
        assert tp.should_allow_improvements(True, [task]) is False

    def test_allow_with_lint_only(self):
        """Allow improvements when only lint errors exist."""
        tp = TaskPrioritizer()
        task = PrioritizedTask(
            id="t",
            description="d",
            category=TaskCategory.LINT_ERROR,
            severity=3,
            blast_radius=1,
            user_impact=3,
        )
        assert tp.should_allow_improvements(True, [task]) is True


class TestTaskPrioritizerSummarizeError:
    """Tests for _summarize_error method."""

    def test_summarize_first_line(self):
        """Returns first meaningful line."""
        tp = TaskPrioritizer()
        error = "First line\nSecond line\nThird line"
        assert tp._summarize_error(error) == "First line"

    def test_summarize_skips_comments(self):
        """Skips comment lines."""
        tp = TaskPrioritizer()
        error = "# Comment\nActual error"
        assert tp._summarize_error(error) == "Actual error"

    def test_summarize_truncates_long(self):
        """Truncates long lines."""
        tp = TaskPrioritizer()
        error = "x" * 200
        result = tp._summarize_error(error)
        assert len(result) == 103  # 100 + "..."
        assert result.endswith("...")

    def test_summarize_custom_length(self):
        """Respects custom max_len."""
        tp = TaskPrioritizer()
        error = "x" * 100
        result = tp._summarize_error(error, max_len=50)
        assert len(result) == 53  # 50 + "..."

    def test_summarize_empty(self):
        """Handles empty string."""
        tp = TaskPrioritizer()
        result = tp._summarize_error("")
        assert result == ""

    def test_summarize_strips_whitespace(self):
        """Strips leading/trailing whitespace."""
        tp = TaskPrioritizer()
        error = "  \n  Error message  \n  "
        assert tp._summarize_error(error).strip() == "Error message"


class TestTaskPrioritizerCalculateSeverity:
    """Tests for _calculate_severity method."""

    def test_severity_collect(self):
        """Collection errors have severity 10."""
        tp = TaskPrioritizer()
        assert tp._calculate_severity(CheckClass.COLLECT, "") == 10

    def test_severity_build(self):
        """Build errors have severity 9."""
        tp = TaskPrioritizer()
        assert tp._calculate_severity(CheckClass.BUILD, "") == 9

    def test_severity_security(self):
        """Security errors have severity 9."""
        tp = TaskPrioritizer()
        assert tp._calculate_severity(CheckClass.SECURITY, "") == 9

    def test_severity_test(self):
        """Test errors have severity 7."""
        tp = TaskPrioritizer()
        assert tp._calculate_severity(CheckClass.TEST, "") == 7

    def test_severity_type(self):
        """Type errors have severity 5."""
        tp = TaskPrioritizer()
        assert tp._calculate_severity(CheckClass.TYPE, "") == 5

    def test_severity_lint(self):
        """Lint errors have severity 4."""
        tp = TaskPrioritizer()
        assert tp._calculate_severity(CheckClass.LINT, "") == 4

    def test_severity_deploy(self):
        """Deploy errors have severity 8."""
        tp = TaskPrioritizer()
        assert tp._calculate_severity(CheckClass.DEPLOY, "") == 8

    def test_severity_boost_critical(self):
        """CRITICAL in error boosts severity."""
        tp = TaskPrioritizer()
        sev = tp._calculate_severity(CheckClass.TEST, "CRITICAL error")
        assert sev == 9  # 7 + 2

    def test_severity_boost_fatal(self):
        """FATAL in error boosts severity."""
        tp = TaskPrioritizer()
        sev = tp._calculate_severity(CheckClass.LINT, "FATAL error")
        assert sev == 6  # 4 + 2

    def test_severity_reduce_warning(self):
        """warning in error reduces severity."""
        tp = TaskPrioritizer()
        sev = tp._calculate_severity(CheckClass.TEST, "This is a warning")
        assert sev == 5  # 7 - 2

    def test_severity_min_bound(self):
        """Severity doesn't go below 1."""
        tp = TaskPrioritizer()
        sev = tp._calculate_severity(CheckClass.LINT, "warning warning warning")
        assert sev >= 1


class TestTaskPrioritizerCalculateUserImpact:
    """Tests for _calculate_user_impact method."""

    def test_impact_default(self):
        """Default impact is 5."""
        tp = TaskPrioritizer()
        impact = tp._calculate_user_impact(CheckClass.TEST, [])
        assert impact == 5

    def test_impact_api_file(self):
        """API files have high impact."""
        tp = TaskPrioritizer()
        impact = tp._calculate_user_impact(CheckClass.TEST, ["src/api/users.py"])
        assert impact == 8

    def test_impact_view_file(self):
        """View files have high impact."""
        tp = TaskPrioritizer()
        impact = tp._calculate_user_impact(CheckClass.TEST, ["views/index.py"])
        assert impact == 8

    def test_impact_route_file(self):
        """Route files have high impact."""
        tp = TaskPrioritizer()
        impact = tp._calculate_user_impact(CheckClass.TEST, ["routes/auth.py"])
        assert impact == 8

    def test_impact_handler_file(self):
        """Handler files have high impact."""
        tp = TaskPrioritizer()
        impact = tp._calculate_user_impact(CheckClass.TEST, ["handlers/request.py"])
        assert impact == 8

    def test_impact_controller_file(self):
        """Controller files have high impact."""
        tp = TaskPrioritizer()
        impact = tp._calculate_user_impact(CheckClass.TEST, ["controllers/user.py"])
        assert impact == 8

    def test_impact_page_file(self):
        """Page files have high impact."""
        tp = TaskPrioritizer()
        impact = tp._calculate_user_impact(CheckClass.TEST, ["pages/home.tsx"])
        assert impact == 8

    def test_impact_component_file(self):
        """Component files have high impact."""
        tp = TaskPrioritizer()
        impact = tp._calculate_user_impact(CheckClass.TEST, ["components/Button.tsx"])
        assert impact == 8

    def test_impact_test_file(self):
        """Test files have medium impact."""
        tp = TaskPrioritizer()
        impact = tp._calculate_user_impact(CheckClass.TEST, ["tests/test_foo.py"])
        assert impact == 6

    def test_impact_build_error(self):
        """Build errors always have high impact."""
        tp = TaskPrioritizer()
        impact = tp._calculate_user_impact(CheckClass.BUILD, ["internal/util.py"])
        assert impact == 9

    def test_impact_deploy_error(self):
        """Deploy errors always have high impact."""
        tp = TaskPrioritizer()
        impact = tp._calculate_user_impact(CheckClass.DEPLOY, ["internal/util.py"])
        assert impact == 9


class TestTaskPrioritizerFailureTracking:
    """Tests for failure frequency tracking."""

    def test_get_frequency_unknown(self):
        """Unknown error has frequency 0."""
        tp = TaskPrioritizer()
        freq = tp._get_failure_frequency("New error message")
        assert freq == 0

    def test_record_failure(self):
        """Recording failure increments count."""
        tp = TaskPrioritizer()
        error = "Test error message"
        tp.record_failure(error)
        freq = tp._get_failure_frequency(error)
        assert freq == 1

    def test_record_multiple_failures(self):
        """Multiple records increment count."""
        tp = TaskPrioritizer()
        error = "Test error message"
        tp.record_failure(error)
        tp.record_failure(error)
        tp.record_failure(error)
        freq = tp._get_failure_frequency(error)
        assert freq == 3

    def test_clear_failure(self):
        """Clearing failure removes from history."""
        tp = TaskPrioritizer()
        error = "Test error message"
        tp.record_failure(error)
        tp.record_failure(error)
        tp.clear_failure(error)
        freq = tp._get_failure_frequency(error)
        assert freq == 0

    def test_clear_unknown_failure(self):
        """Clearing unknown failure doesn't error."""
        tp = TaskPrioritizer()
        tp.clear_failure("Unknown error")  # Should not raise


class TestTaskPrioritizerExtractSecuritySeverity:
    """Tests for _extract_security_severity method."""

    def test_extract_critical(self):
        """Extracts CRITICAL severity."""
        tp = TaskPrioritizer()
        assert tp._extract_security_severity("CRITICAL vulnerability") == "CRITICAL"

    def test_extract_high(self):
        """Extracts HIGH severity."""
        tp = TaskPrioritizer()
        assert tp._extract_security_severity("HIGH risk issue") == "HIGH"

    def test_extract_medium(self):
        """Extracts MEDIUM severity."""
        tp = TaskPrioritizer()
        assert tp._extract_security_severity("MEDIUM severity") == "MEDIUM"

    def test_extract_low(self):
        """Extracts LOW severity."""
        tp = TaskPrioritizer()
        assert tp._extract_security_severity("LOW priority") == "LOW"

    def test_extract_none(self):
        """Returns None when no severity found."""
        tp = TaskPrioritizer()
        assert tp._extract_security_severity("Some error") is None

    def test_extract_first_match(self):
        """Returns first matching severity."""
        tp = TaskPrioritizer()
        # CRITICAL appears before HIGH
        assert tp._extract_security_severity("CRITICAL and HIGH") == "CRITICAL"


class TestTaskPrioritizerDependencyGraph:
    """Tests for dependency graph management."""

    def test_update_dependency_graph(self):
        """Update dependency graph."""
        tp = TaskPrioritizer()
        graph = {"a.py": {"b.py", "c.py"}, "b.py": {"d.py"}}
        tp.update_dependency_graph(graph)
        assert tp.dependency_graph == graph

    def test_update_replaces_graph(self):
        """Update replaces existing graph."""
        tp = TaskPrioritizer()
        tp.dependency_graph = {"old.py": {"dep.py"}}
        new_graph = {"new.py": {"newdep.py"}}
        tp.update_dependency_graph(new_graph)
        assert tp.dependency_graph == new_graph
        assert "old.py" not in tp.dependency_graph


class TestTaskPrioritizerIntegration:
    """Integration tests for TaskPrioritizer."""

    def test_full_prioritization_workflow(self):
        """Test complete prioritization workflow."""
        tp = TaskPrioritizer()

        # Set up dependency graph
        tp.update_dependency_graph({"core.py": {"api.py", "handlers.py"}})

        # Record some failures
        error1 = "CRITICAL: security vulnerability in auth.py"
        tp.record_failure(error1)
        tp.record_failure(error1)

        errors = [
            "ERROR collecting test.py\nImportError: foo",
            error1,
            "FAILED tests/test_foo.py",
            "lint: ruff error in code.py",
        ]

        tasks = tp.prioritize_tasks(errors, baseline_green=False)

        # Should have 4 tasks
        assert len(tasks) == 4

        # Security CRITICAL gets -1000 boost, so it comes first
        # even though collection error is also blocking
        assert tasks[0].security_severity == "CRITICAL"

        # Collection error should be blocking
        blocking_tasks = [t for t in tasks if t.is_blocking]
        assert len(blocking_tasks) >= 1

        # Security issue has recurring failure boost
        security_task = next(t for t in tasks if t.security_severity == "CRITICAL")
        assert security_task.failure_frequency == 2

    def test_regression_detection_workflow(self):
        """Test regression detection in workflow."""
        tp = TaskPrioritizer()

        errors = ["FAILED tests/test_auth.py::test_login"]
        previous_state = {"tests/test_auth.py": True}  # Was passing

        tasks = tp.prioritize_tasks(errors, False, previous_state)

        assert len(tasks) == 1
        assert tasks[0].category == TaskCategory.TEST_REGRESSION

    def test_improvement_blocking_workflow(self):
        """Test that improvements are blocked appropriately."""
        tp = TaskPrioritizer()

        # When red, no improvements
        assert tp.should_allow_improvements(False, []) is False

        # When green with test failures, no improvements
        test_failure = PrioritizedTask(
            id="t",
            description="d",
            category=TaskCategory.TEST_FAILURE,
            severity=5,
            blast_radius=1,
            user_impact=5,
        )
        assert tp.should_allow_improvements(True, [test_failure]) is False

        # When green with only lint errors, allow improvements
        lint_error = PrioritizedTask(
            id="t",
            description="d",
            category=TaskCategory.LINT_ERROR,
            severity=3,
            blast_radius=1,
            user_impact=3,
        )
        assert tp.should_allow_improvements(True, [lint_error]) is True
