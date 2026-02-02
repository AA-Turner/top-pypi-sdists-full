"""
DSLighting 2.0 - Agents Layer

Re-export DSAT workflows.

BaseAgent is an alias for DSATWorkflow.
"""
try:
    from dsat.workflows.base import DSATWorkflow
    BaseAgent = DSATWorkflow
except ImportError:
    BaseAgent = None

__all__ = ["BaseAgent"]
