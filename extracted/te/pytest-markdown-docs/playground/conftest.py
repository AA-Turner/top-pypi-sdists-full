import time

import pytest
import pytest_asyncio
import asyncio


@pytest_asyncio.fixture()
async def async_fix():
    await asyncio.sleep(1)
    yield "ahello"


@pytest.fixture()
def non_async_fix():
    time.sleep(1)
    yield "hello"
