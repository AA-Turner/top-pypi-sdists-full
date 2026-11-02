"""One block moved straight between a file and storage through a signed URL."""

from __future__ import annotations

import hashlib
import http.client
import os
import threading
from collections.abc import Callable, Mapping
from functools import partial
from pathlib import Path
from urllib.parse import urlsplit

from labqoat.volumes.block_window import BlockWindow
from labqoat.net.transport_trust import TransportTrust


class BlockTransfer:
    """Send or fetch exactly one block; a refusal or a digest mismatch is an error naming only host and status.

    Each thread keeps its connection to a storage host open between blocks: a volume of small files is one
    request per file, and a new TLS handshake for each would cost more than the bytes.
    """

    _open = threading.local()
    ATTEMPTS = 3
    TIMEOUT = 300.0
    CHUNK = 1024 * 1024

    @classmethod
    def put(cls, url: str, headers: Mapping[str, str], source: Path, offset: int, length: int) -> None:
        """Upload ``length`` bytes of ``source`` from ``offset``; the signed headers make storage check them."""
        cls._retried(partial(cls._put, url, headers, source, offset, length))

    @classmethod
    def get(cls, url: str, destination: Path, offset: int, digest: str) -> None:
        """Write the block at ``url`` into ``destination`` at ``offset``, refusing any other content."""
        cls._retried(partial(cls._get, url, destination, offset, digest))

    @classmethod
    def _retried(cls, transfer: Callable[[], None]) -> None:
        """Repeat a transfer that failed in transit; the last failure is the one raised."""
        attempt = 1
        while True:
            try:
                transfer()
                return
            except (OSError, http.client.HTTPException):
                cls._drop()
                if attempt == cls.ATTEMPTS:
                    raise
                attempt += 1

    @classmethod
    def _put(cls, url: str, headers: Mapping[str, str], source: Path, offset: int, length: int) -> None:
        """One PUT of the block's bytes, streamed from the file."""
        parsed = urlsplit(url)
        connection = cls._connection(parsed.scheme, str(parsed.hostname), parsed.port)
        with source.open("rb") as file:
            file.seek(offset)
            target = f"{parsed.path}?{parsed.query}"
            connection.request("PUT", target, body=BlockWindow(file, length), headers=dict(headers))
            response = connection.getresponse()
            response.read()
        cls._accepted(parsed.hostname, response.status)

    @classmethod
    def _get(cls, url: str, destination: Path, offset: int, digest: str) -> None:
        """One GET written at the block's offset while its digest is computed."""
        parsed = urlsplit(url)
        connection = cls._connection(parsed.scheme, str(parsed.hostname), parsed.port)
        connection.request("GET", f"{parsed.path}?{parsed.query}")
        response = connection.getresponse()
        if response.status != 200:
            response.read()
        cls._accepted(parsed.hostname, response.status)
        received = cls._receive(response, destination, offset)
        if received != digest:
            raise OSError(f"Volume block {digest} arrived with other content from {parsed.hostname}")

    @classmethod
    def _receive(cls, response: http.client.HTTPResponse, destination: Path, offset: int) -> str:
        """Write the body at ``offset`` and return its digest."""
        hashed = hashlib.sha256()
        descriptor = os.open(destination, os.O_WRONLY)
        try:
            while chunk := response.read(cls.CHUNK):
                hashed.update(chunk)
                os.pwrite(descriptor, chunk, offset)
                offset += len(chunk)
        finally:
            os.close(descriptor)
        return hashed.hexdigest()

    @staticmethod
    def _accepted(host: str | None, status: int) -> None:
        """Refuse anything but success, naming the storage host and status, never the signed URL."""
        if status not in (200, 201, 204):
            raise OSError(f"Volume storage at {host} answered HTTP {status}")

    @classmethod
    def _connection(cls, scheme: str, host: str, port: int | None) -> http.client.HTTPConnection:
        """This thread's open connection to the host, verified against the process's trust store."""
        held: dict[tuple[str, str, int | None], http.client.HTTPConnection] = cls._held()
        key = (scheme, host, port)
        if key not in held:
            held[key] = TransportTrust.connection(scheme, host, port, timeout=cls.TIMEOUT, blocksize=cls.CHUNK)
        return held[key]

    @classmethod
    def _held(cls) -> dict[tuple[str, str, int | None], http.client.HTTPConnection]:
        """The connections this thread keeps open."""
        if not hasattr(cls._open, "connections"):
            cls._open.connections = {}
        held: dict[tuple[str, str, int | None], http.client.HTTPConnection] = cls._open.connections
        return held

    @classmethod
    def _drop(cls) -> None:
        """Close this thread's connections after a failure, so a retry starts on a fresh one."""
        held = cls._held()
        for connection in held.values():
            connection.close()
        held.clear()
