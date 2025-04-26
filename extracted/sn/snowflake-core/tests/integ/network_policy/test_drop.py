import pytest as pytest

from snowflake.core.exceptions import NotFoundError
from tests.integ.utils import random_string


@pytest.mark.min_sf_ver("8.34.0")
@pytest.mark.use_accountadmin
def test_drop(network_policies, template_network_policy):
    network_policy_name = random_string(10, "test_network_policy_")
    network_policy_handle = network_policies[network_policy_name]

    np = template_network_policy
    np.name = network_policy_name

    test_network_policy = network_policies.create(np)

    fetch_handle = test_network_policy.fetch()
    assert fetch_handle.name.upper() == network_policy_name.upper()

    network_policy_handle.drop()

    with pytest.raises(NotFoundError):
        test_network_policy.fetch()

    with pytest.raises(NotFoundError):
        test_network_policy.drop(if_exists=False)

    test_network_policy.drop(if_exists=True)
