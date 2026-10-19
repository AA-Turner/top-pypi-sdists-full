"""A folder that declares itself a cache (`CACHEDIR.TAG`) is never captured.

Live 2026-10-17: five runs started outside a git repo swept cargo's
`quadread/target/` (fingerprints, rlibs, build scripts: 3,674 files, 575 MB) up
as their code. The non-git walk prunes `.venv`/`node_modules` by name and had no
rule for a cargo target folder. `target` is also an ordinary folder name, so the
rule is the folder's own declaration, not its name: the code snapshot (both
ways) and run-output capture honour it. The folder importer does not: what an
import keeps is its classifier model's call (#2937), never a pre-filter.
"""

from __future__ import annotations

import os
import subprocess

import pytest

from probe.sdk import outputs
from probe.sdk import snapshot
from probe.sdk.snapshot import capture_manifest

#: Spelled out from the spec (https://bford.info/cachedir/), not imported: the
#: test pins what cargo actually writes, not whatever the module calls it.
TAG = b"Signature: 8a477f597d28d172789f06886806bc55\n# This file is a cache directory tag created by cargo.\n"


def _git(cwd, *args):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True)


def _cargo_target(root):
    """What `cargo build --release` leaves: a tagged `target/` full of output."""
    target = root / "quadread" / "target"
    (target / "release" / ".fingerprint" / "libc-1a2b").mkdir(parents=True)
    (target / "release" / "deps").mkdir(parents=True)
    (target / "CACHEDIR.TAG").write_bytes(TAG)
    (target / "release" / ".cargo-lock").write_text("")
    (target / "release" / ".fingerprint" / "libc-1a2b" / "lib-libc").write_text("abc")
    (target / "release" / "deps" / "libdm_reader.rlib").write_bytes(b"\x00" * 64)
    return target


@pytest.fixture
def project(tmp_path):
    root = tmp_path / "dm-lab"
    (root / "quadread" / "src").mkdir(parents=True)
    (root / "train.py").write_text("print('train')\n")
    (root / "quadread" / "src" / "lib.rs").write_text("pub fn read() {}\n")
    _cargo_target(root)
    return root


def _paths(manifest):
    return {e["path"] for e in manifest["entries"]}


def test_signature_must_match(tmp_path):
    (tmp_path / "CACHEDIR.TAG").write_text("not a cache tag\n")
    assert not snapshot.is_tagged_cache_dir(str(tmp_path))
    (tmp_path / "CACHEDIR.TAG").write_bytes(TAG)
    assert snapshot.is_tagged_cache_dir(str(tmp_path))
    assert not snapshot.is_tagged_cache_dir(str(tmp_path / "missing"))


def test_non_git_snapshot_skips_a_tagged_build_folder(project):
    m = capture_manifest(str(project))
    assert _paths(m) == {"train.py", "quadread/src/lib.rs"}
    assert {"path": "quadread/target", "reason": "generated"} in m["skipped"]


def test_a_folder_named_target_without_a_tag_is_still_captured(project):
    """The rule is the declaration, not the name: an authored `target/` (labels,
    a target dataset) stays part of the run's code."""
    (project / "target").mkdir()
    (project / "target" / "labels.csv").write_text("id,y\n1,0\n")
    assert "target/labels.csv" in _paths(capture_manifest(str(project)))


def test_git_snapshot_skips_an_untracked_tagged_folder_gitignore_misses(project):
    _git(project, "init", "-q")
    _git(project, "add", "train.py", "quadread/src/lib.rs")
    _git(project, "-c", "user.email=t@example.com", "-c", "user.name=t", "commit", "-q", "-m", "init")
    m = capture_manifest(str(project))
    assert _paths(m) == {"train.py", "quadread/src/lib.rs"}
    reported = [s for s in m["skipped"] if s["path"] == "quadread/target"]
    assert reported == [{"path": "quadread/target", "reason": "generated"}], "one report per folder"


def test_git_snapshot_skips_a_tagged_folder_even_when_committed(project):
    """The tag wins over git: a committed cache folder is still a cache, and the
    server's sweep of older SDKs' captures cannot see tracked status either."""
    _git(project, "init", "-q")
    _git(project, "add", "-A")
    _git(project, "-c", "user.email=t@example.com", "-c", "user.name=t", "commit", "-q", "-m", "init")
    assert _paths(capture_manifest(str(project))) == {"train.py", "quadread/src/lib.rs"}


@pytest.mark.parametrize("git", [False, True])
def test_an_explicit_include_still_captures_a_tagged_folder(project, git):
    """`include=` is the one way in, and the manifest marks those entries
    `included` so the server sweep spares them too."""
    if git:
        _git(project, "init", "-q")
    m = capture_manifest(str(project), include=["quadread/target"])
    lock = [e for e in m["entries"] if e["path"] == "quadread/target/release/.cargo-lock"]
    assert lock and lock[0].get("included") is True


def test_run_outputs_never_walk_a_tagged_folder(project):
    found, cut_short = outputs._walk(str(project), set(), 1000)
    assert not cut_short
    assert not any(p.startswith("quadread/target/") for p in found)
    assert "train.py" in found


def test_unreadable_tag_counts_as_no_tag(tmp_path):
    if os.geteuid() == 0:
        pytest.skip("root reads any file")
    (tmp_path / "CACHEDIR.TAG").write_bytes(TAG)
    (tmp_path / "CACHEDIR.TAG").chmod(0)
    try:
        assert not snapshot.is_tagged_cache_dir(str(tmp_path))
    finally:
        (tmp_path / "CACHEDIR.TAG").chmod(0o644)
