import asyncio
import pytest
from flowtask.tests import BaseTestCase


@pytest.fixture(autouse=True, scope='session')
def component():
    component = 'PrintMessage'
    yield component

pytestmark = pytest.mark.asyncio

class TestDummy(BaseTestCase):
    arguments: dict = {
        "message": "End Task: {first}",
        "level": "WARN",
        "first": "This Brand new Task",
    }
    expected_result: str = 'End Task: This Brand new Task'

def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
