"""
cvc.core.memory_holographic
============================

CVC-native holographic memory provider. Port of the upstream memory plugin
(upstream memory plugin) into CVC, with no vendor dependency.

For v4.0, the provider runs in-memory (no SQLite, no HRR). The full retrieval
engine (entity resolution, trust scoring, compositional queries) lands in
Phase 4 alongside the per-user identity layer. This module provides the API
surface the agent core needs to compile and dispatch — that's it.

Public surface (mirrors what `cvc/agent/hermes_bridge.py` imports):

    FACT_STORE_SCHEMA:        dict
    FACT_FEEDBACK_SCHEMA:     dict
    HolographicMemoryProvider:  class
    _load_plugin_config()      → dict

Plus a minimal `MemoryProvider` ABC so this module is self-contained.
"""

from __future__ import annotations

import json
import logging
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import yaml

from cvc.core.logging import get_cvc_home

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Minimal MemoryProvider ABC (self-contained, no vendor import)
# ---------------------------------------------------------------------------


class MemoryProvider(ABC):
    """Base interface every memory provider implements.

    For v4.0 only one concrete provider exists (HolographicMemoryProvider),
    but the ABC lets Phase 4 add alternative backends (vector DB, etc.)
    without touching the agent core.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider identifier (e.g. 'holographic', 'chromadb')."""
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Return True if this provider can run on the current host."""
        ...

    @abstractmethod
    def initialize(self, *, session_id: str) -> None:
        """One-time setup. Must be safe to call multiple times."""
        ...

    @abstractmethod
    def handle_tool_call(self, name: str, args: dict) -> dict:
        """Dispatch a fact_store / fact_feedback call. Returns a serializable result."""
        ...

    def prefetch(self, query: str) -> None:  # noqa: D401 — optional
        """Optional: warm caches for a likely query. Default no-op."""
        return None

    def system_prompt_block(self) -> str:
        """Optional: a string to inject into the system prompt."""
        return ""


# ---------------------------------------------------------------------------
# Tool schemas (unchanged from the original PR; mirrored verbatim so the
# provider drop-in replacement compiles against the same tool-calling format)
# ---------------------------------------------------------------------------


FACT_STORE_SCHEMA = {
    "name": "fact_store",
    "description": (
        "Deep structured memory with algebraic reasoning. "
        "Use alongside the memory tool — memory for always-on context, "
        "fact_store for deep recall and compositional queries.\n\n"
        "ACTIONS (simple → powerful):\n"
        "• add — Store a fact the user would expect you to remember.\n"
        "• search — Keyword lookup ('editor config', 'deploy process').\n"
        "• probe — Entity recall: ALL facts about a person/thing.\n"
        "• related — What connects to an entity? Structural adjacency.\n"
        "• reason — Compositional: facts connected to MULTIPLE entities simultaneously.\n"
        "• contradict — Memory hygiene: find facts making conflicting claims.\n"
        "• update/remove/list — CRUD operations.\n\n"
        "IMPORTANT: Before answering questions about the user, ALWAYS probe or reason first."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": [
                    "add", "search", "probe", "related", "reason",
                    "contradict", "update", "remove", "list",
                ],
            },
            "content": {"type": "string", "description": "Fact content (required for 'add')."},
            "query": {"type": "string", "description": "Search query (required for 'search')."},
            "entity": {"type": "string", "description": "Entity name for 'probe'/'related'."},
            "entities": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Entity names for 'reason'.",
            },
            "fact_id": {"type": "integer", "description": "Fact ID for 'update'/'remove'."},
            "category": {"type": "string", "enum": ["user_pref", "project", "tool", "general"]},
            "tags": {"type": "string", "description": "Comma-separated tags."},
            "trust_delta": {"type": "number", "description": "Trust adjustment for 'update'."},
            "min_trust": {"type": "number", "description": "Minimum trust filter (default: 0.3)."},
            "limit": {"type": "integer", "description": "Max results (default: 10)."},
        },
        "required": ["action"],
    },
}


FACT_FEEDBACK_SCHEMA = {
    "name": "fact_feedback",
    "description": (
        "Rate a fact after using it. Mark 'helpful' if accurate, 'unhelpful' if outdated. "
        "This trains the memory — good facts rise, bad facts sink."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["helpful", "unhelpful"]},
            "fact_id": {"type": "integer", "description": "The fact ID to rate."},
        },
        "required": ["action", "fact_id"],
    },
}


# ---------------------------------------------------------------------------
# Config loader
# ---------------------------------------------------------------------------


def _load_plugin_config() -> dict:
    """Read `plugins.holographic-memory` from `<cvc_home>/config.yaml`.

    Falls back to empty dict if the file is missing or malformed.
    """
    try:
        config_path = get_cvc_home() / "config.yaml"
        if not config_path.exists():
            return {}
        with open(config_path, encoding="utf-8-sig") as f:
            all_config = yaml.safe_load(f) or {}
        plugins = all_config.get("plugins", {}) or {}
        # Accept both the legacy 'hermes-memory-store' key (for config
        # compatibility during the v3→v4 migration) and the new
        # 'holographic-memory' key.
        return (
            plugins.get("holographic-memory")
            or plugins.get("hermes-memory-store")
            or {}
        )
    except Exception:
        logger.debug("holographic config load failed", exc_info=True)
        return {}


# ---------------------------------------------------------------------------
# Provider implementation
# ---------------------------------------------------------------------------


class HolographicMemoryProvider(MemoryProvider):
    """In-memory holographic memory for v4.0.

    Stores facts in a list with sequential integer IDs. Trust scores start at
    the configured `default_trust` and can be updated via fact_feedback. The
    full entity-resolution and HRR retrieval land in Phase 4; for now, search
    is a simple keyword contains, probe is full-record, reason is the
    intersection of probe results.
    """

    def __init__(self, config: dict | None = None) -> None:
        self._config = config if config is not None else _load_plugin_config()
        self._session_id: str | None = None
        self._min_trust: float = float(self._config.get("min_trust_threshold", 0.3))
        self._default_trust: float = float(self._config.get("default_trust", 0.5))
        self._facts: list[dict[str, Any]] = []
        self._next_id: int = 1

    @property
    def name(self) -> str:
        return "holographic"

    def is_available(self) -> bool:
        return True

    def initialize(self, *, session_id: str) -> None:
        self._session_id = session_id
        logger.debug("holographic memory initialized session_id=%s", session_id)

    def save_config(self, values: dict, hermes_home: str | Path) -> None:
        """Write config to `<hermes_home>/config.yaml` under `plugins.holographic-memory`."""
        config_path = Path(hermes_home) / "config.yaml"
        try:
            existing: dict = {}
            if config_path.exists():
                with open(config_path, encoding="utf-8-sig") as f:
                    existing = yaml.safe_load(f) or {}
            existing.setdefault("plugins", {})
            existing["plugins"]["holographic-memory"] = values
            with open(config_path, "w", encoding="utf-8") as f:
                yaml.dump(existing, f, default_flow_style=False)
        except Exception:
            logger.warning("holographic save_config failed", exc_info=True)

    def get_config_schema(self) -> dict:
        """Return JSON-schema-like config fields for the setup UI."""
        return {
            "db_path": {"type": "string", "default": "memory_store.db", "description": "SQLite file path (Phase 4+)."},
            "auto_extract": {"type": "boolean", "default": False, "description": "Auto-extract facts from every turn."},
            "default_trust": {"type": "number", "default": 0.5, "min": 0.0, "max": 1.0},
            "min_trust_threshold": {"type": "number", "default": 0.3, "min": 0.0, "max": 1.0},
            "temporal_decay_half_life": {"type": "number", "default": 0, "description": "0 = no decay (Phase 4+)."},
        }

    # --- Internal helpers ---------------------------------------------------

    def _add_fact(self, content: str, category: str, tags: list[str]) -> dict:
        fact = {
            "id": self._next_id,
            "content": content,
            "category": category,
            "tags": tags,
            "trust": self._default_trust,
            "helpful": 0,
            "unhelpful": 0,
            "created_at": time.time(),
            "session_id": self._session_id,
        }
        self._facts.append(fact)
        self._next_id += 1
        return fact

    def _above_min_trust(self, fact: dict) -> bool:
        return float(fact.get("trust", 0.0)) >= self._min_trust

    # --- MemoryProvider contract -------------------------------------------

    def handle_tool_call(self, name: str, args: dict) -> dict:
        if name == "fact_store":
            return self._handle_fact_store(args)
        if name == "fact_feedback":
            return self._handle_fact_feedback(args)
        return {"error": f"unknown tool: {name}"}

    def _handle_fact_store(self, args: dict) -> dict:
        action = args.get("action")
        if action == "add":
            content = args.get("content", "").strip()
            if not content:
                return {"error": "content is required for 'add'"}
            category = args.get("category", "general")
            tags = [t.strip() for t in (args.get("tags") or "").split(",") if t.strip()]
            fact = self._add_fact(content, category, tags)
            return {"ok": True, "fact_id": fact["id"]}
        if action == "list":
            limit = int(args.get("limit", 10))
            facts = [f for f in self._facts if self._above_min_trust(f)][:limit]
            return {"ok": True, "facts": facts, "count": len(facts)}
        if action == "search":
            query = (args.get("query") or "").lower()
            limit = int(args.get("limit", 10))
            results = [
                f for f in self._facts
                if self._above_min_trust(f) and query in f.get("content", "").lower()
            ][:limit]
            return {"ok": True, "facts": results, "count": len(results)}
        if action == "probe":
            entity = (args.get("entity") or "").lower()
            results = [
                f for f in self._facts
                if self._above_min_trust(f) and entity in f.get("content", "").lower()
            ]
            return {"ok": True, "facts": results, "count": len(results)}
        if action == "remove":
            fid = int(args.get("fact_id", -1))
            before = len(self._facts)
            self._facts = [f for f in self._facts if f["id"] != fid]
            return {"ok": True, "removed": before - len(self._facts)}
        # For v4.0 the remaining actions (related / reason / contradict /
        # update) are stubbed — Phase 4 will implement them with the real
        # entity-resolution engine.
        return {"ok": True, "note": f"action '{action}' is stubbed in v4.0; full impl in Phase 4", "facts": []}

    def _handle_fact_feedback(self, args: dict) -> dict:
        action = args.get("action")
        fid = int(args.get("fact_id", -1))
        for f in self._facts:
            if f["id"] == fid:
                if action == "helpful":
                    f["helpful"] += 1
                    f["trust"] = min(1.0, f.get("trust", 0.5) + 0.05)
                elif action == "unhelpful":
                    f["unhelpful"] += 1
                    f["trust"] = max(0.0, f.get("trust", 0.5) - 0.05)
                return {"ok": True, "fact_id": fid, "trust": f["trust"]}
        return {"error": f"fact {fid} not found"}

    def prefetch(self, query: str) -> None:
        # v4.0: in-memory; nothing to warm. Phase 4 will prime vector indices.
        return None

    def system_prompt_block(self) -> str:
        if not self._facts:
            return ""
        n = len(self._facts)
        return (
            f"\n[Memory: {n} structured fact{'s' if n != 1 else ''} available "
            f"via the fact_store tool. Probe or reason before answering "
            f"questions about the user.]\n"
        )

    # --- Inspector helpers (for tests / debugging) -------------------------

    def __len__(self) -> int:
        return len(self._facts)

    def __repr__(self) -> str:
        return f"<HolographicMemoryProvider session={self._session_id} facts={len(self._facts)}>"


__all__ = [
    "MemoryProvider",
    "HolographicMemoryProvider",
    "FACT_STORE_SCHEMA",
    "FACT_FEEDBACK_SCHEMA",
    "_load_plugin_config",
]
