"""GitHub adapter provider-specific fixture stub.

Composes with shared parent fixtures from ``tests/unit/adapters/conftest.py``.
Add GitHub-specific mocks and test data here as needed.
"""

from __future__ import annotations

import pytest

from tests.unit.adapters.mock_adapter import MockAdapter


@pytest.fixture()
def github_mock_adapter() -> MockAdapter:
    """Return a MockAdapter configured with GitHub-style defaults."""
    return MockAdapter(
        issue_types=[
            {"name": "bug", "description": "Something isn't working"},
            {"name": "feature", "description": "New feature or request"},
        ],
    )
