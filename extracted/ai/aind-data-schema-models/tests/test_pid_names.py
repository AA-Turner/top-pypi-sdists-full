"""Tests classes in pid_names"""

import unittest

from aind_data_schema_models.pid_names import PIDName
from aind_data_schema_models.registries import Registry


class TestPidNames(unittest.TestCase):
    """Tests classes in pid_names module"""

    def test_instantiate(self):
        """Tests that both classes can be instantiated"""

        pid_name = PIDName(name="Test PID Name", abbreviation="TPN", registry=Registry.RRID, registry_identifier="1234")

        self.assertIsNotNone(pid_name)

        pid_name_other_reg = PIDName(
            name="Test PID Name", abbreviation="TPN", registry="Test Registry (TR)", registry_identifier="1234"
        )

        self.assertIsNotNone(pid_name_other_reg)
