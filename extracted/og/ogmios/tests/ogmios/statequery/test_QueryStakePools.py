from tests.ogmios.test_fixtures import client

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def test_QueryStakePools(client):
    id_str = "My ID string"
    stake_dist, _ = client.query_live_stake_distribution.execute()

    test_pools = list(stake_dist.keys())[:2]
    pool_summaries, id = client.query_stake_pools.execute(test_pools, id_str)

    assert isinstance(pool_summaries, dict)
    assert id == id_str

    summary = pool_summaries[test_pools[0]]
    for key in summary.keys():
        assert key in [
            'id',
            'vrfVerificationKeyHash',
            'pledge',
            'cost',
            'margin',
            'rewardAccount',
            'owners',
            'relays',
            'metadata',
        ]
