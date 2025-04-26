from contextlib import suppress

import pytest as pytest

from snowflake.core.exceptions import NotFoundError
from tests.integ.utils import random_string


@pytest.mark.min_sf_ver("8.34.0")
@pytest.mark.use_accountadmin
def test_create_and_fetch(network_policies, template_network_policy):
    network_policy_name = random_string(10, "test_network_policy_")
    network_policy_handle = network_policies[network_policy_name]

    np = template_network_policy
    np.name = network_policy_name

    test_network_policy = network_policies.create(np)

    try:
        fetch_handle = test_network_policy.fetch()

        assert fetch_handle.name.upper() == network_policy_name.upper()
        assert fetch_handle.allowed_network_rule_list == np.allowed_network_rule_list
        assert fetch_handle.blocked_network_rule_list == np.blocked_network_rule_list
        assert fetch_handle.allowed_ip_list == np.allowed_ip_list
        assert fetch_handle.blocked_ip_list == np.blocked_ip_list

    finally:
        with suppress(NotFoundError):
            network_policy_handle.drop()
