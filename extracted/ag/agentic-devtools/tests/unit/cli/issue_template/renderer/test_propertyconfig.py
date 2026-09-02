"""Tests for the PropertyConfig dataclass (property-section mapping snapshot)."""

from __future__ import annotations

from types import MappingProxyType

import pytest

from agentic_devtools.cli.issue_template.renderer import PropertyConfig


class TestPropertyConfig:
    """Observable-guarantee tests for PropertyConfig (FR-004)."""

    def test_defaults_empty(self) -> None:
        """A default config has empty exclusions and empty mapping."""
        config = PropertyConfig()
        assert config.excluded_fields == frozenset()
        assert dict(config.mapping) == {}

    def test_excluded_fields_coerced_to_frozenset(self) -> None:
        """excluded_fields is normalized to a frozenset."""
        config = PropertyConfig(excluded_fields=frozenset({"url"}))
        assert config.excluded_fields == frozenset({"url"})

    def test_mapping_view_is_read_only(self) -> None:
        """The mapping view is a read-only MappingProxyType."""
        config = PropertyConfig(property_section_mapping={"url": "omit"})
        view = config.mapping
        assert isinstance(view, MappingProxyType)
        with pytest.raises(TypeError):
            view["url"] = "frontmatter"  # type: ignore[index]

    def test_hashable(self) -> None:
        """A config with a mapping remains hashable (no regression)."""
        config = PropertyConfig(property_section_mapping={"url": "omit"})
        assert isinstance(hash(config), int)

    def test_value_equality_order_independent(self) -> None:
        """Two configs from equal key/value pairs compare and hash equal regardless of order."""
        a = PropertyConfig(property_section_mapping={"b": "omit", "a": "frontmatter"})
        b = PropertyConfig(property_section_mapping={"a": "frontmatter", "b": "omit"})
        assert a == b
        assert hash(a) == hash(b)

    def test_inequality_on_different_mapping(self) -> None:
        """Different mappings produce unequal configs."""
        a = PropertyConfig(property_section_mapping={"url": "omit"})
        b = PropertyConfig(property_section_mapping={"url": "frontmatter"})
        assert a != b

    def test_caller_mutation_isolation(self) -> None:
        """Mutating the caller's input dict does not alter the stored snapshot."""
        source = {"url": "frontmatter"}
        config = PropertyConfig(property_section_mapping=source)
        source["url"] = "omit"
        source["created_at"] = "omit"
        assert dict(config.mapping) == {"url": "frontmatter"}

    def test_none_mapping_is_empty(self) -> None:
        """An explicit None mapping yields an empty view."""
        config = PropertyConfig(property_section_mapping=None)
        assert dict(config.mapping) == {}

    def test_non_string_mapping_key_rejected(self) -> None:
        """Non-string mapping keys are rejected instead of being string-coerced."""
        with pytest.raises(TypeError, match="property_section_mapping keys must be strings"):
            PropertyConfig(property_section_mapping={1: "omit"})  # type: ignore[dict-item]

    def test_non_string_mapping_value_rejected(self) -> None:
        """Non-string mapping values are rejected instead of being string-coerced."""
        with pytest.raises(TypeError, match='mapping target for "url" must be a string'):
            PropertyConfig(property_section_mapping={"url": None})  # type: ignore[dict-item]
