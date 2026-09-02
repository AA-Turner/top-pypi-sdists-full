"""Tests for _known_and_required()."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.template_placeholders import (
    BASE_REQUIRED_PROPERTIES,
    CANONICAL_PLACEHOLDER_NAMES,
)
from agentic_devtools.cli.issue_template.validate_templates import _known_and_required


class TestKnownAndRequired:
    """Tests for resolving known-name and required-property sets."""

    def test_base_when_no_slug(self) -> None:
        """With no slug the base canonical/required sets are returned."""
        known, required = _known_and_required(None, None)
        assert known == set(CANONICAL_PLACEHOLDER_NAMES)
        assert required == set(BASE_REQUIRED_PROPERTIES)

    def test_base_when_slug_not_in_schemas(self) -> None:
        """A slug missing from the schema map falls back to the base sets."""
        known, required = _known_and_required("bug", {"feature": (set(), set())})
        assert known == set(CANONICAL_PLACEHOLDER_NAMES)
        assert required == set(BASE_REQUIRED_PROPERTIES)

    def test_augments_from_schema(self) -> None:
        """A matching slug augments the base sets with schema properties."""
        known, required = _known_and_required("bug", {"bug": ({"severity"}, {"severity"})})
        assert "severity" in known
        assert "severity" in required
