"""
cvc.sdk.registry — Agent Registry for the Hive Mind.

Manages multi-agent identities: registration, lookup, filtering,
and branch-permission enforcement.  Backed by both SQLite (IndexDB)
for fast queries AND JSON files under ``.cvc/agents/`` for CRDT-like
portability — each agent profile is a standalone JSON file that can
be synced / merged across nodes via set-union.
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any

from cvc.core.database import IndexDB

logger = logging.getLogger("cvc.sdk.registry")


class AgentRegistry:
    """
    Central registry of hive mind agents.

    Dual-backed:
      * **SQLite** (``agents`` table in ``.cvc/cvc.db``) — fast indexed queries.
      * **JSON files** (``.cvc/agents/{agent_id}.json``) — portable, CRDT-friendly
        (append-only; merge = union of files).

    On ``register()``, both stores are written.  On ``load_from_disk()``,
    JSON files are merged into SQLite (new agents added, existing agents
    updated only if the JSON file is newer).
    """

    def __init__(self, index: IndexDB, agents_dir: Path | None = None) -> None:
        self._index = index
        self._agents_dir = agents_dir
        if self._agents_dir is not None:
            self._agents_dir.mkdir(parents=True, exist_ok=True)

    # -- Registration ------------------------------------------------------

    def register(
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
    ) -> dict[str, Any]:
        """Register a new agent (or update if it already exists)."""
        self._index.insert_agent(
            agent_id=agent_id,
            name=name,
            role=role,
            rank=rank,
            squad=squad,
            capabilities=capabilities,
            metadata=metadata,
            readable_branches=readable_branches,
            writable_branches=writable_branches,
        )
        logger.info("Registered agent %s (squad=%s, rank=%s)", agent_id, squad, rank)

        # Persist to JSON file
        profile = self.get(agent_id)
        if profile is not None:
            self._write_json(profile)

        return profile  # type: ignore[return-value]

    # -- Lookup ------------------------------------------------------------

    def get(self, agent_id: str) -> dict[str, Any] | None:
        """Retrieve an agent profile by ID."""
        return self._index.get_agent(agent_id)

    def list(
        self,
        *,
        squad: str | None = None,
        rank: str | None = None,
        status: str | None = None,
    ) -> list[dict[str, Any]]:
        """List agents, optionally filtered."""
        return self._index.list_agents(squad=squad, rank=rank, status=status)

    # -- Updates -----------------------------------------------------------

    def update(self, agent_id: str, **fields: Any) -> bool:
        """Update fields on an existing agent."""
        ok = self._index.update_agent(agent_id, **fields)
        if ok:
            profile = self.get(agent_id)
            if profile is not None:
                self._write_json(profile)
        return ok

    def deactivate(self, agent_id: str) -> bool:
        """Mark an agent as inactive (soft delete)."""
        ok = self._index.update_agent(agent_id, status="inactive")
        if ok:
            profile = self.get(agent_id)
            if profile is not None:
                self._write_json(profile)
        return ok

    def remove(self, agent_id: str) -> bool:
        """Hard-delete an agent from the registry (SQLite + JSON)."""
        deleted = self._index.delete_agent(agent_id)
        if deleted and self._agents_dir is not None:
            json_path = self._agents_dir / f"{agent_id}.json"
            json_path.unlink(missing_ok=True)
        return deleted

    # -- Permission checks -------------------------------------------------

    def can_read(self, agent_id: str, branch: str) -> bool:
        """Check if agent has read access to the given branch."""
        profile = self.get(agent_id)
        if profile is None:
            return False
        readable = profile.get("readable_branches", [])
        # Empty list = unrestricted read
        if not readable:
            return True
        return branch in readable or "**" in readable

    def can_write(self, agent_id: str, branch: str) -> bool:
        """Check if agent has write access to the given branch."""
        profile = self.get(agent_id)
        if profile is None:
            return False
        writable = profile.get("writable_branches", [])
        # Empty list = unrestricted write
        if not writable:
            return True
        return branch in writable or "**" in writable

    # -- JSON file persistence (CRDT-friendly) -----------------------------

    def _write_json(self, profile: dict[str, Any]) -> None:
        """Write an agent profile to ``.cvc/agents/{agent_id}.json``."""
        if self._agents_dir is None:
            return
        path = self._agents_dir / f"{profile['agent_id']}.json"
        path.write_text(
            json.dumps(profile, indent=2, default=str),
            encoding="utf-8",
        )

    def load_from_disk(self) -> int:
        """
        Scan ``.cvc/agents/*.json`` and merge into the SQLite index.

        CRDT semantics: each JSON file is a fact about an agent.
        Merge = set-union:
          * New agents (no row in SQLite) are inserted.
          * Existing agents are updated only if the JSON's ``updated_at``
            is newer than the SQLite row's ``updated_at``.

        Returns the number of agents merged.
        """
        if self._agents_dir is None or not self._agents_dir.exists():
            return 0
        merged = 0
        for fp in sorted(self._agents_dir.glob("*.json")):
            try:
                data = json.loads(fp.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                logger.warning("Skipping invalid agent file: %s", fp)
                continue
            agent_id = data.get("agent_id")
            if not agent_id:
                continue
            existing = self._index.get_agent(agent_id)
            if existing is None or data.get("updated_at", 0) > existing.get("updated_at", 0):
                self._index.insert_agent(
                    agent_id=agent_id,
                    name=data.get("name"),
                    role=data.get("role"),
                    rank=data.get("rank"),
                    squad=data.get("squad"),
                    capabilities=data.get("capabilities"),
                    metadata=data.get("metadata"),
                    readable_branches=data.get("readable_branches"),
                    writable_branches=data.get("writable_branches"),
                    status=data.get("status", "active"),
                )
                merged += 1
        if merged:
            logger.info("Merged %d agent(s) from disk into SQLite", merged)
        return merged

    def export_all_to_disk(self) -> int:
        """Write all agents from SQLite to individual JSON files. Returns count."""
        if self._agents_dir is None:
            return 0
        agents = self._index.list_agents()
        for a in agents:
            self._write_json(a)
        return len(agents)
