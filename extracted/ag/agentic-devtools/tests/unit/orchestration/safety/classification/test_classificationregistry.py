"""Tests for ClassificationRegistry.get() — unknown tool rejection."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.safety.classification import (
    ActionClassification,
    ClassificationEntry,
    ClassificationRegistry,
)
from agentic_devtools.orchestration.safety.exceptions import UnclassifiedToolError


class TestClassificationRegistryGet:
    """Tests for ClassificationRegistry.get()."""

    def test_get_registered_tool_returns_entry(self) -> None:
        registry = ClassificationRegistry()
        entry = ClassificationEntry("my_tool", ActionClassification.read_only)
        registry.register(entry)
        assert registry.get("my_tool") is entry

    def test_get_unregistered_tool_raises(self) -> None:
        registry = ClassificationRegistry()
        with pytest.raises(UnclassifiedToolError, match="unknown_tool"):
            registry.get("unknown_tool")

    def test_unclassified_error_has_tool_name(self) -> None:
        registry = ClassificationRegistry()
        with pytest.raises(UnclassifiedToolError) as exc_info:
            registry.get("some_tool")
        assert exc_info.value.tool_name == "some_tool"

    def test_has_returns_true_for_registered(self) -> None:
        registry = ClassificationRegistry()
        entry = ClassificationEntry("x", ActionClassification.local_mutation)
        registry.register(entry)
        assert registry.has("x") is True

    def test_has_returns_false_for_unregistered(self) -> None:
        registry = ClassificationRegistry()
        assert registry.has("nonexistent") is False

    def test_tool_names_returns_frozenset(self) -> None:
        registry = ClassificationRegistry()
        registry.register(ClassificationEntry("a", ActionClassification.read_only))
        registry.register(ClassificationEntry("b", ActionClassification.destructive))
        assert registry.tool_names == frozenset({"a", "b"})

    def test_classification_entry_is_frozen(self) -> None:
        entry = ClassificationEntry("t", ActionClassification.read_only)
        with pytest.raises(AttributeError):
            entry.tool_name = "changed"  # type: ignore[misc]

    def test_nondeterministic_fields_default_empty(self) -> None:
        entry = ClassificationEntry("t", ActionClassification.read_only)
        assert entry.nondeterministic_fields == ()

    def test_nondeterministic_fields_custom(self) -> None:
        entry = ClassificationEntry("t", ActionClassification.external_mutation, ("a.b", "c"))
        assert entry.nondeterministic_fields == ("a.b", "c")
