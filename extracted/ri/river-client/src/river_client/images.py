"""Reusable image references and bounded asynchronous upload execution."""

from __future__ import annotations

import asyncio
import hashlib
import os
from pathlib import Path
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import uuid


@dataclass(frozen=True)
class ImageHandle:
    """Immutable metadata for an image owned by one live API session.

    Checkpoints retain bytes in a client-side ImageStore and re-upload on resume.
    """

    id: str
    sha256: str
    byte_count: int
    width: int
    height: int
    session_id: str

    def __post_init__(self):
        uuid.UUID(self.id)
        if not isinstance(self.session_id, str) or not self.session_id:
            raise ValueError("image session_id is required")
        if len(self.sha256) != 64 or any(
            c not in "0123456789abcdef" for c in self.sha256
        ):
            raise ValueError("invalid image digest")
        if min(self.byte_count, self.width, self.height) <= 0:
            raise ValueError("image size and dimensions must be positive")


Image = bytes | ImageHandle


class ImageUploads:
    """One event loop per client; bounded active RPCs and no executor backlog.

    Cancellation stops waiting, but a started upload completes with its original
    key. Its slot is held until the RPC actually ends, preventing cancellation
    from defeating concurrency bounds. The same key recovers the handle.
    """

    def __init__(self, client, concurrency: int):
        if (
            isinstance(concurrency, bool)
            or not isinstance(concurrency, int)
            or concurrency <= 0
        ):
            raise ValueError("image_upload_concurrency must be a positive integer")
        self.client = client
        self.concurrency = concurrency
        self.executor = ThreadPoolExecutor(
            max_workers=concurrency, thread_name_prefix="river-image"
        )
        self.loop = None
        self.slots = None
        self.closed = False

    async def run(self, call):
        loop = asyncio.get_running_loop()
        if self.closed:
            raise RuntimeError("image uploader is closed")
        if self.loop is None:
            self.loop = loop
            self.slots = asyncio.Queue()
            for stub in self.client._get_upload_stubs(self.concurrency):
                self.slots.put_nowait(stub)
        elif self.loop is not loop:
            raise RuntimeError(
                "a client's async image uploads must share one event loop"
            )
        stub = await self.slots.get()
        if self.closed:
            self.slots.put_nowait(stub)
            raise RuntimeError("image uploader is closed")
        try:
            future = loop.run_in_executor(
                self.executor,
                lambda: call(stub),
            )
        except BaseException:
            self.slots.put_nowait(stub)
            raise

        def completed(future):
            self.slots.put_nowait(stub)
            # A cancelled caller may no longer observe an upload failure.
            if not future.cancelled():
                future.exception()

        future.add_done_callback(completed)
        return await asyncio.shield(future)

    def close(self):
        self.closed = True
        self.executor.shutdown(wait=True)


class ImageStore:
    """Content-addressed image bytes on a local/shared durable filesystem."""

    def __init__(self, directory):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True, mode=0o700)

    def put(self, data):
        data = bytes(data)
        digest = hashlib.sha256(data).hexdigest()
        path = self.directory / digest
        if path.exists():
            if path.read_bytes() != data:
                raise ValueError("checkpoint image failed integrity verification")
            return digest
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(
                dir=self.directory, delete=False
            ) as stream:
                temporary = Path(stream.name)
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, path)
            descriptor = os.open(self.directory, os.O_RDONLY)
            try:
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
        return digest

    def read(self, image):
        try:
            data = (self.directory / image.sha256).read_bytes()
        except FileNotFoundError:
            raise ValueError(
                "checkpoint image bytes are missing; preserve the images directory with trainer state"
            ) from None
        if (
            len(data) != image.byte_count
            or hashlib.sha256(data).hexdigest() != image.sha256
        ):
            raise ValueError("checkpoint image failed integrity verification")
        return data

    def copy_images(self, value, source):
        handles = list(image_handles(value))
        for digest, image in {h.sha256: h for h in handles}.items():
            if (self.directory / digest).exists():
                self.read(image)
            elif source is None:
                raise ValueError(
                    "checkpointing image handles requires their local upload image store"
                )
            else:
                self.put(source.read(image))
        return {h.sha256 for h in handles}

    def prune(self, retained):
        # Only this checkpoint's latest atomically committed state owns these
        # files. Never prune the uploader cache, or another checkpoint directory.
        for path in self.directory.iterdir():
            if (
                path.is_file()
                and len(path.name) == 64
                and all(c in "0123456789abcdef" for c in path.name)
                and path.name not in retained
            ):
                path.unlink()


def image_handles(value):
    if isinstance(value, ImageHandle):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from image_handles(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from image_handles(item)


def map_images(value, replace):
    if isinstance(value, ImageHandle):
        return replace(value)
    if isinstance(value, dict):
        return {key: map_images(item, replace) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [map_images(item, replace) for item in value]
    return value
