"""The dedup alias lifecycle past convergence: re-save, background sync, restore.

A row becomes a dedup ALIAS (``duplicate_of_file_id`` = a live canonical root)
when a save converges on content another file already holds
(``test_managed_write_dedup.py``). These tests pin what happens NEXT, and the
two other writers that can land on the same ``cld_files_dedup_canonical``
collision:

  * C2 — an alias re-saved with DIFFERENT bytes must drop its link (the bytes
    are no longer equivalent), and re-converge through the same path when the
    new bytes match a third file.
  * C3 — ``track_write[_async]`` (FileManager's background sync) and
    ``VersionManager.restore_version[_async]`` must converge the same way,
    never swallow the collision, and still propagate an unrelated DB error.

Everything the SUT owns runs for real: ``SyncEngine``, ``VersionManager``,
``DatabaseClient`` and the dedup lookup, over the captured unique indexes in
``_files_db_double`` (S3, IAM and the version recorder are the only doubles).
"""

from __future__ import annotations

import asyncio
import hashlib
from types import SimpleNamespace
from typing import Any

import pytest
from matrx_files.cloud_sync.versioning import VersionManager

from _files_db_double import FilesDB, UniqueViolation, build_engine

USER_ID = "user-1"
PERSONAL_ORG = "org-personal-0001"
FILE_PATH = "docs/q1.pdf"
AT_PATH_URI = "s3://test-bucket/user-1/at-path"
CANONICAL_URI = "s3://test-bucket/user-1/canonical-existing"
THIRD_URI = "s3://test-bucket/user-1/third"
V1_URI = "s3://test-bucket/.versions/at-path/v1/q1.pdf"


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@pytest.fixture
def files_db():
    db = FilesDB()
    db.org_members.add((USER_ID, PERSONAL_ORG))
    with db.bound():
        yield db


def _seed_root(db: FilesDB, content: bytes, path: str, uri: str) -> dict[str, Any]:
    return db.seed_file(
        created_by=USER_ID,
        organization_id=PERSONAL_ORG,
        file_path=path,
        checksum=_sha(content),
        storage_uri=uri,
        current_version=3,
    )


def _seed_alias(db: FilesDB, engine, shared: bytes) -> tuple[dict[str, Any], dict[str, Any]]:
    """The state a converged save leaves: a canonical root holding ``shared`` at
    another path, and the row at FILE_PATH holding the same bytes as its alias."""
    canonical = _seed_root(db, shared, "docs/already_here.pdf", CANONICAL_URI)
    alias = db.seed_file(
        created_by=USER_ID,
        organization_id=PERSONAL_ORG,
        file_path=FILE_PATH,
        checksum=_sha(shared),
        storage_uri=AT_PATH_URI,
        current_version=4,
        duplicate_of_file_id=canonical["id"],
    )
    engine._router.objects.update({AT_PATH_URI: shared, CANONICAL_URI: shared})
    for level in ("read", "write"):
        engine.permissions.allowed.add((USER_ID, alias["id"], level))
    return alias, canonical


async def _resave(engine, writer: str, row_id: str, content: bytes) -> None:
    if writer == "managed_write_async":
        await engine.managed_write_async(FILE_PATH, content)
    else:
        await engine.replace_file_async(row_id, content, user_id=USER_ID)


# ---------------------------------------------------------------------------
# C2 — re-saving an alias
# ---------------------------------------------------------------------------


# Break: the checksum changes but ``duplicate_of_file_id`` is left pointing at a
# canonical whose bytes the row no longer holds (``update_file_async`` drops
# None, so the link can only be cleared explicitly).
@pytest.mark.parametrize("writer", ["managed_write_async", "replace_file_async"])
async def test_resaving_an_alias_with_new_unique_bytes_clears_its_link(files_db, writer):
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)
    alias, canonical = _seed_alias(files_db, engine, b"bytes both rows held")
    new_bytes = b"an edit nobody else holds"

    await _resave(engine, writer, alias["id"], new_bytes)

    row = files_db.files.rows[alias["id"]]
    assert row["checksum"] == _sha(new_bytes)
    assert row["duplicate_of_file_id"] is None, (
        f"stale alias link: {alias['id']} holds new bytes but still points at "
        f"canonical {row['duplicate_of_file_id']}"
    )
    assert await engine.managed_read_async(FILE_PATH) == new_bytes
    untouched = files_db.files.rows[canonical["id"]]
    assert (untouched["checksum"], untouched["duplicate_of_file_id"]) == (
        _sha(b"bytes both rows held"),
        None,
    )
    # The row is a canonical root again: a later upload of the same bytes dedups onto it.
    reupload = await engine.managed_write_async("docs/later.pdf", new_bytes)
    assert reupload.file_id == alias["id"]


# Break: a re-save matching a THIRD file keeps the old link (no violation fires
# while the row is still an alias, so nothing re-converges).
@pytest.mark.parametrize("writer", ["managed_write_async", "replace_file_async"])
async def test_resaving_an_alias_with_a_third_files_bytes_converges_on_that_file(files_db, writer):
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)
    alias, canonical = _seed_alias(files_db, engine, b"bytes both rows held")
    third_bytes = b"bytes a third file already holds"
    third = _seed_root(files_db, third_bytes, "docs/third.pdf", THIRD_URI)
    engine._router.objects[THIRD_URI] = third_bytes

    await _resave(engine, writer, alias["id"], third_bytes)

    row = files_db.files.rows[alias["id"]]
    assert row["checksum"] == _sha(third_bytes)
    assert row["duplicate_of_file_id"] == third["id"], (
        f"alias {alias['id']} now holds the third file's bytes but links to "
        f"{row['duplicate_of_file_id']} (old canonical {canonical['id']})"
    )
    assert engine._router.objects[AT_PATH_URI] == third_bytes
    assert files_db.files.rows[third["id"]]["duplicate_of_file_id"] is None


# Break (sync twin): ``managed_write`` keeps the stale link.
@pytest.mark.parametrize("case", ["unique", "third-file"])
def test_sync_resave_of_an_alias_drops_or_moves_its_link(files_db, case):
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)
    alias, _ = _seed_alias(files_db, engine, b"bytes both rows held")
    if case == "unique":
        new_bytes, expected_link = b"an edit nobody else holds", None
    else:
        new_bytes = b"bytes a third file already holds"
        expected_link = _seed_root(files_db, new_bytes, "docs/third.pdf", THIRD_URI)["id"]

    engine.managed_write(FILE_PATH, new_bytes)

    row = files_db.files.rows[alias["id"]]
    assert (row["checksum"], row["duplicate_of_file_id"]) == (_sha(new_bytes), expected_link)


# ---------------------------------------------------------------------------
# C3 — background sync (track_write) and version restore
# ---------------------------------------------------------------------------


async def _track_write(engine, mode: str, content: bytes) -> None:
    if mode == "async":
        await engine.track_write_async(FILE_PATH, content)
    else:
        await asyncio.to_thread(engine.track_write, FILE_PATH, content)


# Break (production defect): the UPDATE hits the dedup-canonical 23505, the
# broad except logs a warning and the background save is silently lost.
@pytest.mark.parametrize("mode", ["async", "sync"])
async def test_track_write_over_a_path_converges_when_bytes_match_another_canonical(files_db, mode):
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)
    at_path = files_db.seed_file(
        created_by=USER_ID,
        organization_id=PERSONAL_ORG,
        file_path=FILE_PATH,
        checksum=_sha(b"prev"),
        storage_uri=AT_PATH_URI,
        current_version=3,
    )
    content = b"bytes another file already holds"
    canonical = _seed_root(files_db, content, "docs/already_here.pdf", CANONICAL_URI)

    await _track_write(engine, mode, content)

    row = files_db.files.rows[at_path["id"]]
    assert (row["checksum"], row["current_version"]) == (_sha(content), 4), (
        f"background save over {FILE_PATH} was lost: row still holds checksum {row['checksum']}"
    )
    assert row["duplicate_of_file_id"] == canonical["id"]
    assert engine._router.objects[row["storage_uri"]] == content
    assert engine.versions.recorded == [(at_path["id"], _sha(content))]


# Break: a first background sync of a path whose bytes another file holds is
# lost (org never stamped → NOT NULL on the live table; or the collision is
# swallowed), or the path is dropped instead of kept as an alias.
@pytest.mark.parametrize("mode", ["async", "sync"])
async def test_track_write_of_a_new_path_keeps_the_path_as_an_alias_of_the_content_match(files_db, mode):
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)
    content = b"bytes another file already holds"
    canonical = _seed_root(files_db, content, "docs/already_here.pdf", CANONICAL_URI)

    await _track_write(engine, mode, content)

    rows = [r for r in files_db.live_files() if r["file_path"] == FILE_PATH]
    assert len(rows) == 1, f"background save of new path {FILE_PATH} was lost"
    row = rows[0]
    assert (row["organization_id"], row["checksum"]) == (PERSONAL_ORG, _sha(content))
    assert row["duplicate_of_file_id"] == canonical["id"]
    assert engine.versions.recorded == [(row["id"], _sha(content))]


# Break: a broad except swallows every failure, not just the recoverable one.
@pytest.mark.parametrize("branch", ["existing-path", "new-path"])
@pytest.mark.parametrize("mode", ["async", "sync"])
async def test_track_write_propagates_an_unrelated_database_error(files_db, mode, branch):
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)
    if branch == "existing-path":
        files_db.seed_file(
            created_by=USER_ID,
            organization_id=PERSONAL_ORG,
            file_path=FILE_PATH,
            checksum=_sha(b"prev"),
            storage_uri=AT_PATH_URI,
        )

    def connection_reset(*_: Any) -> None:
        raise ConnectionResetError("server closed the connection unexpectedly")

    files_db.files.before_update.append(connection_reset)
    files_db.files.before_create.append(connection_reset)

    with pytest.raises(ConnectionResetError, match="closed the connection"):
        await _track_write(engine, mode, b"some new bytes")


def _versions(engine) -> VersionManager:
    config = SimpleNamespace(
        storage_backend="s3",
        resolve_s3_bucket=lambda: "test-bucket",
        version_storage_prefix=".versions",
    )
    return VersionManager(engine._db, engine._router, config)


def _seed_restorable(db: FilesDB, engine, old: bytes, current: bytes) -> dict[str, Any]:
    row = db.seed_file(
        created_by=USER_ID,
        organization_id=PERSONAL_ORG,
        file_path=FILE_PATH,
        checksum=_sha(current),
        storage_uri=AT_PATH_URI,
        current_version=2,
    )
    db.file_versions.create_sync(
        file_id=row["id"],
        version_number=1,
        storage_uri=V1_URI,
        size_bytes=len(old),
        checksum=_sha(old),
        created_by=USER_ID,
    )
    engine._router.objects.update({AT_PATH_URI: current, V1_URI: old})
    return row


async def _restore(vm: VersionManager, mode: str, file_id: str) -> Any:
    if mode == "async":
        return await vm.restore_version_async(file_id, 1, user_id=USER_ID)
    return await asyncio.to_thread(vm.restore_version, file_id, 1, USER_ID)


# Break: restoring v1 — whose bytes another live canonical now holds — raises a
# raw 23505 (sync) or logs "inconsistency recoverable" and leaves the row's
# checksum describing bytes it no longer holds (async).
@pytest.mark.parametrize("mode", ["async", "sync"])
async def test_restoring_a_version_whose_bytes_another_canonical_holds_converges_on_it(files_db, mode):
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)
    old = b"version one bytes"
    row = _seed_restorable(files_db, engine, old=old, current=b"version two bytes")
    canonical = _seed_root(files_db, old, "docs/already_here.pdf", CANONICAL_URI)

    try:
        await _restore(_versions(engine), mode, row["id"])
    except Exception as exc:
        pytest.fail(f"restore of {row['id']} v1 was lost: {exc}")

    restored = files_db.files.rows[row["id"]]
    assert restored["checksum"] == _sha(old), (
        f"restore left checksum {restored['checksum']} on a row now holding v1 bytes"
    )
    assert restored["duplicate_of_file_id"] == canonical["id"]
    assert engine._router.objects[AT_PATH_URI] == old


# Break: the restore's metadata update catches every exception.
@pytest.mark.parametrize("mode", ["async", "sync"])
async def test_restore_propagates_an_unrelated_database_error(files_db, mode):
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)
    row = _seed_restorable(files_db, engine, old=b"version one bytes", current=b"version two bytes")

    def connection_reset(*_: Any) -> None:
        raise ConnectionResetError("server closed the connection unexpectedly")

    files_db.files.before_update.append(connection_reset)

    with pytest.raises(ConnectionResetError, match="closed the connection"):
        await _restore(_versions(engine), mode, row["id"])


# Break: the restore never records its history row, records it under the wrong
# number, or points it at bytes that are not the restored version's. The row is
# the ONLY thing the history list, version download and the hard-delete purge read.
@pytest.mark.parametrize("current_version,expected_version", [(2, 3), (5, 6)])
@pytest.mark.parametrize("mode", ["async", "sync"])
async def test_restore_records_the_restored_bytes_as_the_next_history_version(
    files_db, mode, current_version, expected_version
):
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)
    old = b"version one bytes"
    row = _seed_restorable(files_db, engine, old=old, current=b"version two bytes")
    files_db.files.rows[row["id"]]["current_version"] = current_version
    vm = _versions(engine)

    await _restore(vm, mode, row["id"])

    history = {v["version_number"]: v for v in files_db.file_versions.rows.values() if v["file_id"] == row["id"]}
    assert sorted(history) == [1, expected_version]
    assert history[expected_version]["change_summary"] == "Restored from version 1"
    assert await vm.read_version_async(row["id"], expected_version) == old


# Break (2026-09-15): restore_version_async logged "operator should repair" when the
# history-row insert failed and returned success — the history silently lost the
# row, version N 404'd, and its .versions object was never purged by hard delete.
@pytest.mark.parametrize("mode", ["async", "sync"])
async def test_restore_propagates_a_failed_history_row_write(files_db, mode):
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)
    row = _seed_restorable(files_db, engine, old=b"version one bytes", current=b"version two bytes")

    def connection_reset(*_: Any) -> None:
        raise ConnectionResetError("server closed the connection unexpectedly")

    files_db.file_versions.before_create.append(connection_reset)

    with pytest.raises(ConnectionResetError, match="closed the connection"):
        await _restore(_versions(engine), mode, row["id"])


# Break: the restore records history version N but the file row never says N.
@pytest.mark.parametrize("current_version,expected_version", [(2, 3), (5, 6)])
@pytest.mark.parametrize("mode", ["async", "sync"])
async def test_restore_persists_the_new_version_number_on_the_file_row(
    files_db, mode, current_version, expected_version
):
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)
    row = _seed_restorable(files_db, engine, old=b"version one bytes", current=b"version two bytes")
    files_db.files.rows[row["id"]]["current_version"] = current_version

    await _restore(_versions(engine), mode, row["id"])

    persisted = files_db.files.rows[row["id"]]["current_version"]
    assert persisted == expected_version, (
        f"restore recorded version {expected_version} but files.files.current_version is "
        f"{persisted}: the version bump was lost"
    )


# Break (2026-09-15): restore_version_async caught a failed ``bump_version`` RPC and
# fell back to computing current_version + 1 WITHOUT writing it: the restore reported
# success and recorded history version N while the row still said N-1. The sync twin
# has no RPC (its converging update writes current_version), so this is async only.
async def test_restore_propagates_a_failed_version_bump(files_db):
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)
    current = b"version two bytes"
    row = _seed_restorable(files_db, engine, old=b"version one bytes", current=current)

    def connection_reset(schema: str, function: str, *_: Any) -> None:
        if function == "bump_version":
            raise ConnectionResetError("server closed the connection unexpectedly")

    files_db.before_rpc.append(connection_reset)

    try:
        await _restore(_versions(engine), "async", row["id"])
    except ConnectionResetError:
        pass
    else:
        pytest.fail(
            "restore reported success but the version bump was lost: files.files.current_version "
            f"is still {files_db.files.rows[row['id']]['current_version']}"
        )
    history = sorted(v["version_number"] for v in files_db.file_versions.rows.values() if v["file_id"] == row["id"])
    assert history == [1], f"a restore with no version number still recorded history {history}"
    assert engine._router.objects[AT_PATH_URI] == current, "live bytes overwritten by a restore that never got its version number"


async def test_collision_probe_runs_in_a_savepoint_so_the_lookup_is_not_poisoned(monkeypatch) -> None:
    """Feedback 7fb72866: inside replace_file_async's transaction a 23505 aborted the whole
    transaction and the canonical lookup died with InFailedSQLTransactionError."""
    import contextlib

    import matrx_orm

    from matrx_files.dedup import update_file_converging_async

    state = {"poisoned": False, "savepoints": 0}

    @contextlib.asynccontextmanager
    async def fake_transaction(database=None):
        state["savepoints"] += 1
        try:
            yield
        except Exception:
            state["poisoned"] = False  # rolled back TO the savepoint: outer txn is healthy
            raise

    class Db:
        def _db_name(self) -> str:
            return "x"

        def __init__(self) -> None:
            self.calls = 0

        async def update_file_async(self, file_id, updates, **kw):
            if state["poisoned"]:
                raise RuntimeError("InFailedSQLTransactionError")
            self.calls += 1
            if self.calls == 1:
                state["poisoned"] = True  # what a raw 23505 does without a savepoint
                raise UniqueViolation("cld_files_dedup_canonical")

        async def get_file_by_checksum_async(self, checksum, **kw):
            if state["poisoned"]:
                raise RuntimeError("InFailedSQLTransactionError")
            return {"id": "canonical-1"}

    monkeypatch.setattr(matrx_orm, "transaction", fake_transaction)
    written = await update_file_converging_async(
        Db(), "f1", {"checksum": "abc"}, current={}, owner_id="u", organization_id=None
    )
    assert written["duplicate_of_file_id"] == "canonical-1"
    assert state["savepoints"] >= 1
