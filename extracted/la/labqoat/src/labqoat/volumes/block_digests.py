"""How a volume names file content: one SHA-256 digest per 64 MiB block."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import BinaryIO, ClassVar


class BlockDigests:
    """Read a file once and name each of its blocks; every block is full but the last."""

    BLOCK_BYTES: ClassVar[int] = 64 * 1024 * 1024
    READ_BYTES: ClassVar[int] = 8 * 1024 * 1024

    @classmethod
    def of(cls, path: Path) -> tuple[int, tuple[str, ...]]:
        """Return the size read and the block digests, both of exactly the bytes read."""
        digests: list[str] = []
        size = 0
        with path.open("rb") as source:
            while (block := cls._block(source)) is not None:
                length, digest = block
                size += length
                digests.append(digest)
                if length < cls.BLOCK_BYTES:
                    break
        return size, tuple(digests)

    @classmethod
    def _block(cls, source: BinaryIO) -> tuple[int, str] | None:
        """Hash the next block, or nothing at the end of the file."""
        digest = hashlib.sha256()
        length = 0
        while length < cls.BLOCK_BYTES and (chunk := source.read(min(cls.READ_BYTES, cls.BLOCK_BYTES - length))):
            digest.update(chunk)
            length += len(chunk)
        return (length, digest.hexdigest()) if length else None
