"""Brain atlas tests"""

import unittest
from aind_data_schema_models.brain_atlas import CCFv3


class TestCCFStructure(unittest.TestCase):
    """CCFStructure tests"""

    def test_from_id_valid(self):
        """Test from_id method with valid IDs."""
        # Test with a few known IDs
        structure = CCFv3.from_id("709")
        self.assertEqual(structure, CCFv3.VP)
        self.assertEqual(structure.id, "709")
        self.assertEqual(structure.acronym, "VP")

        structure = CCFv3.from_id("718")
        self.assertEqual(structure, CCFv3.VPL)
        self.assertEqual(structure.id, "718")
        self.assertEqual(structure.acronym, "VPL")

    def test_from_id_invalid(self):
        """Test from_id method with invalid ID."""
        with self.assertRaises(ValueError):
            CCFv3.from_id("999999")

        with self.assertRaises(ValueError):
            CCFv3.from_id("")

    def test_by_name_valid(self):
        """Test by_name method with valid names."""
        structure = CCFv3.by_name("Ventral posterior complex of the thalamus")
        self.assertEqual(structure, CCFv3.VP)
        self.assertEqual(structure.name, "Ventral posterior complex of the thalamus")

        structure = CCFv3.by_name("Visual areas")
        self.assertEqual(structure, CCFv3.VIS)
        self.assertEqual(structure.name, "Visual areas")

    def test_by_name_invalid(self):
        """Test by_name method with invalid name."""
        with self.assertRaises(ValueError):
            CCFv3.by_name("Nonexistent Structure")

        with self.assertRaises(ValueError):
            CCFv3.by_name("")

    def test_by_acronym_valid(self):
        """Test by_acronym method with valid acronyms."""
        structure = CCFv3.by_acronym("VP")
        self.assertEqual(structure, CCFv3.VP)
        self.assertEqual(structure.acronym, "VP")

        structure = CCFv3.by_acronym("VIS")
        self.assertEqual(structure, CCFv3.VIS)
        self.assertEqual(structure.acronym, "VIS")

    def test_by_acronym_invalid(self):
        """Test by_acronym method with invalid acronym."""
        with self.assertRaises(ValueError):
            CCFv3.by_acronym("XXX")

        with self.assertRaises(ValueError):
            CCFv3.by_acronym("")

    def test_structure_attributes(self):
        """Test that structure attributes are correctly set."""
        structure = CCFv3.VP
        self.assertEqual(structure.atlas, "CCFv3")
        self.assertEqual(structure.name, "Ventral posterior complex of the thalamus")
        self.assertEqual(structure.acronym, "VP")
        self.assertEqual(structure.id, "709")

    def test_case_sensitivity(self):
        """Test case sensitivity of search methods."""
        # Test case-sensitive name search
        with self.assertRaises(ValueError):
            CCFv3.by_name("ventral posterior complex of the thalamus")

        # Test case-sensitive acronym search
        with self.assertRaises(ValueError):
            CCFv3.by_acronym("vp")

    def test_all_structures_have_required_fields(self):
        """Test that all structures have required fields."""
        for attr_name in dir(CCFv3):
            if not attr_name.startswith("_") and not callable(getattr(CCFv3, attr_name)):
                structure = getattr(CCFv3, attr_name)
                if hasattr(structure, "atlas"):  # Check if it's a BrainStructureModel
                    self.assertEqual(structure.atlas, "CCFv3")
                    self.assertIsNotNone(structure.name)
                    self.assertNotEqual(structure.name, "")
                    self.assertIsNotNone(structure.acronym)
                    self.assertNotEqual(structure.acronym, "")
                    self.assertIsNotNone(structure.id)
                    self.assertNotEqual(structure.id, "")

    def test_unique_ids(self):
        """Test that all structure IDs are unique."""
        ids = []
        for attr_name in dir(CCFv3):
            if not attr_name.startswith("_") and not callable(getattr(CCFv3, attr_name)):
                structure = getattr(CCFv3, attr_name)
                if hasattr(structure, "id"):
                    ids.append(structure.id)

        self.assertEqual(len(ids), len(set(ids)), "Duplicate IDs found")

    def test_unique_acronyms(self):
        """Test that all structure acronyms are unique."""
        acronyms = []
        for attr_name in dir(CCFv3):
            if not attr_name.startswith("_") and not callable(getattr(CCFv3, attr_name)):
                structure = getattr(CCFv3, attr_name)
                if hasattr(structure, "acronym"):
                    acronyms.append(structure.acronym)

        self.assertEqual(len(acronyms), len(set(acronyms)), "Duplicate acronyms found")


if __name__ == "__main__":
    unittest.main()
