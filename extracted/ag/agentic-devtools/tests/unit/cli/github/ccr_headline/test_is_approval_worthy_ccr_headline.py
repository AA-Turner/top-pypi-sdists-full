import pytest

from agentic_devtools.cli.github.ccr_headline import is_approval_worthy_ccr_headline


@pytest.mark.parametrize(
    "headline",
    [
        "Ready",
        "This PR is ready.",
        "Ready for human approval.",
        "This pull request is ready to merge!",
        "Only needs human approval/merge.",
        "Awaiting human approval.",
        "Only needs final human review.",
    ],
)
def test_recognizes_explicit_approval_only_headlines(headline: str) -> None:
    assert is_approval_worthy_ccr_headline(headline)


@pytest.mark.parametrize(
    "headline",
    [
        "Previously reported regressions remain unresolved.",
        "Potential vulnerabilities require final human review.",
        "Data corruption requires final human review.",
        "The endpoint exposes credentials and requires final human review.",
        "Broad modernization and limited baseline verification require final human review.",
        "",
    ],
)
def test_does_not_fast_path_non_approval_headlines(headline: str) -> None:
    assert not is_approval_worthy_ccr_headline(headline)
