from tests.ogmios.test_fixtures import client

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def test_QueryStartTime(client):
    id_str = "My ID string"
    stake_dist, id = client.query_live_stake_distribution.execute(id_str)

    assert isinstance(stake_dist, dict)
    assert id == id_str

    # Verify dict entries have the proper keys
    first_pool = list(stake_dist.keys())[0]
    assert stake_dist.get(first_pool).keys() == {"stake", "vrf"}
