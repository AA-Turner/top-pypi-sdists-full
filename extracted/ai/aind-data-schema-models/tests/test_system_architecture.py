"""Testing script for system architecture classes"""

import unittest
from aind_data_schema_models.system_architecture import OperatingSystem, CPUArchitecture


class TestSystemArchitecture(unittest.TestCase):
    """Class for testing Utils.Units"""

    def test_class_construction(self):
        """Tests that OperatingSystem/CPUArchitecture instantiate"""

        self.assertIsNotNone(OperatingSystem.MACOS_SONOMA)
        self.assertIsNotNone(CPUArchitecture.X86_64)
        self.assertEqual(OperatingSystem.DEBIAN_11, OperatingSystem("Debian 11"))
        self.assertEqual(CPUArchitecture.ARM, CPUArchitecture("Arm32"))
