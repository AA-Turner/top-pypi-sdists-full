"""
DSLighting Common - Exceptions

Re-export dsat.common.exceptions.
"""
try:
    from dsat.common.exceptions import *
except ImportError:
    # If DSAT is unavailable, define basic exceptions locally.
    class DSLightingError(Exception):
        """Base exception for DSLighting"""
        pass

    class DataLoadError(DSLightingError):
        """Exception raised when data loading fails"""
        pass

    class AgentExecutionError(DSLightingError):
        """Exception raised when agent execution fails"""
        pass

__all__ = [
    "DSLightingError",
    "DataLoadError",
    "AgentExecutionError",
]
