"""Tests for the _read_control_issue_comments symbol."""

from __future__ import annotations

import hashlib
import json

import pytest

from agentic_devtools.cli.ci.supervision_control import HoldReceipt, SupervisionControl
from agentic_devtools.cli.ci.supervision_control_command import (
    CONTROL_STATE_INDEX_MARKER,
    OPERATION_RECEIPT_MARKER,
    _read_control_issue_comments,
    find_operation_receipt,
    hold_receipt_to_json,
)


def test_read_control_issue_comments_retains_receipts_across_pages(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[list[str]] = []
    receipt = HoldReceipt("run-old", ("loop.yml",), {"loop.yml": True})
    old_receipt = f"{OPERATION_RECEIPT_MARKER}\n" + json.dumps(
        {
            "idempotency_key": "run-old:hold",
            "operation": "hold",
            "receipt": hold_receipt_to_json(receipt),
        }
    )

    def read_provider(arguments: list[str]) -> object:
        calls.append(arguments)
        query = arguments[arguments.index("-f") + 1]
        page_info: dict[str, object]
        if "comments(last:100)" in query:
            nodes = [{"author": {"login": "automation"}, "body": "recent"}]
            page_info = {"hasPreviousPage": True}
        elif "after=cursor-1" in arguments:
            nodes = [{"author": {"login": "automation"}, "body": "recent"}]
            page_info = {"hasNextPage": False, "endCursor": "cursor-2"}
        else:
            nodes = [
                {"author": {"login": "automation"}, "body": old_receipt},
                *({"author": {"login": "automation"}, "body": f"comment-{index}"} for index in range(1, 100)),
            ]
            page_info = {"hasNextPage": True, "endCursor": "cursor-1"}
        return {
            "data": {
                "repository": {
                    "issue": {
                        "comments": {
                            "nodes": nodes,
                            "pageInfo": page_info,
                        }
                    }
                }
            }
        }

    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh", read_provider)

    bodies = _read_control_issue_comments("owner/repo", 42, "automation")

    assert len(calls) == 3
    assert all(call[:2] == ["api", "graphql"] for call in calls)
    assert "comments(last:100)" in calls[0][calls[0].index("-f") + 1]
    assert all("comments(first:100, after:$after)" in call[call.index("-f") + 1] for call in calls[1:])
    assert "owner=owner" in calls[0]
    assert "repo=repo" in calls[0]
    assert "number=42" in calls[0]
    assert "after=null" in calls[1]
    assert "after=cursor-1" in calls[2]
    assert len(bodies) == 101
    assert find_operation_receipt(SupervisionControl(), bodies, "hold", "run-old:hold") == receipt


def test_read_control_issue_comments_uses_recent_index_without_history_pagination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    receipt = HoldReceipt("run-active", ("loop.yml",), {"loop.yml": True})
    encoded_receipt = f"{OPERATION_RECEIPT_MARKER}\n" + json.dumps(
        {
            "idempotency_key": "run-active:hold",
            "operation": "hold",
            "receipt": hold_receipt_to_json(receipt),
        }
    )
    index = f"{CONTROL_STATE_INDEX_MARKER}\n" + json.dumps({"version": 1, "entries": [encoded_receipt]})
    calls: list[list[str]] = []

    def read_provider(arguments: list[str]) -> object:
        calls.append(arguments)
        return {
            "data": {
                "repository": {
                    "issue": {
                        "comments": {
                            "nodes": [
                                {"author": {"login": "automation"}, "body": index},
                                {"author": {"login": "automation"}, "body": "unindexed-write"},
                            ],
                            "pageInfo": {"hasPreviousPage": True},
                        }
                    }
                }
            }
        }

    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh", read_provider)

    bodies = _read_control_issue_comments("owner/repo", 42, "automation")

    assert bodies == [encoded_receipt, "unindexed-write"]
    assert len(calls) == 1
    assert "comments(last:100)" in calls[0][calls[0].index("-f") + 1]


def test_read_control_issue_comments_reassembles_sharded_index(monkeypatch: pytest.MonkeyPatch) -> None:
    entries = ["receipt-1", "receipt-2", "receipt-3"]
    snapshot_id = hashlib.sha256(json.dumps(entries, separators=(",", ":")).encode()).hexdigest()
    index_bodies = [
        f"{CONTROL_STATE_INDEX_MARKER}\n"
        + json.dumps(
            {
                "version": 2,
                "snapshot_id": snapshot_id,
                "shard_index": shard_index,
                "shard_count": 2,
                "entries": shard_entries,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        for shard_index, shard_entries in enumerate((entries[:2], entries[2:]))
    ]
    calls: list[list[str]] = []

    def read_provider(arguments: list[str]) -> object:
        calls.append(arguments)
        return {
            "data": {
                "repository": {
                    "issue": {
                        "comments": {
                            "nodes": [
                                {"author": {"login": "automation"}, "body": index_bodies[0]},
                                {"author": {"login": "automation"}, "body": index_bodies[1]},
                                {"author": {"login": "automation"}, "body": "newer-write"},
                            ],
                            "pageInfo": {"hasPreviousPage": True},
                        }
                    }
                }
            }
        }

    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh", read_provider)

    bodies = _read_control_issue_comments("owner/repo", 42, "automation")

    assert bodies == [*entries, "newer-write"]
    assert len(calls) == 1


@pytest.mark.parametrize(
    "index_json",
    ["not-json", "[]", json.dumps({"version": 2, "entries": []}), json.dumps({"version": 1, "entries": [1]})],
)
def test_read_control_issue_comments_rejects_invalid_index(
    monkeypatch: pytest.MonkeyPatch,
    index_json: str,
) -> None:
    error = "JSON is invalid" if index_json == "not-json" else "index is malformed"
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._run_gh",
        lambda _arguments: {
            "data": {
                "repository": {
                    "issue": {
                        "comments": {
                            "nodes": [
                                {
                                    "author": {"login": "automation"},
                                    "body": f"{CONTROL_STATE_INDEX_MARKER}\n{index_json}",
                                }
                            ],
                            "pageInfo": {"hasPreviousPage": False},
                        }
                    }
                }
            }
        },
    )

    with pytest.raises(RuntimeError, match=error):
        _read_control_issue_comments("owner/repo", 42, "automation")


def test_read_control_issue_comments_ignores_an_incomplete_sharded_index(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    incomplete_index = f"{CONTROL_STATE_INDEX_MARKER}\n" + json.dumps(
        {
            "version": 2,
            "snapshot_id": "0" * 64,
            "shard_index": 0,
            "shard_count": 2,
            "entries": ["partial"],
        }
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._run_gh",
        lambda _arguments: {
            "data": {
                "repository": {
                    "issue": {
                        "comments": {
                            "nodes": [{"author": {"login": "automation"}, "body": incomplete_index}],
                            "pageInfo": {"hasPreviousPage": False},
                        }
                    }
                }
            }
        },
    )

    assert _read_control_issue_comments("owner/repo", 42, "automation") == [incomplete_index]


def test_read_control_issue_comments_rejects_a_sharded_index_digest_mismatch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    index = f"{CONTROL_STATE_INDEX_MARKER}\n" + json.dumps(
        {
            "version": 2,
            "snapshot_id": "0" * 64,
            "shard_index": 0,
            "shard_count": 1,
            "entries": ["receipt"],
        }
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._run_gh",
        lambda _arguments: {
            "data": {
                "repository": {
                    "issue": {
                        "comments": {
                            "nodes": [{"author": {"login": "automation"}, "body": index}],
                            "pageInfo": {"hasPreviousPage": False},
                        }
                    }
                }
            }
        },
    )

    with pytest.raises(RuntimeError, match="digest mismatch"):
        _read_control_issue_comments("owner/repo", 42, "automation")


@pytest.mark.parametrize(
    "page_info",
    [
        None,
        {"hasPreviousPage": "yes"},
    ],
)
def test_read_control_issue_comments_rejects_invalid_pagination(
    monkeypatch: pytest.MonkeyPatch,
    page_info: dict[str, object] | None,
) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._run_gh",
        lambda _arguments: {
            "data": {
                "repository": {
                    "issue": {"comments": {"nodes": [], "pageInfo": page_info}},
                }
            }
        },
    )

    with pytest.raises(ValueError, match="pagination"):
        _read_control_issue_comments("owner/repo", 42, "automation")


@pytest.mark.parametrize(
    "page_info",
    [None, {"hasNextPage": "yes", "endCursor": "cursor-1"}, {"hasNextPage": True, "endCursor": ""}],
)
def test_read_control_issue_comments_rejects_invalid_legacy_pagination(
    monkeypatch: pytest.MonkeyPatch,
    page_info: dict[str, object] | None,
) -> None:
    def read_provider(arguments: list[str]) -> object:
        query = arguments[arguments.index("-f") + 1]
        legacy = "comments(first:100, after:$after)" in query
        return {
            "data": {
                "repository": {
                    "issue": {
                        "comments": {
                            "nodes": [],
                            "pageInfo": page_info if legacy else {"hasPreviousPage": True},
                        }
                    }
                }
            }
        }

    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh", read_provider)

    with pytest.raises(ValueError, match="pagination"):
        _read_control_issue_comments("owner/repo", 42, "automation")
