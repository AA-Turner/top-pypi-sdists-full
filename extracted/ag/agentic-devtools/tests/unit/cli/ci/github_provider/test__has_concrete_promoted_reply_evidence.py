import pytest

from agentic_devtools.cli.ci.github_provider import _has_concrete_promoted_reply_evidence


@pytest.mark.parametrize(
    "reply",
    [
        "Fixed in `agentic_devtools/cli/ci/github_provider.py:6530`.",
        "Resolved at Dockerfile:12.",
        "Resolved at .github/CODEOWNERS:8.",
        "Fixed the validation error in commit abc1234.",
        "Not only fixed in commit abc1234, but also verified at Dockerfile:12.",
        "The issue is fixed in commit `abc1234`.",
        "Verified that the issue is fixed at `src/foo.py:12`.",
        "Verified the fix with `pytest tests/unit/cli/ci/test_review.py::test_promoted_reply` — passed.",
        "Verified with bash scripts/targeted-checks.sh; all checks passed.",
    ],
)
def test__has_concrete_promoted_reply_evidence_accepts_specific_evidence(reply: str) -> None:
    assert _has_concrete_promoted_reply_evidence(reply)


@pytest.mark.parametrize(
    "reply",
    [
        "",
        "Already fixed.",
        "Applied fix.",
        "Tests passed.",
        "Updated `agentic_devtools/cli/ci/github_provider.py`.",
        "Fixed in commit `not-a-commit`.",
        "Ran `pytest tests/unit/cli/ci/test_review.py::test_promoted_reply` but it failed.",
        "The bug is still present at `src/foo.py:12`.",
        "Verified reproduction at `src/foo.py:12`.",
        "Verified the bug reproduces at `src/foo.py:12`.",
        "Verified the defect is present at `src/foo.py:12`.",
        "Verified that the issue exists at `src/foo.py:12`.",
        "Verified that the defect still reproduces at `src/foo.py:12`.",
        "The issue persists at `src/foo.py:12`; fixed in commit `abc1234`.",
        "The issue is not fixed in commit `abc1234`.",
        "Verified that commit `abc1234` does not fix the issue.",
        "The fix still needs to be implemented at `src/foo.py:12`.",
        "The fix has yet to be implemented at `src/foo.py:12`.",
        "The fix is unresolved; `pytest tests/unit/cli/ci/test_review.py::test_promoted_reply` passed.",
        "Verified with bash scripts/targeted-checks.sh; one check failed.",
        "Fixed at `src/foo.py:12`; `pytest tests/unit/test_foo.py::test_fix` failed.",
        "Verified with pytest tests/unit/test_foo.py::test_fix — 2 failures, 3 passed.",
        "Fixed in commit `abc1234`.\nFAILED tests/unit/test_foo.py::test_fix - AssertionError",
        "Fixed in commit `abc1234`.\n================= 1 failed, 3 passed in 0.4s =================",
        "Fixed in commit `abc1234`.\n================= 2 failures, 3 passed in 0.4s =================",
        "Resolved in commit `abc1234`; 1 test failed.",
        "Fixed at `src/foo.py:12`; bash scripts/targeted-checks.sh failed.",
    ],
)
def test__has_concrete_promoted_reply_evidence_rejects_unsupported_claims(reply: str) -> None:
    assert not _has_concrete_promoted_reply_evidence(reply)
