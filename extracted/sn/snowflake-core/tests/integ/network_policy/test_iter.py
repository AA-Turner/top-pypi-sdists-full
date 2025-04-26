from contextlib import suppress

import pytest as pytest

from snowflake.core.exceptions import NotFoundError
from tests.integ.utils import random_string


@pytest.mark.min_sf_ver("8.34.0")
@pytest.mark.use_accountadmin
def test_iter(network_policies, template_network_policy, prepare_rules_for_network_polices):
    names_list = []
    prefix = random_string(5, "test_network_policies_iter_").upper()
    for _ in range(5):
        names_list.append(random_string(10, prefix).upper())

    allowed_rules, blocked_rules = prepare_rules_for_network_polices

    try:
        for name in names_list:
            np = template_network_policy
            np.name = name
            network_policies.create(np)

        tests_network_policies = [np for np in network_policies.iter() if np.name.startswith(prefix)]

        assert len(tests_network_policies) >= 5

        for np in tests_network_policies:
            assert np.name in names_list
            assert allowed_rules == np.allowed_network_rule_list
            assert blocked_rules == np.blocked_network_rule_list
            assert ["8.8.8.8"] == np.allowed_ip_list
            assert ["0.0.0.0"] == np.blocked_ip_list

    finally:
        for name in names_list:
            with suppress(NotFoundError):
                network_policies[name].drop()
