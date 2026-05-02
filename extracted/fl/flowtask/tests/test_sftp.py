import asyncio
import pytest
from flowtask.tests import BaseTestCase


@pytest.fixture(autouse=True, scope='session')
def component():
    component = 'DownloadFromSFTP'
    yield component


pytestmark = pytest.mark.asyncio

class TestSFTP(BaseTestCase):
    arguments: dict = {
        "file": {
            "pattern": "TRO Daily Feed_{value}*.txt",
            "value": ["today", {"mask": "%Y%m%d"}]
        },
        "host": "WALMART_TRO_SFTP_HOST",
        "port": "WALMART_TRO_SFTP_PORT",
        "credentials": {
            "username": "WALMART_TRO_SFTP_USERNAME",
            "password": "WALMART_TRO_SFTP_PASSWORD",
            "known_hosts": None
        },
        "directory": "/home/ubuntu/symbits/walmart/files/download/postpaid/test/"
    }

class TestSFTPByDate(BaseTestCase):
    arguments: dict = {
        "file": {
            "pattern": "Performance_Tracker/*",
            "mdate": "{yesterday}"
        },
        "host": "altice_ltm_sftp_host",
        "port": "altice_ltm_sftp_port",
        "credentials": {
            "username": "altice_ltm_sftp_username",
            "password": "altice_ltm_sftp_password",
            "known_hosts": None
        },
        "directory": "/home/ubuntu/altice/files/test/",
        "overwrite": True,
        "masks": {
            "{yesterday}": ["yesterday", {"mask": "%Y-%m-%d"}]
        }
    }

def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
