"""
DSLighting Core Types - re-export DSAT models.

Type definitions re-exported from DSAT models and config.

Includes:
- Task types (TaskDefinition, TaskType, TaskMode)
- Optimization candidates (WorkflowCandidate)
- Data formats (Plan, ReviewResult, Task, etc.)
- Config types (LLMConfig, TaskConfig, etc.)
"""

try:
    # ===== Task types =====
    from dsat.models import (
        TaskDefinition,
        TaskType,
        TaskMode,
    )

    # ===== Optimization candidates =====
    from dsat.models import WorkflowCandidate

    # ===== Data formats =====
    from dsat.models import (
        ReviewResult,
        Plan,
        Task,
        TaskContract,
        StepPlan,
        FileArtifact,
        ComplexityScore,
        DecomposedPlan,
    )

    # ===== Config types (from dsat.config) =====
    from dsat.config import (
        LLMConfig,
        SandboxConfig,
        TaskConfig,
        RunConfig,
        AgentSearchConfig,
    )

except ImportError:
    # If DSAT is unavailable
    TaskDefinition = None
    TaskType = None
    TaskMode = None
    WorkflowCandidate = None
    ReviewResult = None
    Plan = None
    Task = None
    TaskContract = None
    StepPlan = None
    FileArtifact = None
    ComplexityScore = None
    DecomposedPlan = None
    LLMConfig = None
    SandboxConfig = None
    TaskConfig = None
    RunConfig = None
    AgentSearchConfig = None

__all__ = [
    # Task types
    "TaskDefinition",
    "TaskType",
    "TaskMode",
    # Optimization candidates
    "WorkflowCandidate",
    # Data formats
    "ReviewResult",
    "Plan",
    "Task",
    "TaskContract",
    "StepPlan",
    "FileArtifact",
    "ComplexityScore",
    "DecomposedPlan",
    # Config types
    "LLMConfig",
    "SandboxConfig",
    "TaskConfig",
    "RunConfig",
    "AgentSearchConfig",
]
