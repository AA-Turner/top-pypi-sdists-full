import asyncio
from pandas import DataFrame
import pytest
from flowtask.tests import BaseTestCase


@pytest.fixture(autouse=True, scope="session")
def component():
    component = "DialPad"
    yield component


pytestmark = pytest.mark.asyncio


class TestDialPadStats(BaseTestCase):
    arguments: dict = {
        "credentials": {
            "APIKEY": "DIALPAD_APIKEY",
        },
        "type": "stats",
        "body_params": {
            "export_type": "records",
            "stat_type": "calls",
        },
    }

    expected_result_type = DataFrame


class TestDialPadWrongTypeException(BaseTestCase):
    arguments: dict = {
        "credentials": {
            "APIKEY": "DIALPAD_APIKEY",
        },
        "type": "test_type",
        "params": {},
    }

    expected_exception_msg = "DialPad: Wrong 'type' on task definition"


def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
