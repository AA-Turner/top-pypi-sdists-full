from pathlib import PosixPath
import asyncio
import pytest
from flowtask.tests import BaseTestCase


@pytest.fixture(autouse=True, scope='session')
def component():
    component = 'FileExists'
    yield component


pytestmark = pytest.mark.asyncio

class TestfileExists(BaseTestCase):
    arguments: dict = {
        "directory": "/home/ubuntu/symbits/walmart/files/stores",
        "filename": "Walmart Master Store List.xlsx"
        }
    expected_result = {
        PosixPath('/home/ubuntu/symbits/walmart/files/stores/Walmart Master Store List.xlsx'): True
    }


class TestFilePattern(BaseTestCase):
    arguments: dict = {
        "directory": "/home/ubuntu/symbits/epson/files/sales/",
        "comments": "Support pattern replacements",
        "file": {
            "pattern": "SELLTHRU_TROC_{date}_*.TXT",
            "date": "20200630"
        }
    }

def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
