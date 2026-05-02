import asyncio
import pytest
from flowtask.conf import TASK_PATH
from flowtask.tests import BaseTestCase


@pytest.fixture(autouse=True, scope='session')
def component():
    component = 'ExecuteSQL'
    yield component

pytestmark = pytest.mark.asyncio

class TestExecuteSQL(BaseTestCase):
    arguments: dict = {
        "sql": "CREATE SCHEMA pytest; CREATE TABLE pytest.test (id INTEGER); INSERT INTO pytest.test (id) VALUES (1),(2); DROP SCHEMA IF EXISTS pytest CASCADE;"
    }
    expected_result_type = list

class TestExecuteSQLFile(BaseTestCase):
    arguments: dict = {
        "file_sql": str(TASK_PATH.joinpath('test', 'sql', 'get_stores.sql'))

    }
    expected_result_type = list

def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
