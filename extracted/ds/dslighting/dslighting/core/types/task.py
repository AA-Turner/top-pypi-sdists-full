"""
DSLighting Core Types - Task Definitions

Re-export dsat.models.task.
"""
try:
    from dsat.models.task import (
        TaskDefinition,
        TaskType,
        TaskMode,
    )
except ImportError:
    TaskDefinition = None
    TaskType = None
    TaskMode = None

__all__ = [
    "TaskDefinition",
    "TaskType",
    "TaskMode",
]
