"""Per-file code capture on the client (0193): the default snapshot storage.

The files git cannot supply become one ``kind='code'`` artifact row each,
content-addressed, instead of one tarball per run. These pin the client half:
one PUT per file and none for bytes the server already holds, ``pending_upload``
that means "bytes not stored" file by file, fail-open on a server error, symlinks
carried by the manifest, the manifest URI for non-git trees, and a restore that
verifies every byte it fetched. Per-file storage is the default; the archive path
stays available under ``PROBE_CODE_STORAGE=archive``, and both halves of that
switch are pinned here.
"""

from __future__ import annotations

import os
import subprocess

import httpx
import pytest

import hashlib
import json
import warnings

from probe import cli
from probe.cli.main import _restore_captured_tree
from probe.sdk import errors
from probe.sdk import restore as _restore_mod
from probe.sdk import run as _run_mod
from probe.sdk import snapshot as _snapshot_mod
from tests.conftest import make_client, open_run


def _git(cwd, *args):
    proc = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    assert proc.returncode == 0, f"git {' '.join(args)}: {proc.stderr}"
    return proc.stdout.strip()


@pytest.fixture
def repo(tmp_path):
    """The pushed remote + clean/edited/untracked tree every snapshot suite uses."""
    from tests.conftest import make_pushed_repo

    return make_pushed_repo(tmp_path)


@pytest.fixture(autouse=True)
def _artifacts_storage(monkeypatch):
    monkeypatch.setenv(_run_mod.CODE_STORAGE_ENV, _run_mod.CODE_STORAGE_ARTIFACTS)


def _code_rows(app, run_id: str) -> list[dict]:
    return [a for a in app.artifacts.get(run_id, []) if a.get("kind") == "code"]


def _snapshot_meta(app, run_id: str) -> dict:
    return next(a["meta"] for a in app.artifacts.get(run_id, []) if a.get("kind") == "code_snapshot")


def _snap(run, cwd):
    return run.snapshot(cwd=str(cwd), include_env=False, include_gpu=False)


# --- upload ---------------------------------------------------------------------


def test_each_pending_file_becomes_a_code_row_and_the_count_clears(client, app, repo):
    client.fail_open = False
    run = open_run(client, experiment="e", name="r")
    snap = _snap(run, repo)

    cb = snap["code_bytes"]
    assert cb["storage"] == "artifacts" and cb["uploaded"] is True
    assert cb["pending_upload"] == 0
    assert (cb["n_uploaded"], cb["n_deduped"], cb["n_symlinks"]) == (3, 0, 0)

    rows = _code_rows(app, run.id)
    assert sorted(r["name"] for r in rows) == ["clean.py", "notes.txt", "train.py"]
    assert {r["status"] for r in rows} == {"complete"}
    assert all(r["meta"]["capture"] == "code-snapshot" for r in rows)
    assert not [a for rs in app.artifacts.values() for a in rs if a.get("kind") == "code_bytes"]

    meta = _snapshot_meta(app, run.id)
    assert meta["n_pending_upload"] == 0
    assert meta["storage"] == "artifacts"
    assert "train.py" in meta["paths_text"].split("\n")

    assert len(app.puts) == 3, "one PUT per file, none for the record"
    by_id = {r["id"]: r for r in rows}
    for aid, blob in app.blobs.items():
        assert blob == (repo / by_id[aid]["name"]).read_bytes(), "the bytes that landed are the file"


def test_a_second_run_over_the_same_tree_uploads_nothing(client, app, repo):
    first = open_run(client, experiment="e", name="r1")
    _snap(first, repo)
    app.puts.clear()

    second = open_run(client, experiment="e", name="r2")
    snap = _snap(second, repo)
    cb = snap["code_bytes"]
    assert (cb["n_deduped"], cb["n_uploaded"], cb["pending_upload"]) == (3, 0, 0)
    assert app.puts == [], "content the server holds is never re-sent"
    assert len(_code_rows(app, second.id)) == 3, "the second run still lists every file"
    assert {r["status"] for r in _code_rows(app, second.id)} == {"complete"}


def test_a_rejected_name_is_counted_and_named(client, app, repo):
    app.reject_capture_names = {"notes.txt"}
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="could not be stored"):
        snap = _snap(run, repo)
    cb = snap["code_bytes"]
    assert cb["pending_upload"] == 1
    assert cb["unstored"] == [{"path": "notes.txt", "reason": "name refused by the fake"}]
    assert _snapshot_meta(app, run.id)["n_pending_upload"] == 1
    assert sorted(r["name"] for r in _code_rows(app, run.id)) == ["clean.py", "train.py"]


def test_an_unconfirmed_window_is_retried_once_with_fresh_urls(client, app, repo):
    app.unconfirm_once = True
    run = open_run(client, experiment="e", name="r")
    snap = _snap(run, repo)
    assert snap["code_bytes"]["pending_upload"] == 0
    assert len(app.confirm_batches) == 2, "confirm, then one retry"
    assert len(app.puts) == 6, "the retry re-PUTs the unconfirmed files"
    assert len(app.capture_batches) == 2, "the retry re-presigns: a presigned PUT expires"
    assert [len(b["items"]) for b in app.capture_batches] == [3, 3]


def test_a_server_error_is_fail_open_and_leaves_the_count_honest(client, app, repo):
    app.fail_next_uploads = True
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="code capture stopped"):
        snap = _snap(run, repo)
    cb = snap["code_bytes"]
    assert cb["uploaded"] is False and cb["pending_upload"] == 3
    assert _snapshot_meta(app, run.id)["n_pending_upload"] == 3, "nothing reads this as captured"


def test_strict_raises_on_a_server_error(client, app, repo):
    client.fail_open = False
    app.fail_next_uploads = True
    run = open_run(client, experiment="e", name="r")
    with pytest.raises(errors.RosError):
        _snap(run, repo)


def test_symlinks_are_not_uploaded_and_restore_from_the_manifest(client, app, repo, tmp_path):
    (repo / "link.py").symlink_to("train.py")
    run = open_run(client, experiment="e", name="r")
    snap = _snap(run, repo)
    cb = snap["code_bytes"]
    assert cb["n_symlinks"] == 1 and cb["pending_upload"] == 0
    assert len(app.puts) == 3, "no object for a symlink; the manifest carries its target"

    dest = tmp_path / "out"
    result = _restore_captured_tree(client, run.id, snap["content_hash"], str(dest))
    assert result["n_unavailable"] == 0
    assert os.path.islink(dest / "link.py") and os.readlink(dest / "link.py") == "train.py"
    assert (dest / "train.py").read_bytes() == (repo / "train.py").read_bytes()


def test_a_non_git_tree_records_a_manifest_uri(client, app, tmp_path):
    src = tmp_path / "plain"
    src.mkdir()
    (src / "a.py").write_text("print('a')\n")
    run = open_run(client, experiment="e", name="r")
    snap = _snap(run, src)
    row = next(a for a in app.artifacts.get(run.id, []) if a.get("kind") == "code_snapshot")
    assert row["uri"] == f"probe-manifest:{snap['content_hash']}"


# --- restore ------------------------------------------------------------------


def test_restore_from_capture_rows_verifies_every_byte(client, app, repo, tmp_path):
    run = open_run(client, experiment="e", name="r")
    snap = _snap(run, repo)
    rows = _code_rows(app, run.id)
    victim = next(r for r in rows if r["name"] == "train.py")
    app.blobs[victim["id"]] = b"tampered"
    gone = next(r for r in rows if r["name"] == "notes.txt")
    app.artifacts[run.id].remove(gone)

    dest = tmp_path / "out"
    result = _restore_captured_tree(client, run.id, snap["content_hash"], str(dest))
    status = {f["path"]: f for f in result["files"]}
    assert status["clean.py"]["status"] == "restored"
    assert status["train.py"]["status"] == "unavailable"
    assert "sha256 mismatch" in status["train.py"]["reason"]
    assert status["notes.txt"]["status"] == "unavailable"
    assert status["notes.txt"]["reason"] == "no captured bytes for this file"
    assert not (dest / "train.py").exists(), "a mismatching file is never written"
    assert result["n_unavailable"] == 2


def test_restore_fetches_in_one_download_batch(client, app, repo, tmp_path):
    run = open_run(client, experiment="e", name="r")
    snap = _snap(run, repo)
    app.requests.clear()
    _restore_captured_tree(client, run.id, snap["content_hash"], str(tmp_path / "out"))
    batches = [r for r in app.requests if r.url.path == "/v1/artifacts/download/batch"]
    assert len(batches) == 1, "one presign call for the whole tree, not one per file"


# --- the switch ---------------------------------------------------------------


def test_per_file_storage_is_the_default(client, app, repo, monkeypatch):
    """No variable set: every file git cannot supply becomes a capture row and
    no `code-bytes` archive is written. This is what a fresh install does."""
    monkeypatch.delenv(_run_mod.CODE_STORAGE_ENV, raising=False)
    run = open_run(client, experiment="e", name="r")
    snap = _snap(run, repo)
    assert snap["code_bytes"]["storage"] == _run_mod.CODE_STORAGE_ARTIFACTS
    assert _snapshot_meta(app, run.id)["storage"] == _run_mod.CODE_STORAGE_ARTIFACTS
    assert not [a for a in app.artifacts.get(run.id, []) if a.get("kind") == "code_bytes"]
    assert {r["name"] for r in _code_rows(app, run.id)} == {"clean.py", "train.py", "notes.txt"}


def test_a_run_with_nothing_to_store_is_still_labelled_per_file(client, app, repo, monkeypatch):
    """Everything committed and pushed: no file needs storing, and the record
    still says which storage this run runs under -- not `archive` by default."""
    monkeypatch.delenv(_run_mod.CODE_STORAGE_ENV, raising=False)
    run = open_run(client, experiment="e", name="r")
    # Every file above the size threshold: nothing to store, references only.
    snap = run.snapshot(cwd=str(repo), include_env=False, include_gpu=False, reference_over_bytes=1)
    assert snap["code_bytes"]["reason"] == "nothing pending"
    assert _snapshot_meta(app, run.id)["storage"] == _run_mod.CODE_STORAGE_ARTIFACTS
    assert _code_rows(app, run.id) == []


def test_archive_storage_is_still_available(client, app, repo, monkeypatch):
    monkeypatch.setenv(_run_mod.CODE_STORAGE_ENV, _run_mod.CODE_STORAGE_ARCHIVE)
    run = open_run(client, experiment="e", name="r")
    _snap(run, repo)
    assert _snapshot_meta(app, run.id)["storage"] == _run_mod.CODE_STORAGE_ARCHIVE
    assert [a for a in app.artifacts.get(run.id, []) if a.get("kind") == "code_bytes"]
    assert _code_rows(app, run.id) == []


def test_a_server_without_the_batch_doors_falls_back_even_under_strict(client, app, repo):
    """A lagging self-hosted server is a downgrade, not a failure: the bytes
    still land (in the archive) and strict mode only makes FAILURES raise."""
    app.batch_doors = False
    client.fail_open = False
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="no per-file capture doors"):
        snap = run.snapshot(cwd=str(repo), include_env=False, include_gpu=False, strict=True)
    assert [a for a in app.artifacts.get(run.id, []) if a.get("kind") == "code_bytes"]
    assert _snapshot_meta(app, run.id)["storage"] == _run_mod.CODE_STORAGE_ARCHIVE
    assert snap["code_bytes"]["uploaded"] is True


def test_an_unknown_storage_value_warns_and_uses_the_default(monkeypatch):
    monkeypatch.setenv(_run_mod.CODE_STORAGE_ENV, "blobs")
    with pytest.warns(UserWarning, match="PROBE_CODE_STORAGE"):
        assert _run_mod._code_storage() == _run_mod.CODE_STORAGE_ARTIFACTS


def test_confirm_verdicts_are_not_retried(client, app, repo):
    """`unconfirmed` earns a second PUT + confirm; `failed` (reaped), `refused`
    (wrong door) and `unknown` (no row) are verdicts and land in `unstored`
    with their reason -- one confirm batch, no retry storm."""
    app.fail_capture_names = {"notes.txt"}
    run = open_run(client, experiment="e", name="r")
    snap = _snap(run, repo)
    cb = snap["code_bytes"]
    assert cb["pending_upload"] == 1
    assert cb["unstored"] == [
        {"path": "notes.txt", "reason": "reaped by storage before the upload landed"}
    ]
    assert len(app.confirm_batches) == 1, "a verdict is not retried"


# --- review cycle: hardening and verdicts ------------------------------------


def test_a_decomposed_filename_round_trips_through_the_nfc_server(client, app, repo, tmp_path):
    """The server canonicalises names to NFC; the client joins by position and
    keeps the manifest's spelling for the filesystem."""
    (repo / "cafe\u0301.txt").write_text("decomposed\n")
    run = open_run(client, experiment="e", name="r")
    snap = _snap(run, repo)
    cb = snap["code_bytes"]
    assert cb["pending_upload"] == 0 and cb["n_uploaded"] == 4
    names = {r["name"] for r in _code_rows(app, run.id)}
    assert "caf\u00e9.txt" in names and "cafe\u0301.txt" not in names
    result = _restore_captured_tree(client, run.id, snap["content_hash"], str(tmp_path / "out"))
    assert result["n_unavailable"] == 0
    assert (tmp_path / "out" / "cafe\u0301.txt").read_text() == "decomposed\n"


def test_a_server_without_the_batch_doors_gets_the_archive(client, app, repo):
    app.batch_doors = False
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="no per-file capture doors"):
        snap = _snap(run, repo)
    cb = snap["code_bytes"]
    assert cb["uploaded"] is True and cb["pending_upload"] == 0
    assert cb.get("storage", "archive") == "archive"
    assert any(a.get("kind") == "code_bytes" for a in app.artifacts[run.id])
    assert _code_rows(app, run.id) == []
    assert _snapshot_meta(app, run.id)["storage"] == "archive"


def test_a_file_swapped_for_a_symlink_after_the_manifest_is_never_sent(
    client, app, repo, tmp_path, monkeypatch
):
    secret = tmp_path / "id_rsa"
    secret.write_bytes(b"PRIVATE KEY MATERIAL")
    real = _snapshot_mod.pending_entries

    def swap(manifest):
        (repo / "train.py").unlink()
        (repo / "train.py").symlink_to(secret)
        return real(manifest)

    monkeypatch.setattr(_run_mod._snapshot, "pending_entries", swap)
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="could not be stored"):
        snap = _snap(run, repo)
    cb = snap["code_bytes"]
    assert all(b"PRIVATE" not in blob for blob in app.blobs.values()), "never PUT"
    assert cb["unstored"] == [{"path": "train.py", "reason": "changed since the manifest was taken"}]
    assert cb["pending_upload"] == 1 and cb["n_uploaded"] == 2


def test_a_presigned_signature_never_reaches_the_record_or_a_warning(client, app, repo):
    app.fail_put_names = {"notes.txt"}
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="could not be stored") as caught:
        snap = _snap(run, repo)
    cb = snap["code_bytes"]
    assert cb["unstored"][0]["path"] == "notes.txt"
    assert cb["unstored"][0]["reason"].startswith("upload failed")
    blob = json.dumps(cb) + "".join(str(w.message) for w in caught)
    assert "X-Amz-Signature" not in blob and "FAKESIG" not in blob


def test_a_window_whose_every_put_fails_is_an_outage_not_a_retry_storm(client, app, repo):
    app.fail_put_names = {"clean.py", "train.py", "notes.txt"}
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="code capture stopped after 0 of 3"):
        snap = _snap(run, repo)
    cb = snap["code_bytes"]
    assert cb["uploaded"] is False and cb["pending_upload"] == 3 and cb["reason"] == "upload failed"
    assert len(app.capture_batches) == 1, "no retry presign after an outage"
    assert {r["status"] for r in _code_rows(app, run.id)} == {"pending"}
    assert len(cb["unstored"]) == 3


def test_an_in_flight_window_names_what_happened_not_never_attempted(client, app, repo, monkeypatch):
    """A confirm that raises after the PUTs landed: the bytes are in the store,
    the rows are pending for the reaper, and the record says so per file --
    never "upload stopped before this file", which is for later windows."""
    monkeypatch.setattr(_run_mod, "CAPTURE_WINDOW", 2)
    real = client.confirm_capture_batch
    calls = []

    def boom(ids, **kw):
        calls.append(list(ids))
        raise errors.RosError("confirm exploded", status=500)

    monkeypatch.setattr(client, "confirm_capture_batch", boom)
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="code capture stopped after 0 of 3"):
        cb = _snap(run, repo)["code_bytes"]
    assert len(calls) == 1 and len(app.puts) == 2, "window one PUT, then confirm died"
    reasons = {u["path"]: u["reason"] for u in cb["unstored"]}
    assert sorted(reasons) == ["clean.py", "notes.txt", "train.py"]
    assert list(reasons.values()).count("uploaded, not confirmed by storage") == 2
    assert list(reasons.values()).count("upload stopped before this file") == 1
    monkeypatch.setattr(client, "confirm_capture_batch", real)


def test_the_capture_deadline_stops_the_walk_and_names_the_rest(client, app, repo, monkeypatch):
    """A tree of thousands of files on a flaky link must not park the run start
    for hours: past the deadline the remaining files are named and the run
    goes on."""
    monkeypatch.setattr(_run_mod, "CAPTURE_DEADLINE_SECONDS", 0.0)
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="capture deadline of 0s reached"):
        cb = _snap(run, repo)["code_bytes"]
    assert cb["pending_upload"] == 3 and cb["reason"] == "upload failed"
    assert {u["reason"] for u in cb["unstored"]} == {"upload stopped before this file"}
    assert app.capture_batches == [], "stopped before the first presign"


def test_the_deadline_env_override_is_read(monkeypatch):
    monkeypatch.setenv("PROBE_CODE_CAPTURE_DEADLINE", "42.5")
    assert _run_mod._capture_deadline() == 42.5
    monkeypatch.setenv("PROBE_CODE_CAPTURE_DEADLINE", "soon")
    assert _run_mod._capture_deadline() == _run_mod.CAPTURE_DEADLINE_SECONDS


def test_a_window_that_mostly_fails_is_an_outage(client, app, repo):
    """Half of a window of eight or more failing against storage on the first
    pass is the breaker, not a retry storm over a half-dead link. (Two flaky
    files in a three-file window are still retried -- see the path-order test.)"""
    extra = [f"f{i}.py" for i in range(8)]
    for name in extra:
        (repo / name).write_text(f"# {name}\n")
    app.fail_put_names = set(extra[:6])
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="storage unreachable"):
        cb = _snap(run, repo)["code_bytes"]
    # The five PUTs that landed were confirmed before the walk stopped.
    assert cb["reason"] == "upload failed" and cb["pending_upload"] == 6
    assert len(app.capture_batches) == 1, "no retry presign after an outage"


def test_a_window_storage_rejects_outright_is_an_outage(client, app, repo):
    """A proxy that strips the checksum header makes storage answer 4xx for
    every file: one verdict for the window, not 4,600 rejected PUTs."""
    app.reject_put_names = {"clean.py", "train.py", "notes.txt"}
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="storage rejected every upload in this window"):
        cb = _snap(run, repo)["code_bytes"]
    assert cb["reason"] == "upload failed" and cb["pending_upload"] == 3
    assert len(app.capture_batches) == 1


def test_one_rejected_file_among_stored_ones_is_not_an_outage(client, app, repo):
    app.reject_put_names = {"notes.txt"}
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="could not be stored"):
        cb = _snap(run, repo)["code_bytes"]
    assert cb["pending_upload"] == 1
    assert cb["unstored"][0]["path"] == "notes.txt"
    assert cb["unstored"][0]["reason"].startswith("upload rejected")


def test_strict_raises_when_storage_did_not_take_a_file(client, app, repo):
    """`strict=True` means "raise if my code was not saved": a refused name is
    storage saying no, so the snapshot raises instead of warning."""
    app.reject_capture_names = {"notes.txt"}
    run = open_run(client, experiment="e", name="r")
    with pytest.raises(errors.RosError, match="1 of 3 captured files could not be stored"):
        run.snapshot(cwd=str(repo), include_env=False, include_gpu=False, strict=True)


def test_strict_raises_on_a_put_that_kept_failing(client, app, repo):
    app.fail_put_names = {"notes.txt"}
    run = open_run(client, experiment="e", name="r")
    with pytest.raises(errors.RosError, match="notes.txt: upload failed"):
        run.snapshot(cwd=str(repo), include_env=False, include_gpu=False, strict=True)


def test_strict_only_warns_when_the_tree_moved(client, app, repo, monkeypatch):
    """A file edited between the manifest and the upload is the researcher's
    tree moving, not storage failing: named, warned, never raised."""
    real = client.presign_capture_batch

    def edit_then_presign(run_id, items, **kw):
        (repo / "notes.txt").write_text("edited after the manifest\n")
        return real(run_id, items, **kw)

    monkeypatch.setattr(client, "presign_capture_batch", edit_then_presign)
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="notes.txt: changed since the manifest was taken"):
        snap = run.snapshot(cwd=str(repo), include_env=False, include_gpu=False, strict=True)
    assert snap["code_bytes"]["pending_upload"] == 1


def test_a_half_failed_window_still_confirms_what_landed(client, app, repo):
    """The breaker fires AFTER the confirm: the PUTs that got through are
    banked as stored, not left pending for the reaper."""
    extra = [f"f{i}.py" for i in range(8)]
    for name in extra:
        (repo / name).write_text(f"# {name}\n")
    app.fail_put_names = set(extra[:6])
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="storage unreachable"):
        cb = _snap(run, repo)["code_bytes"]
    assert cb["pending_upload"] == 6
    stored = {r["name"] for r in _code_rows(app, run.id) if r["status"] == "complete"}
    assert stored == {"clean.py", "train.py", "notes.txt", "f6.py", "f7.py"}


def test_a_throttled_put_is_retried_not_recorded(client, app, repo):
    app.throttle_put_once = True
    run = open_run(client, experiment="e", name="r")
    cb = _snap(run, repo)["code_bytes"]
    assert cb["pending_upload"] == 0 and cb["n_files"] == 3


def test_manifest_paths_are_posix_even_on_a_backslash_box(monkeypatch):
    monkeypatch.setattr(_snapshot_mod.os, "sep", "\\")
    assert _snapshot_mod._posix("a\\b.py") == "a/b.py"
    monkeypatch.setattr(_snapshot_mod.os, "sep", "/")
    assert _snapshot_mod._posix("a\\b.py") == "a\\b.py"
    assert _snapshot_mod.wire_name("cafe\u0301.txt") == "caf\u00e9.txt"


def test_the_upload_cap_holds_under_per_file_storage(client, app, repo):
    run = open_run(client, experiment="e", name="r")
    with pytest.raises(_snapshot_mod.SnapshotTooLarge):
        run.snapshot(cwd=str(repo), include_env=False, include_gpu=False, max_upload_bytes=1)
    assert app.capture_batches == [], "refused before the first presign"


def test_a_missing_verdict_is_an_unstored_file_not_a_stored_one(client, app, repo, monkeypatch):
    real = client.presign_capture_batch

    def drop_last(run_id, items, **kw):
        out = real(run_id, items, **kw)
        out["items"] = out["items"][:-1]
        return out

    monkeypatch.setattr(client, "presign_capture_batch", drop_last)
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="could not be stored"):
        cb = _snap(run, repo)["code_bytes"]
    assert cb["pending_upload"] == 1
    assert cb["unstored"][0]["reason"] == "no verdict from storage"


def test_a_confirm_that_names_nothing_leaves_the_file_unstored(client, app, repo, monkeypatch):
    monkeypatch.setattr(
        client,
        "confirm_capture_batch",
        lambda ids: {"confirmed": [], "unconfirmed": [], "refused": [], "unknown": [], "failed": []},
    )
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="could not be stored"):
        cb = _snap(run, repo)["code_bytes"]
    assert cb["pending_upload"] == 3
    assert {u["reason"] for u in cb["unstored"]} == {"no verdict from storage"}
    assert len(app.capture_batches) == 2, "one retry, with fresh URLs, before giving up"


def test_a_tree_larger_than_one_window_is_captured_in_windows(client, app, repo, monkeypatch):
    monkeypatch.setattr(_run_mod, "CAPTURE_WINDOW", 2)
    run = open_run(client, experiment="e", name="r")
    cb = _snap(run, repo)["code_bytes"]
    assert [len(b["items"]) for b in app.capture_batches] == [2, 1]
    assert len({b["captured_at"] for b in app.capture_batches}) == 1
    assert cb["n_uploaded"] == 3 and cb["pending_upload"] == 0


def test_a_server_error_after_the_first_window_keeps_what_landed(client, app, repo, monkeypatch):
    monkeypatch.setattr(_run_mod, "CAPTURE_WINDOW", 2)
    real = client.presign_capture_batch
    calls = []

    def flaky(run_id, items, **kw):
        calls.append(items)
        if len(calls) == 2:
            app.fail_next_uploads = True
        return real(run_id, items, **kw)

    monkeypatch.setattr(client, "presign_capture_batch", flaky)
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="code capture stopped after 2 of 3"):
        cb = _snap(run, repo)["code_bytes"]
    assert (cb["uploaded"], cb["n_uploaded"], cb["pending_upload"]) == (True, 2, 1)
    assert cb["unstored"] == [{"path": "train.py", "reason": "upload stopped before this file"}]
    assert {r["status"] for r in _code_rows(app, run.id)} == {"complete"}


@pytest.mark.parametrize(
    "bucket,reason",
    [
        ("refused", "already an artifact of this run, not captured"),
        ("unknown", "no live artifact row for this file"),
    ],
)
def test_refused_and_unknown_verdicts_are_named_not_retried(
    client, app, repo, monkeypatch, bucket, reason
):
    real = client.confirm_capture_batch

    def verdict(ids):
        out = real(ids)
        victim = next(a["id"] for a in _code_rows(app, run.id) if a["name"] == "notes.txt")
        out["confirmed"] = [i for i in out["confirmed"] if i != victim]
        out[bucket] = [victim]
        return out

    monkeypatch.setattr(client, "confirm_capture_batch", verdict)
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="could not be stored"):
        cb = _snap(run, repo)["code_bytes"]
    assert cb["unstored"] == [{"path": "notes.txt", "reason": reason}]
    assert len(app.confirm_batches) == 1 and len(app.puts) == 3


def test_capture_warnings_cannot_kill_a_run_under_warnings_as_errors(client, app, repo):
    app.reject_capture_names = {"notes.txt"}
    run = open_run(client, experiment="e", name="r")
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        snap = _snap(run, repo)
    assert snap["code_bytes"]["pending_upload"] == 1
    assert _snapshot_meta(app, run.id)["n_pending_upload"] == 1


def test_the_storage_flag_is_case_and_whitespace_insensitive(monkeypatch):
    monkeypatch.setenv(_run_mod.CODE_STORAGE_ENV, " Artifacts ")
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert _run_mod._code_storage() == _run_mod.CODE_STORAGE_ARTIFACTS


def test_tree_limit_reaches_the_wire_at_the_root(client, app, repo):
    run = open_run(client, experiment="e", name="r")
    _snap(run, repo)
    level = client.list_run_artifact_tree(run.id, limit=1)
    assert level["truncated"] is True and len(level["files"]) == 1
    req = [r for r in app.requests if r.url.path.endswith("/artifacts/tree")][-1]
    assert req.url.params.get("limit") == "1"


def test_restore_falls_back_to_the_code_bytes_archive_without_capture_rows(
    client, app, repo, tmp_path, monkeypatch
):
    monkeypatch.setenv(_run_mod.CODE_STORAGE_ENV, _run_mod.CODE_STORAGE_ARCHIVE)
    run = open_run(client, experiment="e", name="r")
    snap = _snap(run, repo)
    assert _code_rows(app, run.id) == []
    result = _restore_captured_tree(client, run.id, snap["content_hash"], str(tmp_path / "out"))
    assert result["n_unavailable"] == 0
    assert (tmp_path / "out" / "train.py").read_bytes() == (repo / "train.py").read_bytes()


def test_a_failed_download_is_reported_per_file_with_its_reason(
    client, app, repo, tmp_path, monkeypatch, capsys
):
    run = open_run(client, experiment="e", name="r")
    snap = _snap(run, repo)
    victim = next(r["id"] for r in _code_rows(app, run.id) if r["name"] == "train.py")
    real = client.transport.get_url

    def failing(url):
        if victim in url:
            raise errors.TransportError("GET r2.test: boom")
        return real(url)

    monkeypatch.setattr(client.transport, "get_url", failing)
    result = _restore_captured_tree(client, run.id, snap["content_hash"], str(tmp_path / "out"))
    status = {f["path"]: f for f in result["files"]}
    assert status["train.py"]["reason"] == "download failed"
    assert status["clean.py"]["status"] == "restored"
    assert "could not download train.py" in capsys.readouterr().err


def test_a_pending_row_at_restore_carries_the_servers_reason(client, app, repo, tmp_path):
    run = open_run(client, experiment="e", name="r")
    snap = _snap(run, repo)
    row = next(r for r in _code_rows(app, run.id) if r["name"] == "notes.txt")
    row["status"] = "pending"
    result = _restore_captured_tree(client, run.id, snap["content_hash"], str(tmp_path / "out"))
    status = {f["path"]: f for f in result["files"]}
    # A pending row is not a capture row restore can use: absent, and said so.
    assert status["notes.txt"]["status"] == "unavailable"
    assert status["notes.txt"]["reason"] == "no captured bytes for this file"
    assert status["train.py"]["status"] == "restored"


def test_a_download_batch_the_server_refuses_reads_as_unavailable_not_a_traceback(
    client, app, repo, tmp_path, monkeypatch
):
    run = open_run(client, experiment="e", name="r")
    snap = _snap(run, repo)

    def locked(ids):
        raise errors.RosError("run is retention-locked", status=402)

    monkeypatch.setattr(client, "presign_download_batch", locked)
    result = _restore_captured_tree(client, run.id, snap["content_hash"], str(tmp_path / "out"))
    assert result["n_unavailable"] == 3
    assert all(f["reason"].startswith("download refused: run is retention-locked") for f in result["files"] if f["status"] == "unavailable")


def test_verify_only_over_capture_rows_writes_nothing(client, app, repo, tmp_path):
    run = open_run(client, experiment="e", name="r")
    snap = _snap(run, repo)
    dest = tmp_path / "never"
    result = _restore_captured_tree(client, run.id, snap["content_hash"], str(dest), verify_only=True)
    assert result["n_unavailable"] == 0 and result["tree_matches"] is True
    assert not dest.exists()


def test_a_deduped_run_restores_from_shared_bytes(client, app, repo, tmp_path):
    first = open_run(client, experiment="e", name="r1")
    _snap(first, repo)
    second = open_run(client, experiment="e", name="r2")
    snap = _snap(second, repo)
    assert snap["code_bytes"]["n_deduped"] == 3
    result = _restore_captured_tree(client, second.id, snap["content_hash"], str(tmp_path / "out"))
    assert result["n_unavailable"] == 0
    assert (tmp_path / "out" / "notes.txt").read_bytes() == (repo / "notes.txt").read_bytes()


def test_a_run_with_both_an_archive_and_capture_rows_restores_from_both(
    client, app, repo, tmp_path, monkeypatch
):
    run = open_run(client, experiment="e", name="r")
    monkeypatch.setenv(_run_mod.CODE_STORAGE_ENV, _run_mod.CODE_STORAGE_ARCHIVE)
    first = _snap(run, repo)  # archive holds v2 train.py
    (repo / "train.py").write_text("print('v3')\n")
    monkeypatch.setenv(_run_mod.CODE_STORAGE_ENV, _run_mod.CODE_STORAGE_ARTIFACTS)
    _snap(run, repo)  # rows hold v3 train.py + the others
    result = _restore_captured_tree(client, run.id, first["content_hash"], str(tmp_path / "out"))
    status = {f["path"]: f for f in result["files"]}
    assert status["train.py"]["status"] == "restored", "the archive-only version is still reachable"
    assert (tmp_path / "out" / "train.py").read_text() == "print('v2 EDITED, uncommitted')\n"


def test_restore_fetches_lazily_in_batches(client, app, repo, tmp_path, monkeypatch):
    monkeypatch.setattr(_restore_mod, "CAPTURE_FETCH_BATCH", 2)
    run = open_run(client, experiment="e", name="r")
    snap = _snap(run, repo)
    calls = []
    real = client.presign_download_batch
    monkeypatch.setattr(client, "presign_download_batch", lambda ids: (calls.append(list(ids)), real(ids))[1])
    result = _restore_captured_tree(client, run.id, snap["content_hash"], str(tmp_path / "out"))
    assert result["n_unavailable"] == 0
    assert [len(c) for c in calls] == [2, 1], "one presign per lazy batch, not one for the tree"


def test_one_changed_file_costs_exactly_one_put(client, app, repo):
    first = open_run(client, experiment="e", name="r1")
    _snap(first, repo)
    (repo / "train.py").write_text("print('v3')\n")
    app.puts.clear()
    second = open_run(client, experiment="e", name="r2")
    cb = _snap(second, repo)["code_bytes"]
    assert (cb["n_uploaded"], cb["n_deduped"]) == (1, 2)
    assert len(app.puts) == 1


def test_the_executable_bit_survives_the_capture_path(client, app, repo, tmp_path):
    (repo / "train.py").chmod(0o755)
    run = open_run(client, experiment="e", name="r")
    snap = _snap(run, repo)
    row = next(r for r in _code_rows(app, run.id) if r["name"] == "train.py")
    assert row["meta"]["mode"] == "100755"
    _restore_captured_tree(client, run.id, snap["content_hash"], str(tmp_path / "out"))
    assert os.access(tmp_path / "out" / "train.py", os.X_OK)


def test_strict_true_raises_on_a_server_error(client, app, repo):
    app.fail_next_uploads = True
    run = open_run(client, experiment="e", name="r")
    with pytest.raises(errors.RosError):
        run.snapshot(cwd=str(repo), include_env=False, include_gpu=False, strict=True)


def test_only_symlinks_pending_sends_no_batch_and_says_why(client, app, tmp_path):
    src = tmp_path / "links"
    src.mkdir()
    (src / "target.bin").write_bytes(b"x" * 4096)
    (src / "link").symlink_to("target.bin")
    run = open_run(client, experiment="e", name="r")
    snap = run.snapshot(
        cwd=str(src), include_env=False, include_gpu=False, reference_over_bytes=1024
    )
    cb = snap["code_bytes"]
    assert (cb["uploaded"], cb["pending_upload"], cb["n_symlinks"]) == (False, 0, 1)
    assert cb["reason"] == "nothing to upload"
    assert app.capture_batches == []


def test_two_put_failures_are_both_named_in_path_order(client, app, repo):
    app.fail_put_names = {"train.py", "notes.txt"}
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="2 of 3"):
        cb = _snap(run, repo)["code_bytes"]
    assert [u["path"] for u in cb["unstored"]] == ["notes.txt", "train.py"]
    assert cb["n_uploaded"] == 1


def test_paths_text_is_bounded(client, app, repo, monkeypatch):
    monkeypatch.setattr(_run_mod, "PATHS_TEXT_MAX_BYTES", 12)
    run = open_run(client, experiment="e", name="r")
    _snap(run, repo)
    meta = _snapshot_meta(app, run.id)
    assert meta["paths_text_truncated"] is True
    assert len(meta["paths_text"].encode()) <= 12
    # The cut lands on a line boundary: /v1/search matches on this text, and a
    # partial path would match a file that was never captured. Sorted, the
    # three paths are clean.py / notes.txt / train.py; 12 bytes fit one.
    assert meta["paths_text"] == "clean.py"


def test_a_fetch_that_cannot_ask_names_every_file_with_the_batch_reason(tmp_path):
    """A blob_fetch that raises BEFORE fetching (the store said no to the whole
    batch) leaves every captured file unavailable with that reason -- not the
    generic "no captured bytes", which is what a falsy reasons mapping gave."""
    from probe.sdk.restore import restore_snapshot

    payload = b"x\n"
    entry = {
        "path": "a.txt",
        "mode": "100644",
        "size": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "source": "blob",
    }

    def refuse(entries):
        raise errors.RosError("run is retention-locked", status=402)

    result = restore_snapshot(
        {"entries": [entry, {**entry, "path": "b.txt"}]}, str(tmp_path / "out"), blob_fetch=refuse
    )
    assert result["n_unavailable"] == 2
    assert {f["reason"] for f in result["files"]} == {"download refused: run is retention-locked"}


def test_a_failed_get_keeps_its_reason_when_the_archive_lacks_the_file_too(
    client, app, repo, tmp_path, monkeypatch
):
    """Union restore: a row-only file whose GET failed reports the fetch reason,
    not "not present in the code-bytes archive" (true, but not why)."""
    run = open_run(client, experiment="e", name="r")
    monkeypatch.setenv(_run_mod.CODE_STORAGE_ENV, _run_mod.CODE_STORAGE_ARCHIVE)
    _snap(run, repo)  # the archive: clean/train/notes
    (repo / "extra.txt").write_text("rows only\n")
    monkeypatch.setenv(_run_mod.CODE_STORAGE_ENV, _run_mod.CODE_STORAGE_ARTIFACTS)
    second = _snap(run, repo)  # rows: all four
    real = client.transport.get_url
    victim = next(r for r in _code_rows(app, run.id) if r["name"] == "extra.txt")

    def failing(url):
        if victim["id"] in url:
            raise errors.TransportError("boom")
        return real(url)

    monkeypatch.setattr(client.transport, "get_url", failing)
    # Restore the SECOND manifest (it lists extra.txt) through both storages.
    result = _restore_captured_tree(client, run.id, second["content_hash"], str(tmp_path / "out"))
    status = {f["path"]: f for f in result["files"]}
    assert status["extra.txt"]["status"] == "unavailable"
    assert status["extra.txt"]["reason"] == "download failed"
    assert status["clean.py"]["status"] == "restored"


def test_put_fileobj_sends_exactly_the_verified_size(app):
    """A file that grows between the hash and the stream must not send the
    growth: Content-Length and the body are both the verified size."""
    import io

    import httpx

    from probe.config import Settings
    from probe.sdk.transport import Transport

    seen: dict = {}

    def handler(request):
        seen["length"] = request.headers.get("content-length")
        seen["body"] = request.read()
        return httpx.Response(200)

    settings = Settings(
        base_url="http://test",
        token="ros_pat_deadbeef",
        ingest_token="ros_ing_cafef00d",
        hmac_secret="s3cr3t",
    )
    transport = Transport(
        settings,
        client=httpx.Client(base_url="http://test", transport=httpx.MockTransport(handler)),
    )
    fh = io.BytesIO(b"0123456789" + b"GROWN")
    transport.put_fileobj("http://r2.test/put/x?X-Amz-Signature=FAKESIG", fh, size=10, chunk_size=4)
    assert seen == {"length": "10", "body": b"0123456789"}


def test_nfc_and_nfd_spellings_of_one_file_are_both_stored_and_restored(
    client, app, repo, tmp_path
):
    """Linux allows `caf\u00e9.txt` and `cafe\u0301.txt` side by side. The server
    keeps one NFC name per bytes, so the pair shares one row: uploaded once,
    both spellings reported stored, both restored."""
    nfc, nfd = "caf\u00e9.txt", "cafe\u0301.txt"
    (repo / nfc).write_bytes(b"same bytes\n")
    (repo / nfd).write_bytes(b"same bytes\n")
    assert sorted(p.name for p in repo.iterdir() if p.name.startswith("caf")) == sorted([nfc, nfd])
    run = open_run(client, experiment="e", name="r")
    snap = _snap(run, repo)
    cb = snap["code_bytes"]
    assert cb["pending_upload"] == 0, cb.get("unstored")
    assert [r["name"] for r in _code_rows(app, run.id) if r["name"] == nfc] and not [
        r for r in _code_rows(app, run.id) if r["name"] == nfd
    ]
    result = _restore_captured_tree(client, run.id, snap["content_hash"], str(tmp_path / "out"))
    status = {f["path"]: f["status"] for f in result["files"]}
    assert status[nfc] == "restored" and status[nfd] == "restored"
    assert (tmp_path / "out" / nfc).read_bytes() == (tmp_path / "out" / nfd).read_bytes() == b"same bytes\n"


def test_blob_fetch_restore_refuses_a_path_outside_dest(tmp_path):
    from probe.sdk.restore import restore_snapshot

    payload = b"pwned\n"
    manifest = {
        "entries": [
            {
                "path": "../escape.txt",
                "mode": "100644",
                "size": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "source": "blob",
            }
        ]
    }
    dest = tmp_path / "dest"
    result = restore_snapshot(
        manifest, str(dest), blob_fetch=lambda entries: {e["path"]: payload for e in entries}
    )
    assert result["files"][0]["status"] == "unavailable"
    assert not (tmp_path / "escape.txt").exists()


# --- the default (nothing exported) --------------------------------------------------


def test_an_empty_storage_export_is_the_default_without_a_warning(monkeypatch):
    """`export PROBE_CODE_STORAGE=` (and a whitespace-only value) reads as unset,
    not as a misconfiguration: per-file storage, and no warning on every run."""
    for value in ("", "   "):
        monkeypatch.setenv(_run_mod.CODE_STORAGE_ENV, value)
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            assert _run_mod._code_storage() == _run_mod.CODE_STORAGE_ARTIFACTS


def test_the_default_falls_back_to_the_archive_on_an_old_server(client, app, repo, monkeypatch):
    """Nothing exported (CI, a fresh install) against a server that predates the
    batch doors: the flip must not make those runs unreproducible. Exactly one
    warning, the archive, a record labelled `archive`, no capture rows."""
    monkeypatch.delenv(_run_mod.CODE_STORAGE_ENV, raising=False)
    app.batch_doors = False
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="no per-file capture doors") as caught:
        snap = _snap(run, repo)
    assert sum("capture doors" in str(w.message) for w in caught) == 1
    cb = snap["code_bytes"]
    assert cb["uploaded"] is True and cb["pending_upload"] == 0
    assert "storage" not in cb
    assert _code_rows(app, run.id) == []
    assert [a for a in app.artifacts[run.id] if a.get("kind") == "code_bytes"]
    assert _snapshot_meta(app, run.id)["storage"] == "archive"


def test_a_405_from_the_presign_door_also_falls_back_to_the_archive(client, app, repo, monkeypatch):
    """A router that knows the path but not the method answers 405, not 404.
    The client reads both as "no batch doors" and takes the archive."""
    monkeypatch.delenv(_run_mod.CODE_STORAGE_ENV, raising=False)
    original = app._dispatch

    def dispatch(request):
        if request.method == "POST" and request.url.path.endswith("/artifacts/uploads/batch"):
            return httpx.Response(405, json={"detail": "Method Not Allowed"})
        return original(request)

    monkeypatch.setattr(app, "_dispatch", dispatch)
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="no per-file capture doors"):
        snap = _snap(run, repo)
    cb = snap["code_bytes"]
    assert cb["uploaded"] is True and cb["pending_upload"] == 0
    assert _code_rows(app, run.id) == []
    assert [a for a in app.artifacts[run.id] if a.get("kind") == "code_bytes"]
    assert _snapshot_meta(app, run.id)["storage"] == "archive"


def test_probe_snapshot_prints_the_per_file_summary_by_default(
    client, app, repo, tmp_path, monkeypatch, capsys
):
    """What a researcher sees after upgrading: `probe snapshot RUN` with nothing
    exported reports files stored, never an archive size."""
    monkeypatch.delenv(_run_mod.CODE_STORAGE_ENV, raising=False)
    run = open_run(client, experiment="e", name="r")
    monkeypatch.setattr(
        cli, "Client", lambda **_kw: make_client(app, tmp_spool=tmp_path / "cli-spool")
    )
    capsys.readouterr()
    assert cli.main(["snapshot", run.id, "--cwd", str(repo), "--no-env", "--no-gpu"]) == 0
    out = capsys.readouterr().out
    assert "3 stored as files (3 uploaded, 0 already held)" in out
    assert "NOT stored" not in out and " MB" not in out
    assert {r["name"] for r in _code_rows(app, run.id)} == {"clean.py", "train.py", "notes.txt"}
    assert _snapshot_meta(app, run.id)["storage"] == "artifacts"


def test_snapshot_show_labels_a_default_capture_as_captured(
    client, app, repo, tmp_path, monkeypatch, capsys
):
    """The rows the SDK writes under the default are the rows `snapshot-show`
    reads back: every file `captured`, none `needs-upload`. The seeded rows in
    test_cli cannot catch a shape drift between writer and reader; a real
    capture can."""
    monkeypatch.delenv(_run_mod.CODE_STORAGE_ENV, raising=False)
    run = open_run(client, experiment="e", name="r")
    _snap(run, repo)
    monkeypatch.setattr(
        cli, "Client", lambda **_kw: make_client(app, tmp_spool=tmp_path / "cli-spool")
    )
    capsys.readouterr()
    assert cli.main(["snapshot-show", run.id]) == 0
    out = capsys.readouterr().out
    assert out.count("captured") == 3
    assert "3 stored as files, 0 pending upload" in out
    assert "needs-upload" not in out and "code-bytes" not in out
