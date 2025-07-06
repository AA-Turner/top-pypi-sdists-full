"""Testing script for the SpecimenProcedureTypes enum"""

import unittest

from aind_data_schema_models.specimen_procedure_types import SpecimenProcedureType


class TestSpecimenProcedureTypes(unittest.TestCase):
    """Tests methods in SpecimenProcedureType class"""

    def test_class_construction(self):
        """Tests enum can be instantiated via string"""

        self.assertEqual(SpecimenProcedureType.DELIPIDATION, SpecimenProcedureType("Delipidation"))


if __name__ == "__main__":
    unittest.main()
