from pathlib import PosixPath
import asyncio
import pytest
from navconfig import BASE_DIR
from flowtask.tests import BaseTestCase


@pytest.fixture(autouse=True, scope='session')
def component():
    component = 'FileCopy'
    yield component


pytestmark = pytest.mark.asyncio

class TestFileCopy(BaseTestCase):
    arguments: dict = {
        "source": {
            "directory": str(BASE_DIR.joinpath('tests', 'sql')),
            "filename": 'get_stores.sql'
        },
        "destination" : {
            "directory": str(BASE_DIR.joinpath('tests', 'sql')),
            "filename": 'copy-{today}.sql',
            "rename": True
        },
        "masks": {
            "{today}": ["today", {"mask": "%Y%m%d"}]
        },
        "remove_source": False
      }
    expected_result_type = dict

class TestFileCopyRemove(BaseTestCase):
    arguments: dict = {
        "source": {
            "directory": str(BASE_DIR.joinpath('tests', 'sql')),
            "filename": 'copy-{today}.sql',
        },
        "destination" : {
            "directory": str(BASE_DIR.joinpath('tests', 'sql')),
            "filename": 'get_stores.sql',
            "rename": True
        },
        "masks": {
            "{today}": ["today", {"mask": "%Y%m%d"}]
        },
        "remove_source": True
      }
    expected_result_type = dict

def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
