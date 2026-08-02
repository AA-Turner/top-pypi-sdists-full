import os
import random
from unittest import TestCase

import pytest

from seba_sqlite import Database


from .database_utils import (
    _CONTROLS,
    _EXPERIMENT_NAME,
    _REALIZATION_WEIGHTS,
    _REALIZATIONS,
    load_info_to_db,
    tmpdir
)


@pytest.mark.database
class TestDatabaseControlValue(TestCase):
    @tmpdir(os.getcwd())
    def test_add_control_value(self):
        set_id = 0
        database = Database(os.getcwd())
        load_info_to_db(
            database,
            **{
                "Experiment": [_EXPERIMENT_NAME],
                "control_definition": _CONTROLS,
            },
        )

        control_value = database.load_control_values(set_id=set_id)
        self.assertFalse(bool(control_value))
        database.add_control_value(set_id, _CONTROLS[0], 15)
        new_control_value = database.load_control_values(set_id=0)
        self.assertTrue(bool(new_control_value))

    @tmpdir(os.getcwd())
    def test_load_control_value_by_batch_num(self):
        database = Database(os.getcwd())
        load_info_to_db(
            database,
            **{
                "Experiment": [_EXPERIMENT_NAME],
                "control_definition": _CONTROLS,
                "Realization": zip(_REALIZATIONS, _REALIZATION_WEIGHTS),
                "Batch": [0],
            },
        )
        database.add_control_value(0, _CONTROLS[0], 15)

        value = {
            "realization_name": _REALIZATIONS[0],
            "set_id": 0,
            "sim_name": "simulation name",
            "is_gradient": True,
        }
        database.add_simulation(**value)
        batch_number = database.load_last_batch().batch_id
        cntrl_val = database.load_control_values(batch_id=batch_number)
        self.assertEqual(len(cntrl_val), 1)
        self.assertEqual(len(cntrl_val[0]), 1)
        self.assertEqual(len(cntrl_val[0][0]), 2)

    @tmpdir(os.getcwd())
    def test_load_control_value_by_set_id(self):
        database = Database(os.getcwd())
        load_info_to_db(
            database,
            **{
                "Experiment": [_EXPERIMENT_NAME],
                "control_definition": _CONTROLS,
            },
        )
        control_value = database.load_control_values(set_id=0)
        self.assertFalse(bool(control_value))

    @tmpdir(os.getcwd())
    def test_load_control_values(self):
        database = Database(os.getcwd())
        load_info_to_db(
            database,
            **{
                "Experiment": [_EXPERIMENT_NAME],
                "control_definition": _CONTROLS,
            },
        )
        for set_id, control_name in zip(range(10), _CONTROLS[:10]):
            database.add_control_value(set_id, control_name, random.randint(1, 100))
        control_values = database.load_control_values()
        self.assertEqual(len(control_values), 10)
