"""The on-change notice: the Codex-shaped half of the tracking indicator.

Codex cannot render a computed status-line segment — its status line is a picker
over built-in items — so the same information is delivered as a message when it
CHANGES. The whole design risk is that it becomes noise, so most of what is
tested here is SILENCE: the hook fires on every agent turn and must say nothing
on almost all of them.
"""

from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parent.parent
_HOOKS = _ROOT / "plugins" / "probe-research" / "hooks"
_NOTIFY = _HOOKS / "statusline_notify.py"
_STATUSLINE = _HOOKS / "statusline.py"

SESSION = "32fae7ad-a401-43d0-bfef-ea032058769e"


@pytest.fixture()
def notify(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    monkeypatch.delenv("PROBE_STATUSLINE", raising=False)
    spec = importlib.util.spec_from_file_location("statusline_notify", _NOTIFY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def marker(notify):
    return notify._load("_session_marker")


def _enable(marker) -> None:
    path = marker.notify_flag_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("on", encoding="utf-8")


def _run(notify, monkeypatch, session_id: str = SESSION, cwd: str | None = None) -> str:
    out = io.StringIO()
    payload = {"session_id": session_id}
    if cwd is not None:
        payload["cwd"] = cwd
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(payload)))
    monkeypatch.setattr("sys.stdout", out)
    assert notify.main([]) == 0
    return out.getvalue()


def _said(raw: str) -> str | None:
    return json.loads(raw)["systemMessage"] if raw.strip() else None


# -- opt-in -----------------------------------------------------------------


def test_silent_when_the_notice_was_never_enabled(notify, marker, monkeypatch) -> None:
    marker.write(SESSION, {"project": "folding"})
    assert _run(notify, monkeypatch) == ""


def test_the_killswitch_silences_it(notify, marker, monkeypatch) -> None:
    _enable(marker)
    marker.write(SESSION, {"project": "folding"})
    monkeypatch.setenv("PROBE_STATUSLINE", "off")
    assert _run(notify, monkeypatch) == ""


# -- on change, and ONLY on change ------------------------------------------


def test_says_it_once_then_stays_quiet(notify, marker, monkeypatch) -> None:
    """THE POINT. A line every turn saying the same thing is one a reader learns
    to skip, at which point it costs attention and delivers nothing."""
    _enable(marker)
    marker.write(SESSION, {"project": "folding"})

    first = _said(_run(notify, monkeypatch))
    assert first == "Probe: tracking → folding"

    for _ in range(5):
        assert _run(notify, monkeypatch) == ""


def test_speaks_again_when_the_project_changes(notify, marker, monkeypatch) -> None:
    _enable(marker)
    marker.write(SESSION, {"project": "folding"})
    _run(notify, monkeypatch)
    marker.write(SESSION, {"project": "bird-sql-sft"})
    assert _said(_run(notify, monkeypatch)) == "Probe: tracking → bird-sql-sft"


def test_speaks_when_a_run_goes_live_and_when_it_ends(notify, marker, monkeypatch) -> None:
    _enable(marker)
    marker.write(SESSION, {"project": "folding", "run_ids": ["r1"], "active_run_ids": []})
    assert _said(_run(notify, monkeypatch)) == "Probe: tracking → folding"

    marker.write(SESSION, {"project": "folding", "run_ids": ["r1"], "active_run_ids": ["r1"]})
    assert _said(_run(notify, monkeypatch)) == "Probe: tracking → folding · running"
    assert _run(notify, monkeypatch) == ""  # still running: nothing new to say

    marker.write(SESSION, {"project": "folding", "run_ids": ["r1"], "active_run_ids": []})
    assert _said(_run(notify, monkeypatch)) == "Probe: tracking → folding"


def test_an_untracked_session_is_stated_once(notify, marker, monkeypatch) -> None:
    """A session that opens already tracked (a resume) has a state worth saying
    once; so does one that has recorded nothing. What neither may do is repeat."""
    _enable(marker)
    assert _said(_run(notify, monkeypatch)) == "Probe: this session is not tracked yet."
    assert _run(notify, monkeypatch) == ""


def test_absent_signal_notice_uses_the_payload_folder_default(
    notify, marker, monkeypatch, tmp_path
) -> None:
    repo = tmp_path / "research"
    repo.mkdir()
    cfg = repo / ".probe"
    cfg.mkdir()
    (cfg / "config.json").write_text(
        json.dumps({"defaults": {"session_tracking": "off"}}), encoding="utf-8"
    )
    _enable(marker)

    assert _run(notify, monkeypatch, cwd=str(repo)) == ""


def test_statusline_uses_folder_resolution_only_when_the_signal_is_absent(
    notify, marker, monkeypatch, tmp_path
) -> None:
    monkeypatch.setenv("PROBE_TOKEN", "configured")
    repo = tmp_path / "research"
    repo.mkdir()
    cfg = repo / ".probe"
    cfg.mkdir()
    (cfg / "config.json").write_text(
        json.dumps({"defaults": {"session_tracking": "off"}}), encoding="utf-8"
    )
    spec = importlib.util.spec_from_file_location("statusline", _STATUSLINE)
    statusline = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(statusline)
    monkeypatch.setattr(statusline, "_load", lambda _name: marker)

    absent = statusline.segment({"session_id": SESSION, "cwd": str(repo)})
    # The folder says `off` in the two-valued vocabulary, which meant "stop
    # recording, keep searching" -- read-only -- and that is the word the
    # segment now shows. `not tracking` is only reached by a caller that
    # resolved the switch to a BOOLEAN and passed no state.
    assert "read" in absent

    assert marker.set_tracking(SESSION, True)
    monkeypatch.setattr(
        marker,
        "resolve_tracking_default",
        lambda *_args, **_kwargs: pytest.fail("seeded statusline walked folder defaults"),
    )
    seeded = statusline.segment({"session_id": SESSION, "cwd": str(repo)})
    assert "not tracking" not in seeded


def test_sessions_do_not_share_notice_state(notify, marker, monkeypatch) -> None:
    other = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    _enable(marker)
    marker.write(SESSION, {"project": "folding"})
    marker.write(other, {"project": "folding"})
    assert _said(_run(notify, monkeypatch, SESSION)) is not None
    assert _said(_run(notify, monkeypatch, other)) is not None


# -- the state key ----------------------------------------------------------


def test_the_key_ignores_churn_that_no_reader_cares_about(marker) -> None:
    """`updated_at` moves on every refresh and `run_ids` churns; comparing whole
    markers would fire a notice several times a minute saying the same thing."""
    a = {"project": "folding", "run_ids": ["r1"], "updated_at": 1.0}
    b = {"project": "folding", "run_ids": ["r1", "r2"], "updated_at": 999.0}
    assert marker.state_key(a, live=False) == marker.state_key(b, live=False)


def test_the_key_separates_the_states_that_matter(marker) -> None:
    keys = {
        marker.state_key(None, live=False),
        marker.state_key({"project": "folding"}, live=False),
        marker.state_key({"project": "folding"}, live=True),
        marker.state_key({"project": "other"}, live=False),
    }
    assert len(keys) == 4


def test_the_message_reuses_the_segments_labels(marker) -> None:
    """One wording, so the two surfaces cannot describe the same state
    differently."""
    assert marker._LABEL_TRACKED in marker.message({"project": "folding"})
    assert marker._ACCENT_TEXT in marker.message({"project": "folding"}, live=True)


# -- fail-silent ------------------------------------------------------------


@pytest.mark.parametrize("payload", [{}, {"session_id": ""}, {"session_id": "short"}])
def test_a_payload_without_a_usable_session_says_nothing(
    notify, marker, monkeypatch, payload
) -> None:
    _enable(marker)
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(payload)))
    out = io.StringIO()
    monkeypatch.setattr("sys.stdout", out)
    assert notify.main([]) == 0
    assert out.getvalue() == ""


def test_garbage_stdin_exits_zero_silently(tmp_path) -> None:
    result = subprocess.run(
        [sys.executable, str(_NOTIFY)],
        input="not json",
        capture_output=True,
        text=True,
        timeout=30,
        env={"PATH": "/usr/bin:/bin", "XDG_STATE_HOME": str(tmp_path), "HOME": str(tmp_path)},
    )
    assert result.returncode == 0
    assert result.stdout == ""


# -- wiring -----------------------------------------------------------------


def test_the_notice_is_wired_to_stop() -> None:
    """Stop is the end of an agent turn — the moment the reader is looking, and
    the one event both agents support."""
    hooks = json.loads((_HOOKS / "hooks.json").read_text())["hooks"]
    commands = [entry["command"] for group in hooks["Stop"] for entry in group["hooks"]]
    assert any("statusline_notify.py" in command for command in commands)
