# Copyright (C) 2018-present Jesus Lara
#
"""Abstract base class for all flowtask job executors."""
from __future__ import annotations
import logging
from abc import ABC, abstractmethod
from flowtask.executors.models import ExecutorConfig, ExecutionHandle, TaskResult


class AbstractJobExecutor(ABC):
    """Abstract base class that all executor backends must implement.

    Subclasses are registered with the ExecutorRegistry via the
    @register_executor decorator and instantiated by resolve_executor().

    Args:
        config: Validated ExecutorConfig for this executor instance.
        **kwargs: Additional keyword arguments passed at construction time.
    """

    def __init__(self, config: ExecutorConfig, **kwargs):
        self._config = config
        self.logger = logging.getLogger(f"FlowTask.Executor.{self.name()}")

    @classmethod
    def name(cls) -> str:
        """Return the registry name for this executor type.

        Subclasses MUST override this method and return the exact name
        used in the @register_executor decorator.

        Returns:
            The string name used in ExecutorRegistry.

        Raises:
            NotImplementedError: If a subclass does not override this method.
        """
        raise NotImplementedError(
            f"{cls.__name__} must implement name() and return the registry name."
        )

    @abstractmethod
    async def dispatch(
        self,
        program: str,
        task: str,
        task_id: str,
        **kwargs,
    ) -> ExecutionHandle:
        """Fire-and-forget: start the task and return immediately.

        Args:
            program: The program slug.
            task: The task identifier within the program.
            task_id: A unique UUID for this execution instance.
            **kwargs: Executor-specific parameters forwarded to the backend.

        Returns:
            An ExecutionHandle that identifies the running task.
        """

    @abstractmethod
    async def run(
        self,
        program: str,
        task: str,
        task_id: str,
        **kwargs,
    ) -> TaskResult:
        """Block until the task completes and return the result.

        Args:
            program: The program slug.
            task: The task identifier within the program.
            task_id: A unique UUID for this execution instance.
            **kwargs: Executor-specific parameters forwarded to the backend.

        Returns:
            A TaskResult with status, result, stats, and optional error.
        """

    async def close(self) -> None:
        """Release any resources held by this executor (connections, sockets…).

        Base implementation is a no-op. Override in subclasses that hold
        persistent connections.
        """
