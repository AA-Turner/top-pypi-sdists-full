from tests.ogmios.test_fixtures import client


def test_QueryLedgerTip(client):
    id_str = "My ID string"
    result, id = client.query_rewards_provenance.execute(id_str)

    assert isinstance(result, dict)
    expected_keys = [
        'desiredNumberOfStakePools',
        'stakePoolPledgeInfluence',
        'totalRewardsInEpoch',
        'activeStakeInEpoch',
        'stakePools',
    ]
    for key in expected_keys:
        assert key in result.keys()
    assert id == id_str
