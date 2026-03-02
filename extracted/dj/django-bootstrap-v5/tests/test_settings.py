from django.test import TestCase, override_settings

from bootstrap5.bootstrap import get_bootstrap_setting


class SettingsTest(TestCase):
    def test_get_bootstrap_setting(self):
        self.assertIsNone(get_bootstrap_setting("SETTING_DOES_NOT_EXIST"))
        self.assertEqual("not none", get_bootstrap_setting("SETTING_DOES_NOT_EXIST", "not none"))
        # Override a setting
        with self.settings(BOOTSTRAP5={"SETTING_DOES_NOT_EXIST": "exists now"}):
            self.assertEqual(get_bootstrap_setting("SETTING_DOES_NOT_EXIST"), "exists now")

