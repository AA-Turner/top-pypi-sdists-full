import json
import os
import sys
from pathlib import Path
from unittest import mock

import pytest

from runlayer_cli.scan import artifact_cache
from runlayer_cli.scan.artifact_cache import ArtifactCache


def _cache(
    path: Path,
    *,
    host: str = "https://example.runlayer.com",
    api_key: str = "rl_org_test",
    now=lambda: 1_000.0,
    ttl_seconds: float = 100.0,
    max_entries: int = 10,
) -> ArtifactCache:
    return ArtifactCache(
        host,
        api_key,
        cache_path=path,
        now=now,
        ttl_seconds=ttl_seconds,
        max_entries=max_entries,
    )


def test_round_trip_and_evict(tmp_path: Path) -> None:
    path = tmp_path / "artifact-cache.json"
    cache = _cache(path)

    assert cache.contains("known") is False
    cache.record("known")
    assert cache.contains("known") is True

    reloaded = _cache(path)
    assert reloaded.contains("known") is True

    reloaded.evict("known")
    assert reloaded.contains("known") is False
    assert _cache(path).contains("known") is False


@pytest.mark.parametrize(
    "contents",
    [
        "not json",
        "[]",
        '{"version": 1}',
    ],
)
def test_corrupt_payload_is_a_miss(tmp_path: Path, contents: str) -> None:
    path = tmp_path / "artifact-cache.json"
    path.write_text(contents, encoding="utf-8")

    assert _cache(path).contains("known") is False


def test_oversized_cache_file_is_rejected_without_loading(tmp_path: Path) -> None:
    path = tmp_path / "artifact-cache.json"
    with path.open("wb") as handle:
        handle.truncate(artifact_cache.ARTIFACT_CACHE_MAX_FILE_BYTES + 1)

    with mock.patch.object(artifact_cache.logger, "warning") as warning_mock:
        assert _cache(path).contains("known") is False

    warning_mock.assert_called_once_with(
        "artifact_cache_integrity_mismatch",
        reason="file_too_large",
    )


def test_version_mismatch_is_a_miss(tmp_path: Path) -> None:
    path = tmp_path / "artifact-cache.json"
    cache = _cache(path)
    cache.record("known")
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version"] = 2
    path.write_text(json.dumps(payload), encoding="utf-8")

    assert _cache(path).contains("known") is False


@pytest.mark.parametrize(
    ("host", "api_key"),
    [
        ("https://other.runlayer.com", "rl_org_test"),
        ("https://example.runlayer.com", "rl_org_other"),
    ],
)
def test_host_or_api_key_mismatch_is_a_miss(
    tmp_path: Path,
    host: str,
    api_key: str,
) -> None:
    path = tmp_path / "artifact-cache.json"
    cache = _cache(path)
    cache.record("known")

    assert _cache(path, host=host, api_key=api_key).contains("known") is False


def test_tampered_entries_invalidate_entire_cache(tmp_path: Path) -> None:
    path = tmp_path / "artifact-cache.json"
    cache = _cache(path)
    cache.record("known")

    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["entries"]["planted"] = 1_000.0
    path.write_text(json.dumps(payload), encoding="utf-8")

    reloaded = _cache(path)
    assert reloaded.contains("known") is False
    assert reloaded.contains("planted") is False


def test_entry_expires_after_ttl(tmp_path: Path) -> None:
    path = tmp_path / "artifact-cache.json"
    clock = [1_000.0]
    cache = _cache(path, now=lambda: clock[0], ttl_seconds=100.0)
    cache.record("known")

    clock[0] = 1_099.0
    assert cache.contains("known") is True

    clock[0] = 1_101.0
    assert cache.contains("known") is False
    assert (
        _cache(
            path,
            now=lambda: clock[0],
            ttl_seconds=100.0,
        ).contains("known")
        is False
    )


def test_entry_cap_evicts_oldest(tmp_path: Path) -> None:
    path = tmp_path / "artifact-cache.json"
    clock = [1_000.0]
    cache = _cache(
        path,
        now=lambda: clock[0],
        ttl_seconds=1_000.0,
        max_entries=3,
    )
    for identifier in ("one", "two", "three", "four"):
        cache.record(identifier)
        clock[0] += 1

    assert cache.contains("one") is False
    assert all(cache.contains(identifier) for identifier in ("two", "three", "four"))


def test_write_failure_is_non_fatal(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    path = tmp_path / "artifact-cache.json"
    cache = _cache(path)

    def fail_replace(_source: str, _destination: Path) -> None:
        raise OSError("read-only filesystem")

    monkeypatch.setattr(artifact_cache.os, "replace", fail_replace)

    cache.record("known")
    cache.evict("known")
    assert cache.contains("known") is False


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX mode bits")
def test_cache_file_is_owner_only(tmp_path: Path) -> None:
    path = tmp_path / "artifact-cache.json"
    _cache(path).record("known")

    assert os.stat(path).st_mode & 0o777 == 0o600
