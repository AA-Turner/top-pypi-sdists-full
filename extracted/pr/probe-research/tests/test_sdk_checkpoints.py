"""A run's checkpoints: best / latest, stored or not, and downloading a set
(`probe.sdk.checkpoints`, `Client.checkpoint`, `Client.download_checkpoint`).

The rows are shaped like the integrations write them
(`probe.integrations._checkpoints`): one `kind="checkpoint"` index row per save,
a hashless path reference whose `meta` is refreshed in place; with
`checkpoints="upload"` its `meta.members` lists the save's files, each its own
`kind="file"` row named `<index>/<member>`.
"""

from __future__ import annotations

import hashlib
import os

import pytest

from probe.sdk import checkpoints
from probe.sdk.checkpoints import AmbiguousCheckpoint, CheckpointNotStored
from probe.sdk.run import Run
from tests.conftest import make_client
from tests.test_outbox import seeded_run


def _index(name, step, *, step_index=None, members=None, **meta):
    row = {
        "id": f"id-{name}",
        "run_id": "run-1",
        "name": name,
        "kind": "checkpoint",
        "is_reference": True,
        "content_hash": None,
        "status": "complete",
        "step_index": step if step_index is None else step_index,
        "created_at": f"2026-10-12T00:00:{step % 60:02d}Z",
        "meta": {"step": step, **meta},
    }
    if members is not None:
        row["meta"].update(members=list(members), upload="requested")
    return row


def _member(index, rel, *, stored=True, refused=False):
    return {
        "id": f"id-{index}/{rel}",
        "run_id": "run-1",
        "name": f"{index}/{rel}",
        "kind": "file",
        "is_reference": not stored or refused,
        "content_hash": "ab" * 32 if stored else None,
        "status": "complete",
        "meta": {"checkpoint": index, **({"upload": "failed"} if refused else {})},
    }


# -- what proves bytes are stored -----------------------------------------------------


@pytest.mark.parametrize(
    ("row", "stored"),
    [
        ({"is_reference": False, "content_hash": "ab", "status": "complete"}, True),
        # A refused upload is a reference row, status complete: not stored.
        ({"is_reference": True, "content_hash": None, "status": "complete", "meta": {"upload": "failed"}}, False),
        ({"is_reference": False, "content_hash": "ab", "status": "pending"}, False),
        ({"is_reference": False, "content_hash": "ab", "status": "failed"}, False),
        ({"is_reference": False, "content_hash": None, "status": "complete"}, False),
        ({"is_reference": False, "content_hash": "ab", "status": "complete", "deleted_at": "x"}, False),
        (None, False),
    ],
)
def test_is_stored(row, stored):
    assert checkpoints.is_stored(row) is stored


def test_the_step_comes_from_meta_first():
    """A reference refreshed in place keeps the step_index it was first written
    with (the run route), while its meta is replaced whole."""
    assert checkpoints.step_of(_index("last.ckpt", 1200, step_index=400)) == 1200
    assert checkpoints.step_of({"step_index": 7, "meta": {}}) == 7
    assert checkpoints.step_of({"step_index": None, "meta": {"step": True}}) is None


# -- latest / best ----------------------------------------------------------------------


def test_latest_is_the_highest_step_even_when_step_index_is_stale():
    rows = [_index("a", 300), _index("last.ckpt", 1200, step_index=400), _index("b", 800)]
    assert checkpoints.select(rows, "latest")["name"] == "last.ckpt"


def test_best_is_the_flagged_row_and_never_a_guess():
    rows = [_index("a", 2, best=False, score=0.1), _index("b", 4, best=True, score=0.9)]
    assert checkpoints.select(rows, "best")["name"] == "b"
    assert checkpoints.select([_index("a", 2, score=0.1)], "best") is None


def test_two_callbacks_with_a_best_each_must_be_told_apart():
    rows = [
        _index("loss-top", 4, best=True, callback="ModelCheckpoint{'monitor': 'val_loss'}"),
        _index("acc-top", 6, best=True, callback="ModelCheckpoint{'monitor': 'val_acc'}"),
    ]
    with pytest.raises(AmbiguousCheckpoint) as caught:
        checkpoints.select(rows, "best")
    assert len(caught.value.callbacks) == 2
    picked = checkpoints.select(rows, "best", callback="ModelCheckpoint{'monitor': 'val_acc'}")
    assert picked["name"] == "acc-top"


def test_deleted_from_disk_but_uploaded_is_still_recoverable():
    stored = _index("ckpt-2@step2", 2, deleted=True, members=["model.safetensors"])
    gone = _index("ckpt-4@step4", 4, deleted=True)  # location only, and the location is gone
    rows = [stored, _member("ckpt-2@step2", "model.safetensors"), gone]
    assert checkpoints.select(rows, "latest")["name"] == "ckpt-2@step2"
    assert checkpoints.select(rows, "latest", recoverable_only=False)["name"] == "ckpt-4@step4"


def test_an_upload_with_a_refused_member_is_not_recoverable_once_deleted():
    index = _index("ckpt-2@step2", 2, deleted=True, members=["model.safetensors", "optimizer.pt"])
    rows = [index, _member("ckpt-2@step2", "model.safetensors"), _member("ckpt-2@step2", "optimizer.pt", refused=True)]
    assert checkpoints.missing_members(index, rows) == ["optimizer.pt"]
    assert checkpoints.select(rows, "latest") is None


def test_which_must_be_latest_or_best():
    with pytest.raises(ValueError):
        checkpoints.select([], "newest")


# -- downloading, against the fake API --------------------------------------------------


def _upload_set(app, tmp_path, files: dict[str, bytes], *, refuse: str | None = None):
    """A run with one uploaded set, logged the way the integrations log it."""
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox")
    run = Run(client, {"id": run_id})
    folder = tmp_path / "checkpoint-2"
    for rel, data in files.items():
        (folder / rel).parent.mkdir(parents=True, exist_ok=True)
        (folder / rel).write_bytes(data)
    for rel in files:
        if rel == refuse:
            run.log_artifact(f"checkpoint-2@step2/{rel}", path=str(folder / rel), reference=True, kind="file",
                             meta={"checkpoint": "checkpoint-2@step2", "upload": "failed"})
            continue
        run.log_artifact(f"checkpoint-2@step2/{rel}", path=str(folder / rel), kind="file", step_index=2,
                         meta={"checkpoint": "checkpoint-2@step2"})
    run.log_artifact("checkpoint-2@step2", path=str(folder), kind="checkpoint", reference=True, step_index=2,
                     meta={"step": 2, "members": sorted(files), "upload": "requested"})
    return client, run_id


def test_download_checkpoint_writes_every_member_byte_for_byte(app, tmp_path):
    files = {"model.safetensors": b"weights" * 100, "optimizer.pt": b"adam" * 50, "sub/rng_state.pth": b"rng"}
    client, run_id = _upload_set(app, tmp_path, files)
    row = client.checkpoint(run_id, "latest")
    assert row["name"] == "checkpoint-2@step2"
    got = client.download_checkpoint(row, tmp_path / "restored")
    assert sorted(f["path"] for f in got["files"]) == sorted(files)
    for rel, data in files.items():
        restored = (tmp_path / "restored" / rel).read_bytes()
        assert restored == data
        assert next(f for f in got["files"] if f["path"] == rel)["sha256"] == hashlib.sha256(data).hexdigest()
    # By id too (the CLI's path).
    again = client.download_checkpoint(row["id"], tmp_path / "again")
    assert len(again["files"]) == 3
    client.close()


def test_download_refuses_before_writing_when_a_member_is_not_stored(app, tmp_path):
    files = {"model.safetensors": b"weights", "optimizer.pt": b"adam"}
    client, run_id = _upload_set(app, tmp_path, files, refuse="optimizer.pt")
    assert client.checkpoint(run_id, "latest") is None  # not recoverable: one file never arrived
    row = client.checkpoint(run_id, "latest", recoverable=False)
    with pytest.raises(CheckpointNotStored) as caught:
        client.download_checkpoint(row, tmp_path / "restored")
    assert caught.value.missing == ["optimizer.pt"]
    assert not (tmp_path / "restored").exists()
    client.close()


def test_download_of_a_location_only_checkpoint_says_where_it_is(app, tmp_path):
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox")
    folder = tmp_path / "checkpoint-4"
    folder.mkdir()
    (folder / "model.safetensors").write_bytes(b"w")
    Run(client, {"id": run_id}).log_artifact("checkpoint-4", path=str(folder), kind="checkpoint", reference=True,
                                             step_index=4, meta={"step": 4})
    row = client.checkpoint(run_id, "latest")
    with pytest.raises(CheckpointNotStored) as caught:
        client.download_checkpoint(row, tmp_path / "restored")
    assert caught.value.location == str(folder)
    client.close()


def test_a_member_path_cannot_leave_the_destination(app, tmp_path):
    index = _index("evil@step1", 1, members=["../../etc/passwd"])
    rows = [index, _member("evil@step1", "../../etc/passwd")]

    class _Client:
        def list_run_artifacts(self, run_id, **_filters):
            return rows

        def download_artifact_to(self, *a, **k):  # pragma: no cover - must not be reached
            raise AssertionError("downloaded outside the destination")

    with pytest.raises(ValueError, match="leave the destination"):
        checkpoints.download(_Client(), index, tmp_path / "restored")


# -- the CLI ------------------------------------------------------------------------------


def test_cli_downloads_a_runs_latest_checkpoint_and_a_checkpoint_by_id(app, tmp_path, monkeypatch, capsys):
    from probe import cli

    app.refuse_reference_downloads = True
    files = {"model.safetensors": b"w" * 10, "optimizer.pt": b"o" * 5}
    client, run_id = _upload_set(app, tmp_path, files)
    index_id = client.checkpoint(run_id, "latest")["id"]
    client.close()
    monkeypatch.setattr(cli, "Client", lambda **_kw: make_client(app, tmp_spool=tmp_path / "cli-spool"))

    assert cli.main(["artifact", "download", "--run", run_id, "--checkpoint", "latest", "-o", str(tmp_path / "a")]) == 0
    assert (tmp_path / "a" / "model.safetensors").read_bytes() == files["model.safetensors"]
    # By id: the index row is a reference (409 from the presign), and its files come down.
    assert cli.main(["artifact", "download", index_id, "-o", str(tmp_path / "b")]) == 0
    assert (tmp_path / "b" / "optimizer.pt").read_bytes() == files["optimizer.pt"]
    capsys.readouterr()

    # No best was marked: a clear miss, not a guess.
    assert cli.main(["artifact", "download", "--run", run_id, "--checkpoint", "best", "-o", str(tmp_path / "c")]) == 1
    assert "no best checkpoint" in capsys.readouterr().err
    # A folder needs a folder.
    assert cli.main(["artifact", "download", "--run", run_id, "--checkpoint", "latest"]) == 2
    assert "pass -o DIR" in capsys.readouterr().err


def test_a_failed_member_takes_back_the_files_already_written(app, tmp_path, monkeypatch):
    """Half a checkpoint would load as a whole one."""
    files = {"a.pt": b"a", "b.pt": b"b"}
    client, run_id = _upload_set(app, tmp_path, files)
    row = client.checkpoint(run_id, "latest")
    real = client.download_artifact_to
    calls = []

    def flaky(artifact_id, dest, **kw):
        calls.append(dest)
        if len(calls) == 2:
            raise OSError("connection reset")
        return real(artifact_id, dest, **kw)

    monkeypatch.setattr(client, "download_artifact_to", flaky)
    with pytest.raises(OSError):
        client.download_checkpoint(row, tmp_path / "restored")
    assert not (tmp_path / "restored").exists()
    assert not [p for p in tmp_path.iterdir() if p.name.startswith(".restored.probe-")]  # staging gone
    client.close()


def test_a_restore_goes_into_a_new_or_empty_folder_only(app, tmp_path):
    """Review: restoring over an existing checkpoint overwrote files a failure
    then deleted, and left stale shards the loader would pick up."""
    client, run_id = _upload_set(app, tmp_path, {"a.pt": b"a"})
    row = client.checkpoint(run_id, "latest")
    busy = tmp_path / "busy"
    busy.mkdir()
    (busy / "old-shard.pt").write_bytes(b"old")
    with pytest.raises(FileExistsError):
        client.download_checkpoint(row, busy)
    assert (busy / "old-shard.pt").read_bytes() == b"old"
    empty = tmp_path / "empty"
    empty.mkdir()
    client.download_checkpoint(row, empty)
    assert (empty / "a.pt").read_bytes() == b"a"
    client.close()


# -- member paths that would leave the destination ---------------------------------------


@pytest.mark.parametrize("rel", ["a\\..\\b.bin", "x/y\x00.bin", "/etc/passwd", "a/../../b"])
def test_a_member_path_with_a_separator_or_parent_is_refused(tmp_path, rel):
    with pytest.raises(ValueError, match="leave the destination"):
        checkpoints._safe_target(tmp_path / "ckpt", rel)


@pytest.mark.parametrize("rel", ["C:x/y.bin", "C:/x/y.bin", "D:y.bin", "epoch=1:step=2.ckpt"])
def test_on_windows_a_drive_or_colon_is_refused(tmp_path, rel):
    """Review (security, CRITICAL): on Windows `Path(dest).joinpath("C:..")`
    drops `dest`, so a drive-qualified segment wrote outside the folder."""
    with pytest.raises(ValueError, match="leave the destination"):
        checkpoints._safe_target(tmp_path / "ckpt", rel, windows=True)


def test_a_colon_is_an_ordinary_character_elsewhere(tmp_path):
    """Review: refusing ':' everywhere made `epoch=1:step=2.ckpt` upload fine
    and never come back on Linux."""
    target = checkpoints._safe_target(tmp_path / "ckpt", "epoch=1:step=2.ckpt", windows=False)
    assert target == tmp_path / "ckpt" / "epoch=1:step=2.ckpt"


def test_a_link_already_in_the_destination_cannot_carry_a_member_out(tmp_path):
    dest = tmp_path / "ckpt"
    dest.mkdir()
    (tmp_path / "outside").mkdir()
    (dest / "sub").symlink_to(tmp_path / "outside")
    with pytest.raises(ValueError, match="leave the destination"):
        checkpoints._safe_target(dest, "sub/model.bin")
    assert checkpoints._safe_target(dest, "nested/model.bin") == dest / "nested" / "model.bin"


# -- the integrations' upload helper ------------------------------------------------------


class _RecordingRun:
    """Stands in for `Run.log_artifact` (signature checked against the real one)."""

    def __init__(self, outbox):
        import types

        self.calls = []
        self._client = types.SimpleNamespace(journal=types.SimpleNamespace(dir=str(outbox)))

    def log_artifact(self, name, **kw):
        import inspect

        inspect.signature(Run.log_artifact).bind(None, name, **kw)  # a real keyword set
        self.calls.append((name, kw))


def _folder(tmp_path, files):
    folder = tmp_path / "checkpoint-10"
    for rel in files:
        (folder / rel).parent.mkdir(parents=True, exist_ok=True)
        (folder / rel).write_bytes(b"x" * 8)
    return folder


def test_members_are_never_uploaded_strict(tmp_path):
    """A strict upload runs synchronously, on the training thread."""
    from probe.integrations import _checkpoints

    folder = _folder(tmp_path, ["model.safetensors", "optimizer.pt"])
    run = _RecordingRun(tmp_path)
    name, meta = _checkpoints.upload_set(run, str(folder), name="checkpoint-10", step=10, meta={}, size=16,
                                         strict=True, warn=lambda *a: None)
    members = [kw for n, kw in run.calls if n.startswith(name + "/")]
    (index,) = [kw for n, kw in run.calls if n == name]
    assert len(members) == 2 and all(kw["strict"] is False for kw in members)
    assert index["strict"] is True and meta["members"] == ["model.safetensors", "optimizer.pt"]


def test_a_set_that_would_be_copied_across_disks_is_recorded_as_a_location(tmp_path, monkeypatch):
    from probe.integrations import _checkpoints

    folder = _folder(tmp_path, ["model.safetensors"])
    run = _RecordingRun(tmp_path)
    files = [("m", str(folder / "model.safetensors"))]
    assert _checkpoints._foreground_bytes(run, files) == 8  # not queued: all of it is sent here
    run._client.async_writes = True
    assert _checkpoints._foreground_bytes(run, files) == 8  # small: copied into the outbox
    from probe.sdk import multipart

    monkeypatch.setattr(multipart, "threshold_bytes", lambda: 4)
    assert _checkpoints._foreground_bytes(run, files) == 0  # big, same disk: a hard link
    monkeypatch.setattr(_checkpoints, "_foreground_bytes", lambda run, files: 3 * 1024**3)
    said = []
    name, meta = _checkpoints.upload_set(run, str(folder), name="checkpoint-10", step=10, meta={}, size=8,
                                         strict=None, warn=lambda key, msg: said.append(msg))
    assert [n for n, _ in run.calls] == [name]  # the index only
    assert "members" not in meta and "upload" not in meta
    assert any("PROBE_OUTBOX_DIR" in m for m in said)


def test_files_a_probe_config_excludes_are_neither_uploaded_nor_named(tmp_path, monkeypatch):
    from probe.integrations import _checkpoints
    from probe.sdk import exclusions, probe_config as pc

    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    pc._CACHE.clear()
    pc._CHECKED.clear()
    exclusions._view_at = -1.0e9
    folder = _folder(tmp_path, ["model.safetensors", "private/notes.json", "secret.json"])
    (folder / pc.CONFIG_NAME).write_text("/private/\nsecret.json\n")
    run = _RecordingRun(tmp_path)
    _name, meta = _checkpoints.upload_set(run, str(folder), name="checkpoint-10", step=10, meta={}, size=24,
                                          strict=None, warn=lambda *a: None)
    named = " ".join(meta["members"]) + " ".join(n for n, _ in run.calls)
    assert "private" not in named and "secret.json" not in named
    assert "model.safetensors" in meta["members"]


def test_two_paths_with_one_basename_at_one_step_get_two_sets(tmp_path):
    """Review: two Lightning callbacks' `last.ckpt` saved at one step shared a
    set name, so their members (found by name) overwrote each other."""
    from probe.integrations import _checkpoints

    taken: dict[str, str] = {}
    a, b = tmp_path / "loss", tmp_path / "acc"
    for folder in (a, b):
        folder.mkdir()
        (folder / "last.ckpt").write_bytes(folder.name.encode())
    run = _RecordingRun(tmp_path)
    first, _ = _checkpoints.upload_set(run, str(a / "last.ckpt"), name="last.ckpt", step=8, meta={}, size=4,
                                       strict=None, warn=lambda *x: None, taken=taken)
    second, _ = _checkpoints.upload_set(run, str(b / "last.ckpt"), name="last.ckpt", step=8, meta={}, size=3,
                                        strict=None, warn=lambda *x: None, taken=taken)
    again, _ = _checkpoints.upload_set(run, str(a / "last.ckpt"), name="last.ckpt", step=8, meta={}, size=4,
                                       strict=None, warn=lambda *x: None, taken=taken)
    assert first == "last@step8.ckpt" and second.startswith("last@step8~") and second.endswith(".ckpt")
    assert again == first
    members = [n for n, _ in run.calls if "/" in n]
    assert len(set(members)) == 2


def test_a_link_inside_a_checkpoint_makes_it_a_location_only(tmp_path):
    """Review: a linked `model.safetensors` was skipped and the rest recorded as
    the whole checkpoint, so a download "succeeded" without the weights."""
    from probe.integrations import _checkpoints

    folder = _folder(tmp_path, ["trainer_state.json"])
    real = tmp_path / "weights.safetensors"
    real.write_bytes(b"w")
    (folder / "model.safetensors").symlink_to(real)
    run, said = _RecordingRun(tmp_path), []
    name, meta = _checkpoints.upload_set(run, str(folder), name="checkpoint-10", step=10, meta={}, size=2,
                                         strict=None, warn=lambda key, msg: said.append(msg))
    assert [n for n, _ in run.calls] == [name] and "members" not in meta
    assert any("model.safetensors" in m for m in said)


def test_a_checkpoint_that_is_itself_a_link_is_followed(tmp_path):
    """Lightning's save_last="link" makes last.ckpt a link to the newest save."""
    from probe.integrations import _checkpoints

    real = tmp_path / "epoch=1.ckpt"
    real.write_bytes(b"w")
    (tmp_path / "last.ckpt").symlink_to(real)
    found = _checkpoints.inventory(str(tmp_path / "last.ckpt"))
    assert found.files == [("last.ckpt", str(real))] and not found.skipped


def test_member_names_are_nfc_like_the_servers(tmp_path):
    import unicodedata

    from probe.integrations import _checkpoints

    decomposed = unicodedata.normalize("NFD", "café.pt")
    folder = _folder(tmp_path, [decomposed])
    (rel, _full), = _checkpoints.inventory(str(folder)).files
    assert rel == unicodedata.normalize("NFC", "café.pt")


def test_the_walk_gives_up_on_a_huge_tree(tmp_path, monkeypatch):
    from probe.integrations import _checkpoints

    monkeypatch.setattr(_checkpoints, "MAX_WALK_ENTRIES", 10)
    folder = tmp_path / "checkpoint-10"
    for i in range(20):
        (folder / f"d{i}").mkdir(parents=True)
    assert _checkpoints.inventory(str(folder)).too_many is True


def test_a_member_whose_bytes_do_not_match_never_reaches_the_folder(tmp_path):
    from pathlib import Path

    index = _index("ck@step1", 1, members=["a.pt", "b.pt"])
    rows = [index, _member("ck@step1", "a.pt"), _member("ck@step1", "b.pt")]
    dest = tmp_path / "out"
    dest.mkdir()

    class _Client:
        def download_artifact_to(self, artifact_id, dest_path):
            Path(dest_path).write_bytes(b"WRONG")
            return {"sha256": "ab" * 32 if artifact_id.endswith("a.pt") else "cd" * 32, "size_bytes": 5}

    with pytest.raises(CheckpointNotStored) as caught:
        checkpoints.download(_Client(), index, dest, rows=rows)
    assert caught.value.missing == ["b.pt"]
    assert list(dest.iterdir()) == []  # the empty folder stays empty


def test_a_stored_checkpoint_file_downloads_under_its_name(app, tmp_path):
    """A script's own `log_artifact("ckpt", path="ckpt-4000.pt")` is a stored
    checkpoint now (the default kind): it comes back as dest/ckpt.pt."""
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox")
    (tmp_path / "ckpt-4000.pt").write_bytes(b"weights")
    Run(client, {"id": run_id}).log_artifact("ckpt", path=str(tmp_path / "ckpt-4000.pt"), step_index=4000, sync=True)
    row = client.checkpoint(run_id, "latest")
    assert row["kind"] == "checkpoint"
    got = client.download_checkpoint(row, tmp_path / "restored")
    assert (tmp_path / "restored" / "ckpt.pt").read_bytes() == b"weights" and got["files"][0]["path"] == "ckpt.pt"
    client.close()


@pytest.mark.parametrize("how", ["pending", "refused"])
def test_latest_is_the_newest_save_that_can_be_had(how):
    """Review: `latest` picked the newest save even when its files never
    arrive (an in-place rewrite abandoned the upload, a preempted job lost its
    outbox), so the crash-resume restore failed while a stored save existed."""
    newest = {**_member("new@step4", "m.pt"), "status": "pending"} if how == "pending" else _member("new@step4", "m.pt", refused=True)
    rows = [_index("old@step2", 2, members=["m.pt"]), _member("old@step2", "m.pt"),
            _index("new@step4", 4, members=["m.pt"]), newest]
    assert checkpoints.select(rows, "latest")["name"] == "old@step2"
    assert checkpoints.select(rows, "latest", recoverable_only=False)["name"] == "new@step4"


def test_an_empty_or_too_big_checkpoint_is_a_location_only(tmp_path, monkeypatch):
    from probe.integrations import _checkpoints

    empty = tmp_path / "checkpoint-1"
    empty.mkdir()
    run, said = _RecordingRun(tmp_path), []
    name, meta = _checkpoints.upload_set(run, str(empty), name="checkpoint-1", step=1, meta={}, size=0,
                                         strict=None, warn=lambda key, msg: said.append(key))
    assert [n for n, _ in run.calls] == [name] and "members" not in meta and said == ["checkpoint_members"]
    monkeypatch.setattr(_checkpoints, "MAX_MEMBERS", 2)
    folder = _folder(tmp_path, ["a.pt", "b.pt"])
    assert len(_checkpoints.inventory(str(folder)).files) == 2 and not _checkpoints.inventory(str(folder)).too_many
    (folder / "c.pt").write_bytes(b"x")
    assert _checkpoints.inventory(str(folder)).too_many


def test_saves_without_a_step_are_separate_sets(tmp_path):
    """Review (Codex P2): a custom callback with no step saved one path twice
    under one set name, so its files became versions of each other."""
    from probe.integrations import _checkpoints

    (tmp_path / "last.ckpt").write_bytes(b"1")
    taken: dict[str, str] = {}
    run = _RecordingRun(tmp_path)
    first, _ = _checkpoints.upload_set(run, str(tmp_path / "last.ckpt"), name="last.ckpt", step=None, meta={},
                                       size=1, strict=None, warn=lambda *x: None, taken=taken)
    second, _ = _checkpoints.upload_set(run, str(tmp_path / "last.ckpt"), name="last.ckpt", step=None, meta={},
                                        size=1, strict=None, warn=lambda *x: None, taken=taken)
    assert first != second and first.endswith(".ckpt") and second.endswith(".ckpt")


@pytest.fixture
def cli_wired(app, tmp_path, monkeypatch):
    from probe import cli

    monkeypatch.setattr(cli, "Client", lambda **_kw: make_client(app, tmp_spool=tmp_path / "cli-spool"))
    app.refuse_reference_downloads = True
    return cli


def test_cli_best_with_two_callbacks_asks_for_callback(app, tmp_path, cli_wired, capsys):
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox")
    run = Run(client, {"id": run_id})
    for name, cb in (("loss-top", "val_loss"), ("acc-top", "val_acc")):
        folder = tmp_path / name
        folder.mkdir()
        run.log_artifact(name, path=str(folder), kind="checkpoint", reference=True, step_index=2,
                         meta={"step": 2, "best": True, "callback": cb})
    client.close()
    out = ["-o", str(tmp_path / "o")]
    assert cli_wired.main(["artifact", "download", "--run", run_id, "--checkpoint", "best", *out]) == 2
    err = capsys.readouterr().err
    assert "val_loss" in err and "val_acc" in err and "--callback" in err
    # The pick works; it is a location only, so it says where it is.
    assert cli_wired.main(["artifact", "download", "--run", run_id, "--checkpoint", "best", "--callback", "val_acc", *out]) == 2
    assert "location only" in capsys.readouterr().err
    for bad in (["--callback", "val_acc", *out], ["--run", run_id, *out],
                ["--run", run_id, "--checkpoint", "newest", *out],
                ["--run", run_id, "--checkpoint", "latest", "--sha256", "ab", *out]):
        assert cli_wired.main(["artifact", "download", *bad]) == 2, bad


def test_cli_download_of_a_plain_reference_by_id_still_names_its_location(app, tmp_path, cli_wired, capsys):
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox")
    folder = tmp_path / "checkpoint-4"
    folder.mkdir()
    Run(client, {"id": run_id}).log_artifact("checkpoint-4", path=str(folder), kind="checkpoint",
                                             reference=True, step_index=4, meta={"step": 4})
    ref_id = client.checkpoint(run_id, "latest")["id"]
    client.close()
    for args in (["-o", str(tmp_path / "x")], ["-o", "-"]):
        assert cli_wired.main(["artifact", "download", ref_id, *args]) == 2
        assert "is a reference ->" in capsys.readouterr().err


def test_cli_an_uploaded_set_by_id_to_stdout_says_it_is_a_folder(app, tmp_path, cli_wired, capsys):
    client, run_id = _upload_set(app, tmp_path, {"a.pt": b"a"})
    index_id = client.checkpoint(run_id, "latest")["id"]
    client.close()
    assert cli_wired.main(["artifact", "download", index_id, "-o", "-"]) == 2
    assert "pass -o DIR" in capsys.readouterr().err
    assert cli_wired.main(["artifact", "download", index_id, "--sha256", "ab", "-o", str(tmp_path / "d")]) == 2


def test_the_newest_row_of_a_repeated_name_is_the_one_restored():
    """Review: rows come newest first and the lookup kept the LAST one, so a
    name saved twice restored the older bytes, hash check passing."""
    index = _index("ck@step5", 5, members=["m.pt"])
    old = {**_member("ck@step5", "m.pt"), "content_hash": "00" * 32, "created_at": "2026-10-12T00:00:01Z"}
    new = {**_member("ck@step5", "m.pt"), "content_hash": "11" * 32, "created_at": "2026-10-12T00:00:09Z"}
    assert checkpoints.member_rows(index, [new, old])["m.pt"]["content_hash"] == "11" * 32
    assert checkpoints.member_rows(index, [old, new])["m.pt"]["content_hash"] == "11" * 32


def test_a_restore_is_staged_inside_the_destination_and_keeps_normal_modes(app, tmp_path):
    """Review: staging beside the destination failed on a mount point (EBUSY,
    EXDEV) or a read-only parent, and the moved-in folder was mode 0700."""
    import stat

    client, run_id = _upload_set(app, tmp_path, {"a.pt": b"a", "sub/b.pt": b"b"})
    row = client.checkpoint(run_id, "latest")
    before = set(tmp_path.iterdir())
    client.download_checkpoint(row, tmp_path / "restored")
    assert set(tmp_path.iterdir()) - before == {tmp_path / "restored"}  # nothing staged beside it
    assert sorted(p.name for p in (tmp_path / "restored").iterdir()) == ["a.pt", "sub"]
    assert stat.S_IMODE((tmp_path / "restored").stat().st_mode) != 0o700
    client.close()


def test_find_reads_checkpoint_rows_then_one_candidates_files(app, tmp_path, monkeypatch):
    """Review: the whole run inventory was listed (twice), and a live run's
    listing can change mid-paging."""
    client, run_id = _upload_set(app, tmp_path, {"a.pt": b"a"})
    calls = []
    real = client.list_run_artifacts
    monkeypatch.setattr(client, "list_run_artifacts", lambda rid, **kw: calls.append(kw) or real(rid, **kw))
    row, files = checkpoints.find(client, run_id, "latest")
    assert row["name"] == "checkpoint-2@step2"
    assert "checkpoint-2@step2/a.pt" in {f["name"] for f in files}
    assert [c.get("kind") for c in calls] == ["checkpoint", None] and calls[1].get("prefix") == "checkpoint-2@step2"
    client.close()


def test_excluded_files_are_counted_and_the_restore_says_so(app, tmp_path):
    client, run_id = _upload_set(app, tmp_path, {"a.pt": b"a"})
    row = dict(client.checkpoint(run_id, "latest"))
    row["meta"] = {**row["meta"], "members_excluded": 2}
    got = client.download_checkpoint(row, tmp_path / "restored")
    assert got["excluded"] == 2 and got["redacted"] == []
    client.close()


@pytest.mark.parametrize("bad", [" padded.pt", "tab\\tname.pt", "zero\u200bwidth.pt"])
def test_a_file_the_server_would_refuse_to_name_makes_the_set_a_location(tmp_path, bad):
    from probe.integrations import _checkpoints

    folder = _folder(tmp_path, ["model.safetensors"])
    (folder / bad).write_bytes(b"x")
    run, said = _RecordingRun(tmp_path), []
    name, meta = _checkpoints.upload_set(run, str(folder), name="checkpoint-10", step=10, meta={}, size=9,
                                         strict=None, warn=lambda key, msg: said.append(key))
    assert [n for n, _ in run.calls] == [name] and "members" not in meta and said == ["checkpoint_incomplete"]


def test_excluded_files_are_counted_on_the_index(tmp_path, monkeypatch):
    from probe.integrations import _checkpoints
    from probe.sdk import exclusions, probe_config as pc

    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    pc._CACHE.clear()
    pc._CHECKED.clear()
    exclusions._view_at = -1.0e9
    folder = _folder(tmp_path, ["model.safetensors", "secret.json"])
    (folder / pc.CONFIG_NAME).write_text("secret.json\n")
    run = _RecordingRun(tmp_path)
    run._client.async_writes = True
    _name, meta = _checkpoints.upload_set(run, str(folder), name="checkpoint-10", step=10, meta={}, size=16,
                                          strict=None, warn=lambda *a: None)
    assert meta["members_excluded"] >= 1 and "secret.json" not in " ".join(meta["members"])


def test_a_failed_move_takes_back_the_moves_already_made(tmp_path, monkeypatch):
    """Review (Codex P2): one move succeeding and the next failing left files
    in the folder, which a retry then refused as not empty."""
    root = tmp_path / "restored"
    root.mkdir()
    staging = root / ".probe-restore-x"
    staging.mkdir()
    (staging / "a.pt").write_bytes(b"a")
    (staging / "b.pt").write_bytes(b"b")
    real = os.replace
    calls = []

    def flaky(src, dst):
        calls.append(dst)
        if len(calls) == 2:
            raise OSError("disk full")
        return real(src, dst)

    monkeypatch.setattr(checkpoints.os, "replace", flaky)
    with pytest.raises(OSError):
        checkpoints._commit(staging, root)
    assert sorted(p.name for p in root.iterdir()) == [".probe-restore-x"]


def test_a_destination_written_to_during_the_download_is_refused(tmp_path):
    root = tmp_path / "restored"
    root.mkdir()
    staging = root / ".probe-restore-x"
    staging.mkdir()
    (staging / "a.pt").write_bytes(b"a")
    (root / "theirs.txt").write_bytes(b"other writer")
    with pytest.raises(FileExistsError, match="changed during the download"):
        checkpoints._commit(staging, root)
    assert (root / "theirs.txt").read_bytes() == b"other writer" and not (root / "a.pt").exists()
