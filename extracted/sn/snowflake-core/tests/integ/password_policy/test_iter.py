import copy

import pytest

from tests.integ.utils import random_string

from .conftest import test_password_policy_template


@pytest.fixture(scope="module")
def password_policies_extended(password_policies):
    names_list = []

    for _ in range(5):
        names_list.append(random_string(10, "test_password_policy_iter_a_"))

    for _ in range(7):
        names_list.append(random_string(10, "test_password_policy_iter_b_"))

    for _ in range(3):
        names_list.append(random_string(10, "test_password_policy_iter_c_"))

    try:
        for name in names_list:
            password_policy = copy.deepcopy(test_password_policy_template)
            password_policy.name = name
            password_policies.create(password_policy)

        yield password_policies
    finally:
        for name in names_list:
            password_policies[name].drop(if_exists=True)


def test_iter_raw(password_policies_extended):
    assert len(list(password_policies_extended.iter())) >= 15


def test_iter_like(password_policies_extended):
    assert len(list(password_policies_extended.iter(like="test_password_policy_iter_a_%"))) == 5
    assert len(list(password_policies_extended.iter(like="test_password_policy_iter_b_%"))) == 7
    assert len(list(password_policies_extended.iter(like="test_password_policy_iter_c_%"))) == 3
    assert len(list(password_policies_extended.iter(like="TEST_PASSWORD_POLICY_ITER_C_%"))) == 3
    assert len(list(password_policies_extended.iter(like="nonexistent_pattern_%"))) == 0


def test_iter_limit(password_policies_extended):
    assert len(list(password_policies_extended.iter(limit=2))) == 2


def test_iter_starts_with(password_policies_extended):
    assert len(list(password_policies_extended.iter(starts_with="test_password_policy_iter_a_".upper()))) == 5
    assert len(list(password_policies_extended.iter(starts_with="test_password_policy_iter_a_"))) == 0
    assert len(list(password_policies_extended.iter(starts_with="test_password_policy_iter_d_".upper()))) == 0
