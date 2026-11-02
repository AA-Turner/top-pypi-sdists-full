from agentic_devtools.adapters.pull_request_create import PullRequestCreateResult


def test_pull_request_create_result_serializes() -> None:
    assert PullRequestCreateResult(True, "github", "created", url="url").as_dict()["url"] == "url"
