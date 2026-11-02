from agentic_devtools.cli.ci.dispatch_state import DispatchIdentity
from agentic_devtools.cli.ci.guards import (
    DISPATCH_CONTRACT_MARKER,
    _as_dispatch_tasks_from_comments,
)

SHA = "a" * 40


def test_maps_comment_payload_to_dispatch_task_shape() -> None:
    identity = DispatchIdentity("repo", 7, SHA, 1)
    comments = [
        {"id": 11, "author": "dispatch-bot", "body": f"{DISPATCH_CONTRACT_MARKER}\n{identity.token}\n#agent-task-123"},
    ]

    tasks = _as_dispatch_tasks_from_comments(identity, comments, dispatch_login="dispatch-bot")

    assert tasks == [
        {
            "id": "11",
            "repo": "repo",
            "pull_request_id": 7,
            "prompt": f"agdt-dispatch-token: {identity.token}",
        }
    ]


def test_returns_original_value_for_non_list_payloads() -> None:
    identity = DispatchIdentity("repo", 7, SHA, 1)
    payload: object = "unexpected-shape"

    assert _as_dispatch_tasks_from_comments(identity, payload) == payload


def test_supports_dict_comment_containers() -> None:
    identity = DispatchIdentity("repo", 7, SHA, 1)
    comments = {
        "comments": [{"id": 11, "author": "dispatch-bot", "body": f"{DISPATCH_CONTRACT_MARKER}\n{identity.token}"}]
    }

    tasks = _as_dispatch_tasks_from_comments(identity, comments, dispatch_login="dispatch-bot")

    assert tasks == [
        {
            "id": "11",
            "repo": "repo",
            "pull_request_id": 7,
            "prompt": f"agdt-dispatch-token: {identity.token}",
        }
    ]


def test_ignores_marker_comments_from_other_authors() -> None:
    identity = DispatchIdentity("repo", 7, SHA, 1)
    comments = [{"id": 11, "author": "other-user", "body": f"{DISPATCH_CONTRACT_MARKER}\n{identity.token}"}]

    tasks = _as_dispatch_tasks_from_comments(identity, comments, dispatch_login="dispatch-bot")

    assert tasks == [{"id": "11", "repo": "repo", "pull_request_id": 7, "prompt": ""}]
