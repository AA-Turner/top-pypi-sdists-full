from pymultirole_plugins.util import comma_separated_to_list


def test_comma_separated_to_list():
    list1 = comma_separated_to_list("a,b, c ,d")
    assert len(list1) == 4
    assert "c" in list1
