"""Probe's state in Kimi Code's footer (`$KIMI_CODE_HOME/tui.toml`).

Kimi runs `[status_line] command` through `sh -c` with a JSON snapshot on stdin
and `KIMI_CODE_STATUS_LINE=1` set, keeps the FIRST stdout line as footer line 1
(replacing its own) and kills the command after 300 ms (Kimi 2.1.1 bundle:
`runStatusLineCommand(command, payload, timeoutMs = 300)`). These tests run the
real chain the same way.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

from probe.cli import statusline

AGENT = Path(__file__).resolve().parents[1]
PLUGIN = AGENT / "plugins" / "probe-research"
SID = "2786940c-962c-405b-9c85-f7b274838857"


@pytest.fixture()
def kimi(tmp_path, monkeypatch):
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("KIMI_CODE_HOME", str(tmp_path / "kimi"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "probe" / "config.json"))
    (tmp_path / "probe").mkdir()
    (tmp_path / "probe" / "config.json").write_text(json.dumps(
        {"current_context": "default", "contexts": {"default": {"base_url": "https://api.example", "token": "t"}}}))
    (tmp_path / "kimi").mkdir()
    return tmp_path


def _snapshot(home: Path) -> str:
    return json.dumps({"model": "gpt-oss-120b", "cwd": str(home / "proj"), "gitBranch": "main",
                       "sessionId": f"session_{SID}", "version": "2.1.1"})


def _run_footer(kimi_root: Path, home: Path) -> tuple[str, float]:
    command = statusline._kimi_command((kimi_root / "kimi" / "tui.toml").read_text())
    env = {**os.environ, "KIMI_CODE_STATUS_LINE": "1"}
    started = time.monotonic()
    out = subprocess.run(["sh", "-c", command], input=_snapshot(home), capture_output=True, text=True,
                         env=env, timeout=5)
    return out.stdout.split("\n")[0].rstrip(), time.monotonic() - started


def test_install_writes_the_slot_and_the_footer_keeps_kimis_own_line(kimi):
    (kimi / "kimi" / "tui.toml").write_text('theme = "auto" # mine\n\n[editor]\ncommand = ""\n')
    statusline.install_kimi(PLUGIN, python=sys.executable)
    text = (kimi / "kimi" / "tui.toml").read_text()
    assert 'theme = "auto" # mine' in text and '[editor]\ncommand = ""' in text  # untouched
    line, took = _run_footer(kimi, kimi / "home")
    assert line.startswith("gpt-oss-120b  ~/proj  main  ")
    assert "tracking" in line or "on" in line or "off" in line or "read-only" in line
    # Wall time, because that is what Kimi's 300 ms kill counts -- but the best
    # of up to three renders: the footer takes ~0.03 s, and one render on a
    # loaded 2-vCPU agent-ci runner read 0.28, 0.35 and 0.47 s. A footer that
    # is really slow (importing our package alone is ~0.3 s) is slow every time.
    tries = [took]
    while tries[-1] >= 0.25 and len(tries) < 3:
        tries.append(_run_footer(kimi, kimi / "home")[1])
    seen = ", ".join(f"{t:.3f}s" for t in tries)
    assert min(tries) < 0.25, f"{seen}: Kimi kills the command at 300 ms"


def test_a_researchers_own_command_keeps_its_line_and_comes_back_on_uninstall(kimi):
    (kimi / "kimi" / "tui.toml").write_text('[status_line]\ncommand = "echo mine; echo second"\n')
    statusline.install_kimi(PLUGIN, python=sys.executable)
    line, _ = _run_footer(kimi, kimi / "home")
    assert line.startswith("mine  ")
    statusline.install_kimi(PLUGIN, python=sys.executable)  # a re-install re-wraps, never nests
    assert statusline._kimi_command((kimi / "kimi" / "tui.toml").read_text()).count("echo mine") == 1

    result = statusline.uninstall_kimi()
    assert result["restored"] == "echo mine; echo second"
    assert statusline._kimi_command((kimi / "kimi" / "tui.toml").read_text()) == "echo mine; echo second"


def test_uninstall_without_a_previous_command_removes_only_ours(kimi):
    (kimi / "kimi" / "tui.toml").write_text('[status_line]\nitems = ["model"]\n')
    statusline.install_kimi(PLUGIN, python=sys.executable)
    statusline.uninstall_kimi()
    assert (kimi / "kimi" / "tui.toml").read_text() == '[status_line]\nitems = ["model"]\n'


def test_a_file_that_is_not_toml_is_left_alone(kimi):
    (kimi / "kimi" / "tui.toml").write_text("theme = [unclosed\n")
    with pytest.raises(ValueError):
        statusline.install_kimi(PLUGIN, python=sys.executable)
    assert (kimi / "kimi" / "tui.toml").read_text() == "theme = [unclosed\n"


def test_the_renderer_reads_kimis_session_id(kimi, monkeypatch):
    monkeypatch.setenv("KIMI_CODE_STATUS_LINE", "1")
    import importlib.util

    spec = importlib.util.spec_from_file_location("sl_kimi", PLUGIN / "hooks" / "statusline.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.resolve_session_id({"sessionId": f"session_{SID}"}) == SID
    monkeypatch.setenv("PROBE_SL_PREFIX", "theirs")
    assert module.kimi_line({"model": "m"}, "● on") == "theirs  ● on"


def test_the_wizard_picks_the_slot_from_the_registry(kimi, monkeypatch):
    calls = []
    monkeypatch.setattr(statusline, "install_kimi", lambda root, python=None: calls.append("kimi") or {})
    monkeypatch.setattr(statusline, "install", lambda root, python=None: calls.append("claude") or {})
    statusline.install_for("kimi_code", PLUGIN)
    statusline.install_for("claude_code", PLUGIN)
    assert calls == ["kimi", "claude"]
    with pytest.raises(ValueError):
        statusline.install_for("codex", PLUGIN)


def test_a_multi_line_command_is_wrapped_and_given_back_whole(kimi):
    tui = kimi / "kimi" / "tui.toml"
    tui.write_text('[status_line]\nitems = [\n  ["model"],\n]\ncommand = """\necho mine\n"""\ntheme = "x"\n')
    statusline.install_kimi(PLUGIN, python=sys.executable)
    text = tui.read_text()
    assert text.count("command =") == 1 and 'theme = "x"' in text and '["model"],' in text
    statusline.uninstall_kimi()
    assert statusline._kimi_command(tui.read_text()).strip() == "echo mine"
    assert 'theme = "x"' in tui.read_text()


def test_a_symlinked_footer_file_stays_a_link(kimi):
    real = kimi / "dotfiles" / "tui.toml"
    real.parent.mkdir()
    real.write_text('theme = "dark"\n')
    tui = kimi / "kimi" / "tui.toml"
    tui.symlink_to(real)
    statusline.install_kimi(PLUGIN, python=sys.executable)
    assert tui.is_symlink() and statusline.kimi_installed()
    assert "probe-research-statusline" in real.read_text()
    statusline.uninstall_kimi()
    assert tui.is_symlink() and real.read_text().strip() == 'theme = "dark"'


@pytest.mark.skipif(not hasattr(os, "geteuid") or os.geteuid() == 0, reason="root writes anywhere")
def test_a_link_into_a_folder_probe_cannot_write_is_left_a_link(kimi):
    """A home-manager link into the read-only Nix store: replacing it with a
    plain file would make the next `home-manager switch` refuse. The write
    fails and the link stays, as it always did."""
    store = kimi / "store"
    store.mkdir()
    (store / "tui.toml").write_text('theme = "dark"\n')
    store.chmod(0o555)
    tui = kimi / "kimi" / "tui.toml"
    tui.symlink_to(store / "tui.toml")
    try:
        with pytest.raises(OSError):
            statusline.install_kimi(PLUGIN, python=sys.executable)
        assert tui.is_symlink()
    finally:
        store.chmod(0o755)


def test_uninstall_refuses_a_layout_it_cannot_edit(kimi, monkeypatch):
    tui = kimi / "kimi" / "tui.toml"
    statusline.install_kimi(PLUGIN, python=sys.executable)
    before = tui.read_text()
    monkeypatch.setattr(statusline, "_with_kimi_command", lambda text, command: text)  # an edit that misses
    with pytest.raises(ValueError, match="left as it is"):
        statusline.uninstall_kimi()
    assert tui.read_text() == before


def test_the_session_start_refresh_counts_kimis_footer(kimi):
    """Kimi-only machines have no Claude renderer folder; the marker refresh
    must still run for them or the footer never sees a fresh state."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("statusline_refresh", PLUGIN / "hooks" / "statusline_refresh.py")
    refresh = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(refresh)
    assert refresh.installed() is False
    statusline.install_kimi(PLUGIN, python=sys.executable)
    assert refresh.installed() is True
    (statusline.kimi_install_dir() / "statusline.py").write_text("# stale")
    refresh.sync_renderer()
    assert (statusline.kimi_install_dir() / "statusline.py").read_bytes() == (PLUGIN / "hooks" / "statusline.py").read_bytes()


# --- machines whose rules predate Kimi's footer (0.214.0) -------------------


@pytest.fixture()
def caught_up(kimi, monkeypatch):
    from probe.cli import setup as wizard

    monkeypatch.setattr(statusline, "discover_plugin_root", lambda source=None: PLUGIN)
    return wizard


def test_an_existing_kimi_machine_gets_the_footer_once(caught_up):
    """The footer is written only by the rules step, which a machine with
    current rules never runs again: 0.214.0 reached no existing Kimi machine."""
    wizard = caught_up
    assert statusline.catch_up_owed("kimi_code")
    lines = wizard.catch_up_statusline("kimi_code")
    assert statusline.installed_for("kimi_code"), lines
    assert lines and lines[0].startswith("Kimi Code status line: on")
    assert not statusline.catch_up_owed("kimi_code")

    statusline.uninstall_kimi()  # the researcher takes it out again
    assert wizard.catch_up_statusline("kimi_code") == []
    assert not statusline.installed_for("kimi_code")


def test_claude_code_is_never_caught_up(caught_up):
    """Its status line has ridden with the rules since it shipped: a missing one
    was removed on purpose."""
    assert not statusline.catch_up_owed("claude_code")
    assert caught_up.catch_up_statusline("claude_code") == []


def test_no_plugin_on_disk_tries_again_next_time(caught_up, monkeypatch):
    monkeypatch.setattr(statusline, "discover_plugin_root", lambda source=None: None)
    assert caught_up.catch_up_statusline("kimi_code") == []
    assert statusline.catch_up_owed("kimi_code")


def test_install_names_the_agent_from_any_shell(kimi, monkeypatch, capsys):
    """From a terminal (or a Kimi shell whose session lookup failed), the
    detected agent is not Kimi: `--agent kimi_code` still writes Kimi's footer."""
    import importlib

    cli_main = importlib.import_module("probe.cli.main")
    monkeypatch.setattr(statusline, "discover_plugin_root", lambda source=None: PLUGIN)
    monkeypatch.setattr(cli_main.agent_session, "detect_agent", lambda *a, **k: None)
    cli_main.statusline_install(plugin_root=None, agent="kimi_code")
    assert statusline.kimi_installed()
    assert json.loads(capsys.readouterr().out)["settings"].endswith("tui.toml")


def test_configure_plans_the_catch_up_so_it_is_not_nothing_to_change(caught_up):
    """`plan()` empty means "Nothing to change" and the run returns before any
    step: the catch-up must be a planned step of its own (as a stale block is)."""
    from probe.cli.capabilities import Capabilities

    wizard = caught_up
    caps = Capabilities(agent_source="kimi_code", tracking_plugin_installed=True,
                        agent_rules_installed=True, logged_in_as="a@b.c")
    have = caps.enabled()  # every other capability as it already is
    selection = wizard.Selection(tracking=have[wizard.Capability.TRACKING], capture=have[wizard.Capability.CAPTURE],
                                 auto_update=caps.auto_update_enabled, agent_rules=True)
    assert any("status line" in step for step in wizard.plan(caps, selection))
    statusline.install_kimi(PLUGIN, python=sys.executable)
    assert not any("status line" in step for step in wizard.plan(caps, selection))


def test_a_footer_from_the_rules_step_then_removed_never_comes_back(caught_up):
    statusline.install_kimi(PLUGIN, python=sys.executable)  # what the rules step does
    statusline.uninstall_kimi()
    assert not statusline.catch_up_owed("kimi_code")
    assert caught_up.catch_up_statusline("kimi_code") == []


@pytest.mark.parametrize("named", ["kimi", "KIMI_CODE", "kimi_code"])
def test_install_takes_any_spelling_of_the_agent(kimi, monkeypatch, capsys, named):
    import importlib

    cli_main = importlib.import_module("probe.cli.main")
    monkeypatch.setattr(statusline, "discover_plugin_root", lambda source=None: PLUGIN)
    cli_main.statusline_install(plugin_root=None, agent=named)
    assert statusline.kimi_installed()


@pytest.mark.parametrize("named", ["codex", "pi", "nonsense"])
def test_install_refuses_an_agent_without_a_status_line(kimi, monkeypatch, named):
    import importlib

    import typer

    cli_main = importlib.import_module("probe.cli.main")
    monkeypatch.setattr(statusline, "discover_plugin_root", lambda source=None: PLUGIN)
    with pytest.raises(typer.Exit):
        cli_main.statusline_install(plugin_root=None, agent=named)
    assert not statusline.kimi_installed()
    assert not statusline.status()["installed"]


def test_before_the_first_message_the_footer_shows_the_new_sessions_state(kimi, tmp_path):
    """Kimi creates its session on the first message, so the footer's first
    renders carry `sessionId: ""`. The renderer fell back to `_hook_harness`,
    which the footer's copy (RENDERER_FILES only) does not carry: it raised, and
    the line showed no Probe at all until the first message (2026-10-06)."""
    copy = tmp_path / "renderer"
    copy.mkdir()
    for name in statusline.RENDERER_FILES:
        shutil.copy(PLUGIN / "hooks" / name, copy / name)
    snapshot = json.dumps({"model": "m", "cwd": str(kimi / "home"), "sessionId": "", "version": "2.1.1"})
    done = subprocess.run(
        [sys.executable, str(copy / "statusline.py")], input=snapshot, capture_output=True, text=True,
        env={**os.environ, "KIMI_CODE_STATUS_LINE": "1", "NO_COLOR": "1"}, check=False,
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip().endswith(("tracking", "off", "on", ")")) and "● " in done.stdout, done.stdout


@pytest.mark.parametrize(("key_held", "degraded"), [(True, False), (False, True)])
def test_before_the_first_message_a_daemon_session_reads_as_starting(kimi, tmp_path, key_held, degraded):
    """Issue 3619: Kimi's footer drew `on (daemon degraded)` until the first
    message (no `sessionId` yet), though the daemon starts with the session.
    It is starting when it can start at all (the daemon's key is held), as the
    footer says once the session exists."""
    config = json.loads((kimi / "probe" / "config.json").read_text())
    config["defaults"] = {"session_state": "full", "recorders": {"kimi_code": "daemon"}}  # harness-literal-ok: the recorder table's key
    if key_held:
        config["contexts"]["default"]["companion_token"] = "daemon-key"
    (kimi / "probe" / "config.json").write_text(json.dumps(config))
    snapshot = json.dumps({"model": "m", "cwd": str(kimi / "home"), "sessionId": "", "version": "2.1.1"})
    done = subprocess.run(
        [sys.executable, str(PLUGIN / "hooks" / "statusline.py")], input=snapshot, capture_output=True, text=True,
        env={**os.environ, "KIMI_CODE_STATUS_LINE": "1", "NO_COLOR": "1"}, check=False,
    )
    assert done.returncode == 0, done.stderr
    assert "on (daemon" in done.stdout, done.stdout
    assert ("degraded" in done.stdout) is degraded, done.stdout
