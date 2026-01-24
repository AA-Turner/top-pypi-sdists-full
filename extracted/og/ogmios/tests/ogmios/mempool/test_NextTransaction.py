import pytest

from ogmios.errors import ResponseError
from tests.ogmios.test_fixtures import client

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def test_NextTransaction(client):
    id_str = "My ID string"
    with pytest.raises(ResponseError):
        # Try getting mempool size before acquiring a snapshot
        client.next_transaction.execute()

    # Acquire a mempool snapshot
    client.acquire_mempool.execute()
    _, id = client.next_transaction.execute(id_str)
    assert id == id_str
