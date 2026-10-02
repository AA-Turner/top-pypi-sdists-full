"""The gate's verdict cache.

The full inspection reads a file into memory at about 1 MB/s on JSON text, and
one upload used to run it five times (check_upload, the outbox snapshot, then
`@freeze_upload` on both `upload_fingerprinted` and `put_file`). The verdict is
a pure function of the bytes and the policy, so it is cached by sha256.
"""

from __future__ import annotations

import pytest

from probe.sdk import secret_gate
from probe.sdk.secret_gate import CredentialBlocked, ScanPolicy, inspect_bytes


# -- the verdict cache ------------------------------------------------------------
def test_the_same_bytes_are_inspected_once(monkeypatch):
    calls = []
    real = secret_gate._inspect_bytes
    monkeypatch.setattr(secret_gate, "_inspect_bytes", lambda raw, limits: calls.append(1) or real(raw, limits))
    first = inspect_bytes(b"plain text, nothing secret")
    second = inspect_bytes(b"plain text, nothing secret")
    assert first == second
    assert len(calls) == 1


def test_a_different_policy_is_a_different_verdict(monkeypatch):
    calls = []
    real = secret_gate._inspect_bytes
    monkeypatch.setattr(secret_gate, "_inspect_bytes", lambda raw, limits: calls.append(1) or real(raw, limits))
    inspect_bytes(b"x" * 10, scan_policy=ScanPolicy())
    inspect_bytes(b"x" * 10, scan_policy=ScanPolicy(allow_opaque=False))
    assert len(calls) == 2


def test_a_refusal_is_never_cached(monkeypatch):
    """"Inspection failed" can come from a MemoryError the same bytes need not
    hit twice: only verdicts are remembered."""
    calls = []
    real = secret_gate._inspect_bytes
    monkeypatch.setattr(secret_gate, "_inspect_bytes", lambda raw, limits: calls.append(1) or real(raw, limits))
    for _ in range(2):
        with pytest.raises(CredentialBlocked):
            inspect_bytes(b"abcde", scan_policy=ScanPolicy(max_bytes=4))
    assert len(calls) == 2


def test_the_servers_copy_keeps_no_cache():
    """The server vendors this file; there one cache would span every tenant,
    and inspection time would say whether another tenant uploaded the same
    bytes recently."""
    from pathlib import Path

    server_copy = Path(__file__).resolve().parents[2] / "app" / "security" / "_credential_gate.py"
    text = server_copy.read_text()
    assert '_CACHE_ENABLED = __name__.startswith("probe.")' in text
    assert secret_gate._CACHE_ENABLED  # and the SDK's own copy does cache


def test_a_fork_never_inherits_a_held_cache_lock():
    import os

    if not hasattr(os, "fork"):
        pytest.skip("no fork")
    with secret_gate._CACHE_LOCK:
        pid = os.fork()
        if pid == 0:
            # The child's lock must be fresh, or this inspection hangs forever.
            try:
                inspect_bytes(b"after the fork")
                os._exit(0)
            except BaseException:
                os._exit(1)
    import time

    deadline = time.monotonic() + 20
    while time.monotonic() < deadline:
        done, status = os.waitpid(pid, os.WNOHANG)
        if done:
            assert os.waitstatus_to_exitcode(status) == 0
            return
        time.sleep(0.05)
    os.kill(pid, 9)
    os.waitpid(pid, 0)
    pytest.fail("the forked child hung on the inherited cache lock")


def test_a_file_over_the_inspection_limit_is_still_refused(tmp_path, monkeypatch):
    """Unchanged on purpose: the server's upload guard inspects in memory and
    caps at the same 64 MB, so a client that let a bigger file through would
    only have it refused one hop later."""
    from probe.sdk.secret_gate import check_upload

    monkeypatch.setattr(secret_gate, "policy", lambda: ScanPolicy(max_bytes=4096))
    path = tmp_path / "big.bin"
    path.write_bytes(b"\x80" * 5000)
    with pytest.raises(CredentialBlocked):
        check_upload(path)


@pytest.mark.parametrize("strict", [False, True])
def test_one_upload_inspects_its_bytes_once(client, tmp_path, monkeypatch, strict):
    """The five gate passes of one synchronous log_artifact collapse to one.
    By default that one is the quick check, and the full inspection does not
    run on this machine at all; the block policy keeps the full one, once."""
    from tests.conftest import open_run

    if strict:
        monkeypatch.setenv("PROBE_ARTIFACT_OPAQUE_POLICY", "block")
    calls, quick = [], []
    real, real_quick = secret_gate._inspect_bytes, secret_gate.redact_quick_bytes
    monkeypatch.setattr(secret_gate, "_inspect_bytes", lambda raw, limits: calls.append(1) or real(raw, limits))
    monkeypatch.setattr(secret_gate, "redact_quick_bytes", lambda raw: quick.append(1) or real_quick(raw))
    run = open_run(client, experiment="gate-once")
    path = tmp_path / "preds.jsonl"
    path.write_text('{"id": 1}\n' * 100)
    run.log_artifact("preds", path=str(path), sync=True)
    assert (len(calls), len(quick)) == ((1, 0) if strict else (0, 1))
