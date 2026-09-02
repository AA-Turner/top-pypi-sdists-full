"""Tests for parse_classification function."""

from __future__ import annotations

import copy
import warnings

import pytest

from agentic_devtools.skill_classification import Classification, parse_classification

# ---------------------------------------------------------------------------
# US1: Well-formed inputs
# ---------------------------------------------------------------------------


class TestParseWellFormed:
    """Well-formed inputs return correct Classification without warnings."""

    def test_full_requires_block(self) -> None:
        fm = {"agdt": {"requires": {"issue_adapter": "jira", "code_hosting": "azure_devops"}}}
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            result = parse_classification(fm)
        assert result == Classification(
            requires_issue_adapter="jira",
            requires_code_hosting="azure_devops",
            always=False,
        )

    def test_partial_issue_adapter_only(self) -> None:
        fm = {"agdt": {"requires": {"issue_adapter": "github"}}}
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            result = parse_classification(fm)
        assert result.requires_issue_adapter == "github"
        assert result.requires_code_hosting is None

    def test_partial_code_hosting_only(self) -> None:
        fm = {"agdt": {"requires": {"code_hosting": "github"}}}
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            result = parse_classification(fm)
        assert result.requires_issue_adapter is None
        assert result.requires_code_hosting == "github"

    def test_always_true_with_requires(self) -> None:
        fm = {"agdt": {"always": True, "requires": {"issue_adapter": "jira"}}}
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            result = parse_classification(fm)
        assert result.always is True
        assert result.requires_issue_adapter == "jira"

    def test_always_true_no_requires(self) -> None:
        fm = {"agdt": {"always": True}}
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            result = parse_classification(fm)
        assert result.always is True
        assert result.requires_issue_adapter is None
        assert result.requires_code_hosting is None


# ---------------------------------------------------------------------------
# SC-001: Empty/absent/None agdt variations → universal, no warning
# ---------------------------------------------------------------------------


class TestParseAbsentEmptyNull:
    """FR-001: Empty/absent/None variations return universal with no warning."""

    @pytest.mark.parametrize(
        "fm",
        [
            {},
            {"agdt": None},
            {"agdt": {}},
            {"agdt": {"requires": None}},
            {"agdt": {"requires": {}}},
        ],
        ids=[
            "empty-dict",
            "agdt-none",
            "agdt-empty-mapping",
            "requires-none",
            "requires-empty-mapping",
        ],
    )
    def test_universal_no_warning(self, fm: dict) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            result = parse_classification(fm)
        assert result == Classification()


# ---------------------------------------------------------------------------
# US2: Non-mapping frontmatter (FR-001 non-mapping guard)
# ---------------------------------------------------------------------------


class TestParseNonMappingFrontmatter:
    """FR-001: Non-mapping frontmatter → universal, no warning, no exception."""

    @pytest.mark.parametrize(
        "fm",
        [None, "bare-string", 42, 3.14, [], True],
        ids=["none", "string", "int", "float", "list", "bool"],
    )
    def test_non_mapping_frontmatter(self, fm: object) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            result = parse_classification(fm)
        assert result == Classification()


# ---------------------------------------------------------------------------
# US2: Non-mapping agdt (FR-002)
# ---------------------------------------------------------------------------


class TestParseNonMappingAgdt:
    """FR-002: Non-mapping agdt → universal with UserWarning."""

    @pytest.mark.parametrize(
        "agdt_value",
        ["not-a-mapping", 42, ["list"], True],
        ids=["string", "int", "list", "bool"],
    )
    def test_non_mapping_agdt_warns(self, agdt_value: object) -> None:
        fm = {"agdt": agdt_value}
        with pytest.warns(UserWarning):
            result = parse_classification(fm)
        assert result == Classification()


# ---------------------------------------------------------------------------
# US2: Non-mapping requires with valid always (FR-003)
# ---------------------------------------------------------------------------


class TestParseNonMappingRequires:
    """FR-003: Non-mapping requires → warning, axes=None, always preserved."""

    def test_non_mapping_requires_preserves_always(self) -> None:
        fm = {"agdt": {"requires": "not-a-mapping", "always": True}}
        with pytest.warns(UserWarning):
            result = parse_classification(fm)
        assert result.requires_issue_adapter is None
        assert result.requires_code_hosting is None
        assert result.always is True

    def test_non_mapping_requires_list(self) -> None:
        fm = {"agdt": {"requires": ["jira"], "always": False}}
        with pytest.warns(UserWarning):
            result = parse_classification(fm)
        assert result == Classification(always=False)


# ---------------------------------------------------------------------------
# US2: Invalid enum values (FR-004)
# ---------------------------------------------------------------------------


class TestParseInvalidEnums:
    """FR-004: Invalid enum values dropped per-axis with warning."""

    def test_single_invalid_issue_adapter(self) -> None:
        fm = {"agdt": {"requires": {"issue_adapter": "invalid_value"}}}
        with pytest.warns(UserWarning):
            result = parse_classification(fm)
        assert result.requires_issue_adapter is None

    def test_single_invalid_code_hosting(self) -> None:
        fm = {"agdt": {"requires": {"code_hosting": "invalid_value"}}}
        with pytest.warns(UserWarning):
            result = parse_classification(fm)
        assert result.requires_code_hosting is None

    def test_mixed_valid_invalid(self) -> None:
        fm = {"agdt": {"requires": {"issue_adapter": "invalid", "code_hosting": "github"}}}
        with pytest.warns(UserWarning):
            result = parse_classification(fm)
        assert result.requires_issue_adapter is None
        assert result.requires_code_hosting == "github"

    def test_all_invalid_yields_universal(self) -> None:
        fm = {"agdt": {"requires": {"issue_adapter": "bad", "code_hosting": "worse"}}}
        with pytest.warns(UserWarning):
            result = parse_classification(fm)
        assert result.requires_issue_adapter is None
        assert result.requires_code_hosting is None

    def test_non_string_axis_value_dropped(self) -> None:
        fm = {"agdt": {"requires": {"issue_adapter": 123}}}
        with pytest.warns(UserWarning):
            result = parse_classification(fm)
        assert result.requires_issue_adapter is None


# ---------------------------------------------------------------------------
# FR-010: always coercion edge cases
# ---------------------------------------------------------------------------


class TestParseAlwaysCoercion:
    """FR-010: Explicit allowlist coercion of 'always' field."""

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (True, True),
            (False, False),
            (1, True),
            (0, False),
            ("true", True),
            ("True", True),
            ("TRUE", True),
            ("yes", True),
            ("Yes", True),
            ("on", True),
            ("1", True),
            ("false", False),
            ("False", False),
            ("no", False),
            ("off", False),
            ("0", False),
        ],
        ids=[
            "bool-true",
            "bool-false",
            "int-1",
            "int-0",
            "str-true-lower",
            "str-true-title",
            "str-true-upper",
            "str-yes-lower",
            "str-yes-title",
            "str-on",
            "str-1",
            "str-false-lower",
            "str-false-title",
            "str-no",
            "str-off",
            "str-0",
        ],
    )
    def test_accepted_values_no_warning(self, value: object, expected: bool) -> None:
        fm = {"agdt": {"always": value}}
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            result = parse_classification(fm)
        assert result.always is expected

    @pytest.mark.parametrize(
        "value",
        ["maybe", "2", "enabled", 99, 3.14, None, []],
        ids=["maybe", "str-2", "enabled", "int-99", "float", "none", "list"],
    )
    def test_unrecognized_warns_and_defaults_false(self, value: object) -> None:
        fm = {"agdt": {"always": value}}
        with pytest.warns(UserWarning):
            result = parse_classification(fm)
        assert result.always is False


# ---------------------------------------------------------------------------
# FR-005: Input dict not mutated
# ---------------------------------------------------------------------------


class TestParseNoMutation:
    """FR-005: parse_classification does not mutate input dict."""

    def test_input_not_mutated(self) -> None:
        fm = {"agdt": {"requires": {"issue_adapter": "jira", "code_hosting": "github"}, "always": True}}
        original = copy.deepcopy(fm)
        parse_classification(fm)
        assert fm == original
