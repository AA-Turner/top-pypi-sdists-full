from datetime import datetime

from tests.ogmios.test_fixtures import client

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def test_QueryStartTime(client):
    id_str = "My ID string"
    start_time, id = client.query_start_time.execute(id_str)

    assert isinstance(start_time, datetime)
    assert id == id_str
