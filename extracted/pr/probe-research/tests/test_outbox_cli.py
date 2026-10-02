"""CLI surface of the async outbox: --async / PROBE_ASYNC enqueue paths, the
intent ping, the outbox command family, the flush alias, and the run-end
barrier (sync = run-scoped drain first; async = ordered journal op).

Wiring mirrors test_cli.py: `cli.Client` is monkeypatched to hand back a
FakeApp-backed client, and the drainer spawn is stubbed out (the worker loop
has its own unit tests -- a CLI test must not fork real processes).
"""

from __future__ import annotations

import contextlib
import json

import pytest
import typer

from probe import cli
from probe.sdk.journal import DrainReport, Journal, drain


from tests.conftest import make_client, open_run


def _cli_main():
    """The `probe.cli.main` MODULE, for reaching its helpers directly.

    `probe.cli` re-exports the `main` FUNCTION under that same name, so the
    attribute shadows the submodule and `cli.main._default_client` is an
    AttributeError on a function. import_module asks for the module by path.
    """
    import importlib

    return importlib.import_module("probe.cli.main")


@pytest.fixture
def outbox_dir(tmp_path):
    return tmp_path / "outbox"


@pytest.fixture
def wired_async(app, outbox_dir, tmp_path, monkeypatch):
    """FakeApp-backed CLI with async credentials available and no real forks."""

    def factory(**kw):
        return make_client(
            app,
            tmp_spool=outbox_dir,
            async_writes=kw.get("async_writes", False),
        )

    monkeypatch.setattr(cli, "Client", factory)
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe.json"))
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_test")
    monkeypatch.setenv("PROBE_BASE_URL", "http://test")
    spawned: list[str | None] = []
    monkeypatch.setattr(
        "probe.cli.outbox_worker.maybe_spawn",
        lambda directory=None: spawned.append(directory) or False,
    )
    cli.main(["experiment", "create", "e", "--question", "h"])
    app.spawned = spawned
    return app


def start_run(app) -> str:
    client = make_client(app)
    run = open_run(client, experiment="e", name="r")
    client.close()
    return run.id


def cli_drain(app, outbox_dir, **kwargs) -> DrainReport:
    client = make_client(app)
    try:
        return drain(Journal(outbox_dir), client_factory=lambda ctx: client, **kwargs)
    finally:
        client.close()


# -- enqueue paths -----------------------------------------------------------


def test_sync_log_path_is_unchanged(wired_async, outbox_dir, capsys):
    """REGRESSION guard: --sync hits the network and leaves the journal empty.

    This used to say "without --async", and it kept passing after the default
    flipped -- for the wrong reason. The fixture injects a transport, and the SDK
    refuses to queue onto an injected transport (nothing could drain it), so a
    bare `log` degrades to sync here even though the default is now async. The
    assertion stayed green while the thing it was guarding stopped being true.
    Pin the FLAG, not the absence of one.
    """
    run_id = start_run(wired_async)
    rc = cli.main(["log", run_id, "loss=0.5", "--step", "1", "--sync"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "logged 1 metric(s)" in out and "(delivered)" in out
    assert wired_async.metric_points_posted[run_id]
    assert Journal(outbox_dir).pending() == []


def test_sync_after_the_subcommand_beats_a_root_async(wired_async, outbox_dir, capsys):
    """Per-command wins over root. `--async` was root-only and a bulk import
    wrote it after the subcommand for every row, getting "No such option" each
    time (test_backfill_enqueue_argv). Both positions work now, and the one
    nearer the verb is the one that means it."""
    run_id = start_run(wired_async)
    assert cli.main(["--async", "log", run_id, "loss=0.5", "--step", "1", "--sync"]) == 0
    assert "(delivered)" in capsys.readouterr().out
    assert Journal(outbox_dir).pending() == [], "--sync after the subcommand must win"


def test_async_log_queues_and_touches_no_run_route(wired_async, outbox_dir, capsys):
    run_id = start_run(wired_async)
    before = len(wired_async.requests)
    rc = cli.main(["--async", "log", run_id, "loss=0.5", "--step", "1"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "logged 1 metric(s)" in out and "(queued)" in out
    assert len(wired_async.requests) == before, (
        "async log must not call the API -- not even get_run (D20-1)"
    )
    ((_, op),) = Journal(outbox_dir).pending()
    assert op["kind"] == "http" and op["run_ref"] == run_id
    assert wired_async.spawned, "enqueue must kick the drainer"
    report = cli_drain(wired_async, outbox_dir)
    assert report.clean and wired_async.metric_points_posted[run_id]


def test_cli_delegates_probe_async_instead_of_parsing_it(monkeypatch, tmp_path):
    """ONE parser owns PROBE_ASYNC, and it is not this one.

    The CLI used to read the variable itself, which meant two implementations of
    the same tri-state that could drift. It now hands the SDK None and lets
    `Client.__init__` resolve it (on / off / unrecognised-warns-and-defers).

    Asserted structurally -- what the CLI PASSES -- rather than by observing a
    resolved client, because the resolution is the SDK's and is already pinned
    there (test_default_async_writes.py). Checking the outcome here would just
    re-test the SDK through two layers of fixture, and did: it read False under
    the suite's injected transport, which is the SDK's guard working correctly.
    """
    cli_main = _cli_main()
    captured: list[dict] = []

    class _Recording:
        def __init__(self, **kwargs):
            captured.append(kwargs)

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    monkeypatch.setattr(cli_main, "Client", _Recording)

    # No flag: the SDK is handed None and does the resolving, whatever
    # PROBE_ASYNC happens to say.
    for value in ("1", "0", "wat", None):
        captured.clear()
        if value is None:
            monkeypatch.delenv("PROBE_ASYNC", raising=False)
        else:
            monkeypatch.setenv("PROBE_ASYNC", value)
        cli_main._default_client(None)
        assert captured[0]["async_writes"] is None, (
            f"PROBE_ASYNC={value!r} must reach the SDK unparsed, not be re-interpreted by the CLI"
        )

    # An explicit flag is the CLI's own answer and does NOT go through the
    # SDK's resolution: `--sync` pins sync, `--async` keeps refusing without
    # deliverable credentials (F7).
    captured.clear()
    cli_main._default_client(False)
    assert captured[0]["async_writes"] is False


def test_default_log_queues_without_any_flag(wired_async, outbox_dir, capsys, monkeypatch):
    """The headline of the flip, and the mirror of the --sync guard above.

    Forced past the injected-transport gate the same way an explicit `--async`
    would be, because the fixture's transport is a test artifact and the default
    under a REAL transport is what this pins.
    """
    run_id = start_run(wired_async)
    monkeypatch.delenv("PROBE_ASYNC", raising=False)
    assert cli.main(["--async", "log", run_id, "loss=1.0", "--step", "1"]) == 0
    out = capsys.readouterr().out
    assert "(queued)" in out and "(delivered)" not in out
    assert len(Journal(outbox_dir).pending()) == 1


def test_async_artifact_add_pings_intent_and_stages(wired_async, outbox_dir, tmp_path, capsys):
    run_id = start_run(wired_async)
    source = tmp_path / "model.bin"
    source.write_bytes(b"weights " * 512)
    rc = cli.main(["--async", "artifact", "add", run_id, str(source)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "added upload" in out and "intent registered" in out and "(queued)" in out
    # The capped ping presigned: the server already holds a pending row (1A).
    (pending_row,) = wired_async.artifacts[run_id]
    assert pending_row["status"] == "pending"
    ((_, op),) = Journal(outbox_dir).pending()
    assert op["upload"]["blob"] is not None, "small file hashes inline (11A)"
    source.write_bytes(b"overwritten")
    report = cli_drain(wired_async, outbox_dir)
    assert report.clean
    # Drain re-presigns (never trusts the ping's row). The REAL server revives
    # the same row in place (uploads_router.py:222); the fake appends a second
    # one -- either way the upload must end complete under this name.
    assert any(
        a["name"] == "model.bin" and a["status"] == "complete"
        for a in wired_async.artifacts[run_id]
    )


def test_async_artifact_add_journals_the_repaired_name(
    wired_async, outbox_dir, tmp_path, capsys
):
    """`--name` with the extension dropped is the shape agents write, and the async
    branch never enters `Client.upload_file` -- it journals a name and the drainer
    POSTs it later. So the repair has to happen at the CLI door, or the queued row
    carries the bare name to a server that will never preview it."""
    run_id = start_run(wired_async)
    source = tmp_path / "study.md"
    source.write_bytes(b"# atomworks\n")
    assert cli.main(
        ["--async", "artifact", "add", run_id, str(source), "--name", "atomworks-study-README"]
    ) == 0
    capsys.readouterr()

    ((_, op),) = Journal(outbox_dir).pending()
    assert op["upload"]["name"] == "atomworks-study-README.md", op["upload"]["name"]
    assert cli_drain(wired_async, outbox_dir).clean
    assert any(
        a["name"] == "atomworks-study-README.md" and a["status"] == "complete"
        for a in wired_async.artifacts[run_id]
    )


def test_async_reference_add_is_a_pure_json_op(wired_async, outbox_dir, tmp_path, capsys):
    run_id = start_run(wired_async)
    source = tmp_path / "big.ckpt"
    source.write_bytes(b"x" * 128)
    rc = cli.main(["--async", "artifact", "add", run_id, str(source), "--reference"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "added reference" in out and "(queued)" in out
    journal = Journal(outbox_dir)
    ((_, op),) = journal.pending()
    assert op["kind"] == "http"
    assert not journal.blobs_dir.exists() or list(journal.blobs_dir.iterdir()) == []
    assert cli_drain(wired_async, outbox_dir).clean
    (artifact,) = wired_async.artifacts[run_id]
    assert artifact["is_reference"] is True


def test_a_code_kind_is_uploaded_even_when_reference_was_asked_for(
    wired_async, outbox_dir, tmp_path, capsys
):
    """Code is stored, never pointed at.

    A `file://` pointer to a training script resolves on one box, for as long as
    that box and that checkout survive, and nothing downstream can tell a live
    pointer from a dead one. That is the failure git referencing was retired from
    `capture_manifest` for; the manual door must not keep it open.
    """
    run_id = start_run(wired_async)
    source = tmp_path / "train.py"
    source.write_text("print('go')\n")

    rc = cli.main(
        ["--async", "artifact", "add", run_id, str(source), "--reference", "--kind", "code"]
    )

    assert rc == 0
    captured = capsys.readouterr()
    assert "added upload" in captured.out, "must take the upload path, not the reference one"
    assert "stored, not referenced" in captured.err, "a silent flip reads as a broken flag"
    ((_, op),) = Journal(outbox_dir).pending()
    assert op["kind"] == "upload", "the bytes have to be staged"
    assert cli_drain(wired_async, outbox_dir).clean
    # The fake appends a fresh row on the drain's re-presign rather than reviving
    # the pending one in place (see test_async_upload... above), so match on the
    # outcome rather than on there being exactly one row.
    rows = [a for a in wired_async.artifacts[run_id] if a["name"] == "train.py"]
    assert rows and all(a["is_reference"] is not True for a in rows), "bytes, not a pointer"
    assert any(a["status"] == "complete" for a in rows)


def test_a_non_code_kind_still_references(wired_async, outbox_dir, tmp_path, capsys):
    """The carve-out is code, not --reference. A checkpoint still records a path."""
    run_id = start_run(wired_async)
    source = tmp_path / "model.ckpt"
    source.write_bytes(b"x" * 128)

    rc = cli.main(
        ["--async", "artifact", "add", run_id, str(source), "--reference", "--kind", "checkpoint"]
    )

    assert rc == 0
    assert "added reference" in capsys.readouterr().out
    ((_, op),) = Journal(outbox_dir).pending()
    assert op["kind"] == "http"


def test_an_unreadable_code_reference_is_refused_not_recorded(
    wired_async, outbox_dir, tmp_path, capsys
):
    """--allow-missing exists so a path on a mount this host cannot see is still
    recorded. For code that is precisely the row being retired, and there is no
    upload to fall back to -- so it fails loudly instead."""
    run_id = start_run(wired_async)
    missing = tmp_path / "gone.py"

    rc = cli.main(
        [
            "--async", "artifact", "add", run_id, str(missing),
            "--reference", "--allow-missing", "--kind", "code",
        ]
    )

    assert rc != 0
    assert "readable from this host" in capsys.readouterr().err
    assert Journal(outbox_dir).pending() == [], "nothing may be queued for a refused row"


def test_a_manifest_code_row_uploads_too(wired_async, outbox_dir, tmp_path, capsys):
    """Enforced per ROW as well as per command line. A rule that holds on one and
    not the other is discovered a hundred thousand rows later, server-side."""
    run_id = start_run(wired_async)
    script = tmp_path / "train.py"
    script.write_text("print('go')\n")
    ckpt = tmp_path / "base.ckpt"
    ckpt.write_bytes(b"y" * 64)
    path = manifest(
        tmp_path,
        {"path": str(script), "reference": True, "kind": "code", "run": run_id},
        {"path": str(ckpt), "reference": True, "kind": "checkpoint", "run": run_id},
    )
    capsys.readouterr()

    rc = cli.main(["artifact", "add", "--from-manifest", path])

    assert rc == 0
    summary = json.loads(capsys.readouterr().out)
    assert (summary["uploads"], summary["references"]) == (1, 1)
    assert cli_drain(wired_async, outbox_dir).clean
    by_name = {a["name"]: a for a in wired_async.artifacts[run_id]}
    assert by_name["train.py"]["is_reference"] is not True
    assert by_name["base.ckpt"]["is_reference"] is True


def test_size_never_promotes_a_code_row_back_to_a_reference(
    wired_async, outbox_dir, tmp_path, capsys
):
    """The manifest path promotes a big row to a reference on size alone. A code
    row demoted out of `reference` must not be handed straight back to it — that
    would reinstate the pointer through the other door."""
    run_id = start_run(wired_async)
    big_script = tmp_path / "generated_model.py"
    big_script.write_text("X = [\n" + "  1,\n" * 2000 + "]\n")
    assert big_script.stat().st_size > 1024
    path = manifest(tmp_path, {"path": str(big_script), "kind": "code", "run": run_id})
    capsys.readouterr()

    rc = cli.main(["artifact", "add", "--from-manifest", path, "--reference-over", "1024"])

    assert rc == 0
    summary = json.loads(capsys.readouterr().out)
    assert (summary["uploads"], summary["references"]) == (1, 0)
    assert cli_drain(wired_async, outbox_dir).clean
    rows = [a for a in wired_async.artifacts[run_id] if a["name"] == "generated_model.py"]
    assert rows and all(a["is_reference"] is not True for a in rows)


def test_the_hyphenated_code_kind_is_caught_too(wired_async, outbox_dir, tmp_path, capsys):
    """`--kind` is free-form and the repo spells this kind both ways -- the SDK
    writes `code_snapshot`, app/artifacts/preview.py matches `code-snapshot`.
    A rule that knows only one spelling is a rule with a hole in it."""
    run_id = start_run(wired_async)
    source = tmp_path / "train.py"
    source.write_text("print('go')\n")

    rc = cli.main(
        ["--async", "artifact", "add", run_id, str(source),
         "--reference", "--kind", " Code-Snapshot "]
    )

    assert rc == 0
    assert "added upload" in capsys.readouterr().out
    ((_, op),) = Journal(outbox_dir).pending()
    assert op["kind"] == "upload"


def test_a_file_uri_cannot_smuggle_a_code_pointer_past_the_rule(
    wired_async, outbox_dir, tmp_path, capsys
):
    """`--uri` is the second door to the same dead pointer. A bucket uri stays
    legal for every kind -- those name durable storage."""
    run_id = start_run(wired_async)

    rc = cli.main(
        ["--async", "artifact", "add", run_id, "--name", "train.py",
         "--uri", "file:///gone/train.py", "--kind", "code"]
    )
    assert rc != 0
    assert "cannot be a file:// pointer" in capsys.readouterr().err
    assert Journal(outbox_dir).pending() == []

    rc = cli.main(
        ["--async", "artifact", "add", run_id, "--name", "train.py",
         "--uri", "s3://bucket/code.tar.gz", "--kind", "code"]
    )
    assert rc == 0, "a bucket uri is durable storage, not a machine-local path"


def test_async_requires_deliverable_credentials(wired_async, monkeypatch, capsys):
    monkeypatch.delenv("PROBE_TOKEN", raising=False)
    rc = cli.main(["--async", "log", "r-1", "loss=1.0"])
    assert rc != 0
    err = capsys.readouterr().err
    from probe.sdk.session_marker import WIZARD_HINT

    assert WIZARD_HINT in err and "PROBE_TOKEN" in err


# -- outbox command family ---------------------------------------------------


def test_outbox_status_reports_and_exits_two_when_pending(wired_async, outbox_dir, capsys):
    run_id = start_run(wired_async)
    assert cli.main(["--spool-dir", str(outbox_dir), "outbox", "status"]) == 0
    capsys.readouterr()
    cli.main(["--async", "log", run_id, "loss=1.0"])
    capsys.readouterr()
    rc = cli.main(["--spool-dir", str(outbox_dir), "outbox", "status", "--verbose"])
    assert rc == 2
    payload = json.loads(capsys.readouterr().out)
    assert payload["pending"] == 1
    assert payload["ops"][0]["run_ref"] == run_id


def test_outbox_pause_blocks_drain_and_resume_rekicks(wired_async, outbox_dir, capsys):
    run_id = start_run(wired_async)
    cli.main(["--async", "log", run_id, "loss=1.0"])
    assert cli.main(["--spool-dir", str(outbox_dir), "outbox", "pause"]) == 0
    assert cli_drain(wired_async, outbox_dir).delivered == 0
    kicks_before = len(wired_async.spawned)
    assert cli.main(["--spool-dir", str(outbox_dir), "outbox", "resume"]) == 0
    assert len(wired_async.spawned) > kicks_before


def test_outbox_retry_requeues_dead_letters(wired_async, outbox_dir, capsys):
    journal = Journal(outbox_dir)
    journal.append_http("POST", "/v1/runs/poisoned/badroute", {})
    assert not cli_drain(wired_async, outbox_dir).clean
    assert len(journal.failed()) == 1
    assert cli.main(["--spool-dir", str(outbox_dir), "outbox", "retry"]) == 0
    assert "requeued 1" in capsys.readouterr().out
    assert len(journal.pending()) == 1 and journal.failed() == []


def test_flush_is_an_alias_of_outbox_drain(wired_async, outbox_dir, monkeypatch, capsys):
    """REGRESSION guard: `probe flush` must drain the journal exactly like
    `probe outbox drain` (it replaced the old spool-only replay)."""
    run_id = start_run(wired_async)
    cli.main(["--async", "log", run_id, "loss=1.0", "--step", "1"])
    capsys.readouterr()

    def factory_drain(journal, run_ref=None, **kw):
        # The alias claim is about WIRING: flush must drain the --spool-dir
        # journal, unscoped (testing review: a stub ignoring `journal` could
        # not catch flush resolving the wrong directory).
        assert journal.dir == outbox_dir and run_ref is None
        return cli_drain(wired_async, outbox_dir, run_ref=run_ref)

    monkeypatch.setattr("probe.sdk.journal.drain", factory_drain)
    rc = cli.main(["--spool-dir", str(outbox_dir), "flush"])
    assert rc == 0
    assert "delivered 1" in capsys.readouterr().out
    assert wired_async.metric_points_posted[run_id]


# -- run end barriers --------------------------------------------------------


def test_run_end_sync_refuses_while_run_ops_undeliverable(
    wired_async, outbox_dir, monkeypatch, capsys
):
    run_id = start_run(wired_async)
    monkeypatch.setattr(
        "probe.sdk.journal.drain",
        lambda j, run_ref=None, **k: DrainReport(
            remaining=1, stopped_transient=True, errors=["net down"]
        ),
    )
    rc = cli.main(["--spool-dir", str(outbox_dir), "run", "end", run_id])
    assert rc == 2
    assert "NOT closed" in capsys.readouterr().err
    assert wired_async.runs[run_id]["status"] != "completed"


def test_run_end_sync_refuses_on_this_runs_dead_letters(
    wired_async, outbox_dir, monkeypatch, capsys
):
    run_id = start_run(wired_async)
    journal = Journal(outbox_dir)
    journal.append_http("POST", f"/v1/runs/{run_id}/badroute", {})
    assert not cli_drain(wired_async, outbox_dir).clean  # dead-letters it
    monkeypatch.setattr("probe.sdk.journal.drain", lambda j, run_ref=None, **k: DrainReport())
    rc = cli.main(["--spool-dir", str(outbox_dir), "run", "end", run_id])
    assert rc == 2
    assert "retry dead letters" in capsys.readouterr().err


def test_run_end_sync_closes_when_clean(wired_async, outbox_dir, monkeypatch, capsys):
    run_id = start_run(wired_async)
    monkeypatch.setattr("probe.sdk.journal.drain", lambda j, run_ref=None, **k: DrainReport())
    rc = cli.main(["--spool-dir", str(outbox_dir), "run", "end", run_id])
    assert rc == 0
    assert wired_async.runs[run_id]["status"] == "completed"


def test_run_end_async_is_ordered_behind_the_runs_data(wired_async, outbox_dir, capsys):
    run_id = start_run(wired_async)
    cli.main(["--async", "log", run_id, "loss=1.0", "--step", "1"])
    rc = cli.main(["--async", "run", "end", run_id])
    assert rc == 0
    assert "queued end" in capsys.readouterr().out
    ops = [op for _, op in Journal(outbox_dir).pending()]
    assert [op["method"] for op in ops] == ["POST", "PATCH"], (
        "run_end must sit BEHIND the run's queued data (the ordering IS the barrier)"
    )
    assert wired_async.runs[run_id]["status"] != "completed"
    assert cli_drain(wired_async, outbox_dir).clean
    assert wired_async.runs[run_id]["status"] == "completed"
    assert wired_async.metric_points_posted[run_id]


# -- the offline handle's writer epoch (SDK reliability 1.10) ------------------


def _reopened_run(app) -> str:
    """A run a relaunch has reopened once: the server is on epoch 2."""
    import uuid

    run_id = start_run(app)
    app.runs[run_id]["status"] = "crashed"
    client = make_client(app)
    try:
        assert client.reopen_run(run_id, session_id=str(uuid.uuid4()))["write_epoch"] == 2
    finally:
        client.close()
    return run_id


def test_async_log_on_a_reopened_run_is_not_fenced(wired_async, outbox_dir):
    """`probe --async log` builds its handle offline (`Run(client, {"id":
    ref})`, no GET), and that handle defaulted to epoch 1 -- so on any
    reopened run every queued point was refused 409 and dead-lettered. An
    epoch nothing supplied is sent as no epoch at all."""
    run_id = _reopened_run(wired_async)
    assert cli.main(["--async", "log", run_id, "loss=0.5", "--step", "1"]) == 0
    ((_, op),) = Journal(outbox_dir).pending()
    assert "write_epoch" not in op["body"], op["body"]

    cli_drain(wired_async, outbox_dir)
    assert Journal(outbox_dir).failed() == [], "the point was dead-lettered"
    assert wired_async.metric_points_posted[run_id]
    assert wired_async.fenced_writes == []


def test_async_run_end_on_a_reopened_run_closes_it(wired_async, outbox_dir):
    """The same default would have refused `probe run end --async` the moment
    the terminal PATCH started carrying an epoch (1.10)."""
    run_id = _reopened_run(wired_async)
    assert cli.main(["--async", "run", "end", run_id]) == 0
    cli_drain(wired_async, outbox_dir)
    assert Journal(outbox_dir).failed() == []
    assert wired_async.runs[run_id]["status"] == "completed"


def test_the_async_handle_stamps_the_brackets_pinned_epoch(wired_async, outbox_dir):
    """`probe run start` pins the generation it opened in the lease (0185),
    and the synchronous handle stamps it. The offline handle reads the same
    local pin, so a bracket superseded by a reopen elsewhere still fences."""
    from probe.cli import run_lock

    run_id = _reopened_run(wired_async)
    run_lock.touch_lease(run_id, write_epoch=2)
    assert cli.main(["--async", "log", run_id, "loss=0.5", "--step", "1"]) == 0
    ((_, op),) = Journal(outbox_dir).pending()
    assert op["body"]["write_epoch"] == 2


def _bracket_whose_job_reopened(app) -> str:
    """The measured shape (review of #2010, MED-1): `probe run start` pins
    epoch 1, the quiet bracket is reaped `untracked`, and the job's own
    `probe.init()` attaches through PROBE_RUN_ID and reopens it: epoch 2."""
    from datetime import datetime, timedelta, timezone

    UTC = timezone.utc

    from probe.cli import run_lock

    run_id = start_run(app)
    run_lock.touch_lease(run_id, write_epoch=1)  # what `probe run start` does
    app.runs[run_id].update(
        status="untracked", ended_at=(datetime.now(UTC) - timedelta(minutes=1)).isoformat()
    )
    client = make_client(app)
    try:
        job = client.attach_run(run_id, heartbeat=False, reopen_if_dead=True)
    finally:
        client.close()
    assert job.write_epoch == 2 and app.runs[run_id]["write_epoch"] == 2
    return run_id


def test_the_jobs_own_reopen_moves_the_brackets_pin(wired_async, outbox_dir):
    from probe.cli import run_lock

    run_id = _bracket_whose_job_reopened(wired_async)

    assert run_lock.lease_write_epoch(run_id) == 2
    assert cli.main(["--async", "log", run_id, "loss=0.5", "--step", "1"]) == 0
    ((_, op),) = Journal(outbox_dir).pending()
    assert op["body"]["write_epoch"] == 2


def test_sync_run_end_closes_the_run_after_the_jobs_own_reopen(wired_async, outbox_dir):
    run_id = _bracket_whose_job_reopened(wired_async)

    assert cli.main(["--spool-dir", str(outbox_dir), "run", "end", run_id]) == 0

    assert wired_async.runs[run_id]["status"] == "completed"
    assert wired_async.fenced_writes == []


def test_async_run_end_closes_the_run_after_the_jobs_own_reopen(wired_async, outbox_dir):
    run_id = _bracket_whose_job_reopened(wired_async)

    assert cli.main(["--async", "run", "end", run_id]) == 0
    cli_drain(wired_async, outbox_dir)

    assert Journal(outbox_dir).failed() == []
    assert wired_async.runs[run_id]["status"] == "completed"


def test_a_reopen_never_creates_a_lease(app, tmp_path):
    """Only a bracket's live lease is re-pinned; an SDK run with no bracket
    must not grow a lease file (it would hold the box against auto-update)."""
    from datetime import datetime, timedelta, timezone

    UTC = timezone.utc

    from probe.cli import run_lock

    client = make_client(app, tmp_spool=tmp_path / "spool")
    run = open_run(client, experiment="e", name="r", heartbeat=False)
    app.runs[run.id].update(
        status="untracked", ended_at=(datetime.now(UTC) - timedelta(minutes=1)).isoformat()
    )
    client.attach_run(run.id, heartbeat=False, reopen_if_dead=True)
    client.close()
    assert run_lock.lease_write_epoch(run.id) is None


# -- run-scoped repair (parity F6) ---------------------------------------------


def test_outbox_retry_and_status_scope_to_a_run(wired_async, outbox_dir, capsys):
    journal = Journal(outbox_dir)
    journal.append_http("POST", "/v1/runs/r-1/badroute", {})
    journal.append_http("POST", "/v1/runs/r-2/badroute", {})
    cli_drain(wired_async, outbox_dir)  # dead-letters both
    capsys.readouterr()

    rc = cli.main(["--spool-dir", str(outbox_dir), "outbox", "status", "--run", "r-1"])
    assert rc == 2
    summary = json.loads(capsys.readouterr().out)
    assert summary["run"] == "r-1"
    assert summary["failed"] == 1, "the other run's dead letter must not count"

    rc = cli.main(["--spool-dir", str(outbox_dir), "outbox", "retry", "--run", "r-1"])
    assert rc == 0
    assert "requeued 1 op(s)" in capsys.readouterr().out
    assert [op["run_ref"] for _, op in Journal(outbox_dir).pending()] == ["r-1"]
    assert [op["run_ref"] for _, op in Journal(outbox_dir).failed()] == ["r-2"]


# -- producer accounting (parity F4) ------------------------------------------


def test_outbox_status_reports_producers(wired_async, outbox_dir, capsys):
    run_id = start_run(wired_async)
    cli.main(["--async", "log", run_id, "loss=1.0", "--step", "1"])
    capsys.readouterr()
    rc = cli.main(["--spool-dir", str(outbox_dir), "outbox", "status"])
    assert rc == 2  # pending op
    summary = json.loads(capsys.readouterr().out)
    (producer,) = summary["producers"]
    assert producer["last_sequence"] == 1
    assert producer["gaps"] == []
    ((_, op),) = Journal(outbox_dir).pending()
    assert op["producer_sequence"] == 1


# -- bounded finish (parity F3) ----------------------------------------------


def test_run_end_flush_timeout_defers_the_close(wired_async, outbox_dir, monkeypatch, capsys):
    run_id = start_run(wired_async)
    cli.main(["--async", "log", run_id, "loss=1.0", "--step", "1"])
    monkeypatch.setattr(  # every barrier pass parks transiently
        "probe.sdk.journal.drain",
        lambda j, run_ref=None, **k: DrainReport(
            remaining=1, stopped_transient=True, errors=["net down"]
        ),
    )
    rc = cli.main(["--spool-dir", str(outbox_dir), "run", "end", run_id, "--flush-timeout", "0.2"])
    assert rc == 0
    assert "end queued" in capsys.readouterr().err
    ops = [op for _, op in Journal(outbox_dir).pending()]
    assert [op["method"] for op in ops] == ["POST", "PATCH"], (
        "the deferred close must sit BEHIND the run's queued data"
    )
    accounting = ops[-1]["body"]["summary"]["probe_finish"]
    assert accounting["deferred"] is True and accounting["pending_at_exit"] == 1
    assert wired_async.runs[run_id]["status"] != "completed"
    assert "draining" in wired_async.runs[run_id]["tags"], "beacon marked intent"
    # The network comes back: everything lands, in order, and the tag clears.
    assert cli_drain(wired_async, outbox_dir).clean
    row = wired_async.runs[run_id]
    assert row["status"] == "completed"
    assert "draining" not in row["tags"]
    assert row["summary"]["probe_finish"]["deferred"] is True
    assert wired_async.metric_points_posted[run_id]


def test_run_end_flush_timeout_closes_normally_when_it_drains_in_time(
    wired_async, outbox_dir, monkeypatch, capsys
):
    run_id = start_run(wired_async)
    cli.main(["--async", "log", run_id, "loss=1.0", "--step", "1"])
    fake = make_client(wired_async)
    monkeypatch.setattr(  # a drain that can actually reach the fake app
        "probe.sdk.journal.drain",
        lambda j, run_ref=None, **k: drain(j, run_ref=run_ref, client_factory=lambda ctx: fake),
    )
    rc = cli.main(["--spool-dir", str(outbox_dir), "run", "end", run_id, "--flush-timeout", "5"])
    fake.close()
    assert rc == 0
    row = wired_async.runs[run_id]
    assert row["status"] == "completed"
    assert "probe_finish" not in (row.get("summary") or {}), (
        "an in-time bounded close is an ordinary close"
    )


def test_run_end_flush_timeout_still_refuses_dead_letters(wired_async, outbox_dir, capsys):
    run_id = start_run(wired_async)
    journal = Journal(outbox_dir)
    journal.append_http("POST", f"/v1/runs/{run_id}/badroute", {})
    assert not cli_drain(wired_async, outbox_dir).clean  # dead-letters it
    rc = cli.main(["--spool-dir", str(outbox_dir), "run", "end", run_id, "--flush-timeout", "0.2"])
    assert rc == 2
    assert "NOT closed" in capsys.readouterr().err


# -- review-pass additions (testing specialist) -------------------------------


def test_banner_surfaces_dead_letters_and_rekicks(wired_async, outbox_dir, capsys):
    journal = Journal(outbox_dir)
    journal.append_http("POST", "/v1/runs/poisoned/badroute", {})
    cli_drain(wired_async, outbox_dir)  # dead-letters it
    journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})
    kicks = len(wired_async.spawned)
    cli.main(["--spool-dir", str(outbox_dir), "project", "list"])
    err = capsys.readouterr().err
    assert "outbox:" in err and "dead-lettered" in err
    assert len(wired_async.spawned) > kicks, "pending + healthy must re-kick"


def test_async_span_add_queues_and_prints_id(wired_async, outbox_dir, capsys):
    run_id = start_run(wired_async)
    before = len(wired_async.requests)
    assert cli.main(["--async", "span", "add", run_id, "--type", "tool_call"]) == 0
    span_id = capsys.readouterr().out.strip().splitlines()[-1]
    assert len(wired_async.requests) == before
    ((_, op),) = Journal(outbox_dir).pending()
    assert op["run_ref"] == run_id and span_id in json.dumps(op["body"])
    assert cli_drain(wired_async, outbox_dir).clean


def test_async_big_file_defers_hash_and_ping(
    wired_async, outbox_dir, tmp_path, monkeypatch, capsys
):
    run_id = start_run(wired_async)
    monkeypatch.setattr("probe.sdk.journal.INLINE_HASH_MAX_BYTES", 8)
    source = tmp_path / "huge.bin"
    source.write_bytes(b"way more than eight bytes")
    before = len(wired_async.requests)
    assert cli.main(["--async", "artifact", "add", run_id, str(source)]) == 0
    assert "intent deferred to drain" in capsys.readouterr().out
    assert len(wired_async.requests) == before, "no ping for big files (11A)"
    ((_, op),) = Journal(outbox_dir).pending()
    assert op["upload"]["blob"] is None
    assert cli_drain(wired_async, outbox_dir).clean
    assert any(a["status"] == "complete" for a in wired_async.artifacts[run_id])


def test_run_end_passes_run_scope_and_ignores_other_runs(
    wired_async, outbox_dir, monkeypatch, capsys
):
    run_id = start_run(wired_async)
    journal = Journal(outbox_dir)
    journal.append_http("POST", "/v1/runs/other-run/badroute", {})
    cli_drain(wired_async, outbox_dir)  # dead-letters the OTHER run's op
    seen_scope: list = []

    def scoped_drain(j, run_ref=None, **kw):
        seen_scope.append(run_ref)
        return DrainReport()

    monkeypatch.setattr("probe.sdk.journal.drain", scoped_drain)
    rc = cli.main(["--spool-dir", str(outbox_dir), "run", "end", run_id])
    assert rc == 0, "another run's dead letter must not block this run's close"
    # First call is the T3-A barrier (run-scoped); Run.finish()'s own flush
    # then drains unscoped, which is fine — the verdict was already computed.
    assert seen_scope[0] == run_id, "barrier drain must be run-scoped (T3-A)"
    assert wired_async.runs[run_id]["status"] == "completed"


def test_outbox_watch_once_and_retry_unknown_and_failed_only_status(
    wired_async, outbox_dir, monkeypatch, capsys
):
    journal = Journal(outbox_dir)
    journal.append_http("POST", "/v1/runs/poisoned/badroute", {})
    cli_drain(wired_async, outbox_dir)
    capsys.readouterr()
    # failed-only queue (pending == 0) still exits 2
    assert cli.main(["--spool-dir", str(outbox_dir), "outbox", "status"]) == 2
    # retry with a bogus op id: exit 1, nothing requeued
    rc = cli.main(["--spool-dir", str(outbox_dir), "outbox", "retry", "nope"])
    assert rc == 1
    assert "requeued 0" in capsys.readouterr().out
    # watch --once drains once and returns
    monkeypatch.setattr("probe.sdk.journal.drain", lambda j, **kw: DrainReport(delivered=0))
    assert cli.main(["--spool-dir", str(outbox_dir), "outbox", "watch", "--once"]) == 0


def test_run_end_refuses_while_paused(wired_async, outbox_dir, capsys):
    """Codex: a paused journal skipped the drain but run end still closed the
    run -- the barrier is about the RESULT (nothing of this run still queued)."""
    run_id = start_run(wired_async)
    cli.main(["--async", "log", run_id, "loss=1.0", "--step", "1"])
    assert cli.main(["--spool-dir", str(outbox_dir), "outbox", "pause"]) == 0
    capsys.readouterr()
    rc = cli.main(["--spool-dir", str(outbox_dir), "run", "end", run_id])
    assert rc == 2
    assert "NOT closed" in capsys.readouterr().err
    assert wired_async.runs[run_id]["status"] != "completed"
    cli.main(["--spool-dir", str(outbox_dir), "outbox", "resume"])


# -- bulk import (`artifact add --from-manifest`) -----------------------------
#
# The whole verb is a cost argument: one process, one anchor resolution, N rows
# journalled. So these tests assert the COSTS, not only that rows land -- a
# manifest that enqueued everything correctly while still resolving per row
# would be the feature failing at the only thing it exists to do.


def manifest(tmp_path, *rows, name="manifest.jsonl"):
    path = tmp_path / name
    path.write_text("".join(json.dumps(row) + "\n" for row in rows))
    return str(path)


def seed_project(app, slug):
    cli.main(["project", "create", "--kind", "general", slug])
    return next(p["id"] for p in app.projects.values() if p["slug"] == slug)


def anchored(app, project_id):
    return app.artifacts.get(f"project:{project_id}", [])


def test_manifest_enqueues_every_row_in_one_process(wired_async, outbox_dir, tmp_path, capsys):
    project_id = seed_project(wired_async, "p")
    files = []
    for i in range(3):
        f = tmp_path / f"shard-{i}.bin"
        f.write_bytes(b"rows " * 64)
        files.append(f)
    path = manifest(
        tmp_path,
        {"path": str(files[0]), "notes": "first shard"},
        {"path": str(files[1]), "name": "renamed.bin"},
        {"path": str(files[2])},
    )
    capsys.readouterr()

    rc = cli.main(["artifact", "add", "--from-manifest", path, "--project", "p"])

    assert rc == 0
    summary = json.loads(capsys.readouterr().out)
    assert summary["rows"] == 3
    assert summary["enqueued"] == 3
    assert summary["failed"] == 0
    assert summary["failures"] == []
    assert len(Journal(outbox_dir).pending()) == 3
    assert wired_async.spawned, "a manifest must kick the drainer once it has queued"

    assert cli_drain(wired_async, outbox_dir).clean
    landed = {a["name"] for a in anchored(wired_async, project_id)}
    assert landed == {"shard-0.bin", "renamed.bin", "shard-2.bin"}


def test_manifest_reports_a_bad_row_and_still_enqueues_the_rest(
    wired_async, outbox_dir, tmp_path, capsys
):
    seed_project(wired_async, "p")
    good = tmp_path / "good.bin"
    good.write_bytes(b"ok")
    path = manifest(
        tmp_path,
        {"path": str(good)},
        {"notes": "no path at all"},
        {"path": str(tmp_path / "missing.bin")},
        {"path": str(good), "file": "typo'd key"},
        {"path": str(good), "name": "second.bin"},
    )
    capsys.readouterr()

    rc = cli.main(["artifact", "add", "--from-manifest", path, "--project", "p"])

    # Non-zero so an unattended caller notices -- but only AFTER the good rows
    # landed and the summary named the bad ones by line.
    assert rc == 1
    summary = json.loads(capsys.readouterr().out)
    assert summary["rows"] == 5
    assert summary["enqueued"] == 2
    assert summary["failed"] == 3
    assert [f["line"] for f in summary["failures"]] == [2, 3, 4]
    assert "needs" in summary["failures"][0]["error"]
    assert "not a regular file" in summary["failures"][1]["error"]
    assert "unknown key" in summary["failures"][2]["error"]
    assert len(Journal(outbox_dir).pending()) == 2


def test_manifest_resolves_each_anchor_once_not_once_per_row(
    wired_async, outbox_dir, tmp_path, capsys
):
    """The cost the verb exists to remove.

    200k rows under one project must not be 200k slug lookups. Counted against
    the fake's request log, so a regression that reintroduced per-row resolution
    shows up here as 6 instead of 2, rather than as a slow import nobody
    profiles."""
    seed_project(wired_async, "p")
    seed_project(wired_async, "second")
    src = tmp_path / "f.bin"
    src.write_bytes(b"bytes")
    rows = []
    for i in range(3):
        rows.append({"path": str(src), "name": f"a-{i}", "project": "p"})
        rows.append({"path": str(src), "name": f"b-{i}", "project": "second"})
    path = manifest(tmp_path, *rows)
    capsys.readouterr()

    before = len(wired_async.requests)
    assert cli.main(["artifact", "add", "--from-manifest", path]) == 0

    summary = json.loads(capsys.readouterr().out)
    assert summary["enqueued"] == 6
    assert summary["anchors_resolved"] == 2, "two distinct slugs, two cache entries"
    lookups = [
        r
        for r in wired_async.requests[before:]
        if r.url.path == "/v1/projects" and r.url.params.get("slug")
    ]
    assert len(lookups) == 2, f"6 rows over 2 projects must cost 2 lookups, got {len(lookups)}"


def test_manifest_bad_anchor_costs_one_lookup_and_fails_every_row_using_it(
    wired_async, outbox_dir, tmp_path, capsys
):
    src = tmp_path / "f.bin"
    src.write_bytes(b"bytes")
    path = manifest(
        tmp_path,
        *[{"path": str(src), "name": f"a-{i}", "project": "nope"} for i in range(4)],
    )
    capsys.readouterr()

    before = len(wired_async.requests)
    assert cli.main(["artifact", "add", "--from-manifest", path]) == 1

    summary = json.loads(capsys.readouterr().out)
    assert summary["enqueued"] == 0 and summary["failed"] == 4
    assert all("nope" in f["error"] for f in summary["failures"])
    lookups = [
        r
        for r in wired_async.requests[before:]
        if r.url.path == "/v1/projects" and r.url.params.get("slug") == "nope"
    ]
    assert len(lookups) == 1, (
        "a failing ref must be cached too -- otherwise the error path pays the "
        f"per-row cost the feature removes, got {len(lookups)}"
    )
    assert Journal(outbox_dir).pending() == []


def test_manifest_reference_rows_stage_zero_bytes(wired_async, outbox_dir, tmp_path, capsys):
    project_id = seed_project(wired_async, "p")
    small = tmp_path / "explicit.ckpt"
    small.write_bytes(b"x" * 64)
    big = tmp_path / "over-threshold.ckpt"
    big.write_bytes(b"y" * 4096)
    path = manifest(
        tmp_path,
        {"path": str(small), "reference": True, "notes": "named a reference"},
        # No `reference` key: the SIZE promotes it, which is the shape a
        # generated manifest of checkpoints has.
        {"path": str(big)},
    )
    capsys.readouterr()

    rc = cli.main(
        [
            "artifact",
            "add",
            "--from-manifest",
            path,
            "--project",
            "p",
            "--reference-over",
            "1024",
        ]
    )

    assert rc == 0
    summary = json.loads(capsys.readouterr().out)
    assert summary["references"] == 2 and summary["uploads"] == 0
    journal = Journal(outbox_dir)
    assert all(op["kind"] == "http" for _, op in journal.pending())
    assert not journal.blobs_dir.exists() or list(journal.blobs_dir.iterdir()) == [], (
        "a reference row records a path; it must never snapshot the bytes"
    )
    assert cli_drain(wired_async, outbox_dir).clean
    rows = anchored(wired_async, project_id)
    assert len(rows) == 2 and all(r["is_reference"] for r in rows)


def test_manifest_row_anchor_beats_the_command_line_default(
    wired_async, outbox_dir, tmp_path, capsys
):
    project_id = seed_project(wired_async, "p")
    run_id = start_run(wired_async)
    src = tmp_path / "f.bin"
    src.write_bytes(b"bytes")
    path = manifest(
        tmp_path,
        {"path": str(src), "name": "on-the-run", "run": run_id, "kind": "checkpoint"},
        {"path": str(src), "name": "on-the-project"},
    )
    capsys.readouterr()

    assert cli.main(["artifact", "add", "--from-manifest", path, "--project", "p"]) == 0
    assert json.loads(capsys.readouterr().out)["enqueued"] == 2
    assert cli_drain(wired_async, outbox_dir).clean

    # `.bin` from the row's path: a manifest row names an artifact the same way
    # `--name` does, so it goes through the same extension repair.
    assert [a["name"] for a in wired_async.artifacts[run_id]] == ["on-the-run.bin"]
    assert [a["name"] for a in anchored(wired_async, project_id)] == ["on-the-project.bin"]


def test_manifest_queues_without_the_async_flag(wired_async, outbox_dir, tmp_path, capsys):
    """--from-manifest is the bulk path, so it journals whether or not --async is
    set: the alternative is N synchronous uploads inside one process, which is
    the cost the verb exists to remove wearing a different hat."""
    seed_project(wired_async, "p")
    src = tmp_path / "f.bin"
    src.write_bytes(b"bytes")
    path = manifest(tmp_path, {"path": str(src)})
    capsys.readouterr()

    before = len(wired_async.requests)
    assert cli.main(["artifact", "add", "--from-manifest", path, "--project", "p"]) == 0

    assert len(Journal(outbox_dir).pending()) == 1
    posts = [r for r in wired_async.requests[before:] if r.method == "POST"]
    assert posts == [], "enqueue must not upload; the drainer delivers"


def test_manifest_rejects_per_row_flags_on_the_command_line(wired_async, tmp_path, capsys):
    path = manifest(tmp_path, {"path": str(tmp_path / "x")})
    assert cli.main(["artifact", "add", "--from-manifest", path, "--name", "x"]) != 0
    assert "per-ROW" in capsys.readouterr().err


def test_single_file_artifact_add_is_unchanged_by_the_manifest_path(
    wired_async, outbox_dir, tmp_path, capsys
):
    """REGRESSION guard for the refactor: `_artifact_add_async` was split so a
    manifest row could reuse its body, and the single-file path must behave
    identically -- same message, same intent ping, same staged blob."""
    run_id = start_run(wired_async)
    source = tmp_path / "model.bin"
    source.write_bytes(b"weights " * 512)

    assert cli.main(["--async", "artifact", "add", run_id, str(source)]) == 0

    out = capsys.readouterr().out
    assert "added upload" in out and "intent registered" in out and "(queued)" in out
    (pending_row,) = wired_async.artifacts[run_id]
    assert pending_row["status"] == "pending", "the capped intent ping still fires"
    ((_, op),) = Journal(outbox_dir).pending()
    assert op["upload"]["blob"] is not None


# -- async-by-default: the new guards ----------------------------------------


def test_require_staged_refuses_instead_of_queueing_an_unstaged_op(tmp_path, monkeypatch):
    """No headroom + require_staged: nothing is appended and op_id is None.

    An unstaged op records src_path and the drainer reads the LIVE file at
    delivery, so a queued-but-unstaged checkpoint uploads whatever the training
    loop rotated in by then. The caller uploads synchronously instead -- and can
    only do that safely because NOTHING was queued here. An op left behind would
    upload the file a second time, from a path whose bytes have since changed.
    """
    source = tmp_path / "ckpt.pt"
    source.write_bytes(b"weights")
    journal = Journal(tmp_path / "outbox")
    monkeypatch.setattr(Journal, "_staging_headroom", lambda self, path: "not enough room")

    result = journal.append_upload(
        anchor="run", anchor_id="r-1", name="ckpt", src_path=str(source), require_staged=True
    )

    assert result["op_id"] is None and result["staged"] is False
    assert result["unstaged_reason"] == "not enough room"
    assert journal.pending() == [], "a refused stage must leave NOTHING queued"


def test_without_require_staged_the_degrade_is_unchanged(tmp_path, monkeypatch):
    """Default False is byte-identical to before: it degrades and still queues."""
    source = tmp_path / "ckpt.pt"
    source.write_bytes(b"weights")
    journal = Journal(tmp_path / "outbox")
    monkeypatch.setattr(Journal, "_staging_headroom", lambda self, path: "not enough room")

    result = journal.append_upload(anchor="run", anchor_id="r-1", name="ckpt", src_path=str(source))

    assert result["op_id"] is not None and result["staged"] is False
    assert len(journal.pending()) == 1


def test_enqueue_upload_never_raises_when_the_outbox_is_unwritable(wired_async, tmp_path):
    """ENOSPC, a read-only XDG_STATE_HOME, flock ENOSYS on Lustre/FUSE.

    Async-by-default moves the per-write failure surface from the network to the
    disk. b820e9c8 guarded the http path for exactly this; the upload path was
    reached through journal.append_upload directly and never got that guard.
    """
    source = tmp_path / "safe.txt"
    source.write_text("synthetic benign artifact")
    client = make_client(wired_async, tmp_spool=tmp_path / "outbox", async_writes=True)
    try:

        def boom(*a, **kw):
            raise OSError(28, "No space left on device")

        object.__setattr__(client.journal, "append_upload", boom)
        assert client._enqueue_upload(anchor="run", anchor_id="r", name="n", src_path=str(source)) is None
    finally:
        client.close()


def test_enqueue_upload_lets_a_keyboard_interrupt_through(wired_async, tmp_path):
    """Staging is a full byte copy, so Ctrl-C lands here more than anywhere else.
    Catching BaseException would take away the user's ability to stop their own
    multi-GB upload."""
    source = tmp_path / "safe.txt"
    source.write_text("synthetic benign artifact")
    client = make_client(wired_async, tmp_spool=tmp_path / "outbox", async_writes=True)
    try:

        def interrupted(*a, **kw):
            raise KeyboardInterrupt

        object.__setattr__(client.journal, "append_upload", interrupted)
        with pytest.raises(KeyboardInterrupt):
            client._enqueue_upload(anchor="run", anchor_id="r", name="n", src_path=str(source))
    finally:
        client.close()


def test_enqueue_upload_scrubs_meta_before_it_reaches_the_journal(wired_async, tmp_path):
    """meta/notes used to land in the ops file verbatim and stay in failed/
    indefinitely. write() scrubs before journaling; this is the same rule for
    the path that does not go through write()."""
    source = tmp_path / "safe.txt"
    source.write_text("synthetic benign artifact")
    client = make_client(wired_async, tmp_spool=tmp_path / "outbox", async_writes=True)
    try:
        seen = {}
        object.__setattr__(
            client.journal, "append_upload", lambda **kw: seen.update(kw) or {"op_id": "x"}
        )
        object.__setattr__(client, "_redact", lambda body: {
            **{k: "[redacted]" for k in body}, "custom_redactor_applied": True,
        })

        client._enqueue_upload(
            anchor="run", anchor_id="r", name="n", src_path=str(source), meta={"token": "sk-live-1"}
        )

        # The mandatory final scrub canonicalizes custom sensitive-field markers.
        assert seen["meta"] == {"token": "<redacted>", "custom_redactor_applied": True}
    finally:
        client.close()


def test_a_project_anchor_does_not_take_the_async_default(wired_async, tmp_path, monkeypatch):
    """QUEUE ONLY WHERE A BARRIER EXISTS.

    `run end` drains by run_ref, so it gates run-anchored writes and nothing
    else. A project-anchored upload has no command in anyone's workflow that
    would force it out, so it stays synchronous and keeps failing loudly rather
    than queueing into a window nothing closes.

    Asserted on the RESOLVED WRITE MODE, not on an empty journal. An
    empty-journal assertion cannot tell "wrote synchronously" from "did not
    write at all", and worse, it passes even with the anchor guard deleted:
    every unflagged path in this file resolves to sync anyway, because the
    fixture injects a transport and the SDK refuses to queue onto one. Proven by
    mutation -- the guard was removed and this test stayed green. What the guard
    actually controls is the value handed to the client, so pin that.
    """
    cli_main = _cli_main()
    asked_for: list = []
    real = cli_main._queue_client_if_possible

    @contextlib.contextmanager
    def recording(explicit):
        asked_for.append(explicit)
        with real(explicit) as client:
            yield client

    monkeypatch.setattr(cli_main, "_queue_client_if_possible", recording)

    source = tmp_path / "dataset.csv"
    source.write_bytes(b"a,b\n1,2\n")
    assert cli.main(["project", "create", "--kind", "general", "p1"]) == 0
    assert cli.main(["artifact", "add", str(source), "--project", "p1"]) == 0

    assert asked_for == [False], (
        "a non-run anchor has no delivery barrier, so it must be resolved to "
        f"sync (False) before a client is built; got {asked_for}"
    )


def test_a_run_anchor_does_take_the_async_default(wired_async, tmp_path, monkeypatch):
    """The other side of the same guard: RUN is the anchor that DOES flip.

    Without this, the test above is satisfied by a guard that forces sync for
    every anchor -- which would silently undo the whole change.
    """
    cli_main = _cli_main()
    asked_for: list = []
    real = cli_main._queue_client_if_possible

    @contextlib.contextmanager
    def recording(explicit):
        asked_for.append(explicit)
        with real(explicit) as client:
            yield client

    monkeypatch.setattr(cli_main, "_queue_client_if_possible", recording)

    run_id = start_run(wired_async)
    source = tmp_path / "ckpt.bin"
    source.write_bytes(b"weights")
    assert cli.main(["artifact", "add", run_id, str(source)]) == 0

    assert asked_for == [None], (
        f"a run anchor must reach the SDK undecided (None) so the default applies; got {asked_for}"
    )


@pytest.mark.parametrize(
    "bad_ref",
    ["", "   ", "--step", "-r", "./runs/r1", "a b", "a\tb", "a\nb"],
)
def test_check_ref_shape_rejects_what_can_never_resolve(bad_ref):
    """The guard exists because a queued write exits 0: a typo stops being an
    instant failure and becomes a dead letter nobody watches. Buys back the
    obvious half for free -- no network, just shapes a run ref cannot have."""
    with pytest.raises(typer.BadParameter):
        _cli_main()._check_ref_shape(bad_ref)


@pytest.mark.parametrize(
    "good_ref",
    ["prophetic-manatee-987", "3c5f3695-0d4e-4a5f-9c11-1b2c3d4e5f60", "id:abc", "r1"],
)
def test_check_ref_shape_passes_anything_that_could_resolve(good_ref):
    """Deliberately NOT a petname or uuid validator. The grammar belongs to the
    server, and a client-side guess would start rejecting valid refs the day it
    widens -- a worse failure than the one the guard prevents."""
    _cli_main()._check_ref_shape(good_ref)


def test_staging_refused_falls_back_to_a_real_upload_and_queues_nothing(
    wired_async, outbox_dir, tmp_path, monkeypatch
):
    """END-TO-END for the require_staged safety argument.

    The pieces were pinned separately -- the journal returning op_id=None, the
    client returning None -- but not the thing that makes them safe: that the
    bytes then actually reach the server, exactly once, with nothing left queued
    behind them. An op left queued would upload the file a second time from a
    src_path whose bytes may have rotated, and the drainer would win.
    """
    run_id = start_run(wired_async)
    source = tmp_path / "ckpt.pt"
    source.write_bytes(b"weights " * 64)
    monkeypatch.setattr(Journal, "_staging_headroom", lambda self, path: "no room")

    rc = cli.main(["artifact", "add", run_id, str(source)])

    assert rc == 0
    assert Journal(outbox_dir).pending() == [], (
        "the fallback did the upload itself, so leaving an op queued would "
        "upload the same file twice"
    )


# -- what the cross-model review caught --------------------------------------


def test_secrets_in_meta_and_notes_never_reach_the_ops_file(
    wired_async, outbox_dir, tmp_path, capsys
):
    """END-TO-END through the real client, which is the point.

    The first version of this scrubbing was dead code: it was gated on
    `Client._redact`, which no CLI path ever sets, so nothing ran while the
    CHANGELOG claimed `--meta` and `--notes` were redacted. A unit test that
    constructed a client WITH a redactor passed happily and proved nothing. This
    drives the CLI the way a user does.

    `notes` is prose, so it needs the value-level pass: `default_scrub` redacts
    by KEY name and "notes" is not a sensitive key, which let a bare token
    through the earlier implementation.
    """
    run_id = start_run(wired_async)
    source = tmp_path / "model.bin"
    source.write_bytes(b"weights " * 64)

    rc = cli.main(
        [
            "--async",
            "artifact",
            "add",
            run_id,
            str(source),
            "--meta",
            "api_key=sk-live-SECRET123",
            "--notes",
            "exported with PROBE_TOKEN=probe_pat_SECRET456",
        ]
    )
    assert rc == 0

    on_disk = "".join(p.read_text() for p in (outbox_dir / "ops").iterdir() if p.is_file())
    assert "sk-live-SECRET123" not in on_disk, "a sensitive META key reached the journal"
    assert "probe_pat_SECRET456" not in on_disk, "a secret in PROSE notes reached the journal"


def test_a_dropped_write_exits_two_instead_of_claiming_it_queued(
    wired_async, outbox_dir, monkeypatch, capsys
):
    """The outbox fails OPEN, so the write returns normally and only warns.

    Printing "(queued)" there reports success for data that reached nothing --
    the one thing a queued write must never do. `Client.dropped_writes` carries
    the signal that `write()`'s None return throws away.
    """
    run_id = start_run(wired_async)

    def unwritable(*a, **kw):
        # Read-only, not full: a FULL disk now sends the write directly
        # instead (plan 1.5; `test_a_write_the_full_outbox_sent_directly_says_so`).
        raise OSError(30, "Read-only file system")

    monkeypatch.setattr(Journal, "append_http", unwritable)

    rc = cli.main(["--async", "log", run_id, "loss=0.5", "--step", "1"])

    assert rc == 2, "a write the outbox refused must not exit 0"
    # ONE readouterr(): it drains the buffer, so a second call returns empty.
    captured = capsys.readouterr()
    assert "(queued)" not in captured.out, "must not claim a queue it does not hold"
    assert "NOT queued" in captured.err


def test_a_write_the_full_outbox_sent_directly_says_so(wired_async, monkeypatch, capsys):
    """Plan 1.5: with the outbox's disk full the write goes straight to the
    server, and the CLI says it was sent rather than queued."""
    run_id = start_run(wired_async)

    def full(*a, **kw):
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(Journal, "append_http", full)
    rc = cli.main(["--async", "log", run_id, "loss=0.5", "--step", "1"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "(sent: outbox low on disk)" in out and "(queued)" not in out


def test_sync_is_refused_on_the_manifest_path_rather_than_ignored(wired_async, tmp_path, capsys):
    """--from-manifest always queues, so --sync cannot be honoured. Every other
    inapplicable flag on that branch is refused; silently accepting the one
    someone reaches for when they need the write to have LANDED would answer
    that request with its opposite."""
    manifest = tmp_path / "m.jsonl"
    manifest.write_text('{"path": "/tmp/x", "name": "n"}\n')

    rc = cli.main(["artifact", "add", "--from-manifest", str(manifest), "--sync"])

    assert rc != 0
    assert "always queues" in capsys.readouterr().err
