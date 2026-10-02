"""``build_pending_archive`` against a working tree that keeps moving, and
against a hostile one.

Drift the size-then-hash check on a PATH NAME does not catch, found by
adversarial review: a file that grew, one that shrank while being streamed, a
same-size edit landing between the verify pass and the stream, a regular file
swapped for a symlink or a FIFO, filesystem errors mid-capture, filenames git
would have C-quoted out of the manifest, and a directory name that used to
split a path out of the tree. Every one must be a classified verdict or a
precise SnapshotError, never a raw OSError escaping the fail-open path, never
a read that blocks, never a partial archive left on disk.
"""

from __future__ import annotations

import gzip
import hashlib
import os
import sys
import tarfile

import pytest

from probe.sdk.snapshot import (
    SnapshotError,
    _HashingReader,
    build_pending_archive,
    capture_manifest,
    is_inside_tree,
)
from tests.test_snapshot_upload import _members


@pytest.fixture
def repo(snapshot_repo):
    return snapshot_repo


def _once(monkeypatch, side_effect, *, target, on_pass: int = 2):
    """Run `side_effect` when tarfile first pulls `target` on its `on_pass`-th
    read of the file. The builder reads each regular file twice through a
    `_HashingReader` on ONE descriptor -- a verification hash, then the stream
    into the tar -- so pass 2 is "after the file was verified, while its bytes
    are entering the archive": the narrowest window drift can hit. The file is
    identified by inode (the descriptor is opened with os.open, so the file
    object carries no name). Returns the `fired` flag; every caller asserts it
    so a refactor that moves the reads turns these tests red, not silent."""
    ino = os.stat(target).st_ino
    original_init = _HashingReader.__init__
    original_read = _HashingReader.read
    passes = {"n": 0}
    fired = {"done": False}

    def init(self, fh):
        original_init(self, fh)
        try:
            mine = os.fstat(fh.fileno()).st_ino == ino
        except (AttributeError, OSError):
            mine = False
        if mine:
            passes["n"] += 1
        self._drift_pass = passes["n"] if mine else None

    def read(self, n=-1):
        if not fired["done"] and getattr(self, "_drift_pass", None) == on_pass:
            fired["done"] = True
            side_effect()
        return original_read(self, n)

    monkeypatch.setattr(_HashingReader, "__init__", init)
    monkeypatch.setattr(_HashingReader, "read", read)
    return fired


def test_a_file_that_grew_during_the_stream_is_archived_as_recorded(repo, tmp_path, monkeypatch):
    """An append keeps the recorded prefix intact, and that prefix IS what the
    manifest recorded: the archive equals the record."""
    manifest = capture_manifest(str(repo))
    entry = next(e for e in manifest["entries"] if e["path"] == "notes.txt")

    def append():
        with open(repo / "notes.txt", "ab") as fh:
            fh.write(b"appended later\n")

    fired = _once(monkeypatch, append, target=repo / "notes.txt")
    dest = tmp_path / "code.tar.gz"
    summary = build_pending_archive(str(repo), manifest, str(dest))
    assert fired["done"]
    assert summary["changed"] == [] and summary["n_files"] == 3
    with gzip.open(dest, "rb") as gz, tarfile.open(fileobj=gz, mode="r") as tar:
        member = tar.extractfile("notes.txt").read()
    assert hashlib.sha256(member).hexdigest() == entry["sha256"]
    assert os.path.getsize(repo / "notes.txt") > entry["size"]


def test_a_file_that_grew_during_the_verify_pass_is_archived_as_recorded(
    repo, tmp_path, monkeypatch
):
    """The verify pass is bounded to the recorded size, so growth during it
    behaves exactly like growth during the stream."""
    manifest = capture_manifest(str(repo))

    def append():
        with open(repo / "notes.txt", "ab") as fh:
            fh.write(b"appended later\n")

    fired = _once(monkeypatch, append, target=repo / "notes.txt", on_pass=1)
    summary = build_pending_archive(str(repo), manifest, str(tmp_path / "code.tar.gz"))
    assert fired["done"] and summary["changed"] == [] and summary["n_files"] == 3


def test_a_file_that_shrank_during_the_stream_aborts_the_archive(repo, tmp_path, monkeypatch):
    """The tar member is already short; nothing can be appended after it."""
    manifest = capture_manifest(str(repo))
    fired = _once(
        monkeypatch, lambda: (repo / "notes.txt").write_bytes(b"un"), target=repo / "notes.txt"
    )
    dest = tmp_path / "code.tar.gz"
    with pytest.raises(SnapshotError, match=r"notes\.txt.*shrank"):
        build_pending_archive(str(repo), manifest, str(dest))
    assert fired["done"] and not dest.exists()


def test_a_same_size_edit_between_the_verify_pass_and_the_stream_is_rebuilt_once(
    repo, tmp_path, monkeypatch
):
    """The narrowest window: verified, then the bytes changed before tarfile
    pulled them, so a wrong member sits in the tar. The archive is rebuilt once
    with that file reported changed -- a sqlite file rewritten in place at a
    constant size would otherwise never let a snapshot through."""
    manifest = capture_manifest(str(repo))
    original = (repo / "notes.txt").read_bytes()
    fired = _once(
        monkeypatch,
        lambda: (repo / "notes.txt").write_bytes(original[:-1] + b"X"),
        target=repo / "notes.txt",
    )
    dest = tmp_path / "code.tar.gz"
    summary = build_pending_archive(str(repo), manifest, str(dest))
    assert fired["done"]
    assert summary["changed"] == ["notes.txt"] and summary["n_files"] == 2
    assert "notes.txt" not in _members(dest)


def test_a_tree_that_will_not_hold_still_raises_after_one_rebuild(repo, tmp_path, monkeypatch):
    import probe.sdk.snapshot as _snapshot_mod

    manifest = capture_manifest(str(repo))
    calls = {"n": 0}
    real = _snapshot_mod._archive_entry

    def always_changing(archive, cwd, entry):
        if entry["path"] in ("notes.txt", "train.py"):
            calls["n"] += 1
            raise _snapshot_mod._ChangedUnderStream(entry["path"])
        return real(archive, cwd, entry)

    monkeypatch.setattr(_snapshot_mod, "_archive_entry", always_changing)
    dest = tmp_path / "code.tar.gz"
    with pytest.raises(SnapshotError, match="re-run the snapshot"):
        build_pending_archive(str(repo), manifest, str(dest))
    assert calls["n"] == 2 and not dest.exists()


def test_a_regular_file_swapped_for_a_symlink_is_changed(repo, tmp_path):
    manifest = capture_manifest(str(repo))
    (repo / "notes.txt").unlink()
    (repo / "notes.txt").symlink_to("clean.py")
    summary = build_pending_archive(str(repo), manifest, str(tmp_path / "code.tar.gz"))
    assert summary["changed"] == ["notes.txt"]


def test_a_regular_file_swapped_for_a_fifo_is_changed_and_never_blocks(repo, tmp_path):
    manifest = capture_manifest(str(repo))
    (repo / "notes.txt").unlink()
    os.mkfifo(repo / "notes.txt")
    summary = build_pending_archive(str(repo), manifest, str(tmp_path / "code.tar.gz"))
    assert summary["changed"] == ["notes.txt"]


def test_a_symlink_swapped_in_between_lstat_and_open_is_changed(repo, tmp_path, monkeypatch):
    """O_NOFOLLOW: the race the lstat cannot close is closed on the descriptor."""
    import probe.sdk.snapshot as _snapshot_mod

    manifest = capture_manifest(str(repo))
    real_lstat = os.lstat

    def lstat_then_swap(path, *a, **kw):
        st = real_lstat(path, *a, **kw)
        if str(path).endswith("notes.txt"):
            os.unlink(path)
            os.symlink("clean.py", path)
        return st

    monkeypatch.setattr(_snapshot_mod.os, "lstat", lstat_then_swap)
    summary = build_pending_archive(str(repo), manifest, str(tmp_path / "code.tar.gz"))
    assert summary["changed"] == ["notes.txt"]


def test_a_file_that_vanishes_between_lstat_and_open_is_missing(repo, tmp_path, monkeypatch):
    import probe.sdk.snapshot as _snapshot_mod

    manifest = capture_manifest(str(repo))
    real_lstat = os.lstat

    def lstat_then_unlink(path, *a, **kw):
        st = real_lstat(path, *a, **kw)
        if str(path).endswith("notes.txt"):
            os.unlink(path)
        return st

    monkeypatch.setattr(_snapshot_mod.os, "lstat", lstat_then_unlink)
    summary = build_pending_archive(str(repo), manifest, str(tmp_path / "code.tar.gz"))
    assert summary["missing"] == ["notes.txt"] and summary["changed"] == []


def test_an_unreadable_file_is_changed_not_propagated(repo, tmp_path):
    if os.geteuid() == 0:
        pytest.skip("root reads everything")
    manifest = capture_manifest(str(repo))
    os.chmod(repo / "notes.txt", 0)
    try:
        summary = build_pending_archive(str(repo), manifest, str(tmp_path / "code.tar.gz"))
    finally:
        os.chmod(repo / "notes.txt", 0o644)
    assert summary["changed"] == ["notes.txt"]


def test_an_empty_file_is_archived_not_refused_as_malformed(repo, tmp_path):
    """size 0 is a value, not an absence."""
    (repo / "empty.py").write_bytes(b"")
    manifest = capture_manifest(str(repo))
    assert next(e for e in manifest["entries"] if e["path"] == "empty.py")["size"] == 0
    dest = tmp_path / "code.tar.gz"
    summary = build_pending_archive(str(repo), manifest, str(dest))
    assert "empty.py" in _members(dest)
    assert summary["n_files"] == 4 and summary["missing"] == [] and summary["changed"] == []


# --- filenames git used to hide, and paths that must never leave the tree ----


def test_quoted_and_non_ascii_filenames_are_captured(repo, tmp_path):
    """Without -z, ls-files C-quotes a double quote, a backslash and every
    non-ASCII byte; the quoted form never isfile()s and the file silently
    leaves the manifest."""
    names = ['plot "final".png', "back\\slash.py", "caf\u00e9.py"]
    for name in names:
        (repo / name).write_text("x\n")
    manifest = capture_manifest(str(repo))
    assert set(names) <= {e["path"] for e in manifest["entries"]}
    dest = tmp_path / "code.tar.gz"
    summary = build_pending_archive(str(repo), manifest, str(dest))
    assert set(names) <= set(_members(dest)) and summary["missing"] == []


@pytest.mark.skipif(sys.platform == "darwin", reason="APFS rejects non-UTF8 filenames; exercised in Linux CI")
def test_a_non_utf8_filename_is_excluded_visibly_not_a_crash(repo, tmp_path):
    """A Latin-1 name cannot enter the tree digest or the JSON record. It used
    to crash `_git` with UnicodeDecodeError past the fail-open handler; now it
    is listed under `skipped` with a reason and the rest of the tree captures."""
    raw = b"caf\xe9-latin1.py"
    with open(os.path.join(os.fsencode(str(repo)), raw), "wb") as fh:
        fh.write(b"x\n")
    manifest = capture_manifest(str(repo))
    assert {e["path"] for e in manifest["entries"]} == {"clean.py", "notes.txt", "train.py"}
    skipped = [s for s in manifest["skipped"] if s["reason"] == "non_utf8_name"]
    assert skipped and "caf" in skipped[0]["path"] and "\ufffd" in skipped[0]["path"]
    summary = build_pending_archive(str(repo), manifest, str(tmp_path / "code.tar.gz"))
    assert summary["n_files"] == 3 and summary["missing"] == []


def test_a_line_separator_in_a_directory_name_cannot_escape_the_tree(tmp_path):
    """Found by review: `x<U+2028>..` split by str.splitlines() into `..` and
    walked OUT of the tree -- a cloned repo could capture the sibling
    ~/.ssh/id_rsa. Paths now come NUL-delimited and are guarded."""
    from tests.conftest import _git_for_fixture as git

    home = tmp_path / "home"
    (home / ".ssh").mkdir(parents=True)
    (home / ".ssh" / "id_rsa").write_text("SECRET\n")
    repo = home / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "t@e.com")
    git(repo, "config", "user.name", "t")
    decoy = repo / "x\u2028.." / ".config"
    decoy.mkdir(parents=True)
    # `.config/known_hosts`, not `.ssh/id_rsa`: a credential folder or a
    # key-shaped name is now skipped on the git path too (plan 0.5), and this
    # test is about the PATH, not the file.
    (decoy / "known_hosts").write_text("decoy\n")
    (repo / "plain.py").write_text("x\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "init")
    manifest = capture_manifest(str(repo))
    paths = {e["path"] for e in manifest["entries"]}
    assert all(is_inside_tree(p) for p in paths)
    assert "x\u2028../.config/known_hosts" in paths, "the real file, under its real name"
    dest = tmp_path / "code.tar.gz"
    build_pending_archive(str(repo), manifest, str(dest))
    assert not any(m.startswith("..") or os.path.isabs(m) for m in _members(dest))
    with gzip.open(dest, "rb") as gz, tarfile.open(fileobj=gz, mode="r") as tar:
        assert tar.extractfile("x\u2028../.config/known_hosts").read() == b"decoy\n"


def test_a_backslash_in_a_filename_is_still_a_filename():
    assert is_inside_tree("back\\slash.py") and is_inside_tree('plot "final".png')


def test_a_manifest_path_outside_the_tree_is_refused(repo, tmp_path):
    manifest = capture_manifest(str(repo))
    entry = next(e for e in manifest["entries"] if e["path"] == "notes.txt")
    for bad in (
        "../notes.txt",
        "/etc/passwd",
        "a/../../notes.txt",
        "a//b",
        "..\\notes.txt",
        "a\\..\\..\\x",
        "C:\\x",
    ):
        entry["path"] = bad
        with pytest.raises(SnapshotError, match="inside the tree"):
            build_pending_archive(str(repo), manifest, str(tmp_path / "code.tar.gz"))
    assert not (tmp_path / "code.tar.gz").exists()



# --- restore is data from the server; it never writes outside its destination ---


def _archive_with(tmp_path, members: dict[str, bytes]):
    dest = tmp_path / "hostile.tar.gz"
    with gzip.open(dest, "wb") as gz, tarfile.open(fileobj=gz, mode="w") as tar:
        for name, data in members.items():
            info = tarfile.TarInfo(name)
            info.size = len(data)
            import io

            tar.addfile(info, io.BytesIO(data))
    return dest


def test_restore_never_writes_through_a_symlinked_parent(tmp_path):
    """Found by review: entry `a -> /outside` then `a/victim.txt` made makedirs
    follow the link and unlink+overwrite a file outside the destination."""
    from probe.sdk.restore import restore_snapshot

    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "victim.txt").write_text("original\n")
    payload = b"pwned\n"
    manifest = {
        "entries": [
            {"path": "a", "mode": "120000", "sha256": hashlib.sha256(str(outside).encode()).hexdigest(),
             "size": len(str(outside)), "source": "blob", "symlink_target": str(outside)},
            {"path": "a/victim.txt", "mode": "100644", "sha256": hashlib.sha256(payload).hexdigest(),
             "size": len(payload), "source": "blob"},
        ]
    }
    archive = _archive_with(tmp_path, {"a/victim.txt": payload})
    dest = tmp_path / "dest"
    result = restore_snapshot(manifest, str(dest), archive_path=str(archive))
    assert (outside / "victim.txt").read_text() == "original\n", "nothing outside dest was touched"
    victim = next(f for f in result["files"] if f["path"] == "a/victim.txt")
    assert victim["status"] == "unavailable" and "symlinked directory" in victim["reason"]


def test_restore_refuses_a_member_larger_than_the_manifest_says(tmp_path):
    from probe.sdk.restore import restore_snapshot

    small = b"x\n"
    manifest = {
        "entries": [
            {"path": "f.py", "mode": "100644", "sha256": hashlib.sha256(small).hexdigest(),
             "size": len(small), "source": "blob"},
        ]
    }
    archive = _archive_with(tmp_path, {"f.py": b"x" * 4096})
    result = restore_snapshot(manifest, str(tmp_path / "dest"), archive_path=str(archive))
    f = result["files"][0]
    assert f["status"] == "unavailable" and "size" in f["reason"]


def test_restore_refuses_a_malformed_manifest_before_touching_disk(tmp_path):
    from probe.sdk.restore import RestoreError, restore_snapshot

    manifest = {"entries": [{"path": "ok.py", "mode": "100644", "sha256": "0" * 64, "size": 0}, {"path": "broken"}]}
    dest = tmp_path / "dest"
    with pytest.raises(RestoreError, match="malformed"):
        restore_snapshot(manifest, str(dest))
    assert not dest.exists()
