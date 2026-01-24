import copy

import pytest

from snowflake.core import CreateMode
from snowflake.core.exceptions import ConflictError
from tests.integ.utils import random_string

from .conftest import (
    test_password_policy_minimal_template,
    test_password_policy_template,
)


def test_create_and_fetch(password_policies):
    name = random_string(10, "test_password_policy_create_and_fetch_")
    password_policy_handle = password_policies[name]

    try:
        password_policy = copy.deepcopy(test_password_policy_template)
        password_policy.name = name
        password_policies.create(password_policy)

        fetched_policy = password_policy_handle.fetch()

        assert fetched_policy.name.upper() == name.upper()
        assert fetched_policy.password_min_length == 8
        assert fetched_policy.password_max_length == 256
        assert fetched_policy.password_min_upper_case_chars == 1
        assert fetched_policy.password_min_lower_case_chars == 1
        assert fetched_policy.password_min_numeric_chars == 1
        assert fetched_policy.password_min_special_chars == 1
        assert fetched_policy.password_min_age_days == 1
        assert fetched_policy.password_max_age_days == 90
        assert fetched_policy.password_max_retries == 5
        assert fetched_policy.password_lockout_time_mins == 15
        assert fetched_policy.password_history == 24
        assert fetched_policy.comment == "Test password policy"
    finally:
        password_policy_handle.drop(if_exists=True)


def test_create_and_fetch_minimal(password_policies):
    name = random_string(10, "test_password_policy_create_and_fetch_")
    password_policy_handle = password_policies[name]

    try:
        password_policy = copy.deepcopy(test_password_policy_minimal_template)
        password_policy.name = name
        password_policies.create(password_policy)

        fetched_policy = password_policy_handle.fetch()

        assert fetched_policy.name.upper() == name.upper()
        assert fetched_policy.password_min_length == 14  # Default value
    finally:
        password_policy_handle.drop(if_exists=True)


def test_create_and_fetch_create_modes(password_policies):
    name = random_string(10, "test_password_policy_create_and_fetch_")
    password_policy_handle = password_policies[name]

    try:
        password_policy = copy.deepcopy(test_password_policy_template)
        password_policy.name = name
        password_policy.comment = "First version"
        password_policies.create(password_policy, mode=CreateMode.error_if_exists)
        assert password_policy_handle.fetch().comment == "First version"

        with pytest.raises(ConflictError):
            password_policies.create(password_policy, mode=CreateMode.error_if_exists)

        password_policy.comment = "Second version"
        password_policies.create(password_policy, mode=CreateMode.or_replace)
        assert password_policy_handle.fetch().comment == "Second version"

        password_policy.comment = "Should not change"
        password_policies.create(password_policy, mode=CreateMode.if_not_exists)
        assert password_policy_handle.fetch().comment == "Second version"
    finally:
        password_policy_handle.drop(if_exists=True)
