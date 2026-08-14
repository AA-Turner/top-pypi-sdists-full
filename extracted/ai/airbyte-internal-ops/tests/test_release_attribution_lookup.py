"""Tests for registry release attribution lookup paths."""

from __future__ import annotations

import io
import json
from collections.abc import Callable
from datetime import datetime, timezone

import pytest

import airbyte_ops_mcp.registry.release_attribution as release_attribution
from airbyte_ops_mcp.registry.store import RegistryStore


class FakeFileSystem:
    """Small in-memory filesystem for registry lookup tests."""

    def __init__(self, files: dict[str, str]) -> None:
        self.files = files
        self.reads: list[str] = []

    def open(self, path: str, mode: str = "r") -> io.StringIO:
        del mode
        self.reads.append(path)
        if path not in self.files:
            raise FileNotFoundError(path)
        return io.StringIO(self.files[path])


def _store() -> RegistryStore:
    return RegistryStore.parse("coral:dev")


def _index_path() -> str:
    return "dev-airbyte-cloud-connector-metadata-service-2/metadata/airbyte/source-test/versions.json"


def _metadata_path(version: str) -> str:
    return f"dev-airbyte-cloud-connector-metadata-service-2/metadata/airbyte/source-test/{version}/metadata.yaml"


def _doc_path(version: str) -> str:
    return f"dev-airbyte-cloud-connector-metadata-service-2/metadata/airbyte/source-test/{version}/doc.md"


def _release(pr_number: int = 123) -> dict[str, object]:
    return {
        "pr_number": pr_number,
        "pr_url": f"https://github.com/airbytehq/airbyte/pull/{pr_number}",
        "attributed_to": "engineer",
        "source": "publish",
    }


def _changelog(pr_number: int = 27684) -> str:
    return (
        "| Version | Date | Pull Request | Subject |\n"
        "| --- | --- | --- | --- |\n"
        f"| 1.0.0 | 2023-06-23 | [{pr_number}](https://github.com/airbytehq/airbyte/pull/{pr_number}) | Change |\n"
    )


def _changelog_files() -> dict[str, str]:
    return {
        _index_path(): json.dumps(
            {"versions": [{"version": "2.0.0"}, {"version": "1.0.0"}]}
        ),
        _metadata_path("1.0.0"): "data: {}\n",
        _doc_path("2.0.0"): _changelog(),
    }


def _list_changelog_files() -> dict[str, str]:
    files = _changelog_files()
    files[_doc_path("2.0.0")] = _changelog() + _changelog(27685).replace(
        "1.0.0", "2.0.0"
    )
    return files


def _empty_pr_data(
    *_args: object,
    **_kwargs: object,
) -> dict[int, dict[str, object]]:
    return {}


def _human_pr_data(
    *_args: object,
    **_kwargs: object,
) -> dict[int, dict[str, object]]:
    return {
        27684: {
            "url": "https://github.com/airbytehq/airbyte/pull/27684",
            "author": {
                "databaseId": 42,
                "login": "human",
                "__typename": "User",
            },
            "mergedAt": "2023-06-23T12:34:56Z",
            "mergeCommit": {"oid": "abc123"},
        }
    }


def _bot_pr_data(
    *_args: object,
    **_kwargs: object,
) -> dict[int, dict[str, object]]:
    return {
        27684: {
            "author": {
                "databaseId": 7,
                "login": "release-bot[bot]",
                "__typename": "Bot",
            }
        }
    }


def _raise_rate_limit(
    *_args: object,
    **_kwargs: object,
) -> dict[int, dict[str, object]]:
    raise ValueError("rate limited")


@pytest.mark.unit
@pytest.mark.parametrize(
    (
        "files",
        "version",
        "expected_status",
        "expected_lookup_path",
        "expected_pr_number",
        "expected_error",
        "expected_reads",
    ),
    [
        pytest.param(
            {
                _index_path(): json.dumps(
                    {"versions": [{"version": "1.0.0", "release": _release()}]}
                )
            },
            "1.0.0",
            "found",
            "index",
            123,
            None,
            [_index_path()],
            id="indexed_hit",
        ),
        pytest.param(
            {
                _index_path(): json.dumps({"versions": [{"version": "1.0.0"}]}),
                _metadata_path("1.0.0"): (
                    "data:\n  generated:\n    release:\n"
                    "      pr_number: 456\n      source: publish\n"
                ),
            },
            "1.0.0",
            "found",
            "metadata",
            456,
            None,
            [_index_path(), _metadata_path("1.0.0")],
            id="metadata_fallback",
        ),
        pytest.param(
            {_index_path(): json.dumps({"versions": []})},
            "1.0.0",
            "not_found",
            "none",
            None,
            None,
            [_index_path(), _metadata_path("1.0.0")],
            id="not_found",
        ),
        pytest.param(
            {_doc_path("1.0.0"): _changelog()},
            "1.0.0",
            "found",
            "changelog",
            27684,
            None,
            [_index_path(), _metadata_path("1.0.0"), _doc_path("1.0.0")],
            id="missing_index_reaches_changelog",
        ),
        pytest.param(
            _changelog_files(),
            "3.0.0",
            "not_found",
            "changelog",
            None,
            None,
            [_index_path(), _metadata_path("3.0.0"), _doc_path("2.0.0")],
            id="changelog_missing_version",
        ),
    ],
)
def test_lookup_release_attribution_tiers(
    files: dict[str, str],
    version: str,
    expected_status: str,
    expected_lookup_path: str,
    expected_pr_number: int | None,
    expected_error: str | None,
    expected_reads: list[str],
) -> None:
    """Lookup tiers return the expected status, path, and pull request."""
    fs = FakeFileSystem(files)
    result = release_attribution.lookup_release_attribution(
        fs=fs, store=_store(), connector="source-test", version=version
    )
    assert result.status == expected_status
    assert result.lookup_path == expected_lookup_path
    assert (
        result.attribution.pr_number if result.attribution is not None else None
    ) == expected_pr_number
    assert result.error == expected_error
    assert fs.reads == expected_reads


@pytest.mark.unit
@pytest.mark.parametrize(
    ("fetch_pr_data", "expected_updates"),
    [
        pytest.param(
            _empty_pr_data,
            {"merged_at": datetime(2023, 6, 23, tzinfo=timezone.utc)},
            id="changelog_without_enrichment",
        ),
        pytest.param(
            _human_pr_data,
            {
                "pr_author_id": 42,
                "pr_author_login": "human",
                "pr_author_type": "User",
                "attributed_to": "human",
                "merge_commit_sha": "abc123",
                "merged_at": datetime(2023, 6, 23, 12, 34, 56, tzinfo=timezone.utc),
            },
            id="changelog_human_enrichment",
        ),
        pytest.param(
            _bot_pr_data,
            {
                "pr_author_id": 7,
                "pr_author_login": "release-bot[bot]",
                "pr_author_type": "Bot",
                "attributed_to": None,
            },
            id="changelog_bot_enrichment",
        ),
        pytest.param(
            _raise_rate_limit,
            {},
            id="changelog_api_failure",
        ),
    ],
)
def test_changelog_lookup_enrichment(
    monkeypatch: pytest.MonkeyPatch,
    fetch_pr_data: Callable[..., dict[int, dict[str, object]]],
    expected_updates: dict[str, object],
) -> None:
    """Changelog attribution survives optional GitHub enrichment outcomes."""
    monkeypatch.setattr(
        release_attribution,
        "resolve_default_github_token",
        lambda allow_none=True: "token",
    )
    monkeypatch.setattr(release_attribution, "_fetch_pr_data", fetch_pr_data)
    fs = FakeFileSystem(_changelog_files())
    result = release_attribution.lookup_release_attribution(
        fs=fs, store=_store(), connector="source-test", version="1.0.0"
    )
    expected = release_attribution.ReleaseAttribution(
        pr_number=27684,
        pr_url="https://github.com/airbytehq/airbyte/pull/27684",
        merged_at=datetime(2023, 6, 23, tzinfo=timezone.utc),
        source="changelog",
    ).model_copy(update=expected_updates)
    assert result.status == "found"
    assert result.lookup_path == "changelog"
    assert result.attribution == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    (
        "files",
        "limit",
        "with_metadata_fallback",
        "expected_items",
        "expected_reads",
    ),
    [
        pytest.param(
            {
                _index_path(): json.dumps(
                    {
                        "versions": [
                            {"version": "1.0.0", "release": _release(100)},
                            {"version": "1.2.0", "release": _release(120)},
                            {"version": "1.1.0", "release": _release(110)},
                        ]
                    }
                )
            },
            2,
            False,
            [
                ("1.2.0", "found", "index"),
                ("1.1.0", "found", "index"),
            ],
            [_index_path()],
            id="newest_first_and_limit",
        ),
        pytest.param(
            {
                _index_path(): json.dumps(
                    {"versions": [{"version": "1.0.0"}, {"version": "1.1.0"}]}
                )
            },
            100,
            False,
            [
                ("1.1.0", "unattributed", "index"),
                ("1.0.0", "unattributed", "index"),
            ],
            [_index_path()],
            id="metadata_fallback_disabled",
        ),
        pytest.param(
            {
                _index_path(): json.dumps({"versions": [{"version": "1.0.0"}]}),
                _metadata_path("1.0.0"): (
                    "data:\n  generated:\n    release:\n"
                    "      pr_number: 456\n      source: publish\n"
                ),
            },
            100,
            True,
            [("1.0.0", "found", "metadata")],
            [_index_path(), _metadata_path("1.0.0")],
            id="metadata_fallback_opt_in",
        ),
    ],
)
def test_list_release_attribution_tiers(
    monkeypatch: pytest.MonkeyPatch,
    files: dict[str, str],
    limit: int,
    with_metadata_fallback: bool,
    expected_items: list[tuple[str, str, str]],
    expected_reads: list[str],
) -> None:
    """Listing returns newest-first results with optional fallback tiers."""
    monkeypatch.setattr(
        release_attribution,
        "resolve_default_github_token",
        lambda allow_none=True: None,
    )
    fs = FakeFileSystem(files)
    result = release_attribution.list_release_attribution(
        fs=fs,
        store=_store(),
        connector="source-test",
        limit=limit,
        with_metadata_fallback=with_metadata_fallback,
    )
    assert [
        (item.version, item.status, item.lookup_path) for item in result.items
    ] == expected_items
    assert fs.reads == expected_reads


@pytest.mark.unit
def test_list_changelog_doc_is_read_once(monkeypatch: pytest.MonkeyPatch) -> None:
    """Listing fallback reads the latest changelog document once."""
    monkeypatch.setattr(
        release_attribution,
        "resolve_default_github_token",
        lambda allow_none=True: None,
    )
    fs = FakeFileSystem(_list_changelog_files())
    result = release_attribution.list_release_attribution(
        fs=fs,
        store=_store(),
        connector="source-test",
        limit=100,
        with_metadata_fallback=True,
    )
    assert [item.status for item in result.items] == ["found", "found"]
    assert fs.reads.count(_doc_path("2.0.0")) == 1


@pytest.mark.unit
def test_changelog_lookup_is_read_only(monkeypatch: pytest.MonkeyPatch) -> None:
    """Changelog lookup does not persist attribution to the index."""
    monkeypatch.setattr(
        release_attribution,
        "resolve_default_github_token",
        lambda allow_none=True: None,
    )
    files = {
        _index_path(): json.dumps(
            {"versions": [{"version": "2.0.0"}, {"version": "1.0.0"}]}
        ),
        _metadata_path("1.0.0"): "data: {}\n",
        _doc_path("2.0.0"): _changelog(),
    }
    fs = FakeFileSystem(files)
    result = release_attribution.lookup_release_attribution(
        fs=fs, store=_store(), connector="source-test", version="1.0.0"
    )
    assert result.status == "found"
    assert "release" not in json.loads(fs.files[_index_path()])["versions"][0]
