"""
Agent - High-Level Agent Interface (Compatibility Wrapper)

This module keeps the API-facing Agent stable while delegating to the
core Agent implementation. This avoids mismatched factory signatures
between DSLighting and DSAT.
"""

from pathlib import Path
from typing import Optional, Union

from dslighting.core.agent import Agent as CoreAgent
from dslighting.core.agent import AgentResult
from dslighting.core.data_loader import TaskContext


class Agent(CoreAgent):
    """
    Backward-compatible API Agent.

    This class simply inherits the core Agent to ensure the public API
    remains consistent and avoids DSAT factory signature mismatches.
    """

    # No overrides needed; core Agent already provides run() and config behavior.
    pass


__all__ = ["Agent", "AgentResult", "TaskContext"]
