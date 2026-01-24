import copy

import pytest

from tests.integ.utils import random_string

from .conftest import test_tag_template


@pytest.fixture(scope="module")
def tags_extended(tags):
    names_list = []

    for _ in range(5):
        names_list.append(random_string(10, "test_tag_iter_a_"))

    for _ in range(7):
        names_list.append(random_string(10, "test_tag_iter_b_"))

    for _ in range(3):
        names_list.append(random_string(10, "test_tag_iter_c_"))

    try:
        for name in names_list:
            tag = copy.deepcopy(test_tag_template)
            tag.name = name
            tags.create(tag)

        yield tags
    finally:
        for name in names_list:
            tags[name].drop(if_exists=True)


def test_iter_raw(tags_extended):
    assert len(list(tags_extended.iter())) >= 15


def test_iter_like(tags_extended):
    assert len(list(tags_extended.iter(like="test_tag_iter_a_%"))) == 5
    assert len(list(tags_extended.iter(like="test_tag_iter_b_%"))) == 7
    assert len(list(tags_extended.iter(like="test_tag_iter_c_%"))) == 3
    assert len(list(tags_extended.iter(like="TEST_TAG_ITER_C_%"))) == 3
    assert len(list(tags_extended.iter(like="nonexistent_pattern_%"))) == 0
