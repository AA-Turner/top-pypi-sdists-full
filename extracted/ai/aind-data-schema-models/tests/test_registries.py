"""Tests classes in registries module"""

import unittest

from aind_data_schema_models.registries import Registry


class TestRegistry(unittest.TestCase):
    """Tests methods in Registry class"""

    def test_class_construction(self):
        """Tests enum can be instantiated via string"""

        self.assertEqual(Registry.ADDGENE, "Addgene (ADDGENE)")


if __name__ == "__main__":
    unittest.main()
