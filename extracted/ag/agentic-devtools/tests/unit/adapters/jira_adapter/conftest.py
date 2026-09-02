"""Jira adapter provider-specific fixture stub.

Composes with shared parent fixtures from ``tests/unit/adapters/conftest.py``.
Add Jira-specific mocks and test data here as needed.
"""

from __future__ import annotations

import pytest

from tests.unit.adapters.mock_adapter import MockAdapter


@pytest.fixture()
def jira_mock_adapter() -> MockAdapter:
    """Return a MockAdapter configured with Jira-style defaults."""
    return MockAdapter(
        issue_types=[
            {"name": "Bug", "description": "A problem which impairs a function"},
            {"name": "Story", "description": "A user story"},
            {"name": "Task", "description": "A task that needs to be done"},
            {"name": "Epic", "description": "A large body of work"},
        ],
        type_properties={
            "Bug": [{"name": "summary", "type": "string", "required": True, "allowed_values": None}],
            "Story": [{"name": "summary", "type": "string", "required": True, "allowed_values": None}],
            "Task": [{"name": "summary", "type": "string", "required": True, "allowed_values": None}],
            "Epic": [{"name": "summary", "type": "string", "required": True, "allowed_values": None}],
        },
    )
