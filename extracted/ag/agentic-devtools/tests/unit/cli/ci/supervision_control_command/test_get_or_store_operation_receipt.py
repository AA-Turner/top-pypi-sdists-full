"""Tests for the get_or_store_operation_receipt symbol."""

from __future__ import annotations

from typing import cast

import pytest

from agentic_devtools.cli.ci.supervision_control import HoldReceipt, SupervisionControl
from agentic_devtools.cli.ci.supervision_control_command import (
    CONTROL_STATE_INDEX_MARKER,
    OPERATION_RECEIPT_MARKER,
    get_or_store_operation_receipt,
)


def _empty_graphql_comments() -> dict[str, object]:
    return {
        "data": {
            "repository": {
                "issue": {"comments": {"nodes": [], "pageInfo": {"hasPreviousPage": False, "hasNextPage": False}}}
            }
        }
    }


def test_get_or_store_operation_receipt_rejects_a_receipt_type_mismatch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def read_provider(arguments: list[str]) -> object:
        if arguments[:2] == ["api", "user"]:
            return {"login": "automation"}
        return _empty_graphql_comments()

    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._run_gh",
        read_provider,
    )

    with pytest.raises(ValueError, match="receipt type does not match"):
        get_or_store_operation_receipt(
            "owner/repo",
            42,
            SupervisionControl(),
            "quarantine",
            "key",
            HoldReceipt("run-1", (), {}),
        )


def test_get_or_store_operation_receipt_requires_read_back(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def read_provider(arguments: list[str]) -> object:
        if arguments[:2] == ["api", "user"]:
            return {"login": "automation"}
        return _empty_graphql_comments()

    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._run_gh",
        read_provider,
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._run_gh_text",
        lambda _arguments: "posted",
    )

    with pytest.raises(RuntimeError, match="read-back mismatch"):
        get_or_store_operation_receipt(
            "owner/repo",
            42,
            SupervisionControl(),
            "hold",
            "key",
            HoldReceipt("run-1", (), {"loop.yml": False}),
        )


def test_get_or_store_operation_receipt_requires_authenticated_author(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._run_gh",
        lambda _arguments: {},
    )

    with pytest.raises(RuntimeError, match="authenticated GitHub identity"):
        get_or_store_operation_receipt(
            "owner/repo",
            42,
            SupervisionControl(),
            "hold",
            "key",
            HoldReceipt("run-1", (), {}),
        )


def test_get_or_store_operation_receipt_round_trips_json_mutation_receipts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    comments: list[dict[str, object]] = []

    def read_provider(arguments: list[str]) -> object:
        if arguments[:2] == ["api", "user"]:
            return {"login": "automation"}
        return {
            "data": {
                "repository": {
                    "issue": {
                        "comments": {
                            "nodes": comments,
                            "pageInfo": {"hasPreviousPage": False, "hasNextPage": False},
                        }
                    }
                }
            }
        }

    def write_provider(arguments: list[str]) -> str:
        comments.append({"author": {"login": "automation"}, "body": arguments[arguments.index("--body") + 1]})
        return "posted"

    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh", read_provider)
    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh_text", write_provider)
    proposed = {
        "labels_created": ["ai-pr-loop-ignore"],
        "labels_reused": ["ai-pr-loop-supervised"],
        "control_issue": 42,
        "control_issue_created": False,
    }

    first, first_replayed = get_or_store_operation_receipt(
        "owner/repo", 42, SupervisionControl(), "ensure-labels", "key", proposed
    )
    second, second_replayed = get_or_store_operation_receipt(
        "owner/repo", 42, SupervisionControl(), "ensure-labels", "key", proposed
    )

    assert first == second == proposed
    assert first_replayed is False
    assert second_replayed is True
    bodies = [cast(str, comment["body"]) for comment in comments]
    assert sum(body.startswith(f"{OPERATION_RECEIPT_MARKER}\n") for body in bodies) == 1
    assert sum(body.startswith(f"{CONTROL_STATE_INDEX_MARKER}\n") for body in bodies) == 1


def test_get_or_store_operation_receipt_rejects_extra_fields_in_mutation_receipts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._run_gh",
        lambda arguments: {"login": "automation"} if arguments[:2] == ["api", "user"] else _empty_graphql_comments(),
    )
    proposed = {
        "labels_created": ["ai-pr-loop-ignore"],
        "labels_reused": ["ai-pr-loop-supervised"],
        "control_issue": 42,
        "control_issue_created": False,
        "unexpected": True,
    }

    with pytest.raises(ValueError, match="receipt type does not match"):
        get_or_store_operation_receipt("owner/repo", 42, SupervisionControl(), "ensure-labels", "key", proposed)
