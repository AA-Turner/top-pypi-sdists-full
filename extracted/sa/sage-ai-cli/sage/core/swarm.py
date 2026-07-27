"""Multi-agent swarm orchestration for SAGE.

This module provides an orchestrator-worker pattern for complex task
decomposition and parallel execution across multiple models.

Features:
- Task decomposition (architecture -> test -> implement -> security -> docs)
- Model routing based on task type and model strengths
- Parallel execution with dependency management
- Result aggregation

P3 Items 119-122: Extract swarm orchestration from main.py.
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

__all__ = [
    "ModelProfile",
    "SwarmOrchestrator",
    "SwarmResult",
    "SwarmTask",
    "TaskType",
]


class TaskType(Enum):
    """Types of tasks for model routing."""

    ARCHITECTURE = "architecture"  # High-level planning, API design
    IMPLEMENTATION = "implementation"  # Writing core logic
    TESTING = "testing"  # Writing tests
    SECURITY = "security"  # Security auditing
    DOCUMENTATION = "documentation"  # Docs, README, comments
    REFACTORING = "refactoring"  # Code cleanup, DRY
    DEBUGGING = "debugging"  # Fixing bugs, analyzing errors
    REVIEW = "review"  # Code review, quality checks


class TaskStatus(Enum):
    """Task execution status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class SwarmTask:
    """A task for the swarm to execute."""

    id: str
    type: TaskType
    description: str
    context: str  # Relevant file contents, errors, etc.
    dependencies: list[str] = field(default_factory=list)  # Task IDs this depends on
    result: str | None = None
    status: TaskStatus = TaskStatus.PENDING
    model_used: str | None = None
    execution_time: float = 0.0
    error: str | None = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type.value,
            "description": self.description,
            "status": self.status.value,
            "model_used": self.model_used,
            "execution_time": self.execution_time,
            "error": self.error,
        }


# Explicit profiles for sage-hosted cloud:* models. The generic substring
# heuristic in from_model_id() works for big-name models but misses our
# specific deployment — this table fills the gap with production-tuned
# strengths. Key uses substring matching (see _cloud_key) so a future
# `cloud:qwen-coder-7b:v2` tag still resolves to this profile.
_CLOUD_MODEL_PROFILES: dict[str, dict] = {
    # The coding specialist — best for IMPLEMENTATION/DEBUGGING/REFACTORING.
    "qwen-coder-7b": {
        "strengths": (
            "IMPLEMENTATION", "DEBUGGING", "REFACTORING", "TESTING",
        ),
        "cost_tier": "cheap",
        "speed": "fast",
        "context_size": 8192,
    },
    # General-purpose workhorse — solid all-around.
    "llama-3-1-8b": {
        "strengths": (
            "DOCUMENTATION", "REVIEW", "ARCHITECTURE", "IMPLEMENTATION",
        ),
        "cost_tier": "cheap",
        "speed": "fast",
        "context_size": 8192,
    },
    # The reasoning specialist — chain-of-thought, architecture, review.
    "deepseek-r1-7b": {
        "strengths": (
            "ARCHITECTURE", "REVIEW", "DEBUGGING", "SECURITY",
        ),
        "cost_tier": "cheap",
        "speed": "fast",
        "context_size": 16384,
    },
    # Alternative chat — strong general instruction following.
    "gemma-2-9b": {
        "strengths": (
            "DOCUMENTATION", "REVIEW", "ARCHITECTURE",
        ),
        "cost_tier": "cheap",
        "speed": "fast",
        "context_size": 8192,
    },
    # Microsoft's compact powerhouse — strong all-rounder.
    "phi-4-14b": {
        "strengths": (
            "ARCHITECTURE", "DOCUMENTATION", "REVIEW", "REFACTORING",
        ),
        "cost_tier": "cheap",
        "speed": "fast",
        "context_size": 8192,
    },
    # Reliable instruction-following workhorse.
    "mistral-7b": {
        "strengths": (
            "DOCUMENTATION", "REVIEW", "IMPLEMENTATION",
        ),
        "cost_tier": "cheap",
        "speed": "fast",
        "context_size": 8192,
    },
    # Vision model — review tasks (look at screenshots, designs, etc.).
    # Deliberately NO IMPLEMENTATION here so the swarm doesn't route code
    # tasks to a vision specialist.
    "llava-next-7b": {
        "strengths": (
            "REVIEW", "DOCUMENTATION",
        ),
        "cost_tier": "cheap",
        "speed": "fast",
        "context_size": 4096,
    },
    # Long-context specialist — large-file analysis, architecture review
    # across the whole codebase.
    "yi-1-5-9b": {
        "strengths": (
            "ARCHITECTURE", "REVIEW", "DOCUMENTATION",
        ),
        "cost_tier": "cheap",
        "speed": "medium",
        "context_size": 32768,
    },
}


def _cloud_key(model_id: str) -> str:
    """Normalize a model_id to its cloud:* profile key.

    `cloud:qwen-coder-7b` → `qwen-coder-7b`
    `cloud:qwen-coder-7b:v2` → `qwen-coder-7b` (strips trailing tag)
    Returns empty string for non-cloud IDs so they fall through to the
    generic heuristic path.
    """
    lower = model_id.lower()
    if not lower.startswith("cloud:"):
        return ""
    name = lower.split(":", 1)[1]
    # Match the longest profile key that's a prefix of `name`
    for key in sorted(_CLOUD_MODEL_PROFILES, key=len, reverse=True):
        if name.startswith(key):
            return key
    return ""


# Hydrate string-name strengths into TaskType enums up-front so the hot
# path in from_model_id doesn't keep doing it. Mutating the dict at
# import time is acceptable since this is module-level config.
def _hydrate_cloud_profiles() -> None:
    for key, profile in _CLOUD_MODEL_PROFILES.items():
        strengths = profile["strengths"]
        if strengths and isinstance(strengths[0], str):
            profile["strengths"] = tuple(getattr(TaskType, name) for name in strengths)


_hydrate_cloud_profiles()


@dataclass
class ModelProfile:
    """Profile for model routing decisions."""

    model_id: str
    strengths: list[TaskType]
    cost_tier: str  # "cheap", "medium", "expensive"
    context_size: int
    speed: str  # "fast", "medium", "slow"

    @classmethod
    def from_model_id(cls, model_id: str, context_size: int = 8192) -> ModelProfile:
        """Create a profile from a model ID using heuristics.

        Checks our explicit cloud:* model table first (production-tuned
        strengths for sage-hosted models), then falls through to the
        generic substring heuristics for everything else.
        """
        # Sage-hosted cloud:* models get explicit, hand-tuned profiles.
        # Substring match so the same entry handles `:latest` etc. tags.
        explicit = _CLOUD_MODEL_PROFILES.get(_cloud_key(model_id))
        if explicit is not None:
            return cls(
                model_id=model_id,
                strengths=list(explicit["strengths"]),
                cost_tier=explicit["cost_tier"],
                context_size=explicit.get("context_size", context_size),
                speed=explicit["speed"],
            )

        # Fallback: generic substring-based heuristics for unknown models.
        name_lower = model_id.lower()

        # Determine cost tier
        if any(x in name_lower for x in ["opus", "gpt-4o", "claude-3.5-sonnet", "o1"]):
            cost_tier = "expensive"
        elif any(x in name_lower for x in ["sonnet", "gpt-4o-mini", "mixtral", "llama-3.1-70b"]):
            cost_tier = "medium"
        else:
            cost_tier = "cheap"

        # Determine speed
        if any(x in name_lower for x in ["flash", "mini", "haiku", "3b", "7b"]):
            speed = "fast"
        elif any(x in name_lower for x in ["70b", "opus", "o1"]):
            speed = "slow"
        else:
            speed = "medium"

        # Determine strengths
        strengths: list[TaskType] = []
        if any(
            x in name_lower for x in ["coder", "code", "deepseek-coder", "starcoder", "codellama"]
        ):
            strengths.extend([TaskType.IMPLEMENTATION, TaskType.DEBUGGING, TaskType.REFACTORING])
        if any(x in name_lower for x in ["opus", "o1", "reasoning", "deepseek-r1"]):
            strengths.extend([TaskType.ARCHITECTURE, TaskType.REVIEW])
        if any(x in name_lower for x in ["instruct", "chat"]):
            strengths.extend([TaskType.DOCUMENTATION, TaskType.REVIEW])

        if not strengths:
            strengths = [TaskType.IMPLEMENTATION, TaskType.DOCUMENTATION]

        return cls(
            model_id=model_id,
            strengths=strengths,
            cost_tier=cost_tier,
            context_size=context_size,
            speed=speed,
        )


@dataclass
class SwarmResult:
    """Result of swarm execution."""

    success: bool
    tasks: list[SwarmTask]
    total_time: float
    models_used: set[str]
    combined_output: str | None = None

    @property
    def completed_tasks(self) -> list[SwarmTask]:
        return [t for t in self.tasks if t.status == TaskStatus.COMPLETED]

    @property
    def failed_tasks(self) -> list[SwarmTask]:
        return [t for t in self.tasks if t.status == TaskStatus.FAILED]


class SwarmOrchestrator:
    """Orchestrates multi-agent task decomposition and execution.

    The orchestrator:
    1. Decomposes complex tasks into sub-tasks
    2. Routes each task to the most appropriate model
    3. Manages dependencies between tasks
    4. Executes tasks in parallel where possible
    5. Aggregates results

    Usage:
        orchestrator = SwarmOrchestrator(router, "default-model")
        tasks = orchestrator.decompose_task("implement user auth")
        result = orchestrator.execute(tasks, send_fn)
    """

    # Model routing preferences - maps task types to preferred model characteristics
    TASK_MODEL_PREFERENCES: dict[TaskType, dict[str, Any]] = {
        TaskType.ARCHITECTURE: {
            "cost_tier": "expensive",
            "preferred_strength": TaskType.ARCHITECTURE,
            "context_priority": True,
        },
        TaskType.IMPLEMENTATION: {
            "cost_tier": "medium",
            "preferred_strength": TaskType.IMPLEMENTATION,
            "context_priority": True,
        },
        TaskType.TESTING: {
            "cost_tier": "cheap",
            "preferred_strength": TaskType.TESTING,
            "context_priority": False,
        },
        TaskType.SECURITY: {
            "cost_tier": "medium",
            "preferred_strength": TaskType.SECURITY,
            "context_priority": False,
        },
        TaskType.DOCUMENTATION: {
            "cost_tier": "cheap",
            "preferred_strength": TaskType.DOCUMENTATION,
            "context_priority": False,
        },
        TaskType.REFACTORING: {
            "cost_tier": "medium",
            "preferred_strength": TaskType.REFACTORING,
            "context_priority": True,
        },
        TaskType.DEBUGGING: {
            "cost_tier": "medium",
            "preferred_strength": TaskType.DEBUGGING,
            "context_priority": True,
        },
        TaskType.REVIEW: {
            "cost_tier": "cheap",
            "preferred_strength": TaskType.REVIEW,
            "context_priority": False,
        },
    }

    def __init__(self, default_model: str, max_workers: int = 3):
        """Initialize the swarm orchestrator.

        Args:
            default_model: Default model to use when no better match found
            max_workers: Maximum parallel workers for task execution
        """
        self.default_model = default_model
        self.max_workers = max_workers
        self.model_profiles: dict[str, ModelProfile] = {}
        self.tasks: dict[str, SwarmTask] = {}
        self._lock = threading.Lock()

    def register_model(self, model_id: str, context_size: int = 8192) -> None:
        """Register a model for routing.

        Args:
            model_id: Model identifier
            context_size: Context window size
        """
        self.model_profiles[model_id] = ModelProfile.from_model_id(model_id, context_size)

    def register_models(self, model_ids: list[str]) -> None:
        """Register multiple models for routing."""
        for model_id in model_ids:
            self.register_model(model_id)

    def select_model_for_task(self, task_type: TaskType) -> str:
        """Select the best model for a given task type.

        Args:
            task_type: Type of task to route

        Returns:
            Model ID to use
        """
        prefs = self.TASK_MODEL_PREFERENCES.get(task_type, {})
        preferred_cost = prefs.get("cost_tier", "medium")
        preferred_strength = prefs.get("preferred_strength", task_type)

        # Find models matching the preferred cost tier and task type
        candidates = []
        for model_id, profile in self.model_profiles.items():
            if profile.cost_tier == preferred_cost and preferred_strength in profile.strengths:
                candidates.append((model_id, 2))  # Best match
            elif preferred_strength in profile.strengths:
                candidates.append((model_id, 1))  # Strength match
            elif profile.cost_tier == preferred_cost:
                candidates.append((model_id, 0))  # Cost match

        if candidates:
            # Sort by score and return best
            candidates.sort(key=lambda x: x[1], reverse=True)
            return candidates[0][0]

        return self.default_model

    def decompose_task(self, prompt: str, context: str = "") -> list[SwarmTask]:
        """Decompose a complex task into sub-tasks.

        Uses pattern matching to identify required task types and
        creates a DAG of tasks with dependencies.

        Args:
            prompt: User's task description
            context: Additional context (file contents, errors, etc.)

        Returns:
            List of SwarmTask objects
        """
        tasks: list[SwarmTask] = []
        prompt_lower = prompt.lower()

        # Determine required task types
        needs_architecture = any(
            x in prompt_lower
            for x in ["create", "implement", "build", "add feature", "design", "architect"]
        )
        needs_testing = any(
            x in prompt_lower for x in ["test", "tdd", "create", "implement", "build", "coverage"]
        )
        needs_implementation = any(
            x in prompt_lower
            for x in ["implement", "build", "create", "fix", "update", "add", "write"]
        )
        needs_debugging = any(
            x in prompt_lower
            for x in ["fix", "debug", "error", "bug", "issue", "broken", "failing"]
        )
        needs_refactoring = any(
            x in prompt_lower for x in ["refactor", "clean", "improve", "optimize", "simplify"]
        )
        needs_docs = (
            any(x in prompt_lower for x in ["document", "readme", "docs", "comment", "explain"])
            or needs_implementation
        )

        task_ids: list[str] = []

        # Architecture planning for new features
        if needs_architecture:
            tasks.append(
                SwarmTask(
                    id="plan",
                    type=TaskType.ARCHITECTURE,
                    description="Create implementation plan and architecture",
                    context=f"Task: {prompt}\n\nContext:\n{context[:3000]}",
                )
            )
            task_ids.append("plan")

        # Testing first (TDD)
        if needs_testing and not needs_debugging:
            deps = ["plan"] if "plan" in task_ids else []
            tasks.append(
                SwarmTask(
                    id="tests",
                    type=TaskType.TESTING,
                    description="Write tests first (TDD approach)",
                    context=f"Task: {prompt}\n\nWrite tests that verify the expected behavior.",
                    dependencies=deps,
                )
            )
            task_ids.append("tests")

        # Debugging task
        if needs_debugging:
            tasks.append(
                SwarmTask(
                    id="debug",
                    type=TaskType.DEBUGGING,
                    description="Analyze and fix the issue",
                    context=f"Task: {prompt}\n\nContext:\n{context[:3000]}",
                )
            )
            task_ids.append("debug")

        # Implementation task
        if needs_implementation:
            deps = []
            if "tests" in task_ids:
                deps.append("tests")
            elif "plan" in task_ids:
                deps.append("plan")
            tasks.append(
                SwarmTask(
                    id="implement",
                    type=TaskType.IMPLEMENTATION,
                    description="Write implementation code",
                    context=f"Task: {prompt}\n\nImplement the solution.",
                    dependencies=deps,
                )
            )
            task_ids.append("implement")

        # Refactoring task
        if needs_refactoring and "implement" not in task_ids:
            tasks.append(
                SwarmTask(
                    id="refactor",
                    type=TaskType.REFACTORING,
                    description="Refactor and improve the code",
                    context=f"Task: {prompt}\n\nContext:\n{context[:3000]}",
                )
            )
            task_ids.append("refactor")

        # Security audit for new code
        if needs_implementation or needs_refactoring:
            impl_dep = (
                "implement"
                if "implement" in task_ids
                else ("refactor" if "refactor" in task_ids else None)
            )
            deps = [impl_dep] if impl_dep else []
            tasks.append(
                SwarmTask(
                    id="security",
                    type=TaskType.SECURITY,
                    description="Security audit of changes",
                    context="Review the written code for security vulnerabilities.",
                    dependencies=deps,
                )
            )
            task_ids.append("security")

        # Documentation for new features
        if needs_docs:
            impl_dep = (
                "implement"
                if "implement" in task_ids
                else ("refactor" if "refactor" in task_ids else None)
            )
            deps = [impl_dep] if impl_dep else []
            tasks.append(
                SwarmTask(
                    id="docs",
                    type=TaskType.DOCUMENTATION,
                    description="Update documentation",
                    context="Add or update documentation for the changes.",
                    dependencies=deps,
                )
            )
            task_ids.append("docs")

        # If no tasks identified, create a generic implementation task
        if not tasks:
            tasks.append(
                SwarmTask(
                    id="main",
                    type=TaskType.IMPLEMENTATION,
                    description=prompt[:200],
                    context=f"Task: {prompt}\n\nContext:\n{context[:3000]}",
                )
            )

        # Store tasks
        for task in tasks:
            self.tasks[task.id] = task

        return tasks

    def execute_task(
        self,
        task: SwarmTask,
        send_fn: Callable[[str, str], str | None],
    ) -> str | None:
        """Execute a single task using the appropriate model.

        Args:
            task: Task to execute
            send_fn: Function to send prompt to model, signature (prompt, model_id) -> response

        Returns:
            Model response or None if failed
        """
        import time

        with self._lock:
            task.status = TaskStatus.RUNNING

        # Select model for this task type
        model_id = self.select_model_for_task(task.type)
        task.model_used = model_id

        # Build the task prompt
        task_prompt = (
            f"## Task: {task.description}\n\n"
            f"## Task Type: {task.type.value}\n\n"
            f"## Context:\n{task.context}\n\n"
            f"## Instructions:\n"
            f"Focus ONLY on this specific task. Output FILE: blocks for any code changes.\n"
            f"Be concise and precise."
        )

        start_time = time.time()

        try:
            result = send_fn(task_prompt, model_id)
            task.execution_time = time.time() - start_time

            with self._lock:
                task.result = result
                task.status = TaskStatus.COMPLETED

            return result

        except Exception as e:
            task.execution_time = time.time() - start_time

            with self._lock:
                task.error = str(e)
                task.status = TaskStatus.FAILED

            return None

    def execute(
        self,
        tasks: list[SwarmTask],
        send_fn: Callable[[str, str], str | None],
        parallel: bool = True,
    ) -> SwarmResult:
        """Execute all tasks respecting dependencies.

        Args:
            tasks: List of tasks to execute
            send_fn: Function to send prompt to model
            parallel: Whether to execute independent tasks in parallel

        Returns:
            SwarmResult with all task results
        """
        import time

        start_time = time.time()
        models_used: set[str] = set()
        results: list[str] = []

        if not parallel:
            # Sequential execution
            for task in tasks:
                # Wait for dependencies
                for dep_id in task.dependencies:
                    dep_task = self.tasks.get(dep_id)
                    if dep_task and dep_task.status != TaskStatus.COMPLETED:
                        task.status = TaskStatus.SKIPPED
                        continue

                result = self.execute_task(task, send_fn)
                if result:
                    results.append(result)
                if task.model_used:
                    models_used.add(task.model_used)
        else:
            # Parallel execution with dependency management
            completed = set()
            remaining = list(tasks)

            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                while remaining:
                    # Find tasks with satisfied dependencies
                    ready = [t for t in remaining if all(d in completed for d in t.dependencies)]

                    if not ready:
                        # No tasks ready, dependencies might be failed
                        for t in remaining:
                            t.status = TaskStatus.SKIPPED
                        break

                    # Execute ready tasks in parallel
                    futures = {
                        executor.submit(self.execute_task, task, send_fn): task for task in ready
                    }

                    for future in as_completed(futures):
                        task = futures[future]
                        try:
                            result = future.result()
                            if result:
                                results.append(result)
                        except Exception as e:
                            task.error = str(e)
                            task.status = TaskStatus.FAILED

                        completed.add(task.id)
                        remaining.remove(task)
                        if task.model_used:
                            models_used.add(task.model_used)

        total_time = time.time() - start_time
        combined_output = "\n\n---\n\n".join(results) if results else None

        success = all(t.status == TaskStatus.COMPLETED for t in tasks)

        return SwarmResult(
            success=success,
            tasks=tasks,
            total_time=total_time,
            models_used=models_used,
            combined_output=combined_output,
        )

    def clear_tasks(self) -> None:
        """Clear all stored tasks."""
        self.tasks.clear()

    def get_task_graph(self) -> dict[str, list[str]]:
        """Get task dependency graph.

        Returns:
            Dict mapping task ID to list of dependent task IDs
        """
        return {task_id: task.dependencies for task_id, task in self.tasks.items()}
