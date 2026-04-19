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


@pytest.fixture(autouse=True)
def _stub_server_routing(monkeypatch: pytest.MonkeyPatch) -> None:
    """Force the memory CLI into its local-fallback path (#1444).

    After #1441 the memory decision CLI routes to a local server first
    and only falls back to the in-process audit writer when the
    connection is refused at loopback.  In this test suite there is no
    server bound — and httpx's py3.14 ``__cause__`` chain doesn't always
    terminate in ``ConnectionRefusedError`` where the routing classifier
    looks, so the CLI trips ``ServerHttpError`` and short-circuits.

    Patching ``call_decision_endpoint`` in the memory_cli module to
    raise ``ServerNotRunningError`` unconditionally is the minimal
    intervention: tests see the pre-#1441 CLI behaviour without mocking
    the full httpx stack and without touching production code.
    """
    from anteroom.cli import _decision_routing
    from anteroom.cli._decision_routing import ServerNotRunningError

    def _raise_not_running(*_args: Any, **_kwargs: Any) -> None:
        raise ServerNotRunningError("stubbed — no server bound in test env")

    # memory_cli does ``from ._decision_routing import call_decision_endpoint``
    # lazily inside each handler, so patching the source module is the right
    # site — every subsequent ``from _decision_routing import ...`` picks up
    # the stub.
    monkeypatch.setattr(_decision_routing, "call_decision_endpoint", _raise_not_running)


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


def _test_identity() -> Any:
    """Minimal :class:`UserIdentity` for tests that need routing/audit paths.

    ``_decision_routing._derive_bearer_token`` requires a non-empty
    ``private_key`` (used as HMAC key material) to construct the bearer
    token that identifies the caller.  The value only needs to be a
    non-empty string — it's never parsed as real PEM here.  See #1444.
    """
    from anteroom.config import UserIdentity

    return UserIdentity(
        user_id="00000000-0000-4000-8000-000000000000",
        display_name="Test User",
        public_key="-----BEGIN PUBLIC KEY-----\ntest-public-key\n-----END PUBLIC KEY-----\n",
        private_key="-----BEGIN PRIVATE KEY-----\ntest-private-key\n-----END PRIVATE KEY-----\n",
    )


def _populate_routing_fields(cfg: Any) -> None:
    """Populate the ``config.app`` fields that ``call_decision_endpoint`` reads.

    After #1441 the memory / workflow decision CLI paths route to the
    local server first (expecting ``ServerNotRunningError`` to fall back
    to a local audit writer in a test environment where no server is
    bound).  The routing helper reads ``config.app.host / port / tls``
    to form a URL — leaving those as ``MagicMock`` proxies crashes URL
    formation before the connection-refused fallback can fire.  Set them
    to loopback so the connection attempt fails cleanly.
    """
    cfg.app.host = "127.0.0.1"
    cfg.app.port = 8080
    cfg.app.tls = None
    # Disable server routing entirely for tests that drive the CLI
    # directly — there's no server for the loopback call to refuse, so
    # set audit.enabled=False which short-circuits get_cli_audit_writer
    # and the CLI path treats the local write as a no-op.
    cfg.audit = None


def _promotion_config() -> Any:
    """Build a minimal AppConfig with a default MemoryPromotionConfig."""
    from unittest.mock import MagicMock

    from anteroom.config import MemoryConfig, MemoryPromotionConfig

    cfg = MagicMock()
    cfg.memory = MemoryConfig(promotion=MemoryPromotionConfig())
    cfg.identity = _test_identity()
    _populate_routing_fields(cfg)
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


# ---------------------------------------------------------------------------
# Pin / unpin / retention slash commands (#625)
# ---------------------------------------------------------------------------


def _retention_config(**overrides: Any) -> Any:
    """Build a config with both promotion and retention settings."""
    from unittest.mock import MagicMock

    from anteroom.config import (
        MemoryConfig,
        MemoryPromotionConfig,
        MemoryRetentionConfig,
    )

    cfg = MagicMock()
    cfg.memory = MemoryConfig(
        promotion=MemoryPromotionConfig(),
        retention=MemoryRetentionConfig(**overrides),
    )
    cfg.identity = _test_identity()
    _populate_routing_fields(cfg)
    return cfg


class TestMemoryPin:
    def test_pin_happy_path(self, db: Any) -> None:
        from anteroom.services.memory_service import create_memory, get_memory

        create_memory(db, "x", scope="user", category="preference", name="slp1")
        output = _capture(
            "/memory pin @user/memory/slp1",
            db=db,
            config=_retention_config(),
        )
        assert "Pinned:" in output
        assert get_memory(db, "@user/memory/slp1")["metadata"]["pinned"] is True

    def test_pin_usage_when_fqn_missing(self, db: Any) -> None:
        output = _capture("/memory pin", db=db, config=_retention_config())
        assert "Usage" in output

    def test_unpin_round_trip(self, db: Any) -> None:
        from anteroom.services.memory_service import create_memory, get_memory

        create_memory(db, "x", scope="user", category="preference", name="slp2")
        _capture("/memory pin @user/memory/slp2", db=db, config=_retention_config())
        output = _capture(
            "/memory unpin @user/memory/slp2",
            db=db,
            config=_retention_config(),
        )
        assert "Unpinned:" in output
        assert get_memory(db, "@user/memory/slp2")["metadata"]["pinned"] is False

    def test_retention_without_config_bails_cleanly(self, db: Any) -> None:
        output = _capture("/memory pin @user/memory/x", db=db, config=None)
        assert "unavailable" in output.lower()


class TestMemoryRetention:
    def test_preview_disabled_shows_disabled_message(self, db: Any) -> None:
        output = _capture(
            "/memory retention preview",
            db=db,
            config=_retention_config(enabled=False),
        )
        assert "disabled" in output.lower()

    def test_preview_enabled_lists_candidates(self, db: Any) -> None:
        from anteroom.services.memory_service import (
            create_memory,
            update_memory_metadata,
        )

        art = create_memory(db, "x", scope="user", category="preference", name="srp1")
        update_memory_metadata(db, art["fqn"], memory_status="rejected")
        output = _capture(
            "/memory retention preview",
            db=db,
            config=_retention_config(enabled=True, purge_statuses=["rejected"]),
        )
        assert "srp1" in output

    def test_purge_without_confirm_is_refused(self, db: Any) -> None:
        output = _capture(
            "/memory retention purge",
            db=db,
            config=_retention_config(enabled=True, purge_statuses=["rejected"]),
        )
        assert "Refusing" in output

    def test_purge_with_confirm_deletes(self, db: Any) -> None:
        from anteroom.services.memory_service import (
            create_memory,
            get_memory,
            update_memory_metadata,
        )

        art = create_memory(db, "x", scope="user", category="preference", name="srp2")
        update_memory_metadata(db, art["fqn"], memory_status="rejected")
        output = _capture(
            "/memory retention purge --confirm",
            db=db,
            config=_retention_config(enabled=True, purge_statuses=["rejected"]),
        )
        assert "Purged" in output
        assert get_memory(db, art["fqn"]) is None

    def test_retention_unknown_subcommand_usage(self, db: Any) -> None:
        output = _capture(
            "/memory retention nonsense",
            db=db,
            config=_retention_config(enabled=True),
        )
        assert "Usage" in output
