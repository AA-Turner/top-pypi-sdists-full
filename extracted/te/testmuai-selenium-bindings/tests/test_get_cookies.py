# selenium-python/tests/test_get_cookies.py
import pytest
from testmu_selenium._helpers.cookies import get_cookies, find_dict_with_kv

COOKIES = [
    {"name": "UULE", "value": "abc", "domain": ".x.com", "httpOnly": True},
    {"name": "sid", "value": "42", "domain": ".x.com", "httpOnly": False},
]


class FakeDriver:
    def get_cookies(self):
        return list(COOKIES)


def test_get_all_cookies_returns_full_list():
    assert get_cookies(FakeDriver(), [], "") == COOKIES


def test_get_cookie_by_name_find_by_kv():
    assert get_cookies(FakeDriver(), [{"non-index": ["name", "UULE"]}], "") == COOKIES[0]


def test_get_cookie_by_index_then_key():
    assert get_cookies(FakeDriver(), [{"index": 0}, {"non-index": ["value"]}], "") == "abc"


def test_field_len():
    assert get_cookies(FakeDriver(), [], "len") == 2


def test_field_keys_on_single_cookie():
    assert get_cookies(FakeDriver(), [{"index": 0}], "keys") == list(COOKIES[0].keys())


def test_missing_kv_raises():
    with pytest.raises(ValueError):
        get_cookies(FakeDriver(), [{"non-index": ["name", "NOPE"]}], "")


def test_find_dict_with_kv_nested():
    assert find_dict_with_kv([{"a": {"name": "z"}}], "name", "z") == {"name": "z"}
