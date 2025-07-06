"""Test licenses"""

import unittest

from aind_data_schema_models.licenses import License


class UnitsTests(unittest.TestCase):
    """Unit tests for the License class"""

    def test_licenses(self):
        """Tests creation of a License object"""

        self.assertIsNotNone(License.CC_BY_40)


if __name__ == "__main__":
    unittest.main()
