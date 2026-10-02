"""The bytes are STORED, not merely counted.

The gap these close: `capture_manifest` classified every file as retrievable
from a pushed remote (`source="git"`, carries a blob id) or not
(`source="blob"`, carries a sha256 and nothing else), its docstring said "git
cannot supply this, someone must upload it", and nothing ever did. A sha256
verifies a file you already have; it cannot produce one you do not. So a run on
an ephemeral box was identified precisely and gone permanently -- confirmed on
bird-sql-sft, where 16 completed runs lost their code when the box was rebuilt
while still reading as captured.

The `source="git"` half has since been retired outright, so these now cover a
simpler promise: everything in the manifest that is not a size reference and
still matches its recorded sha256/size is in the archive; anything that
drifted is left out and named.
"""

from __future__ import annotations

import gzip
import hashlib
import io
import os
import subprocess
import tarfile

import pytest

from probe.sdk import snapshot as _snapshot
from probe.sdk.snapshot import (
    SnapshotError,
    SnapshotTooLarge,
    build_pending_archive,
    capture_manifest,
    pending_entries,
)
from tests.conftest import open_run


def _git(cwd, *args):
    proc = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    assert proc.returncode == 0, f"git {' '.join(args)}: {proc.stderr}"
    return proc.stdout.strip()


@pytest.fixture
def repo(tmp_path):
    """A repo with a pushed remote, one clean file, one edited, one untracked.

    That mix used to be the point, back when the clean file stayed a git
    reference. It is kept because it is a realistic working tree, and because
    the three files now landing identically is itself the thing to pin.
    """
    remote = tmp_path / "remote.git"
    _git(tmp_path, "init", "--bare", "-q", str(remote))
    work = tmp_path / "work"
    work.mkdir()
    _git(work, "init", "-q")
    _git(work, "config", "user.email", "t@e.com")
    _git(work, "config", "user.name", "t")
    (work / "clean.py").write_text("UNCHANGED\n")
    (work / "train.py").write_text("print('v1')\n")
    _git(work, "add", "-A")
    _git(work, "commit", "-qm", "init")
    _git(work, "remote", "add", "origin", str(remote))
    _git(work, "push", "-q", "origin", "HEAD:main")

    (work / "train.py").write_text("print('v2 EDITED, uncommitted')\n")
    (work / "notes.txt").write_text("untracked\n")
    return work


def _members(path):
    with gzip.open(path, "rb") as gz, tarfile.open(fileobj=gz, mode="r") as tar:
        return {m.name: m for m in tar.getmembers()}


# --- what goes in ------------------------------------------------------------


def test_every_file_is_archived_including_the_clean_pushed_one(repo, tmp_path):
    """`clean.py` is committed and pushed. It is archived anyway -- that is the
    retirement of git referencing, seen from the archive side."""
    manifest = capture_manifest(str(repo))
    assert manifest["n_pending_upload"] == 3, [e["path"] for e in pending_entries(manifest)]

    dest = tmp_path / "code.tar.gz"
    summary = build_pending_archive(str(repo), manifest, str(dest))

    names = set(_members(dest))
    assert names == {"clean.py", "train.py", "notes.txt"}
    assert summary["n_files"] == 3


def test_a_size_reference_is_not_archived(repo, tmp_path):
    """The one exclusion left. Its bytes stay where they are by design, so
    sweeping it into the archive would be the duplication the threshold exists
    to prevent -- and would push the archive toward the upload ceiling."""
    (repo / "weights.bin").write_bytes(b"x" * 4096)
    manifest = capture_manifest(str(repo), reference_over_bytes=1024)

    dest = tmp_path / "code.tar.gz"
    build_pending_archive(str(repo), manifest, str(dest))

    assert "weights.bin" not in _members(dest)
    assert {"clean.py", "train.py", "notes.txt"} <= set(_members(dest))


def test_the_archived_bytes_are_the_working_tree_bytes(repo, tmp_path):
    """The edited-but-uncommitted content is exactly what git cannot give back."""
    dest = tmp_path / "code.tar.gz"
    build_pending_archive(str(repo), capture_manifest(str(repo)), str(dest))
    with gzip.open(dest, "rb") as gz, tarfile.open(fileobj=gz, mode="r") as tar:
        body = tar.extractfile("train.py").read().decode()
    assert body == "print('v2 EDITED, uncommitted')\n"


def test_gitignored_files_are_never_uploaded(repo, tmp_path):
    """`.gitignore` is the boundary for the archive exactly as it is for the git
    shadow commit -- a `.env` must not be shipped off the machine."""
    (repo / ".gitignore").write_text("secret.env\n")
    (repo / "secret.env").write_text("TOKEN=hunter2\n")
    dest = tmp_path / "code.tar.gz"
    build_pending_archive(str(repo), capture_manifest(str(repo)), str(dest))
    assert "secret.env" not in _members(dest)


# --- determinism (this is what makes sweep dedup work) -----------------------


def test_identical_trees_produce_byte_identical_archives(repo, tmp_path):
    """The presign `have` check is content-addressed, so a non-deterministic
    archive would re-upload the same code once per run in an N-run sweep."""
    manifest = capture_manifest(str(repo))
    a, b = tmp_path / "a.tar.gz", tmp_path / "b.tar.gz"
    first = build_pending_archive(str(repo), manifest, str(a))
    # touch mtimes: a timestamp must not change the archive
    (repo / "train.py").touch()
    second = build_pending_archive(str(repo), manifest, str(b))
    assert first["sha256"] == second["sha256"]
    assert a.read_bytes() == b.read_bytes()


def test_the_executable_bit_survives(repo, tmp_path):
    """A restored tree whose entrypoint lost +x does not run."""
    script = repo / "run.sh"
    script.write_text("#!/bin/sh\necho hi\n")
    script.chmod(0o755)
    dest = tmp_path / "code.tar.gz"
    build_pending_archive(str(repo), capture_manifest(str(repo)), str(dest))
    assert _members(dest)["run.sh"].mode == 0o755
    assert _members(dest)["notes.txt"].mode == 0o644


def test_symlinks_are_stored_as_links_not_followed(repo, tmp_path):
    (repo / "link.py").symlink_to("train.py")
    dest = tmp_path / "code.tar.gz"
    build_pending_archive(str(repo), capture_manifest(str(repo)), str(dest))
    member = _members(dest)["link.py"]
    assert member.issym() and member.linkname == "train.py"


# --- the cap refuses, never truncates ---------------------------------------


def test_over_the_cap_it_refuses_rather_than_shipping_a_partial_archive(repo, tmp_path):
    """Silently dropping files to fit is the original defect in a new place."""
    (repo / "big.bin").write_bytes(b"x" * 4096)
    with pytest.raises(SnapshotTooLarge, match="over the"):
        build_pending_archive(
            str(repo), capture_manifest(str(repo)), str(tmp_path / "c.tar.gz"), max_bytes=1024
        )
    assert not (tmp_path / "c.tar.gz").exists(), "the cap refuses before any byte is written"


# --- a tree that drifted from its manifest is archived honestly, never short --
#
# The original defect: a file missing at archive time was silently skipped and
# `n_files` still claimed it (a real archive recorded 7,689 files and held 316).
# The contract now: every file that still matches its manifest entry is
# archived and verified; every file that does not is LEFT OUT AND NAMED, and
# `n_files` is what was written. Drift is not an error -- a training job that
# is still writing a log while run 2 of a sweep snapshots is the normal case --
# so nothing here raises for it. Two things do raise: a malformed manifest
# entry, and a file that shrank under the stream (the tar cannot continue).


def _drift(repo, manifest, tmp_path):
    dest = tmp_path / "code.tar.gz"
    summary = build_pending_archive(str(repo), manifest, str(dest))
    return dest, summary


def test_a_file_deleted_after_classification_is_left_out_and_named(repo, tmp_path):
    manifest = capture_manifest(str(repo))
    (repo / "notes.txt").unlink()
    dest, summary = _drift(repo, manifest, tmp_path)
    assert summary["missing"] == ["notes.txt"] and summary["changed"] == []
    assert summary["n_files"] == 2 == len(_members(dest))
    assert "notes.txt" not in _members(dest)
    assert "1 missing from the working tree (notes.txt)" in summary["drift_message"]


def test_a_file_changed_after_classification_is_left_out_and_named(repo, tmp_path):
    manifest = capture_manifest(str(repo))
    (repo / "train.py").write_text("print('v3, longer than the manifest saw')\n")
    dest, summary = _drift(repo, manifest, tmp_path)
    assert summary["changed"] == ["train.py"] and summary["missing"] == []
    assert sorted(_members(dest)) == ["clean.py", "notes.txt"]
    assert "1 changed since the manifest was taken (train.py)" in summary["drift_message"]


def test_a_same_size_edit_is_caught_by_the_hash(repo, tmp_path):
    """Size alone would pass this one; the streamed sha256 must not."""
    manifest = capture_manifest(str(repo))
    original = (repo / "clean.py").read_text()
    (repo / "clean.py").write_text(original[:-2] + "X\n")
    assert len((repo / "clean.py").read_text()) == len(original)
    dest, summary = _drift(repo, manifest, tmp_path)
    assert summary["changed"] == ["clean.py"]
    assert "clean.py" not in _members(dest)


def test_a_retargeted_symlink_is_left_out(repo, tmp_path):
    (repo / "link.py").symlink_to("train.py")
    manifest = capture_manifest(str(repo))
    (repo / "link.py").unlink()
    (repo / "link.py").symlink_to("clean.py")
    dest, summary = _drift(repo, manifest, tmp_path)
    assert summary["changed"] == ["link.py"]
    assert "link.py" not in _members(dest)


def test_a_symlink_replaced_by_a_plain_file_is_changed_and_a_removed_one_missing(
    repo, tmp_path
):
    (repo / "link.py").symlink_to("train.py")
    (repo / "gone.py").symlink_to("train.py")
    manifest = capture_manifest(str(repo))
    (repo / "link.py").unlink()
    (repo / "link.py").write_text("now a file\n")
    (repo / "gone.py").unlink()
    _, summary = _drift(repo, manifest, tmp_path)
    assert summary["changed"] == ["link.py"] and summary["missing"] == ["gone.py"]


def test_n_files_is_what_was_written(repo, tmp_path):
    (repo / "link.py").symlink_to("train.py")
    manifest = capture_manifest(str(repo))
    dest, summary = _drift(repo, manifest, tmp_path)
    assert summary["n_files"] == len(pending_entries(manifest)) == 4 == len(_members(dest))
    assert summary["missing"] == [] and summary["changed"] == []
    assert summary["drift_message"] is None


def test_missing_and_changed_are_both_named_in_one_summary(repo, tmp_path):
    manifest = capture_manifest(str(repo))
    (repo / "clean.py").unlink()
    (repo / "train.py").write_text("also changed, and longer than before\n")
    dest, summary = _drift(repo, manifest, tmp_path)
    assert summary["missing"] == ["clean.py"] and summary["changed"] == ["train.py"]
    assert list(_members(dest)) == ["notes.txt"]
    message = summary["drift_message"]
    assert "1 missing from the working tree (clean.py)" in message
    assert "1 changed since the manifest was taken (train.py)" in message


def test_the_drift_message_names_five_paths_then_counts_the_rest():
    from probe.sdk.snapshot import _partial_archive_message

    five = [f"gone{i}.txt" for i in range(5)]
    assert "+" not in _partial_archive_message(five, [])
    eight = [f"gone{i}.txt" for i in range(8)]
    message = _partial_archive_message(eight, [])
    assert "8 missing" in message and "+3 more" in message
    assert "gone5.txt" not in message


def test_the_hashing_reader_digests_exactly_what_passes_through_it():
    from probe.sdk.snapshot import _HashingReader

    payload = bytes(range(256)) * 300
    whole = _HashingReader(io.BytesIO(payload))
    assert whole.read() == payload
    assert whole.hexdigest() == hashlib.sha256(payload).hexdigest()
    assert whole.bytes_read == len(payload)

    chunked = _HashingReader(io.BytesIO(payload))
    while chunked.read(1000):
        pass
    assert chunked.hexdigest() == hashlib.sha256(payload).hexdigest()

    partial = _HashingReader(io.BytesIO(payload))
    partial.read(10)
    assert partial.hexdigest() == hashlib.sha256(payload[:10]).hexdigest()
    assert partial.bytes_read == 10


def test_a_file_spanning_several_tar_reads_is_hashed_whole(repo, tmp_path):
    """tarfile pulls 16 KiB at a time; the hash must cover every chunk, and a
    same-size edit deep in the file must still be caught."""
    big = bytes(range(256)) * 160  # 40,960 bytes, > 2 tar reads
    (repo / "big.bin").write_bytes(big)
    manifest = capture_manifest(str(repo))
    dest, summary = _drift(repo, manifest, tmp_path)
    assert "big.bin" in _members(dest) and summary["changed"] == []

    edited = bytearray(big)
    edited[39_000] ^= 0xFF
    (repo / "big.bin").write_bytes(bytes(edited))
    _, summary = _drift(repo, manifest, tmp_path)
    assert summary["changed"] == ["big.bin"]


def test_a_manifest_entry_without_sha256_or_size_is_refused_as_malformed(repo, tmp_path):
    """Verification can never be switched off by an incomplete record."""
    for field in ("sha256", "size"):
        manifest = capture_manifest(str(repo))
        entry = next(e for e in manifest["entries"] if e["path"] == "notes.txt")
        del entry[field]
        dest = tmp_path / f"code-{field}.tar.gz"
        with pytest.raises(SnapshotError, match=r"notes\.txt.*malformed"):
            build_pending_archive(str(repo), manifest, str(dest))
        assert not dest.exists()
    (repo / "link.py").symlink_to("train.py")
    manifest = capture_manifest(str(repo))
    del next(e for e in manifest["entries"] if e["path"] == "link.py")["symlink_target"]
    with pytest.raises(SnapshotError, match=r"link\.py.*no recorded target"):
        build_pending_archive(str(repo), manifest, str(tmp_path / "code-link.tar.gz"))


def test_a_refusal_survives_a_failed_cleanup_of_the_partial_archive(repo, tmp_path, monkeypatch):
    """The SnapshotError must still propagate when the partial archive cannot
    be removed: the caller's fail-open handling is keyed on RosError, and an
    escaping OSError would crash the run instead of warning."""
    import probe.sdk.snapshot as _snapshot_mod

    manifest = capture_manifest(str(repo))
    del next(e for e in manifest["entries"] if e["path"] == "notes.txt")["sha256"]
    real_unlink = os.unlink

    def refuse_unlink(path, *args, **kwargs):
        if str(path).endswith("code.tar.gz"):
            raise PermissionError(path)
        return real_unlink(path, *args, **kwargs)

    monkeypatch.setattr(_snapshot_mod.os, "unlink", refuse_unlink)
    with pytest.raises(SnapshotError, match="malformed"):
        build_pending_archive(str(repo), manifest, str(tmp_path / "code.tar.gz"))


# --- drift through Run.snapshot: recorded, named, never silent ---------------


def _drifted_snapshot(client, repo, monkeypatch, mutate, **kw):
    run = open_run(client, experiment="e", name="r")
    real = _snapshot.build_pending_archive

    def drifted(cwd, manifest, dest, **kwargs):
        mutate()
        return real(cwd, manifest, dest, **kwargs)

    monkeypatch.setattr(_snapshot, "build_pending_archive", drifted)
    return run, run.snapshot(cwd=str(repo), include_env=False, include_gpu=False, **kw)


def test_a_drifted_file_is_recorded_as_unstored_and_the_rest_is_kept(
    client, app, repo, monkeypatch
):
    with pytest.warns(UserWarning, match=r"stored 2 of 3 files.*notes\.txt"):
        run, snap = _drifted_snapshot(
            client, repo, monkeypatch, lambda: (repo / "notes.txt").unlink()
        )
    cb = snap["code_bytes"]
    assert cb["uploaded"] is True and cb["n_files"] == 2
    assert cb["pending_upload"] == 1, "one file's bytes did not land"
    assert cb["drifted"] == ["notes.txt"]
    meta = next(a["meta"] for a in app.artifacts[run.id] if a.get("kind") == "code_snapshot")
    assert meta["n_pending_upload"] == 1 and meta["n_classified_pending"] == 3
    stored = next(a for a in app.artifacts[run.id] if a.get("kind") == "code_bytes")
    assert sorted(stored["meta"]["paths"]) == ["clean.py", "train.py"]
    assert stored["meta"]["drifted"] == ["notes.txt"]


def test_in_strict_mode_drift_is_still_recorded_not_raised(client, app, repo, monkeypatch):
    client.fail_open = False
    with pytest.warns(UserWarning, match=r"notes\.txt"):
        _, snap = _drifted_snapshot(
            client, repo, monkeypatch, lambda: (repo / "notes.txt").unlink()
        )
    assert snap["code_bytes"]["pending_upload"] == 1


def test_a_tree_that_drifted_entirely_stores_nothing_and_says_so(
    client, app, repo, monkeypatch
):
    def wipe():
        for name in ("clean.py", "train.py", "notes.txt"):
            (repo / name).unlink()

    with pytest.warns(UserWarning, match=r"stored 0 of 3 files"):
        run, snap = _drifted_snapshot(client, repo, monkeypatch, wipe)
    cb = snap["code_bytes"]
    assert cb["uploaded"] is False and cb["pending_upload"] == 3
    assert cb["reason"] == "tree drifted during capture"
    assert not [a for a in app.artifacts[run.id] if a.get("kind") == "code_bytes"]


def test_a_malformed_manifest_is_fail_open_and_names_itself(client, app, repo, monkeypatch):
    """A SnapshotError (not drift) still takes the fail-open branch, and the
    warning carries the cause so a user can see WHICH record is broken."""
    real = _snapshot.build_pending_archive

    def malformed(cwd, manifest, dest, **kwargs):
        del next(e for e in manifest["entries"] if e["path"] == "notes.txt")["sha256"]
        return real(cwd, manifest, dest, **kwargs)

    monkeypatch.setattr(_snapshot, "build_pending_archive", malformed)
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match=r"upload failed.*notes\.txt.*malformed"):
        snap = run.snapshot(cwd=str(repo), include_env=False, include_gpu=False)
    assert snap["code_bytes"]["pending_upload"] == 3
    assert not [a for a in app.artifacts[run.id] if a.get("kind") == "code_bytes"]


def test_a_storage_failure_in_fail_open_mode_does_not_read_as_stored(client, app, repo):
    """A 503 from storage makes log_artifact record a REFERENCE to the tmp
    archive (which the finally block deletes). That is not stored bytes and
    must not zero n_pending_upload -- it did."""
    app.fail_next_uploads = True
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="storage refused"):
        snap = run.snapshot(cwd=str(repo), include_env=False, include_gpu=False)
    cb = snap["code_bytes"]
    assert cb["uploaded"] is False and cb["pending_upload"] == 3
    meta = next(a["meta"] for a in app.artifacts[run.id] if a.get("kind") == "code_snapshot")
    assert meta["n_pending_upload"] == 3 and meta["n_classified_pending"] == 3
    from probe.cli.main import _code_bytes_row

    assert _code_bytes_row(client, run.id) is None, "a pointer to a deleted tmp file is not stored bytes"


def test_a_spooled_write_still_names_the_drifted_file(client, app, repo, monkeypatch):
    import warnings

    from probe.sdk.run import Run

    original = Run.log_artifact

    def spooled(self, name, *a, **kw):
        return None if name == _snapshot.CODE_BYTES_ARTIFACT else original(self, name, *a, **kw)

    monkeypatch.setattr(Run, "log_artifact", spooled)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        _, snap = _drifted_snapshot(
            client, repo, monkeypatch, lambda: (repo / "notes.txt").unlink()
        )
    assert snap["code_bytes"]["reason"] == "spooled" and snap["code_bytes"]["pending_upload"] == 3
    assert snap["code_bytes"]["drifted"] == ["notes.txt"]
    assert any("notes.txt" in str(w.message) for w in caught), "drifted path never surfaced"


def test_the_drifted_list_is_capped_but_the_count_is_not(client, app, repo, monkeypatch):
    from probe.sdk.snapshot import DRIFTED_META_LIMIT

    for i in range(60):
        (repo / f"gone{i:02d}.txt").write_text("x\n")

    def wipe():
        for i in range(60):
            (repo / f"gone{i:02d}.txt").unlink()

    with pytest.warns(UserWarning, match=r"stored 3 of 63"):
        run, snap = _drifted_snapshot(client, repo, monkeypatch, wipe)
    cb = snap["code_bytes"]
    assert cb["pending_upload"] == 60 and len(cb["drifted"]) == DRIFTED_META_LIMIT
    stored = next(a for a in app.artifacts[run.id] if a.get("kind") == "code_bytes")
    assert len(stored["meta"]["drifted"]) == DRIFTED_META_LIMIT
    assert sorted(stored["meta"]["paths"]) == ["clean.py", "notes.txt", "train.py"]


# --- end to end through Run.snapshot ----------------------------------------


def test_snapshot_uploads_the_pending_bytes_and_clears_the_count(client, app, repo):
    """`n_pending_upload` in the artifact meta must mean "these bytes are gone".
    check_run gates `pending_code_bytes` on it, so reporting the pre-upload
    classification there would call an unreproducible run complete."""
    client.fail_open = False
    run = open_run(client, experiment="e", name="r")
    snap = run.snapshot(cwd=str(repo), include_env=False, include_gpu=False)

    cb = snap["code_bytes"]
    assert cb["uploaded"] is True
    assert cb["n_files"] == 3
    assert cb["pending_upload"] == 0

    meta = next(
        a["meta"]
        for rows in app.artifacts.values()
        for a in rows
        if a.get("kind") == "code_snapshot"
    )
    assert meta["n_pending_upload"] == 0, "bytes are stored; nothing is pending"
    assert meta["n_classified_pending"] == 3, "the pre-upload count survives for diagnostics"
    assert meta["n_git_referenced"] == 0, "no file is excused from upload by git"
    assert sorted(meta["code_bytes"]["archive_sha256"]) is not None

    stored = [a for rows in app.artifacts.values() for a in rows if a.get("kind") == "code_bytes"]
    assert len(stored) == 1
    assert stored[0]["is_reference"] is not True, "must be real bytes, not a pointer"
    assert sorted(stored[0]["meta"]["paths"]) == ["clean.py", "notes.txt", "train.py"]


def test_no_upload_leaves_the_count_honest(client, app, repo):
    client.fail_open = False
    run = open_run(client, experiment="e", name="r")
    snap = run.snapshot(cwd=str(repo), include_env=False, include_gpu=False, upload=False)

    assert snap["code_bytes"]["uploaded"] is False
    assert snap["code_bytes"]["pending_upload"] == 3
    meta = next(
        a["meta"]
        for rows in app.artifacts.values()
        for a in rows
        if a.get("kind") == "code_snapshot"
    )
    assert meta["n_pending_upload"] == 3, "opting out must not look like success"


def test_a_fully_pushed_tree_uploads_all_of_it(client, app, repo):
    """The case git referencing existed for. Committing and pushing everything
    used to make the archive disappear; now it changes nothing at all."""
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "everything")
    _git(repo, "push", "-q", "origin", "HEAD:main")

    client.fail_open = False
    run = open_run(client, experiment="e", name="r")
    snap = run.snapshot(cwd=str(repo), include_env=False, include_gpu=False)

    assert snap["code_bytes"]["uploaded"] is True
    assert snap["code_bytes"]["pending_upload"] == 0
    assert snap["code_bytes"]["n_files"] == 3
    assert [a for rows in app.artifacts.values() for a in rows if a.get("kind") == "code_bytes"]


def test_nothing_pending_means_no_archive_at_all(client, app, repo):
    """Not an empty one. The only route to nothing-pending left is a tree whose
    every file is above the size threshold."""
    client.fail_open = False
    run = open_run(client, experiment="e", name="r")
    snap = run.snapshot(
        cwd=str(repo), include_env=False, include_gpu=False, reference_over_bytes=1
    )

    assert snap["code_bytes"]["pending_upload"] == 0
    assert snap["code_bytes"]["uploaded"] is False
    assert snap["code_bytes"]["reason"] == "nothing pending"
    assert not [a for rows in app.artifacts.values() for a in rows if a.get("kind") == "code_bytes"]



def test_drift_warnings_cannot_kill_a_run_under_warnings_as_errors(client, app, repo, monkeypatch):
    """Drift is the common case on a live tree, and the warning fires AFTER the
    archive landed: under -W error a raw warnings.warn would raise between the
    code-bytes upload and the code-snapshot write, leaving an orphan row."""
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        run, snap = _drifted_snapshot(
            client, repo, monkeypatch, lambda: (repo / "notes.txt").unlink()
        )
    assert snap["code_bytes"]["pending_upload"] == 1
    assert any(a.get("kind") == "code_snapshot" for a in app.artifacts[run.id])
