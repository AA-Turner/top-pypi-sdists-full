"""TUS resumable upload — protocol-marshaling router factory.

The state machine lives in ``matrx_files.cloud_sync.transports.tus``
(``TUSSessionManager``). This module is the thin HTTP layer: parse TUS
headers, run host-injected policy (auth, quota, path relocation), map typed
manager errors to HTTP status codes.

Endpoints (default ``base_path='/files/upload/tus'``):

    OPTIONS {base}              — capabilities advertisement (auth-free)
    POST    {base}              — Creation (+ creation-with-upload body)
    HEAD    {base}/{upload_id}  — Upload-Offset for resume; completed recovery
    PATCH   {base}/{upload_id}  — append bytes (one part / PATCH)
    DELETE  {base}/{upload_id}  — cancel + cleanup

Host-coupled behavior is injected:

* ``user_id_dep``        — FastAPI dependency → authenticated owner id.
* ``file_manager_dep``   — FastAPI dependency → FileManager (``.sync_engine.tus``);
                           or pass a static ``file_service`` instead.
* ``quota_checker_dep``  — FastAPI dependency → async ``(user_id, upload_length)``
                           checker returning a decision with ``allowed`` /
                           ``reason`` / ``raw`` (or ``None`` = allow). Default
                           allows everything (standalone has no tiers).
* ``sanitize_path``      — ``(raw) -> clean`` raising ``ValueError`` on unsafe
                           input. Default: :func:`matrx_files.path_safety.sanitize_logical_path`.
* ``relocate_path``      — ``(clean_path, origin) -> path`` for system-origin
                           relocation of app-captured content. Default: identity.
* ``finalize``           — async ``(fm, manager, *, upload_id, user_id, request_id)``
                           for host post-processing on the final chunk. Default:
                           plain ``manager.finalize_async`` (request_id stamped
                           into session metadata).
* ``request_id_provider``— ``() -> str | None``. Default reads the matrx-connect
                           AppContext when one is installed.

TUS spec: https://tus.io/protocols/resumable-upload
"""

from __future__ import annotations

import tempfile

import base64
import json
from typing import Any, Protocol
from collections.abc import Awaitable, Callable

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from ..cloud_sync.device_writes import (
    DeviceWriteError,
    parse_client_modified_at,
    parse_device_id,
    reconcile_header_and_metadata,
)
from ..cloud_sync.preconditions import (
    PreconditionError,
    PreconditionFailed,
    check_expected_checksum,
    normalize_expected_checksum,
)
from ..cloud_sync.transports.tus import (
    DEFAULT_MAX_SIZE,
    CleanupPending,
    DeclaredChecksumMismatch,
    DeclaredChecksumUnverifiable,
    ExceedsLength,
    OffsetMismatch,
    PartTooSmall,
    PatchTooLarge,
    IdempotencyKeyReuse,
    S3Failure,
    S3NotConfigured,
    TUSError,
    UploadCompleted,
    UploadBusy,
    UploadIncomplete,
    UploadNotFound,
)
from matrx_utils.row_access import LEGACY_LEVEL_VALUES, SHOWN_TO_VALUES, RowAccess, reconcile_row_access

from ..derivations import ClientPolicyMetadataError, assert_no_client_policy_metadata
from ..request_organization import admitted_organization_id
from ..path_safety import sanitize_logical_path
from ..service import FileService
from ..system_origins import relocate_under_system_origin

# ---------------------------------------------------------------------------
# Protocol constants — TUS spec values + the tunable max size.
# ---------------------------------------------------------------------------

TUS_VERSION = "1.0.0"
TUS_SUPPORTED_VERSIONS = "1.0.0"
TUS_EXTENSIONS = "creation,termination,creation-with-upload"
# The ceiling advertised when the host passes no ``max_size``. It deliberately
# no longer "matches the buffered-upload bypass max": the buffered path holds the
# whole body in memory and so is capped at 5 GB on purpose, while the resumable
# path streams in chunks and exists precisely to carry the files that path
# cannot. Tying them together is what refused every multi-GB data export.
TUS_MAX_SIZE = DEFAULT_MAX_SIZE

# Decoded-size cap for the nested metadata_json payload (16 KB).
MAX_METADATA_JSON_BYTES = 16 * 1024

_TUS_HEADERS_BASE: dict[str, str] = {
    "Tus-Resumable": TUS_VERSION,
    "Cache-Control": "no-store",
}


class QuotaDecision(Protocol):
    """Shape of a quota decision — hosts return their own object."""

    allowed: bool
    reason: str | None
    raw: Any


QuotaChecker = Callable[[str, int], Awaitable["QuotaDecision | None"]]
FinalizeCallable = Callable[..., Awaitable[Any]]


def _tus_headers(extra: dict[str, str] | None = None) -> dict[str, str]:
    h = dict(_TUS_HEADERS_BASE)
    if extra:
        h.update(extra)
    return h


def _tus_error(
    status_code: int, detail: dict[str, object], extra_headers: dict[str, str] | None = None
) -> HTTPException:
    """HTTPException carrying the TUS protocol headers.

    The spec requires ``Tus-Resumable`` on EVERY response except OPTIONS —
    error responses included — so every error raised by this router goes
    through here.
    """
    return HTTPException(status_code, detail, headers=_tus_headers(extra_headers))


def _check_tus_version(request: Request) -> None:
    v = request.headers.get("tus-resumable")
    if v and v != TUS_VERSION:
        # Spec: a 412 version mismatch MUST include Tus-Version.
        raise _tus_error(
            status.HTTP_412_PRECONDITION_FAILED,
            {
                "error": "tus_version_mismatch",
                "message": f"Server supports {TUS_VERSION}; client sent {v!r}",
            },
            {"Tus-Version": TUS_SUPPORTED_VERSIONS},
        )


def parse_upload_metadata(header: str | None) -> dict[str, str]:
    """Parse the comma-separated ``key b64(value)`` Upload-Metadata header."""
    out: dict[str, str] = {}
    if not header:
        return out
    for chunk in header.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        parts = chunk.split(" ", 1)
        key = parts[0]
        if len(parts) == 1:
            out[key] = ""
            continue
        try:
            out[key] = base64.b64decode(parts[1]).decode("utf-8")
        except Exception:
            if key == "metadata_json":
                # metadata_json is load-bearing — never silently drop it.
                raise _tus_error(
                    400,
                    {
                        "error": "invalid_metadata",
                        "message": "Upload-Metadata metadata_json is not valid base64/UTF-8",
                    },
                )
            continue
    return out


def merge_metadata_json(metadata: dict[str, str]) -> dict[str, object]:
    """Merge the optional nested ``metadata_json`` key into the flat TUS metadata.

    Mirrors the buffered path (``/files/upload`` ``metadata_json`` form field):
    the value must decode to a JSON object; anything else is a loud 400. On top
    of the buffered contract we cap the decoded size and forbid ``_``-prefixed
    keys (that namespace is server-stamped: ``_idempotency_key``, request ids).
    Flat non-``metadata_json`` keys keep their existing behavior; nested keys
    win on collision so a TUS upload and a buffered upload of the same file
    produce identical nested row metadata (including ``metadata.capture``).
    """
    raw = metadata.pop("metadata_json", None)
    merged: dict[str, object] = dict(metadata)
    if raw is None:
        return merged
    if len(raw.encode("utf-8")) > MAX_METADATA_JSON_BYTES:
        raise _tus_error(
            400,
            {
                "error": "invalid_metadata",
                "message": f"metadata_json exceeds {MAX_METADATA_JSON_BYTES} bytes decoded",
            },
        )
    try:
        parsed = json.loads(raw)
        if not isinstance(parsed, dict):
            raise ValueError("metadata_json must decode to an object")
    except (json.JSONDecodeError, ValueError) as e:
        raise _tus_error(400, {"error": "invalid_metadata", "message": str(e)})
    reserved = [k for k in parsed if isinstance(k, str) and k.startswith("_")]
    if reserved:
        raise _tus_error(
            400,
            {
                "error": "invalid_metadata",
                "message": f"metadata_json keys are reserved (server-stamped): {sorted(reserved)}",
            },
        )
    try:
        # Policy keys (system_artifact / artifact_domain / web_site_id / …) are
        # server-stamped authorization inputs — never accepted from a client.
        assert_no_client_policy_metadata(parsed, context="tus upload metadata")
    except ClientPolicyMetadataError as e:
        raise _tus_error(403, {"error": "reserved_metadata_key", "message": str(e)})
    merged.update(parsed)
    return merged


async def _assert_device_belongs_to_caller(device_id: str, user_id: str) -> None:
    """A write is never attributed to another account's machine (§2.2)."""
    from matrx_files.db.models import AppInstances

    rows = await AppInstances.filter(id=device_id).values("id", "user_id")
    if not rows:
        raise DeviceWriteError(
            "invalid_device",
            f"No registered device {device_id}. Register the device "
            "(public.app_instances) before attributing an upload to it.",
        )
    if str(rows[0]["user_id"]) != str(user_id):
        raise DeviceWriteError(
            "invalid_device",
            f"Device {device_id} belongs to a different user.",
        )


def map_tus_error(e: TUSError) -> HTTPException:
    """Map a state-machine error to the right HTTP status + JSON body."""
    if isinstance(e, DeclaredChecksumMismatch):
        # 422, not 409: 409 already means "your upload SESSION is in the wrong
        # state" on this router, and a corrupt transfer is a different thing.
        return _tus_error(422, {"error": "checksum_mismatch", "message": str(e)})
    if isinstance(e, DeclaredChecksumUnverifiable):
        return _tus_error(422, {"error": "checksum_unverifiable", "message": str(e)})
    if isinstance(e, UploadNotFound):
        return _tus_error(404, {"error": "not_found", "message": str(e)})
    if isinstance(e, UploadCompleted):
        return _tus_error(409, {"error": "upload_completed", "message": str(e)})
    if isinstance(e, IdempotencyKeyReuse):
        return _tus_error(409, {"error": "idempotency_key_reuse", "message": str(e)})
    if isinstance(e, UploadBusy):
        return _tus_error(409, {"error": "upload_busy", "message": str(e)})
    if isinstance(e, UploadIncomplete):
        return _tus_error(409, {"error": "upload_incomplete", "message": str(e)})
    if isinstance(e, CleanupPending):
        return _tus_error(503, {"error": "cleanup_pending", "message": str(e)})
    if isinstance(e, OffsetMismatch):
        return _tus_error(
            409,
            {
                "error": "offset_mismatch",
                "message": str(e),
            },
        )
    if isinstance(e, PartTooSmall):
        return _tus_error(400, {"error": "patch_too_small", "message": str(e)})
    if isinstance(e, ExceedsLength):
        return _tus_error(413, {"error": "exceeds_upload_length", "message": str(e)})
    if isinstance(e, PatchTooLarge):
        return _tus_error(413, {"error": "patch_too_large", "message": str(e)})
    if isinstance(e, S3NotConfigured):
        return _tus_error(503, {"error": "s3_unavailable", "message": str(e)})
    if isinstance(e, S3Failure):
        return _tus_error(502, {"error": f"s3_{e.op}_failed", "message": repr(e.cause)})
    return _tus_error(500, {"error": "tus_internal", "message": str(e)})


def _default_request_id_provider() -> str | None:
    from matrx_connect import try_get_app_context

    ctx = try_get_app_context()
    rid = getattr(ctx, "request_id", None) if ctx else None
    return rid if isinstance(rid, str) and rid else None


async def _default_finalize(
    fm: Any,
    manager: Any,
    *,
    upload_id: str,
    user_id: str,
    request_id: str | None,
) -> Any:
    extra: dict[str, str] = {}
    if request_id:
        extra["request_id"] = request_id
    return await manager.finalize_async(
        upload_id=upload_id,
        owner_id=user_id,
        extra_metadata=extra,
    )


def build_tus_router(
    file_service: FileService | None = None,
    *,
    file_manager_dep: Callable[..., Any] | None = None,
    user_id_dep: Callable[..., str] | None = None,
    quota_checker_dep: Callable[..., QuotaChecker] | None = None,
    sanitize_path: Callable[[str], str] = sanitize_logical_path,
    relocate_path: Callable[[str, str | None], str] | None = None,
    finalize: FinalizeCallable = _default_finalize,
    request_id_provider: Callable[[], str | None] = _default_request_id_provider,
    base_path: str = "/files/upload/tus",
    tags: list[str] | None = None,
    max_size: int | None = None,
) -> APIRouter:
    """Build the TUS router. Exactly one of ``file_service`` /
    ``file_manager_dep`` must be provided; hosts with a per-request
    FileManager dependency pass ``file_manager_dep`` so their own
    dependency overrides keep working.

    ``max_size`` is what OPTIONS advertises as ``Tus-Max-Size``. Pass the SAME
    number the host puts in ``CloudSyncConfig.tus_max_size_bytes``: a client that
    is told one ceiling and refused at another cannot tell a policy from a bug.
    The guard ``tests/test_tus_advertised_ceiling_matches.py`` holds the two
    together.
    """
    advertised_max_size = max_size if max_size is not None else TUS_MAX_SIZE
    if (file_service is None) == (file_manager_dep is None):
        raise ValueError(
            "build_tus_router requires exactly one of file_service / file_manager_dep"
        )
    if file_manager_dep is None:
        assert file_service is not None

        def file_manager_dep() -> Any:  # noqa: E306
            return file_service.file_manager

    if user_id_dep is None:
        # Test-mode default: every request is the same anonymous user.
        def user_id_dep() -> str:  # noqa: E306
            return "anonymous"

    if quota_checker_dep is None:

        def quota_checker_dep() -> QuotaChecker:  # noqa: E306
            async def _allow(user_id: str, upload_length: int) -> None:
                return None

            return _allow

    # Origin routing is package policy, not host policy. Hosts may override the
    # resolver, but standalone must never silently preserve a user-visible path
    # for app-captured content.
    _relocate = relocate_path or relocate_under_system_origin

    router = APIRouter(tags=tags or ["files", "tus"])

    # ------------------------------------------------------------------
    # OPTIONS — capabilities advertisement.
    # ------------------------------------------------------------------

    @router.options(base_path)
    async def tus_options() -> Response:
        return Response(
            status_code=status.HTTP_204_NO_CONTENT,
            headers=_tus_headers(
                {
                    "Tus-Version": TUS_SUPPORTED_VERSIONS,
                    "Tus-Max-Size": str(advertised_max_size),
                    "Tus-Extension": TUS_EXTENSIONS,
                }
            ),
        )

    # ------------------------------------------------------------------
    # POST — Creation. Returns Location header pointing at {base}/{id}.
    # ------------------------------------------------------------------

    @router.post(base_path)
    async def tus_create(
        request: Request,
        fm: Any = Depends(file_manager_dep),
        user_id: str = Depends(user_id_dep),
        check_quota: QuotaChecker = Depends(quota_checker_dep),
    ):
        _check_tus_version(request)

        # Parse + validate the TUS-side headers.
        upload_length_header = request.headers.get("upload-length")
        if not upload_length_header:
            raise _tus_error(
                400, {"error": "missing_upload_length", "message": "Upload-Length is required"}
            )
        try:
            upload_length = int(upload_length_header)
        except ValueError:
            raise _tus_error(400, {"error": "invalid_upload_length"})

        metadata = parse_upload_metadata(request.headers.get("upload-metadata"))
        row_metadata = merge_metadata_json(metadata)
        # Transport-level keys, promoted to columns/session state below. They are
        # not file metadata and must not land on the row (same reason filename /
        # filepath are stripped in create_async).
        for _transport_key in ("sha256", "expectedchecksum", "deviceid", "clientmodifiedat"):
            row_metadata.pop(_transport_key, None)
        # ---- the ONE organization resolution for this TUS session ---------
        # Stamped HERE, at the edge, from the request the auth boundary
        # admitted — and stamped at CREATE, not finalize: a resumable upload
        # can run for minutes and finish on a later request, so the session
        # must carry the organization it was opened in rather than re-derive
        # one from whatever context the finalizing request happens to have.
        # A client-declared organization_id is overwritten, never trusted:
        # placement is context, never authority. See
        # matrx_files/request_organization.py for the outage this closes.
        _admitted_organization_id = admitted_organization_id()
        if _admitted_organization_id:
            row_metadata["organization_id"] = _admitted_organization_id
        file_path = metadata.get("filepath") or metadata.get("filename")
        if not file_path:
            raise _tus_error(
                400,
                {
                    "error": "missing_filepath",
                    "message": "Upload-Metadata must include filepath or filename",
                },
            )
        try:
            clean_path = sanitize_path(file_path)
        except ValueError as e:
            raise _tus_error(400, {"error": "invalid_path", "message": str(e)})

        # App-captured content (recordings, etc.) declares provenance via
        # Upload-Metadata `origin`; the host relocates it under the matching
        # system folder so it is hidden from the user's file tree.
        # Unconditional across EVERY insert path — the TUS row is registered
        # at this path and finalize inherits it.
        origin = row_metadata.get("origin")
        clean_path = _relocate(clean_path, origin if isinstance(origin, str) else None)

        # Row-access words ride Upload-Metadata: ``published_to_web`` ("true"/"false")
        # and ``shown_to``. The retiring single level word is the T-13 transitional
        # wire input, reconciled (and logged) only when neither new word is sent.
        raw_published = metadata.get("published_to_web")
        raw_shown = metadata.get("shown_to")
        raw_legacy = (metadata.get("visibility") or "").lower() or None  # T-13 transitional wire input
        access = reconcile_row_access(
            published_to_web=(
                None if raw_published in (None, "") else str(raw_published).lower() in ("1", "true", "yes")
            ),
            shown_to=raw_shown if raw_shown in SHOWN_TO_VALUES else None,
            legacy_level=raw_legacy if raw_legacy in LEGACY_LEVEL_VALUES else None,
            default=RowAccess(shown_to="only_me"),
            boundary="POST /files/tus",
        )
        mime_type = metadata.get("mimetype") or metadata.get("filetype") or None

        # Host-specific: quota pre-flight at create time. Re-checked on finalize.
        decision = await check_quota(user_id, upload_length)
        if decision is not None and not decision.allowed:
            raise _tus_error(
                413,
                {
                    "error": decision.reason or "quota_exceeded",
                    "message": "Upload refused by account-quota policy.",
                    "details": decision.raw,
                },
            )

        # ---- folder-sync write contract (SPEC-SERVER §2.2, §3.1, §5) --------
        # TUS has no body, so device provenance and the precondition ride
        # Upload-Metadata; the daemon may ALSO send the two provenance values as
        # headers, in which case the HEADER WINS and a disagreement is a 400 --
        # never a silent pick that attributes a file to the wrong machine.
        try:
            declared_sha256 = metadata.get("sha256")
            if declared_sha256:
                declared_sha256 = normalize_expected_checksum(declared_sha256)
                if declared_sha256 == "absent":
                    raise PreconditionError(
                        "invalid_declared_checksum",
                        "Upload-Metadata sha256 must be the 64-hex SHA-256 of the file "
                        "being uploaded; 'absent' is a precondition value, not a checksum.",
                    )
            expected_checksum = normalize_expected_checksum(metadata.get("expectedchecksum"))
            origin_device_id = parse_device_id(
                reconcile_header_and_metadata(
                    name="device id",
                    header_value=request.headers.get("x-matrx-device-id"),
                    metadata_value=metadata.get("deviceid"),
                )
            )
            client_modified_at = parse_client_modified_at(
                reconcile_header_and_metadata(
                    name="client modified time",
                    header_value=request.headers.get("x-matrx-client-modified-at"),
                    metadata_value=metadata.get("clientmodifiedat"),
                )
            )
            if origin_device_id is not None:
                await _assert_device_belongs_to_caller(origin_device_id, user_id)
        except (DeviceWriteError, PreconditionError) as e:
            raise _tus_error(400, {"error": e.code, "message": e.message})

        # Evaluated at creation AND re-evaluated at finalize: a resumable upload
        # can run for minutes, and the state checked here is not necessarily the
        # state it is about to overwrite.
        if expected_checksum is not None:
            try:
                check_expected_checksum(
                    await fm.sync_engine.db.get_file_by_path_async(user_id, clean_path),
                    expected_checksum,
                )
            except PreconditionFailed as conflict:
                raise _tus_error(412, conflict.payload)

        idempotency_key = request.headers.get("x-idempotency-key")
        try:
            result = await fm.sync_engine.tus.create_async(
                owner_id=user_id,
                file_path=clean_path,
                upload_length=upload_length,
                mime_type=mime_type,
                published_to_web=access.published_to_web,
                shown_to=access.shown_to,
                metadata=row_metadata,
                idempotency_key=idempotency_key,
                declared_sha256=declared_sha256,
                expected_checksum=expected_checksum,
                origin_device_id=origin_device_id,
                client_modified_at=client_modified_at,
            )
        except TUSError as e:
            raise map_tus_error(e)

        location = f"{base_path}/{result.upload_id}"
        headers: dict[str, str] = {
            "Location": location,
            "Upload-Offset": str(result.upload_offset),
            "Upload-Length": str(result.upload_length),
        }

        # creation-with-upload: a POST carrying an offset+octet-stream body has
        # its bytes appended immediately — same path as PATCH. Skipped on an
        # idempotency replay (the resumed session's offset is authoritative;
        # the client resumes via HEAD + PATCH).
        carries_body = (
            request.headers.get("content-type") == "application/offset+octet-stream"
        )
        spool: Any = None
        spooled_bytes = 0
        if carries_body and not result.is_replay:
            # Same rule as PATCH: the chunk is spooled in blocks and handed over
            # as a stream, never materialised. A creation-with-upload body is the
            # same size as any other chunk, so it had the same memory cost.
            spool = tempfile.TemporaryFile()
            async for block in request.stream():
                if block:
                    spool.write(block)
                    spooled_bytes += len(block)
            spool.seek(0)
        if spooled_bytes and not result.is_replay:
            manager = fm.sync_engine.tus
            try:
                append = await manager.append_async(
                    upload_id=result.upload_id,
                    owner_id=user_id,
                    body=spool,
                    client_offset=result.upload_offset,
                    body_length=spooled_bytes,
                )
            except TUSError as e:
                spool.close()
                raise map_tus_error(e)
            finally:
                if spool is not None and not spool.closed:
                    spool.close()
            headers["Upload-Offset"] = str(append.new_offset)
            if append.is_final:
                try:
                    finalized = await finalize(
                        fm,
                        manager,
                        upload_id=result.upload_id,
                        user_id=user_id,
                        request_id=request_id_provider(),
                    )
                except PreconditionFailed as conflict:
                    # Re-evaluated at finalize: the row changed while the
                    # resumable upload was in flight. The object is purged and
                    # no row is created; the client gets the whole conflict.
                    raise _tus_error(412, conflict.payload)
                except TUSError as e:
                    raise map_tus_error(e)
                headers["Upload-Offset"] = str(finalized.size_bytes)
                headers["Upload-Complete"] = "true"
                headers["X-Cld-File-Id"] = finalized.file_id

        return Response(
            status_code=status.HTTP_201_CREATED,
            headers=_tus_headers(headers),
        )

    # ------------------------------------------------------------------
    # HEAD — return current Upload-Offset. Used to resume.
    # ------------------------------------------------------------------

    @router.head(base_path + "/{upload_id}")
    async def tus_head(
        upload_id: str,
        request: Request,
        fm: Any = Depends(file_manager_dep),
        user_id: str = Depends(user_id_dep),
    ):
        _check_tus_version(request)
        session = await fm.sync_engine.tus.get_async(
            upload_id=upload_id,
            owner_id=user_id,
        )
        # get_async is owner-scoped: unknown/foreign sessions come back None.
        # Aborted/aborting sessions are gone for good. Active leased states
        # remain visible so reconnecting clients do not create duplicates.
        if not session or session.status not in (
            "in_progress",
            "uploading",
            "ready",
            "finalizing",
            "completed",
        ):
            raise _tus_error(404, {"error": "not_found"})

        if session.status == "completed":
            # Lost-final-response recovery: the server finalized but the client
            # never saw the PATCH response. HEAD must hand back the finished
            # state + the file id so the client never re-uploads. A dedup hit
            # records the canonical winner in metadata; otherwise the session's
            # own file_id IS the finalized files.files row id.
            winner = session.metadata.get("dedup_winner_file_id")
            file_id = winner if isinstance(winner, str) and winner else session.file_id
            return Response(
                status_code=status.HTTP_200_OK,
                headers=_tus_headers(
                    {
                        "Upload-Offset": str(session.upload_length),
                        "Upload-Length": str(session.upload_length),
                        "Upload-Complete": "true",
                        "X-Cld-File-Id": file_id,
                    }
                ),
            )

        active_headers = {
            "Upload-Offset": str(session.upload_offset),
            "Upload-Length": str(session.upload_length),
        }
        if session.status in ("uploading", "ready", "finalizing"):
            active_headers["Retry-After"] = "1"
        return Response(
            status_code=status.HTTP_200_OK,
            headers=_tus_headers(active_headers),
        )

    # ------------------------------------------------------------------
    # PATCH — append one chunk. Each PATCH = one S3 part.
    # ------------------------------------------------------------------

    @router.patch(base_path + "/{upload_id}")
    async def tus_patch(
        upload_id: str,
        request: Request,
        fm: Any = Depends(file_manager_dep),
        user_id: str = Depends(user_id_dep),
        check_quota: QuotaChecker = Depends(quota_checker_dep),
    ):
        _check_tus_version(request)
        if request.headers.get("content-type") != "application/offset+octet-stream":
            raise _tus_error(
                415,
                {
                    "error": "unsupported_media_type",
                    "message": "Content-Type must be application/offset+octet-stream",
                },
            )
        upload_offset_header = request.headers.get("upload-offset")
        if upload_offset_header is None:
            raise _tus_error(400, {"error": "missing_upload_offset"})
        try:
            client_offset = int(upload_offset_header)
        except ValueError:
            raise _tus_error(400, {"error": "invalid_upload_offset"})

        # THE CHUNK IS NEVER HELD WHOLE. `await request.body()` used to read the
        # entire PATCH into memory, so a server running N concurrent uploads at
        # the 256 MiB per-chunk ceiling held N x 256 MiB — the last real limit on
        # multi-GB uploads after the 5 GB ceiling came off. The body is now
        # spooled to a temp file in small blocks and handed to boto3 as a stream,
        # so peak memory is PATCH_BLOCK_BYTES regardless of chunk size.
        declared = request.headers.get("content-length")
        if declared is None:
            raise _tus_error(
                400,
                {
                    "error": "missing_content_length",
                    "message": (
                        "A PATCH must declare Content-Length. Without it the server "
                        "cannot tell a complete chunk from a truncated one, and a "
                        "truncated part stored as whole would silently corrupt the "
                        "upload."
                    ),
                },
            )
        try:
            declared_length = int(declared)
        except ValueError:
            raise _tus_error(400, {"error": "invalid_content_length"})

        manager = fm.sync_engine.tus
        with tempfile.TemporaryFile() as spool:
            read_bytes = 0
            async for block in request.stream():
                if not block:
                    continue
                read_bytes += len(block)
                if read_bytes > declared_length:
                    raise _tus_error(
                        400,
                        {
                            "error": "content_length_mismatch",
                            "message": (
                                f"This chunk declared {declared_length} bytes but the "
                                f"connection kept sending past that. Nothing was "
                                "stored. Resend the chunk; the upload resumes from "
                                "where it is."
                            ),
                        },
                    )
                spool.write(block)
            if read_bytes != declared_length:
                raise _tus_error(
                    400,
                    {
                        "error": "content_length_mismatch",
                        "message": (
                            f"This chunk declared {declared_length} bytes but only "
                            f"{read_bytes} arrived, so it is truncated. Nothing was "
                            "stored. Resend the chunk; the upload resumes from where "
                            "it is and no bytes are lost."
                        ),
                    },
                )
            spool.seek(0)
            try:
                result = await manager.append_async(
                    upload_id=upload_id,
                    owner_id=user_id,
                    body=spool,
                    client_offset=client_offset,
                    body_length=read_bytes,
                )
            except TUSError as e:
                raise map_tus_error(e)

        if not result.is_final:
            return Response(
                status_code=status.HTTP_204_NO_CONTENT,
                headers=_tus_headers({"Upload-Offset": str(result.new_offset)}),
            )

        # Final chunk landed — finalize + host-side post-processing.
        try:
            finalized = await finalize(
                fm,
                manager,
                upload_id=upload_id,
                user_id=user_id,
                request_id=request_id_provider(),
            )
        except PreconditionFailed as conflict:
            # Re-evaluated at finalize (§3.1): the row changed while the
            # resumable upload was in flight. The object is purged and no row is
            # created; the client gets the whole conflict input, not a bare 412.
            raise _tus_error(412, conflict.payload)
        except TUSError as e:
            raise map_tus_error(e)

        return Response(
            status_code=status.HTTP_204_NO_CONTENT,
            headers=_tus_headers(
                {
                    "Upload-Offset": str(finalized.size_bytes),
                    "Upload-Complete": "true",
                    "X-Cld-File-Id": finalized.file_id,
                }
            ),
        )

    # ------------------------------------------------------------------
    # DELETE — Termination extension. Aborts the multipart + marks the row.
    # ------------------------------------------------------------------

    @router.delete(base_path + "/{upload_id}")
    async def tus_delete(
        upload_id: str,
        request: Request,
        fm: Any = Depends(file_manager_dep),
        user_id: str = Depends(user_id_dep),
    ):
        _check_tus_version(request)
        try:
            await fm.sync_engine.tus.abort_async(
                upload_id=upload_id,
                owner_id=user_id,
            )
        except TUSError as e:
            raise map_tus_error(e)
        return Response(status_code=status.HTTP_204_NO_CONTENT, headers=_tus_headers())

    return router
