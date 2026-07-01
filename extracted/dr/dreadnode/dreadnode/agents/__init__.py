import importlib
import typing as t

from dreadnode.agents import exceptions
from dreadnode.agents.tools import (
    FunctionCall,
    FunctionDefinition,
    Tool,
    ToolCall,
    ToolChoice,
    ToolDefinition,
    ToolMode,
    ToolResponse,
    Toolset,
    discover_tools_on_obj,
    tool,
    tool_method,
)
from dreadnode.core.hook import Hook

__all__ = [
    "Agent",
    "AgentJudge",
    "Continue",
    "Fail",
    "Finish",
    "FunctionCall",
    "FunctionDefinition",
    "Hook",
    "JudgeResult",
    "ProcessDecision",
    "ProcessJudge",
    "Reaction",
    "Retry",
    "RetryWithFeedback",
    "Tool",
    "ToolCall",
    "ToolChoice",
    "ToolDefinition",
    "ToolMode",
    "ToolResponse",
    "Toolset",
    "Trajectory",
    "discover_tools_on_obj",
    "events",
    "exceptions",
    "hooks",
    "mcp",
    "process_judge_hook",
    "reactions",
    "skills",
    "stopping",
    "subagent",
    "tool",
    "tool_method",
]

# Names that require deferred imports to break the circular dependency
# with generators.message. The cycle is:
#   message → agents.tools → agents/__init__ → reactions → message
_LAZY_NAMES = frozenset(
    {
        "events",
        "reactions",
        "stopping",
        "Agent",
        "AgentJudge",
        "JudgeResult",
        "ProcessDecision",
        "ProcessJudge",
        "process_judge_hook",
        "Trajectory",
        "Continue",
        "Fail",
        "Finish",
        "Reaction",
        "Retry",
        "RetryWithFeedback",
    }
)


def _lazy_init() -> None:
    """Perform deferred imports and model_rebuild() calls."""
    _events = importlib.import_module("dreadnode.agents.events")
    _reactions = importlib.import_module("dreadnode.agents.reactions")
    _stopping = importlib.import_module("dreadnode.agents.stopping")
    _agent = importlib.import_module("dreadnode.agents.agent")
    _trajectory = importlib.import_module("dreadnode.agents.trajectory")
    _judge = importlib.import_module("dreadnode.agents.judge")

    _Agent = _agent.Agent  # noqa: N806
    _Trajectory = _trajectory.Trajectory  # noqa: N806

    _Agent.model_rebuild()
    _Trajectory.model_rebuild()

    # Expose AgentJudge as ``Agent.Judge`` for discoverability. ``Agent`` is
    # the primary abstraction; ``Agent.Judge(...)`` is the specialized
    # construction mirror for trajectory-scoring use cases.
    _Agent.Judge = _judge.AgentJudge

    _process_judge = importlib.import_module("dreadnode.agents.process_judge")
    _hooks = importlib.import_module("dreadnode.agents.hooks")

    g = globals()
    g["events"] = _events
    g["reactions"] = _reactions
    g["stopping"] = _stopping
    g["Agent"] = _Agent
    g["AgentJudge"] = _judge.AgentJudge
    g["JudgeResult"] = _judge.JudgeResult
    g["ProcessDecision"] = _process_judge.ProcessDecision
    g["ProcessJudge"] = _process_judge.ProcessJudge
    g["process_judge_hook"] = _hooks.process_judge_hook
    g["Trajectory"] = _Trajectory
    g["Continue"] = _reactions.Continue
    g["Fail"] = _reactions.Fail
    g["Finish"] = _reactions.Finish
    g["Reaction"] = _reactions.Reaction
    g["Retry"] = _reactions.Retry
    g["RetryWithFeedback"] = _reactions.RetryWithFeedback


_SUBMODULES = frozenset({"hooks", "mcp", "skills", "subagent"})


def __getattr__(name: str) -> t.Any:
    if name in _LAZY_NAMES:
        _lazy_init()
        return globals()[name]
    if name in _SUBMODULES:
        mod = importlib.import_module(f".{name}", __name__)
        globals()[name] = mod
        return mod
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
