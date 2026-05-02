import asyncio
import pytest
from pandas import DataFrame
from flowtask.tests import BaseTestCase


@pytest.fixture(autouse=True, scope='session')
def component():
    cp = 'RESTClient'
    yield cp

pytestmark = pytest.mark.asyncio

class TestBasicREST(BaseTestCase):
    arguments: dict = {
        "url": "https://gorest.co.in/public/v2/users",
        "method": "get",
        "as_dataframe": True
    }
    expected_result_type = DataFrame

class TestENVVARS(BaseTestCase):
    arguments: dict = {
        "url": "https://api.upcdatabase.org/product/{barcode}",
        "barcode": "0111222333446",
        "credentials": {
            "apikey": "UPC_API_KEY",
        },
        "as_dataframe": True
    }
    expected_result_type = DataFrame

class TestAsList(BaseTestCase):
    arguments: dict = {
        "url": "https://gorest.co.in/public/v2/users",
        "method": "get",
        "as_dataframe": False
    }
    expected_result_type = str

def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
