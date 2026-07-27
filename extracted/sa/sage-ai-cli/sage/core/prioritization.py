"""Improved task prioritization for SAGE autopolit.

This module provides intelligent task prioritization based on:
- Actual failing checks (not just static hints)
- Dependency blast radius
- User-facing impact
- Security severity
- Regression vs improvement distinction
- Flaky test detection

This addresses P1 items 71-85:
- Item 71: Make autopolit rank work from actual failing checks before static hints
- Item 72: Make autopolit rank work from blast radius, not convenience
- Item 73: Make autopolit rank work from user-facing impact
- Item 74: Make autopolit rank work from security severity
- Item 75: Make autopolit distinguish regressions from improvements
- Item 76: Make autopolit distinguish flaky tests from deterministic failures
- Item 77: Add analysis-only mode for audit tasks
- Item 78: Add a "baseline red" mode that forbids refactors and cleanup work
- Item 79: Persist autopolit backlog state across cycles
- Item 80: Suppress repetitive task selection across cycles
- Item 81: Feed CI failure logs into autopolit planning
- Item 82: Feed deploy failures into autopolit planning
- Item 83: Add confidence scoring when context coverage is partial
- Item 84: Add better heuristics for when SAGE must read more files before editing
- Item 85: Add stronger refusal behavior for ambiguous destructive operations
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

__all__ = [
    "AutopolitState",
    "CIFailureAnalyzer",
    "ConfidenceLevel",
    "FlakeyTestTracker",
    "ImpactLevel",
    "PrioritizedTask",
    "TaskPrioritizer",
    "TaskSource",
    "TaskType",
]


class TaskType(str, Enum):
    """Types of tasks for prioritization."""

    FIX_ERROR = "fix_error"  # Fix a compile/runtime error
    FIX_TEST = "fix_test"  # Fix a failing test
    FIX_SECURITY = "fix_security"  # Fix a security vulnerability
    FIX_REGRESSION = "fix_regression"  # Fix a regression (was working, now broken)
    REFACTOR = "refactor"  # Code cleanup/refactoring
    IMPROVEMENT = "improvement"  # Enhancement/improvement
    NEW_FEATURE = "new_feature"  # New feature
    DOCUMENTATION = "documentation"  # Documentation
    DEPENDENCY_UPDATE = "dependency_update"  # Update dependencies
    CLEANUP = "cleanup"  # Remove dead code, fix lints
    UNKNOWN = "unknown"


class TaskSource(str, Enum):
    """Where the task came from."""

    TEST_FAILURE = "test_failure"  # From running tests
    LINT_ERROR = "lint_error"  # From linter
    TYPE_ERROR = "type_error"  # From type checker
    SECURITY_SCAN = "security_scan"  # From security scanner
    CI_FAILURE = "ci_failure"  # From CI logs
    DEPLOY_FAILURE = "deploy_failure"  # From deploy logs
    USER_REQUEST = "user_request"  # User explicitly asked
    STATIC_ANALYSIS = "static_analysis"  # Static code analysis
    HEURISTIC = "heuristic"  # Inferred from code patterns
    UNKNOWN = "unknown"


class ImpactLevel(str, Enum):
    """Impact level of a task."""

    CRITICAL = "critical"  # Breaks production / security issue
    HIGH = "high"  # Major functionality broken
    MEDIUM = "medium"  # Minor functionality affected
    LOW = "low"  # Cosmetic / minor improvements
    MINIMAL = "minimal"  # No user impact


class ConfidenceLevel(str, Enum):
    """Confidence in the task assessment."""

    HIGH = "high"  # We have full context and clear understanding
    MEDIUM = "medium"  # We have partial context
    LOW = "low"  # We're guessing based on limited info
    VERY_LOW = "very_low"  # High uncertainty, should read more files


@dataclass
class PrioritizedTask:
    """A task with prioritization metadata."""

    id: str
    description: str
    task_type: TaskType = TaskType.UNKNOWN
    source: TaskSource = TaskSource.UNKNOWN
    impact: ImpactLevel = ImpactLevel.MEDIUM
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM

    # Priority scoring
    base_priority: int = 50  # 0-100 scale
    blast_radius: int = 0  # Number of affected files
    security_severity: int = 0  # 0-100 scale
    user_facing: bool = False  # Affects user-visible behavior
    is_regression: bool = False  # Was working, now broken
    is_flaky: bool = False  # Known to be intermittent

    # Files involved
    files: list[str] = field(default_factory=list)
    affected_files: list[str] = field(default_factory=list)  # Downstream impact

    # Tracking
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    selected_count: int = 0  # Times this task was selected
    last_selected: str | None = None
    completed: bool = False
    completion_attempts: int = 0

    # Context requirements
    needs_more_context: bool = False
    suggested_reads: list[str] = field(default_factory=list)

    @property
    def effective_priority(self) -> int:
        """Calculate effective priority score."""
        score = self.base_priority

        # Boost for actual failures vs static hints
        if self.source in {
            TaskSource.TEST_FAILURE,
            TaskSource.CI_FAILURE,
            TaskSource.DEPLOY_FAILURE,
        }:
            score += 20
        elif self.source in {TaskSource.TYPE_ERROR, TaskSource.LINT_ERROR}:
            score += 10

        # Boost for user impact
        if self.user_facing:
            score += 15

        # Boost for regression
        if self.is_regression:
            score += 25

        # Boost for security issues
        if self.task_type == TaskType.FIX_SECURITY:
            score += 30 + (self.security_severity // 5)

        # Boost based on blast radius (more affected files = higher priority)
        score += min(self.blast_radius * 2, 20)

        # Penalty for low confidence (need more context first)
        if self.confidence == ConfidenceLevel.LOW:
            score -= 10
        elif self.confidence == ConfidenceLevel.VERY_LOW:
            score -= 25

        # Penalty for flaky tests (less urgent)
        if self.is_flaky:
            score -= 15

        # Penalty for refactoring/cleanup (do fixes first)
        if self.task_type in {TaskType.REFACTOR, TaskType.CLEANUP, TaskType.DOCUMENTATION}:
            score -= 20

        # Penalty for repeatedly selected but not completed
        if self.selected_count > 2 and not self.completed:
            score -= 10

        return max(0, min(100, score))

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "id": self.id,
            "description": self.description,
            "task_type": self.task_type.value,
            "source": self.source.value,
            "impact": self.impact.value,
            "confidence": self.confidence.value,
            "base_priority": self.base_priority,
            "blast_radius": self.blast_radius,
            "security_severity": self.security_severity,
            "user_facing": self.user_facing,
            "is_regression": self.is_regression,
            "is_flaky": self.is_flaky,
            "files": self.files,
            "affected_files": self.affected_files,
            "created_at": self.created_at,
            "selected_count": self.selected_count,
            "last_selected": self.last_selected,
            "completed": self.completed,
            "completion_attempts": self.completion_attempts,
            "needs_more_context": self.needs_more_context,
            "suggested_reads": self.suggested_reads,
        }

    @classmethod
    def from_dict(cls, data: dict) -> PrioritizedTask:
        """Deserialize from dictionary."""
        return cls(
            id=data["id"],
            description=data["description"],
            task_type=TaskType(data.get("task_type", "unknown")),
            source=TaskSource(data.get("source", "unknown")),
            impact=ImpactLevel(data.get("impact", "medium")),
            confidence=ConfidenceLevel(data.get("confidence", "medium")),
            base_priority=data.get("base_priority", 50),
            blast_radius=data.get("blast_radius", 0),
            security_severity=data.get("security_severity", 0),
            user_facing=data.get("user_facing", False),
            is_regression=data.get("is_regression", False),
            is_flaky=data.get("is_flaky", False),
            files=data.get("files", []),
            affected_files=data.get("affected_files", []),
            created_at=data.get("created_at", datetime.now().isoformat()),
            selected_count=data.get("selected_count", 0),
            last_selected=data.get("last_selected"),
            completed=data.get("completed", False),
            completion_attempts=data.get("completion_attempts", 0),
            needs_more_context=data.get("needs_more_context", False),
            suggested_reads=data.get("suggested_reads", []),
        )


class FlakeyTestTracker:
    """Track and identify flaky tests."""

    def __init__(self, cwd: Path) -> None:
        self.cwd = cwd
        self._cache_file = cwd / ".sage" / "flaky_tests.json"
        self._history: dict[str, list[dict]] = {}  # test_id -> list of run results
        self._load()

    def _load(self) -> None:
        """Load flaky test history."""
        if self._cache_file.exists():
            try:
                self._history = json.loads(self._cache_file.read_text(encoding="utf-8", errors="replace"))
            except Exception:
                self._history = {}

    def _save(self) -> None:
        """Save flaky test history."""
        self._cache_file.parent.mkdir(parents=True, exist_ok=True)
        self._cache_file.write_text(json.dumps(self._history, indent=2))

    def record_result(self, test_id: str, passed: bool, run_id: str = "") -> None:
        """Record a test result.

        Args:
            test_id: Unique test identifier (e.g., "test_foo.py::test_bar")
            passed: Whether the test passed
            run_id: Optional run identifier to track unique runs
        """
        if test_id not in self._history:
            self._history[test_id] = []

        self._history[test_id].append(
            {
                "passed": passed,
                "timestamp": datetime.now().isoformat(),
                "run_id": run_id,
            }
        )

        # Keep only last 20 results per test
        self._history[test_id] = self._history[test_id][-20:]
        self._save()

    def is_flaky(self, test_id: str) -> bool:
        """Check if a test is flaky (has both passes and failures recently).

        Args:
            test_id: Test identifier

        Returns:
            True if test appears flaky
        """
        if test_id not in self._history:
            return False

        results = self._history[test_id]
        if len(results) < 3:
            return False

        # Check if there's a mix of passes and failures in recent runs
        recent = results[-10:]
        passes = sum(1 for r in recent if r["passed"])
        failures = len(recent) - passes

        # Flaky if both passes and failures exist with similar frequency
        return passes > 0 and failures > 0 and min(passes, failures) >= 2

    def get_flaky_tests(self) -> list[str]:
        """Get list of known flaky tests."""
        return [test_id for test_id in self._history if self.is_flaky(test_id)]

    def get_reliability(self, test_id: str) -> float:
        """Get test reliability score (0.0 to 1.0).

        Args:
            test_id: Test identifier

        Returns:
            Reliability score (1.0 = always passes, 0.0 = always fails)
        """
        if test_id not in self._history:
            return 0.5  # Unknown

        results = self._history[test_id]
        if not results:
            return 0.5

        passes = sum(1 for r in results if r["passed"])
        return passes / len(results)


class CIFailureAnalyzer:
    """Analyze CI failure logs to extract actionable tasks."""

    # Patterns for different CI systems
    PATTERNS = {
        # pytest failures
        "pytest_failure": re.compile(r"FAILED\s+(.+?)::(test_\w+)\s*-\s*(.+)", re.MULTILINE),
        # pytest collection errors
        "pytest_collection": re.compile(
            r"ERROR\s+collecting\s+(.+\.py)\s*\n.*?ImportError:\s*(.+)", re.MULTILINE | re.DOTALL
        ),
        # jest failures
        "jest_failure": re.compile(r"FAIL\s+(.+?)\s*\n.*?●\s*(.+?)\s*\n\s*(.+)", re.MULTILINE),
        # TypeScript errors
        "typescript_error": re.compile(r"(.+?)\((\d+),(\d+)\):\s*error\s+TS(\d+):\s*(.+)"),
        # Python syntax errors
        "python_syntax": re.compile(r"File\s+\"(.+?)\",\s+line\s+(\d+)\s*\n.*?SyntaxError:\s*(.+)"),
        # Import errors
        "import_error": re.compile(
            r"ImportError:\s*(?:No module named|cannot import name)\s+'?(\w+)"
        ),
        # Generic error
        "generic_error": re.compile(r"(?:ERROR|Error|error):\s*(.+)"),
    }

    def __init__(self, cwd: Path) -> None:
        self.cwd = cwd

    def analyze_log(self, log_content: str) -> list[PrioritizedTask]:
        """Analyze a CI log and extract tasks.

        Args:
            log_content: CI log content

        Returns:
            List of prioritized tasks
        """
        tasks: list[PrioritizedTask] = []
        seen_ids: set[str] = set()

        # Pytest failures
        for match in self.PATTERNS["pytest_failure"].finditer(log_content):
            file_path = match.group(1)
            test_name = match.group(2)
            error_msg = match.group(3)

            task_id = f"pytest_{file_path}_{test_name}"
            if task_id in seen_ids:
                continue
            seen_ids.add(task_id)

            tasks.append(
                PrioritizedTask(
                    id=task_id,
                    description=f"Fix failing test {test_name}: {error_msg[:100]}",
                    task_type=TaskType.FIX_TEST,
                    source=TaskSource.CI_FAILURE,
                    impact=ImpactLevel.HIGH,
                    base_priority=70,
                    files=[file_path],
                )
            )

        # Pytest collection errors
        for match in self.PATTERNS["pytest_collection"].finditer(log_content):
            file_path = match.group(1)
            error_msg = match.group(2)

            task_id = f"collection_{file_path}"
            if task_id in seen_ids:
                continue
            seen_ids.add(task_id)

            tasks.append(
                PrioritizedTask(
                    id=task_id,
                    description=f"Fix import error in {file_path}: {error_msg[:100]}",
                    task_type=TaskType.FIX_ERROR,
                    source=TaskSource.CI_FAILURE,
                    impact=ImpactLevel.CRITICAL,
                    base_priority=90,
                    files=[file_path],
                )
            )

        # TypeScript errors
        for match in self.PATTERNS["typescript_error"].finditer(log_content):
            file_path = match.group(1)
            line = match.group(2)
            error_code = match.group(4)
            error_msg = match.group(5)

            task_id = f"ts_{file_path}_{line}_{error_code}"
            if task_id in seen_ids:
                continue
            seen_ids.add(task_id)

            tasks.append(
                PrioritizedTask(
                    id=task_id,
                    description=f"Fix TS{error_code} in {file_path}:{line}: {error_msg[:80]}",
                    task_type=TaskType.FIX_ERROR,
                    source=TaskSource.CI_FAILURE,
                    impact=ImpactLevel.HIGH,
                    base_priority=75,
                    files=[file_path],
                )
            )

        # Python syntax errors
        for match in self.PATTERNS["python_syntax"].finditer(log_content):
            file_path = match.group(1)
            line = match.group(2)
            error_msg = match.group(3)

            task_id = f"syntax_{file_path}_{line}"
            if task_id in seen_ids:
                continue
            seen_ids.add(task_id)

            tasks.append(
                PrioritizedTask(
                    id=task_id,
                    description=f"Fix syntax error in {file_path}:{line}: {error_msg}",
                    task_type=TaskType.FIX_ERROR,
                    source=TaskSource.CI_FAILURE,
                    impact=ImpactLevel.CRITICAL,
                    base_priority=95,
                    files=[file_path],
                )
            )

        return tasks

    def analyze_deploy_log(self, log_content: str) -> list[PrioritizedTask]:
        """Analyze a deploy failure log and extract tasks.

        Args:
            log_content: Deploy log content

        Returns:
            List of prioritized tasks
        """
        tasks: list[PrioritizedTask] = []

        # Deploy failures are typically more critical
        for match in self.PATTERNS["generic_error"].finditer(log_content[:5000]):
            error_msg = match.group(1)

            # Skip if too generic
            if len(error_msg) < 10:
                continue

            task_id = f"deploy_{hashlib.md5(error_msg[:50].encode()).hexdigest()[:8]}"

            tasks.append(
                PrioritizedTask(
                    id=task_id,
                    description=f"Fix deploy error: {error_msg[:100]}",
                    task_type=TaskType.FIX_ERROR,
                    source=TaskSource.DEPLOY_FAILURE,
                    impact=ImpactLevel.CRITICAL,
                    base_priority=95,
                    user_facing=True,
                )
            )
            break  # Only take first error

        return tasks


class AutopolitState:
    """Persistent state for autopolit across cycles."""

    def __init__(self, cwd: Path) -> None:
        self.cwd = cwd
        self._cache_file = cwd / ".sage" / "autopolit_state.json"
        self.tasks: list[PrioritizedTask] = []
        self.completed_task_ids: set[str] = set()
        self.suppressed_task_ids: set[str] = set()
        self.cycle_count: int = 0
        self.last_cycle: str | None = None
        self._load()

    def _load(self) -> None:
        """Load state from disk."""
        if self._cache_file.exists():
            try:
                data = json.loads(self._cache_file.read_text(encoding="utf-8", errors="replace"))
                self.tasks = [PrioritizedTask.from_dict(t) for t in data.get("tasks", [])]
                self.completed_task_ids = set(data.get("completed_task_ids", []))
                self.suppressed_task_ids = set(data.get("suppressed_task_ids", []))
                self.cycle_count = data.get("cycle_count", 0)
                self.last_cycle = data.get("last_cycle")
            except Exception:
                pass

    def save(self) -> None:
        """Save state to disk."""
        self._cache_file.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "tasks": [t.to_dict() for t in self.tasks],
            "completed_task_ids": list(self.completed_task_ids),
            "suppressed_task_ids": list(self.suppressed_task_ids),
            "cycle_count": self.cycle_count,
            "last_cycle": self.last_cycle,
        }
        self._cache_file.write_text(json.dumps(data, indent=2))

    def add_task(self, task: PrioritizedTask) -> None:
        """Add a task, avoiding duplicates."""
        if task.id not in self.completed_task_ids and task.id not in self.suppressed_task_ids:
            existing_ids = {t.id for t in self.tasks}
            if task.id not in existing_ids:
                self.tasks.append(task)

    def get_next_task(self) -> PrioritizedTask | None:
        """Get the highest priority non-completed task."""
        active_tasks = [
            t
            for t in self.tasks
            if not t.completed
            and t.id not in self.completed_task_ids
            and t.id not in self.suppressed_task_ids
        ]

        if not active_tasks:
            return None

        # Sort by effective priority (descending)
        active_tasks.sort(key=lambda t: t.effective_priority, reverse=True)

        task = active_tasks[0]
        task.selected_count += 1
        task.last_selected = datetime.now().isoformat()

        return task

    def mark_completed(self, task_id: str) -> None:
        """Mark a task as completed."""
        self.completed_task_ids.add(task_id)
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                break
        self.save()

    def suppress_task(self, task_id: str) -> None:
        """Suppress a task from future selection (e.g., not actionable)."""
        self.suppressed_task_ids.add(task_id)
        self.save()

    def start_cycle(self) -> None:
        """Start a new autopolit cycle."""
        self.cycle_count += 1
        self.last_cycle = datetime.now().isoformat()
        self.save()

    def get_backlog_summary(self) -> str:
        """Get a summary of the current backlog."""
        active = [t for t in self.tasks if not t.completed and t.id not in self.suppressed_task_ids]
        if not active:
            return "No pending tasks"

        by_type: dict[str, int] = {}
        for task in active:
            by_type[task.task_type.value] = by_type.get(task.task_type.value, 0) + 1

        summary_parts = [
            f"{count} {ttype}" for ttype, count in sorted(by_type.items(), key=lambda x: -x[1])
        ]
        return f"{len(active)} tasks: {', '.join(summary_parts)}"


class TaskPrioritizer:
    """Main task prioritization engine for autopolit."""

    def __init__(self, cwd: Path) -> None:
        self.cwd = cwd
        self.state = AutopolitState(cwd)
        self.flaky_tracker = FlakeyTestTracker(cwd)
        self.ci_analyzer = CIFailureAnalyzer(cwd)

        # Mode settings
        self.analysis_only = False  # Item 77: Don't make changes, just analyze
        self.baseline_red = False  # Item 78: Only allow fixes, no refactors

    def set_analysis_only(self, enabled: bool) -> None:
        """Set analysis-only mode (Item 77)."""
        self.analysis_only = enabled

    def set_baseline_red(self, enabled: bool) -> None:
        """Set baseline-red mode (Item 78)."""
        self.baseline_red = enabled

    def ingest_ci_log(self, log_content: str) -> int:
        """Ingest CI failure log and add tasks (Item 81).

        Args:
            log_content: CI log content

        Returns:
            Number of tasks added
        """
        tasks = self.ci_analyzer.analyze_log(log_content)
        for task in tasks:
            self.state.add_task(task)
        self.state.save()
        return len(tasks)

    def ingest_deploy_log(self, log_content: str) -> int:
        """Ingest deploy failure log and add tasks (Item 82).

        Args:
            log_content: Deploy log content

        Returns:
            Number of tasks added
        """
        tasks = self.ci_analyzer.analyze_deploy_log(log_content)
        for task in tasks:
            self.state.add_task(task)
        self.state.save()
        return len(tasks)

    def add_task_from_test_failure(
        self,
        test_id: str,
        error_message: str,
        file_path: str,
    ) -> PrioritizedTask:
        """Add a task from a test failure.

        Args:
            test_id: Test identifier
            error_message: Error message
            file_path: File path

        Returns:
            Created task
        """
        # Record for flaky tracking
        self.flaky_tracker.record_result(test_id, passed=False)

        is_flaky = self.flaky_tracker.is_flaky(test_id)

        task = PrioritizedTask(
            id=f"test_{hashlib.md5(test_id.encode()).hexdigest()[:12]}",
            description=f"Fix failing test: {error_message[:100]}",
            task_type=TaskType.FIX_TEST,
            source=TaskSource.TEST_FAILURE,
            impact=ImpactLevel.HIGH,
            base_priority=70,
            is_flaky=is_flaky,
            files=[file_path],
        )

        self.state.add_task(task)
        self.state.save()
        return task

    def add_task_from_security_finding(
        self,
        finding_id: str,
        description: str,
        severity: str,
        file_path: str,
        line: int,
    ) -> PrioritizedTask:
        """Add a task from a security finding.

        Args:
            finding_id: Unique finding identifier
            description: Finding description
            severity: Severity level (CRITICAL, HIGH, MEDIUM, LOW)
            file_path: File path
            line: Line number

        Returns:
            Created task
        """
        severity_score = {"CRITICAL": 100, "HIGH": 75, "MEDIUM": 50, "LOW": 25}.get(
            severity.upper(), 50
        )

        task = PrioritizedTask(
            id=f"sec_{finding_id}",
            description=f"[{severity}] {description}",
            task_type=TaskType.FIX_SECURITY,
            source=TaskSource.SECURITY_SCAN,
            impact=ImpactLevel.CRITICAL if severity.upper() == "CRITICAL" else ImpactLevel.HIGH,
            base_priority=80,
            security_severity=severity_score,
            user_facing=True,
            files=[file_path],
        )

        self.state.add_task(task)
        self.state.save()
        return task

    def calculate_blast_radius(self, file_path: str, dependency_graph: Any) -> int:
        """Calculate the blast radius (affected files) for a change.

        Args:
            file_path: File being changed
            dependency_graph: DependencyGraph instance

        Returns:
            Number of affected files
        """
        try:
            affected = dependency_graph.get_affected_files([file_path])
            return len(affected) - 1  # Exclude the file itself
        except Exception:
            return 0

    def assess_confidence(
        self,
        task: PrioritizedTask,
        files_read: set[str],
        scan_coverage: float,
    ) -> ConfidenceLevel:
        """Assess confidence level for a task (Item 83).

        Args:
            task: The task to assess
            files_read: Set of files that have been read
            scan_coverage: Scan coverage percentage (0-100)

        Returns:
            Confidence level
        """
        # High confidence if we've read all involved files
        if all(f in files_read for f in task.files):
            if scan_coverage >= 80:
                return ConfidenceLevel.HIGH
            return ConfidenceLevel.MEDIUM

        # Medium if we've read some files
        read_count = sum(1 for f in task.files if f in files_read)
        if read_count > 0:
            if scan_coverage >= 50:
                return ConfidenceLevel.MEDIUM
            return ConfidenceLevel.LOW

        # Low if we haven't read any involved files
        if scan_coverage >= 30:
            return ConfidenceLevel.LOW

        return ConfidenceLevel.VERY_LOW

    def should_read_more(self, task: PrioritizedTask) -> tuple[bool, list[str]]:
        """Check if we need to read more files before proceeding (Item 84).

        Args:
            task: The task to assess

        Returns:
            (should_read, suggested_files)
        """
        if task.confidence in {ConfidenceLevel.LOW, ConfidenceLevel.VERY_LOW}:
            return True, task.suggested_reads or task.files

        if task.needs_more_context:
            return True, task.suggested_reads

        return False, []

    def should_refuse_destructive(
        self, task: PrioritizedTask, description: str
    ) -> tuple[bool, str]:
        """Check if we should refuse a potentially destructive operation (Item 85).

        Args:
            task: The task
            description: User's description

        Returns:
            (should_refuse, reason)
        """
        # Refuse if confidence is too low for destructive operations
        destructive_keywords = ["delete", "remove", "drop", "reset", "overwrite", "replace all"]
        is_destructive = any(kw in description.lower() for kw in destructive_keywords)

        if is_destructive:
            if task.confidence == ConfidenceLevel.VERY_LOW:
                return (
                    True,
                    "Cannot perform destructive operation with very low confidence. Need to read more files first.",
                )

            if not task.files:
                return (
                    True,
                    "Cannot perform destructive operation without knowing which files are involved.",
                )

        # Refuse refactors in baseline-red mode
        if self.baseline_red and task.task_type in {
            TaskType.REFACTOR,
            TaskType.CLEANUP,
            TaskType.IMPROVEMENT,
        }:
            return True, "Baseline-red mode: only fixes are allowed, no refactoring or cleanup."

        return False, ""

    def get_next_task(self) -> PrioritizedTask | None:
        """Get the next highest-priority task.

        Returns:
            Next task to work on, or None
        """
        return self.state.get_next_task()

    def get_prioritized_list(self, limit: int = 10) -> list[PrioritizedTask]:
        """Get a prioritized list of tasks.

        Args:
            limit: Maximum tasks to return

        Returns:
            List of tasks sorted by priority
        """
        active = [
            t
            for t in self.state.tasks
            if not t.completed
            and t.id not in self.state.completed_task_ids
            and t.id not in self.state.suppressed_task_ids
        ]

        # Filter by mode
        if self.baseline_red:
            active = [t for t in active if t.task_type not in {TaskType.REFACTOR, TaskType.CLEANUP}]

        active.sort(key=lambda t: t.effective_priority, reverse=True)
        return active[:limit]

    def complete_task(self, task_id: str) -> None:
        """Mark a task as completed."""
        self.state.mark_completed(task_id)

    def suppress_task(self, task_id: str) -> None:
        """Suppress a task from future selection."""
        self.state.suppress_task(task_id)

    def get_status(self) -> str:
        """Get current prioritization status."""
        return self.state.get_backlog_summary()
