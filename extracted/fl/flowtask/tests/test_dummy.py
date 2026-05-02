import asyncio
import pytest
from flowtask.tests import BaseTestCase


@pytest.fixture(autouse=True, scope='session')
def component():
    cp = 'Dummy'
    yield cp

pytestmark = pytest.mark.asyncio

class TestDummy(BaseTestCase):
    arguments: dict = {
        "message": "Hello World"
    }
    expected_result: bool = True

def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
