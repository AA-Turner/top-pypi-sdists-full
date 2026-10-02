"""Rebuild the captured tree, or say precisely what is missing.

Storing bytes without a way to reassemble them moves the gap rather than closing
it, so these tests destroy the working tree before restoring — a restore that
quietly reads the originals would prove nothing.
"""

from __future__ import annotations

import gzip
import os
import shutil
import subprocess
import tarfile
import tempfile

import pytest

from probe.sdk.restore import RestoreError, restore_snapshot, verify_restored_tree
from probe.sdk.snapshot import build_pending_archive, capture_manifest


def _git(cwd, *args):
    proc = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    assert proc.returncode == 0, f"git {' '.join(args)}: {proc.stderr}"
    return proc.stdout.strip()


@pytest.fixture
def captured(tmp_path):
    """A pushed remote, a captured manifest, an archive — then the tree is gone.

    Mirrors the real failure: the box that held the working tree is destroyed and
    all that survives is the remote, the manifest, and the uploaded archive.
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

    (work / "train.py").write_text("LR = 3e-4  # tweaked, never committed\n")
    (work / "config.yaml").write_text("seed: 1337\n")
    (work / "scripts").mkdir()
    (work / "scripts" / "go.sh").write_text("#!/bin/sh\ntrain\n")
    (work / "scripts" / "go.sh").chmod(0o755)

    manifest = capture_manifest(str(work))
    archive = tmp_path / "code.tar.gz"
    build_pending_archive(str(work), manifest, str(archive))

    originals = {
        e["path"]: (work / e["path"]).read_bytes()
        for e in manifest["entries"]
        if e.get("mode") != "120000"
    }
    shutil.rmtree(work)  # *** the box is destroyed ***
    return manifest, str(archive), originals


@pytest.fixture
def legacy_captured(captured, tmp_path):
    """`captured`, re-marked the way a pre-retirement manifest looked.

    Hand-built rather than captured, because `capture_manifest` cannot produce a
    git entry any more — which is the point of the change, and exactly why the
    restore side still needs a fixture that does.
    """
    manifest, archive, originals = captured
    # Fetch the base commit by SHA rather than cloning: the bare remote's own
    # HEAD is unborn (everything was pushed to an explicit refspec), so a clone
    # checks out nothing.
    repo = tempfile.mkdtemp(prefix="probe-legacy-")
    _git(repo, "init", "-q")
    _git(repo, "remote", "add", "origin", str(tmp_path / "remote.git"))
    _git(repo, "fetch", "-q", "origin", manifest["base_commit"])
    blob = _git(repo, "rev-parse", f"{manifest['base_commit']}:clean.py")

    entries = []
    for entry in manifest["entries"]:
        if entry["path"] == "clean.py":
            entry = {**entry, "source": "git", "blob": blob}
        entries.append(entry)
    return {**manifest, "entries": entries, "n_git_referenced": 1}, archive, originals


# --- the whole point ---------------------------------------------------------


def test_a_destroyed_tree_is_rebuilt_byte_for_byte(captured, tmp_path):
    manifest, archive, originals = captured
    dest = tmp_path / "rebuilt"

    result = restore_snapshot(manifest, str(dest), archive_path=archive)

    assert result["n_unavailable"] == 0, [f for f in result["files"] if f.get("reason")]
    assert result["tree_matches"] is True
    for path, want in originals.items():
        assert (dest / path).read_bytes() == want, path
    assert verify_restored_tree(manifest, str(dest)) == []


def test_everything_comes_from_the_archive(captured, tmp_path):
    """`clean.py` is committed and pushed and STILL comes out of the archive —
    a current capture has no git half for restore to reach for."""
    manifest, archive, _ = captured
    result = restore_snapshot(manifest, str(tmp_path / "r"), archive_path=archive)
    by_path = {f["path"]: f["source"] for f in result["files"]}
    assert by_path["clean.py"] == "blob"
    assert by_path["train.py"] == "blob"
    assert by_path["config.yaml"] == "blob"


def test_a_legacy_git_entry_is_still_fetched(legacy_captured, tmp_path):
    """Restore keeps the git half for the manifests already in the database.

    Retiring the classifier changed what gets WRITTEN; it cannot change what
    was written last month, and those runs still restore from their remote.
    Getting either half wrong would still pass a test that only counted files.
    """
    manifest, archive, originals = legacy_captured
    dest = tmp_path / "r"
    result = restore_snapshot(manifest, str(dest), archive_path=archive)

    by_path = {f["path"]: f["source"] for f in result["files"]}
    assert by_path["clean.py"] == "git", "the legacy entry must come from the remote"
    assert by_path["train.py"] == "blob"
    assert result["n_unavailable"] == 0, [f for f in result["files"] if f.get("reason")]
    assert (dest / "clean.py").read_bytes() == originals["clean.py"]


def test_the_executable_bit_is_restored(captured, tmp_path):
    manifest, archive, _ = captured
    dest = tmp_path / "r"
    restore_snapshot(manifest, str(dest), archive_path=archive)
    assert os.access(dest / "scripts" / "go.sh", os.X_OK)


def test_nested_directories_are_created(captured, tmp_path):
    manifest, archive, _ = captured
    dest = tmp_path / "r"
    restore_snapshot(manifest, str(dest), archive_path=archive)
    assert (dest / "scripts" / "go.sh").is_file()


# --- it must refuse to hand back a tree that only looks right ----------------


def test_a_tampered_archive_member_is_refused_not_written(captured, tmp_path):
    """The probe.sandbox-state/1 rule: serve bytes only when the recorded hash
    agrees, degrade to unavailable, never to a wrong answer."""
    manifest, archive, _ = captured
    tampered = tmp_path / "bad.tar.gz"
    with gzip.open(archive, "rb") as gz, tarfile.open(fileobj=gz, mode="r") as src:
        with gzip.open(tampered, "wb") as out, tarfile.open(fileobj=out, mode="w") as dst:
            for m in src.getmembers():
                data = src.extractfile(m).read()
                if m.name == "train.py":
                    data = b"MALICIOUS\n"
                    m.size = len(data)
                dst.addfile(m, __import__("io").BytesIO(data))

    dest = tmp_path / "r"
    result = restore_snapshot(manifest, str(dest), archive_path=str(tampered))

    bad = [f for f in result["files"] if f["path"] == "train.py"]
    assert bad and bad[0]["status"] == "unavailable"
    assert "sha256 mismatch" in bad[0]["reason"]
    assert not (dest / "train.py").exists(), "a mismatching file must never be written"
    assert result["tree_matches"] is False


def test_a_missing_archive_reports_each_file_not_a_silent_gap(captured, tmp_path):
    manifest, _, _ = captured
    result = restore_snapshot(manifest, str(tmp_path / "r"), archive_path=None)
    unavailable = {f["path"] for f in result["files"] if f["status"] == "unavailable"}
    # Every file, `clean.py` included: with no git half there is no second
    # source to fall back to, and the archive is the whole record.
    assert unavailable == {"clean.py", "train.py", "config.yaml", "scripts/go.sh"}
    assert all(
        "archive unavailable" in f["reason"]
        for f in result["files"]
        if f["status"] == "unavailable"
    )
    # No second source to make up the difference: nothing is restored, and the
    # report still names every file rather than failing as one lump.
    assert result["n_restored"] == 0
    assert len(result["files"]) == 4
    assert result["tree_matches"] is False


def test_an_unreachable_remote_reports_the_git_files(legacy_captured, tmp_path):
    """Legacy manifests only — a current capture has no git entries to strand."""
    manifest, archive, _ = legacy_captured
    manifest = {**manifest, "remote": str(tmp_path / "does-not-exist.git")}
    result = restore_snapshot(manifest, str(tmp_path / "r"), archive_path=archive)
    git_files = [f for f in result["files"] if f["source"] == "git"]
    assert all(f["status"] == "unavailable" for f in git_files)
    assert all("cannot fetch" in f["reason"] for f in git_files)


# --- verify-only -------------------------------------------------------------


def test_verify_only_writes_nothing(captured, tmp_path):
    manifest, archive, _ = captured
    dest = tmp_path / "nope"
    result = restore_snapshot(manifest, str(dest), archive_path=archive, verify_only=True)
    assert result["n_unavailable"] == 0
    assert all(f["status"] == "verified" for f in result["files"])
    assert not dest.exists(), "verify-only must not create the destination"


def test_an_empty_manifest_raises(tmp_path):
    with pytest.raises(RestoreError, match="no entries"):
        restore_snapshot({"entries": []}, str(tmp_path / "r"))
