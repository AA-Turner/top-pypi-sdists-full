from tests.ogmios.test_fixtures import client
from ogmios.datatypes import Ada


def test_QueryTreasuryAndReserves(client):
    id_str = "My ID string"
    treasury, reserves, id = client.query_treasury_and_reserves.execute(id_str)
    assert isinstance(treasury, Ada)
    assert isinstance(reserves, Ada)
    assert id == id_str
