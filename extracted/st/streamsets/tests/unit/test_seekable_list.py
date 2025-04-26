# Copyright 2023 StreamSets Inc.

# fmt: off
import pytest

from streamsets.sdk.utils import SeekableList

# fmt: on


class Helper:
    def __init__(self, helper_id, helper_name):
        self.id = helper_id
        self.name = helper_name


@pytest.fixture(autouse=True)
def helper_object_list():
    return [Helper(helper_id=uid, helper_name=name) for uid, name in zip(range(1, 3), ['John', 'Jane', 'Alice'])]


@pytest.fixture(autouse=True)
def helper_object_list_duplicate_id():
    return [Helper(helper_id=uid, helper_name=name) for uid, name in zip([1, 2, 2], ['John', 'Jane', 'Alice'])]


def test_get_valid_input(helper_object_list):
    seekable_list = SeekableList(helper_object_list)
    result = seekable_list.get(id=2)
    assert result.id == 2
    assert result.name == 'Jane'


def test_get_invalid_input(helper_object_list):
    seekable_list = SeekableList(helper_object_list)

    with pytest.raises(ValueError) as e:
        seekable_list.get(id=4)

    assert str(e.value) == "Instance (id=4) is not in list"


def test_get_all_valid_input_duplicate_id(helper_object_list_duplicate_id):
    seekable_list = SeekableList(helper_object_list_duplicate_id)

    result = seekable_list.get_all(id=2)

    assert isinstance(result, SeekableList)
    assert len(result) == 2
    assert result[0].id == 2
    assert result[1].id == 2


def test_get_all_invalid_input(helper_object_list):
    seekable_list = SeekableList(helper_object_list)

    result = seekable_list.get_all(id=4)

    assert isinstance(result, SeekableList)
    assert len(result) == 0


def test_cast_seekable_to_list(helper_object_list):
    seekable_list = SeekableList(helper_object_list)
    casted_list = list(seekable_list)

    assert isinstance(casted_list, list)
    assert isinstance(casted_list[0], Helper)

    seekable_list_ids = [helper.id for helper in seekable_list]
    casted_list_ids = [helper.id for helper in casted_list]

    assert seekable_list_ids == casted_list_ids
