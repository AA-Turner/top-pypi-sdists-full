"""Pipeline actions package."""

from agentic_devtools.cli.ci.pipeline.actions.apply_suggestions import ApplySuggestionsAction
from agentic_devtools.cli.ci.pipeline.actions.approve import ApproveAction
from agentic_devtools.cli.ci.pipeline.actions.critique_adjudication import CritiqueAdjudicationAction
from agentic_devtools.cli.ci.pipeline.actions.defer_suppressed import DeferSuppressedAction
from agentic_devtools.cli.ci.pipeline.actions.dispatch_conflict_resolution import (
    DispatchConflictResolutionAction,
)
from agentic_devtools.cli.ci.pipeline.actions.dispatch_repair import DispatchRepairAction
from agentic_devtools.cli.ci.pipeline.actions.guards import GuardsAction
from agentic_devtools.cli.ci.pipeline.actions.merge import MergeAction
from agentic_devtools.cli.ci.pipeline.actions.publish import PublishAction
from agentic_devtools.cli.ci.pipeline.actions.rebase import RebaseAction
from agentic_devtools.cli.ci.pipeline.actions.request_review import RequestReviewAction
from agentic_devtools.cli.ci.pipeline.actions.resolve_threads import ResolveThreadsAction
from agentic_devtools.cli.ci.pipeline.actions.retry_failed_session import RetryFailedSessionAction
from agentic_devtools.cli.ci.pipeline.actions.squash import SquashAction
from agentic_devtools.cli.ci.pipeline.actions.takeover import (
    TakeOverAutomationCommitAction,
    TakeOverCopilotCommitAction,
)

__all__ = [
    "ApplySuggestionsAction",
    "ApproveAction",
    "CritiqueAdjudicationAction",
    "DeferSuppressedAction",
    "DispatchConflictResolutionAction",
    "DispatchRepairAction",
    "GuardsAction",
    "MergeAction",
    "PublishAction",
    "RebaseAction",
    "RetryFailedSessionAction",
    "RequestReviewAction",
    "ResolveThreadsAction",
    "SquashAction",
    "TakeOverAutomationCommitAction",
    "TakeOverCopilotCommitAction",
]
