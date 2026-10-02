"""The tracking auto-mark: a session's first research write turns its signal on.

Two layers under test. `session_marker.set_tracking_if_absent` is the exclusive
publisher: it decides only when nobody has, and an existing decision — either
direction, either spelling — is never touched. `Transport._auto_mark_tracking`
is the gate that invokes it: research routes only, writes only, coding-agent
sessions only, never while `PROBE_SESSION_TRACKING` holds the setting down, and
never in a way that can break the write it rides on.

The CRITICAL case here is the env override: this is the first non-hook writer
of the signal file, and an explicit `on` written despite a machine-wide
forced-off would outlive and defeat it. That regression is pinned twice (both
directions), not once.
"""

from __future__ import annotations

import json

import httpx
import pytest

from probe.sdk import errors, session_marker
from probe.sdk import transport as transport_module
from probe.sdk.config import Settings
from probe.sdk.transport import Transport

SESSION = "0f0e29be-6a1a-4e6f-9f66-1c8f6f3f0001"
SESSION_B = "0f0e29be-6a1a-4e6f-9f66-1c8f6f3f0002"

# Shape verified against a live Claude Code session (see
# test_agent_session_headers.LIVE): detection key, session id, version suffix.
LIVE = {
    "CLAUDECODE": "1",
    "CLAUDE_CODE_ENTRYPOINT": "cli",
    "CLAUDE_CODE_SESSION_ID": SESSION,
    "CLAUDE_CODE_VERSION": "2.1.219 (Claude Code)",
}


@pytest.fixture
def state(monkeypatch: pytest.MonkeyPatch, tmp_path):
    """Isolated marker state + a live-shaped Claude Code environment."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    monkeypatch.delenv("PROBE_CONFIG_PATH", raising=False)
    for key, value in LIVE.items():
        monkeypatch.setenv(key, value)
    return tmp_path


def _transport(handler=None) -> Transport:
    handler = handler or (lambda request: httpx.Response(201, json={}))
    return Transport(
        Settings(base_url="https://example.test", token="t", ingest_token="ros_ing_x"),
        client=httpx.Client(
            base_url="https://example.test", transport=httpx.MockTransport(handler)
        ),
    )


# --- the exclusive publisher -------------------------------------------------


def test_absent_becomes_on_and_only_once(state) -> None:
    assert session_marker.set_tracking_if_absent(SESSION, True) is True
    assert session_marker.tracking_signal(SESSION) == "on"
    assert session_marker.tracking_signal_path(SESSION).read_text() == "on\n"
    # The second caller finds a decision and makes none.
    assert session_marker.set_tracking_if_absent(SESSION, True) is False


def test_an_explicit_off_is_never_touched(state) -> None:
    assert session_marker.set_tracking(SESSION, False)
    assert session_marker.set_tracking_if_absent(SESSION, True) is False
    assert session_marker.tracking_signal(SESSION) == "off"


def test_the_legacy_off_spelling_counts_as_a_decision(state) -> None:
    legacy = session_marker._legacy_off_path(SESSION)
    legacy.parent.mkdir(parents=True, exist_ok=True)
    legacy.touch()
    assert session_marker.set_tracking_if_absent(SESSION, True) is False
    assert session_marker.tracking_signal(SESSION) == "off"


def test_an_invalid_session_id_publishes_nothing(state) -> None:
    assert session_marker.set_tracking_if_absent("bad id\n", True) is False


def test_the_temp_file_never_survives(state) -> None:
    session_marker.set_tracking_if_absent(SESSION, True)
    leftovers = [
        p for p in session_marker.sessions_dir().iterdir() if ".tmp-" in p.name
    ]
    assert leftovers == []


def test_losing_the_publish_race_preserves_the_off(state, monkeypatch) -> None:
    """A researcher typing `off` between our read and our publish keeps their
    off — os.link refuses to replace, by construction."""
    path = session_marker.tracking_signal_path(SESSION)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("off\n", encoding="utf-8")
    # Simulate the read having seen "absent" before the off landed.
    monkeypatch.setattr(session_marker, "tracking_signal", lambda sid: None)
    assert session_marker.set_tracking_if_absent(SESSION, True) is False
    assert path.read_text() == "off\n"


def _machine_default_off(tmp_path) -> None:
    """Set this machine's default to `off` in the CONFIG FILE.

    The file, not `PROBE_SESSION_TRACKING`: the env is documented as an
    override and never the home for this setting, so the file is the case that
    has to hold. Pinning only the env would pass while the home was broken --
    which is exactly how a default-off box came to create projects.
    """
    cfg = tmp_path / "config" / "probe"
    cfg.mkdir(parents=True, exist_ok=True)
    (cfg / "config.json").write_text(
        json.dumps({"version": 2, "defaults": {"session_tracking": "off"}}),
        encoding="utf-8",
    )


def _folder_default_off(folder) -> None:
    cfg = folder / ".probe"
    cfg.mkdir(parents=True, exist_ok=True)
    (cfg / "config.json").write_text(
        json.dumps({"defaults": {"session_tracking": "off"}}), encoding="utf-8"
    )


def test_the_seed_writes_the_value_it_is_given(state) -> None:
    assert session_marker.set_tracking_if_absent(SESSION, False) is True
    assert session_marker.tracking_signal(SESSION) == "off"
    assert session_marker.tracking_signal_path(SESSION).read_text() == "off\n"


# --- the transport gate ------------------------------------------------------


def test_a_research_write_never_flips_a_default_off_machine_on(state) -> None:
    """The regression that started this: a session on a default-off machine
    created a project, and the write marked the session `on` -- automation
    authoring a declaration the researcher never made. The default IS the
    researcher choosing what a new session starts at, so a write may settle
    that value and may never contradict it."""
    _machine_default_off(state)
    _transport().request("POST", "/v1/projects", json_body={"name": "p"})
    assert session_marker.tracking_signal(SESSION) == "off"
    assert session_marker.is_tracking(session_marker.tracking_signal(SESSION)) is False


def test_a_research_write_settles_the_process_folder_default(state, monkeypatch) -> None:
    repo = state / "research"
    cwd = repo / "src"
    cwd.mkdir(parents=True)
    _folder_default_off(repo)
    monkeypatch.chdir(cwd)

    _transport().request("POST", "/v1/projects", json_body={"name": "p"})

    assert session_marker.tracking_signal(SESSION) == "off"



def test_a_research_write_marks_the_session(state) -> None:
    _transport().request("POST", "/v1/projects", json_body={"name": "p"})
    assert session_marker.tracking_signal(SESSION) == "on"


def test_a_nested_research_route_marks_too(state) -> None:
    _transport().request("POST", "/v1/runs/abc/artifacts", json_body={})
    assert session_marker.tracking_signal(SESSION) == "on"


def test_an_ingest_write_marks_too(state) -> None:
    _transport().request("POST", "/ingest/v1/runs/abc/metrics", json_body={})
    assert session_marker.tracking_signal(SESSION) == "on"


def test_plumbing_writes_never_mark(state) -> None:
    _transport().request("POST", "/v1/tokens", json_body={})
    assert session_marker.tracking_signal(SESSION) is None


def test_reads_never_mark(state) -> None:
    _transport().request("GET", "/v1/projects")
    assert session_marker.tracking_signal(SESSION) is None


def test_a_failed_write_marks_nothing(state) -> None:
    """AFTER success by contract: a write that never landed marks nothing."""
    transport = _transport(lambda request: httpx.Response(404, json={"detail": "no"}))
    with pytest.raises(errors.RosError):
        transport.request("POST", "/v1/projects", json_body={})
    assert session_marker.tracking_signal(SESSION) is None


def test_no_agent_session_means_no_mark(state, monkeypatch) -> None:
    for key in LIVE:
        monkeypatch.delenv(key, raising=False)
    _transport().request("POST", "/v1/projects", json_body={})
    assert session_marker.tracking_signal(SESSION) is None


@pytest.mark.parametrize("held", ["off", "on"])
def test_the_env_override_holds_the_signal_down(state, monkeypatch, held) -> None:
    """CRITICAL. While `PROBE_SESSION_TRACKING` holds the setting — EITHER
    direction — the auto-mark writes nothing: an explicit signal file would
    outlive the env's scope and (for forced-off) permanently defeat it."""
    monkeypatch.setenv("PROBE_SESSION_TRACKING", held)
    _transport().request("POST", "/v1/projects", json_body={})
    assert session_marker.tracking_signal(SESSION) is None


def test_an_explicit_off_survives_a_research_write(state) -> None:
    session_marker.set_tracking(SESSION, False)
    _transport().request("POST", "/v1/projects", json_body={})
    assert session_marker.tracking_signal(SESSION) == "off"


def test_an_explicit_signal_bypasses_folder_resolution(
    state, monkeypatch
) -> None:
    session_marker.set_tracking(SESSION, False)
    monkeypatch.setattr(
        transport_module.session_marker,
        "resolve_tracking_default",
        lambda *_args, **_kwargs: pytest.fail(
            "an existing signal must bypass folder resolution"
        ),
    )

    _transport().request("POST", "/v1/projects", json_body={})

    assert session_marker.tracking_signal(SESSION) == "off"


def test_a_broken_mark_never_breaks_the_write(state, monkeypatch) -> None:
    calls = {"n": 0}

    def boom(sid: str, on: bool) -> bool:
        calls["n"] += 1
        raise RuntimeError("marker filesystem is on fire")

    monkeypatch.setattr(
        transport_module.session_marker, "set_tracking_if_absent", boom
    )
    transport = _transport()
    resp = transport.request("POST", "/v1/projects", json_body={})
    assert resp.status_code == 201
    # And it is NOT remembered as settled: a raising marker is a transient
    # failure like any other, so the next write tries again.
    transport.request("POST", "/v1/projects", json_body={})
    assert calls["n"] == 2


def test_the_memo_is_per_session_not_per_transport(state, monkeypatch) -> None:
    """One long-lived transport serves many callers (the hosted MCP memoizes
    one per token). Each session must get its own mark."""
    transport = _transport()
    transport.request("POST", "/v1/projects", json_body={})
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SESSION_B)
    transport.request("POST", "/v1/projects", json_body={})
    assert session_marker.tracking_signal(SESSION) == "on"
    assert session_marker.tracking_signal(SESSION_B) == "on"


def test_a_legacy_off_landing_mid_publish_wins(state, monkeypatch) -> None:
    """os.link arbitrates `<sid>.state` only, so an old client writing the
    legacy `<sid>.off` while we publish would leave the files with `on` winning
    the read — automation overriding an explicit opt-out.

    The GUARD READ MOVED with the third state: `set_tracking_if_absent` now
    delegates to `set_session_state_if_absent`, which asks `session_state`, so
    that is what this has to hook. Patching the old entry point left the legacy
    file never created and the test asserting nothing.
    """
    real = session_marker.session_state

    def absent_then_off(sid: str):
        # Absent at the guard; the legacy off appears before the publish.
        session_marker._legacy_off_path(sid).parent.mkdir(parents=True, exist_ok=True)
        session_marker._legacy_off_path(sid).touch()
        monkeypatch.setattr(session_marker, "session_state", real)
        return None

    monkeypatch.setattr(session_marker, "session_state", absent_then_off)
    assert session_marker.set_tracking_if_absent(SESSION, True) is False
    assert not session_marker.tracking_signal_path(SESSION).exists(), (
        "the published `on` must be removed when an opt-out won the race"
    )
    assert session_marker.tracking_signal(SESSION) == "off"


def test_two_threads_never_publish_an_empty_marker(state) -> None:
    """A PID-named temp file is shared by threads of one process; the loser
    truncates what the winner already published."""
    import threading

    seen: list[str] = []
    barrier = threading.Barrier(4)

    def race() -> None:
        barrier.wait()
        session_marker.set_tracking_if_absent(SESSION, True)
        try:
            seen.append(session_marker.tracking_signal_path(SESSION).read_text())
        except OSError:
            pass

    threads = [threading.Thread(target=race) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert session_marker.tracking_signal(SESSION) == "on"
    assert all(text == "on\n" for text in seen), f"a reader saw a partial marker: {seen}"
    assert [p for p in session_marker.sessions_dir().iterdir() if ".tmp-" in p.name] == []


def test_a_transient_failure_is_retried_not_cached(state, monkeypatch) -> None:
    """False means "a decision exists" OR "the write failed". Caching on False
    alone turns one bad moment into a permanently unmarked session."""
    calls = {"n": 0}

    def failing(sid: str, on: bool) -> bool:
        calls["n"] += 1
        return False  # e.g. read-only state dir

    monkeypatch.setattr(
        transport_module.session_marker, "set_tracking_if_absent", failing
    )
    transport = _transport()
    transport.request("POST", "/v1/projects", json_body={})
    transport.request("POST", "/v1/projects", json_body={})
    assert calls["n"] == 2, "a failed mark must be retried on the next write"


def test_a_redirect_is_not_a_landed_write(state) -> None:
    transport = _transport(lambda request: httpx.Response(307, json={}))
    transport.request("POST", "/v1/projects", json_body={})
    assert session_marker.tracking_signal(SESSION) is None


def test_a_look_alike_route_does_not_mark(state) -> None:
    """`/v1/projects-search` is not `/v1/projects`."""
    _transport().request("POST", "/v1/projects-search", json_body={})
    assert session_marker.tracking_signal(SESSION) is None


def test_the_memo_is_bounded(state) -> None:
    transport = _transport()
    for i in range(transport_module._TRACKING_MEMO_CAP + 5):
        transport._tracking_marked.add(f"pad-{i}")
    transport.request("POST", "/v1/projects", json_body={})
    assert len(transport._tracking_marked) <= transport_module._TRACKING_MEMO_CAP
    assert session_marker.tracking_signal(SESSION) == "on"


def test_a_settled_session_costs_no_further_stats(state, monkeypatch) -> None:
    transport = _transport()
    transport.request("POST", "/v1/projects", json_body={})
    calls = {"n": 0}

    def counting(sid: str, on: bool) -> bool:
        calls["n"] += 1
        return False

    monkeypatch.setattr(
        transport_module.session_marker, "set_tracking_if_absent", counting
    )
    transport.request("POST", "/v1/projects", json_body={})
    assert calls["n"] == 0
