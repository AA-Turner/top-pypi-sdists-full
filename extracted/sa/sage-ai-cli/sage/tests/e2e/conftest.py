import pytest


def pytest_collection_modifyitems(items):
    """Mark all e2e tests as integration (real cloud API calls)."""
    for item in items:
        item.add_marker(pytest.mark.integration)
        item.add_marker(pytest.mark.timeout(900))
