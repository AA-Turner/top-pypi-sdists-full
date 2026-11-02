"""``/files/sync/mappings`` — the rows a device's folder mappings live in.

SPEC-SERVER §6.3, ruling C4. Two writers, split by what they OWN:

* the **browser / desktop UI** writes the user's INTENT -- ``desired_state``,
  ``direction``, ``knobs`` -- direct-to-Supabase under RLS, because that is the
  canonical transport for pure UI↔DB;
* the **daemon** writes its OBSERVATION -- ``state`` and the counters -- through
  ``PATCH /files/sync/mappings/{id}`` under ``If-Match: W/"v<version>"``.

The race that split kills: the user taps Pause (``desired_state='paused'``), the
daemon's next heartbeat writes ``state='syncing'`` -- and the pause survives,
because they are different columns. The UI shows ``state`` and marks it
"pausing…" while the two disagree. A control that lies is the failure mode this
removes, and a database trigger enforces the split rather than a comment.

Creation goes through this router (never direct INSERT from the app) so D20's
admission rules can run. ``organization_id`` is carried EXPLICITLY on the create
body: the database never chooses, inherits, copies or defaults an organization.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from pydantic import BaseModel, Field

from .errors import map_exception

#: `state` is the daemon's; `desired_state` is the user's. Enforced in the DB too.
DAEMON_OWNED_COLUMNS = (
    "state",
    "state_reason",
    "state_changed_at",
    "last_seen_at",
    "last_synced_at",
    "items_total",
    "bytes_total",
)

_ENTRY_FIELDS = (
    "id",
    "created_by",
    "device_id",
    "folder_id",
    "organization_id",
    "local_path",
    "local_path_display",
    "direction",
    "desired_state",
    "state",
    "state_reason",
    "state_changed_at",
    "last_seen_at",
    "last_synced_at",
    "items_total",
    "bytes_total",
    "knobs",
    "version",
    "created_at",
    "updated_at",
    "deleted_at",
)


class SyncMappingEntry(BaseModel):
    id: str
    created_by: str
    device_id: str
    folder_id: str | None = None
    organization_id: str
    local_path: str
    local_path_display: str | None = None
    direction: str
    desired_state: str
    state: str
    state_reason: str | None = None
    state_changed_at: str | None = None
    last_seen_at: str | None = None
    last_synced_at: str | None = None
    items_total: int | None = None
    bytes_total: int | None = None
    knobs: dict[str, Any] = Field(default_factory=dict)
    version: int
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None


class CreateSyncMappingBody(BaseModel):
    #: EXPLICIT. There is no default and no inheritance: a mapping's
    #: organization is chosen at creation (D5) and carried on every write it
    #: performs (no-db-assigned-org).
    organization_id: str
    device_id: str
    local_path: str
    folder_id: str | None = None
    local_path_display: str | None = None
    direction: Literal["two_way", "upload_only", "download_only"] = "two_way"
    knobs: dict[str, Any] = Field(default_factory=dict)


class DaemonObservationBody(BaseModel):
    """The daemon's observation columns. Nothing here is the user's intent."""

    state: str | None = None
    state_reason: str | None = None
    state_changed_at: str | None = None
    last_seen_at: str | None = None
    last_synced_at: str | None = None
    items_total: int | None = None
    bytes_total: int | None = None


def _iso(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)


def _entry(row: dict[str, Any]) -> SyncMappingEntry:
    return SyncMappingEntry(
        id=str(row["id"]),
        created_by=str(row["created_by"]),
        device_id=str(row["device_id"]),
        folder_id=str(row["folder_id"]) if row.get("folder_id") else None,
        organization_id=str(row["organization_id"]),
        local_path=row["local_path"],
        local_path_display=row.get("local_path_display"),
        direction=row["direction"],
        desired_state=row["desired_state"],
        state=row["state"],
        state_reason=row.get("state_reason"),
        state_changed_at=_iso(row.get("state_changed_at")),
        last_seen_at=_iso(row.get("last_seen_at")),
        last_synced_at=_iso(row.get("last_synced_at")),
        items_total=row.get("items_total"),
        bytes_total=row.get("bytes_total"),
        knobs=row.get("knobs") or {},
        version=row["version"],
        created_at=_iso(row.get("created_at")),
        updated_at=_iso(row.get("updated_at")),
        deleted_at=_iso(row.get("deleted_at")),
    )


def _parse_weak_version(raw: str | None) -> int:
    """``If-Match: W/"v7"`` -> 7. Required on every daemon write.

    Without it two daemons (or one daemon and its own retry) overwrite each
    other's status and the browser shows whichever landed last.
    """
    if raw is None or not raw.strip():
        raise HTTPException(
            428,
            {
                "error": "precondition_required",
                "message": (
                    'PATCH /files/sync/mappings/{id} requires If-Match: W/"v<version>" '
                    "naming the row version this report was computed from."
                ),
            },
        )
    value = raw.strip()
    if value.startswith('W/"v') and value.endswith('"'):
        try:
            return int(value[4:-1])
        except ValueError:
            pass
    raise HTTPException(
        400,
        {
            "error": "invalid_if_match",
            "message": f'If-Match must be W/"v<version>"; got {raw!r}.',
        },
    )


def _uuid_or_400(value: str, field: str) -> str:
    try:
        return str(UUID(value))
    except ValueError as exc:
        raise HTTPException(
            400, {"error": "invalid_uuid", "message": f"{field} must be a uuid; got {value!r}."}
        ) from exc


def build_sync_mappings_router(
    *,
    user_id_dep: Any = None,
    prefix: str = "/files",
    tags: list[str] | None = None,
) -> APIRouter:
    """Build the ``/files/sync/mappings`` router.

    ``user_id_dep`` MUST be a FastAPI dependency returning the authenticated
    user id. Without one the router serves an anonymous user — fine for tests,
    dangerous in production, same posture as ``build_file_router``.
    """
    router = APIRouter(prefix=prefix, tags=tags or ["files", "sync"])

    if user_id_dep is None:

        def user_id_dep() -> str:  # noqa: E306
            return "anonymous"

    def _model():
        from matrx_files.db import ensure_bound  # noqa: F401 — pool must be registered
        from matrx_files.db.models_files import SyncMappings

        return SyncMappings

    @router.get("/sync/mappings", response_model=list[SyncMappingEntry])
    async def list_mappings(
        device_id: str | None = Query(None),
        user_id: str = Depends(user_id_dep),
    ) -> list[SyncMappingEntry]:
        try:
            flt: dict[str, Any] = {"created_by": user_id, "deleted_at__isnull": True}
            if device_id:
                flt["device_id"] = _uuid_or_400(device_id, "device_id")
            rows = await _model().filter(**flt).order_by("local_path").values(*_ENTRY_FIELDS)
        except Exception as e:
            raise map_exception(e, operation="sync mapping listing")
        return [_entry(dict(r)) for r in rows]

    @router.post("/sync/mappings", response_model=SyncMappingEntry, status_code=201)
    async def create_mapping(
        body: CreateSyncMappingBody,
        user_id: str = Depends(user_id_dep),
    ) -> SyncMappingEntry:
        try:
            created = await _model().create(
                # The owner is this caller, never a value the body could name.
                created_by=user_id,
                organization_id=_uuid_or_400(body.organization_id, "organization_id"),
                device_id=_uuid_or_400(body.device_id, "device_id"),
                folder_id=(
                    _uuid_or_400(body.folder_id, "folder_id") if body.folder_id else None
                ),
                local_path=body.local_path,
                local_path_display=body.local_path_display,
                direction=body.direction,
                knobs=body.knobs,
            )
        except Exception as e:
            raise map_exception(e, operation="sync mapping creation")
        row = await _model().filter(id=created.id).values(*_ENTRY_FIELDS)
        return _entry(dict(row[0]))

    @router.patch("/sync/mappings/{mapping_id}", response_model=SyncMappingEntry)
    async def report_observation(
        mapping_id: str,
        body: DaemonObservationBody,
        if_match: str | None = Header(default=None, alias="If-Match"),
        user_id: str = Depends(user_id_dep),
    ) -> SyncMappingEntry:
        expected_version = _parse_weak_version(if_match)
        mapping_id = _uuid_or_400(mapping_id, "mapping_id")
        try:
            rows = await _model().filter(id=mapping_id, created_by=user_id).values(*_ENTRY_FIELDS)
            if not rows:
                raise HTTPException(
                    404,
                    {"error": "not_found", "message": f"No sync mapping {mapping_id}."},
                )
            current = dict(rows[0])
            if int(current["version"]) != expected_version:
                # 412 carrying the CURRENT row: the daemon re-reads intent
                # (desired_state) before retrying, instead of clobbering a Pause
                # the user set while this report was in flight.
                raise HTTPException(412, _entry(current).model_dump())

            changes = {
                k: v for k, v in body.model_dump(exclude_unset=True).items() if k in DAEMON_OWNED_COLUMNS
            }
            if not changes:
                return _entry(current)
            changes.setdefault("state_changed_at", datetime.now(UTC))
            await _model().filter(id=mapping_id).update(**changes)
            rows = await _model().filter(id=mapping_id).values(*_ENTRY_FIELDS)
        except HTTPException:
            raise
        except Exception as e:
            raise map_exception(e, operation="sync mapping observation")
        return _entry(dict(rows[0]))

    @router.delete("/sync/mappings/{mapping_id}", status_code=204)
    async def delete_mapping(
        mapping_id: str,
        user_id: str = Depends(user_id_dep),
    ) -> None:
        mapping_id = _uuid_or_400(mapping_id, "mapping_id")
        try:
            rows = await _model().filter(id=mapping_id, created_by=user_id).values("id")
            if not rows:
                raise HTTPException(
                    404,
                    {"error": "not_found", "message": f"No sync mapping {mapping_id}."},
                )
            # Soft delete. The user's own removal goes through
            # desired_state='removed' first, so the daemon can unwind the mapping
            # on disk before the row disappears from under it.
            await _model().filter(id=mapping_id).update(deleted_at=datetime.now(UTC))
        except HTTPException:
            raise
        except Exception as e:
            raise map_exception(e, operation="sync mapping deletion")

    return router


__all__ = [
    "DAEMON_OWNED_COLUMNS",
    "CreateSyncMappingBody",
    "DaemonObservationBody",
    "SyncMappingEntry",
    "build_sync_mappings_router",
]
