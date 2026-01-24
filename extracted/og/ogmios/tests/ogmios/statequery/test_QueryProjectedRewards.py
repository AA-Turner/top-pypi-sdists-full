from datetime import datetime

from ogmios.datatypes import Ada
from tests.ogmios.test_fixtures import client

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def test_QueryProjectedRewards_key(client):
    # This test relies on this address having a balance on the testnet
    stake_key = "stake_test1urlvxquq2pm8teqed7ek4sgjuc0zrx07z9czmy5fvwey92cq8c5dh"
    id_str = "My ID string"
    projection, id = client.query_projected_rewards.execute(
        stake=[Ada(10000)], keys=[stake_key], id=id_str
    )

    assert isinstance(projection, dict)
    assert id == id_str


def test_QueryProjectedRewards_script(client):
    # This test relies on this address having a balance on the testnet
    script_key = "stake_test1urlvxquq2pm8teqed7ek4sgjuc0zrx07z9czmy5fvwey92cq8c5dh"
    id_str = "My ID string"
    projection, id = client.query_projected_rewards.execute(
        stake=[Ada(10000)], scripts=[script_key], id=id_str
    )

    assert isinstance(projection, dict)
    assert id == id_str
