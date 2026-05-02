import pytest
from pandas import DataFrame
from flowtask.tests import PandasTestCase


@pytest.fixture(autouse=True, scope='session')
def component():
    cp = 'Populartimes'
    yield cp


pytestmark = pytest.mark.asyncio


class TestPopulartimes(PandasTestCase):
    file_test = 'populartimes.csv'
    arguments: dict = {
        "type": "by_placeid"
    }
    expected_result_type = DataFrame
