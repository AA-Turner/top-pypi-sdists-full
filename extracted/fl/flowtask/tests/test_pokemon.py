from pandas import DataFrame
import pytest
from flowtask.tests import BaseTestCase #, PandasTestCase


@pytest.fixture(autouse=True, scope="session")
def component():
    component = "Pokemon"
    yield component


pytestmark = pytest.mark.asyncio


class TestPokemonReadMachines(BaseTestCase):
    arguments: dict = {
        "credentials": {
            "BASE_URL": "POKEMON_BASE_URL",
            "CLIENT_ID": "POKEMON_CLIENT_ID",
            "CLIENT_SECRET": "POKEMON_CLIENT_SECRET",
        },
        "type": "machines",
    }

    expected_result_type = DataFrame


class TestPokemonReadInventory(BaseTestCase):
    arguments: dict = {
        "credentials": {
            "BASE_URL": "POKEMON_BASE_URL",
            "CLIENT_ID": "POKEMON_CLIENT_ID",
            "CLIENT_SECRET": "POKEMON_CLIENT_SECRET",
        },
        "type": "inventory",
        "ids": [
            "Q00625",
            "Q00013",
            "Q00011",
            "Q00015",
            "Q00036",
        ],
    }

    expected_result_type = DataFrame

# TODO
# class TestPokemonReadInventoryFromPreviousDataIds(PandasTestCase):
#     pass
