"""`probe uninstall` end to end in a sandbox HOME (clean-uninstall plan U-T1..U-T9, V-T1).

Every test here builds a Probe install the way the installers leave one -- a
uv tool env switched side by side, its shims, the service's and the SDK's
state, the config, Claude Code's and Codex's records -- under a throwaway
HOME, TMPDIR, UV_TOOL_DIR/UV_TOOL_BIN_DIR and agent homes, then uninstalls
it. Nothing here touches the real machine: the server is a fake, and the
process sweep only ever matches this sandbox's paths.

The clean-slate check is a filesystem diff against the snapshot taken before
the install: what may remain is exactly what was there (the researcher's
files, uv's own, the agents' own settings) plus `ALLOWED_AFTER`.
"""

from __future__ import annotations

import contextlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import pytest

from probe.cli import codex_hooks, uninstall, uninstall_plan
from probe.cli import uninstall_procs
from tests.reinstall_harness import reinstall_wheels, uv_machine  # noqa: F401 -- fixtures

#: The real approval: conftest stands one in for every test (`_no_real_codex_hook_approval`).
APPROVE = codex_hooks.approve

VERSION = "0.900.1"
BASE = "https://api.example.test"
DEVICE = "d" * 32
INSTALLATION = "11111111-2222-3333-4444-555555555555"


# -- the sandbox -------------------------------------------------------------------------


@pytest.fixture
def home(tmp_path, monkeypatch):
    home = tmp_path / "home"
    home.mkdir()
    for name, value in {
        "HOME": home,
        "XDG_CONFIG_HOME": home / ".config",
        "XDG_DATA_HOME": home / ".local" / "share",
        "XDG_CACHE_HOME": home / ".cache",
        "UV_TOOL_DIR": home / ".local" / "share" / "uv" / "tools",
        "UV_TOOL_BIN_DIR": home / ".local" / "bin",
        "TMPDIR": tmp_path / "tmp",
        # Probe's outbox, in this HOME's state folder: never the box's.
        "PROBE_OUTBOX_DIR": home / ".local" / "state" / "probe" / "outbox",
        "CODEX_HOME": home / ".codex",
        "PI_CODING_AGENT_DIR": home / ".pi" / "agent",
        "KIMI_CODE_HOME": home / ".kimi-code",
    }.items():
        monkeypatch.setenv(name, str(value))
    (tmp_path / "tmp").mkdir()
    for name in ("XDG_STATE_HOME", "CLAUDE_CONFIG_DIR", "PROBE_CONFIG_PATH", "PROBE_TOKEN",
                 "PROBE_INGEST_TOKEN", "PROBE_MCP_TOKEN", "PROBE_TRANSCRIPT_STATE_DIR", "PROBE_VERSION_CACHE",
                 "CLAUDE_CODE_SESSION_ID", "PI_SESSION_ID", "PROBE_KIMI_SESSION_ID"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("PROBE_TELEMETRY", "off")
    monkeypatch.setattr(tempfile, "tempdir", None)
    from probe.sdk import journal

    monkeypatch.setattr(journal, "_private_fallback", None)
    return home


def researcher_files(home: Path) -> None:
    """What was on the machine before Probe, and must be after it."""
    (home / "project").mkdir()
    (home / "project" / ".probe.config").write_text("exclude: secrets/\n")
    (home / ".probe.config").write_text("exclude: private/\n")
    (home / "project" / ".venv" / "lib").mkdir(parents=True)
    tools = Path(os.environ["UV_TOOL_DIR"])
    tools.mkdir(parents=True)
    (tools / ".lock").write_text("")
    (tools / ".gitignore").write_text("*")
    (tools / "ruff").mkdir()
    bins = Path(os.environ["UV_TOOL_BIN_DIR"])
    bins.mkdir(parents=True)
    (bins / "probe-foo").write_text("#!/bin/sh\necho someone else's\n")  # a probe* name that is not Probe's
    (bins / "ruff").symlink_to(tools / "ruff")
    claude = home / ".claude"
    (claude / "plugins").mkdir(parents=True)
    (claude / "plugins" / "installed_plugins.json").write_text(json.dumps(
        {"version": 2, "plugins": {"other@else": [{"scope": "user", "installPath": "/x"}]}}))
    (claude / "plugins" / "known_marketplaces.json").write_text(json.dumps({"else": {"source": "x"}}))
    (claude / "settings.json").write_text(json.dumps(
        {"model": "opus", "statusLine": {"type": "command", "command": "my-status"},
         "enabledPlugins": {"other@else": True}}, indent=2))
    (claude / "CLAUDE.md").write_text("# my own rules\n")
    (claude / "skills" / "mine").mkdir(parents=True)
    (claude / "skills" / "mine" / "SKILL.md").write_text("mine\n")
    codex = home / ".codex"
    codex.mkdir()
    (codex / "config.toml").write_text('model = "gpt-5"\n\n[mcp_servers.other]\nurl = "https://other"\n')


def install_probe(home: Path) -> dict:
    """A Probe install as the side-by-side installer and the wizard leave it."""
    from probe.cli import agent_rules, statusline
    from probe.sdk.config import save_context
    from probe.service import paths

    share = Path(os.environ["XDG_DATA_HOME"]) / "uv"
    tools = Path(os.environ["UV_TOOL_DIR"])
    bins = Path(os.environ["UV_TOOL_BIN_DIR"])
    versions = tools.parent / "probe-versions"
    tools.mkdir(parents=True, exist_ok=True)
    bins.mkdir(parents=True, exist_ok=True)
    envs = []
    for version in ("0.900.0", VERSION):
        env = versions / version / "probe-research"
        (env / "bin").mkdir(parents=True)
        (env / "bin" / "python").symlink_to(sys.executable)
        (env / "pyvenv.cfg").write_text(f"home = {Path(sys.executable).parent}\nversion_info = 3.12.0\n")
        for name in ("probe", "probe-research-mcp"):
            (env / "bin" / name).write_text("#!/bin/sh\n")
        (env / "uv-receipt.toml").write_text(
            '[tool]\nrequirements = [{ name = "probe-research" }]\nentrypoints = [\n'
            f'    {{ name = "probe", install-path = "{bins / "probe"}", from = "probe-research" }},\n'
            f'    {{ name = "probe-research-mcp", install-path = "{bins / "probe-research-mcp"}", '
            'from = "probe-research" },\n]\n')
        (versions / version / f".used-{paths.machine_key()}").write_text("")
        envs.append(env)
    (tools / "probe-research").symlink_to(envs[-1])
    (versions / "active.json").write_text(json.dumps(
        {"active": str(envs[-1]), "previous": str(envs[0]), "tools": str(tools), "bin": str(bins)}))
    for name in ("probe", "probe-research-mcp"):
        (bins / name).symlink_to(tools / "probe-research" / "bin" / name)
    state = paths.state_dir()
    service = paths.service_dir()
    service.mkdir(parents=True)
    (service / "sessions.json").write_text(json.dumps({"v": 1, "sessions": []}))
    (service / "service.log").write_text("log\n")
    (paths.root_dir() / "runtime.json").write_text(json.dumps({"python": str(envs[-1] / "bin" / "python")}))
    for name, text in (("autoupdate.json", "{}"), ("wizard.lock", ""), ("state.lock", "")):
        (state / name).write_text(text)
    (state / "device.json").write_text(json.dumps({"device_instance_id": DEVICE}))
    (state / "team-note").mkdir()
    (state / "team-note" / "probe-team-note.md").write_text("note\n")
    (state / "outbox").mkdir()
    (state / "lifeboat").mkdir()
    (state / "lifeboat" / "lifeboat.sh").write_text("#!/bin/sh\n")
    (state / "import-jobs").mkdir()
    telemetry = home / ".local" / "state" / "probe-telemetry"
    telemetry.mkdir(parents=True)
    (telemetry / "machine_id").write_text("abc\n")
    (telemetry / "identity.json").write_text("{}")
    (home / ".cache" / "probe").mkdir(parents=True)
    (home / ".cache" / "probe" / "version-check.json").write_text("{}")
    save_context({"base_url": BASE, "token": "probe_pat_api", "mcp_token": "probe_pat_mcp",
                  "companion_token": "probe_pat_daemon", "ingest_token": "ros_ing_ctx"})
    # Claude Code: plugins, marketplace, rules, skills, status line, capture tap.
    claude = home / ".claude"
    ledger = claude / "plugins" / "installed_plugins.json"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    data = json.loads(ledger.read_text()) if ledger.exists() else {"version": 2, "plugins": {}}
    for name in ("probe-research", "probe-research-tap"):
        data["plugins"][f"{name}@research-os-agent"] = [{"scope": "user", "installPath": str(
            claude / "plugins" / "cache" / "research-os-agent" / name / "1.0")}]
    ledger.write_text(json.dumps(data))
    known_path = claude / "plugins" / "known_marketplaces.json"
    known = json.loads(known_path.read_text()) if known_path.exists() else {}
    known["research-os-agent"] = {"source": {"repo": "prbe-ai/research-os-agent"}}
    (claude / "plugins" / "known_marketplaces.json").write_text(json.dumps(known))
    (claude / "plugins" / "marketplaces" / "research-os-agent").mkdir(parents=True)
    (claude / "plugins" / "cache" / "research-os-agent" / "probe-research" / "1.0").mkdir(parents=True)
    agent_rules.install(claude / "CLAUDE.md")
    (claude / "skills" / "probe").mkdir(parents=True)
    (claude / "skills" / "probe" / "SKILL.md").write_text("probe\n")
    (claude / "skills" / "probe" / ".probe-installed").write_text("probe-research\n")
    (claude / "skills" / ".probe-sync.lock").write_text("")
    settings_path = claude / "settings.json"
    settings = json.loads(settings_path.read_text()) if settings_path.exists() else {}
    if settings_path.exists():
        shutil.copy(settings_path, claude / "settings.json.probe-backup")
    previous = (settings.get("statusLine") or {}).get("command", "")
    settings["statusLine"] = {"type": "command",
                              "command": statusline.chain(previous, statusline.renderer_command("/usr/bin/python3"))}
    settings.setdefault("enabledPlugins", {})["probe-research@research-os-agent"] = True
    (claude / "settings.json").write_text(json.dumps(settings, indent=2))
    (claude / "probe-research-statusline").mkdir()
    tap = claude / "plugins" / "probe-research-tap"
    tap.mkdir()
    (tap / ".token").write_text("ros_ing_tap\n")
    (tap / ".config").write_text(json.dumps({"api_base_url": BASE}))
    (tap / "logs").mkdir()
    # Codex: its plugin, marketplace, MCP entry and hook approvals.
    codex = home / ".codex"
    codex.mkdir(exist_ok=True)
    with (codex / "config.toml").open("a") as handle:
        handle.write(
            '\n[plugins."probe-research@research-os-agent"]\nenabled = true\n'
            '\n[marketplaces.research-os-agent]\nsource = "github"\n'
            '\n[mcp_servers.probe-research]\nurl = "https://mcp.research.prbe.ai/mcp"\n'
            '\n[mcp_servers.probe-research.http_headers]\nAuthorization = "Bearer probe_pat_mcp"\n'
            '\n[hooks.state."probe-research@research-os-agent:hooks/hooks.json:SessionStart:0"]\ntrusted = "abc"\n')
    (codex / ".tmp" / "marketplaces" / "research-os-agent").mkdir(parents=True)
    agent_rules.install(codex / "AGENTS.md")
    return {"tools": tools, "bins": bins, "versions": versions, "envs": envs, "share": share}


def snapshot(home: Path) -> dict[str, str]:
    """{relative path: kind (+ content for small files)} of everything under HOME."""
    out = {}
    for root, dirs, files in os.walk(home):
        for name in dirs + files:
            path = Path(root) / name
            rel = str(path.relative_to(home))
            if path.is_symlink():
                out[rel] = f"link:{os.readlink(path)}"
            elif path.is_dir():
                out[rel] = "dir"
            else:
                out[rel] = "file"
    return out


class FakeServer:
    """The API, as it behaves: retiring this device revokes the keys bound to
    it only (a shared MCP key is detached instead), a released key is gone for
    good, and every call with a revoked key answers 401. The order of calls is
    recorded."""

    #: This device's own keys (released with it); the MCP key is shared.
    DEVICE_KEYS = ("probe_pat_api", "probe_pat_daemon")

    def __init__(self) -> None:
        self.calls: list[tuple] = []
        self.retired = False
        self.revoked: set[str] = set()
        self.lose_retire_answer = False
        self.down = False

    def client(self, base_url, token):
        server = self
        from probe.sdk import errors

        def authorized() -> None:
            if server.down:
                raise errors.TransportError("connection refused")
            if token in server.revoked:
                raise errors.AuthError("token revoked", status=401)

        class Client:
            def __enter__(self):
                return self

            def __exit__(self, *exc):
                return False

            def retire_client_installations(self, ids):
                server.calls.append(("retire", token, tuple(ids)))
                authorized()
                if server.retired:
                    raise errors.NotFoundError("no matching clients to retire", status=404)
                server.retired = True
                server.revoked.update(server.DEVICE_KEYS)
                if server.lose_retire_answer:
                    server.lose_retire_answer = False
                    raise errors.TransportError("connection reset")
                return {"retired": list(ids), "captures_revoked": 1}

            def logout(self):
                server.calls.append(("revoke", token))
                authorized()
                if token == "probe_pat_mcp":
                    return {"revoked": False, "detached": True, "still_used_by": ["laptop-2"]}
                server.revoked.add(token)
                return {"revoked": True, "detached": False}

        return Client()


@pytest.fixture
def server(monkeypatch):
    fake = FakeServer()
    monkeypatch.setattr(uninstall, "_client", fake.client)

    def ids(*, device_id=None):
        if fake.down:
            raise uninstall_plan.Offline(f"{BASE}: connection refused")
        return {"device_ids": [DEVICE], "installation_ids": [INSTALLATION],
                "contexts": {"default": {"base_url": BASE, "installation_ids": [INSTALLATION]}}}

    monkeypatch.setattr(uninstall_plan, "server_ids", ids)

    def revoke_capture(token, base_url, timeout=5.0):
        fake.calls.append(("capture", token))
        return None if fake.down else True

    monkeypatch.setattr("probe.cli.capabilities.revoke_capture_token", revoke_capture)
    return fake


@pytest.fixture
def no_exec(monkeypatch):
    """Run the finisher in this process instead of exec'ing it."""
    from probe._shared import finisher
    from probe.service import paths

    finished = {}

    def finish(run):
        monkeypatch.setenv(finisher.LOCK_FD_ENV, str(run.lock_fd))  # as the exec hands it over
        folder = paths.uninstall_dir()
        shutil.copyfile(finisher.__file__, folder / uninstall.FINISHER_NAME)
        finished["plan"] = json.loads(paths.uninstall_plan_path().read_text())
        finished["code"] = finisher.run(str(paths.uninstall_plan_path()))
        return finished["code"]

    monkeypatch.setattr(uninstall, "_phase_finishing", finish)
    return finished


#: What may be left after an uninstall that was not there before it: only the
#: standard folders (never removed, even when Probe made them), empty.
ALLOWED_AFTER: set[str] = {".cache", ".config", ".local", ".local/state", ".local/share", ".local/bin"}


class Killed(BaseException):
    """Stands for SIGKILL: nothing of the run's own handles it."""


def _clean_slate(before: dict, after: dict) -> None:
    added = {p: k for p, k in after.items() if p not in before}
    added = {p: k for p, k in added.items() if p not in ALLOWED_AFTER}
    assert not added, f"left behind: {sorted(added)}"
    missing = {p for p in before if p not in after}
    assert not missing, f"removed something that was not Probe's: {sorted(missing)}"


def _uninstall(**kwargs) -> int:
    from probe.core import events

    with events.session(False):
        return uninstall.run(uninstall.Options(yes=True, **kwargs))


# -- the whole run -------------------------------------------------------------------------


def test_uninstall_leaves_exactly_what_was_there_before(home, server, no_exec):
    researcher_files(home)
    before = snapshot(home)
    install_probe(home)
    assert _uninstall() == 0
    assert no_exec["code"] == 0
    _clean_slate(before, snapshot(home))
    # The agents' own files came back to what they were, byte for byte where
    # Probe's edit could be undone exactly.
    claude = home / ".claude"
    settings = json.loads((claude / "settings.json").read_text())
    assert settings["statusLine"]["command"] == "my-status" and settings["enabledPlugins"] == {"other@else": True}
    assert json.loads((claude / "plugins" / "installed_plugins.json").read_text())["plugins"].keys() == {"other@else"}
    assert (claude / "CLAUDE.md").read_text() == "# my own rules\n"
    codex = (home / ".codex" / "config.toml").read_text()
    assert "probe-research" not in codex and "research-os-agent" not in codex and "[mcp_servers.other]" in codex


def test_server_retires_first_then_revokes_every_key_and_reports_a_detached_one(home, server, no_exec, capsys):
    install_probe(home)
    assert _uninstall() == 0
    kinds = [call[0] for call in server.calls]
    assert kinds[0] == "retire" and server.calls[0][1] == "probe_pat_daemon"  # the DELETE-scope daemon key
    revoked = {call[1] for call in server.calls if call[0] == "revoke"}
    assert revoked == {"probe_pat_api", "probe_pat_mcp", "probe_pat_daemon"}
    captured = {call[1] for call in server.calls if call[0] == "capture"}
    assert captured == {"ros_ing_tap", "ros_ing_ctx"}
    out = capsys.readouterr().out
    assert "stays in use on 1 other device(s): laptop-2" in out


def test_shims_come_from_the_receipt_never_a_glob(home, server, no_exec):
    researcher_files(home)
    laid = install_probe(home)
    plan = uninstall_plan.compute(server=None)
    assert sorted(plan["shims"]) == [str(laid["bins"] / "probe"), str(laid["bins"] / "probe-research-mcp")]
    assert not any("probe-foo" in p["path"] for p in plan["paths"])
    assert not any(p["path"].endswith("/ruff") or p["path"].endswith("tools/.lock") for p in plan["paths"])


def test_a_custom_tool_and_bin_dir_are_followed(home, server, no_exec, monkeypatch, tmp_path):
    monkeypatch.setenv("UV_TOOL_DIR", str(tmp_path / "opt" / "uv-tools" / "tools"))
    monkeypatch.setenv("UV_TOOL_BIN_DIR", str(tmp_path / "opt" / "bin"))
    researcher_files(home)
    before_opt = snapshot(tmp_path / "opt")
    laid = install_probe(home)
    assert laid["tools"].parent == tmp_path / "opt" / "uv-tools"
    assert _uninstall() == 0
    assert snapshot(tmp_path / "opt") == before_opt


def test_json_events_end_with_the_finishers_done(home, server, tmp_path):
    """`probe uninstall --yes --json --offline` in a process of its own, the
    exec included: the last line is the finisher's `done`."""
    researcher_files(home)
    before = snapshot(home)
    install_probe(home)
    env = {k: v for k, v in os.environ.items() if not k.startswith("PYTEST")}
    done = subprocess.run([sys.executable, "-m", "probe.cli", "uninstall", "--yes", "--offline", "--json"],
                          capture_output=True, text=True, timeout=120, env=env, cwd=str(home))
    lines = [json.loads(line) for line in done.stdout.splitlines() if line.strip()]
    assert done.returncode == 0, done.stderr
    assert lines[-1]["event"] == "done" and lines[-1]["exit_code"] == 0
    names = [step["name"] for step in lines[-1]["steps"]]
    assert names[-1] == "uninstall_finish" and "uninstall_state" in names
    server_step = next(step for step in lines[-1]["steps"] if step["name"] == "uninstall_server")
    assert server_step["status"] == "skipped" and lines[-1]["complete"] is False  # offline: revoke by hand
    after = snapshot(home)
    _clean_slate(before, after)


# -- scope (U-T2) ----------------------------------------------------------------------------


def test_refuses_while_probe_is_in_use_and_force_goes_on(home, server, no_exec, monkeypatch, capsys):
    install_probe(home)
    users = [uninstall_procs.User(uninstall_procs.UserKind.SESSION, "claude_code session abc (pid 1234)")]
    monkeypatch.setattr(uninstall_procs, "live_users", lambda: users)
    assert _uninstall() == 2
    assert "session abc" in capsys.readouterr().err
    from probe.service import paths

    assert not paths.uninstall_dir().exists() and (home / ".local" / "share" / "uv" / "probe-versions").exists()
    assert _uninstall(force=True) == 0


def test_refuses_inside_a_recorded_session_even_with_force(home, server, no_exec, monkeypatch, capsys):
    """An agent must not uninstall Probe from under its own session: a person
    does, in a terminal of their own. --force is never the way round it."""
    install_probe(home)
    installed = snapshot(home)
    monkeypatch.setattr(uninstall_procs, "recorded_session_here", lambda: "sess-1")
    assert _uninstall() == 2
    err = capsys.readouterr().err
    assert "outside any agent session" in err and "--force" not in err
    assert _uninstall(force=True) == 2
    assert snapshot(home) == installed


def test_a_shared_home_keeps_the_other_machines_service_folder(home, server, no_exec, capsys):
    from probe.service import paths

    researcher_files(home)
    install_probe(home)
    other = paths.root_dir() / "0123456789abcdef"
    other.mkdir()
    (other / "service.log").write_text("busy\n")
    assert _uninstall() == 2  # used recently: another computer is a live user
    assert "another computer" in capsys.readouterr().err
    assert _uninstall(force=True) == 0
    assert (other / "service.log").exists()
    assert not paths.service_dir().exists()


# -- offline and unsent research (U-T5, U-T6) ---------------------------------------------------


def test_offline_refuses_before_anything_is_destroyed(home, server, no_exec, capsys):
    server.down = True
    before = snapshot(home)
    install_probe(home)
    installed = snapshot(home)
    assert _uninstall() == 2
    assert "cannot reach Probe's server" in capsys.readouterr().err
    assert snapshot(home) == installed
    assert before != installed


def test_offline_flag_removes_locally_and_names_the_dashboard(home, server, no_exec, capsys):
    researcher_files(home)
    before = snapshot(home)
    install_probe(home)
    server.down = True
    assert _uninstall(offline=True) == 0
    assert "example.test/settings" in capsys.readouterr().out
    assert not any(call[0] in ("retire", "revoke") for call in server.calls)
    _clean_slate(before, snapshot(home))


def _queue_one(home: Path) -> None:
    from probe.sdk.journal import Journal, default_root

    Journal(default_root()).append_http("POST", "/v1/runs", {"name": "r"})


def test_unsent_research_stops_a_yes_run(home, server, no_exec, monkeypatch, capsys):
    install_probe(home)
    _queue_one(home)
    monkeypatch.setattr(uninstall, "drain", lambda deadline, lines: None)  # the server takes nothing
    assert _uninstall() == 2
    err = capsys.readouterr().err
    assert "1 queued write(s)" in err and "--discard-unsent" in err
    from probe.service import paths

    assert not paths.uninstall_dir().exists()  # cancelled before the point of no return
    assert not any(call[0] == "revoke" for call in server.calls)
    assert _uninstall(discard_unsent=True) == 0


def test_unsent_research_can_be_saved_to_a_backup_file(home, server, no_exec, monkeypatch):
    install_probe(home)
    monkeypatch.setattr(uninstall, "_confirm", lambda run: None)  # the person said Remove
    _queue_one(home)
    monkeypatch.setattr(uninstall, "drain", lambda deadline, lines: None)
    monkeypatch.setattr(uninstall, "_ask_unsent", lambda unsent, **_: uninstall.UnsentChoice.BACKUP)
    from probe.core import events

    with events.session(False):
        code = uninstall.run(uninstall.Options(interactive=True))
    assert code == 0
    saved = list(home.glob("probe-unsent-*.tar.gz"))
    assert len(saved) == 1 and saved[0].stat().st_mode & 0o777 == 0o600
    import tarfile

    with tarfile.open(saved[0]) as archive:
        assert any("ops" in name for name in archive.getnames())


def test_the_interactive_cancel_changes_nothing(home, server, no_exec, monkeypatch):
    install_probe(home)
    monkeypatch.setattr(uninstall, "_confirm", lambda run: None)  # the person said Remove
    _queue_one(home)
    monkeypatch.setattr(uninstall, "drain", lambda deadline, lines: None)
    monkeypatch.setattr(uninstall, "_ask_unsent", lambda unsent, **_: uninstall.UnsentChoice.CANCEL)
    from probe.core import events

    with events.session(False):
        assert uninstall.run(uninstall.Options(interactive=True)) == 2
    from probe.service import paths

    assert not paths.uninstall_dir().exists()
    assert (Path(os.environ["UV_TOOL_DIR"]) / "probe-research").is_symlink()


# -- interruption (V-T1) ---------------------------------------------------------------------------


@pytest.mark.parametrize("phase", ["stopping", "draining", "server", "integrations", "state"])
def test_killed_in_any_phase_a_rerun_finishes(home, server, no_exec, monkeypatch, phase):
    """A kill inside a phase leaves the barrier at it; a rerun (the owner gone)
    finishes from there, or (before the point of no return) starts again."""
    from probe.service import paths

    researcher_files(home)
    before = snapshot(home)
    install_probe(home)
    target = f"_phase_{phase}"
    real = getattr(uninstall, target)

    def killed(run):
        raise Killed  # SIGKILL: no handler of ours runs

    monkeypatch.setitem(uninstall._PHASE_STEPS, uninstall.Phase(phase), killed)
    with pytest.raises(Killed):
        _uninstall()
    barrier = json.loads(paths.uninstall_barrier_path().read_text())
    assert barrier["phase"] == phase
    barrier["pid"] = 999999999  # the owner died with the kill
    paths.uninstall_barrier_path().write_text(json.dumps(barrier))
    monkeypatch.setitem(uninstall._PHASE_STEPS, uninstall.Phase(phase), real)
    assert _uninstall() == 0
    _clean_slate(before, snapshot(home))


def test_an_unreadable_barrier_is_finished_from_the_first_phase(home, server, no_exec, monkeypatch):
    """A barrier nothing can be read of (a disk error, a hand edit) is LIVE:
    the rerun takes it over and runs every phase again, which is safe."""
    from probe.service import paths

    researcher_files(home)
    before = snapshot(home)
    install_probe(home)

    def killed(run):
        raise Killed

    real = uninstall._PHASE_STEPS[uninstall.Phase.STATE]
    monkeypatch.setitem(uninstall._PHASE_STEPS, uninstall.Phase.STATE, killed)
    with pytest.raises(Killed):
        _uninstall()
    paths.uninstall_barrier_path().write_text("{not json")
    monkeypatch.setitem(uninstall._PHASE_STEPS, uninstall.Phase.STATE, real)
    assert _uninstall() == 0
    _clean_slate(before, snapshot(home))


def test_a_barrier_past_the_point_of_no_return_is_live_without_its_owner(home):
    from probe._shared import uninstall_barrier
    from probe.service import client, paths

    paths.private_dir(paths.uninstall_dir())
    paths.uninstall_barrier_path().write_text(json.dumps(
        {"v": 1, "pid": 999999999, "start": "1", "at": 0, "phase": "server", "plan": ""}))
    assert uninstall_barrier.live() and client.uninstall_barrier() is not None
    assert client.ensure() == client.Ensured.UNINSTALLING
    paths.uninstall_barrier_path().write_text(json.dumps(
        {"v": 1, "pid": 999999999, "start": "1", "at": 0, "phase": "draining", "plan": ""}))
    assert client.uninstall_barrier() is None  # stale: an install may clear it


def test_a_lost_retire_answer_is_finished_by_the_rerun(home, server, no_exec, capsys):
    """The server retired the device but the answer never came: the run stops
    (exit 1, resumable) without revoking that account's keys, so the rerun
    retires first again. Those keys were revoked with the device, so the
    rerun's retire is refused (401): that proves nothing, and it says where to
    check."""
    researcher_files(home)
    before = snapshot(home)
    install_probe(home)
    server.lose_retire_answer = True
    server.calls.clear()
    import probe.cli.uninstall as module

    original = module.SERVER_TRIES
    module.SERVER_TRIES = 1
    try:
        assert _uninstall() == 1
    finally:
        module.SERVER_TRIES = original
    assert not any(call[0] == "revoke" for call in server.calls)  # the account's revokes waited
    from probe.service import paths

    barrier = json.loads(paths.uninstall_barrier_path().read_text())
    assert barrier["phase"] == "server"
    barrier["pid"] = 999999999
    paths.uninstall_barrier_path().write_text(json.dumps(barrier))
    assert _uninstall() == 0
    retires = [call for call in server.calls if call[0] == "retire"]
    # The rerun retires first again; the keys the lost retire revoked answer
    # 401, which proves nothing: it names the dashboard.
    assert [call[1] for call in retires] == ["probe_pat_daemon", "probe_pat_daemon", "probe_pat_api"]
    assert "remove this computer under Settings > Connected clients" in capsys.readouterr().out
    _clean_slate(before, snapshot(home))


def test_killed_in_the_finisher_the_copy_finishes_by_hand(home, server, monkeypatch):
    from probe._shared import finisher
    from probe.service import paths

    researcher_files(home)
    before = snapshot(home)
    install_probe(home)

    def stop_before_finishing(run):
        shutil.copyfile(finisher.__file__, paths.uninstall_dir() / uninstall.FINISHER_NAME)
        raise Killed

    monkeypatch.setattr(uninstall, "_phase_finishing", stop_before_finishing)
    with pytest.raises(Killed):
        _uninstall()
    copy = paths.uninstall_dir() / uninstall.FINISHER_NAME
    done = subprocess.run(["python3", "-I", str(copy), "--plan", str(paths.uninstall_plan_path())],
                          capture_output=True, text=True, timeout=60, env={**os.environ, "HOME": str(home)})
    assert done.returncode == 0, done.stdout + done.stderr
    _clean_slate(before, snapshot(home))


def test_an_install_made_during_the_uninstall_is_kept(home, server, no_exec, monkeypatch):
    """Generation-bound: an env made again at a planned path after the plan
    is another install's; the finisher keeps it."""
    install_probe(home)
    real = uninstall._phase_state
    version = Path(os.environ["UV_TOOL_DIR"]).parent / "probe-versions" / VERSION

    def reinstalled(run):
        real(run)
        shutil.rmtree(version)
        (version / "probe-research").mkdir(parents=True)
        (version / "probe-research" / "pyvenv.cfg").write_text("home = /usr/bin\n")

    monkeypatch.setitem(uninstall._PHASE_STEPS, uninstall.Phase.STATE, reinstalled)
    assert _uninstall() == 0
    assert (version / "probe-research" / "pyvenv.cfg").exists()


def test_the_base_python_is_never_one_being_deleted(home):
    laid = install_probe(home)
    plan = uninstall_plan.compute(server=None)
    python = uninstall.base_python(plan)
    assert python is not None
    assert not any(python.startswith(str(env)) for env in laid["envs"])


# -- the process sweep (U-T4) ------------------------------------------------------------------------


def test_the_sweep_stops_a_process_of_this_install_and_nothing_else(home, tmp_path):
    """Matched by its EXECUTABLE only: a program outside the env that has a
    file of the env among its arguments (`less`, `vim`, a viewer) is not Probe's."""
    laid = install_probe(home)
    viewer = tmp_path / "viewer.py"
    viewer.write_text("import time\ntime.sleep(60)\n")
    ours = subprocess.Popen([str(laid["envs"][-1] / "bin" / "python"), "-c", "import time; time.sleep(60)"])
    other = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    reader = subprocess.Popen([sys.executable, str(viewer), str(laid["envs"][-1] / "pyvenv.cfg")])
    try:
        plan = uninstall_plan.compute(server=None)
        found = uninstall_procs.find(uninstall_procs.sweep_roots(plan))
        assert [p.pid for p in found] == [ours.pid]
        assert uninstall_procs.stop(found, grace=5) == []
        assert ours.wait(timeout=10) is not None
        assert other.poll() is None and reader.poll() is None
    finally:
        for proc in (ours, other, reader):
            if proc.poll() is None:
                proc.kill()
                proc.wait()


def test_a_capture_uploader_is_known_by_its_pid_file_its_command_and_its_start(home, tmp_path):
    folder = Path(os.environ["PROBE_TEST_TAP_PID_DIR"])
    tap = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)", "tap", "watch", "--session-id",
                            "sess-a"])
    stranger = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)", "tap"])
    try:
        time.sleep(0.2)
        (folder / "probe-research-tap-watcher-sess-a.pid").write_text(str(tap.pid))
        (folder / "probe-research-tap-watcher-sess-b.pid").write_text(str(stranger.pid))  # says "tap", no watch
        (folder / "probe-research-tap-watcher-sess-c.pid").write_text(str(tap.pid))  # another session's file
        found = uninstall_procs.tap_watchers()
        assert [p.pid for p in found] == [tap.pid]
    finally:
        for proc in (tap, stranger):
            proc.kill()
            proc.wait()


# -- unsynced note edits (D1) -------------------------------------------------------


def _dirty_notes(home: Path) -> None:
    """A team-note edit and an entity-note edit no Stop hook sent."""
    from probe.service import paths

    state = paths.state_dir()
    team = state / "team-note"
    (team / "abcd" ).mkdir(parents=True)
    (team / "abcd" / "base.md").write_text("# team\n")
    (team / "probe-team-note.md").write_text("# team\nmy unsent line\n")
    (team / "probe-team-note.md.owner").write_text("abcd\n")
    note = state / "notes" / "project" / "11111111-1111-1111-1111-111111111111"
    note.mkdir(parents=True)
    (note / "note.base").write_text("old\n")
    (note / "note.md").write_text("old\nmy unsent finding\n")


def test_unsynced_note_edits_are_unsent_research(home, server, no_exec, monkeypatch, capsys):
    install_probe(home)
    _dirty_notes(home)
    monkeypatch.setattr("probe.cli.uninstall_notes.send", lambda deadline, lines: None)  # nothing reached
    assert _uninstall() == 2
    assert "2 unsynced note edit(s)" in capsys.readouterr().err
    from probe.service import paths

    assert (paths.state_dir() / "team-note" / "probe-team-note.md").exists()
    assert not paths.uninstall_dir().exists()
    assert _uninstall(discard_unsent=True) == 0


def test_note_edits_that_were_sent_hold_nothing_back(home, server, no_exec, monkeypatch):
    install_probe(home)
    _dirty_notes(home)
    from probe.cli import uninstall_notes

    def sent(deadline, lines):  # what a landed push leaves: the base is the document
        for edit in uninstall_notes.unsynced():
            base = edit.path.with_suffix(".base") if edit.kind != uninstall_notes.TEAM_NOTE else (
                edit.path.parent / "abcd" / "base.md")
            base.write_text(edit.path.read_text())

    monkeypatch.setattr(uninstall_notes, "send", sent)
    assert _uninstall() == 0


def test_unsynced_note_edits_go_into_the_backup_file(home, server, no_exec, monkeypatch):
    import tarfile

    install_probe(home)
    _dirty_notes(home)
    monkeypatch.setattr("probe.cli.uninstall_notes.send", lambda deadline, lines: None)
    monkeypatch.setattr(uninstall, "_ask_unsent", lambda unsent, **_: uninstall.UnsentChoice.BACKUP)
    monkeypatch.setattr(uninstall, "_confirm", lambda run: None)
    from probe.core import events

    with events.session(False):
        assert uninstall.run(uninstall.Options(interactive=True)) == 0
    (saved,) = home.glob("probe-unsent-*.tar.gz")
    with tarfile.open(saved) as archive:
        names = archive.getnames()
    assert any(name.endswith("probe-team-note.md") for name in names)
    assert any(name.endswith("note.md") for name in names)


# -- isolation guard -------------------------------------------------------------------


def test_an_uninstall_in_a_sandbox_touches_nothing_outside_it(home, server, no_exec, tmp_path):
    """The box-wide `$TMPDIR` fallback outboxes (`/tmp/probe-outbox-<uid>*`)
    are this uid's in every HOME: an uninstall whose TMPDIR was not isolated
    deleted one (2026-10-26). A canary there, and every path of the plan, prove
    the sandbox held."""
    real_tmp = Path("/tmp")
    if not real_tmp.is_dir() or not hasattr(os, "getuid"):
        pytest.skip("no /tmp")

    def outboxes() -> dict:
        found = {}
        for path in real_tmp.glob(f"probe-outbox-{os.getuid()}*"):
            with contextlib.suppress(OSError):
                st = path.lstat()
                found[str(path)] = (st.st_ino, st.st_mtime_ns)
        return found

    canary = Path(tempfile.mkdtemp(prefix=f"probe-outbox-{os.getuid()}-guard-", dir=str(real_tmp)))
    try:
        before = outboxes()
        researcher_files(home)
        install_probe(home)
        assert _uninstall() == 0
        plan = no_exec["plan"]
        named = [p["path"] for p in plan["paths"]] + plan["env_generations"] + plan["shims"]
        assert named and all(path.startswith(str(tmp_path)) for path in named), [
            path for path in named if not path.startswith(str(tmp_path))]
        assert canary.is_dir()
        assert outboxes() == before
    finally:
        shutil.rmtree(canary, ignore_errors=True)


# -- an installer meets an uninstall that stopped halfway ---------------------------------


def _killed_at(phase: str, monkeypatch) -> None:
    from probe.service import paths

    def killed(run):
        raise Killed

    real = uninstall._PHASE_STEPS[uninstall.Phase(phase)]
    monkeypatch.setitem(uninstall._PHASE_STEPS, uninstall.Phase(phase), killed)
    with pytest.raises(Killed):
        _uninstall()
    monkeypatch.setitem(uninstall._PHASE_STEPS, uninstall.Phase(phase), real)
    barrier = json.loads(paths.uninstall_barrier_path().read_text())
    barrier["pid"] = 999999999  # the owner died with the kill
    paths.uninstall_barrier_path().write_text(json.dumps(barrier))


def test_an_installer_finishes_an_uninstall_that_stopped_halfway_then_goes_on(home, server, monkeypatch, capsys):
    researcher_files(home)
    before = snapshot(home)
    install_probe(home)
    _killed_at("integrations", monkeypatch)
    found, said = uninstall.finish_interrupted()
    assert (found, said) == (uninstall.Interrupted.FINISHED, "")
    assert "An uninstall stopped halfway (phase integrations); finishing it first" in capsys.readouterr().err
    _clean_slate(before, snapshot(home))
    assert os.environ.get("PROBE_TELEMETRY") == "off"  # the fixture's value, put back after the state phase


def test_an_uninstall_running_now_is_never_taken_over(home, server, no_exec):
    from probe.service import paths, procid

    install_probe(home)
    owner = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    try:
        paths.private_dir(paths.uninstall_dir())
        paths.uninstall_barrier_path().write_text(json.dumps(
            {"v": 1, "pid": owner.pid, "start": procid.start_time(owner.pid), "at": 0, "phase": "integrations",
             "plan": ""}))
        installed = snapshot(home)
        found, said = uninstall.finish_interrupted()
        assert found is uninstall.Interrupted.RUNNING and "running" in said
        assert snapshot(home) == installed
    finally:
        owner.kill()
        owner.wait()


def test_an_uninstall_that_stopped_before_the_server_is_no_installers_business(home, server, no_exec, monkeypatch):
    install_probe(home)
    _killed_at("draining", monkeypatch)
    assert uninstall.finish_interrupted() == (uninstall.Interrupted.NONE, "")  # stale: the installer clears it


# -- called off before the point of no return: as if it never began (review P0) -----------------


@pytest.fixture
def restarts(monkeypatch):
    """`client.ensure` as the call-off runs it: recorded, nothing spawned."""
    from probe.service import client

    calls = []

    def ensure(*, wait: float = 0.0):
        calls.append(wait)
        return client.Ensured.SPAWNED

    monkeypatch.setattr(client, "ensure", ensure)
    return calls


def _tap(home: Path) -> Path:
    return home / ".claude" / "plugins" / "probe-research-tap"


def test_a_refusal_for_unsent_research_puts_everything_back(home, server, no_exec, monkeypatch, restarts, capsys):
    """Exit 2 with unsent research: capture still on (no killswitch, its key
    kept), import jobs kept, the service started again, no barrier, and the
    line says what was stopped meanwhile."""
    from probe.service import paths

    install_probe(home)
    _queue_one(home)
    job = paths.state_dir() / "import-jobs" / "0123456789abcdef0123456789abcdef"
    job.mkdir(parents=True)
    (job / "job.json").write_text("{}")
    monkeypatch.setattr(uninstall, "drain", lambda deadline, lines: None)

    def stopped(plan, *, force, lines, stopped=None):
        if stopped is not None:
            stopped.append("the Probe service")
        lines.append("Stopped the Probe service.")
        return []

    monkeypatch.setattr(uninstall_procs, "stop_everything", stopped)
    assert _uninstall() == 2
    assert not (_tap(home) / ".disabled").exists() and (_tap(home) / ".token").exists()
    assert (job / "job.json").exists()
    assert not paths.uninstall_dir().exists()
    assert restarts
    assert not any(call[0] in ("retire", "revoke", "capture") for call in server.calls)
    err = capsys.readouterr().err
    assert "Nothing was removed. Stopped meanwhile: the Probe service." in err
    assert "starting again" in err


@pytest.mark.parametrize("signal_", ["ctrl-c", "sigterm"])
def test_ctrl_c_or_sigterm_before_the_server_puts_everything_back(home, server, no_exec, monkeypatch, restarts,
                                                                  signal_):
    from probe.service import paths

    install_probe(home)

    def interrupted(deadline, lines):
        raise KeyboardInterrupt if signal_ == "ctrl-c" else uninstall.Terminated(15)

    monkeypatch.setattr(uninstall, "drain", interrupted)
    assert _uninstall() == 2
    assert not paths.uninstall_dir().exists() and restarts
    assert not (_tap(home) / ".disabled").exists()
    assert (Path(os.environ["UV_TOOL_DIR"]) / "probe-research").is_symlink()


def test_ctrl_c_after_the_server_leaves_the_barrier_for_the_rerun(home, server, no_exec, monkeypatch, restarts,
                                                                 capsys):
    from probe.service import paths

    researcher_files(home)
    before = snapshot(home)
    install_probe(home)
    real = uninstall._PHASE_STEPS[uninstall.Phase.INTEGRATIONS]

    def interrupted(run):
        raise KeyboardInterrupt

    monkeypatch.setitem(uninstall._PHASE_STEPS, uninstall.Phase.INTEGRATIONS, interrupted)
    assert _uninstall() == 1
    assert "run `probe uninstall` again to finish" in capsys.readouterr().err
    assert json.loads(paths.uninstall_barrier_path().read_text())["phase"] == "integrations"
    assert not restarts
    monkeypatch.setitem(uninstall._PHASE_STEPS, uninstall.Phase.INTEGRATIONS, real)
    assert _uninstall() == 0
    _clean_slate(before, snapshot(home))


def test_with_no_terminal_and_no_yes_nothing_happens(home, server, no_exec, capsys):
    install_probe(home)
    installed = snapshot(home)
    from probe.core import events

    with events.session(False):
        assert uninstall.run(uninstall.Options(yes=False, interactive=False)) == 2
    assert "Pass --yes to confirm" in capsys.readouterr().err
    assert snapshot(home) == installed


def test_a_custom_outbox_is_kept_not_deleted(home, server, no_exec, monkeypatch, tmp_path, capsys):
    """PROBE_OUTBOX_DIR outside Probe's folders may be the researcher's: what
    is queued there is kept, said so, and asks no D1 question."""
    from probe.sdk.journal import Journal, default_root

    custom = tmp_path / "lab-outbox"
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(custom))
    install_probe(home)
    Journal(default_root()).append_http("POST", "/v1/runs", {"name": "r"})
    monkeypatch.setattr(uninstall, "drain", lambda deadline, lines: None)
    assert _uninstall() == 0
    out = capsys.readouterr().out
    assert "Kept 1 unsent item(s)" in out and "Deleting" not in out
    assert any(custom.rglob("*.json"))


def test_a_rerun_offline_at_the_server_keeps_the_barrier(home, server, no_exec, monkeypatch, capsys):
    from probe.service import paths

    install_probe(home)
    _killed_at("server", monkeypatch)
    server.down = True
    assert _uninstall() == 2
    assert "--offline" in capsys.readouterr().err
    assert json.loads(paths.uninstall_barrier_path().read_text())["phase"] == "server"


def test_what_is_left_in_integrations_or_state_ends_partial_and_resumable(home, server, no_exec, monkeypatch):
    from probe.service import paths

    researcher_files(home)
    before = snapshot(home)
    install_probe(home)
    stuck = paths.state_dir() / "team-note"
    real = uninstall._remove_path
    monkeypatch.setattr(uninstall, "_remove_path", lambda path: False if Path(path) == stuck else real(path))
    assert _uninstall() == 1
    assert json.loads(paths.uninstall_barrier_path().read_text())["phase"] == "state"
    assert (Path(os.environ["UV_TOOL_DIR"]) / "probe-research").is_symlink()  # the finisher did not run
    monkeypatch.setattr(uninstall, "_remove_path", real)
    barrier = json.loads(paths.uninstall_barrier_path().read_text())
    barrier["pid"] = 999999999
    paths.uninstall_barrier_path().write_text(json.dumps(barrier))
    assert _uninstall() == 0
    _clean_slate(before, snapshot(home))


def test_the_finisher_runs_on_this_interpreter_or_one_that_proves_it_starts(home, monkeypatch):
    laid = install_probe(home)
    plan = uninstall_plan.compute(server=None)
    assert uninstall.base_python(plan) == os.path.realpath(sys.executable)
    # This interpreter inside an env being deleted: only a candidate that
    # starts may run the finisher; none does here, so it runs in-process.
    plan["env_generations"].append(os.path.dirname(os.path.dirname(os.path.realpath(sys.executable))))
    monkeypatch.setattr(uninstall, "_python_works", lambda python: False)
    assert uninstall.base_python(plan) is None
    del laid


# -- review of #3511, round 2 -----------------------------------------------------------------


def _live_owner():
    """A process standing for another `probe uninstall` that runs right now."""
    return subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])


def _their_barrier(owner, phase: str = "draining") -> dict:
    """Run A's barrier and plan, as A leaves them while it waits at the D1 question."""
    from probe.service import paths, procid

    paths.private_dir(paths.uninstall_dir())
    record = {"v": 1, "pid": owner.pid, "start": procid.start_time(owner.pid), "at": 0, "phase": phase,
              "plan": str(paths.uninstall_plan_path())}
    paths.uninstall_barrier_path().write_text(json.dumps(record))
    _their_plan()
    return record


def _their_plan() -> None:
    from probe.service import paths

    paths.private_dir(paths.uninstall_dir())
    paths.uninstall_plan_path().write_text(json.dumps({"v": 1, "paths": [], "theirs": True}))


@pytest.mark.parametrize("how", ["refused", "ctrl-c at the lock", "ctrl-c at the lock, their plan only",
                                 "the lock timed out, their plan only"])
def test_a_second_run_never_calls_off_the_first_runs_uninstall(home, server, no_exec, monkeypatch, restarts,
                                                               how):
    """Run A waits at the unsent-research question. Run B is refused ("another
    uninstall is running"), or is stopped while it waits for the install lock
    A holds: B calls off only what B wrote, so A's barrier and plan stay and
    nothing restarts the service under A."""
    from probe._shared import handoff
    from probe.service import paths

    install_probe(home)
    owner = _live_owner()
    try:
        if how == "refused":
            theirs = _their_barrier(owner)
        else:
            theirs = None

            def take_lock(root, wait_s):  # A takes the lock and gets on while B waits
                nonlocal theirs
                if "plan only" in how:
                    _their_plan()  # A between its plan and its barrier
                else:
                    theirs = _their_barrier(owner)
                if "timed out" in how:
                    return None
                raise KeyboardInterrupt

            monkeypatch.setattr(handoff, "take_lock", take_lock)
        assert _uninstall() == 2
        assert json.loads(paths.uninstall_plan_path().read_text()).get("theirs") is True
        if theirs is not None:
            assert json.loads(paths.uninstall_barrier_path().read_text()) == theirs
        assert not restarts
        assert not any(call[0] in ("retire", "revoke", "capture") for call in server.calls)
    finally:
        owner.kill()
        owner.wait()


@pytest.mark.parametrize("left", ["unreadable", "unknown phase"])
def test_a_resumed_run_that_is_refused_leaves_the_uninstall_half_done_and_says_how_to_finish(
        home, server, no_exec, monkeypatch, restarts, capsys, left):
    """An unreadable or unknown-phase barrier resumes from "stopping"; nobody
    knows how far that run got. Refused (unsent research), the resumed run
    never calls off: the barrier stays LIVE (also once this run is gone), the
    service is not started again, and it says the uninstall is half-done."""
    from probe._shared import uninstall_barrier
    from probe.service import paths

    install_probe(home)
    _killed_at("server", monkeypatch)
    if left == "unreadable":
        paths.uninstall_barrier_path().write_text("{not json")
    else:
        record = json.loads(paths.uninstall_barrier_path().read_text())
        paths.uninstall_barrier_path().write_text(json.dumps({**record, "phase": "a-later-releases-phase"}))
    _queue_one(home)
    monkeypatch.setattr(uninstall, "drain", lambda deadline, lines: None)  # the server takes nothing
    capsys.readouterr()
    assert _uninstall() == 2
    err = capsys.readouterr().err
    assert "half-done" in err and "--discard-unsent" in err and "probe uninstall --backup-unsent" in err
    assert "Nothing was removed" not in err and "starting again" not in err
    assert not restarts
    record = uninstall_barrier.read()
    assert record is not None and record["phase"] == uninstall.RESUMING
    assert uninstall_barrier.state(record) == uninstall_barrier.State.LIVE
    # ... and LIVE once this run's process is gone, too: never "draining" + a dead owner (STALE).
    paths.uninstall_barrier_path().write_text(json.dumps({**record, "pid": 999999999}))
    assert uninstall_barrier.state() == uninstall_barrier.State.LIVE
    said = uninstall_barrier.refusal()
    assert "finisher.py" not in said and "must be finished first: run `probe uninstall`" in said
    assert _uninstall(discard_unsent=True) == 0
    assert not paths.uninstall_dir().exists()


def _summary_draft(home: Path) -> Path:
    """A session's summary draft that differs from its base: never sent from here."""
    from probe.service import paths

    folder = paths.state_dir() / "summaries" / "run" / "22222222-2222-2222-2222-222222222222"
    folder.mkdir(parents=True)
    (folder / "sess-1.base").write_text("old summary\n")
    draft = folder / "sess-1.md"
    draft.write_text("old summary\nmy draft line\n")
    return draft


def test_summary_drafts_are_counted_apart_and_a_rerun_online_is_not_the_advice(home, server, no_exec, monkeypatch,
                                                                                capsys):
    install_probe(home)
    _summary_draft(home)
    monkeypatch.setattr("probe.cli.uninstall_notes.send", lambda deadline, lines: None)
    unsent = uninstall.count_unsent()
    assert (unsent.drafts, unsent.notes, unsent.sendable) == (1, 0, 0)
    assert _uninstall() == 2
    err = capsys.readouterr().err
    assert "1 summary draft(s), never sent" in err and "note edit" not in err
    assert "--discard-unsent" in err and "backup" in err
    assert "Run it again once online" not in err
    # With something sendable too: a rerun online sends that, never the drafts.
    mixed = uninstall._unsent_advice(uninstall.Unsent(ops=1, drafts=1))
    assert "--discard-unsent" in mixed and "never the drafts" in mixed and "once online so they are sent" not in mixed
    assert _uninstall(discard_unsent=True) == 0


def test_a_parked_team_note_counts_once_not_once_per_sidecar(home):
    """`park()` leaves the copy with its `.owner`, `.base` and `.meta`: one edit."""
    from probe.cli import team_note_file, uninstall_notes
    from probe.service import paths

    team = paths.state_dir() / "team-note"
    (team / "abcd").mkdir(parents=True)
    (team / "abcd" / "base.md").write_text("# team\n")
    (team / "abcd" / "meta.json").write_text('{"version": 3}')
    document = team / team_note_file.DOCUMENT_NAME
    document.write_text("# team\nanother credential's line\n")
    document.with_name(document.name + ".owner").write_text("abcd\n")
    parked = team_note_file.park(document)
    assert parked is not None
    assert {p.name for p in team.glob(f"{parked.name}.*")} == {
        f"{parked.name}{suffix}" for suffix in (".owner", ".base", ".meta")}
    edits = uninstall_notes.unsynced()
    assert [(e.kind, e.path) for e in edits] == [(uninstall_notes.TEAM_NOTE, parked)]


def test_a_backup_cut_short_leaves_no_file_that_looks_complete(home, monkeypatch):
    import tarfile

    source = home / "queued.json"
    source.write_text("{}" * 1000)

    def cut(self, *args, **kwargs):
        self.fileobj.write(b"\x1f\x8b partial")
        raise KeyboardInterrupt

    with monkeypatch.context() as patched:  # never `undo()`: that drops the sandbox HOME too
        patched.setattr(tarfile.TarFile, "add", cut)
        with pytest.raises(KeyboardInterrupt):
            uninstall.backup(uninstall.Unsent(ops=1, sources=[source]))
    assert not list(home.glob("probe-unsent-*")) and not list(home.glob(".probe-unsent-*"))
    saved = uninstall.backup(uninstall.Unsent(ops=1, sources=[source]))
    assert saved.name.startswith("probe-unsent-") and saved.stat().st_mode & 0o777 == 0o600
    with tarfile.open(saved) as archive:
        assert archive.getnames() == ["queued.json"]
    assert [p.name for p in home.glob("*probe-unsent-*")] == [saved.name]


@pytest.mark.parametrize("why", ["busy", "offline"])
def test_a_resumed_run_refused_at_the_lock_or_offline_says_what_finishes_it(home, server, no_exec, monkeypatch,
                                                                           restarts, capsys, why):
    """Nothing unsent, so no --discard-unsent advice: the lock is held (an
    update, or another uninstall), or the server cannot be reached."""
    from probe._shared import handoff, uninstall_barrier
    from probe.service import paths

    install_probe(home)
    _killed_at("server", monkeypatch)
    if why == "busy":
        paths.uninstall_barrier_path().write_text("{not json")
        monkeypatch.setattr(handoff, "take_lock", lambda root, wait_s: None)
        said = "another Probe update or uninstall is running; try again when it ends"
    else:
        server.down = True
        said = "come back online, or run `probe uninstall --offline` to finish locally"
    capsys.readouterr()
    assert _uninstall() == 2
    err = capsys.readouterr().err
    assert said in err and "half-done" in err
    assert "--discard-unsent" not in err and "Nothing was removed" not in err and not restarts
    assert uninstall_barrier.state() == uninstall_barrier.State.LIVE


def test_a_resumed_runs_question_offers_stop_here_not_cancel(home, server, no_exec, monkeypatch, restarts, capsys):
    from probe.cli import tui
    from probe.core import events
    from probe.service import paths

    install_probe(home)
    _killed_at("server", monkeypatch)
    paths.uninstall_barrier_path().write_text("{not json")
    _queue_one(home)
    monkeypatch.setattr(uninstall, "drain", lambda deadline, lines: None)
    asked = []

    def review(title, body, options):
        asked.append([label for label, _value in options])
        return uninstall.UnsentChoice.CANCEL

    monkeypatch.setattr(tui, "window", lambda enabled: contextlib.nullcontext())
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(tui, "leave_window", lambda: None)
    monkeypatch.setattr(tui, "review", review)
    with events.session(False):
        assert uninstall.run(uninstall.Options(interactive=True)) == 2
    assert asked and asked[0][0] == uninstall.STOP_HERE_LABEL
    assert uninstall.STOP_HERE_LABEL == (
        "Stop here (the uninstall stays half-done; run `probe uninstall` to finish)")
    assert not any(uninstall.CANCEL_LABEL in labels for labels in asked)
    err = capsys.readouterr().err
    assert "stopped here" in err and "cancelled" not in err and not restarts
    assert json.loads(paths.uninstall_barrier_path().read_text())["phase"] == uninstall.RESUMING


# -- installers finish an uninstall that stopped halfway (lane R's entries) ---------------------


def test_probe_repair_finishes_an_uninstall_killed_in_integrations_then_installs_afresh(uv_machine, monkeypatch,
                                                                                       capsys):
    """Real uv: `probe uninstall` killed in its integrations phase (its owner
    gone, past the point of no return), then `probe repair`: the uninstall is
    finished first (installer mode), then the repair installs a working CLI and
    asks for the keeper and the lifeboat."""
    import typer

    import probe
    from probe._shared import installs, uninstall_barrier
    from probe.cli import install_pipeline, repair
    from probe.service import keeper, paths

    m = uv_machine
    for name in ("CLAUDE_CODE_SESSION_ID", "PI_SESSION_ID", "PROBE_KIMI_SESSION_ID", "PROBE_TOKEN",
                 "PROBE_INGEST_TOKEN", "PROBE_MCP_TOKEN"):
        monkeypatch.delenv(name, raising=False)
    assert install_pipeline.install_cli("1.0.1").ok
    note = paths.state_dir() / "team-note" / "probe-team-note.md"
    note.parent.mkdir(parents=True, exist_ok=True)
    note.write_text("# team\n")
    _killed_at("integrations", monkeypatch)
    assert uninstall_barrier.state() == uninstall_barrier.State.LIVE
    assert installs.active(m.tools) is not None  # the CLI is still there: the finisher never ran

    monkeypatch.setattr(probe, "__version__", "1.0.1")  # the release `probe repair` runs as
    monkeypatch.setattr(repair, "_agents", lambda: [])
    monkeypatch.setattr(repair, "repair_identity", lambda: repair.Part(lines=["held"]))
    monkeypatch.setattr(repair, "repair_service", lambda out: repair.Part(lines=["the Probe service runs 1.0.1"]))
    asked = []
    monkeypatch.setattr(keeper, "install", lambda env: asked.append(env) or "installed the keeper and the lifeboat")
    capsys.readouterr()
    code = 0
    try:
        repair.run()
    except typer.Exit as exc:
        code = exc.exit_code
    err = capsys.readouterr().err
    assert code == 0, err
    assert "An uninstall stopped halfway (phase integrations); finishing it first" in err
    assert uninstall_barrier.state() == uninstall_barrier.State.ABSENT and not paths.uninstall_dir().exists()
    assert not note.exists()  # the uninstall's state phase ran
    assert installs.active(m.tools) is not None and m.probe() == "probe 1.0.1"
    assert asked, "the repair asks for the keeper and the lifeboat"


def test_an_installer_entry_finishes_only_a_dead_owners_uninstall(home, monkeypatch):
    """`install_pipeline.refusal` (every install entry asks it first): a LIVE
    barrier whose owner is gone is finished; a running owner refuses."""
    from probe.cli import daemon_cli, install_pipeline
    from probe.service import paths, procid

    paths.private_dir(paths.uninstall_dir())
    paths.uninstall_barrier_path().write_text(json.dumps(
        {"v": 1, "pid": os.getpid(), "start": procid.start_time(os.getpid()), "at": 0, "phase": "integrations",
         "plan": ""}))
    monkeypatch.setattr(uninstall, "run", lambda options: pytest.fail("never taken over while its owner runs"))
    assert "running" in install_pipeline.refusal(finish=True)
    finished = []
    monkeypatch.setattr(uninstall, "finish_interrupted",
                        lambda: finished.append(1) or (uninstall.Interrupted.FINISHED, ""))
    record = json.loads(paths.uninstall_barrier_path().read_text())
    paths.uninstall_barrier_path().write_text(json.dumps({**record, "pid": 999999999}))
    # Not an install entry (`npx probe-research backfill`, any other wizard action): refused, never finished.
    assert "must be finished first" in install_pipeline.refusal() and finished == []
    monkeypatch.setattr(install_pipeline.uninstall_barrier, "refusal", lambda: None)  # finished: nothing left
    gate = install_pipeline.gate(finish=True)
    assert (gate.refused, gate.finished) == ("", True) and finished == [1]
    # `probe daemon install` asks the same question, then goes on.
    from typer.testing import CliRunner

    provisioned = []
    monkeypatch.setattr(daemon_cli, "_hold_identity", lambda: [])
    monkeypatch.setattr(daemon_cli, "_provision", lambda *, fresh=False: provisioned.append(fresh))
    result = CliRunner().invoke(daemon_cli.daemon_app, ["install"])
    assert result.exit_code == 0, result.output
    assert finished == [1, 1] and provisioned == [True]  # finished here: installed afresh, no shortcut


# -- the desktop app runs `probe uninstall --yes --json` itself ---------------------------------


def test_the_desktop_apps_own_uninstall_never_quits_it(monkeypatch):
    calls = []
    monkeypatch.setattr(uninstall_procs.sys, "platform", "darwin")
    monkeypatch.setattr(uninstall_procs.subprocess, "run",
                        lambda argv, **kw: calls.append(argv) or subprocess.CompletedProcess(argv, 0, "", ""))
    monkeypatch.setenv("PROBE_DESKTOP_HUMAN", "1")
    lines: list[str] = []
    uninstall_procs.quit_desktop_app(lines)
    assert calls == [] and lines == []
    monkeypatch.delenv("PROBE_DESKTOP_HUMAN")
    uninstall_procs.quit_desktop_app(lines)
    assert [argv[0] for argv in calls] == ["pgrep", "osascript"]


def test_this_process_and_its_parents_are_never_live_users(home, monkeypatch):
    """The desktop app (an ancestor of its `probe uninstall`) is not a user of
    the install it removes; another process is."""
    stranger = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    try:
        holds = [{"run": "app", "pid": os.getppid(), "start": "x"}, {"run": "me", "pid": os.getpid(), "start": "x"},
                 {"run": "other", "pid": stranger.pid, "start": "x"}]
        monkeypatch.setattr(uninstall_procs, "_exec_holds", lambda: holds)
        found = uninstall_procs.live_users()
        assert [u.pid for u in found] == [stranger.pid]
    finally:
        stranger.kill()
        stranger.wait()


def test_backup_unsent_saves_the_backup_and_goes_on(home, server, no_exec, monkeypatch, capsys):
    import tarfile

    install_probe(home)
    _queue_one(home)
    monkeypatch.setattr(uninstall, "drain", lambda deadline, lines: None)
    assert _uninstall() == 2  # --yes with neither flag still stops
    assert "--backup-unsent" in capsys.readouterr().err
    assert _uninstall(backup_unsent=True) == 0
    assert "(--backup-unsent)" in capsys.readouterr().out
    (saved,) = home.glob("probe-unsent-*.tar.gz")
    with tarfile.open(saved) as archive:
        assert any("ops" in name for name in archive.getnames())


def test_discard_and_backup_together_are_a_usage_error(home, server, no_exec):
    import importlib

    from typer.testing import CliRunner

    main = importlib.import_module("probe.cli.main")  # `probe.cli.main` the module, not the function
    installed = snapshot(home)
    result = CliRunner().invoke(main.app, ["uninstall", "--yes", "--discard-unsent", "--backup-unsent"])
    assert result.exit_code == 2 and "cannot be used together" in result.output
    assert snapshot(home) == installed


def _json_uninstall(**kwargs) -> tuple[int, dict]:
    """A `probe uninstall --yes --json` run in this process: (exit code, its `result` event)."""
    import typer

    from probe.core import events

    got: list[dict] = []
    code = 0
    try:
        with events.session(True, sink=got.append):
            code = uninstall.run(uninstall.Options(yes=True, json=True, **kwargs))
            if code:
                raise typer.Exit(code)
    except typer.Exit as exc:
        code = exc.exit_code
    assert got[-1]["event"] == "done" and got[-1]["exit_code"] == code
    return code, next(event for event in got if event["event"] == "result")


@pytest.mark.parametrize("why", ["unsent_research", "live_users", "in_session", "offline", "busy", "partial", "done"])
def test_the_json_result_says_why_as_data(home, server, no_exec, monkeypatch, why):
    from probe._shared import handoff
    from probe.service import paths

    install_probe(home)
    want: dict = {}
    if why == "unsent_research":
        _queue_one(home)
        monkeypatch.setattr(uninstall, "drain", lambda deadline, lines: None)
        want = {"code": "unsent_research", "resumed": False, "total": 1, "sending_can_help": True,
                "counts": {"queued_writes": 1, "offline_runs": 0, "transcript_pieces": 0, "note_edits": 0,
                           "summary_drafts": 0}}
    elif why == "live_users":
        users = [uninstall_procs.User(uninstall_procs.UserKind.SESSION, "claude_code session abc (pid 1234)", 1234)]
        monkeypatch.setattr(uninstall_procs, "live_users", lambda: users)
        want = {"code": "live_users", "resumed": False,
                "users": [{"kind": "session", "label": "claude_code session abc (pid 1234)", "pid": 1234}]}
    elif why == "in_session":
        monkeypatch.setattr(uninstall_procs, "recorded_session_here", lambda: "sess-1")
        want = {"code": "in_session", "resumed": False, "session": "sess-1"}
    elif why == "offline":
        server.down = True
        want = {"code": "offline", "resumed": False, "error": f"{BASE}: connection refused"}
    elif why == "busy":
        monkeypatch.setattr(handoff, "take_lock", lambda root, wait_s: None)
        want = {"code": "busy", "resumed": False}
    elif why == "partial":
        stuck = paths.state_dir() / "team-note"
        real = uninstall._remove_path
        monkeypatch.setattr(uninstall, "_remove_path", lambda path: False if Path(path) == stuck else real(path))
        want = {"code": "partial", "resumed": False, "resume": "probe uninstall", "phase": "state"}
    code, result = _json_uninstall()
    if why == "done":
        assert code == 0 and "reason" not in result
        return
    assert code == (1 if why == "partial" else 2)
    assert result["reason"] == want


# -- review of ec1aaa079c ------------------------------------------------------------------------


def test_probe_daemon_install_after_a_halfway_uninstall_ends_with_the_cli_on_path(uv_machine, monkeypatch):
    """P1-1, real uv: the finish takes the CLI's link and `probe` command; `probe
    daemon install` then installs the CLI again (never "already installed")
    and starts the service."""
    from typer.testing import CliRunner

    import probe
    from probe._shared import installs, uninstall_barrier
    from probe.cli import daemon_cli, install_pipeline

    m = uv_machine
    for name in ("CLAUDE_CODE_SESSION_ID", "PI_SESSION_ID", "PROBE_KIMI_SESSION_ID", "PROBE_TOKEN"):
        monkeypatch.delenv(name, raising=False)
    assert install_pipeline.install_cli("1.0.1").ok
    _killed_at("integrations", monkeypatch)
    monkeypatch.setattr(probe, "__version__", "1.0.1")
    monkeypatch.setattr(daemon_cli, "_hold_identity", lambda: [])
    monkeypatch.setattr(daemon_cli, "ai_libraries", lambda: "1.0")  # this process HAS them: no shortcut taken
    monkeypatch.setattr(daemon_cli, "_fresh_ai_libraries", lambda python: "1.0")  # the stand-in wheel has none
    started = []
    monkeypatch.setattr(daemon_cli, "_start_service", lambda: started.append(1))
    result = CliRunner().invoke(daemon_cli.daemon_app, ["install"])
    assert result.exit_code == 0, result.output
    assert "already installed" not in result.output
    assert uninstall_barrier.state() == uninstall_barrier.State.ABSENT
    assert installs.tool_state(m.tools) == installs.ToolPath.LINKED and m.probe() == "probe 1.0.1"
    assert started == [1]


def test_an_installer_backs_up_what_was_queued_after_the_crash(home, server, monkeypatch, capsys):
    """P1-2: killed past "draining", then a training run queued a write; the
    installer finishing the uninstall cannot ask, so the write goes into
    `~/probe-unsent-<date>.tar.gz`, said in one line, and the finish goes on."""
    import tarfile

    install_probe(home)
    _killed_at("integrations", monkeypatch)
    _queue_one(home)
    capsys.readouterr()
    assert uninstall.finish_interrupted() == (uninstall.Interrupted.FINISHED, "")
    (saved,) = home.glob("probe-unsent-*.tar.gz")
    with tarfile.open(saved) as archive:
        assert any("ops" in name for name in archive.getnames())
    out = capsys.readouterr().out
    assert f"to {saved} (finishing an uninstall that had stopped, with nobody to ask)" in out


def test_a_resumed_interactive_run_asks_about_what_was_queued_since(home, server, no_exec, monkeypatch):
    install_probe(home)
    _killed_at("integrations", monkeypatch)
    _queue_one(home)
    asked = []
    monkeypatch.setattr(uninstall, "_ask_unsent",
                        lambda unsent, **kw: asked.append((unsent.ops, kw)) or uninstall.UnsentChoice.DELETE)
    from probe.core import events

    with events.session(False):
        assert uninstall.run(uninstall.Options(interactive=True)) == 0
    assert asked == [(1, {"resumed": True})]


@pytest.mark.parametrize("left", ["unreadable", "resuming", "a-later-releases-phase"])
def test_an_installer_never_runs_an_uninstall_it_cannot_place(home, server, monkeypatch, left):
    """P2-3: how far it got is unknown: only `probe uninstall` runs it."""
    from probe.service import paths

    install_probe(home)
    _killed_at("server", monkeypatch)
    if left == "unreadable":
        paths.uninstall_barrier_path().write_text("{not json")
    else:
        record = json.loads(paths.uninstall_barrier_path().read_text())
        paths.uninstall_barrier_path().write_text(json.dumps({**record, "phase": left}))
    monkeypatch.setattr(uninstall, "run", lambda options: pytest.fail("never from an installer"))
    found, said = uninstall.finish_interrupted()
    assert found is uninstall.Interrupted.RUNNING and "finish it with `probe uninstall`" in said


def test_the_uninstall_never_goes_on_without_the_install_lock(home, server, no_exec, monkeypatch):
    from probe._shared import handoff
    from probe.service import paths

    install_probe(home)
    installed = snapshot(home)

    def broken(root, wait_s):
        raise PermissionError(13, "Permission denied")

    monkeypatch.setattr(handoff, "take_lock", broken)
    code, result = _json_uninstall()
    assert code == 2 and result["reason"]["code"] == "busy" and "Permission denied" in result["reason"]["error"]
    assert not paths.uninstall_dir().exists() and snapshot(home) == installed


def test_an_owner_on_another_machine_is_never_cleared_resumed_or_finished(home, server, no_exec, monkeypatch,
                                                                          capsys):
    """P2-4, a shared home: the barrier names its host and machine key; another
    host's owner reads as running, whatever its pid says here."""
    import socket

    from probe._shared import uninstall_barrier
    from probe.service import paths

    install_probe(home)
    _killed_at("draining", monkeypatch)  # reversible: STALE if it were this machine's
    record = json.loads(paths.uninstall_barrier_path().read_text())
    assert record["host"] == socket.gethostname() and record["machine_key"] == paths.machine_key()
    assert uninstall_barrier.state() == uninstall_barrier.State.STALE
    paths.uninstall_barrier_path().write_text(json.dumps({**record, "machine_key": "f" * 16}))
    assert uninstall_barrier.state() == uninstall_barrier.State.LIVE and uninstall_barrier.clear_stale() is None
    assert uninstall.finish_interrupted()[0] is uninstall.Interrupted.RUNNING
    capsys.readouterr()
    assert _uninstall() == 2 and "another uninstall is running" in capsys.readouterr().err


def test_only_an_install_entry_finishes_a_halfway_uninstall(home, server, monkeypatch):
    """P2-6: the bootstrap finishes one only for an install (`finish_uninstall`);
    `npx probe-research backfill` and every other wizard action refuse with
    the reader's line."""
    from probe.cli import bootstrap

    install_probe(home)
    _killed_at("integrations", monkeypatch)
    monkeypatch.setattr(uninstall, "finish_interrupted", lambda: pytest.fail("not an install entry"))
    boot = bootstrap.ensure_persistent_install()
    assert boot.refused and "must be finished first: run `probe uninstall`" in boot.message


def test_an_installer_with_no_barrier_left_starts_no_uninstall(home, server, no_exec):
    """P2-7: the barrier went meanwhile: the embedded run returns, never a fresh `--yes` uninstall."""
    install_probe(home)
    installed = snapshot(home)
    from probe.core import events

    with events.session(False):
        assert uninstall.run(uninstall.Options(yes=True, embedded=True)) == 0
    assert snapshot(home) == installed and not server.calls


def test_doctor_and_status_say_first_that_an_uninstall_stopped_halfway(home, server, monkeypatch):
    """A plain `uv tool install` by hand after a killed uninstall: the barrier
    stays LIVE, so nothing of Probe starts or updates; `probe status` and
    `probe doctor` say so on their first line."""
    import importlib

    from typer.testing import CliRunner

    main = importlib.import_module("probe.cli.main")
    install_probe(home)
    assert uninstall.halfway_notice() is None
    _killed_at("integrations", monkeypatch)
    want = ("An uninstall of Probe stopped halfway (phase integrations). Run `probe repair` (or `npx "
            "probe-research`) to finish it and set Probe up again, or `probe uninstall` to finish removing it.")
    assert uninstall.halfway_notice() == want
    for command in (["status"], ["doctor"]):
        result = CliRunner().invoke(main.app, command)
        assert result.exit_code == 0, result.output
        assert result.output.splitlines()[0] == want, command


def _probe_approves_its_codex_hooks(monkeypatch, record: Path) -> None:
    """Probe's own approval (`codex_hooks.approve`) against a stand-in Codex
    app-server that, as Codex does, writes a trust record when it approves."""
    key = "probe-research@research-os-agent:hooks/hooks.json:stop:0:0"

    class Server:
        error = None

        def call(self, _id, method, params):
            if method == "config/batchWrite":
                record.parent.mkdir(parents=True, exist_ok=True)
                record.write_text("sha256:" + "a" * 64 + "\n")
            return {"data": []}

        def close(self):
            pass

    with monkeypatch.context() as patched:
        patched.setattr(codex_hooks, "_open", lambda timeout: Server())
        patched.setattr(codex_hooks, "approvable", lambda result, cache, marketplace: [(key, "sha256:x")])
        patched.setattr(codex_hooks, "_trust_states", lambda checked: {key: codex_hooks.TRUSTED})
        assert APPROVE().approved == (key,)


def test_what_probes_install_left_holding_nothing_goes_too(home, server, no_exec, monkeypatch):
    """The V-T2 harness's leftovers, with Claude Code and Codex installed
    before Probe (their homes exist) and Kimi Code not at all: the empty
    skills folder, Claude's plugin ledger and known marketplaces with nothing
    left, a settings.json of empty plugin settings, an empty config.toml,
    Codex's trust records of Probe's hooks, and `~/.kimi-code/plugins`. A trust
    record of another hook stays."""
    (home / ".claude").mkdir()
    trust = home / ".codex" / ".hook-trust"
    trust.mkdir(parents=True)
    (trust / ("b" * 64)).write_text("sha256:" + "9" * 64 + "\n")  # another hook's: stays
    Path(os.environ["UV_TOOL_DIR"]).mkdir(parents=True)  # uv's own, there before Probe and never removed
    before = snapshot(home)
    install_probe(home)
    claude = home / ".claude"
    settings = json.loads((claude / "settings.json").read_text())
    settings["extraKnownMarketplaces"] = {"research-os-agent": {"source": {"source": "github"}}}
    (claude / "settings.json").write_text(json.dumps(settings))
    (claude / "skills" / "probe").mkdir(exist_ok=True)
    _probe_approves_its_codex_hooks(monkeypatch, trust / ("c" * 64))
    kimi = home / ".kimi-code" / "plugins"
    kimi.mkdir(parents=True)
    (kimi / ".probe-installed.lock").write_text("")
    assert _uninstall() == 0
    _clean_slate(before, snapshot(home))
    assert (trust / ("b" * 64)).exists() and not (home / ".kimi-code").exists()


def test_configure_makes_no_kimi_folder_where_kimi_code_is_not_installed(home):
    from probe.cli import kimi_config

    assert kimi_config.sync_mcp_bearer() == []
    assert not kimi_config.kimi_home().exists()


# -- review of 81a0d1bd93 ------------------------------------------------------------------------


def test_a_new_hostname_on_the_same_machine_never_keeps_a_dead_uninstall_alive(home, monkeypatch):
    """P1: macOS renames the host when the network changes. The machine KEY
    decides; the hostname only for a record without one; and where the key
    cannot be read (the tap's copy), the pid check alone."""
    from probe._shared import uninstall_barrier
    from probe.service import paths

    paths.private_dir(paths.uninstall_dir())
    record = {"v": 1, "pid": 999999999, "start": "1", "at": 0, "plan": "", "phase": "planned",
              "host": "old-name.local", "machine_key": paths.machine_key()}
    paths.uninstall_barrier_path().write_text(json.dumps(record))
    assert uninstall_barrier.state() == uninstall_barrier.State.STALE
    paths.uninstall_barrier_path().write_text(json.dumps({**record, "machine_key": None}))
    assert uninstall_barrier.state() == uninstall_barrier.State.LIVE  # no key: the hostname decides
    paths.uninstall_barrier_path().write_text(json.dumps({**record, "machine_key": "f" * 16}))
    assert uninstall_barrier.state() == uninstall_barrier.State.LIVE

    def unreadable():
        raise ImportError("no probe.service here")

    monkeypatch.setattr(paths, "machine_key", unreadable)
    assert uninstall_barrier.state() == uninstall_barrier.State.STALE  # the pid check alone


@pytest.mark.parametrize(("argv", "env", "finishes"), [
    (["wizard", "--action", "update", "--yes"], {}, False),  # the SessionStart hook's background update
    (["wizard", "--action", "update", "--yes"], {"PROBE_AUTOUPDATE_TRIGGER": "session_start"}, False),
    (["wizard", "--action", "update", "--yes"], {"PROBE_AUTOUPDATE_TRIGGER": "manual"}, True),
    (["wizard", "--action", "configure", "--yes"], {}, True),
    (["wizard", "--action", "diagnose", "--yes"], {}, False),
])
def test_only_an_update_a_person_asked_for_finishes_a_halfway_uninstall(home, monkeypatch, argv, env, finishes):
    import importlib

    import typer
    from typer.testing import CliRunner

    from probe.cli import bootstrap

    main = importlib.import_module("probe.cli.main")
    monkeypatch.delenv("PROBE_AUTOUPDATE_TRIGGER", raising=False)
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    asked = []

    def bootstrap_(**kwargs):
        asked.append(kwargs.get("finish_uninstall"))
        raise typer.Exit(0)

    monkeypatch.setattr(bootstrap, "ensure_persistent_install", bootstrap_)
    monkeypatch.setattr(main, "_version_notice", lambda: None)
    CliRunner().invoke(main.app, argv)
    assert asked == [finishes]


def test_codex_trust_records_go_only_when_probes_approval_made_them_and_they_are_unchanged(
        home, server, no_exec, monkeypatch, capsys):
    """Probe records the `.hook-trust` entries its own approval made; the
    uninstall removes exactly those, while unchanged. One from an approval
    before this release (no record) stays, and nothing is said about it."""
    from probe.cli import codex_hooks

    install_probe(home)
    trust = home / ".codex" / ".hook-trust"
    trust.mkdir(parents=True)
    (trust / ("e" * 64)).write_text("sha256:" + "1" * 64)  # approved before this release: no record
    ours, changed = trust / ("c" * 64), trust / ("d" * 64)
    _probe_approves_its_codex_hooks(monkeypatch, ours)
    _probe_approves_its_codex_hooks(monkeypatch, changed)
    assert set(codex_hooks.trust_records()) == {str(ours), str(changed)}
    changed.write_text("sha256:" + "2" * 64)  # Codex re-approved it for something else since
    capsys.readouterr()
    assert _uninstall() == 0
    out = capsys.readouterr().out
    assert not ours.exists() and changed.exists() and (trust / ("e" * 64)).exists()
    assert "Removed Codex's trust records of Probe's hooks (1)." in out and "e" * 64 not in out


def _claude_files(home: Path, *, settings=None, ledger=None, known=None) -> dict:
    claude = home / ".claude"
    plugins = claude / "plugins"
    plugins.mkdir(parents=True, exist_ok=True)
    files = {}
    for name, path, data in (("settings", claude / "settings.json", settings),
                             ("ledger", plugins / "installed_plugins.json", ledger),
                             ("known", plugins / "known_marketplaces.json", known)):
        if data is not None:
            path.write_text(json.dumps(data))
        files[name] = path
    return files


def test_hollow_cleanup_a_never_through_a_link(home, tmp_path):
    from probe.cli import uninstall_agents

    dotfiles = tmp_path / "dotfiles"
    dotfiles.mkdir()
    (dotfiles / "settings.json").write_text(json.dumps({"enabledPlugins": {}}))
    files = _claude_files(home, ledger={"version": 2, "plugins": {}}, known={})
    files["settings"].symlink_to(dotfiles / "settings.json")
    real_claude = tmp_path / "real-claude"
    (real_claude / "plugins").mkdir(parents=True)
    (real_claude / "plugins" / "installed_plugins.json").write_text(json.dumps({"version": 2, "plugins": {}}))
    uninstall_agents.remove_hollow()
    assert (dotfiles / "settings.json").exists() and files["settings"].is_symlink()
    # A symlinked ~/.claude: nothing under it is removed.
    for path in (files["ledger"], files["known"]):
        path.unlink(missing_ok=True)
    shutil.rmtree(home / ".claude")
    (home / ".claude").symlink_to(real_claude)
    uninstall_agents.remove_hollow()
    assert (real_claude / "plugins" / "installed_plugins.json").exists()


def test_hollow_cleanup_b_another_plugins_key_is_content(home):
    from probe.cli import uninstall_agents

    files = _claude_files(home, settings={"enabledPlugins": {"other@mkt": {}}})
    uninstall_agents.remove_hollow()
    assert json.loads(files["settings"].read_text()) == {"enabledPlugins": {"other@mkt": {}}}


def test_hollow_cleanup_c_the_ledger_stays_while_another_marketplace_is_cloned(home):
    from probe.cli import uninstall_agents

    files = _claude_files(home, ledger={"version": 2, "plugins": {}})  # known_marketplaces.json missing
    (files["ledger"].parent / "marketplaces" / "someone-else").mkdir(parents=True)
    uninstall_agents.remove_hollow()
    assert files["ledger"].exists()
    shutil.rmtree(files["ledger"].parent / "marketplaces" / "someone-else")
    uninstall_agents.remove_hollow()
    assert not files["ledger"].exists() and not (home / ".claude" / "plugins").exists()


def test_hollow_cleanup_d_an_empty_settings_file_goes(home):
    from probe.cli import uninstall_agents

    files = _claude_files(home, settings={})
    lines = uninstall_agents.remove_hollow()
    assert not files["settings"].exists() and any("settings.json" in line for line in lines)
