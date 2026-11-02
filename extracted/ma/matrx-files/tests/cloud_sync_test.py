"""Cloud sync integration test.

Tests the full round-trip: upload → retrieve → permission checks.

Uses the real developer user from .env — no fakes, no mocks. This is a manual
script, NOT an automated pytest suite (its functions take an ``engine`` arg and
require live AWS S3 + Supabase credentials), so it is excluded from pytest
collection via ``tests/conftest.py``. Run it by hand from the
packages/matrx-utils directory:

    python tests/cloud_sync_test.py
"""

import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent.parent / ".env")

from matrx_utils import vcprint, clear_terminal
from matrx_files import FileManager
from matrx_files.cloud_sync import CloudSyncConfig


# ---------------------------------------------------------------------------
# Real developer identity — never fake
# ---------------------------------------------------------------------------

DEVELOPER_USER_ID = os.environ.get("TEST_ADMIN_USER_ID", "").strip()
if not DEVELOPER_USER_ID:
    raise EnvironmentError(
        "TEST_ADMIN_USER_ID is not set in .env. "
        "It must be the admin@admin.com test account's UUID (tests never act as a real person)."
    )


# ---------------------------------------------------------------------------
# Build a FileManager with cloud sync enabled
# ---------------------------------------------------------------------------

def make_fm(user_id: str) -> FileManager:
    """Create a FileManager backed by cloud sync for the given user."""
    config = CloudSyncConfig(user_id=user_id)
    return FileManager("cloud_sync_test", new_instance=True, cloud_sync=config)


# ---------------------------------------------------------------------------
# Test functions — no logic, just operations
# ---------------------------------------------------------------------------

async def test_upload_private_file(engine) -> dict:
    return (await engine.managed_write_async(
        "tests/hello_private.txt",
        "Hello from cloud sync - private file.",
        visibility="personal",
        change_summary="initial upload",
    )).model_dump()


async def test_retrieve_file(engine) -> bytes:
    return await engine.managed_read_async("tests/hello_private.txt")


async def test_upload_public_file(engine) -> dict:
    return (await engine.managed_write_async(
        "tests/hello_public.txt",
        "Hello from cloud sync - public file.",
        visibility="public",
        change_summary="initial upload",
    )).model_dump()


async def test_list_files(engine) -> list:
    return await engine.list_files_async()


async def test_file_versions(engine, file_id: str) -> list:
    return await engine._db.list_versions_async(file_id)


async def test_share_file(engine, grantee_id: str) -> dict:
    """Upload a file and share it with another user."""
    return (await engine.managed_write_async(
        "tests/hello_shared.txt",
        "Hello from cloud sync - shared with a grantee.",
        visibility="personal",
        share_with=[grantee_id],
        share_level="read",
        change_summary="shared upload",
    )).model_dump()


async def test_permission_check(engine, file_id: str) -> str | None:
    """Check what permission the current user has on their own file."""
    result = await engine._db.get_user_permission_async(file_id, "file", DEVELOPER_USER_ID)
    return result


async def test_list_permissions(engine, file_id: str) -> list:
    return await engine._db.list_permissions_async(file_id, "file")


async def test_get_file_metadata(engine, file_path: str) -> dict | None:
    return await engine._db.get_file_by_path_async(DEVELOPER_USER_ID, file_path)


# ---------------------------------------------------------------------------
# Main — run everything and vcprint results
# ---------------------------------------------------------------------------

async def main():
    fm = make_fm(DEVELOPER_USER_ID)
    engine = fm.sync_engine

    vcprint(
        {"user_id": DEVELOPER_USER_ID, "bucket": engine._config.resolve_s3_bucket()},
        "[CLOUD SYNC TEST] Config",
        color="cyan",
    )

    # 1. Upload a private file
    upload_result = await test_upload_private_file(engine)
    vcprint(upload_result, "[CLOUD SYNC TEST] 1. Upload private file", color="green")

    file_id = upload_result["file_id"]

    # 2. Retrieve the same file
    content = await test_retrieve_file(engine)
    vcprint(
        {"bytes": len(content), "content": content.decode()},
        "[CLOUD SYNC TEST] 2. Retrieve private file",
        color="green",
    )

    # 3. Check file metadata in DB
    metadata = await test_get_file_metadata(engine, "tests/hello_private.txt")
    vcprint(metadata, "[CLOUD SYNC TEST] 3. File metadata from DB", color="blue")

    # 4. Version history
    versions = await test_file_versions(engine, file_id)
    vcprint(versions, "[CLOUD SYNC TEST] 4. Version history", color="blue")

    # 5. Upload a public file
    public_result = await test_upload_public_file(engine)
    vcprint(public_result, "[CLOUD SYNC TEST] 5. Upload public file", color="green")

    # 6. List all files
    all_files = await test_list_files(engine)
    vcprint(all_files, "[CLOUD SYNC TEST] 6. All files for user", color="cyan")

    # 7. Share a file (share with yourself — proves the ACL path without needing
    #    a second real user; in production this would be another user's UUID)
    shared_result = await test_share_file(engine, grantee_id=DEVELOPER_USER_ID)
    vcprint(shared_result, "[CLOUD SYNC TEST] 7. Upload + share file", color="green")

    # 8. List permissions on the shared file
    perms = await test_list_permissions(engine, shared_result["file_id"])
    vcprint(perms, "[CLOUD SYNC TEST] 8. Permissions on shared file", color="yellow")


if __name__ == "__main__":
    clear_terminal()
    asyncio.run(main())
