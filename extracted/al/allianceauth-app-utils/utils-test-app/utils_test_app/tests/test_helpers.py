from time import time
from unittest.mock import patch

from django.core.cache import cache
from django.test import TestCase

from app_utils.helpers import default_if_none, humanize_number, throttle


class TestingDefaultIfNone(TestCase):
    def test_should_return_value(self):
        # when
        result = default_if_none("alpha", "bravo")
        # then
        self.assertEqual(result, "alpha")

    def test_should_return_default(self):
        # when
        result = default_if_none(None, "bravo")
        # then
        self.assertEqual(result, "bravo")

    def test_should_return_value_for_false(self):
        # when
        result = default_if_none(False, "bravo")
        # then
        self.assertFalse(result)


class TestFormatisk(TestCase):
    def test_should_return_formatted_string_from_number_1(self):
        # when
        result = humanize_number(1260000000)
        # then
        self.assertEqual(result, "1.3b")

    def test_should_return_formatted_string_from_number_2(self):
        # when
        result = humanize_number(123456789)
        # then
        self.assertEqual(result, "123.5m")

    def test_should_return_formatted_string_from_string(self):
        # when
        result = humanize_number("1234567890")
        # then
        self.assertEqual(result, "1.2b")

    def test_should_raise_value_error_when_type_invalid(self):
        # when/then
        with self.assertRaises(ValueError):
            humanize_number("invalid")

    def test_should_use_custom_magnitude(self):
        # when
        result = humanize_number(123456789, "b")
        # then
        self.assertEqual(result, "0.1b")

    def test_should_format_with_custom_precision(self):
        # when
        result = humanize_number("1234567890", precision=3)
        # then
        self.assertEqual(result, "1.235b")


def my_func():
    """Dummy function for testing throttle()"""
    return "dummy"


@patch(f"{__package__}.test_helpers.my_func", wraps=my_func)
class TestThrottle(TestCase):
    def setUp(self) -> None:
        cache.clear()

    def test_should_run_once(self, spy_my_func):
        # when
        result = throttle(my_func, "test-1", timeout=60)
        # then
        self.assertEqual(spy_my_func.call_count, 1)
        self.assertEqual(result, "dummy")

    def test_should_run_twice_only(self, spy_my_func):
        # given
        start = time()
        # when
        while time() < start + 1.1:
            throttle(my_func, "test-1", timeout=1)
        # then
        self.assertEqual(spy_my_func.call_count, 2)

    def test_should_once_per_context_id(self, spy_my_func):
        # when
        throttle(my_func, "test-1", timeout=60)
        throttle(my_func, "test-2", timeout=60)
        throttle(my_func, "test-1", timeout=60)
        throttle(my_func, "test-2", timeout=60)
        # then
        self.assertEqual(spy_my_func.call_count, 2)
