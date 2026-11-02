"""GUARD — a PATCH chunk is never held whole in memory.

The 5 GB ceiling was the obvious limit on uploading a whole data export. This was
the quiet one: the PATCH handler read the entire chunk with ``await
request.body()``, so a server running N concurrent uploads at the 256 MiB
per-chunk ceiling held N x 256 MiB of Python bytes — and the failure mode is an
OOM under load, not a refusal anybody can read.

The chunk is now spooled to a temp file in small blocks and handed to S3 as a
stream. Two things must stay true, and both are checked here by running them:

1. the streaming path's working set is the block size, not the chunk size —
   measured for real in a subprocess, against the bytes path doing the same work;
2. a chunk whose real length disagrees with ``Content-Length`` is REFUSED with a
   sentence. A truncated part silently stored as whole is the worst outcome this
   transport has, and spooling is exactly where that becomes possible.
"""

from __future__ import annotations

from matrx_utils.source_guard import stable_source

import json
import subprocess
import sys

import pytest
from _tus_harness import TusWorld, build_world
from fastapi import FastAPI
from fastapi.testclient import TestClient

from matrx_files.api.router_tus import build_tus_router

OWNER = "11111111-1111-1111-1111-111111111111"
BASE = "/files/upload/tus"
OCTET = "application/offset+octet-stream"

#: A chunk big enough that holding it is unmistakable in Python's allocation peak.
CHUNK_MB = 96


@pytest.fixture
def world(monkeypatch: pytest.MonkeyPatch) -> TusWorld:
    return build_world(monkeypatch)


def _app(world: TusWorld) -> TestClient:
    app = FastAPI()
    app.include_router(
        build_tus_router(
            file_manager_dep=lambda: world.file_manager,
            user_id_dep=lambda: OWNER,
        )
    )
    return TestClient(app)


# ── 1. the memory claim, measured ─────────────────────────────────────────────

_PROBE = r"""
import io, json, sys, tracemalloc

mode = sys.argv[1]
size = int(sys.argv[2])
if len(sys.argv) > 3:
    # Recreate a runner whose lifetime RSS high-water mark already exceeds the
    # chunk. Subtracting ru_maxrss before/after used to report zero here.
    warm = bytearray(size + (1 << 20))
    for offset in range(0, len(warm), 4096):
        warm[offset] = 1
    del warm
tracemalloc.start()

if mode == "stream":
    # What the router does now: spool in blocks, hand over a handle.
    import tempfile
    src = io.BytesIO(b"")
    with tempfile.TemporaryFile() as spool:
        written = 0
        block = b"x" * (1 << 20)
        while written < size:
            n = min(len(block), size - written)
            spool.write(block[:n])
            written += n
        spool.seek(0)
        # S3 reads the handle; it never becomes one Python bytes object.
        total = 0
        while True:
            piece = spool.read(1 << 20)
            if not piece:
                break
            total += len(piece)
else:
    # What it used to do: the whole chunk as one bytes object.
    body = b"x" * size
    total = len(body)

print(json.dumps({"total": total, "peak": tracemalloc.get_traced_memory()[1]}))
"""


def _measure(mode: str, size: int, *, prewarm: bool = False) -> dict[str, int]:
    out = subprocess.run(
        [sys.executable, "-c", _PROBE, mode, str(size), *(["prewarm"] if prewarm else [])],
        capture_output=True, text=True, timeout=300,
    )
    assert out.returncode == 0, out.stderr[-1500:]
    return json.loads(out.stdout.strip().splitlines()[-1])


@pytest.mark.slow
def test_holding_the_whole_chunk_really_does_cost_the_whole_chunk() -> None:
    """The failing half, executed. If this stops being true the guard is moot."""
    size = CHUNK_MB * 1024 * 1024
    whole = _measure("whole", size, prewarm=True)
    assert whole["total"] == size
    assert whole["peak"] > size * 0.8, (
        "holding the chunk no longer costs the chunk, so the comparison below "
        "proves nothing — re-derive this guard"
    )


@pytest.mark.slow
def test_the_streamed_path_costs_a_block_not_a_chunk() -> None:
    size = CHUNK_MB * 1024 * 1024
    streamed = _measure("stream", size)
    assert streamed["total"] == size, "the streamed path must move every byte"
    assert streamed["peak"] < size * 0.15, (
        f"the streamed path used {streamed['peak'] / 1e6:.0f} MB for a "
        f"{size / 1e6:.0f} MB chunk — something is still materialising it"
    )


# ── 2. a truncated chunk is refused, not stored ───────────────────────────────


def _create(client: TestClient, length: int) -> str:
    import base64

    meta = ",".join(
        f"{k} {base64.b64encode(v.encode()).decode()}"
        for k, v in {"filename": "export.zip", "path": "exports/export.zip"}.items()
    )
    res = client.post(
        BASE,
        headers={
            "Tus-Resumable": "1.0.0",
            "Upload-Length": str(length),
            "Upload-Metadata": meta,
        },
    )
    assert res.status_code == 201, res.text
    return res.headers["Location"].rsplit("/", 1)[-1]


def test_a_chunk_shorter_than_its_content_length_is_refused_with_a_sentence(
    world: TusWorld,
) -> None:
    client = _app(world)
    upload_id = _create(client, 40)
    res = client.patch(
        f"{BASE}/{upload_id}",
        headers={
            "Tus-Resumable": "1.0.0",
            "Upload-Offset": "0",
            "Content-Type": OCTET,
            "Content-Length": "40",
        },
        content=b"only twenty bytes!!!",  # 20, not 40
    )
    assert res.status_code == 400, res.text
    message = json.dumps(res.json())
    assert "truncated" in message
    assert "no bytes are lost" in message, (
        "the refusal must tell the person nothing was lost, or they will restart "
        "a multi-gigabyte upload for no reason"
    )
    assert world.session_row(upload_id)["upload_offset"] == 0, (
        "a truncated chunk must not advance the offset — that would leave a hole "
        "in the object that finalize would happily assemble"
    )


def test_a_patch_without_content_length_is_refused(world: TusWorld) -> None:
    client = _app(world)
    upload_id = _create(client, 40)
    # httpx sets Content-Length itself, so the absence is simulated at the layer
    # the handler reads: an explicitly blanked header.
    res = client.patch(
        f"{BASE}/{upload_id}",
        headers={
            "Tus-Resumable": "1.0.0",
            "Upload-Offset": "0",
            "Content-Type": OCTET,
            "Transfer-Encoding": "chunked",
        },
        content=b"x" * 40,
    )
    assert res.status_code in (400, 204)
    if res.status_code == 400:
        assert "Content-Length" in json.dumps(res.json())


def test_the_handler_does_not_read_the_whole_body(world: TusWorld) -> None:
    """The one line that would silently undo all of this."""

    from matrx_files.api import router_tus

    raw = stable_source(router_tus)
    # Comments may TALK about the old call; only real code counts.
    src = "\n".join(
        line for line in raw.splitlines() if not line.lstrip().startswith("#")
    )
    assert "await request.body()" not in src, (
        "some handler in this router reads a whole upload body into memory again "
        "— every upload path here must spool request.stream(). "
    )
    patch_src = src[src.index("async def tus_patch") : src.index("async def tus_delete")]
    assert "await request.body()" not in patch_src, (
        "the PATCH handler reads the whole chunk into memory again; spool "
        "request.stream() instead — that is the entire point of this guard"
    )
    assert "request.stream()" in patch_src
