"""Tests for the IssueFacts dataclass."""

import dataclasses

import pytest

from agentic_devtools.cli.ci.models import IssueFacts


class TestIssueFacts:
    """Tests for the IssueFacts dataclass."""

    def test_fields(self) -> None:
        facts = IssueFacts(number=1240, state="open", body="body")
        assert facts.number == 1240
        assert facts.state == "open"
        assert facts.body == "body"
        assert facts.resource_kind == "issue"

    def test_is_frozen(self) -> None:
        facts = IssueFacts(number=1, state="open", body="")
        with pytest.raises(dataclasses.FrozenInstanceError):
            facts.state = "closed"  # type: ignore[misc]
