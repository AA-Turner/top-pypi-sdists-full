"""Tests for ``build_feature_branch_name``."""

from agentic_devtools.cli.speckit.scaffold_new_feature import build_feature_branch_name


def test_build_feature_branch_name_uses_short_name() -> None:
    result = build_feature_branch_name("Add user authentication", short_name="really-long-short-name-here")
    assert result == "really-long-short-name-here"


def test_build_feature_branch_name_uses_feature_fallback() -> None:
    assert build_feature_branch_name("   ") == "feature"


def test_build_feature_branch_name_filters_stop_words() -> None:
    # "Add" and "to" are stop words; "login" and "flow" are meaningful
    assert build_feature_branch_name("Add login flow") == "login-flow"


def test_build_feature_branch_name_keeps_first_three_meaningful_words() -> None:
    # Exactly 3 meaningful words retained
    assert build_feature_branch_name("Add user authentication flow") == "user-authentication-flow"


def test_build_feature_branch_name_keeps_four_when_exactly_four() -> None:
    # Exactly 4 meaningful words → all four are kept
    result = build_feature_branch_name("configure database connection pooling")
    assert result == "configure-database-connection-pooling"


def test_build_feature_branch_name_caps_at_three_when_more_than_four() -> None:
    # More than 4 meaningful words → first 3 only
    result = build_feature_branch_name("implement secure oauth login redirect callback")
    assert result == "implement-secure-oauth"
