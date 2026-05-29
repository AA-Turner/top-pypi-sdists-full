# Copyright (C) 2018-present Jesus Lara
#
"""Pydantic data models for the flowtask executor framework."""
from __future__ import annotations
from enum import Enum
from typing import Any, Literal, Optional
from pydantic import BaseModel, Field


class ExecutorType(str, Enum):
    """Supported executor backends."""

    LOCAL = "local"
    QWORKER = "qworker"
    PUBLISH = "publish"
    DOCKER = "docker"
    K8S = "k8s"


class ExecutorConfig(BaseModel):
    """Configuration for an executor instance.

    Attributes:
        type: The executor backend type.
        image: Container image (Docker/K8s only).
        namespace: Kubernetes namespace (K8s only).
        env: Extra environment variables passed to the container.
        timeout: Maximum execution time in seconds.
        priority: Queue priority key for qworker executor.
    """

    type: ExecutorType = ExecutorType.LOCAL
    image: Optional[str] = None
    namespace: Optional[str] = None
    env: dict[str, str] = Field(default_factory=dict)
    timeout: int = Field(default=600, ge=1)
    priority: Optional[str] = None

    @classmethod
    def from_yaml(cls, value: Any) -> "ExecutorConfig":
        """Build an ExecutorConfig from a task YAML executor field.

        Args:
            value: Can be None (→ LOCAL default), str (→ type name),
                   or dict (→ full config).

        Returns:
            A validated ExecutorConfig instance.

        Raises:
            ValueError: If value is not None, str, or dict.
        """
        if value is None:
            return cls(type=ExecutorType.LOCAL)
        if isinstance(value, str):
            return cls(type=ExecutorType(value))
        if isinstance(value, dict):
            return cls(**value)
        raise ValueError(
            f"executor must be None, a string, or a dict; got {type(value).__name__}"
        )


class ExecutionHandle(BaseModel):
    """Handle returned by dispatch() — identifies a running execution.

    Attributes:
        executor_type: The executor that produced this handle.
        execution_id: Unique identifier for this execution (container id, job name, uuid…).
        task_program: The program slug.
        task_name: The task identifier within the program.
        channel: The PUB/SUB or Stream channel for lifecycle events.
    """

    executor_type: ExecutorType
    execution_id: str
    task_program: str
    task_name: str
    channel: str


class TaskResult(BaseModel):
    """Result returned by run() when task execution completes.

    Attributes:
        status: One of "success" or "failed".
        result: The task's return value (if any).
        stats: Optional performance statistics from the task.
        error: Error message when status == "failed".
        execution_id: Matches ExecutionHandle.execution_id.
    """

    status: Literal["success", "failed", "timeout"] = "success"
    result: Any = None
    stats: Optional[Any] = None
    error: Optional[str] = None
    execution_id: Optional[str] = None
