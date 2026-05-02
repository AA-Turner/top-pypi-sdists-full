import asyncio
import pytest
from pandas import DataFrame
from flowtask.tests import PandasTestCase



@pytest.fixture(autouse=True, scope='session')
def component():
    cp = 'UniqueRows'
    yield cp

pytestmark = pytest.mark.asyncio

class TestUniqueBasic(PandasTestCase):
    file_test = 'HR Employees.csv'
    arguments: dict = {
        "unique": ["Associate ID"]
      }
    expected_result_type = DataFrame

class TestUniqueKeep(PandasTestCase):
    file_test = 'HR Employees.csv'
    arguments: dict = {
        "comments": "Unique Ordering by Associate, keeping last record",
        "unique": ["Associate ID"],
        "order": {"Associate ID": "asc"},
        "keep": "last"
      }
    expected_result_type = DataFrame

def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
