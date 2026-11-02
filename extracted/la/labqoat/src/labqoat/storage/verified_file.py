"""Content verification and safe logical paths for workflow files."""

import hashlib
from pathlib import Path, PurePosixPath


class VerifiedFile:
    """Enforce exact-byte identities and safe relative file names."""

    @staticmethod
    def digest(path: Path) -> str:
        """Hash file bytes through a bounded streaming read."""
        with path.open("rb") as stream:
            return hashlib.file_digest(stream, "sha256").hexdigest()

    @staticmethod
    def validate(path: Path, digest: str, byte_size: int) -> Path:
        """Require the expected byte length and SHA-256 digest."""
        if path.stat().st_size != byte_size or VerifiedFile.digest(path) != digest:
            raise ValueError("Asset bytes do not match their immutable identity")
        return path

    @staticmethod
    def relative(name: str) -> PurePosixPath:
        """Reject traversal, absolute names, and ambiguous path spellings."""
        path = PurePosixPath(name)
        if not name or path.is_absolute() or str(path) != name:
            raise ValueError("Expected a canonical relative file path")
        if ".." in path.parts or "\\" in name or "\x00" in name or name == ".":
            raise ValueError("Unsafe relative file path")
        return path
