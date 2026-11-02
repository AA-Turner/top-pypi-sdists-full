"""Shared offline GitHub CLI responses."""

import json
from types import SimpleNamespace


def _mock_run_safe_response(data):
    class _Result:
        returncode = 0
        stdout = json.dumps(data)
        stderr = ""

    return _Result()


def _page(nodes, *, has_next=False, cursor=None):
    return _mock_run_safe_response(
        {
            "data": {
                "node": {
                    "comments": {
                        "pageInfo": {"hasNextPage": has_next, "endCursor": cursor},
                        "nodes": nodes,
                    }
                }
            }
        }
    )


def _preflight_responses(status: int | None) -> tuple[list, str, list[str]]:
    """Arrange real CLI successes and permanent capability denials for two bases."""
    if status is None:
        return [], "identity", []
    identity = _mock_run_safe_response({"login": "bot"})
    repository = _mock_run_safe_response({"permissions": {"push": True}})
    failure = SimpleNamespace(
        returncode=1,
        stdout=f"HTTP/1.1 {status} Rejected\n\n",
        stderr="private raw response offline-credential",
    )
    if status == 401:
        return [failure] * 2, "identity", ["/user", "/user"]
    responses = [identity, repository if status == 200 else failure] * 2
    capability = "review_eligibility" if status == 200 else "repository_visibility"
    return responses, capability, ["/user", "/repos/base/one", "/user", "/repos/base/two"]
