"""Tests for ``_is_tagged_cost_warning``."""

from agentic_devtools.cli.config.project_config import (
    WARN_COST_DATA_INVALID,
    WARN_COST_DATA_MISSING,
    WARN_COST_DATA_STALE,
    _is_tagged_cost_warning,
)


class TestIsTaggedCostWarning:
    """Tests for the cost-warning tag detector."""

    def test_missing_tag_is_recognized(self):
        assert _is_tagged_cost_warning(f"{WARN_COST_DATA_MISSING}: some detail") is True

    def test_invalid_tag_is_recognized(self):
        assert _is_tagged_cost_warning(f"{WARN_COST_DATA_INVALID}: some detail") is True

    def test_stale_tag_is_recognized(self):
        assert _is_tagged_cost_warning(f"{WARN_COST_DATA_STALE}: some detail") is True

    def test_untagged_string_is_not_recognized(self):
        assert _is_tagged_cost_warning("just a plain error message") is False

    def test_empty_string_is_not_recognized(self):
        assert _is_tagged_cost_warning("") is False

    def test_partial_prefix_is_not_recognized(self):
        assert _is_tagged_cost_warning("WARN_COST_DATA") is False

    def test_tag_without_colon_is_not_recognized(self):
        assert _is_tagged_cost_warning(WARN_COST_DATA_MISSING) is False
