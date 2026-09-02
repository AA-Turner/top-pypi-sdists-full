"""Tests for derive_context_id."""

import hashlib
from pathlib import Path

from agentic_devtools.cli.setup.registry import derive_context_id


class TestDeriveContextId:
    """Tests for derive_context_id."""

    def test_is_sixteen_hex_chars(self, tmp_path: Path) -> None:
        """The context id is 16 lowercase hex characters."""
        context_id = derive_context_id(tmp_path)
        assert len(context_id) == 16
        assert all(char in "0123456789abcdef" for char in context_id)

    def test_matches_sha256_of_canonical_path(self, tmp_path: Path) -> None:
        """The id equals the first 16 hex chars of SHA-256 of the canonical path."""
        expected = hashlib.sha256(str(tmp_path.resolve()).encode("utf-8")).hexdigest()[:16]
        assert derive_context_id(tmp_path) == expected

    def test_same_path_yields_same_id(self, tmp_path: Path) -> None:
        """Reruns for the same clone resolve to the same context id."""
        assert derive_context_id(tmp_path) == derive_context_id(tmp_path)

    def test_different_paths_yield_different_ids(self, tmp_path: Path) -> None:
        """Different clones at different paths produce distinct context ids."""
        repo_a = tmp_path / "a"
        repo_b = tmp_path / "b"
        repo_a.mkdir()
        repo_b.mkdir()
        assert derive_context_id(repo_a) != derive_context_id(repo_b)

    def test_resolves_symlinks_to_same_id(self, tmp_path: Path) -> None:
        """A symlink and its target resolve to the same canonical context id."""
        target = tmp_path / "real"
        target.mkdir()
        link = tmp_path / "link"
        link.symlink_to(target)
        assert derive_context_id(link) == derive_context_id(target)
