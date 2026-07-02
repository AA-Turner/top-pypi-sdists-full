from unittest.mock import Mock, patch

from django.test import TestCase

from app_utils.app_settings import clean_setting

MODULE_PATH = "app_utils.app_settings"


@patch(MODULE_PATH + ".settings")
class TestCleanSetting(TestCase):
    def test_default_if_not_set(self, mock_settings):
        # when
        result = clean_setting("TEST_SETTING_DUMMY", 42)
        # then
        self.assertEqual(result, 42)

    def test_default_if_none(self, mock_settings):
        # given
        mock_settings.TEST_SETTING_DUMMY = Mock(spec=None)
        # when
        result = clean_setting("TEST_SETTING_DUMMY", False)
        # then
        self.assertEqual(result, False)

    def test_default_if_not_set_for_none(self, mock_settings):
        # given
        mock_settings.TEST_SETTING_DUMMY = Mock(spec=None)
        # when
        result = clean_setting("TEST_SETTING_DUMMY", None, required_type=int)
        # then
        self.assertEqual(result, None)

    def test_true_stays_true(self, mock_settings):
        # given
        mock_settings.TEST_SETTING_DUMMY = True
        # when
        result = clean_setting("TEST_SETTING_DUMMY", False)
        # then
        self.assertEqual(result, True)

    def test_false_stays_false(self, mock_settings):
        # given
        mock_settings.TEST_SETTING_DUMMY = False
        # when
        result = clean_setting("TEST_SETTING_DUMMY", False)
        # then
        self.assertEqual(result, False)

    def test_default_for_invalid_type_bool(self, mock_settings):
        # given
        mock_settings.TEST_SETTING_DUMMY = "invalid type"
        # when
        result = clean_setting("TEST_SETTING_DUMMY", False)
        # then
        self.assertEqual(result, False)

    def test_default_for_invalid_type_int(self, mock_settings):
        # given
        mock_settings.TEST_SETTING_DUMMY = "invalid type"
        # when
        result = clean_setting("TEST_SETTING_DUMMY", 50)
        # then
        self.assertEqual(result, 50)

    def test_none_allowed_for_type_int(self, mock_settings):
        # given
        mock_settings.TEST_SETTING_DUMMY = None
        # when
        result = clean_setting("TEST_SETTING_DUMMY", 50)
        # then
        self.assertIsNone(result)

    def test_default_if_below_minimum_1(self, mock_settings):
        """when setting is below minimum and default is > minium, then use minimum"""
        # given
        mock_settings.TEST_SETTING_DUMMY = -5
        # when
        result = clean_setting("TEST_SETTING_DUMMY", default_value=50)
        # then
        self.assertEqual(result, 0)

    def test_default_if_below_minimum_2(self, mock_settings):
        """when setting is below minimum, then use minimum"""
        # given
        mock_settings.TEST_SETTING_DUMMY = -50
        # when
        result = clean_setting("TEST_SETTING_DUMMY", default_value=50, min_value=-10)
        # then
        self.assertEqual(result, -10)

    def test_default_if_below_minimum_3(self, mock_settings):
        """when default is None and setting is below minimum, then use minimum"""
        # given
        mock_settings.TEST_SETTING_DUMMY = 10
        # when
        result = clean_setting(
            "TEST_SETTING_DUMMY", default_value=None, required_type=int, min_value=30
        )
        # then
        self.assertEqual(result, 30)

    def test_setting_if_above_maximum(self, mock_settings):
        """when setting is above maximum, then use maximum"""
        # given
        mock_settings.TEST_SETTING_DUMMY = 100
        # when
        result = clean_setting("TEST_SETTING_DUMMY", default_value=10, max_value=50)
        # then
        self.assertEqual(result, 50)

    def test_default_below_minimum(self, mock_settings):
        """when default is below minimum, then raise exception"""
        # given
        mock_settings.TEST_SETTING_DUMMY = 10
        # when/then
        with self.assertRaises(ValueError):
            clean_setting("TEST_SETTING_DUMMY", default_value=10, min_value=50)

    def test_default_above_maximum(self, mock_settings):
        """when default is below minimum, then raise exception"""
        # given
        mock_settings.TEST_SETTING_DUMMY = 10
        # when/then
        with self.assertRaises(ValueError):
            clean_setting("TEST_SETTING_DUMMY", default_value=100, max_value=50)

    def test_default_is_none_needs_required_type(self, mock_settings):
        # given
        mock_settings.TEST_SETTING_DUMMY = "invalid type"
        # when/then
        with self.assertRaises(ValueError):
            clean_setting("TEST_SETTING_DUMMY", default_value=None)

    def test_when_value_in_choices_return_it(self, mock_settings):
        # given
        mock_settings.TEST_SETTING_DUMMY = "bravo"
        # when
        result = clean_setting(
            "TEST_SETTING_DUMMY", default_value="alpha", choices=["alpha", "bravo"]
        )
        # then
        self.assertEqual(result, "bravo")

    def test_when_value_not_in_choices_return_default(self, mock_settings):
        # given
        mock_settings.TEST_SETTING_DUMMY = "charlie"
        # when
        result = clean_setting(
            "TEST_SETTING_DUMMY", default_value="alpha", choices=["alpha", "bravo"]
        )
        # then
        self.assertEqual(result, "alpha")

    def test_abort_when_require_type_is_invalid(self, mock_settings):
        # when/then
        with self.assertRaises(TypeError):
            clean_setting("TEST_SETTING_DUMMY", 42, required_type="invalid")
