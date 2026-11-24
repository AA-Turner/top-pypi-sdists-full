"""``files.ensure_folder_chain`` never leaves a folder's organization to the database (AD240).

SUT: the 3-argument ``files.ensure_folder_chain(p_owner_id, p_folder_path, p_organization_id)``.
ONE scenario table with literal outcomes runs through two executors:

* ``sql`` — the function from ``cloud_sync/sql/041_ensure_folder_chain_explicit_organization.sql``
  overlaid with ``LIVE_BODY_2026_10_12`` (the body applied to Matrx Main from chat on 2026-10-12:
  folder identity is (owner, organization, path)), executed verbatim on a throwaway local PostgreSQL. The fixture table has ``organization_id NOT
  NULL`` and NO org-assignment trigger, so an INSERT that omits the organization is a 23502 and a
  wrong organization is a literal mismatch — nothing in the fixture can supply one.
* ``double`` — ``tests/_files_db_double.py``'s model of the same function, which every engine
  test (``FileService.mutate_file``, the presigned lane) runs through, held to the same literals.

Breaks guarded: the INSERT omits or swaps ``organization_id``; a missing organization is defaulted
instead of refused; an existing live folder is re-labelled or duplicated; a segment is skipped; the
owner's folder of ANOTHER organization at a path is reused (a person's folder tree is per
organization — reusing it put 977 files under another organization's folder until 2026-10-12).
"""

from __future__ import annotations

import asyncio
import os
import subprocess
import uuid
from dataclasses import dataclass
from pathlib import Path

import matrx_files
import pytest

from _files_db_double import FilesDB
from test_hard_delete_alias_promotion import _free_port, _pg_bindir

OWNER = "0b000000-0000-4000-8000-000000000001"
TEAM = "0a000000-0000-4000-8000-00000000000a"
PERSONAL = "0a000000-0000-4000-8000-00000000000b"

SQL_FILE = (
    Path(matrx_files.__file__).parent
    / "cloud_sync"
    / "sql"
    / "041_ensure_folder_chain_explicit_organization.sql"
)
# The current definition (live 2026-11-18): a live folder reached through the chain whose parent is
# trashed or gone is re-homed under the chain's live parent.
SQL_062 = SQL_FILE.parent / "062_folder_chain_never_resolves_through_a_trashed_parent.sql"


@dataclass(frozen=True)
class Scenario:
    id: str
    existing: tuple[tuple[str, str], ...]  # live folders already owned by OWNER: (path, org)
    path: str
    org: str | None
    # every folder after the call: (folder_path, organization_id, parent folder_path)
    folders: frozenset[tuple[str, str, str | None]]
    leaf: str | None  # folder_path of the returned id
    sqlstate: str | None = None


SCENARIOS = [
    Scenario(
        "creates-every-segment-in-the-named-team-org",
        existing=(),
        path="projects/q3",
        org=TEAM,
        folders=frozenset({("projects", TEAM, None), ("projects/q3", TEAM, "projects")}),
        leaf="projects/q3",
    ),
    Scenario(
        "creates-every-segment-in-the-named-personal-org",
        existing=(),
        path="/archive/2026/",
        org=PERSONAL,
        folders=frozenset({("archive", PERSONAL, None), ("archive/2026", PERSONAL, "archive")}),
        leaf="archive/2026",
    ),
    Scenario(
        "reuses-a-live-folder-of-the-same-organization",
        existing=(("projects", TEAM),),
        path="projects/q4",
        org=TEAM,
        folders=frozenset({("projects", TEAM, None), ("projects/q4", TEAM, "projects")}),
        leaf="projects/q4",
    ),
    Scenario(
        "never-reuses-or-relabels-another-organizations-folder",
        existing=(("projects", PERSONAL),),
        path="projects/q4",
        org=TEAM,
        folders=frozenset(
            {
                ("projects", PERSONAL, None),
                ("projects", TEAM, None),
                ("projects/q4", TEAM, "projects"),
            }
        ),
        leaf="projects/q4",
    ),
    Scenario(
        "refuses-a-missing-organization-and-writes-nothing",
        existing=(),
        path="projects/q3",
        org=None,
        folders=frozenset(),
        leaf=None,
        sqlstate="22004",
    ),
]


# ---------------------------------------------------------------------------
# Executor: the production SQL on a throwaway PostgreSQL
# ---------------------------------------------------------------------------

# The columns files.folders carries in the generated model (matrx_files/db/models_files.py
# ``Folders``) with the live partial unique key (package sql 034) and NOT NULL organization.
FIXTURE_DDL = """
CREATE ROLE anon; CREATE ROLE authenticated; CREATE ROLE service_role;
CREATE SCHEMA files;
CREATE TABLE files.folders (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    created_by uuid NOT NULL,
    organization_id uuid NOT NULL,
    folder_path text NOT NULL,
    folder_name text NOT NULL,
    parent_id uuid REFERENCES files.folders(id) ON DELETE CASCADE,
    visibility text NOT NULL DEFAULT 'internal',
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    is_system boolean NOT NULL DEFAULT false,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    deleted_at timestamptz
);
CREATE UNIQUE INDEX folders_owner_org_path_key
    ON files.folders (created_by, organization_id, folder_path) WHERE deleted_at IS NULL;
"""

# The body live on Matrx Main since 2026-10-12 (applied from chat, clone-proven; the package sql
# chain still ends at 041 for this function). The conflict key names the organization.
LIVE_BODY_2026_10_12 = r"""
CREATE OR REPLACE FUNCTION files.ensure_folder_chain(p_owner_id uuid, p_folder_path text, p_organization_id uuid)
 RETURNS uuid
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'pg_catalog', 'public'
AS $function$
DECLARE v_path TEXT; v_part TEXT; v_parent UUID := NULL; v_current_path TEXT := ''; v_id UUID;
BEGIN
    IF p_organization_id IS NULL THEN
        RAISE EXCEPTION 'ensure_folder_chain: p_organization_id is required — the organization is never defaulted (owner %, path %)',
            p_owner_id, p_folder_path
            USING ERRCODE = '22004';
    END IF;
    v_path := trim(both '/' from p_folder_path);
    IF v_path = '' THEN RETURN NULL; END IF;
    FOR v_part IN SELECT unnest(string_to_array(v_path, '/'))
    LOOP
        v_current_path := CASE WHEN v_current_path = '' THEN v_part ELSE v_current_path || '/' || v_part END;
        -- Keyed on (owner, organization, path): another organization's folder at this path is
        -- never returned — this organization gets its own.
        INSERT INTO files.folders (created_by, organization_id, folder_path, folder_name, parent_id)
        VALUES (p_owner_id, p_organization_id, v_current_path, v_part, v_parent)
        ON CONFLICT (created_by, organization_id, folder_path) WHERE deleted_at IS NULL
        DO UPDATE SET updated_at = now()
        RETURNING id INTO v_id;
        v_parent := v_id;
    END LOOP;
    RETURN v_parent;
END;
$function$;
"""


@pytest.fixture(scope="module")
def pg_dsn(tmp_path_factory: pytest.TempPathFactory):
    pytest.importorskip("asyncpg")
    bindir = _pg_bindir()
    if bindir is None:
        pytest.skip(
            "the sql executor needs PostgreSQL >= 15 server binaries (initdb + postgres); "
            "install them or set MATRX_FILES_TEST_PG_BINDIR"
        )
    root = tmp_path_factory.mktemp("folder_chain_pg")
    data = root / "data"
    env = {**os.environ, "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"}
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

    async def _install() -> None:
        import asyncpg

        conn = await asyncpg.connect(dsn)
        try:
            await conn.execute(FIXTURE_DDL)
            await conn.execute(SQL_FILE.read_text())
            await conn.execute(LIVE_BODY_2026_10_12)
            await conn.execute(SQL_062.read_text())
        finally:
            await conn.close()

    try:
        asyncio.run(_install())
        yield dsn
    finally:
        subprocess.run(
            [str(bindir / "pg_ctl"), "-D", str(data), "-m", "immediate", "stop"],
            capture_output=True,
            env=env,
        )


async def _run_sql(dsn: str, sc: Scenario):
    import asyncpg

    conn = await asyncpg.connect(dsn)
    tx = conn.transaction()
    await tx.start()
    sqlstate = leaf = None
    try:
        for path, org in sc.existing:
            await conn.execute(
                "INSERT INTO files.folders (created_by, organization_id, folder_path, folder_name)"
                " VALUES ($1, $2, $3, $4)",
                uuid.UUID(OWNER),
                uuid.UUID(org),
                path,
                path.rsplit("/", 1)[-1],
            )
        await conn.execute("SAVEPOINT call")
        try:
            leaf_id = await conn.fetchval(
                "SELECT files.ensure_folder_chain($1::uuid, $2::text, $3::uuid)",
                uuid.UUID(OWNER),
                sc.path,
                uuid.UUID(sc.org) if sc.org else None,
            )
        except asyncpg.PostgresError as exc:
            sqlstate = exc.sqlstate
            await conn.execute("ROLLBACK TO SAVEPOINT call")
            leaf_id = None
        rows = await conn.fetch(
            "SELECT f.id, f.folder_path, f.organization_id, p.folder_path AS parent_path"
            " FROM files.folders f LEFT JOIN files.folders p ON p.id = f.parent_id"
        )
    finally:
        await tx.rollback()
        await conn.close()
    by_id = {str(r["id"]): r["folder_path"] for r in rows}
    leaf = by_id.get(str(leaf_id)) if leaf_id else None
    folders = frozenset((r["folder_path"], str(r["organization_id"]), r["parent_path"]) for r in rows)
    return folders, leaf, sqlstate


def _run_double(sc: Scenario):
    db = FilesDB()
    for path, org in sc.existing:
        db.folders.create_sync(
            created_by=OWNER, organization_id=org, folder_path=path, folder_name=path.rsplit("/", 1)[-1]
        )
    sqlstate = leaf_id = None
    try:
        leaf_id = db.rpc("files", "ensure_folder_chain", OWNER, sc.path, sc.org)
    except Exception as exc:  # the double raises what asyncpg surfaces: .sqlstate + message
        sqlstate = getattr(exc, "sqlstate", None)
        if sqlstate is None:
            raise
    rows = list(db.folders.rows.values())
    by_id = {r["id"]: r["folder_path"] for r in rows}
    folders = frozenset(
        (r["folder_path"], r["organization_id"], by_id.get(r["parent_id"])) for r in rows
    )
    return folders, (by_id.get(leaf_id) if leaf_id else None), sqlstate


@pytest.mark.parametrize("executor", ["sql", "double"])
@pytest.mark.parametrize("sc", SCENARIOS, ids=[s.id for s in SCENARIOS])
async def test_every_folder_the_chain_creates_carries_the_named_organization(
    pg_dsn: str, sc: Scenario, executor: str
):
    if executor == "sql":
        folders, leaf, sqlstate = await _run_sql(pg_dsn, sc)
    else:
        folders, leaf, sqlstate = _run_double(sc)

    assert sqlstate == sc.sqlstate, f"{executor}: refusal for org={sc.org!r}"
    assert folders == sc.folders, f"{executor}: folders after ensure_folder_chain({sc.path!r}, {sc.org!r})"
    assert leaf == sc.leaf, f"{executor}: returned leaf"


# ---------------------------------------------------------------------------
# A chain never resolves through a trashed parent (062, 2026-11-18)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Stranded:
    id: str
    # (path, parent path or None, trashed) in creation order; a parent path names the row created
    # just before at that path (so a trashed twin can be a parent)
    existing: tuple[tuple[str, str | None, bool], ...]
    path: str
    # every LIVE folder after the call: (folder_path, parent folder_path, parent is live)
    live: frozenset[tuple[str, str | None, bool]]


STRANDED = [
    Stranded(
        "a-live-child-of-a-trashed-parent-is-rehomed-under-the-recreated-parent",
        existing=(("Plant logs", None, True), ("Plant logs/Inbox", "Plant logs", False)),
        path="Plant logs/Inbox",
        live=frozenset({("Plant logs", None, True), ("Plant logs/Inbox", "Plant logs", True)}),
    ),
    Stranded(
        "a-live-child-with-no-parent-below-the-root-is-rehomed",
        existing=(("Plant logs/Inbox", None, False),),
        path="Plant logs/Inbox",
        live=frozenset({("Plant logs", None, True), ("Plant logs/Inbox", "Plant logs", True)}),
    ),
    Stranded(
        "a-different-live-parent-is-never-overridden",
        existing=(("Shared", None, False), ("Plant logs/Inbox", "Shared", False)),
        path="Plant logs/Inbox",
        live=frozenset(
            {("Shared", None, True), ("Plant logs", None, True), ("Plant logs/Inbox", "Shared", True)}
        ),
    ),
]


async def _run_stranded_sql(dsn: str, sc: Stranded):
    import asyncpg

    conn = await asyncpg.connect(dsn)
    tx = conn.transaction()
    await tx.start()
    try:
        ids: dict[str, uuid.UUID] = {}
        for path, parent, trashed in sc.existing:
            ids[path] = await conn.fetchval(
                "INSERT INTO files.folders (created_by, organization_id, folder_path, folder_name, parent_id,"
                " deleted_at) VALUES ($1, $2, $3, $4, $5, CASE WHEN $6 THEN now() END) RETURNING id",
                uuid.UUID(OWNER),
                uuid.UUID(TEAM),
                path,
                path.rsplit("/", 1)[-1],
                ids.get(parent) if parent else None,
                trashed,
            )
        await conn.fetchval(
            "SELECT files.ensure_folder_chain($1::uuid, $2::text, $3::uuid)", uuid.UUID(OWNER), sc.path, uuid.UUID(TEAM)
        )
        rows = await conn.fetch(
            "SELECT f.folder_path, p.folder_path AS parent_path, (p.id IS NOT NULL AND p.deleted_at IS NULL) AS live"
            " FROM files.folders f LEFT JOIN files.folders p ON p.id = f.parent_id WHERE f.deleted_at IS NULL"
        )
    finally:
        await tx.rollback()
        await conn.close()
    return frozenset(
        (r["folder_path"], r["parent_path"], bool(r["live"]) or r["parent_path"] is None) for r in rows
    )


def _run_stranded_double(sc: Stranded):
    db = FilesDB()
    ids: dict[str, str] = {}
    for path, parent, trashed in sc.existing:
        ids[path] = db.folders.create_sync(
            created_by=OWNER,
            organization_id=TEAM,
            folder_path=path,
            folder_name=path.rsplit("/", 1)[-1],
            parent_id=ids.get(parent) if parent else None,
            deleted_at="2026-11-18T00:00:00Z" if trashed else None,
        ).to_dict()["id"]
    db.rpc("files", "ensure_folder_chain", OWNER, sc.path, TEAM)
    rows = db.folders.rows
    out = set()
    for r in rows.values():
        if r.get("deleted_at") is not None:
            continue
        p = rows.get(r.get("parent_id")) if r.get("parent_id") else None
        out.add((r["folder_path"], p["folder_path"] if p else None, p is None or p.get("deleted_at") is None))
    return frozenset(out)


@pytest.mark.parametrize("executor", ["sql", "double"])
@pytest.mark.parametrize("sc", STRANDED, ids=[s.id for s in STRANDED])
async def test_a_chain_never_resolves_through_a_trashed_parent(pg_dsn: str, sc: Stranded, executor: str):
    live = await _run_stranded_sql(pg_dsn, sc) if executor == "sql" else _run_stranded_double(sc)
    assert live == sc.live, f"{executor}: live folders after ensure_folder_chain({sc.path!r})"
