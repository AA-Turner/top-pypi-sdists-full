"""Pins the pure diff engine behind filesystem.sync().

sync() is one-way like ``rsync -r`` without deltas: list both sides, diff
on path/type/size/mtime (+sha256 with checksum=True), send the changed set
as ~50 MiB tar batches. These tests pin the engine's decisions against
plain data and tmpdir trees — no executor, no network.
"""

import io
import os
import sys
import tempfile
import unittest

from koyeb.sandbox.sync import (
    SyncDiff,
    build_archive,
    diff,
    excluded,
    extract_archive,
    format_mtime,
    hash_candidates,
    mtime_seconds,
    path_excluded,
    path_match,
    plan_batches,
    prune_descendants,
    relative_remote,
    walk_local,
)

PART = 50 * 1024 * 1024


def _entry(path, type_, size=0, mtime="2026-10-27T10:00:00Z", mode="0644"):
    return {
        "path": path,
        "type": type_,
        "size": size,
        "mtime": mtime,
        "mode": mode,
    }


class TestPathMatch(unittest.TestCase):
    """Go path.Match semantics: * and ? do not cross the / separator."""

    def test_literal(self):
        self.assertTrue(path_match("a.txt", "a.txt"))
        self.assertFalse(path_match("a.txt", "b.txt"))

    def test_star_does_not_cross_separator(self):
        self.assertTrue(path_match("*.py", "a.py"))
        self.assertFalse(path_match("*.py", "a/b.py"))

    def test_question_mark_single_nonslash(self):
        self.assertTrue(path_match("a?c", "abc"))
        self.assertFalse(path_match("a?c", "a/c"))

    def test_character_class(self):
        self.assertTrue(path_match("[a-c]x", "bx"))
        self.assertFalse(path_match("[a-c]x", "dx"))

    def test_star_matches_empty(self):
        self.assertTrue(path_match("a*", "a"))
        self.assertTrue(path_match("*", "anything"))

    def test_malformed_class_raises(self):
        # The executor answers 400 on a bad pattern; the walk mirrors that
        # by refusing to guess. Cross-checked against Go's path.Match.
        with self.assertRaises(ValueError):
            path_match("x[", "x")

    def test_trailing_escape_raises(self):
        # A lone trailing backslash escapes nothing; Go answers
        # ErrBadPattern for every candidate.
        with self.assertRaises(ValueError):
            path_match("a\\", "x")
        with self.assertRaises(ValueError):
            path_match("a\\", "aXY")

    def test_malformed_later_chunk_raises_on_earlier_mismatch(self):
        # Go validates the whole pattern before returning a match result:
        # an early mismatch with a malformed later chunk still errors.
        with self.assertRaises(ValueError):
            path_match("a*x[", "b")

    def test_single_unit_mismatch_is_not_a_match(self):
        # A chunk whose last unit mismatches is exhausted AND failed — the
        # verdict must come from the failure, not the chunk length. The
        # buggy reading matched a*b against b (Go: false).
        rows = [
            ("a*b", "b", False),
            ("a?b", "ab", False),
            ("ab", "b", False),
            ("*b", "b", True),
        ]
        for pattern, name, want in rows:
            self.assertEqual(
                path_match(pattern, name), want, f"{pattern!r} vs {name!r}"
            )

    def test_go_cross_checked_arms(self):
        # Every row verified against Go's path.Match on this machine.
        rows = [
            ("*", "a/b", False),
            ("a/*", "a/b/c", False),
            ("a/*/c", "a/b/c", True),
            ("a*b*c", "aXbYc", True),
            ("a*b*c", "a/b/c", False),
            ("sub/.git", ".git", False),
            ("*.log", "sub/a.log", False),
            # '!' is a literal class member in Go (no negation); '^' negates.
            ("[!a-c]x", "dx", False),
            ("[^a-c]x", "dx", True),
            # An escaped star is a chunk, not a split point.
            ("a\\*b", "a*b", True),
            ("a\\*b", "aXb", False),
            # An escaped class member is a literal, Go's \\ c rule.
            ("[\\]]", "]", True),
            ("[\\-]", "-", True),
            ("[\\-]", "x", False),
            ("", "x", False),
            ("", "", True),
        ]
        for pattern, name, want in rows:
            self.assertEqual(
                path_match(pattern, name), want, f"{pattern!r} vs {name!r}"
            )


class TestExcluded(unittest.TestCase):
    def test_direct_match(self):
        self.assertTrue(excluded("a.log", ["*.log"]))

    def test_suffix_match(self):
        self.assertTrue(excluded("sub/a.log", ["*.log"]))
        self.assertFalse(excluded("sub/a.txt", ["*.log"]))

    def test_no_match(self):
        self.assertFalse(excluded("a.txt", ["*.log"]))
        self.assertFalse(excluded("a/b/c.txt", ["*.log", "*.py"]))

    def test_multiple_patterns_any_match(self):
        self.assertTrue(excluded("a/b.py", ["*.log", "*.py"]))

    def test_directory_entry_matches_by_own_name(self):
        # The pruning rule: a dir entry matches, the walk never descends.
        self.assertTrue(excluded(".git", [".git"]))
        self.assertTrue(excluded("sub/.git", [".git"]))


class TestPathExcluded(unittest.TestCase):
    def test_own_path_match(self):
        self.assertTrue(path_excluded("skip.log", ["*.log"]))

    def test_ancestor_prefix_match(self):
        self.assertTrue(path_excluded("x/backup/small.txt", ["backup"]))

    def test_sibling_is_not_excluded(self):
        self.assertFalse(path_excluded("a/backup2/x", ["backup"]))

    def test_deep_non_match_is_not_excluded(self):
        self.assertFalse(path_excluded("x/y/z.txt", ["*.log"]))

    def test_class_pattern_matches_through_prefix(self):
        # A metachar pattern prunes same-named dirs via the class rule.
        self.assertTrue(path_excluded("data1/x", ["data[1]"]))


class TestMtimeFormat(unittest.TestCase):
    def test_nanoseconds_kept_and_trimmed(self):
        ns = 1774590000_123456789
        self.assertTrue(format_mtime(ns).endswith(".123456789Z"))
        self.assertTrue(format_mtime(1774590000_500000000).endswith(".5Z"))
        self.assertTrue(format_mtime(1774590000_000001000).endswith(".000001Z"))

    def test_zero_fraction_omitted(self):
        formatted = format_mtime(1774590000_000000000)
        self.assertTrue(formatted.endswith("Z"))
        self.assertNotIn(".", formatted)

    def test_mtime_seconds_floors(self):
        self.assertEqual(
            mtime_seconds("2026-10-27T10:00:00.123456789Z"),
            mtime_seconds("2026-10-27T10:00:00Z"),
        )
        self.assertEqual(
            mtime_seconds("2026-10-27T10:00:00.999Z"),
            mtime_seconds("2026-10-27T10:00:00Z"),
        )

    def test_round_trip(self):
        for ns in (1774590000_000000000, 1774590000_123456789, 1774590059_500000000):
            self.assertEqual(mtime_seconds(format_mtime(ns)), ns // 1_000_000_000)


class TestWalkLocal(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = self._tmp.name
        self.addCleanup(self._tmp.cleanup)

    def _make(self, rel, content=b"x"):
        path = os.path.join(self.root, *rel.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(content)
        return path

    def test_unreadable_subtree_raises_instead_of_dropping(self):
        # A silent subtree drop would push a remotely-wrong tree; the
        # walk refuses to guess, as it does for malformed patterns.
        if getattr(os, "geteuid", lambda: -1)() == 0:
            self.skipTest("root reads through chmod-000")
        if sys.platform == "win32":
            self.skipTest("chmod-000 is not a real barrier on Windows")
        self._make("visible.txt")
        locked = os.path.join(self.root, "locked")
        os.makedirs(locked)
        self._make("locked/inner.txt")
        os.chmod(locked, 0)
        self.addCleanup(os.chmod, locked, 0o755)

        with self.assertRaises(OSError):
            walk_local(self.root)

    def test_entries_in_fileentry_shape(self):
        self._make("a.txt", b"hello")
        os.makedirs(os.path.join(self.root, "sub"))
        self._make("sub/b.bin", b"12345")
        os.symlink("a.txt", os.path.join(self.root, "link.txt"))
        os.symlink("sub", os.path.join(self.root, "sublink"))

        entries = walk_local(self.root)

        by_path = {e["path"]: e for e in entries}
        self.assertEqual(
            sorted(by_path),
            ["a.txt", "link.txt", "sub", "sub/b.bin", "sublink"],
        )
        self.assertEqual(by_path["a.txt"]["type"], "file")
        self.assertEqual(by_path["a.txt"]["size"], 5)
        self.assertEqual(by_path["sub"]["type"], "dir")
        self.assertEqual(by_path["link.txt"]["type"], "symlink")
        self.assertEqual(by_path["link.txt"]["size"], len("a.txt"))
        # A symlinked dir is listed as a link, not descended into.
        self.assertEqual(by_path["sublink"]["type"], "symlink")
        # Every mtime parses back; modes are 4-digit octal perms.
        for entry in entries:
            mtime_seconds(entry["mtime"])
            self.assertRegex(entry["mode"], r"^[0-7]{4}$")

    def test_root_itself_is_not_an_entry(self):
        self._make("a.txt")
        entries = walk_local(self.root)
        self.assertEqual([e["path"] for e in entries], ["a.txt"])

    def test_special_files_skipped(self):
        self._make("a.txt")
        os.mkfifo(os.path.join(self.root, "pipe"))
        entries = walk_local(self.root)
        self.assertEqual([e["path"] for e in entries], ["a.txt"])

    def test_excluded_dir_skipped_whole(self):
        self._make("a.txt")
        self._make(".git/config")
        self._make("sub/c.txt")
        entries = walk_local(self.root, exclude=(".git",))
        self.assertEqual(
            sorted(e["path"] for e in entries), ["a.txt", "sub", "sub/c.txt"]
        )

    def test_excluded_file_by_suffix(self):
        self._make("a.py")
        self._make("sub/b.py")
        self._make("sub/c.txt")
        entries = walk_local(self.root, exclude=("*.py",))
        self.assertEqual(sorted(e["path"] for e in entries), ["sub", "sub/c.txt"])

    def test_mode_reflects_real_permissions(self):
        path = self._make("a.sh")
        os.chmod(path, 0o755)
        entry = walk_local(self.root)[0]
        self.assertEqual(entry["mode"], "0755")

    def test_mtime_reflects_file(self):
        path = self._make("a.txt")
        os.utime(path, ns=(1774590000_123456789, 1774590000_123456789))
        entry = walk_local(self.root)[0]
        self.assertEqual(mtime_seconds(entry["mtime"]), 1774590000)


class TestDiff(unittest.TestCase):
    def test_new_file_transfers(self):
        result = diff([_entry("a.txt", "file", 5)], [])
        self.assertEqual([e["path"] for e in result.to_transfer], ["a.txt"])
        self.assertEqual(result.bytes, 5)

    def test_identical_file_skipped(self):
        same = _entry("a.txt", "file", 5, mtime="2026-10-27T10:00:00.100Z")
        result = diff([same], [same])
        self.assertEqual(result.to_transfer, [])
        self.assertEqual(result.skipped, 1)

    def test_size_difference_transfers(self):
        result = diff([_entry("a.txt", "file", 5)], [_entry("a.txt", "file", 6)])
        self.assertEqual([e["path"] for e in result.to_transfer], ["a.txt"])

    def test_directory_size_difference_is_not_a_change(self):
        # A directory's st_size is a filesystem-format artifact (APFS
        # ~64, ext4 4096) that can never converge cross-filesystem.
        result = diff([_entry("d", "dir", 64)], [_entry("d", "dir", 4096)])
        self.assertEqual(result.to_transfer, [])
        self.assertEqual(result.skipped, 1)

    def test_mtime_difference_past_a_second_transfers(self):
        result = diff(
            [_entry("a.txt", "file", 5, mtime="2026-10-27T10:00:01Z")],
            [_entry("a.txt", "file", 5, mtime="2026-10-27T10:00:00Z")],
        )
        self.assertEqual([e["path"] for e in result.to_transfer], ["a.txt"])

    def test_mtime_difference_within_the_same_second_skips(self):
        # tar PAX mtime cannot round-trip nanoseconds; the diff is
        # whole-second like rsync's default.
        result = diff(
            [_entry("a.txt", "file", 5, mtime="2026-10-27T10:00:00.900Z")],
            [_entry("a.txt", "file", 5, mtime="2026-10-27T10:00:00.100Z")],
        )
        self.assertEqual(result.to_transfer, [])
        self.assertEqual(result.skipped, 1)

    def test_type_change_transfers(self):
        result = diff([_entry("a", "dir")], [_entry("a", "file", 5)])
        self.assertEqual([e["path"] for e in result.to_transfer], ["a"])

    def test_symlink_target_change_caught_by_size(self):
        result = diff(
            [_entry("l", "symlink", size=7)], [_entry("l", "symlink", size=3)]
        )
        self.assertEqual([e["path"] for e in result.to_transfer], ["l"])

    def test_remote_only_skipped_without_delete(self):
        result = diff([], [_entry("gone.txt", "file", 5)])
        self.assertEqual(result.to_transfer, [])
        self.assertEqual(result.deletes, [])
        self.assertEqual(result.skipped, 1)

    def test_remote_only_deleted_with_delete(self):
        result = diff([], [_entry("gone.txt", "file", 5)], delete=True)
        self.assertEqual([e["path"] for e in result.deletes], ["gone.txt"])
        self.assertEqual(result.skipped, 0)

    def test_remote_error_entry_skipped(self):
        result = diff(
            [_entry("a.txt", "file", 5)],
            [{"path": "a.txt", "error": "permission denied"}],
        )
        # Cannot prove unchanged: an unreadable entry is not a transfer
        # candidate, it is skipped.
        self.assertEqual(result.to_transfer, [])
        self.assertEqual(result.skipped, 1)

    def test_remote_other_type_skipped(self):
        result = diff([], [_entry("dev", "other")])
        self.assertEqual(result.skipped, 1)
        self.assertEqual(result.deletes, [])

    def test_local_other_type_skipped(self):
        result = diff([_entry("dev", "other")], [])
        self.assertEqual(result.to_transfer, [])
        self.assertEqual(result.skipped, 1)

    def test_unarchivable_pair_is_never_a_delete(self):
        # Both sides have an unarchivable entry at the same path: the
        # source cannot replace it, so the destination must keep it.
        result = diff(
            [_entry("dev", "other")],
            [_entry("dev", "other")],
            delete=True,
        )
        self.assertEqual(result.deletes, [])
        self.assertEqual(result.skipped, 1)

    def test_checksum_hashes_only_matching_files(self):
        same = _entry("a.txt", "file", 5)
        local_calls = []
        remote_calls = []

        def local_hash(path):
            local_calls.append(path)
            return "aa"

        def remote_hash(path):
            remote_calls.append(path)
            return "aa"

        result = diff(
            [same, _entry("b.txt", "file", 5, mtime="2026-10-27T10:00:01Z")],
            [same, _entry("b.txt", "file", 5, mtime="2026-10-27T10:00:00Z")],
            local_hash=local_hash,
            remote_hash=remote_hash,
        )
        self.assertEqual(local_calls, ["a.txt"])
        self.assertEqual(remote_calls, ["a.txt"])
        # b.txt differs by mtime, so it transfers without any hashing.
        self.assertEqual([e["path"] for e in result.to_transfer], ["b.txt"])

    def test_checksum_mismatch_transfers(self):
        same = _entry("a.txt", "file", 5)
        result = diff(
            [same],
            [same],
            local_hash=lambda p: "aa",
            remote_hash=lambda p: "bb",
        )
        self.assertEqual([e["path"] for e in result.to_transfer], ["a.txt"])

    def test_checksum_none_remote_hash_skips(self):
        same = _entry("a.txt", "file", 5)
        result = diff(
            [same],
            [same],
            local_hash=lambda p: "aa",
            remote_hash=lambda p: None,
        )
        self.assertEqual(result.to_transfer, [])
        self.assertEqual(result.skipped, 1)

    def test_bytes_sum_file_sizes_only(self):
        result = diff(
            [
                _entry("a.txt", "file", 5),
                _entry("d", "dir"),
                _entry("l", "symlink", size=3),
            ],
            [],
        )
        self.assertEqual(result.bytes, 5)

    def test_dir_mtime_difference_transfers(self):
        result = diff(
            [_entry("d", "dir", mtime="2026-10-27T10:00:05Z")],
            [_entry("d", "dir", mtime="2026-10-27T10:00:00Z")],
        )
        self.assertEqual([e["path"] for e in result.to_transfer], ["d"])

    def test_hash_candidates_are_only_matching_files(self):
        from koyeb.sandbox.sync import hash_candidates

        same = _entry("same.txt", "file", 5)
        candidates = hash_candidates(
            [
                same,
                _entry("changed.txt", "file", 5, mtime="2026-10-27T10:00:01Z"),
                _entry("resized.txt", "file", 6),
                _entry("new.txt", "file", 5),
                _entry("d", "dir"),
                _entry("l", "symlink", size=3),
            ],
            [
                same,
                _entry("changed.txt", "file", 5, mtime="2026-10-27T10:00:00Z"),
                _entry("resized.txt", "file", 5),
                _entry("d", "dir"),
                _entry("l", "symlink", size=3),
            ],
        )
        self.assertEqual(candidates, ["same.txt"])


class TestPlanBatches(unittest.TestCase):
    def test_greedy_fill_within_part_size(self):
        entries = [
            _entry("a", "file", 20),
            _entry("b", "file", 20),
            _entry("c", "file", 20),
        ]
        batches, oversized = plan_batches(entries, part_size=50)
        self.assertEqual([[e["path"] for e in b] for b in batches], [["a", "b"], ["c"]])
        self.assertEqual(oversized, [])

    def test_file_never_split(self):
        entries = [_entry("a", "file", 30), _entry("b", "file", 30)]
        batches, oversized = plan_batches(entries, part_size=50)
        self.assertEqual([[e["path"] for e in b] for b in batches], [["a"], ["b"]])

    def test_file_equal_to_part_size_is_not_oversized(self):
        entries = [_entry("a", "file", 50)]
        batches, oversized = plan_batches(entries, part_size=50)
        self.assertEqual(len(batches), 1)
        self.assertEqual(oversized, [])

    def test_oversized_file_separated(self):
        entries = [
            _entry("big", "file", 51),
            _entry("small", "file", 10),
        ]
        batches, oversized = plan_batches(entries, part_size=50)
        self.assertEqual([[e["path"] for e in b] for b in batches], [["small"]])
        self.assertEqual([e["path"] for e in oversized], ["big"])

    def test_dirs_and_symlinks_ride_batches(self):
        entries = [_entry("d", "dir"), _entry("l", "symlink"), _entry("a", "file", 10)]
        batches, oversized = plan_batches(entries, part_size=50)
        self.assertEqual([[e["path"] for e in b] for b in batches], [["d", "l", "a"]])

    def test_only_dirs_yields_one_batch(self):
        entries = [_entry("d", "dir"), _entry("d/e", "dir")]
        batches, oversized = plan_batches(entries, part_size=50)
        self.assertEqual([[e["path"] for e in b] for b in batches], [["d", "d/e"]])
        self.assertEqual(oversized, [])

    def test_empty_input(self):
        batches, oversized = plan_batches([], part_size=50)
        self.assertEqual(batches, [])
        self.assertEqual(oversized, [])


class TestPruneDescendants(unittest.TestCase):
    def test_descendants_of_kept_root_dropped(self):
        self.assertEqual(prune_descendants(["a", "a/b", "a/b/c", "d"]), ["a", "d"])

    def test_unsorted_input_prunes_to_topmost(self):
        self.assertEqual(prune_descendants(["a/b", "a"]), ["a"])

    def test_no_descendants_unchanged(self):
        self.assertEqual(prune_descendants(["a", "b/c"]), ["a", "b/c"])


class TestRelativeRemote(unittest.TestCase):
    def test_relative_path_kept(self):
        self.assertEqual(relative_remote("project"), "project")
        self.assertEqual(relative_remote("a/b"), "a/b")

    def test_dot_prefix_normalized(self):
        self.assertEqual(relative_remote("./project"), "project")

    def test_absolute_path_takes_basename(self):
        self.assertEqual(relative_remote("/home/dev/project"), "project")

    def test_trailing_slash_normalized(self):
        self.assertEqual(relative_remote("project/"), "project")


class TestSyncDiffShape(unittest.TestCase):
    def test_fields(self):
        result = diff([_entry("a", "file", 1)], [])
        self.assertIsInstance(result, SyncDiff)
        self.assertEqual(result.bytes, 1)
        self.assertEqual(result.deletes, [])
        self.assertEqual(result.skipped, 0)


class TestBuildExtractArchive(unittest.TestCase):
    """Round-trip the tar batches through the real engine: what sync() sends
    is what the executor will extract, and what sync() extracts locally is
    what the executor streamed."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = self._tmp.name
        self.addCleanup(self._tmp.cleanup)
        self.src = os.path.join(self.root, "src")
        self.dst = os.path.join(self.root, "dst")
        self.archive = os.path.join(self.root, "batch.tgz")
        os.makedirs(self.src)
        os.makedirs(self.dst)

    def _tree(self):
        with open(os.path.join(self.src, "a.txt"), "wb") as f:
            f.write(b"hello")
        os.chmod(os.path.join(self.src, "a.txt"), 0o755)
        os.utime(
            os.path.join(self.src, "a.txt"),
            ns=(1774590000_123456789, 1774590000_123456789),
        )
        os.makedirs(os.path.join(self.src, "sub"))
        with open(os.path.join(self.src, "sub", "b.bin"), "wb") as f:
            f.write(b"\x00\xff")
        os.symlink("a.txt", os.path.join(self.src, "link"))
        os.makedirs(os.path.join(self.src, "empty"))
        return walk_local(self.src)

    def test_round_trip_preserves_everything(self):
        entries = self._tree()
        build_archive(self.src, entries, self.archive)
        extracted = extract_archive(self.archive, self.dst)

        self.assertEqual(
            sorted(extracted), ["a.txt", "empty", "link", "sub", "sub/b.bin"]
        )
        with open(os.path.join(self.dst, "a.txt"), "rb") as f:
            self.assertEqual(f.read(), b"hello")
        self.assertEqual(
            oct(os.stat(os.path.join(self.dst, "a.txt")).st_mode & 0o7777),
            oct(0o755),
        )
        self.assertEqual(
            os.stat(os.path.join(self.dst, "a.txt")).st_mtime_ns // 1_000_000_000,
            1774590000,
        )
        with open(os.path.join(self.dst, "sub", "b.bin"), "rb") as f:
            self.assertEqual(f.read(), b"\x00\xff")
        self.assertTrue(os.path.islink(os.path.join(self.dst, "link")))
        self.assertEqual(os.readlink(os.path.join(self.dst, "link")), "a.txt")
        self.assertTrue(os.path.isdir(os.path.join(self.dst, "empty")))

    def test_extraction_replaces_existing_members(self):
        entries = self._tree()
        with open(os.path.join(self.dst, "a.txt"), "wb") as f:
            f.write(b"stale")
        build_archive(self.src, entries, self.archive)
        extract_archive(self.archive, self.dst)
        with open(os.path.join(self.dst, "a.txt"), "rb") as f:
            self.assertEqual(f.read(), b"hello")

    def test_file_member_replaces_in_the_way_dir(self):
        entries = self._tree()
        os.makedirs(os.path.join(self.dst, "a.txt"))
        with open(os.path.join(self.dst, "a.txt", "stale"), "wb") as f:
            f.write(b"stale")
        build_archive(self.src, entries, self.archive)
        extract_archive(self.archive, self.dst)
        with open(os.path.join(self.dst, "a.txt"), "rb") as f:
            self.assertEqual(f.read(), b"hello")

    def test_dir_member_replaces_in_the_way_file(self):
        entries = self._tree()
        with open(os.path.join(self.dst, "sub"), "wb") as f:
            f.write(b"stale")
        build_archive(self.src, entries, self.archive)
        extract_archive(self.archive, self.dst)
        self.assertTrue(os.path.isdir(os.path.join(self.dst, "sub")))
        with open(os.path.join(self.dst, "sub", "b.bin"), "rb") as f:
            self.assertEqual(f.read(), b"\x00\xff")

    def test_dir_member_replaces_symlink_without_following_it(self):
        # Following a symlinked dir would write members outside the
        # destination; the member must replace the link itself.
        entries = self._tree()
        outside = os.path.join(self.root, "outside")
        os.makedirs(outside)
        os.symlink(outside, os.path.join(self.dst, "sub"))
        build_archive(self.src, entries, self.archive)
        extract_archive(self.archive, self.dst)
        sub = os.path.join(self.dst, "sub")
        self.assertTrue(os.path.isdir(sub))
        self.assertFalse(os.path.islink(sub))
        with open(os.path.join(sub, "b.bin"), "rb") as f:
            self.assertEqual(f.read(), b"\x00\xff")
        self.assertEqual(os.listdir(outside), [])

    def test_keep_filter_extracts_only_changed_set(self):
        entries = self._tree()
        # A local tree that already has everything but b.bin.
        with open(os.path.join(self.dst, "a.txt"), "wb") as f:
            f.write(b"old-content")
        build_archive(self.src, entries, self.archive)
        keep = {"sub", "sub/b.bin"}
        extracted = extract_archive(self.archive, self.dst, keep=keep)

        self.assertEqual(sorted(extracted), ["sub", "sub/b.bin"])
        with open(os.path.join(self.dst, "a.txt"), "rb") as f:
            self.assertEqual(f.read(), b"old-content")
        with open(os.path.join(self.dst, "sub", "b.bin"), "rb") as f:
            self.assertEqual(f.read(), b"\x00\xff")

    def test_traversal_members_refused(self):
        import tarfile

        with tarfile.open(self.archive, "w:gz") as tar:
            info = tarfile.TarInfo("../evil.txt")
            info.size = 2
            tar.addfile(info, io.BytesIO(b"hi"))

        with self.assertRaises(ValueError):
            extract_archive(self.archive, self.dst)

    def test_absolute_members_refused(self):
        import tarfile

        with tarfile.open(self.archive, "w:gz") as tar:
            info = tarfile.TarInfo("/etc/evil.txt")
            info.size = 2
            tar.addfile(info, io.BytesIO(b"hi"))

        with self.assertRaises(ValueError):
            extract_archive(self.archive, self.dst)

    def _raw_archive(self, *members):
        """Write an archive of (name, kind, payload) members as sent."""
        import tarfile

        with tarfile.open(self.archive, "w:gz") as tar:
            for name, kind, payload in members:
                info = tarfile.TarInfo(name)
                if kind == "dir":
                    info.type = tarfile.DIRTYPE
                    info.mode = payload
                    tar.addfile(info)
                elif kind == "sym":
                    info.type = tarfile.SYMTYPE
                    info.linkname = payload
                    tar.addfile(info)
                else:
                    info.size = len(payload)
                    tar.addfile(info, io.BytesIO(payload))

    def _outside(self):
        outside = os.path.join(self.root, "outside")
        os.makedirs(outside)
        os.chmod(outside, 0o755)
        return outside

    def test_member_through_symlink_member_refused(self):
        outside = self._outside()
        self._raw_archive(("a", "sym", outside), ("a/evil.txt", "file", b"hi"))

        with self.assertRaises(ValueError):
            extract_archive(self.archive, self.dst)
        self.assertEqual(os.listdir(outside), [])

    def test_member_through_existing_symlink_refused(self):
        outside = self._outside()
        os.symlink(outside, os.path.join(self.dst, "a"))
        self._raw_archive(("a/sub", "dir", 0o755), ("a/sub/evil.txt", "file", b"hi"))

        with self.assertRaises(ValueError):
            extract_archive(self.archive, self.dst)
        self.assertEqual(os.listdir(outside), [])

    def test_file_member_replaces_symlink_without_following(self):
        outside = self._outside()
        victim = os.path.join(outside, "victim.txt")
        with open(victim, "wb") as f:
            f.write(b"keep")
        os.symlink(victim, os.path.join(self.dst, "a.txt"))
        self._raw_archive(("a.txt", "file", b"new"))

        extract_archive(self.archive, self.dst)

        with open(victim, "rb") as f:
            self.assertEqual(f.read(), b"keep")
        self.assertFalse(os.path.islink(os.path.join(self.dst, "a.txt")))

    def test_dir_mode_not_applied_through_later_symlink(self):
        outside = self._outside()
        self._raw_archive(("d", "dir", 0o700), ("d", "sym", outside))

        extract_archive(self.archive, self.dst)

        self.assertEqual(os.stat(outside).st_mode & 0o777, 0o755)

    def test_symlink_members_kept_as_sent(self):
        # Links are data, like rsync -l: kept, never written through.
        self._raw_archive(("abs", "sym", "/usr/bin/python3"), ("rel", "sym", "../up"))

        extract_archive(self.archive, self.dst)

        self.assertEqual(os.readlink(os.path.join(self.dst, "abs")), "/usr/bin/python3")
        self.assertEqual(os.readlink(os.path.join(self.dst, "rel")), "../up")


if __name__ == "__main__":
    unittest.main()
