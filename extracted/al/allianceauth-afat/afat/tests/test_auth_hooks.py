"""
Tests for auth hooks
"""

# Standard Library
import importlib
import sys
from unittest.mock import patch

# Alliance Auth AFAT
from afat.models import FatsInTimeFilter
from afat.tests import BaseTestCase


class TestResgisterSecureGroupsFilters(BaseTestCase):
    """
    Tests for the register_securegroups_filters function in auth_hooks.py, which conditionally defines filters based on the presence of securegroups.
    """

    def test_filters_defined_when_securegroups_installed_true(self):
        """
        Test that the filters defined for securegroups_installed are defined.

        :return:
        :rtype:
        """

        # Ensure module not loaded so import runs under patched condition
        sys.modules.pop("afat.auth_hooks", None)

        with patch("afat.app_settings.securegroups_installed", return_value=True):
            importlib.import_module("afat.auth_hooks")

        # This needs to be imported here, not globally
        # Alliance Auth AFAT
        import afat.auth_hooks as ah

        self.assertTrue(hasattr(ah, "filters"))
        self.assertEqual(ah.filters(), [FatsInTimeFilter])

        # Cleanup
        sys.modules.pop("afat.auth_hooks", None)

    def test_filters_not_defined_when_securegroups_installed_false(self):
        """
        Test that the filters defined for securegroups_installed are not defined.

        :return:
        :rtype:
        """

        # Ensure module not loaded so import runs under patched condition
        sys.modules.pop("afat.auth_hooks", None)

        with patch("afat.app_settings.securegroups_installed", return_value=False):
            importlib.import_module("afat.auth_hooks")

        # This needs to be imported here, not globally
        # Alliance Auth AFAT
        import afat.auth_hooks as ah

        self.assertFalse(hasattr(ah, "filters"))

        # Cleanup
        sys.modules.pop("afat.auth_hooks", None)
