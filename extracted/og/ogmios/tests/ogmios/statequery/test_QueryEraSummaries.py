from datetime import datetime

from ogmios.datatypes import EraSummary
from tests.ogmios.test_fixtures import client

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def test_QueryEraSummaries(client):
    id_str = "My ID string"
    era_summaries, id = client.query_era_summaries.execute(id_str)

    for summary in era_summaries:
        assert isinstance(summary, EraSummary)
    assert id == id_str
