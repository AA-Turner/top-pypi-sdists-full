import asyncio
import pytest
from flowtask.tests import BaseTestCase


@pytest.fixture(autouse=True, scope='session')
def component():
    component = 'DownloadFromFTP'
    yield component

pytestmark = pytest.mark.asyncio

class TestBaseFTP(BaseTestCase):
    arguments: dict = {
        "host": "trendmicro_host",
        "port": "trendmicro_port",
        "use_tls": True,
        "credentials": {
            "user": "trendmicro_user",
            "password": "trendmicro_password"
        },
        "source": {
            "filename": "20221128051005-FtpCombinedMarketShareReport.2022-11-26.csv",
            "directory": "/Market Share S2 and TTS/"
        },
        "destination": {
            "directory": "/home/ubuntu/symbits/trendmicro/files/market_share/test/"
        }
    }

class TestFTPPattern(BaseTestCase):
    arguments: dict = {
        "host": "trendmicro_host",
        "port": "trendmicro_port",
        "use_tls": True,
        "file": {
            "pattern": "{monday}.*-Limited852StoreReport.{saturday}.csv",
            "values": {
                "monday": ["date_dow", {
                    "day_of_week": "monday",
                    "mask": "%Y%m%d"
                }],
                "saturday": ["date_diff_dow", {
                    "diff": 2,
                    "day_of_week": "monday",
                    "mask": "%Y-%m-%d"
                }]
            },
            "directory": "/Limited852Report"
        },
        "credentials": {
            "user": "trendmicro_user",
            "password": "trendmicro_password"
        },
        "download": {
            "directory": "/home/ubuntu/symbits/trendmicro/files/market_share/test/"
        }
    }

def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
