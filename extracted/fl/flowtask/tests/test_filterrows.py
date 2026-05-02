import asyncio
import pytest
from pandas import DataFrame
from flowtask.tests import PandasTestCase



@pytest.fixture(autouse=True, scope='session')
def component():
    cp = 'FilterRows'
    yield cp

pytestmark = pytest.mark.asyncio

class TestFilterBasic(PandasTestCase):
    file_test = 'HR Employees.csv'
    arguments: dict = {
        "clean_dates": True,
        "drop_empty": True,
        "clean_numbers": True
    }
    expected_result_type = DataFrame

class TestFilterConditions(PandasTestCase):
    file_test = 'HR Employees.csv'
    arguments: dict = {
        "filter_conditions": {
            "drop_columns": {
                "columns": ["Payroll Company Code", "Payroll Name", "Reports To Name", "Location Description"]
            }
        }
      }
    expected_result_type = DataFrame

def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
