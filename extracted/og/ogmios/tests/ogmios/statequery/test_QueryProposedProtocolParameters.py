import pytest
from typing import Union

from ogmios import ProtocolParameters
from tests.ogmios.test_fixtures import client


@pytest.mark.skip
def test_QueryProposedProtocolParameters(client):
    id_str = "My ID string"
    result, id = client.query_proposed_protocol_parameters.execute(id_str)

    assert isinstance(result, Union[ProtocolParameters, None])
    assert id == id_str
