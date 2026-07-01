"""
cvc.sdk.agent — Per-agent interface for the hive mind.

Each ``Agent`` instance is bound to a specific agent identity and provides
methods for committing, recalling, and querying scoped context.
"""

from __future__ import annotations

import logging
import threading
import time
from typing import Any, Callable
import asyncio
from cvc.sdk.telemetry import emit_telemetry

from cvc.core.database import ContextDatabase
from cvc.core.models import (
    CognitiveCommit,
    CommitMetadata,
    CommitType,
    ContentBlob,
    ContextMessage,
    CVCCommitRequest,
)
from cvc.sdk.events import AGENT_TARGETED, COMMIT_CREATED, EventBus, EventCallback
from cvc.sdk.registry import AgentRegistry
from cvc.sdk.router import Router

logger = logging.getLogger("cvc.sdk.agent")

# Type alias for auto-responder callbacks
AutoResponder = Callable[[dict[str, Any], "Agent"], str | None]


class Agent:
    """
    A hive mind agent bound to a specific identity.

    Provides scoped access to the Merkle DAG — commits go through the
    router for branch targeting, and recalls are limited to branches the
    agent can read.

    Usage::

        agent = hive.register_agent("SPC-AEG-02", role="specialist", squad="aegis")
        agent.commit("Completed radiation analysis", content={"findings": "..."})
        recent = agent.context(limit=5)
        results = agent.recall("radiation levels")
    """

    def __init__(
        self,
        agent_id: str,
        db: ContextDatabase,
        registry: AgentRegistry,
        router: Router,
        event_bus: EventBus,
        *,
        engine: Any = None,
        write_lock: threading.Lock | None = None,
    ) -> None:
        self.agent_id = agent_id
        self._db = db
        self._registry = registry
        self._router = router
        self._event_bus = event_bus
        self._engine = engine  # CVCEngine, if available
        self._write_lock = write_lock or threading.Lock()
        # Per-agent context window (Phase 7) — 0 means no limit
        self._context_window: int = 0
        # Auto-trigger (Phase 5)
        self._auto_respond: bool = False
        self._on_targeted_callbacks: list[EventCallback] = []
        self._responder: AutoResponder | None = None
        self._listening = False

    @property
    def profile(self) -> dict[str, Any] | None:
        """Current agent profile from the registry."""
        return self._registry.get(self.agent_id)

    @property
    def squad(self) -> str | None:
        p = self.profile
        return p.get("squad") if p else None

    @property
    def rank(self) -> str | None:
        p = self.profile
        return p.get("rank") if p else None

    @property
    def context_window(self) -> int:
        """The maximum number of commits in this agent's active context.

        A value of ``0`` means no limit (the default).
        """
        return self._context_window

    @context_window.setter
    def context_window(self, size: int) -> None:
        self._context_window = max(0, size)

    # -- Commit ------------------------------------------------------------

    def commit(
        self,
        message: str,
        *,
        content: dict[str, Any] | None = None,
        commit_type: CommitType = CommitType.CHECKPOINT,
        tags: list[str] | None = None,
        target_agent_id: str | None = None,
        action_type: str | None = None,
        branch: str | None = None,
        messages: list[dict[str, str]] | None = None,
    ) -> str:
        """
        Commit a cognitive turn to the hive mind.

        Returns the commit hash.
        """
        # Build content blob (can be done outside the lock — pure data)
        context_messages = []
        if messages:
            context_messages = [
                ContextMessage(role=m.get("role", "assistant"), content=m.get("content", ""))
                for m in messages
            ]
        blob = ContentBlob(
            messages=context_messages,
            tool_outputs=content or {},
        )

        # Thread-safe: the entire branch-resolve → store → head-advance
        # sequence is locked to prevent races on SQLite reads/writes.
        with self._write_lock:
            target_branch = branch or self._router.target_branch(self.agent_id)

            # Enforce write permission
            if not self._router.validate_write(self.agent_id, target_branch):
                raise PermissionError(
                    f"Agent {self.agent_id} cannot write to branch {target_branch}"
                )

            # Ensure branch exists
            bp = self._db.index.get_branch(target_branch)
            if bp is None:
                squad = self.squad
                if squad:
                    self._router.ensure_squad_branch(squad)
                    bp = self._db.index.get_branch(target_branch)
                if bp is None:
                    raise ValueError(f"Branch {target_branch} does not exist")

            # Build metadata with hive mind fields
            profile = self.profile or {}
            meta = CommitMetadata(
                agent_id=self.agent_id,
                tags=tags or [],
                squad=profile.get("squad"),
                target_agent_id=target_agent_id,
                rank=profile.get("rank"),
                action_type=action_type,
            )

            commit = CognitiveCommit(
                parent_hashes=[bp.head_hash],
                commit_type=commit_type,
                message=message,
                content_blob=blob,
                metadata=meta,
            )

            commit_hash = self._db.store_commit(commit)
            self._db.index.advance_head(target_branch, commit_hash)

        logger.info(
            "Agent %s committed %s on %s: %s",
            self.agent_id, commit_hash[:12], target_branch, message[:60],
        )

        # Fire events
        event_data = {
            "commit_hash": commit_hash,
            "agent_id": self.agent_id,
            "branch": target_branch,
            "message": message,
            "squad": profile.get("squad"),
            "target_agent_id": target_agent_id,
            "action_type": action_type,
        }
        self._event_bus.emit(COMMIT_CREATED, event_data)
        if target_agent_id:
            self._event_bus.emit(AGENT_TARGETED, event_data)

        return commit_hash

    # -- Recall (semantic search) ------------------------------------------

    def recall(self, query: str, *, limit: int = 5) -> list[CognitiveCommit]:
        """
        Semantic search within the agent's accessible scope.

        Uses ChromaDB's metadata-filtered vector search to restrict results
        to branches/squads this agent can read.  Falls back to text search.
        """
        if self._db.vectors.available:
            # Build a Chroma where-filter scoped to readable branches
            readable = self._router.readable_branches(self.agent_id)
            where_filter = self._build_vector_filter(readable)

            if where_filter:
                results = self._db.vectors.search_filtered(
                    query, n=limit, where=where_filter,
                )
            else:
                results = self._db.vectors.search(query, n=limit)

            if results:
                commits = []
                for r in results:
                    c = self._db.index.get_commit(r["commit_hash"])
                    if c is not None:
                        commits.append(c)
                return commits

        # Fallback: text search within squad commits or all commits
        squad = self.squad
        if squad:
            return self._db.index.list_commits_by_squad(squad, limit=limit)
        return self._db.index.search_commits(query, limit=limit)

    @staticmethod
    def _build_vector_filter(readable_branches: list[str]) -> dict | None:
        """Build a Chroma ``where`` clause for branch-scoped vector search."""
        if not readable_branches:
            return None
        if len(readable_branches) == 1:
            return {"branch": readable_branches[0]}
        return {"branch": {"$in": readable_branches}}

    # -- Context -----------------------------------------------------------

    def context(self, *, limit: int = 10) -> list[CognitiveCommit]:
        """Get recent commits visible to this agent.

        If a ``context_window`` has been configured on this agent, *limit*
        is capped to that value so the agent stays within its window.
        """
        effective_limit = min(limit, self._context_window) if self._context_window else limit
        return self._router.context_for(self.agent_id, limit=effective_limit)

    def inbox(self, *, limit: int = 20) -> list[CognitiveCommit]:
        """Get commits addressed specifically to this agent."""
        return self._db.index.list_commits_by_target(self.agent_id, limit=limit)

    def squad_context(self, *, limit: int = 20) -> list[CognitiveCommit]:
        """Get recent commits from the agent's squad."""
        squad = self.squad
        if not squad:
            return []
        return self._db.index.list_commits_by_squad(squad, limit=limit)

    def history(self, *, limit: int = 50) -> list[CognitiveCommit]:
        """Get this agent's own commit history."""
        return self._db.index.list_commits_by_agent(self.agent_id, limit=limit)

    # -- Auto-trigger (Phase 5) -------------------------------------------

    @property
    def auto_respond(self) -> bool:
        """Whether this agent auto-responds when targeted by another agent."""
        return self._auto_respond

    @auto_respond.setter
    def auto_respond(self, value: bool) -> None:
        self._auto_respond = value
        if value and not self._listening:
            self._start_listening()

    def on_targeted(self, callback: EventCallback) -> None:
        """Register a callback invoked when a commit targets this agent.

        The callback receives the event dict with keys like
        ``commit_hash``, ``agent_id`` (sender), ``message``, etc.
        """
        self._on_targeted_callbacks.append(callback)
        if not self._listening:
            self._start_listening()

    def set_responder(self, responder: AutoResponder) -> None:
        """Set the auto-responder function.

        When ``auto_respond`` is True and a commit targets this agent,
        the responder is called with ``(event_data, self)`` and should
        return a message string to auto-commit, or ``None`` to skip.

        Example::

            def my_responder(event, agent):
                return f"Acknowledged: {event['message']}"

            agent.auto_respond = True
            agent.set_responder(my_responder)
        """
        self._responder = responder
        if not self._listening:
            self._start_listening()

    def _start_listening(self) -> None:
        """Wire this agent into the event bus for AGENT_TARGETED events."""
        if self._listening:
            return
        self._listening = True
        self._event_bus.on(AGENT_TARGETED, self._handle_targeted)

    def stop_listening(self) -> None:
        """Unregister from the event bus."""
        if not self._listening:
            return
        self._listening = False
        self._event_bus.off(AGENT_TARGETED, self._handle_targeted)

    def _handle_targeted(self, event: dict[str, Any]) -> None:
        """Internal handler for AGENT_TARGETED events."""
        target = event.get("target_agent_id")
        if target != self.agent_id:
            return
        # Don't react to our own commits
        if event.get("agent_id") == self.agent_id:
            return

        logger.info("Agent %s targeted by %s: %s", self.agent_id, event.get("agent_id"), event.get("message", "")[:60])

        # Fire on_targeted callbacks
        for cb in self._on_targeted_callbacks:
            try:
                cb(event)
            except Exception:
                logger.exception("Error in on_targeted callback for %s", self.agent_id)

        # Auto-respond if enabled
        if self._auto_respond and self._responder:
            try:
                response_msg = self._responder(event, self)
                if response_msg:
                    self.commit(
                        response_msg,
                        target_agent_id=event.get("agent_id"),
                        action_type="AUTO_RESPONSE",
                    )
            except Exception:
                logger.exception("Auto-responder error for agent %s", self.agent_id)

    # -- Hive Memory integration -------------------------------------------

    async def share_to_hive(
        self,
        content: str,
        *,
        category: str = "general",
        tags: list[str] | None = None,
    ) -> str:
        """
        Share a finding/decision/task to the Hive Memory.

        This is the primary way agents contribute to the shared cognitive
        space.  The entry is stored as a commit on the ``hive/memory``
        branch and is readable by all agents.

        Returns the commit hash.
        """
        from cvc.sdk.hivemind import HiveMemory
        hive_mem = HiveMemory(self._get_hive())
        asyncio.create_task(emit_telemetry({"agent_id": self.agent_id, "action": "write"}))
        return await hive_mem.write(
            self.agent_id, content, category=category, tags=tags,
        )

    async def read_hive(
        self,
        query: str = "",
        *,
        category: str | None = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Read from the shared Hive Memory.

        Returns entries matching the query/category filter.
        """
        from cvc.sdk.hivemind import HiveMemory
        hive_mem = HiveMemory(self._get_hive())
        asyncio.create_task(emit_telemetry({"agent_id": self.agent_id, "action": "read"}))
        return await hive_mem.read(query, category=category, limit=limit)

    async def hive_context(self, *, limit: int = 5) -> str:
        """
        Get a summary of recent Hive Memory for system prompt injection.
        """
        from cvc.sdk.hivemind import HiveMemory
        hive_mem = HiveMemory(self._get_hive())
        asyncio.create_task(emit_telemetry({"agent_id": self.agent_id, "action": "read"}))
        return await hive_mem.summary_context(limit=limit)

    def _get_hive(self) -> Any:
        """Get the parent HiveMind instance (lazy discovery)."""
        # The HiveMind is reconstructed from the same DB + config
        if self._engine is not None:
            from cvc.sdk.hivemind import HiveMind
            hive = HiveMind.__new__(HiveMind)
            hive._db = self._db
            hive._engine = self._engine
            hive._registry = self._registry
            hive._router = self._router
            hive._event_bus = self._event_bus
            hive._write_lock = self._write_lock
            hive._agents = {}
            return hive
        raise RuntimeError("Agent not connected to a HiveMind instance")
