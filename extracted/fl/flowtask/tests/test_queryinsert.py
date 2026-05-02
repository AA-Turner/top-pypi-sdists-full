import asyncio
import pytest
from flowtask.tests import BaseTestCase


@pytest.fixture(autouse=True, scope='session')
def component():
    component = 'QueryToInsert'
    yield component


pytestmark = pytest.mark.asyncio

class TestQueryInsert(BaseTestCase):
    arguments: dict = {
        "schema": "troc",
        "tablename": "query_util",
        "action": "insert",
        "pk": [ "query_slug" ],
        "directory": "/home/ubuntu/symbits/",
        "filter": {}
    }


class TestQueryUpdate(BaseTestCase):
    arguments: dict = {
        "schema": "troc",
        "tablename": "query_util",
        "action": "update",
        "pk": [ "query_slug" ],
        "directory": "/home/ubuntu/symbits/",
        "filter": {}
    }


def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
