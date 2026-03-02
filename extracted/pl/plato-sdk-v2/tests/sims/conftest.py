"""Shared fixtures for sim integration tests."""

import pytest

from plato.v2 import AsyncPlato


@pytest.fixture
async def plato_client():
    """Create AsyncPlato client."""
    client = AsyncPlato()
    yield client
    await client.close()
