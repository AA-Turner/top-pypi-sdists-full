"""Exception hierarchy for the Chronos workflow runtime.

All workflow-specific errors derive from :class:`WorkflowError` so callers can
catch the whole family with one clause. Inside a running workflow script the
injected ``agent()`` primitive soft-fails (returns ``None``) for agent-side
problems and raises ONLY :class:`BudgetExceededError`,
:class:`WorkflowCancelledError`, and :class:`WorkflowLimitError`.
"""

from __future__ import annotations


class WorkflowError(Exception):
    """Base class for all workflow errors."""


class WorkflowScriptError(WorkflowError):
    """A workflow script failed to compile or violated a script pre-check.

    ``lineno`` and ``excerpt`` are expressed in the USER's script coordinates
    (the ``async def __workflow_main__():`` wrapper line is already stripped).
    """

    def __init__(
        self,
        message: str,
        *,
        lineno: int | None = None,
        excerpt: str | None = None,
    ) -> None:
        super().__init__(message)
        self.lineno = lineno
        self.excerpt = excerpt


class BudgetExceededError(WorkflowError):
    """The workflow's USD budget ceiling has been reached."""


class WorkflowCancelledError(WorkflowError):
    """The workflow was cancelled (cancel endpoint / service shutdown)."""


class WorkflowLimitError(WorkflowError):
    """A hard runtime limit (e.g. ``max_total_calls``) was hit."""
