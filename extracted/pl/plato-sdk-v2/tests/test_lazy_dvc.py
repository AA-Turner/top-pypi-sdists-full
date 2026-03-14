"""Unit tests for plato.worlds.lazy_dvc — DVCManifestEntry, DVCManifest, and smart_commit."""

import hashlib
import json
import os
import shutil
import subprocess
from collections.abc import Callable
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
import tenacity

from plato.chronos.models import DVCManifestEntry
from plato.worlds.dvc_models import DVCManifest, LazyDVCMount, S3Config, smart_commit
from plato.worlds.lazy_dvc import mount_lazy, unmount_lazy

SDK_ROOT = Path(__file__).resolve().parents[1]
PLATO_FUSE_ROOT = SDK_ROOT / "plato-fuse"
PLATO_FUSE_DEBUG_BINARY = PLATO_FUSE_ROOT / "target" / "debug" / "plato-fuse"
HAS_LOCAL_FUSE = Path("/dev/fuse").exists() and shutil.which("fusermount3") is not None
DUMMY_AWS_CREDENTIALS = {
    "AWS_DEFAULT_REGION": "us-east-1",
    "AWS_ACCESS_KEY_ID": "test-access-key",
    "AWS_SECRET_ACCESS_KEY": "test-secret-key",
    "AWS_SESSION_TOKEN": "test-session-token",
}


@pytest.fixture(scope="session")
def local_plato_fuse_binary(tmp_path_factory: pytest.TempPathFactory) -> Path:
    if not HAS_LOCAL_FUSE:
        pytest.skip("local FUSE support is unavailable")
    target_dir = tmp_path_factory.mktemp("plato-fuse-target")
    env = dict(os.environ)
    env["CARGO_TARGET_DIR"] = str(target_dir)
    subprocess.run(["cargo", "build", "-q"], cwd=PLATO_FUSE_ROOT, check=True, env=env)
    binary = target_dir / "debug" / "plato-fuse"
    assert binary.is_file()
    return binary


@pytest.fixture
def local_fuse_s3_config() -> S3Config:
    return S3Config(
        bucket="test-bucket",
        prefix="test-prefix",
        credentials=dict(DUMMY_AWS_CREDENTIALS),
    )


@pytest.fixture
def local_fuse_mount_dir(tmp_path):
    cache_dir = tmp_path / "cache"
    overlay_dir = cache_dir / "overlay"
    overlay_dir.mkdir(parents=True)
    mountpoint = tmp_path / "mount"
    mountpoint.mkdir()
    return tmp_path, cache_dir, overlay_dir, mountpoint


def _retry_assert(assertion: Callable[[], None]) -> None:
    for attempt in tenacity.Retrying(
        stop=tenacity.stop_after_delay(5),
        wait=tenacity.wait_fixed(0.05),
        reraise=True,
    ):
        with attempt:
            assertion()


def _write_smart_commit_meta(
    cache_dir: Path,
    *,
    directories: list[dict[str, int]] | None = None,
    dir_renames: list[dict[str, str]] | None = None,
) -> None:
    meta: dict[str, object] = {
        "modified": [],
        "deleted": [],
        "created": [],
    }
    if directories is not None:
        meta["directories"] = directories
    if dir_renames is not None:
        meta["dir_renames"] = dir_renames
    (cache_dir / "meta.json").write_text(json.dumps(meta))


def _write_cached_file(cache_dir: Path, relpath: str, data: bytes) -> None:
    cache_path = cache_dir / "cache" / relpath
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_bytes(data)


async def _smart_commit_with_mocked_s3(mount: LazyDVCMount, s3_config: S3Config) -> tuple[str, str, list[dict]]:
    uploaded: dict[str, bytes] = {}

    async def mock_upload(_config: S3Config, key: str, data: bytes) -> None:
        uploaded[key] = data

    async def mock_batch_upload(_config: S3Config, uploads: list[tuple[str, str]]) -> None:
        for local_path, key in uploads:
            uploaded[key] = Path(local_path).read_bytes()

    async def mock_download(_config: S3Config, key: str) -> bytes:
        return uploaded[key]

    with (
        patch("plato.worlds.dvc_models.s3_upload_bytes", side_effect=mock_upload),
        patch("plato.worlds.dvc_models.s3_upload_batch", side_effect=mock_batch_upload),
        patch("plato.worlds.dvc_models.s3_download_bytes", side_effect=mock_download),
    ):
        manifest_md5, dvc_yaml = await smart_commit(mount, s3_config)

    manifest_entries = json.loads(next(data for key, data in uploaded.items() if key.endswith(".dir")))
    return manifest_md5, dvc_yaml, manifest_entries


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

    def test_directory_to_dict(self):
        entry = DVCManifestEntry(relpath="runtime/postgres", mode=0o750, isdir=True)
        d = entry.model_dump(exclude_none=True)
        assert d == {"relpath": "runtime/postgres", "isdir": True, "mode": 0o750}
        assert "md5" not in d
        assert "size" not in d
        assert "isexec" not in d
        assert "islink" not in d

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

    def test_from_dict_directory(self):
        d = {"relpath": "runtime/postgres", "isdir": True, "mode": 0o700}
        entry = DVCManifestEntry(**d)
        assert entry.isdir is True
        assert entry.mode == 0o700
        assert entry.md5 is None
        assert (entry.size or 0) == 0

    def test_from_dict_directory_defaults_mode_for_backward_compatibility(self):
        d = {"relpath": "runtime/postgres", "isdir": True}
        entry = DVCManifestEntry(**d)
        assert entry.isdir is True

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

    def test_round_trip_directory(self):
        original = DVCManifestEntry(relpath="runtime/postgres/data", mode=0o750, isdir=True)
        restored = DVCManifestEntry(**original.model_dump(exclude_none=True))
        assert restored.isdir is True
        assert restored.mode == 0o750
        assert restored.relpath == "runtime/postgres/data"

    def test_missing_size_defaults_none(self):
        entry = DVCManifestEntry(**{"relpath": "a", "md5": "b"})
        assert entry.size is None

    def test_no_symlink_target_defaults_none(self):
        entry = DVCManifestEntry(**{"relpath": "a", "md5": "b", "islink": True})
        assert entry.islink is True
        assert entry.symlink_target is None

    def test_directory_to_dict_round_trip_short_form(self):
        entry = DVCManifestEntry(relpath="runtime/postgres", mode=0o750, isdir=True)
        assert entry.model_dump(exclude_none=True) == {"relpath": "runtime/postgres", "isdir": True, "mode": 0o750}

    def test_directory_from_dict_defaults_mode(self):
        entry = DVCManifestEntry(**{"relpath": "runtime/postgres", "isdir": True})
        assert entry.isdir is True
        assert entry.md5 is None


# ---------------------------------------------------------------------------
# DVCManifest round-trip
# ---------------------------------------------------------------------------


class TestDVCManifest:
    def test_manifest_round_trip_mixed_entries(self):
        entries = [
            DVCManifestEntry(relpath="subdir", mode=0o750, isdir=True),
            DVCManifestEntry(relpath="a.txt", md5="aaa", size=10),
            DVCManifestEntry(relpath="b.sh", md5="bbb", size=20, isexec=True),
            DVCManifestEntry(
                relpath="c.link",
                md5="ccc",
                size=5,
                islink=True,
                symlink_target="./real",
            ),
        ]
        manifest = DVCManifest(entries_list=entries, manifest_md5="m123")
        d = manifest.to_dict()
        restored = DVCManifest.from_dict(d)

        assert len(restored.entries_list) == 4
        assert restored.manifest_md5 == "m123"

        by_relpath = {e.relpath: e for e in restored.entries_list}
        assert by_relpath["subdir"].isdir
        assert by_relpath["subdir"].mode == 0o750
        assert not by_relpath["a.txt"].islink
        assert by_relpath["b.sh"].isexec is True
        assert by_relpath["c.link"].islink is True
        assert by_relpath["c.link"].symlink_target == "./real"

    def test_manifest_from_dict_reads_old_file_only_entries(self):
        manifest = DVCManifest.from_dict(
            {
                "entries": [
                    {"relpath": "script.sh", "md5": "abc", "size": 12, "isexec": True},
                    {"relpath": "link", "md5": "def", "size": 4, "islink": True, "symlink_target": "target"},
                ],
                "manifest_md5": "old",
            }
        )

        by_relpath = manifest.entries_dict()
        assert by_relpath["script.sh"].isexec is True
        assert by_relpath["link"].islink is True

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
            {"relpath": "runtime", "isdir": True, "mode": 0o750},
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
        assert by_relpath["runtime"].isdir is True
        assert by_relpath["data.bin"].size == 42
        assert by_relpath["link.txt"].islink is True
        assert by_relpath["link.txt"].symlink_target == "../target"
        assert by_relpath["known.txt"].size == 7

    @pytest.mark.asyncio
    async def test_from_dvc_file_resolves_symlink_target_from_s3(self):
        s3_config = S3Config(
            bucket="test-bucket",
            prefix="test-prefix",
            credentials={"AWS_ACCESS_KEY_ID": "fake", "AWS_SECRET_ACCESS_KEY": "fake"},
        )
        dvc_content = "outs:\n- md5: deadbeef.dir\n"
        manifest_items = [
            {"relpath": "link-no-target", "md5": "aa11", "size": 0, "islink": True},
        ]
        symlink_target_content = b"../real-target.txt"

        call_count = 0

        async def mock_s3_download(_config, key):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return json.dumps(manifest_items).encode()
            return symlink_target_content

        with patch(
            "plato.worlds.dvc_models.s3_download_bytes",
            new=AsyncMock(side_effect=mock_s3_download),
        ):
            manifest = await DVCManifest.from_dvc_file(dvc_content, s3_config)

        entry = manifest.entries_dict()["link-no-target"]
        assert entry.islink is True
        assert entry.symlink_target == "../real-target.txt"
        assert entry.size == len(symlink_target_content)

    @pytest.mark.asyncio
    async def test_from_dvc_file_symlink_target_s3_download_fails_gracefully(self):
        s3_config = S3Config(
            bucket="test-bucket",
            prefix="test-prefix",
            credentials={"AWS_ACCESS_KEY_ID": "fake", "AWS_SECRET_ACCESS_KEY": "fake"},
        )
        dvc_content = "outs:\n- md5: deadbeef.dir\n"
        manifest_items = [
            {"relpath": "broken-link", "md5": "aa11", "size": 0, "islink": True},
        ]

        call_count = 0

        async def mock_s3_download(_config, key):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return json.dumps(manifest_items).encode()
            raise RuntimeError("S3 not available")

        with patch(
            "plato.worlds.dvc_models.s3_download_bytes",
            new=AsyncMock(side_effect=mock_s3_download),
        ):
            manifest = await DVCManifest.from_dvc_file(dvc_content, s3_config)

        entry = manifest.entries_dict()["broken-link"]
        assert entry.islink is True
        assert entry.symlink_target is None
        assert (entry.size or 0) == 0

    @pytest.mark.asyncio
    async def test_from_dvc_file_symlink_no_md5_no_target(self):
        """Symlink with no md5 and no target should just get size=0."""
        s3_config = S3Config(
            bucket="test-bucket",
            prefix="test-prefix",
            credentials={"AWS_ACCESS_KEY_ID": "fake", "AWS_SECRET_ACCESS_KEY": "fake"},
        )
        dvc_content = "outs:\n- md5: deadbeef.dir\n"
        manifest_items = [
            {"relpath": "no-md5-link", "size": 0, "islink": True},
        ]

        with patch(
            "plato.worlds.dvc_models.s3_download_bytes",
            new=AsyncMock(return_value=json.dumps(manifest_items).encode()),
        ):
            manifest = await DVCManifest.from_dvc_file(dvc_content, s3_config)

        entry = manifest.entries_dict()["no-md5-link"]
        assert entry.islink is True
        assert entry.symlink_target is None
        assert (entry.size or 0) == 0

    @pytest.mark.asyncio
    async def test_from_dvc_file_parses_legacy_file_only_manifest(self):
        s3_config = S3Config(
            bucket="test-bucket",
            prefix="test-prefix",
            credentials={"AWS_ACCESS_KEY_ID": "fake", "AWS_SECRET_ACCESS_KEY": "fake"},
        )
        dvc_content = "outs:\n- md5: deadbeef.dir\n"
        manifest_items = [{"relpath": "known.bin", "md5": "aa11", "size": 99}]

        with patch(
            "plato.worlds.dvc_models.s3_download_bytes",
            new=AsyncMock(return_value=json.dumps(manifest_items).encode()),
        ):
            manifest = await DVCManifest.from_dvc_file(dvc_content, s3_config)

        assert manifest.entries_list == [DVCManifestEntry(relpath="known.bin", md5="aa11", size=99)]

    @pytest.mark.asyncio
    async def test_from_dvc_file_keeps_zero_size_when_s3_object_missing(self):
        s3_config = S3Config(
            bucket="test-bucket",
            prefix="test-prefix",
            credentials={"AWS_ACCESS_KEY_ID": "fake", "AWS_SECRET_ACCESS_KEY": "fake"},
        )
        dvc_content = "outs:\n- md5: deadbeef.dir\n"
        manifest_items = [{"relpath": "missing.bin", "md5": "aa11", "size": 0}]

        with (
            patch(
                "plato.worlds.dvc_models.s3_download_bytes",
                new=AsyncMock(return_value=json.dumps(manifest_items).encode()),
            ),
            patch(
                "plato.worlds.dvc_models.s3_head_size",
                new=AsyncMock(side_effect=FileNotFoundError("missing")),
            ),
        ):
            manifest = await DVCManifest.from_dvc_file(dvc_content, s3_config)

        assert (manifest.entries_list[0].size or 0) == 0

    @pytest.mark.asyncio
    async def test_from_dvc_file_skips_head_for_existing_sizes(self):
        s3_config = S3Config(
            bucket="test-bucket",
            prefix="test-prefix",
            credentials={"AWS_ACCESS_KEY_ID": "fake", "AWS_SECRET_ACCESS_KEY": "fake"},
        )
        dvc_content = "outs:\n- md5: deadbeef.dir\n"
        manifest_items = [{"relpath": "known.bin", "md5": "aa11", "size": 99}]

        with (
            patch(
                "plato.worlds.dvc_models.s3_download_bytes",
                new=AsyncMock(return_value=json.dumps(manifest_items).encode()),
            ),
            patch(
                "plato.worlds.dvc_models.s3_head_size",
                new=AsyncMock(),
            ) as mock_head,
        ):
            manifest = await DVCManifest.from_dvc_file(dvc_content, s3_config)

        assert manifest.entries_list[0].size == 99
        mock_head.assert_not_awaited()


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

    @pytest.mark.asyncio
    async def test_smart_commit_emits_directory_entries_and_excludes_them_from_nfiles(self, s3_config, mount_dir):
        _tmp_path, cache_dir, overlay_dir, mountpoint = mount_dir

        original = DVCManifest(
            entries_list=[DVCManifestEntry(relpath="file.txt", md5="orig_md5", size=5)],
            manifest_md5="orig",
        )
        (mountpoint / "file.txt").write_text("hello")
        runtime_dir = mountpoint / ".runtime" / "postgres" / "data"
        runtime_dir.mkdir(parents=True)
        runtime_dir.chmod(0o750)

        mount = LazyDVCMount(mountpoint=mountpoint, cache_dir=cache_dir, manifest=original, worker_proc=None)
        uploaded: dict[str, bytes] = {}

        async def mock_upload(config, key, data):
            uploaded[key] = data

        async def mock_download(_config, key):
            return uploaded[key]

        with (
            patch("plato.worlds.dvc_models.s3_upload_bytes", side_effect=mock_upload),
            patch("plato.worlds.dvc_models.s3_download_bytes", side_effect=mock_download),
        ):
            _manifest_md5, dvc_yaml = await smart_commit(mount, s3_config)

        manifest_entries = json.loads(next(data for key, data in uploaded.items() if key.endswith(".dir")))
        by_relpath = {entry["relpath"]: entry for entry in manifest_entries}

        assert by_relpath[".runtime"]["isdir"] is True
        assert by_relpath[".runtime/postgres"]["isdir"] is True
        assert by_relpath[".runtime/postgres/data"] == {
            "relpath": ".runtime/postgres/data",
            "isdir": True,
            "mode": 0o750,
        }
        assert "nfiles: 1" in dvc_yaml

    @pytest.mark.asyncio
    async def test_smart_commit_preserves_empty_directory_and_mode_only_change(self, s3_config, mount_dir):
        _tmp_path, cache_dir, overlay_dir, mountpoint = mount_dir
        original = DVCManifest(entries_list=[], manifest_md5="orig")

        runtime_dir = mountpoint / ".runtime" / "postgres" / "data"
        runtime_dir.mkdir(parents=True)
        runtime_dir.chmod(0o700)
        runtime_dir.chmod(0o750)

        mount = LazyDVCMount(mountpoint=mountpoint, cache_dir=cache_dir, manifest=original, worker_proc=None)
        uploaded: dict[str, bytes] = {}

        async def mock_upload(config, key, data):
            uploaded[key] = data

        async def mock_download(_config, key):
            return uploaded[key]

        with (
            patch("plato.worlds.dvc_models.s3_upload_bytes", side_effect=mock_upload),
            patch("plato.worlds.dvc_models.s3_download_bytes", side_effect=mock_download),
        ):
            _manifest_md5, dvc_yaml = await smart_commit(mount, s3_config)

        manifest_entries = json.loads(next(data for key, data in uploaded.items() if key.endswith(".dir")))
        assert {
            "relpath": ".runtime/postgres/data",
            "isdir": True,
            "mode": 0o750,
        } in manifest_entries
        assert "size: 0" in dvc_yaml
        assert "nfiles: 0" in dvc_yaml

    @pytest.mark.asyncio
    async def test_smart_commit_updates_existing_directory_mode_without_overlay_file_changes(
        self, s3_config, mount_dir
    ):
        _tmp_path, cache_dir, _overlay_dir, mountpoint = mount_dir
        original = DVCManifest(
            entries_list=[DVCManifestEntry(relpath=".runtime/postgres/data", mode=0o700, isdir=True)],
            manifest_md5="orig",
        )

        runtime_dir = mountpoint / ".runtime" / "postgres" / "data"
        runtime_dir.mkdir(parents=True)
        runtime_dir.chmod(0o750)

        mount = LazyDVCMount(mountpoint=mountpoint, cache_dir=cache_dir, manifest=original, worker_proc=None)
        uploaded: dict[str, bytes] = {}

        async def mock_upload(config, key, data):
            uploaded[key] = data

        async def mock_download(_config, key):
            return uploaded[key]

        with (
            patch("plato.worlds.dvc_models.s3_upload_bytes", side_effect=mock_upload),
            patch("plato.worlds.dvc_models.s3_download_bytes", side_effect=mock_download),
        ):
            await smart_commit(mount, s3_config)

        manifest_entries = json.loads(next(data for key, data in uploaded.items() if key.endswith(".dir")))
        by_relpath = {entry["relpath"]: entry for entry in manifest_entries}
        assert by_relpath[".runtime/postgres/data"]["mode"] == 0o750

    @pytest.mark.asyncio
    async def test_smart_commit_drops_stale_file_entry_when_path_is_now_a_directory(self, s3_config, mount_dir):
        _tmp_path, cache_dir, _overlay_dir, mountpoint = mount_dir
        original = DVCManifest(
            entries_list=[DVCManifestEntry(relpath=".runtime", size=0)],
            manifest_md5="orig",
        )

        runtime_dir = mountpoint / ".runtime" / "postgres" / "data"
        runtime_dir.mkdir(parents=True)

        mount = LazyDVCMount(mountpoint=mountpoint, cache_dir=cache_dir, manifest=original, worker_proc=None)
        uploaded: dict[str, bytes] = {}

        async def mock_upload(config, key, data):
            uploaded[key] = data

        async def mock_download(_config, key):
            return uploaded[key]

        with (
            patch("plato.worlds.dvc_models.s3_upload_bytes", side_effect=mock_upload),
            patch("plato.worlds.dvc_models.s3_download_bytes", side_effect=mock_download),
        ):
            _manifest_md5, dvc_yaml = await smart_commit(mount, s3_config)

        manifest_entries = json.loads(next(data for key, data in uploaded.items() if key.endswith(".dir")))
        runtime_entries = [entry for entry in manifest_entries if entry["relpath"] == ".runtime"]
        assert runtime_entries == [{"relpath": ".runtime", "isdir": True, "mode": 0o755}]
        assert "nfiles: 0" in dvc_yaml

    @pytest.mark.asyncio
    async def test_smart_commit_ignores_stale_overlay_file_when_live_path_is_directory(self, s3_config, mount_dir):
        _tmp_path, cache_dir, overlay_dir, mountpoint = mount_dir
        original = DVCManifest(entries_list=[], manifest_md5="orig")

        runtime_dir = mountpoint / ".runtime" / "postgres" / "data"
        runtime_dir.mkdir(parents=True)
        (overlay_dir / ".runtime").write_text("stale overlay file")

        mount = LazyDVCMount(mountpoint=mountpoint, cache_dir=cache_dir, manifest=original, worker_proc=None)
        uploaded: dict[str, bytes] = {}
        batch_uploads: list[tuple[str, str]] = []

        async def mock_upload(config, key, data):
            uploaded[key] = data

        async def mock_batch_upload(_config, uploads):
            batch_uploads.extend(uploads)
            for local_path, key in uploads:
                uploaded[key] = Path(local_path).read_bytes()

        async def mock_download(_config, key):
            return uploaded[key]

        with (
            patch("plato.worlds.dvc_models.s3_upload_bytes", side_effect=mock_upload),
            patch("plato.worlds.dvc_models.s3_upload_batch", side_effect=mock_batch_upload),
            patch("plato.worlds.dvc_models.s3_download_bytes", side_effect=mock_download),
        ):
            _manifest_md5, dvc_yaml = await smart_commit(mount, s3_config)

        manifest_entries = json.loads(next(data for key, data in uploaded.items() if key.endswith(".dir")))
        runtime_entries = [entry for entry in manifest_entries if entry["relpath"] == ".runtime"]
        assert runtime_entries == [{"relpath": ".runtime", "isdir": True, "mode": 0o755}]
        assert batch_uploads == []
        assert "nfiles: 0" in dvc_yaml

    @pytest.mark.asyncio
    async def test_smart_commit_prefers_meta_directory_snapshot_over_mount_walk(self, s3_config, mount_dir):
        _tmp_path, cache_dir, _overlay_dir, mountpoint = mount_dir
        mount = LazyDVCMount(
            mountpoint=mountpoint,
            cache_dir=cache_dir,
            manifest=DVCManifest(entries_list=[], manifest_md5="orig"),
            worker_proc=None,
        )
        mount.meta_path.write_text(
            json.dumps(
                {
                    "modified": [],
                    "deleted": [],
                    "created": [],
                    "directories": [
                        {"relpath": ".runtime", "mode": 0o755},
                        {"relpath": ".runtime/postgres/data", "mode": 0o750},
                    ],
                }
            )
        )
        uploaded: dict[str, bytes] = {}

        async def mock_upload(config, key, data):
            uploaded[key] = data

        async def mock_download(_config, key):
            return uploaded[key]

        with (
            patch("plato.worlds.dvc_models._scan_mount_directories", side_effect=AssertionError("should not walk")),
            patch("plato.worlds.dvc_models.s3_upload_bytes", side_effect=mock_upload),
            patch("plato.worlds.dvc_models.s3_download_bytes", side_effect=mock_download),
        ):
            await smart_commit(mount, s3_config)

        manifest_entries = json.loads(next(data for key, data in uploaded.items() if key.endswith(".dir")))
        assert {"relpath": ".runtime", "isdir": True, "mode": 0o755} in manifest_entries
        assert {"relpath": ".runtime/postgres/data", "isdir": True, "mode": 0o750} in manifest_entries

    @pytest.mark.asyncio
    async def test_smart_commit_remaps_original_files_for_directory_renames(self, s3_config, mount_dir):
        _tmp_path, cache_dir, _overlay_dir, mountpoint = mount_dir
        original = DVCManifest(
            entries_list=[
                DVCManifestEntry(relpath="runtime/postgres/PG_VERSION", md5="abc123", size=2),
                DVCManifestEntry(relpath="runtime", mode=0o755, isdir=True),
                DVCManifestEntry(relpath="runtime/postgres", mode=0o700, isdir=True),
            ],
            manifest_md5="orig",
        )
        renamed_file = mountpoint / "data" / "postgres" / "PG_VERSION"
        renamed_file.parent.mkdir(parents=True)
        renamed_file.write_text("16")

        mount = LazyDVCMount(mountpoint=mountpoint, cache_dir=cache_dir, manifest=original, worker_proc=None)
        mount.meta_path.write_text(
            json.dumps(
                {
                    "modified": [],
                    "deleted": [],
                    "created": [],
                    "directories": [
                        {"relpath": "data", "mode": 0o755},
                        {"relpath": "data/postgres", "mode": 0o700},
                    ],
                    "dir_renames": [
                        {"old_relpath": "runtime", "new_relpath": "data"},
                    ],
                }
            )
        )
        uploaded: dict[str, bytes] = {}

        async def mock_upload(config, key, data):
            uploaded[key] = data

        async def mock_download(_config, key):
            return uploaded[key]

        with (
            patch("plato.worlds.dvc_models.s3_upload_bytes", side_effect=mock_upload),
            patch("plato.worlds.dvc_models.s3_download_bytes", side_effect=mock_download),
        ):
            await smart_commit(mount, s3_config)

        manifest_entries = json.loads(next(data for key, data in uploaded.items() if key.endswith(".dir")))
        relpaths = {entry["relpath"] for entry in manifest_entries}
        assert "data/postgres/PG_VERSION" in relpaths
        assert "runtime/postgres/PG_VERSION" not in relpaths

    @pytest.mark.asyncio
    async def test_smart_commit_remaps_original_files_for_chained_directory_renames(self, s3_config, mount_dir):
        _tmp_path, cache_dir, _overlay_dir, mountpoint = mount_dir
        original = DVCManifest(
            entries_list=[
                DVCManifestEntry(relpath="runtime/postgres/PG_VERSION", md5="abc123", size=2),
                DVCManifestEntry(relpath="runtime", mode=0o755, isdir=True),
                DVCManifestEntry(relpath="runtime/postgres", mode=0o700, isdir=True),
            ],
            manifest_md5="orig",
        )
        renamed_file = mountpoint / "data" / "mysql" / "PG_VERSION"
        renamed_file.parent.mkdir(parents=True)
        renamed_file.write_text("16")

        mount = LazyDVCMount(mountpoint=mountpoint, cache_dir=cache_dir, manifest=original, worker_proc=None)
        mount.meta_path.write_text(
            json.dumps(
                {
                    "modified": [],
                    "deleted": [],
                    "created": [],
                    "directories": [
                        {"relpath": "data", "mode": 0o755},
                        {"relpath": "data/mysql", "mode": 0o700},
                    ],
                    "dir_renames": [
                        {"old_relpath": "runtime", "new_relpath": "data"},
                        {"old_relpath": "runtime/postgres", "new_relpath": "data/mysql"},
                    ],
                }
            )
        )
        uploaded: dict[str, bytes] = {}

        async def mock_upload(config, key, data):
            uploaded[key] = data

        async def mock_download(_config, key):
            return uploaded[key]

        with (
            patch("plato.worlds.dvc_models.s3_upload_bytes", side_effect=mock_upload),
            patch("plato.worlds.dvc_models.s3_download_bytes", side_effect=mock_download),
        ):
            await smart_commit(mount, s3_config)

        manifest_entries = json.loads(next(data for key, data in uploaded.items() if key.endswith(".dir")))
        relpaths = {entry["relpath"] for entry in manifest_entries}
        assert "data/mysql/PG_VERSION" in relpaths
        assert "data/postgres/PG_VERSION" not in relpaths
        assert "runtime/postgres/PG_VERSION" not in relpaths


@pytest.mark.skipif(not HAS_LOCAL_FUSE, reason="local FUSE support is unavailable")
class TestSmartCommitLiveFuseRepros:
    @pytest.mark.asyncio
    async def test_live_fuse_directory_mutations_do_not_emit_live_meta(
        self,
        local_fuse_mount_dir,
        local_fuse_s3_config,
        local_plato_fuse_binary,
        monkeypatch,
    ):
        _tmp_path, cache_dir, _overlay_dir, mountpoint = local_fuse_mount_dir
        monkeypatch.setenv("PLATO_FUSE_BINARY", str(local_plato_fuse_binary))

        mount = await mount_lazy(
            mountpoint=mountpoint,
            manifest=DVCManifest(entries_list=[], manifest_md5="orig"),
            s3_config=local_fuse_s3_config,
            cache_dir=cache_dir,
        )
        live_meta_path = cache_dir / "live-meta.json"
        try:
            runtime_dir = mountpoint / ".runtime" / "postgres" / "data"
            runtime_dir.mkdir(parents=True)
            runtime_dir.chmod(0o750)
            (mountpoint / ".runtime" / "postgres").rename(mountpoint / ".runtime" / "pgdata")
            scratch_dir = mountpoint / ".runtime" / "pgdata" / "scratch"
            scratch_dir.mkdir()
            scratch_dir.rmdir()

            def assert_runtime_dir_state() -> None:
                renamed_dir = mountpoint / ".runtime" / "pgdata" / "data"
                assert renamed_dir.is_dir()
                assert renamed_dir.stat().st_mode & 0o777 == 0o750
                assert not scratch_dir.exists()

            _retry_assert(assert_runtime_dir_state)
            assert not live_meta_path.exists()

            _manifest_md5, _dvc_yaml, manifest_entries = await _smart_commit_with_mocked_s3(
                mount,
                local_fuse_s3_config,
            )
        finally:
            await unmount_lazy(mount)

        dir_entries = {entry["relpath"]: entry for entry in manifest_entries if entry.get("isdir")}
        assert ".runtime/pgdata/data" in dir_entries
        assert ".runtime/postgres/data" not in dir_entries
        assert dir_entries[".runtime/pgdata/data"]["mode"] == 0o750

    @pytest.mark.asyncio
    async def test_live_fuse_smart_commit_uses_live_directory_snapshot_without_meta(
        self,
        local_fuse_mount_dir,
        local_fuse_s3_config,
        local_plato_fuse_binary,
        monkeypatch,
    ):
        _tmp_path, cache_dir, _overlay_dir, mountpoint = local_fuse_mount_dir
        monkeypatch.setenv("PLATO_FUSE_BINARY", str(local_plato_fuse_binary))

        mount = await mount_lazy(
            mountpoint=mountpoint,
            manifest=DVCManifest(entries_list=[], manifest_md5="orig"),
            s3_config=local_fuse_s3_config,
            cache_dir=cache_dir,
        )
        try:
            runtime_dir = mountpoint / ".runtime" / "postgres" / "data"
            runtime_dir.mkdir(parents=True)
            runtime_dir.chmod(0o750)

            def assert_runtime_dir_state() -> None:
                assert runtime_dir.is_dir()
                assert runtime_dir.stat().st_mode & 0o777 == 0o750

            _retry_assert(assert_runtime_dir_state)
            assert not mount.meta_path.exists()

            _manifest_md5, _dvc_yaml, manifest_entries = await _smart_commit_with_mocked_s3(
                mount,
                local_fuse_s3_config,
            )
        finally:
            await unmount_lazy(mount)

        dir_entries = {entry["relpath"]: entry for entry in manifest_entries if entry.get("isdir")}
        assert dir_entries[".runtime"]["mode"] == 0o755
        assert dir_entries[".runtime/postgres"]["mode"] == 0o755
        assert dir_entries[".runtime/postgres/data"]["mode"] == 0o750

    @pytest.mark.asyncio
    async def test_live_fuse_smart_commit_drops_stale_file_entry_when_manifest_path_is_now_directory(
        self,
        local_fuse_mount_dir,
        local_fuse_s3_config,
        local_plato_fuse_binary,
        monkeypatch,
    ):
        _tmp_path, cache_dir, _overlay_dir, mountpoint = local_fuse_mount_dir
        monkeypatch.setenv("PLATO_FUSE_BINARY", str(local_plato_fuse_binary))
        manifest = DVCManifest(
            entries_list=[
                DVCManifestEntry(relpath=".runtime", size=0),
                DVCManifestEntry(relpath=".runtime/postgres", mode=0o755, isdir=True),
                DVCManifestEntry(relpath=".runtime/postgres/data", mode=0o750, isdir=True),
            ],
            manifest_md5="orig",
        )
        mount = await mount_lazy(
            mountpoint=mountpoint,
            manifest=manifest,
            s3_config=local_fuse_s3_config,
            cache_dir=cache_dir,
        )
        try:

            def assert_runtime_dir_state() -> None:
                assert (mountpoint / ".runtime").is_dir()
                assert (mountpoint / ".runtime" / "postgres" / "data").is_dir()

            _retry_assert(assert_runtime_dir_state)

            _manifest_md5, _dvc_yaml, manifest_entries = await _smart_commit_with_mocked_s3(
                mount,
                local_fuse_s3_config,
            )
        finally:
            await unmount_lazy(mount)

        runtime_entries = [entry for entry in manifest_entries if entry["relpath"] == ".runtime"]
        assert runtime_entries == [{"relpath": ".runtime", "isdir": True, "mode": 0o755}]

    @pytest.mark.asyncio
    async def test_live_fuse_smart_commit_ignores_stale_overlay_file_when_directory_restores(
        self,
        local_fuse_mount_dir,
        local_fuse_s3_config,
        local_plato_fuse_binary,
        monkeypatch,
    ):
        _tmp_path, cache_dir, overlay_dir, mountpoint = local_fuse_mount_dir
        monkeypatch.setenv("PLATO_FUSE_BINARY", str(local_plato_fuse_binary))
        manifest = DVCManifest(
            entries_list=[
                DVCManifestEntry(relpath=".runtime", mode=0o755, isdir=True),
                DVCManifestEntry(relpath=".runtime/postgres", mode=0o755, isdir=True),
                DVCManifestEntry(relpath=".runtime/postgres/data", mode=0o750, isdir=True),
            ],
            manifest_md5="orig",
        )
        (overlay_dir / ".runtime").write_text("stale overlay file")
        mount = await mount_lazy(
            mountpoint=mountpoint,
            manifest=manifest,
            s3_config=local_fuse_s3_config,
            cache_dir=cache_dir,
        )
        try:

            def assert_runtime_dir_state() -> None:
                assert (mountpoint / ".runtime").is_dir()
                assert (mountpoint / ".runtime" / "postgres" / "data").is_dir()

            _retry_assert(assert_runtime_dir_state)

            _manifest_md5, _dvc_yaml, manifest_entries = await _smart_commit_with_mocked_s3(
                mount,
                local_fuse_s3_config,
            )
        finally:
            await unmount_lazy(mount)

        runtime_entries = [entry for entry in manifest_entries if entry["relpath"] == ".runtime"]
        assert runtime_entries == [{"relpath": ".runtime", "isdir": True, "mode": 0o755}]

    @pytest.mark.asyncio
    async def test_live_fuse_smart_commit_keeps_unchanged_files_under_directory_rename(
        self,
        local_fuse_mount_dir,
        local_fuse_s3_config,
        local_plato_fuse_binary,
        monkeypatch,
    ):
        _tmp_path, cache_dir, _overlay_dir, mountpoint = local_fuse_mount_dir
        monkeypatch.setenv("PLATO_FUSE_BINARY", str(local_plato_fuse_binary))
        manifest = DVCManifest(
            entries_list=[
                DVCManifestEntry(relpath="runtime/postgres/PG_VERSION", md5="abc123", size=2),
                DVCManifestEntry(relpath="runtime", mode=0o755, isdir=True),
                DVCManifestEntry(relpath="runtime/postgres", mode=0o700, isdir=True),
            ],
            manifest_md5="orig",
        )
        mount = await mount_lazy(
            mountpoint=mountpoint,
            manifest=manifest,
            s3_config=local_fuse_s3_config,
            cache_dir=cache_dir,
        )
        try:
            (mountpoint / "runtime").rename(mountpoint / "data")

            def assert_rename_applied() -> None:
                assert not (mountpoint / "runtime").exists()
                assert (mountpoint / "data" / "postgres" / "PG_VERSION").exists()

            _retry_assert(assert_rename_applied)
            assert not mount.meta_path.exists()

            _manifest_md5, _dvc_yaml, manifest_entries = await _smart_commit_with_mocked_s3(
                mount,
                local_fuse_s3_config,
            )
        finally:
            await unmount_lazy(mount)

        relpaths = {entry["relpath"] for entry in manifest_entries}
        assert "data/postgres/PG_VERSION" in relpaths
        assert "runtime/postgres/PG_VERSION" not in relpaths

    @pytest.mark.asyncio
    async def test_live_fuse_smart_commit_ignores_new_directories_when_meta_snapshot_is_stale(
        self,
        local_fuse_mount_dir,
        local_fuse_s3_config,
        local_plato_fuse_binary,
        monkeypatch,
    ):
        _tmp_path, cache_dir, _overlay_dir, mountpoint = local_fuse_mount_dir
        _write_smart_commit_meta(
            cache_dir,
            directories=[
                {"relpath": ".runtime", "mode": 0o755},
            ],
        )
        monkeypatch.setenv("PLATO_FUSE_BINARY", str(local_plato_fuse_binary))

        mount = await mount_lazy(
            mountpoint=mountpoint,
            manifest=DVCManifest(entries_list=[], manifest_md5="orig"),
            s3_config=local_fuse_s3_config,
            cache_dir=cache_dir,
        )
        try:
            runtime_dir = mountpoint / ".runtime" / "postgres" / "data"
            runtime_dir.mkdir(parents=True)
            runtime_dir.chmod(0o750)

            def assert_runtime_dir_state() -> None:
                assert runtime_dir.is_dir()
                assert runtime_dir.stat().st_mode & 0o777 == 0o750

            _retry_assert(assert_runtime_dir_state)

            _manifest_md5, _dvc_yaml, manifest_entries = await _smart_commit_with_mocked_s3(
                mount,
                local_fuse_s3_config,
            )
        finally:
            await unmount_lazy(mount)

        dir_entries = {entry["relpath"]: entry for entry in manifest_entries if entry.get("isdir")}
        assert dir_entries[".runtime/postgres/data"]["mode"] == 0o750

    @pytest.mark.asyncio
    async def test_live_fuse_smart_commit_ignores_directory_mode_change_when_meta_snapshot_is_stale(
        self,
        local_fuse_mount_dir,
        local_fuse_s3_config,
        local_plato_fuse_binary,
        monkeypatch,
    ):
        _tmp_path, cache_dir, _overlay_dir, mountpoint = local_fuse_mount_dir
        manifest = DVCManifest(
            entries_list=[
                DVCManifestEntry(relpath=".runtime", mode=0o755, isdir=True),
                DVCManifestEntry(relpath=".runtime/postgres", mode=0o755, isdir=True),
                DVCManifestEntry(relpath=".runtime/postgres/data", mode=0o700, isdir=True),
            ],
            manifest_md5="orig",
        )
        _write_smart_commit_meta(
            cache_dir,
            directories=[
                {"relpath": ".runtime", "mode": 0o755},
                {"relpath": ".runtime/postgres", "mode": 0o755},
                {"relpath": ".runtime/postgres/data", "mode": 0o700},
            ],
        )
        monkeypatch.setenv("PLATO_FUSE_BINARY", str(local_plato_fuse_binary))

        mount = await mount_lazy(
            mountpoint=mountpoint,
            manifest=manifest,
            s3_config=local_fuse_s3_config,
            cache_dir=cache_dir,
        )
        try:
            runtime_dir = mountpoint / ".runtime" / "postgres" / "data"

            def assert_initial_mode() -> None:
                assert runtime_dir.is_dir()
                assert runtime_dir.stat().st_mode & 0o777 == 0o700

            _retry_assert(assert_initial_mode)
            runtime_dir.chmod(0o750)

            def assert_updated_mode() -> None:
                assert runtime_dir.stat().st_mode & 0o777 == 0o750

            _retry_assert(assert_updated_mode)

            _manifest_md5, _dvc_yaml, manifest_entries = await _smart_commit_with_mocked_s3(
                mount,
                local_fuse_s3_config,
            )
        finally:
            await unmount_lazy(mount)

        dir_entries = {entry["relpath"]: entry for entry in manifest_entries if entry.get("isdir")}
        assert dir_entries[".runtime/postgres/data"]["mode"] == 0o750

    @pytest.mark.asyncio
    async def test_live_fuse_smart_commit_keeps_renamed_file_mode_change_on_visible_path(
        self,
        local_fuse_mount_dir,
        local_fuse_s3_config,
        local_plato_fuse_binary,
        monkeypatch,
    ):
        _tmp_path, cache_dir, _overlay_dir, mountpoint = local_fuse_mount_dir
        monkeypatch.setenv("PLATO_FUSE_BINARY", str(local_plato_fuse_binary))
        original_data = b"echo hi\n"
        _write_cached_file(cache_dir, "config.sh", original_data)
        manifest = DVCManifest(
            entries_list=[DVCManifestEntry(relpath="config.sh", md5=hashlib.md5(original_data).hexdigest(), size=8)],
            manifest_md5="orig",
        )

        mount = await mount_lazy(
            mountpoint=mountpoint,
            manifest=manifest,
            s3_config=local_fuse_s3_config,
            cache_dir=cache_dir,
        )
        try:
            source = mountpoint / "config.sh"
            renamed = mountpoint / "run.sh"
            source.rename(renamed)

            def assert_rename_applied() -> None:
                assert not source.exists()
                assert renamed.exists()

            _retry_assert(assert_rename_applied)
            renamed.chmod(0o755)

            def assert_exec_mode_applied() -> None:
                assert renamed.stat().st_mode & 0o777 == 0o755

            _retry_assert(assert_exec_mode_applied)

            _manifest_md5, _dvc_yaml, manifest_entries = await _smart_commit_with_mocked_s3(
                mount,
                local_fuse_s3_config,
            )
        finally:
            await unmount_lazy(mount)

        by_relpath = {entry["relpath"]: entry for entry in manifest_entries}
        assert "config.sh" not in by_relpath
        assert by_relpath["run.sh"]["isexec"] is True
        assert by_relpath["run.sh"]["md5"] == hashlib.md5(original_data).hexdigest()
        assert by_relpath["run.sh"]["size"] == len(original_data)

    @pytest.mark.asyncio
    async def test_live_fuse_smart_commit_ignores_deleted_new_file(
        self,
        local_fuse_mount_dir,
        local_fuse_s3_config,
        local_plato_fuse_binary,
        monkeypatch,
    ):
        _tmp_path, cache_dir, _overlay_dir, mountpoint = local_fuse_mount_dir
        monkeypatch.setenv("PLATO_FUSE_BINARY", str(local_plato_fuse_binary))

        mount = await mount_lazy(
            mountpoint=mountpoint,
            manifest=DVCManifest(entries_list=[], manifest_md5="orig"),
            s3_config=local_fuse_s3_config,
            cache_dir=cache_dir,
        )
        try:
            scratch = mountpoint / "scratch.txt"
            scratch.write_text("temporary\n")

            def assert_created() -> None:
                assert scratch.exists()

            _retry_assert(assert_created)
            scratch.unlink()

            def assert_deleted() -> None:
                assert not scratch.exists()

            _retry_assert(assert_deleted)

            _manifest_md5, _dvc_yaml, manifest_entries = await _smart_commit_with_mocked_s3(
                mount,
                local_fuse_s3_config,
            )
        finally:
            await unmount_lazy(mount)

        assert manifest_entries == []

    @pytest.mark.asyncio
    async def test_live_fuse_smart_commit_includes_deleted_files(
        self,
        local_fuse_mount_dir,
        local_fuse_s3_config,
        local_plato_fuse_binary,
        monkeypatch,
    ):
        _tmp_path, cache_dir, _overlay_dir, mountpoint = local_fuse_mount_dir
        monkeypatch.setenv("PLATO_FUSE_BINARY", str(local_plato_fuse_binary))
        original_data = b"hello world\n"
        _write_cached_file(cache_dir, "doomed.txt", original_data)
        manifest = DVCManifest(
            entries_list=[
                DVCManifestEntry(
                    relpath="doomed.txt", md5=hashlib.md5(original_data).hexdigest(), size=len(original_data)
                )
            ],
            manifest_md5="orig",
        )

        mount = await mount_lazy(
            mountpoint=mountpoint,
            manifest=manifest,
            s3_config=local_fuse_s3_config,
            cache_dir=cache_dir,
        )
        try:
            target = mountpoint / "doomed.txt"

            def assert_visible() -> None:
                assert target.exists()

            _retry_assert(assert_visible)
            target.unlink()

            def assert_deleted() -> None:
                assert not target.exists()

            _retry_assert(assert_deleted)

            _manifest_md5, _dvc_yaml, manifest_entries = await _smart_commit_with_mocked_s3(
                mount,
                local_fuse_s3_config,
            )
        finally:
            await unmount_lazy(mount)

        relpaths = [entry["relpath"] for entry in manifest_entries]
        assert "doomed.txt" not in relpaths

    @pytest.mark.asyncio
    async def test_live_fuse_cross_device_mv_preserves_file(
        self,
        local_fuse_mount_dir,
        local_fuse_s3_config,
        monkeypatch,
        tmp_path,
    ):
        """Regression: jq '...' "$FILE" > /tmp/x && mv /tmp/x "$FILE" must not
        cause the file to disappear from live smart_commit manifests."""
        _tmp_path, cache_dir, _overlay_dir, mountpoint = local_fuse_mount_dir
        fuse_bin = shutil.which("plato-fuse")
        assert fuse_bin, "plato-fuse not found on PATH"
        monkeypatch.setenv("PLATO_FUSE_BINARY", fuse_bin)

        original_data = b'{"tasks": [{"id": "1.1", "is_completed": false}]}\n'
        _write_cached_file(cache_dir, "progress.json", original_data)
        manifest = DVCManifest(
            entries_list=[
                DVCManifestEntry(
                    relpath="progress.json",
                    md5=hashlib.md5(original_data).hexdigest(),
                    size=len(original_data),
                ),
            ],
            manifest_md5="orig",
        )

        mount = await mount_lazy(
            mountpoint=mountpoint,
            manifest=manifest,
            s3_config=local_fuse_s3_config,
            cache_dir=cache_dir,
        )
        try:
            target = mountpoint / "progress.json"

            def assert_visible() -> None:
                assert target.exists()
                assert target.read_bytes() == original_data

            _retry_assert(assert_visible)

            # Exact pattern agents use: write to /tmp then mv over the FUSE file
            updated_data = b'{"tasks": [{"id": "1.1", "is_completed": true}]}\n'
            tmp_file = tmp_path / "progress_tmp.json"
            tmp_file.write_bytes(updated_data)
            subprocess.run(
                ["mv", str(tmp_file), str(target)],
                check=True,
            )

            def assert_updated() -> None:
                assert target.exists()
                assert target.read_bytes() == updated_data

            _retry_assert(assert_updated)

            _manifest_md5, _dvc_yaml, manifest_entries = await _smart_commit_with_mocked_s3(
                mount,
                local_fuse_s3_config,
            )
        finally:
            await unmount_lazy(mount)

        relpaths = {entry["relpath"] for entry in manifest_entries}
        assert "progress.json" in relpaths, (
            f"progress.json disappeared from manifest after cross-device mv! Got: {relpaths}"
        )

    @pytest.mark.asyncio
    async def test_live_fuse_concurrent_cross_device_mv_preserves_file(
        self,
        local_fuse_mount_dir,
        local_fuse_s3_config,
        monkeypatch,
        tmp_path,
    ):
        """Simulate 4 agents racing to update the same file via
        jq > /tmp/x && mv /tmp/x $FILE, then verify the file survives
        a live smart_commit."""
        _tmp_path, cache_dir, _overlay_dir, mountpoint = local_fuse_mount_dir
        fuse_bin = shutil.which("plato-fuse")
        assert fuse_bin, "plato-fuse not found on PATH"
        monkeypatch.setenv("PLATO_FUSE_BINARY", fuse_bin)

        original_data = b'{"tasks": [{"id": "1.1", "is_completed": false}]}\n'
        _write_cached_file(cache_dir, "progress.json", original_data)
        manifest = DVCManifest(
            entries_list=[
                DVCManifestEntry(
                    relpath="progress.json",
                    md5=hashlib.md5(original_data).hexdigest(),
                    size=len(original_data),
                ),
            ],
            manifest_md5="orig",
        )

        mount = await mount_lazy(
            mountpoint=mountpoint,
            manifest=manifest,
            s3_config=local_fuse_s3_config,
            cache_dir=cache_dir,
        )
        try:
            target = mountpoint / "progress.json"

            def assert_visible() -> None:
                assert target.exists()

            _retry_assert(assert_visible)

            import concurrent.futures

            def agent_update(agent_id: int) -> None:
                for i in range(5):
                    data = f'{{"tasks": [{{"id": "1.1", "agent": {agent_id}, "iter": {i}}}]}}\n'
                    tmp_file = tmp_path / f"progress_tmp_{agent_id}_{i}.json"
                    tmp_file.write_text(data)
                    # mv may fail transiently under concurrency; that's fine
                    subprocess.run(
                        ["mv", str(tmp_file), str(target)],
                        check=False,
                    )

            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
                futures = [pool.submit(agent_update, i) for i in range(4)]
                for f in concurrent.futures.as_completed(futures, timeout=10):
                    f.result()

            def assert_still_exists() -> None:
                assert target.exists()

            _retry_assert(assert_still_exists)

            _manifest_md5, _dvc_yaml, manifest_entries = await _smart_commit_with_mocked_s3(
                mount,
                local_fuse_s3_config,
            )
        finally:
            await unmount_lazy(mount)

        relpaths = {entry["relpath"] for entry in manifest_entries}
        assert "progress.json" in relpaths, (
            f"progress.json disappeared from manifest after concurrent cross-device mv! Got: {relpaths}"
        )

    @pytest.mark.asyncio
    async def test_live_fuse_truly_deleted_file_stays_deleted(
        self,
        local_fuse_mount_dir,
        local_fuse_s3_config,
        monkeypatch,
    ):
        """A file that is unlinked and NOT re-created must stay out of the manifest."""
        _tmp_path, cache_dir, _overlay_dir, mountpoint = local_fuse_mount_dir
        fuse_bin = shutil.which("plato-fuse")
        assert fuse_bin, "plato-fuse not found on PATH"
        monkeypatch.setenv("PLATO_FUSE_BINARY", fuse_bin)

        original_data = b"delete me\n"
        _write_cached_file(cache_dir, "doomed.txt", original_data)
        manifest = DVCManifest(
            entries_list=[
                DVCManifestEntry(
                    relpath="doomed.txt",
                    md5=hashlib.md5(original_data).hexdigest(),
                    size=len(original_data),
                ),
            ],
            manifest_md5="orig",
        )

        mount = await mount_lazy(
            mountpoint=mountpoint,
            manifest=manifest,
            s3_config=local_fuse_s3_config,
            cache_dir=cache_dir,
        )
        try:
            target = mountpoint / "doomed.txt"

            def assert_visible() -> None:
                assert target.exists()

            _retry_assert(assert_visible)

            target.unlink()

            def assert_gone() -> None:
                assert not target.exists()

            _retry_assert(assert_gone)

            _manifest_md5, _dvc_yaml, manifest_entries = await _smart_commit_with_mocked_s3(
                mount,
                local_fuse_s3_config,
            )
        finally:
            await unmount_lazy(mount)

        relpaths = {entry["relpath"] for entry in manifest_entries}
        assert "doomed.txt" not in relpaths, (
            f"doomed.txt should have been deleted but is still in manifest! Got: {relpaths}"
        )


@pytest.mark.skipif(not HAS_LOCAL_FUSE, reason="local FUSE support is unavailable")
class TestFuseVisibleAttrBlocking:
    """Regression tests for visible_attr blocking the single-threaded FUSE loop.

    The refactored FUSE handler calls hydrate_unknown_size() during lookup/getattr
    (via visible_attr), which can trigger an S3 download for manifest entries with
    size=0.  Because the FUSE loop is single-threaded (fuser::mount2), a blocking
    S3 call freezes the entire mount — every subsequent operation from every process
    queues behind the blocked download.

    These tests reproduce the issue by pointing S3 at a local TCP server that
    accepts connections but never responds, ensuring the download truly blocks.
    """

    @pytest.fixture
    def blocking_s3_config(self):
        """S3Config pointing at a local HTTP server that blocks S3 object downloads.

        The server handles AWS SDK initialization requests (STS, etc.) with fast
        error responses, but blocks forever on S3 GET object requests — simulating
        a slow/hanging S3 download that freezes the single-threaded FUSE loop.
        """
        import http.server
        import socketserver
        import threading

        class _SlowHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                if "/dvc-cache/" in self.path:
                    # S3 object download — block forever to simulate slow S3
                    self.send_response(200)
                    self.send_header("Content-Length", "999999")
                    self.end_headers()
                    threading.Event().wait()
                else:
                    # SDK init requests — fail fast so the binary can start
                    self.send_response(403)
                    self.end_headers()

            def do_POST(self):
                # STS AssumeRole etc. — fail fast
                self.send_response(403)
                self.end_headers()

            def do_PUT(self):
                self.send_response(403)
                self.end_headers()

            def do_HEAD(self):
                self.send_response(403)
                self.end_headers()

            def log_message(self, fmt, *args):
                pass

        class _ThreadedServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
            daemon_threads = True

        server = _ThreadedServer(("127.0.0.1", 0), _SlowHandler)
        port = server.server_address[1]
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()

        config = S3Config(
            bucket="test-bucket",
            prefix="test-prefix",
            credentials=dict(DUMMY_AWS_CREDENTIALS),
        )
        yield config, port

        server.shutdown()

    @pytest.mark.asyncio
    async def test_stat_on_unknown_size_manifest_entry_should_not_block_fuse(
        self,
        local_fuse_mount_dir,
        local_plato_fuse_binary,
        blocking_s3_config,
        monkeypatch,
    ):
        """stat() on a manifest file with size=0 must not block the FUSE loop.

        Before the fix, visible_attr called hydrate_unknown_size which called
        fetch_data → s3.download(), blocking the single-threaded FUSE loop.
        This caused bun install (and any other concurrent FS operation) to hang.
        """
        _tmp_path, cache_dir, _overlay_dir, mountpoint = local_fuse_mount_dir
        s3_config, blocking_port = blocking_s3_config

        monkeypatch.setenv("PLATO_FUSE_BINARY", str(local_plato_fuse_binary))
        # Point the AWS SDK at our blocking TCP server
        monkeypatch.setenv("AWS_ENDPOINT_URL", f"http://127.0.0.1:{blocking_port}")

        manifest = DVCManifest(
            entries_list=[
                DVCManifestEntry(relpath="package.json", md5="abc123def456abc123def456abc123de", size=0),
            ],
            manifest_md5="test_manifest",
        )

        mount = await mount_lazy(
            mountpoint=mountpoint,
            manifest=manifest,
            s3_config=s3_config,
            cache_dir=cache_dir,
        )
        try:
            import concurrent.futures

            # stat() triggers lookup → visible_attr → hydrate_unknown_size.
            # If hydrate_unknown_size blocks on S3, this will time out.
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(lambda: (mountpoint / "package.json").stat())
                try:
                    future.result(timeout=5)
                except concurrent.futures.TimeoutError:
                    pytest.fail(
                        "FUSE mount hung on stat() for a manifest entry with size=0 — "
                        "visible_attr/hydrate_unknown_size is blocking on S3"
                    )
        finally:
            await unmount_lazy(mount)

    @pytest.mark.asyncio
    async def test_readdir_with_unknown_size_entries_should_not_block_fuse(
        self,
        local_fuse_mount_dir,
        local_plato_fuse_binary,
        blocking_s3_config,
        monkeypatch,
    ):
        """readdir + getattr on a directory with size=0 entries must not hang.

        This simulates what bun install does: list a directory and stat each
        entry.  If visible_attr blocks on S3 for any entry, the entire mount
        hangs.
        """
        _tmp_path, cache_dir, _overlay_dir, mountpoint = local_fuse_mount_dir
        s3_config, blocking_port = blocking_s3_config

        monkeypatch.setenv("PLATO_FUSE_BINARY", str(local_plato_fuse_binary))
        monkeypatch.setenv("AWS_ENDPOINT_URL", f"http://127.0.0.1:{blocking_port}")

        manifest = DVCManifest(
            entries_list=[
                DVCManifestEntry(relpath="web/package.json", md5="aaa111bbb222ccc333ddd444eee555ff", size=0),
                DVCManifestEntry(relpath="web/tsconfig.json", md5="fff000eee111ddd222ccc333bbb444aa", size=0),
                DVCManifestEntry(relpath="web/next.config.js", md5="111222333444555666777888999aaabbb", size=0),
            ],
            manifest_md5="test_manifest",
        )

        mount = await mount_lazy(
            mountpoint=mountpoint,
            manifest=manifest,
            s3_config=s3_config,
            cache_dir=cache_dir,
        )
        try:
            import concurrent.futures

            def _list_and_stat():
                entries = list((mountpoint / "web").iterdir())
                for entry in entries:
                    entry.stat()
                return entries

            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(_list_and_stat)
                try:
                    result = future.result(timeout=5)
                    assert len(result) == 3
                except concurrent.futures.TimeoutError:
                    pytest.fail(
                        "FUSE mount hung during readdir + stat of directory with "
                        "size=0 manifest entries — visible_attr is blocking on S3"
                    )
        finally:
            await unmount_lazy(mount)

    @pytest.mark.asyncio
    async def test_create_new_file_while_unknown_size_entry_exists_should_not_block(
        self,
        local_fuse_mount_dir,
        local_plato_fuse_binary,
        blocking_s3_config,
        monkeypatch,
    ):
        """Creating new files must not be blocked by manifest entries needing S3.

        This is the core bun install scenario: the workspace has manifest files
        from a prior commit, and bun install creates thousands of new symlinks
        and files in node_modules.  If any lookup/getattr on a manifest file
        blocks on S3, the new file creation also hangs.
        """
        _tmp_path, cache_dir, _overlay_dir, mountpoint = local_fuse_mount_dir
        s3_config, blocking_port = blocking_s3_config

        monkeypatch.setenv("PLATO_FUSE_BINARY", str(local_plato_fuse_binary))
        monkeypatch.setenv("AWS_ENDPOINT_URL", f"http://127.0.0.1:{blocking_port}")

        manifest = DVCManifest(
            entries_list=[
                DVCManifestEntry(relpath="web/package.json", md5="aaa111bbb222ccc333ddd444eee555ff", size=0),
            ],
            manifest_md5="test_manifest",
        )

        mount = await mount_lazy(
            mountpoint=mountpoint,
            manifest=manifest,
            s3_config=s3_config,
            cache_dir=cache_dir,
        )
        try:
            import concurrent.futures

            def _create_files():
                nm = mountpoint / "web" / "node_modules"
                nm.mkdir(parents=True)
                bin_dir = nm / ".bin"
                bin_dir.mkdir()
                # Simulate bun install creating symlinks
                for i in range(5):
                    (bin_dir / f"tool-{i}").symlink_to(f"../../pkg-{i}/bin/tool")
                # Also stat an existing manifest file (would block pre-fix)
                (mountpoint / "web" / "package.json").stat()
                return True

            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(_create_files)
                try:
                    assert future.result(timeout=10)
                except concurrent.futures.TimeoutError:
                    pytest.fail(
                        "FUSE mount hung while creating new files alongside "
                        "manifest entries with size=0 — S3 is blocking the FUSE loop"
                    )
        finally:
            await unmount_lazy(mount)


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
