import pytest

import agentic_devtools.cli.ci.guards as guards_module
from agentic_devtools.cli.ci.dispatch_state import DispatchIdentity
from agentic_devtools.cli.ci.guards import (
    DISPATCH_CONTRACT_MARKER,
    ReconciliationResult,
    canonical_dispatch_token,
    reconcile_uncertain_marker_comment,
)

SHA = "d" * 40


def test_reconciles_unique_marker_comment() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)
    token = canonical_dispatch_token(identity)
    page = {
        "comments": [{"id": 44, "author": "dispatch-bot", "body": f"{DISPATCH_CONTRACT_MARKER}\n{token}\n\nbody"}],
        "has_more": False,
    }

    result = reconcile_uncertain_marker_comment(identity, [page], dispatch_login="dispatch-bot")

    assert result.outcome == "unique_match"
    assert result.marker_comment_id == 44
    assert result.task_id is None


def test_requires_canonical_marker_layout() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)
    token = canonical_dispatch_token(identity)
    bodies = (
        f"quoted {DISPATCH_CONTRACT_MARKER}\n{token}",
        f"{DISPATCH_CONTRACT_MARKER}\n{token}-trailing",
        f"{DISPATCH_CONTRACT_MARKER}\n{token} trailing",
    )

    for body in bodies:
        result = reconcile_uncertain_marker_comment(
            identity,
            [{"comments": [{"id": 44, "author": "dispatch-bot", "body": body}], "has_more": False}],
            dispatch_login="dispatch-bot",
        )
        assert result.outcome == "complete_miss"


def test_classifies_marker_miss_ambiguity_and_incomplete() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)
    token = canonical_dispatch_token(identity)
    marker_body = f"{DISPATCH_CONTRACT_MARKER}\n{token}"
    assert (
        reconcile_uncertain_marker_comment(
            identity,
            [{"comments": [{"id": 5, "author": "dispatch-bot", "body": "unrelated"}], "has_more": False}],
            dispatch_login="dispatch-bot",
        ).outcome
        == "complete_miss"
    )
    assert (
        reconcile_uncertain_marker_comment(identity, [{"comments": [], "has_more": False}]).outcome == "complete_miss"
    )
    assert (
        reconcile_uncertain_marker_comment(
            identity,
            [
                {
                    "comments": [
                        {"id": 1, "author": "dispatch-bot", "body": marker_body},
                        {"id": 2, "author": "dispatch-bot", "body": marker_body},
                    ],
                    "has_more": False,
                }
            ],
            dispatch_login="dispatch-bot",
        ).outcome
        == "ambiguous"
    )
    assert (
        reconcile_uncertain_marker_comment(
            identity,
            [{"comments": [{"id": 1, "author": "dispatch-bot", "body": marker_body}], "has_more": True}],
            dispatch_login="dispatch-bot",
        ).outcome
        == "incomplete"
    )


def test_rejects_invalid_comment_pages() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)
    token = canonical_dispatch_token(identity)
    page = {
        "comments": [{"id": True, "author": "dispatch-bot", "body": f"{DISPATCH_CONTRACT_MARKER}\n{token}"}],
        "status": 200,
        "status_code": 401,
        "has_more": False,
    }

    result = reconcile_uncertain_marker_comment(identity, [page], dispatch_login="dispatch-bot")

    assert result.outcome == "incomplete"


def test_fails_closed_for_boolean_marker_comment_ids() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)
    token = canonical_dispatch_token(identity)

    result = reconcile_uncertain_marker_comment(
        identity,
        [
            {
                "comments": [{"id": True, "author": "dispatch-bot", "body": f"{DISPATCH_CONTRACT_MARKER}\n{token}"}],
                "has_more": False,
            }
        ],
        dispatch_login="dispatch-bot",
    )

    assert result.outcome == "incomplete"
    assert result.marker_comment_id is None


def test_fails_closed_for_conflicting_comment_container_aliases() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)
    token = canonical_dispatch_token(identity)
    marker = {"id": 44, "body": f"{DISPATCH_CONTRACT_MARKER}\n{token}"}

    result = reconcile_uncertain_marker_comment(
        identity,
        [{"comments": [], "items": [marker], "has_more": False}],
    )

    assert result.outcome == "incomplete"


def test_fails_closed_for_type_collapsing_comment_container_aliases() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)
    token = canonical_dispatch_token(identity)
    marker_body = f"{DISPATCH_CONTRACT_MARKER}\n{token}"

    result = reconcile_uncertain_marker_comment(
        identity,
        [
            {
                "comments": [{"id": 1, "body": marker_body}],
                "items": [{"id": True, "author": "dispatch-bot", "body": marker_body}],
                "has_more": False,
            }
        ],
        dispatch_login="dispatch-bot",
    )

    assert result.outcome == "incomplete"


def test_fails_closed_for_missing_or_unrecognized_comment_containers() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)

    assert reconcile_uncertain_marker_comment(identity, [{"has_more": False}]).outcome == "incomplete"
    assert reconcile_uncertain_marker_comment(identity, [{"data": {"unexpected": []}, "has_more": False}]).outcome == (
        "incomplete"
    )


def test_fails_closed_for_conflicting_nested_comment_containers() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)

    result = reconcile_uncertain_marker_comment(
        identity,
        [{"data": {"comments": [], "items": [{"id": 44, "body": "body"}]}, "has_more": False}],
    )

    assert result.outcome == "incomplete"


def test_fails_closed_for_type_collapsing_nested_comment_container_aliases() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)
    token = canonical_dispatch_token(identity)
    marker_body = f"{DISPATCH_CONTRACT_MARKER}\n{token}"

    result = reconcile_uncertain_marker_comment(
        identity,
        [
            {
                "data": {
                    "comments": [{"id": 1, "body": marker_body}],
                    "items": [{"id": True, "body": marker_body}],
                },
                "has_more": False,
            }
        ],
    )

    assert result.outcome == "incomplete"


def test_fails_closed_for_non_integer_marker_comment_ids() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)
    token = canonical_dispatch_token(identity)

    result = reconcile_uncertain_marker_comment(
        identity,
        [
            {
                "comments": [{"id": "44", "author": "dispatch-bot", "body": f"{DISPATCH_CONTRACT_MARKER}\n{token}"}],
                "has_more": False,
            }
        ],
        dispatch_login="dispatch-bot",
    )

    assert result.outcome == "incomplete"
    assert result.marker_comment_id is None


def test_fails_closed_when_unique_match_lacks_string_identifier(monkeypatch: pytest.MonkeyPatch) -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)

    def fake_reconcile_uncertain_dispatch(*_args, **_kwargs):
        return ReconciliationResult("unique_match", task_id=None, evidence={})

    monkeypatch.setattr(guards_module, "reconcile_uncertain_dispatch", fake_reconcile_uncertain_dispatch)

    result = reconcile_uncertain_marker_comment(identity, [{"comments": [], "has_more": False}])

    assert result.outcome == "incomplete"
    assert result.marker_comment_id is None


def test_fails_closed_when_unique_match_lacks_numeric_identifier(monkeypatch: pytest.MonkeyPatch) -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)

    def fake_reconcile_uncertain_dispatch(*_args, **_kwargs):
        return ReconciliationResult("unique_match", task_id="task-1", evidence={})

    monkeypatch.setattr(guards_module, "reconcile_uncertain_dispatch", fake_reconcile_uncertain_dispatch)

    result = reconcile_uncertain_marker_comment(identity, [{"comments": [], "has_more": False}])

    assert result.outcome == "incomplete"
    assert result.marker_comment_id is None


def test_fails_closed_for_conflicting_marker_comment_id_alias_types() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)
    token = canonical_dispatch_token(identity)

    result = reconcile_uncertain_marker_comment(
        identity,
        [
            {
                "comments": [
                    {
                        "id": 44,
                        "comment_id": True,
                        "author": "dispatch-bot",
                        "body": f"{DISPATCH_CONTRACT_MARKER}\n{token}",
                    }
                ],
                "has_more": False,
            }
        ],
        dispatch_login="dispatch-bot",
    )

    assert result.outcome == "incomplete"
    assert result.marker_comment_id is None


def test_supports_dict_and_callable_page_sources() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)
    token = canonical_dispatch_token(identity)
    marker_body = f"{DISPATCH_CONTRACT_MARKER}\n{token}"
    direct = reconcile_uncertain_marker_comment(
        identity,
        {"data": {"comments": [{"id": 7, "author": "dispatch-bot", "body": marker_body}]}, "is_last": True},
        dispatch_login="dispatch-bot",
    )
    assert direct.outcome == "unique_match"
    assert direct.marker_comment_id == 7

    calls: list[object | None] = []

    def fetch(cursor: object | None) -> object:
        calls.append(cursor)
        if cursor is None:
            return {"comments": [], "has_more": True, "next_token": "next"}
        return {"comments": [{"id": 9, "author": "dispatch-bot", "body": marker_body}], "has_more": False}

    result = reconcile_uncertain_marker_comment(identity, fetch, dispatch_login="dispatch-bot")
    assert result.outcome == "unique_match"
    assert result.marker_comment_id == 9
    assert calls == [None, "next"]


def test_fails_closed_for_malformed_comment_entries() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)
    token = canonical_dispatch_token(identity)
    marker_body = f"{DISPATCH_CONTRACT_MARKER}\n{token}"

    assert (
        reconcile_uncertain_marker_comment(
            identity,
            [{"comments": [{"id": 1, "author": "dispatch-bot", "body": 1}], "has_more": False}],
            dispatch_login="dispatch-bot",
        ).outcome
        == "incomplete"
    )
    assert (
        reconcile_uncertain_marker_comment(
            identity,
            [{"comments": [1, {"id": 2, "author": "dispatch-bot", "body": marker_body}], "has_more": False}],
            dispatch_login="dispatch-bot",
        ).outcome
        == "incomplete"
    )
    assert reconcile_uncertain_marker_comment(identity, [{"comments": "bad-shape", "has_more": False}]).outcome == (
        "incomplete"
    )
    assert reconcile_uncertain_marker_comment(identity, [None]).outcome == "incomplete"


def test_ignores_spoofed_marker_comments_from_untrusted_authors() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)
    token = canonical_dispatch_token(identity)

    result = reconcile_uncertain_marker_comment(
        identity,
        [
            {
                "comments": [{"id": 44, "author": "other-user", "body": f"{DISPATCH_CONTRACT_MARKER}\n{token}"}],
                "has_more": False,
            }
        ],
        dispatch_login="dispatch-bot",
    )

    assert result.outcome == "complete_miss"
    assert result.marker_comment_id is None


def test_fails_closed_for_matching_marker_when_dispatch_login_is_missing() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)
    token = canonical_dispatch_token(identity)

    result = reconcile_uncertain_marker_comment(
        identity,
        [
            {
                "comments": [{"id": 44, "author": "dispatch-bot", "body": f"{DISPATCH_CONTRACT_MARKER}\n{token}"}],
                "has_more": False,
            }
        ],
    )

    assert result.outcome == "incomplete"
    assert result.marker_comment_id is None


def test_fails_closed_for_matching_marker_when_author_is_missing() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)
    token = canonical_dispatch_token(identity)

    result = reconcile_uncertain_marker_comment(
        identity,
        [{"comments": [{"id": 44, "body": f"{DISPATCH_CONTRACT_MARKER}\n{token}"}], "has_more": False}],
        dispatch_login="dispatch-bot",
    )

    assert result.outcome == "incomplete"
    assert result.marker_comment_id is None
