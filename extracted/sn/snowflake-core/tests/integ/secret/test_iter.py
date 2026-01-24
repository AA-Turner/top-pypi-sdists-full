import copy

import pytest

from tests.integ.utils import random_string

from .conftest import test_generic_string_secret_template


@pytest.fixture(scope="module")
def secrets_extended(secrets):
    names_list = []

    for _ in range(5):
        names_list.append(random_string(10, "test_secret_iter_a_"))

    for _ in range(7):
        names_list.append(random_string(10, "test_secret_iter_b_"))

    for _ in range(3):
        names_list.append(random_string(10, "test_secret_iter_c_"))

    try:
        for name in names_list:
            secret = copy.deepcopy(test_generic_string_secret_template)
            secret.name = name
            secrets.create(secret)

        yield secrets
    finally:
        for name in names_list:
            secrets[name].drop(if_exists=True)


def test_iter_raw(secrets_extended):
    assert len(list(secrets_extended.iter())) >= 15


def test_iter_like(secrets_extended):
    assert len(list(secrets_extended.iter(like="test_secret_iter_a_%"))) == 5
    assert len(list(secrets_extended.iter(like="test_secret_iter_b_%"))) == 7
    assert len(list(secrets_extended.iter(like="test_secret_iter_c_%"))) == 3
    assert len(list(secrets_extended.iter(like="TEST_SECRET_ITER_C_%"))) == 3
    assert len(list(secrets_extended.iter(like="nonexistent_pattern_%"))) == 0


def test_iter_limit(secrets_extended):
    assert len(list(secrets_extended.iter(limit=2))) == 2


def test_iter_starts_with(secrets_extended):
    assert len(list(secrets_extended.iter(starts_with="test_secret_iter_a_".upper()))) == 5
    assert len(list(secrets_extended.iter(starts_with="test_secret_iter_a_"))) == 0
    assert len(list(secrets_extended.iter(starts_with="test_secret_iter_d_".upper()))) == 0


def test_iter_from_name(secrets_extended):
    # The limit keyword is required for the from keyword to function, limit=20 was chosen arbitrarily
    # as it does not affect the test
    secrets_from_b = list(secrets_extended.iter(limit=20, from_name="test_secret_iter_b_".upper()))
    assert len(secrets_from_b) == 10
