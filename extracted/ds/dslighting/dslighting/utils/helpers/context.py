"""
DSLighting Utils - Context Manager

Re-export dsat.utils.context.ContextManager.
"""
try:
    from dsat.utils.context import ContextManager
except ImportError:
    ContextManager = None

__all__ = ["ContextManager"]
