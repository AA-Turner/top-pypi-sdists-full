import pytest

from agentic_devtools.cli.ci.models import CLOUD_CODING_AGENT_LOGINS, COPILOT_REVIEWER_LOGIN
from agentic_devtools.cli.ci.pipeline.validation_evidence import is_evidence_author


@pytest.mark.parametrize(
    "login",
    ["Copilot", *sorted(CLOUD_CODING_AGENT_LOGINS)],
)
def test_accepts_evidence_authors_case_insensitively(login: str) -> None:
    assert is_evidence_author(login)
    assert is_evidence_author(login.swapcase())


@pytest.mark.parametrize("login", [None, 1, [], {}, COPILOT_REVIEWER_LOGIN, "human-user"])
def test_rejects_non_strings_and_non_evidence_authors(login: object) -> None:
    assert not is_evidence_author(login)
