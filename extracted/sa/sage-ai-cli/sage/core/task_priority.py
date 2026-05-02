"""Task prioritization for SAGE autopolit.

Addresses:
- P1-18: Rank tasks by severity, not by prompt keywords
- P1-19: Rank tasks by blast radius
- P1-20: Rank tasks by user-facing impact
- P1-21: Rank tasks by failing check class
- P1-22: Rank tasks by security severity
- P1-23: Rank tasks by deploy risk
- P1-24: Use dependency graph in task prioritization
- P1-25: Use recurring failure frequency
- P1-27: Distinguish regressions, enhancements, refactors, hygiene
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum


class TaskCategory(IntEnum):
    """Task categories in priority order (lower = higher priority)."""

    # P0: Critical/Blocking
    SECURITY_CRITICAL = 1
    TEST_COLLECTION_ERROR = 2
    BUILD_FAILURE = 3
    DEPLOY_BLOCKER = 4

    # P1: Test/Validation failures
    TEST_REGRESSION = 10
    TEST_FAILURE = 11
    LINT_ERROR = 12
    TYPE_ERROR = 13

    # P2: Quality issues
    SECURITY_WARNING = 20
    COVERAGE_GAP = 21
    DEPRECATION = 22

    # P3: Improvements
    ENHANCEMENT = 30
    REFACTOR = 31
    HYGIENE = 32
    DOCUMENTATION = 33

    # P4: Optional
    OPTIMIZATION = 40
    NICE_TO_HAVE = 50


class CheckClass(IntEnum):
    """Classes of checks in execution order."""

    COLLECT = 1  # Test collection (imports, syntax)
    TEST = 2  # Test execution
    LINT = 3  # Linting
    TYPE = 4  # Type checking
    BUILD = 5  # Build/compilation
    DEPLOY = 6  # Deployment
    SECURITY = 7  # Security scanning


@dataclass
class FailureSignature:
    """Signature of a failure for deduplication and tracking."""

    check_class: CheckClass
    error_type: str
    file_path: str | None = None
    line_number: int | None = None
    message_hash: str = ""

    def __hash__(self):
        return hash((self.check_class, self.error_type, self.file_path, self.line_number))


@dataclass
class PrioritizedTask:
    """A task with computed priority."""

    id: str
    description: str
    category: TaskCategory
    severity: int  # 1-10, 10 being most severe
    blast_radius: int  # Number of files/components affected
    user_impact: int  # 1-10, 10 being most impactful
    is_blocking: bool = False
    affected_files: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    failure_frequency: int = 0  # How many times this has failed recently
    security_severity: str | None = None  # CRITICAL, HIGH, MEDIUM, LOW
    deploy_risk: int = 0  # 1-10

    @property
    def priority_score(self) -> int:
        """Calculate priority score (lower = higher priority)."""
        base = self.category.value * 100

        # Adjust for severity (higher severity = lower score)
        severity_adj = (10 - self.severity) * 5

        # Adjust for blast radius (larger = lower score)
        blast_adj = max(0, 10 - self.blast_radius) * 2

        # Adjust for user impact (higher = lower score)
        impact_adj = (10 - self.user_impact) * 3

        # Blocking tasks get priority boost
        blocking_adj = -500 if self.is_blocking else 0

        # Recurring failures get priority boost
        frequency_adj = -self.failure_frequency * 10

        # Security critical gets major boost
        security_adj = 0
        if self.security_severity == "CRITICAL":
            security_adj = -1000
        elif self.security_severity == "HIGH":
            security_adj = -500
        elif self.security_severity == "MEDIUM":
            security_adj = -100

        # Deploy risk adjustment
        deploy_adj = -self.deploy_risk * 20

        return (
            base
            + severity_adj
            + blast_adj
            + impact_adj
            + blocking_adj
            + frequency_adj
            + security_adj
            + deploy_adj
        )


class TaskPrioritizer:
    """Intelligent task prioritization for autopolit.

    Priority rules:
    1. Blocking issues first (collection errors, build failures)
    2. Security critical issues
    3. Test failures (regressions before new failures)
    4. Lint/type errors
    5. Coverage gaps
    6. Enhancements and refactors
    7. Hygiene tasks only when green
    """

    def __init__(self):
        self.failure_history: dict[str, int] = {}  # signature -> count
        self.dependency_graph: dict[str, set[str]] = {}  # file -> dependents

    def classify_error(self, error_output: str) -> tuple[CheckClass, TaskCategory]:
        """Classify an error into check class and task category."""

        # Test collection errors (highest priority)
        if any(
            x in error_output
            for x in [
                "ERROR collecting",
                "ImportError",
                "ModuleNotFoundError",
                "SyntaxError",
                "IndentationError",
            ]
        ):
            return CheckClass.COLLECT, TaskCategory.TEST_COLLECTION_ERROR

        # Build failures
        if any(
            x in error_output
            for x in [
                "Build failed",
                "Compilation error",
                "compile error",
                "npm ERR!",
                "cargo build failed",
            ]
        ):
            return CheckClass.BUILD, TaskCategory.BUILD_FAILURE

        # Security issues
        if any(
            x in error_output
            for x in [
                "CRITICAL",
                "vulnerability",
                "CVE-",
                "security",
                "injection",
            ]
        ):
            return CheckClass.SECURITY, TaskCategory.SECURITY_CRITICAL

        # Test failures
        if any(
            x in error_output
            for x in [
                "FAILED",
                "AssertionError",
                "test failed",
                "tests failed",
            ]
        ):
            return CheckClass.TEST, TaskCategory.TEST_FAILURE

        # Lint errors
        if any(
            x in error_output
            for x in [
                "lint",
                "ruff",
                "eslint",
                "pylint",
                "flake8",
            ]
        ):
            return CheckClass.LINT, TaskCategory.LINT_ERROR

        # Type errors
        if any(
            x in error_output
            for x in [
                "mypy",
                "pyright",
                "TypeScript",
                "type error",
            ]
        ):
            return CheckClass.TYPE, TaskCategory.TYPE_ERROR

        return CheckClass.TEST, TaskCategory.TEST_FAILURE

    def extract_affected_files(self, error_output: str) -> list[str]:
        """Extract file paths from error output."""
        import re

        files = []
        # Common patterns for file paths in error messages
        patterns = [
            r"(?:^|\s)([^\s:]+\.py)(?::\d+)?",
            r"(?:^|\s)([^\s:]+\.(?:js|ts|tsx|jsx))(?::\d+)?",
            r'File "([^"]+)"',
            r"in ([^\s]+\.py)",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, error_output, re.MULTILINE)
            files.extend(matches)

        # Deduplicate and filter
        seen = set()
        result = []
        for f in files:
            if f not in seen and not f.startswith("<"):
                seen.add(f)
                result.append(f)

        return result

    def calculate_blast_radius(self, files: list[str]) -> int:
        """Calculate blast radius based on files and their dependents."""
        affected = set(files)

        # Add dependents from dependency graph
        for f in files:
            if f in self.dependency_graph:
                affected.update(self.dependency_graph[f])

        return len(affected)

    def is_regression(self, task: PrioritizedTask, previous_state: dict[str, bool]) -> bool:
        """Check if this failure is a regression (was passing before)."""
        for file in task.affected_files:
            if previous_state.get(file, False):  # Was passing
                return True
        return False

    def prioritize_tasks(
        self,
        error_outputs: list[str],
        baseline_green: bool,
        previous_state: dict[str, bool] | None = None,
    ) -> list[PrioritizedTask]:
        """Prioritize tasks based on error outputs.

        Args:
            error_outputs: List of error messages/outputs
            baseline_green: Whether the baseline validation passed
            previous_state: Previous pass/fail state by file

        Returns:
            Sorted list of prioritized tasks (highest priority first)
        """
        previous_state = previous_state or {}
        tasks: list[PrioritizedTask] = []

        for i, error in enumerate(error_outputs):
            check_class, category = self.classify_error(error)
            affected_files = self.extract_affected_files(error)
            blast_radius = self.calculate_blast_radius(affected_files)

            # Create task
            task = PrioritizedTask(
                id=f"task_{i}",
                description=self._summarize_error(error),
                category=category,
                severity=self._calculate_severity(check_class, error),
                blast_radius=blast_radius,
                user_impact=self._calculate_user_impact(check_class, affected_files),
                is_blocking=check_class in (CheckClass.COLLECT, CheckClass.BUILD),
                affected_files=affected_files,
                failure_frequency=self._get_failure_frequency(error),
                security_severity=self._extract_security_severity(error),
            )

            # Check for regression
            if self.is_regression(task, previous_state):
                task.category = TaskCategory.TEST_REGRESSION
                task.severity = min(10, task.severity + 2)

            tasks.append(task)

        # Sort by priority score (lower = higher priority)
        tasks.sort(key=lambda t: t.priority_score)

        return tasks

    def should_allow_improvements(
        self, baseline_green: bool, pending_tasks: list[PrioritizedTask]
    ) -> bool:
        """Check if improvement/hygiene tasks should be allowed.

        P0-7: Block cleanup cycles while baseline is red.
        """
        if not baseline_green:
            return False

        # Block if any blocking tasks remain
        if any(t.is_blocking for t in pending_tasks):
            return False

        # Block if any test failures remain
        if any(
            t.category in (TaskCategory.TEST_FAILURE, TaskCategory.TEST_REGRESSION)
            for t in pending_tasks
        ):
            return False

        return True

    def _summarize_error(self, error: str, max_len: int = 100) -> str:
        """Create a short summary of the error."""
        # Extract first meaningful line
        lines = error.strip().split("\n")
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#"):
                return line[:max_len] + ("..." if len(line) > max_len else "")
        return error[:max_len]

    def _calculate_severity(self, check_class: CheckClass, error: str) -> int:
        """Calculate severity 1-10 based on check class and error content."""
        base_severity = {
            CheckClass.COLLECT: 10,
            CheckClass.BUILD: 9,
            CheckClass.SECURITY: 9,
            CheckClass.TEST: 7,
            CheckClass.TYPE: 5,
            CheckClass.LINT: 4,
            CheckClass.DEPLOY: 8,
        }.get(check_class, 5)

        # Adjust for error content
        if "CRITICAL" in error or "FATAL" in error:
            base_severity = min(10, base_severity + 2)
        if "warning" in error.lower():
            base_severity = max(1, base_severity - 2)

        return base_severity

    def _calculate_user_impact(self, check_class: CheckClass, affected_files: list[str]) -> int:
        """Calculate user impact 1-10."""
        # Higher impact for user-facing files
        user_facing_patterns = [
            "api",
            "view",
            "route",
            "handler",
            "controller",
            "page",
            "component",
        ]

        impact = 5
        for f in affected_files:
            f_lower = f.lower()
            if any(p in f_lower for p in user_facing_patterns):
                impact = max(impact, 8)
            if "test" in f_lower:
                impact = max(impact, 6)

        # Build/deploy issues always high impact
        if check_class in (CheckClass.BUILD, CheckClass.DEPLOY):
            impact = max(impact, 9)

        return impact

    def _get_failure_frequency(self, error: str) -> int:
        """Get how many times this error has occurred recently."""
        # Create a signature from the error
        sig = hash(error[:200])
        return self.failure_history.get(str(sig), 0)

    def record_failure(self, error: str) -> None:
        """Record a failure for frequency tracking."""
        sig = str(hash(error[:200]))
        self.failure_history[sig] = self.failure_history.get(sig, 0) + 1

    def clear_failure(self, error: str) -> None:
        """Clear a failure from history (it was fixed)."""
        sig = str(hash(error[:200]))
        if sig in self.failure_history:
            del self.failure_history[sig]

    def _extract_security_severity(self, error: str) -> str | None:
        """Extract security severity if present."""
        if "CRITICAL" in error:
            return "CRITICAL"
        if "HIGH" in error:
            return "HIGH"
        if "MEDIUM" in error:
            return "MEDIUM"
        if "LOW" in error:
            return "LOW"
        return None

    def update_dependency_graph(self, graph: dict[str, set[str]]) -> None:
        """Update the dependency graph for blast radius calculation."""
        self.dependency_graph = graph
