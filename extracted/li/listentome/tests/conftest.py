from __future__ import annotations

import pytest

from tests.fake_backend import FakeBackend


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def backend() -> FakeBackend:
    return FakeBackend()
