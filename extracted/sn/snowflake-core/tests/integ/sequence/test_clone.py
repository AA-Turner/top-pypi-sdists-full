import copy

from typing import Iterator

import pytest

from snowflake.core import CreateMode
from snowflake.core.exceptions import ConflictError, NotFoundError
from snowflake.core.sequence import Sequence, SequenceResource
from tests.integ.utils import random_string

from .conftest import test_sequence_template


@pytest.fixture
def temp_sequence(sequences) -> Iterator[SequenceResource]:
    sequence_name = random_string(10, "test_sequence_clone_original_")
    sequence = copy.deepcopy(test_sequence_template)
    sequence.name = sequence_name
    sequence_handle = sequences.create(sequence)

    try:
        yield sequence_handle
    finally:
        sequences[sequence_name].drop(if_exists=True)


def test_clone(sequences, temp_sequence):
    clone_name = random_string(10, "test_sequence_clone_")
    clone_sequence = Sequence(name=clone_name, comment="Updated comment")

    try:
        temp_sequence.clone(clone_sequence)

        fetched_clone = sequences[clone_name].fetch()
        assert fetched_clone.name == clone_name.upper()
        assert fetched_clone.start == 2
        assert fetched_clone.increment == 2
        assert fetched_clone.ordered is True
        assert fetched_clone.comment == "Updated comment"
        assert fetched_clone.schema_name == sequences.schema.name.upper()
        assert fetched_clone.database_name == sequences.database.name.upper()
    finally:
        sequences[clone_name].drop(if_exists=True)


def test_clone_nonexistent_sequence(sequences):
    nonexistent_name = random_string(10, "test_sequence_clone_nonexistest_")
    clone_name = random_string(10, "test_sequence_clone_")
    clone_sequence = Sequence(name=clone_name)

    with pytest.raises(NotFoundError):
        sequences[nonexistent_name].clone(clone_sequence)


def test_clone_create_modes(sequences, temp_sequence):
    clone_name = random_string(10, "test_sequence_clone_modes_")
    clone_sequence = Sequence(name=clone_name, comment="First version")

    try:
        temp_sequence.clone(clone_sequence, create_mode=CreateMode.error_if_exists)

        assert sequences[clone_name].fetch().comment == "First version"

        with pytest.raises(ConflictError):
            temp_sequence.clone(clone_sequence, create_mode=CreateMode.error_if_exists)

        clone_sequence.comment = "Second version"
        temp_sequence.clone(clone_sequence, create_mode=CreateMode.or_replace)
        assert sequences[clone_name].fetch().comment == "Second version"

        clone_sequence.comment = "Should not change"
        temp_sequence.clone(clone_sequence, create_mode=CreateMode.if_not_exists)
        assert sequences[clone_name].fetch().comment == "Second version"
    finally:
        sequences[clone_name].drop(if_exists=True)


def test_clone_across_schema(temp_sequence, temp_schema):
    clone_name = random_string(10, "test_sequence_clone_cross_schema_")
    clone_sequence = Sequence(name=clone_name)

    try:
        temp_sequence.clone(clone_sequence, target_schema=temp_schema.name)

        cloned_handle = temp_schema.sequences[clone_name]
        fetched_clone = cloned_handle.fetch()

        assert fetched_clone.name == clone_name.upper()
        assert fetched_clone.schema_name == temp_schema.name.upper()
        assert fetched_clone.database_name == temp_sequence.database.name.upper()
    finally:
        temp_schema.sequences[clone_name].drop(if_exists=True)


def test_clone_across_database(temp_sequence, databases, temp_db):
    clone_name = random_string(10, "test_sequence_clone_cross_db_")
    clone_sequence = Sequence(name=clone_name)

    try:
        temp_sequence.clone(clone_sequence, target_database=temp_db.name, target_schema="PUBLIC")

        cloned_handle = databases[temp_db.name].schemas["PUBLIC"].sequences[clone_name]
        fetched_clone = cloned_handle.fetch()

        assert fetched_clone.name == clone_name.upper()
        assert fetched_clone.schema_name == "PUBLIC"
        assert fetched_clone.database_name == temp_db.name.upper()
    finally:
        databases[temp_db.name].schemas["PUBLIC"].sequences[clone_name].drop()
