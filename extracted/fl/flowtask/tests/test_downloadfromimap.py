import asyncio
import pytest
from flowtask.tests import BaseTestCase


@pytest.fixture(autouse=True, scope='session')
def component():
    cp = 'DownloadFromIMAP'
    yield cp

pytestmark = pytest.mark.asyncio


class TestDownloadWSP(BaseTestCase):
    arguments: dict = {
        "credentials": {
            "host": "email_host",
            "port": "email_port",
            "user": "email_host_user",
            "password": "email_host_password",
            "use_ssl": True
        },
        "search_terms": {
            "ON": "{search_today}",
            "SUBJECT": "TRO Daily POS Feed"
        },
        "attachments": {
            "rename": "TRODAILYPOSFEED.TROCAuto {today}.xlsx",
            "directory": "/home/ubuntu/symbits/walmart/files/wsp/"
        },
        "masks": {
            "{search_today}": ["today", {"mask": "%d-%b-%Y"}],
            "{today}": ["today", {"mask": "%Y-%m-%d"}]
        }
    }
    expected_result_type = dict


def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
