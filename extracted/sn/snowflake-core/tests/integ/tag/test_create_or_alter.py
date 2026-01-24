import copy

from tests.integ.utils import random_string

from .conftest import test_tag_template


def test_create_or_alter_tag(tags):
    tag_name = random_string(10, "test_tag_create_or_alter_")
    tag_def = copy.deepcopy(test_tag_template)
    tag_def.name = tag_name
    tag_def.comment = "created by test_create_or_alter_tag"

    tag = tags[tag_name]
    tag.create_or_alter(tag_def)
    try:
        fetched_tag = tag.fetch()
        assert fetched_tag.name.upper() == tag_name.upper()
        assert fetched_tag.allowed_values == tag_def.allowed_values
        assert fetched_tag.comment == tag_def.comment

        fetched_tag.comment = "altered by test_create_or_alter_tag"
        fetched_tag.allowed_values = ["new_value1", "new_value2", "new_value3"]
        tag.create_or_alter(fetched_tag)

        altered_tag = tag.fetch()
        assert altered_tag.name.upper() == tag_name.upper()
        assert altered_tag.allowed_values == ["new_value1", "new_value2", "new_value3"]
        assert altered_tag.comment == "altered by test_create_or_alter_tag"
    finally:
        tag.drop(if_exists=True)


def test_create_or_alter_unset_comment(tags):
    tag_name = random_string(10, "test_tag_unset_comment_")
    tag_def = copy.deepcopy(test_tag_template)
    tag_def.name = tag_name
    tag_def.comment = "comment to be removed"

    tag = tags.create(tag_def)
    try:
        updated_tag_def = copy.deepcopy(test_tag_template)
        updated_tag_def.name = tag_name
        updated_tag_def.comment = None
        tag.create_or_alter(updated_tag_def)

        fetched_tag = tag.fetch()
        assert fetched_tag.name.upper() == tag_name.upper()
        assert fetched_tag.comment is None
    finally:
        tag.drop(if_exists=True)
