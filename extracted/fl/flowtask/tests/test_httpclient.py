import asyncio
import pytest
from pandas import DataFrame
from flowtask.tests import BaseTestCase


@pytest.fixture(autouse=True, scope='session')
def component():
    cp = 'HTTPClient'
    yield cp

pytestmark = pytest.mark.asyncio

class TestBasicHTTP(BaseTestCase):
    arguments: dict = {
        "comments": "Download HTML Information from a URL.",
        "url": "https://dummyjson.com/products/1",
        "method": "get",
        "as_dataframe": "true"
    }
    expected_result_type = DataFrame

class TestStringHTTP(BaseTestCase):
    arguments: dict = {
        "comments": "Download HTML Information from a URL.",
        "url": "https://datatables.net/examples/data_sources/dom",
        "method": "get",
        "as_dataframe": "false"
    }
    expected_result_type = str

def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
