"""Tests for _collect_properties()."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.validate_templates import _collect_properties


class TestCollectProperties:
    """Tests for the in-place property-collection helper."""

    def test_non_list_properties_noop(self) -> None:
        """A non-list properties value leaves the sets unchanged."""
        all_names: set[str] = set()
        required: set[str] = set()
        _collect_properties("nope", all_names, required)
        assert all_names == set()
        assert required == set()

    def test_skips_bad_property_entries(self) -> None:
        """Non-dict entries and blank/non-str names are skipped."""
        all_names: set[str] = set()
        required: set[str] = set()
        _collect_properties(
            ["not-a-dict", {"name": "  "}, {"name": 5}, {"name": "ok", "required": True}],
            all_names,
            required,
        )
        assert all_names == {"ok"}
        assert required == {"ok"}

    def test_excluded_required_property_is_known_but_not_required(self) -> None:
        """included_in_template=false keeps the property known without requiring it."""
        all_names: set[str] = set()
        required: set[str] = set()
        _collect_properties(
            [{"name": "secret", "required": True, "included_in_template": False}],
            all_names,
            required,
        )
        assert all_names == {"secret"}
        assert required == set()
