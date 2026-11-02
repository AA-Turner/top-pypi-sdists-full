"""Public share-link byte router.

Mounted WITHOUT authentication — anyone with a share token can resolve
the referenced file. Tokens are CANONICAL ``platform.share_links`` tokens;
the atomic ``iam.resolve_share_token`` resolver enforces revocation,
expiry and max-uses (and consumes one use).

    GET /share/{token}              inline-safe file bytes (canonical public URL)
    GET /share/{token}/download     same bytes (legacy-compatible alias)
    GET /share/{token}/files/{file_id}
                                    bytes of ONE child file of the shared record
                                    (a shared chat's attachment) — access
                                    ladder T-19b. Authorized by
                                    ``iam.share_link_child_file``: the token
                                    is live and the file is a media part of a
                                    visible message of the conversation it
                                    shares. Does NOT consume a use.

Both routes render image/video/audio/PDF inline by default. Callers that
explicitly want a browser download use ``?inline=false``. Active content such
as HTML/SVG/JS is always forced to attachment by the shared streamer policy.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, Request, status
from fastapi.responses import StreamingResponse

from ..cloud_sync.permissions import _is_contextual_system_artifact
from ..service import FileService
from .errors import map_exception


def build_share_router(
    file_service: FileService,
    *,
    prefix: str = "/share",
    tags: list[str] | None = None,
) -> APIRouter:
    """Build the public share-link resolver router. No auth required."""
    router = APIRouter(prefix=prefix, tags=tags or ["share"])

    async def stream_share(
        token: str,
        request: Request,
        *,
        inline: bool,
    ) -> StreamingResponse:
        try:
            link = await file_service.sync_engine.permissions.resolve_share_link_async(token)
        except Exception as exc:
            raise map_exception(
                exc,
                operation="share link resolution",
                user_message="This share link could not be opened right now.",
            ) from exc
        if not link:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                {
                    "error": "share_link_invalid",
                    "message": "Share link invalid, expired, or exhausted",
                },
            )
        file_id = link.get("resource_id")
        if not file_id or link.get("resource_type") != "file":
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                {"error": "not_downloadable", "message": "Share link does not point to a file"},
            )
        record = await file_service.read_record_unchecked(file_id)
        if not record:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                {"error": "not_found", "message": "Shared file no longer exists"},
            )
        # Contextual system artifacts (web-crawl evidence) are container-owned
        # and viewer-ceiling: nobody can hold the 'admin' a share link requires
        # to mint, so any token pointing at one predates the policy (or was
        # minted before the tags were stamped). Serving it would hand anonymous
        # callers bytes the access policy denies to anon unconditionally.
        if _is_contextual_system_artifact(record):
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                {
                    "error": "share_link_invalid",
                    "message": "Share link invalid, expired, or exhausted",
                },
            )
        try:
            streamed = await file_service.sync_engine.streamer.open_stream(
                record,
                range_header=request.headers.get("range"),
                allow_inline=inline,
            )
        except Exception as exc:
            raise map_exception(
                exc,
                operation="shared file streaming",
                user_message="This shared file could not be served right now.",
            ) from exc
        return StreamingResponse(
            streamed.iterator,
            status_code=streamed.status_code,
            media_type=streamed.media_type,
            headers={
                "X-Content-Type-Options": "nosniff",
                **streamed.headers,
            },
        )

    @router.get("/{token}/files/{file_id}")
    async def child_file_share(
        token: str,
        file_id: str,
        request: Request,
        inline: bool = Query(
            True,
            description="Render safe media inline. Set false to force a browser download.",
        ),
    ) -> StreamingResponse:
        """Bytes of one file attached to the shared record — nothing else.

        The token alone reaches ONLY the files that are children of the record
        it shares (a shared chat's attachments); any other file id answers the
        same 404 as a dead token, so the route never confirms a file exists.
        """
        try:
            child = await file_service.sync_engine.permissions.resolve_share_child_file_async(
                token, file_id
            )
        except Exception as exc:
            raise map_exception(
                exc,
                operation="shared child file authorization",
                user_message="This shared file could not be opened right now.",
            ) from exc
        if not child:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                {
                    "error": "share_link_invalid",
                    "message": "This link does not reach that file, or the link is off, expired, or used up.",
                },
            )
        record = await file_service.read_record_unchecked(child["file_id"])
        if not record or record.get("deleted_at"):
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                {"error": "not_found", "message": "The shared file no longer exists."},
            )
        if _is_contextual_system_artifact(record):
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                {
                    "error": "share_link_invalid",
                    "message": "This link does not reach that file, or the link is off, expired, or used up.",
                },
            )
        try:
            streamed = await file_service.sync_engine.streamer.open_stream(
                record,
                range_header=request.headers.get("range"),
                allow_inline=inline,
            )
        except Exception as exc:
            raise map_exception(
                exc,
                operation="shared child file streaming",
                user_message="This shared file could not be served right now.",
            ) from exc
        return StreamingResponse(
            streamed.iterator,
            status_code=streamed.status_code,
            media_type=streamed.media_type,
            headers={
                "X-Content-Type-Options": "nosniff",
                "Cache-Control": "private, no-store",
                **streamed.headers,
            },
        )

    @router.get("/{token}/download")
    async def download_share(
        token: str,
        request: Request,
        inline: bool = Query(
            True,
            description="Render safe media inline. Set false to force a browser download.",
        ),
    ) -> StreamingResponse:
        """Backward-compatible byte route used by already-issued URLs."""
        return await stream_share(token, request, inline=inline)

    @router.get("/{token}")
    async def inline_share(
        token: str,
        request: Request,
        inline: bool = Query(
            True,
            description="Render safe media inline. Set false to force a browser download.",
        ),
    ) -> StreamingResponse:
        """Canonical clean public URL for Markdown and raw media tags."""
        return await stream_share(token, request, inline=inline)

    return router


__all__ = ["build_share_router"]
