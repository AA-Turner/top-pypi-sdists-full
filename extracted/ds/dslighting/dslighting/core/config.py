"""
DSLighting Core Config - configuration class definitions.

Re-export dsat.config.
"""
try:
    from dsat.config import (
        LLMConfig,           # LLM configuration
        SandboxConfig,       # Sandbox configuration
        TaskConfig,          # Task configuration
        RunConfig,           # Run configuration
        AgentSearchConfig,   # Search configuration
    )
except ImportError:
    LLMConfig = None
    SandboxConfig = None
    TaskConfig = None
    RunConfig = None
    AgentSearchConfig = None

__all__ = [
    "LLMConfig",
    "SandboxConfig",
    "TaskConfig",
    "RunConfig",
    "AgentSearchConfig",
]
