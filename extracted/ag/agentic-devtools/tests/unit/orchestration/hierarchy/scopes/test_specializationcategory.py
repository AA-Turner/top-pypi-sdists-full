"""Unit tests for canonical capability provisioning (FR-016)."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.hierarchy.scopes import (
    AgentScopeLevel,
    SpecializationCategory,
    required_capabilities,
)


@pytest.mark.parametrize(
    ("category", "expected"),
    [
        (SpecializationCategory.PYTHON, ("python_language",)),
        (SpecializationCategory.MARKDOWN, ("markdown_authoring",)),
        (SpecializationCategory.YAML, ("yaml_authoring",)),
        (SpecializationCategory.TYPESCRIPT, ("typescript_language",)),
    ],
)
def test_specialization_capabilities(category: SpecializationCategory, expected: tuple[str, ...]) -> None:
    caps = required_capabilities(AgentScopeLevel.SUBTASK, category)
    for cap in expected:
        assert cap in caps
