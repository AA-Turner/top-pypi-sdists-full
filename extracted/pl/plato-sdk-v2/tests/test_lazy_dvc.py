"""Unit tests for plato.worlds.lazy_dvc — DVCManifestEntry, DVCManifest, and smart_commit."""

import hashlib
import json
import os
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from plato.chronos.models import DVCManifestEntry
from plato.worlds.dvc_models import DVCManifest, LazyDVCMount, S3Config, smart_commit

# ---------------------------------------------------------------------------
# DVCManifestEntry serialization
# ---------------------------------------------------------------------------


class TestDVCManifestEntry:
    def test_regular_file(self):
        entry = DVCManifestEntry(relpath="readme.md", md5="def456", size=50)
        d = entry.model_dump(exclude_none=True)
        assert d == {"relpath": "readme.md", "md5": "def456", "size": 50}
        assert "isexec" not in d
        assert "islink" not in d

    def test_executable_file(self):
        entry = DVCManifestEntry(relpath="bin/run.sh", md5="aaa", size=30, isexec=True)
        d = entry.model_dump(exclude_none=True)
        assert d["isexec"] is True
        assert "islink" not in d

    def test_symlink(self):
        entry = DVCManifestEntry(
            relpath="node_modules/.bin/tsc",
            md5="bbb",
            size=20,
            islink=True,
            symlink_target="../typescript/bin/tsc",
        )
        d = entry.model_dump(exclude_none=True)
        assert d["islink"] is True
        assert d["symlink_target"] == "../typescript/bin/tsc"
        assert "isexec" not in d

    def test_symlink_no_target(self):
        entry = DVCManifestEntry(relpath="link", md5="ccc", size=0, islink=True)
        d = entry.model_dump(exclude_none=True)
        assert d["islink"] is True
        assert "symlink_target" not in d

    def test_from_dict_regular(self):
        entry = DVCManifestEntry(**{"relpath": "a.txt", "md5": "abc", "size": 10})
        assert entry.relpath == "a.txt"
        assert entry.md5 == "abc"
        assert entry.size == 10
        assert entry.islink is None
        assert entry.isexec is None

    def test_from_dict_executable(self):
        entry = DVCManifestEntry(**{"relpath": "run.sh", "md5": "x", "size": 5, "isexec": True})
        assert entry.isexec is True

    def test_from_dict_symlink(self):
        entry = DVCManifestEntry(
            **{"relpath": "link", "md5": "y", "size": 8, "islink": True, "symlink_target": "../target"}
        )
        assert entry.islink is True
        assert entry.symlink_target == "../target"

    def test_round_trip_regular(self):
        original = DVCManifestEntry(relpath="file.txt", md5="abc", size=100)
        restored = DVCManifestEntry(**original.model_dump(exclude_none=True))
        assert restored.relpath == original.relpath
        assert restored.md5 == original.md5
        assert restored.size == original.size

    def test_round_trip_executable(self):
        original = DVCManifestEntry(relpath="run.sh", md5="x", size=50, isexec=True)
        restored = DVCManifestEntry(**original.model_dump(exclude_none=True))
        assert restored.isexec is True

    def test_round_trip_symlink(self):
        original = DVCManifestEntry(relpath="link.js", md5="z", size=12, islink=True, symlink_target="../real.js")
        d = original.model_dump(exclude_none=True)
        assert "isexec" not in d
        restored = DVCManifestEntry(**d)
        assert restored.islink is True
        assert restored.symlink_target == "../real.js"

    def test_missing_size_defaults_none(self):
        entry = DVCManifestEntry(**{"relpath": "a", "md5": "b"})
        assert entry.size is None

    def test_no_symlink_target_defaults_none(self):
        entry = DVCManifestEntry(**{"relpath": "a", "md5": "b", "islink": True})
        assert entry.islink is True
        assert entry.symlink_target is None


# ---------------------------------------------------------------------------
# DVCManifest round-trip
# ---------------------------------------------------------------------------


class TestDVCManifest:
    def test_manifest_round_trip_mixed_entries(self):
        entries = [
            DVCManifestEntry(relpath="a.txt", md5="aaa", size=10),
            DVCManifestEntry(relpath="b.sh", md5="bbb", size=20, isexec=True),
            DVCManifestEntry(relpath="c.link", md5="ccc", size=5, islink=True, symlink_target="./real"),
        ]
        manifest = DVCManifest(entries_list=entries, manifest_md5="m123")
        d = manifest.to_dict()
        restored = DVCManifest.from_dict(d)

        assert len(restored.entries_list) == 3
        assert restored.manifest_md5 == "m123"

        by_relpath = {e.relpath: e for e in restored.entries_list}
        assert not by_relpath["a.txt"].islink
        assert by_relpath["b.sh"].isexec is True
        assert by_relpath["c.link"].islink is True
        assert by_relpath["c.link"].symlink_target == "./real"

    def test_entries_dict(self):
        entries = [
            DVCManifestEntry(relpath="x", md5="1", size=1),
            DVCManifestEntry(relpath="y", md5="2", size=2),
        ]
        manifest = DVCManifest(entries_list=entries, manifest_md5="m")
        d = manifest.entries_dict()
        assert set(d.keys()) == {"x", "y"}
        assert d["x"].md5 == "1"

    @pytest.mark.asyncio
    async def test_from_dvc_file_parses_manifest(self):
        s3_config = S3Config(
            bucket="test-bucket",
            prefix="test-prefix",
            credentials={"AWS_ACCESS_KEY_ID": "fake", "AWS_SECRET_ACCESS_KEY": "fake"},
        )
        dvc_content = "outs:\n- md5: deadbeef.dir\n"
        manifest_items = [
            {"relpath": "data.bin", "md5": "aa11", "size": 42},
            {"relpath": "link.txt", "md5": "bb22", "size": 9, "islink": True, "symlink_target": "../target"},
            {"relpath": "known.txt", "md5": "cc33", "size": 7},
        ]

        with patch(
            "plato.worlds.dvc_models.s3_download_bytes",
            new=AsyncMock(return_value=json.dumps(manifest_items).encode()),
        ):
            manifest = await DVCManifest.from_dvc_file(dvc_content, s3_config)

        by_relpath = manifest.entries_dict()
        assert by_relpath["data.bin"].size == 42
        assert by_relpath["link.txt"].islink is True
        assert by_relpath["link.txt"].symlink_target == "../target"
        assert by_relpath["known.txt"].size == 7


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

        original = DVCManifest(
            entries_list=[DVCManifestEntry(relpath="file.txt", md5="orig_md5", size=5)],
            manifest_md5="orig_manifest",
        )
        (mountpoint / "file.txt").write_text("hello")

        link_dir = overlay_dir / "links"
        link_dir.mkdir()
        os.symlink("../file.txt", link_dir / "ref.txt")

        meta = {"modified": [], "deleted": [], "created": ["links/ref.txt"]}
        (cache_dir / "meta.json").write_text(json.dumps(meta))

        mount = LazyDVCMount(mountpoint=mountpoint, cache_dir=cache_dir, manifest=original, worker_proc=None)

        uploaded: dict[str, bytes] = {}

        async def mock_upload(config, key, data):
            uploaded[key] = data

        async def mock_batch_upload(config, uploads):
            for local_path, key in uploads:
                uploaded[key] = Path(local_path).read_bytes()

        async def mock_download(config, key):
            return uploaded[key]

        with (
            patch("plato.worlds.dvc_models.s3_upload_bytes", side_effect=mock_upload),
            patch("plato.worlds.dvc_models.s3_upload_batch", side_effect=mock_batch_upload),
            patch("plato.worlds.dvc_models.s3_download_bytes", side_effect=mock_download),
        ):
            manifest_md5, dvc_yaml = await smart_commit(mount, s3_config)

        manifest_key = f"{s3_config.cache_prefix}/{manifest_md5[:2]}/{manifest_md5[2:]}.dir"
        assert manifest_key in uploaded

        entries = json.loads(uploaded[manifest_key])
        by_relpath = {e["relpath"]: e for e in entries}

        assert "file.txt" in by_relpath
        assert by_relpath["file.txt"]["md5"] == "orig_md5"

        assert "links/ref.txt" in by_relpath
        link_entry = by_relpath["links/ref.txt"]
        assert link_entry["islink"] is True
        assert link_entry["symlink_target"] == "../file.txt"
        expected_md5 = hashlib.md5(b"../file.txt").hexdigest()
        assert link_entry["md5"] == expected_md5

    @pytest.mark.asyncio
    async def test_smart_commit_modified_to_symlink(self, s3_config, mount_dir):
        """A regular file that was replaced by a symlink in the overlay."""
        tmp_path, cache_dir, overlay_dir, mountpoint = mount_dir

        original = DVCManifest(
            entries_list=[DVCManifestEntry(relpath="config.json", md5="old_md5", size=100)],
            manifest_md5="orig",
        )

        os.symlink("defaults/config.json", overlay_dir / "config.json")

        meta = {"modified": ["config.json"], "deleted": [], "created": []}
        (cache_dir / "meta.json").write_text(json.dumps(meta))

        mount = LazyDVCMount(mountpoint=mountpoint, cache_dir=cache_dir, manifest=original, worker_proc=None)

        uploaded: dict[str, bytes] = {}

        async def mock_upload(config, key, data):
            uploaded[key] = data

        async def mock_batch_upload(config, uploads):
            for local_path, key in uploads:
                uploaded[key] = Path(local_path).read_bytes()

        async def mock_download(config, key):
            return uploaded[key]

        with (
            patch("plato.worlds.dvc_models.s3_upload_bytes", side_effect=mock_upload),
            patch("plato.worlds.dvc_models.s3_upload_batch", side_effect=mock_batch_upload),
            patch("plato.worlds.dvc_models.s3_download_bytes", side_effect=mock_download),
        ):
            await smart_commit(mount, s3_config)

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
            entries_list=[DVCManifestEntry(relpath="run.sh", md5="old", size=10, isexec=True)],
            manifest_md5="orig",
        )
        (mountpoint / "run.sh").write_text("#!/bin/sh\necho hi\n")

        meta = {"modified": [], "deleted": [], "created": []}
        (cache_dir / "meta.json").write_text(json.dumps(meta))

        mount = LazyDVCMount(mountpoint=mountpoint, cache_dir=cache_dir, manifest=original, worker_proc=None)

        uploaded: dict[str, bytes] = {}

        async def mock_upload(config, key, data):
            uploaded[key] = data

        async def mock_download(config, key):
            return uploaded[key]

        with (
            patch("plato.worlds.dvc_models.s3_upload_bytes", side_effect=mock_upload),
            patch("plato.worlds.dvc_models.s3_download_bytes", side_effect=mock_download),
        ):
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

        async def mock_batch_upload(config, uploads):
            for local_path, key in uploads:
                uploaded[key] = Path(local_path).read_bytes()

        async def mock_download(config, key):
            return uploaded[key]

        with (
            patch("plato.worlds.dvc_models.s3_upload_bytes", side_effect=mock_upload),
            patch("plato.worlds.dvc_models.s3_upload_batch", side_effect=mock_batch_upload),
            patch("plato.worlds.dvc_models.s3_download_bytes", side_effect=mock_download),
        ):
            await smart_commit(mount, s3_config)

        for key, data in uploaded.items():
            if key.endswith(".dir"):
                entries = json.loads(data)
                assert len(entries) == 1
                assert "islink" not in entries[0]
                assert entries[0]["md5"] == hashlib.md5(b"hello").hexdigest()
                break


class TestPlatoFuseBinarySelection:
    @pytest.mark.asyncio
    async def test_ensure_plato_fuse_honors_env_override(self, tmp_path, monkeypatch):
        from plato.worlds import lazy_dvc

        binary_path = tmp_path / "plato-fuse"
        binary_path.write_text("binary")
        binary_path.chmod(0o755)

        monkeypatch.setenv("PLATO_FUSE_BINARY", str(binary_path))
        monkeypatch.setattr(lazy_dvc.shutil, "which", lambda _: None)

        binary = await lazy_dvc._ensure_plato_fuse()
        assert binary == str(binary_path)

    @pytest.mark.asyncio
    async def test_ensure_plato_fuse_finds_on_path(self, monkeypatch):
        from plato.worlds import lazy_dvc

        monkeypatch.setattr(lazy_dvc.shutil, "which", lambda _: "/usr/local/bin/plato-fuse")

        binary = await lazy_dvc._ensure_plato_fuse()
        assert binary == "/usr/local/bin/plato-fuse"
