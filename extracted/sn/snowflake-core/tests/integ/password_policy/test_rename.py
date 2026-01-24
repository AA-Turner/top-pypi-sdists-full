import copy

import pytest

from snowflake.core.exceptions import NotFoundError
from tests.integ.utils import random_string

from .conftest import test_password_policy_template


def test_rename(password_policies):
    original_name = random_string(10, "test_original_password_policy_")
    new_name = random_string(10, "test_renamed_password_policy_")

    password_policy = copy.deepcopy(test_password_policy_template)
    password_policy.name = original_name
    password_policy_handle = password_policies.create(password_policy)

    try:
        fetched_policy = password_policy_handle.fetch()
        assert fetched_policy.name.upper() == original_name.upper()

        password_policy_handle.rename(new_name)

        fetched_policy = password_policy_handle.fetch()
        assert fetched_policy.name == new_name.upper()
        assert fetched_policy.schema_name == password_policies.schema.name.upper()
        assert fetched_policy.database_name == password_policies.database.name.upper()

        with pytest.raises(NotFoundError):
            password_policies[original_name].fetch()

    finally:
        password_policy_handle.drop(if_exists=True)


def test_rename_nonexistent_password_policy(password_policies):
    """Test renaming a non-existent password policy raises NotFoundError."""
    nonexistent_name = random_string(10, "test_nonexistent_password_policy_")
    new_name = random_string(10, "test_new_name_password_policy_")

    with pytest.raises(NotFoundError):
        password_policies[nonexistent_name].rename(new_name)

    password_policies[nonexistent_name].rename(new_name, if_exists=True)


def test_rename_password_policy_cross_schema(password_policies, temp_schema):
    """Test renaming password policy across schemas."""
    original_name = random_string(10, "test_cross_schema_password_policy_")
    new_name = random_string(10, "test_renamed_cross_schema_password_policy_")

    password_policy = copy.deepcopy(test_password_policy_template)
    password_policy.name = original_name
    password_policy_handle = password_policies.create(password_policy)

    try:
        password_policy_handle.rename(
            new_name, target_schema=temp_schema.name, target_database=password_policy_handle.database.name
        )

        fetched_policy = password_policy_handle.fetch()
        assert fetched_policy.name.upper() == new_name.upper()
        assert fetched_policy.schema_name.upper() == temp_schema.name.upper()
        assert fetched_policy.database_name.upper() == password_policy_handle.database.name.upper()

        with pytest.raises(NotFoundError):
            password_policies[original_name].fetch()

    finally:
        password_policy_handle.drop(if_exists=True)
