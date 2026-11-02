"""Verify tracked benchmark fixture bytes against an exact Git commit."""

import os
import re
import stat
import subprocess
from pathlib import Path


def _run_git(root: Path, arguments: list[str]) -> bytes:
    result = subprocess.run(
        ["git", "-C", os.fspath(root), *arguments],
        check=True,
        capture_output=True,
        shell=False,
    )
    return result.stdout


def _parse_tree_record(record: bytes, object_id_length: int) -> tuple[bytes, bytes]:
    fixture_prefix = b"tests/fixtures/reviewing-agent-benchmark"
    if not record or b"\t" not in record:
        raise ValueError(f"Malformed fixture tree record: {record!r}")
    metadata, path_bytes = record.split(b"\t", 1)
    fields = metadata.split(b" ")
    if len(fields) != 3:
        raise ValueError(f"Malformed fixture tree metadata: {metadata!r}")
    mode, entry_type, blob_id = fields
    if (
        mode not in {b"100644", b"100755"}
        or entry_type != b"blob"
        or len(blob_id) != object_id_length
        or re.fullmatch(rb"[0-9a-f]+", blob_id) is None
    ):
        raise ValueError(f"Unsupported or malformed fixture tree entry for {os.fsdecode(path_bytes)!r}: {metadata!r}")
    path_parts = path_bytes.split(b"/")
    if not path_bytes.startswith(fixture_prefix + b"/") or any(part in {b"", b".", b".."} for part in path_parts):
        raise ValueError(f"Malformed fixture path in tree inventory: {path_bytes!r}")
    return path_bytes, blob_id


def _parse_fixture_inventory(tree_output: bytes, commit: str) -> dict[bytes, bytes]:
    if not isinstance(tree_output, bytes):
        raise ValueError("Git returned a malformed fixture tree inventory")
    if not tree_output:
        raise ValueError("Git fixture tree inventory is empty")
    if not tree_output.endswith(b"\0"):
        raise ValueError("Git fixture tree inventory is truncated")

    inventory: dict[bytes, bytes] = {}
    for record in tree_output[:-1].split(b"\0"):
        path_bytes, blob_id = _parse_tree_record(record, len(commit))
        if path_bytes in inventory:
            raise ValueError(f"Duplicate fixture path in tree inventory: {os.fsdecode(path_bytes)!r}")
        inventory[path_bytes] = blob_id

    return inventory


def _verify_fixture_file(root: Path, path_bytes: bytes, expected_blob: bytes, object_id_length: int) -> None:
    relative_path = os.fsdecode(path_bytes)
    fixture_path = root / relative_path
    try:
        file_stat = fixture_path.lstat()
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Tracked fixture is missing: {relative_path}") from exc
    if not stat.S_ISREG(file_stat.st_mode):
        raise ValueError(f"Tracked fixture is not a regular file: {relative_path}")
    try:
        with fixture_path.open("rb") as fixture_file:
            fixture_file.read(1)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Tracked fixture is missing: {relative_path}") from exc
    except OSError as exc:
        raise ValueError(f"Tracked fixture is not readable: {relative_path}: {exc}") from exc

    attribute_output = _run_git(root, ["check-attr", "-z", "text", "--", relative_path])
    if not isinstance(attribute_output, bytes):
        raise ValueError(f"Malformed text attribute result for {relative_path}: {attribute_output!r}")
    attribute_fields = attribute_output.split(b"\0")
    if (
        len(attribute_fields) != 4
        or attribute_fields[-1] != b""
        or attribute_fields[0] != path_bytes
        or attribute_fields[1] != b"text"
    ):
        raise ValueError(f"Malformed or ambiguous text attribute result for {relative_path}: {attribute_output!r}")
    attribute_value = attribute_fields[2]
    if attribute_value != b"unset":
        raise ValueError(f"Expected text=unset for {relative_path}, observed {os.fsdecode(attribute_value)!r}")

    hash_output = _run_git(root, ["hash-object", "--no-filters", "--", relative_path])
    actual_blob = hash_output[:-1] if isinstance(hash_output, bytes) and hash_output.endswith(b"\n") else b""
    if len(actual_blob) != object_id_length or re.fullmatch(rb"[0-9a-f]+", actual_blob) is None:
        raise ValueError(f"Malformed raw hash result for {relative_path}: {hash_output!r}")
    if actual_blob != expected_blob:
        raise ValueError(
            f"Raw fixture blob mismatch for {relative_path}: expected "
            f"{os.fsdecode(expected_blob)}, actual {os.fsdecode(actual_blob)}"
        )


def verify_fixture_bytes(commit: str, root: Path) -> int:
    """Verify raw worktree bytes and effective text attributes for tracked fixtures."""
    if re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", commit) is None:
        raise ValueError(f"commit must be a full lowercase SHA-1 or SHA-256 object ID: {commit!r}")

    root = Path(root)
    if not root.exists():
        raise FileNotFoundError(f"Repository root does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Repository root is not a directory: {root}")

    top_level_output = _run_git(root, ["rev-parse", "--show-toplevel"])
    if not isinstance(top_level_output, bytes) or not top_level_output.endswith(b"\n"):
        raise ValueError(f"Git returned a malformed repository top-level for {root}")
    observed_root = Path(os.fsdecode(top_level_output[:-1]))
    if observed_root.resolve() != root.resolve():
        raise ValueError(f"root must be the repository top-level: expected {observed_root}, observed {root}")

    head_output = _run_git(root, ["rev-parse", "HEAD"])
    observed_commit = head_output[:-1] if head_output.endswith(b"\n") else head_output
    if observed_commit != commit.encode("ascii"):
        raise ValueError(
            f"repository HEAD does not match requested commit: expected {commit}, observed {observed_commit!r}"
        )

    tree_output = _run_git(
        root,
        ["ls-tree", "-r", "-z", "--full-tree", commit, "--", "tests/fixtures/reviewing-agent-benchmark"],
    )
    inventory = _parse_fixture_inventory(tree_output, commit)
    for path_bytes, expected_blob in inventory.items():
        _verify_fixture_file(root, path_bytes, expected_blob, len(commit))
    return len(inventory)
