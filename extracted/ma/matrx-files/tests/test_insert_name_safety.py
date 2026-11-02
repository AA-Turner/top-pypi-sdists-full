"""The name rule runs on INSERT too — not only on the one path a human types.

Migration 037 built ONE validator and pointed `rename_file` at it. A rename is
the rarest way a name reaches `files.files`: every upload, every TUS finalize,
every presigned lane, every service writer and every hand INSERT walked past it.
Migration 044 puts the UNIVERSAL half of the rule on a BEFORE INSERT trigger, so
a name no filesystem anywhere can hold cannot enter the table by any road.

The split this file pins, and why it is the ruling rather than a softening:

* **Universal** — `/`, control characters, `.`/`..`, empty, over the segment
  limit. Each one CORRUPTS THE PATH ITSELF and no device can materialise it.
  Refused on INSERT. Live offenders before 044: 0 of 241,523 rows, every rule.
* **Windows-only** — `< > : " | ? *`, a trailing dot or space, `CON`/`AUX`/…,
  a backslash, edge whitespace. Still refused on RENAME (a name a human just
  typed). ACCEPTED on INSERT, because the device already created the file and
  THE CLOUD NEVER RENAMES USER DATA — a Windows device shows the named state
  with a remedy (SPEC-ENGINE §5). This is the 11 `Scans/` rows' own ruling,
  applied at the moment of arrival: those rows are `Scan Aug 17 2:01 AM.pdf`,
  the owner's macOS scanner, still in use; and `coding-sessions/.../con.py`
  (2026-09-16) is an ordinary legal Python file in a repository.
* **NFC** — normalized, never refused. macOS hands out NFD; refusing it would
  break every macOS upload, and NFD and NFC are the SAME name. The trigger
  carries the normalization into `file_path`'s final segment in the same
  statement, so the two columns cannot disagree.

Every write here happens inside a transaction that is always rolled back.
"""

from __future__ import annotations

import os
import uuid as _uuid

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

_REQUIRED_ENV = ("SUPABASE_MATRIX_HOST", "SUPABASE_MATRIX_PASSWORD")

#: Refused on INSERT: the path itself is corrupt, on every operating system.
UNIVERSAL_OFFENDERS = [
    (".", '"." and ".."'),
    ("..", '"." and ".."'),
    ("a/b.txt", "ONE path segment"),
    ("a\nb.txt", "control character"),
    ("a\tb.txt", "control character"),
    ("x" * 300, "exceeds"),
    ("   ", "empty or only whitespace"),
    ("", "empty or only whitespace"),
]

#: ACCEPTED on INSERT and REFUSED on rename. The ruling, in one list.
WINDOWS_ONLY = [
    ("Scan Aug 17 2:01 AM.pdf", "the owner's macOS scanner writes the colon itself"),
    ("con.py", "a legal Python file on macOS and Linux"),
    ("trailing.", "Windows drops the dot; macOS does not"),
    ('x<y>z.txt', "Windows-illegal punctuation, POSIX-legal"),
    (" leading.txt", "Windows strips the space; macOS keeps it"),
    ("back\\slash.txt", "backslash is a separator only on Windows"),
]


def _skip_without_db() -> None:
    missing = [n for n in _REQUIRED_ENV if not os.environ.get(n)]
    if missing:
        pytest.skip(f"live platform database unavailable: {', '.join(missing)} unset")


async def _conn():
    from matrx_orm import acquire_connection

    from matrx_files.db import bootstrap_db

    return acquire_connection(bootstrap_db())


async def _seed(conn):
    """admin@admin.com and an organization it belongs to — never anyone else.

    Resolved from the data on whatever database this run reaches (since
    2026-09-23 pytest is repointed off the live database by
    matrx_orm.pytest_live_db_guard), never a hardcoded uuid, never an arbitrary
    device owner. The organization is passed explicitly on every write.
    """
    row = await conn.fetchrow(
        "SELECT u.id::text AS owner, m.organization_id::text AS org "
        "FROM auth.users u JOIN iam.memberships m ON m.user_id = u.id "
        "WHERE u.email = 'admin@admin.com' AND m.deleted_at IS NULL "
        "AND m.organization_id IS NOT NULL ORDER BY m.created_at LIMIT 1"
    )
    if row is None:
        pytest.skip("admin@admin.com has no organization membership on this database")
    return row


async def _insert(conn, owner: str, org: str, name: str) -> str:
    """A RAW insert — no route, no RPC, nothing that could sanitise on the way."""
    tag = _uuid.uuid4().hex[:10]
    return await conn.fetchval(
        "INSERT INTO files.files (created_by, organization_id, file_path, file_name, "
        "storage_uri, mime_type, size_bytes) "
        "VALUES ($1::uuid,$2::uuid,$3,$4,$5,'text/plain',3) RETURNING id::text",
        owner, org, f"InsertNameProbe/{tag}/{name}", name, f"s3://probe/{tag}",
    )


# --------------------------------------------------------------- the red half ----


@pytest.mark.parametrize(
    ("name", "expected_reason"), UNIVERSAL_OFFENDERS,
    ids=[n[:20] or "empty" for n, _ in UNIVERSAL_OFFENDERS],
)
async def test_a_universal_offender_cannot_be_inserted_by_any_writer(
    name: str, expected_reason: str
) -> None:
    """Red before 044: every one of these landed, by INSERT, in silence.

    `basename('…/..') == '..'`, so the drift census stays GREEN on it — the row
    corrupts a replica without any surface saying so, which is the worst shape a
    defect here can take.
    """
    _skip_without_db()
    import asyncpg

    async with await _conn() as conn:
        tx = conn.transaction()
        await tx.start()
        try:
            seed = await _seed(conn)
            sp = conn.transaction()
            await sp.start()
            with pytest.raises(asyncpg.PostgresError) as exc:
                await _insert(conn, seed["owner"], seed["org"], name)
            await sp.rollback()
            assert exc.value.sqlstate == "22023", (
                f"{name!r} was rejected by something other than the name rule: "
                f"{exc.value.sqlstate} {exc.value}"
            )
            assert expected_reason in str(exc.value), (
                f"{name!r} was refused but the message does not name the rule: {exc.value}"
            )
            left_behind = await conn.fetchval(
                "SELECT count(*) FROM files.files WHERE file_name = $1 "
                "AND file_path LIKE 'InsertNameProbe/%'", name,
            )
            assert left_behind == 0
        finally:
            await tx.rollback()


# ------------------------------------------------------------- the green half ----


@pytest.mark.parametrize(("name", "why"), WINDOWS_ONLY, ids=[n[:20] for n, _ in WINDOWS_ONLY])
async def test_a_windows_only_name_is_accepted_on_insert_and_refused_on_rename(
    name: str, why: str
) -> None:
    """Both halves of the ruling, in one test, so neither can drift alone.

    If the INSERT half ever starts refusing these, the owner cannot scan a
    document any more. If the RENAME half ever stops refusing them, a user can
    deliberately type a name their own Windows device can never hold.
    """
    _skip_without_db()
    import asyncpg

    async with await _conn() as conn:
        tx = conn.transaction()
        await tx.start()
        try:
            seed = await _seed(conn)
            file_id = await _insert(conn, seed["owner"], seed["org"], name)
            assert file_id, f"INSERT refused {name!r} — {why}"
            stored = await conn.fetchval(
                "SELECT file_name FROM files.files WHERE id = $1::uuid", file_id
            )
            assert stored == name, "the cloud rewrote a name the device chose"

            with pytest.raises(asyncpg.PostgresError) as exc:
                await conn.fetchval("SELECT files.assert_safe_file_name($1)", name)
            assert exc.value.sqlstate == "22023", (
                f"rename no longer refuses {name!r} — the Windows-only half is gone"
            )
        finally:
            await tx.rollback()


async def test_an_ordinary_name_is_untouched() -> None:
    """Falsifiability: a trigger that refused everything would pass the red half."""
    _skip_without_db()
    async with await _conn() as conn:
        tx = conn.transaction()
        await tx.start()
        try:
            seed = await _seed(conn)
            file_id = await _insert(conn, seed["owner"], seed["org"], "report.txt")
            row = await conn.fetchrow(
                "SELECT file_name, file_path FROM files.files WHERE id = $1::uuid", file_id
            )
            assert row["file_name"] == "report.txt"
            assert row["file_path"].endswith("/report.txt")
        finally:
            await tx.rollback()


async def test_nfd_arrives_and_is_stored_nfc_in_both_columns() -> None:
    """One file, not two. macOS hands out NFD and Linux NFC.

    The column pair is the point: normalizing `file_name` alone would make
    `file_name <> basename(file_path)` — the exact drift §4.4 censuses for.
    """
    _skip_without_db()
    nfd = "café.txt"
    nfc = "café.txt"
    assert nfd != nfc and len(nfd) == 9 and len(nfc) == 8

    async with await _conn() as conn:
        tx = conn.transaction()
        await tx.start()
        try:
            seed = await _seed(conn)
            file_id = await _insert(conn, seed["owner"], seed["org"], nfd)
            row = await conn.fetchrow(
                "SELECT file_name, file_path FROM files.files WHERE id = $1::uuid", file_id
            )
            assert row["file_name"] == nfc, "the NFD name was stored unnormalised"
            assert row["file_path"].endswith(f"/{nfc}"), (
                f"file_path was left in NFD while file_name was normalized: {row['file_path']!r}"
            )
        finally:
            await tx.rollback()


# ------------------------------------------------------------- the class, live ----


async def test_the_trigger_is_attached_to_files_files_on_insert_only() -> None:
    """An UPDATE is migration 038's business; the 11 alive rows are a ruling."""
    _skip_without_db()
    async with await _conn() as conn:
        row = await conn.fetchrow(
            "SELECT pg_get_triggerdef(t.oid) AS def FROM pg_trigger t "
            "JOIN pg_class c ON c.oid = t.tgrelid "
            "JOIN pg_namespace n ON n.oid = c.relnamespace "
            "WHERE n.nspname='files' AND c.relname='files' "
            "AND t.tgname='guard_file_name_safety' AND NOT t.tgisinternal"
        )
    assert row is not None, "files.files has no INSERT name-safety trigger at all"
    definition = row["def"]
    assert "BEFORE INSERT" in definition, definition
    assert "UPDATE" not in definition, (
        f"the trigger also fires on UPDATE: {definition}. The 11 alive rows with "
        "Windows-illegal names STAY, and 038 already owns the UPDATE path."
    )


async def test_the_validator_is_one_function_not_two_opinions() -> None:
    """`assert_safe_file_name` inherits the universal half; it does not copy it."""
    _skip_without_db()
    async with await _conn() as conn:
        full = await conn.fetchval(
            "SELECT prosrc FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace "
            "WHERE n.nspname='files' AND p.proname='assert_safe_file_name'"
        )
        trigger = await conn.fetchval(
            "SELECT prosrc FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace "
            "WHERE n.nspname='files' AND p.proname='guard_file_name_safety'"
        )
    for src, who in ((full, "assert_safe_file_name"), (trigger, "guard_file_name_safety")):
        assert "files.assert_storable_file_name(" in src, (
            f"{who} no longer delegates to the universal half — a second opinion "
            "about what a legal name is is a second rule the daemon does not share."
        )
    for stale in ("[[:cntrl:]]", "IN ('.', '..')"):
        assert stale not in full, (
            f"assert_safe_file_name grew its own copy of a universal rule: {stale}"
        )


async def test_existing_windows_illegal_rows_still_read_unchanged() -> None:
    """The ruling, as an invariant true on ANY database this run reaches.

    The 11 `Scans/` rows are a fact about the LIVE corpus, and since 2026-09-23
    pytest never reaches the live database (matrx_orm.pytest_live_db_guard). So
    the count is proven live out of band (round-3 report: 11 before 044, 11
    after) and this test pins what must hold wherever such rows exist: they are
    still readable, and neither column was rewritten out of step with the other.
    An empty target proves nothing, so it says so instead of passing.
    """
    _skip_without_db()
    async with await _conn() as conn:
        rows = await conn.fetch(
            "SELECT file_name, file_path FROM files.files "
            "WHERE file_name ~ '[<>:\"|?*]' AND deleted_at IS NULL"
        )
    if not rows:
        pytest.skip(
            "no Windows-illegal rows on this database (not the live corpus); "
            "the live count is verified out of band"
        )
    for row in rows:
        assert row["file_path"].endswith(row["file_name"]), (
            f"{row['file_name']!r} no longer matches its path — something rewrote user data"
        )
