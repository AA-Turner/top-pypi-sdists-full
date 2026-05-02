import asyncio
import pytest
from flowtask.tests import BaseTestCase


@pytest.fixture(autouse=True, scope='session')
def component():
    component = 'DownloadFromIMAP'
    yield component


pytestmark = pytest.mark.asyncio

class TestIMAP(BaseTestCase):
    arguments: dict = {
        "credentials": {
            "host": "email_host",
            "port": "email_port",
            "user": "email_host_user",
            "password": "email_host_password",
            "use_ssl": True
        },
        "search_terms": {
            "SINCE": "{search_monday}",
            "SUBJECT": "TROC Daily Inventory Trend Report"
        },
        "attachments": {
            "directory": "/home/ubuntu/symbits/walmart/files/daily_inventory/test/"
        },
        "masks": {
            "{search_monday}": ["date_dow", {"day_of_week": "monday", "mask": "%d-%b-%Y"}]
        },
        "overwrite": True
    }

class TestIMAPOnSubject(BaseTestCase):
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
            "directory": "/home/ubuntu/symbits/bose/files/worked_hours/test/"
        },
        "masks": {
            "{search_today}": ["today", {"mask": "%d-%b-%Y"}]
        },
        "overwrite": True
      }

def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
