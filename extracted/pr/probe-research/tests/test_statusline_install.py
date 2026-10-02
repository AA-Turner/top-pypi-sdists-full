"""Claiming a share of the status-line slot without breaking whoever else is in it.

The composition tests are string assertions, but the two that matter EXECUTE the
composed command through /bin/sh, because both bugs this module exists to avoid
are invisible to a string comparison: a predecessor ending in a shell comment,
and a predecessor that drains stdin. Both produce a chain that looks perfectly
correct and renders nothing.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

import pytest

from probe import cli
from probe.cli import statusline
from probe.sdk import session_marker


SHOW_SESSION = "statusline-show-1111-2222-333333333333"


@pytest.fixture()
def claude_home(tmp_path, monkeypatch):
    home = tmp_path / "claude"
    home.mkdir()
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(home))
    return home


@pytest.fixture()
def plugin_root(tmp_path):
    """A stand-in plugin tree: install copies files, it does not import them."""
    root = tmp_path / "plugin"
    (root / "hooks").mkdir(parents=True)
    for name in statusline.RENDERER_FILES:
        (root / "hooks" / name).write_text(f"# {name}\n", encoding="utf-8")
    return root


@pytest.fixture()
def show_env(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_statusline_show")
    monkeypatch.delenv("PROBE_CONFIG_PATH", raising=False)
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)


def _settings(home) -> dict:
    return json.loads((home / "settings.json").read_text(encoding="utf-8"))


def _command(home) -> str:
    return _settings(home)["statusLine"]["command"]


def _write_slot(home, command: str, **rest) -> None:
    payload = {"statusLine": {"type": "command", "command": command}}
    payload.update(rest)
    (home / "settings.json").write_text(json.dumps(payload), encoding="utf-8")


# -- composition ------------------------------------------------------------


def test_install_into_an_empty_slot(claude_home, plugin_root) -> None:
    result = statusline.install(plugin_root)
    assert result["chained_after"] is None
    assert statusline.MARKER in _command(claude_home)


def test_install_keeps_the_previous_command(claude_home, plugin_root) -> None:
    _write_slot(claude_home, "my-prompt --fancy")
    result = statusline.install(plugin_root)
    assert result["chained_after"] == "my-prompt --fancy"
    assert "my-prompt --fancy" in _command(claude_home)


def test_install_preserves_unrelated_settings(claude_home, plugin_root) -> None:
    _write_slot(claude_home, "my-prompt", model="opus", permissions={"allow": ["x"]})
    statusline.install(plugin_root)
    settings = _settings(claude_home)
    assert settings["model"] == "opus"
    assert settings["permissions"] == {"allow": ["x"]}


def test_reinstall_does_not_nest(claude_home, plugin_root) -> None:
    _write_slot(claude_home, "my-prompt")
    statusline.install(plugin_root)
    first = _command(claude_home)
    statusline.install(plugin_root)
    assert _command(claude_home) == first
    assert first.count(statusline.MARKER) == 1


def test_the_renderer_is_copied_to_a_stable_directory(claude_home, plugin_root) -> None:
    """The plugin's own path carries its version and would break on every release."""
    result = statusline.install(plugin_root)
    assert sorted(result["copied"]) == sorted(statusline.RENDERER_FILES)
    for name in statusline.RENDERER_FILES:
        assert (statusline.install_dir() / name).is_file()
    assert str(statusline.install_dir()) in result["command"]


def test_sync_is_content_compared(claude_home, plugin_root) -> None:
    statusline.install(plugin_root)
    assert statusline.sync(plugin_root) == []  # identical bytes: nothing to do
    (plugin_root / "hooks" / "statusline.py").write_text("# changed\n", encoding="utf-8")
    assert statusline.sync(plugin_root) == ["statusline.py"]


# -- the two bugs that only show up when the command RUNS --------------------


def _render(home, payload: dict) -> str:
    """Execute the composed status-line command exactly as Claude Code does."""
    return subprocess.run(
        ["/bin/sh", "-c", _command(home)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=30,
    ).stdout


def _fake_renderer(tmp_path, plugin_root) -> None:
    """Replace the copied renderer with one that echoes what it was given, so a
    test can tell "our segment ran" from "our segment ran with no stdin"."""
    (plugin_root / "hooks" / "statusline.py").write_text(
        "import sys, json\n"
        "raw = sys.stdin.read()\n"
        "try:\n"
        "    sid = json.loads(raw).get('session_id', 'NOJSON')\n"
        "except Exception:\n"
        "    sid = 'NOSTDIN'\n"
        "sys.stdout.write('  <' + sid + '>')\n",
        encoding="utf-8",
    )


def test_a_predecessor_ending_in_a_comment_does_not_comment_us_out(
    claude_home, plugin_root, tmp_path
) -> None:
    """THE BUG THIS MODULE'S NEWLINES EXIST FOR.

    imsg-device's installer appends `# imsg-device statusline` as its idempotency
    marker, and a `a; b` chain after that comments the rest of the line -- our
    segment included -- silently.
    """
    _fake_renderer(tmp_path, plugin_root)
    _write_slot(claude_home, "/bin/echo -n NEIGHBOUR # imsg-device statusline")
    statusline.install(plugin_root, python=sys.executable)
    out = _render(claude_home, {"session_id": "sess-1234"})
    assert "NEIGHBOUR" in out, "the predecessor must still render"
    assert "<sess-1234>" in out, "our segment was commented out by their marker"


def test_a_predecessor_that_drains_stdin_does_not_starve_us(
    claude_home, plugin_root, tmp_path
) -> None:
    """Most status lines start with `input=$(cat)`. Only one process is piped to,
    so an unteed chain leaves the second command reading an empty pipe -- which
    looks exactly like a renderer bug, forever."""
    _fake_renderer(tmp_path, plugin_root)
    _write_slot(claude_home, 'greedy=$(cat); /bin/echo -n "got:${#greedy}"')
    statusline.install(plugin_root, python=sys.executable)
    out = _render(claude_home, {"session_id": "sess-1234"})
    assert "got:" in out and "got:0" not in out, "the predecessor lost its stdin"
    assert "<sess-1234>" in out, "we lost our stdin"


def test_a_failing_predecessor_does_not_take_us_down(claude_home, plugin_root, tmp_path) -> None:
    _fake_renderer(tmp_path, plugin_root)
    _write_slot(claude_home, "/bin/sh -c 'exit 3'")
    statusline.install(plugin_root, python=sys.executable)
    assert "<sess-1234>" in _render(claude_home, {"session_id": "sess-1234"})


# -- uninstall --------------------------------------------------------------


def test_uninstall_restores_the_predecessor_exactly(claude_home, plugin_root) -> None:
    original = "my-prompt --fancy # someone-elses-marker"
    _write_slot(claude_home, original)
    statusline.install(plugin_root)
    result = statusline.uninstall()
    assert result["removed"] is True
    assert _command(claude_home) == original


def test_uninstall_removes_the_key_when_it_wrapped_nothing(claude_home, plugin_root) -> None:
    """An empty command is not the same as no status line, and would render as a
    permanently blank row."""
    statusline.install(plugin_root)
    statusline.uninstall()
    assert "statusLine" not in _settings(claude_home)


def test_uninstall_leaves_a_slot_we_never_touched_alone(claude_home) -> None:
    _write_slot(claude_home, "someone-elses-prompt")
    result = statusline.uninstall()
    assert result["removed"] is False
    assert _command(claude_home) == "someone-elses-prompt"


def test_status_reports_the_slot(claude_home, plugin_root) -> None:
    assert statusline.status()["installed"] is False
    _write_slot(claude_home, "my-prompt")
    statusline.install(plugin_root)
    reported = statusline.status()
    assert reported["installed"] is True
    assert reported["chained_after"] == "my-prompt"


# -- CLI debugging entrypoint ----------------------------------------------


def _show(capsys) -> tuple[str, dict]:
    assert cli.main(["statusline", "show", "--session", SHOW_SESSION]) in (0, None)
    lines = capsys.readouterr().out.splitlines()
    return lines[0], json.loads(lines[1])


def test_show_renders_an_existing_on_signal_without_resolving_defaults(
    show_env, monkeypatch, capsys
) -> None:
    assert session_marker.set_tracking(SHOW_SESSION, True)
    monkeypatch.setattr(
        session_marker,
        "resolve_tracking_default",
        lambda *_args, **_kwargs: pytest.fail(
            "an existing signal must bypass folder resolution"
        ),
    )

    segment, detail = _show(capsys)

    assert "tracking" in segment
    assert "not tracking" not in segment
    assert detail["session_id"] == SHOW_SESSION


def test_show_renders_an_existing_off_signal_without_resolving_defaults(
    show_env, monkeypatch, capsys
) -> None:
    assert session_marker.set_tracking(SHOW_SESSION, False)
    monkeypatch.setattr(
        session_marker,
        "resolve_tracking_default",
        lambda *_args, **_kwargs: pytest.fail(
            "an existing signal must bypass folder resolution"
        ),
    )

    segment, _detail = _show(capsys)

    assert "not tracking" in segment


def test_show_renders_for_an_mcp_only_configuration(
    show_env, monkeypatch, capsys
) -> None:
    monkeypatch.delenv("PROBE_TOKEN", raising=False)
    monkeypatch.setenv("PROBE_MCP_TOKEN", "probe_mcp_statusline_show")
    assert session_marker.set_tracking(SHOW_SESSION, True)

    segment, _detail = _show(capsys)

    assert "tracking" in segment


def test_show_uses_the_process_cwd_folder_default_when_signal_is_absent(
    show_env, tmp_path, monkeypatch, capsys
) -> None:
    repo = tmp_path / "research"
    cwd = repo / "src"
    cwd.mkdir(parents=True)
    config = repo / ".probe" / "config.json"
    config.parent.mkdir()
    config.write_text(
        json.dumps({"defaults": {"session_tracking": "off"}}), encoding="utf-8"
    )
    monkeypatch.chdir(cwd)

    segment, _detail = _show(capsys)

    assert session_marker.tracking_signal(SHOW_SESSION) is None
    assert "not tracking" in segment


# -- the file we are editing is not ours ------------------------------------


def test_a_symlinked_settings_file_is_written_through(tmp_path, monkeypatch, plugin_root) -> None:
    """People symlink settings.json into a dotfiles repo. Writing the LINK
    replaces it with a regular file and quietly detaches them from the repo."""
    home = tmp_path / "claude"
    home.mkdir()
    real = tmp_path / "dotfiles" / "settings.json"
    real.parent.mkdir()
    real.write_text(json.dumps({"model": "opus"}), encoding="utf-8")
    (home / "settings.json").symlink_to(real)
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(home))

    statusline.install(plugin_root)

    assert (home / "settings.json").is_symlink()
    assert statusline.MARKER in json.loads(real.read_text())["statusLine"]["command"]


def test_the_backup_is_taken_once_and_never_overwritten(claude_home, plugin_root) -> None:
    """The FIRST backup is the pre-Probe state; a later one would only capture
    our own edit, which is not what anyone reaches for it to recover."""
    _write_slot(claude_home, "original")
    statusline.install(plugin_root)
    backup = claude_home / "settings.json.probe-backup"
    assert "original" == json.loads(backup.read_text())["statusLine"]["command"]
    statusline.install(plugin_root)
    assert "original" == json.loads(backup.read_text())["statusLine"]["command"]


def test_a_settings_file_that_is_not_json_is_not_destroyed_silently(
    claude_home, plugin_root
) -> None:
    """It is still backed up before we replace it, so nothing is unrecoverable."""
    (claude_home / "settings.json").write_text("{ broken", encoding="utf-8")
    statusline.install(plugin_root)
    assert (claude_home / "settings.json.probe-backup").read_text() == "{ broken"
    assert statusline.MARKER in _command(claude_home)


# -- discovery --------------------------------------------------------------


def test_explicit_plugin_root_wins(monkeypatch, plugin_root) -> None:
    monkeypatch.setenv("PROBE_PLUGIN_ROOT", str(plugin_root))
    assert statusline.discover_plugin_root() == plugin_root


def test_discovery_finds_this_checkout(monkeypatch) -> None:
    monkeypatch.delenv("PROBE_PLUGIN_ROOT", raising=False)
    found = statusline.discover_plugin_root()
    assert found is not None
    assert (found / "hooks" / "statusline.py").is_file()


def test_the_interpreter_is_never_the_active_virtualenv(tmp_path, monkeypatch) -> None:
    """`probe` runs from inside a venv; baking that interpreter into settings.json
    means the status line dies silently when the venv is deleted."""
    venv = tmp_path / "venv"
    (venv / "bin").mkdir(parents=True)
    fake = venv / "bin" / "python3"
    fake.write_text("#!/bin/sh\n", encoding="utf-8")
    fake.chmod(0o755)
    monkeypatch.setenv("VIRTUAL_ENV", str(venv))
    monkeypatch.setenv("PATH", os.pathsep.join([str(venv / "bin"), "/usr/bin", "/bin"]))

    chosen = statusline.python_bin()

    assert str(venv) not in chosen
    assert os.path.isabs(chosen)
