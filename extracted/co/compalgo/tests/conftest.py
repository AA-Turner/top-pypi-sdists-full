"""
Pytest configuration and shared fixtures for CompALGO test suite
"""
import pytest


def pytest_configure(config):
    """Register custom pytest markers"""
    config.addinivalue_line(
        "markers", "unit: Unit tests (no external dependencies)"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests (may require external resources)"
    )
    config.addinivalue_line(
        "markers", "network: Tests that require network access to Algorand nodes"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take significant time to run"
    )


def pytest_collection_modifyitems(config, items):
    """
    Automatically mark tests based on their names and location
    """
    for item in items:
        # Mark network tests
        if "network" in item.nodeid or "anchor" in item.nodeid or "verify" in item.nodeid:
            if "test_e2e" in item.nodeid or "test_verify" in item.nodeid:
                item.add_marker(pytest.mark.network)
        
        # Mark slow tests
        if "slow" in item.nodeid or "e2e" in item.nodeid or "concurrent" in item.nodeid:
            item.add_marker(pytest.mark.slow)
        
        # Mark integration tests
        if "e2e" in item.nodeid or "full_flow" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        
        # Mark unit tests
        if "verdict" in item.nodeid or "parser" in item.nodeid:
            if "e2e" not in item.nodeid:
                item.add_marker(pytest.mark.unit)
