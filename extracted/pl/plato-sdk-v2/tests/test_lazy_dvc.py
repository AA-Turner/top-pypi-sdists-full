"""Unit tests for plato.worlds.lazy_dvc — DVCFileEntry, DVCManifest, and smart_commit."""

import hashlib
import json
import os
from unittest.mock import patch

import pytest

from plato.worlds.dvc_models import DVCFileEntry, DVCManifest, LazyDVCMount, S3Config, smart_commit

# ---------------------------------------------------------------------------
# DVCFileEntry round-trip
# ---------------------------------------------------------------------------


class TestDVCFileEntry:
    def test_regular_file_defaults(self):
        entry = DVCFileEntry(relpath="src/main.py", md5="abc123", size=100)
        assert entry.mode == 0o644
        assert entry.is_symlink is False
        assert entry.symlink_target == ""

    def test_regular_file_to_dict(self):
        entry = DVCFileEntry(relpath="readme.md", md5="def456", size=50)
        d = entry.to_dict()
        assert d == {"relpath": "readme.md", "md5": "def456", "size": 50}
        assert "isexec" not in d
        assert "islink" not in d

    def test_executable_file_to_dict(self):
        entry = DVCFileEntry(relpath="bin/run.sh", md5="aaa", size=30, mode=0o755)
        d = entry.to_dict()
        assert d["isexec"] is True
        assert "islink" not in d

    def test_symlink_to_dict(self):
        entry = DVCFileEntry(
            relpath="node_modules/.bin/tsc",
            md5="bbb",
            size=20,
            mode=0o777,
            is_symlink=True,
            symlink_target="../typescript/bin/tsc",
        )
        d = entry.to_dict()
        assert d["islink"] is True
        assert d["symlink_target"] == "../typescript/bin/tsc"

    def test_symlink_to_dict_no_isexec(self):
        """Symlinks with mode 0o777 must NOT emit isexec."""
        entry = DVCFileEntry(
            relpath="link",
            md5="aaa",
            size=5,
            mode=0o777,
            is_symlink=True,
            symlink_target="target",
        )
        d = entry.to_dict()
        assert "isexec" not in d
        assert d["islink"] is True

    def test_symlink_no_target_to_dict(self):
        entry = DVCFileEntry(relpath="link", md5="ccc", size=0, is_symlink=True)
        d = entry.to_dict()
        assert d["islink"] is True
        assert "symlink_target" not in d

    def test_from_dict_regular(self):
        d = {"relpath": "a.txt", "md5": "abc", "size": 10}
        entry = DVCFileEntry.from_dict(d)
        assert entry.relpath == "a.txt"
        assert entry.md5 == "abc"
        assert entry.size == 10
        assert entry.mode == 0o644
        assert entry.is_symlink is False
        assert entry.symlink_target == ""

    def test_from_dict_executable(self):
        d = {"relpath": "run.sh", "md5": "x", "size": 5, "isexec": True}
        entry = DVCFileEntry.from_dict(d)
        assert entry.mode == 0o755

    def test_from_dict_symlink(self):
        d = {"relpath": "link", "md5": "y", "size": 8, "islink": True, "symlink_target": "../target"}
        entry = DVCFileEntry.from_dict(d)
        assert entry.is_symlink is True
        assert entry.symlink_target == "../target"
        assert entry.mode == 0o644  # symlink mode comes from manifest, not isexec

    def test_round_trip_regular(self):
        original = DVCFileEntry(relpath="file.txt", md5="abc", size=100)
        restored = DVCFileEntry.from_dict(original.to_dict())
        assert restored.relpath == original.relpath
        assert restored.md5 == original.md5
        assert restored.size == original.size
        assert restored.is_symlink == original.is_symlink

    def test_round_trip_executable(self):
        original = DVCFileEntry(relpath="run.sh", md5="x", size=50, mode=0o755)
        restored = DVCFileEntry.from_dict(original.to_dict())
        assert restored.mode == 0o755

    def test_round_trip_symlink(self):
        original = DVCFileEntry(
            relpath="link.js",
            md5="z",
            size=12,
            mode=0o777,
            is_symlink=True,
            symlink_target="../real.js",
        )
        d = original.to_dict()
        assert "isexec" not in d  # symlinks must not get isexec
        restored = DVCFileEntry.from_dict(d)
        assert restored.is_symlink is True
        assert restored.symlink_target == "../real.js"
        # mode round-trips as 0o644 (default for non-exec) — FUSE layer
        # hardcodes 0o777 for symlinks via _make_attrs, so this is fine
        assert restored.mode == 0o644

    def test_from_dict_missing_size_defaults_zero(self):
        d = {"relpath": "a", "md5": "b"}
        assert DVCFileEntry.from_dict(d).size == 0

    def test_from_dict_no_symlink_target_defaults_empty(self):
        d = {"relpath": "a", "md5": "b", "islink": True}
        entry = DVCFileEntry.from_dict(d)
        assert entry.is_symlink is True
        assert entry.symlink_target == ""


# ---------------------------------------------------------------------------
# DVCManifest round-trip
# ---------------------------------------------------------------------------


class TestDVCManifest:
    def test_manifest_round_trip_mixed_entries(self):
        entries = [
            DVCFileEntry(relpath="a.txt", md5="aaa", size=10),
            DVCFileEntry(relpath="b.sh", md5="bbb", size=20, mode=0o755),
            DVCFileEntry(
                relpath="c.link",
                md5="ccc",
                size=5,
                is_symlink=True,
                symlink_target="./real",
            ),
        ]
        manifest = DVCManifest(entries_list=entries, manifest_md5="m123")
        d = manifest.to_dict()
        restored = DVCManifest.from_dict(d)

        assert len(restored.entries_list) == 3
        assert restored.manifest_md5 == "m123"

        by_relpath = {e.relpath: e for e in restored.entries_list}
        assert not by_relpath["a.txt"].is_symlink
        assert by_relpath["b.sh"].mode == 0o755
        assert by_relpath["c.link"].is_symlink
        assert by_relpath["c.link"].symlink_target == "./real"

    def test_entries_dict(self):
        entries = [
            DVCFileEntry(relpath="x", md5="1", size=1),
            DVCFileEntry(relpath="y", md5="2", size=2),
        ]
        manifest = DVCManifest(entries_list=entries, manifest_md5="m")
        d = manifest.entries_dict()
        assert set(d.keys()) == {"x", "y"}
        assert d["x"].md5 == "1"


# ---------------------------------------------------------------------------
# smart_commit with symlinks
# ---------------------------------------------------------------------------


class TestSmartCommitSymlinks:
    @pytest.fixture
    def s3_config(self):
        return S3Config(
            bucket="test-bucket",
            prefix="test-prefix",
            credentials={"AWS_ACCESS_KEY_ID": "fake", "AWS_SECRET_ACCESS_KEY": "fake"},
        )

    @pytest.fixture
    def mount_dir(self, tmp_path):
        cache_dir = tmp_path / "cache"
        overlay_dir = cache_dir / "overlay"
        overlay_dir.mkdir(parents=True)
        mountpoint = tmp_path / "mount"
        mountpoint.mkdir()
        return tmp_path, cache_dir, overlay_dir, mountpoint

    @pytest.mark.asyncio
    async def test_smart_commit_creates_symlink_entry(self, s3_config, mount_dir):
        tmp_path, cache_dir, overlay_dir, mountpoint = mount_dir

        # Set up a manifest with one regular file
        original = DVCManifest(
            entries_list=[DVCFileEntry(relpath="file.txt", md5="orig_md5", size=5)],
            manifest_md5="orig_manifest",
        )

        # Create a new symlink in the overlay
        link_dir = overlay_dir / "links"
        link_dir.mkdir()
        os.symlink("../file.txt", link_dir / "ref.txt")

        # Write meta.json indicating the symlink was created
        meta = {"modified": [], "deleted": [], "created": ["links/ref.txt"]}
        (cache_dir / "meta.json").write_text(json.dumps(meta))

        mount = LazyDVCMount(
            mountpoint=mountpoint,
            cache_dir=cache_dir,
            manifest=original,
            worker_proc=None,
        )

        uploaded: dict[str, bytes] = {}

        async def mock_upload(config, key, data):
            uploaded[key] = data

        with patch("plato.worlds.dvc_models.s3_upload_bytes", side_effect=mock_upload):
            manifest_md5, dvc_yaml = await smart_commit(mount, s3_config)

        # The manifest should have been uploaded
        manifest_key = f"{s3_config.cache_prefix}/{manifest_md5[:2]}/{manifest_md5[2:]}.dir"
        assert manifest_key in uploaded

        # Parse the uploaded manifest
        entries = json.loads(uploaded[manifest_key])
        by_relpath = {e["relpath"]: e for e in entries}

        # Original file should be preserved
        assert "file.txt" in by_relpath
        assert by_relpath["file.txt"]["md5"] == "orig_md5"

        # Symlink should appear with islink flag
        assert "links/ref.txt" in by_relpath
        link_entry = by_relpath["links/ref.txt"]
        assert link_entry["islink"] is True
        assert link_entry["symlink_target"] == "../file.txt"
        # MD5 should be of the target string, not the file contents
        expected_md5 = hashlib.md5(b"../file.txt").hexdigest()
        assert link_entry["md5"] == expected_md5

    @pytest.mark.asyncio
    async def test_smart_commit_modified_to_symlink(self, s3_config, mount_dir):
        """A regular file that was replaced by a symlink in the overlay."""
        tmp_path, cache_dir, overlay_dir, mountpoint = mount_dir

        original = DVCManifest(
            entries_list=[DVCFileEntry(relpath="config.json", md5="old_md5", size=100)],
            manifest_md5="orig",
        )

        # Replace with a symlink in overlay
        os.symlink("defaults/config.json", overlay_dir / "config.json")

        meta = {"modified": ["config.json"], "deleted": [], "created": []}
        (cache_dir / "meta.json").write_text(json.dumps(meta))

        mount = LazyDVCMount(mountpoint=mountpoint, cache_dir=cache_dir, manifest=original, worker_proc=None)

        uploaded: dict[str, bytes] = {}

        async def mock_upload(config, key, data):
            uploaded[key] = data

        with patch("plato.worlds.dvc_models.s3_upload_bytes", side_effect=mock_upload):
            await smart_commit(mount, s3_config)

        # Find the manifest in uploads
        manifest_entries = None
        for key, data in uploaded.items():
            if key.endswith(".dir"):
                manifest_entries = json.loads(data)
                break

        assert manifest_entries is not None
        entry = manifest_entries[0]
        assert entry["relpath"] == "config.json"
        assert entry["islink"] is True
        assert entry["symlink_target"] == "defaults/config.json"

    @pytest.mark.asyncio
    async def test_smart_commit_preserves_executable_mode(self, s3_config, mount_dir):
        tmp_path, cache_dir, overlay_dir, mountpoint = mount_dir

        original = DVCManifest(
            entries_list=[DVCFileEntry(relpath="run.sh", md5="old", size=10, mode=0o755)],
            manifest_md5="orig",
        )

        # Untouched file — should preserve mode in manifest
        meta = {"modified": [], "deleted": [], "created": []}
        (cache_dir / "meta.json").write_text(json.dumps(meta))

        mount = LazyDVCMount(mountpoint=mountpoint, cache_dir=cache_dir, manifest=original, worker_proc=None)

        uploaded: dict[str, bytes] = {}

        async def mock_upload(config, key, data):
            uploaded[key] = data

        with patch("plato.worlds.dvc_models.s3_upload_bytes", side_effect=mock_upload):
            await smart_commit(mount, s3_config)

        for key, data in uploaded.items():
            if key.endswith(".dir"):
                entries = json.loads(data)
                assert entries[0]["isexec"] is True
                break

    @pytest.mark.asyncio
    async def test_smart_commit_regular_file_overlay(self, s3_config, mount_dir):
        """A new regular file in the overlay should NOT have islink."""
        tmp_path, cache_dir, overlay_dir, mountpoint = mount_dir

        original = DVCManifest(entries_list=[], manifest_md5="empty")

        (overlay_dir / "new.txt").write_text("hello")

        meta = {"modified": [], "deleted": [], "created": ["new.txt"]}
        (cache_dir / "meta.json").write_text(json.dumps(meta))

        mount = LazyDVCMount(mountpoint=mountpoint, cache_dir=cache_dir, manifest=original, worker_proc=None)

        uploaded: dict[str, bytes] = {}

        async def mock_upload(config, key, data):
            uploaded[key] = data

        with patch("plato.worlds.dvc_models.s3_upload_bytes", side_effect=mock_upload):
            await smart_commit(mount, s3_config)

        for key, data in uploaded.items():
            if key.endswith(".dir"):
                entries = json.loads(data)
                assert len(entries) == 1
                assert "islink" not in entries[0]
                assert entries[0]["md5"] == hashlib.md5(b"hello").hexdigest()
                break
