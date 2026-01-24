from ogmios import ProtocolParameters
from tests.ogmios.test_fixtures import client


def test_QueryProtocolParameters(client):
    id_str = "My ID string"
    result, id = client.query_protocol_parameters.execute(id_str)

    assert isinstance(result, ProtocolParameters)
    assert id == id_str
