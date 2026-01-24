from tests.ogmios.test_fixtures import client

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def test_QueryEpoch(client):
    id_str = "My ID string"
    epoch, id = client.query_epoch.execute(id_str)

    assert isinstance(epoch, int)
    assert id == id_str
