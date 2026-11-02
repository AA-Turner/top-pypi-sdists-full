"""Tests for unsupported file paths."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.file_classification import unsupported_paths
from agentic_devtools.orchestration.hierarchy.scopes import SpecializationCategory


def test_unsupported_paths_returns_binary_paths() -> None:
    by_category: dict[SpecializationCategory, tuple[str, ...]] = {
        SpecializationCategory.PYTHON: ("a.py",),
        SpecializationCategory.UNSUPPORTED_OR_BINARY: ("a.bin",),
    }

    assert unsupported_paths(by_category) == ("a.bin",)
