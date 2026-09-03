"""Tests for supported file-classification categories."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.file_classification import supported_categories
from agentic_devtools.orchestration.hierarchy.scopes import SpecializationCategory


def test_supported_categories_excludes_unsupported_paths() -> None:
    by_category: dict[SpecializationCategory, tuple[str, ...]] = {
        SpecializationCategory.PYTHON: ("a.py",),
        SpecializationCategory.UNSUPPORTED_OR_BINARY: ("a.bin",),
    }

    assert supported_categories(by_category) == {SpecializationCategory.PYTHON: ("a.py",)}
