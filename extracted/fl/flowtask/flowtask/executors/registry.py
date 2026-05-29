# Copyright (C) 2018-present Jesus Lara
#
"""Executor registry for the flowtask executor framework."""
from typing import TYPE_CHECKING
from flowtask.executors.exceptions import ExecutorNotFound

if TYPE_CHECKING:
    from flowtask.executors.base import AbstractJobExecutor


class ExecutorRegistry:
    """Registry mapping executor names to their classes.

    Uses classmethods so it can be used without instantiation. The registry
    is populated by the @register_executor decorator.
    """

    _executors: dict[str, type] = {}

    @classmethod
    def register(cls, name: str):
        """Decorator factory that registers an executor class under a given name.

        Args:
            name: The name to register the executor under (e.g., "local", "docker").

        Returns:
            A decorator that registers the class and returns it unchanged.
        """
        def decorator(executor_class: type) -> type:
            cls._executors[name] = executor_class
            return executor_class
        return decorator

    @classmethod
    def get(cls, name: str) -> type:
        """Return the executor class registered under name.

        Args:
            name: The executor name to look up.

        Returns:
            The executor class.

        Raises:
            ExecutorNotFound: If no executor is registered under name.
        """
        if name not in cls._executors:
            available = ", ".join(cls._executors.keys()) or "(none)"
            raise ExecutorNotFound(
                f"Executor '{name}' not found. Available: {available}"
            )
        return cls._executors[name]

    @classmethod
    def available(cls) -> list[str]:
        """Return a list of all registered executor names.

        Returns:
            Sorted list of registered executor name strings.
        """
        return sorted(cls._executors.keys())


def register_executor(name: str):
    """Convenience function — same as ExecutorRegistry.register(name).

    Args:
        name: The name to register the executor class under.

    Returns:
        Decorator that registers and returns the class unchanged.
    """
    return ExecutorRegistry.register(name)
