import asyncio
import pytest
from pandas import DataFrame
from flowtask.tests import BaseTestCase


@pytest.fixture(autouse=True, scope='session')
def component():
    cp = 'RESTClient'
    yield cp

pytestmark = pytest.mark.asyncio


class TestBoseTickets(BaseTestCase):
    """
    """
    arguments: dict = {
        "url": "https://bose.tickets.trocdigital.io/api/v1/tickets/",
        "expected_credentials": {
            "apikey": "str"
        },
        "credentials": {
            "apikey": "ZAMMAD_BOSE_TOKEN"
        },
        "method": "get",
        "as_dataframe": "true"
    }
    expected_result_type = DataFrame

class TestBasicREST(BaseTestCase):
    arguments: dict = {
        "url": "https://gorest.co.in/public/v2/users",
        "method": "get",
        "as_dataframe": "true"
    }
    expected_result_type = DataFrame

def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
