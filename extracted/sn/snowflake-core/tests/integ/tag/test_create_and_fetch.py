import copy

import pytest

from snowflake.core import CreateMode
from snowflake.core.exceptions import ConflictError
from tests.utils import is_gov_deployment, random_string

from .conftest import (
    test_tag_minimal_template,
    test_tag_template,
)


def test_create_and_fetch(tags, snowflake_region):
    name = random_string(10, "test_tag_create_and_fetch_")
    tag_handle = tags[name]

    try:
        tag = copy.deepcopy(test_tag_template)
        tag.name = name
        tags.create(tag)

        fetched_tag = tag_handle.fetch()

        assert fetched_tag.name == name.upper()
        assert fetched_tag.allowed_values == ["value1", "value2", "value3"]
        assert fetched_tag.comment == "Test tag"
        if is_gov_deployment(snowflake_region):
            assert fetched_tag.propagate == "NONE"
        else:
            assert fetched_tag.propagate is None
        assert fetched_tag.on_conflict is None
        assert fetched_tag.database_name == tags.database.name.upper()
        assert fetched_tag.schema_name == tags.schema.name.upper()
    finally:
        tag_handle.drop(if_exists=True)


def test_create_and_fetch_minimal(tags, snowflake_region):
    name = random_string(10, "test_tag_create_and_fetch_minimal_")
    tag_handle = tags[name]

    try:
        tag = copy.deepcopy(test_tag_minimal_template)
        tag.name = name
        tags.create(tag)

        fetched_tag = tag_handle.fetch()

        assert fetched_tag.name == name.upper()
        assert fetched_tag.allowed_values is None
        assert fetched_tag.comment is None
        if is_gov_deployment(snowflake_region):
            assert fetched_tag.propagate == "NONE"
        else:
            assert fetched_tag.propagate is None
        assert fetched_tag.on_conflict is None
        assert fetched_tag.database_name == tags.database.name.upper()
        assert fetched_tag.schema_name == tags.schema.name.upper()
    finally:
        tag_handle.drop(if_exists=True)


def test_create_and_fetch_create_modes(tags):
    name = random_string(10, "test_tag_create_and_fetch_modes_")
    tag_handle = tags[name]

    try:
        tag = copy.deepcopy(test_tag_template)
        tag.name = name
        tag.comment = "First version"
        tags.create(tag, mode=CreateMode.error_if_exists)
        assert tag_handle.fetch().comment == "First version"

        with pytest.raises(ConflictError):
            tags.create(tag, mode=CreateMode.error_if_exists)

        tag.comment = "Second version"
        tags.create(tag, mode=CreateMode.or_replace)
        assert tag_handle.fetch().comment == "Second version"

        tag.comment = "Should not change"
        tags.create(tag, mode=CreateMode.if_not_exists)
        assert tag_handle.fetch().comment == "Second version"
    finally:
        tag_handle.drop(if_exists=True)
