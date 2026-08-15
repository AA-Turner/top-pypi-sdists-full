# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for read-only compile dry runs."""

from __future__ import annotations

import io
import json
import os
from dataclasses import replace
from pathlib import Path
from typing import Callable

import pytest

import airbyte_ops_mcp.registry.compare as compare_module
import airbyte_ops_mcp.registry.compile as compile_module
from airbyte_ops_mcp.registry._constants import DEV_METADATA_SERVICE_BUCKET_NAME
from airbyte_ops_mcp.registry._gcs_helpers import get_gcs_storage_client
from airbyte_ops_mcp.registry.store import RegistryStore


class _RecordingFileSystem:
    """Minimal filesystem double that records writes and rejects source writes."""

    def __init__(self, *, reject_writes: bool) -> None:
        self.reject_writes = reject_writes
        self.writes: list[str] = []

    def open(self, path: str, mode: str = "r") -> io.StringIO:
        if "w" in mode:
            if self.reject_writes:
                raise AssertionError(f"source write attempted: {path}")
            self.writes.append(path)
        return io.StringIO()

    def exists(self, path: str) -> bool:
        return False

    def glob(self, path: str) -> list[str]:
        return []

    def rm(self, path: str, recursive: bool = False) -> None:
        if self.reject_writes:
            raise AssertionError(f"source delete attempted: {path}")

    def copy(self, source: str, destination: str, recursive: bool = False) -> None:
        if self.reject_writes:
            raise AssertionError(f"source copy attempted: {source}")

    def makedirs(self, path: str, exist_ok: bool = False) -> None:
        return None

    def mv(self, path1: str, path2: str, recursive: bool = False) -> None:
        return None

    def touch(self, path: str, truncate: bool = True, **kwargs: object) -> None:
        return None

    def mkdir(self, path: str, create_parents: bool = True, **kwargs: object) -> None:
        return None

    def rmdir(self, path: str) -> None:
        return None


@pytest.mark.unit
@pytest.mark.parametrize(
    "operation",
    [
        pytest.param(lambda fs: fs.rm("path"), id="rm"),
        pytest.param(lambda fs: fs.copy("source", "destination"), id="copy"),
        pytest.param(lambda fs: fs.mv("source", "destination"), id="mv"),
        pytest.param(lambda fs: fs.makedirs("path"), id="makedirs"),
        pytest.param(lambda fs: fs.touch("path"), id="touch"),
        pytest.param(lambda fs: fs.mkdir("path"), id="mkdir"),
        pytest.param(lambda fs: fs.rmdir("path"), id="rmdir"),
    ],
)
@pytest.mark.parametrize(
    "target",
    [
        pytest.param("coral:local:/tmp/registry-test", id="local_store"),
        pytest.param("coral:dev", id="gcs_store"),
    ],
)
def test_read_only_filesystem_rejects_mutations(
    monkeypatch: pytest.MonkeyPatch,
    operation: Callable[[compile_module._ReadOnlyRegistryFileSystem], None],
    target: str,
) -> None:
    """The source proxy rejects every filesystem mutation operation."""
    raw_filesystem = _RecordingFileSystem(reject_writes=False)
    monkeypatch.setattr(
        compile_module.fsspec,
        "filesystem",
        lambda filesystem_name: raw_filesystem,
    )
    monkeypatch.setattr(
        compile_module.gcsfs,
        "GCSFileSystem",
        lambda token: raw_filesystem,
    )
    filesystem = compile_module._filesystem_for_store(
        replace(RegistryStore.parse(target), read_only=True)
    )
    assert isinstance(filesystem, compile_module._ReadOnlyRegistryFileSystem)
    with pytest.raises(PermissionError, match="Read-only"):
        operation(filesystem)


@pytest.mark.unit
def test_compile_output_store_never_writes_source(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """A separate output store makes source mutations structurally unreachable."""
    source_fs = _RecordingFileSystem(reject_writes=True)
    output_fs = _RecordingFileSystem(reject_writes=False)

    monkeypatch.setattr(
        compile_module.gcsfs,
        "GCSFileSystem",
        lambda token: source_fs,
    )
    monkeypatch.setattr(
        compile_module.fsspec,
        "filesystem",
        lambda filesystem_name: output_fs,
    )
    monkeypatch.setattr(
        compile_module,
        "_scan_versions_and_markers",
        lambda *args, **kwargs: ({}, set(), set()),
    )
    registry_source_modes: list[bool] = []

    def capture_registry_source_mode(
        *args: object, **kwargs: object
    ) -> list[dict[str, object]]:
        registry_source_modes.append(bool(kwargs["source_from_version_dirs"]))
        return []

    monkeypatch.setattr(
        compile_module,
        "_compile_global_registry",
        capture_registry_source_mode,
    )

    source = RegistryStore.parse("coral:prod")
    output = RegistryStore.parse(f"coral:local:{tmp_path}")
    result = compile_module.compile_registry(
        store=source,
        output_store=output,
        with_metrics=False,
    )

    assert result.status == "success"
    assert source_fs.writes == []
    assert output_fs.writes
    assert registry_source_modes == [True, True]


@pytest.mark.unit
def test_compile_output_store_carries_forward_source_release_data(
    tmp_path: Path,
) -> None:
    """An output-store compile preserves release data from the source index."""
    source_root = tmp_path / "source"
    metadata_root = source_root / "metadata/airbyte/source-test/1.0.0"
    metadata_root.mkdir(parents=True)
    (metadata_root / "metadata.yaml").write_text(
        "data:\n  definitionId: definition-id\n",
    )
    (source_root / "metadata/airbyte/source-test/versions.json").write_text(
        json.dumps(
            {
                "connector": "source-test",
                "versions": [
                    {
                        "version": "1.0.0",
                        "yanked": False,
                        "is_latest": True,
                        "release": {"pr_number": 123},
                    }
                ],
            }
        )
    )

    result = compile_module.compile_registry(
        store=RegistryStore.parse(f"coral:local:{source_root}"),
        output_store=RegistryStore.parse(f"coral:local:{tmp_path / 'output'}"),
        with_metrics=False,
    )

    assert result.errors == []
    output_index = json.loads(
        (tmp_path / "output/metadata/airbyte/source-test/versions.json").read_text()
    )
    assert output_index["versions"][0]["release"] == {"pr_number": 123}


@pytest.mark.unit
def test_compile_rejects_production_output_store() -> None:
    """Production registry stores cannot be compile output targets."""
    with pytest.raises(
        ValueError, match="Production stores cannot be compile output targets"
    ):
        compile_module.compile_registry(
            store=RegistryStore.parse("coral:dev"),
            output_store=RegistryStore.parse("coral:prod"),
        )


@pytest.mark.unit
def test_compile_rejects_mismatched_output_registry() -> None:
    """Compile output must retain the source registry identity."""
    with pytest.raises(ValueError, match=r"same registry type.*coral.*sonar"):
        compile_module.compile_registry(
            store=RegistryStore.parse("coral:dev"),
            output_store=RegistryStore.parse("sonar:local:/tmp/output"),
        )


def _snapshot_dev_registry_objects() -> dict[str, tuple[int | None, str | None]]:
    client = get_gcs_storage_client()
    snapshot: dict[str, tuple[int | None, str | None]] = {}
    for prefix in ("metadata/", "registries/v0/"):
        for blob in client.list_blobs(DEV_METADATA_SERVICE_BUCKET_NAME, prefix=prefix):
            if prefix == "metadata/" and not blob.name.endswith("/versions.json"):
                continue
            snapshot[blob.name] = (
                blob.generation,
                blob.updated.isoformat() if blob.updated is not None else None,
            )
    return snapshot


@pytest.mark.integration
@pytest.mark.gcs_integration
def test_dev_compile_dry_run_does_not_write_source(tmp_path: Path) -> None:
    """A real dev dry run leaves every writable source object unchanged."""
    if not (os.environ.get("GCS_CREDENTIALS") or os.environ.get("GCP_GSM_CREDENTIALS")):
        pytest.skip(
            "No explicit GCS credential configured for dev-bucket integration test."
        )

    source = RegistryStore.parse("coral:dev")
    output = RegistryStore.parse(f"coral:local:{tmp_path / 'dry-run'}")
    before = _snapshot_dev_registry_objects()

    result = compile_module.compile_registry(
        store=source,
        output_store=output,
        with_secrets_mask=True,
    )

    assert result.errors == []
    assert result.connectors_scanned > 0
    assert all(
        (tmp_path / "dry-run" / "registries" / "v0" / filename).is_file()
        for filename in (
            "cloud_registry.json",
            "oss_registry.json",
            "composite_registry.json",
        )
    )
    assert list((tmp_path / "dry-run" / "metadata").glob("airbyte/*/versions.json"))

    after = _snapshot_dev_registry_objects()
    assert after == before

    comparison = compare_module.compare_stores(
        RegistryStore.parse(f"coral:local:{tmp_path / 'dry-run'}"),
        RegistryStore.parse("coral:dev"),
        with_artifacts=False,
    )
    assert comparison.errors == []
    assert comparison.connectors_only_in_store == []
    assert comparison.connectors_only_in_reference == []
