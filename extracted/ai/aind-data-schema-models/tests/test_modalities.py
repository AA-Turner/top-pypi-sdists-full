"""Tests classes in modalities module"""

import unittest

from aind_data_schema_models.modalities import Modality


class TestModality(unittest.TestCase):
    """Tests methods in Modality class"""

    def test_from_abbreviation(self):
        """Tests modality can be constructed from abbreviation"""

        self.assertEqual(Modality.ECEPHYS, Modality.from_abbreviation("ecephys"))


if __name__ == "__main__":
    unittest.main()
