import copy

import pytest

from tests.integ.utils import random_string

from .conftest import test_sequence_template


@pytest.fixture(scope="module")
def sequences_extended(sequences):
    names_list = []

    for _ in range(5):
        names_list.append(random_string(10, "test_sequence_iter_a_"))

    for _ in range(7):
        names_list.append(random_string(10, "test_sequence_iter_b_"))

    for _ in range(3):
        names_list.append(random_string(10, "test_sequence_iter_c_"))

    try:
        for name in names_list:
            sequence = copy.deepcopy(test_sequence_template)
            sequence.name = name
            sequences.create(sequence)

        yield sequences
    finally:
        for name in names_list:
            sequences[name].drop(if_exists=True)


def test_iter_raw(sequences_extended):
    assert len(list(sequences_extended.iter())) >= 15


def test_iter_like(sequences_extended):
    assert len(list(sequences_extended.iter(like="test_sequence_iter_a_%"))) == 5
    assert len(list(sequences_extended.iter(like="test_sequence_iter_b_%"))) == 7
    assert len(list(sequences_extended.iter(like="test_sequence_iter_c_%"))) == 3
    assert len(list(sequences_extended.iter(like="TEST_SEQUENCE_ITER_C_%"))) == 3
    assert len(list(sequences_extended.iter(like="nonexistent_pattern_%"))) == 0
