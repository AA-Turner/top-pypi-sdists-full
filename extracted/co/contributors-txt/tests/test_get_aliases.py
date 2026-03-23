from pathlib import Path

import pytest
from contributors_txt.const import DEFAULT_TEAM_ROLE
from contributors_txt.create_content import Alias, get_aliases

aliases_file = Path(__file__).parent / ".contributors_aliases.json"


def test_basic(recwarn: pytest.WarningsRecorder) -> None:
    aliases = get_aliases(aliases_file)
    assert aliases == [
        Alias(
            mails=[
                "66853113+pre-commit-ci[bot]@users.noreply.github.com",
                "49699333+dependabot[bot]@users.noreply.github.com",
            ],
            authoritative_mail="bot@noreply.github.com",
            name="bot",
            team=DEFAULT_TEAM_ROLE,
        ),
        Alias(
            mails=["66853113+pre-commit-ci[bot]@users.noreply.github.com"],
            authoritative_mail="bot@noreply.github.com",
            name="pre-commit-ci[bot]",
            team=DEFAULT_TEAM_ROLE,
        ),
    ]
    assert len(recwarn) == 1
    assert "old copyrite format" in str(recwarn.pop())
