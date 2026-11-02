"""Driver-level stand-in for the ``files`` schema — used by the dedup tests.

What is REAL here: ``DatabaseClient`` (every query it builds, including the
dedup ``_checksum_query`` and the path / folder lookups) and matrx-orm's
``QueryBuilder`` (filter-key validation against the generated ``Files`` /
``Folders`` models). What is replaced: only the SQL executor (and the
``matrx_orm.transaction`` it would open, which rolls the in-memory rows back on a
raise) — the recorded
``filters`` / ``order_by_fields`` / ``limit_val`` of the real builder are
evaluated over in-memory rows with Postgres semantics (``=``, ``IS NULL``,
ASC NULLS LAST, DESC NULLS FIRST).

The unique indexes below were CAPTURED from Matrx Main on 2026-09-10
(``select indexdef from pg_indexes where schemaname='files'``):

  cld_files_dedup_canonical  UNIQUE (organization_id, created_by, checksum)
      NULLS NOT DISTINCT WHERE deleted_at IS NULL AND duplicate_of_file_id IS
      NULL AND parent_file_id IS NULL AND checksum IS NOT NULL
  cld_files_owner_id_file_path_key  UNIQUE (created_by, file_path)
      WHERE deleted_at IS NULL
  uq_cld_files_storage_uri  UNIQUE (storage_uri) WHERE storage_uri IS NOT NULL
  folders_owner_org_path_key  UNIQUE (created_by, organization_id, folder_path)
      WHERE deleted_at IS NULL   -- a trashed folder releases its path; since 2026-10-12
      -- a person's folder tree is per organization (was (created_by, folder_path))

S3 (object store), IAM RPCs, the ACL checker and the version recorder are
external dependencies and get small honest doubles.
"""

from __future__ import annotations

import copy
import itertools
import json
import uuid
from contextlib import asynccontextmanager, contextmanager
from dataclasses import dataclass, field
from types import SimpleNamespace
from typing import Any
from unittest.mock import patch

from matrx_files.cloud_sync.db import DatabaseClient
from matrx_files.cloud_sync.sync_engine import SyncEngine
from matrx_files.db import PACKAGE_DB_NAME, models_files, models_iam

_clock = itertools.count(1)


def _ts() -> str:
    # Monotonic, sortable stand-in for the DB's now() default.
    return f"2026-09-10T00:00:{next(_clock):06d}Z"


class UniqueViolation(Exception):
    """asyncpg's UniqueViolationError as the classifiers read it: ``.sqlstate`` + ``.constraint_name``.

    Production code decides a race by ``matrx_orm.db_sqlstate`` / ``db_constraint`` — never the
    message words — so the double carries the same two fields the real error does."""

    sqlstate = "23505"  # asyncpg's UniqueViolationError carries it; the RPC wrappers map on it

    def __init__(self, constraint: str) -> None:
        self.constraint = constraint
        self.constraint_name = constraint  # asyncpg's attribute; matrx_orm.db_constraint reads it
        super().__init__(
            f'duplicate key value violates unique constraint "{constraint}" (SQLSTATE 23505)'
        )


class _PgError(Exception):
    """A plpgsql ``RAISE ... USING ERRCODE`` as asyncpg surfaces it: ``.sqlstate`` + message."""

    def __init__(self, sqlstate: str, message: str) -> None:
        self.sqlstate = sqlstate
        super().__init__(message)


@dataclass
class _Instance:
    data: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return dict(self.data)


@dataclass
class _Result:
    rows_affected: int


def _matches(row: dict[str, Any], flt: dict[str, Any]) -> bool:
    for key, value in flt.items():
        name, op = key, "eq"
        if "__" in key:
            name, op = key.rsplit("__", 1)
        if op == "eq":
            if value is None:
                if row.get(name) is not None:
                    return False
            elif row.get(name) != value:
                return False
        elif op == "lt":
            if row.get(name) is None or not row[name] < value:
                return False
        elif op == "in":
            if row.get(name) not in value:
                return False
        elif op == "isnull":
            if (row.get(name) is None) != bool(value):
                return False
        elif op == "json_key":
            # matrx-orm: ``(key, expected)`` -> ``col ->> key = expected``; a bare key ->
            # ``col ->> key IS NOT NULL``. ``->>`` yields text (NULL for a missing key or
            # a non-object column), and NULL never equals anything.
            key, expected = value if isinstance(value, tuple) else (value, None)
            doc = row.get(name)
            raw = doc.get(key) if isinstance(doc, dict) else None
            text = None if raw is None else raw if isinstance(raw, str) else json.dumps(raw)
            if text is None or (isinstance(value, tuple) and text != str(expected)):
                return False
        else:  # pragma: no cover - loud on any operator the double can't honor
            raise NotImplementedError(f"files double does not evaluate lookup {key!r}")
    return True


def _order(rows: list[dict[str, Any]], fields: list[Any]) -> list[dict[str, Any]]:
    out = list(rows)
    for spec in reversed(fields):
        if not isinstance(spec, str):  # pragma: no cover
            raise NotImplementedError(f"files double does not evaluate order_by {spec!r}")
        desc = spec.startswith("-")
        name = spec.lstrip("-")
        present = [r for r in out if r.get(name) is not None]
        nulls = [r for r in out if r.get(name) is None]
        present.sort(key=lambda r: r[name], reverse=desc)
        out = nulls + present if desc else present + nulls
    return out


class _Query:
    def __init__(self, table: _Table, builder: Any) -> None:
        self._table = table
        self._builder = builder

    def filter(self, *args: Any, **kwargs: Any) -> _Query:
        return _Query(self._table, self._builder.filter(*args, **kwargs))

    def order_by(self, *fields: Any) -> _Query:
        return _Query(self._table, self._builder.order_by(*fields))

    def limit(self, value: int) -> _Query:
        return _Query(self._table, self._builder.limit(value))

    def _evaluate(self) -> list[dict[str, Any]]:
        b = self._builder
        if b.excludes:  # pragma: no cover
            raise NotImplementedError("files double does not evaluate exclude()")
        rows = list(self._table.rows.values())
        for flt in b.filters:
            if not isinstance(flt, dict):  # pragma: no cover
                raise NotImplementedError(f"files double does not evaluate {flt!r}")
            rows = [r for r in rows if _matches(r, flt)]
        rows = _order(rows, list(b.order_by_fields))
        if b.limit_val is not None:
            rows = rows[: b.limit_val]
        return rows

    async def first(self) -> _Instance | None:
        return self.first_sync()

    def first_sync(self) -> _Instance | None:
        rows = self._evaluate()
        return _Instance(rows[0]) if rows else None

    async def all(self) -> list[_Instance]:
        return [_Instance(r) for r in self._evaluate()]

    def values_sync(self, *fields: str) -> list[dict[str, Any]]:
        return [{f: r.get(f) for f in fields} for r in self._evaluate()]

    async def values(self, *fields: str) -> list[dict[str, Any]]:
        return self.values_sync(*fields)


class _Table:
    def __init__(
        self,
        model: Any,
        defaults: dict[str, Any],
        uniques: list[Any],
        *,
        set_null_fks: tuple[str, ...] = (),
    ) -> None:
        self.model = model
        self.rows: dict[str, dict[str, Any]] = {}
        self._defaults = defaults
        self._uniques = uniques
        self._set_null_fks = set_null_fks
        self.before_create: list[Any] = []
        # Hooks run before an UPDATE lands: ``hook(where, values)``. A test uses
        # one to inject an unrelated database failure (connection reset, ...).
        self.before_update: list[Any] = []

    def filter(self, *args: Any, **kwargs: Any) -> _Query:
        return _Query(self, self.model.filter(*args, **kwargs))

    def _check_unique(self, candidate: dict[str, Any], *, ignore_id: str | None) -> None:
        for name, cols, predicate in self._uniques:
            if not predicate(candidate):
                continue
            key = tuple(candidate.get(c) for c in cols)
            for row in self.rows.values():
                if row["id"] == ignore_id or not predicate(row):
                    continue
                if tuple(row.get(c) for c in cols) == key:
                    raise UniqueViolation(name)

    def create_sync(self, **values: Any) -> _Instance:
        for hook in list(self.before_create):
            hook(values)
        unknown = set(values) - set(self.model._fields)
        if unknown:
            raise ValueError(f"no such column(s) on {self.model.__name__}: {sorted(unknown)}")
        row = {c: None for c in self.model._fields}
        row.update(self._defaults)
        row.update({"id": str(uuid.uuid4()), "created_at": _ts()})
        row.update(values)
        if row["id"] in self.rows:
            raise UniqueViolation(f"cld_{self.model._table_name}_pkey")
        self._check_unique(row, ignore_id=None)
        self.rows[row["id"]] = row
        return _Instance(dict(row))

    async def create(self, **values: Any) -> _Instance:
        return self.create_sync(**values)

    def update_where_sync(self, where: dict[str, Any], **values: Any) -> _Result:
        for hook in list(self.before_update):
            hook(where, values)
        hits =[r for r in self.rows.values() if _matches(r, where)]
        for row in hits:
            candidate = {**row, **values}
            self._check_unique(candidate, ignore_id=row["id"])
            row.update(values)
        return _Result(rows_affected=len(hits))

    async def update_where(self, where: dict[str, Any], **values: Any) -> _Result:
        return self.update_where_sync(where, **values)

    def delete_row_sync(self, row_id: str, *, set_null_fks: tuple[str, ...] = ()) -> None:
        """DELETE one row; each ``ON DELETE SET NULL`` FK update is re-checked
        against the unique indexes and a violation aborts the whole statement."""
        snapshot = {rid: dict(r) for rid, r in self.rows.items()}
        self.rows.pop(row_id)
        try:
            for row in self.rows.values():
                for fk in set_null_fks:
                    if row.get(fk) == row_id:
                        self._check_unique({**row, fk: None}, ignore_id=row["id"])
                        row[fk] = None
        except Exception:
            self.rows.clear()
            self.rows.update(snapshot)
            raise

    def delete_where_sync(self, **where: Any) -> _Result:
        """DELETE ... WHERE, each row through the table's ON DELETE SET NULL FKs."""
        hits = [r["id"] for r in self.rows.values() if _matches(r, where)]
        for row_id in hits:
            self.delete_row_sync(row_id, set_null_fks=self._set_null_fks)
        return _Result(rows_affected=len(hits))

    async def delete_where(self, **where: Any) -> _Result:
        return self.delete_where_sync(**where)

    async def upsert(self, data: dict[str, Any], on_conflict: Any) -> _Instance:
        return self.upsert_sync(data, on_conflict)

    def _infer_arbiter(self, on_conflict: Any) -> tuple[str, ...]:
        """Mimic Postgres ON CONFLICT inference: a bare column list matches only a
        NON-partial unique index on exactly those columns; a partial index needs a
        target carrying its predicate (matrx_orm.ConflictTarget.partial)."""
        where = getattr(on_conflict, "where", None)
        cols = tuple(
            e.strip('"') for e in (getattr(on_conflict, "expressions", None) or on_conflict)
        )
        for _name, ucols, predicate in self._uniques:
            if set(ucols) != set(cols):
                continue
            partial = not predicate({"deleted_at": "x", "checksum": None, "storage_uri": None})
            if partial and not where:
                continue
            return cols
        raise RuntimeError(
            "no unique or exclusion constraint matching the ON CONFLICT specification"
        )

    def upsert_sync(self, data: dict[str, Any], on_conflict: Any) -> _Instance:
        on_conflict = list(self._infer_arbiter(on_conflict))
        for row in self.rows.values():
            if all(row.get(c) == data.get(c) for c in on_conflict):
                row.update(data)
                return _Instance(dict(row))
        return self.create_sync(**data)


def _canonical_root(r: dict[str, Any]) -> bool:
    return (
        r.get("deleted_at") is None
        and r.get("duplicate_of_file_id") is None
        and r.get("parent_file_id") is None
        and r.get("checksum") is not None
    )


class _CascadeStub:
    """A table only the ORM hard-delete cascade touches (delete by file/resource
    id). No test models rows in it, so a delete affects nothing."""

    def delete_where_sync(self, **where: Any) -> _Result:
        return _Result(rows_affected=0)

    async def delete_where(self, **where: Any) -> _Result:
        return self.delete_where_sync(**where)


_CASCADE_ONLY_MODELS = (
    "FileRagJobs",
    "PageAnnotations",
    "Entities",
    "Overrides",
    "AnalysisResult",
    "Pages",
    "Analysis",
    "Structure",
)


class FilesDB:
    """In-memory ``files.files`` / ``files.file_versions`` / ``files.folders`` /
    ``iam.permissions``."""

    def __init__(self) -> None:
        self.files = _Table(
            models_files.Files,
            {"current_version": 1, "metadata": {}, "derivation_metadata": {}, "visibility": "personal"},
            [
                ("cld_files_dedup_canonical", ("organization_id", "created_by", "checksum"), _canonical_root),
                ("cld_files_owner_id_file_path_key", ("created_by", "file_path"), lambda r: r.get("deleted_at") is None),
                ("uq_cld_files_storage_uri", ("storage_uri",), lambda r: r.get("storage_uri") is not None),
            ],
            # Captured live: both self-FKs are ON DELETE SET NULL.
            set_null_fks=("duplicate_of_file_id", "parent_file_id"),
        )
        # Captured live: UNIQUE (file_id, version_number); storage_uri is NOT unique.
        self.file_versions = _Table(
            models_files.FileVersions,
            {"metadata": {}},
            [("cld_file_versions_file_id_version_number_key", ("file_id", "version_number"), lambda r: True)],
        )
        self.folders = _Table(
            models_files.Folders,
            {"metadata": {}, "is_system": False, "visibility": "personal"},
            [
                (
                    "folders_owner_org_path_key",
                    ("created_by", "organization_id", "folder_path"),
                    lambda r: r.get("deleted_at") is None,
                )
            ],
        )
        # Captured live: PK (id); status CHECK in (in_progress, uploading, ready,
        # finalizing, aborting, completed, aborted). The presigned lane's durable
        # pending store (multipart_upload_id = 'presigned') and TUS share it.
        self.uploads_inflight = _Table(
            models_files.UploadsInflight,
            {"upload_offset": 0, "metadata": {}, "parts": [], "status": "in_progress"},
            [],
        )
        self.permissions = _Table(models_iam.Permissions, {"status": "active"}, [])
        self.share_links = _CascadeStub()
        self.cascade_only = {name: _CascadeStub() for name in _CASCADE_ONLY_MODELS}
        # RPC names that raise as if the SQL function were missing — drives the
        # engine onto the ORM fallback cascade.
        self.unavailable_rpcs: set[str] = set()
        # Hooks run before an RPC executes: ``hook(schema, function, *args)``. A test
        # uses one to inject a database failure into one named function.
        self.before_rpc: list[Any] = []
        self.org_members: set[tuple[str, str]] = set()

    # -- seeding -------------------------------------------------------
    def seed_file(self, **values: Any) -> dict[str, Any]:
        """Insert a row through the same constraints the live table enforces."""
        values.setdefault("file_name", str(values.get("file_path", "f")).rsplit("/", 1)[-1])
        values.setdefault("storage_uri", f"s3://test-bucket/seed/{uuid.uuid4()}")
        return self.files.create_sync(**values).to_dict()

    # -- the driver ----------------------------------------------------
    def models(self) -> tuple[Any, Any]:
        files_models = {
            "Files": self.files,
            "Folders": self.folders,
            "FileVersions": self.file_versions,
            "UploadsInflight": self.uploads_inflight,
            **self.cascade_only,
        }
        return SimpleNamespace(**files_models), SimpleNamespace(Permissions=self.permissions)

    def rpc(self, schema: str, function: str, *args: Any, mode: str = "scalar") -> Any:
        for hook in self.before_rpc:
            hook(schema, function, *args)
        if function in self.unavailable_rpcs:
            # What ``matrx_orm.call_function`` surfaces when the SQL function is not
            # installed: asyncpg's own UndefinedFunctionError, SQLSTATE 42883, raised
            # before the function body runs — nothing in the double's rows changes.
            from asyncpg.exceptions import UndefinedFunctionError

            raise UndefinedFunctionError(f"function {schema}.{function}(unknown) does not exist")
        if (schema, function) == ("public", "bump_version"):
            return self._bump_version(str(args[0]))
        if (schema, function) == ("iam", "has_org_access_for"):
            user_id, org_id = args
            return (str(user_id), str(org_id)) in self.org_members
        if (schema, function) == ("files", "soft_delete_file"):
            # Captured live 2026-09-10: UPDATE files.files SET deleted_at = now()
            # WHERE id = p_file_id AND deleted_at IS NULL (share links: not modeled).
            hit = self.files.update_where_sync(
                {"id": str(args[0]), "deleted_at__isnull": True}, deleted_at=_ts()
            )
            return bool(hit.rows_affected)
        if (schema, function) == ("files", "hard_delete_file"):
            return self._hard_delete_file(str(args[0]))
        if (schema, function) == ("public", "move_file"):
            return self._move_file(str(args[0]), args[1])
        if (schema, function) == ("public", "rename_file"):
            return self._rename_file(str(args[0]), str(args[1]))
        if (schema, function) == ("files", "ensure_folder_chain"):
            if len(args) != 3:
                # AD240: the org-less 2-argument form is being retired (package sql 043);
                # a caller still using it is a caller that lets the database pick the org.
                from asyncpg.exceptions import UndefinedFunctionError

                raise UndefinedFunctionError(
                    f"function files.ensure_folder_chain({len(args)} args) does not exist — "
                    "pass (owner_id, folder_path, organization_id)"
                )
            return self._ensure_folder_chain(str(args[0]), args[1], args[2])
        raise NotImplementedError(f"files double has no RPC {schema}.{function}")

    def _rename_file(self, file_id: str, new_name: str) -> dict[str, Any]:
        """``public.rename_file`` as read from ``pg_proc`` on Matrx Main 2026-09-15, for a
        service-role caller (``auth.uid()`` NULL, editor gate skipped): the live file or
        ``no_data_found``; ``files.assert_safe_file_name`` (only its separator rule is modeled:
        ``/`` or ``\\`` -> 22023); keep ``file_path``'s directory and replace the last segment;
        UPDATE through the unique indexes, so a taken path raises 23505 (the caller's 409)."""
        row = self.files.rows.get(file_id)
        if row is None or row.get("deleted_at") is not None:
            raise _PgError("P0002", f"file {file_id} not found")
        if "/" in new_name or "\\" in new_name:
            raise _PgError("22023", f"invalid file name {new_name}: a file name is ONE path segment")
        old_path = row["file_path"]
        new_path = new_name if "/" not in old_path else f"{old_path.rsplit('/', 1)[0]}/{new_name}"
        self.files.update_where_sync({"id": file_id}, file_name=new_name, file_path=new_path, updated_at=_ts())
        return {"file_id": file_id, "old_path": old_path, "new_path": new_path, "file_name": new_name}

    def _ensure_folder_chain(
        self, owner_id: str, folder_path: str | None, organization_id: str | None
    ) -> str | None:
        """``files.ensure_folder_chain(p_owner_id, p_folder_path, p_organization_id)`` as written
        in ``cloud_sync/sql/041`` (live 2026-09-15): a NULL organization raises 22004 before any row
        is touched; trim ``/``, an empty path returns NULL; each segment reuses the owner's live
        folder at that path (the ``ON CONFLICT ... DO UPDATE`` arm — its organization is NOT
        rewritten) or is inserted under the previous one WITH the named organization; the leaf id
        is returned. Held to the SQL by ``test_ensure_folder_chain_explicit_org.py``. Since
        2026-10-12 (live) the conflict key is (owner, organization, path): only the owner's folder
        IN THIS ORGANIZATION is reused; another organization's folder at the path is not."""
        if organization_id is None:
            raise _PgError(
                "22004",
                "ensure_folder_chain: p_organization_id is required — the organization is never defaulted",
            )
        path = str(folder_path or "").strip("/")
        if not path:
            return None
        parent: str | None = None
        current = ""
        for part in path.split("/"):
            current = part if not current else f"{current}/{part}"
            live = next(
                (
                    r
                    for r in self.folders.rows.values()
                    if r.get("created_by") == owner_id
                    and str(r.get("organization_id")) == str(organization_id)
                    and r.get("folder_path") == current
                    and r.get("deleted_at") is None
                ),
                None,
            )
            if live is not None:
                self.folders.update_where_sync({"id": live["id"]}, updated_at=_ts())
                parent = live["id"]
            else:
                parent = self.folders.create_sync(
                    created_by=owner_id,
                    folder_path=current,
                    folder_name=part,
                    parent_id=parent,
                    organization_id=str(organization_id),
                ).to_dict()["id"]
        return parent

    def _bump_version(self, file_id: str) -> int:
        """``public.bump_version`` as read from ``pg_proc`` on Matrx Main 2026-09-15, for a
        service-role caller (``auth.uid()`` NULL, so the editor gate is skipped):
        ``UPDATE files.files SET current_version = current_version + 1, updated_at = now()
        WHERE id = p_file_id AND deleted_at IS NULL RETURNING current_version``; no row
        raises ``no_data_found``."""
        row = self.files.rows.get(file_id)
        if row is None or row.get("deleted_at") is not None:
            raise LookupError(f"bump_version: file {file_id} not found or deleted (SQLSTATE P0002)")
        new_version = row["current_version"] + 1
        self.files.update_where_sync(
            {"id": file_id, "deleted_at__isnull": True}, current_version=new_version, updated_at=_ts()
        )
        return new_version

    def _move_file(self, file_id: str, folder_id: str | None) -> dict[str, Any]:
        """``public.move_file`` as written in ``cloud_sync/sql/030_rename_and_move_file.sql``
        (live-verified 2026-09-13), for a service-role caller (``auth.uid()`` NULL,
        so both editor gates are skipped): load the live file, NULL folder = the
        file's own org root, refuse a cross-organization move (42501), recompute
        ``file_path`` from the folder and UPDATE through the unique indexes."""
        row = self.files.rows.get(file_id)
        if row is None or row.get("deleted_at") is not None:
            raise LookupError(f"file {file_id} not found (SQLSTATE P0002)")
        if folder_id is None:
            folder_path, folder_org = "", row.get("organization_id")
        else:
            folder = self.folders.rows.get(str(folder_id))
            if folder is None or folder.get("deleted_at") is not None:
                raise LookupError(f"folder {folder_id} not found (SQLSTATE P0002)")
            folder_path = (folder.get("folder_path") or "").strip("/")
            folder_org = folder.get("organization_id")
        if folder_org != row.get("organization_id"):
            raise PermissionError(
                f"cross-organization move refused: file {file_id} belongs to organization "
                f"{row.get('organization_id')}, folder {folder_id} to organization {folder_org}"
            )
        old_path = row["file_path"]
        new_path = row["file_name"] if not folder_path else f"{folder_path}/{row['file_name']}"
        self.files.update_where_sync({"id": file_id}, parent_folder_id=folder_id, file_path=new_path)
        return {"file_id": file_id, "old_path": old_path, "new_path": new_path, "folder_id": folder_id}

    def _hard_delete_file(self, file_id: str) -> dict[str, Any]:
        """``files.hard_delete_file`` as written in ``cloud_sync/sql/042`` (service-role
        caller): hard-delete every ``parent_file_id`` child first, then the row; report
        ``main`` + child URIs. A child's ``retained`` URIs are candidates again once the
        parent row is gone (AD238) — retained only if a SURVIVING row still names them.
        ``files.files.duplicate_of_file_id`` / ``parent_file_id`` are FOREIGN KEY
        ... ON DELETE SET NULL."""
        extra: list[str] = []
        child_retained: list[str] = []
        for child in [r for r in self.files.rows.values() if r.get("parent_file_id") == file_id]:
            report = self._hard_delete_file(child["id"])
            extra += [u for u in [report["main"], *report["versions"]] if u]
            child_retained += report.get("retained") or []
        row = self.files.rows.get(file_id)
        if row is None:
            return {
                "main": None,
                "versions": extra,
                "main_retained": False,
                "retained": list(dict.fromkeys(child_retained)),
            }
        version_uris = [
            r.get("storage_uri")
            for r in self.file_versions.rows.values()
            if r.get("file_id") == file_id and r.get("storage_uri")
        ]
        client = self.client()
        client._rehome_aliases_for_hard_delete(self.models()[0], file_id)
        self.file_versions.delete_where_sync(file_id=file_id)
        main = row.get("storage_uri")
        self.files.delete_row_sync(file_id, set_null_fks=("duplicate_of_file_id", "parent_file_id"))
        candidates = [u for u in [main, *version_uris, *extra, *child_retained] if u]
        purge, retained = client._partition_referenced_uris(self.models()[0], candidates)
        main_retained = bool(main and main in retained)
        return {
            "main": None if main_retained else main,
            "versions": [u for u in purge if u != main],
            "main_retained": main_retained,
            "retained": retained,
        }

    def client(self) -> DatabaseClient:
        client = DatabaseClient(SimpleNamespace())

        async def _rpc(schema: str, function: str, *args: Any, mode: str = "scalar") -> Any:
            return self.rpc(schema, function, *args, mode=mode)

        client._rpc = _rpc  # type: ignore[method-assign]
        client._rpc_sync = self.rpc  # type: ignore[method-assign]
        # The pool every query above runs on: the name ``bind_to_host`` / ``bootstrap_db``
        # register. Nothing is registered here, so the real resolver would scream.
        client._db_name = lambda: PACKAGE_DB_NAME  # type: ignore[method-assign]
        return client

    @asynccontextmanager
    async def _transaction(self, database: str | None = None):
        """``matrx_orm.transaction`` over the double. Every ``_rpc`` and model write inside
        the block joins it (``call_function`` reads the active connection), so it must be
        opened on the pool those run on, and a raise inside it rolls every in-memory row
        back like the Postgres ROLLBACK. S3 writes are not transactional and stay."""
        if database != PACKAGE_DB_NAME:
            raise RuntimeError(
                f"transaction opened on {database!r}, not the matrx-files pool "
                f"{PACKAGE_DB_NAME!r} every DatabaseClient query runs on"
            )
        tables = (self.files, self.file_versions, self.folders, self.permissions)
        snapshot = [copy.deepcopy(table.rows) for table in tables]
        try:
            yield
        except BaseException:
            for table, rows in zip(tables, snapshot, strict=True):
                table.rows.clear()
                table.rows.update(rows)
            raise

    @contextmanager
    def bound(self):
        # ``purge_escape`` opens a real Postgres transaction and sets
        # ``matrx.purge_root_id`` in it — the D23 tombstone-retention escape
        # (migration 033). This double replaces the SQL executor entirely, so
        # there is no transaction to open and no BEFORE DELETE trigger to
        # escape; the block is replaced by a no-op that still asserts the root
        # id is a uuid, which is the only half of the contract a Postgres-less
        # executor can honor. The escape itself is proven against the live DB
        # in ``test_tombstone_retention_floor.py``.
        @contextmanager
        def _no_postgres_escape(root_file_id):
            from matrx_files.cloud_sync.purge_escape import _normalize_root

            _normalize_root(root_file_id)
            yield

        @asynccontextmanager
        async def _escape(root_file_id):
            with _no_postgres_escape(root_file_id):
                yield

        with (
            patch("matrx_files.cloud_sync.db._models", self.models),
            patch(
                "matrx_files.cloud_sync.db.DatabaseClient._share_model",
                return_value=self.share_links,
            ),
            patch("matrx_files.cloud_sync.purge_escape.purge_escape", _escape),
            patch("matrx_orm.transaction", self._transaction),
        ):
            yield self

    def live_files(self) -> list[dict[str, Any]]:
        return [r for r in self.files.rows.values() if r.get("deleted_at") is None]


class ObjectStore:
    """S3 stand-in: storage_uri -> bytes."""

    def __init__(self) -> None:
        self.objects: dict[str, bytes] = {}
        self.puts: list[str] = []  # every PUT ever issued, even if later deleted

    async def write_async(self, uri: str, data: bytes, content_type: str | None = None) -> None:
        self.write(uri, data, content_type)

    async def delete_async(self, uri: str) -> None:
        self.objects.pop(uri, None)

    async def read_async(self, uri: str) -> bytes:
        if uri not in self.objects:
            raise FileNotFoundError(uri)
        return self.objects[uri]

    def read(self, uri: str) -> bytes:
        if uri not in self.objects:
            raise FileNotFoundError(uri)
        return self.objects[uri]

    def write(self, uri: str, data: bytes, content_type: str | None = None) -> None:
        self.puts.append(uri)
        self.objects[uri] = bytes(data)

    def delete(self, uri: str) -> None:
        self.objects.pop(uri, None)


@dataclass
class Grants:
    """ACL checker stand-in: (user, resource_id, level) tuples that pass."""

    allowed: set[tuple[str, str, str]] = field(default_factory=set)

    async def require_async(self, resource_type: str, resource_id: str, minimum: str = "read", user_id: str | None = None) -> str:
        return self.require(resource_type, resource_id, minimum, user_id)

    def require(self, resource_type: str, resource_id: str, minimum: str = "read", user_id: str | None = None) -> str:
        if (str(user_id), str(resource_id), minimum) not in self.allowed:
            raise PermissionError(f"User '{user_id}' lacks '{minimum}' on {resource_type} {resource_id}")
        return minimum


@dataclass
class VersionLog:
    recorded: list[tuple[str, str]] = field(default_factory=list)

    async def record_version_async(self, record: dict, content: bytes, *, checksum: str, change_summary: str | None = None, user_id: str | None = None) -> None:
        self.record_version(record, content, checksum=checksum, change_summary=change_summary, user_id=user_id)

    def record_version(self, record: dict, content: bytes, *, checksum: str, change_summary: str | None = None, user_id: str | None = None) -> None:
        self.recorded.append((str(record["id"]), checksum))


def build_engine(db: FilesDB, *, user_id: str, organization_id: str) -> SyncEngine:
    """A real SyncEngine wired to the real DatabaseClient over the double.

    ``organization_id`` is REQUIRED because a write's organization is CARRIED,
    never defaulted: it is the organization the host boundary admitted for this
    request. Installing it here is the same seam a real host installs with
    ``matrx_utils.conf.configure_context`` — the package reads it and refuses a
    write when it is absent, and it NEVER asks who the owner is instead
    (common-docs/policies/context-is-carried-never-rebuilt.md). The autouse
    ``conftest`` fixture restores the seam after each test.
    """
    from matrx_utils import ctx as matrx_ctx

    matrx_ctx._context_getter = lambda: matrx_ctx.SimpleUserContext(
        user_id=user_id,
        is_authenticated=True,
        organization_id=organization_id,
    )

    engine = object.__new__(SyncEngine)
    engine._config = SimpleNamespace(
        user_id=user_id,
        storage_backend="s3",
        resolve_s3_bucket=lambda: "test-bucket",
    )
    engine._router = ObjectStore()
    engine._db = db.client()
    engine.permissions = Grants()
    engine.versions = VersionLog()
    engine._variants_service = None
    engine._fm_ref = None
    return engine
