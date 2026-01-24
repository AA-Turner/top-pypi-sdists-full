import pytest
import json

from ogmios.errors import InvalidMethodError, InvalidResponseError, ResponseError
from ogmios.datatypes import Origin, Point, GenesisConfiguration, Era

from tests.ogmios.test_fixtures import client, era

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def test_QueryGenesisConfiguration_byron(client):
    id_str = "My ID string"
    genesis_configuration, id = client.query_genesis_configuration.execute(Era.byron.value, id_str)

    assert isinstance(genesis_configuration, GenesisConfiguration)
    assert id == id_str


def test_QueryGenesisConfiguration_shelley(client, era):
    if Era.get_index(era) < Era.get_index(Era.shelley):
        pytest.skip("Test only valid for shelley era")

    id_str = "My ID string"
    genesis_configuration, id = client.query_genesis_configuration.execute(
        Era.shelley.value, id_str
    )

    assert isinstance(genesis_configuration, GenesisConfiguration)
    assert id == id_str


def test_QueryGenesisConfiguration_alonzo(client, era):
    if Era.get_index(era) < Era.get_index(Era.alonzo):
        pytest.skip("Test only valid for alonzo era")

    id_str = "My ID string"
    genesis_configuration, id = client.query_genesis_configuration.execute(Era.alonzo.value, id_str)

    assert isinstance(genesis_configuration, GenesisConfiguration)
    assert id == id_str


def test_QueryGenesisConfiguration_conway(client, era):
    if Era.get_index(era) < Era.get_index(Era.conway):
        pytest.skip("Test only valid for conway era")

    id_str = "My ID string"
    genesis_configuration, id = client.query_genesis_configuration.execute(Era.conway.value, id_str)

    assert isinstance(genesis_configuration, GenesisConfiguration)
    assert id == id_str
