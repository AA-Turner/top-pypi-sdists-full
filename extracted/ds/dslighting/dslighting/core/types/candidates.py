"""
DSLighting Core Types - Workflow Candidates

Re-export dsat.models.candidates.WorkflowCandidate.
"""
try:
    from dsat.models.candidates import WorkflowCandidate
except ImportError:
    WorkflowCandidate = None

__all__ = ["WorkflowCandidate"]
