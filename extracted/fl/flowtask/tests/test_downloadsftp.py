import asyncio
import pytest
from flowtask.tests import BaseTestCase


@pytest.fixture(autouse=True, scope='session')
def component():
    cp = 'DownloadFromSFTP'
    yield cp

pytestmark = pytest.mark.asyncio


class TestHourly(BaseTestCase):
    """Test Hourly Postpaid
    """
    arguments: dict = {
        "file": {
            "pattern": "WARPRG_WARPTRO_US/TROC Hourly Cumulative FTP Feed_{value}*.xlsx",
            "value": [
                "today",
                {
                    "mask": "%Y%m%d%H",
                    "tz": "America/New_York"
                }
            ]
        },
        "client_keys": "/home/jesuslara/.ssh/jesuslara.pem",
        "host": "WALMART_TRO_SFTP_HOST",
        "port": "WALMART_TRO_SFTP_PORT",
        "credentials": {
            "username": "WALMART_TRO_SFTP_USERNAME",
            "password": "WALMART_TRO_SFTP_PASSWORD",
            "known_hosts": None
        },
        "directory": "/home/ubuntu/symbits/walmart/files/hourly_postpaid/"
    }
    expected_result_type = list

class TestDownloadOther(BaseTestCase):
    arguments: dict = {
        "file": {
            "pattern": "incoming/SalesDevice_{salesDate}.csv",
            "salesDate": [
                "today",
                {
                    "mask": "%Y%m%d"
                }
            ]
        },
        "host": "52.21.11.35",
        "port": 22,
        "credentials": {
            "username": "ltm-user",
            "password": "n-*ALsHDcxEes7Kj7Gi43H!DMtyoXE",
            "known_hosts": None
        },
        "directory": "/home/ubuntu/symbits/xfinity/files/ltm/acc_sales/",
        "overwrite": False,
        "rename": "{today}_acc_sales_devices.csv",
        "masks": {
            "{today}": ["today", {
                "mask": "%Y%m%d"
            }]
        }
    }
    expected_result_type = list

def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
