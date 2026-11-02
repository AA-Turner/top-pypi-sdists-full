"""Tests for _sanitize_mapping()."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import cast

import pytest

from agentic_devtools.cli.ci.reconciliation.metric_attributes import _sanitize_mapping


def test_stringifies_and_sorts_keys() -> None:
    attributes = cast(Mapping[str, object], {"z": 1, 2: "two", "a": 3})

    sanitized = _sanitize_mapping(attributes)

    assert list(sanitized.items()) == [("2", "two"), ("a", 3), ("z", 1)]


def test_returns_immutable_copy() -> None:
    attributes = {"pages": 2}

    sanitized = _sanitize_mapping(attributes)
    attributes["pages"] = 99

    assert isinstance(sanitized, MappingProxyType)
    assert sanitized["pages"] == 2
    with pytest.raises(TypeError):
        sanitized["pages"] = 3  # type: ignore[index]


def test_sanitizes_nested_mappings() -> None:
    sanitized = _sanitize_mapping({"nested": {"values": [1, 2]}})

    assert isinstance(sanitized["nested"], MappingProxyType)
    assert sanitized["nested"]["values"] == (1, 2)  # type: ignore[index]


def test_validates_attribution_event_schema() -> None:
    sanitized = _sanitize_mapping(
        {"pr_number": 42, "outcome": "unknown", "reason": "incomplete"},
        event_type="unknown_attribution",
    )

    assert dict(sanitized) == {
        "outcome": "unknown",
        "pr_number": 42,
        "reason": "incomplete",
    }
    with pytest.raises(ValueError, match="Unsupported"):
        _sanitize_mapping(
            {"outcome": "unknown", "token": "secret"},
            event_type="unknown_attribution",
        )
    with pytest.raises(ValueError, match="Missing"):
        _sanitize_mapping({}, event_type="provider_attribution_failure")
    with pytest.raises(ValueError, match="positive integer"):
        _sanitize_mapping(
            {"outcome": "unknown", "pr_number": -1},
            event_type="unknown_attribution",
        )
    with pytest.raises(ValueError, match="Unsupported"):
        _sanitize_mapping(
            {"outcome": ["unknown"]},
            event_type="unknown_attribution",
        )
    with pytest.raises(ValueError, match="Unsupported"):
        _sanitize_mapping(
            {"outcome": "unsupported"},
            event_type="unknown_attribution",
        )
    assert dict(
        _sanitize_mapping(
            {"outcome": "failed", "reason": "provider_error"},
            event_type="provider_attribution_failure",
        )
    ) == {"outcome": "failed", "reason": "provider_error"}
