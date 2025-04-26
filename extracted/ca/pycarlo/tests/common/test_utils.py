from pycarlo.common.utils import truncate_string


def test_truncate_string():
    assert "abcd" == truncate_string("abcde", 4)
    assert "abñ" == truncate_string("abñde", 4)
    assert "añc" == truncate_string("añcd", 4)
    assert "abc" == truncate_string("abcñe", 4)
