"""Unit tests for the memory CLI handlers."""

from __future__ import annotations

import argparse
import sqlite3
from io import StringIO
from typing import Any
from unittest.mock import patch

import pytest
from rich.console import Console

from anteroom.db import _SCHEMA, ThreadSafeConnection
from anteroom.services.memory_service import create_memory


@pytest.fixture()
def db() -> ThreadSafeConnection:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(_SCHEMA)
    conn.commit()
    return ThreadSafeConnection(conn)


def _make_args(**kwargs: Any) -> argparse.Namespace:
    return argparse.Namespace(**kwargs)


def _capture_console() -> tuple[Console, StringIO]:
    buf = StringIO()
    console = Console(file=buf, width=120, no_color=True)
    return console, buf


# ---------------------------------------------------------------------------
# _handle_list
# ---------------------------------------------------------------------------


class TestHandleList:
    def test_empty_list(self, db: ThreadSafeConnection) -> None:
        console, buf = _capture_console()
        with patch("anteroom.cli.memory_cli.console", console):
            from anteroom.cli.memory_cli import _handle_list

            _handle_list(db, _make_args(scope=None, category=None, status=None, namespace=None))
        assert "No memories found" in buf.getvalue()

    def test_list_renders_table(self, db: ThreadSafeConnection) -> None:
        create_memory(db, "dark mode", scope="user", category="preference", name="dark")
        create_memory(db, "uses pg", scope="project", category="project_fact", project_slug="app", name="pg")

        console, buf = _capture_console()
        with patch("anteroom.cli.memory_cli.console", console):
            from anteroom.cli.memory_cli import _handle_list

            _handle_list(db, _make_args(scope=None, category=None, status=None, namespace=None))
        out = buf.getvalue()
        assert "@user/memory/dark" in out
        assert "@app/memory/pg" in out
        assert "preference" in out
        assert "project_fact" in out

    def test_list_filters_by_scope(self, db: ThreadSafeConnection) -> None:
        create_memory(db, "a", scope="user", category="preference", name="u")
        create_memory(db, "b", scope="local", category="preference", name="l")

        console, buf = _capture_console()
        with patch("anteroom.cli.memory_cli.console", console):
            from anteroom.cli.memory_cli import _handle_list

            _handle_list(db, _make_args(scope="user", category=None, status=None, namespace=None))
        out = buf.getvalue()
        assert "@user/memory/u" in out
        assert "@local/memory/l" not in out


# ---------------------------------------------------------------------------
# _handle_show
# ---------------------------------------------------------------------------


class TestHandleShow:
    def test_show_existing(self, db: ThreadSafeConnection) -> None:
        create_memory(db, "hello there", scope="user", category="preference", name="s1")

        console, buf = _capture_console()
        with patch("anteroom.cli.memory_cli.console", console):
            from anteroom.cli.memory_cli import _handle_show

            _handle_show(db, _make_args(fqn="@user/memory/s1"))
        out = buf.getvalue()
        assert "hello there" in out
        assert "@user/memory/s1" in out
        assert "preference" in out

    def test_show_missing_exits_nonzero(self, db: ThreadSafeConnection) -> None:
        console, _ = _capture_console()
        with patch("anteroom.cli.memory_cli.console", console):
            from anteroom.cli.memory_cli import _handle_show

            with pytest.raises(SystemExit) as exc_info:
                _handle_show(db, _make_args(fqn="@user/memory/nope"))
        assert exc_info.value.code == 1


# ---------------------------------------------------------------------------
# _handle_create
# ---------------------------------------------------------------------------


class TestHandleCreate:
    def test_create_user_scope(self, db: ThreadSafeConnection) -> None:
        console, buf = _capture_console()
        args = _make_args(
            content="a preference",
            scope="user",
            category="preference",
            name="c1",
            project_slug=None,
            status="active",
        )
        with patch("anteroom.cli.memory_cli.console", console):
            from anteroom.cli.memory_cli import _handle_create

            _handle_create(db, args)
        assert "Created" in buf.getvalue()
        assert "@user/memory/c1" in buf.getvalue()

    def test_create_empty_content_exits(self, db: ThreadSafeConnection) -> None:
        console, _ = _capture_console()
        args = _make_args(
            content="",
            scope="user",
            category="preference",
            name=None,
            project_slug=None,
            status="active",
        )
        with patch("anteroom.cli.memory_cli.console", console):
            from anteroom.cli.memory_cli import _handle_create

            with pytest.raises(SystemExit) as exc_info:
                _handle_create(db, args)
        assert exc_info.value.code == 1

    def test_create_project_requires_slug(self, db: ThreadSafeConnection) -> None:
        console, buf = _capture_console()
        args = _make_args(
            content="x",
            scope="project",
            category="preference",
            name=None,
            project_slug=None,
            status="active",
        )
        with patch("anteroom.cli.memory_cli.console", console):
            from anteroom.cli.memory_cli import _handle_create

            with pytest.raises(SystemExit) as exc_info:
                _handle_create(db, args)
        assert exc_info.value.code == 1
        assert "project_slug" in buf.getvalue()

    def test_create_duplicate_fqn_exits_cleanly(self, db: ThreadSafeConnection) -> None:
        # The service raises sqlite3.IntegrityError on duplicate FQNs. The CLI
        # must catch it and exit(1) with a clear message instead of crashing.
        create_memory(db, "first", scope="user", category="preference", name="dup-cli")

        console, buf = _capture_console()
        args = _make_args(
            content="second",
            scope="user",
            category="preference",
            name="dup-cli",
            project_slug=None,
            status="active",
        )
        with patch("anteroom.cli.memory_cli.console", console):
            from anteroom.cli.memory_cli import _handle_create

            with pytest.raises(SystemExit) as exc_info:
                _handle_create(db, args)
        assert exc_info.value.code == 1
        assert "already exists" in buf.getvalue().lower()

    def test_create_reads_content_from_stdin(self, db: ThreadSafeConnection, monkeypatch: pytest.MonkeyPatch) -> None:
        # `--content -` must read from stdin so `aroom memory create --content -` works.
        import io

        monkeypatch.setattr("sys.stdin", io.StringIO("stdin payload\n"))

        console, buf = _capture_console()
        args = _make_args(
            content="-",
            scope="user",
            category="preference",
            name="stdin-mem",
            project_slug=None,
            status="active",
        )
        with patch("anteroom.cli.memory_cli.console", console):
            from anteroom.cli.memory_cli import _handle_create

            _handle_create(db, args)

        from anteroom.services.memory_service import get_memory

        assert get_memory(db, "@user/memory/stdin-mem")["content"] == "stdin payload"


# ---------------------------------------------------------------------------
# _handle_edit
# ---------------------------------------------------------------------------


class TestHandleEdit:
    def test_edit_content(self, db: ThreadSafeConnection) -> None:
        create_memory(db, "v1", scope="user", category="preference", name="ed1")

        console, buf = _capture_console()
        args = _make_args(fqn="@user/memory/ed1", content="v2", status=None, category=None)
        with patch("anteroom.cli.memory_cli.console", console):
            from anteroom.cli.memory_cli import _handle_edit

            _handle_edit(db, args)
        assert "Updated" in buf.getvalue()

        from anteroom.services.memory_service import get_memory

        assert get_memory(db, "@user/memory/ed1")["content"] == "v2"

    def test_edit_status(self, db: ThreadSafeConnection) -> None:
        create_memory(db, "x", scope="user", category="preference", name="ed2")

        console, buf = _capture_console()
        args = _make_args(fqn="@user/memory/ed2", content=None, status="archived", category=None)
        with patch("anteroom.cli.memory_cli.console", console):
            from anteroom.cli.memory_cli import _handle_edit

            _handle_edit(db, args)
        assert "Updated" in buf.getvalue()

        from anteroom.services.memory_service import get_memory

        assert get_memory(db, "@user/memory/ed2")["metadata"]["memory_status"] == "archived"

    def test_edit_category(self, db: ThreadSafeConnection) -> None:
        create_memory(db, "x", scope="user", category="preference", name="ed2b")

        console, buf = _capture_console()
        args = _make_args(fqn="@user/memory/ed2b", content=None, status=None, category="decision")
        with patch("anteroom.cli.memory_cli.console", console):
            from anteroom.cli.memory_cli import _handle_edit

            _handle_edit(db, args)
        assert "Updated" in buf.getvalue()

        from anteroom.services.memory_service import get_memory

        assert get_memory(db, "@user/memory/ed2b")["metadata"]["memory_category"] == "decision"

    def test_edit_invalid_status_surfaces_service_error(self, db: ThreadSafeConnection) -> None:
        # The service rejects invalid status values even though argparse
        # also constrains the CLI choices. Exercise the ValueError path so
        # regressions in the service-layer guard surface in tests.
        create_memory(db, "x", scope="user", category="preference", name="ed-err")

        console, buf = _capture_console()
        args = _make_args(fqn="@user/memory/ed-err", content=None, status="not-a-status", category=None)
        with patch("anteroom.cli.memory_cli.console", console):
            from anteroom.cli.memory_cli import _handle_edit

            with pytest.raises(SystemExit) as exc_info:
                _handle_edit(db, args)
        assert exc_info.value.code == 1
        assert "Invalid memory_status" in buf.getvalue()

    def test_edit_nothing_specified_exits(self, db: ThreadSafeConnection) -> None:
        create_memory(db, "x", scope="user", category="preference", name="ed3")

        console, _ = _capture_console()
        args = _make_args(fqn="@user/memory/ed3", content=None, status=None, category=None)
        with patch("anteroom.cli.memory_cli.console", console):
            from anteroom.cli.memory_cli import _handle_edit

            with pytest.raises(SystemExit) as exc_info:
                _handle_edit(db, args)
        assert exc_info.value.code == 1

    def test_edit_missing_exits(self, db: ThreadSafeConnection) -> None:
        console, _ = _capture_console()
        args = _make_args(fqn="@user/memory/nope", content="x", status=None, category=None)
        with patch("anteroom.cli.memory_cli.console", console):
            from anteroom.cli.memory_cli import _handle_edit

            with pytest.raises(SystemExit) as exc_info:
                _handle_edit(db, args)
        assert exc_info.value.code == 1


# ---------------------------------------------------------------------------
# _handle_delete
# ---------------------------------------------------------------------------


class TestHandleDelete:
    def test_delete_existing(self, db: ThreadSafeConnection) -> None:
        create_memory(db, "gone", scope="user", category="preference", name="d1")

        console, buf = _capture_console()
        with patch("anteroom.cli.memory_cli.console", console):
            from anteroom.cli.memory_cli import _handle_delete

            _handle_delete(db, _make_args(fqn="@user/memory/d1"))
        assert "Deleted" in buf.getvalue()

        from anteroom.services.memory_service import get_memory

        assert get_memory(db, "@user/memory/d1") is None

    def test_delete_missing_exits(self, db: ThreadSafeConnection) -> None:
        console, _ = _capture_console()
        with patch("anteroom.cli.memory_cli.console", console):
            from anteroom.cli.memory_cli import _handle_delete

            with pytest.raises(SystemExit) as exc_info:
                _handle_delete(db, _make_args(fqn="@user/memory/nope"))
        assert exc_info.value.code == 1


# ---------------------------------------------------------------------------
# _run_memory dispatcher
# ---------------------------------------------------------------------------


class TestDispatcher:
    def test_missing_action_prints_usage(self, tmp_path: Any) -> None:
        from unittest.mock import MagicMock

        from anteroom.cli.memory_cli import _run_memory

        cfg = MagicMock()
        cfg.app.data_dir = tmp_path
        console, buf = _capture_console()
        with patch("anteroom.cli.memory_cli.console", console):
            # No memory_action — dispatcher should print usage and return before
            # opening the DB.
            _run_memory(cfg, _make_args(memory_action=None))
        assert "Usage: aroom memory" in buf.getvalue()

    def test_unknown_action_prints_error(self, tmp_path: Any) -> None:
        from unittest.mock import MagicMock

        from anteroom.cli.memory_cli import _run_memory

        cfg = MagicMock()
        cfg.app.data_dir = tmp_path
        console, buf = _capture_console()
        with (
            patch("anteroom.cli.memory_cli.console", console),
            patch("anteroom.db.get_db") as mock_get_db,
        ):
            mock_get_db.return_value = MagicMock()
            _run_memory(cfg, _make_args(memory_action="bogus"))
        assert "Unknown memory action" in buf.getvalue()


# ---------------------------------------------------------------------------
# Promotion / review handlers (#920)
# ---------------------------------------------------------------------------


def _cfg_with_promotion(**overrides: Any) -> Any:
    from unittest.mock import MagicMock

    from anteroom.config import MemoryConfig, MemoryPromotionConfig

    cfg = MagicMock()
    cfg.memory = MemoryConfig(promotion=MemoryPromotionConfig(**overrides))
    cfg.identity = None  # reviewer_id falls back to "cli-reviewer"
    return cfg


class TestHandlePropose:
    def test_propose_prints_fqn_and_status(self, db: ThreadSafeConnection) -> None:
        from anteroom.cli.memory_cli import _handle_propose

        cfg = _cfg_with_promotion()
        console, buf = _capture_console()
        args = _make_args(
            content="dark mode",
            scope="user",
            category="preference",
            proposer="user",
            proposer_id="u-1",
            name="prop1",
            conversation_id=None,
            message_id=None,
            project_slug=None,
        )
        with patch("anteroom.cli.memory_cli.console", console):
            _handle_propose(cfg, db, args)
        assert "Proposed:" in buf.getvalue()
        assert "candidate" in buf.getvalue()

    def test_propose_empty_content_exits(self, db: ThreadSafeConnection) -> None:
        from anteroom.cli.memory_cli import _handle_propose

        cfg = _cfg_with_promotion()
        console, buf = _capture_console()
        args = _make_args(
            content="",
            scope="user",
            category="preference",
            proposer="user",
            proposer_id=None,
            name=None,
            conversation_id=None,
            message_id=None,
            project_slug=None,
        )
        with patch("anteroom.cli.memory_cli.console", console), pytest.raises(SystemExit):
            _handle_propose(cfg, db, args)
        assert "content is empty" in buf.getvalue()

    def test_propose_agent_blocked_surfaces(self, db: ThreadSafeConnection) -> None:
        from anteroom.cli.memory_cli import _handle_propose

        cfg = _cfg_with_promotion(agent_proposals_enabled=False)
        console, buf = _capture_console()
        args = _make_args(
            content="x",
            scope="user",
            category="preference",
            proposer="agent",
            proposer_id="agent-id",
            name="agent-proposal",
            conversation_id=None,
            message_id=None,
            project_slug=None,
        )
        with patch("anteroom.cli.memory_cli.console", console), pytest.raises(SystemExit):
            _handle_propose(cfg, db, args)
        assert "Blocked:" in buf.getvalue()


class TestHandleCandidates:
    def test_list_empty(self, db: ThreadSafeConnection) -> None:
        from anteroom.cli.memory_cli import _handle_candidates

        console, buf = _capture_console()
        with patch("anteroom.cli.memory_cli.console", console):
            _handle_candidates(db, _make_args(status="candidate", namespace=None, limit=None))
        assert "No candidates" in buf.getvalue()

    def test_list_renders_rows(self, db: ThreadSafeConnection) -> None:
        from anteroom.cli.memory_cli import _handle_candidates, _handle_propose

        cfg = _cfg_with_promotion()
        for i in range(2):
            args = _make_args(
                content=f"a{i}",
                scope="user",
                category="preference",
                proposer="user",
                proposer_id="u-1",
                name=f"cand{i}",
                conversation_id=None,
                message_id=None,
                project_slug=None,
            )
            with patch("anteroom.cli.memory_cli.console", Console(file=StringIO())):
                _handle_propose(cfg, db, args)

        console, buf = _capture_console()
        with patch("anteroom.cli.memory_cli.console", console):
            _handle_candidates(db, _make_args(status="candidate", namespace=None, limit=None))
        out = buf.getvalue()
        assert "cand0" in out and "cand1" in out


class TestHandleApproveReject:
    def _propose(self, cfg: Any, db: ThreadSafeConnection, name: str) -> str:
        from anteroom.cli.memory_cli import _handle_propose

        args = _make_args(
            content="prefer dark mode",
            scope="user",
            category="preference",
            proposer="user",
            proposer_id="u-1",
            name=name,
            conversation_id=None,
            message_id=None,
            project_slug=None,
        )
        with patch("anteroom.cli.memory_cli.console", Console(file=StringIO())):
            _handle_propose(cfg, db, args)
        return f"@user/memory/{name}"

    def test_approve_transitions(self, db: ThreadSafeConnection) -> None:
        from anteroom.cli.memory_cli import _handle_approve

        cfg = _cfg_with_promotion()
        fqn = self._propose(cfg, db, "appcli1")
        console, buf = _capture_console()
        args = _make_args(fqn=fqn, edit_content=None, edit_category=None)
        with patch("anteroom.cli.memory_cli.console", console):
            _handle_approve(cfg, db, args)
        assert "Approved:" in buf.getvalue()
        assert "active" in buf.getvalue()

    def test_approve_missing_fqn_exits(self, db: ThreadSafeConnection) -> None:
        from anteroom.cli.memory_cli import _handle_approve

        cfg = _cfg_with_promotion()
        console, buf = _capture_console()
        args = _make_args(fqn="@user/memory/none", edit_content=None, edit_category=None)
        with patch("anteroom.cli.memory_cli.console", console), pytest.raises(SystemExit):
            _handle_approve(cfg, db, args)
        assert "Error:" in buf.getvalue()

    def test_reject_transitions(self, db: ThreadSafeConnection) -> None:
        from anteroom.cli.memory_cli import _handle_reject

        cfg = _cfg_with_promotion()
        fqn = self._propose(cfg, db, "rejcli1")
        console, buf = _capture_console()
        args = _make_args(fqn=fqn, reason="stale")
        with patch("anteroom.cli.memory_cli.console", console):
            _handle_reject(cfg, db, args)
        assert "Rejected:" in buf.getvalue()
        assert "stale" in buf.getvalue()
