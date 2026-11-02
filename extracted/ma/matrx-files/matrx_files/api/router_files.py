"""Canonical files router — CRUD + URLs.

Exposes the most-used file endpoints:

    POST   /files/upload
    GET    /files/sync/changes   (device-replica change feed, keyset cursor)
    GET    /files/sync/folders   (device-replica folder tree)
    GET    /files/{file_id}
    GET    /files/{file_id}/url
    PATCH  /files/{file_id}
    DELETE /files/{file_id}
    POST   /files/{file_id}/restore

A host that needs more (folder CRUD, share-link CRUD, group ACL, search,
trash, presigned uploads, TUS) wires their own routers calling the
same ``FileService`` methods. This factory covers the standalone-test
surface: a new host can mount this and have a working file system.
"""

from __future__ import annotations

import base64
import json
from collections.abc import Callable, Iterator
from datetime import UTC, datetime
from typing import Any, Literal
from urllib.parse import quote as _url_quote

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    Header,
    HTTPException,
    Query,
    Request,
    UploadFile,
    status,
)
from fastapi.responses import Response, StreamingResponse
from pydantic import BaseModel, ConfigDict, Field

from ..derivations import ClientPolicyMetadataError, assert_no_client_policy_metadata
from ..file_session_mint import FileSessionSourceResolver, mint_file_session_response
from ..service import FileService
from ..path_safety import sanitize_logical_path
from ..request_organization import admitted_organization_id
from ..system_origins import relocate_under_system_origin
from ..asset_envelope import AssetCombinedOpResponse
from matrx_utils.row_access import (
    LegacyLevelInput,
    RowAccess,
    ShownToLiteral,
    legacy_level_echo,
    reconcile_row_access,
    stated_row_access,
)
from ..media_sniff import SNIFF_HEAD_BYTES, sniff_mime_type
from ..audio_extract import AudioExtractionRequest, AudioExtractionResult
from ..cloud_sync.device_writes import resolve_write_origin
from ..cloud_sync.idempotency import IdempotencyStore
from ..cloud_sync.preconditions import (
    PreconditionFailed,
    check_expected_checksum,
    check_if_match,
    normalize_expected_checksum,
    parse_if_match,
)
from .errors import map_exception
from .read_by_access import file_read_decided_by_access
from ..office_pdf import OfficePdfRequest, OfficePdfResult
from ..pdf_pages import PdfPageSelectionRequest, PdfPageSelectionResult
from .records import FileRecord, to_file_record_with_urls_async


class _UploadResponse(BaseModel):
    file_id: str
    file_path: str
    size_bytes: int | None = None
    checksum: str | None = None
    url: str | None = None
    cdn_url: str | None = None
    download_url: str | None = None
    published_to_web: bool = False
    shown_to: str | None = None
    visibility: str | None = None  # T-13 transitional wire echo (derived from the two words)
    share_token: str | None = None
    share_url: str | None = None


class _ShareLinkRecord(BaseModel):
    """A single share-link row (canonical platform.share_links). Shape matches
    aidream's ShareLinkRecord so the contract is byte-identical across host +
    service."""

    model_config = ConfigDict(extra="allow")

    token: str | None = None
    resource_id: str | None = None
    resource_type: str | None = None
    permission_level: str | None = None
    created_by: str | None = None
    expires_at: str | None = None
    max_uses: int | None = None
    use_count: int | None = None


class _CreateShareLinkRequest(BaseModel):
    # CONVERGE: the access levels are `viewer` · `commenter` · `editor` · `admin`, and `admin` is
    # the top level on a thing — one vocabulary everywhere — declared 2026-09-10, AI Matrx Data
    # Doctrine R18/R19 (recorded in common-docs/systems/platform/access/DECISIONS.md, 2026-09-10).
    # Observed here: this request narrows share-LINK levels to `viewer` | `editor`. The canonical
    # RPC `public.create_share_link` accepts `viewer, editor, admin` and
    # `platform.share_links.permission_level` is the full `permission_level` enum [live
    # brsgrqvjdzwihsvnfqkf, 2026-09-10] — so this is a CAP, not a vocabulary. Whether a share LINK
    # may ever carry `admin` (delete / transfer to anyone holding the URL) is undecided and is NOT
    # widened here. Reconcile when you next change this for another reason. Do NOT escalate.
    # Register: /projects/data-doctrine-adoption/REGISTER.md#DD-050
    permission_level: Literal["viewer", "editor"] = "viewer"
    expires_at: str | None = None
    max_uses: int | None = None


class _SyncFileEntry(BaseModel):
    """One row of the device-replica change feed (files.files, safe fields).

    ``deleted_at`` set ⇒ tombstone: the device removes its local copy and
    keeps the tombstone in its index until acknowledged.
    """

    file_id: str
    file_path: str
    file_name: str
    mime_type: str | None = None
    size_bytes: int | None = None
    checksum: str | None = None
    published_to_web: bool = False
    shown_to: str | None = None
    visibility: str | None = None  # T-13 transitional wire echo
    version: int = 1
    folder_id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None
    # --- feed v2 (SPEC-SERVER §2.3); nothing above was removed ---
    #: public.app_instances.id of the device that wrote this row, or None for a
    #: browser upload. The daemon treats None as "not mine" and applies the change.
    origin_device_id: str | None = None
    #: The local filesystem mtime the writing client observed, RFC3339 UTC.
    #: Presentation and download_only restore only -- never an ordering key.
    client_modified_at: str | None = None
    #: REQUIRED. The row's organization, so the engine can stamp its own writes
    #: explicitly instead of letting the database choose one.
    organization_id: str


class _SyncChangesResponse(BaseModel):
    files: list[_SyncFileEntry]
    next_cursor: str | None = None
    has_more: bool = False
    server_time: str


class _SyncFolderEntry(BaseModel):
    folder_id: str
    folder_path: str
    folder_name: str
    parent_id: str | None = None
    published_to_web: bool = False
    shown_to: str | None = None
    visibility: str | None = None  # T-13 transitional wire echo
    is_system: bool = False
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None


class _SyncFoldersResponse(BaseModel):
    folders: list[_SyncFolderEntry]
    # The folder feed adopts the file feed's cursor contract verbatim
    # (SPEC-SERVER §2.4): every response carries a cursor the client stores and
    # passes back forever, and `has_more` says whether the page filled.
    next_cursor: str
    has_more: bool = False
    # Kept, and now ALWAYS false: a cursor means the listing can never be
    # silently short. It is removed only once every client stops reading it
    # (matrx-local's old engine still does).
    truncated: bool = False
    server_time: str


def _replay_upload_response(cached: dict) -> _UploadResponse:
    """Return the STORED response for an idempotent replay (SPEC-SERVER §3.3).

    A replay with the same key and the same precondition returns the original
    response verbatim, even if the row has since moved on -- it never re-uploads
    and never re-evaluates the precondition. A stored 412 is replayed AS a 412:
    a losing write must lose identically, or a retry loop silently becomes a
    last-write-wins overwrite.
    """
    body = cached.get("response_body") or {}
    if int(cached.get("status_code") or 200) == 412:
        raise PreconditionFailed(body)
    return _UploadResponse(**body)


def _encode_sync_cursor(ts: datetime, row_id: str, include_deleted: bool) -> str:
    payload = json.dumps(
        {"v": 1, "ts": ts.isoformat(), "id": row_id, "d": bool(include_deleted)},
        separators=(",", ":"),
    )
    return base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")


def _decode_sync_cursor(cursor: str) -> tuple[datetime, str, bool]:
    """Decode an opaque sync cursor. Raises ValueError (→ 400) on garbage."""
    try:
        padded = cursor + "=" * (-len(cursor) % 4)
        data = json.loads(base64.urlsafe_b64decode(padded.encode()).decode())
        if not isinstance(data, dict):
            raise ValueError("cursor payload is not an object")
        if data.get("v") != 1:
            raise ValueError(f"unknown cursor version {data.get('v')!r}")
        return (
            datetime.fromisoformat(data["ts"]),
            str(data["id"]),
            bool(data.get("d")),
        )
    except (ValueError, KeyError, TypeError, AttributeError, json.JSONDecodeError) as e:
        raise ValueError(f"malformed sync cursor: {e}") from e


def _iso_or_none(value: Any) -> str | None:
    if value is None:
        return None
    return value.isoformat() if isinstance(value, datetime) else str(value)


class _PatchBody(BaseModel):
    """Union mutation body for PATCH /files/{id}.

    Every field is optional. Sub-operations run sequentially with best-
    effort atomicity; failures accumulate in ``errors[]`` on the
    response envelope rather than rolling everything back.
    """

    # Direct field updates
    name: str | None = None
    folder: str | None = None
    published_to_web: bool | None = None
    shown_to: ShownToLiteral | None = None
    visibility: LegacyLevelInput | None = None  # T-13 transitional wire input
    metadata: dict[str, Any] | None = None
    # Bundled sub-ops
    share: dict[str, Any] | None = None
    share_revoke: bool = False
    permissions: list[dict[str, Any]] | None = None
    permissions_revoke: list[dict[str, Any]] | None = None
    variants: list[str] | list[dict[str, Any]] | None = None
    # Version + trash management
    restore_version: int | None = None
    restore_from_trash: bool = False
    # Copy out
    copy_to: str | None = None


class _BulkBody(BaseModel):
    """Bulk discriminator: ``{ids[], op, args}``."""

    ids: list[str] = Field(..., min_length=1, max_length=500)
    op: Literal["move", "delete", "restore", "publish", "shown_to", "visibility", "share"]
    args: dict[str, Any] | None = None


def _map_exc(exc: Exception, operation: str = "file operation") -> HTTPException:
    """Delegate to the ONE mapper — it logs the traceback and names the cause."""
    return map_exception(exc, operation=operation)


# Range-header support for /download endpoint (RFC 7233).
_RANGE_CHUNK_BYTES = 256 * 1024  # 256 KiB — keeps the byte cache happy.


def _parse_range_header(header: str | None, total_size: int) -> tuple[int, int] | None:
    """Parse ``Range: bytes=<start>-<end>``.

    Returns (start, end) inclusive offsets, ``None`` when absent or malformed,
    or the sentinel ``(-1, -1)`` when the request is unsatisfiable so the
    caller can return 416.
    """
    if not header or total_size <= 0:
        return None
    if not header.strip().lower().startswith("bytes="):
        return None
    spec = header.strip()[6:].split(",", 1)[0].strip()
    if "-" not in spec:
        return None
    start_s, end_s = spec.split("-", 1)
    start_s, end_s = start_s.strip(), end_s.strip()
    last = total_size - 1
    try:
        if not start_s:
            n = int(end_s)
            if n <= 0:
                return None
            start, end = max(0, total_size - n), last
        else:
            start = int(start_s)
            end = int(end_s) if end_s else last
    except ValueError:
        return None
    if start > last:
        return (-1, -1)
    if end > last:
        end = last
    if end < start:
        return None
    return (start, end)


def _content_disposition(file_name: str, *, attachment: bool) -> str:
    disp = "attachment" if attachment else "inline"
    try:
        file_name.encode("ascii")
        return f'{disp}; filename="{file_name}"'
    except UnicodeEncodeError:
        ascii_fallback = file_name.encode("ascii", "replace").decode("ascii")
        return f"{disp}; filename=\"{ascii_fallback}\"; filename*=UTF-8''{_url_quote(file_name)}"


def build_file_router(
    file_service: FileService,
    *,
    user_id_dep: Callable[..., str] | None = None,
    prefix: str = "/files",
    tags: list[str] | None = None,
    file_session_source_resolver: FileSessionSourceResolver | None = None,
    require_file_session_source: bool = False,
) -> APIRouter:
    """Build a FastAPI router exposing the core file endpoints.

    ``user_id_dep`` MUST be a FastAPI dependency that returns the
    authenticated user_id (a string). Hosts wire this to their JWT
    validation / guest fingerprint resolver. Without a real
    ``user_id_dep`` the router will accept all requests with an
    anonymous user_id — fine for tests, dangerous in production.
    """
    router = APIRouter(prefix=prefix, tags=tags or ["files"])

    if user_id_dep is None:
        # Test-mode default: every request is the same anonymous user.
        def _anonymous_user_id() -> str:
            return "anonymous"

        user_id_dep = _anonymous_user_id

    # ------------------------------------------------------------------
    # POST /session — mint the browser file-session cookie.
    #
    # The auth lane behind durable private render URLs: an authenticated
    # client (Bearer / fingerprint, credentials:'include') calls this once
    # at bootstrap (and again on a 401'd render); the HttpOnly SameSite=None
    # cookie then rides every <img>/<video> request to
    # GET /files/{id}/download. The middleware accepts it ONLY on GET
    # byte-serving routes — see matrx-connect middleware/session_cookie.py.
    # ------------------------------------------------------------------
    @router.post("/session")
    async def mint_file_session(request: Request, user_id: str = Depends(user_id_dep)) -> Response:
        return await mint_file_session_response(
            user_id,
            context=getattr(request.state, "context", None),
            source_resolver=file_session_source_resolver,
            require_source=require_file_session_source,
        )

    # ------------------------------------------------------------------
    # POST /upload — buffered multipart write.
    # ------------------------------------------------------------------
    @router.post("/upload", response_model=_UploadResponse)
    async def upload_file(
        request: Request,
        file: UploadFile = File(...),
        file_path: str = Form(...),
        published_to_web: bool | None = Form(None),
        shown_to: ShownToLiteral | None = Form(None),
        visibility: LegacyLevelInput | None = Form(None),  # T-13 transitional wire input
        metadata_json: str | None = Form(None),
        intent: Literal["create", "alias_existing", "force_new_copy"] | None = Form(None),
        reason: str | None = Form(None),
        # SPEC-SERVER §3.1. The SHA-256 the client believes the server currently
        # holds at this file_path, or the literal "absent" meaning "I believe no
        # alive row exists here". Omitted = today's last-write-wins, unchanged,
        # so no existing caller breaks (S8: optional on the wire, mandatory in
        # the sync engine, enforced by the engine's own test).
        expected_checksum: str | None = Form(None),
        # Device provenance (SPEC-SERVER §2.2). Headers, not form fields: TUS has
        # no body at all and PATCH has a JSON one, so a header is the ONE spelling
        # that works on every write route -- and it matches the existing
        # X-Request-Id / X-Idempotency-Key convention on this route.
        x_matrx_device_id: str | None = Header(default=None, alias="X-Matrx-Device-Id"),
        x_matrx_client_modified_at: str | None = Header(
            default=None, alias="X-Matrx-Client-Modified-At"
        ),
        x_request_id: str | None = Header(default=None, alias="X-Request-Id"),
        x_idempotency_key: str | None = Header(default=None, alias="X-Idempotency-Key"),
        user_id: str = Depends(user_id_dep),
    ) -> _UploadResponse:
        # ---- the ONE organization resolution for this request ------------
        # Resolved HERE, at the edge, from the request the auth boundary
        # admitted — not deep in the write path from an ambient seam the host
        # may not have wired, and not from a metadata dict an intermediate
        # layer may not have filled. Both were true on 2026-09-19 and every
        # upload to files.matrxserver.com returned 400 "carries no
        # organization" while the browser's verified X-Organization-Id sat
        # unread one layer away. See matrx_files/request_organization.py.
        request_organization_id = admitted_organization_id()
        try:
            # FastAPI 0.152 supplies False for an omitted optional multipart
            # bool. The raw form distinguishes that omission from an explicit
            # false, so legacy visibility applies only when neither new access
            # field was submitted.
            form = await request.form()
            effective_published_to_web = (
                published_to_web if "published_to_web" in form else None
            )
            content = await file.read()
            sniffed_mime = sniff_mime_type(
                claimed=file.content_type,
                head_bytes=content[:SNIFF_HEAD_BYTES],
                filename=file.filename,
            )
            parsed_meta: dict[str, Any] = {}
            if metadata_json:
                try:
                    parsed_meta = json.loads(metadata_json)
                except (json.JSONDecodeError, ValueError) as e:
                    raise HTTPException(400, {"error": "invalid_metadata", "message": str(e)})
                if not isinstance(parsed_meta, dict):
                    # A JSON scalar/array parses fine and then explodes deep in
                    # the write path as a TypeError → 500. It is a client input
                    # error; say so at the edge.
                    raise HTTPException(
                        400,
                        {
                            "error": "invalid_metadata",
                            "message": (
                                "metadata_json must be a JSON object, got "
                                f"{type(parsed_meta).__name__}"
                            ),
                        },
                    )
                try:
                    # Policy keys are server-stamped authorization inputs —
                    # never accepted from an upload client.
                    assert_no_client_policy_metadata(
                        parsed_meta, context="buffered upload metadata"
                    )
                except ClientPolicyMetadataError as e:
                    raise HTTPException(403, {"error": "reserved_metadata_key", "message": str(e)})
            # Stamp request_id into metadata so the realtime row carries it
            # and the FE can deterministically dedup its own writes.
            if x_request_id:
                parsed_meta["request_id"] = x_request_id
            if x_idempotency_key:
                parsed_meta["_idempotency_key"] = x_idempotency_key
            clean_path = sanitize_logical_path(file_path)
            access = reconcile_row_access(
                published_to_web=effective_published_to_web,
                shown_to=shown_to,
                legacy_level=visibility,
                default=RowAccess(shown_to="only_me"),
                boundary="POST /files/upload",
            )
            clean_path = relocate_under_system_origin(
                clean_path,
                parsed_meta.get("origin") if isinstance(parsed_meta.get("origin"), str) else None,
            )
            # Validated BEFORE any bytes are written: a device id naming another
            # user's machine is refused, never stored, because that machine would
            # then skip a change it never made.
            origin = await resolve_write_origin(
                user_id=user_id,
                device_id=x_matrx_device_id,
                client_modified_at=x_matrx_client_modified_at,
            )
            # ---- write precondition (SPEC-SERVER §3) --------------------------
            # Two devices editing one file both used to win, in arrival order,
            # and the loser's bytes were simply gone. Evaluated against the row
            # that exists at this path RIGHT NOW; a mismatch is 412 carrying the
            # engine's whole conflict input, never a silent overwrite.
            expected = normalize_expected_checksum(expected_checksum)
            idempotency_fingerprint = {
                "file_path": clean_path,
                "expected_checksum": expected,
                "intent": intent,
                # The fingerprint follows the normalized write intent, not the
                # particular legacy/new spelling. A retry must never replay a
                # personal write as an Anyone link (or vice versa).
                "access": {
                    "published_to_web": access.published_to_web,
                    "shown_to": access.shown_to,
                    "wants_anyone_link": access.wants_anyone_link,
                },
            }
            store = (
                IdempotencyStore(file_service.file_manager) if x_idempotency_key else None
            )
            if store is not None:
                # §3.3: same key + same precondition returns the STORED response
                # (200/201 or a stored 412) even if the row has since moved on;
                # same key + a DIFFERENT precondition is a client bug and raises
                # IdempotencyConflict -> 409 idempotency_key_reuse. It never
                # re-uploads and never silently accepts a second request.
                cached = await store.lookup(
                    owner_id=user_id,
                    key=x_idempotency_key,
                    endpoint="POST /files/upload",
                    body=idempotency_fingerprint,
                )
                if cached is not None:
                    return _replay_upload_response(cached)
            if expected is not None:
                current = await file_service.file_manager.sync_engine.db.get_file_by_path_async(
                    user_id, clean_path
                )
                try:
                    check_expected_checksum(current, expected)
                except PreconditionFailed as conflict:
                    if store is not None:
                        # A losing write must lose IDENTICALLY on retry.
                        await store.persist(
                            owner_id=user_id,
                            key=x_idempotency_key,
                            endpoint="POST /files/upload",
                            body=idempotency_fingerprint,
                            status_code=412,
                            response_body=conflict.payload,
                        )
                    raise
            # The standalone buffered route is an upload orchestration path,
            # not a raw storage primitive. ``upload_simple`` performs the
            # canonical managed write and schedules universal media processing
            # (thumbnail/preview variants + intrinsic metadata). Calling
            # ``write`` here created healthy masters with no preview assets.
            if intent is not None:
                intent_result = await file_service.upload_with_intent(
                    content,
                    intent=intent,
                    reason=reason,
                    file_path=clean_path,
                    mime_type=sniffed_mime,
                    published_to_web=access.published_to_web,
                    shown_to=access.shown_to,
                    owner_id=user_id,
                    organization_id=request_organization_id,
                    metadata=parsed_meta or None,
                )
                result = intent_result.get("result")
                if result is None:
                    # The buffered upload door is a byte-write operation. An
                    # explicit alias-existing request legitimately writes no
                    # bytes, but it still needs the canonical row's wire
                    # metadata. Keep that behavior out of this response shape
                    # until a caller needs it; Q1's deliberate copy always
                    # produces a managed-write result.
                    raise RuntimeError(
                        f"buffered upload intent {intent!r} produced no managed write"
                    )
                response_path = str(intent_result.get("file_path") or clean_path)
            else:
                # Preserve the legacy/default upload behavior exactly. Strict
                # dedup semantics are opt-in so every existing upload caller
                # remains byte-for-byte compatible.
                result = await file_service.upload_simple(
                    content,
                    file_path=clean_path,
                    mime_type=sniffed_mime,
                    published_to_web=access.published_to_web,
                    shown_to=access.shown_to,
                    user_id=user_id,
                    organization_id=request_organization_id,
                    metadata=parsed_meta or None,
                    origin_device_id=origin.device_id,
                    client_modified_at=origin.client_modified_at,
                )
                response_path = clean_path
            share_token = getattr(result, "share_token", None)
            share_url = getattr(result, "share_url", None)
            if access.wants_anyone_link:
                share_link = await file_service.permissions.create_share_link_async(
                    "file", result.file_id, permission_level="viewer", user_id=user_id
                )
                share_token = str(share_link["token"])
                share_url = str(share_link.get("url") or f"/share/{share_token}")
            # Third-party hosts may still supply the old minimal SyncResult
            # shape while moving to the two row-access words. The request's
            # already-reconciled access is the safe fallback; never read the
            # retired result.visibility field.
            result_published_to_web = getattr(result, "published_to_web", access.published_to_web)
            result_shown_to = getattr(result, "shown_to", access.shown_to)
            result_visibility = legacy_level_echo(
                {"published_to_web": result_published_to_web, "shown_to": result_shown_to}
            )
            if store is not None:
                await store.persist(
                    owner_id=user_id,
                    key=x_idempotency_key,
                    endpoint="POST /files/upload",
                    body=idempotency_fingerprint,
                    status_code=200,
                    response_body={
                        "file_id": result.file_id,
                        "file_path": response_path,
                        "size_bytes": result.size_bytes,
                        "checksum": result.checksum,
                        "url": result.url,
                        "cdn_url": result.cdn_url,
                        "download_url": result.download_url,
                        "published_to_web": result_published_to_web,
                        "shown_to": result_shown_to,
                        "visibility": result_visibility,
                        "share_token": share_token,
                        "share_url": share_url,
                    },
                    resource_id=result.file_id,
                    resource_type="file",
                )
            return _UploadResponse(
                file_id=result.file_id,
                file_path=response_path,
                size_bytes=result.size_bytes,
                checksum=result.checksum,
                url=result.url,
                cdn_url=result.cdn_url,
                download_url=result.download_url,
                published_to_web=result_published_to_web,
                shown_to=result_shown_to,
                visibility=result_visibility,
                share_token=share_token,
                share_url=share_url,
            )
        except Exception as e:
            raise _map_exc(e, "file upload")

    # ------------------------------------------------------------------
    # GET /sync/changes — keyset-paginated change feed for device replicas
    # (desktop file sync). Registered BEFORE /{file_id} so the literal
    # segment can never be captured as a file id.
    #
    # Protocol: first call with neither ``since`` nor ``cursor`` is the
    # bootstrap (alive rows only, from the beginning); every response
    # returns ``next_cursor`` — the client stores it and passes it back on
    # every subsequent call, forever. Once the bootstrap drains
    # (has_more=false) the returned cursor flips tombstone-aware, so
    # deletions ride the same feed from then on. ``since`` (ISO-8601) is
    # an alternative entry point for a client that kept a raw
    # ``updated_at`` watermark; it is tombstone-aware from the start.
    # ------------------------------------------------------------------
    @router.get("/sync/changes", response_model=_SyncChangesResponse)
    async def sync_changes(
        since: str | None = Query(
            None, description="ISO-8601 updated_at watermark (tombstone-aware)"
        ),
        cursor: str | None = Query(
            None, description="Opaque cursor from a previous response (wins over since)"
        ),
        limit: int = Query(500, ge=1, le=2000),
        include_system: bool = Query(
            False, description="Include system-managed paths (generations/, system-files/)"
        ),
        user_id: str = Depends(user_id_dep),
    ) -> _SyncChangesResponse:
        try:
            if cursor:
                cursor_ts, cursor_id, include_deleted = _decode_sync_cursor(cursor)
            elif since:
                cursor_ts = datetime.fromisoformat(since.replace("Z", "+00:00"))
                cursor_id, include_deleted = "", True
            else:
                cursor_ts, cursor_id, include_deleted = None, "", False

            engine = file_service.file_manager.sync_engine
            rows = await engine.list_sync_changes_async(
                cursor_ts=cursor_ts,
                cursor_id=cursor_id or None,
                include_deleted=include_deleted,
                include_system=include_system,
                limit=limit,
                user_id=user_id,
            )
        except Exception as e:
            raise _map_exc(e, "sync change feed")

        has_more = len(rows) == limit
        if rows:
            last = rows[-1]
            last_ts = last["updated_at"]
            if not isinstance(last_ts, datetime):
                last_ts = datetime.fromisoformat(str(last_ts))
            # Once a feed position exists, future polls must see tombstones —
            # the bootstrap-only alive filter applies just until it drains.
            next_d = include_deleted or not has_more
            next_cursor = _encode_sync_cursor(last_ts, str(last["id"]), next_d)
        elif cursor_ts is not None:
            # Empty page at a known position ⇒ the feed is drained here —
            # the returned cursor is always tombstone-aware from this point
            # (a bootstrap that ends on an empty page must still flip).
            next_cursor = _encode_sync_cursor(cursor_ts, cursor_id, True)
        else:
            # Empty bootstrap (user has no files yet): anchor at epoch,
            # tombstone-aware, so the same cursor protocol still applies.
            next_cursor = _encode_sync_cursor(datetime(1970, 1, 1, tzinfo=UTC), "", True)

        return _SyncChangesResponse(
            files=[
                _SyncFileEntry(
                    file_id=str(r["id"]),
                    file_path=r["file_path"],
                    file_name=r.get("file_name") or r["file_path"].rsplit("/", 1)[-1],
                    mime_type=r.get("mime_type"),
                    size_bytes=r.get("size_bytes"),
                    checksum=r.get("checksum"),
                    published_to_web=bool(r.get("published_to_web")),
                    shown_to=r.get("shown_to"),
                    visibility=legacy_level_echo(r),
                    version=r.get("current_version") or 1,
                    folder_id=str(r["parent_folder_id"]) if r.get("parent_folder_id") else None,
                    created_at=_iso_or_none(r.get("created_at")),
                    updated_at=_iso_or_none(r.get("updated_at")),
                    deleted_at=_iso_or_none(r.get("deleted_at")),
                    origin_device_id=(
                        str(r["origin_device_id"]) if r.get("origin_device_id") else None
                    ),
                    client_modified_at=_iso_or_none(r.get("client_modified_at")),
                    organization_id=str(r["organization_id"]),
                )
                for r in rows
            ],
            next_cursor=next_cursor,
            has_more=has_more,
            server_time=datetime.now(UTC).isoformat(),
        )

    # ------------------------------------------------------------------
    # GET /sync/folders — the folder half of a device replica's tree.
    # ------------------------------------------------------------------
    @router.get("/sync/folders", response_model=_SyncFoldersResponse)
    async def sync_folders(
        since: str | None = Query(
            None, description="ISO-8601 updated_at watermark (tombstone-aware)"
        ),
        cursor: str | None = Query(
            None, description="Opaque cursor from a previous response (wins over since)"
        ),
        limit: int = Query(500, ge=1, le=2000),
        include_deleted: bool = Query(False),
        include_system: bool = Query(False),
        user_id: str = Depends(user_id_dep),
    ) -> _SyncFoldersResponse:
        # Same protocol as /sync/changes, same codec, same flip: the first call
        # with neither `since` nor `cursor` is the bootstrap (alive rows only);
        # once it drains the returned cursor is tombstone-aware forever.
        try:
            if cursor:
                cursor_ts, cursor_id, include_deleted_cursor = _decode_sync_cursor(cursor)
                include_deleted = include_deleted or include_deleted_cursor
            elif since:
                cursor_ts = datetime.fromisoformat(since.replace("Z", "+00:00"))
                cursor_id, include_deleted = "", True
            else:
                cursor_ts, cursor_id = None, ""

            engine = file_service.file_manager.sync_engine
            rows = await engine.list_all_folders_async(
                cursor_ts=cursor_ts,
                cursor_id=cursor_id or None,
                include_deleted=include_deleted,
                include_system=include_system,
                limit=limit,
                user_id=user_id,
            )
        except Exception as e:
            raise _map_exc(e, "sync folder listing")

        has_more = len(rows) == limit
        if rows:
            last_ts = rows[-1]["updated_at"]
            if not isinstance(last_ts, datetime):
                last_ts = datetime.fromisoformat(str(last_ts))
            next_cursor = _encode_sync_cursor(
                last_ts, str(rows[-1]["id"]), include_deleted or not has_more
            )
        elif cursor_ts is not None:
            next_cursor = _encode_sync_cursor(cursor_ts, cursor_id, True)
        else:
            next_cursor = _encode_sync_cursor(datetime(1970, 1, 1, tzinfo=UTC), "", True)

        return _SyncFoldersResponse(
            folders=[
                _SyncFolderEntry(
                    folder_id=str(r["id"]),
                    folder_path=r["folder_path"],
                    folder_name=r.get("folder_name") or r["folder_path"].rsplit("/", 1)[-1],
                    parent_id=str(r["parent_id"]) if r.get("parent_id") else None,
                    published_to_web=bool(r.get("published_to_web")),
                    shown_to=r.get("shown_to"),
                    visibility=legacy_level_echo(r),
                    is_system=bool(r.get("is_system")),
                    created_at=_iso_or_none(r.get("created_at")),
                    updated_at=_iso_or_none(r.get("updated_at")),
                    deleted_at=_iso_or_none(r.get("deleted_at")),
                )
                for r in rows
            ],
            next_cursor=next_cursor,
            has_more=has_more,
            truncated=False,
            server_time=datetime.now(UTC).isoformat(),
        )

    # ------------------------------------------------------------------
    # GET /{file_id} — fetch a single record.
    # ------------------------------------------------------------------
    # A read decided by access (standalone/admission.py): admitted without an organization.
    @router.get(
        "/{file_id}",
        response_model=FileRecord,
        dependencies=[Depends(file_read_decided_by_access)],
    )
    async def get_file(
        file_id: str,
        user_id: str = Depends(user_id_dep),
    ) -> FileRecord:
        try:
            record = await file_service.read_record(file_id, user_id=user_id)
            return await to_file_record_with_urls_async(file_service.file_manager, record)
        except Exception as e:
            raise _map_exc(e, "file record read")

    # ------------------------------------------------------------------
    # POST /{file_id}/pdf-pages — one cached PDF from arbitrary source pages.
    # ------------------------------------------------------------------
    @router.post("/{file_id}/pdf-pages", response_model=PdfPageSelectionResult)
    async def select_pdf_pages(
        file_id: str,
        body: PdfPageSelectionRequest,
        user_id: str = Depends(user_id_dep),
    ) -> PdfPageSelectionResult:
        try:
            return await file_service.select_pdf_pages(
                file_id,
                user_id=user_id,
                request=body,
            )
        except Exception as e:
            raise _map_exc(e, "PDF page selection")

    # ------------------------------------------------------------------
    # POST /{file_id}/office-pdf — pdf_conversion derivative of an Office
    # file (LibreOffice). Idempotent per (parent, kind, source revision).
    # ------------------------------------------------------------------
    @router.post("/{file_id}/office-pdf", response_model=OfficePdfResult)
    async def convert_office_pdf(
        file_id: str,
        body: OfficePdfRequest | None = None,
        user_id: str = Depends(user_id_dep),
    ) -> OfficePdfResult:
        try:
            return await file_service.convert_office_pdf(
                file_id,
                user_id=user_id,
                request=body,
            )
        except Exception as e:
            raise _map_exc(e, "Office PDF conversion")

    # ------------------------------------------------------------------
    # POST /{file_id}/extract-audio — audio_extracted derivative of a video.
    # Idempotent per (parent, kind, source revision).
    # ------------------------------------------------------------------
    @router.post("/{file_id}/extract-audio", response_model=AudioExtractionResult)
    async def extract_audio(
        file_id: str,
        body: AudioExtractionRequest | None = None,
        user_id: str = Depends(user_id_dep),
    ) -> AudioExtractionResult:
        try:
            return await file_service.extract_audio(
                file_id,
                user_id=user_id,
                request=body,
            )
        except Exception as e:
            raise _map_exc(e, "audio extraction")

    # ------------------------------------------------------------------
    # GET /{file_id}/download — bytes stream with ETag + Range + Length.
    #
    # Honors RFC 7233 Range requests so the FE byte cache + Service
    # Worker can stream large PDFs / videos chunk-by-chunk and resume
    # mid-flight. ETag is the SHA-256 checksum from the cld_files row;
    # the FE keys its IndexedDB cache on this so the cache survives
    # version bumps without unnecessary re-downloads.
    # ------------------------------------------------------------------
    @router.get("/{file_id}/download", dependencies=[Depends(file_read_decided_by_access)])
    async def download_file(
        file_id: str,
        request: Request,
        inline: bool = Query(
            False, description="Set Content-Disposition: inline (render in browser)"
        ),
        user_id: str = Depends(user_id_dep),
    ):
        try:
            record = await file_service.read_record(file_id, user_id=user_id)
        except Exception as e:
            raise _map_exc(e, "file download")

        file_name = record.get("file_name") or record["file_path"].rsplit("/", 1)[-1]
        media_type = record.get("mime_type") or "application/octet-stream"
        checksum = record.get("checksum") or ""
        total_size = int(record.get("size_bytes") or 0)

        # If we don't know the total size yet (legacy rows), HEAD S3.
        storage_uri = record.get("canonical_storage_uri") or record["storage_uri"]
        s3 = None
        backend_router = file_service.router
        if hasattr(backend_router, "is_configured") and backend_router.is_configured("s3"):
            s3 = backend_router.s3
        if total_size <= 0 and s3 is not None:
            try:
                uri_path = storage_uri.split("://", 1)[1]
                bucket, key = s3._parse_path(uri_path)
                head = await s3.get_metadata_async(uri_path)
                total_size = int(head.get("size") or 0)
            except Exception:
                pass

        base_headers = {
            "Accept-Ranges": "bytes",
            "X-Content-Type-Options": "nosniff",
            "ETag": f'"{checksum}"',
            "Content-Disposition": _content_disposition(file_name, attachment=not inline),
        }

        # Range path (RFC 7233). Only S3-backed reads support streaming —
        # other backends fall back to buffered.
        range_header = request.headers.get("range") or request.headers.get("Range")
        parsed = _parse_range_header(range_header, total_size) if total_size > 0 else None

        if parsed == (-1, -1):
            return Response(
                status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
                headers={**base_headers, "Content-Range": f"bytes */{total_size}"},
            )

        # S3 streaming path (range-aware).
        if s3 is not None and total_size > 0:
            try:
                uri_path = storage_uri.split("://", 1)[1]
                bucket, key = s3._parse_path(uri_path)
            except Exception as e:
                raise _map_exc(e, "file download")
            client = s3._get_client()
            get_kw: dict[str, Any] = {"Bucket": bucket, "Key": key}
            is_range = parsed is not None
            if is_range:
                start, end = parsed  # type: ignore[misc]
                get_kw["Range"] = f"bytes={start}-{end}"
            try:
                s3_resp = client.get_object(**get_kw)
            except Exception as e:
                raise _map_exc(e, "file download")
            body = s3_resp.get("Body")
            if body is None:
                raise HTTPException(502, {"error": "s3_error", "message": "S3 returned no body"})

            if is_range:
                start, end = parsed  # type: ignore[misc]
                length = end - start + 1
                headers = {
                    **base_headers,
                    "Content-Range": f"bytes {start}-{end}/{total_size}",
                    "Content-Length": str(length),
                }
                status_code = status.HTTP_206_PARTIAL_CONTENT
            else:
                headers = {**base_headers, "Content-Length": str(total_size)}
                status_code = status.HTTP_200_OK

            def _iter_chunks() -> Iterator[bytes]:
                try:
                    for chunk in body.iter_chunks(chunk_size=_RANGE_CHUNK_BYTES):
                        if chunk:
                            yield chunk
                finally:
                    try:
                        body.close()
                    except Exception:
                        pass

            return StreamingResponse(
                _iter_chunks(),
                status_code=status_code,
                media_type=media_type,
                headers=headers,
            )

        # Buffered fallback (non-S3 backends or unknown size).
        try:
            content = await backend_router.read_async(storage_uri)
        except Exception as e:
            raise _map_exc(e, "file download")
        return Response(
            content=content,
            media_type=media_type,
            headers={**base_headers, "Content-Length": str(len(content))},
        )

    # ------------------------------------------------------------------
    # PATCH /{file_id} — union mutation body (FE-team A.2).
    #
    # Accepts any combination of: name / folder / published_to_web / shown_to / metadata /
    # share / share_revoke / permissions / permissions_revoke / variants /
    # restore_version / restore_from_trash / copy_to.
    #
    # Response contract (identical to the aidream host router — the FE
    # derefs a plain FileRecord for basic updates, see thunks.ts):
    #   - only publish/shown_to/metadata set, no X-Idempotency-Key → FileRecord
    #   - any combined-op field or an idempotency key → the
    #     AssetCombinedOpResponse envelope ({asset, share_link, errors[]},
    #     best-effort atomic, never full rollback).
    # ------------------------------------------------------------------
    @router.patch("/{file_id}", response_model=FileRecord | AssetCombinedOpResponse)
    async def patch_file(
        file_id: str,
        body: _PatchBody,
        metadata_merge: bool = Query(
            True,
            description="If true (default), merge into existing metadata. False = replace "
            "(server-stamped policy keys always survive).",
        ),
        x_idempotency_key: str | None = Header(default=None, alias="X-Idempotency-Key"),
        # SPEC-SERVER §3.1. `"<64 hex sha256>"` names the bytes the client read;
        # `W/"v<n>"` names the version, for metadata-only mutations where the
        # bytes are untouched and a checksum would say nothing about what was
        # read. Omitted = last-write-wins, unchanged.
        if_match: str | None = Header(default=None, alias="If-Match"),
        user_id: str = Depends(user_id_dep),
    ):
        is_combined_op = (
            body.name is not None
            or body.folder is not None
            or body.share is not None
            or body.share_revoke
            or bool(body.permissions)
            or bool(body.permissions_revoke)
            or bool(body.variants)
            or body.restore_version is not None
            or body.restore_from_trash
            or body.copy_to is not None
            or x_idempotency_key is not None
        )
        published, shown = stated_row_access(
            published_to_web=body.published_to_web,
            shown_to=body.shown_to,
            legacy_level=body.visibility,
            boundary="PATCH /files/{file_id}",
        )
        try:
            condition = parse_if_match(if_match)
            if condition is not None:
                # Evaluated against the row as it exists RIGHT NOW. A stale
                # client is refused with 412 and the whole conflict input,
                # never allowed to overwrite a change it never saw.
                current = await file_service.file_manager.sync_engine.db.get_file_async(
                    file_id, include_deleted=True
                )
                check_if_match(current, condition)
            if is_combined_op:
                return await file_service.mutate_file(
                    file_id,
                    user_id=user_id,
                    name=body.name,
                    folder=body.folder,
                    published_to_web=published,
                    shown_to=shown,
                    metadata=body.metadata,
                    metadata_replace=not metadata_merge,
                    share=body.share,
                    share_revoke=body.share_revoke,
                    permissions=body.permissions,
                    permissions_revoke=body.permissions_revoke,
                    variants=body.variants,
                    restore_version=body.restore_version,
                    restore_from_trash=body.restore_from_trash,
                    copy_to=body.copy_to,
                    idempotency_key=x_idempotency_key,
                    request_payload_for_idempotency=body.model_dump(exclude_none=True),
                )

            # Basic path: publish/shown_to/metadata only (or an empty body) →
            # the caller gets the canonical FileRecord back, never the
            # envelope (FE consumers deref FileRecord fields directly).
            if published is None and shown is None and body.metadata is None:
                record = await file_service.read_record(file_id, user_id=user_id, level="write")
                return await to_file_record_with_urls_async(file_service.file_manager, record)
            result = await file_service.mutate_file(
                file_id,
                user_id=user_id,
                published_to_web=published,
                shown_to=shown,
                metadata=body.metadata,
                metadata_replace=not metadata_merge,
            )
            sub_errors = result.get("errors") or []
            if sub_errors:
                # A basic update has exactly one intent — a sub-op failure IS
                # the request failing; never return a record implying success.
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    {"error": "patch_failed", "errors": sub_errors},
                )
            record = await file_service.read_record(file_id, user_id=user_id)
            return await to_file_record_with_urls_async(file_service.file_manager, record)
        except Exception as e:
            raise _map_exc(e, "file update")

    # ------------------------------------------------------------------
    # POST /bulk — bulk discriminator (FE-team A.3).
    # ------------------------------------------------------------------
    @router.post("/bulk")
    async def bulk_files(
        body: _BulkBody,
        x_idempotency_key: str | None = Header(default=None, alias="X-Idempotency-Key"),
        user_id: str = Depends(user_id_dep),
    ) -> dict:
        try:
            return await file_service.bulk_op(
                user_id=user_id,
                ids=body.ids,
                op=body.op,
                args=body.args,
                idempotency_key=x_idempotency_key,
                request_payload_for_idempotency=body.model_dump(),
            )
        except Exception as e:
            raise _map_exc(e, "bulk file operation")

    # ------------------------------------------------------------------
    # DELETE /{file_id} — soft delete.
    # ------------------------------------------------------------------
    @router.delete("/{file_id}")
    async def delete_file(
        file_id: str,
        user_id: str = Depends(user_id_dep),
    ) -> dict:
        try:
            ok = await file_service.soft_delete(file_id, user_id=user_id)
            return {"deleted": bool(ok)}
        except Exception as e:
            raise _map_exc(e, "file delete")

    # ------------------------------------------------------------------
    # POST /{file_id}/restore — undo a soft-delete.
    # ------------------------------------------------------------------
    @router.post("/{file_id}/restore")
    async def restore_file(
        file_id: str,
        user_id: str = Depends(user_id_dep),
    ) -> dict:
        try:
            ok = await file_service.restore(file_id, user_id=user_id)
            return {"restored": bool(ok)}
        except Exception as e:
            raise _map_exc(e, "file restore")

    # ------------------------------------------------------------------
    # Share links — list + create for a file. Uses the package's own
    # PermissionsManager (canonical platform.share_links + iam.permissions), so the
    # standalone service serves the same /files/{id}/share-links contract
    # the FE (server-client.ts) already calls against aidream.
    # ------------------------------------------------------------------
    def _permissions_for(user_id: str):
        from ..cloud_sync.permissions import PermissionsManager

        db = file_service.file_manager.sync_engine.db
        return PermissionsManager(db, user_id=user_id)

    @router.get("/{file_id}/share-links", response_model=list[_ShareLinkRecord])
    async def list_file_share_links(
        file_id: str,
        user_id: str = Depends(user_id_dep),
    ) -> list[_ShareLinkRecord]:
        try:
            pm = _permissions_for(user_id)
            rows = await pm.list_share_links_async("file", file_id)
        except Exception as e:
            raise _map_exc(e, "share link listing")
        return [_ShareLinkRecord.model_validate(r) for r in rows]

    @router.post("/{file_id}/share-links", response_model=_ShareLinkRecord)
    async def create_file_share_link(
        file_id: str,
        body: _CreateShareLinkRequest,
        user_id: str = Depends(user_id_dep),
    ) -> _ShareLinkRecord:
        try:
            pm = _permissions_for(user_id)
            row = await pm.create_share_link_async(
                "file",
                file_id,
                permission_level=body.permission_level,
                expires_at=body.expires_at,
                max_uses=body.max_uses,
            )
        except Exception as e:
            raise _map_exc(e, "share link creation")
        return _ShareLinkRecord.model_validate(row)

    return router


__all__ = ["build_file_router"]
