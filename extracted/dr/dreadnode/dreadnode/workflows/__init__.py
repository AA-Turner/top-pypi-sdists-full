"""Authored multi-step agent pipelines.

A workflow is a graph of typed events and steps, authored in Python in a
capability's ``workflows/`` directory. Steps consume an event, do work (often
running an agent), and emit the next — so the edges of the graph *are* the event
types, and the topology is extractable without running any step body.

    from dreadnode.workflows import Workflow, WorkflowEvent, StartEvent, Ctx

    class Cloned(WorkflowEvent):
        repo_path: str

    workflow = Workflow(name="analysis", input=AnalysisInput)

    @workflow.step
    async def clone(ctx: Ctx, ev: StartEvent[AnalysisInput]) -> Cloned:
        ...

**Where the code lives.** The *authoring* surface and the compiler live here,
because they introspect user code. The topology document, fact log, fold, and
scheduler live in ``dreadnode-workflow-core`` — a tiny pure package shared with
the platform, so both execution hosts run the same scheduler and the same fold
rather than two implementations that can drift. They are re-exported here so
authors only ever import from one place.

See ``plans/workflows-prd.md`` for the full design.
"""

from dreadnode_workflow_core import (
    Action,
    ApprovalDecision,
    ApprovalOutcome,
    ApprovalRequest,
    Collect,
    CompleteRun,
    EmittedEvent,
    Fact,
    FactKind,
    FailRun,
    FailureClass,
    MaterializeFanOut,
    NodeFailure,
    NodeState,
    ReadyNode,
    RequestApproval,
    RunState,
    SkipNode,
    StartEvent,
    StopEvent,
    Topology,
    UnitKey,
    WorkflowEvent,
    check_min_success,
    fold,
    fold_incremental,
    next_actions,
    parse_unit,
    unit_key,
)

from dreadnode.workflows.compile import compile_workflow
from dreadnode.workflows.context import AgentResult, Ctx, ToolCall
from dreadnode.workflows.errors import CompileError, WorkflowCompileError
from dreadnode.workflows.host import (
    FactSink,
    MemoryFactSink,
    PlatformFactSink,
    RunResult,
    WorkflowHost,
    WorkflowRunCancelled,
)
from dreadnode.workflows.workflow import StepDef, Workflow

__all__ = [
    "Action",
    "AgentResult",
    "ApprovalDecision",
    "ApprovalOutcome",
    "ApprovalRequest",
    "Collect",
    "CompileError",
    "CompleteRun",
    "Ctx",
    "EmittedEvent",
    "Fact",
    "FactKind",
    "FactSink",
    "FailRun",
    "FailureClass",
    "MaterializeFanOut",
    "MemoryFactSink",
    "NodeFailure",
    "NodeState",
    "PlatformFactSink",
    "ReadyNode",
    "RequestApproval",
    "RunResult",
    "RunState",
    "SkipNode",
    "StartEvent",
    "StepDef",
    "StopEvent",
    "ToolCall",
    "Topology",
    "UnitKey",
    "Workflow",
    "WorkflowCompileError",
    "WorkflowEvent",
    "WorkflowHost",
    "WorkflowRunCancelled",
    "check_min_success",
    "compile_workflow",
    "fold",
    "fold_incremental",
    "next_actions",
    "parse_unit",
    "unit_key",
]
