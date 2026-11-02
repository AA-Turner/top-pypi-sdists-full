"""Tests for run_legacy_mode (spawned legacy-mode task target, issue #2117)."""

from unittest.mock import patch

from agentic_devtools.cli.jira.create_epic_router import run_legacy_mode


def test_emits_routing_record_then_calls_create_epic(capsys):
    with patch("agentic_devtools.cli.jira.create_commands.create_epic") as create_epic:
        run_legacy_mode(dry_run_override=True)

    out = capsys.readouterr().out
    assert '"event": "create_epic.routing"' in out
    assert '"mode": "legacy"' in out
    assert '"basis": "legacy_state_present"' in out
    create_epic.assert_called_once_with(dry_run_override=True)


def test_default_override_is_false(capsys):
    with patch("agentic_devtools.cli.jira.create_commands.create_epic") as create_epic:
        run_legacy_mode()
    create_epic.assert_called_once_with(dry_run_override=False)
