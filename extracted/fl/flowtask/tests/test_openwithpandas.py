import asyncio
import pytest
import pandas as pd
from flowtask.tests import BaseTestCase


@pytest.fixture(autouse=True, scope='session')
def component():
    component = 'OpenWithPandas'
    yield component


pytestmark = pytest.mark.asyncio


class TestOpenWithPandas(BaseTestCase):
    arguments: dict = {
        "directory": "/home/ubuntu/symbits/att/files/agent_staffing/",
        "filename": "AgentStaffingData_12082020.csv",
        "mime": "text/csv",
        "process": True,
        "trim": True,
        "map": {
            "tablename": "agent_staffing_raw",
            "schema": "att",
            "replace": True
        }
    }
    expected_result_type = pd.DataFrame


class TestOpenExcel(BaseTestCase):
    arguments: dict = {
        "directory": "/home/ubuntu/symbits/harman/files/stores",
        "filename": "Store List.xlsx",
        "mime": "application/vnd.ms-excel",
        "map": {
            "tablename": "stores_details_raw",
            "schema": "harman",
            "replace": True
        }
    }

class TestOpenExcelMultiple(BaseTestCase):
    arguments: dict = {
        "directory": "/home/ubuntu/symbits/harman/files/stores",
        "filename": ["Store List.xlsx", "Store List.xlsx"],
        "mime": "application/vnd.ms-excel",
        "map": {
            "tablename": "stores_details_raw",
            "schema": "harman",
            "replace": True
        }
    }

def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
