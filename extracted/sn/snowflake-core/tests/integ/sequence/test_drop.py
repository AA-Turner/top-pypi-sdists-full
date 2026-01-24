import copy

import pytest

from snowflake.core.exceptions import NotFoundError
from tests.integ.utils import random_string

from .conftest import test_sequence_template


def test_drop(sequences):
    prefix = "test_sequence_drop_"
    pre_create_count = len(list(sequences.iter(like=prefix + "%")))

    name = random_string(10, prefix)
    sequence_handle = sequences[name]

    sequence = copy.deepcopy(test_sequence_template)
    sequence.name = name
    sequences.create(sequence)

    created_count = len(list(sequences.iter(like=prefix + "%")))
    assert pre_create_count + 1 == created_count

    sequence_handle.drop()

    after_drop_count = len(list(sequences.iter(like=prefix + "%")))
    assert pre_create_count == after_drop_count

    with pytest.raises(NotFoundError):
        sequence_handle.drop()
        sequence_handle.drop(if_exists=False)

    sequence_handle.drop(if_exists=True)
