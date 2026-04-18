"""Integration tests for /memory REPL command.

Drives ``_handle_memory_command()`` with captured Rich Console output,
following the ``test_mission_repl.py`` pattern.
"""

from __future__ import annotations

import io
import re
from pathlib import Path
from typing import Any

import pytest

from anteroom.cli import renderer
from anteroom.cli.repl import _handle_memory_command

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    from anteroom.db import init_db

    return init_db(tmp_path / "test.db")


def _capture(user_input: str, *, cmd: str = "/memory", db: Any, config: Any = None) -> str:
    buf = io.StringIO()
    from rich.console import Console

    console = Console(file=buf, width=120, force_terminal=True, color_system="truecolor")
    original = renderer.console
    renderer.console = console
    try:
        _handle_memory_command(user_input, cmd=cmd, db=db, config=config)
    finally:
        renderer.console = original
    return _ANSI_RE.sub("", buf.getvalue())


def _promotion_config() -> Any:
    """Build a minimal AppConfig with a default MemoryPromotionConfig."""
    from unittest.mock import MagicMock

    from anteroom.config import MemoryConfig, MemoryPromotionConfig

    cfg = MagicMock()
    cfg.memory = MemoryConfig(promotion=MemoryPromotionConfig())
    cfg.identity = None
    return cfg


class TestMemoryList:
    def test_empty(self, db: Any) -> None:
        output = _capture("/memory list", db=db)
        assert "No memories found" in output

    def test_memories_alias_lists(self, db: Any) -> None:
        output = _capture("/memories", cmd="/memories", db=db)
        assert "No memories found" in output

    def test_with_entries(self, db: Any) -> None:
        from anteroom.services.memory_service import create_memory

        create_memory(db, "dark mode", scope="user", category="preference", name="dark")
        output = _capture("/memory list", db=db)
        assert "@user/memory/dark" in output
        assert "preference" in output

    def test_filter_by_scope(self, db: Any) -> None:
        from anteroom.services.memory_service import create_memory

        create_memory(db, "a", scope="user", category="preference", name="u1")
        create_memory(db, "b", scope="local", category="preference", name="l1")
        output = _capture("/memory list --scope user", db=db)
        assert "@user/memory/u1" in output
        assert "@local/memory/l1" not in output


class TestMemoryShow:
    def test_missing_usage(self, db: Any) -> None:
        output = _capture("/memory show", db=db)
        assert "Usage" in output

    def test_existing(self, db: Any) -> None:
        from anteroom.services.memory_service import create_memory

        create_memory(db, "content text", scope="user", category="preference", name="s1")
        output = _capture("/memory show @user/memory/s1", db=db)
        assert "content text" in output
        assert "@user/memory/s1" in output

    def test_not_found(self, db: Any) -> None:
        output = _capture("/memory show @user/memory/nope", db=db)
        assert "Not found" in output


class TestMemoryCreate:
    def test_create_user(self, db: Any) -> None:
        output = _capture(
            "/memory create --content hello --scope user --category preference --name c1",
            db=db,
        )
        assert "Created" in output
        assert "@user/memory/c1" in output

    def test_create_quoted_multi_word_content(self, db: Any) -> None:
        # REPL tokenisation must honour quoted args so multi-word content
        # passes through intact — plain str.split() would break this.
        from anteroom.services.memory_service import get_memory

        output = _capture(
            '/memory create --content "hello there world" --scope user --category preference --name c-quote',
            db=db,
        )
        assert "Created" in output
        mem = get_memory(db, "@user/memory/c-quote")
        assert mem is not None
        assert mem["content"] == "hello there world"

    def test_create_duplicate_is_clean_error(self, db: Any) -> None:
        from anteroom.services.memory_service import create_memory

        create_memory(db, "first", scope="user", category="preference", name="dup-repl")
        output = _capture(
            "/memory create --content second --scope user --category preference --name dup-repl",
            db=db,
        )
        # Expect the friendly error, not a crash.
        assert "already exists" in output.lower()


class TestMemoryEdit:
    def test_edit_content(self, db: Any) -> None:
        from anteroom.services.memory_service import create_memory, get_memory

        create_memory(db, "v1", scope="user", category="preference", name="e1")
        output = _capture("/memory edit @user/memory/e1 --content v2", db=db)
        assert "Updated" in output
        assert get_memory(db, "@user/memory/e1")["content"] == "v2"

    def test_edit_status(self, db: Any) -> None:
        from anteroom.services.memory_service import create_memory, get_memory

        create_memory(db, "x", scope="user", category="preference", name="e2")
        output = _capture("/memory edit @user/memory/e2 --status archived", db=db)
        assert "Updated" in output
        assert get_memory(db, "@user/memory/e2")["metadata"]["memory_status"] == "archived"


class TestMemoryDelete:
    def test_delete(self, db: Any) -> None:
        from anteroom.services.memory_service import create_memory, get_memory

        create_memory(db, "gone", scope="user", category="preference", name="d1")
        output = _capture("/memory delete @user/memory/d1", db=db)
        assert "Deleted" in output
        assert get_memory(db, "@user/memory/d1") is None

    def test_delete_missing_usage(self, db: Any) -> None:
        output = _capture("/memory delete", db=db)
        assert "Usage" in output


class TestUnknownAction:
    def test_unknown_subcommand(self, db: Any) -> None:
        # After #920, any of propose / candidates / approve / reject are
        # valid subcommands — verify an actually-unknown subcommand still
        # surfaces usage.
        output = _capture("/memory archive @user/memory/x", db=db, config=_promotion_config())
        assert "Usage" in output

    def test_promotion_without_config_bails_cleanly(self, db: Any) -> None:
        # If the REPL dispatches without a config (older callers, test
        # scenarios), the promotion subcommands should print a clean
        # "unavailable" message instead of raising.
        output = _capture("/memory approve @user/memory/x", db=db, config=None)
        assert "unavailable" in output.lower()


# ---------------------------------------------------------------------------
# Promotion / review subcommands (#920)
# ---------------------------------------------------------------------------


class TestMemoryPropose:
    def test_propose_happy_path(self, db: Any) -> None:
        output = _capture(
            "/memory propose --content dark_mode_preferred --scope user --category preference --name p1",
            db=db,
            config=_promotion_config(),
        )
        assert "Proposed:" in output
        assert "candidate" in output

    def test_propose_quoted_content(self, db: Any) -> None:
        from anteroom.services.memory_service import get_memory

        _capture(
            '/memory propose --content "multi word content" --scope user --category preference --name p2',
            db=db,
            config=_promotion_config(),
        )
        mem = get_memory(db, "@user/memory/p2")
        assert mem is not None
        assert mem["content"] == "multi word content"

    def test_propose_usage_on_missing_required(self, db: Any) -> None:
        output = _capture("/memory propose", db=db, config=_promotion_config())
        assert "Usage" in output

    def test_propose_with_conversation_id(self, db: Any) -> None:
        from anteroom.services.memory_service import get_memory

        _capture(
            "/memory propose --content x --scope user --category preference --name p3 "
            "--conversation-id aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            db=db,
            config=_promotion_config(),
        )
        mem = get_memory(db, "@user/memory/p3")
        assert mem is not None
        assert mem["metadata"]["provenance"]["conversation_id"] == "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"


class TestMemoryCandidates:
    def test_candidates_empty(self, db: Any) -> None:
        output = _capture("/memory candidates", db=db, config=_promotion_config())
        assert "No candidates" in output

    def test_candidates_after_propose(self, db: Any) -> None:
        cfg = _promotion_config()
        _capture(
            "/memory propose --content x --scope user --category preference --name cand1",
            db=db,
            config=cfg,
        )
        output = _capture("/memory candidates", db=db, config=cfg)
        assert "cand1" in output


class TestMemoryApproveReject:
    def test_approve_transitions(self, db: Any) -> None:
        cfg = _promotion_config()
        _capture(
            "/memory propose --content x --scope user --category preference --name ar1",
            db=db,
            config=cfg,
        )
        output = _capture("/memory approve @user/memory/ar1", db=db, config=cfg)
        assert "Approved:" in output
        assert "active" in output

    def test_approve_usage_when_fqn_missing(self, db: Any) -> None:
        output = _capture("/memory approve", db=db, config=_promotion_config())
        assert "Usage" in output

    def test_reject_transitions(self, db: Any) -> None:
        cfg = _promotion_config()
        _capture(
            "/memory propose --content x --scope user --category preference --name ar2",
            db=db,
            config=cfg,
        )
        output = _capture('/memory reject @user/memory/ar2 --reason "stale info"', db=db, config=cfg)
        assert "Rejected:" in output
        assert "stale info" in output

    def test_reject_usage_when_reason_missing(self, db: Any) -> None:
        output = _capture("/memory reject @user/memory/x", db=db, config=_promotion_config())
        assert "Usage" in output
