import asyncio
import pytest
from flowtask.tests import BaseTestCase


@pytest.fixture(autouse=True, scope='session')
def component():
    component = 'DownloadFromSharepoint'
    yield component

pytestmark = pytest.mark.asyncio

class TestSharepoint(BaseTestCase):
    arguments: dict = {
        "credentials": {
            "username": "email_host_user",
            "password": "email_host_password",
            "tenant": "symbits",
            "site": "trocstorage"
        },
        "file": {
            "filename": "Cricket%20MSL%20as%20of%203.11.2021v3.xlsx",
            "directory": "troc/Cricket/Master Store List/"
        },
        "destination": {
            "directory": "/home/ubuntu/symbits/cricket/files/stores/",
            "filename": "Cricket MSL as of 3.11.2021v3.xlsx"
        }
    }

class TestSharepointMasks(BaseTestCase):
    arguments: dict = {
        "credentials": {
            "username": "email_host_user",
            "password": "email_host_password",
            "tenant": "symbits",
            "site": "MT_BusinessDevelopment"
        },
        "file": {
            "filename": "Lowes WE{friday}.xlsx",
            "directory": "Client Data Repository/HISENSE/Lowes/Lowes Sales Data/"
        },
        "destination": {
            "directory": "/home/ubuntu/symbits/hisense/lowes_inventory/",
            "filename": "Lowes WE{friday}.xlsx"
        },
        "masks": {
            "{friday}": ["date_diff_dow", {
                "diff": 7,
                "day_of_week": "friday",
                "mask": "%-m.%d.%y"
            }]
        }
    }

def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
