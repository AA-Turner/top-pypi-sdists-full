"""Tests classes in atlas module"""

import unittest

from aind_data_schema_models.atlas import AtlasName


class TestAtlasName(unittest.TestCase):
    """Tests methods in AtlasName class"""

    def test_class_construction(self):
        """Tests enum can be instantiated via string"""

        self.assertEqual(AtlasName.CCF, AtlasName("CCF"))


if __name__ == "__main__":
    unittest.main()
