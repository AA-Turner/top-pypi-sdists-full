"""Gated column reads and stored-byte reads — the gate's door for callers that
need a few columns of a file row (or the bytes behind one stored object) and
used to query ``files.files`` / the storage router directly.

Every function here answers the SAME access question as
``FileService.read_record_for_active_user`` and the ``resolve_media`` gate,
FAIL-CLOSED:

* an ambient request user → only rows that user may ``read`` (the host's
  authoritative access checker, ``iam.has_access_for`` in AI Dream);
* an explicit ``matrx_utils.ctx.system_file_access("<job>")`` scope (an
  internal job that declared itself) → every matching row;
* neither → ``PermissionError``. No identity and no declared job = denied.

Two explicit forms of the same answer, for callers that know more than the
ambient context:

* ``user_id=`` — the principal is named by the caller (a background step that
  carries the request's user without an ambient context); the checker decides
  for that user exactly as it would for an ambient one.
* ``parent_grant=`` — a REGISTERED parent door (``"<door>:<parent id>"``):
  the host decided access on the PARENT record the file is reached through
  (a signer link, a social post) the way the public share route decides it on
  the share token. The door is registered once at boot with
  ``register_parent_door(name, reached)``; ``reached(parent_id, file_ids)``
  answers which of those files the parent actually names. Only those files
  pass through the door — an unregistered door, or a file the parent does not
  name, is never served through it (a named principal / declared job may
  still clear the rest). The read still serves only the file's own stored
  objects.

The service-role connection bypasses RLS, so this code IS the access control
for these reads (scripts/check_file_access_gate.py lists every door that skips
it).
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable, Iterable, Sequence
from typing import Any

from matrx_files.cloud_sync.permissions import get_access_checker


logger = logging.getLogger(__name__)


class FileReadDenied(PermissionError):
    """No ambient user and no declared ``system_file_access`` job."""


def _ambient_user_id() -> str:
    from matrx_utils.ctx import get_active_context

    ctx = get_active_context()
    return str(getattr(ctx, "user_id", None) or "").strip() if ctx is not None else ""


def _system_reason() -> str | None:
    from matrx_utils.ctx import get_system_file_access_reason

    return get_system_file_access_reason()


#: ``reached(parent_id, file_ids)`` → the subset of ``file_ids`` the parent record names.
ParentDoor = Callable[[str, frozenset[str]], Awaitable[Iterable[str]]]

_PARENT_DOORS: dict[str, ParentDoor] = {}


def register_parent_door(name: str, reached: ParentDoor) -> None:
    """Register the parent door ``name`` (a token/membership door like the public share route).

    The host decides access on the parent record at its own route; ``reached`` proves which files
    that parent names, so the door can never be used to reach any other file. Re-registering the
    same name replaces it (boot is idempotent).
    """
    door = str(name or "").strip()
    if not door or ":" in door:
        raise ValueError("a parent door is named by one word without ':'")
    _PARENT_DOORS[door] = reached


def registered_parent_doors() -> frozenset[str]:
    return frozenset(_PARENT_DOORS)


def _parent_door(parent_grant: str) -> tuple[ParentDoor, str, str]:
    grant = str(parent_grant or "").strip()
    name, _, parent_id = grant.partition(":")
    name, parent_id = name.strip(), parent_id.strip()
    if not name or not parent_id:
        raise ValueError(
            "parent_grant names a registered parent door and its record: '<door>:<id>'"
        )
    reached = _PARENT_DOORS.get(name)
    if reached is None:
        raise FileReadDenied(
            f"parent door {name!r} is not registered (matrx_files.gated_reads.register_parent_door)"
        )
    return reached, name, parent_id


async def readable_file_ids(
    file_ids: Iterable[str],
    *,
    level: str = "read",
    user_id: str | None = None,
    parent_grant: str | None = None,
) -> set[str]:
    """The subset of ``file_ids`` the current caller may access at ``level``.

    ``user_id`` names the principal explicitly (else the ambient request user);
    ``parent_grant`` passes the files a registered parent door names (see the
    module docstring); the rest still need the principal or a declared job.
    Raises ``FileReadDenied`` when the caller is neither a request user, a named
    principal, a registered parent door, nor a declared internal job.
    """
    ids = {str(i) for i in file_ids if i}
    through_door: set[str] = set()
    if parent_grant is not None:
        reached, name, parent_id = _parent_door(parent_grant)
        through_door = ids & {str(i) for i in await reached(parent_id, frozenset(ids))}
        logger.debug("gated read through parent door %s:%s: %d of %d file(s)",
                     name, parent_id, len(through_door), len(ids))
        ids -= through_door
        if not ids:
            return through_door
        if not (str(user_id or "").strip() or _ambient_user_id() or _system_reason()):
            # The door answered for what its parent names; nothing else is cleared.
            return through_door
    uid = str(user_id or "").strip() or _ambient_user_id()
    if uid:
        checker = get_access_checker()
        if checker is None:
            raise FileReadDenied(
                "file access for a request user needs the host access checker "
                "(matrx_files.configure_access_checker) — none is configured"
            )
        return through_door | {fid for fid in ids if await checker(uid, "file", fid, level)}
    if _system_reason():
        return through_door | ids
    raise FileReadDenied(
        "file access requires an authenticated user or an explicit "
        "matrx_utils.ctx.system_file_access() scope (fail-closed)"
    )


async def read_file_rows(
    columns: Sequence[str],
    *,
    live_only: bool = False,
    order_by: Sequence[str] = (),
    offset: int = 0,
    limit: int | None = None,
    user_id: str | None = None,
    parent_grant: str | None = None,
    where: Any = None,
    **filters: Any,
) -> list[dict[str, Any]]:
    """``files.files`` rows matching ``filters`` (matrx-orm lookups, e.g.
    ``id__in=[…]``, ``created_by=…``), as dicts of ``columns`` plus ``id``,
    keeping only the rows the caller may read. ``live_only`` drops trashed rows;
    ``order_by`` / ``offset`` / ``limit`` page a long scan (an internal job's);
    ``where`` is an optional matrx-orm ``Q`` expression ANDed with ``filters``.

    Columns are always explicit: files.files carries column-list SELECT grants.
    """
    from matrx_files.db.models_files import Files

    if live_only:
        filters.setdefault("deleted_at__isnull", True)
    if not filters and where is None:
        raise ValueError("read_file_rows needs at least one filter — it never scans the whole table")
    wanted = list(dict.fromkeys(["id", *columns]))
    query = Files.filter(where, **filters) if where is not None else Files.filter(**filters)
    if order_by:
        query = query.order_by(*order_by)
    if offset:
        query = query.offset(offset)
    if limit is not None:
        query = query.limit(limit)
    rows = [dict(r) for r in await query.values(*wanted)]
    if not rows:
        return []
    allowed = await readable_file_ids(
        (str(r["id"]) for r in rows), user_id=user_id, parent_grant=parent_grant
    )
    return [r for r in rows if str(r["id"]) in allowed]


async def read_file_row(
    file_id: str,
    columns: Sequence[str],
    *,
    live_only: bool = False,
    user_id: str | None = None,
    parent_grant: str | None = None,
) -> dict[str, Any] | None:
    """One file row's ``columns`` (plus ``id``), or None when it is missing or
    the caller may not read it."""
    if not file_id:
        return None
    rows = await read_file_rows(
        columns, live_only=live_only, user_id=user_id, parent_grant=parent_grant, id=str(file_id)
    )
    return rows[0] if rows else None


async def read_stored_bytes(
    fm: Any,
    file_id: str,
    storage_uri: str,
    *,
    user_id: str | None = None,
    parent_grant: str | None = None,
    operation: Any | None = None,
) -> bytes:
    """The bytes stored at ``storage_uri`` — which must be the file's current
    object or one of its recorded versions — after the gate has cleared the
    caller to read ``file_id`` (ambient user, named ``user_id``, named
    ``parent_grant`` or a declared job — see the module docstring).

    Raises ``FileReadDenied`` / ``PermissionError`` when the caller may not
    read the file, ``FileNotFoundError`` when the object is not one of the
    file's own.
    """
    from matrx_files.db.models_files import Files, FileVersions

    fid = str(file_id or "")
    uri = str(storage_uri or "")
    if not fid or not uri:
        raise FileNotFoundError("a stored-byte read names both the file and its storage object")
    if fid not in await readable_file_ids([fid], user_id=user_id, parent_grant=parent_grant):
        raise PermissionError(f"the caller may not read file {fid}")
    owns = await Files.filter(id=fid, storage_uri=uri).values("id")
    if not owns:
        owns = await FileVersions.filter(file_id=fid, storage_uri=uri).values("id")
    if not owns:
        raise FileNotFoundError(f"storage object is not a version of file {fid}")
    if operation is not None:
        from matrx_files.external_object_runtime import admit_remote

        await admit_remote(fm.sync_engine, uri, operation=operation, unit="stored_bytes_read", file_id=fid)
    raw = await fm.sync_engine.router.read_async(uri)
    return bytes(raw) if isinstance(raw, (bytes, bytearray)) else str(raw).encode("utf-8")


async def read_granted_record(
    fm: Any, file_id: str, *, parent_grant: str, user_id: str | None = None
) -> dict[str, Any] | None:
    """The whole file row for a stream whose access the host decided on the
    PARENT record (``parent_grant="<door>:<id>"`` — a registered parent door),
    e.g. a social post's stored media. A file the parent does not name is
    cleared only by ``user_id``'s own access. None when the row is missing or
    not cleared."""
    fid = str(file_id or "")
    if not fid or fid not in await readable_file_ids([fid], parent_grant=parent_grant, user_id=user_id):
        return None
    return await fm.sync_engine.db.get_file_async(fid)


async def read_folder_rows(
    columns: Sequence[str],
    *,
    live_only: bool = False,
    limit: int | None = None,
    user_id: str | None = None,
    **filters: Any,
) -> list[dict[str, Any]]:
    """``files.folders`` rows matching ``filters`` (matrx-orm lookups), as dicts
    of ``columns`` plus ``id``, keeping only the folders the caller may ``read``.

    Same fail-closed answer as :func:`read_file_rows`, asked of the ``folder``
    resource type: a named ``user_id`` or the ambient request user is checked by
    the host's access checker; a declared ``system_file_access`` job reads all;
    neither raises ``FileReadDenied``.
    """
    from matrx_files.db.models_files import Folders

    if live_only:
        filters.setdefault("deleted_at__isnull", True)
    if not filters:
        raise ValueError("read_folder_rows needs at least one filter — it never scans the whole table")
    wanted = list(dict.fromkeys(["id", *columns]))
    query = Folders.filter(**filters)
    if limit is not None:
        query = query.limit(limit)
    rows = [dict(r) for r in await query.values(*wanted)]
    if not rows:
        return []
    uid = str(user_id or "").strip() or _ambient_user_id()
    if uid:
        checker = get_access_checker()
        if checker is None:
            raise FileReadDenied(
                "folder access for a request user needs the host access checker "
                "(matrx_files.configure_access_checker) — none is configured"
            )
        return [r for r in rows if await checker(uid, "folder", str(r["id"]), "read")]
    if _system_reason():
        return rows
    raise FileReadDenied(
        "folder access requires an authenticated user or an explicit "
        "matrx_utils.ctx.system_file_access() scope (fail-closed)"
    )


async def read_pathway_file_rows_readable(
    pathway: str,
    columns: Sequence[str],
    *,
    user_id: str | None = None,
    organization_id: str | None = None,
    page_size: int = 500,
) -> dict[str, dict[str, Any]]:
    """Every live ``files.files`` row of ``pathway`` the principal may open, id → row of ``columns``
    (plus ``id`` and ``organization_id``).

    The BULK form of the gate for a pathway-scoped scan (the scanner's masters): candidates are read
    page by page by their indexed pathway, and each page is cleared with the page form of the access
    check (``matrx_orm.platform_access_many`` → ``iam.has_access_for_many_in``, the same lanes as
    ``iam.has_access_for``) — never the whole-file-set form, which cost ~2.7 s for a handful of rows.
    ``organization_id`` is an on-page filter that narrows the candidates, never widens. Same fail-closed
    answer as :func:`read_file_rows`: a named ``user_id`` or the ambient user is checked; a declared
    ``system_file_access`` job reads all; neither raises ``FileReadDenied``.
    """
    from matrx_files.db.models_files import Files
    from matrx_orm import platform_access_many

    uid = str(user_id or "").strip() or _ambient_user_id()
    system = bool(_system_reason())
    if not uid and not system:
        raise FileReadDenied(
            "file access requires an authenticated user or an explicit "
            "matrx_utils.ctx.system_file_access() scope (fail-closed)"
        )
    wanted = list(dict.fromkeys(["id", "organization_id", *columns]))
    out: dict[str, dict[str, Any]] = {}
    after: str | None = None
    while True:
        filters: dict[str, Any] = {"file_pathway": pathway, "deleted_at__isnull": True}
        if organization_id:
            filters["organization_id"] = str(organization_id)
        if after:
            filters["id__gt"] = after
        page = [dict(r) for r in await Files.filter(**filters).order_by("id").limit(page_size).values(*wanted)]
        if not page:
            break
        ids = [str(r["id"]) for r in page]
        if uid:
            hints = [str(r["organization_id"]) if r.get("organization_id") else None for r in page]
            allowed = await platform_access_many(uid, "file", ids, "viewer", organization_hints=hints)
            out.update({str(r["id"]): r for r in page if allowed.get(str(r["id"]))})
        else:
            out.update({str(r["id"]): r for r in page})
        if len(page) < page_size:
            break
        after = ids[-1]
    return out
