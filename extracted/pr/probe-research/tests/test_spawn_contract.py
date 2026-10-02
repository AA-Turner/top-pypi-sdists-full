"""One argv, three callers, one fixture — the cross-language contract test.

`tap start` was created to delete a second copy of the spawn. Its callers are
now in two languages and pin the argv separately: `daemon.test.ts` asserts a
literal list, this side asserts another, and `tap/start.py`'s argparse defines
a third. Nothing compared them, so a renamed flag would have gone green on
every suite and produced a pi session that silently captures nothing.

`plugins/probe-research-tap/spawn-contract.json` is the one place the flag
names live. This file checks the two Python-visible ends against it; the
TypeScript end is checked by `daemon.test.ts`'s own reader of the same file.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TAP = ROOT / "agent" / "plugins" / "probe-research-tap"
CONTRACT = TAP / "spawn-contract.json"


@pytest.fixture(scope="module")
def contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def expected_argv(contract: dict, session_id: str, cwd: str, transcript: str) -> list[str]:
    """The argv every caller must build, from the fixture rather than by hand."""
    values = {"session_id": session_id, "cwd": cwd, "transcript": transcript}
    argv = list(contract["subcommand"])
    for name in contract["flag_order"]:
        argv += [contract["flags"][name], values[name]]
    return argv


def test_the_spawner_accepts_every_flag_the_contract_names(contract):
    """`tap start`'s parser is the consumer. Ask it, do not read its source.

    `--help` is the cheapest question that still goes through argparse, so a
    renamed or removed flag fails here rather than at a customer's first
    tracked session.
    """
    completed = subprocess.run(
        [sys.executable, "-m", "tap", "start", "--help"],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
        cwd=TAP,
        env={"PATH": "/usr/bin:/bin", "PYTHONPATH": str(TAP)},
    )
    assert completed.returncode == 0, completed.stderr
    for name, flag in contract["flags"].items():
        assert flag in completed.stdout, f"{flag} ({name}) is not a `tap start` flag"


def test_the_cli_self_heal_builds_the_contract_argv(contract, tmp_path, monkeypatch):
    """The Python caller, checked against the fixture rather than a literal."""
    from probe.cli import capture_state

    transcript = tmp_path / "session.jsonl"
    transcript.write_text('{"type":"session"}\n', encoding="utf-8")
    tap_state = tmp_path / "tap-state"
    tap_state.mkdir()
    (tap_state / ".token").write_text("probe_ing_test", encoding="utf-8")

    monkeypatch.setenv("PROBE_PI_TAP_PLUGIN_DIR", str(tap_state))
    monkeypatch.setenv("PI_SESSION_FILE", str(transcript))
    monkeypatch.setattr(capture_state, "_tracking_is_on", lambda sid, cwd: True)
    monkeypatch.setattr(capture_state, "_capture_installed", lambda cwd: True)
    monkeypatch.setattr(capture_state, "_tap_runtime", lambda: (sys.executable, None))
    monkeypatch.setattr(
        capture_state,
        "session_capture_state",
        lambda sid, source=None: capture_state.CaptureState(False, None, "not started"),
    )

    spawned: list[list[str]] = []
    monkeypatch.setattr(capture_state, "_run", lambda argv, env: spawned.append(argv) or 0)

    sid = "01a06383-6f4e-751a-b94c-bcefef19938c"
    capture_state.ensure_capture(sid, cwd=tmp_path, source="pi")

    assert len(spawned) == 1
    interpreter, *rest = spawned[0]
    assert interpreter == sys.executable
    assert rest == expected_argv(contract, sid, str(tmp_path), str(transcript))


def test_the_typescript_caller_reads_this_same_file():
    """Pin the other half of the contract to the fixture too.

    Without this, the TS suite could quietly stop reading the file and go back
    to a hand-written literal, which is the state this fixture exists to end.
    """
    src = (ROOT / "agent" / "plugins" / "probe-research-pi" / "tests" / "daemon.test.ts").read_text(
        encoding="utf-8"
    )
    assert "spawn-contract.json" in src, (
        "daemon.test.ts no longer reads the shared spawn contract; the two "
        "callers can drift again"
    )
