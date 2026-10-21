"""`--agent` is repeatable, and every agent named goes through ONE approval.

The desktop app's agent picker maps to one `configure` run: `--agent claude
--agent pi` installs both behind a single browser approval. Every value the
flag took before keeps its meaning -- the table below was captured from
origin/main (34865d40a) with the same fixture.
"""

from __future__ import annotations

import os

import pytest
from typer.testing import CliRunner

from probe.sdk.config import save_context
from tests import test_wizard_json_events as events

device = events.device
main = events.main

OLD_VALUES = [
    ("claude", ["claude_code"]),
    ("claude_code", ["claude_code"]),
    ("codex", ["codex"]),
    ("pi", ["pi"]),
    ("kimi", ["kimi_code"]),
    ("both", ["claude_code", "codex"]),
    ("all", ["claude_code", "codex"]),
    ("claude,codex", ["claude_code", "codex"]),
    ("codex,claude", ["claude_code", "codex"]),
    ("BOTH", ["claude_code", "codex"]),
    (" Claude ", ["claude_code"]),
]


@pytest.fixture
def applied(device, monkeypatch):
    """The agents each configure pass ran for, in order."""
    seen: list[str | None] = []
    monkeypatch.setattr(
        main, "_run_wizard_action", lambda *a, **k: seen.append(os.environ.get("PROBE_AGENT")) or []
    )
    return seen


@pytest.mark.parametrize("value,sources", OLD_VALUES)
def test_every_old_agent_value_configures_the_same_agents(applied, value, sources):
    CliRunner().invoke(main.app, ["wizard", "--action", "configure", "--yes", "--agent", value])
    assert applied == sources


@pytest.mark.parametrize("value", ["bogus", "claude,pi"])
def test_an_unknown_agent_is_still_refused_with_the_same_words(applied, value):
    result = CliRunner().invoke(main.app, ["wizard", "--action", "configure", "--yes", "--agent", value])
    assert "--agent must be claude, codex, pi, kimi, or both" in events.plain(result.stderr)


def test_a_sign_in_flag_with_an_unknown_agent_says_the_flag_would_be_dropped(applied):
    """The sign-in-only refusal comes first, as on main: `--agent` is a flag it
    would drop, whatever its value."""
    result = CliRunner().invoke(main.app, ["wizard", "--token", "probe_pat_x", "--agent", "bogus"])
    assert "these flags only sign in, so --agent would be ignored" in events.plain(result.stderr)


def test_a_repeated_agent_flag_configures_each_agent_in_one_run(applied):
    CliRunner().invoke(
        main.app, ["wizard", "--action", "configure", "--yes", "--agent", "claude", "--agent", "pi"]
    )
    assert applied == ["claude_code", "pi"]


def test_install_takes_a_repeated_agent_flag_too(applied):
    CliRunner().invoke(main.app, ["install", "--yes", "--agent", "claude", "--agent", "pi"])
    assert applied == ["claude_code", "pi"]


def test_two_named_agents_share_one_browser_approval(device):
    CliRunner().invoke(
        main.app, ["wizard", "--action", "configure", "--yes", "--agent", "claude", "--agent", "pi"]
    )
    assert len(device.authorizations) == 1


def test_two_named_agents_are_both_installed(device):
    CliRunner().invoke(
        main.app, ["wizard", "--action", "configure", "--yes", "--agent", "claude", "--agent", "pi"]
    )
    assert {source for source, kind in device.installed if kind == "tracking"} == {"claude_code", "pi"}


# -- a lone missing MCP grant ---------------------------------------------------


@pytest.fixture
def missing_only_mcp(device):
    """Signed in, capture paired and everything installed: only the read token
    the MCP serves is missing (a `--token` login mints none)."""
    save_context({"token": "probe_pat_api", "ingest_token": "ros_ing_claude_code"})
    device.installed.update(
        ("claude_code", kind) for kind in ("tracking", "capture", "updates", "rules")
    )
    return device


def test_a_json_run_asks_for_a_lone_missing_mcp_grant(missing_only_mcp):
    CliRunner().invoke(
        main.app, ["wizard", "--action", "configure", "--yes", "--agent", "claude", "--json"]
    )
    assert missing_only_mcp.authorizations == [["mcp"]]


def test_a_headless_run_without_json_still_skips_it(missing_only_mcp):
    """Unchanged: nobody is there to approve, so the install does not wait on it."""
    CliRunner().invoke(main.app, ["wizard", "--action", "configure", "--yes", "--agent", "claude"])
    assert missing_only_mcp.authorizations == []
