import copy

import pytest

from tests.integ.utils import random_string

from .conftest import test_network_rule_template


@pytest.fixture(scope="module")
def network_rules_extended(network_rules):
    names_list = []

    for _ in range(5):
        names_list.append(random_string(10, "test_network_rule_iter_a_"))

    for _ in range(7):
        names_list.append(random_string(10, "test_network_rule_iter_b_"))

    for _ in range(3):
        names_list.append(random_string(10, "test_network_rule_iter_c_"))

    try:
        for name in names_list:
            network_rule = copy.deepcopy(test_network_rule_template)
            network_rule.name = name
            network_rules.create(network_rule)

        yield network_rules
    finally:
        for name in names_list:
            network_rules[name].drop(if_exists=True)


def test_iter_raw(network_rules_extended):
    assert len(list(network_rules_extended.iter())) >= 15


def test_iter_like(network_rules_extended):
    assert len(list(network_rules_extended.iter(like="test_network_rule_iter_a_%"))) == 5
    assert len(list(network_rules_extended.iter(like="test_network_rule_iter_b_%"))) == 7
    assert len(list(network_rules_extended.iter(like="test_network_rule_iter_c_%"))) == 3
    assert len(list(network_rules_extended.iter(like="TEST_NETWORK_RULE_ITER_C_%"))) == 3
    assert len(list(network_rules_extended.iter(like="nonexistent_pattern_%"))) == 0


def test_iter_limit(network_rules_extended):
    assert len(list(network_rules_extended.iter(limit=2))) == 2


def test_iter_starts_with(network_rules_extended):
    assert len(list(network_rules_extended.iter(starts_with="test_network_rule_iter_a_".upper()))) == 5
    assert len(list(network_rules_extended.iter(starts_with="test_network_rule_iter_a_"))) == 0
    assert len(list(network_rules_extended.iter(starts_with="test_network_rule_iter_d_".upper()))) == 0


def test_iter_from_name(network_rules_extended):
    # The limit keyword is required for the from keyword to function, limit=20 was chosen arbitrarily
    # as it does not affect the test
    rules_from_b = list(network_rules_extended.iter(limit=20, from_name="test_network_rule_iter_b_".upper()))
    assert len(rules_from_b) == 10
