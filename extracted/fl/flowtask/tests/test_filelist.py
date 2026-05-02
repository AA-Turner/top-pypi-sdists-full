import asyncio
import pytest
from navconfig import BASE_DIR
from flowtask.conf import TASK_PATH
from flowtask.tests import BaseTestCase


@pytest.fixture(autouse=True, scope='session')
def component():
    component = 'FileList'
    yield component


pytestmark = pytest.mark.asyncio

class TestFileList(BaseTestCase):
    arguments: dict = {
        "file": {
            "pattern": "*.sql",
            "value": ""
        },
        "directory": str(TASK_PATH.joinpath('test', 'sql')),
        "iterate": False
    }
    expected_result_type = list


def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
