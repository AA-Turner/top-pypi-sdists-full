import copy

import pytest

from snowflake.core import CreateMode
from snowflake.core.exceptions import ConflictError
from tests.integ.utils import random_string

from .conftest import (
    test_network_rule_minimal_template,
    test_network_rule_template,
)


def test_create_and_fetch(network_rules):
    name = random_string(10, "test_network_rule_create_and_fetch_")
    network_rule_handle = network_rules[name]

    try:
        network_rule = copy.deepcopy(test_network_rule_template)
        network_rule.name = name
        network_rules.create(network_rule)

        fetched_rule = network_rule_handle.fetch()

        assert fetched_rule.name.upper() == name.upper()
        assert fetched_rule.type == "HOST_PORT"
        assert fetched_rule.mode.upper() == "EGRESS"
        assert fetched_rule.value_list == ["example.com:443", "api.example.com:443"]
        assert fetched_rule.comment == "Test network rule"
    finally:
        network_rule_handle.drop(if_exists=True)


def test_create_and_fetch_minimal(network_rules):
    name = random_string(10, "test_network_rule_create_and_fetch_")
    network_rule_handle = network_rules[name]

    try:
        network_rule = copy.deepcopy(test_network_rule_minimal_template)
        network_rule.name = name
        network_rules.create(network_rule)

        fetched_rule = network_rule_handle.fetch()

        assert fetched_rule.name.upper() == name.upper()
        assert fetched_rule.type == "IPv4"
        assert fetched_rule.mode.upper() == "INGRESS"
        assert fetched_rule.value_list == []
        assert fetched_rule.comment is None
    finally:
        network_rule_handle.drop(if_exists=True)


def test_create_and_fetch_create_modes(network_rules):
    name = random_string(10, "test_network_rule_create_and_fetch_")
    network_rule_handle = network_rules[name]

    try:
        network_rule = copy.deepcopy(test_network_rule_template)
        network_rule.name = name
        network_rule.comment = "First version"
        network_rules.create(network_rule, mode=CreateMode.error_if_exists)
        assert network_rule_handle.fetch().comment == "First version"

        with pytest.raises(ConflictError):
            network_rules.create(network_rule, mode=CreateMode.error_if_exists)

        network_rule.comment = "Second version"
        network_rules.create(network_rule, mode=CreateMode.or_replace)
        assert network_rule_handle.fetch().comment == "Second version"

        network_rule.comment = "Should not change"
        network_rules.create(network_rule, mode=CreateMode.if_not_exists)
        assert network_rule_handle.fetch().comment == "Second version"
    finally:
        network_rule_handle.drop(if_exists=True)
