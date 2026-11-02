"""Tests for file-backed trusted reconciliation repository."""

from __future__ import annotations

from pathlib import Path

import pytest

import agentic_devtools.cli.ci.reconciliation.repository as repository_module
from agentic_devtools.cli.ci.reconciliation.repository import (
    FileBackedReconciliationRepository,
    ManifestConflictError,
    ManifestOverflowError,
    MissingArchiveShardError,
    ReconciliationManifest,
    normalize_immutable_entry,
)


def test_load_missing_manifest_returns_empty(tmp_path: Path) -> None:
    repo = FileBackedReconciliationRepository(tmp_path, repo="owner/repo")
    loaded = repo.load()
    assert loaded.repo == "owner/repo"
    assert loaded.revision == 0


def test_save_requires_matching_revision(tmp_path: Path) -> None:
    repo = FileBackedReconciliationRepository(tmp_path, repo="owner/repo")
    saved = repo.save(ReconciliationManifest(repo="owner/repo", revision=0), expected_revision=0)
    with pytest.raises(ManifestConflictError):
        repo.save(saved, expected_revision=0)


def test_save_rejects_oversized_manifest(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(repository_module, "MAX_STATE_SIZE_BYTES", 128)
    repo = FileBackedReconciliationRepository(tmp_path, repo="owner/repo")
    manifest = ReconciliationManifest(repo="owner/repo", revision=0, inventory={"k": {"v": "x" * 200}})
    with pytest.raises(ManifestOverflowError):
        repo.save(manifest, expected_revision=0)


def test_append_immutable_entry_rejects_unknown_channel(tmp_path: Path) -> None:
    repo = FileBackedReconciliationRepository(tmp_path, repo="owner/repo")
    manifest = ReconciliationManifest(repo="owner/repo", revision=0)
    with pytest.raises(ValueError, match="unsupported channel"):
        repo.append_immutable_entry(manifest=manifest, record_id="r1", channel="unknown", entry={})


def test_append_immutable_entry_rolls_over_oldest_entries(tmp_path: Path) -> None:
    repo = FileBackedReconciliationRepository(tmp_path, repo="owner/repo")
    manifest = ReconciliationManifest(repo="owner/repo", revision=0, ledgers={"r1": {"observations": []}})
    for index in range(40):
        manifest = repo.append_immutable_entry(
            manifest=manifest,
            record_id="r1",
            channel="observations",
            entry={"id": index, "reason": f"e-{index}"},
        )
    assert len(manifest.ledgers["r1"]["observations"]) <= 32
    assert manifest.archive_pointers["r1"]


def test_append_immutable_entry_rejects_oversized_normalized_entry(tmp_path: Path) -> None:
    repo = FileBackedReconciliationRepository(tmp_path, repo="owner/repo")
    manifest = ReconciliationManifest(repo="owner/repo", revision=0)
    entry = {"structured": [str(i) for i in range(4000)]}
    with pytest.raises(ManifestOverflowError):
        repo.append_immutable_entry(manifest=manifest, record_id="r1", channel="observations", entry=entry)


def test_assert_archive_integrity_fails_for_missing_shard(tmp_path: Path) -> None:
    repo = FileBackedReconciliationRepository(tmp_path, repo="owner/repo")
    manifest = ReconciliationManifest(
        repo="owner/repo",
        revision=0,
        archive_pointers={"r1": [{"shard_id": "missing", "entry_count": 1, "content_sha256": "x", "size_bytes": 5}]},
    )
    with pytest.raises(MissingArchiveShardError):
        repo.assert_archive_integrity(manifest)


def test_normalize_immutable_entry_adds_truncation_metadata() -> None:
    normalized = normalize_immutable_entry({"reason": "x" * 5000})
    assert "_truncation" in normalized


def test_append_immutable_entry_rolls_over_when_manifest_nears_capacity(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(repository_module, "MAX_STATE_SIZE_BYTES", 1600)
    repo = FileBackedReconciliationRepository(tmp_path, repo="owner/repo")
    manifest = ReconciliationManifest(
        repo="owner/repo",
        revision=0,
        ledgers={"r1": {"observations": [{"reason": "x" * 200} for _ in range(5)]}},
    )
    updated = repo.append_immutable_entry(
        manifest=manifest,
        record_id="r1",
        channel="observations",
        entry={"reason": "x" * 200},
    )
    assert updated.archive_pointers["r1"]


def test_append_immutable_entry_raises_when_projection_cannot_fit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(repository_module, "MAX_STATE_SIZE_BYTES", 250)
    repo = FileBackedReconciliationRepository(tmp_path, repo="owner/repo")
    manifest = ReconciliationManifest(
        repo="owner/repo",
        revision=0,
        inventory={"forced": {"details": "x" * 500}},
        ledgers={"r1": {"observations": [{"reason": "x" * 100}]}},
    )
    with pytest.raises(ManifestOverflowError, match="cannot fit"):
        repo.append_immutable_entry(
            manifest=manifest,
            record_id="r1",
            channel="observations",
            entry={"reason": "y" * 100},
        )


def test_assert_archive_integrity_accepts_existing_shards(tmp_path: Path) -> None:
    repo = FileBackedReconciliationRepository(tmp_path, repo="owner/repo")
    pointer_a = repo._write_archive_shard(record_id="r1", entries=[{"reason": "a"}])  # noqa: SLF001
    pointer_b = repo._write_archive_shard(record_id="r2", entries=[{"reason": "b"}])  # noqa: SLF001
    manifest = ReconciliationManifest(
        repo="owner/repo",
        revision=0,
        archive_pointers={"r1": [pointer_a], "r2": [pointer_b]},
    )
    repo.assert_archive_integrity(manifest)
    repo.assert_archive_integrity(ReconciliationManifest(repo="owner/repo", revision=0))


def test_load_rejects_corrupted_archive_shard(tmp_path: Path) -> None:
    repo = FileBackedReconciliationRepository(tmp_path, repo="owner/repo")
    pointer = repo._write_archive_shard(record_id="r1", entries=[{"reason": "a"}])  # noqa: SLF001
    pointer["content_sha256"] = "0" * 64
    manifest = ReconciliationManifest(
        repo="owner/repo",
        revision=0,
        archive_pointers={"r1": [pointer]},
    )
    repo._manifest_path.parent.mkdir(parents=True, exist_ok=True)  # noqa: SLF001
    repo._manifest_path.write_text(  # noqa: SLF001
        repository_module._serialize_manifest(manifest),
        encoding="utf-8",
    )

    with pytest.raises(MissingArchiveShardError, match="digest mismatch"):
        repo.load()


def test_archive_integrity_rejects_invalid_pointer_and_payloads(tmp_path: Path) -> None:
    repo = FileBackedReconciliationRepository(tmp_path, repo="owner/repo")
    with pytest.raises(MissingArchiveShardError, match="invalid archive shard pointer"):
        repo.assert_archive_integrity(
            ReconciliationManifest(
                repo="owner/repo",
                revision=0,
                archive_pointers={"r1": [None]},  # type: ignore[list-item]
            )
        )
    with pytest.raises(MissingArchiveShardError, match="missing archive shard"):
        repo.assert_archive_integrity(
            ReconciliationManifest(
                repo="owner/repo",
                revision=0,
                archive_pointers={
                    "r1": [
                        {
                            "shard_id": "0" * 24,
                            "entry_count": 1,
                            "content_sha256": "0" * 64,
                            "size_bytes": 2,
                        }
                    ],
                },
            )
        )

    pointer = repo._write_archive_shard(record_id="r1", entries=[{"reason": "a"}])  # noqa: SLF001
    with pytest.raises(MissingArchiveShardError, match="size mismatch"):
        repo.assert_archive_integrity(
            ReconciliationManifest(
                repo="owner/repo",
                revision=0,
                archive_pointers={"r1": [{**pointer, "size_bytes": pointer["size_bytes"] + 1}]},
            )
        )
    with pytest.raises(MissingArchiveShardError, match="entry-count mismatch"):
        repo.assert_archive_integrity(
            ReconciliationManifest(
                repo="owner/repo",
                revision=0,
                archive_pointers={"r1": [{**pointer, "entry_count": 2}]},
            )
        )

    shard_path = tmp_path / "archive" / f"{pointer['shard_id']}.json"
    payload = b"not-json"
    shard_path.write_bytes(payload)
    invalid_pointer = {
        **pointer,
        "size_bytes": len(payload),
        "content_sha256": repository_module.sha256(payload).hexdigest(),
    }
    with pytest.raises(MissingArchiveShardError, match="invalid archive shard"):
        repo.assert_archive_integrity(
            ReconciliationManifest(repo="owner/repo", revision=0, archive_pointers={"r1": [invalid_pointer]})
        )


def test_archive_shard_size_cap_and_idempotent_write(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo = FileBackedReconciliationRepository(tmp_path, repo="owner/repo")
    pointer = repo._write_archive_shard(record_id="r1", entries=[{"reason": "ok"}])  # noqa: SLF001
    second_pointer = repo._write_archive_shard(record_id="r1", entries=[{"reason": "ok"}])  # noqa: SLF001
    assert pointer["shard_id"] == second_pointer["shard_id"]

    monkeypatch.setattr(repository_module, "_SHARD_MAX_BYTES", 20)
    with pytest.raises(ManifestOverflowError, match="archive shard exceeds"):
        repo._write_archive_shard(record_id="r1", entries=[{"reason": "x" * 100}])  # noqa: SLF001
