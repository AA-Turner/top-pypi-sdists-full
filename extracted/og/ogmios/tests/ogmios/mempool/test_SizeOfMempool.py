import pytest

from ogmios.errors import ResponseError
from tests.ogmios.test_fixtures import client

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def test_SizeOfMempool(client):
    id_str = "My ID string"
    with pytest.raises(ResponseError):
        # Try getting mempool size before acquiring a snapshot
        client.size_of_mempool.execute()

    # Acquire a mempool snapshot
    client.acquire_mempool.execute()
    max_capacity, current_size, num_transactions, id = client.size_of_mempool.execute(id_str)
    assert isinstance(max_capacity, int)
    assert isinstance(current_size, int)
    assert isinstance(num_transactions, int)
    assert max_capacity > 0
    assert id == id_str
    if current_size > 0:
        assert num_transactions > 0
    else:
        assert num_transactions == 0
