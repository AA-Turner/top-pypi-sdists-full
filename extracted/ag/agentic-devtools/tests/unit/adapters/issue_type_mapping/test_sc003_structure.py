"""Structural assertion: mapping functions use no inline provider-native literals (SC-003, FR-005).

Hierarchy routing tokens ('parent', 'epic-link') and neutral type identifiers
('subtask', 'epic') used in control flow are explicitly excluded from this
constraint per the task specification.
"""

from __future__ import annotations

import ast
import inspect
import textwrap
from collections.abc import Callable
from typing import Any

from agentic_devtools.adapters.issue_type_mapping import (
    map_issue_type_to_github_labels,
    map_issue_type_to_jira,
)

# Strings that are permitted in control flow — neutral type names and routing tokens
_PERMITTED_STRINGS = frozenset(
    {
        "subtask",
        "epic",
        "parent",
        "epic-link",
    }
)


def _extract_string_literals(func: Callable[..., Any]) -> set[str]:
    """Extract all string literal values from a function's AST."""
    source = textwrap.dedent(inspect.getsource(func))
    tree = ast.parse(source)
    literals: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            literals.add(node.value)
    return literals


class TestSc003Structure:
    def test_github_mapping_no_provider_native_literals(self) -> None:
        literals = _extract_string_literals(map_issue_type_to_github_labels)
        provider_strings = {"Epic", "Feature", "Subtask", "Task", "Bug"}
        unexpected = literals & provider_strings
        assert not unexpected, f"Found provider-native literals in GitHub mapping function: {unexpected}"

    def test_jira_mapping_no_provider_native_literals(self) -> None:
        literals = _extract_string_literals(map_issue_type_to_jira)
        provider_strings = {"Epic", "Feature", "Sub-task", "Task", "Bug", "Story"}
        unexpected = literals & provider_strings
        assert not unexpected, f"Found provider-native literals in Jira mapping function: {unexpected}"

    def test_mapping_functions_only_use_permitted_strings(self) -> None:
        for func in (map_issue_type_to_github_labels, map_issue_type_to_jira):
            literals = _extract_string_literals(func)
            # Filter out docstrings (multi-line strings with newlines)
            non_docstring = {s for s in literals if "\n" not in s}
            non_permitted = {s for s in non_docstring if s not in _PERMITTED_STRINGS}
            # Only flag strings that could be provider-native labels/types
            # (title-cased or containing hyphens that look like Jira types)
            suspect = {s for s in non_permitted if (s[0:1].isupper() and len(s) > 1) or s in {"bug", "feature", "task"}}
            assert not suspect, f"Suspect provider-native literals in {func.__name__}: {suspect}"
