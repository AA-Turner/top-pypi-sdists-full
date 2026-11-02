import pytest

from agentic_devtools.adapters.pull_request_threads import PullRequestThreadsRequest


def test_valid_request() -> None:
    request = PullRequestThreadsRequest("github", "owner/repo", 12)
    assert request.pull_request_id == 12


@pytest.mark.parametrize(
    "args",
    [
        ("bitbucket", "owner/repo", 1),
        ([], "owner/repo", 1),
        ("github", "", 1),
        ("github", "owner/repo/extra", 1),
        ("github", "owner/repo name", 1),
        ("github", "owner/repo", True),
        ("github", "owner/repo", 0),
    ],
)
def test_rejects_invalid_request(args: tuple[object, object, object]) -> None:
    with pytest.raises(ValueError):
        PullRequestThreadsRequest(*args)  # type: ignore[arg-type]
