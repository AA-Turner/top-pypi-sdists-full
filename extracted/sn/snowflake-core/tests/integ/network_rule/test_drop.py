import copy

import pytest

from snowflake.core.exceptions import NotFoundError
from tests.integ.utils import random_string

from .conftest import test_network_rule_template


def test_drop(network_rules):
    prefix = "test_network_rule_drop_"
    pre_create_count = len(list(network_rules.iter(like=prefix + "%")))

    name = random_string(10, prefix)
    network_rule_handle = network_rules[name]

    network_rule = copy.deepcopy(test_network_rule_template)
    network_rule.name = name
    network_rules.create(network_rule)

    created_count = len(list(network_rules.iter(like=prefix + "%")))
    assert pre_create_count + 1 == created_count

    network_rule_handle.drop()

    after_drop_count = len(list(network_rules.iter(like=prefix + "%")))
    assert pre_create_count == after_drop_count

    with pytest.raises(NotFoundError):
        network_rule_handle.drop()
        network_rule_handle.drop(if_exists=False)

    network_rule_handle.drop(if_exists=True)
