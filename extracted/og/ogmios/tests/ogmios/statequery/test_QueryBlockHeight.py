from ogmios.datatypes import Origin

from tests.ogmios.test_fixtures import client

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def test_QueryBlockHeight_tip(client):
    # Get tip
    _, tip, _ = client.find_intersection.execute([Origin()])

    id_str = "My ID string"
    block_height, id = client.query_block_height.execute(id_str)

    assert isinstance(block_height, int)
    assert block_height == tip.height
    assert id == id_str
