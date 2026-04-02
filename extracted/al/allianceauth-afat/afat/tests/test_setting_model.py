"""
Test checks for installed modules we might use
"""

# Alliance Auth AFAT
from afat.models import Setting
from afat.tests import BaseTestCase


class TestSettingModel(BaseTestCase):
    """
    Test the Setting model
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Setup the test class.

        :return:
        :rtype:
        """

        super().setUpClass()

    def test_default_fatlink_expiry_time(self):
        """
        Test default fatlink expiry time.

        :return:
        :rtype:
        """

        self.assertEqual(
            first=Setting.get_setting(Setting.Field.DEFAULT_FATLINK_EXPIRY_TIME),
            second=60,
        )

    def test_get_setting_with_invalid_key(self):
        """
        Test get_setting with an invalid key.

        :return:
        :rtype:
        """

        with self.assertRaises(expected_exception=KeyError):
            Setting.get_setting("invalid_key")

    def test_get_setting_with_valid_key(self):
        """
        Test get_setting with a valid key.

        :return:
        :rtype:
        """

        settings = Setting.get_solo()
        settings.default_fatlink_expiry_time = 75
        settings.save()

        self.assertEqual(
            first=Setting.get_setting(Setting.Field.DEFAULT_FATLINK_EXPIRY_TIME),
            second=75,
        )

    def test_model_str(self):
        """
        Test model string representation.

        :return:
        :rtype:
        """

        settings = Setting.get_solo()

        self.assertEqual(first=str(settings), second="AFAT Settings")
