import asyncio
import pytest
from flowtask.tests import BaseTestCase


@pytest.fixture(autouse=True, scope='session')
def component():
    component = 'DownloadFromSmartSheet'
    yield component


pytestmark = pytest.mark.asyncio

class TestSmartSheet(BaseTestCase):
    arguments: dict = {
        "file_id": "373896609326980",
        "file_format": "application/vnd.ms-excel",
        "destination": {
            "filename": "WORP MPL 2022.xlsx",
            "directory": "/home/ubuntu/symbits/worp/files/stores/test/"
        }
    }

def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
