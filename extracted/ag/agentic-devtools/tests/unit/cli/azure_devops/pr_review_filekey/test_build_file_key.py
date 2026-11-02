"""Tests for build_file_key."""

import hashlib

from agentic_devtools.cli.azure_devops.pr_review_filekey import build_file_key


class TestBuildFileKey:
    """Tests for the build_file_key function."""

    def test_basic_path_has_slug_and_hash(self):
        """A basic path produces a readable slug plus an 8-char hex suffix."""
        key = build_file_key("src/app/component.ts")
        slug, _, digest = key.rpartition("-")
        assert slug == "src-app-component-ts"
        assert len(digest) == 8
        assert all(c in "0123456789abcdef" for c in digest)

    def test_hash_matches_case_preserved_normalized_path(self):
        """The hash is computed over the case-preserved normalized path."""
        expected = hashlib.sha256(b"src/app/component.ts").hexdigest()[:8]
        key = build_file_key("/src/app/component.ts")
        assert key.endswith(expected)

    def test_leading_slash_and_backslashes_normalized(self):
        """Leading slashes and backslashes do not change the key."""
        assert build_file_key("/src/a.ts") == build_file_key("src/a.ts")
        assert build_file_key("src\\a.ts") == build_file_key("src/a.ts")

    def test_stable_for_same_path(self):
        """Same path always yields the same key."""
        assert build_file_key("src/a.ts") == build_file_key("src/a.ts")

    def test_different_paths_differ(self):
        """Different paths yield different keys."""
        assert build_file_key("src/a.ts") != build_file_key("src/b.ts")

    def test_case_only_difference_is_collision_safe(self):
        """Paths differing only in case share a slug but differ by hash suffix.

        This is the Windows case-insensitive-safety guarantee: the readable slug
        collides, but the full key does not, so the on-disk filenames are distinct.
        """
        upper = build_file_key("src/Foo.ts")
        lower = build_file_key("src/foo.ts")
        assert upper != lower
        # Slugs (everything before the hash) are identical.
        assert upper.rpartition("-")[0] == lower.rpartition("-")[0]

    def test_empty_path_uses_fallback_slug(self):
        """An empty path falls back to the 'file' slug with the empty-string hash."""
        expected = hashlib.sha256(b"").hexdigest()[:8]
        key = build_file_key("")
        assert key == f"file-{expected}"

    def test_whitespace_only_path_uses_fallback_slug(self):
        """A whitespace/slash-only path falls back to the 'file' slug."""
        key = build_file_key("  ///  ")
        assert key.startswith("file-")

    def test_special_characters_replaced(self):
        """Special characters collapse into single hyphens in the slug."""
        key = build_file_key("src/my file (v2).ts")
        slug = key.rpartition("-")[0]
        assert slug == "src-my-file-v2-ts"
        assert "--" not in slug

    def test_long_path_slug_truncated(self):
        """Very long paths have their slug truncated but keep a full hash."""
        long_path = "src/" + "/".join(f"segment{i}" for i in range(40)) + "/file.ts"
        key = build_file_key(long_path)
        slug, _, digest = key.rpartition("-")
        assert len(slug) <= 60
        assert len(digest) == 8
        assert not slug.endswith("-")

    def test_reserved_windows_name_is_disambiguated(self):
        """A path whose slug equals a reserved Windows device name stays safe.

        The hash suffix means the base filename is never exactly 'con', so it is
        not treated as a reserved device name by Windows.
        """
        key = build_file_key("con")
        assert key.startswith("con-")
        assert key != "con"
