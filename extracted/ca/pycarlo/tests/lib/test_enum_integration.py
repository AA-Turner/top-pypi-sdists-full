"""
Integration tests for the custom Enum with the actual generated schema.

These tests verify that the SDK works correctly with the current schema,
even though it still uses sgqlc.types.Enum (not yet regenerated).
"""

import logging
from unittest import TestCase

from pycarlo.lib.schema import EntitlementTypes


class TestEnumIntegration(TestCase):
    """Test that our custom Enum works with actual schema enums."""

    def test_entitlement_types_known_values(self):
        """Test that known EntitlementTypes values work correctly."""
        # These are known values in the current schema
        sso = EntitlementTypes("SSO")
        self.assertEqual(sso, "SSO")
        self.assertEqual(sso, EntitlementTypes.SSO)

        multi_workspace = EntitlementTypes("MULTI_WORKSPACE")
        self.assertEqual(multi_workspace, "MULTI_WORKSPACE")
        self.assertEqual(multi_workspace, EntitlementTypes.MULTI_WORKSPACE)

    def test_entitlement_types_in_operator(self):
        """Test that the 'in' operator works with EntitlementTypes."""
        # Use __choices__ for type-safe assertions
        self.assertIn("SSO", EntitlementTypes.__choices__)
        self.assertIn("MULTI_WORKSPACE", EntitlementTypes.__choices__)
        self.assertIn("AUTH_GROUP_CONNECTION_RESTRICTION", EntitlementTypes.__choices__)

        # Unknown value should not be in the enum
        self.assertNotIn("UNKNOWN_FUTURE_VALUE", EntitlementTypes.__choices__)

    def test_entitlement_types_list_operations(self):
        """Test list operations with EntitlementTypes."""
        entitlements = [
            EntitlementTypes("SSO"),
            EntitlementTypes("MULTI_WORKSPACE"),
            EntitlementTypes("AUDIT_LOGGING"),
        ]

        self.assertEqual(len(entitlements), 3)
        self.assertIn("SSO", entitlements)
        self.assertIn("MULTI_WORKSPACE", entitlements)
        self.assertIn("AUDIT_LOGGING", entitlements)

    def test_entitlement_types_filtering(self):
        """Test filtering operations with EntitlementTypes."""
        all_values = ["SSO", "MULTI_WORKSPACE", "AUDIT_LOGGING"]
        entitlements = [EntitlementTypes(v) for v in all_values]

        # Filter for specific value
        sso_only = [e for e in entitlements if e == "SSO"]
        self.assertEqual(len(sso_only), 1)
        self.assertEqual(sso_only[0], "SSO")

        # Filter using enum attribute
        multi_workspace_only = [e for e in entitlements if e == EntitlementTypes.MULTI_WORKSPACE]
        self.assertEqual(len(multi_workspace_only), 1)
        self.assertEqual(multi_workspace_only[0], "MULTI_WORKSPACE")


class TestEnumBackwardCompatibility(TestCase):
    """
    Test backward compatibility scenario.

    The schema has been transformed to use pycarlo.lib.types.Enum,
    so unknown values are now handled gracefully.
    """

    def test_unknown_value_behavior_after_transformation(self):
        """
        Test that unknown values are handled gracefully after transformation.

        With the transformed schema (using pycarlo.lib.types.Enum), unknown values
        are returned as strings with a warning logged.
        """
        # After transformation: returns string with warning
        with self.assertLogs("pycarlo.lib.types", level=logging.WARNING) as log:
            result = EntitlementTypes("UNKNOWN_FUTURE_ENTITLEMENT")

        self.assertEqual(result, "UNKNOWN_FUTURE_ENTITLEMENT")
        self.assertIn("Unknown enum value", log.records[0].message)
        self.assertIn("UNKNOWN_FUTURE_ENTITLEMENT", log.records[0].message)
