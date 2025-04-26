from .. import pop_utils


def test_pop_utils_remove():
    assert pop_utils.remove_pop_from_str(None, "") == ""
    assert pop_utils.remove_pop_from_str("", "") == ""
    assert pop_utils.remove_pop_from_str(" ", "") == ""
    assert pop_utils.remove_pop_from_str("foobar", "") == "foobar"
    assert pop_utils.remove_pop_from_str("foobar", "foobar") == ""
    assert pop_utils.remove_pop_from_str("foobar,1,3", "foobar") == "1,3"
    assert pop_utils.remove_pop_from_str("foobar,1,3", "foobar") == "1,3"
    assert pop_utils.remove_pop_from_str("foobar,1,3", "3") == "1,foobar"
    assert pop_utils.remove_pop_from_str("3,2,1", "") == "1,2,3"
    assert pop_utils.remove_pop_from_str("3,2,1", "3") == "1,2"


def test_pop_utils_add():
    assert pop_utils.add_pop_to_str(None, "") == ""
    assert pop_utils.add_pop_to_str("", "") == ""
    assert pop_utils.add_pop_to_str("1,2,3", "") == "1,2,3"
    assert pop_utils.add_pop_to_str("1,2,3", "") == "1,2,3"
    assert pop_utils.add_pop_to_str("1,3", "2") == "1,2,3"
    assert pop_utils.add_pop_to_str("4,3,2,1", "2") == "1,2,3,4"
