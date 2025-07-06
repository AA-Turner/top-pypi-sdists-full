"""Test utils.units"""

import unittest
from decimal import Decimal
from typing import TypeVar

from aind_data_schema_models.units import SizeUnit

ScalarType = TypeVar("ScalarType", Decimal, int)


class UnitsTests(unittest.TestCase):
    """Class for testing Utils.Units"""

    def test_units(self):
        """Tests creation of a SizeVal object"""

        self.assertIsNotNone(SizeUnit.MM)


if __name__ == "__main__":
    unittest.main()
