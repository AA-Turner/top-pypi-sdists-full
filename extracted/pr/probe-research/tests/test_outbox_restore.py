"""The one-time restore of writes set aside behind one revoked key (Bucket, 2026-10-22/23).

A re-sign-in on a customer's Mac revoked the key his training jobs held (`PROBE_TOKEN`,
fingerprint 738f7f8ed3fe16d6). Their writes waited, then `probe outbox discard --held` set
12,357 of them aside in the outbox root's `discarded/`, and nothing ever sends a set-aside
write. The restore puts back only that credential's writes from those two days that the
server never refused for their content and the login may send, into the same root journal;
the rescue then adopts the credential and sends them. Every restored write ends sent,
refused (back aside, still marked) or deferred (queued for the next pass).
"""

from __future__ import annotations

import json
import os
import shutil
import time

import pytest

from probe import analytics as telemetry
from probe.sdk.delivery import outbox as outbox_worker
from probe.sdk.delivery.journal.failures import restores
from probe.sdk.delivery.journal.failures.restores import (
    RESTORE_DONE,
    RESTORE_FINGERPRINT,
    RESTORED_KEY,
    KeptAside,
    RestoreCounts,
    restore_set_aside,
)
from probe.sdk.delivery.journal.journal import Journal
from probe.sdk.delivery.ops.ops import CREDENTIAL_NAMESPACE, DELIVERY_NAMESPACE
from probe.sdk.settings import settings as config
from tests.served_fake_app import serve
from tests.test_outbox import seeded_run

HOSTED = "https://api.research.prbe.ai"
OTHER_FP = "cd" * 8
#: What the fake's `/v1/me` answers by default, and what SDK 0.266.5 stamped on each write.
ACCOUNT = ("lab-42", "00000000-0000-0000-0000-000000000001")
STORED = "probe_pat_storedlogin_B_0123456789abcdef"
#: The set-aside files' mtime (2026-10-22 21:50Z): a restore keeps it.
OLD_MTIME = 1_761_169_800


@pytest.fixture(autouse=True)
def isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "probe" / "config.json"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    for var in ("PROBE_BASE_URL", "PROBE_TOKEN", "PROBE_INGEST_TOKEN", "PROBE_MCP_TOKEN",
                "PROBE_OUTBOX_DIR", "PROBE_OUTBOX_RESCUE", "PROBE_OUTBOX_WORKER"):
        monkeypatch.delenv(var, raising=False)
    (tmp_path / "probe").mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(Journal, "discover", staticmethod(lambda: []))
    monkeypatch.setattr("probe.sdk.delivery.outbox.drain.credentials._IDENTITY_CACHE", {})


@pytest.fixture()
def no_workers(monkeypatch):
    """The rescue's foreground pass only: no detached worker after it."""
    for module in (outbox_worker.drainers.detached, outbox_worker.outbox, outbox_worker.rescuer):
        monkeypatch.setattr(module, "maybe_spawn", lambda directory=None: False)


@pytest.fixture()
def restored_events(monkeypatch):
    seen: list = []
    monkeypatch.setattr(telemetry.events, "emit_outbox_restored", lambda counts: seen.append(counts) or True)
    return seen


def _stamp(fp=RESTORE_FINGERPRINT, source="env", account=ACCOUNT) -> dict:
    stamp = {"source": source, "fingerprint": fp}
    if account:
        stamp.update(customer_id=account[0], user_id=account[1])
    return stamp


def _set_aside(root, *, base_url=HOSTED, step=1, run_id="r-1", day="2026-10-22", fp=RESTORE_FINGERPRINT,
               source="env", account=ACCOUNT, method="POST", path=None, last_error=None, **extra) -> str:
    """One write as SDK 0.266.5 queued it in its credential's queue, then set aside in the
    outbox root's `discarded/` (what `discard --held` and the relocation left). Its name."""
    queue = Journal(
        str(root / CREDENTIAL_NAMESPACE / fp),
        context={"name": None, "base_url": base_url, "principal": _stamp(fp, source, account)},
    )
    body = None if method == "DELETE" else {
        "points": [{"key": "loss", "kind": "model", "value": float(step), "step_index": step}]
    }
    op_id = queue.append_http(method, path or f"/v1/runs/{run_id}/metrics", body)
    (queued,) = [p for p, op in queue.pending() if op["op_id"] == op_id]
    op = json.loads(queued.read_text())
    op.update(enqueued_at=f"{day}T21:50:00+00:00", last_error=last_error, **extra)
    target = root / "discarded"
    target.mkdir(parents=True, exist_ok=True)
    (target / queued.name).write_text(json.dumps(op, indent=2) + "\n")
    queued.unlink()
    os.utime(target / queued.name, (OLD_MTIME, OLD_MTIME))
    return queued.name


def _set_aside_upload(root, tmp_path, *, keep_bytes: bool, staged: bool = True) -> str:
    """An upload this credential queued in the root, set aside: staged with its bytes kept in
    the root's `blobs/` or collected, or (``staged`` False) naming its file where it was."""
    journal = Journal(str(root), context={"name": None, "base_url": HOSTED, "principal": _stamp()})
    src = tmp_path / f"ckpt-{keep_bytes}-{staged}.bin"
    src.write_bytes(b"weights" if keep_bytes else b"gone")
    queued = journal.append_upload(anchor="run", anchor_id="r-1", name=src.name, src_path=str(src),
                                   run_ref="r-1", inline_hash=True, stage=staged)
    (path,) = [p for p, op in journal.pending() if op["op_id"] == queued["op_id"]]
    op = json.loads(path.read_text())
    op["enqueued_at"] = "2026-10-23T09:00:00+00:00"
    (root / "discarded").mkdir(parents=True, exist_ok=True)
    (root / "discarded" / path.name).write_text(json.dumps(op))
    path.unlink()
    os.utime(root / "discarded" / path.name, (OLD_MTIME, OLD_MTIME))
    if not keep_bytes and staged:
        (journal.blobs_dir / queued["blob"]).unlink()
    return path.name


def _prune_credential_queues(root) -> None:
    """The credential queue went once idle (`credential_queues` 0 on the Mac)."""
    shutil.rmtree(root / CREDENTIAL_NAMESPACE, ignore_errors=True)


def _restored_in(folder) -> dict:
    out = {}
    for path in sorted(folder.glob("*.json")) if folder.exists() else []:
        op = json.loads(path.read_text())
        if op.get(RESTORED_KEY):
            out[path.name] = op
    return out


def _login(url: str, token: str = STORED) -> None:
    config.save_context({"base_url": url, "token": token, "identity": None})


def _steps_sent(app, run_id) -> list:
    return sorted(p["step_index"] for p in app.metric_points_posted.get(run_id, []))


# -- which writes go back ------------------------------------------------------------------


def test_only_this_incidents_sendable_writes_go_back(tmp_path):
    root = tmp_path / "outbox"
    back = {
        _set_aside(root, step=1),
        _set_aside(root, step=2, day="2026-10-23", last_error="AuthError: invalid or revoked token"),
        _set_aside(root, step=3, source="code", last_error="ScopeError: this API key was revoked"),
        # A passing failure (the laptop slept) is no verdict on the write: a run's oldest.
        _set_aside(root, step=13, last_error="TransportError: connection reset"),
        _set_aside(root, step=14, last_error="ServerError: 503 unavailable"),
        _set_aside(root, step=15, last_error="RosError: Too Many Requests"),  # a 429
        _set_aside_upload(root, tmp_path, keep_bytes=True),
    }
    kept = {
        _set_aside(root, step=4, last_error="ConflictError: stale write epoch 1; the run is at epoch 3"),
        _set_aside(root, step=5, last_error="NotFoundError: run not found"),
        _set_aside(root, step=6, path="/ingest/v1/sessions"),
        _set_aside(root, step=7, method="DELETE"),
        _set_aside(root, step=8, last_error="ValidationError: points must be finite"),
        _set_aside(root, step=9, restored_at="2026-11-01T00:00:00+00:00"),
        _set_aside_upload(root, tmp_path, keep_bytes=False),
        _set_aside_upload(root, tmp_path, keep_bytes=True, staged=False),
    }
    others = {
        _set_aside(root, step=10, fp=OTHER_FP),  # another credential: a deliberate drop, maybe
        _set_aside(root, step=11, day="2026-10-24"),  # another day
        _set_aside(root, step=12, source="config"),  # a stored-login write
    }
    _prune_credential_queues(root)
    tombstone = root / DELIVERY_NAMESPACE / "discarded" / "receipt.json"
    tombstone.parent.mkdir(parents=True)
    tombstone.write_text((root / "discarded" / sorted(back)[0]).read_text())

    counts = restore_set_aside(Journal(str(root)))

    assert set(_restored_in(root / "ops")) == back
    assert sorted(os.listdir(root / "discarded")) == sorted(kept | others)
    assert (counts.writes, counts.uploads, counts.unmoved) == (7, 1, 0)
    assert counts.by_enqueue_day == {"2026-10-22": 5, "2026-10-23": 2}
    assert counts.kept == {KeptAside.REFUSED: 3, KeptAside.NOT_SENDABLE: 2,
                           KeptAside.RESTORED_BEFORE: 1, KeptAside.BYTES_GONE: 2}
    assert counts.bytes_gone == 2 and counts.base_url == HOSTED
    assert tombstone.exists(), "a receipt namespace's tombstone is how its recovery knows"
    for name in back:
        assert os.stat(root / "ops" / name).st_mtime == OLD_MTIME, "name and mtime are kept"
    assert Journal.read_status(str(root))["pending"] == 7
    journal = Journal(str(root))
    journal.gc_blobs()
    (upload,) = [op for op in _restored_in(root / "ops").values() if op["kind"] == "upload"]
    assert journal.blob_path(upload).exists(), "the restored upload's bytes are referenced again"


def test_a_write_is_restored_once(tmp_path):
    """D2: put back once; set aside again (here by hand), it stays aside."""
    root = tmp_path / "outbox"
    name = _set_aside(root)
    assert restore_set_aside(Journal(str(root))).writes == 1
    os.replace(root / "ops" / name, root / "discarded" / name)
    again = restore_set_aside(Journal(str(root)))
    assert again.writes == 0 and again.kept == {KeptAside.RESTORED_BEFORE: 1}


def test_a_restore_moves_in_batches_and_counts_once(tmp_path, monkeypatch):
    root = tmp_path / "outbox"
    for step in range(5):
        _set_aside(root, step=step)
    _prune_credential_queues(root)
    monkeypatch.setattr(restores, "_RESTORE_BATCH", 2)
    assert restore_set_aside(Journal(str(root))).writes == 5
    assert Journal.read_status(str(root))["pending"] == 5
    assert not os.listdir(root / "discarded")


def test_a_name_already_queued_is_never_sent_twice(tmp_path):
    """The move is one rename, so a cut-short move leaves one copy; a name `ops/` holds anyway
    is not put back beside it."""
    root = tmp_path / "outbox"
    name = _set_aside(root)
    Journal(str(root))._ensure()
    shutil.copy(root / "discarded" / name, root / "ops" / name)
    counts = restore_set_aside(Journal(str(root)))
    assert (counts.writes, counts.unmoved) == (0, 0)
    assert os.listdir(root / "ops") == [name]


def test_the_retry_clock_restarts_and_the_attempts_stay(tmp_path):
    """Ten days old with 81 attempts, one 503 would dead-letter it (the transient budget), as
    `probe outbox retry` knows. The attempts stay: a 409 naming an id is ours only on a retry."""
    root = tmp_path / "outbox"
    name = _set_aside(root, attempts=81, first_failed_at=OLD_MTIME)
    restore_set_aside(Journal(str(root)))
    op = json.loads((root / "ops" / name).read_text())
    assert "first_failed_at" not in op and op["attempts"] == 81 and op[RESTORED_KEY]


def test_a_failed_move_leaves_the_restore_undone_and_the_next_pass_finishes(tmp_path, monkeypatch, no_workers):
    """A full disk at the first pass must not end the restore for good."""
    root = tmp_path / "outbox"
    name = _set_aside(root)
    _prune_credential_queues(root)
    real_replace = os.replace

    def full(src, dst, *a, **k):
        if str(src).endswith(name):
            raise OSError(28, "No space left on device")
        return real_replace(src, dst, *a, **k)

    monkeypatch.setattr(restores.os, "replace", full)
    outbox_worker.rescue(str(root))
    assert not (root / RESTORE_DONE).exists(), "nothing waits, but one could not move"
    assert os.listdir(root / "discarded") == [name]
    monkeypatch.setattr(restores.os, "replace", real_replace)
    outbox_worker.rescue(str(root))
    assert not os.listdir(root / "discarded") and list(_restored_in(root / "ops")) == [name]


def test_a_file_that_fails_to_read_leaves_the_restore_undone(tmp_path, monkeypatch):
    """An I/O error passes; a file this user may not read (`sudo probe`) is no write of theirs
    and must not keep every pass looking forever."""
    root = tmp_path / "outbox"
    _set_aside(root)
    real = restores.Path.read_bytes

    def failing(error):
        return lambda self: (_ for _ in ()).throw(error)

    monkeypatch.setattr(restores.Path, "read_bytes", failing(OSError(5, "Input/output error")))
    assert restore_set_aside(Journal(str(root))).unmoved == 1
    monkeypatch.setattr(restores.Path, "read_bytes", failing(PermissionError(13, "Permission denied")))
    assert restore_set_aside(Journal(str(root))).unmoved == 0
    monkeypatch.setattr(restores.Path, "read_bytes", real)
    assert restore_set_aside(Journal(str(root))).writes == 1


def test_a_paused_outbox_starts_no_restore(tmp_path, monkeypatch):
    root = tmp_path / "outbox"
    _set_aside(root)
    Journal(str(root)).pause()
    monkeypatch.setattr(outbox_worker.rescuer, "spawn_rescuer", lambda j: pytest.fail("spawned"))
    assert outbox_worker.claim_restore(Journal(str(root))) is False
    assert outbox_worker.maybe_restore(Journal(str(root))) is False


def test_nothing_set_aside_means_nothing_done(tmp_path):
    root = tmp_path / "outbox"
    assert restore_set_aside(Journal(str(root))) == RestoreCounts()
    (root / "discarded").mkdir(parents=True)
    _set_aside(root, fp=OTHER_FP)
    assert restore_set_aside(Journal(str(root))).writes == 0
    assert not (root / "ops").exists() or not os.listdir(root / "ops")


# -- what the rescue does with them: sent, refused or deferred ---------------------------------


def _ben(app, tmp_path, url, n=4) -> tuple:
    """Ben's Mac: ``n`` metric writes of one run set aside, stamped with his account."""
    run_id = seeded_run(app, tmp_path)
    root = tmp_path / "outbox"
    for step in range(1, n + 1):
        _set_aside(root, base_url=url, step=step, run_id=run_id, day="2026-10-22" if step % 2 else "2026-10-23")
    _prune_credential_queues(root)
    return root, run_id


def _dispositions(app, root, run_id) -> dict:
    """Each restored write's one outcome, by step: sent (on the server), refused (back aside,
    stamped) or deferred (queued, stamped)."""
    steps = lambda ops: sorted(op["body"]["points"][0]["step_index"] for op in ops.values())  # noqa: E731
    return {
        "sent": _steps_sent(app, run_id),
        "refused": steps(_restored_in(root / "discarded")),
        "deferred": steps(_restored_in(root / "ops")),
    }


def _hold(state_dir_fp=RESTORE_FINGERPRINT):
    from probe.sdk.delivery.outbox.drain.holders import record_holder

    record_holder(state_dir_fp)


def _let_go():
    from probe.sdk.delivery.outbox.drain.holders import _holders_path

    records = json.loads(_holders_path().read_text())
    for holder in records[RESTORE_FINGERPRINT]["holders"]:
        holder["started"] -= 3600
    _holders_path().write_text(json.dumps(records))


SETUPS = {
    # outcome, how the Mac stands, how it stands after it is fixed (None: a final outcome)
    "same_account": ("sent", lambda app, url: _login(url), None),
    "other_account": ("refused", lambda app, url: (
        app.me_identities.__setitem__(STORED, {"customer_id": "lab-99", "user_id": "u-else"}), _login(url)), None),
    "no_login": ("deferred", lambda app, url: None, lambda app, url: _login(url)),
    "me_unanswered": ("deferred", lambda app, url: (setattr(app, "me_status", 503), _login(url)),
                      lambda app, url: setattr(app, "me_status", 200)),
    "live_holder": ("deferred", lambda app, url: (_hold(), _login(url)), lambda app, url: _let_go()),
}


@pytest.mark.parametrize("setup", sorted(SETUPS))
def test_every_restored_write_ends_sent_refused_or_deferred(app, tmp_path, monkeypatch, no_workers,
                                                            restored_events, setup):
    outcome, stand, fix = SETUPS[setup]
    with serve(app) as url:
        root, run_id = _ben(app, tmp_path, url)
        stand(app, url)
        assert outbox_worker.rescue(str(root)) == 0
        found = _dispositions(app, root, run_id)
        assert found == {k: [1, 2, 3, 4] if k == outcome else [] for k in found}, found
        (counts,) = restored_events
        assert (counts.writes, counts.deferred, counts.refused) == (
            4, 4 if outcome == "deferred" else 0, 4 if outcome == "refused" else 0)
        assert (root / RESTORE_DONE).exists() is (outcome != "deferred")
        if fix is None:
            return
        fix(app, url)
        monkeypatch.setattr("probe.sdk.delivery.outbox.drain.credentials._IDENTITY_CACHE", {})
        outbox_worker.rescue(str(root))
        assert _dispositions(app, root, run_id) == {"sent": [1, 2, 3, 4], "refused": [], "deferred": []}
        assert (root / RESTORE_DONE).exists()
        assert len(restored_events) == 1, "the pass that only sent is reported by outbox.rescued"


def test_the_sent_writes_go_out_with_the_stored_login(app, tmp_path, no_workers, restored_events, capsys):
    with serve(app) as url:
        root, run_id = _ben(app, tmp_path, url)
        _login(url)
        outbox_worker.rescue(str(root))
    bearers = {r.headers.get("authorization") for r in app.requests if r.url.path.endswith("/metrics")}
    assert bearers == {f"Bearer {STORED}"}
    assert _steps_sent(app, run_id) == [1, 2, 3, 4]
    out = capsys.readouterr().out
    assert f"restored 4 set-aside write(s) of credential {RESTORE_FINGERPRINT}" in out
    assert "rescue pass: delivered 4" in out


def test_a_refused_write_is_never_tried_again(app, tmp_path, no_workers, restored_events):
    with serve(app) as url:
        root, run_id = _ben(app, tmp_path, url)
        app.me_identities[STORED] = {"customer_id": "lab-99", "user_id": "u-else"}
        _login(url)
        outbox_worker.rescue(str(root))
        (root / RESTORE_DONE).unlink()  # even with the marker gone
        app.me_identities.clear()  # and a login that would send them
        outbox_worker.rescue(str(root))
    assert _steps_sent(app, run_id) == []
    assert len(_restored_in(root / "discarded")) == 4
    first, second = restored_events
    assert (first.refused, first.refused_reason) == (4, "other_account")
    assert (second.writes, second.kept) == (0, {KeptAside.RESTORED_BEFORE: 4})


def test_one_scope_refusal_keeps_every_write_of_the_credential(app, tmp_path, no_workers, restored_events):
    """`adoption_account` keeps a credential's writes for one write refused for scope; kept
    aside alone, that refusal would vanish from its view and the login would send the rest."""
    run_id = seeded_run(app, tmp_path)
    root = tmp_path / "outbox"
    with serve(app) as url:
        _set_aside(root, base_url=url, step=1, run_id=run_id, refused_for_scope=True,
                   last_error="ScopeError: insufficient scope: write required")
        _set_aside(root, base_url=url, step=2, run_id=run_id)
        _prune_credential_queues(root)
        _login(url)
        outbox_worker.rescue(str(root))
    assert _steps_sent(app, run_id) == [] and len(os.listdir(root / "discarded")) == 2
    (counts,) = restored_events
    assert (counts.writes, counts.kept) == (0, {KeptAside.SCOPE: 2})


def test_writes_with_no_account_on_record_are_refused(app, tmp_path, no_workers, restored_events):
    """D4: neither a stamp nor a recorded account says whose they were: nothing goes out."""
    run_id = seeded_run(app, tmp_path)
    root = tmp_path / "outbox"
    with serve(app) as url:
        _set_aside(root, base_url=url, run_id=run_id, account=None)
        _prune_credential_queues(root)
        _login(url)
        outbox_worker.rescue(str(root))
    assert _steps_sent(app, run_id) == [] and len(_restored_in(root / "discarded")) == 1
    (counts,) = restored_events
    assert counts.refused_reason == "unknown_account"


def test_a_paused_outbox_restores_nothing_and_stays_undone(tmp_path, no_workers, restored_events):
    root = tmp_path / "outbox"
    _set_aside(root)
    Journal(str(root)).pause()
    outbox_worker.rescue(str(root))
    assert len(os.listdir(root / "discarded")) == 1 and not (root / RESTORE_DONE).exists()
    assert restored_events == []


def test_a_machine_with_nothing_to_restore_reports_nothing_and_is_done(tmp_path, no_workers, restored_events):
    root = tmp_path / "outbox"
    _set_aside(root, fp=OTHER_FP)
    outbox_worker.rescue(str(root))
    assert (root / RESTORE_DONE).exists() and restored_events == []
    assert len(os.listdir(root / "discarded")) == 1


# -- what starts it ---------------------------------------------------------------------------


def test_the_every_command_check_starts_the_rescuer_until_the_restore_is_done(tmp_path, monkeypatch):
    root = tmp_path / "outbox"
    _set_aside(root)
    journal = Journal(str(root))
    started: list = []
    monkeypatch.setattr(outbox_worker.rescuer, "spawn_rescuer", lambda j: started.append(j.dir) or True)
    # An idle rescue (an older CLI's) put the next look off by hours: the restore does not wait.
    stamp = outbox_worker._rescue_stamp(journal)
    stamp.write_text("x")
    later = time.time() + outbox_worker.RESCUE_IDLE_SECONDS
    os.utime(stamp, (later, later))
    assert outbox_worker.maybe_rescue(journal, {}) is True
    assert outbox_worker.maybe_rescue(journal, {}) is False, "at most once per ten minutes"
    os.utime(root / outbox_worker._RESTORE_STAMP, (1, 1))
    (root / RESTORE_DONE).write_text("x")
    assert outbox_worker.maybe_rescue(journal, {}) is False, "done: nothing to start it for"
    assert started == [root]


def test_no_set_aside_folder_starts_nothing(tmp_path, monkeypatch):
    root = tmp_path / "outbox"
    Journal(str(root))._ensure()
    monkeypatch.setattr(outbox_worker.rescuer, "spawn_rescuer", lambda j: pytest.fail("spawned"))
    assert outbox_worker.claim_restore(Journal(str(root))) is False
    assert outbox_worker.maybe_rescue(Journal(str(root)), {}) is False


def test_the_killswitch_starts_nothing(tmp_path, monkeypatch):
    root = tmp_path / "outbox"
    _set_aside(root)
    monkeypatch.setenv(outbox_worker.RESCUE_ENV, "off")
    monkeypatch.setattr(outbox_worker.rescuer, "spawn_rescuer", lambda j: pytest.fail("spawned"))
    assert outbox_worker.maybe_rescue(Journal(str(root)), {}) is False


def test_the_probe_service_starts_it_with_the_login_shells_variables(tmp_path, monkeypatch):
    """No command at all: the service starting after the update starts the restore, once
    per ten minutes while it is not done."""
    from tests.test_outbox_pause_expiry import _running_service, _wait

    root = tmp_path / "outbox"
    _set_aside(root)
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(root))
    started: list = []
    monkeypatch.setattr(outbox_worker.rescuer, "spawn_rescuer",
                        lambda journal, env=None: started.append((str(journal.dir), env)) or True)
    env = {"PATH": "/usr/bin:/bin", "PROBE_CONFIG_PATH": str(tmp_path / "probe" / "config.json")}
    with _running_service(tmp_path, monkeypatch, env):
        assert _wait(lambda: len(started) == 1)
        time.sleep(0.5)
    assert started == [(str(root), env)]


def test_the_probe_service_honors_the_login_shells_killswitch(tmp_path, monkeypatch):
    from tests.test_outbox_pause_expiry import _running_service, _wait

    root = tmp_path / "outbox"
    _set_aside(root)
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(root))
    started: list = []
    monkeypatch.setattr(outbox_worker.rescuer, "spawn_rescuer", lambda journal, env=None: started.append(env) or True)
    with _running_service(tmp_path, monkeypatch, {"PATH": "/usr/bin", outbox_worker.RESCUE_ENV: "off"}):
        assert _wait(lambda: (root / outbox_worker._RESTORE_STAMP).exists()), "the look never ran"
        time.sleep(0.5)
    assert started == []


def test_the_service_started_rescuer_keeps_the_services_home_and_no_credential(monkeypatch):
    """Its login-shell variables carry no HOME or TMPDIR (where the fallback outboxes are)."""
    monkeypatch.setenv("HOME", "/home/someone")
    monkeypatch.setenv("TMPDIR", "/tmp/someone")
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_service_own_0123456789")
    env = outbox_worker._rescuer_env({"PATH": "/usr/bin", "XDG_STATE_HOME": "/s"})
    assert (env["HOME"], env["TMPDIR"], env["XDG_STATE_HOME"], env["PATH"]) == ("/home/someone", "/tmp/someone", "/s", "/usr/bin")
    assert "PROBE_TOKEN" not in env and env["PROBE_OUTBOX_WORKER"] == "1"


def test_the_every_command_check_restores_an_outbox_with_no_status_file(tmp_path, monkeypatch):
    import importlib

    main = importlib.import_module("probe.cli.main")
    root = tmp_path / "outbox"
    _set_aside(root)
    _prune_credential_queues(root)
    assert Journal.read_status(str(root)) is None
    started: list = []
    monkeypatch.setattr(outbox_worker.rescuer, "spawn_rescuer", lambda j: started.append(j.dir) or True)
    monkeypatch.setattr(main._conn, "spool_dir", str(root))
    main._outbox_notice()
    assert started == [root]


def test_a_restored_write_is_proof_its_credential_could_not_send():
    """Only the lane heads ever recorded the 401; the rest of a set-aside backlog has no
    `last_error`, so a restored write must count as the dead key's evidence."""
    from probe.sdk.delivery.outbox.drain.adoption import op_shows_dead_credential

    op = {"context": {"principal": _stamp()}, "last_error": None, RESTORED_KEY: "2026-11-01T00:00:00+00:00"}
    assert not op_shows_dead_credential(op) and restores.was_restored(op)


# -- the report --------------------------------------------------------------------------------


@pytest.fixture()
def captured(monkeypatch):
    records: list[dict] = []
    monkeypatch.setenv("PROBE_TELEMETRY", "on")
    monkeypatch.setattr(telemetry.sender, "_sender", None)
    monkeypatch.setattr(telemetry.sender, "_flush_registered", True)
    monkeypatch.setattr(telemetry._Sender, "start", lambda self: None)
    monkeypatch.setattr(telemetry._Sender, "put", lambda self, rec: records.append(rec))
    return records


def _restored_props(records) -> list:
    return [r["properties"] for r in records if r["event"] == telemetry.EVENT_OUTBOX_RESTORED]


def test_outbox_restored_carries_counts_only(tmp_path, captured):
    root = tmp_path / "outbox"
    _set_aside(root, step=1)
    _set_aside(root, step=2, day="2026-10-23")
    _set_aside(root, step=3, last_error="NotFoundError: run not found")
    counts = restore_set_aside(Journal(str(root)))
    counts.deferred = 2
    assert telemetry.emit_outbox_restored(counts) is True
    (props,) = _restored_props(captured)
    assert {k: props.get(k) for k in ("writes", "uploads", "bytes_gone", "by_enqueue_day", "kept",
                                      "refused", "refused_reason", "deferred")} == {
        "writes": 2, "uploads": 0, "bytes_gone": 0,
        "by_enqueue_day": {"2026-10-23": 1, "2026-10-22": 1},
        "kept": {"refused": 1}, "refused": 0, "refused_reason": None, "deferred": 2,
    }
    text = json.dumps(props)
    assert RESTORE_FINGERPRINT not in text and str(tmp_path) not in text and "/v1/runs" not in text


@pytest.mark.parametrize(("env", "base_url"), [({"PROBE_TELEMETRY": "off"}, HOSTED),
                                               ({}, "https://research.internal.example.com")])
def test_outbox_restored_honors_the_killswitch_and_self_host(tmp_path, monkeypatch, captured, env, base_url):
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    root = tmp_path / "outbox"
    _set_aside(root, base_url=base_url)
    counts = restore_set_aside(Journal(str(root)))
    assert counts.writes == 1
    assert telemetry.emit_outbox_restored(counts) is False
    assert _restored_props(captured) == []
