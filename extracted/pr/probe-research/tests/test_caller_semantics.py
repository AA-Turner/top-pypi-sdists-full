"""What a caller may conclude from a write that returned nothing.

`Client.write` returns the server's row when it goes over the network and None
when it queues. Roughly forty call sites were written when writes were always
synchronous, and they read that value for four different jobs: verifying a
write landed, deciding whether to delete durable state, counting what shipped,
and refreshing a local handle. Under async they all see None -- and every test
stayed green, because None was always a legal value. It just means something
else now.

Four categories, and one test per real hazard:

  1. durable state deleted on a clean return
  2. ordering: a queued write and a server read disagreeing
  3. verification that only runs on a returned row
  4. counters and status fields reporting queued as landed
"""

from __future__ import annotations

import warnings

import pytest

from probe.sdk import errors
from probe.sdk.run import Run

from tests.conftest import make_client
from tests.test_outbox import seeded_run


@pytest.fixture(autouse=True)
def _isolated_config(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe.json"))
    monkeypatch.delenv("PROBE_ASYNC", raising=False)
    monkeypatch.delenv("PROBE_FINISH_TIMEOUT_SEC", raising=False)


# -- 2. ordering: the deferred close must not revert queued tags --------------


def test_a_deferred_finish_does_not_clobber_queued_tags(app, tmp_path, monkeypatch):
    """`set_tags` REPLACES the whole list, so a queued one and a server read
    disagree by construction. The bounded finish used to read the run over the
    network, capture that stale list as its "restore the tags" beacon value,
    and stamp it into the terminal PATCH -- and FIFO lands the queued tag write
    FIRST, so the close then reverted it. Silent, and it needs exactly the
    conditions a bounded finish exists for.
    """
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = Run(client, {"id": run_id})

    # A tag write that is still queued when the close happens.
    client.journal.append_http(
        "PATCH", f"/v1/runs/{run_id}", {"tags": ["keep-me"]}, run_ref=run_id
    )
    queued = [op for op in run._queued_ops(client.journal.pending())]
    assert any("tags" in (op.get("body") or {}) for op in queued)

    report = run._queue_deferred_finish("completed", None, len(queued))

    terminal = [op for op in run._queued_ops(client.journal.pending())][-1]
    assert "tags" not in (terminal.get("body") or {}), (
        "the deferred close re-sent a tag list it read from the server, which "
        "FIFO replays AFTER the caller's queued tag write and reverts it"
    )
    assert report["finish_queued"] is True
    client.close()


def test_the_draining_beacon_still_fires_without_a_queued_tag_write(app, tmp_path):
    """Skipping the beacon is the narrow remedy, not the new default: with no
    tag write in flight there is nothing to clobber and the dashboard should
    still learn the run is draining."""
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = Run(client, {"id": run_id})
    client.journal.append_http(
        "POST", f"/v1/runs/{run_id}/metrics", {"points": []}, run_ref=run_id
    )

    run._queue_deferred_finish("completed", None, 1)

    assert "draining" in app.runs[run_id]["tags"]
    terminal = [op for op in run._queued_ops(client.journal.pending())][-1]
    assert "tags" in (terminal.get("body") or {}), "the beacon must still be cleared"
    client.close()


# -- 3. verification that only runs on a returned row -------------------------


def test_set_tags_verification_actually_runs(app, tmp_path):
    """The pre-0066 guard catches a backend that accepts `tags`, ignores them
    and answers 200. It runs only `if data:`, so under async it never fired for
    the SDK callers it was written for -- and `run.tags` kept reporting the
    pre-write list."""
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = Run(client, {"id": run_id})

    data = run.set_tags(["alpha", "beta"])

    assert data is not None, "set_tags must return the row its guard verifies"
    assert set(run.tags) == {"alpha", "beta"}, "the handle must reflect the write"
    client.close()


def test_a_queued_env_ref_says_it_was_not_verified(app, tmp_path):
    """env_ref stays async on purpose -- finish() orders its completeness check
    after the drain so this PATCH and the code snapshot are observed together.
    The lost capability probe is therefore announced rather than silently
    skipped: a guard nobody knows was skipped is worse than no guard."""
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = Run(client, {"id": run_id})

    with pytest.warns(UserWarning, match="env_ref was queued"):
        run._pin_env_ref_for_test() if hasattr(run, "_pin_env_ref_for_test") else run.snapshot(
            cwd=str(tmp_path), include_env=False, include_gpu=False
        )
    client.close()


def test_reconcile_artifact_sees_a_queued_record(app, tmp_path):
    """The duplicate-prevention scan listed the server only. Under async the
    original log_artifact may still be queued, so the listing found nothing,
    the caller re-logged, and BOTH landed on drain -- producing exactly the
    duplicate this method exists to prevent."""
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = Run(client, {"id": run_id})

    run.log_artifact("ckpt", uri="s3://b/ckpt", content_hash="sha256:abc")
    assert client.journal.pending(), "the artifact write must still be queued"

    found = run.reconcile_artifact("ckpt", "sha256:abc")

    assert found is not None, "a queued artifact is already recorded; re-logging duplicates it"
    assert found.get("state") == "queued", "it has no server id yet — say so"
    client.close()


# -- 4. counters and status that must not report queued as landed -------------


def test_an_async_reward_reads_queued_not_spooled(app, tmp_path, monkeypatch):
    """`None` means BOTH "journaled, will deliver" and "fail-open spooled after
    a failure". Collapsing them made every healthy async trial record permanent
    partial capture -- and that verdict rides into the published manifest via
    capture_report, so a fine run advertised itself as incomplete."""
    from probe.connectors.harbor import capture_trial, stage_trial
    from tests.conftest import open_run
    from tests.test_harbor_connector import _write_trial

    # This reward-state test captures the fixture's opaque native fork state.
    monkeypatch.setenv("PROBE_ARTIFACT_OPAQUE_POLICY", "allow")
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = open_run(client, experiment="e", name="r")
    staged = stage_trial(_write_trial(tmp_path / "live"), tmp_path / "pvc" / "trial")

    capture_trial(run, staged, step_index=7, expand=False)

    recorded = staged.ledger.context.get("reward_logged") or {}
    assert recorded.get("state") == "queued", (
        f"a healthy async write recorded {recorded.get('state')!r}; only a "
        "fail-open spool after a real failure is 'spooled'"
    )
    client.close()


def test_a_dropped_reward_reads_dropped_not_queued(app, tmp_path, monkeypatch):
    """#2022 review. A reward at or below a resumed run's resume point is
    DROPPED, and `log()` returns None for that as for a queued write: the
    ledger recorded it as `queued`, which nothing would ever deliver."""
    from probe.connectors.harbor import capture_trial, stage_trial
    from tests.conftest import open_run
    from tests.test_harbor_connector import _write_trial

    monkeypatch.setenv("PROBE_ARTIFACT_OPAQUE_POLICY", "allow")
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = open_run(client, experiment="e", name="r")
    run.arm_resume_guard(10)
    staged = stage_trial(_write_trial(tmp_path / "live"), tmp_path / "pvc" / "trial")

    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        capture_trial(run, staged, step_index=7, expand=False)

    assert (staged.ledger.context.get("reward_logged") or {}).get("state") == "dropped"
    client.close()


def test_a_queued_reward_is_retried_by_a_strict_pass(app, tmp_path, monkeypatch):
    """`reward_already_logged` tested the dict's PRESENCE, so an unconfirmed
    reward permanently suppressed the strict retry built to heal it -- the
    retry mechanism was the one thing that could not repair this failure.
    Metric points are idempotent on (run, key, step), so re-attempting is safe.
    """
    from probe.connectors.harbor import capture_trial, stage_trial
    from tests.conftest import open_run
    from tests.test_harbor_connector import _write_trial

    # This reward-state test captures the fixture's opaque native fork state.
    monkeypatch.setenv("PROBE_ARTIFACT_OPAQUE_POLICY", "allow")
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = open_run(client, experiment="e", name="r")
    staged = stage_trial(_write_trial(tmp_path / "live"), tmp_path / "pvc" / "trial")

    capture_trial(run, staged, step_index=7, expand=False)          # queued
    before = app.metrics_inserted
    capture_trial(run, staged, step_index=7, expand=False, strict=True)  # must retry

    assert app.metrics_inserted > before, (
        "a queued reward was treated as already logged, so the strict retry "
        "skipped the write it exists to confirm"
    )
    assert (staged.ledger.context.get("reward_logged") or {}).get("state") == "confirmed"
    client.close()


# -- async artifact uploads: staged, or synchronous ---------------------------


def _ckpt(tmp_path, name="ckpt.bin", body=b"weights-v1"):
    p = tmp_path / name
    p.write_bytes(body)
    return str(p)


def test_an_artifact_upload_is_queued_not_posted(app, tmp_path, monkeypatch):
    """The headline: a checkpoint upload used to run presign → PUT → confirm on
    the caller's thread, so a slow R2 stalled the training loop — the same
    failure class as the original incident, on a different path."""
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = Run(client, {"id": run_id})

    monkeypatch.setattr(
        client.transport, "post", lambda *a, **k: pytest.fail("must not touch the network")
    )
    assert run.log_artifact("ckpt", path=_ckpt(tmp_path)) is None

    # Queued in the waiting room for its credential scan (off this thread),
    # then promoted into an ordinary staged upload op.
    assert len(client.journal.waiting(run_ref=run_id)) == 1
    client.journal.promote_waiting()
    ops = [op for _, op in client.journal.pending()]
    assert [op["kind"] for op in ops] == ["upload"]
    assert ops[0]["upload"]["staged"] is True, "the bytes must be snapshotted"
    client.close()


def test_a_rotated_checkpoint_still_uploads_the_bytes_it_was_given(app, tmp_path):
    """Checkpoint rotation — write ckpt-1000, delete ckpt-900 — is the NORMAL
    shape of this workload. Queueing an op that merely references the live file
    would upload whatever is there at drain time, or dead-letter if it is gone.
    Staging is what makes the queued artifact mean what the caller meant."""
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = Run(client, {"id": run_id})
    path = _ckpt(tmp_path, body=b"epoch-1000")

    run.log_artifact("ckpt", path=path)
    pathlib_path = __import__("pathlib").Path(path)
    pathlib_path.write_bytes(b"epoch-1100-overwritten")  # the loop rotates it
    # Rotated BEFORE the credential scan: the waiting room holds the bytes the
    # caller handed over, not whatever is at the path when the scan runs.
    client.journal.promote_waiting()

    op = [op for _, op in client.journal.pending()][0]
    blob = client.journal.blobs_dir / op["upload"]["blob"]
    assert blob.read_bytes() == b"epoch-1000", "the queued upload captured the wrong bytes"
    client.close()


def test_no_disk_headroom_uploads_synchronously_instead_of_queueing(
    app, tmp_path, monkeypatch
):
    """`append_upload` degrades to an UNSTAGED op when the disk is tight, which
    is right at a command line and wrong beside a training loop. The SDK demands
    a staged op and does the work now rather than take something that references
    a file which may rotate under it."""
    from probe.sdk import journal as journal_mod

    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = Run(client, {"id": run_id})
    monkeypatch.setattr(journal_mod, "MIN_FREE_BYTES", 1 << 60)  # nothing fits

    result = run.log_artifact("ckpt", path=_ckpt(tmp_path))

    assert isinstance(result, dict), "it must have uploaded, not queued"
    assert [op for _, op in client.journal.pending()] == []
    client.close()


def test_an_unstaged_op_is_never_queued(app, tmp_path, monkeypatch):
    """The invariant a headroom PRE-CHECK could not hold.

    Asking "is there room?" and then appending measures free space twice, and
    between the two another writer on this journal can take it -- a neighbouring
    agent session, or this very training loop writing the next checkpoint. The
    pre-check said yes, the append degraded, and an UNSTAGED op went into the
    queue reporting success. At drain that op re-reads the live path, which by
    then is the rotated checkpoint.

    Simulated by a headroom that is fine when asked and gone when used. The
    assertion is the invariant itself, not the call count: whatever this queues,
    it is staged, or it is not queued at all.
    """
    from probe.sdk import journal as journal_mod

    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = Run(client, {"id": run_id})

    seen = {"n": 0}

    def headroom_vanishes(self, src_path):
        seen["n"] += 1
        return None if seen["n"] == 1 else "low disk: another writer took it"

    monkeypatch.setattr(journal_mod.Journal, "_staging_headroom", headroom_vanishes)

    run.log_artifact("ckpt", path=_ckpt(tmp_path))

    for _, op in client.journal.pending():
        assert op["upload"]["staged"] is True, (
            "an unstaged op re-reads src_path at drain; by then it is the "
            "rotated checkpoint, not the bytes that were logged"
        )
    client.close()


def test_strict_and_explicit_sync_still_upload_inline(app, tmp_path):
    """strict means "raise, and hand back the row" — neither of which a queued
    write can do. Same resolution order as Client.write."""
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = Run(client, {"id": run_id})

    strict_row = run.log_artifact("a", path=_ckpt(tmp_path, "a.bin"), strict=True)
    sync_row = run.log_artifact("b", path=_ckpt(tmp_path, "b.bin"), sync=True)

    assert isinstance(strict_row, dict) and isinstance(sync_row, dict)
    assert [op for _, op in client.journal.pending()] == []
    client.close()


def test_probe_async_uploads_off_keeps_uploads_inline(app, tmp_path, monkeypatch):
    """Queueing a metric batch costs a few hundred bytes; queueing a checkpoint
    costs a copy of the checkpoint. Someone may reasonably want one and not the
    other, so uploads have their own knob."""
    monkeypatch.setenv("PROBE_ASYNC_UPLOADS", "0")
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = Run(client, {"id": run_id})

    assert isinstance(run.log_artifact("ckpt", path=_ckpt(tmp_path)), dict)
    assert [op for _, op in client.journal.pending()] == []
    client.close()


def test_a_rejected_queued_upload_still_records_a_reference(app, tmp_path):
    """The synchronous path degrades a permanently-rejected upload to a
    reference row carrying `meta.upload = "failed"`, which `check_run` counts
    as a capture gap. The drainer had no such path, so a queued upload that was
    rejected left NO artifact row anywhere — a capability regression hiding
    inside the feature."""
    from probe.sdk.journal import drain

    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = Run(client, {"id": run_id})
    run.log_artifact("ckpt", path=_ckpt(tmp_path))

    # A PERMANENT rejection. The fake app's `fail_next_uploads` answers 503,
    # which classifies transient and parks the op rather than dead-lettering it.
    def reject(*a, **k):
        raise errors.ValidationError("unsupported content type", status=422)

    client.upload_fingerprinted = reject
    drain(client.journal, client_factory=lambda ctx: client)

    # `ckpt.bin`, not `ckpt`: the upload keeps the file's extension now, and the
    # fake honours the server's exact `name` filter.
    rows = client.list_run_artifacts(run_id, name="ckpt.bin", scope="own") or []
    assert rows, "a rejected upload must still leave a record of the file"
    assert rows[0]["is_reference"] is True
    assert (rows[0].get("meta") or {}).get("upload") == "failed"
    client.close()
