import copy

import pytest

from snowflake.core.exceptions import NotFoundError
from tests.integ.utils import random_string

from .conftest import test_sequence_template


def test_rename(sequences):
    original_name = random_string(10, "test_sequence_rename_original_")
    new_name = random_string(10, "test_sequence_rename_")

    sequence = copy.deepcopy(test_sequence_template)
    sequence.name = original_name
    sequence_handle = sequences.create(sequence)

    try:
        fetched_sequence = sequence_handle.fetch()
        assert fetched_sequence.name == original_name.upper()

        sequence_handle.rename(new_name)

        fetched_sequence = sequence_handle.fetch()
        assert fetched_sequence.name == new_name.upper()
        assert fetched_sequence.schema_name == sequences.schema.name.upper()
        assert fetched_sequence.database_name == sequences.database.name.upper()

        with pytest.raises(NotFoundError):
            sequences[original_name].fetch()

    finally:
        sequence_handle.drop(if_exists=True)


def test_rename_nonexistent_sequence(sequences):
    nonexistent_name = random_string(10, "test_sequence_rename_nonexistest_")
    new_name = random_string(10, "test_sequence_rename_")

    with pytest.raises(NotFoundError):
        sequences[nonexistent_name].rename(new_name)

    sequences[nonexistent_name].rename(new_name, if_exists=True)


def test_rename_across_schema(sequences, temp_schema):
    original_name = random_string(10, "test_sequence_rename_cross_schema_original_")
    new_name = random_string(10, "test_sequence_rename_cross_schema_")

    sequence = copy.deepcopy(test_sequence_template)
    sequence.name = original_name
    sequence_handle = sequences.create(sequence)

    try:
        sequence_handle.rename(new_name, target_schema=temp_schema.name)

        fetched_sequence = sequence_handle.fetch()
        assert fetched_sequence.name == new_name.upper()
        assert fetched_sequence.schema_name == temp_schema.name.upper()
        assert fetched_sequence.database_name == sequences.database.name.upper()

        with pytest.raises(NotFoundError):
            sequences[original_name].fetch()

    finally:
        sequence_handle.drop(if_exists=True)


def test_rename_across_database(sequences, temp_db):
    original_name = random_string(10, "test_sequence_rename_cross_db_original_")
    new_name = random_string(10, "test_sequence_rename_cross_db_")

    sequence = copy.deepcopy(test_sequence_template)
    sequence.name = original_name
    sequence_handle = sequences.create(sequence)

    try:
        sequence_handle.rename(new_name, target_database=temp_db.name, target_schema="PUBLIC")

        fetched_sequence = sequence_handle.fetch()
        assert fetched_sequence.name == new_name.upper()
        assert fetched_sequence.schema_name == "PUBLIC"
        assert fetched_sequence.database_name == temp_db.name.upper()

        with pytest.raises(NotFoundError):
            sequences[original_name].fetch()

    finally:
        sequence_handle.drop(if_exists=True)
