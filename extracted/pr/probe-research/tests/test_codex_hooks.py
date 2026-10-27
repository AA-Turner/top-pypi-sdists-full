"""`probe doctor` asks Codex which of Probe's hooks it will run.

Codex skips a hooks.json entry it has not approved without a word, and a Probe
update that changes an entry needs approval again: nothing of Probe's runs to
report it. The fixture is a real `hooks/list` answer recorded from codex-cli
0.159.2 on 2026-10-05 (commands truncated, home path renamed), so the shape the
summary reads is Codex's, not ours.
"""

from __future__ import annotations

import copy
import json
import os
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

from probe.cli import codex_hooks, doctor, setup, updater
from probe.cli.capabilities import Capabilities

FIXTURE = json.loads((Path(__file__).parent / "fixtures" / "codex_hooks_list_0.159.2.json").read_text())
RESULT = FIXTURE["result"]
#: conftest stands every test's `approve` and the wizard's `codex_hooks_waiting`
#: in for ones that cannot ask Codex: these are the real ones.
APPROVE = codex_hooks.approve
WAITING = setup.codex_hooks_waiting


def _result(mutate=None) -> dict:
    result = copy.deepcopy(RESULT)
    if mutate:
        mutate(result["data"][0]["hooks"])
    return result


def test_the_recorded_answer_reads_as_all_approved():
    found = codex_hooks.summarize(_result())
    assert found is not None
    assert found.total == len(RESULT["data"][0]["hooks"]) > 20
    assert found.untrusted == ()
    # The "1 issue loading hooks" banner: the tap's 20s SessionEnd entry, which
    # Codex clamps to 3s. By design (Claude Code needs the 20s), so not a fault
    # doctor shows every Codex user.
    assert found.warnings == ()


def test_any_other_probe_warning_is_shown():
    result = _result()
    result["data"][0]["warnings"] = ["ignoring hooks in /x/plugins/cache/m/probe-research-daemon/1.0.0/hooks/hooks.json: bad"]
    assert codex_hooks.summarize(result).warnings == tuple(result["data"][0]["warnings"])


def test_an_unapproved_hook_is_counted_and_named():
    def untrust(hooks):
        for hook in hooks:
            if hook["key"].startswith("probe-research-daemon@") and hook["eventName"] == "preToolUse":
                hook["trustStatus"] = "untrusted"

    found = codex_hooks.summarize(_result(untrust))
    assert found.untrusted and all(k.startswith("probe-research-daemon@") for k in found.untrusted)
    rows = "\n".join(codex_hooks.rows(found, doctor._row))
    assert f"{len(found.untrusted)} of {found.total} switched off until approved" in rows
    assert "/hooks" in rows and "probe-research-daemon" in rows


def test_a_disabled_hook_is_not_a_hook_codex_should_run():
    def disable(hooks):
        hooks[0]["enabled"] = False
        hooks[0]["trustStatus"] = "untrusted"

    found = codex_hooks.summarize(_result(disable))
    assert found.untrusted == ()
    assert found.total == len(RESULT["data"][0]["hooks"]) - 1


def test_other_plugins_hooks_are_not_counted():
    def foreign(hooks):
        hooks.append({**hooks[0], "key": "posthog@posthog:hooks/hooks.json:stop:0:0", "trustStatus": "untrusted"})

    assert codex_hooks.summarize(_result(foreign)).untrusted == ()


@pytest.mark.parametrize(
    "shape",
    [{}, {"data": "x"}, {"data": [{"hooks": [{"nokey": 1}]}]}, {"data": ["x"]}, {"data": [{"hooks": 5}]}, {"data": [{"warnings": 5}]}],
)
def test_an_unknown_shape_is_unknown_not_all_clear(shape):
    assert codex_hooks.summarize(shape) is None
    assert "unknown" in "\n".join(codex_hooks.rows(None, doctor._row))


def test_no_codex_on_path_is_unknown(monkeypatch):
    monkeypatch.setattr(codex_hooks.shutil, "which", lambda _name: None)
    assert codex_hooks.list_hooks() is None
    assert codex_hooks.status() is None


def test_a_codex_that_never_answers_is_bounded(monkeypatch, tmp_path):
    """An older Codex without hooks/list, or one stuck at start: give up, never hang doctor."""
    fake = tmp_path / "codex"
    fake.write_text("#!/bin/sh\nsleep 30\n", encoding="utf-8")
    fake.chmod(0o755)
    monkeypatch.setattr(codex_hooks.shutil, "which", lambda _name: str(fake))
    assert codex_hooks.list_hooks(timeout=0.5) is None


def test_an_error_answer_is_unknown(monkeypatch, tmp_path):
    fake = tmp_path / "codex"
    fake.write_text(
        "#!/bin/sh\nwhile read -r line; do case \"$line\" in *'\"id\": 2'*|*'\"id\":2'*) "
        "echo '{\"jsonrpc\":\"2.0\",\"id\":2,\"error\":{\"code\":-32601,\"message\":\"no\"}}';; esac; done\n",
        encoding="utf-8",
    )
    fake.chmod(0o755)
    monkeypatch.setattr(codex_hooks.shutil, "which", lambda _name: str(fake))
    assert codex_hooks.list_hooks(timeout=5) is None


def test_a_real_shaped_answer_round_trips(monkeypatch, tmp_path):
    """The client half: requests go out, the id-2 answer comes back as its result."""
    answer = tmp_path / "answer.json"
    answer.write_text(json.dumps({"jsonrpc": "2.0", "id": 2, "result": RESULT}), encoding="utf-8")
    fake = tmp_path / "codex"
    fake.write_text(
        f"#!/bin/sh\nwhile read -r line; do case \"$line\" in *hooks/list*) cat '{answer}'; echo;; esac; done\n",
        encoding="utf-8",
    )
    fake.chmod(0o755)
    monkeypatch.setattr(codex_hooks.shutil, "which", lambda _name: str(fake))
    assert codex_hooks.list_hooks(timeout=5) == RESULT


def test_doctor_shows_the_section_only_when_given():
    caps = Capabilities(agent_source="codex", codex_available=True)
    rows = codex_hooks.rows(codex_hooks.summarize(_result()), doctor._row)
    with_rows = doctor.render(caps, codex_hooks=rows)
    assert "Codex hooks" in with_rows and "approved" in with_rows
    assert "Codex hooks" not in doctor.render(caps)


@pytest.mark.parametrize("source", ["codex", "claude_code"])
def test_doctor_does_not_ask_codex_without_codex(monkeypatch, source):
    monkeypatch.setattr(codex_hooks, "status", lambda *a, **k: pytest.fail("asked Codex"))
    assert doctor.codex_hook_rows(Capabilities(agent_source=source, codex_available=False)) == []


def test_doctor_asks_codex_from_a_claude_code_report_too(monkeypatch):
    """A plain terminal reports for Claude Code, and that is where someone runs it."""
    monkeypatch.setattr(codex_hooks, "status", lambda *a, **k: codex_hooks.summarize(_result()))
    assert doctor.codex_hook_rows(Capabilities(agent_source="claude_code", codex_available=True))[0] == "Codex hooks"


def test_giving_up_ends_the_app_server_a_launcher_started(monkeypatch, tmp_path):
    """A `codex` launcher that does not exec leaves its child behind a plain kill."""
    marker = tmp_path / "server-alive"
    fake = tmp_path / "codex"
    fake.write_text(f"#!/bin/sh\n(sleep 2; touch {marker}) &\nwait\n", encoding="utf-8")
    fake.chmod(0o755)
    monkeypatch.setattr(codex_hooks.shutil, "which", lambda _name: str(fake))
    assert codex_hooks.list_hooks(timeout=0.3) is None
    import time

    time.sleep(2.5)
    assert not marker.exists(), "the launcher's child outlived doctor's timeout"


def test_doctor_asks_codex_for_a_codex_report(monkeypatch):
    found = codex_hooks.summarize(_result())
    monkeypatch.setattr(codex_hooks, "status", lambda *a, **k: found)
    rows = doctor.codex_hook_rows(Capabilities(agent_source="codex", codex_available=True))
    assert rows[0] == "Codex hooks" and f"all {found.total} approved" in rows[1]


# -- `probe status`: Codex's answer, cached, and the heartbeat ------------------

MARKET = "research-os-agent"
TAP_END = f"probe-research-tap@{MARKET}:hooks/hooks.json:sessionEnd:0:0"
TAP_START = f"probe-research-tap@{MARKET}:hooks/hooks.json:sessionStart:0:0"
SID = "019a0b1c-2d3e-7f40-8152-637485960a1b"


def _answer(**trust: str) -> dict:
    keys = {"end": TAP_END, "start": TAP_START}
    return {"data": [{"hooks": [{"key": keys[k], "trustStatus": v, "enabled": True} for k, v in trust.items()],
                      "warnings": []}]}


@pytest.fixture
def device(tmp_path, monkeypatch):
    """A home of its own: Codex's folder, the CLI's state, and a `codex` that
    logs each start and answers hooks/list with what `answering` set."""
    home = tmp_path / "home"
    (home / ".codex").mkdir(parents=True)
    (home / ".codex" / "config.toml").write_text(f'[plugins."probe-research-tap@{MARKET}"]\nenabled = true\n')
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("CODEX_HOME", raising=False)
    monkeypatch.setenv("XDG_STATE_HOME", str(home / ".local" / "state"))
    calls = tmp_path / "calls.log"
    calls.touch()
    answer = tmp_path / "answer.json"
    fake = tmp_path / "codex"
    fake.write_text(
        f"#!/bin/sh\necho \"codex $*\" >> '{calls}'\n"
        f"while read -r line; do case \"$line\" in *hooks/list*) "
        f"printf '{{\"jsonrpc\":\"2.0\",\"id\":2,\"result\":%s}}\\n' \"$(cat '{answer}')\";; esac; done\n",
        encoding="utf-8",
    )
    fake.chmod(0o755)
    state = SimpleNamespace(home=home, calls=calls, fake=fake, binary=str(fake))

    def answering(result: dict) -> None:
        answer.write_text(json.dumps(result), encoding="utf-8")

    state.answering = answering
    state.asked = lambda: calls.read_text().splitlines()
    monkeypatch.setattr(codex_hooks, "codex_binary", lambda: state.binary)
    answering(_answer(end="untrusted", start="trusted"))
    return state


def _install(device, *versions: str, plugin: str = "probe-research-tap") -> None:
    for version in versions:
        (device.home / ".codex" / "plugins" / "cache" / MARKET / plugin / version).mkdir(parents=True)


def _expect(device, sid: str, flag: str, *, age: float, alive: bool = False) -> None:
    hooks = device.home / ".local" / "state" / "probe" / "hooks"
    (hooks / "expect").mkdir(parents=True, exist_ok=True)
    record = hooks / "expect" / sid
    record.write_text(flag + "\n")
    os.utime(record, (time.time() - age,) * 2)
    if alive:
        (hooks / "alive").mkdir(parents=True, exist_ok=True)
        (hooks / "alive" / sid).touch()


def test_status_asks_nothing_where_codex_has_no_probe_plugin(device):
    assert codex_hooks.status_snapshot() == codex_hooks.blank_snapshot(codex_hooks.HooksState.NONE)
    assert device.asked() == []


def test_status_names_the_hooks_waiting_for_approval_and_keeps_the_answer(device):
    _install(device, "0.9.25")
    first = codex_hooks.status_snapshot()
    assert first["state"] == "needs_approval" and first["untrusted"] == [TAP_END]
    assert isinstance(first["checked_at"], int)
    assert device.asked() == ["codex app-server"]
    assert codex_hooks.status_snapshot() == first, "the cached answer"
    assert device.asked() == ["codex app-server"], "asked once per TTL"
    line = codex_hooks.status_line(first)
    assert "1 Probe hook switched off" in line and "/hooks" in line


def test_an_update_an_approval_or_the_ttl_asks_again(device):
    _install(device, "0.9.25")
    codex_hooks.status_snapshot()
    _install(device, "0.9.26")
    device.answering(_answer(end="trusted", start="trusted"))
    assert codex_hooks.status_snapshot()["state"] == "approved", "a new Probe version is asked about"
    assert len(device.asked()) == 2
    config = device.home / ".codex" / "config.toml"
    os.utime(config, (time.time() + 5,) * 2)
    device.answering(_answer(end="untrusted", start="trusted"))
    assert codex_hooks.status_snapshot()["state"] == "needs_approval", "Codex's config moved: an approval, maybe"
    assert len(device.asked()) == 3
    assert codex_hooks.status_snapshot(now=time.time() + codex_hooks.STATUS_TTL_S + 1)["state"] == "needs_approval"
    assert len(device.asked()) == 4, "older than the TTL"


def test_a_hung_codex_costs_status_its_timeout_once(device):
    _install(device, "0.9.25")
    device.fake.write_text(f"#!/bin/sh\necho \"codex $*\" >> '{device.calls}'\nexec sleep 30\n", encoding="utf-8")
    started = time.monotonic()
    assert codex_hooks.status_snapshot()["state"] == "unknown"
    assert time.monotonic() - started < codex_hooks.STATUS_TIMEOUT_S + 1.5
    started = time.monotonic()
    assert codex_hooks.status_snapshot()["state"] == "unknown"
    assert time.monotonic() - started < 0.5 and len(device.asked()) == 1, "not waited on again within the TTL"


def test_no_codex_binary_reads_the_heartbeat_alone(device):
    _install(device, "0.9.25")
    device.binary = None
    _expect(device, SID, "1", age=120)
    found = codex_hooks.status_snapshot()
    assert (found["state"], found["unheard_session"], found["checked_at"]) == ("needs_approval", SID, None)
    assert device.asked() == []
    assert "Probe's hooks are off" in codex_hooks.status_line(found)


@pytest.mark.parametrize(
    "records, unheard",
    [
        ([(SID, "1", 120, True)], None),
        ([(SID, "1", 5, False)], None),  # inside the grace: its heartbeat may still be coming
        ([(SID, "0", 120, False)], None),  # started before the hooks moved behind dispatch.sh
        ([(SID, "1", codex_hooks.HEARTBEAT_WINDOW_S + 60, False)], None),
        ([("older", "1", 600, False), (SID, "1", 120, True)], None),  # the newest one heard them
        ([("older", "1", 600, True), (SID, "1", 120, False), ("newest-off", "0", 90, False)], SID),
    ],
    ids=["heard", "too-young", "not-expected", "too-old", "newest-heard", "newest-expecting-unheard"],
)
def test_the_heartbeat_rule(device, records, unheard):
    for sid, flag, age, alive in records:
        _expect(device, sid, flag, age=age, alive=alive)
    (device.home / ".local" / "state" / "probe" / "hooks" / "expect" / f"{SID}.shown").write_text("3\n")
    assert codex_hooks.unheard_session() == unheard


def test_codexs_own_answer_decides_over_an_old_unheard_session(device):
    _install(device, "0.9.25")
    device.answering(_answer(end="trusted", start="trusted"))
    _expect(device, SID, "1", age=3600)
    found = codex_hooks.status_snapshot()
    assert (found["state"], found["unheard_session"]) == ("approved", SID)
    assert codex_hooks.status_line(found) == "all approved"


def test_no_enabled_probe_hook_is_none(device):
    _install(device, "0.9.25")
    device.answering({"data": [{"hooks": [], "warnings": []}]})
    assert codex_hooks.status_snapshot()["state"] == "none"
    assert codex_hooks.status_line({"state": "none"}) is None


def test_a_broken_cache_is_asked_again(device):
    _install(device, "0.9.25")
    codex_hooks.status_snapshot()
    cache = device.home / ".local" / "state" / "probe" / codex_hooks.STATUS_CACHE
    good = json.loads(cache.read_text())
    for broken in ("{", "[]", json.dumps({**good, "installed": "x"}), json.dumps({**good, "untrusted": "x"})):
        cache.write_text(broken)
        assert codex_hooks.status_snapshot()["state"] == "needs_approval"
    assert len(device.asked()) == 5


# -- approving Probe's own hooks ---------------------------------------------------
#
# Codex records an approval as `[hooks.state."<key>"] trusted_hash` and its
# app-server's `config/batchWrite` is how it writes one itself. The fake below
# keeps Codex's hook list and its approvals in files: `hooks/list` answers from
# them, `config/batchWrite` records the edits and trusts every key whose
# `trusted_hash` matches that hook's currentHash (Codex's own rule).

FAKE_APP_SERVER = r"""
import json, sys
state, writes, refuse = sys.argv[1], sys.argv[2], sys.argv[3] == "1"
for line in sys.stdin:
    message = json.loads(line)
    method, ident = message.get("method"), message.get("id")
    if method == "hooks/list":
        hooks = json.load(open(state))
        print(json.dumps({"jsonrpc": "2.0", "id": ident, "result": {"data": [{"cwd": "/", "hooks": hooks, "warnings": [], "errors": []}]}}), flush=True)
    elif method == "config/batchWrite":
        with open(writes, "a") as out:
            out.write(json.dumps(message["params"]) + "\n")
        if refuse:
            print(json.dumps({"jsonrpc": "2.0", "id": ident, "error": {"code": -32600, "message": "managed"}}), flush=True)
            continue
        hooks = json.load(open(state))
        for edit in message["params"]["edits"]:
            for hook in hooks:
                if edit["keyPath"] == 'hooks.state."%s".trusted_hash' % hook["key"] and edit["value"] == hook["currentHash"]:
                    hook["trustStatus"] = "trusted"
        json.dump(hooks, open(state, "w"))
        print(json.dumps({"jsonrpc": "2.0", "id": ident, "result": {"status": "ok"}}), flush=True)
"""


def _hook(codex_home: Path, plugin: str, event: str, trust: str = "untrusted", *, market: str = MARKET,
          source: str = "plugin", path: Path | None = None, **extra) -> dict:
    plugin_id = f"{plugin}@{market}"
    where = path or codex_home / "plugins" / "cache" / market / plugin / "0.1.0" / "hooks" / "hooks.json"
    return {
        "key": f"{plugin_id}:hooks/hooks.json:{event}:0:0",
        "pluginId": plugin_id if source == "plugin" else None,
        "source": source,
        "sourcePath": str(where),
        "trustStatus": trust,
        "currentHash": f"sha256:{plugin}-{event}",
        "enabled": True,
        "isManaged": False,
        **extra,
    }


@pytest.fixture
def codex(tmp_path, monkeypatch):
    """A Codex home and a `codex` whose app-server is FAKE_APP_SERVER."""
    home = tmp_path / "codex-home"
    home.mkdir()
    monkeypatch.setenv("CODEX_HOME", str(home))
    server = tmp_path / "server.py"
    server.write_text(FAKE_APP_SERVER, encoding="utf-8")
    state, writes = tmp_path / "hooks.json", tmp_path / "writes.jsonl"
    writes.touch()
    refuse = tmp_path / "refuse"
    fake = tmp_path / "codex"
    fake.write_text(
        f"#!/bin/sh\nexec '{os.sys.executable}' '{server}' '{state}' '{writes}' \"$(cat '{refuse}' 2>/dev/null || echo 0)\"\n",
        encoding="utf-8",
    )
    fake.chmod(0o755)
    monkeypatch.setattr(codex_hooks, "codex_binary", lambda: str(fake))

    def hooks(*items: dict) -> None:
        state.write_text(json.dumps(list(items)), encoding="utf-8")

    return SimpleNamespace(
        home=home,
        hooks=hooks,
        written=lambda: [json.loads(line) for line in writes.read_text().splitlines()],
        trust=lambda: {hook["key"]: hook["trustStatus"] for hook in json.loads(state.read_text())},
        refuse=lambda: refuse.write_text("1"),
    )


def test_probes_waiting_hooks_are_approved_the_way_hooks_approves_them(codex):
    daemon = _hook(codex.home, "probe-research-daemon", "sessionStart")
    changed = _hook(codex.home, "probe-research-tap", "sessionEnd", trust="modified")
    done = _hook(codex.home, "probe-research-tap", "stop", trust="trusted")
    codex.hooks(daemon, changed, done)
    outcome = APPROVE(timeout=10)
    assert outcome == codex_hooks.Approval(approved=tuple(sorted([daemon["key"], changed["key"]])), done=True)
    (write,) = codex.written()
    assert write["edits"] == [
        {"keyPath": f'hooks.state."{hook["key"]}".trusted_hash', "value": hook["currentHash"], "mergeStrategy": "replace"}
        for hook in sorted([daemon, changed], key=lambda hook: hook["key"])
    ]
    assert set(codex.trust().values()) == {"trusted"}


def test_nothing_waiting_writes_nothing(codex):
    codex.hooks(_hook(codex.home, "probe-research-tap", "stop", trust="trusted"))
    assert APPROVE(timeout=10) == codex_hooks.Approval(done=True)
    assert codex.written() == []


@pytest.mark.parametrize(
    "stranger",
    [
        pytest.param({"plugin": "someone-elses-plugin"}, id="another-plugin"),
        pytest.param({"plugin": "probe-research-tap", "market": "a-fork"}, id="probe-name-other-marketplace"),
        pytest.param({"plugin": "probe-research-tap", "path": Path("/tmp/elsewhere/hooks.json")}, id="outside-the-cache"),
        pytest.param({"plugin": "probe-research-tap", "source": "project"}, id="a-projects-hook"),
        pytest.param({"plugin": "probe-research-tap", "isManaged": True}, id="managed"),
        pytest.param({"plugin": "probe-research-tap", "enabled": False}, id="switched-off"),
        pytest.param({"plugin": "probe-research-tap", "pluginId": "probe-research@research-os-agent"},
                     id="key-and-plugin-id-disagree"),
        pytest.param({"plugin": "probe-research-tap", "sibling": "probe-research"}, id="a-sibling-plugins-folder"),
        pytest.param({"plugin": "probe-research-tap", "dotdot": True}, id="dotdot-out-of-the-cache"),
        pytest.param({"plugin": "probe-research-tap", "symlink": True}, id="symlink-out-of-the-cache"),
    ],
)
def test_only_probes_own_plugin_hooks_are_ever_approved(codex, stranger):
    """An approval says "run this command": Probe gives it for the hooks of its own
    plugins, from its own marketplace, loaded from their copies in Codex's cache."""
    plugin = stranger.pop("plugin")
    cache = codex.home / "plugins" / "cache" / MARKET
    # A Probe copy in Codex's cache, so the wizard's question really asks Codex.
    (cache / "probe-research-daemon" / "0.0.9").mkdir(parents=True)
    if sibling := stranger.pop("sibling", None):
        stranger["path"] = cache / sibling / "0.1.0" / "hooks" / "hooks.json"
    if stranger.pop("dotdot", False):
        stranger["path"] = cache / plugin / ".." / ".." / ".." / ".." / "elsewhere" / "hooks.json"
    if stranger.pop("symlink", False):
        outside = codex.home.parent / "outside"
        outside.mkdir()
        (cache / plugin).mkdir(parents=True)
        (cache / plugin / "0.1.0").symlink_to(outside)
    hook = _hook(codex.home, plugin, "sessionStart", **stranger)
    codex.hooks(hook)
    outcome = APPROVE(timeout=10)
    assert outcome is not None and outcome.approved == () and outcome.error is None
    assert codex.written() == []
    # A Probe-named hook Probe may not approve still WAITS: never reported as done,
    # so the person is still sent to /hooks.
    waits = plugin in codex_hooks.PROBE_PLUGINS and stranger.get("enabled", True) is not False
    assert outcome.done is not waits
    assert WAITING() is False, "never work for the wizard either"


def test_a_codex_that_refuses_the_write_says_so(codex):
    codex.hooks(_hook(codex.home, "probe-research-tap", "sessionStart"))
    codex.refuse()
    outcome = APPROVE(timeout=10)
    assert outcome == codex_hooks.Approval(error="Codex refused it: managed")
    assert len(codex.written()) == 1


def test_no_codex_or_no_answer_is_none(codex, monkeypatch, tmp_path):
    monkeypatch.setattr(codex_hooks, "codex_binary", lambda: None)
    assert APPROVE(timeout=5) is None
    gone = tmp_path / "gone"
    gone.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    gone.chmod(0o755)
    monkeypatch.setattr(codex_hooks, "codex_binary", lambda: str(gone))
    started = time.monotonic()
    assert APPROVE(timeout=5) is None
    assert time.monotonic() - started < 3, "a Codex that exited must not cost the whole timeout"


def test_the_wizard_drops_the_hooks_step_only_when_the_approval_took(monkeypatch):
    caps = Capabilities(agent_source="codex", codex_available=True)
    selection = setup.Selection(tracking=True, capture=True, auto_update=True, agent_rules=True)
    assert setup.CODEX_HOOK_STEPS[0] in setup.restart_notice(caps, selection)
    assert setup.restart_notice(caps, selection, codex_hooks_approved=True) == ["Restart Codex to load Probe."]
    assert setup.install_next(caps, selection, codex_hooks_approved=True) == (True, [])


@pytest.mark.parametrize(
    ("outcome", "expected"),
    [
        (None, ([f"Probe's hooks in Codex still need approval (Codex could not be asked): {setup.CODEX_HOOKS_INSTRUCTION}"], False)),
        (codex_hooks.Approval(done=True), ([], True)),
        (codex_hooks.Approval(approved=("a", "b"), done=True), (["Approved Probe's 2 hooks in Codex."], True)),
        (codex_hooks.Approval(), ([f"Probe's hooks in Codex still need approval (a Probe hook still waits): {setup.CODEX_HOOKS_INSTRUCTION}"], False)),
        (
            codex_hooks.Approval(approved=("a",), error="1 still waiting"),
            (["Approved Probe's 1 hook in Codex.",
              f"Probe's hooks in Codex still need approval (1 still waiting): {setup.CODEX_HOOKS_INSTRUCTION}"], False),
        ),
    ],
)
def test_the_wizards_approval_never_fails_the_install(monkeypatch, outcome, expected):
    """A hook left waiting is what `/hooks` already fixes: the install stays a
    success and the closing note keeps sending the person there."""
    monkeypatch.setattr(codex_hooks, "approve", lambda *a, **k: outcome)
    lines, done = setup.approve_codex_hooks()
    assert (lines, done) == expected
    assert not any(setup.reports_failure(line) for line in lines)


@pytest.mark.parametrize(
    ("outcome", "said"),
    [
        (codex_hooks.Approval(approved=("a",), done=True), "; approved 1 Probe hook in Codex"),
        (codex_hooks.Approval(done=True), ""),
        (None, ""),
        (
            codex_hooks.Approval(error="Codex refused it: managed"),
            "; Probe's hooks still wait for approval in Codex (Codex refused it: managed): type /hooks there",
        ),
    ],
)
def test_an_update_approves_and_says_how_many(monkeypatch, outcome, said):
    monkeypatch.setattr(codex_hooks, "approve", lambda *a, **k: outcome)
    assert updater._approve_codex_hooks() == said


def test_a_re_list_that_drops_a_key_does_not_count_it_approved(codex, monkeypatch):
    """Approved means Codex now SAYS trusted, never that a key went missing; and a
    hook still waiting is never `done`, whatever the summary of the re-list says."""
    hook = _hook(codex.home, "probe-research-tap", "sessionStart")
    codex.hooks(hook)
    monkeypatch.setattr(codex_hooks, "_trust_states", lambda result: {})
    outcome = APPROVE(timeout=10)
    assert outcome == codex_hooks.Approval(error="1 still waiting", done=False)


def test_a_run_that_turns_capture_off_never_approves_the_tap(codex):
    """Capture off (DISABLE) leaves the tap installed: the wizard approves only the
    plugins its selection keeps on, and judges `done` by those alone."""
    tracking = _hook(codex.home, "probe-research-daemon", "sessionStart")
    tap = _hook(codex.home, "probe-research-tap", "sessionStart")
    codex.hooks(tracking, tap)
    only = setup.codex_plugins_kept_on(setup.Selection(tracking=True, capture=False, auto_update=True, agent_rules=True))
    assert only == frozenset({"probe-research", "probe-research-daemon"})
    outcome = APPROVE(timeout=10, only=only)
    assert outcome == codex_hooks.Approval(approved=(tracking["key"],), done=True)
    assert codex.trust() == {tracking["key"]: "trusted", tap["key"]: "untrusted"}


@pytest.mark.parametrize(
    ("reported", "plain"),
    [
        ("\\\\?\\C:\\Users\\x\\.codex", "C:\\Users\\x\\.codex"),
        ("\\\\?\\UNC\\srv\\share\\.codex", "\\\\srv\\share\\.codex"),
        ("/home/x/.codex", "/home/x/.codex"),
    ],
)
def test_windows_extended_length_paths_compare_as_plain_ones(reported, plain):
    assert str(codex_hooks._plain(Path(reported))) == str(Path(plain))


@pytest.mark.parametrize(
    ("error", "said"),
    [
        (None, "Codex did not answer"),
        ({"code": -32601, "message": "Method not found"}, "this Codex is too old to take it"),
        ({"code": -32600, "message": "Invalid configuration:\n features.x is not supported"},
         "Codex refused it: Invalid configuration: features.x is not supported"),
    ],
)
def test_a_refused_write_is_named_in_codexs_own_words(error, said):
    assert codex_hooks._refusal(error) == said


def test_on_windows_closing_ends_the_whole_launcher_tree(codex, monkeypatch, tmp_path):
    """npm's codex.cmd -> node -> codex.exe: `taskkill /T` ends all of it."""
    monkeypatch.setattr(codex_hooks, "signal", SimpleNamespace())
    monkeypatch.setattr(codex_hooks, "_on_windows", lambda: True)
    ran: list[list[str]] = []
    real_run = codex_hooks.subprocess.run
    monkeypatch.setattr(codex_hooks.subprocess, "run", lambda argv, **kw: ran.append(argv))
    pidfile = tmp_path / "pid"
    stuck = tmp_path / "stuck"
    stuck.write_text(f"#!/bin/sh\necho $$ > '{pidfile}'\ntrap '' TERM\nwhile :; do sleep 1; done\n", encoding="utf-8")
    stuck.chmod(0o755)
    monkeypatch.setattr(codex_hooks, "codex_binary", lambda: str(stuck))
    try:
        assert codex_hooks.list_hooks(timeout=0.5) is None
        pid = int(pidfile.read_text())
        assert ran == [["taskkill", "/T", "/F", "/PID", str(pid)]]
    finally:
        monkeypatch.setattr(codex_hooks.subprocess, "run", real_run)
        os.kill(int(pidfile.read_text()), 9)


def test_the_wizard_asks_with_the_same_rule_approve_uses(codex):
    """A Probe-named plugin from another marketplace waits, but it is not Probe's
    to approve: it must not make every re-run skip "Already set up"."""
    (codex.home / "plugins" / "cache" / MARKET / "probe-research-tap" / "0.1.0").mkdir(parents=True)
    codex.hooks(_hook(codex.home, "probe-research-tap", "sessionStart", market="a-fork"))
    assert WAITING() is False
    codex.hooks(_hook(codex.home, "probe-research-tap", "sessionStart"))
    assert WAITING() is True


def test_the_approval_key_is_escaped_the_way_codex_escapes_it():
    """codex-rs/app-server/src/effective_plugin_change.rs::hook_trusted_hash_edit."""
    edit = codex_hooks._trust_edit('p@m:a"b\\c', "sha256:x")
    assert edit == {"keyPath": 'hooks.state."p@m:a\\"b\\\\c".trusted_hash', "value": "sha256:x", "mergeStrategy": "replace"}


def test_without_process_groups_closing_never_raises_and_still_ends_codex(codex, monkeypatch, tmp_path):
    """Windows has no `os.killpg` or `signal.SIGKILL`: closing a Codex that will
    not exit must still end it, and never fail the install or update. Only this
    module's view of them goes (`Popen.kill` keeps the real SIGKILL)."""
    monkeypatch.setattr(codex_hooks, "signal", SimpleNamespace())
    pidfile = tmp_path / "pid"
    stuck = tmp_path / "stuck"
    stuck.write_text(f"#!/bin/sh\necho $$ > '{pidfile}'\ntrap '' TERM\nwhile :; do sleep 1; done\n", encoding="utf-8")
    stuck.chmod(0o755)
    monkeypatch.setattr(codex_hooks, "codex_binary", lambda: str(stuck))
    for ask in (lambda: APPROVE(timeout=0.5), lambda: codex_hooks.list_hooks(timeout=0.5)):
        pidfile.unlink(missing_ok=True)
        assert ask() is None
        pid = int(pidfile.read_text())
        with pytest.raises(ProcessLookupError):
            os.kill(pid, 0)
