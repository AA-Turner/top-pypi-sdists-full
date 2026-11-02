"""Tests for check_unknown_placeholders() (FR-002, W001)."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.issue_template.template_placeholders import (
    CANONICAL_PLACEHOLDER_NAMES,
    PLACEHOLDER_ALIASES,
)
from agentic_devtools.cli.issue_template.validate_templates import (
    check_unknown_placeholders,
)


class TestCheckUnknownPlaceholders:
    """Tests for W001 unknown-placeholder detection."""

    @pytest.mark.parametrize(
        "placeholder_name",
        sorted(CANONICAL_PLACEHOLDER_NAMES)
        + sorted(PLACEHOLDER_ALIASES)
        + ["severity", "raw_field", "custom_provider_value", "desciption", "titel"],
    )
    def test_placeholder_name_permutations(self, placeholder_name: str) -> None:
        """SC-002: at least 15 placeholder-name permutations are classified correctly."""
        known = set(CANONICAL_PLACEHOLDER_NAMES) | {"severity", "raw_field", "custom_provider_value"}
        diags = check_unknown_placeholders(f"{{{{{placeholder_name}}}}}", known)
        if placeholder_name in known or placeholder_name in PLACEHOLDER_ALIASES:
            assert diags == []
        else:
            assert [diag.code for diag in diags] == ["W001"]

    def test_alias_resolves_to_canonical(self) -> None:
        """An alias placeholder (issue_id -> id) is recognized as known."""
        assert check_unknown_placeholders("{{issue_id}}", set(CANONICAL_PLACEHOLDER_NAMES)) == []

    def test_unknown_placeholder_reports_w001(self) -> None:
        """A typo placeholder not in the known set is reported as W001."""
        diags = check_unknown_placeholders("{{desciption}}", set(CANONICAL_PLACEHOLDER_NAMES))
        assert len(diags) == 1
        assert diags[0].code == "W001"
        assert diags[0].level == "warning"
        assert diags[0].line == 1
        assert diags[0].column == 1
        assert "desciption" in diags[0].message

    def test_type_specific_property_is_known(self) -> None:
        """A name present in the extra known set is not flagged."""
        known = set(CANONICAL_PLACEHOLDER_NAMES) | {"severity"}
        assert check_unknown_placeholders("{{severity}}", known) == []

    def test_multiple_unknown_placeholders(self) -> None:
        """Each unknown placeholder yields its own diagnostic."""
        diags = check_unknown_placeholders("{{foo}} {{bar}}", set(CANONICAL_PLACEHOLDER_NAMES))
        assert [d.message for d in diags] == [
            "Unknown placeholder: '{{foo}}'",
            "Unknown placeholder: '{{bar}}'",
        ]
