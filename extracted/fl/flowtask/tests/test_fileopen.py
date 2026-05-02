import asyncio
import pytest
from flowtask.tests import BaseTestCase
import io


@pytest.fixture(autouse=True, scope='session')
def component():
    component = 'FileOpen'
    yield component

def get_file():
    with open('/home/ubuntu/symbits/walmart/files/stores.csv', 'r') as fp:
        content = fp.read()
        stream = io.StringIO(content)
        stream.seek(0)
    return stream

pytestmark = pytest.mark.asyncio

class TestFileOpen(BaseTestCase):
    arguments: dict = {
        "directory": "/home/ubuntu/symbits/walmart/files",
        "file": {
            "pattern": "stores.csv",
            "today": ["current_date", {"mask": "%Y%m%d"}]
        }
    }
    # expected_result = {
    #     'stores.csv': get_file()
    # }



def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
