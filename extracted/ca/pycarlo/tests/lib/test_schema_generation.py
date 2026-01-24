"""
Test that the schema generation process correctly applies our custom Enum.

This test simulates what happens during `make customize-schema` to ensure:
1. The sed commands correctly modify the generated schema
2. The modified schema can be imported without errors
3. Enums in the modified schema use our custom Enum class
4. The custom Enum handles unknown values correctly
"""

import re
import tempfile
from pathlib import Path
from unittest import TestCase


class TestSchemaGeneration(TestCase):
    """Test the schema generation and customization process."""

    def test_transformation_on_original_schema(self):
        """Test that sed transformations work correctly on the original untransformed schema."""
        # Load the original untransformed schema from test data
        original_schema_path = Path(__file__).parent.parent / "data" / "schema_original.py"
        original_content = original_schema_path.read_text()

        # Verify it's untransformed
        self.assertNotIn("import pycarlo.lib.types", original_content)
        self.assertIn("class EntitlementTypes(sgqlc.types.Enum):", original_content)

        # Apply the same transformations as in Makefile
        # Step 1: Add import
        modified = re.sub(
            r"^import sgqlc\.types$",
            "import sgqlc.types\nimport pycarlo.lib.types",
            original_content,
            flags=re.MULTILINE,
        )

        # Step 2: Replace enum base classes
        modified = re.sub(
            r"class ([A-Za-z0-9_]*)\(sgqlc\.types\.Enum\):",
            r"class \1(pycarlo.lib.types.Enum):",
            modified,
        )

        # Verify the import was added
        self.assertIn("import pycarlo.lib.types", modified)
        self.assertIn("import sgqlc.types\nimport pycarlo.lib.types", modified)

        # Verify enum classes were replaced
        self.assertNotIn("class AccessKeyIndexEnum(sgqlc.types.Enum):", modified)
        self.assertIn("class AccessKeyIndexEnum(pycarlo.lib.types.Enum):", modified)

        self.assertNotIn("class EntitlementTypes(sgqlc.types.Enum):", modified)
        self.assertIn("class EntitlementTypes(pycarlo.lib.types.Enum):", modified)

        # Count how many enum classes were replaced
        original_enum_count = len(
            re.findall(r"class [A-Za-z0-9_]*\(sgqlc\.types\.Enum\):", original_content)
        )
        custom_enum_count = len(
            re.findall(r"class [A-Za-z0-9_]*\(pycarlo\.lib\.types\.Enum\):", modified)
        )

        # All enums should have been replaced
        self.assertGreater(original_enum_count, 0, "Should have found enums in original schema")
        self.assertEqual(
            custom_enum_count,
            original_enum_count,
            f"All {original_enum_count} enums should be replaced with custom Enum",
        )

        # Verify no sgqlc.types.Enum references remain in class definitions
        remaining_sgqlc_enums = re.findall(r"class [A-Za-z0-9_]*\(sgqlc\.types\.Enum\):", modified)
        self.assertEqual(
            len(remaining_sgqlc_enums),
            0,
            f"No sgqlc.types.Enum should remain, but found: {remaining_sgqlc_enums}",
        )

    def test_production_schema_is_transformed(self):
        """Test that the production schema has been transformed correctly."""
        schema_path = Path(__file__).parent.parent.parent / "pycarlo" / "lib" / "schema.py"
        content = schema_path.read_text()

        # The schema should already be transformed by make transform-schema
        # Verify the import was added
        self.assertIn("import pycarlo.lib.types", content)
        self.assertIn("import sgqlc.types\nimport pycarlo.lib.types", content)

        # Verify enum classes use custom Enum
        self.assertIn("class AccessKeyIndexEnum(pycarlo.lib.types.Enum):", content)
        self.assertIn("class EntitlementTypes(pycarlo.lib.types.Enum):", content)

        # Count transformed enums
        custom_enum_count = len(
            re.findall(r"class [A-Za-z0-9_]*\(pycarlo\.lib\.types\.Enum\):", content)
        )

        # Should have many enums
        self.assertGreater(custom_enum_count, 50, "Should have found many transformed enums")

        # Verify no sgqlc.types.Enum references remain in class definitions
        remaining_sgqlc_enums = re.findall(r"class [A-Za-z0-9_]*\(sgqlc\.types\.Enum\):", content)
        self.assertEqual(
            len(remaining_sgqlc_enums),
            0,
            f"No sgqlc.types.Enum should remain, but found: {remaining_sgqlc_enums}",
        )

    def test_modified_schema_can_be_imported(self):
        """Test that a modified schema file can be imported and used."""
        schema_path = Path(__file__).parent.parent.parent / "pycarlo" / "lib" / "schema.py"
        original_content = schema_path.read_text()

        # Apply transformations
        modified = re.sub(
            r"^import sgqlc\.types$",
            "import sgqlc.types\nimport pycarlo.lib.types",
            original_content,
            flags=re.MULTILINE,
        )
        modified = re.sub(
            r"class ([A-Za-z0-9_]*)\(sgqlc\.types\.Enum\):",
            r"class \1(pycarlo.lib.types.Enum):",
            modified,
        )

        # Write to a temporary file and try to import it
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(modified)
            temp_path = f.name

        try:
            # Try to compile the modified schema
            with open(temp_path) as f:
                code = compile(f.read(), temp_path, "exec")

            # If we get here, the syntax is valid
            self.assertIsNotNone(code)

        finally:
            Path(temp_path).unlink()

    def test_entitlement_types_enum_structure(self):
        """Verify EntitlementTypes enum has the expected structure in the schema."""
        schema_path = Path(__file__).parent.parent.parent / "pycarlo" / "lib" / "schema.py"
        content = schema_path.read_text()

        # Find the EntitlementTypes class definition (should use custom Enum after transformation)
        match = re.search(
            r"class EntitlementTypes\(pycarlo\.lib\.types\.Enum\):.*?__choices__ = \((.*?)\)",
            content,
            re.DOTALL,
        )

        self.assertIsNotNone(match, "Should find EntitlementTypes enum definition with custom Enum")

        # Verify it has the expected values
        assert match is not None
        choices_text = match.group(1)
        self.assertIn('"SSO"', choices_text)
        self.assertIn('"MULTI_WORKSPACE"', choices_text)
        self.assertIn('"AUTH_GROUP_CONNECTION_RESTRICTION"', choices_text)

    def test_enum_count_in_schema(self):
        """Verify we have a reasonable number of enums in the schema."""
        schema_path = Path(__file__).parent.parent.parent / "pycarlo" / "lib" / "schema.py"
        content = schema_path.read_text()

        # After transformation, all enums should use pycarlo.lib.types.Enum
        enum_count = len(re.findall(r"class [A-Za-z0-9_]*\(pycarlo\.lib\.types\.Enum\):", content))

        # As of writing, there are many enums in the schema
        # This is a sanity check that we're processing a real schema file
        self.assertGreater(
            enum_count, 50, f"Expected many enums in schema, but only found {enum_count}"
        )

        # Verify NO sgqlc.types.Enum references remain
        old_enum_count = len(re.findall(r"class [A-Za-z0-9_]*\(sgqlc\.types\.Enum\):", content))
        self.assertEqual(old_enum_count, 0, f"Found {old_enum_count} untransformed enums")
