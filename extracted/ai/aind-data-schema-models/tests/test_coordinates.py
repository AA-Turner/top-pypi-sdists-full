"""Test coordinate_enums"""

import unittest

from aind_data_schema_models.coordinates import AxisName


class UnitsTests(unittest.TestCase):
    """Class for testing coordinate_enums"""

    def test_units(self):
        """Tests creation of a SizeVal object"""

        self.assertIsNotNone(AxisName.X)


if __name__ == "__main__":
    unittest.main()
