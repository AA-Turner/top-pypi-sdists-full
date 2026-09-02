"""Tests for _pr_artifact_from_payload in retro_spec/artifact_collector.py."""

from __future__ import annotations

from agentic_devtools.cli.speckit.retro_spec.artifact_collector import _pr_artifact_from_payload


class TestPrArtifactFromPayload:
    """Tests for the _pr_artifact_from_payload normalizer."""

    def test_returns_artifact_for_valid_payload(self) -> None:
        """A well-formed dict with required fields produces a PRArtifact."""
        payload = {
            "number": 42,
            "title": "feat: something",
            "body": "description",
            "state": "MERGED",
            "mergedAt": "2024-01-01",
        }
        artifact = _pr_artifact_from_payload(payload)
        assert artifact is not None
        assert artifact.number == 42
        assert artifact.title == "feat: something"
        assert artifact.body == "description"
        assert artifact.state == "MERGED"
        assert artifact.merged_at == "2024-01-01"

    def test_returns_none_for_non_dict(self) -> None:
        """Non-dict payloads are rejected."""
        assert _pr_artifact_from_payload("not a dict") is None
        assert _pr_artifact_from_payload(None) is None
        assert _pr_artifact_from_payload(42) is None

    def test_returns_none_for_zero_number(self) -> None:
        """A PR number of 0 is rejected as invalid."""
        assert _pr_artifact_from_payload({"number": 0, "title": "t"}) is None

    def test_returns_none_for_negative_number(self) -> None:
        """A negative PR number is rejected."""
        assert _pr_artifact_from_payload({"number": -1, "title": "t"}) is None

    def test_returns_none_for_boolean_number(self) -> None:
        """bool is a subclass of int; True must not be accepted as a PR number."""
        assert _pr_artifact_from_payload({"number": True, "title": "t"}) is None
        assert _pr_artifact_from_payload({"number": False, "title": "t"}) is None

    def test_returns_none_for_non_int_number(self) -> None:
        """A string PR number is rejected."""
        assert _pr_artifact_from_payload({"number": "42", "title": "t"}) is None

    def test_returns_none_for_non_string_title(self) -> None:
        """A non-string title is rejected."""
        assert _pr_artifact_from_payload({"number": 1, "title": 99}) is None

    def test_defaults_body_to_empty_string_when_absent(self) -> None:
        """Missing body defaults to empty string."""
        artifact = _pr_artifact_from_payload({"number": 1, "title": "t"})
        assert artifact is not None
        assert artifact.body == ""

    def test_defaults_body_to_empty_string_when_null(self) -> None:
        """Null body (JSON null) defaults to empty string."""
        artifact = _pr_artifact_from_payload({"number": 1, "title": "t", "body": None})
        assert artifact is not None
        assert artifact.body == ""

    def test_defaults_state_to_merged_when_absent(self) -> None:
        """Missing state defaults to 'MERGED'."""
        artifact = _pr_artifact_from_payload({"number": 1, "title": "t"})
        assert artifact is not None
        assert artifact.state == "MERGED"

    def test_defaults_merged_at_to_empty_string_when_absent(self) -> None:
        """Missing mergedAt defaults to empty string."""
        artifact = _pr_artifact_from_payload({"number": 1, "title": "t"})
        assert artifact is not None
        assert artifact.merged_at == ""
