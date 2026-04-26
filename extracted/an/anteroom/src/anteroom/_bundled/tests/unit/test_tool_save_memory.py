"""Unit tests for the save_memory tool (#217).

Covers:
- handler happy-path per category
- scope restrictions (user / local OK; project rejected in Phase 1)
- input validation (content length, category enum)
- typed error translation (agent-disabled, rate-limit, duplicate FQN, missing context)
- registration + _extra_context translation contract (tools/__init__.py::call_tool branch)
"""

from __future__ import annotations

import asyncio
import sqlite3
from typing import Any
from unittest.mock import MagicMock

import pytest

from anteroom.config import MemoryConfig, MemoryPromotionConfig
from anteroom.db import _SCHEMA, ThreadSafeConnection
from anteroom.services import memory_promotion
from anteroom.services.memory_service import list_memories
from anteroom.tools import ToolRegistry, register_default_tools
from anteroom.tools import save_memory as save_memory_tool

CONV_A = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
USER_ID = "00000000-0000-4000-8000-000000000000"


@pytest.fixture()
def db() -> ThreadSafeConnection:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(_SCHEMA)
    conn.commit()
    return ThreadSafeConnection(conn)


def _cfg_with_promotion(**overrides: Any) -> Any:
    """Build a minimal AppConfig-shaped object exposing .memory.promotion."""
    cfg = MagicMock()
    cfg.memory = MemoryConfig(promotion=MemoryPromotionConfig(**overrides))
    return cfg


# ---------------------------------------------------------------------------
# DEFINITION contract
# ---------------------------------------------------------------------------


class TestDefinition:
    def test_name_is_save_memory(self) -> None:
        assert save_memory_tool.DEFINITION["name"] == "save_memory"

    def test_required_parameters(self) -> None:
        params = save_memory_tool.DEFINITION["parameters"]
        assert params["type"] == "object"
        assert set(params["required"]) == {"content", "category"}

    def test_category_enum(self) -> None:
        props = save_memory_tool.DEFINITION["parameters"]["properties"]
        assert set(props["category"]["enum"]) == {
            "preference",
            "project_fact",
            "decision",
            "workflow_hint",
        }

    def test_scope_enum_phase1(self) -> None:
        props = save_memory_tool.DEFINITION["parameters"]["properties"]
        # Phase 1: only user + local surfaced to the LLM. project deferred.
        assert set(props["scope"]["enum"]) == {"user", "local"}

    def test_content_bounded(self) -> None:
        props = save_memory_tool.DEFINITION["parameters"]["properties"]
        assert props["content"]["minLength"] == 1
        assert props["content"]["maxLength"] == 500


# ---------------------------------------------------------------------------
# Happy-path per category
# ---------------------------------------------------------------------------


class TestHappyPath:
    @pytest.mark.parametrize(
        "category",
        ["preference", "project_fact", "decision", "workflow_hint"],
    )
    def test_creates_candidate_for_every_category(self, db: ThreadSafeConnection, category: str) -> None:
        cfg = _cfg_with_promotion()
        result = asyncio.run(
            save_memory_tool.handle(
                content=f"remember {category}",
                category=category,
                scope="user",
                _db=db,
                _conversation_id=CONV_A,
                _config=cfg,
                _user_id=USER_ID,
            )
        )
        assert "error" not in result
        assert result["memory_status"] == "candidate"
        assert result["category"] == category
        assert result["fqn"].startswith("@user/memory/")

    def test_scope_local_creates_under_local_namespace(self, db: ThreadSafeConnection) -> None:
        cfg = _cfg_with_promotion()
        result = asyncio.run(
            save_memory_tool.handle(
                content="a local fact",
                category="preference",
                scope="local",
                _db=db,
                _conversation_id=CONV_A,
                _config=cfg,
                _user_id=USER_ID,
            )
        )
        assert "error" not in result
        assert result["fqn"].startswith("@local/memory/")

    def test_default_scope_is_user(self, db: ThreadSafeConnection) -> None:
        cfg = _cfg_with_promotion()
        result = asyncio.run(
            save_memory_tool.handle(
                content="no scope given",
                category="preference",
                _db=db,
                _conversation_id=CONV_A,
                _config=cfg,
                _user_id=USER_ID,
            )
        )
        assert "error" not in result
        assert result["fqn"].startswith("@user/memory/")

    def test_provenance_records_conversation_id(self, db: ThreadSafeConnection) -> None:
        cfg = _cfg_with_promotion()
        asyncio.run(
            save_memory_tool.handle(
                content="provenance test",
                category="preference",
                scope="user",
                _db=db,
                _conversation_id=CONV_A,
                _config=cfg,
                _user_id=USER_ID,
            )
        )
        existing = list_memories(db)
        assert len(existing) == 1
        prov = (existing[0].get("metadata") or {}).get("provenance") or {}
        assert prov.get("conversation_id") == CONV_A

    def test_lineage_attributes_agent_as_proposer(self, db: ThreadSafeConnection) -> None:
        cfg = _cfg_with_promotion()
        asyncio.run(
            save_memory_tool.handle(
                content="proposer test",
                category="preference",
                scope="user",
                _db=db,
                _conversation_id=CONV_A,
                _config=cfg,
                _user_id=USER_ID,
            )
        )
        existing = list_memories(db)
        lineage = (existing[0].get("metadata") or {}).get("lineage") or []
        assert lineage
        assert lineage[0]["event"] == "proposed"
        assert lineage[0]["actor"] == "agent"
        assert lineage[0].get("actor_id") == USER_ID

    def test_return_shape_has_documented_keys(self, db: ThreadSafeConnection) -> None:
        cfg = _cfg_with_promotion()
        result = asyncio.run(
            save_memory_tool.handle(
                content="shape",
                category="preference",
                scope="user",
                _db=db,
                _conversation_id=CONV_A,
                _config=cfg,
                _user_id=USER_ID,
            )
        )
        # Keys the LLM needs to know the outcome
        assert "fqn" in result
        assert "memory_status" in result
        assert "category" in result
        assert "scope" in result

    def test_local_auto_approve_returns_active(self, db: ThreadSafeConnection) -> None:
        cfg = _cfg_with_promotion(local_auto_approve=True)
        result = asyncio.run(
            save_memory_tool.handle(
                content="auto approved",
                category="preference",
                scope="user",
                _db=db,
                _conversation_id=CONV_A,
                _config=cfg,
                _user_id=USER_ID,
            )
        )
        assert "error" not in result
        assert result["memory_status"] == "active"
        existing = list_memories(db)
        assert len(existing) == 1
        metadata = existing[0].get("metadata") or {}
        assert metadata["reviewed_by"] == "system:auto_approve"
        assert metadata["reviewed_at"]
        lineage = metadata.get("lineage") or []
        assert lineage[0]["event"] == "auto_approved"
        assert lineage[0]["actor"] == "system"


# ---------------------------------------------------------------------------
# Input validation — typed errors
# ---------------------------------------------------------------------------


class TestInputValidation:
    def test_scope_project_rejected_with_typed_error(self, db: ThreadSafeConnection) -> None:
        cfg = _cfg_with_promotion()
        result = asyncio.run(
            save_memory_tool.handle(
                content="no project scope yet",
                category="preference",
                scope="project",
                _db=db,
                _conversation_id=CONV_A,
                _config=cfg,
                _user_id=USER_ID,
            )
        )
        assert "error" in result
        assert "project" in result["error"].lower()
        # Nothing persisted.
        assert list_memories(db) == []

    def test_content_empty_rejected(self, db: ThreadSafeConnection) -> None:
        cfg = _cfg_with_promotion()
        result = asyncio.run(
            save_memory_tool.handle(
                content="",
                category="preference",
                scope="user",
                _db=db,
                _conversation_id=CONV_A,
                _config=cfg,
                _user_id=USER_ID,
            )
        )
        assert "error" in result
        assert list_memories(db) == []

    def test_content_over_500_chars_rejected(self, db: ThreadSafeConnection) -> None:
        cfg = _cfg_with_promotion()
        result = asyncio.run(
            save_memory_tool.handle(
                content="x" * 501,
                category="preference",
                scope="user",
                _db=db,
                _conversation_id=CONV_A,
                _config=cfg,
                _user_id=USER_ID,
            )
        )
        assert "error" in result
        assert list_memories(db) == []

    def test_invalid_category_rejected(self, db: ThreadSafeConnection) -> None:
        cfg = _cfg_with_promotion()
        result = asyncio.run(
            save_memory_tool.handle(
                content="hello",
                category="bogus_category",
                scope="user",
                _db=db,
                _conversation_id=CONV_A,
                _config=cfg,
                _user_id=USER_ID,
            )
        )
        assert "error" in result
        assert list_memories(db) == []

    def test_content_whitespace_only_rejected(self, db: ThreadSafeConnection) -> None:
        """Whitespace-only content is treated as empty — can't bypass the length check."""
        cfg = _cfg_with_promotion()
        result = asyncio.run(
            save_memory_tool.handle(
                content="   \t  \n  ",
                category="preference",
                scope="user",
                _db=db,
                _conversation_id=CONV_A,
                _config=cfg,
                _user_id=USER_ID,
            )
        )
        assert "error" in result
        assert list_memories(db) == []

    def test_whitespace_padded_content_is_stored_stripped(self, db: ThreadSafeConnection) -> None:
        """Content passed through strip() before persistence — no whitespace bypass.

        Regression: a caller could pad content with whitespace so the raw string
        exceeded 500 chars but ``content.strip()`` stayed within the bound. The
        handler must not store the padded version; otherwise the advertised
        500-char cap is bypassable and memories render with ragged whitespace.
        """
        cfg = _cfg_with_promotion()
        # Raw length 513, stripped length 500 — passes validation before the fix
        # and ended up persisting a 513-char memory.
        padded = "    " + ("x" * 500) + "         "
        assert len(padded) > 500
        assert len(padded.strip()) == 500
        result = asyncio.run(
            save_memory_tool.handle(
                content=padded,
                category="preference",
                scope="user",
                _db=db,
                _conversation_id=CONV_A,
                _config=cfg,
                _user_id=USER_ID,
            )
        )
        assert "error" not in result
        stored = list_memories(db)
        assert len(stored) == 1
        assert stored[0]["content"] == "x" * 500
        assert len(stored[0]["content"]) <= 500

    def test_scope_unknown_value_rejected(self, db: ThreadSafeConnection) -> None:
        """Any scope outside {user, local, project} hits the fallback error."""
        cfg = _cfg_with_promotion()
        result = asyncio.run(
            save_memory_tool.handle(
                content="hello",
                category="preference",
                scope="global",
                _db=db,
                _conversation_id=CONV_A,
                _config=cfg,
                _user_id=USER_ID,
            )
        )
        assert "error" in result
        assert "scope" in result["error"].lower()
        assert list_memories(db) == []

    def test_conversation_id_none_persists_null_provenance(self, db: ThreadSafeConnection) -> None:
        """When no conversation is active, provenance.conversation_id is stored as None."""
        cfg = _cfg_with_promotion()
        result = asyncio.run(
            save_memory_tool.handle(
                content="no conversation",
                category="preference",
                scope="user",
                _db=db,
                _conversation_id=None,
                _config=cfg,
                _user_id=USER_ID,
            )
        )
        assert "error" not in result
        stored = list_memories(db)
        assert len(stored) == 1
        prov = (stored[0].get("metadata") or {}).get("provenance") or {}
        # The memory_service normalises provenance with all fields initialised;
        # the contract is that conversation_id is None, not that the key is absent.
        assert prov.get("conversation_id") is None


# ---------------------------------------------------------------------------
# Service-layer typed errors translated
# ---------------------------------------------------------------------------


class TestGovernanceErrors:
    def test_agent_disabled_returns_typed_error(self, db: ThreadSafeConnection) -> None:
        cfg = _cfg_with_promotion(agent_proposals_enabled=False)
        result = asyncio.run(
            save_memory_tool.handle(
                content="blocked",
                category="preference",
                scope="user",
                _db=db,
                _conversation_id=CONV_A,
                _config=cfg,
                _user_id=USER_ID,
            )
        )
        assert "error" in result
        assert "agent" in result["error"].lower()
        assert list_memories(db) == []

    def test_rate_limit_returns_retry_hint(self, db: ThreadSafeConnection) -> None:
        cfg = _cfg_with_promotion(max_candidates_per_conversation=1)
        # First call succeeds.
        first = asyncio.run(
            save_memory_tool.handle(
                content="first",
                category="preference",
                scope="user",
                _db=db,
                _conversation_id=CONV_A,
                _config=cfg,
                _user_id=USER_ID,
            )
        )
        assert "error" not in first
        # Second call in the same conversation trips the cap.
        second = asyncio.run(
            save_memory_tool.handle(
                content="second",
                category="preference",
                scope="user",
                _db=db,
                _conversation_id=CONV_A,
                _config=cfg,
                _user_id=USER_ID,
            )
        )
        assert "error" in second
        assert "retry_hint" in second

    def test_duplicate_fqn_returns_typed_error(self, db: ThreadSafeConnection, monkeypatch: pytest.MonkeyPatch) -> None:
        cfg = _cfg_with_promotion()

        def _explode(*_a: Any, **_kw: Any) -> Any:
            raise sqlite3.IntegrityError("UNIQUE constraint failed: artifacts.fqn")

        monkeypatch.setattr(memory_promotion, "propose_candidate", _explode)

        result = asyncio.run(
            save_memory_tool.handle(
                content="dup",
                category="preference",
                scope="user",
                _db=db,
                _conversation_id=CONV_A,
                _config=cfg,
                _user_id=USER_ID,
            )
        )
        assert "error" in result
        assert "already exists" in result["error"].lower() or "duplicate" in result["error"].lower()


class TestContextGuards:
    def test_missing_db_returns_typed_error(self) -> None:
        cfg = _cfg_with_promotion()
        result = asyncio.run(
            save_memory_tool.handle(
                content="hello",
                category="preference",
                scope="user",
                _db=None,
                _conversation_id=CONV_A,
                _config=cfg,
                _user_id=USER_ID,
            )
        )
        assert "error" in result
        assert "unavailable" in result["error"].lower()

    def test_missing_config_returns_typed_error(self, db: ThreadSafeConnection) -> None:
        result = asyncio.run(
            save_memory_tool.handle(
                content="hello",
                category="preference",
                scope="user",
                _db=db,
                _conversation_id=CONV_A,
                _config=None,
                _user_id=USER_ID,
            )
        )
        assert "error" in result
        assert "unavailable" in result["error"].lower()

    def test_config_without_memory_promotion_returns_typed_error(self, db: ThreadSafeConnection) -> None:
        """A non-None config that lacks ``.memory.promotion`` must not crash."""

        class _MinimalConfig:
            pass  # no .memory attribute at all

        result = asyncio.run(
            save_memory_tool.handle(
                content="hello",
                category="preference",
                scope="user",
                _db=db,
                _conversation_id=CONV_A,
                _config=_MinimalConfig(),
                _user_id=USER_ID,
            )
        )
        assert "error" in result
        assert "unavailable" in result["error"].lower()

    def test_generic_promotion_error_translated(
        self, db: ThreadSafeConnection, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Base PromotionError falls through to the generic translation branch."""
        from anteroom.services.memory_promotion import PromotionError

        def _raise(*_a: Any, **_kw: Any) -> Any:
            raise PromotionError("storage unavailable")

        monkeypatch.setattr(memory_promotion, "propose_candidate", _raise)

        cfg = _cfg_with_promotion()
        result = asyncio.run(
            save_memory_tool.handle(
                content="x",
                category="preference",
                scope="user",
                _db=db,
                _conversation_id=CONV_A,
                _config=cfg,
                _user_id=USER_ID,
            )
        )
        assert "error" in result
        assert "failed to save memory" in result["error"].lower()


# ---------------------------------------------------------------------------
# Registration + _extra_context dict-key translation contract
# ---------------------------------------------------------------------------


class TestRegistration:
    def test_registered_by_register_default_tools(self) -> None:
        registry = ToolRegistry()
        register_default_tools(registry)
        assert registry.has_tool("save_memory")

    def test_openai_definition_exposed(self) -> None:
        registry = ToolRegistry()
        register_default_tools(registry)
        names = [t["function"]["name"] for t in registry.get_openai_tools()]
        assert "save_memory" in names

    def test_call_tool_translates_unprefixed_extra_context_keys(self) -> None:
        """Pins the dict-key translation contract.

        _extra_context passes **unprefixed** keys (``db``, ``conversation_id``,
        ``config``, ``user_id``). ``ToolRegistry.call_tool`` translates them
        into the underscore-prefixed kwargs the handler declares. Mirrors the
        existing ``bash`` / ``run_agent`` translation branches.
        """
        registry = ToolRegistry()
        captured: dict[str, Any] = {}

        async def fake_handle(**kwargs: Any) -> dict[str, Any]:
            captured.update(kwargs)
            return {"ok": True}

        registry.register("save_memory", fake_handle, save_memory_tool.DEFINITION)

        mock_db = MagicMock(name="db")
        mock_config = MagicMock(name="config")
        asyncio.run(
            registry.call_tool(
                "save_memory",
                {"content": "x", "category": "preference", "scope": "user"},
                _extra_context={
                    "db": mock_db,
                    "conversation_id": CONV_A,
                    "config": mock_config,
                    "user_id": USER_ID,
                },
            )
        )
        assert captured.get("_db") is mock_db
        assert captured.get("_conversation_id") == CONV_A
        assert captured.get("_config") is mock_config
        assert captured.get("_user_id") == USER_ID


class TestTier:
    def test_save_memory_is_write_tier(self) -> None:
        from anteroom.tools.tiers import DEFAULT_TOOL_TIERS, ToolTier

        assert DEFAULT_TOOL_TIERS.get("save_memory") == ToolTier.WRITE
