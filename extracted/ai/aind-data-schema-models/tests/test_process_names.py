"""Tests classes in process_names module"""

import unittest

from aind_data_schema_models.process_names import ProcessName


class TestProcessName(unittest.TestCase):
    """Tests methods in ProcessName class"""

    def test_class_construction(self):
        """Tests enum can be instantiated via string"""

        self.assertEqual(ProcessName.COMPRESSION, ProcessName("Compression"))


if __name__ == "__main__":
    unittest.main()
