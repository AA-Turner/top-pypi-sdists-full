import copy

import pytest

from snowflake.core.exceptions import NotFoundError
from tests.integ.utils import random_string

from .conftest import test_tag_template


def test_rename(tags):
    original_name = random_string(10, "test_original_tag_")
    new_name = random_string(10, "test_renamed_tag_")

    tag = copy.deepcopy(test_tag_template)
    tag.name = original_name
    tag_handle = tags.create(tag)

    try:
        fetched_tag = tag_handle.fetch()
        assert fetched_tag.name.upper() == original_name.upper()

        tag_handle.rename(new_name)
        fetched_tag = tag_handle.fetch()

        assert fetched_tag.name == new_name.upper()
        assert fetched_tag.schema_name == tags.schema.name.upper()
        assert fetched_tag.database_name == tags.database.name.upper()

        with pytest.raises(NotFoundError):
            tags[original_name].fetch()

    finally:
        tag_handle.drop(if_exists=True)


def test_rename_nonexistent_tag(tags):
    nonexistent_name = random_string(10, "test_nonexistent_tag_")
    new_name = random_string(10, "test_new_name_tag_")

    with pytest.raises(NotFoundError):
        tags[nonexistent_name].rename(new_name)

    tags[nonexistent_name].rename(new_name, if_exists=True)


def test_rename_tag_cross_schema(tags, temp_schema):
    original_name = random_string(10, "test_cross_schema_tag_")
    new_name = random_string(10, "test_renamed_cross_schema_tag_")

    tag = copy.deepcopy(test_tag_template)
    tag.name = original_name
    tag_handle = tags.create(tag)

    try:
        tag_handle.rename(new_name, target_schema=temp_schema.name)

        fetched_tag = tag_handle.fetch()
        assert fetched_tag.name == new_name.upper()
        assert fetched_tag.schema_name == temp_schema.name.upper()
        assert fetched_tag.database_name == tags.database.name.upper()

        with pytest.raises(NotFoundError):
            tags[original_name].fetch()

    finally:
        tag_handle.drop(if_exists=True)


def test_rename_across_database(tags, temp_db):
    original_name = random_string(10, "test_cross_db_tag_")
    new_name = random_string(10, "test_renamed_cross_db_tag_")

    tag = copy.deepcopy(test_tag_template)
    tag.name = original_name
    tag_handle = tags.create(tag)

    try:
        tag_handle.rename(new_name, target_database=temp_db.name, target_schema="PUBLIC")

        fetched_tag = tag_handle.fetch()
        assert fetched_tag.name == new_name.upper()
        assert fetched_tag.schema_name == "PUBLIC"
        assert fetched_tag.database_name == temp_db.name.upper()

        with pytest.raises(NotFoundError):
            tags[original_name].fetch()

    finally:
        tag_handle.drop(if_exists=True)
