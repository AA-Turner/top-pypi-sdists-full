import pytest

from agentic_devtools.cli.ci.models import IssueCommentInfo
from agentic_devtools.cli.ci.pipeline.validation_evidence import (
    BLOCKER_MARKER,
    EVIDENCE_REQUIRED_LABEL,
    FOLLOWUP_KEY,
    GATE_STATE_KEY,
    RECOVERY_MARKER,
    EvidenceGateState,
    find_head_evidence,
)

HEAD_SHA = "0123456789abcdef0123456789abcdef01234567"


def comment(author: str, body: str) -> IssueCommentInfo:
    return IssueCommentInfo(id=1, author=author, body=body)


def test_recognizes_real_heading_after_quoted_request() -> None:
    evidence = comment(
        "Copilot",
        f"> Please add the validation receipt.\n\n## Validation evidence\n\nValidated head `{HEAD_SHA}`.",
    )

    assert find_head_evidence([evidence], HEAD_SHA) is evidence


@pytest.mark.parametrize(
    "body",
    [
        f"> ## Validation evidence\n{HEAD_SHA}",
        f"```markdown\n## Validation evidence\n{HEAD_SHA}\n```",
    ],
)
def test_ignores_quoted_and_fenced_headings(body: str) -> None:
    assert find_head_evidence([comment("Copilot", body)], HEAD_SHA) is None


@pytest.mark.parametrize("invalid_closer", ["```", "````python"])
def test_ignores_headings_inside_fence_after_invalid_closer(invalid_closer: str) -> None:
    body = f"````text\n{invalid_closer}\n## Validation evidence\n{HEAD_SHA}\n````"

    assert find_head_evidence([comment("Copilot", body)], HEAD_SHA) is None


def test_ignores_headings_after_four_space_indented_closer() -> None:
    body = f"```\n    ```\n## Validation evidence\n{HEAD_SHA}"

    assert find_head_evidence([comment("Copilot", body)], HEAD_SHA) is None


def test_recognizes_heading_after_inline_code_span() -> None:
    body = f"```example```\n## Validation evidence\n{HEAD_SHA}"

    assert find_head_evidence([comment("Copilot", body)], HEAD_SHA) is not None


def test_recognizes_heading_after_closing_fence_with_trailing_whitespace() -> None:
    body = f"````text\nexample\n````  \t\n## Validation evidence\n{HEAD_SHA}"

    assert find_head_evidence([comment("Copilot", body)], HEAD_SHA) is not None


@pytest.mark.parametrize("token", [HEAD_SHA, HEAD_SHA[:7], HEAD_SHA[:39]])
def test_accepts_full_and_short_head_prefixes(token: str) -> None:
    evidence = comment("copilot-swe-agent", f"## Validation evidence\n{token}")

    assert find_head_evidence([evidence], HEAD_SHA) is evidence


@pytest.mark.parametrize(
    ("body", "head_sha"),
    [
        (f"## Validation evidence\n{HEAD_SHA}", "not-a-sha"),
        (f"## Validation evidence\n{HEAD_SHA}", HEAD_SHA[:-1]),
        (f"## Validation evidence\n{HEAD_SHA}", HEAD_SHA + "0"),
        ("## Validation evidence\n0123456g", HEAD_SHA),
        ("## Validation evidence\n012345", HEAD_SHA),
        ("## Validation evidence\nffffffff", HEAD_SHA),
    ],
)
def test_rejects_invalid_or_nonmatching_sha_tokens(body: str, head_sha: str) -> None:
    assert find_head_evidence([comment("Copilot", body)], head_sha) is None


def test_returns_last_qualifying_evidence_and_ignores_irrelevant_comments() -> None:
    first = comment("Copilot", f"## Validation evidence\n{HEAD_SHA[:7]}")
    wrong_author = comment("human-user", f"## Validation evidence\n{HEAD_SHA}")
    wrong_head = comment("Copilot", "## Validation evidence\nffffffff")
    missing_heading = comment("Copilot", HEAD_SHA)
    last = comment("app/copilot-swe-agent", f"## validation EVIDENCE\n{HEAD_SHA}")

    assert find_head_evidence([first, wrong_author, wrong_head, missing_heading, last], HEAD_SHA) is last


def test_exposes_gate_state_and_marker_constants() -> None:
    assert [state.value for state in EvidenceGateState] == [
        "not_applicable",
        "satisfied",
        "missing",
        "unknown",
    ]
    assert EVIDENCE_REQUIRED_LABEL == "ai-validation-evidence-required"
    assert RECOVERY_MARKER == "<!-- agdt:validation-evidence-recovery:v1 -->"
    assert BLOCKER_MARKER == "<!-- agdt:validation-evidence-blocked:v1 -->"
    assert GATE_STATE_KEY == "validation_evidence_gate"
    assert FOLLOWUP_KEY == "validation_evidence_followup"
