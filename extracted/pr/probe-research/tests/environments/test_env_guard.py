"""Cheap static guards for lane E3's environments. They always run; every
other test here is opt-in (PROBE_ENV_TESTS=1)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

from tests.environments import envkit, envlib

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent


def _flatten(d: dict, prefix: str = "") -> dict[str, float]:
    out: dict[str, float] = {}
    for key, value in d.items():
        name = f"{prefix}{key}"
        if isinstance(value, dict):
            out.update(_flatten(value, name + "/"))
        else:
            out[name] = value
    return out


def test_env_guard_loop_values_match():
    """customer_loop.py (run by the released SDK, which may not import the
    harness) and envlib (which reconciles) must agree on every value."""
    spec = importlib.util.spec_from_file_location("customer_loop", envlib.CUSTOMER_LOOP)
    loop = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loop)
    assert loop.CONFIG == envlib.CONFIG
    for step in (0, 1, 6, 7, 199, 229, 299):
        flat = _flatten(loop.row(step))
        assert set(flat) == set(envlib.KEYS)
        for key, value in flat.items():
            assert value == envlib.point_value(step, key), (step, key)


def test_is_sdk_helper_cmdline_matches_outbox_sender_and_outputs_reporter():
    """The outbox sender (outbox_worker.py:463-464) and the output-capture
    crash reporter (logcapture.py:756, :774, both `-m probe.sdk.outputs`)
    must be recognized so a real-server run_child() waits for them; anything
    else marked_pids() catches (e.g. a Ray daemon) must not be."""
    cmds = [
        b"/venv/bin/python3\x00-m\x00probe.sdk.outbox_worker\x00"
        b"/tmp/env-x/home/.local/state/probe/journal\x00",
        b"/venv/bin/python3\x00-m\x00probe.sdk.outputs\x00--recover\x00"
        b"/tmp/env-x/home/.local/state/probe/outputs/entry.json\x00",
        b"/venv/bin/python3\x00-m\x00probe.sdk.outputs\x00--writer-gone\x00"
        b"/tmp/env-x/home/.local/state/probe/outputs/entry.json\x00",
    ]
    for raw in cmds:
        assert envkit.is_sdk_helper_cmdline(raw.decode()), raw

    not_helpers = [
        b"/venv/bin/python3\x00-u\x00/venv/lib/python3.11/site-packages/"
        b"ray/_private/workers/default_worker.py\x00--node-ip-address=127.0.0.1\x00"
        b"--home=/tmp/env-x/home\x00",
        b"/venv/bin/python3\x00tests/environments/envchild.py\x00--tmpdir=/tmp/env-x/t\x00",
        b"",
    ]
    for raw in not_helpers:
        assert not envkit.is_sdk_helper_cmdline(raw.decode()), raw


def test_sdk_helper_pids_filters_marked_pids_by_cmdline(monkeypatch):
    """sdk_helper_pids() narrows marked_pids() down to just the SDK's own
    detached helpers, leaving other marked processes (e.g. a Ray daemon) out
    -- those are still reaped immediately by reap_marked(), just not waited
    on by wait_for_sdk_helpers()."""
    marker = "/tmp/env-x"
    cmdlines = {
        111: "/venv/bin/python3\x00-m\x00probe.sdk.outbox_worker\x00/tmp/env-x/journal\x00",
        222: "/venv/bin/python3\x00-u\x00ray/_private/workers/default_worker.py\x00/tmp/env-x\x00",
        333: "/venv/bin/python3\x00-m\x00probe.sdk.outputs\x00--writer-gone\x00/tmp/env-x/e\x00",
    }
    monkeypatch.setattr(envkit, "marked_pids", lambda m: list(cmdlines) if m == marker else [])
    monkeypatch.setattr(envkit, "_cmdline", lambda pid: cmdlines[pid])

    assert envkit.sdk_helper_pids(marker) == [111, 333]


def test_wait_for_sdk_helpers_returns_immediately_when_grace_is_zero(monkeypatch):
    calls = []
    monkeypatch.setattr(envkit, "sdk_helper_pids", lambda m: calls.append(m) or [111])
    assert envkit.wait_for_sdk_helpers("/tmp/env-x", 0) == [111]
    assert calls == ["/tmp/env-x"]  # checked once, never slept on


def test_wait_for_sdk_helpers_polls_until_helpers_exit(monkeypatch):
    """It must not kill anything itself -- just poll sdk_helper_pids() until
    the helper(s) are gone or the deadline passes -- and Ray-style marked
    pids play no part in that decision."""
    remaining = [[999], [999], []]
    monkeypatch.setattr(envkit, "sdk_helper_pids", lambda m: remaining.pop(0))
    slept = []
    monkeypatch.setattr(envkit.time, "sleep", lambda s: slept.append(s))
    monkeypatch.setattr(envkit.time, "monotonic", lambda: 0.0)

    assert envkit.wait_for_sdk_helpers("/tmp/env-x", 300) == []
    assert slept == [0.5, 0.5]


def test_env_guard_os_matrix_list_names_real_files():
    listed = [
        line.strip()
        for line in (HERE / "os_matrix" / "os_sensitive_tests.txt").read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]
    assert listed and len(listed) == len(set(listed))
    missing = [p for p in listed if not (REPO / "agent" / p).is_file()]
    assert missing == []
    workflow = (REPO / ".github" / "workflows" / "agent-os-matrix.yml").read_text()
    assert "tests/environments/os_matrix/os_sensitive_tests.txt" in workflow


def test_env_guard_big_artifact_is_unique_per_run(tmp_path, monkeypatch):
    """A byte-identical `*-big.bin` in every run shares one content hash, and
    a real server takes one active multipart upload per hash in a team: runs
    of the suite waited on each other (409). Same size, different bytes."""
    import hashlib

    from tests.environments import envchild

    digests = set()
    for n in range(2):
        monkeypatch.setattr(envchild, "ART", str(tmp_path / f"run{n}"))
        path = envchild.write_artifacts("job", big=True)["job-big.bin"]
        assert Path(path).stat().st_size == envchild.BIG_BYTES
        digests.add(hashlib.sha256(Path(path).read_bytes()).hexdigest())
    assert len(digests) == 2
