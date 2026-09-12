"""Pure workflow core — topology, facts, fold, scheduler.

Shared by both execution hosts so they cannot disagree on control flow. Nothing
here does I/O, reads a clock, or uses randomness; the only dependency is pydantic.

Consumers:

* ``dreadnode`` (SDK) — the runtime host, plus the authoring surface and
  compiler that *produce* the topology this package consumes.
* ``dreadnode-server`` (API) — folds appended facts into the queryable
  projection, and (when durability lands) runs the platform host.
"""

from dreadnode_workflow_core.events import (
    ApprovalDecision,
    ApprovalOutcome,
    ApprovalRequest,
    Collect,
    FailureClass,
    NodeFailure,
    StartEvent,
    StopEvent,
    WorkflowEvent,
)
from dreadnode_workflow_core.facts import (
    Fact,
    FactKind,
    UnitKey,
    parse_unit,
    unit_key,
)
from dreadnode_workflow_core.scheduler import (
    Action,
    CompleteRun,
    FailRun,
    MaterializeFanOut,
    ReadyNode,
    RequestApproval,
    SkipNode,
    check_min_success,
    next_actions,
)
from dreadnode_workflow_core.state import (
    EmittedEvent,
    NodeState,
    NodeStatus,
    RunState,
    RunStatus,
    fold,
    fold_incremental,
)
from dreadnode_workflow_core.topology import (
    TOPOLOGY_SIZE_CAP_BYTES,
    TOPOLOGY_VERSION,
    EdgeKind,
    EventTypeDoc,
    FanOutPoint,
    FieldDoc,
    JoinPoint,
    NodeConfig,
    NodeConsumes,
    NodeEmit,
    NodeKind,
    ParamDoc,
    SourceSpan,
    Topology,
    TopologyEdge,
    TopologyInput,
    TopologyNode,
    WorkflowConfig,
)

__all__ = [
    "TOPOLOGY_SIZE_CAP_BYTES",
    "TOPOLOGY_VERSION",
    "Action",
    "ApprovalDecision",
    "ApprovalOutcome",
    "ApprovalRequest",
    "Collect",
    "CompleteRun",
    "EdgeKind",
    "EmittedEvent",
    "EventTypeDoc",
    "Fact",
    "FactKind",
    "FailRun",
    "FailureClass",
    "FanOutPoint",
    "FieldDoc",
    "JoinPoint",
    "MaterializeFanOut",
    "NodeConfig",
    "NodeConsumes",
    "NodeEmit",
    "NodeFailure",
    "NodeKind",
    "NodeState",
    "NodeStatus",
    "ParamDoc",
    "ReadyNode",
    "RequestApproval",
    "RunState",
    "RunStatus",
    "SkipNode",
    "SourceSpan",
    "StartEvent",
    "StopEvent",
    "Topology",
    "TopologyEdge",
    "TopologyInput",
    "TopologyNode",
    "UnitKey",
    "WorkflowConfig",
    "WorkflowEvent",
    "check_min_success",
    "fold",
    "fold_incremental",
    "next_actions",
    "parse_unit",
    "unit_key",
]
