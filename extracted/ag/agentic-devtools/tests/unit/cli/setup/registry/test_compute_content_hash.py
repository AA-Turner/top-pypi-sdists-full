"""Tests for compute_content_hash."""

import hashlib
from pathlib import Path

from agentic_devtools.cli.setup.registry import compute_content_hash


class TestComputeContentHash:
    """Tests for compute_content_hash."""

    def test_matches_hashlib_for_small_file(self, tmp_path: Path) -> None:
        """The digest matches hashlib.sha256 of the file bytes."""
        target = tmp_path / "cert.pem"
        target.write_bytes(b"-----BEGIN CERT-----\nabc\n")
        assert compute_content_hash(target) == hashlib.sha256(target.read_bytes()).hexdigest()

    def test_empty_file_hashes_to_sha256_of_empty(self, tmp_path: Path) -> None:
        """An empty file hashes to the SHA-256 of the empty byte string."""
        target = tmp_path / "empty"
        target.write_bytes(b"")
        assert compute_content_hash(target) == hashlib.sha256(b"").hexdigest()

    def test_reads_multi_chunk_file_correctly(self, tmp_path: Path) -> None:
        """A file larger than the chunk size is hashed correctly across chunks."""
        target = tmp_path / "big.bin"
        payload = b"x" * (65536 * 2 + 17)
        target.write_bytes(payload)
        assert compute_content_hash(target) == hashlib.sha256(payload).hexdigest()

    def test_identical_content_yields_identical_hash(self, tmp_path: Path) -> None:
        """Two files with identical content produce identical hashes (dedup key)."""
        first = tmp_path / "a"
        second = tmp_path / "b"
        first.write_bytes(b"same")
        second.write_bytes(b"same")
        assert compute_content_hash(first) == compute_content_hash(second)
