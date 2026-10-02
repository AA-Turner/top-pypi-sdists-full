"""Checksum behaviour tests for Python bindings."""

from __future__ import annotations

import os

import pytest

from snowflake_code_unit_registry import CodeUnitRegistry, ErrorCode, compute_file_checksum
from snowflake_code_unit_registry._native import ScaiError
from snowflake_code_unit_registry.types import CodeUnit

EMPTY_XXHASH3_DIGEST = "99aa06d3014798d86001c324468d497f"


# ── helpers ──────────────────────────────────────────────────────────────────


def write_file(directory: str, name: str, content: bytes) -> str:
    """Write a file inside `directory` and return its repo-relative name."""
    path = os.path.join(directory, name)
    with open(path, "wb") as f:
        f.write(content)
    return name


def make_cu_with_source(relative_path: str, cu_id: str = "cu-checksum") -> dict:
    """Return a raw dict suitable for creating a CodeUnit with a source file path."""
    return make_cu_with_files({"source": {"path": relative_path}}, cu_id=cu_id)


def make_cu_with_files(files: dict, cu_id: str = "cu-checksum") -> dict:
    """Return a minimal raw dict suitable for creating/upserting a CodeUnit."""
    return {
        "id": cu_id,
        "schemaVersion": 1,
        "isMissing": False,
        "inScope": True,
        "kind": "databaseObject",
        "objectType": "table",
        "files": files,
    }


# ── compute_file_checksum ─────────────────────────────────────────────────────


def test_compute_file_checksum_returns_32_hex_chars(registry_dir: str):
    path = os.path.join(registry_dir, "sample.sql")
    with open(path, "wb") as f:
        f.write(b"SELECT 1")
    digest = compute_file_checksum(path)
    assert len(digest) == 32
    assert all(c in "0123456789abcdef" for c in digest)


def test_compute_file_checksum_matches_known_xxhash3_vector(registry_dir: str):
    path = os.path.join(registry_dir, "empty.bin")
    with open(path, "wb") as f:
        f.write(b"")
    assert compute_file_checksum(path) == EMPTY_XXHASH3_DIGEST


def test_compute_file_checksum_missing_file_raises(registry_dir: str):
    missing = os.path.join(registry_dir, "nonexistent.sql")
    with pytest.raises(ScaiError) as exc_info:
        compute_file_checksum(missing)
    assert exc_info.value.error_code == ErrorCode.FILE_IO_ERROR
    # The message must surface the attempted path and the failing operation
    # so production diagnostics don't require a debugger to identify which
    # FFI-supplied path actually reached the filesystem.
    assert missing in str(exc_info.value)
    assert "open" in str(exc_info.value)


# ── explicit checksum helper APIs ─────────────────────────────────────────────


def test_update_checksum_refreshes_all_changed_files(registry_dir: str):
    write_file(registry_dir, "src.sql", b"src v1")
    write_file(registry_dir, "snap.sql", b"snap v1")
    registry = CodeUnitRegistry.init(registry_dir)
    cu = CodeUnit.model_validate({
        "id": "cu-checksum",
        "schemaVersion": 1,
        "isMissing": False,
        "inScope": True,
        "kind": "databaseObject",
        "objectType": "table",
        "files": {
            "source": {"path": "src.sql"},
            "snapshot": {"path": "snap.sql"},
        },
    })
    registry.create(cu)
    registry.update_checksum("cu-checksum")
    loaded1 = registry.get_by_id("cu-checksum")
    source1 = loaded1.files.source.checksum
    snapshot1 = loaded1.files.snapshot.checksum

    write_file(registry_dir, "src.sql", b"src v2")
    write_file(registry_dir, "snap.sql", b"snap v2")
    registry.update_checksum("cu-checksum")
    loaded2 = registry.get_by_id("cu-checksum")
    assert loaded2.files.source.checksum != source1
    assert loaded2.files.snapshot.checksum != snapshot1


def test_update_checksum_skips_unchanged_files(registry_dir: str):
    write_file(registry_dir, "src.sql", b"src v1")
    write_file(registry_dir, "snap.sql", b"snap v1")
    registry = CodeUnitRegistry.init(registry_dir)
    cu = CodeUnit.model_validate({
        "id": "cu-checksum-skip",
        "schemaVersion": 1,
        "isMissing": False,
        "inScope": True,
        "kind": "databaseObject",
        "objectType": "table",
        "files": {
            "source": {"path": "src.sql"},
            "snapshot": {"path": "snap.sql"},
        },
    })
    registry.create(cu)
    registry.update_checksum("cu-checksum-skip")
    loaded1 = registry.get_by_id("cu-checksum-skip")
    source1 = loaded1.files.source.checksum
    snapshot1 = loaded1.files.snapshot.checksum

    write_file(registry_dir, "src.sql", b"src v2")
    registry.update_checksum("cu-checksum-skip")
    loaded2 = registry.get_by_id("cu-checksum-skip")
    assert loaded2.files.source.checksum != source1
    assert loaded2.files.snapshot.checksum == snapshot1


def test_validate_checksum_reports_mismatch(registry_dir: str):
    src_path = write_file(registry_dir, "evolving.sql", b"version 1")
    registry = CodeUnitRegistry.init(registry_dir)
    cu = CodeUnit.model_validate(make_cu_with_source("evolving.sql"))
    registry.create(cu)
    registry.update_checksum("cu-checksum")

    with open(os.path.join(registry_dir, src_path), "wb") as f:
        f.write(b"version 2")
    report = registry.validate_checksum("cu-checksum", checksum_mode="source")
    source = next(e for e in report.entries if e.field == "files.source")
    assert source.status == "mismatch"


def test_validate_checksum_reports_missing_file(registry_dir: str):
    src_path = write_file(registry_dir, "missing.sql", b"version 1")
    registry = CodeUnitRegistry.init(registry_dir)
    cu = CodeUnit.model_validate(make_cu_with_source("missing.sql"))
    registry.create(cu)
    registry.update_checksum("cu-checksum")

    os.remove(os.path.join(registry_dir, src_path))
    report = registry.validate_checksum("cu-checksum", checksum_mode="source")
    source = next(e for e in report.entries if e.field == "files.source")
    assert source.status == "missing_file"


# ── invalid mode ──────────────────────────────────────────────────────────────


def test_update_checksum_respects_mode(registry_dir: str):
    """update_checksum only refreshes entries selected by the mode."""
    registry = CodeUnitRegistry.init(registry_dir)
    write_file(registry_dir, "src.sql", b"src")
    write_file(registry_dir, "out.sql", b"out")
    cu = CodeUnit.model_validate(
        make_cu_with_files(
            {"source": {"path": "src.sql"}, "converted": {"path": "out.sql"}},
            cu_id="cu-checksum",
        )
    )
    registry.create(cu)

    registry.update_checksum("cu-checksum", checksum_mode="source")
    loaded = registry.get_by_id("cu-checksum")
    assert loaded.files.source.checksum is not None
    assert loaded.files.converted.checksum is None

    registry.update_checksum("cu-checksum", checksum_mode="converted")
    loaded = registry.get_by_id("cu-checksum")
    assert loaded.files.converted.checksum is not None


# ── find_sql_file_changes ─────────────────────────────────────────────────────


def test_find_sql_file_changes_empty_registry(registry_dir: str):
    registry = CodeUnitRegistry.init(registry_dir)
    result = registry.find_sql_file_changes()
    assert len(result.code_unit_changes) == 0
    assert len(result.untracked_files) == 0
    assert len(result.errors) == 0


def test_find_sql_file_changes_no_changes(registry_dir: str):
    write_file(registry_dir, "src.sql", b"SELECT 1")
    registry = CodeUnitRegistry.init(registry_dir)
    cu = CodeUnit.model_validate(make_cu_with_source("src.sql"))
    registry.create(cu)
    registry.update_checksum("cu-checksum")
    result = registry.find_sql_file_changes(checksum_mode="source")
    assert len(result.code_unit_changes) == 0


def test_find_sql_file_changes_detects_modified_source(registry_dir: str):
    write_file(registry_dir, "src.sql", b"SELECT 1")
    registry = CodeUnitRegistry.init(registry_dir)
    cu = CodeUnit.model_validate(make_cu_with_source("src.sql"))
    registry.create(cu)
    registry.update_checksum("cu-checksum")

    write_file(registry_dir, "src.sql", b"SELECT 2 -- modified")
    result = registry.find_sql_file_changes(checksum_mode="source")
    assert "cu-checksum" in result.code_unit_changes
    changes = result.code_unit_changes["cu-checksum"]
    assert len(changes) == 1
    assert changes[0].change_type == "modified"


def test_find_sql_file_changes_detects_removed_source(registry_dir: str):
    write_file(registry_dir, "src.sql", b"SELECT 1")
    registry = CodeUnitRegistry.init(registry_dir)
    cu = CodeUnit.model_validate(make_cu_with_source("src.sql"))
    registry.create(cu)
    registry.update_checksum("cu-checksum")

    os.remove(os.path.join(registry_dir, "src.sql"))
    result = registry.find_sql_file_changes(checksum_mode="source")
    assert "cu-checksum" in result.code_unit_changes
    assert result.code_unit_changes["cu-checksum"][0].change_type == "removed"


def test_find_sql_file_changes_detects_untracked_files(registry_dir: str):
    write_file(registry_dir, "tracked.sql", b"ok")
    registry = CodeUnitRegistry.init(registry_dir)
    cu = CodeUnit.model_validate(make_cu_with_source("tracked.sql"))
    registry.create(cu)
    registry.update_checksum("cu-checksum")

    source_dir = os.path.join(registry_dir, "source")
    os.makedirs(source_dir, exist_ok=True)
    with open(os.path.join(source_dir, "orphan.sql"), "wb") as f:
        f.write(b"surprise")

    result = registry.find_sql_file_changes(checksum_mode="source")
    assert len(result.code_unit_changes) == 0
    assert any("orphan.sql" in f.path for f in result.untracked_files)


def test_find_sql_file_changes_mode_source_ignores_converted(registry_dir: str):
    write_file(registry_dir, "src.sql", b"SELECT 1")
    write_file(registry_dir, "cvt.sql", b"SELECT 1 AS col")
    registry = CodeUnitRegistry.init(registry_dir)
    cu = CodeUnit.model_validate(make_cu_with_files({
        "source": {"path": "src.sql"},
        "converted": {"path": "cvt.sql"},
    }))
    registry.create(cu)
    registry.update_checksum("cu-checksum")

    write_file(registry_dir, "cvt.sql", b"modified converted!")
    result = registry.find_sql_file_changes(checksum_mode="source")
    assert len(result.code_unit_changes) == 0


def test_find_sql_file_changes_with_filter(registry_dir: str):
    write_file(registry_dir, "a.sql", b"SELECT 1")
    write_file(registry_dir, "b.sql", b"SELECT 2")
    registry = CodeUnitRegistry.init(registry_dir)

    cu_a = CodeUnit.model_validate({
        "id": "cu-a", "schemaVersion": 1, "isMissing": False, "inScope": True,
        "kind": "databaseObject", "objectType": "table",
        "source": {"name": "Alpha"},
        "files": {"source": {"path": "a.sql"}},
    })
    cu_b = CodeUnit.model_validate({
        "id": "cu-b", "schemaVersion": 1, "isMissing": False, "inScope": True,
        "kind": "databaseObject", "objectType": "table",
        "source": {"name": "Beta"},
        "files": {"source": {"path": "b.sql"}},
    })
    registry.create(cu_a)
    registry.update_checksum("cu-a")
    registry.create(cu_b)
    registry.update_checksum("cu-b")

    write_file(registry_dir, "a.sql", b"modified a")
    write_file(registry_dir, "b.sql", b"modified b")

    result = registry.find_sql_file_changes(
        checksum_mode="source", filter="source.name = 'Alpha'"
    )
    assert "cu-a" in result.code_unit_changes
    assert "cu-b" not in result.code_unit_changes


def test_find_sql_file_changes_multiple_units_mixed(registry_dir: str):
    write_file(registry_dir, "a.sql", b"file a")
    write_file(registry_dir, "b.sql", b"file b")
    write_file(registry_dir, "c.sql", b"file c")
    registry = CodeUnitRegistry.init(registry_dir)

    for cu_id, path in [("cu-a", "a.sql"), ("cu-b", "b.sql"), ("cu-c", "c.sql")]:
        cu = CodeUnit.model_validate(make_cu_with_source(path, cu_id=cu_id))
        registry.create(cu)
        registry.update_checksum(cu_id)

    write_file(registry_dir, "a.sql", b"modified a")
    os.remove(os.path.join(registry_dir, "b.sql"))

    result = registry.find_sql_file_changes(checksum_mode="source")
    assert len(result.code_unit_changes) == 2
    assert result.code_unit_changes["cu-a"][0].change_type == "modified"
    assert result.code_unit_changes["cu-b"][0].change_type == "removed"
    assert "cu-c" not in result.code_unit_changes


def test_find_sql_file_changes_errors_empty_on_success(registry_dir: str):
    write_file(registry_dir, "src.sql", b"content")
    registry = CodeUnitRegistry.init(registry_dir)
    cu = CodeUnit.model_validate(make_cu_with_source("src.sql"))
    registry.create(cu)
    registry.update_checksum("cu-checksum")
    result = registry.find_sql_file_changes()
    assert len(result.errors) == 0
