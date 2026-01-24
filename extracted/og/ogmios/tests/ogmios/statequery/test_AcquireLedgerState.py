import pytest

from ogmios.errors import ResponseError
from ogmios.datatypes import Origin, Point

from tests.ogmios.test_fixtures import client

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def test_AcquireLedgerState_tip(client):
    # Get tip
    _, tip, _ = client.find_intersection.execute([Origin()])

    id_str = "My ID string"
    point, id = client.acquire_ledger_state.execute(tip.to_point(), id_str)

    assert isinstance(point, Point)
    assert tip.to_point() == point
    assert id == id_str


def test_AcquireLedgerState_origin(client):
    # Get tip
    point, _, _ = client.find_intersection.execute([Origin()])

    # Origin is too old to acquire ledger state
    with pytest.raises(ResponseError):
        _, _ = client.acquire_ledger_state.execute(point)
