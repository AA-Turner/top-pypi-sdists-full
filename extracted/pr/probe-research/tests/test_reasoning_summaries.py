"""The agent's reasoning summaries, turned on for the daemon (`reasoning_summaries`).

The daemon reads an agent's reasoning only where the agent writes summaries of
it: Claude Code's `showThinkingSummaries`, Codex's `model_reasoning_summary`.
Moving an agent to the daemon turns them on where the user never chose;
leaving the daemon or uninstalling puts back what Probe replaced; an explicit
choice -- in the agent's own config or on the wizard's one row -- is the
user's and survives both.
"""

from __future__ import annotations

import importlib
import json
import stat
from pathlib import Path

import pytest

from probe._compat import tomllib
from probe.cli import codex_config
from probe.cli import reasoning_summaries as rs
from probe.cli import setup as wizard
from probe.cli.capabilities import Capabilities
from probe.sdk import session_marker

CC, CODEX = rs.CLAUDE_CODE, rs.CODEX


@pytest.fixture(autouse=True)
def isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "probe" / "config.json"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "claude"))
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex"))
    return tmp_path


def _settings_file(tmp_path: Path) -> Path:
    return tmp_path / "claude" / "settings.json"


def _codex_file(tmp_path: Path) -> Path:
    return tmp_path / "codex" / "config.toml"


def _write(tmp_path: Path, data: dict) -> None:
    path = _settings_file(tmp_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")


def _read(tmp_path: Path) -> dict:
    return json.loads(_settings_file(tmp_path).read_text(encoding="utf-8"))


def _write_codex(tmp_path: Path, text: str) -> Path:
    path = _codex_file(tmp_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _codex_text(tmp_path: Path) -> str:
    return _codex_file(tmp_path).read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Claude Code: on where nobody chose; undone only if Probe did it.
# ---------------------------------------------------------------------------


def test_turning_the_daemon_on_turns_summaries_on_where_nobody_chose(isolate):
    _write(isolate, {"theme": "dark", "statusLine": {"type": "command", "command": "x"}})
    lines = rs.on_for_daemon(CC)
    assert _read(isolate) == {
        "theme": "dark", "statusLine": {"type": "command", "command": "x"}, "showThinkingSummaries": True,
    }, "one key added, nothing else touched"
    assert rs.claimed(CC)
    assert lines[0].startswith("Claude Code's reasoning summaries → on")
    assert any("terminal" in line and "uploaded" in line for line in lines), "says what the user will see"
    assert (isolate / "claude" / "settings.json.probe-backup").is_file(), "the pre-edit file is kept once"


def test_a_missing_settings_file_is_created(isolate):
    rs.on_for_daemon(CC)
    assert _read(isolate) == {"showThinkingSummaries": True}


def test_an_explicit_off_is_the_users_and_is_left_alone(isolate):
    _write(isolate, {"showThinkingSummaries": False})
    lines = rs.on_for_daemon(CC)
    assert _read(isolate) == {"showThinkingSummaries": False}
    assert not rs.claimed(CC)
    assert "will not see why" in " ".join(lines)
    assert rs.undo_for_agent(CC) == []
    assert _read(isolate) == {"showThinkingSummaries": False}


def test_already_on_by_the_user_is_neither_claimed_nor_undone(isolate):
    _write(isolate, {"showThinkingSummaries": True})
    assert rs.on_for_daemon(CC) == []
    assert not rs.claimed(CC)
    assert rs.undo_for_agent(CC) == []
    assert _read(isolate) == {"showThinkingSummaries": True}


def test_leaving_the_daemon_undoes_only_what_probe_did(isolate):
    _write(isolate, {"theme": "dark"})
    rs.on_for_daemon(CC)
    lines = rs.undo_for_agent(CC)
    assert _read(isolate) == {"theme": "dark"}, "back to Claude Code's default: the key removed"
    assert not rs.claimed(CC)
    assert lines == ["Claude Code's reasoning summaries → back to Claude Code's default."]
    assert rs.undo_for_agent(CC) == [], "twice is a no-op"


def test_a_user_who_turned_it_off_since_keeps_it_off(isolate):
    rs.on_for_daemon(CC)
    _write(isolate, {"showThinkingSummaries": False})
    assert rs.undo_for_agent(CC) == []
    assert _read(isolate) == {"showThinkingSummaries": False}
    assert not rs.claimed(CC), "the claim is dropped either way"


def test_the_rows_choice_survives_the_switch_and_uninstall(isolate):
    rs.on_for_daemon(CC)
    lines = rs.set_explicit(True, (CC,))
    assert lines == ["Daemon sees the agent's reasoning → on (Claude Code; new sessions)"]
    assert not rs.claimed(CC), "now the user's choice"
    assert rs.undo_for_agent(CC) == []
    assert _read(isolate) == {"showThinkingSummaries": True}
    rs.set_explicit(False, (CC,))
    assert _read(isolate) == {"showThinkingSummaries": False}
    assert rs.on_for_daemon(CC)[0].startswith("Claude Code's reasoning summaries are off")


def test_a_symlinked_settings_file_is_written_through(isolate):
    target = isolate / "dotfiles" / "claude-settings.json"
    target.parent.mkdir(parents=True)
    target.write_text(json.dumps({"theme": "dark"}), encoding="utf-8")
    link = _settings_file(isolate)
    link.parent.mkdir(parents=True)
    link.symlink_to(target)
    rs.on_for_daemon(CC)
    assert link.is_symlink(), "the link is not replaced by a regular file"
    assert json.loads(target.read_text(encoding="utf-8")) == {"theme": "dark", "showThinkingSummaries": True}


def test_an_unwritable_settings_file_is_reported_not_raised(isolate, monkeypatch):
    from probe.cli import statusline

    def boom(path, settings):
        raise PermissionError("read-only file system")

    monkeypatch.setattr(statusline, "_save", boom)
    lines = rs.on_for_daemon(CC)
    assert lines == ["! could not turn on Claude Code's reasoning summaries: read-only file system"]
    assert not rs.claimed(CC)


@pytest.mark.parametrize("raw", ['{"theme": "dark",}', "[1, 2]", "// comment\n{}"])
def test_a_settings_file_that_does_not_parse_is_never_rewritten(isolate, raw):
    path = _settings_file(isolate)
    path.parent.mkdir(parents=True)
    path.write_text(raw, encoding="utf-8")
    lines = rs.on_for_daemon(CC)
    assert path.read_text(encoding="utf-8") == raw, "the user's other settings are not replaced"
    assert lines[0].startswith("! could not turn on Claude Code's reasoning summaries: left ")
    assert not rs.claimed(CC)
    assert rs.set_explicit(True, (CC,))[0].startswith("! could not set")
    assert path.read_text(encoding="utf-8") == raw


def test_the_undo_touches_only_the_file_probe_turned_it_on_in(isolate, monkeypatch):
    """Two Claude configs (`CLAUDE_CONFIG_DIR`): Probe's `true` went into A; an
    uninstall run from a shell pointing at B must not remove the user's own `true`
    there, and must still undo A."""
    rs.on_for_daemon(CC)  # into isolate/claude
    other = isolate / "claude-b"
    other.mkdir()
    (other / "settings.json").write_text(json.dumps({"showThinkingSummaries": True}), encoding="utf-8")
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(other))
    assert rs.undo_for_agent(CC) == ["Claude Code's reasoning summaries → back to Claude Code's default."]
    assert json.loads((other / "settings.json").read_text(encoding="utf-8")) == {"showThinkingSummaries": True}
    assert _read(isolate) == {}, "the file Probe edited is the one undone"


def test_an_unreadable_file_at_undo_keeps_the_claim(isolate):
    rs.on_for_daemon(CC)
    path = _settings_file(isolate)
    path.write_text('{"showThinkingSummaries": true,}', encoding="utf-8")  # the user broke it
    lines = rs.undo_for_agent(CC)
    assert lines[0].startswith("! could not read ")
    assert rs.claimed(CC), "kept, so the undo can still happen once the file is fixed"
    assert rs.doctor_value(CC).startswith("unknown — ")
    path.write_text('{"showThinkingSummaries": true}', encoding="utf-8")
    rs.undo_for_agent(CC)
    assert _read(isolate) == {}


def test_a_failed_write_leaves_no_claim_and_no_setting(isolate, monkeypatch):
    from probe.cli import statusline

    monkeypatch.setattr(statusline, "_save", lambda path, settings: (_ for _ in ()).throw(OSError("disk full")))
    assert rs.on_for_daemon(CC) == ["! could not turn on Claude Code's reasoning summaries: disk full"]
    assert not rs.claimed(CC)
    assert not _settings_file(isolate).exists()


def test_a_write_keeps_the_files_permissions(isolate):
    _write(isolate, {"env": {"TOKEN": "x"}})
    path = _settings_file(isolate)
    path.chmod(0o600)
    rs.on_for_daemon(CC)
    assert stat.S_IMODE(path.stat().st_mode) == 0o600


def test_a_symlink_loop_reads_as_unset_instead_of_crashing(isolate):
    link = _settings_file(isolate)
    link.parent.mkdir(parents=True)
    link.symlink_to(link)
    assert rs.current(CC) in (rs.State.UNSET, rs.State.UNREADABLE)
    assert rs.on_for_daemon(CC)[0].startswith("!"), "reported, not raised"
    link.unlink()  # the suite's teardown resolves this path


def test_doctor_says_whether_the_daemon_sees_the_reasoning(isolate):
    assert rs.doctor_value(CC).startswith("hidden — reasoning summaries off (Claude Code's default)")
    rs.on_for_daemon(CC)
    assert rs.doctor_value(CC) == "visible (reasoning summaries on, set by Probe)"
    rs.set_explicit(False, (CC,))
    assert rs.doctor_value(CC).startswith("hidden — reasoning summaries off (off in your Claude Code config)")


# ---------------------------------------------------------------------------
# Codex: the same rules, in config.toml, with `auto` put back as found.
# ---------------------------------------------------------------------------

_CODEX_CONFIG = (
    'model = "gpt-5-codex"\n'
    "\n"
    "[profiles.deep]\n"
    'model_reasoning_summary = "none"\n'
    "\n"
    "[mcp_servers.probe-research]\n"
    'url = "https://mcp.test/mcp"\n'
)


def test_codex_summaries_go_on_as_a_top_level_key_above_the_first_table(isolate):
    _write_codex(isolate, _CODEX_CONFIG)
    lines = rs.on_for_daemon(CODEX)
    text = _codex_text(isolate)
    parsed = tomllib.loads(text)
    assert parsed["model_reasoning_summary"] == "detailed"
    assert parsed["profiles"]["deep"]["model_reasoning_summary"] == "none", "a profile's own value is its own"
    assert text.index('model_reasoning_summary = "detailed"') < text.index("[profiles.deep]")
    assert text.replace('model_reasoning_summary = "detailed"\n\n', "", 1) == _CODEX_CONFIG, "no other line moved"
    assert rs.claimed(CODEX)
    assert lines[0] == "Codex's reasoning summaries → on, so the daemon sees why the agent chose what it did."


def test_codex_leaving_the_daemon_restores_the_file(isolate):
    _write_codex(isolate, _CODEX_CONFIG)
    rs.on_for_daemon(CODEX)
    assert rs.undo_for_agent(CODEX) == ["Codex's reasoning summaries → back to Codex's default."]
    assert tomllib.loads(_codex_text(isolate)).get("model_reasoning_summary") is None
    assert not rs.claimed(CODEX)


def test_codex_auto_is_replaced_and_put_back(isolate):
    """`auto` is Codex's default, spelled out: nobody chose summaries, so Probe
    turns them on -- and puts `auto` back, not an absent key, on the way out."""
    _write_codex(isolate, 'model_reasoning_summary = "auto"\nmodel = "x"\n')
    rs.on_for_daemon(CODEX)
    assert _codex_text(isolate) == 'model_reasoning_summary = "detailed"\nmodel = "x"\n', "replaced in place"
    rs.undo_for_agent(CODEX)
    assert _codex_text(isolate) == 'model_reasoning_summary = "auto"\nmodel = "x"\n'


@pytest.mark.parametrize("value", ["none", "concise", "detailed", "verbose"])
def test_codex_a_value_the_user_set_is_never_replaced(isolate, value):
    original = f'model_reasoning_summary = "{value}"\n'
    _write_codex(isolate, original)
    rs.on_for_daemon(CODEX)
    assert _codex_text(isolate) == original
    assert not rs.claimed(CODEX)
    assert rs.undo_for_agent(CODEX) == []


def test_codex_a_value_changed_since_is_the_users(isolate):
    rs.on_for_daemon(CODEX)
    _write_codex(isolate, 'model_reasoning_summary = "concise"\n')
    assert rs.undo_for_agent(CODEX) == []
    assert _codex_text(isolate) == 'model_reasoning_summary = "concise"\n'
    assert not rs.claimed(CODEX)


def test_codex_a_config_that_does_not_parse_is_never_rewritten(isolate):
    raw = "model = \n[broken\n"
    path = _write_codex(isolate, raw)
    lines = rs.on_for_daemon(CODEX)
    assert path.read_text(encoding="utf-8") == raw
    assert lines[0].startswith("! could not turn on Codex's reasoning summaries: left ")
    assert not rs.claimed(CODEX)
    assert rs.set_explicit(True, (CODEX,))[0].startswith("! could not set Codex's")
    assert path.read_text(encoding="utf-8") == raw


def test_codex_a_write_keeps_the_files_mode_and_a_new_file_is_private(isolate):
    path = _write_codex(isolate, 'model = "x"\n')
    path.chmod(0o640)
    rs.on_for_daemon(CODEX)
    assert stat.S_IMODE(path.stat().st_mode) == 0o640
    path.unlink()
    rs.set_explicit(True, (CODEX,))
    assert stat.S_IMODE(path.stat().st_mode) == 0o600, "config.toml holds MCP tokens"


def test_codex_a_missing_config_is_created_and_undone(isolate):
    rs.on_for_daemon(CODEX)
    assert _codex_text(isolate) == 'model_reasoning_summary = "detailed"\n'
    rs.undo_for_agent(CODEX)
    assert _codex_text(isolate) == ""


def test_codex_a_last_line_without_a_newline_is_not_joined(isolate):
    _write_codex(isolate, 'model = "x"')
    rs.on_for_daemon(CODEX)
    assert tomllib.loads(_codex_text(isolate)) == {"model": "x", "model_reasoning_summary": "detailed"}


def test_codex_the_quoted_key_spelling_is_the_same_key(isolate):
    _write_codex(isolate, '"model_reasoning_summary" = "auto"\n')
    rs.on_for_daemon(CODEX)
    assert tomllib.loads(_codex_text(isolate)) == {"model_reasoning_summary": "detailed"}


def test_write_top_level_refuses_what_would_not_read_back(isolate):
    """A top-level value continued onto more lines cannot be swapped line for
    line; the result is checked, and refused rather than written."""
    raw = 'model_reasoning_summary = """\nauto"""\n'
    path = _write_codex(isolate, raw)
    with pytest.raises(codex_config.ConfigError):
        codex_config.write_top_level("model_reasoning_summary", "detailed", path=path)
    assert path.read_text(encoding="utf-8") == raw


@pytest.mark.parametrize(
    "line", ['model_reasoning_summary = ["detailed"]', "model_reasoning_summary = { a = 1 }",
             "model_reasoning_summary.x = 1"],
)
def test_codex_a_value_that_is_not_a_string_is_reported_not_raised(isolate, line):
    original = line + "\n"
    _write_codex(isolate, original)
    assert rs.current(CODEX) is rs.State.OFF, "someone typed it: theirs"
    assert "will not see why" in " ".join(rs.on_for_daemon(CODEX))
    assert rs.set_explicit(False, (CODEX,)) == ["Daemon sees the agent's reasoning → off (Codex; new sessions)"]
    assert _codex_text(isolate) == original
    assert rs.doctor_value(CODEX).startswith("hidden — ")
    assert rs.row_on((CODEX,)) is False


def test_codex_a_symlinked_config_is_written_through(isolate):
    target = isolate / "dotfiles" / "codex.toml"
    target.parent.mkdir(parents=True)
    target.write_text('model = "x"\n', encoding="utf-8")
    link = _codex_file(isolate)
    link.parent.mkdir(parents=True)
    link.symlink_to(target)
    rs.on_for_daemon(CODEX)
    assert link.is_symlink(), "the link is not replaced by a regular file"
    assert tomllib.loads(target.read_text(encoding="utf-8"))["model_reasoning_summary"] == "detailed"
    rs.undo_for_agent(CODEX)
    assert target.read_text(encoding="utf-8") == 'model = "x"\n'


def test_codex_a_bracket_inside_a_multiline_string_is_not_a_table(isolate):
    """A markdown link opening a line of a prompt is part of the string: the key
    goes above the REAL first table, and the undo finds it again."""
    original = (
        'developer_instructions = """\n[docs](https://x)\n"""\n'
        "\n"
        "[profiles.deep]\n"
        'model = "y"\n'
    )
    _write_codex(isolate, original)
    rs.on_for_daemon(CODEX)
    parsed = tomllib.loads(_codex_text(isolate))
    assert parsed["model_reasoning_summary"] == "detailed"
    assert parsed["developer_instructions"] == "[docs](https://x)\n", "the string is unchanged"
    assert rs.undo_for_agent(CODEX) == ["Codex's reasoning summaries → back to Codex's default."]
    assert "model_reasoning_summary" not in tomllib.loads(_codex_text(isolate))


def test_codex_crlf_line_endings_are_kept(isolate):
    path = _write_codex(isolate, "")
    path.write_bytes(b'model = "x"\r\n\r\n[profiles.deep]\r\nmodel = "y"\r\n')
    rs.on_for_daemon(CODEX)
    raw = path.read_bytes()
    assert b"\n" not in raw.replace(b"\r\n", b""), "no bare LF introduced or left"
    assert b'model_reasoning_summary = "detailed"\r\n' in raw


def test_write_top_level_never_reports_a_removal_it_could_not_make(isolate):
    path = _write_codex(isolate, "model_reasoning_summary.x = 1\n")
    with pytest.raises(codex_config.ConfigError):
        codex_config.write_top_level("model_reasoning_summary", None, path=path)


def test_the_row_keeps_a_users_own_on_spelling(isolate):
    _write_codex(isolate, 'model_reasoning_summary = "concise"\n')
    rs.set_explicit(True, (CC, CODEX))
    assert _codex_text(isolate) == 'model_reasoning_summary = "concise"\n', "already on: not rewritten"
    assert _read(isolate) == {"showThinkingSummaries": True}


@pytest.mark.parametrize("value", ["false", None, 0])
def test_claude_a_value_the_user_typed_is_theirs(isolate, value):
    _write(isolate, {"showThinkingSummaries": value})
    assert rs.current(CC) is rs.State.OFF
    rs.on_for_daemon(CC)
    assert _read(isolate) == {"showThinkingSummaries": value}
    assert not rs.claimed(CC)


def test_one_agents_claim_does_not_touch_the_others(isolate):
    rs.on_for_daemon(CC)
    rs.on_for_daemon(CODEX)
    rs.undo_for_agent(CODEX)
    assert rs.claimed(CC) and not rs.claimed(CODEX)
    assert _read(isolate) == {"showThinkingSummaries": True}
    rs.undo_for_agent(CC)
    assert not (isolate / "state" / "probe" / "reasoning-summaries.json").exists(), "an empty claim is removed"


def test_a_damaged_claim_claims_nothing(isolate):
    _write(isolate, {"showThinkingSummaries": True})
    claim = isolate / "state" / "probe" / "reasoning-summaries.json"
    claim.parent.mkdir(parents=True)
    claim.write_text("{not json", encoding="utf-8")
    assert rs.undo_for_agent(CC) == []
    assert _read(isolate) == {"showThinkingSummaries": True}, "a guess never takes the user's value"


# ---------------------------------------------------------------------------
# Wired into the wizard: Who records, the one row, uninstall.
# ---------------------------------------------------------------------------


@pytest.fixture
def calls(monkeypatch):
    from test_who_records import Calls

    c = Calls(monkeypatch)
    c.key["held"] = True
    return c


def test_moving_claude_code_to_the_daemon_and_back(isolate, calls):
    caps = Capabilities(agent_source="claude_code", tracking_plugin_installed=True, capture_plugin_installed=True)
    lines = wizard.apply_recorder(caps, session_marker.RECORDER_DAEMON, base_url="https://api.test")
    assert _read(isolate) == {"showThinkingSummaries": True}
    assert lines.index("Who records in Claude Code → the daemon") < next(
        i for i, line in enumerate(lines) if line.startswith("Claude Code's reasoning summaries → on"))
    assert not _codex_file(isolate).exists(), "Codex's config is Codex's move"
    lines = wizard.apply_recorder(caps, session_marker.RECORDER_AGENT, base_url="https://api.test")
    assert _read(isolate) == {}
    assert "Claude Code's reasoning summaries → back to Claude Code's default." in lines


def test_moving_codex_to_the_daemon_and_back(isolate, calls):
    caps = Capabilities(agent_source="codex", tracking_plugin_installed=True, capture_plugin_installed=True)
    lines = wizard.apply_recorder(caps, session_marker.RECORDER_DAEMON, base_url="https://api.test")
    assert tomllib.loads(_codex_text(isolate))["model_reasoning_summary"] == "detailed"
    assert any(line.startswith("Codex's reasoning summaries → on") for line in lines)
    assert not _settings_file(isolate).exists(), "Claude's settings are Claude's move"
    wizard.apply_recorder(caps, session_marker.RECORDER_AGENT, base_url="https://api.test")
    assert "model_reasoning_summary" not in tomllib.loads(_codex_text(isolate))


def _stub_uninstall(monkeypatch):
    from probe.cli import import_jobs

    class Off:
        plugin_removed = verified = True
        warnings: list = []

        def summary(self):
            return "Capture off."

    monkeypatch.setattr(import_jobs, "clear_all", lambda: None)
    monkeypatch.setattr(wizard, "turn_off", lambda mode: Off())
    monkeypatch.setattr(wizard, "uninstall_plugin", lambda name, source=None: wizard.claude_cli.Result(ok=True))
    monkeypatch.setattr(wizard, "apply_agent_rules", lambda on: [])
    monkeypatch.setattr(wizard, "clear_killswitch", lambda: None)


def test_uninstall_undoes_what_probe_turned_on(isolate, monkeypatch):
    rs.on_for_daemon(CC)
    rs.on_for_daemon(CODEX)
    _stub_uninstall(monkeypatch)
    lines = wizard.remove_everything(Capabilities(agent_source="claude_code"))
    assert _read(isolate) == {}
    assert "Claude Code's reasoning summaries → back to Claude Code's default." in lines
    assert rs.claimed(CODEX), "Codex is uninstalled on its own pass, not Claude Code's"


def test_the_one_row_covers_every_agent_set_up(isolate):
    wizard.grouped_settings()  # the registry agrees: enum, group, copy
    both = {"claude_code": Capabilities(), "codex": Capabilities()}
    assert wizard.read_settings(both)[wizard.Setting.REASONING_SUMMARIES] is False
    lines = wizard.apply_settings({wizard.Setting.REASONING_SUMMARIES: True}, caps_by_source=both)
    assert lines == ["Daemon sees the agent's reasoning → on (Claude Code, Codex; new sessions)"]
    assert _read(isolate) == {"showThinkingSummaries": True}
    assert tomllib.loads(_codex_text(isolate)) == {"model_reasoning_summary": "detailed"}
    assert wizard.read_settings(both)[wizard.Setting.REASONING_SUMMARIES] is True
    rs.set_explicit(False, (CODEX,))
    assert wizard.read_settings(both)[wizard.Setting.REASONING_SUMMARIES] is False, "on only when ALL are on"
    wizard.apply_settings({wizard.Setting.REASONING_SUMMARIES: False}, caps_by_source=both)
    assert _read(isolate) == {"showThinkingSummaries": False}
    assert tomllib.loads(_codex_text(isolate)) == {"model_reasoning_summary": "none"}


def test_the_row_leaves_an_agent_not_set_up_alone(isolate):
    only_claude = {"claude_code": Capabilities()}
    wizard.apply_settings({wizard.Setting.REASONING_SUMMARIES: True}, caps_by_source=only_claude)
    assert _read(isolate) == {"showThinkingSummaries": True}
    assert not _codex_file(isolate).exists()
    assert wizard.read_settings(only_claude)[wizard.Setting.REASONING_SUMMARIES] is True


def test_the_row_lives_on_the_daemons_page_not_settings():
    """What the daemon sees is asked on the daemon's page (Enter on Defaults ›
    Who records, or straight after switching to the daemon), not on Settings."""
    daemon_page = {s for _, settings in wizard.DAEMON_GROUPS for s in settings}
    settings = {s for _, group in wizard.SETTINGS_GROUPS for s in group}
    assert wizard.Setting.REASONING_SUMMARIES in daemon_page
    assert wizard.Setting.REASONING_SUMMARIES not in settings


def test_the_pages_choice_lands_after_the_switch(isolate, monkeypatch, calls):
    """Switching to the daemon turns reasoning summaries on where nobody chose;
    the daemon's page then asks, and an untick there is a choice, so it lands
    last."""
    from probe.cli import tui

    cli_main = importlib.import_module("probe.cli.main")
    monkeypatch.setattr(wizard, "daemon_availability", lambda base_url=None: (True, None))
    monkeypatch.setattr(wizard, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_" + "1" * 32)  # a switch needs a signed-in machine
    seen = {}

    def page(current, **kw):
        seen.update(kw)
        return {wizard.Setting.REASONING_SUMMARIES: False}

    monkeypatch.setattr(wizard, "run_settings_menu", page)
    caps = {"claude_code": Capabilities(agent_source="claude_code", tracking_plugin_installed=True,
                                        capture_plugin_installed=True)}
    lines = cli_main._run_recorder_action(
        yes=False, caps_by_source=caps, base_now="https://api.test", chosen=session_marker.RECORDER_DAEMON
    )
    assert seen["groups"] == wizard.DAEMON_GROUPS
    assert _read(isolate) == {"showThinkingSummaries": False}
    assert not _codex_file(isolate).exists(), "Codex is not set up here, so the row left it alone"
    assert lines[-1] == "Daemon sees the agent's reasoning → off (Claude Code; new sessions)"
