"""THE name validator: a name the server accepts must be one a device can create.

Migration 035 fixed the ORDER of `rename_file`'s checks. The re-verify then ran
every input past the amended body and found the CLASS still open: `.`, `..`, a
300-character name and a name containing a newline were all ACCEPTED and written
into `file_path`. `pdf-extractions/..` is a path no sync daemon can materialise,
and `basename('…/..') == '..'`, so the drift census stays green on it — it would
corrupt a replica in silence, which is the worst shape a defect can take here.

Migration 037 moves the whole rule into ONE function, `files.assert_safe_file_name`,
so `rename_file`, `move_file`, the upload routes and the conflict-copy renderer
cannot grow separate opinions about what a legal name is. These tests exercise
that function directly (every rule, cheaply) and then prove `rename_file` really
delegates to it.

SELECT only — the validator is IMMUTABLE and touches no row.
"""

from __future__ import annotations

import os

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

_REQUIRED_ENV = ("SUPABASE_MATRIX_HOST", "SUPABASE_MATRIX_PASSWORD")

#: SPEC-ENGINE §2: `sync.max_segment_chars`, org · device, default 255 — the
#: per-segment ceiling of APFS, ext4 and NTFS alike.
MAX_SEGMENT = 255

REFUSED = [
    ("a/b", "ONE path segment", "a slash is a path, not a name"),
    ("trailing/", "ONE path segment", "checked on the caller's own string, before any trim"),
    ("/leading", "ONE path segment", "same"),
    ("back\\slash", "ONE path segment", "backslash is Windows's separator"),
    (".", '"." and ".."', "names a directory, not a file"),
    ("..", '"." and ".."', "a path no device can materialise"),
    ("", "empty", "nothing to name"),
    # Whitespace-only trips the EDGE-whitespace rule before the empty rule; both
    # refuse it, and the message names the one that actually fired.
    ("   ", "whitespace", "whitespace-only is not a name"),
    (" leading.txt", "whitespace", "Windows would disagree with us about the name"),
    # A trailing SPACE is edge whitespace; a trailing DOT has its own rule.
    ("trailing.txt ", "whitespace", "Windows silently drops it"),
    ("trailing.", "trailing dot or space", "Windows silently drops it"),
    ("a\nb.txt", "control character", "a newline breaks every line-oriented tool"),
    ("a\tb.txt", "control character", "same class"),
    ("x" * (MAX_SEGMENT + 1), "exceeds", "longer than any supported filesystem accepts"),
    ("CON", "reserved Windows device name", "cannot exist as a file on Windows"),
    ("con.txt", "reserved Windows device name", "extension does not rescue it"),
    ("AuX.log", "reserved Windows device name", "case does not either"),
    ("COM1.txt", "reserved Windows device name", "the numbered devices too"),
    ("LPT9", "reserved Windows device name", "and the printers"),
]

ACCEPTED = [
    ("report.txt", "report.txt"),
    ("x" * MAX_SEGMENT, "x" * MAX_SEGMENT),
    ("CONTRACT.txt", "CONTRACT.txt"),      # a PREFIX of CON is not CON
    ("com10.txt", "com10.txt"),            # only COM1-9 are devices
    ("my.file.name.txt", "my.file.name.txt"),
    ("a b.txt", "a b.txt"),                # interior spaces are ordinary
    ("café.txt", "café.txt"),   # NFD in, NFC out — one file on every OS
]


def _skip_without_db() -> None:
    missing = [n for n in _REQUIRED_ENV if not os.environ.get(n)]
    if missing:
        pytest.skip(f"live platform database unavailable: {', '.join(missing)} unset")


async def _conn():
    from matrx_orm import acquire_connection

    from matrx_files.db import bootstrap_db

    return acquire_connection(bootstrap_db())


@pytest.mark.parametrize(("name", "expected_reason", "why"), REFUSED, ids=[r[0][:24] or "empty" for r in REFUSED])
async def test_an_unmaterialisable_name_is_refused(name, expected_reason, why) -> None:
    _skip_without_db()
    import asyncpg

    async with await _conn() as conn:
        with pytest.raises(asyncpg.PostgresError) as exc:
            await conn.fetchval("SELECT files.assert_safe_file_name($1)", name)
    assert exc.value.sqlstate == "22023", f"{name!r} raised {exc.value.sqlstate} ({why})"
    assert expected_reason in str(exc.value), (
        f"{name!r} was refused, but the message does not name the rule: {exc.value}"
    )


@pytest.mark.parametrize(("name", "becomes"), ACCEPTED)
async def test_a_legal_name_survives_unchanged_except_for_nfc(name, becomes) -> None:
    _skip_without_db()
    async with await _conn() as conn:
        got = await conn.fetchval("SELECT files.assert_safe_file_name($1)", name)
    assert got == becomes


async def test_the_limit_comes_from_the_knob_not_a_constant() -> None:
    """`sync.max_segment_chars` is a knob; the validator must read it."""
    _skip_without_db()
    import asyncpg

    async with await _conn() as conn:
        tx = conn.transaction()
        await tx.start()
        try:
            await conn.execute("SELECT set_config('matrx.max_segment_chars','8',true)")
            assert await conn.fetchval("SELECT files.assert_safe_file_name($1)", "12345678")
            with pytest.raises(asyncpg.PostgresError) as exc:
                await conn.fetchval("SELECT files.assert_safe_file_name($1)", "123456789")
            assert exc.value.sqlstate == "22023"
            assert "exceeds the 8" in str(exc.value)
        finally:
            await tx.rollback()


async def test_rename_file_delegates_to_the_one_validator() -> None:
    """Red if rename_file grows its own copy of the rule and they drift."""
    _skip_without_db()
    async with await _conn() as conn:
        src = await conn.fetchval(
            "SELECT prosrc FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace "
            "WHERE n.nspname='public' AND p.proname='rename_file'"
        )
    assert "files.assert_safe_file_name(" in src, (
        "public.rename_file no longer calls the shared validator — a second opinion "
        "about what a legal name is is a second rule the daemon does not share."
    )
    for stale in ("position('/' in v_raw)", "normalize(v_raw, NFC)"):
        assert stale not in src, f"rename_file still carries its own inline rule: {stale}"


@pytest.mark.parametrize("name", [".", "..", "a\nb.txt", "x" * 300])
async def test_the_residual_names_reach_rename_file_and_are_refused(name: str) -> None:
    """End to end: the four the re-verify proved were ACCEPTED and written."""
    _skip_without_db()
    import asyncpg
    import uuid as _uuid

    async with await _conn() as conn:
        tx = conn.transaction()
        await tx.start()
        try:
            seed = await conn.fetchrow(
                "SELECT user_id::text AS owner, organization_id::text AS org "
                "FROM public.app_instances WHERE deleted_at IS NULL "
                "AND organization_id IS NOT NULL LIMIT 1"
            )
            if seed is None:
                pytest.skip("no seed identity available")
            tag = _uuid.uuid4().hex[:10]
            file_id = await conn.fetchval(
                "INSERT INTO files.files (created_by, organization_id, file_path, file_name, "
                "storage_uri, mime_type, size_bytes) "
                "VALUES ($1::uuid,$2::uuid,$3,$4,$5,'text/plain',3) RETURNING id::text",
                seed["owner"], seed["org"], f"NameProbe/{tag}/original.txt",
                "original.txt", f"s3://probe/{tag}",
            )
            sp = conn.transaction()
            await sp.start()
            with pytest.raises(asyncpg.PostgresError) as exc:
                await conn.fetchval("SELECT public.rename_file($1::uuid, $2)", file_id, name)
            await sp.rollback()
            assert exc.value.sqlstate == "22023"
            still = await conn.fetchval(
                "SELECT file_name FROM files.files WHERE id = $1::uuid", file_id
            )
            assert still == "original.txt"
        finally:
            await tx.rollback()
