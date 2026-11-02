"""Tests for reading filtered, immutable dispatch-state snapshots."""

import json
from pathlib import Path
from typing import Any, cast

import pytest

from agentic_devtools.cli.ci.dispatch_state import DispatchIdentity, DispatchRecord
from agentic_devtools.cli.ci.dispatch_state_codec import read_dispatch_state_snapshot

HEAD_SHA = "a" * 40
WORK_DIGEST = "b" * 64


def _canonical_record(repo: str, pull_request_id: int, head_sha: str, ordinal: int) -> dict[str, Any]:
    return {
        "repo": repo,
        "pull_request_id": pull_request_id,
        "head_sha": head_sha,
        "review_id": 0,
        "work_digest": WORK_DIGEST,
        "ordinal": ordinal,
        "metadata": {"nested": [1, 2]},
    }


def _record_key(record: dict[str, Any]) -> str:
    return (
        f"{record['repo']}:{record['pull_request_id']}:{record['head_sha']}:"
        f"{record['review_id']}:{record['work_digest']}:{record['ordinal']}"
    )


def _payload() -> dict[str, Any]:
    legacy_records = [
        DispatchRecord.new(DispatchIdentity("repo", 7, HEAD_SHA, 1)),
        DispatchRecord.new(DispatchIdentity("other", 7, HEAD_SHA, 1)),
        DispatchRecord.new(DispatchIdentity("repo", 8, HEAD_SHA, 1)),
        DispatchRecord.new(DispatchIdentity("repo", 7, "c" * 40, 1)),
    ]
    canonical_records = [
        _canonical_record("owner/repo", 7, HEAD_SHA, 4),
        _canonical_record("other/repo", 7, HEAD_SHA, 4),
        _canonical_record("owner/repo", 8, HEAD_SHA, 4),
        _canonical_record("owner/repo", 7, "c" * 40, 4),
    ]
    return {
        "version": 2,
        "records": {record.identity.key: record.to_dict() for record in legacy_records},
        "canonical_records": {_record_key(record): record for record in canonical_records},
    }


def test_filters_each_namespace_by_its_explicit_selector(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    path.write_text(json.dumps(_payload()), encoding="utf-8")

    snapshot = read_dispatch_state_snapshot(
        path,
        legacy_repo="REPO",
        canonical_repo="owner/repo",
        pull_request_id=7,
        head_sha=HEAD_SHA,
    )

    assert len(snapshot.records) == 1
    assert len(snapshot.canonical_records) == 1
    assert len(snapshot.envelope.records) == 4
    assert len(snapshot.envelope.canonical_records) == 4
    assert list(tmp_path.iterdir()) == [path]


@pytest.mark.parametrize(
    ("selectors", "message"),
    [
        ({"legacy_repo": "owner/repo"}, "repo"),
        ({"canonical_repo": "repo"}, "owner/name"),
        ({"legacy_repo": ""}, "repo"),
        ({"canonical_repo": "Owner/repo"}, "repo"),
        ({"pull_request_id": True}, "pull_request_id"),
        ({"head_sha": "A" * 40}, "head_sha"),
    ],
)
def test_rejects_invalid_selectors(tmp_path: Path, selectors: dict[str, object], message: str) -> None:
    path = tmp_path / "dispatch.json"
    path.write_text(json.dumps(_payload()), encoding="utf-8")
    arguments: dict[str, object] = {
        "legacy_repo": "repo",
        "canonical_repo": "owner/repo",
        "pull_request_id": 7,
        "head_sha": HEAD_SHA,
    }
    arguments.update(selectors)

    with pytest.raises(ValueError, match=message):
        read_dispatch_state_snapshot(path, **arguments)  # type: ignore[arg-type]


def test_requires_both_repository_selectors(tmp_path: Path) -> None:
    reader = cast(Any, read_dispatch_state_snapshot)
    with pytest.raises(TypeError):
        reader(
            tmp_path / "missing.json",
            canonical_repo="owner/repo",
            pull_request_id=7,
            head_sha=HEAD_SHA,
        )
    with pytest.raises(TypeError):
        reader(
            tmp_path / "missing.json",
            legacy_repo="repo",
            pull_request_id=7,
            head_sha=HEAD_SHA,
        )


def test_missing_file_returns_an_empty_snapshot_and_other_read_errors_surface(tmp_path: Path) -> None:
    missing = read_dispatch_state_snapshot(
        tmp_path / "missing.json",
        legacy_repo="repo",
        canonical_repo="owner/repo",
        pull_request_id=7,
        head_sha=HEAD_SHA,
    )
    assert missing.records == {}
    assert missing.canonical_records == {}

    invalid_utf8 = tmp_path / "invalid.json"
    invalid_utf8.write_bytes(b"\xff")
    with pytest.raises(UnicodeDecodeError):
        read_dispatch_state_snapshot(
            invalid_utf8,
            legacy_repo="repo",
            canonical_repo="owner/repo",
            pull_request_id=7,
            head_sha=HEAD_SHA,
        )
