from unittest.mock import Mock, patch

import requests
from django.test import TestCase

from eveuniverse.utils import (
    NoSocketsTestCase,
    SocketAccessError,
    chunks,
    clean_setting,
)

MODULE_PATH = "eveuniverse.utils"


class TestChunks(TestCase):
    def test_chunks(self):
        a0 = [1, 2, 3, 4, 5, 6]
        a1 = list(chunks(a0, 2))
        self.assertListEqual(a1, [[1, 2], [3, 4], [5, 6]])


class TestCleanSetting(TestCase):
    @patch(MODULE_PATH + ".settings")
    def test_default_if_not_set(self, mock_settings):
        mock_settings.TEST_SETTING_DUMMY = Mock(spec=None)
        result = clean_setting(
            "TEST_SETTING_DUMMY",
            False,
        )
        self.assertEqual(result, False)

    @patch(MODULE_PATH + ".settings")
    def test_default_if_not_set_for_none(self, mock_settings):
        mock_settings.TEST_SETTING_DUMMY = Mock(spec=None)
        result = clean_setting("TEST_SETTING_DUMMY", None, required_type=int)
        self.assertEqual(result, None)

    @patch(MODULE_PATH + ".settings")
    def test_true_stays_true(self, mock_settings):
        mock_settings.TEST_SETTING_DUMMY = True
        result = clean_setting(
            "TEST_SETTING_DUMMY",
            False,
        )
        self.assertEqual(result, True)

    @patch(MODULE_PATH + ".settings")
    def test_false_stays_false(self, mock_settings):
        mock_settings.TEST_SETTING_DUMMY = False
        result = clean_setting("TEST_SETTING_DUMMY", False)
        self.assertEqual(result, False)

    @patch(MODULE_PATH + ".settings")
    def test_default_for_invalid_type_bool(self, mock_settings):
        mock_settings.TEST_SETTING_DUMMY = "invalid type"
        result = clean_setting("TEST_SETTING_DUMMY", False)
        self.assertEqual(result, False)

    @patch(MODULE_PATH + ".settings")
    def test_default_for_invalid_type_int(self, mock_settings):
        mock_settings.TEST_SETTING_DUMMY = "invalid type"
        result = clean_setting("TEST_SETTING_DUMMY", 50)
        self.assertEqual(result, 50)

    @patch(MODULE_PATH + ".settings")
    def test_default_if_below_minimum_1(self, mock_settings):
        mock_settings.TEST_SETTING_DUMMY = -5
        result = clean_setting("TEST_SETTING_DUMMY", default_value=50)
        self.assertEqual(result, 50)

    @patch(MODULE_PATH + ".settings")
    def test_default_if_below_minimum_2(self, mock_settings):
        mock_settings.TEST_SETTING_DUMMY = -50
        result = clean_setting("TEST_SETTING_DUMMY", default_value=50, min_value=-10)
        self.assertEqual(result, 50)

    @patch(MODULE_PATH + ".settings")
    def test_default_for_invalid_type_int_2(self, mock_settings):
        mock_settings.TEST_SETTING_DUMMY = 1000
        result = clean_setting("TEST_SETTING_DUMMY", default_value=50, max_value=100)
        self.assertEqual(result, 50)

    @patch(MODULE_PATH + ".settings")
    def test_default_is_none_needs_required_type(self, mock_settings):
        mock_settings.TEST_SETTING_DUMMY = "invalid type"
        with self.assertRaises(ValueError):
            clean_setting("TEST_SETTING_DUMMY", default_value=None)

    @patch(MODULE_PATH + ".settings")
    def test_when_value_in_choices_return_it(self, mock_settings):
        mock_settings.TEST_SETTING_DUMMY = "bravo"
        result = clean_setting(
            "TEST_SETTING_DUMMY", default_value="alpha", choices=["alpha", "bravo"]
        )
        self.assertEqual(result, "bravo")

    @patch(MODULE_PATH + ".settings")
    def test_when_value_not_in_choices_return_default(self, mock_settings):
        mock_settings.TEST_SETTING_DUMMY = "charlie"
        result = clean_setting(
            "TEST_SETTING_DUMMY", default_value="alpha", choices=["alpha", "bravo"]
        )
        self.assertEqual(result, "alpha")


class TestNoSocketsTestCase(NoSocketsTestCase):
    def test_raises_exception_on_attempted_network_access(self):
        with self.assertRaises(SocketAccessError):
            requests.get("https://www.google.com")
