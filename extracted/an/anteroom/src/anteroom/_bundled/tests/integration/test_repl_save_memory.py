"""CLI integration tests for the save_memory tool (#217).

Exercises the end-to-end path from a simulated LLM tool call through the
ToolRegistry into the memory_promotion pipeline, then out through the
memory CLI's approve/reject surface.

Mirrors the test harness style of ``tests/unit/test_tools.py`` and
``tests/integration/test_repl_memory.py``: no real AI service, no
prompt_toolkit — we drive ``ToolRegistry.call_tool`` directly with the
same ``_extra_context`` dict the REPL assembles, and use the promotion
service for the approve step.
"""

from __future__ import annotations

import asyncio
import sqlite3
from typing import Any
from unittest.mock import MagicMock

import pytest

from anteroom.config import MemoryConfig, MemoryPromotionConfig, SafetyConfig
from anteroom.db import _SCHEMA, ThreadSafeConnection
from anteroom.services import memory_promotion
from anteroom.services.memory_service import get_memory, list_memories
from anteroom.tools import ToolRegistry, register_default_tools

CONV = "11111111-1111-4111-8111-111111111111"
UID = "22222222-2222-4222-8222-222222222222"


@pytest.fixture()
def db() -> ThreadSafeConnection:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(_SCHEMA)
    conn.commit()
    return ThreadSafeConnection(conn)


@pytest.fixture()
def app_config() -> Any:
    cfg = MagicMock()
    cfg.memory = MemoryConfig(promotion=MemoryPromotionConfig())
    return cfg


@pytest.fixture()
def registry(db: ThreadSafeConnection) -> ToolRegistry:
    reg = ToolRegistry()
    register_default_tools(reg)
    return reg


def _call_save_memory(
    registry: ToolRegistry,
    db: ThreadSafeConnection,
    app_config: Any,
    *,
    content: str = "use 4-space indent",
    category: str = "preference",
    scope: str = "user",
    confirm_callback: Any = None,
) -> dict[str, Any]:
    return asyncio.run(
        registry.call_tool(
            "save_memory",
            {"content": content, "category": category, "scope": scope},
            confirm_callback=confirm_callback,
            _extra_context={
                "db": db,
                "conversation_id": CONV,
                "config": app_config,
                "user_id": UID,
            },
        )
    )


# ---------------------------------------------------------------------------
# Tool-call → candidate → approve round trip
# ---------------------------------------------------------------------------


class TestCandidateRoundTrip:
    def test_tool_call_persists_candidate(
        self, registry: ToolRegistry, db: ThreadSafeConnection, app_config: Any
    ) -> None:
        result = _call_save_memory(registry, db, app_config)
        assert "error" not in result, result
        assert result["memory_status"] == "candidate"
        fqn = result["fqn"]

        stored = get_memory(db, fqn)
        assert stored is not None
        assert stored["content"] == "use 4-space indent"
        meta = stored.get("metadata") or {}
        assert meta.get("memory_status") == "candidate"
        assert meta.get("memory_category") == "preference"

    def test_candidate_visible_to_promotion_list(
        self, registry: ToolRegistry, db: ThreadSafeConnection, app_config: Any
    ) -> None:
        _call_save_memory(registry, db, app_config, content="first")
        _call_save_memory(registry, db, app_config, content="second")
        candidates = memory_promotion.list_candidates(db)
        assert len(candidates) == 2
        contents = {c["content"] for c in candidates}
        assert contents == {"first", "second"}

    def test_approve_round_trip_promotes_to_active(
        self, registry: ToolRegistry, db: ThreadSafeConnection, app_config: Any
    ) -> None:
        created = _call_save_memory(registry, db, app_config, content="promote me")
        fqn = created["fqn"]

        promoted = memory_promotion.approve_candidate(
            db,
            fqn,
            reviewer_id=UID,
            reviewer_display="Test User",
            config=app_config.memory.promotion,
        )
        assert promoted["metadata"]["memory_status"] == "active"

        lineage = promoted["metadata"]["lineage"]
        # Lineage carries the original agent proposal + the reviewer approval.
        events = [entry["event"] for entry in lineage]
        assert events == ["proposed", "approved"]
        assert lineage[0]["actor"] == "agent"
        assert lineage[1]["to_status"] == "active"


# ---------------------------------------------------------------------------
# Approval gate parity — ask_for_writes prompts; auto mode doesn't
# ---------------------------------------------------------------------------


class TestApprovalGate:
    def test_ask_for_writes_invokes_confirm_callback(
        self, registry: ToolRegistry, db: ThreadSafeConnection, app_config: Any
    ) -> None:
        registry.set_safety_config(SafetyConfig(enabled=True, approval_mode="ask_for_writes"))
        invoked: list[Any] = []

        async def _confirm(verdict: Any) -> bool:
            invoked.append(verdict)
            return True

        result = _call_save_memory(registry, db, app_config, confirm_callback=_confirm)
        assert "error" not in result, result
        assert len(invoked) == 1
        assert invoked[0].tool_name == "save_memory"

    def test_auto_mode_skips_confirm_callback(
        self, registry: ToolRegistry, db: ThreadSafeConnection, app_config: Any
    ) -> None:
        registry.set_safety_config(SafetyConfig(enabled=True, approval_mode="auto"))
        invoked: list[Any] = []

        async def _confirm(verdict: Any) -> bool:
            invoked.append(verdict)
            return True

        result = _call_save_memory(registry, db, app_config, confirm_callback=_confirm)
        assert "error" not in result, result
        assert invoked == []

    def test_denied_by_user_blocks_and_persists_nothing(
        self, registry: ToolRegistry, db: ThreadSafeConnection, app_config: Any
    ) -> None:
        registry.set_safety_config(SafetyConfig(enabled=True, approval_mode="ask_for_writes"))

        async def _deny(_verdict: Any) -> bool:
            return False

        result = _call_save_memory(registry, db, app_config, confirm_callback=_deny)
        assert result.get("error") == "Operation denied by user"
        assert list_memories(db) == []
