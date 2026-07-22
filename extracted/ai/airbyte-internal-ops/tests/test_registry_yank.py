from __future__ import annotations

import re

import pytest
import yaml

from airbyte_ops_mcp.registry.coral_registry_store import CoralRegistry
from airbyte_ops_mcp.registry.store import RegistryStore
from airbyte_ops_mcp.registry.yank import (
    YankedVersion,
    YankMarkerDetail,
    _yanked_version_from_marker_path,
    get_yank_marker,
    list_yanked_versions,
    yank_connector_version,
)


class FakeBlob:
    def __init__(
        self,
        exists: bool = False,
        *,
        name: str = "",
        content: bytes = b"",
    ) -> None:
        self._exists = exists
        self.name = name
        self._content = content
        self.uploaded_content = ""
        self.content_type = ""

    def exists(self) -> bool:
        return self._exists

    def upload_from_string(self, content: str, content_type: str) -> None:
        self.uploaded_content = content
        self.content_type = content_type

    def download_as_text(self) -> str:
        return self._content.decode("utf-8")


class FakeBucket:
    def __init__(self) -> None:
        self.blobs: dict[str, FakeBlob] = {}

    def blob(self, path: str) -> FakeBlob:
        return self.blobs[path]


def _glob_to_regex(pattern: str) -> re.Pattern[str]:
    """Translate a GCS `matchGlob` pattern (`*` not crossing `/`) to a regex."""
    out = ["^"]
    i = 0
    while i < len(pattern):
        char = pattern[i]
        if char == "*":
            if pattern[i : i + 2] == "**":
                out.append(".*")
                i += 2
                continue
            out.append("[^/]*")
        else:
            out.append(re.escape(char))
        i += 1
    out.append("$")
    return re.compile("".join(out))


class FakeStorageClient:
    def __init__(
        self,
        bucket: FakeBucket | None = None,
        *,
        blobs: dict[str, bytes] | None = None,
    ) -> None:
        self.bucket_value = bucket
        self._blobs = blobs or {}

    def bucket(self, bucket_name: str) -> FakeBucket:
        assert self.bucket_value is not None
        return self.bucket_value

    def list_blobs(self, bucket_name: str, *, match_glob: str) -> list[FakeBlob]:
        matcher = _glob_to_regex(match_glob)
        return [
            FakeBlob(name=name, content=content)
            for name, content in sorted(self._blobs.items())
            if matcher.match(name)
        ]


def test_yank_connector_version_records_approval_url(monkeypatch) -> None:
    bucket = FakeBucket()
    metadata_path = "metadata/airbyte/source-faker/1.2.3/metadata.yaml"
    yank_path = "metadata/airbyte/source-faker/1.2.3/version-yank.yml"
    bucket.blobs[metadata_path] = FakeBlob(exists=True)
    bucket.blobs[yank_path] = FakeBlob(exists=False)

    monkeypatch.setattr(
        "airbyte_ops_mcp.registry.yank.get_gcs_storage_client",
        lambda: FakeStorageClient(bucket),
    )

    result = yank_connector_version(
        connector_name="source-faker",
        version="1.2.3",
        bucket_name="prod-airbyte-cloud-connector-metadata-service",
        reason="bad release",
        approval_url="https://github.com/airbytehq/airbyte/pull/123#issuecomment-456",
    )

    assert result.success is True
    assert bucket.blobs[yank_path].content_type == "application/x-yaml"
    marker = yaml.safe_load(bucket.blobs[yank_path].uploaded_content)
    assert marker["approval_url"] == (
        "https://github.com/airbytehq/airbyte/pull/123#issuecomment-456"
    )
    assert marker["reason"] == "bad release"


_BUCKET = "prod-airbyte-cloud-connector-metadata-service"
_BASE = f"{_BUCKET}/metadata/airbyte"


@pytest.mark.parametrize(
    "path, expected",
    [
        pytest.param(
            f"{_BASE}/source-faker/1.2.3/version-yank.yml",
            ("source-faker", "1.2.3"),
            id="well-formed",
        ),
        pytest.param(
            f"{_BASE}/destination-snowflake/3.2.0/version-yank.yml",
            ("destination-snowflake", "3.2.0"),
            id="destination",
        ),
        pytest.param("some/other/path.yml", None, id="outside-base"),
        pytest.param(f"{_BASE}/only-two-parts.yml", None, id="too-shallow"),
        pytest.param(
            f"{_BASE}/source-faker/1.2.3/metadata.yaml",
            None,
            id="wrong-filename",
        ),
        pytest.param(
            f"{_BASE}/source-faker/1.2.3/extra/version-yank.yml",
            None,
            id="too-deep",
        ),
    ],
)
def test_yanked_version_from_marker_path(
    path: str,
    expected: tuple[str, str] | None,
) -> None:
    assert _yanked_version_from_marker_path(path, base=_BASE) == expected


class FakeGCSFileSystem:
    """Minimal `gcsfs.GCSFileSystem` stand-in for `exists` + `cat_file`."""

    def __init__(self, files: dict[str, bytes]) -> None:
        self._files = files

    def __call__(self, *args: object, **kwargs: object) -> FakeGCSFileSystem:
        return self

    def exists(self, path: str) -> bool:
        return path in self._files

    def cat_file(self, path: str) -> bytes:
        return self._files[path]


def test_list_yanked_versions(monkeypatch) -> None:
    blobs = {
        "metadata/airbyte/source-faker/1.2.3/version-yank.yml": yaml.safe_dump(
            {
                "yanked": True,
                "yanked_at": "2026-06-18T14:30:00Z",
                "reason": "bad release",
                "approval_url": "https://github.com/airbytehq/airbyte/pull/1",
            }
        ).encode("utf-8"),
        "metadata/airbyte/destination-snowflake/3.2.0/version-yank.yml": b"not: [valid",
        # Decoys the server-side `matchGlob` must exclude: a non-marker file and
        # a too-deep path that `*/*/version-yank.yml` should not match.
        "metadata/airbyte/source-faker/1.2.3/metadata.yaml": b"irrelevant",
        "metadata/airbyte/source-faker/1.2.3/nested/version-yank.yml": b"too: deep",
    }
    monkeypatch.setattr(
        "airbyte_ops_mcp.registry.yank.get_gcs_storage_client",
        lambda: FakeStorageClient(blobs=blobs),
    )

    result = list_yanked_versions(_BUCKET)

    assert result == [
        YankedVersion(
            connector_name="destination-snowflake",
            version="3.2.0",
        ),
        YankedVersion(
            connector_name="source-faker",
            version="1.2.3",
            yanked_at="2026-06-18T14:30:00Z",
            reason="bad release",
            approval_url="https://github.com/airbytehq/airbyte/pull/1",
        ),
    ]


def _install_fake_fs(monkeypatch, files: dict[str, bytes]) -> None:
    monkeypatch.setattr(
        "airbyte_ops_mcp.registry.yank.gcsfs.GCSFileSystem",
        FakeGCSFileSystem(files),
    )
    monkeypatch.setattr(
        "airbyte_ops_mcp.registry.yank.get_gcs_credentials_token",
        lambda: None,
    )


def test_get_yank_marker_returns_parsed_detail_and_raw(monkeypatch) -> None:
    raw = yaml.safe_dump(
        {
            "yanked": True,
            "yanked_at": "2026-06-18T14:30:00Z",
            "reason": "bad release",
            "approval_url": "https://github.com/airbytehq/airbyte/pull/1",
        }
    )
    path = f"{_BASE}/source-faker/1.2.3/version-yank.yml"
    _install_fake_fs(monkeypatch, {path: raw.encode("utf-8")})

    marker = get_yank_marker("source-faker", "1.2.3", _BUCKET)

    assert marker == YankMarkerDetail(
        connector_name="source-faker",
        version="1.2.3",
        yanked_at="2026-06-18T14:30:00Z",
        reason="bad release",
        approval_url="https://github.com/airbytehq/airbyte/pull/1",
        raw=raw,
    )


def test_get_yank_marker_returns_none_when_not_yanked(monkeypatch) -> None:
    _install_fake_fs(monkeypatch, {})

    assert get_yank_marker("source-faker", "9.9.9", _BUCKET) is None


def test_coral_registry_list_yanked_versions_delegates(monkeypatch) -> None:
    captured: dict[str, object] = {}
    sentinel = [YankedVersion(connector_name="source-faker", version="1.2.3")]

    def fake_list(*, bucket_name: str, with_details: bool) -> list[YankedVersion]:
        captured["bucket_name"] = bucket_name
        captured["with_details"] = with_details
        return sentinel

    monkeypatch.setattr(
        "airbyte_ops_mcp.registry.coral_registry_store.list_yanked_versions",
        fake_list,
    )

    registry = CoralRegistry(RegistryStore.parse("coral:prod"))
    result = registry.list_yanked_versions()

    assert result is sentinel
    assert captured["bucket_name"] == registry.bucket_name
    assert captured["with_details"] is True


def test_coral_registry_get_yank_marker_delegates(monkeypatch) -> None:
    captured: dict[str, object] = {}
    sentinel = YankMarkerDetail(connector_name="source-faker", version="1.2.3")

    def fake_get(
        *, connector_name: str, version: str, bucket_name: str
    ) -> YankMarkerDetail:
        captured["connector_name"] = connector_name
        captured["version"] = version
        captured["bucket_name"] = bucket_name
        return sentinel

    monkeypatch.setattr(
        "airbyte_ops_mcp.registry.coral_registry_store.get_yank_marker",
        fake_get,
    )

    registry = CoralRegistry(RegistryStore.parse("coral:prod"))
    result = registry.get_yank_marker("source-faker", "1.2.3")

    assert result is sentinel
    assert captured["connector_name"] == "source-faker"
    assert captured["version"] == "1.2.3"
    assert captured["bucket_name"] == registry.bucket_name
