from datetime import datetime

from tests.ogmios.test_fixtures import client

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def test_QueryRewardAccountSummaries_key_empty(client):
    # This test relies on this address having a balance on the testnet
    stake_key = "stake_test1urlvxquq2pm8teqed7ek4sgjuc0zrx07z9czmy5fvwey92cq8c5dh"
    id_str = "My ID string"
    result, id = client.query_reward_account_summaries.execute(keys=[stake_key], id=id_str)

    assert result == {}
    assert id == id_str


def test_QueryRewardAccountSummaries_key(client):
    # This test relies on this address having a balance on the testnet
    stake_key = "stake_test1uq9947tw3wg5y7l0wmc59eyuz2fc4p76m6qjnwmw5ss58vsmzhs0n"
    id_str = "My ID string"
    result, id = client.query_reward_account_summaries.execute(keys=[stake_key], id=id_str)

    expected_keys = ["delegate", "rewards"]
    assert isinstance(result, dict)
    for key in expected_keys:
        assert key in result.get(list(result.keys())[0]).keys()
    assert id == id_str


def test_QueryRewardAccountSummaries_script_empty(client):
    # This test relies on this address having a balance on the testnet
    script_key = "stake_test1urlvxquq2pm8teqed7ek4sgjuc0zrx07z9czmy5fvwey92cq8c5dh"
    id_str = "My ID string"
    result, id = client.query_reward_account_summaries.execute(scripts=[script_key], id=id_str)

    assert result == {}
    assert id == id_str
