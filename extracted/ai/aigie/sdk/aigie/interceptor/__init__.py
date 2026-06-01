"""
Aigie Interceptor Module - Real-time runtime interception for LLM calls.

This module provides the infrastructure for intercepting LLM calls before
and after execution, enabling:
- Context drift detection and correction
- Tool error prevention and recovery
- Runtime stability enforcement
- Automatic fix application
"""

from .chain import InterceptorChain
from .context_tracker import ContextTracker
from .protocols import (
    FixAction,
    FixActionType,
    InterceptionBlockedError,
    InterceptionContext,
    InterceptionDecision,
    InterceptionRetryError,
    PostCallHook,
    PostCallResult,
    PreCallHook,
    PreCallResult,
)

__all__ = [
    # Enums and Data Classes
    "InterceptionDecision",
    "InterceptionContext",
    "PreCallResult",
    "PostCallResult",
    "FixAction",
    "FixActionType",
    # Protocols
    "PreCallHook",
    "PostCallHook",
    # Exceptions
    "InterceptionBlockedError",
    "InterceptionRetryError",
    # Core Classes
    "InterceptorChain",
    "ContextTracker",
]
