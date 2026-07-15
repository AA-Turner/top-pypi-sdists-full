"""
cvc.sdk — Multi-Agent Cognitive Memory SDK.

Public API for using CVC as a hive mind platform.

Usage::

    from cvc.sdk import HiveMind

    hive = HiveMind(".cvc")
    agent = hive.register_agent("SPC-01", role="specialist", squad="aegis")
    agent.commit("Analysis complete", content={"findings": "..."})
    recent = agent.context(limit=5)
"""

from cvc.sdk.agent import Agent
from cvc.sdk.ambient import AmbientChannel
from cvc.sdk.compactor import CompactionResult, HiveCompactor
from cvc.sdk.events import (
    AGENT_REGISTERED,
    AGENT_TARGETED,
    BRANCH_UPDATED,
    COMMIT_CREATED,
    SQUAD_MERGED,
    SYNC_COMPLETED,
    EventBus,
    EventCallback,
    EventEnvelope,
    Subscription,
)
from cvc.sdk.hivemind import HiveMind
from cvc.sdk.registry import AgentRegistry
from cvc.sdk.router import Router, RoutingConfig, default_branches_for_rank, resolve_branch_patterns
from cvc.sdk.sync import GossipProtocol, SyncEngine, SyncResult

__all__ = [
    # Core classes
    "HiveMind",
    "Agent",
    "AgentRegistry",
    "Router",
    "EventBus",
    # Ambient legibility / telepathy (Fable5 Phase 5)
    "AmbientChannel",
    # Compaction (Phase 7)
    "HiveCompactor",
    "CompactionResult",
    # Sync (Phase 4)
    "SyncEngine",
    "SyncResult",
    "GossipProtocol",
    # Events (Phase 5)
    "EventCallback",
    "EventEnvelope",
    "Subscription",
    # Routing (Phase 6)
    "RoutingConfig",
    "resolve_branch_patterns",
    # Utilities
    "default_branches_for_rank",
    # Event constants
    "COMMIT_CREATED",
    "AGENT_TARGETED",
    "BRANCH_UPDATED",
    "SQUAD_MERGED",
    "AGENT_REGISTERED",
    "SYNC_COMPLETED",
]
