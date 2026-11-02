"""In-memory doubles for the TUS suites (test_tus_wire.py, test_tus_dedup.py).

The doubles replace only what ``TUSSessionManager`` and the TUS router CALL:

* the boto3 S3 client (multipart create / upload_part / complete / abort,
  head / delete) with S3's real assembly rules: parts are concatenated in the
  order the CompleteMultipartUpload list names them, the list must ascend,
  every ETag must match an uploaded part, unlisted parts are dropped, and a
  FULL_OBJECT SHA-256 upload returns the base64 SHA-256 of the assembled
  bytes (COMPOSITE returns the ``<b64>-<n>`` hash-of-hashes form);
* the matrx-orm model layer for ``files.uploads_inflight`` / ``files.files``
  (rows in dicts, the lookup operators this package uses, the real
  ``UpdateResult`` type, and the live unique constraints the finalize path
  depends on — ``(created_by, file_path)`` and the dedup canonical index on
  ``(organization_id, created_by, checksum)`` for root, non-alias rows);
* the iam RPCs (org membership), the host access checker, the folder-chain
  RPC, and the best-effort thumbnail kick-off;
* the HOST BOUNDARY itself — ``build_world`` registers a context getter
  (what ``configure_context`` installs in a real host) so every write in the
  world runs with the organization the boundary admitted, CARRIED, never
  resolved from an organization picked for the owner
  (common-docs/policies/context-is-carried-never-rebuilt.md).

Everything the SUT owns runs for real: the router, the manager's state
machine, ``SyncEngine._resolve_write_organization_id_async`` /
``_validate_duplicate_target_async``, ``PermissionsManager.require_async``,
``DatabaseClient.get_file_by_checksum_async`` (the dedup scope query), and
``tus_cleanup.sweep_once``.

Expected values in the tests come from the TUS 1.0.0 spec, literals, and
``hashlib`` over the bytes the test uploaded — never from these doubles.
"""

from __future__ import annotations

import asyncio
import base64
import hashlib
import inspect
import io
import uuid
import itertools
import re
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from posixpath import dirname
from types import SimpleNamespace
from typing import Any

import pytest
from matrx_orm.core.types import UpdateResult

from matrx_files.cloud_sync.config import CloudSyncConfig
from matrx_files.cloud_sync.sync_engine import SyncEngine
from matrx_files.cloud_sync.transports.tus import (
    TUSFinalizeResult,
    TUSSessionManager,
)

BUCKET = "test-bucket"
MIN_PART = 4  # manager min_part_bytes for the suites; S3's 5 MiB rule is the manager's job
_EPOCH = datetime(2026, 1, 1, tzinfo=UTC)


# ---------------------------------------------------------------------------
# S3
# ---------------------------------------------------------------------------


class S3ClientError(Exception):
    """botocore ClientError envelope: ``exc.response['Error']['Code']``."""

    def __init__(self, code: str, message: str | None = None) -> None:
        self.response = {"Error": {"Code": code, "Message": message or code}}
        super().__init__(f"{code}: {message or code}")


def _b64(raw: bytes) -> str:
    return base64.b64encode(raw).decode("ascii")


class FakeS3Client:
    """The boto3 S3 client subset TUS uses, with real multipart semantics."""

    def __init__(
        self,
        *,
        reject_full_object_sha256: bool = False,
        checksum_override: str | None = None,
    ) -> None:
        self.objects: dict[tuple[str, str], bytes] = {}
        self.uploads: dict[str, dict[str, Any]] = {}
        self.create_calls: list[dict[str, Any]] = []
        self.complete_calls = 0
        self.reject_full_object_sha256 = reject_full_object_sha256
        self.checksum_override = checksum_override
        # op name -> exception raised INSTEAD of performing the op
        self.fail: dict[str, BaseException] = {}
        # op name -> exception raised AFTER the op took effect (lost response)
        self.fail_after: dict[str, BaseException] = {}
        # op name -> callable run on entry (thread-side; use threading primitives)
        self.before: dict[str, Callable[[], None]] = {}
        self._ids = itertools.count(1)

    def _enter(self, op: str) -> None:
        hook = self.before.get(op)
        if hook is not None:
            hook()
        exc = self.fail.get(op)
        if exc is not None:
            raise exc

    def _leave(self, op: str) -> None:
        exc = self.fail_after.get(op)
        if exc is not None:
            raise exc

    def create_multipart_upload(
        self,
        *,
        Bucket: str,
        Key: str,
        ChecksumAlgorithm: str | None = None,
        ChecksumType: str | None = None,
        ContentType: str | None = None,
    ) -> dict[str, Any]:
        self.create_calls.append(
            {
                "Bucket": Bucket,
                "Key": Key,
                "ChecksumAlgorithm": ChecksumAlgorithm,
                "ChecksumType": ChecksumType,
            }
        )
        self._enter("create_multipart_upload")
        if self.reject_full_object_sha256 and ChecksumType == "FULL_OBJECT":
            raise S3ClientError(
                "InvalidRequest",
                "The FULL_OBJECT checksum type cannot be used with the sha256 checksum algorithm.",
            )
        upload_id = f"mpu-{next(self._ids)}"
        self.uploads[upload_id] = {
            "Bucket": Bucket,
            "Key": Key,
            "algorithm": ChecksumAlgorithm,
            "type": ChecksumType,
            "parts": {},
        }
        return {"Bucket": Bucket, "Key": Key, "UploadId": upload_id}

    def _upload(self, bucket: str, key: str, upload_id: str) -> dict[str, Any]:
        up = self.uploads.get(upload_id)
        if up is None or up["Bucket"] != bucket or up["Key"] != key:
            raise S3ClientError("NoSuchUpload", "The specified upload does not exist.")
        return up

    def upload_part(
        self, *, Bucket: str, Key: str, UploadId: str, PartNumber: int,
        Body: bytes | Any,
    ) -> dict[str, Any]:
        self._enter("upload_part")
        up = self._upload(Bucket, Key, UploadId)
        # Real S3 accepts bytes OR a file-like Body and streams the latter, which
        # is how the PATCH handler avoids holding a whole chunk in memory. The
        # double has to accept both or it would fail the streaming path for a
        # reason S3 never would.
        data = bytes(Body.read()) if hasattr(Body, "read") else bytes(Body)
        etag = f'"{hashlib.md5(data).hexdigest()}"'
        up["parts"][PartNumber] = (etag, data)
        self._leave("upload_part")
        return {"ETag": etag}

    def complete_multipart_upload(
        self,
        *,
        Bucket: str,
        Key: str,
        UploadId: str,
        MultipartUpload: dict[str, Any],
    ) -> dict[str, Any]:
        self._enter("complete_multipart_upload")
        up = self._upload(Bucket, Key, UploadId)
        listed = list(MultipartUpload.get("Parts") or [])
        if not listed:
            raise S3ClientError("MalformedXML", "no parts listed")
        numbers = [int(p["PartNumber"]) for p in listed]
        if numbers != sorted(set(numbers)):
            raise S3ClientError("InvalidPartOrder", f"parts not ascending: {numbers}")
        chunks: list[bytes] = []
        for p in listed:
            stored = up["parts"].get(int(p["PartNumber"]))
            if stored is None or stored[0] != p["ETag"]:
                raise S3ClientError("InvalidPart", f"part {p['PartNumber']} not uploaded")
            chunks.append(stored[1])
        data = b"".join(chunks)
        self.objects[(Bucket, Key)] = data
        del self.uploads[UploadId]
        self.complete_calls += 1
        resp: dict[str, Any] = {"Bucket": Bucket, "Key": Key, "ETag": '"assembled"'}
        if self.checksum_override is not None:
            resp["ChecksumSHA256"] = self.checksum_override
        elif up["algorithm"] == "SHA256":
            if up["type"] == "FULL_OBJECT":
                resp["ChecksumSHA256"] = _b64(hashlib.sha256(data).digest())
            else:
                composite = hashlib.sha256(
                    b"".join(hashlib.sha256(c).digest() for c in chunks)
                ).digest()
                resp["ChecksumSHA256"] = f"{_b64(composite)}-{len(chunks)}"
        self._leave("complete_multipart_upload")
        return resp

    def copy_object(self, *, CopySource: dict[str, str], Bucket: str, Key: str, **_: Any) -> dict[str, Any]:
        src = self.objects.get((CopySource["Bucket"], CopySource["Key"]))
        if src is None:
            raise S3ClientError("NoSuchKey")
        self.objects[(Bucket, Key)] = src
        return {}

    def head_object(self, *, Bucket: str, Key: str) -> dict[str, Any]:
        self._enter("head_object")
        data = self.objects.get((Bucket, Key))
        if data is None:
            raise S3ClientError("404", "Not Found")
        return {"ContentLength": len(data)}

    def get_object(self, *, Bucket: str, Key: str) -> dict[str, Any]:
        """Streaming read of an assembled object.

        Used by the streamed SHA-256 re-hash the declared-checksum contract
        falls back to when S3 will not supply a FULL_OBJECT checksum. The Body
        is a real chunked reader so a test proves the hasher streams rather than
        buffering the whole object.
        """
        self._enter("get_object")
        data = self.objects.get((Bucket, Key))
        if data is None:
            raise S3ClientError("404", "Not Found")
        return {"ContentLength": len(data), "Body": io.BytesIO(data)}

    def delete_object(self, *, Bucket: str, Key: str) -> dict[str, Any]:
        self._enter("delete_object")
        self.objects.pop((Bucket, Key), None)
        return {}

    def abort_multipart_upload(self, *, Bucket: str, Key: str, UploadId: str) -> dict[str, Any]:
        self._enter("abort_multipart_upload")
        self._upload(Bucket, Key, UploadId)
        del self.uploads[UploadId]
        return {}


# ---------------------------------------------------------------------------
# matrx-orm model layer
# ---------------------------------------------------------------------------


class UniqueViolation(Exception):
    """asyncpg UniqueViolationError surface: SQLSTATE and constraint as attributes, as asyncpg carries them."""

    sqlstate = "23505"

    def __init__(self, message: str) -> None:
        super().__init__(message)
        named = re.search(r'unique constraint "([^"]+)"', message)
        self.constraint_name = named.group(1) if named else None


def _matches(row: dict[str, Any], filters: dict[str, Any]) -> bool:
    for key, expected in filters.items():
        name, _, op = key.partition("__")
        actual = row.get(name)
        if op == "":
            ok = actual == expected
        elif op == "in":
            ok = actual in expected
        elif op == "isnull":
            ok = (actual is None) == bool(expected)
        elif op == "lt":
            ok = actual is not None and actual < expected
        else:
            raise AssertionError(f"fake ORM does not implement lookup {key!r}")
        if not ok:
            return False
    return True


class FakeInstance:
    def __init__(self, data: dict[str, Any]) -> None:
        self._data = dict(data)

    def to_dict(self) -> dict[str, Any]:
        return dict(self._data)


class FakeQuery:
    def __init__(
        self,
        table: FakeTable,
        filters: dict[str, Any],
        order: tuple[str, ...] = (),
        limit: int | None = None,
    ) -> None:
        self._table = table
        self._filters = filters
        self._order = order
        self._limit = limit

    def filter(self, **more: Any) -> FakeQuery:
        return FakeQuery(self._table, {**self._filters, **more}, self._order, self._limit)

    def order_by(self, *fields: str) -> FakeQuery:
        return FakeQuery(self._table, self._filters, fields, self._limit)

    def limit(self, n: int) -> FakeQuery:
        return FakeQuery(self._table, self._filters, self._order, n)

    def _select(self) -> list[dict[str, Any]]:
        rows = [dict(r) for r in self._table.rows.values() if _matches(r, self._filters)]
        for name in reversed(self._order):
            desc = name.startswith("-")
            col = name.lstrip("-")
            rows.sort(key=lambda r: (r.get(col) is None, r.get(col)), reverse=desc)
        return rows[: self._limit] if self._limit is not None else rows

    async def first(self) -> FakeInstance | None:
        await asyncio.sleep(0)
        rows = self._select()
        return FakeInstance(rows[0]) if rows else None

    async def values(self, *cols: str) -> list[dict[str, Any]]:
        await asyncio.sleep(0)
        return [{c: r.get(c) for c in cols} for r in self._select()]


UniqueRule = Callable[[dict[str, Any], list[dict[str, Any]]], str | None]


class FakeTable:
    def __init__(self, name: str, *, unique: UniqueRule | None = None) -> None:
        self.name = name
        self.rows: dict[str, dict[str, Any]] = {}
        self._unique = unique
        self._seq = itertools.count(1)
        self.before_create: Callable[[dict[str, Any]], Awaitable[None] | None] | None = None
        self.fail_after_commit: BaseException | None = None

    def _stamp(self, values: dict[str, Any]) -> dict[str, Any]:
        row = dict(values)
        row["id"] = str(row.get("id") or uuid.uuid4())  # the column default, as in the DB
        row.setdefault("created_at", _EPOCH + timedelta(seconds=next(self._seq)))
        row.setdefault("deleted_at", None)
        if self.name == "cld_files":
            row.setdefault("current_version", 1)  # files.files.current_version DEFAULT 1
        return row

    def seed(self, **values: Any) -> dict[str, Any]:
        row = self._stamp(values)
        self.rows[row["id"]] = row
        return row

    async def create(self, **values: Any) -> FakeInstance:
        await asyncio.sleep(0)
        if self.before_create is not None:
            maybe = self.before_create(values)
            if inspect.isawaitable(maybe):
                await maybe
        row = self._stamp(values)
        if row["id"] in self.rows:
            raise UniqueViolation(
                f'duplicate key value violates unique constraint "{self.name}_pkey" (SQLSTATE 23505)'
            )
        if self._unique is not None:
            violation = self._unique(row, list(self.rows.values()))
            if violation:
                raise UniqueViolation(violation)
        self.rows[row["id"]] = row
        if self.fail_after_commit is not None:
            raise self.fail_after_commit
        return FakeInstance(row)

    def filter(self, **filters: Any) -> FakeQuery:
        return FakeQuery(self, filters)

    async def update_where(self, filters: dict[str, Any], **updates: Any) -> UpdateResult:
        await asyncio.sleep(0)
        hit = [r for r in self.rows.values() if _matches(r, filters)]
        for r in hit:
            r.update(updates)
        return UpdateResult(rows_affected=len(hit), updated_rows=[dict(r) for r in hit])


def _is_canonical(row: dict[str, Any]) -> bool:
    return bool(
        row.get("checksum")
        and row.get("deleted_at") is None
        and row.get("duplicate_of_file_id") is None
        and row.get("parent_file_id") is None
    )


def _files_unique(new: dict[str, Any], rows: list[dict[str, Any]]) -> str | None:
    for r in rows:
        if r.get("deleted_at") is not None:
            continue
        if r.get("created_by") == new.get("created_by") and r.get("file_path") == new.get("file_path"):
            return (
                "duplicate key value violates unique constraint "
                '"cld_files_owner_id_file_path_key" (SQLSTATE 23505)'
            )
        if (
            _is_canonical(new)
            and _is_canonical(r)
            and r.get("checksum") == new.get("checksum")
            and r.get("organization_id") == new.get("organization_id")
            and r.get("created_by") == new.get("created_by")
        ):
            return (
                "duplicate key value violates unique constraint "
                '"cld_files_dedup_canonical" (SQLSTATE 23505)'
            )
    return None


# ---------------------------------------------------------------------------
# World
# ---------------------------------------------------------------------------


#: The organization the host boundary admitted for every request in a world.
#: An organization is TENANCY, not a per-user workspace: several owners act in
#: this one organization, exactly as they do live.
CARRIED_ORG = "org-carried-0001"


@dataclass
class TusWorld:
    s3: FakeS3Client
    inflight: FakeTable
    files: FakeTable
    engine: SyncEngine
    manager: TUSSessionManager
    org_members: dict[str, set[str]] = field(default_factory=dict)
    # (user_id, resource_type, resource_id, level) granted by the host checker
    grants: set[tuple[str, str, str, str]] = field(default_factory=set)
    folder_calls: list[tuple[str, str, str]] = field(default_factory=list)
    folder_failure: BaseException | None = None
    folder_hook: Callable[[str, str, str], Awaitable[None]] | None = None

    @property
    def file_manager(self) -> SimpleNamespace:
        return SimpleNamespace(sync_engine=self.engine)

    def session_row(self, upload_id: str) -> dict[str, Any]:
        return self.inflight.rows[upload_id]

    def object_at(self, key: str) -> bytes | None:
        return self.s3.objects.get((BUCKET, key))

    def live_files(self) -> list[dict[str, Any]]:
        return [r for r in self.files.rows.values() if r.get("deleted_at") is None]


def build_world(
    monkeypatch: pytest.MonkeyPatch,
    *,
    s3: FakeS3Client | None = None,
    min_part_bytes: int = MIN_PART,
) -> TusWorld:
    s3 = s3 or FakeS3Client()
    inflight = FakeTable("uploads_inflight")
    files = FakeTable("cld_files", unique=_files_unique)
    versions = FakeTable("file_versions")
    mf = SimpleNamespace(UploadsInflight=inflight, Files=files, FileVersions=versions)

    def models() -> tuple[SimpleNamespace, SimpleNamespace]:
        return mf, SimpleNamespace()

    for module in (
        "matrx_files.cloud_sync.transports.tus",
        "matrx_files.cloud_sync.transports.tus_cleanup",
        "matrx_files.cloud_sync.db",
    ):
        monkeypatch.setattr(f"{module}._models", models)

    router = SimpleNamespace(
        is_configured=lambda name: name == "s3",
        s3=SimpleNamespace(_get_client=lambda: s3),
    )
    engine = SyncEngine(CloudSyncConfig(s3_bucket=BUCKET), router)
    manager = TUSSessionManager(engine, min_part_bytes=min_part_bytes)
    engine._tus_manager = manager
    world = TusWorld(s3=s3, inflight=inflight, files=files, engine=engine, manager=manager)

    # The host boundary. A real host calls ``matrx_utils.conf.configure_context``
    # with a getter that returns the request's admitted context; the package
    # READS the organization off it and refuses a write when there is none. The
    # world installs the same seam, so the TUS suites exercise the carried
    # organization instead of a personal-org default.
    from matrx_utils import ctx as _matrx_ctx

    monkeypatch.setattr(
        _matrx_ctx,
        "_context_getter",
        lambda: _matrx_ctx.SimpleUserContext(
            user_id="",
            is_authenticated=True,
            organization_id=CARRIED_ORG,
        ),
    )

    async def rpc(schema: str, function: str, *args: Any, mode: str = "scalar") -> Any:
        if (schema, function) == ("iam", "has_org_access_for"):
            user_id, org_id = args
            return user_id in world.org_members.get(org_id, set())
        raise AssertionError(f"TUS path made an unexpected RPC {schema}.{function}{args}")

    monkeypatch.setattr(engine._db, "_rpc", rpc)

    async def ensure_folder(file_path: str, user_id: str, org_id: str) -> str:
        world.folder_calls.append((file_path, user_id, org_id))
        if world.folder_hook is not None:
            await world.folder_hook(file_path, user_id, org_id)
        if world.folder_failure is not None:
            raise world.folder_failure
        return f"folder:{org_id}:{dirname(file_path)}"

    monkeypatch.setattr(engine, "_ensure_folder_async", ensure_folder)

    async def access_checker(user_id: str, resource_type: str, resource_id: str, level: str) -> bool:
        return (user_id, resource_type, resource_id, level) in world.grants

    monkeypatch.setattr("matrx_files.cloud_sync.permissions._access_checker", access_checker)

    async def no_thumbnail(fm: Any, file_id: str, **_: Any) -> bool:
        return False

    monkeypatch.setattr(
        "matrx_files.cloud_sync.processing.generate_thumbnail_for_file", no_thumbnail
    )
    return world


def chunks_of(content: bytes, size: int = MIN_PART) -> list[bytes]:
    return [content[i : i + size] for i in range(0, len(content), size)]


async def upload_to_ready(
    world: TusWorld,
    *,
    owner: str,
    path: str,
    content: bytes,
    metadata: dict[str, Any] | None = None,
) -> str:
    """Create a session and append every chunk; returns the upload id (status ready)."""
    created = await world.manager.create_async(
        owner_id=owner,
        file_path=path,
        upload_length=len(content),
        metadata=metadata,
    )
    offset = 0
    for chunk in chunks_of(content):
        appended = await world.manager.append_async(
            upload_id=created.upload_id,
            owner_id=owner,
            body=chunk,
            client_offset=offset,
        )
        offset = appended.new_offset
    return created.upload_id


async def upload_file(
    world: TusWorld,
    *,
    owner: str,
    path: str,
    content: bytes,
    metadata: dict[str, Any] | None = None,
) -> tuple[str, TUSFinalizeResult]:
    upload_id = await upload_to_ready(
        world, owner=owner, path=path, content=content, metadata=metadata
    )
    result = await world.manager.finalize_async(upload_id=upload_id, owner_id=owner)
    return upload_id, result
