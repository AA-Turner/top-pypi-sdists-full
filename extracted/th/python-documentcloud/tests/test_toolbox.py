# Future
from __future__ import division, print_function, unicode_literals

# DocumentCloud
from documentcloud.toolbox import get_id


def test_get_id_number():
    assert get_id(42) == 42


def test_get_id_str():
    assert get_id("42") == "42"


def test_get_id_prefix():
    assert get_id("42-foo-bar") == "42"


def test_get_id_postfix():
    assert get_id("foo-bar-42") == "42"


def test_get_id_both():
    assert get_id("42-foo-bar-123") == "42"
