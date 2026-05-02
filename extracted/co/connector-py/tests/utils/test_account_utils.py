from connector.utils.account import split_name


def test_split_name():
    assert split_name("John Doe") == ("John", "Doe")
    assert split_name("John") == ("John", None)
    assert split_name(None) == (None, None)
    assert split_name("John Doe Smith") == ("John", "Doe Smith")
