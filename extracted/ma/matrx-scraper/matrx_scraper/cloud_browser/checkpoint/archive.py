"""Streaming tar+zstd archive of a closed profile directory, with the exclusion
list that is part of ``PROFILE_FORMAT_VERSION`` (S3 §1, §3.1), and a path-safe
extractor (S3 §4/§5 V4).

The whole profile is never held in memory: the tar stream is written to a temp
file through a zstd compressor, and the plaintext SHA-256 + byte count are computed
over the compressed stream as it is produced.
"""

from __future__ import annotations

import hashlib
import os
import tarfile
from dataclasses import dataclass
from pathlib import Path

import zstandard

from .constants import (
    ARCHIVE_CHUNK_BYTES,
    ARCHIVE_EXCLUDE_NAMES,
    ARCHIVE_EXCLUDE_PREFIXES,
    ARCHIVE_EXCLUDE_SUFFIXES,
    EXPECTED_ARCHIVE_MEMBERS,
    ZSTD_LEVEL,
)
from .errors import CaptureError, VerificationError


@dataclass(frozen=True)
class ArchiveResult:
    path: Path
    plaintext_hash: str  # sha256 of the archive bytes (tar+zstd), lowercase hex
    plaintext_byte_count: int


def _is_excluded(rel_path: str) -> bool:
    """rel_path uses forward slashes, relative to the archive root."""
    name = rel_path.rsplit("/", 1)[-1]
    if name in ARCHIVE_EXCLUDE_NAMES:
        return True
    if any(name.endswith(s) for s in ARCHIVE_EXCLUDE_SUFFIXES):
        return True
    # A prefix like "Default/GPUCache/" matches the tree rooted there, whether the
    # path starts with it or contains it as a path segment ("/Default/GPUCache/…").
    padded = f"/{rel_path}"
    for prefix in ARCHIVE_EXCLUDE_PREFIXES:
        seg = prefix.rstrip("/")
        if (
            rel_path.startswith(prefix)
            or f"/{seg}/" in f"{padded}/"
            or padded.startswith(f"/{seg}/")
        ):
            return True
    return False


def archive_profile(profile_dir: Path, dest_path: Path) -> ArchiveResult:
    """Stream ``profile_dir`` into ``dest_path`` as tar+zstd, applying exclusions.

    ``dest_path`` is created mode 0600. External symlink targets are refused
    (ARCHIVE_FORMAT: no external symlink targets).
    """
    profile_dir = profile_dir.resolve()
    if not profile_dir.is_dir():
        raise CaptureError(f"profile dir not found: {profile_dir}", code="archive_failed")

    hasher = hashlib.sha256()
    total = 0

    # Open dest 0600.
    fd = os.open(dest_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        with os.fdopen(fd, "wb") as raw:

            class _HashingWriter:
                def write(self, data: bytes) -> int:
                    nonlocal total
                    hasher.update(data)
                    total += len(data)
                    raw.write(data)
                    return len(data)

            cctx = zstandard.ZstdCompressor(level=ZSTD_LEVEL)
            with cctx.stream_writer(_HashingWriter(), closefd=False) as zwriter:
                with tarfile.open(fileobj=zwriter, mode="w|", format=tarfile.PAX_FORMAT) as tar:
                    for entry in sorted(profile_dir.rglob("*")):
                        rel = entry.relative_to(profile_dir).as_posix()
                        if _is_excluded(rel):
                            continue
                        if entry.is_symlink():
                            target = os.readlink(entry)
                            resolved = (entry.parent / target).resolve()
                            if not str(resolved).startswith(str(profile_dir)):
                                raise CaptureError(
                                    f"external symlink target refused: {rel} -> {target}",
                                    code="archive_failed",
                                )
                            continue  # in-tree symlinks are dropped (regenerable)
                        if entry.is_dir():
                            continue  # directories implied by their members
                        if not entry.is_file():
                            continue
                        tar.add(entry, arcname=rel, recursive=False)
    except CaptureError:
        dest_path.unlink(missing_ok=True)
        raise
    except Exception as exc:
        dest_path.unlink(missing_ok=True)
        raise CaptureError(f"archive failed: {exc}", code="archive_failed") from exc

    return ArchiveResult(
        path=dest_path, plaintext_hash=hasher.hexdigest(), plaintext_byte_count=total
    )


def extract_archive(archive_path: Path, dest_dir: Path) -> None:
    """Extract a tar+zstd archive into ``dest_dir`` with path-safety enforced.

    No absolute members, no ``..``, no symlinks/hardlinks escaping the root.
    """
    dest_dir.mkdir(parents=True, exist_ok=True)
    os.chmod(dest_dir, 0o700)
    try:
        dctx = zstandard.ZstdDecompressor()
        with open(archive_path, "rb") as raw:
            with dctx.stream_reader(raw) as reader:
                with tarfile.open(fileobj=reader, mode="r|") as tar:
                    # streaming mode: filter+extract member-by-member
                    for member in tar:
                        if member.name.startswith("/") or ".." in Path(member.name).parts:
                            raise VerificationError(
                                f"unsafe archive member: {member.name!r}",
                                code="archive_unreadable",
                            )
                        if member.issym() or member.islnk():
                            raise VerificationError(
                                f"link member refused: {member.name!r}",
                                code="archive_unreadable",
                            )
                        target = (dest_dir / member.name).resolve()
                        if not str(target).startswith(str(dest_dir.resolve())):
                            raise VerificationError(
                                f"archive member escapes root: {member.name!r}",
                                code="archive_unreadable",
                            )
                        tar.extract(member, dest_dir, filter="data")
    except VerificationError:
        raise
    except Exception as exc:
        raise VerificationError(f"archive unreadable: {exc}", code="archive_unreadable") from exc


def assert_expected_members(dest_dir: Path) -> None:
    """V4 probe: the expected top-level members exist (S3 §5.2)."""
    for member in EXPECTED_ARCHIVE_MEMBERS:
        if not (dest_dir / member).exists():
            raise VerificationError(
                f"expected archive member missing after extract: {member!r}",
                code="archive_unreadable",
            )


def stream_size(path: Path, chunk: int = ARCHIVE_CHUNK_BYTES) -> int:
    return path.stat().st_size
