from tests.ogmios.test_fixtures import client

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def test_AcquireMempool(client):
    id_str = "My ID string"
    slot, id = client.acquire_mempool.execute(id_str)

    assert isinstance(slot, int)
    assert slot > 0
    assert id == id_str
