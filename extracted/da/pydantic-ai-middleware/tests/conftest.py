"""Pytest configuration and fixtures."""

from __future__ import annotations

import pytest
from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel


@pytest.fixture
def test_model() -> TestModel:
    """Create a test model for testing."""
    return TestModel()


@pytest.fixture
def simple_agent(test_model: TestModel) -> Agent[None, str]:
    """Create a simple agent for testing."""
    return Agent(test_model, output_type=str)
