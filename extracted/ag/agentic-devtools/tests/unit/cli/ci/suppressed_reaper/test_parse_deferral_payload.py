"""Tests for suppressed_reaper.parse_deferral_payload()."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.suppressed_reaper import parse_deferral_payload
from tests.unit.cli.ci.suppressed_reaper._fixtures import REVIEW_ID, issue_body


def _marker(payload: str) -> str:
    return f"<!-- ai-pr-loop:suppressed-comment-deferral {payload} -->"


class TestParseDeferralPayload:
    """The issue-side marker is the authoritative source of ``finding_count``."""

    def test_returns_the_decoded_payload(self) -> None:
        """A well-formed marker yields its JSON payload."""
        payload = parse_deferral_payload(issue_body(finding_count=3))
        assert payload is not None
        assert payload["review_id"] == REVIEW_ID
        assert payload["finding_count"] == 3

    def test_returns_none_when_the_marker_is_absent(self) -> None:
        """A body that is not a deferral issue yields nothing."""
        assert parse_deferral_payload("## Just an issue") is None

    def test_returns_none_for_empty_body(self) -> None:
        """An empty body is handled without raising."""
        assert parse_deferral_payload("") is None

    def test_returns_none_for_invalid_json(self) -> None:
        """A malformed payload is rejected rather than raised."""
        assert parse_deferral_payload(_marker("{not json}")) is None

    def test_returns_none_for_a_non_object_payload(self) -> None:
        """The marker pattern only captures a braced object, so an array never matches."""
        assert parse_deferral_payload(_marker("[1, 2]")) is None

    @pytest.mark.parametrize(
        "payload",
        [
            '{"review_id":1}',
            '{"finding_count":1}',
            '{"review_id":"1","finding_count":1}',
            '{"review_id":1,"finding_count":"1"}',
            '{"review_id":true,"finding_count":1}',
            '{"review_id":1,"finding_count":false}',
        ],
    )
    def test_returns_none_when_required_integers_are_missing_or_mistyped(self, payload: str) -> None:
        """Both integers must be present and genuinely integral."""
        assert parse_deferral_payload(_marker(payload)) is None

    def test_returns_none_when_marker_is_not_on_the_first_line(self) -> None:
        """The contract requires the marker to be the first line; a later marker is rejected."""
        good_payload = '{"review_id":1,"finding_count":2}'
        body = f"## Some heading\n\n{_marker(good_payload)}"
        assert parse_deferral_payload(body) is None

    def test_returns_none_when_marker_appears_more_than_once(self) -> None:
        """Duplicate markers create ambiguity and are rejected."""
        good_payload = '{"review_id":1,"finding_count":2}'
        m = _marker(good_payload)
        body = f"{m}\n\n{m}"
        assert parse_deferral_payload(body) is None

    @pytest.mark.parametrize(
        "payload",
        [
            '{"pr":1,"review_id":1,"base_sha":"' + "a" * 40 + '","finding_count":0}',
            '{"pr":1,"review_id":0,"base_sha":"' + "a" * 40 + '","finding_count":1}',
            '{"pr":0,"review_id":1,"base_sha":"' + "a" * 40 + '","finding_count":1}',
        ],
    )
    def test_returns_none_when_any_positive_integer_field_is_zero(self, payload: str) -> None:
        """All of pr, review_id, and finding_count must be strictly positive."""
        assert parse_deferral_payload(_marker(payload)) is None

    def test_returns_none_when_pr_field_is_missing(self) -> None:
        """The ``pr`` field is required by the contract."""
        payload = '{"review_id":1,"base_sha":"' + "a" * 40 + '","finding_count":1}'
        assert parse_deferral_payload(_marker(payload)) is None

    def test_returns_none_when_base_sha_is_missing(self) -> None:
        """The ``base_sha`` field is required by the contract."""
        payload = '{"pr":1,"review_id":1,"finding_count":1}'
        assert parse_deferral_payload(_marker(payload)) is None

    @pytest.mark.parametrize(
        "base_sha",
        [
            "abc",  # too short
            "a" * 39,  # one char short of 40
            "a" * 41,  # one char over 40
            "g" * 40,  # not hex
            "A" * 40,  # uppercase not accepted
            "",
        ],
    )
    def test_returns_none_when_base_sha_is_not_40_hex(self, base_sha: str) -> None:
        """base_sha must be exactly 40 lowercase hex characters."""
        payload = f'{{"pr":1,"review_id":1,"base_sha":"{base_sha}","finding_count":1}}'
        assert parse_deferral_payload(_marker(payload)) is None
