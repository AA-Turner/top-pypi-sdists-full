"""Tests classes in pid_names"""

import unittest

from aind_data_schema_models.pid_names import PIDName, BaseName


class TestPidNames(unittest.TestCase):
    """Tests classes in pid_names module"""

    def test_instantiate(self):
        """Tests that both classes can be instantiated"""

        name = BaseName(name="Test Name", abbreviation="TN")

        pid_name = PIDName(name="Test PID Name", abbreviation="TPN", registry=name, registry_identifier="1234")

        self.assertIsNotNone(name)
        self.assertIsNotNone(pid_name)
