from ogmios.datatypes import Origin, Point

from tests.ogmios.test_fixtures import client

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def test_QueryLedgerTip(client):
    # Get tip
    _, tip, _ = client.find_intersection.execute([Origin()])

    id_str = "My ID string"
    queried_tip, id = client.query_ledger_tip.execute(id_str)

    assert isinstance(queried_tip, Point)
    assert queried_tip == tip.to_point()
    assert id == id_str
