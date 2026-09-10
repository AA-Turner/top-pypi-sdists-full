from collections.abc import Iterator

import agentic_devtools.cli.ci.guards as guards_module
from agentic_devtools.cli.ci.dispatch_state import DispatchIdentity
from agentic_devtools.cli.ci.guards import canonical_dispatch_token, reconcile_uncertain_dispatch

SHA = "b" * 40


def test_requires_complete_pagination_and_exact_scope() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)
    token = canonical_dispatch_token(identity)
    page = {
        "tasks": [{"id": "44", "repo": "repo", "pull_request_id": 8, "prompt": f"agdt-dispatch-token: {token}\nrest"}],
        "has_more": False,
    }
    result = reconcile_uncertain_dispatch(identity, [page])
    assert result.outcome == "unique_match"
    assert result.task_id == "44"

    incomplete = reconcile_uncertain_dispatch(identity, [{"tasks": [], "has_more": True}])
    assert incomplete.outcome == "incomplete"


def test_classifies_misses_and_ambiguity() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)
    token = canonical_dispatch_token(identity)
    task = {"id": "task-1", "repo": "owner/repo", "pr_number": 8, "prompt": f"dispatch-token={token}\nrest"}
    assert reconcile_uncertain_dispatch(identity, {"items": [task], "is_last": True}).outcome == "unique_match"
    assert reconcile_uncertain_dispatch(identity, [{"tasks": [task], "has_more": False}]).task_id == "task-1"
    assert reconcile_uncertain_dispatch(identity, [task]).outcome == "incomplete"
    duplicate = dict(task)
    duplicate["id"] = "task-2"
    assert (
        reconcile_uncertain_dispatch(identity, [{"tasks": [task, duplicate], "has_more": False}]).outcome == "ambiguous"
    )
    result = reconcile_uncertain_dispatch(
        identity,
        [{"tasks": [{"id": "task-9", "repo": "repo", "pull_request_id": 8, "prompt": "unrelated"}], "has_more": False}],
    )
    assert result.outcome == "complete_miss"


def test_fails_closed_for_conflicting_task_aliases_and_ids() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)
    token = canonical_dispatch_token(identity)
    candidate = {
        "id": "task-1",
        "task_id": "task-2",
        "repo": "repo",
        "pull_request_id": 8,
        "prompt": f"agdt-dispatch-token: {token}",
    }
    result = reconcile_uncertain_dispatch(
        identity,
        [{"tasks": [], "items": [candidate], "has_more": False}],
    )
    assert result.outcome == "incomplete"
    assert reconcile_uncertain_dispatch(identity, [{"tasks": [candidate], "has_more": False}]).outcome == "incomplete"
    type_conflict = {**candidate, "id": "1", "task_id": True}
    assert reconcile_uncertain_dispatch(identity, [{"tasks": [type_conflict], "has_more": False}]).outcome == (
        "incomplete"
    )


def test_fails_closed_for_tasks_with_malformed_prompts() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)

    for prompt in (None, 42):
        result = reconcile_uncertain_dispatch(
            identity,
            [{"tasks": [{"id": "1", "repo": "repo", "pull_request_id": 8, "prompt": prompt}], "has_more": False}],
        )
        assert result.outcome == "incomplete"


def test_ignores_nonmatching_candidates_before_scope_and_id_validation() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)
    candidates = (
        {"id": "1", "repo": "wrong", "pull_request_id": 8, "prompt": "unrelated"},
        {"id": "bad/id", "repo": "repo", "pull_request_id": 8, "prompt": "unrelated"},
    )

    for candidate in candidates:
        result = reconcile_uncertain_dispatch(
            identity,
            [{"tasks": [candidate], "repo": "repo", "pull_request_id": 8, "has_more": False}],
        )
        assert result.outcome == "complete_miss"


def test_ignores_unrelated_tasks_when_recovering_a_unique_match() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)
    token = canonical_dispatch_token(identity)

    result = reconcile_uncertain_dispatch(
        identity,
        [
            {
                "tasks": [
                    {"id": "1", "repo": "other", "pull_request_id": 99, "prompt": "unrelated"},
                    {"id": "task-1", "repo": "repo", "pull_request_id": 8, "prompt": f"agdt-dispatch-token: {token}"},
                ],
                "repo": "repo",
                "pull_request_id": 8,
                "has_more": False,
            }
        ],
    )

    assert result.outcome == "unique_match"
    assert result.task_id == "task-1"


def test_rejects_bad_pages_and_scopes() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)
    token = canonical_dispatch_token(identity)
    base = {"id": "1", "repo": "repo", "pull_request_id": 8, "prompt": f"agdt:dispatch: {token}"}
    bad_candidates = [
        {**base, "repo": "wrong"},
        {**base, "pull_request_id": 9},
        {**base, "id": 0},
        {**base, "id": "bad/id"},
        {**base, "id": True},
        {**base, "repo": "a/b/c"},
        {**base, "pull_request_id": "8"},
    ]
    for candidate in bad_candidates:
        result = reconcile_uncertain_dispatch(identity, [{"tasks": [candidate], "has_more": False}])
        assert result.outcome == "incomplete"
    pages: tuple[object, ...] = (
        None,
        [],
        {"tasks": ["bad"], "has_more": False},
        {"tasks": [], "status": 401, "has_more": False},
        {"tasks": [], "status": 429, "has_more": False},
        {"tasks": [], "status": 200, "status_code": 201, "has_more": False},
        {"tasks": [], "status": 200, "status_code": 401, "has_more": False},
        {"tasks": [], "status": [200], "has_more": False},
        {"tasks": [], "authorized": False, "has_more": False},
        {"tasks": [], "authorized": 0, "has_more": False},
        {"tasks": [], "partial": True, "has_more": False},
        {"tasks": [], "partial": 0, "has_more": False},
        {"tasks": [], "partial": False, "truncated": True, "has_more": False},
        {"tasks": [], "truncated": "false", "has_more": False},
        {"tasks": [], "has_more": "true"},
        {"tasks": [], "has_more": False, "next_token": "next"},
        {"tasks": [], "next": None, "next_token": "next"},
        {"tasks": [], "next": "next", "continuation": "other"},
        {"tasks": [], "is_last": "true"},
        {"tasks": [], "has_more": True, "next_token": "next", "is_last": True},
        {"tasks": [], "is_last": False},
        {"tasks": [], "has_more": False, "is_last": False},
        {"tasks": [], "has_more": True, "next_token": "next", "is_last": False},
    )
    for page in pages:
        assert reconcile_uncertain_dispatch(identity, [page]).outcome == "incomplete"
    assert (
        reconcile_uncertain_dispatch(
            identity, [{"data": {"tasks": []}, "repo": "repo", "pull_request_id": 8, "has_more": False}]
        ).outcome
        == "complete_miss"
    )
    assert reconcile_uncertain_dispatch(identity, [{"has_more": False}]).outcome == "incomplete"
    assert reconcile_uncertain_dispatch(identity, [{"data": {"unexpected": []}, "has_more": False}]).outcome == (
        "incomplete"
    )
    assert reconcile_uncertain_dispatch(
        identity, [{"tasks": [], "repo": "repo", "pull_request_id": 8, "authorized": True, "has_more": False}]
    ).outcome == ("complete_miss")
    assert reconcile_uncertain_dispatch(
        identity, [{"tasks": [], "repo": "repo", "pull_request_id": 8, "truncated": False, "has_more": False}]
    ).outcome == ("complete_miss")


def test_follows_callable_continuation_until_completion() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)
    token = canonical_dispatch_token(identity)
    calls = []

    def fetch(cursor: object | None) -> object:
        calls.append(cursor)
        if cursor is None:
            return {"tasks": [], "has_more": True, "next_token": "next"}
        return {
            "tasks": [{"id": "3", "repo": "repo", "pull_request_id": 8, "prompt": f"agdt-dispatch-token: {token}"}],
            "has_more": False,
        }

    result = reconcile_uncertain_dispatch(identity, fetch)
    assert result.outcome == "unique_match"
    assert calls == [None, "next"]


def test_fails_closed_for_repeated_or_malformed_continuations() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)

    def repeated(cursor: object | None) -> object:
        return (
            {"tasks": [], "has_more": True, "next_token": "next"}
            if cursor is None
            else {"tasks": [], "has_more": True, "next_token": "next"}
        )

    def malformed(_cursor: object | None) -> object:
        return {"tasks": [], "has_more": True, "next_token": {"page": 2}}

    assert reconcile_uncertain_dispatch(identity, repeated).outcome == "incomplete"
    assert reconcile_uncertain_dispatch(identity, malformed).outcome == "incomplete"
    assert reconcile_uncertain_dispatch(identity, lambda _cursor: None).outcome == "incomplete"


def test_fails_closed_when_callable_stops_without_a_continuation_token() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)

    def incomplete_fetch(cursor: object | None) -> object:
        return {"tasks": [], "has_more": True, "next_token": "next"} if cursor is None else {"tasks": []}

    assert reconcile_uncertain_dispatch(identity, incomplete_fetch).outcome == "incomplete"


def test_fails_closed_when_callable_fetch_raises() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)

    def failing_fetch(_cursor: object | None) -> object:
        raise RuntimeError("boom")

    assert reconcile_uncertain_dispatch(identity, failing_fetch).outcome == "incomplete"


def test_fails_closed_when_iterable_fetch_raises() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)

    def pages() -> Iterator[object]:
        yield {"tasks": [], "has_more": True, "next_token": "next"}
        raise RuntimeError("boom")

    result = reconcile_uncertain_dispatch(identity, pages())
    assert result.outcome == "incomplete"
    assert result.evidence is not None
    assert result.evidence["pages"] == 1


def test_fails_closed_when_iterable_trailing_page_check_raises() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)

    class RaisesAfterEnd:
        def __iter__(self) -> Iterator[object]:
            return self

        def __next__(self) -> object:
            if not hasattr(self, "_seen"):
                self._seen = True
                return {"tasks": [], "has_more": False}
            raise RuntimeError("boom")

    result = reconcile_uncertain_dispatch(identity, RaisesAfterEnd())
    assert result.outcome == "incomplete"
    assert result.evidence is not None
    assert result.evidence["pages"] == 2


def test_fails_closed_when_iterable_exceeds_follow_up_budget() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)
    page_limit = guards_module._MAX_RECONCILIATION_FOLLOW_UPS + 5
    seen = 0

    def pages() -> Iterator[object]:
        nonlocal seen
        for index in range(page_limit):
            seen += 1
            yield {"tasks": [], "has_more": True, "next_token": f"next-{index}"}

    result = reconcile_uncertain_dispatch(identity, pages())

    assert result.outcome == "incomplete"
    assert result.evidence is not None
    assert result.evidence["pages"] == guards_module._MAX_RECONCILIATION_FOLLOW_UPS + 2
    assert seen == guards_module._MAX_RECONCILIATION_FOLLOW_UPS + 2


def test_treats_an_unattested_empty_page_as_incomplete() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)

    result = reconcile_uncertain_dispatch(identity, [{"tasks": [], "has_more": False}])

    assert result.outcome == "incomplete"


def test_treats_an_attested_empty_page_as_authoritative_complete_miss() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)

    result = reconcile_uncertain_dispatch(
        identity, [{"tasks": [], "repo": "repo", "pull_request_id": 8, "has_more": False}]
    )

    assert result.outcome == "complete_miss"


def test_treats_nonmatching_scoped_tasks_as_authoritative_complete_miss() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)

    result = reconcile_uncertain_dispatch(
        identity,
        [
            {
                "tasks": [{"id": "task-9", "repo": "repo", "pull_request_id": 8, "prompt": "unrelated"}],
                "repo": "repo",
                "pull_request_id": 8,
                "has_more": False,
            }
        ],
    )

    assert result.outcome == "complete_miss"


def test_fails_closed_for_mismatched_page_level_scope_metadata() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)

    result = reconcile_uncertain_dispatch(
        identity, [{"tasks": [], "repo": "wrong", "pull_request_id": 8, "has_more": False}]
    )

    assert result.outcome == "incomplete"


def test_fails_closed_for_trailing_pages_after_explicit_end() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)
    token = canonical_dispatch_token(identity)

    result = reconcile_uncertain_dispatch(
        identity,
        [
            {"tasks": [], "has_more": False},
            {
                "tasks": [
                    {"id": "44", "repo": "repo", "pull_request_id": 8, "prompt": f"agdt-dispatch-token: {token}"}
                ],
                "has_more": False,
            },
        ],
    )

    assert result.outcome == "incomplete"


def test_fails_closed_for_trailing_none_after_explicit_end() -> None:
    identity = DispatchIdentity("repo", 8, SHA, 1)

    result = reconcile_uncertain_dispatch(
        identity,
        [
            {"tasks": [], "has_more": False},
            None,
        ],
    )

    assert result.outcome == "incomplete"
