from __future__ import annotations

import yaml

from airbyte_ops_mcp.registry.yank import yank_connector_version


class FakeBlob:
    def __init__(self, exists: bool = False) -> None:
        self._exists = exists
        self.uploaded_content = ""
        self.content_type = ""

    def exists(self) -> bool:
        return self._exists

    def upload_from_string(self, content: str, content_type: str) -> None:
        self.uploaded_content = content
        self.content_type = content_type


class FakeBucket:
    def __init__(self) -> None:
        self.blobs: dict[str, FakeBlob] = {}

    def blob(self, path: str) -> FakeBlob:
        return self.blobs[path]


class FakeStorageClient:
    def __init__(self, bucket: FakeBucket) -> None:
        self.bucket_value = bucket

    def bucket(self, bucket_name: str) -> FakeBucket:
        return self.bucket_value


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
