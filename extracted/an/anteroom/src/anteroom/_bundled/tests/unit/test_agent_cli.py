"""Unit tests for cli.agent_cli (#1459)."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    from anteroom.db import init_db

    return init_db(tmp_path / "test.db")


class TestAgentStatusModelRow:
    """/agent status prints the persisted model (#1459)."""

    def test_model_row_shown_when_persisted(self, db: Any) -> None:
        """When a run has model in metadata, /agent status displays a Model: row."""
        from anteroom.cli.agent_cli import handle_agent_status
        from anteroom.services.storage import (
            create_agent_run,
            create_conversation,
            update_agent_run,
        )

        conv = create_conversation(db, title="c")
        run = create_agent_run(
            db,
            conversation_id=conv["id"],
            kind="detached_subagent",
            title="ran",
            metadata={"prompt": "p", "model": "claude-sonnet-4-6", "output": ""},
        )
        update_agent_run(db, run["id"], status="completed")

        console_output: list[str] = []
        renderer = MagicMock()
        renderer.console.print = lambda msg, **kw: console_output.append(str(msg))

        handle_agent_status(db, run["id"][:8], renderer)

        joined = "\n".join(console_output)
        assert "Model:" in joined
        assert "claude-sonnet-4-6" in joined

    def test_model_row_absent_when_no_model(self, db: Any) -> None:
        """When a run has no model in metadata, /agent status omits the Model: row."""
        from anteroom.cli.agent_cli import handle_agent_status
        from anteroom.services.storage import (
            create_agent_run,
            create_conversation,
            update_agent_run,
        )

        conv = create_conversation(db, title="c")
        run = create_agent_run(
            db,
            conversation_id=conv["id"],
            kind="detached_subagent",
            title="ran",
            metadata={"prompt": "p"},  # no model
        )
        update_agent_run(db, run["id"], status="completed")

        console_output: list[str] = []
        renderer = MagicMock()
        renderer.console.print = lambda msg, **kw: console_output.append(str(msg))

        handle_agent_status(db, run["id"][:8], renderer)

        joined = "\n".join(console_output)
        assert "Model:" not in joined
