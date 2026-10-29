"""After an update, the Probe service moves what open sessions read to the installed copy (plan C9).

`probe.service.followup` (the status-line renderer, the contexts the managed
block is refreshed in) and `recorders.installed_tap` (the tap a session's agent
has installed now). The cycle that runs them is in tests/test_service_updater.py
(`test_after_an_update_open_sessions_read_the_installed_copy`).
"""

from __future__ import annotations

import importlib.util
import json
import os
import threading
from pathlib import Path

import pytest

from probe.cli import statusline as cli_statusline
from probe.service import followup, recorders

AGENT = Path(__file__).resolve().parents[1]
MARKET = "research-os-agent"


def _hook_module():
    path = AGENT / "plugins" / "probe-research" / "hooks" / "statusline_refresh.py"
    spec = importlib.util.spec_from_file_location("_followup_statusline_refresh", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_renderer_files_are_the_installers_and_the_hooks():
    assert followup.RENDERER_FILES == cli_statusline.RENDERER_FILES == _hook_module().RENDERER_FILES
    assert followup.RENDERER_DIRNAME == cli_statusline.install_dir().name


def _plugin(home: Path, name: str, version: str, mark: str) -> Path:
    root = home / ".claude" / "plugins" / "cache" / MARKET / name / version
    (root / "hooks").mkdir(parents=True)
    for file in followup.RENDERER_FILES:
        (root / "hooks" / file).write_text(f"# {file} {mark}\n")
    return root


def _ledger(home: Path, plugins: dict) -> None:
    path = home / ".claude" / "plugins" / "installed_plugins.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"version": 2, "plugins": {
        key: [{"scope": "user", "installPath": str(p)} for p in paths] for key, paths in plugins.items()}}))


@pytest.mark.parametrize("case", ["installed", "several-copies", "no-ledger", "not-installed-here"])
def test_the_renderer_comes_from_the_copy_the_ledger_names_only(tmp_path, case):
    home = tmp_path / "home"
    old, new = _plugin(home, "probe-research", "0.170.0", "old"), _plugin(home, "probe-research", "0.171.0", "new")
    target = home / ".claude" / followup.RENDERER_DIRNAME
    if case != "not-installed-here":
        target.mkdir(parents=True)
        (target / "statusline.py").write_text("# before\n")
    if case == "installed":
        _ledger(home, {f"probe-research@{MARKET}": [new]})
    elif case == "several-copies":
        _ledger(home, {f"probe-research@{MARKET}": [old, new]})
    env = {"HOME": str(home)}
    changed = followup.sync_renderer(env)
    if case in ("installed", "several-copies"):
        # Several copies under one key: the user-scope one, else the newest
        # (`test_two_installs_still_refresh_the_renderer`).
        assert sorted(changed) == sorted(followup.RENDERER_FILES)
        assert (target / "statusline.py").read_text() == "# statusline.py new\n"
        assert followup.sync_renderer(env) == [], "content-compared: nothing to copy twice"
    else:
        assert changed == []
        if case != "not-installed-here":
            assert (target / "statusline.py").read_text() == "# before\n"
        else:
            assert not target.exists(), "a status line nobody installed is never installed"


def test_the_daemon_profiles_plugin_carries_the_renderer_too(tmp_path):
    home = tmp_path / "home"
    lean = _plugin(home, "probe-research-daemon", "0.171.0", "lean")
    (home / ".claude" / followup.RENDERER_DIRNAME).mkdir(parents=True)
    _ledger(home, {f"probe-research-daemon@{MARKET}": [lean]})
    assert followup.installed_renderer_root({"HOME": str(home)}) == lean.resolve()


def test_a_context_is_where_files_live_never_a_credential_or_one_sessions_switch():
    envs = [
        {"HOME": "/h", "XDG_STATE_HOME": "/h/s", "CLAUDE_CONFIG_DIR": "/h/c", "PROBE_TOKEN": "x",
         "PROBE_BASE_URL": "http://127.0.0.1:1", "PROBE_SESSION_STATE": "off",
         "HTTPS_PROXY": "http://user:secret@proxy:8080", "HTTP_PROXY": "http://proxy:8080"},
        {"XDG_STATE_HOME": "/h/s", "CLAUDE_CONFIG_DIR": "/h/c", "HTTP_PROXY": "http://proxy:8080"},  # the same one
        None,
    ]
    assert followup.contexts(envs) == [{}, {"XDG_STATE_HOME": "/h/s", "CLAUDE_CONFIG_DIR": "/h/c",
                                            "HTTP_PROXY": "http://proxy:8080"}]
    many = [{"XDG_STATE_HOME": f"/s{i}"} for i in range(10)]
    assert len(followup.contexts(many)) == followup.MAX_CONTEXTS


def _tap(root: Path) -> Path:
    (root / "tap").mkdir(parents=True)
    (root / "tap" / "hosted.py").write_text("")
    (root / "tap" / "main.py").write_text("")
    return root


def _session(root: Path, **env) -> dict:
    return {"sid": "s", "tap_root": str(root), "tap_version": root.name, "env": env}


def test_the_installed_tap_is_the_one_claude_codes_ledger_names(tmp_path):
    home = tmp_path / "home"
    cache = home / ".claude" / "plugins" / "cache" / MARKET / "probe-research-tap"
    old, new = _tap(cache / "0.10.0"), _tap(cache / "0.10.1")
    _tap(cache / "0.10.9")  # an orphaned newer folder the ledger does not name
    _ledger(home, {f"probe-research-tap@{MARKET}": [new]})
    assert recorders.installed_tap(_session(old, HOME=str(home))) == (str(new.resolve()), "0.10.1")
    _ledger(home, {f"probe-research-tap@{MARKET}": [old]})  # rolled back: followed too
    assert recorders.installed_tap(_session(new, HOME=str(home))) == (str(old.resolve()), "0.10.0")
    _ledger(home, {f"probe-research-tap@{MARKET}": [old, new]})
    assert recorders.installed_tap(_session(old, HOME=str(home))) is None, "several copies: none is the installed one"


def _settle(root: Path, seconds: float = 60) -> Path:
    """Date a tap folder (and its `tap/`, `hooks/`) `seconds` back: one Codex
    finished writing (`recorders._settled`)."""
    import os
    import time

    when = time.time() - seconds
    for part in (root, root / "tap", root / "hooks"):
        if part.exists():
            os.utime(part, (when, when))
    return root


def test_the_installed_tap_under_codex_is_the_newest_version_folder_of_its_cache(tmp_path):
    codex = tmp_path / "codex"
    cache = codex / "plugins" / "cache" / MARKET / "probe-research-tap"
    old, new = _settle(_tap(cache / "0.10.0")), _settle(_tap(cache / "0.10.12"))
    (cache / "0.10.13").mkdir()  # being written: no tap in it yet
    assert recorders.installed_tap(_session(old, CODEX_HOME=str(codex))) == (str(new.resolve()), "0.10.12")
    # A folder outside the agent's own caches (a checkout): nothing to follow.
    checkout = _tap(tmp_path / "src" / "probe-research-tap" / "0.10.0")
    assert recorders.installed_tap(_session(checkout, CODEX_HOME=str(codex), HOME=str(tmp_path))) is None


def test_the_installed_tap_under_kimi_is_the_one_its_plugin_list_records(tmp_path):
    """Kimi parity K2: Kimi keeps one folder per version (`managed/probe-research-tap@<v>`)
    and records the one it loads next in `installed.json`; the service follows that
    record, as it follows Claude Code's ledger (rollbacks too)."""
    import json

    plugins = tmp_path / "home" / ".kimi-code" / "plugins"
    managed = plugins / "managed"
    old, new = _tap(managed / "probe-research-tap@0.10.12"), _tap(managed / "probe-research-tap@0.10.20")
    listed = plugins / "installed.json"

    def record(root):
        listed.write_text(json.dumps({"plugins": [{"id": "probe-research", "root": str(managed / "probe-research@1")},
                                                 {"id": "probe-research-tap", "root": str(root)}]}))

    record(new)
    assert recorders.installed_tap(_session(old)) == (str(new.resolve()), "0.10.20")
    record(old)  # rolled back: followed too
    assert recorders.installed_tap(_session(new)) == (str(old.resolve()), "0.10.12")
    listed.write_text("not json")
    assert recorders.installed_tap(_session(old)) is None
    record(tmp_path / "elsewhere" / "probe-research-tap@0.10.30")  # not beside it: never followed
    assert recorders.installed_tap(_session(old)) is None
    half = managed / "probe-research-tap@0.10.31"
    half.mkdir()  # recorded but holding no tap yet
    record(half)
    assert recorders.installed_tap(_session(old)) is None


@pytest.mark.parametrize("fresh", ["", "tap", "hooks"])
def test_a_codex_folder_still_being_written_is_not_the_installed_tap_yet(tmp_path, fresh):
    """Codex picks by listing, so its newest folder may be one it is still
    copying: a folder (or its `tap/`, `hooks/`) written in the last SETTLE_S
    is skipped, and said, so the follow-up asks again once it settles."""
    import os
    import time

    codex = tmp_path / "codex"
    cache = codex / "plugins" / "cache" / MARKET / "probe-research-tap"
    old = _settle(_tap(cache / "0.10.0"))
    new = _tap(cache / "0.10.12")
    (new / "hooks").mkdir()
    _settle(new)
    os.utime(new / fresh if fresh else new, (time.time(), time.time()))
    unsettled: list = []
    assert recorders.installed_tap(_session(old, CODEX_HOME=str(codex)), unsettled) == (str(old.resolve()), "0.10.0")
    assert unsettled == [str(new.resolve())]
    _settle(new)
    assert recorders.installed_tap(_session(old, CODEX_HOME=str(codex))) == (str(new.resolve()), "0.10.12")


def test_the_follow_up_asks_again_about_a_folder_still_being_written(tmp_path, monkeypatch):
    """`follow_installed` says so (`settling`) when a newer folder is still
    being written, and the service's follow-up asks again once it would have
    settled, at most FOLLOW_TAP_TRIES times; a folder that settles is
    followed (a restart onto it)."""
    from types import SimpleNamespace

    from probe.service import server

    codex = tmp_path / "codex"
    cache = codex / "plugins" / "cache" / MARKET / "probe-research-tap"
    old = _settle(_tap(cache / "0.10.0"))
    new = _tap(cache / "0.10.12")
    host = recorders.RecorderHost(log=lambda line: None, loop_getter=lambda: None)
    monkeypatch.setattr(host, "_save", lambda: None)
    host.hosted, host.tap_version = object(), "0.10.0"
    thread = SimpleNamespace(is_alive=lambda: True)
    host.recordings["s"] = SimpleNamespace(thread=thread, controls=SimpleNamespace(stop=SimpleNamespace(is_set=lambda: False)),
                                           params=_session(old, CODEX_HOME=str(codex)))
    assert host.follow_installed() is None and host.settling is True
    later, restarts = [], []
    fake = SimpleNamespace(stop_reason=None, recorders=host, _restart_for_update=restarts.append,
                           _loop=SimpleNamespace(call_later=lambda delay, fn, *args: later.append((delay, args))))
    fake._follow_tap = lambda *args: None  # what call_later is handed
    server.Service._follow_tap(fake)
    assert later == [(server.TAP_SETTLE_S + 1.0, (server.FOLLOW_TAP_TRIES - 1,))] and not restarts
    server.Service._follow_tap(fake, 1)
    assert len(later) == 1, "no more tries left"
    _settle(new)
    server.Service._follow_tap(fake, 2)
    assert restarts and host.wanted == (str(new.resolve()), "0.10.12") and host.settling is False


def _scoped_ledger(home: Path, key: str, entries: list[tuple[str, Path]]) -> None:
    path = home / ".claude" / "plugins" / "installed_plugins.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"version": 2, "plugins": {key: [
        {"scope": scope, "installPath": str(p), **({"projectPath": "/repo"} if scope != "user" else {})}
        for scope, p in entries]}}))


@pytest.mark.parametrize("case", ["user-and-project", "two-projects", "user-only"])
def test_two_installs_still_refresh_the_renderer(tmp_path, case):
    """A key listing a user-scope and a project-scope install (at different
    versions) was skipped as ambiguous, and the hook's copies each read
    "another copy is installed": nobody refreshed the renderer. The user-scope
    entry is the renderer's, else the newest; the hook picks the same copy."""
    home = tmp_path / "home"
    older = _plugin(home, "probe-research", "0.171.0", "older")
    newer = _plugin(home, "probe-research", "0.172.0", "newer")
    key = f"probe-research@{MARKET}"
    entries = {
        "user-and-project": [("project", newer), ("user", older)],
        "two-projects": [("project", older), ("local", newer)],
        "user-only": [("user", newer)],
    }[case]
    _scoped_ledger(home, key, entries)
    wanted = {"user-and-project": older, "two-projects": newer, "user-only": newer}[case].resolve()
    target = home / ".claude" / followup.RENDERER_DIRNAME
    target.mkdir(parents=True)
    env = {"HOME": str(home)}
    assert followup.installed_renderer_root(env) == wanted
    assert followup.sync_renderer(env)
    mark = "older" if wanted == older.resolve() else "newer"
    assert (target / "statusline.py").read_text() == f"# statusline.py {mark}\n"
    hook = _hook_module()
    ledger = json.loads((home / ".claude" / "plugins" / "installed_plugins.json").read_text())
    assert Path(hook.renderer_copy(ledger["plugins"][key])) == wanted


# -- an install from before `refreshInterval` --------------------------------


def test_the_follow_ups_refresh_interval_marker_and_chain_are_the_installers():
    assert followup.REFRESH_INTERVAL_S == cli_statusline.REFRESH_INTERVAL_S
    assert followup.STATUSLINE_MARKER == cli_statusline.MARKER
    assert followup.CHAIN_OPEN == cli_statusline._OPEN


def _settings_file(home: Path, slot: object, **rest) -> Path:
    path = home / ".claude" / "settings.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"statusLine": slot, **rest}, indent=4))
    return path


def _ours() -> str:
    return f"_probe_sl_input=$(cat)\nprintf '%s' \"$_probe_sl_input\" | 'py' 'sl.py' {cli_statusline.MARKER}"


def _ensure(home: Path, tmp_path: Path, **env) -> bool:
    return followup.ensure_refresh_interval({"HOME": str(home), **env}, seen_dir=tmp_path / "seen")


def test_an_older_probe_status_line_is_given_its_refresh_interval_once(tmp_path):
    home = tmp_path / "home"
    path = _settings_file(home, {"type": "command", "command": _ours()}, model="opus", env={"K": "v"}, note="café")
    path.chmod(0o600)
    before = path.read_text()
    assert _ensure(home, tmp_path) is True
    data = json.loads(path.read_text())
    assert data == {"statusLine": {"type": "command", "command": _ours(),
                                   "refreshInterval": cli_statusline.REFRESH_INTERVAL_S},
                    "model": "opus", "env": {"K": "v"}, "note": "café"}
    assert "café" in path.read_text(), "nothing else is rewritten as escapes"
    assert path.stat().st_mode & 0o777 == 0o600, "a settings file kept private stays private"
    assert (path.parent / "settings.json.probe-backup").read_text() == before, "the pre-edit file is kept"
    # Removed by the person afterwards: never put back.
    data["statusLine"].pop("refreshInterval")
    path.write_text(json.dumps(data))
    assert _ensure(home, tmp_path) is False
    assert "refreshInterval" not in json.loads(path.read_text())["statusLine"]
    assert sorted(p.name for p in path.parent.iterdir()) == ["settings.json", "settings.json.probe-backup"]


@pytest.mark.parametrize("case", ["someone-elses", "chained", "own-interval", "no-slot", "not-json",
                                  "not-an-object", "missing"])
def test_the_refresh_interval_follow_up_leaves_everything_else_alone(tmp_path, case):
    home = tmp_path / "home"
    path = home / ".claude" / "settings.json"
    if case == "someone-elses":
        _settings_file(home, {"type": "command", "command": "my-prompt"})
    elif case == "chained":  # over another status line: it would re-run that one unasked
        _settings_file(home, {"type": "command", "command": cli_statusline.chain("my-prompt", "x " + cli_statusline.MARKER)})
    elif case == "own-interval":
        _settings_file(home, {"type": "command", "command": _ours(), "refreshInterval": 2})
    elif case == "no-slot":
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps({"model": "opus"}))
    elif case == "not-json":
        path.parent.mkdir(parents=True)
        path.write_text('{"statusLine": {"command": "' + cli_statusline.MARKER + '"')
    elif case == "not-an-object":
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps([cli_statusline.MARKER]))
    before = path.read_bytes() if path.exists() else None
    assert _ensure(home, tmp_path) is False
    assert (path.read_bytes() if path.exists() else None) == before
    assert not (path.parent / "settings.json.probe-backup").exists()


def test_the_refresh_interval_follow_up_never_waits_on_a_settings_link_to_a_fifo(tmp_path):
    home = tmp_path / "home"
    (home / ".claude").mkdir(parents=True)
    fifo = tmp_path / "pipe"
    os.mkfifo(fifo)
    (home / ".claude" / "settings.json").symlink_to(fifo)
    assert _ensure(home, tmp_path) is False


def test_the_refresh_interval_follow_up_writes_through_a_symlink_and_honours_claude_config_dir(tmp_path):
    dotfiles = tmp_path / "dotfiles" / "settings.json"
    dotfiles.parent.mkdir()
    dotfiles.write_text(json.dumps({"statusLine": {"type": "command", "command": _ours()}}))
    config = tmp_path / "cc"
    config.mkdir()
    (config / "settings.json").symlink_to(dotfiles)
    assert _ensure(tmp_path / "home", tmp_path, CLAUDE_CONFIG_DIR=str(config))
    assert (config / "settings.json").is_symlink(), "a dotfiles link stays a link"
    assert json.loads(dotfiles.read_text())["statusLine"]["refreshInterval"] == cli_statusline.REFRESH_INTERVAL_S


def test_the_refresh_interval_follow_up_never_overwrites_a_change_made_meanwhile(tmp_path, monkeypatch):
    home = tmp_path / "home"
    path = _settings_file(home, {"type": "command", "command": _ours()})
    real = followup._read_settings
    reads = {"n": 0}

    def read(target):
        text = real(target)
        reads["n"] += 1
        return text + " " if reads["n"] == 2 else text  # Claude Code saved it between our read and our write

    monkeypatch.setattr(followup, "_read_settings", read)
    before = path.read_text()
    assert _ensure(home, tmp_path) is False
    assert path.read_text() == before
    assert sorted(p.name for p in path.parent.iterdir()) == ["settings.json", "settings.json.probe-backup"], \
        "no temp file left behind"


def test_the_update_follow_up_gives_older_status_lines_their_refresh_interval(tmp_path, monkeypatch):
    """`Service._follow_update` runs it for each context, once per config folder."""
    import asyncio
    from types import SimpleNamespace

    from probe.service import server

    seen: list = []
    monkeypatch.setattr(followup, "sync_renderer", lambda env: [])
    monkeypatch.setattr(followup, "ensure_refresh_interval", lambda env, *, seen_dir: seen.append(env) or True)
    monkeypatch.setattr(server.paths, "home", lambda: tmp_path / "home")
    monkeypatch.setattr(server.paths, "service_dir", lambda: tmp_path / "service")
    fake = SimpleNamespace(
        stop_reason=None, _warming=set(), _interval_folders=set(), _interval_lock=threading.Lock(),
        recorders=SimpleNamespace(contexts=lambda: [{"env": {"CLAUDE_CONFIG_DIR": "/cc"}, "harness": "claude_code"}]),
        notes=SimpleNamespace(request=lambda *a, **k: None),
    )
    fake._refresh_interval = lambda env: server.Service._refresh_interval(fake, env)

    async def scenario():
        server.Service._follow_update(fake, tap=False)
        await asyncio.gather(*list(fake._warming))
        server.Service._follow_update(fake, tap=False)
        await asyncio.gather(*list(fake._warming))

    asyncio.run(scenario())
    assert [env.get("CLAUDE_CONFIG_DIR") for env in seen] == [None, "/cc"], "each context once, never twice"
    assert all(env["HOME"] == str(tmp_path / "home") for env in seen)
