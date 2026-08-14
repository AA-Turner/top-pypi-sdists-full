from __future__ import annotations

import io
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pytest

from airbyte_ops_mcp.registry.release_attribution import (
    ReleaseAttribution,
    ReleaseAttributionIndex,
    ReleaseAttributionSummary,
    _iter_version_records,
    _request_graphql,
    build_release_attribution,
    derive_git_author,
    enrich_release_attribution,
    extract_pr_number,
    read_release_attribution_index,
    scan_release_attribution,
    write_release_attribution_index,
)


@pytest.mark.unit
@pytest.mark.parametrize(
    ("subject", "expected"),
    [
        ("feat: release (#12345)", 12345),
        ("chore: text (not a PR ref)", None),
        ("chore: two refs (#12) and final (#34)", 34),
        ("chore: release (#123) trailing text", None),
    ],
)
def test_extract_pr_number(subject: str, expected: int | None) -> None:
    """Only a trailing parenthesized number is a pull request reference."""
    assert extract_pr_number(subject) == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    ("name", "email", "expected"),
    [
        (
            "AJ Steers",
            "12345+aaronsteers@users.noreply.github.com",
            (12345, "aaronsteers", "User"),
        ),
        (
            "octavia-bot-hoard[bot]",
            "987+octavia-bot-hoard[bot]@users.noreply.github.com",
            (987, "octavia-bot-hoard[bot]", "Bot"),
        ),
        ("Human Bot", "human@example.com", (None, None, None)),
        ("Airbyte", "airbyte@airbyte.io", (None, None, None)),
    ],
)
def test_derive_git_author(
    name: str,
    email: str,
    expected: tuple[int | None, str | None, str | None],
) -> None:
    """Derive stable noreply identity and detect bot authors."""
    assert derive_git_author(name, email) == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    ("output", "expected_merge_sha", "expected_pr_number", "expected_record_count"),
    [
        pytest.param(
            (
                "\x01newsha\x1fNew User\x1f1+new@users.noreply.github.com\x1f2025-01-02T00:00:00+00:00\x1fbump (#2)\n"
                "+++ b/airbyte-integrations/connectors/source-test/metadata.yaml\n"
                "+  dockerImageTag: 2.0.0\n"
                "\x01oldsha\x1fOld User\x1f2+old@users.noreply.github.com\x1f2025-01-01T00:00:00+00:00\x1fbump (#1)\n"
                "+++ b/airbyte-integrations/connectors/source-test/metadata.yaml\n"
                "+  dockerImageTag: 2.0.0\n"
            ),
            "newsha",
            2,
            2,
            id="duplicate_versions_keep_newest",
        ),
        pytest.param(
            (
                "\x01sha\x1fAirbyte\x1fairbyte@airbyte.io\x1f2025-01-01T00:00:00+00:00\x1fautomated bump\n"
                "+++ b/airbyte-integrations/connectors/source-test/metadata.yaml\n"
                "+  dockerImageTag: 1.0.0\n"
            ),
            "sha",
            None,
            1,
            id="missing_pr_is_retained",
        ),
    ],
)
def test_iter_version_records_scenarios(
    output: str,
    expected_merge_sha: str,
    expected_pr_number: int | None,
    expected_record_count: int,
) -> None:
    """Duplicate and missing-PR records retain their asserted attribution."""
    records = _iter_version_records(io.StringIO(output))
    assert records[0][2].merge_commit_sha == expected_merge_sha
    assert records[0][2].pr_number == expected_pr_number
    assert len(records) == expected_record_count


@pytest.mark.unit
def test_scan_release_attribution_collapses_duplicate_versions(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Scanning collapses duplicate versions to the newest record."""
    output = io.StringIO(
        "\x01newsha\x1fNew User\x1f1+new@users.noreply.github.com\x1f2025-01-02T00:00:00+00:00\x1fbump (#2)\n"
        "+++ b/airbyte-integrations/connectors/source-test/metadata.yaml\n"
        "+  dockerImageTag: 2.0.0\n"
        "\x01oldsha\x1fOld User\x1f2+old@users.noreply.github.com\x1f2025-01-01T00:00:00+00:00\x1fbump (#1)\n"
        "+++ b/airbyte-integrations/connectors/source-test/metadata.yaml\n"
        "+  dockerImageTag: 2.0.0\n"
    )

    class FakeProcess:
        stdout = output
        stderr = io.StringIO()

        def wait(self) -> int:
            return 0

    monkeypatch.setattr(
        "airbyte_ops_mcp.registry.release_attribution._ensure_full_clone",
        lambda _: None,
    )
    monkeypatch.setattr(
        "airbyte_ops_mcp.registry.release_attribution._git_command",
        lambda *_args: FakeProcess(),
    )
    index = scan_release_attribution(tmp_path)
    assert index.summary.duplicate_versions_collapsed == 1
    assert index.connectors["source-test"]["2.0.0"].merge_commit_sha == "newsha"


@pytest.mark.unit
@pytest.mark.parametrize(
    ("is_prerelease", "subject", "pr_number", "expected_source"),
    [
        pytest.param(
            False, "chore: bump connector (#123)", None, "publish", id="publish"
        ),
        pytest.param(True, "branch change", 123, "prerelease", id="prerelease_with_pr"),
        pytest.param(
            True, "branch change", None, "prerelease", id="prerelease_without_pr"
        ),
    ],
)
def test_build_release_attribution_scenarios(
    tmp_path: Path,
    is_prerelease: bool,
    subject: str,
    pr_number: int | None,
    expected_source: str,
) -> None:
    """Build publish and prerelease attribution from the latest metadata commit."""
    repo_path = tmp_path
    metadata_path = (
        repo_path
        / "airbyte-integrations"
        / "connectors"
        / "source-test"
        / "metadata.yaml"
    )
    metadata_path.parent.mkdir(parents=True)
    metadata_path.write_text(
        f"data:\n  dockerImageTag: {'1.0.0-rc.1' if is_prerelease else '1.0.0'}\n"
    )
    subprocess.run(["git", "init", "-q", str(repo_path)], check=True)
    subprocess.run(
        ["git", "-C", str(repo_path), "config", "user.name", "Test User"],
        check=True,
    )
    subprocess.run(
        [
            "git",
            "-C",
            str(repo_path),
            "config",
            "user.email",
            "1+test@users.noreply.github.com",
        ],
        check=True,
    )
    subprocess.run(["git", "-C", str(repo_path), "add", "."], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(repo_path),
            "commit",
            "-q",
            "-m",
            subject,
        ],
        check=True,
    )

    record = build_release_attribution(
        repo_path,
        metadata_path,
        pr_number=pr_number,
        is_prerelease=is_prerelease,
    )

    assert record.source == expected_source
    assert record.pr_number == (pr_number if is_prerelease else 123)
    assert record.pr_author_id == 1
    assert record.pr_author_login == "test"
    if is_prerelease:
        assert record.merge_commit_sha is None
        assert record.merged_at is None
        assert record.pr_url == (
            f"https://github.com/airbytehq/airbyte/pull/{pr_number}"
            if pr_number
            else None
        )
    else:
        assert record.merge_commit_sha
        assert record.merged_at is not None


@pytest.mark.unit
def test_release_attribution_index_round_trip(tmp_path: Path) -> None:
    """Writing and reading an attribution index preserves its Pydantic model."""
    records = _iter_version_records(
        io.StringIO(
            "\x01sha\x1fTest User\x1f1+test@users.noreply.github.com\x1f2025-01-01T00:00:00+00:00\x1fbump (#1)\n"
            "+++ b/airbyte-integrations/connectors/source-test/metadata.yaml\n"
            "+  dockerImageTag: 1.0.0\n"
        )
    )
    record = records[0][2]
    index = ReleaseAttributionIndex(
        connectors={"source-test": {"1.0.0": record}},
        summary=ReleaseAttributionSummary(
            connectors=1,
            versions=1,
            versions_with_pr=1,
            versions_with_author_login=1,
            duplicate_versions_collapsed=0,
        ),
    )
    path = tmp_path / "attribution.json"
    write_release_attribution_index(index, path)
    assert read_release_attribution_index(path) == index


@pytest.mark.unit
@pytest.mark.parametrize(
    ("repository_data", "errors", "expected_updates"),
    [
        pytest.param(
            {
                "pr_123": {
                    "url": "https://github.com/airbytehq/airbyte/pull/123",
                    "author": None,
                    "mergedAt": None,
                    "mergeCommit": None,
                }
            },
            None,
            {"pr_url": "https://github.com/airbytehq/airbyte/pull/123"},
            id="null_author",
        ),
        pytest.param(
            {
                "pr_123": {
                    "url": "https://github.com/airbytehq/airbyte/pull/123",
                    "author": {
                        "databaseId": 2,
                        "login": "alice",
                        "__typename": "User",
                    },
                    "mergedAt": "2025-01-02T00:00:00+00:00",
                    "mergeCommit": {"oid": "github-sha"},
                }
            },
            [{"path": ["repository", "pr_456"]}],
            {
                "pr_url": "https://github.com/airbytehq/airbyte/pull/123",
                "pr_author_id": 2,
                "pr_author_login": "alice",
                "pr_author_type": "User",
                "attributed_to": "alice",
                "merge_commit_sha": "github-sha",
                "merged_at": datetime(2025, 1, 2, tzinfo=timezone.utc),
            },
            id="partial_errors_preserve_enrichment",
        ),
        pytest.param(
            {
                "pr_123": {
                    "url": "https://github.com/airbytehq/airbyte/pull/123",
                    "author": {
                        "databaseId": 2,
                        "login": "alice",
                        "__typename": "User",
                    },
                    "mergedAt": "2025-01-02T00:00:00+00:00",
                    "mergeCommit": {"oid": "github-sha"},
                }
            },
            None,
            {
                "pr_url": "https://github.com/airbytehq/airbyte/pull/123",
                "pr_author_id": 2,
                "pr_author_login": "alice",
                "pr_author_type": "User",
                "attributed_to": "alice",
                "merge_commit_sha": "github-sha",
                "merged_at": datetime(2025, 1, 2, tzinfo=timezone.utc),
            },
            id="successful_enrichment",
        ),
    ],
)
def test_graphql_enrichment_scenarios(
    repository_data: dict[str, object],
    errors: list[dict[str, object]] | None,
    expected_updates: dict[str, object],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """GraphQL enrichment preserves Git identity across response outcomes."""

    class FakeResponse:
        status_code = 200

        def raise_for_status(self) -> None:
            return None

        @property
        def headers(self) -> dict[str, str]:
            return {}

        def json(self) -> dict[str, object]:
            return {
                "data": {"repository": repository_data},
                **({"errors": errors} if errors is not None else {}),
            }

    monkeypatch.setattr(
        "airbyte_ops_mcp.registry.release_attribution.requests.post",
        lambda *_args, **_kwargs: FakeResponse(),
    )
    response_repository = _request_graphql("query", "token")
    assert "pr_123" in response_repository

    record = ReleaseAttribution(
        pr_number=123,
        pr_url=None,
        pr_author_id=1,
        pr_author_login="test",
        pr_author_type="User",
        attributed_to="test",
        merge_commit_sha="git-sha",
        merged_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
        source="git-backfill",
    )
    index = ReleaseAttributionIndex(
        connectors={"source-test": {"1.0.0": record}},
        summary=ReleaseAttributionSummary(
            connectors=1,
            versions=1,
            versions_with_pr=1,
            versions_with_author_login=1,
            duplicate_versions_collapsed=0,
        ),
    )
    enriched = enrich_release_attribution(index, token="token")
    assert enriched.connectors["source-test"]["1.0.0"] == record.model_copy(
        update=expected_updates
    )


@pytest.mark.unit
def test_shallow_repo_guard(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Backfill refuses shallow repositories before scanning history."""
    original_run = subprocess.run

    def fake_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        command = args[0]
        if isinstance(command, list) and "--is-shallow-repository" in command:
            return subprocess.CompletedProcess(command, 0, "true\n", "")
        return original_run(*args, **kwargs)

    monkeypatch.setattr(subprocess, "run", fake_run)
    with pytest.raises(ValueError, match="shallow"):
        scan_release_attribution(tmp_path)
