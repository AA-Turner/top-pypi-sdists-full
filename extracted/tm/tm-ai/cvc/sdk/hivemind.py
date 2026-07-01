"""
cvc.sdk.hivemind — The main ``HiveMind`` class.

Top-level entry point for using CVC as a multi-agent cognitive memory
platform.  Wraps ``CVCEngine`` + ``ContextDatabase`` with a clean,
developer-friendly API.

Usage::



    hive = HiveMind(".cvc")
    zeus = hive.register_agent("MC-01", role="mission_controller", rank="zeus")
    zeus.commit("Mission initialized", action_type="DIRECTIVE")

    captain = hive.register_agent("CPT-AEG-01", role="captain", rank="captain", squad="aegis")
    captain.commit("Squad Aegis: tasking specialists", target_agent_id="SPC-AEG-01")
"""

from __future__ import annotations

import logging
import threading
from pathlib import Path
from typing import Any
import asyncio
import threading

_hive_lock = threading.Lock()

from cvc.core.database import ContextDatabase
from cvc.core.models import (
    CognitiveCommit,
    CommitMetadata,
    CommitType,
    ContentBlob,
    ContextMessage,
    CVCBranchRequest,
    CVCConfig,
    CVCMergeRequest,
)
from cvc.operations.engine import CVCEngine
from cvc.sdk.agent import Agent
from cvc.sdk.compactor import CompactionResult, HiveCompactor, SummariserFn
from cvc.sdk.events import AGENT_REGISTERED, SQUAD_MERGED, EventBus, EventCallback, Subscription
from cvc.sdk.registry import AgentRegistry
from cvc.sdk.router import Router, RoutingConfig, default_branches_for_rank

logger = logging.getLogger("cvc.sdk.hivemind")

# Rank ordering for rank-priority merge: higher index = higher priority
_RANK_ORDER: dict[str, int] = {
    "specialist": 0,
    "captain": 1,
    "mission_controller": 2,
    "zeus": 3,
}


class HiveMind:
    """
    Multi-agent cognitive memory — the hive mind.

    Opens (or initializes) a CVC store and provides methods for
    agent registration, commit, recall, branching, and merging.
    Thread-safe for concurrent agent operations.
    """

    def __init__(self, path: str | Path = ".cvc", *, vector_enabled: bool | None = None) -> None:
        cvc_root = Path(path)
        self._config = CVCConfig(
            cvc_root=cvc_root,
            db_path=cvc_root / "cvc.db",
            objects_dir=cvc_root / "objects",
            branches_dir=cvc_root / "branches",
            chroma_persist_dir=cvc_root / "chroma",
            pageindex_dir=cvc_root / "pageindex",
        )
        if vector_enabled is not None:
            self._config.vector_enabled = vector_enabled
        self._config.ensure_dirs()
        self._db = ContextDatabase(self._config)
        self._engine = CVCEngine(self._config, self._db)
        self._event_bus = EventBus()
        self._agents_dir = cvc_root / "agents"
        self._agents_dir.mkdir(parents=True, exist_ok=True)
        self._registry = AgentRegistry(self._db.index, self._agents_dir)
        # Merge any agent JSON files that were synced from other nodes
        self._registry.load_from_disk()
        # Load routing config from .cvc/routing.yaml (Phase 6)
        self._routing_config = RoutingConfig.load(cvc_root)
        self._router = Router(self._db.index, self._registry, self._routing_config)
        self._agents: dict[str, Agent] = {}
        # Thread lock for concurrent multi-agent writes (Phase 3)
        self._write_lock = threading.Lock()
        # Context compaction (Phase 7)
        self._compactor = HiveCompactor(self._db)

    # -- Properties --------------------------------------------------------

    @property
    def db(self) -> ContextDatabase:
        return self._db

    @property
    def engine(self) -> CVCEngine:
        return self._engine

    @property
    def events(self) -> EventBus:
        return self._event_bus

    @property
    def registry(self) -> AgentRegistry:
        return self._registry

    @property
    def router(self) -> Router:
        return self._router

    @property
    def routing_config(self) -> RoutingConfig:
        return self._routing_config

    def save_routing_config(self) -> None:
        """Persist the current routing config to ``.cvc/routing.yaml``."""
        self._routing_config.save(self._config.cvc_root)

    # -- Compaction (Phase 7) -----------------------------------------------

    @property
    def compactor(self) -> HiveCompactor:
        """The hive mind's compactor for context distillation."""
        return self._compactor

    def compact(
        self,
        *,
        strategy: str = "summarize",
        max_age_hours: float = 24.0,
        branch: str | None = None,
        min_commits: int = 3,
    ) -> CompactionResult:
        """Compact old commits into distilled summaries.

        Original commits are NEVER deleted — distilled commits are additive.

        Parameters
        ----------
        strategy:
            ``"summarize"`` — create summary commits for old chains.
        max_age_hours:
            Commits older than this are candidates for compaction.
        branch:
            Compact only this branch, or all branches if ``None``.
        min_commits:
            Minimum eligible commits required to trigger compaction.
        """
        return self._compactor.compact(
            strategy=strategy,
            max_age_hours=max_age_hours,
            branch=branch,
            min_commits=min_commits,
        )

    def auto_anchor(
        self,
        *,
        branch: str | None = None,
        every_n: int = 10,
    ) -> CompactionResult:
        """Create periodic anchor commits for faster sync and delta compression.

        Parameters
        ----------
        branch:
            Check only this branch, or all branches if ``None``.
        every_n:
            Create an anchor after this many commits since the last one.
        """
        return self._compactor.auto_anchor(branch=branch, every_n=every_n)

    def set_summariser(self, fn: SummariserFn) -> None:
        """Set a custom summariser function for compaction.

        The function receives a list of ``CognitiveCommit`` and returns
        a summary string.  Use this to plug in an LLM-powered summariser::

            def llm_summarise(commits):
                text = "\\n".join(c.message for c in commits)
                return my_llm.summarize(text)

            hive.set_summariser(llm_summarise)
        """
        self._compactor.summariser = fn

    # -- Event bus convenience (Phase 5) -----------------------------------

    def on(self, event: str, callback: EventCallback) -> None:
        """Register a synchronous event handler on the hive mind.

        Example::

            hive.on("commit.created", lambda e: print(e["commit_hash"]))
        """
        self._event_bus.on(event, callback)

    def on_async(self, event: str, callback: Any) -> None:
        """Register an async event handler."""
        self._event_bus.on_async(event, callback)

    def off(self, event: str, callback: EventCallback | None = None) -> None:
        """Remove an event handler."""
        self._event_bus.off(event, callback)

    def subscribe(
        self,
        subscriber_id: str,
        events: list[str] | None = None,
        *,
        agent_filter: str | None = None,
        replay: bool = False,
    ) -> Subscription:
        """Create a queue-based subscription for event streaming."""
        return self._event_bus.subscribe(
            subscriber_id, events, agent_filter=agent_filter, replay=replay,
        )

    def unsubscribe(self, subscriber_id: str) -> None:
        """Remove a queue-based subscription."""
        self._event_bus.unsubscribe(subscriber_id)

    # -- Agent management --------------------------------------------------

    def register_agent(
        self,
        agent_id: str,
        *,
        name: str | None = None,
        role: str | None = None,
        rank: str | None = None,
        squad: str | None = None,
        capabilities: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        readable_branches: list[str] | None = None,
        writable_branches: list[str] | None = None,
        agent_branch: bool = False,
    ) -> Agent:
        """
        Register an agent and return an ``Agent`` handle.

        If the agent already exists, its profile is updated.
        If a squad is specified, the squad branch is auto-created.
        If no readable/writable branches are given, defaults are
        computed from the agent's rank (specialist → squad only,
        captain → squad + global read, zeus → global).
        If *agent_branch* is True, a per-agent branch ``agent/{id}``
        is created.
        """
        # Auto-compute branch ACL from rank when not explicitly given
        if readable_branches is None and writable_branches is None:
            readable_branches, writable_branches = default_branches_for_rank(rank, squad)

        self._registry.register(
            agent_id,
            name=name,
            role=role,
            rank=rank,
            squad=squad,
            capabilities=capabilities,
            metadata=metadata,
            readable_branches=readable_branches,
            writable_branches=writable_branches,
        )

        # Auto-create squad branch
        if squad:
            self._router.ensure_squad_branch(squad)

        # Optionally create per-agent branch
        if agent_branch:
            self._router.ensure_agent_branch(agent_id)

        agent = Agent(
            agent_id=agent_id,
            db=self._db,
            registry=self._registry,
            router=self._router,
            event_bus=self._event_bus,
            engine=self._engine,
            write_lock=self._write_lock,
        )
        self._agents[agent_id] = agent

        self._event_bus.emit(AGENT_REGISTERED, {
            "agent_id": agent_id,
            "role": role,
            "rank": rank,
            "squad": squad,
        })

        return agent

    def get_agent(self, agent_id: str) -> Agent | None:
        """Get a previously registered Agent handle."""
        if agent_id in self._agents:
            return self._agents[agent_id]
        # Check registry
        profile = self._registry.get(agent_id)
        if profile is None:
            return None
        agent = Agent(
            agent_id=agent_id,
            db=self._db,
            registry=self._registry,
            router=self._router,
            event_bus=self._event_bus,
            engine=self._engine,
            write_lock=self._write_lock,
        )
        self._agents[agent_id] = agent
        return agent

    def list_agents(
        self,
        *,
        squad: str | None = None,
        rank: str | None = None,
    ) -> list[dict[str, Any]]:
        """List all registered agents."""
        return self._registry.list(squad=squad, rank=rank)

    # -- Branching & merging -----------------------------------------------

    def branch(self, name: str, *, description: str = "", source_commit: str | None = None) -> str:
        """Create a new branch. Returns the source commit hash."""
        resp = self._engine.branch(CVCBranchRequest(
            name=name,
            source_commit=source_commit,
            description=description,
        ))
        if not resp.success:
            raise RuntimeError(resp.message)
        return resp.commit_hash or ""

    def merge(self, source: str, target: str = "main") -> str:
        """Merge source branch into target. Returns the merge commit hash."""
        resp = self._engine.merge(CVCMergeRequest(
            source_branch=source,
            target_branch=target,
        ))
        if not resp.success:
            raise RuntimeError(resp.message)
        return resp.commit_hash or ""

    def merge_squads(
        self,
        target: str = "main",
        *,
        strategy: str = "all",
    ) -> list[str]:
        """Merge squad branches into the target branch.

        Strategies:
        - ``"all"`` (default): merge every squad branch in alphabetical order.
        - ``"rank-priority"``: merge in ascending rank order so higher ranks
          are merged last (and thus win conflicts).
        - ``"timestamp"``: merge oldest head-commit first so the newest
          squad wins conflicts.
        """
        squad_branches = [
            bp for bp in self._db.index.list_branches()
            if bp.name.startswith("squad/") and bp.name != target
        ]
        if not squad_branches:
            return []

        if strategy == "rank-priority":
            squad_branches = self._sort_by_rank_priority(squad_branches)
        elif strategy == "timestamp":
            squad_branches.sort(key=lambda bp: bp.created_at)
        else:
            squad_branches.sort(key=lambda bp: bp.name)

        merged: list[str] = []
        for bp in squad_branches:
            try:
                h = self.merge(bp.name, target)
                merged.append(h)
                self._event_bus.emit(SQUAD_MERGED, {
                    "source": bp.name,
                    "target": target,
                    "commit_hash": h,
                    "strategy": strategy,
                })
            except RuntimeError as e:
                logger.warning("Failed to merge %s: %s", bp.name, e)
        return merged

    def _sort_by_rank_priority(
        self, branches: list[Any],
    ) -> list[Any]:
        """Sort branch pointers so that higher-ranked squads are merged last."""
        def _squad_max_rank(bp: Any) -> int:
            squad_name = bp.name.removeprefix("squad/")
            agents = self._registry.list(squad=squad_name)
            if not agents:
                return -1
            return max(
                _RANK_ORDER.get((a.get("rank") or "").lower(), -1)
                for a in agents
            )
        return sorted(branches, key=_squad_max_rank)

    # -- Query -------------------------------------------------------------

    def log(
        self,
        *,
        branch: str | None = None,
        agent_id: str | None = None,
        squad: str | None = None,
        limit: int = 50,
    ) -> list[CognitiveCommit]:
        """Query the commit log with optional filters."""
        if agent_id:
            return self._db.index.list_commits_by_agent(agent_id, limit=limit)
        if squad:
            return self._db.index.list_commits_by_squad(squad, limit=limit)
        return self._db.index.list_commits(branch=branch, limit=limit)

    def recall(self, query: str, *, limit: int = 5) -> list[CognitiveCommit]:
        """Global semantic search across the entire hive mind."""
        if self._db.vectors.available:
            results = self._db.vectors.query(query, n_results=limit)
            if results:
                commits = []
                for doc_id in results:
                    c = self._db.index.get_commit(doc_id)
                    if c is not None:
                        commits.append(c)
                return commits
        return self._db.index.search_commits(query, limit=limit)

    # -- Status ------------------------------------------------------------

    def status(self) -> dict[str, Any]:
        """Return a summary of the hive mind state."""
        branches = self._db.index.list_branches()
        agents = self._registry.list()
        return {
            "branch_count": len(branches),
            "branches": [b.name for b in branches],
            "agent_count": len(agents),
            "agents": [a["agent_id"] for a in agents],
            "active_branch": self._engine.active_branch,
            "head_hash": self._engine.head_hash,
        }


# ---------------------------------------------------------------------------
# HiveMemory — The shared cognitive space (The Plüberous)
# ---------------------------------------------------------------------------

HIVE_MEMORY_BRANCH = "hive/memory"


class HiveMemory:
    """
    Shared memory space for the Hive Mind.

    Agents NEVER communicate directly — they read/write to this shared
    memory.  Each write is a CVC commit on the ``hive/memory`` branch
    with ``action_type="HIVE_MEMORY"`` in metadata.  Communication is
    emergent from shared state.

    Categories:
        - decisions — resolved choices, architectural decisions
        - findings — discovered facts, analysis results
        - tasks — work items, delegated tasks
        - alerts — warnings, errors, security issues
        - general — uncategorized entries
    """

    CATEGORIES = ("decisions", "findings", "tasks", "alerts", "general")

    def __init__(self, hive: HiveMind) -> None:
        self._hive = hive
        self._db = hive.db
        self._engine = hive.engine
        self._lock = threading.Lock()
        self._ensure_branch()

    def _ensure_branch(self) -> None:
        """Create the hive/memory branch if it doesn't exist."""
        bp = self._db.index.get_branch(HIVE_MEMORY_BRANCH)
        if bp is None:
            try:
                self._hive.branch(HIVE_MEMORY_BRANCH, description="Shared hive memory")
            except RuntimeError:
                pass  # Branch may exist from a race

    async def write(
        self,
        agent_id: str,
        content: str,
        *,
        category: str = "general",
        tags: list[str] | None = None,
        metadata_extra: dict[str, Any] | None = None,
    ) -> str:
        """
        Write an entry to the shared hive memory.

        Returns the commit hash.
        """
        if category not in self.CATEGORIES:
            category = "general"

        blob = ContentBlob(
            messages=[ContextMessage(
                role="assistant",
                content=content,
            )],
            tool_outputs={"category": category, "tags": tags or [], **(metadata_extra or {})},
        )

        meta = CommitMetadata(
            agent_id=agent_id,
            tags=tags or [],
            action_type="HIVE_MEMORY",
        )

        with self._lock:
            bp = self._db.index.get_branch(HIVE_MEMORY_BRANCH)
            if bp is None:
                self._ensure_branch()
                bp = self._db.index.get_branch(HIVE_MEMORY_BRANCH)
            if bp is None:
                raise RuntimeError("Failed to create hive/memory branch")

            commit = CognitiveCommit(
                parent_hashes=[bp.head_hash],
                commit_type=CommitType.CHECKPOINT,
                message=f"[{category}] {content[:80]}",
                content_blob=blob,
                metadata=meta,
            )

            commit_hash = self._db.store_commit(commit)
            self._db.index.advance_head(HIVE_MEMORY_BRANCH, commit_hash)

        logger.info(
            "Hive memory write by %s [%s]: %s",
            agent_id, category, content[:60],
        )
        return commit_hash

    async def read(
        self,
        query: str = "",
        *,
        category: str | None = None,
        agent_id: str | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """
        Read from hive memory with optional filters.

        Returns a list of memory entries as dicts.
        """
        # Get commits from the hive/memory branch
        commits = await _run_locked(self._db.index.list_commits, branch=HIVE_MEMORY_BRANCH, limit=limit * 3)

        results: list[dict[str, Any]] = []
        for c in commits:
            meta = c.metadata if hasattr(c, "metadata") else CommitMetadata()
            if hasattr(meta, "model_dump"):
                meta_dict = meta.model_dump() if hasattr(meta, "model_dump") else {}
            else:
                meta_dict = {}

            entry_agent = meta_dict.get("agent_id", "") if isinstance(meta_dict, dict) else ""
            tool_outputs = {}
            if hasattr(c, "content_blob") and hasattr(c.content_blob, "tool_outputs"):
                tool_outputs = c.content_blob.tool_outputs or {}
            entry_cat = tool_outputs.get("category", "general")
            entry_tags = tool_outputs.get("tags", [])

            # Apply filters
            if category and entry_cat != category:
                continue
            if agent_id and entry_agent != agent_id:
                continue

            # Extract content from messages
            content = ""
            if hasattr(c, "content_blob") and c.content_blob.messages:
                content = c.content_blob.messages[0].content

            # Text search filter
            if query and query.lower() not in content.lower() and query.lower() not in c.message.lower():
                continue

            results.append({
                "id": c.commit_hash[:16] if hasattr(c, "commit_hash") else "",
                "agent_id": entry_agent,
                "content": content,
                "category": entry_cat,
                "tags": entry_tags,
                "timestamp": meta_dict.get("timestamp", 0) if isinstance(meta_dict, dict) else 0,
                "commit_hash": c.commit_hash if hasattr(c, "commit_hash") else "",
                "message": c.message if hasattr(c, "message") else "",
            })

            if len(results) >= limit:
                break

        return results

    async def read_recent(self, *, limit: int = 20) -> list[dict[str, Any]]:
        """Get the most recent hive memory entries."""
        return await self.read(limit=limit)

    async def read_by_category(self, category: str, *, limit: int = 20) -> list[dict[str, Any]]:
        """Filter hive memory by category."""
        return await self.read(category=category, limit=limit)

    async def read_by_agent(self, agent_id: str, *, limit: int = 20) -> list[dict[str, Any]]:
        """Get entries contributed by a specific agent."""
        return await self.read(agent_id=agent_id, limit=limit)

    async def stats(self) -> dict[str, Any]:
        """Get hive memory statistics."""
        all_entries = await self.read(limit=1000)
        categories: dict[str, int] = {}
        agents: set[str] = set()
        for e in all_entries:
            cat = e.get("category", "general")
            categories[cat] = categories.get(cat, 0) + 1
            agents.add(e.get("agent_id", ""))
        return {
            "total_entries": len(all_entries),
            "categories": categories,
            "contributing_agents": list(agents),
            "agent_count": len(agents),
        }

    async def summary_context(self, *, limit: int = 5) -> str:
        """
        Build a context string summarizing recent hive memory for agent injection.

        This is injected into agent system prompts so they are aware of
        the shared hive state.
        """
        entries = await self.read_recent(limit=limit)
        if not entries:
            return ""
        lines = ["## Hive Memory (Recent Shared Knowledge)"]
        for e in entries:
            agent = e.get("agent_id", "unknown")
            cat = e.get("category", "general")
            content = e.get("content", "")[:200]
            lines.append(f"- [{cat}] ({agent}): {content}")
        return "\n".join(lines)

    # -- Sync (Phase 4 — CRDT distributed sync) -------------------------

    def sync(self, remote: HiveMind) -> Any:
        """Bidirectional G-Set CRDT sync with another HiveMind instance.

        All commits, blobs, branches, and agent registries are merged
        using set-union semantics — no conflicts possible.

        Returns a ``SyncResult`` with push/pull counts.
        """
        from cvc.sdk.sync import SyncEngine
        engine = SyncEngine(self._db)
        result = engine.sync_local(remote._db)
        # Re-merge agent JSON files that may have arrived
        self._registry.load_from_disk()
        return result

    def export_pack(self, output_path: str | Path) -> int:
        """Export all commits to a portable ``.cvcpack`` archive.

        Returns the number of commits exported.
        """
        from cvc.sdk.sync import SyncEngine
        engine = SyncEngine(self._db)
        return engine.export_pack(Path(output_path))

    def import_pack(self, pack_path: str | Path) -> Any:
        """Import a ``.cvcpack`` archive (G-Set union merge).

        Returns a ``SyncResult``.
        """
        from cvc.sdk.sync import SyncEngine
        engine = SyncEngine(self._db)
        result = engine.import_pack(Path(pack_path))
        self._registry.load_from_disk()
        return result

    def start_gossip(
        self,
        peers: list[HiveMind],
        *,
        interval_seconds: float = 30.0,
    ) -> None:
        """Start a background gossip thread that periodically syncs with peers."""
        from cvc.sdk.sync import GossipProtocol
        if hasattr(self, '_gossip') and self._gossip.running:
            return
        self._gossip = GossipProtocol(
            self._db,
            peers=[p._db for p in peers],
        )
        self._gossip.start(interval_seconds=interval_seconds)

    def stop_gossip(self) -> None:
        """Stop the background gossip thread."""
        if hasattr(self, '_gossip'):
            self._gossip.stop()

    def close(self) -> None:
        """Close all database connections and stop background threads."""
        if hasattr(self, '_gossip'):
            self._gossip.stop()
        self._db.index.close()

async def _run_locked(func, *args, **kwargs):
    def wrapper():
        with _hive_lock:
            return func(*args, **kwargs)
    return await asyncio.to_thread(wrapper)
