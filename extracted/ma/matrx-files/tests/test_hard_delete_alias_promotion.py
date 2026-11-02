"""Hard-deleting a dedup canonical never refuses, strands or purges its aliases.

Owner ruling (2026-09-10): when a canonical ``files.files`` row is hard-deleted,
exactly ONE surviving alias is promoted to canonical — live before trashed, then
oldest ``created_at``, tie -> smallest id — and every other alias is repointed
at it, in the same transaction; the storage purge never deletes an object a
surviving row still references. An alias whose key (organization, owner,
checksum) another live canonical root already holds converges on THAT root
instead: promoting it would violate ``cld_files_dedup_canonical``, which is the
dedup invariant and is never relaxed.

The defect this pins (live 2026-09-10, 864 canonicals exposed): ``FOREIGN KEY
duplicate_of_file_id ... ON DELETE SET NULL`` turned 2+ aliases into canonical
roots with the same key, the DELETE raised 23505 and the file could never be
hard-deleted. The ORM fallback cascade nulled every alias explicitly — same
23505.

ONE scenario table with literal expected outcomes runs through three executors:

* ``sql`` — the package's LATEST migration defining ``public.hard_delete_file``,
  executed verbatim on a throwaway local PostgreSQL whose tables carry the
  unique indexes and self-FKs captured live from Matrx Main (2026-09-10). This
  IS the production function; nothing about it is doubled.
* ``orm-fallback`` — ``DatabaseClient.hard_delete_file_fallback_async``, the
  production Python cascade the engine uses when the RPC fails, over the
  in-memory double that enforces the same unique indexes and SET NULL FKs.
* ``double-rpc`` — the double's model of the SQL function. Every engine test
  relies on it, so it is held to the same literals and cannot drift from the
  real function.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import shutil
import socket
import subprocess
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import matrx_files
import pytest

from _files_db_double import FilesDB, UniqueViolation, build_engine

# ---------------------------------------------------------------------------
# Scenario table
# ---------------------------------------------------------------------------

ORG = "0a000000-0000-4000-8000-000000000001"
OWNER = "0b000000-0000-4000-8000-000000000001"
TRASHED_AT = "2026-09-10T01:00:00+00:00"
URI_PREFIX = "s3://test-bucket/"

_NAMES = ("C", "A1", "A2", "A3", "T", "L", "R", "S1", "S2", "SY", "RY", "V")
# Suffix order == uuid byte order, so "smallest id" is decidable by eye.
ID = {name: f"00000000-0000-4000-8000-{n:012d}" for n, name in enumerate(_NAMES, 1)}
NAME = {v: k for k, v in ID.items()}


def uri(label: str) -> str:
    """``C`` is row C's own object; ``C.v1`` is its version-1 object."""
    return URI_PREFIX + label


@dataclass(frozen=True)
class Row:
    name: str
    second: int  # created_at = 2026-09-10T00:00:<second>Z
    checksum: str | None = "K"
    dup: str | None = None
    parent: str | None = None
    trashed: bool = False
    versions: tuple[str, ...] = ()  # file_versions.storage_uri labels, v1..vN


@dataclass(frozen=True)
class Scenario:
    id: str
    rows: tuple[Row, ...]  # inserted in this order
    delete: str
    remaining: dict[str, str | None]  # every surviving row -> row its duplicate_of_file_id names
    main: str | None
    versions: frozenset[str]
    main_retained: bool = False
    retained: frozenset[str] = field(default_factory=frozenset)


SCENARIOS = [
    Scenario(
        "0-aliases",
        rows=(Row("C", 1, versions=("C.v1",)),),
        delete="C",
        remaining={},
        main="C",
        versions=frozenset({"C.v1"}),
    ),
    Scenario(
        "1-alias-is-promoted",
        rows=(Row("C", 1, versions=("C.v1",)), Row("A1", 5, dup="C")),
        delete="C",
        remaining={"A1": None},
        main="C",
        versions=frozenset({"C.v1"}),
    ),
    Scenario(
        # Inserted newest-first: insertion order must not decide the heir.
        "2-aliases-oldest-promoted-other-repointed",
        rows=(Row("C", 1, versions=("C.v1",)), Row("A2", 7, dup="C"), Row("A1", 5, dup="C")),
        delete="C",
        remaining={"A1": None, "A2": "A1"},
        main="C",
        versions=frozenset({"C.v1"}),
    ),
    Scenario(
        # A3 and A1 share created_at; the smaller id (A1) wins the tie.
        "3-aliases-created-at-tie-smallest-id-promoted",
        rows=(
            Row("C", 1),
            Row("A2", 9, dup="C"),
            Row("A3", 5, dup="C"),
            Row("A1", 5, dup="C"),
        ),
        delete="C",
        remaining={"A1": None, "A2": "A1", "A3": "A1"},
        main="C",
        versions=frozenset(),
    ),
    Scenario(
        "live-alias-outranks-an-older-trashed-alias",
        rows=(Row("C", 1), Row("T", 2, dup="C", trashed=True), Row("L", 6, dup="C")),
        delete="C",
        remaining={"L": None, "T": "L"},
        main="C",
        versions=frozenset(),
    ),
    Scenario(
        # Live shape (3 rows 2026-09-10): the canonical is in the trash and a
        # later upload made R the live root for the same key. Promoting A would
        # be a second root for R's key — A converges on R instead.
        "trashed-canonical-alias-converges-on-the-live-root-for-its-key",
        rows=(Row("C", 1, trashed=True), Row("A1", 3, dup="C"), Row("R", 4)),
        delete="C",
        remaining={"A1": "R", "R": None},
        main="C",
        versions=frozenset(),
    ),
    Scenario(
        # Live shape (136 stale aliases 2026-09-10): aliases whose checksum no
        # longer matches the canonical regroup by THEIR OWN key.
        "stale-alias-keys-regroup-by-their-own-key",
        rows=(
            Row("RY", 2, checksum="Y"),
            Row("C", 1),
            Row("A1", 3, dup="C"),
            Row("S1", 4, checksum="X", dup="C"),
            Row("S2", 5, checksum="X", dup="C"),
            Row("SY", 6, checksum="Y", dup="C"),
        ),
        delete="C",
        remaining={"RY": None, "A1": None, "S1": None, "S2": "S1", "SY": "RY"},
        main="C",
        versions=frozenset(),
    ),
    Scenario(
        # file_versions.storage_uri is not unique: a surviving alias's version
        # row can name the canonical's main object and one of its versions.
        "purge-keeps-every-object-a-surviving-row-references",
        rows=(
            Row("C", 1, versions=("C.v1", "C.v2")),
            Row("A1", 3, dup="C", versions=("C", "C.v1")),
        ),
        delete="C",
        remaining={"A1": None},
        main=None,
        versions=frozenset({"C.v2"}),
        main_retained=True,
        retained=frozenset({"C", "C.v1"}),
    ),
    Scenario(
        "derivative-children-still-cascade-and-purge",
        rows=(
            Row("C", 1, versions=("C.v1",)),
            Row("V", 2, checksum="K2", parent="C", versions=("V.v1",)),
            Row("A1", 3, dup="C"),
        ),
        delete="C",
        remaining={"A1": None},
        main="C",
        versions=frozenset({"C.v1", "V", "V.v1"}),
    ),
    # AD238 — a child's retained objects are re-checked once the parent row is gone.
    Scenario(
        # The parent's own version row is the ONLY reference to the child's main
        # object: the child keeps it, the parent's delete frees it — it must purge.
        "child-main-only-the-deleted-parent-referenced-is-purged",
        rows=(
            Row("C", 1, versions=("V",)),
            Row("V", 2, checksum="K2", parent="C"),
        ),
        delete="C",
        remaining={},
        main="C",
        versions=frozenset({"V"}),
    ),
    Scenario(
        # Same shape for a version object the child and the parent both name.
        "child-version-only-the-deleted-parent-referenced-is-purged",
        rows=(
            Row("C", 1, versions=("C.v1",)),
            Row("V", 2, checksum="K2", parent="C", versions=("C.v1",)),
        ),
        delete="C",
        remaining={},
        main="C",
        versions=frozenset({"C.v1", "V"}),
    ),
    Scenario(
        # A surviving alias still names the child's object after the parent is gone:
        # the re-check keeps it retained — never purged just because a child had it.
        "child-object-a-surviving-alias-references-stays-retained",
        rows=(
            Row("C", 1, versions=("V",)),
            Row("V", 2, checksum="K2", parent="C"),
            Row("A1", 3, dup="C", versions=("V",)),
        ),
        delete="C",
        remaining={"A1": None},
        main="C",
        versions=frozenset(),
        retained=frozenset({"V"}),
    ),
    Scenario(
        # The parent never names the child's object, so ONLY the re-check of the
        # child's retained list can report it: dropping that list instead of
        # re-checking it loses the surviving alias's reference from the report.
        "child-object-only-a-surviving-alias-references-is-reported-retained",
        rows=(
            Row("C", 1),
            Row("V", 2, checksum="K2", parent="C"),
            Row("A1", 3, dup="C", versions=("V",)),
        ),
        delete="C",
        remaining={"A1": None},
        main="C",
        versions=frozenset(),
        retained=frozenset({"V"}),
    ),
]


def _created_at(second: int) -> str:
    return f"2026-09-10T00:00:{second:02d}+00:00"


def _label(u: str | None) -> str | None:
    if u is None:
        return None
    assert u.startswith(URI_PREFIX), f"purge report named a URI outside the scenario: {u!r}"
    return u[len(URI_PREFIX) :]


def _normalize(report: Any) -> dict[str, Any]:
    if isinstance(report, str):
        report = json.loads(report)
    assert isinstance(report, dict), f"hard_delete_file returned no purge report: {report!r}"
    return {
        "main": _label(report.get("main")),
        "versions": frozenset(_label(u) for u in report.get("versions") or []),
        "main_retained": bool(report.get("main_retained")),
        "retained": frozenset(_label(u) for u in report.get("retained") or []),
    }


def _expected(sc: Scenario) -> dict[str, Any]:
    return {
        "main": sc.main,
        "versions": sc.versions,
        "main_retained": sc.main_retained,
        "retained": sc.retained,
    }


# ---------------------------------------------------------------------------
# Executor: the production SQL on a throwaway PostgreSQL
# ---------------------------------------------------------------------------

SQL_DIR = Path(matrx_files.__file__).parent / "cloud_sync" / "sql"

# Captured live from Matrx Main 2026-09-10 (information_schema.columns,
# pg_indexes, pg_constraint) — only the columns hard_delete_file reads or writes,
# with every unique index and self-FK that governs them. auth.uid() answers NULL:
# the aidream pool is a service-role caller.
FIXTURE_DDL = """
CREATE SCHEMA auth;
CREATE SCHEMA iam;
CREATE SCHEMA files;
CREATE SCHEMA platform;
CREATE FUNCTION auth.uid() RETURNS uuid LANGUAGE sql STABLE AS $$ SELECT NULL::uuid $$;
CREATE FUNCTION iam.has_access(text, uuid, text) RETURNS boolean LANGUAGE plpgsql AS $$
BEGIN RAISE EXCEPTION 'iam.has_access must not run for a service-role caller'; END $$;
CREATE TABLE files.files (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    created_by uuid NOT NULL,
    organization_id uuid NOT NULL,
    file_path text NOT NULL,
    file_name text NOT NULL,
    storage_uri text NOT NULL,
    checksum text,
    created_at timestamptz NOT NULL DEFAULT now(),
    deleted_at timestamptz,
    parent_file_id uuid,
    duplicate_of_file_id uuid,
    CONSTRAINT cld_files_duplicate_of_file_id_fkey FOREIGN KEY (duplicate_of_file_id)
        REFERENCES files.files(id) ON DELETE SET NULL,
    CONSTRAINT cld_files_parent_file_id_fkey FOREIGN KEY (parent_file_id)
        REFERENCES files.files(id) ON DELETE SET NULL
);
CREATE UNIQUE INDEX cld_files_dedup_canonical ON files.files USING btree
    (organization_id, created_by, checksum) NULLS NOT DISTINCT
    WHERE ((deleted_at IS NULL) AND (duplicate_of_file_id IS NULL)
           AND (parent_file_id IS NULL) AND (checksum IS NOT NULL));
CREATE UNIQUE INDEX cld_files_owner_id_file_path_key ON files.files USING btree
    (created_by, file_path) WHERE (deleted_at IS NULL);
CREATE UNIQUE INDEX uq_cld_files_storage_uri ON files.files USING btree (storage_uri)
    WHERE (storage_uri IS NOT NULL);
CREATE TABLE files.file_versions (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    file_id uuid NOT NULL REFERENCES files.files(id) ON DELETE CASCADE,
    version_number integer NOT NULL,
    storage_uri text NOT NULL,
    organization_id uuid NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX cld_file_versions_file_id_version_number_key
    ON files.file_versions USING btree (file_id, version_number);
CREATE TABLE platform.share_links (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    resource_type text NOT NULL,
    resource_id uuid NOT NULL
);
CREATE TABLE iam.permissions (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    resource_type text NOT NULL,
    resource_id uuid NOT NULL
);
"""


def _latest_hard_delete_migration() -> Path:
    defining = [
        p for p in SQL_DIR.glob("*.sql") if "FUNCTION public.hard_delete_file" in p.read_text()
    ]
    assert defining, f"no package migration under {SQL_DIR} defines public.hard_delete_file"
    return max(defining, key=lambda p: (int(p.name.split("_", 1)[0]), p.name))


def _pg_major(bindir: Path) -> int:
    out = subprocess.run(
        [str(bindir / "postgres"), "--version"], capture_output=True, text=True
    ).stdout
    match = re.search(r"\(PostgreSQL\)\s+(\d+)", out)
    return int(match.group(1)) if match else 0


def _pg_bindir() -> Path | None:
    candidates: list[Path] = []
    if os.environ.get("MATRX_FILES_TEST_PG_BINDIR"):
        candidates.append(Path(os.environ["MATRX_FILES_TEST_PG_BINDIR"]))
    pg_config = shutil.which("pg_config")
    if pg_config:
        out = subprocess.run([pg_config, "--bindir"], capture_output=True, text=True).stdout
        candidates.append(Path(out.strip()))
    for pattern in (
        "opt/homebrew/opt/postgresql@*/bin",
        "usr/local/opt/postgresql@*/bin",
        "usr/lib/postgresql/*/bin",
    ):
        candidates.extend(sorted(Path("/").glob(pattern), reverse=True))
    for bindir in candidates:
        if (bindir / "initdb").exists() and (bindir / "postgres").exists():
            # NULLS NOT DISTINCT (the live dedup index) needs PostgreSQL 15+.
            if _pg_major(bindir) >= 15:
                return bindir
    return None


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


async def _install(dsn: str, migration_sql: str) -> None:
    import asyncpg

    conn = await asyncpg.connect(dsn)
    try:
        await conn.execute(FIXTURE_DDL)
        await conn.execute(migration_sql)
    finally:
        await conn.close()


@pytest.fixture(scope="module")
def pg_dsn(tmp_path_factory: pytest.TempPathFactory):
    pytest.importorskip("asyncpg")
    bindir = _pg_bindir()
    if bindir is None:
        pytest.skip(
            "the sql executor needs PostgreSQL >= 15 server binaries (initdb + postgres); "
            "install them or set MATRX_FILES_TEST_PG_BINDIR"
        )
    root = tmp_path_factory.mktemp("hard_delete_pg")
    data = root / "data"
    env = {**os.environ, "LC_ALL": "C", "LANG": "C"}
    subprocess.run(
        [str(bindir / "initdb"), "-D", str(data), "-U", "postgres", "--auth=trust", "-E", "UTF8", "--locale=C"],
        check=True,
        capture_output=True,
        env=env,
    )
    port = _free_port()
    subprocess.run(
        [
            str(bindir / "pg_ctl"),
            "-D",
            str(data),
            "-l",
            str(root / "postgres.log"),
            "-w",
            "-o",
            f"-p {port} -c listen_addresses=127.0.0.1 -c unix_socket_directories=''",
            "start",
        ],
        check=True,
        capture_output=True,
        env=env,
    )
    dsn = f"postgresql://postgres@127.0.0.1:{port}/postgres"
    try:
        asyncio.run(_install(dsn, _latest_hard_delete_migration().read_text()))
        yield dsn
    finally:
        subprocess.run(
            [str(bindir / "pg_ctl"), "-D", str(data), "-m", "immediate", "stop"],
            capture_output=True,
            env=env,
        )


async def _run_sql(dsn: str, sc: Scenario) -> tuple[dict[str, str | None], dict[str, Any]]:
    import asyncpg

    conn = await asyncpg.connect(dsn)
    tx = conn.transaction()
    await tx.start()
    try:
        for r in sc.rows:
            await conn.execute(
                "INSERT INTO files.files (id, created_by, organization_id, file_path, file_name,"
                " storage_uri, checksum, created_at, deleted_at, parent_file_id, duplicate_of_file_id)"
                " VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)",
                uuid.UUID(ID[r.name]),
                uuid.UUID(OWNER),
                uuid.UUID(ORG),
                f"docs/{r.name}",
                r.name,
                uri(r.name),
                r.checksum,
                datetime.fromisoformat(_created_at(r.second)),
                datetime.fromisoformat(TRASHED_AT) if r.trashed else None,
                uuid.UUID(ID[r.parent]) if r.parent else None,
                uuid.UUID(ID[r.dup]) if r.dup else None,
            )
            for n, label in enumerate(r.versions, 1):
                await conn.execute(
                    "INSERT INTO files.file_versions (file_id, version_number, storage_uri, organization_id)"
                    " VALUES ($1, $2, $3, $4)",
                    uuid.UUID(ID[r.name]),
                    n,
                    uri(label),
                    uuid.UUID(ORG),
                )
        try:
            report = await conn.fetchval(
                "SELECT files.hard_delete_file($1)", uuid.UUID(ID[sc.delete])
            )
        except asyncpg.PostgresError as exc:
            pytest.fail(
                f"hard_delete_file({sc.delete}) was refused — the file can never be "
                f"deleted and nothing is purged: {exc}"
            )
        rows = await conn.fetch("SELECT id, duplicate_of_file_id FROM files.files")
    finally:
        await tx.rollback()
        await conn.close()
    remaining = {
        NAME[str(row["id"])]: NAME[str(row["duplicate_of_file_id"])]
        if row["duplicate_of_file_id"]
        else None
        for row in rows
    }
    return remaining, _normalize(report)


# ---------------------------------------------------------------------------
# Executors: the ORM fallback cascade and the double's model, in memory
# ---------------------------------------------------------------------------


def _seed_double(sc: Scenario) -> FilesDB:
    db = FilesDB()
    for r in sc.rows:
        db.files.create_sync(
            id=ID[r.name],
            created_by=OWNER,
            organization_id=ORG,
            file_path=f"docs/{r.name}",
            file_name=r.name,
            storage_uri=uri(r.name),
            checksum=r.checksum,
            created_at=_created_at(r.second),
            deleted_at=TRASHED_AT if r.trashed else None,
            parent_file_id=ID[r.parent] if r.parent else None,
            duplicate_of_file_id=ID[r.dup] if r.dup else None,
        )
        for n, label in enumerate(r.versions, 1):
            db.file_versions.create_sync(
                file_id=ID[r.name], version_number=n, storage_uri=uri(label), organization_id=ORG
            )
    return db


async def _run_in_memory(sc: Scenario, executor: str) -> tuple[dict[str, str | None], dict[str, Any]]:
    db = _seed_double(sc)
    with db.bound():
        client = db.client()
        try:
            if executor == "orm-fallback":
                report = await client.hard_delete_file_fallback_async(ID[sc.delete])
            else:
                report = await client.hard_delete_file_async(ID[sc.delete])
        except UniqueViolation as exc:
            pytest.fail(
                f"{executor} hard delete of {sc.delete} was refused — the file can never be "
                f"deleted and nothing is purged: {exc}"
            )
    remaining = {
        NAME[row["id"]]: NAME[row["duplicate_of_file_id"]] if row["duplicate_of_file_id"] else None
        for row in db.files.rows.values()
    }
    return remaining, _normalize(report)


# Break: promotion picks no heir, picks by insertion order / newest / a trashed
# row first, leaves an alias on the deleted canonical, makes a second root for a
# key a live root already holds, or purges an object a surviving row references.
@pytest.mark.parametrize("executor", ["sql", "orm-fallback", "double-rpc"])
@pytest.mark.parametrize("sc", SCENARIOS, ids=[s.id for s in SCENARIOS])
async def test_hard_deleting_a_canonical_promotes_one_alias_and_repoints_the_rest(
    pg_dsn: str, sc: Scenario, executor: str
):
    if executor == "sql":
        remaining, report = await _run_sql(pg_dsn, sc)
    else:
        remaining, report = await _run_in_memory(sc, executor)

    assert remaining == sc.remaining, f"{executor}: alias links after deleting {sc.delete}"
    assert report == _expected(sc), f"{executor}: purge report after deleting {sc.delete}"


# ---------------------------------------------------------------------------
# The engine: what a user sees after the ONE hard-delete primitive runs
# ---------------------------------------------------------------------------

USER_ID = "user-1"
PERSONAL_ORG = "org-personal-0001"
CANON_PATH = "docs/original.pdf"
CANON_URI = "s3://test-bucket/user-1/original"


@pytest.fixture
def files_db():
    db = FilesDB()
    db.org_members.add((USER_ID, PERSONAL_ORG))
    with db.bound():
        yield db


def _seed(db: FilesDB, path: str, storage_uri: str, content: bytes, second: int, **extra: Any) -> dict[str, Any]:
    import hashlib

    return db.seed_file(
        created_by=USER_ID,
        organization_id=PERSONAL_ORG,
        file_path=path,
        storage_uri=storage_uri,
        checksum=hashlib.sha256(content).hexdigest(),
        created_at=_created_at(second),
        **extra,
    )


def _pin_cascade(files_db: FilesDB, engine: Any, cascade: str) -> None:
    """Make the parametrized cascade the ONLY one able to serve the delete.

    The engine falls back to the ORM cascade on ANY SQL-function failure, so an
    unpinned ``[sql-fn]`` case passes a broken SQL model through the fallback.
    ``[orm-fallback]`` makes the function missing (SQLSTATE 42883); ``[sql-fn]``
    fails the test the moment the fallback runs. ``pytest.fail`` raises a
    BaseException, so the engine's ``except Exception`` cannot swallow it."""
    if cascade == "orm-fallback":
        files_db.unavailable_rpcs.add("hard_delete_file")
        return

    async def _fallback_must_not_run(file_id: str) -> dict | None:
        pytest.fail(f"[sql-fn] the SQL function failed for {file_id}; the ORM fallback served the delete")

    engine._db.hard_delete_file_fallback_async = _fallback_must_not_run


def _grant_all(engine: Any, *rows: dict[str, Any]) -> None:
    for row in rows:
        for level in ("read", "write", "admin"):
            engine.permissions.allowed.add((USER_ID, row["id"], level))


# Break (live defect 2026-09-10): the canonical of a force copy / converged save
# with 2+ aliases cannot be hard-deleted (23505), or deleting it hides or purges
# an alias's bytes.
@pytest.mark.parametrize("cascade", ["sql-fn", "orm-fallback"])
async def test_hard_deleting_a_canonical_keeps_every_alias_readable(files_db, cascade):
    content = b"bytes three paths hold"
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)
    canonical = _seed(files_db, CANON_PATH, CANON_URI, content, 1)
    late = _seed(files_db, "docs/late.pdf", "s3://test-bucket/user-1/late", content, 8, duplicate_of_file_id=canonical["id"])
    early = _seed(files_db, "docs/early.pdf", "s3://test-bucket/user-1/early", content, 4, duplicate_of_file_id=canonical["id"])
    engine._router.objects.update(
        {CANON_URI: content, late["storage_uri"]: content, early["storage_uri"]: content}
    )
    _grant_all(engine, canonical, late, early)
    _pin_cascade(files_db, engine, cascade)

    try:
        assert await engine.managed_delete_async(CANON_PATH, hard_delete=True)
    except Exception as exc:
        pytest.fail(f"hard delete of a canonical with two aliases failed: {exc}")

    assert await engine.managed_read_async("docs/early.pdf") == content
    assert await engine.managed_read_async("docs/late.pdf") == content
    rows = files_db.files.rows
    assert canonical["id"] not in rows
    assert (rows[early["id"]]["duplicate_of_file_id"], rows[late["id"]]["duplicate_of_file_id"]) == (
        None,
        early["id"],
    )
    assert engine._router.objects == {early["storage_uri"]: content, late["storage_uri"]: content}


# Break: the purge deletes the canonical's object although the promoted alias's
# own version history still names it — the alias's v1 would 404 forever.
@pytest.mark.parametrize("cascade", ["sql-fn", "orm-fallback"])
async def test_hard_delete_never_purges_an_object_a_surviving_alias_still_references(files_db, cascade):
    content = b"bytes the alias history still names"
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)
    canonical = _seed(files_db, CANON_PATH, CANON_URI, content, 1)
    alias = _seed(files_db, "docs/copy.pdf", "s3://test-bucket/user-1/copy", content, 3, duplicate_of_file_id=canonical["id"])
    files_db.file_versions.create_sync(
        file_id=alias["id"], version_number=1, storage_uri=CANON_URI, organization_id=PERSONAL_ORG
    )
    engine._router.objects.update({CANON_URI: content, alias["storage_uri"]: content})
    _grant_all(engine, canonical, alias)
    _pin_cascade(files_db, engine, cascade)

    try:
        assert await engine.managed_delete_async(CANON_PATH, hard_delete=True)
    except Exception as exc:
        pytest.fail(f"hard delete of a canonical with one alias failed: {exc}")

    assert engine._router.objects.get(CANON_URI) == content, (
        "hard delete purged an object the surviving alias's version 1 still references"
    )
    assert canonical["id"] not in files_db.files.rows
    assert files_db.files.rows[alias["id"]]["duplicate_of_file_id"] is None
