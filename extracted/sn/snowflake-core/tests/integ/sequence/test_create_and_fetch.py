import copy

import pytest

from snowflake.core import CreateMode
from snowflake.core.exceptions import ConflictError
from tests.integ.utils import random_string

from .conftest import (
    test_sequence_minimal_template,
    test_sequence_template,
)


def test_create_and_fetch(sequences):
    name = random_string(10, "test_sequence_create_and_fetch_")
    sequence_handle = sequences[name]

    try:
        sequence = copy.deepcopy(test_sequence_template)
        sequence.name = name
        sequences.create(sequence)

        fetched_sequence = sequence_handle.fetch()

        assert fetched_sequence.name == name.upper()
        assert fetched_sequence.start == 2
        assert fetched_sequence.increment == 2
        assert fetched_sequence.ordered is True
        assert fetched_sequence.comment == "Test sequence"
        assert fetched_sequence.database_name == sequences.database.name.upper()
        assert fetched_sequence.schema_name == sequences.schema.name.upper()
    finally:
        sequence_handle.drop(if_exists=True)


def test_create_and_fetch_minimal(sequences):
    name = random_string(10, "test_sequence_create_and_fetch_")
    sequence_handle = sequences[name]

    try:
        sequence = copy.deepcopy(test_sequence_minimal_template)
        sequence.name = name
        sequences.create(sequence)

        fetched_sequence = sequence_handle.fetch()

        assert fetched_sequence.name == name.upper()
        assert fetched_sequence.start == 1
        assert fetched_sequence.increment == 1
        assert fetched_sequence.ordered is False
        assert fetched_sequence.comment is None
        assert fetched_sequence.database_name == sequences.database.name.upper()
        assert fetched_sequence.schema_name == sequences.schema.name.upper()
    finally:
        sequence_handle.drop(if_exists=True)


def test_create_and_fetch_create_modes(sequences):
    name = random_string(10, "test_sequence_create_and_fetch_")
    sequence_handle = sequences[name]

    try:
        sequence = copy.deepcopy(test_sequence_template)
        sequence.name = name
        sequence.comment = "First version"
        sequences.create(sequence, mode=CreateMode.error_if_exists)
        assert sequence_handle.fetch().comment == "First version"

        with pytest.raises(ConflictError):
            sequences.create(sequence, mode=CreateMode.error_if_exists)

        sequence.comment = "Second version"
        sequences.create(sequence, mode=CreateMode.or_replace)
        assert sequence_handle.fetch().comment == "Second version"

        sequence.comment = "Should not change"
        sequences.create(sequence, mode=CreateMode.if_not_exists)
        assert sequence_handle.fetch().comment == "Second version"
    finally:
        sequence_handle.drop(if_exists=True)
