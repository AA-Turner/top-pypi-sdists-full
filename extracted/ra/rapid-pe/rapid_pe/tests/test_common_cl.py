# -*- coding: utf-8 -*-

"""Test suite for `rapidpe.common_cl`
"""

import pytest

from rapid_pe import common_cl


@pytest.mark.parametrize(("in_", "out"), [
    (("key 1=value 1", "key 2=value 2"),
     {"key 1": "value 1", "key 2": "value 2"}),
])
def test_parse_cl_key_value(in_, out):
    assert common_cl.parse_cl_key_value(in_) == out
