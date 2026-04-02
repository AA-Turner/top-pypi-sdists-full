"""
Test checks for installed modules we might use
"""

# Django
from django.test import modify_settings

# Alliance Auth AFAT
from afat.app_settings import (
    fittings_installed,
    securegroups_installed,
    use_fittings_module_for_doctrines,
)
from afat.models import Setting
from afat.tests import BaseTestCase


class TestModulesInstalled(BaseTestCase):
    """
    Test if modules are installed
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Setup the test class

        :return:
        :rtype:
        """

        super().setUpClass()

    @modify_settings(INSTALLED_APPS={"remove": "fittings"})
    def test_for_fittings_installed_when_not_installed(self):
        """
        Test for fittings_installed when it is not installed.

        :return:
        :rtype:
        """

        self.assertFalse(expr=fittings_installed())

    @modify_settings(INSTALLED_APPS={"append": "fittings"})
    def test_for_fittings_installed_when_installed(self):
        """
        Test for fittings_installed when it is installed.

        :return:
        :rtype:
        """

        self.assertTrue(expr=fittings_installed())

    @modify_settings(INSTALLED_APPS={"remove": "securegroups"})
    def test_for_securegroups_installed_when_not_installed(self):
        """
        Test for securegroups when it is not installed.

        :return:
        :rtype:
        """

        self.assertFalse(expr=securegroups_installed())

    @modify_settings(INSTALLED_APPS={"append": "securegroups"})
    def test_for_securegroups_installed_when_installed(self):
        """
        Test for securegroups when it is installed.

        :return:
        :rtype:
        """

        self.assertTrue(expr=securegroups_installed())

    @modify_settings(INSTALLED_APPS={"remove": "fittings"})
    def test_for_use_fittings_module_for_doctrines_when_fittings_not_installed_and_not_enabled(
        self,
    ):
        """
        Test for use_fittings_module_for_doctrines when the fittings module is not installed and not enabled in settings.

        :return:
        :rtype:
        """

        settings = Setting.get_solo()
        settings.use_doctrines_from_fittings_module = False
        settings.save()

        self.assertFalse(
            expr=Setting.get_setting(Setting.Field.USE_DOCTRINES_FROM_FITTINGS_MODULE)
        )
        self.assertFalse(expr=use_fittings_module_for_doctrines())

    @modify_settings(INSTALLED_APPS={"remove": "fittings"})
    def test_for_use_fittings_module_for_doctrines_when_fittings_not_installed_but_enabled(
        self,
    ):
        """
        Test for use_fittings_module_for_doctrines when the fittings module is not installed but enabled in settings.

        :return:
        :rtype:
        """

        settings = Setting.get_solo()
        settings.use_doctrines_from_fittings_module = True
        settings.save()

        self.assertTrue(
            expr=Setting.get_setting(Setting.Field.USE_DOCTRINES_FROM_FITTINGS_MODULE)
        )
        self.assertFalse(expr=use_fittings_module_for_doctrines())

    @modify_settings(INSTALLED_APPS={"append": "fittings"})
    def test_for_use_fittings_module_for_doctrines_when_fittings_installed_and_enabled(
        self,
    ):
        """
        Test for use_fittings_module_for_doctrines when the fittings module is installed and enabled in settings.

        :return:
        :rtype:
        """

        settings = Setting.get_solo()
        settings.use_doctrines_from_fittings_module = True
        settings.save()

        self.assertTrue(
            expr=Setting.get_setting(Setting.Field.USE_DOCTRINES_FROM_FITTINGS_MODULE)
        )
        self.assertTrue(expr=use_fittings_module_for_doctrines())

    @modify_settings(INSTALLED_APPS={"append": "fittings"})
    def test_for_use_fittings_module_for_doctrines_when_fittings_installed_but_not_enabled(
        self,
    ):
        """
        Test for use_fittings_module_for_doctrines when the fittings module is installed but not enabled in settings.

        :return:
        :rtype:
        """

        settings = Setting.get_solo()
        settings.use_doctrines_from_fittings_module = False
        settings.save()

        self.assertFalse(
            expr=Setting.get_setting(Setting.Field.USE_DOCTRINES_FROM_FITTINGS_MODULE)
        )
        self.assertFalse(expr=use_fittings_module_for_doctrines())
