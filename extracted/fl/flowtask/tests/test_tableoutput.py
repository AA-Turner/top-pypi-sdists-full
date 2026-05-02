import asyncio
import pytest
from asyncdb import AsyncDB
from querysource.conf import default_dsn
from flowtask.tests import PandasTestCase


create_table = """
CREATE TABLE IF NOT EXISTS employees (
    associate_id INT,
    display_name VARCHAR(255),
    file_number INT,
    PRIMARY KEY (associate_id)
);
"""

drop_table = "DROP TABLE IF EXISTS employees;"


@pytest.fixture(scope='session', autouse=True)
def component():
    cp = 'TableOutput'
    yield cp


@pytest.fixture(scope='session')
def data_sample():
    # Sample data to convert to a pandas DataFrame
    return [
        {"associate_id": 1, "display_name": "John Smith", "file_number": 1001},
        {"associate_id": 2, "display_name": "Jane Doe", "file_number": 1002},
        {"associate_id": 3, "display_name": "William Shatner", "file_number": 1003},
    ]

pytestmark = pytest.mark.asyncio

class TestTableOuput(PandasTestCase):
    file_test = None
    renamed_cols: list = ['associate_id', 'display_name', 'file_number']

    async def startup_function(self):
        """
        Setup the table before running the test.
        """
        db = AsyncDB('pg', dsn=default_dsn)
        async with await db.connection() as conn:
            await conn.execute(create_table)
        return True

    async def ending_function(self):
        """
        Teardown the table after running the test.
        """
        db = AsyncDB('pg', dsn=default_dsn)
        async with await db.connection() as conn:
            await conn.execute(drop_table)
        return True

    async def test_run(self):
        await super().test_run()

    arguments: dict = {
        "dsn": default_dsn,
        "table": "employees",
        "schema": "public",
        "pk": ["associate_id"],
        "if_exists": "append"
    }

def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
