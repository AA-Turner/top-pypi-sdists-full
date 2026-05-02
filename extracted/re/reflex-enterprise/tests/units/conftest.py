"""Pytest configuration for the enterprise app."""

import pytest

from reflex_enterprise.app import AppEnterprise


@pytest.fixture
def app() -> AppEnterprise:
    """App fixture."""
    return AppEnterprise()
