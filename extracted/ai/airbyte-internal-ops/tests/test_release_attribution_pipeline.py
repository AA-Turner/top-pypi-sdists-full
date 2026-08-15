# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for release attribution persistence in compiled version indexes."""

from __future__ import annotations

import io
from typing import Literal

import pytest
import yaml

from airbyte_ops_mcp.registry.compile import (
    _build_version_index,
    _read_previous_version_index,
    _version_index_is_unchanged,
)
from airbyte_ops_mcp.registry.release_attribution import ReleaseAttribution
from airbyte_ops_mcp.registry.store import RegistryStore


class CountingFileSystem:
    """Small in-memory filesystem that counts metadata reads."""

    def __init__(self, files: dict[str, str]) -> None:
        self.files = files
        self.reads: list[str] = []

    def open(self, path: str, mode: str = "r") -> io.StringIO:
        if "r" in mode:
            self.reads.append(path)
            if path not in self.files:
                raise FileNotFoundError(path)
            return io.StringIO(self.files[path])
        raise AssertionError(f"Unexpected write: {path}")


class FlakyFileSystem(CountingFileSystem):
    """Filesystem that fails once for a selected metadata path."""

    def __init__(self, files: dict[str, str], failing_path: str) -> None:
        super().__init__(files)
        self.failing_path = failing_path
        self.failed = False

    def open(self, path: str, mode: str = "r") -> io.StringIO:
        if path == self.failing_path and not self.failed:
            self.reads.append(path)
            self.failed = True
            raise OSError("transient read failure")
        return super().open(path, mode)


def _release(
    pr_number: int,
    source: Literal["publish", "git-backfill", "prerelease", "changelog"] = "publish",
) -> dict:
    return ReleaseAttribution(
        pr_number=pr_number,
        pr_url=f"https://github.com/airbytehq/airbyte/pull/{pr_number}",
        source=source,
    ).model_dump(mode="json")


@pytest.mark.unit
@pytest.mark.parametrize(
    "has_prior_release",
    [
        pytest.param(True, id="carry_forward_existing_release"),
        pytest.param(False, id="historical_without_release_stays_frozen"),
    ],
)
def test_historical_entries_avoid_metadata_reads(has_prior_release: bool) -> None:
    """Historical entries avoid metadata reads while latest metadata is read."""
    store = RegistryStore.parse("coral:dev/test")
    latest_path = (
        f"{store.bucket_root}/metadata/airbyte/source-test/1.1.0/metadata.yaml"
    )
    fs = CountingFileSystem(
        {latest_path: yaml.safe_dump({"data": {"definitionId": "definition"}})}
    )
    index = _build_version_index(
        fs,
        store=store,
        connector="source-test",
        versions=["1.1.0", "1.0.0"],
        yanked=set(),
        latest_version="1.1.0",
        previous_index={
            "connector": "source-test",
            "versions": [
                (
                    {"version": "1.1.0", "release": _release(11)}
                    if has_prior_release
                    else {"version": "1.1.0"}
                ),
                (
                    {"version": "1.0.0", "release": _release(10)}
                    if has_prior_release
                    else {"version": "1.0.0"}
                ),
            ],
        },
    )
    if has_prior_release:
        assert index["versions"][1]["release"]["pr_number"] == 10
    else:
        assert "release" not in index["versions"][1]
    assert fs.reads == [latest_path]


@pytest.mark.unit
def test_definition_id_carries_forward_when_latest_metadata_is_unavailable(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """A missing latest entry does not discard the prior definition ID."""
    store = RegistryStore.parse("coral:dev/test")
    fs = CountingFileSystem({})
    index = _build_version_index(
        fs,
        store=store,
        connector="source-test",
        versions=["1.0.0"],
        yanked=set(),
        latest_version="1.1.0",
        previous_index={
            "connector": "source-test",
            "definition_id": "definition",
            "versions": [{"version": "1.0.0"}],
        },
    )
    assert index["definition_id"] == "definition"
    assert "Could not read metadata for latest version" in caplog.text


@pytest.mark.unit
@pytest.mark.parametrize(
    "full_restate",
    [
        pytest.param(False, id="new_version"),
        pytest.param(True, id="full_restate"),
    ],
)
def test_new_version_metadata_release_scenarios(full_restate: bool) -> None:
    """New and restated versions are enriched from metadata."""
    store = RegistryStore.parse("coral:dev/test")
    metadata_path = (
        f"{store.bucket_root}/metadata/airbyte/source-test/1.1.0/metadata.yaml"
    )
    fs = CountingFileSystem(
        {
            metadata_path: yaml.safe_dump(
                {"data": {"generated": {"release": _release(11)}}}
            )
        }
    )
    index = _build_version_index(
        fs,
        store=store,
        connector="source-test",
        versions=["1.1.0"],
        yanked=set(),
        latest_version=None,
        previous_index={
            "connector": "source-test",
            "versions": (
                [{"version": "1.1.0", "release": _release(10)}] if full_restate else []
            ),
        },
        full_restate=full_restate,
    )
    assert index["versions"][0]["release"]["pr_number"] == 11
    assert fs.reads == [metadata_path]


@pytest.mark.unit
def test_existing_released_at_survives_non_restate_compile() -> None:
    """A prior release timestamp is preserved when recompiling normally."""
    store = RegistryStore.parse("coral:dev/test")
    released_at = "2025-01-02T03:04:05Z"
    prior_release = _release(10)
    prior_release["released_at"] = released_at
    fs = CountingFileSystem({})
    index = _build_version_index(
        fs,
        store=store,
        connector="source-test",
        versions=["1.0.0"],
        yanked=set(),
        latest_version=None,
        previous_index={
            "connector": "source-test",
            "versions": [{"version": "1.0.0", "release": prior_release}],
        },
        full_restate=False,
    )
    assert index["versions"][0]["release"]["released_at"] == released_at


@pytest.mark.unit
def test_full_restate_preserves_supplied_attribution_index() -> None:
    """A full restate keeps historical releases supplied by the Git index."""
    store = RegistryStore.parse("coral:dev/test")
    latest_path = (
        f"{store.bucket_root}/metadata/airbyte/source-test/1.1.0/metadata.yaml"
    )
    fs = CountingFileSystem(
        {latest_path: yaml.safe_dump({"data": {"definitionId": "definition"}})}
    )
    release_index = {"1.0.0": ReleaseAttribution(pr_number=10, source="git-backfill")}
    seeded = _build_version_index(
        fs,
        store=store,
        connector="source-test",
        versions=["1.1.0", "1.0.0"],
        yanked=set(),
        latest_version="1.1.0",
        previous_index={"connector": "source-test", "versions": []},
        release_attribution=release_index,
    )
    restated = _build_version_index(
        fs,
        store=store,
        connector="source-test",
        versions=["1.1.0", "1.0.0"],
        yanked=set(),
        latest_version="1.1.0",
        previous_index=seeded,
        full_restate=True,
        release_attribution=release_index,
    )
    assert restated["versions"][1]["release"]["pr_number"] == 10
    assert restated["versions"][1]["release"]["source"] == "git-backfill"


@pytest.mark.unit
def test_release_seed_avoids_metadata_read() -> None:
    """A backfill index can seed a missing release block directly."""
    store = RegistryStore.parse("coral:dev/test")
    fs = CountingFileSystem({})
    index = _build_version_index(
        fs,
        store=store,
        connector="source-test",
        versions=["1.0.0"],
        yanked=set(),
        latest_version=None,
        release_attribution={
            "1.0.0": ReleaseAttribution(pr_number=99, source="git-backfill")
        },
    )
    assert index["versions"][0]["release"]["source"] == "git-backfill"
    assert fs.reads == []


@pytest.mark.unit
@pytest.mark.parametrize(
    ("read_fails", "expected_reads"),
    [
        pytest.param(True, 2, id="failed_read_retries"),
        pytest.param(False, 1, id="successful_missing_release_is_terminal"),
    ],
)
def test_release_read_retry_scenarios(
    read_fails: bool,
    expected_reads: int,
) -> None:
    """Only failed metadata reads are retried."""
    store = RegistryStore.parse("coral:dev/test")
    metadata_path = (
        f"{store.bucket_root}/metadata/airbyte/source-test/1.0.0/metadata.yaml"
    )
    if read_fails:
        fs = FlakyFileSystem(
            {
                metadata_path: yaml.safe_dump(
                    {"data": {"generated": {"release": _release(22)}}}
                )
            },
            metadata_path,
        )
    else:
        fs = CountingFileSystem({metadata_path: yaml.safe_dump({"data": {}})})
    first_index = _build_version_index(
        fs,
        store=store,
        connector="source-test",
        versions=["1.0.0"],
        yanked=set(),
        latest_version=None,
        previous_index={"connector": "source-test", "versions": []},
    )
    second_index = _build_version_index(
        fs,
        store=store,
        connector="source-test",
        versions=["1.0.0"],
        yanked=set(),
        latest_version=None,
        previous_index=first_index,
    )
    assert "release" not in first_index["versions"][0]
    if read_fails:
        assert first_index["versions"][0]["release_pending"] is True
        assert second_index["versions"][0]["release"]["pr_number"] == 22
        assert "release_pending" not in second_index["versions"][0]
    else:
        assert second_index == first_index
        assert "release_pending" not in first_index["versions"][0]
    assert fs.reads == [metadata_path] * expected_reads


@pytest.mark.unit
def test_corrupt_prior_index_falls_back(caplog: pytest.LogCaptureFixture) -> None:
    """Malformed prior indexes return `None` and log a warning."""
    fs = CountingFileSystem({"index.json": "{not-json"})
    assert (
        _read_previous_version_index(fs, "index.json", connector="source-test") is None
    )
    assert "corrupt" in caplog.text or "Could not read" in caplog.text


@pytest.mark.unit
def test_unchanged_version_index_is_detected_for_write_skip() -> None:
    """Equivalent serialized indexes are identified without a write."""
    index = {"connector": "source-test", "versions": [{"version": "1.0.0"}]}
    assert _version_index_is_unchanged(index, dict(index))
    assert not _version_index_is_unchanged(
        index, {"connector": "source-test", "versions": []}
    )
