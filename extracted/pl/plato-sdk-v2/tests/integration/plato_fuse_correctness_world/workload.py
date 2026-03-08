#!/usr/bin/env python3
"""Filesystem correctness workload — runs on the agent or world VM.

Exercises every FUSE operation and returns structured JSON with pass/fail
results so the world can assert correctness without parsing log output.
"""

from __future__ import annotations

import json
import os
import pathlib
import sys


def check_lazy_load(root: pathlib.Path, expected_files: list[str]) -> dict:
    """Verify seed files are stat-able and readable."""
    results: dict[str, object] = {"pass": True, "errors": []}
    for relpath in expected_files:
        p = root / relpath
        if not p.exists():
            results["errors"].append(f"missing: {relpath}")
            results["pass"] = False
            continue
        st = p.stat()
        if st.st_size == 0:
            results["errors"].append(f"zero-size: {relpath}")
            results["pass"] = False
            continue
        data = p.read_bytes()
        if len(data) != st.st_size:
            results["errors"].append(f"size mismatch: {relpath} stat={st.st_size} read={len(data)}")
            results["pass"] = False
    results["files_checked"] = len(expected_files)
    return results


def check_file_operations(root: pathlib.Path) -> dict:
    """Create, write, read, rename, unlink, mkdir, rmdir, symlink, hardlink."""
    errors: list[str] = []

    # --- create + write + read ---
    f = root / "ops" / "created.txt"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text("hello world")
    if f.read_text() != "hello world":
        errors.append("create+read failed")

    # --- modify ---
    f.write_text("modified content")
    if f.read_text() != "modified content":
        errors.append("modify+read failed")

    # --- same-handle read-after-write on materialized manifest file ---
    same_handle = root / "store" / "pkg_002" / "file_0002.json"
    same_handle_payload = b"same-handle"
    fd = os.open(str(same_handle), os.O_RDWR)
    try:
        os.pwrite(fd, same_handle_payload, 0)
        if os.pread(fd, len(same_handle_payload), 0) != same_handle_payload:
            errors.append("same-handle read-after-write failed")
    finally:
        os.close(fd)

    # --- rename ---
    renamed = root / "ops" / "renamed.txt"
    f.rename(renamed)
    if not renamed.exists():
        errors.append("rename: target missing")
    if f.exists():
        errors.append("rename: source still exists")
    if renamed.read_text() != "modified content":
        errors.append("rename: content changed")

    # --- hardlink ---
    hardlinked = root / "ops" / "hardlinked.txt"
    try:
        os.link(str(renamed), str(hardlinked))
        renamed_stat = renamed.stat()
        hardlinked_stat = hardlinked.stat()
        if hardlinked.read_text() != "modified content":
            errors.append("hardlink: content mismatch")
        if hardlinked_stat.st_ino != renamed_stat.st_ino:
            errors.append("hardlink: inode mismatch")
        if renamed_stat.st_nlink < 2 or hardlinked_stat.st_nlink < 2:
            errors.append("hardlink: nlink not incremented")
        hardlinked.write_text("shared via hardlink")
        if renamed.read_text() != "shared via hardlink":
            errors.append("hardlink: writes did not propagate")
        moved_hardlink = root / "ops" / "hardlinked-renamed.txt"
        hardlinked.rename(moved_hardlink)
        moved_stat = moved_hardlink.stat()
        renamed_stat = renamed.stat()
        if moved_stat.st_ino != renamed_stat.st_ino:
            errors.append("hardlink rename: inode mismatch")
        if moved_stat.st_nlink < 2 or renamed_stat.st_nlink < 2:
            errors.append("hardlink rename: nlink dropped")
        moved_hardlink.write_text("shared after hardlink rename")
        if renamed.read_text() != "shared after hardlink rename":
            errors.append("hardlink rename: writes did not propagate")
        hardlinked = moved_hardlink
    except OSError as e:
        errors.append(f"hardlink failed: {e}")

    # --- symlink ---
    symlinked = root / "ops" / "symlinked.txt"
    symlinked.symlink_to("renamed.txt")
    if not symlinked.is_symlink():
        errors.append("symlink: not a symlink")
    if symlinked.read_text() != "shared after hardlink rename":
        errors.append("symlink: content mismatch via readlink")

    # --- chmod + truncate ---
    renamed.chmod(0o600)
    if renamed.stat().st_mode & 0o777 != 0o600:
        errors.append("chmod: mode mismatch")
    renamed.write_text("truncate me")
    with renamed.open("r+b") as fh:
        fh.truncate(4)
    if renamed.read_text() != "trun":
        errors.append("truncate: content mismatch")

    # --- unlink ---
    hardlinked.unlink()
    if hardlinked.exists():
        errors.append("unlink: file still exists")
    if renamed.read_text() != "trun":
        errors.append("unlink: surviving hardlink lost content")
    if renamed.stat().st_nlink != 1:
        errors.append("unlink: nlink not decremented")

    # --- mkdir + rmdir ---
    d = root / "ops" / "subdir" / "nested"
    d.mkdir(parents=True, exist_ok=True)
    if not d.is_dir():
        errors.append("mkdir: dir not created")
    d.rmdir()
    if d.exists():
        errors.append("rmdir: dir still exists")

    # --- postgres-style directory permissions ---
    pgdata = root / ".runtime" / "postgres" / "data"
    pgdata.mkdir(parents=True, mode=0o700, exist_ok=False)
    if pgdata.stat().st_mode & 0o777 != 0o700:
        errors.append(f"postgres mkdir 0700: mode mismatch {(pgdata.stat().st_mode & 0o777):o}")
    pgdata.chmod(0o750)
    if pgdata.stat().st_mode & 0o777 != 0o750:
        errors.append(f"postgres chmod 0750: mode mismatch {(pgdata.stat().st_mode & 0o777):o}")
    (pgdata / "PG_VERSION").write_text("16")
    if (pgdata / "PG_VERSION").read_text() != "16":
        errors.append("postgres dir write/read failed")

    # --- large-ish tree create + rm -rf ---
    tree_root = root / "ops" / "tree"
    for i in range(50):
        p = tree_root / f"pkg_{i:03d}" / f"file_{i}.txt"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"content-{i}")
    import shutil

    shutil.rmtree(tree_root)
    if tree_root.exists():
        errors.append("rmtree: tree still exists")

    return {"pass": len(errors) == 0, "errors": errors}


def check_cross_vm_visibility(root: pathlib.Path) -> dict:
    """Write a sentinel file so the world VM can verify it appeared."""
    sentinel = root / "cross_vm_sentinel.txt"
    sentinel.write_text("written-by-agent")
    return {"pass": sentinel.exists(), "sentinel_path": str(sentinel)}


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("root", help="Mount root to test against")
    parser.add_argument("--check", required=True, choices=["lazy_load", "file_ops", "cross_vm"])
    parser.add_argument("--expected-files", help="Comma-separated relpaths for lazy_load check")
    args = parser.parse_args()

    root = pathlib.Path(args.root).resolve()
    assert root.exists(), f"Root does not exist: {root}"

    if args.check == "lazy_load":
        expected = args.expected_files.split(",") if args.expected_files else []
        result = check_lazy_load(root, expected)
    elif args.check == "file_ops":
        result = check_file_operations(root)
    elif args.check == "cross_vm":
        result = check_cross_vm_visibility(root)
    else:
        result = {"pass": False, "errors": [f"unknown check: {args.check}"]}

    print(json.dumps(result))
    sys.exit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
