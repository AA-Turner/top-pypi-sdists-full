"""A machine's file or a device's write is never the person's file or recent activity.

The guard for the 2026-09-24 incident: the desktop coding-session recorder filed
64,261 ``artifact_kind='coding_session_artifact'`` rows into a person's storage,
``files.is_user_visible_path`` called them his files, and they filled his Files
tree and every row of his Recents. Owner ruling (Arman, 2026-09-24; folder-sync
DECISIONS R3/R5): files a machine or a device writes are never the person's files
or recent activity; Recents shows only files the person created or edited in the app.

This test WRITES five real rows (and one device) -- as the shared test identity admin@admin.com,
inside ONE transaction that is always rolled back -- and asks the database's own
doors, never a re-statement of the rule:

* the browser's door, ``files.get_user_file_tree`` (scope ``'tree'``), for the Files tree;
* ``files.is_recent_activity(files.files)`` for Recents (matrx-frontend's Recents
  view applies exactly this rule, mirrored and parity-guarded by
  ``pnpm check:user-visible-parity``).

Expected: the person's upload is in the tree and in Recents; a produced artifact
(anywhere, and under ``coding-sessions/``) is in neither; a device-synced file IS
in the tree (a synced folder holds the person's own files, D16) but is NOT recent
activity.

Rule + registry: common-docs ``systems/files/file-service/USER_FILES_VS_MACHINE_FILES.md``.
"""

from __future__ import annotations

import json
import os
import uuid

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

_REQUIRED_ENV = ("SUPABASE_MATRIX_HOST", "SUPABASE_MATRIX_PASSWORD")
_TEST_IDENTITY = "admin@admin.com"


class _Rollback(Exception):
    """Raised to end the transaction; nothing this test writes may survive it."""


def _skip_without_db() -> None:
    missing = [n for n in _REQUIRED_ENV if not os.environ.get(n)]
    if missing:
        pytest.skip(f"platform database unavailable: {', '.join(missing)} unset")


async def test_machine_and_device_rows_never_reach_the_persons_tree_or_recents() -> None:
    _skip_without_db()
    asyncpg = pytest.importorskip("asyncpg")
    from matrx_files.db import bootstrap_db, connection_url

    bootstrap_db()
    conn = await asyncpg.connect(connection_url())
    verdict: dict[str, dict[str, bool]] = {}
    try:
        user_id = await conn.fetchval(
            "select id from auth.users where email = $1", _TEST_IDENTITY
        )
        assert user_id, (
            f"{_TEST_IDENTITY} does not exist on this database; the guard needs the "
            "shared test identity and never borrows a real person's account."
        )
        org_id = await conn.fetchval(
            "select organization_id from iam.organization_member"
            " where user_id = $1 order by organization_id limit 1",
            user_id,
        )
        assert org_id, f"{_TEST_IDENTITY} belongs to no organization on this database"

        tag = f"zz-machine-guard-{uuid.uuid4().hex[:10]}"
        try:
            async with conn.transaction():
                await conn.execute("SET LOCAL lock_timeout = '3s'")
                await conn.execute("SET LOCAL statement_timeout = '60s'")
                device_id = await conn.fetchval(
                    "insert into public.app_instances (user_id, instance_id, organization_id)"
                    " values ($1, $2, $3) returning id",
                    user_id,
                    f"{tag}-device",
                    org_id,
                )

                async def insert(name: str, path: str, **cols: object) -> str:
                    columns = ["created_by", "organization_id", "file_path", "file_name", "storage_uri"]
                    values: list[object] = [user_id, org_id, path, name, f"s3://guard/{tag}/{name}"]
                    for key, value in cols.items():
                        columns.append(key)
                        values.append(value)
                    placeholders = ", ".join(f"${i + 1}" for i in range(len(values)))
                    row_id = await conn.fetchval(
                        f"insert into files.files ({', '.join(columns)})"
                        f" values ({placeholders}) returning id::text",
                        *values,
                    )
                    return row_id

                ids = {
                    "person_upload": await insert("person.txt", f"{tag}/person.txt"),
                    "artifact_anywhere": await insert(
                        "artifact.md",
                        f"{tag}/artifact.md",
                        artifact_kind="coding_session_artifact",
                    ),
                    "artifact_in_namespace": await insert(
                        "log.md",
                        f"coding-sessions/claude_code/{tag}/log.md",
                        artifact_kind="coding_session_artifact",
                    ),
                    "machine_namespace_no_kind": await insert(
                        "shot.png", f"tool-images/{tag}/shot.png"
                    ),
                    "device_synced": await insert(
                        "synced.txt", f"{tag}/synced.txt", origin_device_id=device_id
                    ),
                    # A service carried it for the organization (upload_for_organization):
                    # browsable in the org's tree, never the person's recent activity.
                    "carried_for_organization": await insert(
                        "original.json.gz",
                        f"page-captures-{org_id}/scrape_parsed_page/{tag}/original.json.gz",
                    ),
                }

                tree: set[str] = set()
                offset = 0
                while True:
                    payload = await conn.fetchval(
                        "select files.get_user_file_tree($1::uuid, 5000, $2::int,"
                        " false, false, 'updated_at_desc', 'tree')",
                        user_id,
                        offset,
                    )
                    page = json.loads(payload) if isinstance(payload, str) else payload
                    page = page or []
                    tree.update(str(r["id"]) for r in page if r.get("kind") == "file")
                    if len(page) < 5000:
                        break
                    offset += 5000

                for label, row_id in ids.items():
                    recent = await conn.fetchval(
                        "select files.is_recent_activity(f.*) from files.files f where f.id = $1::uuid",
                        row_id,
                    )
                    verdict[label] = {"tree": row_id in tree, "recents": bool(recent)}
                raise _Rollback
        except _Rollback:
            pass
    finally:
        await conn.close()

    expected = {
        "person_upload": {"tree": True, "recents": True},
        "artifact_anywhere": {"tree": False, "recents": False},
        "artifact_in_namespace": {"tree": False, "recents": False},
        "machine_namespace_no_kind": {"tree": False, "recents": False},
        "device_synced": {"tree": True, "recents": False},
        "carried_for_organization": {"tree": True, "recents": False},
    }
    assert verdict == expected, (
        "A machine's or a device's file reached the person's Files or Recents "
        "(or the person's own upload did not).\n"
        f"  got:      {verdict}\n  expected: {expected}\n"
        "The one rule lives in matrx_files/user_visible.py -> files.is_user_visible* / "
        "files.is_recent_activity*; see common-docs systems/files/file-service/USER_FILES_VS_MACHINE_FILES.md."
    )
