#!/usr/bin/env python3
"""
Test for forgiving enums feature (DX-40).

This script tests that the SDK gracefully handles unknown enum values instead of crashing.

How it works:
1. Calls getUser with real credentials to see what entitlements you have
2. Removes one of those entitlement values from the installed schema enum
3. Calls getUser again to verify it doesn't crash (forgiving behavior)

Usage:
    python utils/test_forgiving_enums.py [VERSION]

Arguments:
    VERSION: Optional. The pycarlo version to test (e.g., "0.12.0b1", "0.11.27")
             If not provided, uses the currently installed version.

Examples:
    # Test the beta version with forgiving enums
    python utils/test_forgiving_enums.py 0.12.0b1

    # Test the old version (should fail - proves the fix works)
    python utils/test_forgiving_enums.py 0.11.27

    # Test currently installed version
    python utils/test_forgiving_enums.py

Prerequisites:
    Set your credentials via MCD_DEFAULT_API_ID and MCD_DEFAULT_API_TOKEN env vars,
    or use ~/.mcd/profiles.ini (created via 'montecarlo configure')
"""

import logging
import os
import re
import sys
from typing import Tuple

from pycarlo.core import Client, Query

# Set up logging to see the warning messages
logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")


def parse_version(version_str: str) -> Tuple[int, int, int]:
    """Parse version string like '0.12.0b1' or '0.11.27' into (major, minor, patch)."""
    # Remove any pre-release suffix (b1, rc1, etc.)
    version_str = re.sub(r"[a-z].*$", "", version_str)
    parts = version_str.split(".")
    return (int(parts[0]), int(parts[1]), int(parts[2]) if len(parts) > 2 else 0)


def find_schema_file() -> str:
    """Find the installed pycarlo schema.py file."""
    import pycarlo.lib.schema

    return pycarlo.lib.schema.__file__


def get_user_entitlements(client: Client) -> Query:
    """
    Fetch real user entitlements from the API using sgqlc Operation.

    IMPORTANT: We must use Query operation (not raw string query) to trigger
    enum deserialization. Raw string queries just return Box objects without
    going through enum type conversion.
    """
    query = Query()
    query.get_user.email()
    query.get_user.account.name()
    query.get_user.account.entitlements()  # This will deserialize through EntitlementTypes enum

    result = client(query)
    return result


def remove_enum_value_from_schema(schema_file: str, enum_class: str, value_to_remove: str) -> bool:
    """
    Remove a specific value from an enum in the schema file.

    This simulates what happens when the SDK is out of date and doesn't
    know about a new enum value that the API returns.
    """
    print(f"\n📝 Modifying schema file: {schema_file}")
    print(f"   Removing '{value_to_remove}' from {enum_class}.__choices__")

    with open(schema_file, "r") as f:
        content = f.read()

    # Find the enum class definition and its __choices__ tuple
    # Pattern: class EntitlementTypes(sgqlc.types.Enum):
    #              __choices__ = ('SSO', 'NOTIFICATIONS', ...)
    pattern = rf"(class {enum_class}\([^)]+\):.*?__choices__ = \()([^)]+)(\))"

    def remove_value(match: re.Match[str]) -> str:
        prefix = match.group(1)
        choices = match.group(2)
        suffix = match.group(3)

        # Remove the value from the choices tuple
        # Handle both 'VALUE' and "VALUE" formats
        choices_modified = re.sub(rf"['\"]?{value_to_remove}['\"]?,?\s*", "", choices)
        # Clean up any double commas or trailing commas
        choices_modified = re.sub(r",\s*,", ",", choices_modified)
        choices_modified = re.sub(r",\s*\)", ")", choices_modified)

        return prefix + choices_modified + suffix

    content_modified = re.sub(pattern, remove_value, content, flags=re.DOTALL)

    if content == content_modified:
        print(f"   ⚠️  WARNING: Could not find/remove '{value_to_remove}' from schema")
        return False

    # Write the modified content back
    with open(schema_file, "w") as f:
        f.write(content_modified)

    print(f"   ✅ Removed '{value_to_remove}' from schema")
    return True


def reload_schema() -> None:
    """Reload the schema module to pick up changes."""
    import importlib

    import pycarlo.lib.schema

    importlib.reload(pycarlo.lib.schema)
    print("   ✅ Reloaded schema module")


if __name__ == "__main__":
    # Get version from command line argument if provided
    version = sys.argv[1] if len(sys.argv) > 1 else "unknown"

    print("=" * 70)
    print(f"Testing Forgiving Enums Feature - pycarlo v{version}")
    print("=" * 70)

    # Step 1: Get real entitlements
    print("\n📡 Step 1: Fetching your real entitlements from the API...")
    print("-" * 70)

    try:
        client = Client()
        result = get_user_entitlements(client)

        email = result.get_user.email
        account_name = result.get_user.account.name
        entitlements = result.get_user.account.entitlements  # This is a list of enum strings

        print(f"✅ User: {email}")
        print(f"✅ Account: {account_name}")
        print("✅ Entitlements found:")

        # entitlements is already a list of strings (enum values)
        for value in entitlements:
            print(f"   - {value}")

        if not entitlements:
            print("\n❌ No entitlements found. Cannot proceed with test.")
            sys.exit(1)

        # Pick the first entitlement to remove
        value_to_remove: str = str(entitlements[0])

    except Exception as e:
        print(f"\n❌ Failed to fetch user data: {type(e).__name__}: {e}")
        print("\nMake sure you have credentials configured:")
        print("  - Set MCD_DEFAULT_API_ID and MCD_DEFAULT_API_TOKEN env vars, or")
        print("  - Use ~/.mcd/profiles.ini (created via 'montecarlo configure')")
        sys.exit(1)

    # Step 2: Modify the schema to remove one entitlement
    print(f"\n🔧 Step 2: Removing '{value_to_remove}' from the schema...")
    print("-" * 70)

    schema_file = find_schema_file()
    backup_file = schema_file + ".backup"

    # Backup the original schema
    import shutil

    shutil.copy2(schema_file, backup_file)
    print(f"✅ Backed up schema to: {backup_file}")

    try:
        if not remove_enum_value_from_schema(schema_file, "EntitlementTypes", value_to_remove):
            print("\n⚠️  Could not modify schema. Restoring backup...")
            shutil.copy2(backup_file, schema_file)
            sys.exit(1)

        reload_schema()

        # Verify the enum was actually modified
        from pycarlo.lib.schema import EntitlementTypes

        print("\n   📋 Current EntitlementTypes values after reload:")
        for choice in EntitlementTypes.__choices__:
            print(f"      - {choice}")

        # Verify the removed value is not in the enum
        if value_to_remove not in EntitlementTypes.__choices__:
            print(f"\n   ✅ Confirmed: '{value_to_remove}' is NOT in the enum anymore!")
        else:
            print(f"\n   ❌ ERROR: '{value_to_remove}' is still in the enum!")
            raise Exception(f"Failed to remove '{value_to_remove}' from schema")

        # Step 3: Call getUser again with the modified schema
        print(f"\n🧪 Step 3: Calling getUser again (schema missing '{value_to_remove}')...")
        print("-" * 70)

        # Create a new client to pick up the reloaded schema
        client2 = Client()
        result2 = get_user_entitlements(client2)

        print("✅ SUCCESS: Query completed without crashing!")
        print("\nEntitlements received:")
        # entitlements is a list of enum strings
        for value in result2.get_user.account.entitlements:
            is_unknown = value == value_to_remove
            marker = " ⚠️  (was removed from schema!)" if is_unknown else ""
            print(f"   - {value}{marker}")

        print("\n" + "=" * 70)
        print("🎉 TEST PASSED!")
        print(
            f"   pycarlo v{version} handled the unknown enum value '{value_to_remove}' gracefully."
        )
        print("   This proves the forgiving enums feature is working!")
        print("   Check above for a WARNING log about the unknown enum value.")
        print("=" * 70)

    except Exception as e:
        # Parse version to determine if failure is expected
        try:
            parsed_version = parse_version(version)
            expected_to_fail = parsed_version < (0, 12, 0)
        except Exception:
            expected_to_fail = False  # Can't parse version, don't assume

        # Extract the key error message (the part about enum not accepting the value)
        error_str = str(e)
        # Look for the pattern "EntitlementTypes does not accept value X"
        enum_error_match = re.search(r"(EntitlementTypes does not accept value [A-Z_]+)", error_str)

        status_icon = "✅" if expected_to_fail else "❌"
        status_text = "PASSED" if expected_to_fail else "FAILED"
        print(f"\n{status_icon} TEST {status_text}: {type(e).__name__}")

        if expected_to_fail:
            print(
                f"   pycarlo v{version} crashed as expected (versions < 0.12.0 don't have the fix)."
            )
            print("   This proves the forgiving enums feature is needed!")

            # Verify the error is specifically about the enum rejection
            if enum_error_match and value_to_remove in enum_error_match.group(1):
                print(f"\n   ✅ Verified enum rejection: {enum_error_match.group(1)}")
            else:
                print("\n   ⚠️  Unexpected error (not the expected enum rejection)")

            print(f"\n   Full error: {error_str}")
        else:
            print(
                f"   pycarlo v{version} crashed unexpectedly when encountering "
                f"the removed enum value."
            )
            print("   The forgiving enums feature should have prevented this!")
            print(f"\n   Full error: {error_str}")

        print("=" * 70)

        # If we expected it to fail and it did, that's actually a pass
        if not expected_to_fail:
            raise

    finally:
        # Restore the original schema
        print("\n🔄 Restoring original schema...")
        shutil.copy2(backup_file, schema_file)
        os.remove(backup_file)
        print("✅ Schema restored")
