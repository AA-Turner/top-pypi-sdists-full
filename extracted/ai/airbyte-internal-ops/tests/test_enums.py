# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for registry StrEnum types."""

from __future__ import annotations

import pytest

from airbyte_ops_mcp.registry._enums import (
    ConnectorLanguage,
    ConnectorType,
    SupportLevel,
)

# ---------------------------------------------------------------------------
# SupportLevel - construction and string identity
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "value,expected",
    [
        pytest.param("archived", SupportLevel.ARCHIVED, id="archived"),
        pytest.param("community", SupportLevel.COMMUNITY, id="community"),
        pytest.param("certified", SupportLevel.CERTIFIED, id="certified"),
    ],
)
def test_support_level_from_value(value: str, expected: SupportLevel) -> None:
    """SupportLevel can be constructed from its string value."""
    assert SupportLevel(value) is expected
    # StrEnum members compare equal to their string value.
    assert expected == value


# ---------------------------------------------------------------------------
# SupportLevel.precedence
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "level,expected_precedence",
    [
        pytest.param(SupportLevel.ARCHIVED, 100, id="archived_100"),
        pytest.param(SupportLevel.COMMUNITY, 200, id="community_200"),
        pytest.param(SupportLevel.CERTIFIED, 300, id="certified_300"),
    ],
)
def test_support_level_precedence(
    level: SupportLevel, expected_precedence: int
) -> None:
    """Each SupportLevel has a well-known integer precedence."""
    assert level.precedence == expected_precedence


@pytest.mark.unit
def test_support_level_precedence_ordering() -> None:
    """Precedence increases from archived -> community -> certified."""
    assert SupportLevel.ARCHIVED.precedence < SupportLevel.COMMUNITY.precedence
    assert SupportLevel.COMMUNITY.precedence < SupportLevel.CERTIFIED.precedence


# ---------------------------------------------------------------------------
# SupportLevel.from_precedence
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "precedence,expected",
    [
        pytest.param(100, SupportLevel.ARCHIVED, id="100_archived"),
        pytest.param(200, SupportLevel.COMMUNITY, id="200_community"),
        pytest.param(300, SupportLevel.CERTIFIED, id="300_certified"),
    ],
)
def test_support_level_from_precedence(precedence: int, expected: SupportLevel) -> None:
    """from_precedence returns the correct member for known values."""
    assert SupportLevel.from_precedence(precedence) is expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "bad_precedence",
    [
        pytest.param(0, id="zero"),
        pytest.param(150, id="between"),
        pytest.param(999, id="large"),
    ],
)
def test_support_level_from_precedence_errors(bad_precedence: int) -> None:
    """from_precedence raises ValueError for unknown precedence values."""
    with pytest.raises(ValueError, match="Unrecognized support-level precedence"):
        SupportLevel.from_precedence(bad_precedence)


# ---------------------------------------------------------------------------
# SupportLevel.parse - keywords and legacy integer strings
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "value,expected",
    [
        pytest.param("archived", SupportLevel.ARCHIVED, id="keyword_archived"),
        pytest.param("community", SupportLevel.COMMUNITY, id="keyword_community"),
        pytest.param("certified", SupportLevel.CERTIFIED, id="keyword_certified"),
        pytest.param("100", SupportLevel.ARCHIVED, id="int_100"),
        pytest.param("200", SupportLevel.COMMUNITY, id="int_200"),
        pytest.param("300", SupportLevel.CERTIFIED, id="int_300"),
    ],
)
def test_support_level_parse(value: str, expected: SupportLevel) -> None:
    """parse accepts both keyword and legacy integer string inputs."""
    assert SupportLevel.parse(value) is expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "bad_value",
    [
        pytest.param("gold", id="unknown_keyword"),
        pytest.param("999", id="unknown_int"),
        pytest.param("", id="empty"),
    ],
)
def test_support_level_parse_errors(bad_value: str) -> None:
    """parse raises ValueError for unrecognised values."""
    with pytest.raises(ValueError, match="Unrecognized support level"):
        SupportLevel.parse(bad_value)


# ---------------------------------------------------------------------------
# ConnectorType
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "value,expected",
    [
        pytest.param("source", ConnectorType.SOURCE, id="source"),
        pytest.param("destination", ConnectorType.DESTINATION, id="destination"),
    ],
)
def test_connector_type_parse(value: str, expected: ConnectorType) -> None:
    """ConnectorType.parse accepts valid type strings."""
    assert ConnectorType.parse(value) is expected


@pytest.mark.unit
def test_connector_type_parse_error() -> None:
    """ConnectorType.parse raises ValueError for invalid input."""
    with pytest.raises(ValueError, match="Unrecognized connector type"):
        ConnectorType.parse("transform")


# ---------------------------------------------------------------------------
# ConnectorLanguage
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "value,expected",
    [
        pytest.param("python", ConnectorLanguage.PYTHON, id="python"),
        pytest.param("java", ConnectorLanguage.JAVA, id="java"),
        pytest.param("low-code", ConnectorLanguage.LOW_CODE, id="low_code"),
        pytest.param(
            "manifest-only", ConnectorLanguage.MANIFEST_ONLY, id="manifest_only"
        ),
    ],
)
def test_connector_language_parse(value: str, expected: ConnectorLanguage) -> None:
    """ConnectorLanguage.parse accepts valid language strings."""
    assert ConnectorLanguage.parse(value) is expected


@pytest.mark.unit
def test_connector_language_parse_error() -> None:
    """ConnectorLanguage.parse raises ValueError for invalid input."""
    with pytest.raises(ValueError, match="Unrecognized language"):
        ConnectorLanguage.parse("rust")
