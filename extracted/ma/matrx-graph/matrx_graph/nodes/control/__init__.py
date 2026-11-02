"""Control-flow node pack.

``control.barrier`` was REMOVED (ENGINE_SPEC §6.1 resolution, 2026-07-08):
§3 join semantics already make any multi-inbound node a synchronization
point (fires once when every inbound edge resolves), and §4.4 aggregated
dispatch synchronizes map fan-ins automatically (``control.gather``). The
old channel-counter executor was structurally broken for same-step Send
arrivals (audit E4). ``validate_definition`` tombstones the type with a
loud, actionable error.
"""

from matrx_graph.nodes.control.branch import (
    BranchConfig,
    BranchExecutor,
    BranchInput,
    BranchOutput,
)
from matrx_graph.nodes.control.gather import GatherExecutor
from matrx_graph.nodes.control.human_input import (
    HumanInputConfig,
    HumanInputExecutor,
    HumanInputInput,
    HumanInputOutput,
)
from matrx_graph.nodes.control.loop import LoopExecutor
from matrx_graph.nodes.control.map import MapExecutor
from matrx_graph.nodes.control.send import (
    SendConfig,
    SendExecutor,
    SendInput,
    SendOutput,
)

__all__ = [
    "BranchConfig",
    "BranchExecutor",
    "BranchInput",
    "BranchOutput",
    "GatherExecutor",
    "HumanInputConfig",
    "HumanInputExecutor",
    "HumanInputInput",
    "HumanInputOutput",
    "LoopExecutor",
    "MapExecutor",
    "SendConfig",
    "SendExecutor",
    "SendInput",
    "SendOutput",
]
