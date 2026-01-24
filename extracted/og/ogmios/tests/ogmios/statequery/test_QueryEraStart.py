from tests.ogmios.test_fixtures import client

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def test_QueryEraStart(client):
    id_str = "My ID string"
    time, slot, epoch, id = client.query_era_start.execute(id_str)

    assert isinstance(time, int)
    assert isinstance(slot, int)
    assert isinstance(epoch, int)
    assert id == id_str
