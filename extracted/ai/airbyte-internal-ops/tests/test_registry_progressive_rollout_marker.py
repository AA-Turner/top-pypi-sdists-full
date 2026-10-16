from __future__ import annotations

import yaml

from airbyte_ops_mcp.registry.progressive_rollout_marker import (
    annotate_progressive_rollout_marker,
    finalize_progressive_rollout_marker,
    get_progressive_rollout_marker,
)
from airbyte_ops_mcp.registry.store import RegistryStore

_BUCKET = "prod-airbyte-cloud-connector-metadata-service"
_PATH = "metadata/airbyte/source-faker/1.2.3/progressive-rollout.yml"
_VERSION_DIR = "metadata/airbyte/source-faker/1.2.3"
_METADATA_PATH = f"{_VERSION_DIR}/metadata.yaml"
_YANK_PATH = f"{_VERSION_DIR}/version-yank.yml"


class FakeBlob:
    def __init__(
        self,
        files: dict[str, bytes],
        path: str,
        events: list[tuple[str, str]],
    ) -> None:
        self.files = files
        self.path = path
        self.name = path
        self.events = events

    def exists(self) -> bool:
        return self.path in self.files

    def upload_from_string(self, content: str, content_type: str) -> None:
        assert content_type == "application/x-yaml"
        self.events.append(("upload", self.path))
        self.files[self.path] = content.encode("utf-8")

    def delete(self) -> None:
        self.events.append(("delete", self.path))
        self.files.pop(self.path, None)


class FakeStorageClient:
    def __init__(
        self,
        files: dict[str, bytes],
        events: list[tuple[str, str]] | None = None,
    ) -> None:
        self.files = files
        self.events = events if events is not None else []

    def bucket(self, bucket_name: str) -> FakeStorageClient:
        assert bucket_name == _BUCKET
        return self

    def blob(self, path: str) -> FakeBlob:
        return FakeBlob(self.files, path, self.events)

    def list_blobs(self, *, prefix: str) -> list[FakeBlob]:
        return [self.blob(path) for path in self.files if path.startswith(prefix)]

    def copy_blob(
        self,
        source_blob: FakeBlob,
        destination_bucket: FakeStorageClient,
        *,
        new_name: str,
    ) -> None:
        assert destination_bucket is self
        self.events.append(("copy", new_name))
        self.files[new_name] = self.files[source_blob.path]


class FakeFileSystem:
    def __init__(self, files: dict[str, bytes]) -> None:
        self.files = files

    def exists(self, path: str) -> bool:
        return path.removeprefix(f"{_BUCKET}/") in self.files

    def cat_file(self, path: str) -> bytes:
        return self.files[path.removeprefix(f"{_BUCKET}/")]

    def glob(self, pattern: str) -> list[str]:
        prefix = pattern.removeprefix(f"{_BUCKET}/").removesuffix(
            "progressive-rollout-*.yml"
        )
        return [
            f"{_BUCKET}/{path}"
            for path in self.files
            if path.startswith(prefix)
            and path.startswith(f"{prefix}progressive-rollout-")
            and path.endswith(".yml")
        ]


def _install_fake_gcs(
    monkeypatch,
    files: dict[str, bytes],
    events: list[tuple[str, str]] | None = None,
) -> FakeStorageClient:
    storage_client = FakeStorageClient(files, events)
    monkeypatch.setattr(
        "airbyte_ops_mcp.registry.progressive_rollout_marker.gcsfs.GCSFileSystem",
        lambda **_: FakeFileSystem(files),
    )
    monkeypatch.setattr(
        "airbyte_ops_mcp.registry.progressive_rollout_marker.get_gcs_credentials_token",
        lambda: None,
    )
    monkeypatch.setattr(
        "airbyte_ops_mcp.registry.progressive_rollout_marker.get_gcs_storage_client",
        lambda: storage_client,
    )
    return storage_client


def test_get_progressive_rollout_marker_parses_fields_and_raw(monkeypatch) -> None:
    raw = yaml.safe_dump(
        {
            "progressive_rollout": True,
            "created_at": "2026-06-20T11:30:00Z",
            "promotion_requested_at": "2026-06-20T15:00:00Z",
            "promotion_requested_by": "ops@example.com",
            "rollout_id": "rollout-123",
        },
        sort_keys=False,
    ).encode()
    files = {_PATH: raw}
    _install_fake_gcs(monkeypatch, files)

    marker = get_progressive_rollout_marker("source-faker", "1.2.3", _BUCKET)

    assert marker is not None
    assert marker.progressive_rollout is True
    assert marker.created_at == "2026-06-20T11:30:00Z"
    assert marker.promotion_requested_by == "ops@example.com"
    assert marker.rollout_id == "rollout-123"
    assert marker.raw == raw.decode()


def test_get_progressive_rollout_marker_returns_none_when_absent(monkeypatch) -> None:
    files: dict[str, bytes] = {}
    _install_fake_gcs(monkeypatch, files)

    assert get_progressive_rollout_marker("source-faker", "1.2.3", _BUCKET) is None


def test_get_progressive_rollout_marker_disables_filesystem_caches(monkeypatch) -> None:
    files: dict[str, bytes] = {}
    filesystem_kwargs: list[dict[str, object]] = []

    monkeypatch.setattr(
        "airbyte_ops_mcp.registry.progressive_rollout_marker.gcsfs.GCSFileSystem",
        lambda **kwargs: filesystem_kwargs.append(kwargs) or FakeFileSystem(files),
    )
    monkeypatch.setattr(
        "airbyte_ops_mcp.registry.progressive_rollout_marker.get_gcs_credentials_token",
        lambda: None,
    )

    assert get_progressive_rollout_marker("source-faker", "1.2.3", _BUCKET) is None

    assert filesystem_kwargs == [
        {
            "token": None,
            "skip_instance_cache": True,
            "use_listings_cache": False,
        }
    ]


def test_get_progressive_rollout_marker_falls_back_to_latest_dated_marker(
    monkeypatch,
) -> None:
    older_path = (
        "metadata/airbyte/source-faker/1.2.3/progressive-rollout-promoted-20260620.yml"
    )
    latest_path = (
        "metadata/airbyte/source-faker/1.2.3/progressive-rollout-aborted-20260621.yml"
    )
    files = {
        older_path: b"progressive_rollout: true\n",
        latest_path: (
            b"progressive_rollout: true\npromotion_requested_by: ops@example.com\n"
        ),
    }
    _install_fake_gcs(monkeypatch, files)

    marker = get_progressive_rollout_marker("source-faker", "1.2.3", _BUCKET)

    assert marker is not None
    assert marker.state == "aborted"
    assert marker.marker_date == "20260621"
    assert marker.promotion_requested_by == "ops@example.com"


def test_annotate_preserves_keys_and_is_idempotent(monkeypatch) -> None:
    files = {_PATH: b"progressive_rollout: true\ncreated_at: original\ncustom: value\n"}
    _install_fake_gcs(monkeypatch, files)

    first = annotate_progressive_rollout_marker(
        connector_name="source-faker",
        version="1.2.3",
        bucket_name=_BUCKET,
        promotion_requested_at="2026-06-20T15:00:00Z",
        promotion_requested_by="ops@example.com",
        rollout_id="rollout-123",
    )
    second = annotate_progressive_rollout_marker(
        connector_name="source-faker",
        version="1.2.3",
        bucket_name=_BUCKET,
        promotion_requested_at="2026-06-20T16:00:00Z",
        promotion_requested_by="other@example.com",
        rollout_id="rollout-456",
    )

    assert first.success is True
    assert second.success is True
    values = yaml.safe_load(files[_PATH])
    assert values["progressive_rollout"] is True
    assert values["created_at"] == "original"
    assert values["custom"] == "value"
    assert values["promotion_requested_at"] == "2026-06-20T16:00:00Z"
    assert values["promotion_requested_by"] == "other@example.com"
    assert values["rollout_id"] == "rollout-456"


def test_annotate_does_not_write_when_marker_is_absent(monkeypatch) -> None:
    files: dict[str, bytes] = {}
    _install_fake_gcs(monkeypatch, files)

    result = annotate_progressive_rollout_marker(
        connector_name="source-faker",
        version="1.2.3",
        bucket_name=_BUCKET,
        promotion_requested_by="ops@example.com",
        rollout_id="rollout-123",
    )

    assert result.success is False
    assert files == {}


def test_annotate_does_not_write_dated_marker_when_active_marker_is_absent(
    monkeypatch,
) -> None:
    dated_path = (
        "metadata/airbyte/source-faker/1.2.3/progressive-rollout-promoted-20260620.yml"
    )
    files = {dated_path: b"progressive_rollout: true\n"}
    _install_fake_gcs(monkeypatch, files)

    result = annotate_progressive_rollout_marker(
        connector_name="source-faker",
        version="1.2.3",
        bucket_name=_BUCKET,
        promotion_requested_by="ops@example.com",
        rollout_id="rollout-123",
    )

    assert result.success is False
    assert files == {dated_path: b"progressive_rollout: true\n"}


def test_annotate_does_not_recreate_active_marker_after_finalize_race(
    monkeypatch,
) -> None:
    dated_path = (
        "metadata/airbyte/source-faker/1.2.3/progressive-rollout-promoted-20260620.yml"
    )
    files = {dated_path: b"progressive_rollout: true\n"}

    exists_calls = 0

    class FinalizingFileSystem(FakeFileSystem):
        def exists(self, path: str) -> bool:
            nonlocal exists_calls
            exists_calls += 1
            return exists_calls == 1

    monkeypatch.setattr(
        "airbyte_ops_mcp.registry.progressive_rollout_marker.gcsfs.GCSFileSystem",
        lambda **_: FinalizingFileSystem(files),
    )
    monkeypatch.setattr(
        "airbyte_ops_mcp.registry.progressive_rollout_marker.get_gcs_credentials_token",
        lambda: None,
    )
    monkeypatch.setattr(
        "airbyte_ops_mcp.registry.progressive_rollout_marker.get_gcs_storage_client",
        lambda: FakeStorageClient(files),
    )

    result = annotate_progressive_rollout_marker(
        connector_name="source-faker",
        version="1.2.3",
        bucket_name=_BUCKET,
        promotion_requested_by="ops@example.com",
        rollout_id="rollout-123",
    )

    assert result.success is False
    assert files == {dated_path: b"progressive_rollout: true\n"}


def test_finalize_aborted_yanks_before_renaming_marker(monkeypatch) -> None:
    events: list[tuple[str, str]] = []
    files = {
        _PATH: b"progressive_rollout: true\n",
        _METADATA_PATH: b"dockerImageTag: 1.2.3\n",
    }
    _install_fake_gcs(monkeypatch, files, events)

    result = finalize_progressive_rollout_marker(
        connector_name="source-faker",
        store=RegistryStore.parse("coral:prod"),
        outcome="aborted",
        version="1.2.3",
    )

    assert result.success is True
    assert result.yank_path == _YANK_PATH
    assert result.to_dict()["yank_path"] == _YANK_PATH
    assert events[0] == ("upload", _YANK_PATH)
    assert events == [
        ("upload", _YANK_PATH),
        ("copy", result.target_path),
        ("delete", _PATH),
    ]
    marker = yaml.safe_load(files[_YANK_PATH])
    assert marker["yanked"] is True
    assert marker["reason"] == "Progressive rollout of 1.2.3 aborted."


def test_finalize_aborted_does_not_overwrite_existing_yank(monkeypatch) -> None:
    events: list[tuple[str, str]] = []
    files = {
        _PATH: b"progressive_rollout: true\n",
        _METADATA_PATH: b"dockerImageTag: 1.2.3\n",
        _YANK_PATH: b"yanked: true\nreason: existing\n",
    }
    _install_fake_gcs(monkeypatch, files, events)

    result = finalize_progressive_rollout_marker(
        connector_name="source-faker",
        store=RegistryStore.parse("coral:prod"),
        outcome="aborted",
        version="1.2.3",
    )

    assert result.success is True
    assert result.yank_path == _YANK_PATH
    assert "already yanked" in result.message
    assert events == [("copy", result.target_path), ("delete", _PATH)]
    assert files[_YANK_PATH] == b"yanked: true\nreason: existing\n"


def test_finalize_aborted_yanks_when_active_marker_is_missing(monkeypatch) -> None:
    aborted_path = f"{_VERSION_DIR}/progressive-rollout-aborted-20260620.yml"
    files = {
        _METADATA_PATH: b"dockerImageTag: 1.2.3\n",
        aborted_path: b"progressive_rollout: true\n",
    }
    events: list[tuple[str, str]] = []
    _install_fake_gcs(monkeypatch, files, events)

    result = finalize_progressive_rollout_marker(
        connector_name="source-faker",
        store=RegistryStore.parse("coral:prod"),
        outcome="aborted",
        version="1.2.3",
    )

    assert result.success is True
    assert result.yank_path == _YANK_PATH
    assert files[_YANK_PATH]
    assert events == [("upload", _YANK_PATH)]


def test_finalize_aborted_does_not_yank_when_only_promoted_marker_exists(
    monkeypatch,
) -> None:
    promoted_path = f"{_VERSION_DIR}/progressive-rollout-promoted-20260620.yml"
    files = {
        _METADATA_PATH: b"dockerImageTag: 1.2.3\n",
        promoted_path: b"progressive_rollout: true\n",
    }
    events: list[tuple[str, str]] = []
    _install_fake_gcs(monkeypatch, files, events)

    result = finalize_progressive_rollout_marker(
        connector_name="source-faker",
        store=RegistryStore.parse("coral:prod"),
        outcome="aborted",
        version="1.2.3",
    )

    assert result.success is True
    assert result.yank_path is None
    assert "promoted marker" in result.message
    assert _YANK_PATH not in files
    assert events == []


def test_finalize_aborted_does_not_yank_without_audit_marker(monkeypatch) -> None:
    files = {_METADATA_PATH: b"dockerImageTag: 1.2.3\n"}
    events: list[tuple[str, str]] = []
    _install_fake_gcs(monkeypatch, files, events)

    result = finalize_progressive_rollout_marker(
        connector_name="source-faker",
        store=RegistryStore.parse("coral:prod"),
        outcome="aborted",
        version="1.2.3",
    )

    assert result.success is True
    assert result.yank_path is None
    assert "no aborted rollout audit marker" in result.message
    assert _YANK_PATH not in files
    assert events == []


def test_finalize_aborted_skips_yank_when_metadata_is_missing(monkeypatch) -> None:
    files = {_PATH: b"progressive_rollout: true\n"}
    events: list[tuple[str, str]] = []
    _install_fake_gcs(monkeypatch, files, events)

    result = finalize_progressive_rollout_marker(
        connector_name="source-faker",
        store=RegistryStore.parse("coral:prod"),
        outcome="aborted",
        version="1.2.3",
    )

    assert result.success is True
    assert result.yank_path is None
    assert _YANK_PATH not in files
    assert events == [("copy", result.target_path), ("delete", _PATH)]


def test_finalize_promoted_does_not_touch_yank_marker(monkeypatch) -> None:
    events: list[tuple[str, str]] = []
    files = {
        _PATH: b"progressive_rollout: true\n",
        _METADATA_PATH: b"dockerImageTag: 1.2.3\n",
    }
    _install_fake_gcs(monkeypatch, files, events)

    result = finalize_progressive_rollout_marker(
        connector_name="source-faker",
        store=RegistryStore.parse("coral:prod"),
        outcome="promoted",
        version="1.2.3",
    )

    assert result.success is True
    assert result.yank_path is None
    assert events[0][0] == "copy"
    assert all(path != _YANK_PATH for _, path in events)


def test_finalize_aborted_dry_run_does_not_write(monkeypatch) -> None:
    events: list[tuple[str, str]] = []
    files = {
        _PATH: b"progressive_rollout: true\n",
        _METADATA_PATH: b"dockerImageTag: 1.2.3\n",
    }
    _install_fake_gcs(monkeypatch, files, events)

    result = finalize_progressive_rollout_marker(
        connector_name="source-faker",
        store=RegistryStore.parse("coral:prod"),
        outcome="aborted",
        version="1.2.3",
        dry_run=True,
    )

    assert result.success is True
    assert result.yank_path == _YANK_PATH
    assert "write" in result.message
    assert "then rename" in result.message
    assert events == []
    assert set(files) == {_PATH, _METADATA_PATH}


def test_finalize_aborted_dry_run_skips_yank_when_metadata_is_missing(
    monkeypatch,
) -> None:
    events: list[tuple[str, str]] = []
    files = {_PATH: b"progressive_rollout: true\n"}
    _install_fake_gcs(monkeypatch, files, events)

    result = finalize_progressive_rollout_marker(
        connector_name="source-faker",
        store=RegistryStore.parse("coral:prod"),
        outcome="aborted",
        version="1.2.3",
        dry_run=True,
    )

    assert result.success is True
    assert result.yank_path is None
    assert result.target_path is not None
    assert "Skipped yank" in result.message
    assert "would rename" in result.message
    assert events == []
    assert files == {_PATH: b"progressive_rollout: true\n"}


def test_finalize_aborted_dry_run_preserves_existing_yank(monkeypatch) -> None:
    events: list[tuple[str, str]] = []
    files = {
        _PATH: b"progressive_rollout: true\n",
        _METADATA_PATH: b"dockerImageTag: 1.2.3\n",
        _YANK_PATH: b"yanked: true\nreason: existing\n",
    }
    _install_fake_gcs(monkeypatch, files, events)

    result = finalize_progressive_rollout_marker(
        connector_name="source-faker",
        store=RegistryStore.parse("coral:prod"),
        outcome="aborted",
        version="1.2.3",
        dry_run=True,
    )

    assert result.success is True
    assert result.yank_path == _YANK_PATH
    assert "already yanked" in result.message
    assert "would rename" in result.message
    assert events == []
    assert files[_YANK_PATH] == b"yanked: true\nreason: existing\n"


def test_finalize_aborted_dry_run_with_missing_active_marker_reports_no_rename(
    monkeypatch,
) -> None:
    aborted_path = f"{_VERSION_DIR}/progressive-rollout-aborted-20260620.yml"
    files = {
        _METADATA_PATH: b"dockerImageTag: 1.2.3\n",
        aborted_path: b"progressive_rollout: true\n",
    }
    events: list[tuple[str, str]] = []
    _install_fake_gcs(monkeypatch, files, events)

    result = finalize_progressive_rollout_marker(
        connector_name="source-faker",
        store=RegistryStore.parse("coral:prod"),
        outcome="aborted",
        version="1.2.3",
        dry_run=True,
    )

    assert result.success is True
    assert result.yank_path == _YANK_PATH
    assert result.target_path is None
    assert "no active progressive rollout marker" in result.message
    assert "Would write" in result.message
    assert events == []
    assert _YANK_PATH not in files


def test_finalize_aborted_dry_run_skips_yank_for_promoted_audit_marker(
    monkeypatch,
) -> None:
    promoted_path = f"{_VERSION_DIR}/progressive-rollout-promoted-20260620.yml"
    files = {
        _METADATA_PATH: b"dockerImageTag: 1.2.3\n",
        promoted_path: b"progressive_rollout: true\n",
    }
    events: list[tuple[str, str]] = []
    _install_fake_gcs(monkeypatch, files, events)

    result = finalize_progressive_rollout_marker(
        connector_name="source-faker",
        store=RegistryStore.parse("coral:prod"),
        outcome="aborted",
        version="1.2.3",
        dry_run=True,
    )

    assert result.success is True
    assert result.yank_path is None
    assert result.target_path is None
    assert "promoted marker" in result.message
    assert "no active progressive rollout marker" in result.message
    assert events == []
    assert _YANK_PATH not in files


def test_finalize_aborted_yank_path_respects_store_prefix(monkeypatch) -> None:
    prefix = "test-prefix"
    prefixed_path = f"{prefix}/{_PATH}"
    prefixed_metadata = f"{prefix}/{_METADATA_PATH}"
    prefixed_yank = f"{prefix}/{_YANK_PATH}"
    files = {
        prefixed_path: b"progressive_rollout: true\n",
        prefixed_metadata: b"dockerImageTag: 1.2.3\n",
    }
    _install_fake_gcs(monkeypatch, files)

    result = finalize_progressive_rollout_marker(
        connector_name="source-faker",
        store=RegistryStore.parse(f"coral:prod/{prefix}"),
        outcome="aborted",
        version="1.2.3",
    )

    assert result.yank_path == prefixed_yank
    assert prefixed_yank in files
