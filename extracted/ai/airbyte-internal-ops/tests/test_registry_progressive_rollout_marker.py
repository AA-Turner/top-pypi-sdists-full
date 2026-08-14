from __future__ import annotations

import yaml

from airbyte_ops_mcp.registry.progressive_rollout_marker import (
    annotate_progressive_rollout_marker,
    get_progressive_rollout_marker,
)

_BUCKET = "prod-airbyte-cloud-connector-metadata-service"
_PATH = "metadata/airbyte/source-faker/1.2.3/progressive-rollout.yml"


class FakeBlob:
    def __init__(self, files: dict[str, bytes], path: str) -> None:
        self.files = files
        self.path = path

    def upload_from_string(self, content: str, content_type: str) -> None:
        assert content_type == "application/x-yaml"
        self.files[self.path] = content.encode("utf-8")


class FakeStorageClient:
    def __init__(self, files: dict[str, bytes]) -> None:
        self.files = files

    def bucket(self, bucket_name: str) -> FakeStorageClient:
        assert bucket_name == _BUCKET
        return self

    def blob(self, path: str) -> FakeBlob:
        return FakeBlob(self.files, path)


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


def _install_fake_gcs(monkeypatch, files: dict[str, bytes]) -> None:
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
        lambda: FakeStorageClient(files),
    )


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
