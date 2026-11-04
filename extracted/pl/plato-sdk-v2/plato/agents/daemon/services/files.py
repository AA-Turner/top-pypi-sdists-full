"""Files service: raw-byte push/pull, streamed both ways.

Push writes an octet-stream body to a path (creating parent dirs). Pull streams
the file back with sha256 + size headers. Streaming means large spools (whose
JSONL records exceed the 64KB line limit that broke SSH cat-based reads) move
without any per-line framing constraint.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from aiohttp import web

from plato.agents.daemon.http_util import error_response, ok_response, request_id_of
from plato.agents.daemon.state import DaemonContext
from plato.rpc.models.files import FileStatResponse, FileWriteResponse
from plato.rpc.protocol import (
    API_PREFIX,
    CAP_FILES_PULL,
    CAP_FILES_PUSH,
    HEADER_FILE_SIZE,
    HEADER_REQUEST_ID,
)

_CHUNK = 1024 * 1024


def _require_path(request: web.Request) -> str | None:
    return request.query.get("path")


async def _push(request: web.Request) -> web.StreamResponse:
    path_str = _require_path(request)
    if not path_str:
        return error_response(request, "INVALID_REQUEST", "path query param required")
    path = Path(path_str)
    mkdirs = request.query.get("mkdirs", "1") != "0"
    mode = int(request.query.get("mode", "0o600"), 0) if "mode" in request.query else 0o600

    if mkdirs:
        path.parent.mkdir(parents=True, exist_ok=True)

    hasher = hashlib.sha256()
    total = 0
    try:
        with open(path, "wb") as fh:
            async for chunk in request.content.iter_chunked(_CHUNK):
                fh.write(chunk)
                hasher.update(chunk)
                total += len(chunk)
        path.chmod(mode)
    except OSError as exc:
        return error_response(request, "INTERNAL", f"write failed: {exc}")

    return ok_response(
        request,
        FileWriteResponse(path=str(path), bytes_written=total, sha256=hasher.hexdigest()),
    )


async def _pull(request: web.Request) -> web.StreamResponse:
    path_str = _require_path(request)
    if not path_str:
        return error_response(request, "INVALID_REQUEST", "path query param required")
    path = Path(path_str)
    if not path.is_file():
        return error_response(request, "NOT_FOUND", f"no such file: {path}")

    size = path.stat().st_size
    # Optional additive param: ?tail=N returns only the last N bytes — spool
    # tails for failure logging shouldn't cost a full-file download. Old
    # daemons ignore unknown params and send the whole body, so callers slice
    # client-side too (see FilesStub.pull_tail).
    start = 0
    tail_raw = request.query.get("tail")
    if tail_raw is not None:
        try:
            tail = int(tail_raw)
        except ValueError:
            return error_response(request, "INVALID_REQUEST", f"invalid tail: {tail_raw!r}")
        if tail < 0:
            return error_response(request, "INVALID_REQUEST", f"invalid tail: {tail_raw!r}")
        start = max(0, size - tail)
    resp = web.StreamResponse(
        headers={
            "Content-Type": "application/octet-stream",
            # Always the FULL file size — with ?tail, callers compare it to the
            # body length to know how much was truncated.
            HEADER_FILE_SIZE: str(size),
            HEADER_REQUEST_ID: request_id_of(request),
        }
    )
    resp.content_length = size - start
    await resp.prepare(request)
    hasher = hashlib.sha256()
    with open(path, "rb") as fh:
        fh.seek(start)
        while True:
            chunk = fh.read(_CHUNK)
            if not chunk:
                break
            hasher.update(chunk)
            await resp.write(chunk)
    # sha256 is a trailer conceptually; we set it as a header before prepare
    # would require reading twice, so pull clients verify size and may re-hash.
    await resp.write_eof()
    return resp


async def _stat(request: web.Request) -> web.Response:
    path_str = _require_path(request)
    if not path_str:
        return error_response(request, "INVALID_REQUEST", "path query param required")
    path = Path(path_str)
    if not path.exists():
        return ok_response(request, FileStatResponse(path=str(path), exists=False))
    st = path.stat()
    return ok_response(
        request,
        FileStatResponse(path=str(path), exists=True, size=st.st_size, is_dir=path.is_dir()),
    )


def register(app: web.Application, ctx: DaemonContext) -> None:
    app.router.add_put(f"{API_PREFIX}/files/content", _push)
    app.router.add_get(f"{API_PREFIX}/files/content", _pull)
    app.router.add_get(f"{API_PREFIX}/files/stat", _stat)
    ctx.capabilities.append(CAP_FILES_PUSH)
    ctx.capabilities.append(CAP_FILES_PULL)
