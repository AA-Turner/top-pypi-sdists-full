# Copyright (C) 2018-present Jesus Lara
#
"""flowtask.executors — pluggable job executor framework.

Public API:
    AbstractJobExecutor — base class for all executor implementations
    ExecutorRegistry    — class-based executor registry
    register_executor   — decorator to register an executor class
    ExecutorConfig      — Pydantic config model
    ExecutionHandle     — returned by dispatch()
    TaskResult          — returned by run()
    ExecutorType        — enum of supported executor types
    ExecutorNotFound    — raised when executor name is unknown
    ExecutorConnectionError — raised on backend connectivity failure
    ExecutorError       — general executor runtime error
"""
from flowtask.executors.base import AbstractJobExecutor
from flowtask.executors.models import (
    ExecutorType,
    ExecutorConfig,
    ExecutionHandle,
    TaskResult,
)
from flowtask.executors.registry import ExecutorRegistry, register_executor
from flowtask.executors.exceptions import (
    ExecutorNotFound,
    ExecutorConnectionError,
    ExecutorError,
)
from flowtask.executors.events import ExecutorLifecyclePublisher
from flowtask.executors.resolver import resolve_executor, determine_execution_mode

# Import concrete executors to trigger @register_executor decorators
from flowtask.executors import local  # noqa: F401
from flowtask.executors import qworker  # noqa: F401
from flowtask.executors import publish  # noqa: F401

# Conditional imports for optional backend executors
try:
    from flowtask.executors import docker  # noqa: F401
except ImportError:
    pass  # aiodocker not installed

try:
    from flowtask.executors import k8s  # noqa: F401
except ImportError:
    pass  # kr8s not installed

__all__ = [
    "AbstractJobExecutor",
    "ExecutorType",
    "ExecutorConfig",
    "ExecutionHandle",
    "TaskResult",
    "ExecutorRegistry",
    "register_executor",
    "ExecutorNotFound",
    "ExecutorConnectionError",
    "ExecutorError",
    "ExecutorLifecyclePublisher",
    "local",
    "qworker",
    "publish",
    "resolve_executor",
    "determine_execution_mode",
]
