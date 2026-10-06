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
from pathlib import Path

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
