"""The status-line refresh hook: it must cost nothing to people who did not opt in.

The hook is wired into the SHARED `hooks/hooks.json`, which both the Claude Code
and the Codex flavours of the plugin load. So it runs for every plugin user on
SessionStart and on every matching PostToolUse — including under Codex, whose
status line is a picker over BUILT-IN ITEMS (`/statusline`, "Select which items
to display"; unknown items are ignored) and therefore can never render a segment
produced by a command.

That makes the install gate the load-bearing thing under test here: without it,
every one of those users pays three API calls per refresh for a segment that may
not exist and, under Codex, cannot.

Same contract as the telemetry hook: stdlib-only, fail-silent, exit 0 always.
Nothing here does network — the spawn is monkeypatched or the gate is shut.
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parent.parent
_HOOKS = _ROOT / "plugins" / "probe-research" / "hooks"
_REFRESH = _HOOKS / "statusline_refresh.py"


@pytest.fixture()
def hook(monkeypatch, tmp_path):
    """The hook module, with CLAUDE_CONFIG_DIR pointed at a temp dir."""
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "claude"))
    monkeypatch.delenv("PROBE_STATUSLINE", raising=False)
    spec = importlib.util.spec_from_file_location("statusline_refresh", _REFRESH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _install(hook) -> None:
    Path(hook.install_dir()).mkdir(parents=True, exist_ok=True)


def _run(hook, monkeypatch, payload: dict) -> list:
    """Drive the hook's stdin path, capturing what it would have spawned."""
    spawned: list = []
    monkeypatch.setattr(hook, "spawn", lambda session_id: spawned.append(session_id))
    monkeypatch.setattr("sys.stdin", __import__("io").StringIO(json.dumps(payload)))
    assert hook.main([]) == 0
    return spawned


SESSION = {"session_id": "32fae7ad-a401-43d0-bfef-ea032058769e", "hook_event_name": "SessionStart"}


# -- the gate ---------------------------------------------------------------


def test_does_nothing_when_the_status_line_was_never_installed(hook, monkeypatch) -> None:
    """THE DEFECT THIS GUARDS. An opt-in feature must cost nothing to everyone
    who did not opt in — and under Codex, where a command-produced segment can
    never render at all, the spend could never buy anything."""
    assert hook.installed() is False
    assert _run(hook, monkeypatch, SESSION) == []


def test_refreshes_once_installed(hook, monkeypatch) -> None:
    _install(hook)
    assert hook.installed() is True
    assert _run(hook, monkeypatch, SESSION) == [SESSION["session_id"]]


def test_the_detached_child_re_checks_the_gate(hook, monkeypatch) -> None:
    """It was spawned milliseconds ago; an uninstall in between should stop the
    request rather than let one last one through."""
    called: list = []
    monkeypatch.setattr(hook, "refresh", lambda session_id: called.append(session_id))
    assert hook.main(["fetch", SESSION["session_id"]]) == 0
    assert called == []  # not installed

    _install(hook)
    assert hook.main(["fetch", SESSION["session_id"]]) == 0
    assert called == [SESSION["session_id"]]


def test_the_killswitch_still_wins(hook, monkeypatch) -> None:
    _install(hook)
    monkeypatch.setenv("PROBE_STATUSLINE", "off")
    assert _run(hook, monkeypatch, SESSION) == []


# -- fail-silent ------------------------------------------------------------


@pytest.mark.parametrize(
    "payload", [{}, {"session_id": ""}, {"session_id": 7}, {"session_id": "short"}]
)
def test_a_payload_without_a_usable_session_is_a_no_op(hook, monkeypatch, payload) -> None:
    _install(hook)
    assert _run(hook, monkeypatch, payload) == []


@pytest.mark.parametrize("raw", ["", "not json", "[]", "null"])
def test_garbage_stdin_exits_zero_silently(hook, monkeypatch, raw) -> None:
    _install(hook)
    monkeypatch.setattr(hook, "spawn", lambda session_id: pytest.fail("should not spawn"))
    monkeypatch.setattr("sys.stdin", __import__("io").StringIO(raw))
    assert hook.main([]) == 0


def test_the_hook_prints_nothing_and_exits_zero_as_a_subprocess(tmp_path) -> None:
    """End to end under a real interpreter: a PostToolUse hook that printed could
    alter the session, and the gate is shut here so nothing reaches the network."""
    result = subprocess.run(
        [sys.executable, str(_REFRESH)],
        input=json.dumps(SESSION),
        capture_output=True,
        text=True,
        timeout=30,
        env={"PATH": "/usr/bin:/bin", "CLAUDE_CONFIG_DIR": str(tmp_path), "HOME": str(tmp_path)},
    )
    assert result.returncode == 0
    assert result.stdout == ""


# -- contract ---------------------------------------------------------------


def test_the_hook_is_wired_into_the_shared_hooks_file() -> None:
    """Both flavours load this file, which is why the gate has to exist."""
    hooks = json.loads((_HOOKS / "routes.json").read_text())["hooks"]
    wired = [
        entry["command"]
        for event in ("SessionStart", "PostToolUse")
        for group in hooks[event]
        for entry in group["hooks"]
    ]
    assert sum("statusline_refresh.py" in command for command in wired) == 2


def test_captured_agents_match_the_servers_list() -> None:
    """`AGENT_KEYS` builds the `<agent>_session_id` foreign-key lookups, and the
    server only records the agents it captures. Drift here means a silently
    missing liveness source."""
    spec = importlib.util.spec_from_file_location("statusline_refresh", _REFRESH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    from probe.sdk.agent_session import AGENTS

    assert set(mod.AGENT_KEYS) == {spec.label for spec in AGENTS if spec.captured}


# -- maintenance is not tracking ---------------------------------------------


def test_a_session_with_tracking_off_still_gets_its_renderer_refreshed(
    hook, monkeypatch, tmp_path
) -> None:
    """THE BUG THIS GUARDS, found by verifying a real plugin upgrade.

    Gating the renderer sync behind the tracking-off switch meant a session that
    turned tracking off never picked up a new renderer — so it could not learn to
    display `tracking off`, and showed a stale, wrong state forever. The session
    that opted out needs the refresh MORE than one that did not.
    """
    _install(hook)
    marker = hook._load("_session_marker")
    marker.set_tracking(SESSION["session_id"], False)

    synced: list = []
    monkeypatch.setattr(hook, "sync_renderer", lambda: synced.append(True))
    assert _run(hook, monkeypatch, SESSION) == [], "must not spend a request"
    assert synced == [True], "but must still refresh the renderer"


def test_tracking_off_still_stops_the_network(hook, monkeypatch) -> None:
    _install(hook)
    marker = hook._load("_session_marker")
    marker.set_tracking(SESSION["session_id"], False)
    assert _run(hook, monkeypatch, SESSION) == []




def _copy_of_this_plugin(cache: Path, version: str, marker: str) -> Path:
    """A version folder of this plugin in a Claude Code cache, its renderer marked."""
    root = cache / "research-os-agent" / "probe-research" / version
    shutil.copytree(_HOOKS, root / "hooks", ignore=shutil.ignore_patterns("__pycache__"))
    (root / "hooks" / "statusline.py").write_text((_HOOKS / "statusline.py").read_text() + f"\n# {marker}\n")
    return root


@pytest.mark.parametrize("ledger_names", ["new", "old", "none"])
def test_a_copy_the_install_ledger_does_not_name_never_writes_the_renderer(tmp_path, ledger_names) -> None:
    """The renderer copy in Claude Code's config folder is what every session's
    status line runs. A session left open on an older plugin copy that could
    not hand its SessionStart to the installed one (a `/clear`, a resume) wrote
    its OLD renderer over the installed one's (surface audit #7). A copy writes
    it only when the ledger names no other copy of this plugin."""
    claude = tmp_path / "claude"
    cache = claude / "plugins" / "cache"
    old = _copy_of_this_plugin(cache, "0.170.0", "OLD-RENDERER")
    new = _copy_of_this_plugin(cache, "0.171.0", "NEW-RENDERER")
    installed = {"new": new, "old": old}.get(ledger_names)
    if installed is not None:
        (claude / "plugins" / "installed_plugins.json").write_text(json.dumps({"version": 2, "plugins": {
            "probe-research@research-os-agent": [{"scope": "user", "installPath": str(installed)}]}}))
    target = claude / "probe-research-statusline"
    target.mkdir(parents=True)
    (target / "statusline.py").write_text("# the renderer before\n")
    env = {"PATH": "/usr/bin:/bin", "CLAUDE_CONFIG_DIR": str(claude), "HOME": str(tmp_path),
           "PROBE_STATUSLINE": "", "XDG_STATE_HOME": str(tmp_path / "state")}
    for root in (old,):
        done = subprocess.run([sys.executable, str(root / "hooks" / "statusline_refresh.py")],
                              input=json.dumps(SESSION), capture_output=True, text=True, timeout=30, env=env)
        assert done.returncode == 0 and done.stdout == "", done.stderr
    written = (target / "statusline.py").read_text()
    if ledger_names == "new":
        assert written == "# the renderer before\n", "the old copy rolled the renderer back"
    else:
        # The ledger names this copy, or no copy at all (a checkout, no ledger): as before.
        assert "OLD-RENDERER" in written


def test_two_installs_still_refresh_the_renderer(tmp_path) -> None:
    """Claude Code's ledger can list one plugin key twice: a user-scope install
    and a project-scope one at another version. Every copy then read "another
    copy is installed" and nobody refreshed the renderer any more (every
    SessionStart did before). The user-scope copy is the renderer's (the
    service's `followup.installed_renderer_root` picks the same one): it writes,
    the project's older copy does not roll it back."""
    claude = tmp_path / "claude"
    cache = claude / "plugins" / "cache"
    project = _copy_of_this_plugin(cache, "0.171.0", "PROJECT-RENDERER")
    user = _copy_of_this_plugin(cache, "0.172.0", "USER-RENDERER")
    (claude / "plugins" / "installed_plugins.json").write_text(json.dumps({"version": 2, "plugins": {
        "probe-research@research-os-agent": [
            {"scope": "user", "installPath": str(user)},
            {"scope": "project", "projectPath": str(tmp_path / "repo"), "installPath": str(project)},
        ]}}))
    target = claude / "probe-research-statusline"
    target.mkdir(parents=True)
    (target / "statusline.py").write_text("# OLD RENDERER\n")
    env = {"PATH": "/usr/bin:/bin", "CLAUDE_CONFIG_DIR": str(claude), "HOME": str(tmp_path),
           "PROBE_STATUSLINE": "", "XDG_STATE_HOME": str(tmp_path / "state")}
    for root in (user, project):
        done = subprocess.run([sys.executable, str(root / "hooks" / "statusline_refresh.py")],
                              input=json.dumps(SESSION), capture_output=True, text=True, timeout=30, env=env)
        assert done.returncode == 0 and done.stdout == "", done.stderr
    written = (target / "statusline.py").read_text()
    assert "USER-RENDERER" in written, written[-200:]
