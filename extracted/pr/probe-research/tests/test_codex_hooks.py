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

from probe.cli import codex_hooks, doctor
from probe.cli.capabilities import Capabilities

FIXTURE = json.loads((Path(__file__).parent / "fixtures" / "codex_hooks_list_0.159.2.json").read_text())
RESULT = FIXTURE["result"]


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
