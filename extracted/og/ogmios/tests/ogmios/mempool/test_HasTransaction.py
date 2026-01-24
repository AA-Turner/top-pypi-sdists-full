import pytest

from ogmios.errors import ResponseError
from tests.ogmios.test_fixtures import client

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def test_HasTransaction(client):
    id_str = "My ID string"
    tx_id = "90181c517248757d3a5beadc9c3fe64bf821d3e889a963fc717003ec248757d3"
    with pytest.raises(ResponseError):
        # Try getting mempool size before acquiring a snapshot
        client.has_transaction.execute(tx_id)

    # Acquire a mempool snapshot
    client.acquire_mempool.execute()
    has_tx, id = client.has_transaction.execute(tx_id, id_str)
    assert isinstance(has_tx, bool)
    assert not has_tx
    assert id == id_str
