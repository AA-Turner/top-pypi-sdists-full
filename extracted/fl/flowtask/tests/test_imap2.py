import asyncio
import pytest
from flowtask.tests import BaseTestCase


@pytest.fixture(autouse=True, scope='session')
def component():
    cp = 'DownloadFromIMAP'
    yield cp

pytestmark = pytest.mark.asyncio


class TestDownloadWorked(BaseTestCase):
    """Query SQL from File
    """
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
            "SUBJECT": "Custom Punch with Pay Codes - Excel",
            "FROM": "eet_application@adp.com"
        },
        "overwrite": True,
        "attachments": {
            "directory": "/home/ubuntu/symbits/troc/files/worked_hours/"
        },
        "masks": {
            "{search_today}": ["today", {"mask": "%d-%b-%Y"}]
        }
    }
    expected_result_type = dict


def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
