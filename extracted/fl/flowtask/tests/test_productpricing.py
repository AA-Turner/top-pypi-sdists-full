import pytest
from pandas import DataFrame
from flowtask.tests import PandasTestCase


@pytest.fixture(autouse=True, scope='session')
def component():
    cp = 'ProductPricing'
    yield cp


pytestmark = pytest.mark.asyncio


class TestProductPricing(PandasTestCase):
    file_test = 'productpricing.csv'
    arguments: dict = {
        "column": "model"
    }
    expected_result_type = DataFrame
