"""`probe doctor --bundle [--send]`: the debug log (`probe.core.debug_bundle`).

A fake machine with a credential planted in every place the bundle reads --
each agent's config, Probe's config, a Codex TOML, an agent process's
environment, its command line, this command's environment, a log -- and a
transcript whose content must never leave. The bundle is built for real
(every source), unzipped, and searched. The send runs against a real HTTP
server (`test_core_report.Stub`) standing in for the API and for the upload
slot. What it does not claim: what the real server and relay accept.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import os
import subprocess
import sys
import time
import zipfile
from pathlib import Path

import pytest
from typer.testing import CliRunner

from probe.cli import pi_config
from probe.core import debug_bundle, report
from probe.harness import get_registry
from tests.test_core_report import CLI_TOKEN, DAEMON_KEY, SID, Stub, _closed_port

BUNDLE_ID = "0b5e2f6a-3c4d-4e5f-8a9b-0c1d2e3f4a5b"


def _secret(n: int) -> str:
    """A realistic opaque credential, distinct per place it is planted."""
    return hashlib.sha256(f"planted-{n}".encode()).hexdigest()[:40]


SECRETS = {n: _secret(n) for n in range(1, 16)}
TRANSCRIPT_WORDS = "THE RESEARCHER ASKED ABOUT THE SECRET PROTEIN FOLD"


@pytest.fixture
def stub():
    server = Stub()
    yield server
    server.close()


@pytest.fixture
def fake_machine(tmp_path, monkeypatch, stub):
    """Every source the bundle reads, each holding a planted credential."""
    from probe.sdk.config import save_context

    home = Path.home()
    monkeypatch.setenv("PROBE_BASE_URL", stub.url)
    save_context({"base_url": stub.url, "token": CLI_TOKEN, "companion_token": DAEMON_KEY,
                  "mcp_token": "probe_pat_" + SECRETS[1]})

    claude = home / ".claude"
    (claude / "plugins").mkdir(parents=True)
    (claude / "settings.json").write_text(json.dumps({
        "model": "opus",
        "env": {"ANTHROPIC_API_KEY": SECRETS[2], "PROBE_SESSION_STATE": "on"},
        "apiKeyHelper": f"echo {SECRETS[3]}",
        "mcpServers": {"probe": {"headers": {"Authorization": f"Bearer {SECRETS[4]}"}}},
    }))
    (claude / ".credentials.json").write_text(json.dumps({"claudeAiOauth": {"accessToken": SECRETS[5]}}))
    (home / ".claude.json").write_text(json.dumps({
        "oauthAccount": {"emailAddress": "someone@example.test", "accessToken": SECRETS[6]},
        "projects": {"/work/proj": {"history": [{"display": TRANSCRIPT_WORDS}], "lastModelUsage": {"opus": 1}}},
    }))
    (claude / "plugins" / "installed_plugins.json").write_text(json.dumps({"plugins": {"probe-research": []}}))

    codex = home / ".codex"
    codex.mkdir()
    (codex / "config.toml").write_text(
        'model = "gpt-5"\n'
        "[mcp_servers.probe]\n"
        f'bearer_token = "{SECRETS[7]}"\n'
        f'env = {{ API_KEY = "{SECRETS[8]}" }}\n'
    )
    (codex / "auth.json").write_text(json.dumps({"tokens": {"access_token": SECRETS[9]}}))

    transcript = claude / "projects" / "-work-proj" / f"{SID}.jsonl"
    transcript.parent.mkdir(parents=True)
    transcript.write_text(
        json.dumps({"type": "user", "cwd": "/work/proj", "message": {"content": TRANSCRIPT_WORDS}}) + "\n"
        + json.dumps({"type": "assistant", "cwd": "/work/proj",
                      "message": {"model": "claude-opus-5-5", "content": [{"text": TRANSCRIPT_WORDS}]}}) + "\n"
    )

    state = report.state_root()
    state.mkdir(parents=True, exist_ok=True)
    (state / "daemon-errors.log").write_text(
        f"{time.strftime('%Y-%m-%dT%H:%M:%S')} session {SID}: failed with token probe_pat_{SECRETS[10]}\n")

    # A fake coding agent on PATH whose `--version` prints a credential.
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake = bin_dir / "claude"
    fake.write_text(f"#!/bin/sh\necho '2.1.0 (Claude Code) PROBE_TOKEN=probe_pat_{SECRETS[11]}'\n")
    fake.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}/usr/bin{os.pathsep}/bin")
    # This command's own environment.
    monkeypatch.setenv("OPENAI_API_KEY", SECRETS[12])
    monkeypatch.setenv("HTTPS_PROXY", f"http://user:{SECRETS[13]}@proxy.example.test:3128")
    return stub


@pytest.fixture
def live_agent(fake_machine):
    """A running "agent" with a credential in its environment and in its
    command line, registered with the service as a live session's owner."""
    from probe.service import paths, procid

    env = {**os.environ, "PROBE_TOKEN": "probe_pat_" + SECRETS[14], "CLAUDE_CODE_SESSION_ID": SID}
    child = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(120)", "probe-fake-agent", "--token", SECRETS[15],
         f"--api-key={SECRETS[15]}"], env=env)
    try:
        start = None
        for _ in range(50):
            start = procid.start_time(child.pid)
            if start:
                break
            time.sleep(0.05)
        folder = paths.service_dir()
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "sessions.json").write_text(json.dumps({"v": 1, "saved_at": time.time(), "sessions": [{
            "sid": SID, "harness": "claude_code", "mode": "on", "owner": {"pid": child.pid, "start_time": start},
            "generation": 1, "registered_at": time.time(), "heartbeat_at": time.time(),
            "state_dir": str(report.state_root())}]}))
        (folder / "recorders.json").write_text(json.dumps({"v": 1, "sessions": [
            {"sid": SID, "env": {"PROBE_TOKEN": CLI_TOKEN, "PROBE_TELEMETRY": "on"}}]}))
        (folder / "service.log").write_text("[2026-10-23T00:00:00Z] probe-service[1]: started\n")
        yield child
    finally:
        child.kill()
        child.wait()


def _unzipped(path: Path) -> dict[str, str]:
    with zipfile.ZipFile(path) as archive:
        return {name: archive.read(name).decode("utf-8", errors="replace") for name in archive.namelist()}


def _assert_clean(files: dict[str, str]) -> None:
    every = "\n".join(files.values())
    for n, secret in SECRETS.items():
        assert secret not in every, f"planted secret {n} reached the debug log"
    for secret in (CLI_TOKEN, DAEMON_KEY):
        assert secret not in every
    assert TRANSCRIPT_WORDS not in every


# ---------------------------------------------------------------------------
# What the zip holds, and what it never holds
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="reads agent environments from /proc")
def test_no_planted_credential_or_transcript_reaches_the_zip(live_agent, tmp_path):
    bundle = debug_bundle.build(out_dir=tmp_path / "out")
    files = _unzipped(bundle.path)
    _assert_clean(files)

    # Each place was READ (the test is not passing on an empty zip): the
    # credential's slot is there, redacted.
    settings = json.loads(files["agents/claude_code/home/settings.json"])
    assert settings["model"] == "opus" and settings["env"]["ANTHROPIC_API_KEY"] == "<redacted>"
    claude_json = json.loads(files["agents/claude_code/claude.json"])
    assert claude_json["oauthAccount"] == "<redacted>"  # the OAuth block, dropped whole
    assert "history" in json.dumps(claude_json) and "lastModelUsage" in json.dumps(claude_json)
    assert "agents/claude_code/home/.credentials.json.listing.json" in files  # listed, never read
    assert 'model = "gpt-5"' in files["agents/codex/home/config.toml"]
    assert "agents/codex/home/auth.json.listing.json" in files
    assert json.loads(files["probe/config.json"])["contexts"]["default"]["token"] == "<redacted>"
    assert "2.1.0 (Claude Code)" in files["agents/claude_code/version.txt"]
    assert json.loads(files["service/recorders.json"])["sessions"][0]["env"]["PROBE_TOKEN"] == "<redacted>"
    this = json.loads(files["system/env-this-command.json"])
    assert this["OPENAI_API_KEY"] == "<redacted>" and "proxy.example.test" in this["HTTPS_PROXY"]
    (agent_env,) = [json.loads(v) for k, v in files.items() if k.startswith("system/env-agents/")]
    assert agent_env["sid"] == SID and agent_env["env"]["PROBE_TOKEN"] == "<redacted>"
    assert agent_env["env"]["CLAUDE_CODE_SESSION_ID"] == SID
    processes = json.loads(files["system/processes.json"])
    (agent_process,) = [p for p in processes if p["pid"] == live_agent.pid]
    assert agent_process["cmdline"][-3:] == ["--token", "<arg>", "--api-key=<arg>"]
    assert "failed with token" in files["daemon/daemon-errors.log"]

    # The transcript, by metadata only.
    (row,) = json.loads(files["agents/claude_code/transcripts.json"])
    assert row["path"].endswith(f"{SID}.jsonl") and row["lines"] == 2
    assert (row["last_event_type"], row["model"], row["cwd"]) == ("assistant", "claude-opus-5-5", "/work/proj")

    # The layout, and the README.
    for folder in ("probe/", "service/", "sessions/", "daemon/", "agents/", "system/", "network/"):
        assert any(name.startswith(folder) for name in files), folder
    assert files["README.txt"].startswith("Probe debug log")
    assert bundle.files == len(files)
    if os.name == "posix":
        assert oct(bundle.path.stat().st_mode & 0o777) == "0o600"


def test_a_failing_or_hanging_source_is_skipped_and_said(fake_machine, tmp_path, monkeypatch):
    def hangs(_sink):
        time.sleep(5)

    def breaks(_sink):
        raise RuntimeError("boom")

    sources = debug_bundle._sources()
    monkeypatch.setattr(debug_bundle, "_sources", lambda: [("hangs", hangs), ("breaks", breaks), *sources[:2]])
    started = time.monotonic()
    bundle = debug_bundle.build(out_dir=tmp_path, collection=debug_bundle.collect(source_budget_s=0.3))
    assert time.monotonic() - started < 15
    assert {"hangs", "breaks"} <= set(bundle.skipped)
    readme = _unzipped(bundle.path)["README.txt"]
    assert "hangs: stopped: its first step took over 0.3 s" in readme and "breaks: failed: RuntimeError" in readme


def test_the_whole_collection_has_one_deadline(fake_machine, monkeypatch):
    monkeypatch.setattr(debug_bundle, "_sources", lambda: [("slow", lambda _s: time.sleep(0.6)),
                                                           ("never_reached", lambda _s: None)])
    collection = debug_bundle.collect(deadline_s=1.0)
    # `slow` finishes inside the 1 s; what is left is too little to start another source.
    assert collection.skipped == {"never_reached": "the debug log's time budget ran out first"}


# ---------------------------------------------------------------------------
# Bounds: each file, the contents, the zip
# ---------------------------------------------------------------------------


def _log_collection(sizes: dict[str, int]) -> debug_bundle.Collection:
    collection = debug_bundle.Collection(started_at=time.time())
    for name, size in sizes.items():
        lines = "".join(f"{name} line {i:08d} {os.urandom(24).hex()}\n" for i in range(size // 75))
        collection.files[name] = debug_bundle.Entry(lines.encode(), log=True)
    collection.files["probe/config.json"] = debug_bundle.Entry(b'{"small": true}\n')
    return collection


def test_each_file_is_its_last_five_mebibytes(tmp_path, monkeypatch):
    monkeypatch.setattr(debug_bundle, "FILE_CAP", 4096)
    log = tmp_path / "big.log"
    log.write_bytes("".join(f"line {i}\n" for i in range(5000)).encode())  # no CRLF on Windows
    sink = debug_bundle.Sink()
    sink.log_file("service/big.log", log)
    data = sink.files["service/big.log"].data.decode()
    assert len(data) <= 4096 and data.endswith("line 4999\n") and data.startswith("line ")
    assert sink.notes and sink.notes[0].startswith("service/big.log: only its last")


def test_past_the_caps_the_oldest_log_lines_go_first_and_the_readme_says_so(tmp_path):
    collection = _log_collection({"service/service.log": 600_000, "daemon/daemon-errors.log": 300_000})
    bundle = debug_bundle.build(out_dir=tmp_path, collection=collection, uncompressed_cap=400_000,
                                send_cap=300_000, relay_cap=600_000)
    files = _unzipped(bundle.path)
    contents = sum(len(v.encode()) for k, v in files.items() if k != "README.txt")
    assert contents <= 400_000 and bundle.bytes <= 300_000 and bundle.bytes + contents <= 600_000
    # The newest lines stay; the config is untouched.
    assert files["service/service.log"].rstrip().splitlines()[-1].startswith("service/service.log line 00007999")
    assert files["probe/config.json"] == '{"small": true}\n'
    assert "service/service.log: oldest lines dropped" in files["README.txt"]


def test_the_zip_is_trimmed_to_the_send_cap(tmp_path):
    """Random log lines barely compress: the zip itself must come under the cap."""
    collection = _log_collection({"service/service.log": 900_000})
    bundle = debug_bundle.build(out_dir=tmp_path, collection=collection, send_cap=250_000)
    assert bundle.bytes <= 250_000
    assert "service/service.log: oldest lines dropped" in _unzipped(bundle.path)["README.txt"]


def test_the_server_caps_are_the_contracts():
    """Contract rev 5b (server PR #3325): zip <= 25 MiB, zip + contents <= ~120 MiB."""
    assert debug_bundle.SEND_CAP == 25 * 1024 * 1024
    assert debug_bundle.UNCOMPRESSED_CAP + debug_bundle.SEND_CAP <= 120 * 1024 * 1024


def test_only_the_newest_three_bundles_stay_in_probes_own_folder(fake_machine, monkeypatch):
    monkeypatch.setattr(debug_bundle, "_sources", lambda: [])
    for n in range(5):
        collection = debug_bundle.Collection(started_at=time.time() + n)
        debug_bundle.build(collection=collection)
    kept = sorted(debug_bundle.default_dir().glob("probe-debug-*.zip"))
    assert len(kept) == debug_bundle.KEEP_BUNDLES


# ---------------------------------------------------------------------------
# Sending: create, PUT exactly as told, complete
# ---------------------------------------------------------------------------


def _slot(stub: Stub, *, put_status: int = 200, complete_status: int = 200) -> None:
    stub.routes[("POST", debug_bundle.ROUTE)] = (201, {
        "id": BUNDLE_ID,
        "upload": {"url": f"{stub.url}/upload/slot", "method": "PUT",
                   "headers": {"x-probe-upload": "capability-abc", "content-type": "application/zip"}},
        "expires_at": "2026-10-23T20:00:00Z",
    }, {})
    stub.routes[("PUT", "/upload/slot")] = (put_status, {}, {})
    stub.routes[("POST", f"{debug_bundle.ROUTE}/{BUNDLE_ID}/complete")] = (
        complete_status, {"id": BUNDLE_ID, "bytes": 0} if complete_status == 200 else {"detail": "no"}, {})


def _small_bundle(tmp_path) -> debug_bundle.Bundle:
    collection = debug_bundle.Collection(started_at=time.time(), harnesses=["claude_code"], session_ids=[SID])
    collection.files["probe/x.txt"] = debug_bundle.Entry(b"hello\n")
    return debug_bundle.build(out_dir=tmp_path, collection=collection)


@pytest.fixture
def signed_in(monkeypatch, stub):
    from probe.sdk.config import save_context

    monkeypatch.setenv("PROBE_BASE_URL", stub.url)
    save_context({"base_url": stub.url, "token": CLI_TOKEN, "companion_token": DAEMON_KEY})
    return stub


def test_a_send_creates_puts_exactly_as_told_and_completes(signed_in, tmp_path, monkeypatch):
    monkeypatch.setenv(debug_bundle.APP_VERSION_ENV, "0.1.48")
    _slot(signed_in)
    bundle = _small_bundle(tmp_path)
    result = debug_bundle.send(bundle)
    assert result == {"id": BUNDLE_ID, "bytes": bundle.bytes, "files": bundle.files, "skipped": [],
                      "path": str(bundle.path)}
    create, put, complete = signed_in.requests
    body = json.loads(create["body"])
    assert body == {"schema": 1, "bytes": bundle.bytes, "sha256": hashlib.sha256(bundle.path.read_bytes()).hexdigest(),
                    "cli_version": body["cli_version"], "app_version": "0.1.48", "os": report.os_label(),
                    "harnesses": ["claude_code"], "session_ids": [SID]}
    assert create["headers"]["Authorization"] == f"Bearer {CLI_TOKEN}"
    assert (put["method"], put["path"]) == ("PUT", "/upload/slot")
    assert put["headers"]["x-probe-upload"] == "capability-abc"
    assert put["headers"]["content-type"] == "application/zip"
    assert "Authorization" not in put["headers"]  # the slot carries its own capability
    assert put["body"] == bundle.path.read_bytes()
    assert complete["path"] == f"{debug_bundle.ROUTE}/{BUNDLE_ID}/complete"
    assert complete["headers"]["Authorization"] == f"Bearer {CLI_TOKEN}"


@pytest.mark.parametrize(("where", "status", "headers", "error"), [
    ("create", 429, {"Retry-After": "120"}, "rate_limited"),
    ("create", 413, {}, "too_large"),
    ("create", 422, {}, "server"),
    ("create", 501, {}, "server"),
    ("put", 401, {}, "server"),
    ("put", 403, {}, "server"),
    ("put", 408, {}, "server"),
    ("put", 413, {}, "too_large"),
    ("put", 422, {}, "too_large"),
    ("put", 503, {}, "server"),
    ("complete", 409, {}, "server"),
    ("complete", 422, {}, "server"),
])
def test_each_refusal_maps_to_the_contracts_kind_and_keeps_the_zip(signed_in, tmp_path, where, status, headers,
                                                                   error):
    _slot(signed_in)
    route = {"create": ("POST", debug_bundle.ROUTE), "put": ("PUT", "/upload/slot"),
             "complete": ("POST", f"{debug_bundle.ROUTE}/{BUNDLE_ID}/complete")}[where]
    signed_in.routes[route] = (status, {"detail": "no"}, headers)
    bundle = _small_bundle(tmp_path)
    result = debug_bundle.send(bundle)
    assert result == {"error": error, "status": status, "retry_after": 120.0 if headers else None,
                      "path": str(bundle.path)}
    assert bundle.path.is_file()


def test_offline_is_offline(signed_in, tmp_path, monkeypatch):
    bundle = _small_bundle(tmp_path)
    monkeypatch.setenv("PROBE_BASE_URL", f"http://127.0.0.1:{_closed_port()}")
    assert debug_bundle.send(bundle) == {"error": "offline", "status": None, "retry_after": None,
                                         "path": str(bundle.path)}


def test_refused_with_both_credentials_is_unauthorized(signed_in, tmp_path):
    signed_in.routes[("POST", debug_bundle.ROUTE)] = (401, {"detail": "invalid token"}, {})
    result = debug_bundle.send(_small_bundle(tmp_path))
    assert (result["error"], result["status"]) == ("unauthorized", 401)
    assert [r["headers"]["Authorization"].split()[-1] for r in signed_in.requests] == [CLI_TOKEN, DAEMON_KEY]


# ---------------------------------------------------------------------------
# The CLI the desktop app runs
# ---------------------------------------------------------------------------


def _cli(args: list[str]):
    main = importlib.import_module("probe.cli.main")
    return CliRunner().invoke(main.app, args)


def _quick(monkeypatch) -> None:
    monkeypatch.setattr(debug_bundle, "_sources", lambda: [("probe", debug_bundle._probe_files)])


def test_bundle_send_json_prints_the_contracts_last_line(signed_in, tmp_path, monkeypatch):
    _quick(monkeypatch)
    _slot(signed_in)
    result = _cli(["doctor", "--bundle", "--send", "--json", "--out", str(tmp_path)])
    assert result.exit_code == 0, result.output
    last = json.loads(result.stdout.strip().splitlines()[-1])
    assert set(last) == {"id", "bytes", "files", "skipped", "path"} and last["id"] == BUNDLE_ID
    assert Path(last["path"]).parent == tmp_path


def test_bundle_send_json_failure_exits_1_with_the_error_object(signed_in, tmp_path, monkeypatch):
    _quick(monkeypatch)
    signed_in.routes[("POST", debug_bundle.ROUTE)] = (429, {"detail": "slow"}, {"Retry-After": "30"})
    result = _cli(["doctor", "--bundle", "--send", "--json", "--out", str(tmp_path)])
    assert result.exit_code == 1
    last = json.loads(result.stdout.strip().splitlines()[-1])
    assert last == {"error": "rate_limited", "status": 429, "retry_after": 30.0, "path": last["path"]}
    assert Path(last["path"]).is_file()


def test_bundle_alone_only_saves(signed_in, monkeypatch):
    _quick(monkeypatch)
    result = _cli(["doctor", "--bundle"])
    assert result.exit_code == 0, result.output
    assert "Saved the debug log to " in result.output
    assert signed_in.requests == []
    assert list(debug_bundle.default_dir().glob("probe-debug-*.zip"))


def test_bundle_flags_need_bundle():
    assert _cli(["doctor", "--json"]).exit_code == 2
    assert _cli(["doctor", "--out", "/tmp"]).exit_code == 2


# ---------------------------------------------------------------------------
# Review of #3326: each of these failed on 1bd55e3f4
# ---------------------------------------------------------------------------


def _only(monkeypatch, *names: str) -> None:
    sources = dict(debug_bundle._sources())
    monkeypatch.setattr(debug_bundle, "_sources", lambda: [(n, sources[n]) for n in names])


def test_the_log_is_filed_under_every_session_and_agent_it_holds(fake_machine, monkeypatch):
    """Not only the sessions live at that moment: a recent session it has a folder for, and each
    coding agent whose folder it filled, so staff find the log from any of them (live run 10-23:
    11 session folders, 1 session id, no agents)."""
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID", raising=False)
    recent = "0b6f2c1e-5a4d-4b8e-9f10-2c3d4e5f6a7b"
    daemon = report.state_root() / "daemon"
    daemon.mkdir(parents=True, exist_ok=True)
    (daemon / f"{recent}.log").write_text("worker started\n")
    _only(monkeypatch, "sessions", *(f"agent_{h.id}" for h in get_registry().all()))
    collection = debug_bundle.collect()
    assert any(path.startswith(f"sessions/{recent}/") for path in collection.files)
    assert recent in collection.session_ids
    # Claude Code (binary, settings, a transcript) and Codex (settings only), never an agent that
    # is not on the machine: every registered agent's folder holds `facts.json` and
    # `transcripts.json`, so counting a filled folder named all 4 on every log.
    assert {f"agents/{h.id}/facts.json" for h in get_registry().captured()} <= set(collection.files)
    assert collection.harnesses == ["claude_code", "codex"]


def test_an_agent_with_only_a_recent_transcript_is_named():
    files = {f"agents/{h}/{name}": debug_bundle.Entry(b"[]\n")
             for h in ("claude_code", "codex") for name in ("facts.json", "transcripts.json")}
    files["agents/codex/transcripts.json"] = debug_bundle.Entry(b'[{"path": "rollout.jsonl"}]\n')
    assert debug_bundle._harnesses_with_files(files) == ["codex"]  # noqa: SLF001


@pytest.mark.parametrize(("answer", "named"), [
    ("exit 0\ncodex-cli 0.50.0\n", ["codex"]),
    ("exit 126\npermission denied\n", []),
    ("timed out after 10 s\n", []),
    ("not found\n", []),
])
def test_a_version_names_the_agent_only_when_its_program_answered(answer, named):
    """A broken launcher on PATH is not the agent installed."""
    files = {"agents/codex/facts.json": debug_bundle.Entry(b"{}\n"),
             "agents/codex/transcripts.json": debug_bundle.Entry(b"[]\n"),
             "agents/codex/version.txt": debug_bundle.Entry(f"$ codex --version\n{answer}".encode())}
    assert debug_bundle._harnesses_with_files(files) == named  # noqa: SLF001


#: The real sniff, before conftest's `_no_ambient_pi_binary` pins it off for every test.
_REAL_PI_BINARY_AVAILABLE = pi_config.pi_binary_available


@pytest.mark.parametrize(("help_line", "named"), [("pi - AI coding assistant", ["pi"]), ("pi - digits of pi", [])])
def test_another_packages_pi_is_not_the_agent(fake_machine, monkeypatch, tmp_path, help_line, named):
    """`pi` is two letters: CLN's digits-of-pi program on PATH names no agent, as in the wizard."""
    fake = tmp_path / "bin" / "pi"
    fake.write_text(f"#!/bin/sh\necho '{help_line}'\n")
    fake.chmod(0o755)
    monkeypatch.setattr(pi_config, "pi_binary_available", _REAL_PI_BINARY_AVAILABLE)
    _REAL_PI_BINARY_AVAILABLE.cache_clear()
    _only(monkeypatch, "agent_pi")
    try:
        collection = debug_bundle.collect()
    finally:
        _REAL_PI_BINARY_AVAILABLE.cache_clear()
    assert collection.harnesses == named
    assert ("agents/pi/version.txt" in collection.files) == bool(named)


def test_processes_are_this_users_and_keep_only_program_and_flag_names(fake_machine, monkeypatch, tmp_path):
    prompt = "refactor the billing module for ACME"
    child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)", "probe-fake-agent", "-p", prompt,
                              "-phunter2Secret", "--password", "pw-12345678"])
    try:
        _only(monkeypatch, "processes")
        files = _unzipped(debug_bundle.build(out_dir=tmp_path).path)
    finally:
        child.kill()
        child.wait()
    text = files["system/processes.json"]
    assert prompt not in text and "hunter2Secret" not in text and "pw-12345678" not in text
    (row,) = [p for p in json.loads(text) if p["pid"] == child.pid]
    # macOS framework Pythons run as `.../Python.app/Contents/MacOS/Python`, not as the venv's `python`.
    assert row["cmdline"][0].lower().startswith("python")
    assert row["cmdline"][1:] == ["-c", "<arg>", "<arg>", "-p", "<arg>", "-p<arg>",
                              "--password", "<arg>"]


def test_another_users_processes_are_left_out(monkeypatch):
    """A shared node: another user's agent and its prompt are not ours to send.
    (psutil's process list stood in for: the suite cannot start another user's process.)"""
    from types import SimpleNamespace

    import psutil

    other = SimpleNamespace(info={
        "pid": 4242, "ppid": 1, "name": "claude", "create_time": 0.0, "memory_info": None,
        "cmdline": ["claude", "-p", "someone else's prompt"],
        "uids": SimpleNamespace(real=os.getuid() + 1 if hasattr(os, "getuid") else 1),
        "username": "someone-else",
    })
    monkeypatch.setattr(psutil, "process_iter", lambda attrs=None: iter([other]))
    sink = debug_bundle.Sink()
    debug_bundle._processes(sink)
    assert json.loads(sink.files["system/processes.json"].data) == []


def test_a_config_that_does_not_parse_is_listed_never_written(fake_machine, tmp_path, monkeypatch):
    home = Path.home()
    (home / ".claude.json").write_text(
        '{"oauthAccount": {"emailAddress": "someone@example.test"}, '
        '"projects": {"/p": {"history": [{"display": "a private prompt"}]}},}')  # trailing comma
    (home / ".codex" / "config.toml").write_text('model = "gpt-5"\n[broken\nnote = "a private note"\n')
    _only(monkeypatch, "agent_claude_code", "agent_codex")
    files = _unzipped(debug_bundle.build(out_dir=tmp_path).path)
    every = "\n".join(files.values())
    assert "someone@example.test" not in every and "a private prompt" not in every and "a private note" not in every
    listing = json.loads(files["agents/claude_code/claude.json.listing.json"])
    assert listing["not_parsed"] and listing["bytes"] > 0
    assert "agents/codex/home/config.toml.listing.json" in files


def test_a_big_config_is_parsed_whole_not_tailed(fake_machine, tmp_path, monkeypatch):
    """`~/.claude.json` past the 5 MiB log tail: read whole, so its OAuth block
    and prompt history are found by key, not left to a text scrub."""
    monkeypatch.setattr(debug_bundle, "FILE_CAP", 1024)
    (Path.home() / ".claude.json").write_text(json.dumps({
        "oauthAccount": {"emailAddress": "someone@example.test"},
        "projects": {f"/p{i}": {"history": [{"display": f"private prompt {i}"}], "lastCost": i}
                     for i in range(200)},
    }))
    _only(monkeypatch, "agent_claude_code")
    files = _unzipped(debug_bundle.build(out_dir=tmp_path).path)
    clean = json.loads(files["agents/claude_code/claude.json"])
    assert clean["oauthAccount"] == "<redacted>" and clean["projects"]["/p199"]["lastCost"] == 199
    assert "private prompt" not in files["agents/claude_code/claude.json"]


def test_credentials_under_unusual_names_args_and_headers_never_reach_the_zip(fake_machine, tmp_path, monkeypatch):
    (Path.home() / ".claude" / "settings.json").write_text(json.dumps({
        "mcpServers": {"supabase": {"command": "npx", "args": ["-y", "@supabase/mcp", "--access-token",
                                                               "sbp_" + SECRETS[1]]}},
        "env": {"DB_PASS": SECRETS[2], "MYSQL_PWD": SECRETS[3], "GH_PAT": SECRETS[4],
                "ANTHROPIC_CUSTOM_HEADERS": f"X-Gateway-Key: {SECRETS[5]}"},
    }))
    monkeypatch.setenv("OTEL_EXPORTER_OTLP_HEADERS", f"x-honeycomb-team={SECRETS[6]}")
    _only(monkeypatch, "agent_claude_code", "env_this_command")
    files = _unzipped(debug_bundle.build(out_dir=tmp_path).path)
    every = "\n".join(files.values())
    for n in range(1, 7):
        assert SECRETS[n] not in every, n
    settings = json.loads(files["agents/claude_code/home/settings.json"])
    assert settings["env"]["ANTHROPIC_CUSTOM_HEADERS"] == "<redacted>"
    assert json.loads(files["system/env-this-command.json"])["OTEL_EXPORTER_OTLP_HEADERS"] == (
        "x-honeycomb-team=<redacted>")


def test_a_slow_file_keeps_the_files_before_it_and_stops_the_rest(fake_machine, monkeypatch):
    reached = []

    def source(sink):
        sink.text("service/first.log", "first\n", log=True)
        time.sleep(1.5)  # one file that takes too long
        sink.text("service/second.log", "second\n", log=True)
        reached.append("after second")

    monkeypatch.setattr(debug_bundle, "_sources", lambda: [("slow", source)])
    collection = debug_bundle.collect(source_budget_s=0.4)
    assert "service/first.log" in collection.files and "service/second.log" not in collection.files
    assert collection.skipped["slow"].startswith("stopped")
    time.sleep(1.6)
    assert reached == []  # the abandoned source stopped at its next file


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="no FIFOs here")
def test_a_fifo_where_a_file_should_be_never_blocks_a_source(fake_machine, monkeypatch):
    state = report.state_root()
    (state / "daemon-errors.log").unlink()
    os.mkfifo(state / "daemon-errors.log")
    (state / "reasoning-summaries.json").write_text('{"claude_code": "on"}')
    _only(monkeypatch, "daemon")
    collection = debug_bundle.collect(source_budget_s=2.0)
    assert "daemon" not in collection.skipped
    assert "daemon/reasoning-summaries.json" in collection.files


def test_the_combined_cap_is_checked_before_anything_is_sent(signed_in, tmp_path, monkeypatch):
    collection = debug_bundle.Collection(started_at=time.time())
    collection.files["probe/zeros.bin"] = debug_bundle.Entry(b"\0" * 200_000)  # compresses to almost nothing
    bundle = debug_bundle.build(out_dir=tmp_path, collection=collection)
    monkeypatch.setattr(debug_bundle, "RELAY_CAP", 100_000)
    _slot(signed_in)
    result = debug_bundle.send(bundle)
    assert result["error"] == "too_large" and signed_in.requests == []


def test_a_bundle_that_vanished_still_answers_the_contracts_object(signed_in, tmp_path):
    bundle = _small_bundle(tmp_path)
    bundle.path.unlink()
    assert debug_bundle.send(bundle) == {"error": "server", "status": None, "retry_after": None,
                                         "path": str(bundle.path)}


def test_a_broken_tls_setup_still_prints_the_last_line(signed_in, tmp_path, monkeypatch):
    import probe.sdk.tls as tls

    _quick(monkeypatch)
    _slot(signed_in)

    def broken():
        raise OSError("no CA bundle")

    monkeypatch.setattr(tls, "ssl_context", broken)
    result = _cli(["doctor", "--bundle", "--send", "--json", "--out", str(tmp_path)])
    assert result.exit_code == 1
    last = json.loads(result.stdout.strip().splitlines()[-1])
    assert last["error"] in ("offline", "server") and set(last) == {"error", "status", "retry_after", "path"}


def test_an_expired_upload_says_so(signed_in, tmp_path, monkeypatch):
    _quick(monkeypatch)
    _slot(signed_in, put_status=401)
    result = _cli(["doctor", "--bundle", "--send", "--out", str(tmp_path)])
    assert result.exit_code == 1
    assert "the upload expired; try again" in result.output and "not signed in" not in result.output


# ---------------------------------------------------------------------------
# Delta review of 8eccea95b: each of these failed on 8eccea95b
# ---------------------------------------------------------------------------


def test_an_expired_upload_is_a_retry_for_the_app(signed_in, tmp_path, monkeypatch):
    """A 401 on the PUT is the slot expiring, not the login: the app's word is
    `server` (try again), never `unauthorized` (sign in again)."""
    _quick(monkeypatch)
    _slot(signed_in, put_status=401)
    result = _cli(["doctor", "--bundle", "--send", "--json", "--out", str(tmp_path)])
    assert result.exit_code == 1
    last = json.loads(result.stdout.strip().splitlines()[-1])
    assert (last["error"], last["status"]) == ("server", 401)


def test_a_transcript_deleted_mid_scan_costs_only_itself(fake_machine, monkeypatch):
    """An agent pruning its old sessions while the log is built: the file is gone between the
    listing and the read of its date. The agent's other transcripts, facts and settings stay."""
    projects = Path.home() / ".claude" / "projects" / "-work-proj"
    pruned = projects / "pruned.jsonl"
    pruned.write_text(json.dumps({"type": "user"}) + "\n")
    listed = Path.is_file

    def is_file(self, *args, **kwargs):
        found = listed(self, *args, **kwargs)
        if found and self == pruned:
            self.unlink()
        return found

    monkeypatch.setattr(Path, "is_file", is_file)
    _only(monkeypatch, "agent_claude_code")
    collection = debug_bundle.collect()
    assert "agent_claude_code" not in collection.skipped
    transcripts = json.loads(collection.files["agents/claude_code/transcripts.json"].data)
    assert [Path(t["path"]).name for t in transcripts] == [f"{SID}.jsonl"]
    assert "agents/claude_code/home/settings.json" in collection.files
    assert collection.harnesses == ["claude_code"]


def test_a_transcript_deleted_after_its_date_is_read_gives_its_slot_up(fake_machine, monkeypatch):
    """Gone by the time it is described: the next newest transcript takes its place."""
    projects = Path.home() / ".claude" / "projects" / "-work-proj"
    pruned = projects / "pruned.jsonl"
    pruned.write_text(json.dumps({"type": "user"}) + "\n")
    os.utime(pruned, (time.time() + 60, time.time() + 60))
    described = debug_bundle.describe

    def describe(path):
        if path == pruned:
            path.unlink()
        return described(path)

    monkeypatch.setattr(debug_bundle, "describe", describe)
    monkeypatch.setattr(debug_bundle, "RECENT_TRANSCRIPTS", 1)
    _only(monkeypatch, "agent_claude_code")
    transcripts = json.loads(debug_bundle.collect().files["agents/claude_code/transcripts.json"].data)
    assert [Path(t["path"]).name for t in transcripts] == [f"{SID}.jsonl"]


def _failing_listing(monkeypatch, failures: int) -> None:
    """The transcript folder walk raises for its first `failures` calls, as Python 3.10 and 3.11's
    `glob` do when a session folder is deleted during the walk."""
    left = [failures]
    walk = Path.glob

    def glob(self, pattern, *args, **kwargs):
        if self.name == "projects" and left[0] > 0:
            left[0] -= 1
            raise FileNotFoundError(2, "No such file or directory", str(self / "gone-session"))
        return walk(self, pattern, *args, **kwargs)

    monkeypatch.setattr(Path, "glob", glob)


def test_a_session_folder_deleted_mid_walk_is_listed_again(fake_machine, monkeypatch):
    """An agent deleting a burst of session folders can fail the walk more than once."""
    _failing_listing(monkeypatch, 2)
    _only(monkeypatch, "agent_claude_code")
    transcripts = json.loads(debug_bundle.collect().files["agents/claude_code/transcripts.json"].data)
    assert [Path(t["path"]).name for t in transcripts] == [f"{SID}.jsonl"]


def test_a_listing_that_keeps_failing_says_so_and_keeps_the_rest(fake_machine, monkeypatch):
    """Never an empty list that reads as an agent with no sessions."""
    _failing_listing(monkeypatch, 3)
    _only(monkeypatch, "agent_claude_code")
    collection = debug_bundle.collect()
    assert json.loads(collection.files["agents/claude_code/transcripts.json"].data) == []
    assert any(n.startswith("agents/claude_code/transcripts.json: not listed (FileNotFoundError)")
               for n in collection.notes)
    assert "agents/claude_code/home/settings.json" in collection.files


def test_a_settings_folder_gone_after_its_check_costs_only_its_files(fake_machine, monkeypatch):
    """The agent uninstalled while the log is built: its folder listing fails, the rest stays."""
    claude = Path.home() / ".claude"
    listing = Path.iterdir

    def iterdir(self):
        if self == claude:
            raise FileNotFoundError(2, "No such file or directory", str(self))
        return listing(self)

    monkeypatch.setattr(Path, "iterdir", iterdir)
    _only(monkeypatch, "agent_claude_code")
    collection = debug_bundle.collect()
    assert "agent_claude_code" not in collection.skipped
    assert "agents/claude_code/claude.json" in collection.files
    assert "agents/claude_code/home: not listed (FileNotFoundError)" in collection.notes


def test_an_action_record_gone_after_its_date_is_read_gives_its_slot_up(fake_machine, monkeypatch):
    """Not written into the log as an empty file: the next newest record takes its place."""
    from probe.service import paths

    actions = paths.service_dir() / paths.ACTIONS_DIRNAME
    actions.mkdir(parents=True)
    (actions / "kept.log").write_text("update finished\n")
    (actions / "gone.json").write_text("{}\n")
    os.utime(actions / "gone.json", (time.time() + 60, time.time() + 60))
    monkeypatch.setattr(debug_bundle, "RECENT_ACTIONS", 1)
    dated = report.newest_first

    def newest_first(found):
        listed = dated(found)
        if (actions / "gone.json") in listed:
            (actions / "gone.json").unlink()
        return listed

    monkeypatch.setattr(report, "newest_first", newest_first)
    _only(monkeypatch, "service_files")
    files = debug_bundle.collect().files
    assert "service/actions/kept.log" in files
    assert "service/actions/gone.json" not in files


@pytest.mark.skipif(os.name != "posix" or os.geteuid() == 0, reason="needs a folder this user cannot enter")
def test_an_agent_folder_this_user_cannot_enter_costs_only_what_is_in_it(fake_machine, monkeypatch):
    """`sudo claude` leaves `~/.claude` root-owned: the agent's version and facts are kept and the
    notes say its folder could not be listed."""
    claude = Path.home() / ".claude"
    claude.chmod(0)
    try:
        _only(monkeypatch, "agent_claude_code")
        collection = debug_bundle.collect()
    finally:
        claude.chmod(0o755)
    assert "agent_claude_code" not in collection.skipped
    assert "agents/claude_code/facts.json" in collection.files
    assert "agents/claude_code/home: not listed (PermissionError)" in collection.notes


def test_a_huge_agent_config_never_costs_the_agents_transcripts(fake_machine, monkeypatch):
    """The cheap facts (version, transcripts) are written before the configs: a
    config that stalls its step loses itself, not them."""
    (Path.home() / ".claude.json").write_text(json.dumps(
        {"projects": {f"/p{i}": {"note": f"value {i}", "more": [f"a{i}", f"b{i}"]} for i in range(60000)}}))
    _only(monkeypatch, "agent_claude_code")
    collection = debug_bundle.collect(source_budget_s=0.3)
    assert collection.skipped["agent_claude_code"].startswith("stopped")
    assert "agents/claude_code/transcripts.json" in collection.files
    assert "agents/claude_code/facts.json" in collection.files


def test_the_docs_describe_the_command_line_rule():
    readme_rule = "command lines keep only the program and flag names"
    def flat(text: str) -> str:
        return " ".join(text.split())

    assert readme_rule in flat(debug_bundle.__doc__)
    collection = debug_bundle.Collection(started_at=time.time())
    assert readme_rule in flat(debug_bundle._readme(collection, {}))
