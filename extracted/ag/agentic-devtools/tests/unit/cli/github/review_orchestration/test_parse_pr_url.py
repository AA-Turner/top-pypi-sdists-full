import pytest

from agentic_devtools.cli.github.review_orchestration import parse_pr_url


def test_canonical_url_and_optional_review_hint():
    assert parse_pr_url("https://github.com/Example/Project/pull/7") == ("example/project", 7, None)
    assert parse_pr_url("https://github.com/Example/Project/pull/7#pullrequestreview-19") == ("example/project", 7, 19)


@pytest.mark.parametrize(
    "url",
    [
        None,
        7,
        "",
        "http://github.com/a/b/pull/1",
        "https://github.com.evil/a/b/pull/1",
        "https://user@github.com/a/b/pull/1",
        "https://github.com/a/b/pull/0",
        "https://github.com/a/b/pull/01",
        "https://github.com/a/b/pull/1/files",
        "https://github.com/a/b/pull/1?x=y",
        "https://github.com/a/b/pull/1#issuecomment-2",
        "https://github.com/a/b/pull/1#pullrequestreview-0",
        "https://github.com/a/../pull/1",
        "https://github.com/-a/b/pull/1",
        "https://github.com/a/b/pull/1\n",
    ],
)
def test_rejects_noncanonical_or_ambiguous_url(url):
    with pytest.raises(ValueError, match="canonical GitHub PR URL"):
        parse_pr_url(url)
