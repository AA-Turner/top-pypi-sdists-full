# Copyright (C) 2018-present Jesus Lara
#
"""Executor exceptions for flowtask executor framework."""
from typing import Optional
from flowtask.exceptions import FlowTaskError


class ExecutorNotFound(FlowTaskError):
    """Raised when an executor name is not found in the registry."""

    def __init__(self, message: Optional[str] = None, status: int = 404):
        super().__init__(message or "Executor not found", status)


class ExecutorConnectionError(FlowTaskError):
    """Raised when the executor cannot connect to its backend (Docker, K8s, Redis)."""

    def __init__(self, message: Optional[str] = None, status: int = 503):
        super().__init__(message or "Executor connection error", status)


class ExecutorError(FlowTaskError):
    """General executor runtime error."""

    def __init__(self, message: Optional[str] = None, status: int = 500):
        super().__init__(message or "Executor error", status)
