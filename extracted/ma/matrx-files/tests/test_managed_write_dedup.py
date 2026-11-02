"""Phase 1 — managed_write_async dedup gate.

Mirrors test_tus_dedup.py for the original Phase 1 seam in
``packages/matrx-utils/matrx_utils/file_handling/cloud_sync/sync_engine.py``:

  * Brand-new ROOT inserts consult ``dedup.lookup_existing_async`` before
    the S3 PUT. A scope-matching hit short-circuits — no router write,
    no INSERT — and returns the canonical row's ``SyncResult`` with
    ``is_new=False``.
  * Derivatives (``parent_file_id`` / ``derivation_kind`` in EITHER
    kwargs OR metadata) bypass the lookup so byte-identical variants of
    distinct parents are intentionally separate rows. Legacy metadata
    lineage is normalized into the dedicated INSERT columns before storage.
  * Race recovery on the INSERT: the unique-violation on
    ``cld_files_dedup_canonical`` is detected, the winner is re-queried,
    the orphan S3 object is deleted, and the caller gets the winner's
    ``SyncResult``.

The DEDUP DECISION tests (bottom section) run the real ``SyncEngine``, real
``DatabaseClient`` and real ``dedup.lookup_existing_async`` over the captured
``files.files`` constraints in ``_files_db_double`` — no double owns the scope,
hash identity, reuse-vs-insert or race-recovery decision. The remaining tests
use mocked collaborators only to prove REFUSALS happen before any storage
write (ACL, membership, immutability, lineage validation) and to drive race /
cancellation timings a sequential double cannot express.
"""

from __future__ import annotations

import asyncio
import hashlib
import threading
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from matrx_files.cloud_sync.sync_engine import FolderOrganizationMismatch, SyncEngine
from matrx_files.dedup import DedupLookupResult, FilePathConflictError

from _files_db_double import FilesDB, UniqueViolation, build_engine

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


USER_ID = "user-1"
FILE_PATH = "docs/q1.pdf"
#: The organization the host boundary admitted for these requests. Every write
#: below reads it off the request context — the package never asks who the owner
#: is (common-docs/policies/context-is-carried-never-rebuilt.md).
CARRIED_ORG = "org-carried-0001"


def _carry_organization(organization_id: str = CARRIED_ORG) -> None:
    """Install the host's context seam (what ``configure_context`` installs).

    The autouse ``conftest`` fixture restores it after every test.
    """
    from matrx_utils import ctx as matrx_ctx

    matrx_ctx._context_getter = lambda: matrx_ctx.SimpleUserContext(
        user_id=USER_ID,
        is_authenticated=True,
        organization_id=organization_id,
    )


@pytest.mark.asyncio
async def test_managed_write_hashes_content_off_event_loop(monkeypatch):
    hash_threads: list[int] = []
    original_checksum = SyncEngine._checksum

    def tracked_checksum(content: bytes) -> str:
        hash_threads.append(threading.get_ident())
        return original_checksum(content)

    monkeypatch.setattr(SyncEngine, "_checksum", staticmethod(tracked_checksum))
    engine = _make_engine()
    loop_thread = threading.get_ident()
    canonical = _existing_row()
    canonical["checksum"] = hashlib.sha256(b"large-enough-in-production").hexdigest()

    with patch(
        "matrx_files.dedup.lookup_existing_async",
        AsyncMock(
            return_value=DedupLookupResult(
                checksum=canonical["checksum"],
                existing=canonical,
                scope="owner",
            )
        ),
    ):
        await engine.managed_write_async(FILE_PATH, b"large-enough-in-production")

    assert hash_threads
    assert all(thread_id != loop_thread for thread_id in hash_threads)


def _make_engine(
    *,
    existing_at_path: dict[str, Any] | None = None,
    upsert_raises: BaseException | None = None,
    inserted_id: str = "new-file-id-0001",
) -> SyncEngine:
    """Build a SyncEngine without running its heavy ``__init__``.

    Replaces ``_db`` / ``_router`` / ``permissions`` / ``versions`` with
    AsyncMocks so the gate logic runs in isolation. ``object.__new__``
    sidesteps DatabaseClient construction (which would otherwise try to
    resolve Supabase credentials at import time).
    """
    engine = object.__new__(SyncEngine)
    config = MagicMock()
    config.user_id = USER_ID
    config.storage_backend = "s3"
    config.resolve_s3_bucket = MagicMock(return_value="test-bucket")
    engine._config = config

    router = MagicMock()
    router.write_async = AsyncMock(return_value=None)
    router.delete_async = AsyncMock(return_value=None)
    router.get_url_async = AsyncMock(return_value="https://cdn/test")
    engine._router = router

    db = MagicMock()
    db.get_file_by_path_async = AsyncMock(return_value=existing_at_path)
    db.get_file_async = AsyncMock(return_value=None)
    db.upsert_file_async = (
        AsyncMock(side_effect=upsert_raises)
        if upsert_raises is not None
        else AsyncMock(
            return_value={
                "id": inserted_id,
                "owner_id": USER_ID,
                "file_path": FILE_PATH,
                "current_version": 1,
                "storage_uri": f"s3://test-bucket/{USER_ID}/{inserted_id}",
            }
        )
    )
    db.update_file_async = AsyncMock(return_value=None)
    db.upsert_permission_async = AsyncMock(return_value=None)
    db._rpc = AsyncMock(return_value=True)
    _carry_organization()
    engine._db = db

    permissions = MagicMock()
    permissions.require_async = AsyncMock(return_value=None)
    engine.permissions = permissions

    versions = MagicMock()
    versions.record_version_async = AsyncMock(return_value=None)
    engine.versions = versions

    engine._variants_service = None
    engine._fm_ref = None

    # _ensure_folder_async returns a folder_id; the value doesn't matter
    # to the gate — only that the insert payload carries something.
    engine._ensure_folder_async = AsyncMock(  # type: ignore[method-assign]
        return_value="folder-id-x"
    )
    # build_urls_for_record_async returns the durable URL flavours; the
    # gate uses them verbatim. Stub a fixed shape.
    engine.build_urls_for_record_async = AsyncMock(  # type: ignore[method-assign]
        return_value={
            "url": "https://cdn/test",
            "cdn_url": "https://cdn/test",
            "download_url": "https://cdn/test?download",
        }
    )
    return engine


def _make_sync_engine(
    *,
    existing_at_path: dict[str, Any] | None = None,
) -> SyncEngine:
    engine = object.__new__(SyncEngine)
    config = MagicMock()
    config.user_id = USER_ID
    config.storage_backend = "s3"
    config.resolve_s3_bucket.return_value = "test-bucket"
    engine._config = config

    router = MagicMock()
    router.write = MagicMock()
    router.delete = MagicMock()
    engine._router = router

    db = MagicMock()
    db.get_file_by_path.return_value = existing_at_path
    db.get_file.return_value = None
    db.get_file_by_checksum.return_value = None
    db._rpc_sync.return_value = True
    _carry_organization()
    db.upsert_file.return_value = {
        "id": "new-file-id",
        "current_version": 1,
    }
    engine._db = db

    engine.permissions = MagicMock()
    engine.versions = MagicMock()
    engine._ensure_folder = MagicMock(return_value="folder-id")  # type: ignore[method-assign]
    engine.build_urls_for_record = MagicMock(  # type: ignore[method-assign]
        return_value={
            "url": "https://cdn/test",
            "cdn_url": "https://cdn/test",
            "download_url": "https://cdn/test?download",
        }
    )
    return engine


def _existing_row(file_id: str = "canonical-existing-0001") -> dict[str, Any]:
    return {
        "id": file_id,
        "file_path": "docs/already_here.pdf",
        "storage_uri": f"s3://test-bucket/{USER_ID}/{file_id}",
        "canonical_storage_uri": f"s3://test-bucket/{USER_ID}/{file_id}",
        "size_bytes": 12,
        "checksum": hashlib.sha256(b"prev").hexdigest(),
        "owner_id": USER_ID,
        "current_version": 3,
        "published_to_web": False,
        "shown_to": "only_me",
        "mime_type": "application/pdf",
    }


@pytest.mark.asyncio
async def test_system_immutable_path_rejects_overwrite_before_s3_put() -> None:
    immutable = _existing_row()
    immutable["file_path"] = FILE_PATH
    immutable["metadata"] = {"system_immutable": True}
    engine = _make_engine(existing_at_path=immutable)

    with pytest.raises(PermissionError, match="cannot be overwritten"):
        await engine.managed_write_async(FILE_PATH, b"replacement")

    engine._router.write_async.assert_not_called()


@pytest.mark.asyncio
async def test_system_immutable_file_rejects_replace_and_publish_before_s3() -> None:
    immutable = _existing_row()
    immutable["metadata"] = {"system_immutable": True}
    engine = _make_engine()
    engine._db.get_file_async = AsyncMock(return_value=immutable)
    engine._router.copy_async = AsyncMock()

    with pytest.raises(PermissionError, match="cannot be replaced"):
        await engine.replace_file_async(immutable["id"], b"replacement", user_id=USER_ID)
    with pytest.raises(PermissionError, match="cannot be published or unpublished"):
        await engine.set_published_to_web_async(immutable["id"], True, user_id=USER_ID)

    engine._router.write_async.assert_not_called()
    engine._router.copy_async.assert_not_called()




# ---------------------------------------------------------------------------
# 2. Organization membership gates storage (refusal before any write)
# ---------------------------------------------------------------------------




@pytest.mark.asyncio
async def test_explicit_organization_requires_membership_before_storage_write():
    engine = _make_engine()
    engine._db._rpc = AsyncMock(return_value=False)

    with pytest.raises(PermissionError, match="not a member"):
        await engine.managed_write_async(
            FILE_PATH,
            b"org scoped content",
            metadata={"organization_id": "org-not-mine"},
        )

    engine._db._rpc.assert_awaited_once_with(
        "iam",
        "has_org_access_for",
        USER_ID,
        "org-not-mine",
    )
    engine._router.write_async.assert_not_called()
    engine._db.upsert_file_async.assert_not_called()




@pytest.mark.asyncio
async def test_existing_org_path_revalidates_current_membership_before_overwrite():
    existing = _existing_row()
    existing["file_path"] = FILE_PATH
    existing["organization_id"] = "org-revoked"
    engine = _make_engine(existing_at_path=existing)
    engine._db._rpc = AsyncMock(return_value=False)

    with pytest.raises(PermissionError, match="not a member"):
        await engine.managed_write_async(FILE_PATH, b"replacement")

    engine._db._rpc.assert_awaited_once_with(
        "iam",
        "has_org_access_for",
        USER_ID,
        "org-revoked",
    )
    engine._router.write_async.assert_not_called()
    engine._db.upsert_file_async.assert_not_called()


@pytest.mark.asyncio
async def test_reupload_at_an_existing_path_under_a_different_organization_converges_instead_of_refusing():
    """A person re-dropping the same export must never see an internal-column
    refusal (bring-your-export round 7, 2026-09-18, production build 5260b10f).

    ``cld_files`` is UNIQUE on ``(created_by, file_path)`` — the path already
    identifies exactly one row for this owner, in ONE organization — so a
    second upload at the same path that happens to declare a DIFFERENT
    organization (e.g. the caller's active org changed between the two
    uploads) can never relocate that row. It must converge on the row's own
    organization and update in place, not raise "organization_id cannot
    change when updating an existing file path".
    """
    existing = _existing_row()
    existing["file_path"] = FILE_PATH
    existing["organization_id"] = "org-original-0001"
    engine = _make_engine(existing_at_path=existing)

    result = await engine.managed_write_async(
        FILE_PATH,
        b"replacement",
        metadata={"organization_id": "org-different-0002"},
    )

    assert result is not None
    # Membership is revalidated against the EXISTING row's organization, not
    # the mismatched one the caller requested — the row's own org wins.
    # (checked once to decide adopt-or-new-path, once to authorize the write)
    engine._db._rpc.assert_awaited_with(
        "iam",
        "has_org_access_for",
        USER_ID,
        "org-original-0001",
    )
    engine._db.update_file_async.assert_awaited_once()
    engine.permissions.require_async.assert_awaited_once_with(
        "file", existing["id"], "write", USER_ID
    )


def test_sync_reupload_at_an_existing_path_under_a_different_organization_converges_instead_of_refusing():
    """Sync twin of the async convergence test above."""
    existing = _existing_row()
    existing["file_path"] = FILE_PATH
    existing["organization_id"] = "org-original-0001"
    engine = _make_sync_engine(existing_at_path=existing)

    result = engine.managed_write(
        FILE_PATH,
        b"replacement",
        metadata={"organization_id": "org-different-0002"},
    )

    assert result is not None
    engine._db._rpc_sync.assert_called_once_with(
        "iam",
        "has_org_access_for",
        USER_ID,
        "org-original-0001",
    )
    engine._db.update_file.assert_called_once()






@pytest.mark.asyncio
async def test_unknown_derivation_kind_fails_before_storage_write():
    engine = _make_engine()

    with pytest.raises(ValueError, match="Unknown file derivation_kind"):
        await engine.managed_write_async(
            FILE_PATH,
            b"unregistered derivative",
            derivation_kind="future_kind_without_migration",
        )

    engine._router.write_async.assert_not_called()
    engine._db.upsert_file_async.assert_not_called()


@pytest.mark.asyncio
async def test_parent_without_kind_fails_before_storage_write():
    engine = _make_engine()

    with pytest.raises(ValueError, match="parent_file_id requires derivation_kind"):
        await engine.managed_write_async(
            FILE_PATH,
            b"incomplete lineage",
            parent_file_id="parent-without-kind",
        )

    engine._router.write_async.assert_not_called()
    engine._db.upsert_file_async.assert_not_called()


# ---------------------------------------------------------------------------
# 5. Existing row at the same file_path — refusals before storage
# ---------------------------------------------------------------------------




@pytest.mark.asyncio
async def test_create_only_existing_path_fails_before_storage_or_update():
    existing = _existing_row()
    existing["file_path"] = FILE_PATH
    engine = _make_engine(existing_at_path=existing)

    with pytest.raises(FilePathConflictError):
        await engine.managed_write_async(
            FILE_PATH,
            b"different bytes",
            file_id="fresh-id",
            create_only=True,
        )

    engine._router.write_async.assert_not_called()
    engine._db.update_file_async.assert_not_called()


@pytest.mark.asyncio
async def test_existing_path_write_acl_is_checked_before_storage():
    existing = _existing_row()
    existing["file_path"] = FILE_PATH
    engine = _make_engine(existing_at_path=existing)
    engine.permissions.require_async = AsyncMock(
        side_effect=PermissionError("revoked contextual access")
    )

    with pytest.raises(PermissionError, match="revoked contextual access"):
        await engine.managed_write_async(FILE_PATH, b"replacement")

    engine._router.write_async.assert_not_called()
    engine._db.update_file_async.assert_not_called()


@pytest.mark.asyncio
async def test_unreadable_parent_fails_before_dedup_or_storage():
    engine = _make_engine()
    engine.permissions.require_async = AsyncMock(
        side_effect=PermissionError("requires read access")
    )

    with (
        patch(
            "matrx_files.dedup.lookup_existing_async",
            AsyncMock(),
        ) as lookup_mock,
        pytest.raises(PermissionError, match="requires read access"),
    ):
        await engine.managed_write_async(
            FILE_PATH,
            b"derived",
            parent_file_id="hidden-parent",
            derivation_kind="variant",
        )

    lookup_mock.assert_not_awaited()
    engine._router.write_async.assert_not_called()
    engine._db.upsert_file_async.assert_not_called()


@pytest.mark.asyncio
async def test_metadata_duplicate_uses_equivalence_validation_not_contextual_read_acl():
    engine = _make_engine()
    content = b"intentional copy"
    engine.permissions.require_async = AsyncMock(
        side_effect=PermissionError("no contextual domain edge yet")
    )
    engine._db.get_file_async = AsyncMock(
        return_value={
            "id": "canonical-id",
            "owner_id": USER_ID,
            "organization_id": CARRIED_ORG,
            "checksum": hashlib.sha256(content).hexdigest(),
            "parent_file_id": None,
            "duplicate_of_file_id": None,
        }
    )

    with patch(
        "matrx_files.dedup.lookup_existing_async",
        AsyncMock(),
    ) as lookup_mock:
        await engine.managed_write_async(
            FILE_PATH,
            content,
            metadata={"duplicate_of_file_id": "canonical-id"},
        )

    engine.permissions.require_async.assert_not_awaited()
    lookup_mock.assert_not_awaited()
    payload = engine._db.upsert_file_async.await_args.args[0]
    assert payload["duplicate_of_file_id"] == "canonical-id"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "target_overrides",
    [
        {"checksum": hashlib.sha256(b"different bytes").hexdigest()},
        {"owner_id": "different-owner"},
        {"organization_id": "different-organization"},
        {"parent_file_id": "parent-id"},
        {"duplicate_of_file_id": "another-canonical-id"},
    ],
)
async def test_duplicate_target_must_match_content_and_canonical_scope(
    target_overrides,
):
    engine = _make_engine()
    target = {
        "id": "not-equivalent",
        "owner_id": USER_ID,
        "organization_id": CARRIED_ORG,
        "checksum": hashlib.sha256(b"new bytes").hexdigest(),
        "parent_file_id": None,
        "duplicate_of_file_id": None,
    }
    target.update(target_overrides)
    engine._db.get_file_async = AsyncMock(return_value=target)

    with pytest.raises(ValueError, match="identical content"):
        await engine.managed_write_async(
            FILE_PATH,
            b"new bytes",
            duplicate_of_file_id="not-equivalent",
        )

    engine._router.write_async.assert_not_called()
    engine._db.upsert_file_async.assert_not_called()


@pytest.mark.asyncio
async def test_create_only_path_race_with_different_content_is_a_path_conflict():
    path_unique = UniqueViolation("cld_files_owner_id_file_path_key")
    engine = _make_engine(upsert_raises=path_unique)
    winner = _existing_row(file_id="other-content-winner")
    winner["file_path"] = FILE_PATH
    engine._db.get_file_by_path_async = AsyncMock(side_effect=[None, winner])

    with (
        patch(
            "matrx_files.dedup.lookup_existing_async",
            AsyncMock(
                return_value=DedupLookupResult(
                    checksum=hashlib.sha256(b"new bytes").hexdigest(),
                    existing=None,
                    scope="none",
                )
            ),
        ),
        pytest.raises(FilePathConflictError),
    ):
        await engine.managed_write_async(
            FILE_PATH,
            b"new bytes",
            file_id="fresh-id",
            create_only=True,
        )

    engine._router.delete_async.assert_awaited_once()


@pytest.mark.asyncio
async def test_legacy_path_race_never_converges_on_different_content():
    path_unique = UniqueViolation("cld_files_owner_id_file_path_key")
    engine = _make_engine(upsert_raises=path_unique)
    winner = _existing_row(file_id="other-content-winner")
    winner["file_path"] = FILE_PATH
    engine._db.get_file_by_path_async = AsyncMock(side_effect=[None, winner])

    with (
        patch(
            "matrx_files.dedup.lookup_existing_async",
            AsyncMock(
                return_value=DedupLookupResult(
                    checksum=hashlib.sha256(b"new bytes").hexdigest(),
                    existing=None,
                    scope="none",
                )
            ),
        ),
        pytest.raises(Exception, match="cld_files_owner_id_file_path_key"),
    ):
        await engine.managed_write_async(
            FILE_PATH,
            b"new bytes",
            file_id="fresh-id",
        )

    engine._router.delete_async.assert_awaited_once()
    engine.versions.record_version_async.assert_not_called()


@pytest.mark.asyncio
async def test_folder_lookup_names_the_files_organization():
    """A person's folder tree is per organization: the lookup is keyed on
    (owner, organization, path), so the folder found is the file's organization's."""
    engine = _make_engine()
    engine._ensure_folder_async = SyncEngine._ensure_folder_async.__get__(engine)
    engine._db.get_folder_by_path_async = AsyncMock(
        return_value={"id": "folder-id", "organization_id": "org-shared"}
    )
    engine._db.create_folder_async = AsyncMock()

    folder_id = await engine._ensure_folder_async(FILE_PATH, USER_ID, "org-shared")

    assert folder_id == "folder-id"
    engine._db.get_folder_by_path_async.assert_awaited_once_with(
        USER_ID, FILE_PATH.rsplit("/", 1)[0], "org-shared"
    )
    engine._db.create_folder_async.assert_not_called()


@pytest.mark.asyncio
async def test_another_organizations_folder_is_refused_never_reused():
    """Until 2026-10-12 the owner's folder of ANOTHER organization was reused (977 files ended
    up under another organization's folder). A lookup that returns one is a defect: refused."""
    engine = _make_engine()
    engine._ensure_folder_async = SyncEngine._ensure_folder_async.__get__(engine)
    engine._db.get_folder_by_path_async = AsyncMock(
        side_effect=[None, {"id": "folder-race", "organization_id": "org-other"}]
    )
    engine._db.create_folder_async = AsyncMock(side_effect=RuntimeError("unique folder path"))

    with pytest.raises(FolderOrganizationMismatch):
        await engine._ensure_folder_async(FILE_PATH, USER_ID, "org-shared")


@pytest.mark.asyncio
async def test_concurrent_same_org_folder_winner_is_reused():
    engine = _make_engine()
    engine._ensure_folder_async = SyncEngine._ensure_folder_async.__get__(engine)
    engine._db.get_folder_by_path_async = AsyncMock(
        side_effect=[
            None,
            {"id": "folder-race", "organization_id": "org-shared"},
        ]
    )
    engine._db.create_folder_async = AsyncMock(side_effect=RuntimeError("unique folder path"))

    folder_id = await engine._ensure_folder_async(
        FILE_PATH,
        USER_ID,
        "org-shared",
    )

    assert folder_id == "folder-race"


def test_sync_write_authorizes_existing_file_before_storage():
    existing = _existing_row()
    existing["file_path"] = FILE_PATH
    existing["organization_id"] = "org-shared"
    engine = _make_sync_engine(existing_at_path=existing)
    engine.permissions.require.side_effect = PermissionError("write denied")

    with pytest.raises(PermissionError, match="write denied"):
        engine.managed_write(FILE_PATH, b"replacement")

    engine._router.write.assert_not_called()
    engine._db.update_file.assert_not_called()


def test_sync_write_validates_and_stamps_explicit_organization():
    engine = _make_sync_engine()

    engine.managed_write(
        FILE_PATH,
        b"new bytes",
        metadata={"organization_id": "org-shared"},
    )

    engine._db._rpc_sync.assert_called_once_with(
        "iam",
        "has_org_access_for",
        USER_ID,
        "org-shared",
    )
    engine._ensure_folder.assert_called_once_with(
        FILE_PATH,
        USER_ID,
        "org-shared",
    )
    payload = engine._db.upsert_file.call_args.args[0]
    assert payload["organization_id"] == "org-shared"
    assert payload["id"]
    assert payload["storage_uri"].endswith(f"/{payload['id']}")


def test_sync_folder_lookup_names_the_files_organization():
    engine = _make_sync_engine()
    engine._ensure_folder = SyncEngine._ensure_folder.__get__(engine)
    engine._db.get_folder_by_path.return_value = {"id": "folder-id", "organization_id": "org-shared"}

    assert engine._ensure_folder(FILE_PATH, USER_ID, "org-shared") == "folder-id"
    engine._db.get_folder_by_path.assert_called_once_with(
        USER_ID, FILE_PATH.rsplit("/", 1)[0], "org-shared"
    )
    engine._db.create_folder.assert_not_called()


def test_sync_another_organizations_folder_is_refused_never_reused():
    engine = _make_sync_engine()
    engine._ensure_folder = SyncEngine._ensure_folder.__get__(engine)
    engine._db.get_folder_by_path.side_effect = [
        None,
        {"id": "folder-race", "organization_id": "org-other"},
    ]
    engine._db.create_folder.side_effect = RuntimeError("unique folder path")

    with pytest.raises(FolderOrganizationMismatch):
        engine._ensure_folder(FILE_PATH, USER_ID, "org-shared")


def test_sync_concurrent_same_org_folder_winner_is_reused():
    engine = _make_sync_engine()
    engine._ensure_folder = SyncEngine._ensure_folder.__get__(engine)
    engine._db.get_folder_by_path.side_effect = [
        None,
        {"id": "folder-race", "organization_id": "org-shared"},
    ]
    engine._db.create_folder.side_effect = RuntimeError("unique folder path")

    assert (
        engine._ensure_folder(
            FILE_PATH,
            USER_ID,
            "org-shared",
        )
        == "folder-race"
    )


def test_sync_new_path_race_reuses_same_checksum_winner_without_overwrite():
    engine = _make_sync_engine()
    checksum = hashlib.sha256(b"same bytes").hexdigest()
    winner = _existing_row(file_id="sync-race-winner")
    winner["file_path"] = FILE_PATH
    winner["checksum"] = checksum
    engine._db.get_file_by_path.side_effect = [None, winner]
    engine._db.upsert_file.side_effect = UniqueViolation("cld_files_owner_id_file_path_key")

    result = engine.managed_write(FILE_PATH, b"same bytes")

    assert result.file_id == "sync-race-winner"
    engine._router.delete.assert_called_once()
    engine.versions.record_version.assert_not_called()


def test_sync_new_path_race_never_aliases_different_bytes():
    engine = _make_sync_engine()
    winner = _existing_row(file_id="sync-race-winner")
    winner["file_path"] = FILE_PATH
    winner["checksum"] = hashlib.sha256(b"winner bytes").hexdigest()
    engine._db.get_file_by_path.side_effect = [None, winner]
    engine._db.upsert_file.side_effect = UniqueViolation("cld_files_owner_id_file_path_key")

    with pytest.raises(UniqueViolation, match="cld_files_owner_id_file_path_key"):
        engine.managed_write(FILE_PATH, b"loser bytes")

    engine._router.delete.assert_called_once()
    engine.versions.record_version.assert_not_called()




# ---------------------------------------------------------------------------
# 7. Race recovery — non-dedup-related insert failure is re-raised
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_unrelated_insert_failure_bubbles_up():
    """An INSERT that fails for a reason NEITHER race handler knows how
    to recover from (a non-unique DB error, FK violation, connection
    drop) must bubble up — never be silently swallowed. The orphan S3
    object we already PUT is still cleaned up on the way out (P0-1):
    a failed insert must not leak storage."""
    content = b"insert that fails for an unrelated reason"
    other_violation = Exception('foreign key violation "cld_files_some_fk" SQLSTATE 23503')
    engine = _make_engine(upsert_raises=other_violation)

    with patch(
        "matrx_files.dedup.lookup_existing_async",
        AsyncMock(
            return_value=DedupLookupResult(
                checksum=hashlib.sha256(content).hexdigest(),
                existing=None,
                scope="none",
            )
        ),
    ):
        with pytest.raises(Exception) as exc_info:
            await engine.managed_write_async(FILE_PATH, content)

    assert "23503" in str(exc_info.value)
    # Orphan S3 cleanup DID run — a failed insert must not leak its object.
    engine._router.delete_async.assert_called_once()
    # The winner was never read — this is not a recoverable race.
    engine.versions.record_version_async.assert_not_called()


# ---------------------------------------------------------------------------
# 8. Race recovery — (owner_id, file_path) collision converges on the winner
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_path_unique_collision_recovers_to_winner():
    """A concurrent pinned-id insert that loses the (owner_id, file_path)
    slot (e.g. two variant-render passes for the same content-deduped
    master writing the same variant path) must NOT corrupt the winner's
    primary key. It now raises 23505 on cld_files_owner_id_file_path_key;
    the loser recovers idempotently by reading the winner, returns its
    SyncResult (is_new=False), deletes its own orphan S3 object, and
    records NO version (the winner already has one)."""
    content = b"variant bytes written twice concurrently"
    winner = _existing_row(file_id="variant-winner-0001")
    winner["checksum"] = hashlib.sha256(content).hexdigest()
    path_violation = UniqueViolation("cld_files_owner_id_file_path_key")
    engine = _make_engine(upsert_raises=path_violation)
    # First lookup (pre-insert) finds nothing; the post-collision read
    # returns the winning row that won the slot.
    engine._db.get_file_by_path_async = AsyncMock(side_effect=[None, winner])

    # Derivative write (variant) — bypasses the dedup lookup entirely, so
    # the ONLY recovery path is the (owner_id, file_path) handler.
    result = await engine.managed_write_async(
        FILE_PATH,
        content,
        parent_file_id="master-0001",
        derivation_kind="variant",
    )

    assert result.file_id == winner["id"]
    assert result.is_new is False
    # Orphan S3 object (our losing write) cleaned up.
    engine._router.delete_async.assert_called_once()
    # No version recorded — the winner already has its own.
    engine.versions.record_version_async.assert_not_called()


@pytest.mark.asyncio
async def test_cancelled_async_insert_is_observed_before_storage_compensation():
    """Cancellation cannot delete a UUID-key object whose row committed."""
    engine = _make_engine()
    insert_started = asyncio.Event()
    release_insert = asyncio.Event()

    async def delayed_insert(payload: dict[str, Any]) -> dict[str, Any]:
        insert_started.set()
        await release_insert.wait()
        return {
            **payload,
            "id": payload["id"],
            "current_version": 1,
        }

    engine._db.upsert_file_async = AsyncMock(side_effect=delayed_insert)

    with patch(
        "matrx_files.dedup.lookup_existing_async",
        AsyncMock(
            return_value=DedupLookupResult(
                checksum=hashlib.sha256(b"cancelled insert").hexdigest(),
                existing=None,
                scope="none",
            )
        ),
    ):
        task = asyncio.create_task(engine.managed_write_async(FILE_PATH, b"cancelled insert"))
        await insert_started.wait()
        task.cancel()
        release_insert.set()
        with pytest.raises(asyncio.CancelledError):
            await task

    engine._router.delete_async.assert_not_called()
    engine.versions.record_version_async.assert_awaited_once()


@pytest.mark.asyncio
async def test_async_insert_timeout_reconciles_exact_committed_row():
    """A lost response returns the exact committed UUID row without cleanup."""
    engine = _make_engine(upsert_raises=TimeoutError("response lost"))
    content = b"committed despite timeout"
    checksum = hashlib.sha256(content).hexdigest()
    committed = {
        "id": "committed-file-id",
        "file_path": FILE_PATH,
        "storage_uri": f"s3://test-bucket/{USER_ID}/committed-file-id",
        "file_name": "q1.pdf",
        "mime_type": "application/pdf",
        "size_bytes": len(content),
        "checksum": checksum,
        "visibility": "personal",
        "current_version": 1,
    }
    engine._db.get_file_async = AsyncMock(return_value=committed)

    with (
        patch(
            "matrx_files.dedup.lookup_existing_async",
            AsyncMock(
                return_value=DedupLookupResult(
                    checksum=checksum,
                    existing=None,
                    scope="none",
                )
            ),
        ),
        patch(
            "matrx_files.cloud_sync.sync_engine.uuid.uuid4",
            return_value="committed-file-id",
        ),
    ):
        result = await engine.managed_write_async(FILE_PATH, content)

    assert result.file_id == "committed-file-id"
    engine._db.get_file_async.assert_awaited_once_with(
        "committed-file-id",
        include_deleted=True,
    )
    engine._router.delete_async.assert_not_called()


# ---------------------------------------------------------------------------
# THE TRASHED-FOLDER WRITE BARRIER (regression, 2026-08-11)
#
# Folder lookups filter deleted_at is null; the (created_by, folder_path)
# uniqueness the INSERT collides with does not. A soft-deleted folder made
# every write beneath it fail FOREVER as an unmapped 500: absent → duplicate →
# absent again → raise. A 2026-06-14 cleanup trashed real users' Transcripts /
# Transcripts/Recordings folders, so from then on every finished audio
# recording failed to save while its chunks (a different folder) uploaded fine.
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_trashed_folder_is_revived_instead_of_failing_the_write():
    engine = _make_engine()
    engine._ensure_folder_async = SyncEngine._ensure_folder_async.__get__(engine)
    # Live lookups (parent + the colliding path) never see the trashed row.
    engine._db.get_folder_by_path_async = AsyncMock(return_value=None)
    engine._db.create_folder_async = AsyncMock(
        side_effect=RuntimeError(
            'duplicate key value violates unique constraint "cld_files_owner_id_folder_path_key"'
        )
    )
    engine._db.get_folder_by_path_any_state_async = AsyncMock(
        return_value={
            "id": "trashed-folder",
            "organization_id": "org-shared",
            "deleted_at": "2026-06-14T08:18:49.789068+00:00",
        }
    )
    engine._db.restore_folder_async = AsyncMock(
        return_value={
            "id": "trashed-folder",
            "organization_id": "org-shared",
            "deleted_at": None,
        }
    )

    folder_id = await engine._ensure_folder_async(FILE_PATH, USER_ID, "org-shared")

    assert folder_id == "trashed-folder"
    engine._db.restore_folder_async.assert_awaited_once_with("trashed-folder")


@pytest.mark.asyncio
async def test_insert_failure_with_no_folder_at_all_still_raises():
    """Revival must never swallow a genuine INSERT failure."""
    engine = _make_engine()
    engine._ensure_folder_async = SyncEngine._ensure_folder_async.__get__(engine)
    engine._db.get_folder_by_path_async = AsyncMock(return_value=None)
    engine._db.create_folder_async = AsyncMock(side_effect=RuntimeError("disk on fire"))
    engine._db.get_folder_by_path_any_state_async = AsyncMock(return_value=None)
    engine._db.restore_folder_async = AsyncMock()

    with pytest.raises(RuntimeError, match="disk on fire"):
        await engine._ensure_folder_async(FILE_PATH, USER_ID, "org-shared")

    engine._db.restore_folder_async.assert_not_called()


def test_sync_trashed_folder_is_revived_instead_of_failing_the_write():
    engine = _make_sync_engine()
    engine._ensure_folder = SyncEngine._ensure_folder.__get__(engine)
    engine._db.get_folder_by_path = MagicMock(return_value=None)
    engine._db.create_folder = MagicMock(
        side_effect=RuntimeError("duplicate key value violates unique constraint")
    )
    engine._db.get_folder_by_path_any_state = MagicMock(
        return_value={
            "id": "trashed-folder",
            "organization_id": "org-shared",
            "deleted_at": "2026-06-14T08:18:49.789068+00:00",
        }
    )
    engine._db.restore_folder = MagicMock(
        return_value={
            "id": "trashed-folder",
            "organization_id": "org-shared",
            "deleted_at": None,
        }
    )

    folder_id = engine._ensure_folder(FILE_PATH, USER_ID, "org-shared")

    assert folder_id == "trashed-folder"
    engine._db.restore_folder.assert_called_once_with("trashed-folder")


# ---------------------------------------------------------------------------
# DEDUP DECISION — real SyncEngine + real DatabaseClient + real dedup lookup
#
# Everything the gate owns runs for real: the checksum, the scope handed to
# ``dedup.lookup_existing_async``, the checksum query itself, and the insert /
# race-recovery against the unique indexes CAPTURED from Matrx Main (see
# ``_files_db_double``). Only S3, IAM RPCs, the ACL checker and the version
# recorder are doubles. Each test names the break it catches.
# ---------------------------------------------------------------------------

PERSONAL_ORG = "org-personal-0001"
OTHER_USER = "user-2"


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@pytest.fixture
def files_db():
    db = FilesDB()
    db.org_members.add((USER_ID, PERSONAL_ORG))  # every user belongs to their personal org
    with db.bound():
        yield db


def _seed_canonical(db: FilesDB, content: bytes, **overrides: Any) -> dict[str, Any]:
    values: dict[str, Any] = {
        "created_by": USER_ID,
        "organization_id": PERSONAL_ORG,
        "file_path": "docs/already_here.pdf",
        "checksum": _sha(content),
        "storage_uri": "s3://test-bucket/user-1/canonical-existing",
        "current_version": 3,
    }
    values.update(overrides)
    return db.seed_file(**values)


# Break: gate skipped, or handed the wrong owner / org / checksum. The unique
# index + race recovery would still converge on the canonical row, so the
# forcing signal is the upload itself: a dedup hit must never PUT the bytes.
async def test_root_write_of_owned_content_reuses_canonical_row_without_writing(files_db):
    content = b"the same content uploaded twice"
    canonical = _seed_canonical(files_db, content)
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)

    result = await engine.managed_write_async(FILE_PATH, content)

    assert result.file_id == canonical["id"]
    assert result.is_new is False
    assert result.storage_uri == "s3://test-bucket/user-1/canonical-existing"
    assert result.checksum == _sha(content)
    assert engine._router.puts == [], "a dedup hit uploaded the bytes before converging"
    assert engine._router.objects == {}
    assert [r["id"] for r in files_db.live_files()] == [canonical["id"]]
    assert engine.versions.recorded == []


# Break: hash computed over the wrong bytes, row stamped with the wrong
# org/owner, object not stored under the row's URI, or no version recorded.
async def test_root_write_of_new_content_persists_row_object_and_version(files_db):
    content = b"genuinely new content"
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)

    result = await engine.managed_write_async(FILE_PATH, content)

    row = files_db.files.rows[result.file_id]
    assert result.is_new is True
    assert row["checksum"] == _sha(content)
    assert row["created_by"] == USER_ID
    assert row["organization_id"] == PERSONAL_ORG
    assert row["file_path"] == FILE_PATH
    assert engine._router.objects == {row["storage_uri"]: content}
    assert engine.versions.recorded == [(result.file_id, row["checksum"])]


# Break (production defect, jobs-bar cold-walk-11, 2026-09-18): SHA-256 of
# EMPTY content is the same constant hash (`e3b0c44298fc1c14...`) for every
# zero-byte upload, ever, in a scope. Blank-file uploads therefore always
# collide with whatever unrelated file first happened to be uploaded empty
# in that owner/org — a real walk uploaded a blank irrigation-domain file and
# the dedup short-circuit silently handed back an unrelated pre-existing
# `official-mcat-content-outline.pdf` row instead of creating a new (empty)
# row, and the caller (a "Dump everything you have" batch attach) had no way
# to know the id it received did not correspond to the file it uploaded. An
# empty payload carries no content to legitimately deduplicate, so root
# dedup must never fire for it — it must always create a fresh row.
async def test_root_write_of_empty_content_never_aliases_an_unrelated_canonical_row(
    files_db,
):
    unrelated = _seed_canonical(
        files_db, b"", file_path="docs/official-mcat-content-outline.pdf"
    )
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)

    result = await engine.managed_write_async(FILE_PATH, b"")

    assert result.file_id != unrelated["id"]
    assert result.is_new is True
    row = files_db.files.rows[result.file_id]
    assert row["file_path"] == FILE_PATH
    assert engine._router.objects[row["storage_uri"]] == b""


def test_sync_root_write_of_empty_content_never_aliases_an_unrelated_canonical_row(
    files_db,
):
    """Sync twin of the break above — ``managed_write`` (non-async) must not
    alias empty uploads either."""
    unrelated = _seed_canonical(
        files_db, b"", file_path="docs/official-mcat-content-outline.pdf"
    )
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)

    result = engine.managed_write(FILE_PATH, b"")

    assert result.file_id != unrelated["id"]
    assert result.is_new is True
    row = files_db.files.rows[result.file_id]
    assert row["file_path"] == FILE_PATH
    assert engine._router.objects[row["storage_uri"]] == b""


@pytest.mark.parametrize(
    "decoy",
    [
        {"created_by": OTHER_USER},
        {"organization_id": "org-other"},
        {"deleted_at": "2026-06-14T08:18:49Z"},
        {"parent_file_id": "some-master", "derivation_kind": "variant"},
        {"duplicate_of_file_id": "some-canonical"},
    ],
    ids=["other-member", "other-org", "trashed", "derivative", "force-copy"],
)
async def test_root_write_never_aliases_a_row_outside_the_callers_canonical_scope(
    files_db, decoy
):
    """Break: cross-tenant / trashed / non-canonical reuse — the caller would be
    handed a row they cannot read or that is not a live canonical upload."""
    content = b"identical bytes owned elsewhere"
    other = _seed_canonical(files_db, content, **decoy)
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)

    result = await engine.managed_write_async(FILE_PATH, content)

    assert result.is_new is True
    assert result.file_id != other["id"]
    assert files_db.files.rows[result.file_id]["organization_id"] == PERSONAL_ORG
    assert engine._router.objects[result.storage_uri] == content


async def test_explicit_organization_scopes_dedup_row_and_folder_to_that_org(files_db):
    """Break: the validated explicit org is not what the lookup, the folder and
    the row all use — the personal copy would be aliased into another org."""
    content = b"org scoped content"
    _seed_canonical(files_db, content)  # same bytes, PERSONAL org
    files_db.org_members.add((USER_ID, "org-shared"))
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)

    result = await engine.managed_write_async(
        FILE_PATH,
        content,
        metadata={"scope": {"organization_id": "org-shared"}},
    )

    assert result.is_new is True
    assert files_db.files.rows[result.file_id]["organization_id"] == "org-shared"
    folder = files_db.folders.rows[files_db.files.rows[result.file_id]["parent_folder_id"]]
    assert (folder["folder_path"], folder["organization_id"]) == ("docs", "org-shared")


@pytest.mark.parametrize("via", ["kwargs", "metadata"])
async def test_derivative_write_of_canonical_bytes_gets_its_own_lineage_row(files_db, via):
    """Break: derivatives consult dedup (blank page renders of distinct PDFs
    would alias one row) or lineage never lands in the INSERT columns."""
    content = b"identical blank page bytes"
    canonical = _seed_canonical(files_db, content)
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)
    engine.permissions.allowed.add((USER_ID, "parent-pdf-1", "read"))
    lineage = {"parent_file_id": "parent-pdf-1", "derivation_kind": "rendered_page_image"}

    if via == "kwargs":
        result = await engine.managed_write_async(FILE_PATH, content, **lineage)
    else:
        result = await engine.managed_write_async(
            FILE_PATH, content, metadata={**lineage, "page_number": 1}
        )

    row = files_db.files.rows[result.file_id]
    assert result.is_new is True
    assert result.file_id != canonical["id"]
    assert (row["parent_file_id"], row["derivation_kind"]) == (
        "parent-pdf-1",
        "rendered_page_image",
    )
    assert engine._router.objects[row["storage_uri"]] == content


async def test_derivation_kind_without_parent_still_reuses_root_canonical(files_db):
    """Break: a caller-controlled kind alone opts out of root dedup."""
    content = b"variant payload"
    canonical = _seed_canonical(files_db, content)
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)

    result = await engine.managed_write_async(
        FILE_PATH, content, metadata={"derivation_kind": "variant"}
    )

    assert result.file_id == canonical["id"]
    assert engine._router.objects == {}


async def test_save_over_existing_path_writes_the_next_version_onto_that_row(files_db):
    """Break: the path-keyed update is skipped, bumps no version, or rekeys the
    object away from the URI the row already references."""
    content = b"new version of an existing file"
    at_path = files_db.seed_file(
        created_by=USER_ID,
        organization_id=PERSONAL_ORG,
        file_path=FILE_PATH,
        checksum=_sha(b"prev"),
        storage_uri="s3://test-bucket/user-1/at-path",
        current_version=3,
    )
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)
    engine.permissions.allowed.add((USER_ID, at_path["id"], "write"))

    result = await engine.managed_write_async(FILE_PATH, content)

    row = files_db.files.rows[at_path["id"]]
    assert (result.file_id, result.is_new) == (at_path["id"], False)
    assert (row["current_version"], row["checksum"]) == (4, _sha(content))
    assert engine._router.objects == {"s3://test-bucket/user-1/at-path": content}
    assert engine.versions.recorded == [(at_path["id"], _sha(content))]


CANONICAL_PATH = "docs/already_here.pdf"
CANONICAL_URI = "s3://test-bucket/user-1/canonical-existing"
AT_PATH_URI = "s3://test-bucket/user-1/at-path"


def _seed_save_over_a_content_match(
    db: FilesDB, engine: SyncEngine, content: bytes
) -> tuple[dict[str, Any], dict[str, Any]]:
    """A file at FILE_PATH holding old bytes + ANOTHER live canonical root of the
    same owner/org already holding ``content``; both objects exist in storage."""
    at_path = db.seed_file(
        created_by=USER_ID,
        organization_id=PERSONAL_ORG,
        file_path=FILE_PATH,
        checksum=_sha(b"prev"),
        storage_uri=AT_PATH_URI,
        current_version=3,
    )
    elsewhere = _seed_canonical(db, content)
    engine._router.objects.update({AT_PATH_URI: b"prev", CANONICAL_URI: content})
    engine.permissions.allowed.add((USER_ID, at_path["id"], "write"))
    return at_path, elsewhere


# Break (production defect 2026-09-10, fixed with this test): the path row's
# UPDATE to bytes another canonical root already holds hit a raw 23505 on
# ``cld_files_dedup_canonical`` and the user's save was lost. Also: the save is
# redirected to the content match, or the row does not become its alias.
async def test_save_over_existing_path_is_never_redirected_to_a_content_match(files_db):
    content = b"new version of an existing file"
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)
    at_path, elsewhere = _seed_save_over_a_content_match(files_db, engine, content)

    try:
        result = await engine.managed_write_async(FILE_PATH, content)
    except Exception as exc:  # the defect: a raw unique violation loses the save
        pytest.fail(f"save over {FILE_PATH} was lost: {exc}")

    row = files_db.files.rows[at_path["id"]]
    assert (result.file_id, result.is_new, result.version_number) == (at_path["id"], False, 4)
    assert (row["file_path"], row["current_version"], row["checksum"]) == (
        FILE_PATH,
        4,
        _sha(content),
    )
    assert row["duplicate_of_file_id"] == elsewhere["id"]
    assert engine._router.objects == {AT_PATH_URI: content, CANONICAL_URI: content}
    assert engine.versions.recorded == [(at_path["id"], _sha(content))]
    canonical = files_db.files.rows[elsewhere["id"]]
    assert (canonical["current_version"], canonical["duplicate_of_file_id"]) == (3, None)


# Break (sync twin of the defect above): ``managed_write`` loses the same save.
def test_sync_save_over_existing_path_converges_on_the_content_match(files_db):
    content = b"new version of an existing file"
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)
    at_path, elsewhere = _seed_save_over_a_content_match(files_db, engine, content)

    try:
        result = engine.managed_write(FILE_PATH, content)
    except Exception as exc:
        pytest.fail(f"sync save over {FILE_PATH} was lost: {exc}")

    row = files_db.files.rows[at_path["id"]]
    assert (result.file_id, result.is_new) == (at_path["id"], False)
    assert (row["current_version"], row["checksum"]) == (4, _sha(content))
    assert row["duplicate_of_file_id"] == elsewhere["id"]
    assert engine._router.objects[AT_PATH_URI] == content


# Break (same class, by file id): ``replace_file_async`` loses the replacement.
async def test_replace_with_bytes_of_another_canonical_converges_on_it(files_db):
    content = b"replacement identical to another file"
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)
    at_path, elsewhere = _seed_save_over_a_content_match(files_db, engine, content)

    try:
        result = await engine.replace_file_async(at_path["id"], content, user_id=USER_ID)
    except Exception as exc:
        pytest.fail(f"replace of {at_path['id']} was lost: {exc}")

    row = files_db.files.rows[at_path["id"]]
    assert result.file_id == at_path["id"]
    assert (row["current_version"], row["checksum"]) == (4, _sha(content))
    assert row["duplicate_of_file_id"] == elsewhere["id"]
    assert engine._router.objects[AT_PATH_URI] == content


# Break: converging aliases the path row onto the canonical's OBJECT (or leaves
# a dangling edge), so removing one side destroys or hides the other's bytes.
@pytest.mark.parametrize("mode", ["soft", "hard"])
@pytest.mark.parametrize("removed", ["path-row", "canonical"])
async def test_removing_either_side_of_a_converged_save_leaves_the_other_readable(
    files_db, removed, mode
):
    content = b"new version of an existing file"
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)
    at_path, elsewhere = _seed_save_over_a_content_match(files_db, engine, content)
    await engine.managed_write_async(FILE_PATH, content)
    for row_id in (at_path["id"], elsewhere["id"]):
        engine.permissions.allowed.update({(USER_ID, row_id, "read"), (USER_ID, row_id, "admin")})
    gone_path, kept_path, kept_id = (
        (FILE_PATH, CANONICAL_PATH, elsewhere["id"])
        if removed == "path-row"
        else (CANONICAL_PATH, FILE_PATH, at_path["id"])
    )

    assert await engine.managed_delete_async(gone_path, hard_delete=(mode == "hard"))

    assert await engine.managed_read_async(kept_path) == content
    assert [r["id"] for r in files_db.live_files()] == [kept_id]
    with pytest.raises(FileNotFoundError):
        await engine.managed_read_async(gone_path)
    if mode == "hard" and removed == "canonical":
        # FK ON DELETE SET NULL: the surviving copy is promoted to a root.
        assert files_db.files.rows[kept_id]["duplicate_of_file_id"] is None


async def test_trashed_row_at_the_same_path_does_not_block_a_new_upload(files_db):
    """Break: a lookup that sees trashed rows turns the soft-deleted file into
    the write target (a new upload lands on a row still in the trash)."""
    content = b"re-upload after trashing"
    trashed = files_db.seed_file(
        created_by=USER_ID,
        organization_id=PERSONAL_ORG,
        file_path=FILE_PATH,
        checksum=_sha(content),
        deleted_at="2026-06-14T08:18:49Z",
    )
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)

    result = await engine.managed_write_async(FILE_PATH, content)

    assert result.is_new is True
    assert result.file_id != trashed["id"]
    assert files_db.files.rows[result.file_id]["deleted_at"] is None
    assert [r["id"] for r in files_db.live_files()] == [result.file_id]


async def test_trashed_duplicate_target_is_refused_before_storage(files_db):
    """Break: equivalence validation reads trashed rows, so a force-copy could
    point its duplicate_of_file_id at a file in the trash."""
    content = b"intentional copy"
    trashed = _seed_canonical(files_db, content, deleted_at="2026-06-14T08:18:49Z")
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)

    with pytest.raises(ValueError, match="identical content"):
        await engine.managed_write_async(
            FILE_PATH, content, duplicate_of_file_id=trashed["id"]
        )

    assert engine._router.objects == {}


async def test_canonical_insert_race_converges_on_the_callers_winner(files_db):
    """A concurrent write of the same bytes wins the canonical slot between the
    lookup (miss) and our INSERT. The real ``cld_files_dedup_canonical`` violation
    fires; recovery must re-query in the caller's scope, return the winner,
    delete our orphan object, and record no version.

    Break: winner re-queried in the wrong scope, orphan leaked, or a second
    version recorded."""
    content = b"raced upload bytes"
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)
    winner: dict[str, Any] = {}

    def concurrent_winner(values: dict[str, Any]) -> None:
        files_db.files.before_create.clear()
        winner.update(
            files_db.seed_file(
                created_by=USER_ID,
                organization_id=PERSONAL_ORG,
                file_path="docs/canonical_raced.pdf",
                checksum=_sha(content),
                storage_uri="s3://test-bucket/user-1/race-winner",
            )
        )

    files_db.files.before_create.append(concurrent_winner)

    result = await engine.managed_write_async(FILE_PATH, content)

    assert result.file_id == winner["id"]
    assert result.is_new is False
    assert result.storage_uri == "s3://test-bucket/user-1/race-winner"
    assert engine._router.objects == {}
    assert engine.versions.recorded == []
    assert [r["id"] for r in files_db.live_files()] == [winner["id"]]
