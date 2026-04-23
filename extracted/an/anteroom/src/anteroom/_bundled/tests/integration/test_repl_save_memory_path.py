"""REPL-path integration tests for the save_memory tool (#217).

These tests address the senior-review gap from PR #1452: the original
``test_repl_save_memory.py`` exercised ``ToolRegistry.call_tool`` directly
without going through the CLI REPL's ``_extra_context`` assembly (the
exact two lines changed in ``cli/repl.py``).

The tests below drive the **shared** ``build_tool_extra_context`` helper
that the REPL now calls at its tool-dispatch site, then thread the real
dict through ``ToolRegistry.call_tool``. The helper is the single source
of truth for the unprefixed→underscore-prefixed key contract on the CLI
side; exercising it end-to-end proves that:

1. ``config`` / ``user_id`` are present in the REPL's tool-call context
   (the bug the senior review flagged).
2. ``call_tool`` translates them into the ``_config`` / ``_user_id``
   kwargs the ``save_memory`` handler declares.
3. The handler stamps ``proposer_id`` onto the memory lineage from the
   REPL's resolved ``config.identity.user_id``.
"""

from __future__ import annotations

import asyncio
import sqlite3

import pytest

from anteroom.config import MemoryConfig, MemoryPromotionConfig, SafetyConfig, UserIdentity
from anteroom.db import _SCHEMA, ThreadSafeConnection
from anteroom.services.memory_service import list_memories
from anteroom.tools import ToolRegistry, register_default_tools
from anteroom.tools.tool_context import build_tool_extra_context

CONV = "55555555-5555-4555-8555-555555555555"


@pytest.fixture()
def db() -> ThreadSafeConnection:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(_SCHEMA)
    conn.commit()
    return ThreadSafeConnection(conn)


class _TestConfig:
    """Minimal AppConfig-shaped object the REPL would produce at start-up."""

    def __init__(self, *, identity: UserIdentity | None) -> None:
        self.memory = MemoryConfig(promotion=MemoryPromotionConfig())
        self.identity = identity
        self.safety = SafetyConfig(approval_mode="auto")


def _identity(user_id: str) -> UserIdentity:
    return UserIdentity(
        user_id=user_id,
        display_name="Test User",
        public_key="-----BEGIN PUBLIC KEY-----\ntest-pub\n-----END PUBLIC KEY-----\n",
        private_key="-----BEGIN PRIVATE KEY-----\ntest-priv\n-----END PRIVATE KEY-----\n",
    )


# ---------------------------------------------------------------------------
# Shape of the helper the REPL now calls at its tool-dispatch site
# ---------------------------------------------------------------------------


class TestBuildToolExtraContext:
    """Pin the exact dict the REPL hands to ``ToolRegistry.call_tool``."""

    def test_contains_all_seven_keys(self, db: ThreadSafeConnection) -> None:
        cfg = _TestConfig(identity=_identity("u-1"))
        ctx = build_tool_extra_context(
            bg_manager=None,
            detach_manager=None,
            conversation_id=CONV,
            db=db,
            config=cfg,
        )
        assert set(ctx.keys()) == {
            "bg_manager",
            "detach_manager",
            "conversation_id",
            "db",
            "config",
            "user_id",
            "tool_call_id",
        }

    def test_config_passed_through(self, db: ThreadSafeConnection) -> None:
        cfg = _TestConfig(identity=_identity("u-2"))
        ctx = build_tool_extra_context(bg_manager=None, detach_manager=None, conversation_id=CONV, db=db, config=cfg)
        assert ctx["config"] is cfg

    def test_user_id_resolved_from_identity(self, db: ThreadSafeConnection) -> None:
        cfg = _TestConfig(identity=_identity("u-abc"))
        ctx = build_tool_extra_context(bg_manager=None, detach_manager=None, conversation_id=CONV, db=db, config=cfg)
        assert ctx["user_id"] == "u-abc"

    def test_user_id_none_when_identity_missing(self, db: ThreadSafeConnection) -> None:
        """CLI may run without an identity (first-run / --no-identity)."""
        cfg = _TestConfig(identity=None)
        ctx = build_tool_extra_context(bg_manager=None, detach_manager=None, conversation_id=CONV, db=db, config=cfg)
        assert ctx["user_id"] is None

    def test_tool_call_id_passed_through(self, db: ThreadSafeConnection) -> None:
        cfg = _TestConfig(identity=_identity("u-call"))
        ctx = build_tool_extra_context(
            bg_manager=None,
            detach_manager=None,
            conversation_id=CONV,
            db=db,
            config=cfg,
            tool_call_id="call-xyz",
        )
        assert ctx["tool_call_id"] == "call-xyz"


# ---------------------------------------------------------------------------
# End-to-end: REPL dict → call_tool → save_memory handler → DB
# ---------------------------------------------------------------------------


class TestReplPathRoundTrip:
    def test_tool_registry_translates_repl_dict_to_handler_kwargs(self, db: ThreadSafeConnection) -> None:
        """The REPL builds the dict; call_tool translates it; save_memory receives it."""
        cfg = _TestConfig(identity=_identity("repl-user-1"))
        repl_dict = build_tool_extra_context(
            bg_manager=None,
            detach_manager=None,
            conversation_id=CONV,
            db=db,
            config=cfg,
        )

        registry = ToolRegistry()
        register_default_tools(registry)

        result = asyncio.run(
            registry.call_tool(
                "save_memory",
                {"content": "remembered from repl path", "category": "preference", "scope": "user"},
                _extra_context=repl_dict,
            )
        )
        assert "error" not in result, result
        assert result["memory_status"] == "candidate"
        assert result["fqn"].startswith("@user/memory/")

    def test_repl_user_id_lands_on_lineage_actor_id(self, db: ThreadSafeConnection) -> None:
        """The REPL's resolved user_id flows through as the promotion ``proposer_id``
        — this is the payoff of threading ``config`` / ``user_id`` through the
        REPL's ``_extra_context`` dict.
        """
        cfg = _TestConfig(identity=_identity("repl-user-xyz"))
        repl_dict = build_tool_extra_context(
            bg_manager=None,
            detach_manager=None,
            conversation_id=CONV,
            db=db,
            config=cfg,
        )

        registry = ToolRegistry()
        register_default_tools(registry)

        asyncio.run(
            registry.call_tool(
                "save_memory",
                {"content": "lineage-attributed", "category": "decision", "scope": "user"},
                _extra_context=repl_dict,
            )
        )

        stored = list_memories(db)
        assert len(stored) == 1
        lineage = (stored[0].get("metadata") or {}).get("lineage") or []
        assert lineage
        assert lineage[0]["event"] == "proposed"
        assert lineage[0]["actor"] == "agent"
        assert lineage[0].get("actor_id") == "repl-user-xyz"

    def test_repl_without_identity_still_persists_candidate_with_null_actor(self, db: ThreadSafeConnection) -> None:
        """CLI first-run / --no-identity: no user_id, but the tool still works."""
        cfg = _TestConfig(identity=None)
        repl_dict = build_tool_extra_context(
            bg_manager=None,
            detach_manager=None,
            conversation_id=CONV,
            db=db,
            config=cfg,
        )

        registry = ToolRegistry()
        register_default_tools(registry)

        result = asyncio.run(
            registry.call_tool(
                "save_memory",
                {"content": "no identity", "category": "preference", "scope": "user"},
                _extra_context=repl_dict,
            )
        )
        assert "error" not in result, result
        stored = list_memories(db)
        lineage = (stored[0].get("metadata") or {}).get("lineage") or []
        assert lineage[0]["actor"] == "agent"
        assert lineage[0].get("actor_id") is None


# ---------------------------------------------------------------------------
# Regression guard — the REPL's call site uses the helper, not a literal dict
# ---------------------------------------------------------------------------


class TestReplCallSiteUsesHelper:
    """If someone reverts the helper back to an inline dict literal, fail loudly.

    This is a belt-and-suspenders test against drift: the refactor extracted
    the assembly specifically so the two interface sites (CLI + web) can't
    silently diverge. We read the REPL's source and assert the helper is
    invoked at the tool-dispatch site.
    """

    def test_repl_source_references_build_tool_extra_context(self) -> None:
        from pathlib import Path

        import anteroom.cli.repl as _repl

        src = Path(_repl.__file__).read_text()
        # The helper is invoked at the tool-dispatch site.
        assert "build_tool_extra_context(" in src, (
            "cli/repl.py must use build_tool_extra_context() to assemble the "
            "_extra_context dict — do not inline the assembly (see #1452 review)."
        )
