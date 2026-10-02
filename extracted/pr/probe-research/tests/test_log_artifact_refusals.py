"""`log_artifact` never raises into a training loop for a size or credential
refusal (plan 0.7).

Live before this: a 70 MB `log_artifact` raised `CredentialBlocked: Artifact
upload refused: file exceeds inspection size limit` out of the loop, and
`CredentialBlocked` was not a `RosError`, so a caller guarding its logging with
`except RosError` still died. Now, outside `strict=True`, the refusal warns once
per reason and records the reference row the synchronous path already writes
when an upload fails (pointer + size, `meta.upload = "failed"` and the reason in
`meta.upload_error`). `strict=True` still raises, now catchable as a RosError.
"""

from __future__ import annotations

import json
import os
import warnings

import pytest

from probe import errors as public_errors
from probe.sdk import errors
from probe.sdk import run as run_mod
from probe.sdk import secret_gate
from probe.sdk.secret_gate import CredentialBlocked, CredentialInPath
from tests.conftest import make_client, open_run

SEVENTY_MB = 70 * 1024 * 1024
# Assembled at import time so no literal here has a credential's shape.
PATH_TOKEN = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"


def _sparse(path, size=SEVENTY_MB):
    with open(path, "wb") as fh:
        fh.truncate(size)
    return path


def _rows(app, run_id, name):
    return [a for a in app.artifacts.get(run_id, []) if a.get("name") == name]


def _user_warnings(caught):
    return [str(w.message) for w in caught if issubclass(w.category, UserWarning)]


# --- the type -----------------------------------------------------------------


def test_credential_blocked_is_a_ros_error():
    exc = CredentialBlocked("Artifact upload refused: file exceeds inspection size limit")
    assert isinstance(exc, errors.RosError)
    assert isinstance(exc, public_errors.RosError)
    assert isinstance(CredentialInPath("x"), errors.RosError)
    assert exc.status is None, "RosError handlers read .status; a local refusal has none"
    # Callers that caught it by name keep catching it.
    with pytest.raises(CredentialBlocked):
        raise CredentialInPath("x")


# --- the loop keeps going -----------------------------------------------------


@pytest.mark.parametrize("async_writes", [False, True], ids=["sync", "async"])
def test_a_70mb_artifact_warns_and_records_a_reference(app, tmp_path, async_writes):
    client = make_client(app, tmp_spool=tmp_path / "spool", async_writes=async_writes)
    run = open_run(client, experiment="e", name="r")
    big = _sparse(tmp_path / "ckpt-4000.pt")

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        run.log_artifact("ckpt", path=str(big))
    run.log({"train/loss": 1.25}, step=1)  # the loop carries on
    client.flush()

    rows = _rows(app, run.id, "ckpt.pt")
    assert len(rows) == 1, "the refusal still leaves a record on the run"
    row = rows[0]
    assert row["is_reference"] is True
    assert row["size_bytes"] == SEVENTY_MB
    assert row["uri"].startswith("file://") and row["uri"].endswith("ckpt-4000.pt")
    meta = row["meta"]
    assert meta["upload"] == "failed", "check_run counts it as a capture gap"
    assert "exceeds inspection size limit" in meta["upload_error"]
    assert meta["local_path"] == os.path.abspath(big)
    assert app.puts == [], "no byte of it left the machine"

    messages = _user_warnings(caught)
    assert len([m for m in messages if "ckpt" in m]) == 1
    assert "exceeds inspection size limit" in messages[0]


def test_strict_true_still_raises_and_is_catchable_as_ros_error(client, app, tmp_path):
    run = open_run(client, experiment="e", name="r")
    big = _sparse(tmp_path / "ckpt.pt")
    with pytest.raises(CredentialBlocked, match="inspection size limit"):
        run.log_artifact("ckpt", path=str(big), strict=True)
    with pytest.raises(errors.RosError):
        run.log_artifact("ckpt", path=str(big), strict=True)
    assert _rows(app, run.id, "ckpt.pt") == [], "strict records nothing in its place"


def test_a_fail_closed_client_still_raises(app, tmp_path):
    client = make_client(app, fail_open=False, tmp_spool=tmp_path / "spool")
    run = open_run(client, experiment="e", name="r")
    with pytest.raises(CredentialBlocked):
        run.log_artifact("ckpt", path=str(_sparse(tmp_path / "ckpt.pt")))


def test_the_warning_is_said_once_per_reason_and_every_refusal_is_recorded(client, app, tmp_path):
    run = open_run(client, experiment="e", name="r")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        for step in range(3):
            run.log_artifact(f"ckpt-{step}", path=str(_sparse(tmp_path / f"ckpt-{step}.pt")))
    assert len(_user_warnings(caught)) == 1, "a checkpoint every N steps must not flood stderr"
    for step in range(3):
        (row,) = _rows(app, run.id, f"ckpt-{step}.pt")
        assert row["meta"]["upload"] == "failed"


def test_a_credential_in_the_path_is_never_recorded(client, app, tmp_path):
    folder = tmp_path / PATH_TOKEN
    folder.mkdir()
    src = folder / "notes.txt"
    src.write_text("ordinary\n")
    run = open_run(client, experiment="e", name="r")

    with pytest.warns(UserWarning, match="credential"):
        run.log_artifact("notes", path=str(src))

    (row,) = _rows(app, run.id, "notes.txt")
    assert row["meta"]["upload"] == "failed"
    assert "uri" not in row or row["uri"] is None
    sent = json.dumps([json.loads(r.content) for r in app.requests if r.content and r.method != "PUT"])
    assert PATH_TOKEN not in sent, "the pointer must not carry the credential it was refused for"


def test_a_file_that_changes_after_its_fingerprint_is_recorded_not_raised(
    client, app, tmp_path, monkeypatch
):
    """`@freeze_upload` refuses bytes that no longer match the fingerprint.
    That refusal fires in the decorator, OUTSIDE `_upload_file`'s fail-open
    handler, so it used to reach the loop even without any size problem."""
    src = tmp_path / "metrics.json"
    src.write_text('{"acc": 0.9}\n')
    real = run_mod._fingerprint
    monkeypatch.setattr(run_mod, "_fingerprint", lambda p: ("0" * 64, real(p)[1]))
    run = open_run(client, experiment="e", name="r")

    with pytest.warns(UserWarning, match="source changed"):
        run.log_artifact("metrics", path=str(src))

    (row,) = _rows(app, run.id, "metrics.json")
    assert row["is_reference"] is True
    assert "source changed since its fingerprint was taken" in row["meta"]["upload_error"]


def test_a_refusal_during_the_put_falls_back_with_its_reason(client, app, tmp_path, monkeypatch):
    """Inside `_upload_file` the transport's own gate can refuse (the source
    shrank mid-upload). `CredentialBlocked` was outside that handler's
    `except RosError`, so it escaped; now it is the same fail-open fallback."""
    src = tmp_path / "preds.jsonl"
    src.write_text('{"q": 1}\n')

    def refuse(*_a, **_k):
        secret_gate._refuse("source size changed before upload")

    monkeypatch.setattr(client.transport, "put_file", refuse)
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="recorded as a reference"):
        run.log_artifact("preds", path=str(src))
    # The presign's own pending row is there too (the upload reaper's), exactly
    # as for any failed PUT; the reference row is the record.
    (row,) = [r for r in _rows(app, run.id, "preds.jsonl") if r.get("is_reference")]
    assert row["meta"]["upload"] == "failed"
    assert "source size changed before upload" in row["meta"]["upload_error"]


def test_an_ordinary_upload_is_unchanged(client, app, tmp_path):
    src = tmp_path / "preds.jsonl"
    src.write_text('{"q": 1}\n')
    run = open_run(client, experiment="e", name="r")
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        row = run.log_artifact("preds", path=str(src))
    assert row["is_reference"] is False
    assert len(app.puts) == 1


# --- review fixes (#2007) -------------------------------------------------------
#
# Only what the GATE refuses about a real file is the loop's to survive. A
# mistake in the call raises, as it did before 0.7: the warn-once rule would
# otherwise make the second typo in a run completely silent.


def test_a_missing_path_raises_and_records_nothing(client, app, tmp_path):
    run = open_run(client, experiment="e", name="r")
    for attempt in range(2):  # the second typo is as loud as the first
        with pytest.raises(FileNotFoundError, match="no such file"):
            run.log_artifact("ckpt", path=str(tmp_path / f"typo-{attempt}.pt"))
    assert app.artifacts.get(run.id, []) == []


def test_a_missing_path_with_allow_missing_records_a_pointer(client, app, tmp_path):
    run = open_run(client, experiment="e", name="r")
    gone = tmp_path / "on-another-host.pt"
    with pytest.warns(UserWarning, match="no such file on this host"):
        run.log_artifact("ckpt", path=str(gone), allow_missing=True)
    (row,) = _rows(app, run.id, "ckpt.pt")
    assert row["is_reference"] is True and row["meta"]["upload"] == "failed"
    assert row["meta"]["local_path"] == os.path.abspath(gone)
    assert "size_bytes" not in row


def test_a_directory_raises(client, app, tmp_path):
    run = open_run(client, experiment="e", name="r")
    folder = tmp_path / "checkpoints"
    folder.mkdir()
    with pytest.raises(IsADirectoryError, match="directory"):
        run.log_artifact("checkpoints", path=str(folder))
    assert app.artifacts.get(run.id, []) == []


@pytest.mark.parametrize(
    "wrong", [{"content_hash": "0" * 64}, {"size_bytes": 999}], ids=["hash", "size"]
)
def test_a_wrong_caller_fingerprint_raises(client, app, tmp_path, wrong):
    src = tmp_path / "preds.jsonl"
    src.write_text('{"q": 1}\n')
    run = open_run(client, experiment="e", name="r")
    with pytest.raises(ValueError, match="do not match the file"):
        run.log_artifact("preds", path=str(src), **wrong)
    assert app.artifacts.get(run.id, []) == [] and app.puts == []


@pytest.mark.parametrize("case", [str.lower, str.upper], ids=["lower", "upper"])
def test_a_right_caller_fingerprint_still_uploads(client, app, tmp_path, case):
    """The control: the check refuses a WRONG fingerprint, not a supplied one.
    (Upper-case hex is the same digest; it used to read as "source changed".)"""
    import hashlib

    src = tmp_path / "preds.jsonl"
    src.write_text('{"q": 1}\n')
    digest = hashlib.sha256(src.read_bytes()).hexdigest()
    run = open_run(client, experiment="e", name="r")
    row = run.log_artifact(
        "preds", path=str(src), content_hash=case(digest), size_bytes=src.stat().st_size
    )
    assert row["is_reference"] is False and len(app.puts) == 1


def test_one_warning_per_reason_across_refusals_and_failed_uploads(client, app, tmp_path):
    """One warner for both paths: two failed uploads say it once, and a gate
    refusal -- a different reason -- still gets its own line."""
    run = open_run(client, experiment="e", name="r")
    src = tmp_path / "preds.jsonl"
    src.write_text('{"q": 1}\n')
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        for step in range(2):
            app.fail_next_uploads = True  # one-shot at the presign door
            run.log_artifact(f"preds-{step}", path=str(src))
        run.log_artifact("ckpt", path=str(_sparse(tmp_path / "ckpt.pt")))
    messages = _user_warnings(caught)
    assert len(messages) == 2, messages
    assert "the upload did not complete" in messages[0]
    assert "exceeds inspection size limit" in messages[1]
    for step in range(2):
        (row,) = [r for r in _rows(app, run.id, f"preds-{step}.jsonl") if r.get("is_reference")]
        assert row["meta"]["upload"] == "failed"


def test_the_withheld_path_placeholder_is_never_empty(client, app, tmp_path):
    """The server refuses a reference with neither a uri nor a
    meta.local_path, and a credential-shaped path gets no uri."""
    folder = tmp_path / PATH_TOKEN
    folder.mkdir()
    (folder / "notes.txt").write_text("ordinary\n")
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning):
        run.log_artifact("notes", path=str(folder / "notes.txt"))
    (row,) = _rows(app, run.id, "notes.txt")
    assert not row.get("uri")
    assert isinstance(row["meta"]["local_path"], str) and row["meta"]["local_path"].strip()


def _refuse_matching(monkeypatch, predicate, reason="file exceeds inspection size limit"):
    real = run_mod.check_upload

    def check(path, **kw):
        if predicate(os.path.basename(path)):
            secret_gate._refuse(reason)
        return real(path, **kw)

    monkeypatch.setattr(run_mod, "check_upload", check)


def test_a_refused_code_archive_warns_once_in_its_own_words(client, app, tmp_path, monkeypatch):
    """The snapshot, not `log_artifact`, reports the archive: once, with the
    gate's reason, and without telling the user to pass strict=True to a call
    they never made."""
    from tests.conftest import make_pushed_repo

    repo = make_pushed_repo(tmp_path)
    _refuse_matching(monkeypatch, lambda base: base.startswith("probe-code-"))
    run = open_run(client, experiment="e", name="r")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        snap = run.snapshot(cwd=str(repo), include_env=False, include_gpu=False)
    messages = _user_warnings(caught)
    assert len(messages) == 1, messages
    assert "code-bytes upload failed (refused by the credential gate: file exceeds" in messages[0]
    assert "strict=True" not in messages[0]
    assert snap["code_bytes"]["uploaded"] is False and snap["code_bytes"]["pending_upload"] == 3


def test_a_code_file_the_gate_refuses_is_not_called_storage_rejected(
    client, app, tmp_path, monkeypatch
):
    """Per-file capture: the local gate refusing a stream is not storage
    rejecting it, and three of them are not a storage outage."""
    from tests.conftest import make_pushed_repo

    monkeypatch.setenv(run_mod.CODE_STORAGE_ENV, run_mod.CODE_STORAGE_ARTIFACTS)
    repo = make_pushed_repo(tmp_path)

    def gate_refuses(*_a, **_k):
        secret_gate._refuse("file exceeds inspection size limit")

    monkeypatch.setattr(client.transport, "put_fileobj", gate_refuses)
    run = open_run(client, experiment="e", name="r")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        cb = run.snapshot(cwd=str(repo), include_env=False, include_gpu=False)["code_bytes"]
    reasons = {u["reason"] for u in cb["unstored"]}
    assert reasons == {"refused by the credential gate: file exceeds inspection size limit"}
    assert not any("storage" in m and "rejected" in m for m in _user_warnings(caught))

    with pytest.raises(errors.RosError, match="refused by the credential gate"):
        open_run(client, experiment="e", name="r2").snapshot(
            cwd=str(repo), include_env=False, include_gpu=False, strict=True
        )


def test_harbor_ledger_records_the_refusal_reason(app, tmp_path, monkeypatch):
    """harbor asks `log_artifact(sync=True)` for the row in hand. The refusal
    row used to be journaled under an async client, so the ledger said only
    "upload did not return a confirmed artifact"."""
    from probe.connectors.harbor import capture_trial, stage_trial

    client = make_client(app, tmp_spool=tmp_path / "spool", async_writes=True)
    run = open_run(client, experiment="e", name="r")
    source = tmp_path / "live"
    source.mkdir()
    (source / "only.txt").write_text("bytes")
    staged = stage_trial(source, tmp_path / "pvc" / "trial")
    _refuse_matching(monkeypatch, lambda base: base == "only.txt")

    with pytest.warns(UserWarning, match="exceeds inspection size limit"):
        capture_trial(run, staged, step_index=5, expand=False)
    (entry,) = staged.ledger.pending_artifacts()
    assert entry["state"] == "upload_failed"
    assert entry["error"] == "Artifact upload refused: file exceeds inspection size limit"


def test_the_servers_gate_copy_has_no_sdk_error_import():
    """The vendored copy's refusal base is a plain Exception, written by the
    sync script -- not a try/except that would bind `.errors` to whatever
    module of that name the destination package holds."""
    import importlib.util
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    server_copy = (root / "app" / "security" / "_credential_gate.py").read_text()
    assert "from .errors import" not in server_copy
    assert "\n_RefusalBase = Exception\n" in server_copy

    spec = importlib.util.spec_from_file_location(
        "sync_credential_scrubber", root / "scripts" / "sync_credential_scrubber.py"
    )
    script = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(script)
    source = (root / "agent" / "src" / "probe" / "sdk" / "secret_gate.py").read_text()
    assert "\n_RefusalBase = Exception\n" in script._vendor_refusal_base(source, Path("x"))
    # A source that no longer has the block stops the sync rather than
    # shipping the SDK import unrewritten.
    with pytest.raises(SystemExit, match="refusal base-class block"):
        script._vendor_refusal_base(source.replace("_RefusalBase", "_Base"), Path("x"))


# --- `probe artifact add` must not say "(delivered)" for a pointer -------------


@pytest.fixture
def cli_run(app, tmp_path, monkeypatch):
    from probe import cli

    monkeypatch.setattr(cli, "Client", lambda **_kw: make_client(app, tmp_spool=tmp_path / "spool"))
    assert cli.main(["project", "create", "--kind", "general", "p"]) == 0
    assert cli.main(["experiment", "create", "e", "--question", "h", "--project", "p"]) == 0
    return cli


def _start(cli, capsys) -> str:
    capsys.readouterr()
    assert cli.main(["run", "start", "--experiment", "e", "--name", "r1"]) == 0
    return capsys.readouterr().out.strip()


def test_cli_exits_1_when_the_gate_refused_the_file(cli_run, app, capsys, tmp_path):
    rid = _start(cli_run, capsys)
    big = _sparse(tmp_path / "ckpt.pt")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        rc = cli_run.main(["artifact", "add", rid, str(big), "--sync"])
    out, err = capsys.readouterr()
    assert rc == 1
    assert "(delivered)" not in out
    assert (
        "error: not uploaded (Artifact upload refused: file exceeds inspection size limit); "
        "a pointer was recorded" in err
    )
    (row,) = _rows(app, rid, "ckpt.pt")
    assert row["meta"]["upload"] == "failed", "the pointer is still recorded"


def test_cli_exits_1_when_the_upload_fell_back_to_a_pointer(cli_run, app, capsys, tmp_path):
    """The older false success: a failed PUT fell back to a reference and the
    CLI still printed (delivered)."""
    rid = _start(cli_run, capsys)
    src = tmp_path / "preds.jsonl"
    src.write_text('{"q": 1}\n')
    app.fail_next_uploads = True
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        rc = cli_run.main(["artifact", "add", rid, str(src), "--sync"])
    out, err = capsys.readouterr()
    assert rc == 1 and "(delivered)" not in out
    assert "error: not uploaded (" in err and "a pointer was recorded" in err


def test_cli_exits_1_for_a_missing_path_and_records_nothing(cli_run, app, capsys, tmp_path):
    rid = _start(cli_run, capsys)
    rc = cli_run.main(["artifact", "add", rid, str(tmp_path / "typo.pt"), "--sync"])
    out, err = capsys.readouterr()
    assert rc == 1 and "(delivered)" not in out
    assert "no such file" in err
    assert app.artifacts.get(rid, []) == []


def test_cli_delivered_is_still_exit_0(cli_run, app, capsys, tmp_path):
    rid = _start(cli_run, capsys)
    src = tmp_path / "preds.jsonl"
    src.write_text('{"q": 1}\n')
    rc = cli_run.main(["artifact", "add", rid, str(src), "--sync"])
    out, err = capsys.readouterr()
    assert rc == 0
    assert "(delivered)" in out and "error" not in err
    (row,) = _rows(app, rid, "preds.jsonl")
    assert row.get("is_reference") is False
