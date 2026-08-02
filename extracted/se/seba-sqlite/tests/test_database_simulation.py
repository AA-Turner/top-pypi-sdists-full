import os
import random
from unittest import TestCase

import pytest

from seba_sqlite import Database
from seba_sqlite.exceptions import ObjectNotFoundError


from .database_utils import (
    _CONTROLS,
    _EXISTING_SIMULATION_NAME,
    _EXPERIMENT_NAME,
    _FUNCTIONS,
    _REALIZATION_WEIGHTS,
    _REALIZATIONS,
    load_info_to_db,
    tmpdir
)


@pytest.mark.database
class TestDatabaseSimulation(TestCase):
    @tmpdir(os.getcwd())
    def test_add_multiple_simulation(self):
        database = Database(os.getcwd())
        load_info_to_db(
            database,
            **{
                "Experiment": [_EXPERIMENT_NAME],
                "Function": _FUNCTIONS,
                "Batch": [0],
                "control_definition": _CONTROLS,
                "Realization": zip(_REALIZATIONS, _REALIZATION_WEIGHTS),
            },
        )
        sim_names = ["Simulation_{}".format(i) for i in range(5)]
        for name in sim_names:
            with self.assertRaises(ObjectNotFoundError):
                database.load_simulation(name=name)
        values = [
            {
                "realization_name": random.choice(_REALIZATIONS),
                "set_id": x,
                "sim_name": name,
                "is_gradient": random.choice([True, False]),
            }
            for x, name in enumerate(sim_names)
        ]
        for value in values:
            database.add_simulation(**value)
        for name in sim_names:
            simulation = database.load_simulation(name=name)
            self.assertIsNotNone(simulation)
            self.assertNotEqual(simulation.simulation_id, 0)
            self.assertNotEqual(simulation.batch_id, 1)
            self.assertNotEqual(simulation.realization_id, 0)

    @tmpdir(os.getcwd())
    def test_get_inexisting_simulation(self):
        database = Database(os.getcwd())
        load_info_to_db(
            database,
            **{
                "Experiment": [_EXPERIMENT_NAME],
                "Function": _FUNCTIONS,
                "Batch": [0],
                "control_definition": _CONTROLS,
                "Realization": zip(_REALIZATIONS, _REALIZATION_WEIGHTS),
            },
        )
        with self.assertRaises(ObjectNotFoundError):
            database.load_simulation(name="Inexisting Simulation")

    @tmpdir(os.getcwd())
    def test_get_existing_simulation(self):
        database = Database(os.getcwd())
        load_info_to_db(
            database,
            **{
                "Experiment": [_EXPERIMENT_NAME],
                "Function": _FUNCTIONS,
                "Batch": [0],
                "control_definition": _CONTROLS,
                "Realization": zip(_REALIZATIONS, _REALIZATION_WEIGHTS),
                "Simulation": [[_REALIZATIONS[0], 0, _EXISTING_SIMULATION_NAME]],
                "dict_order": ["Function", "Batch", "control_definition", "Simulation"],
            },
        )
        simulation = database.load_simulation(name=_EXISTING_SIMULATION_NAME)
        self.assertIsNotNone(simulation)

    @tmpdir(os.getcwd())
    def test_set_end_simulation(self):
        """
        Sets the end time for a simulation along if it is a success or not.
        """
        database = Database(os.getcwd())
        load_info_to_db(
            database,
            **{
                "Experiment": [_EXPERIMENT_NAME],
                "Function": _FUNCTIONS,
                "Batch": [0],
                "control_definition": _CONTROLS,
                "Realization": zip(_REALIZATIONS, _REALIZATION_WEIGHTS),
                "Simulation": [[_REALIZATIONS[0], 0, _EXISTING_SIMULATION_NAME]],
                "dict_order": ["Function", "Batch", "control_definition", "Simulation"],
            },
        )
        simulation = database.load_simulation(name=_EXISTING_SIMULATION_NAME)
        self.assertIsNone(simulation.end_time_stamp)
        self.assertEqual(simulation.success, 1)
        database.set_simulation_ended(
            sim_name=_EXISTING_SIMULATION_NAME,
            success=False,
        )
        simulation = database.load_simulation(name=_EXISTING_SIMULATION_NAME)
        self.assertIsNotNone(simulation.success)
        self.assertIsNotNone(simulation.end_time_stamp)
        reload_simulation = database.load_simulation(name=_EXISTING_SIMULATION_NAME)
        self.assertEqual(reload_simulation.success, False)
        self.assertIsNotNone(reload_simulation.end_time_stamp)

    @tmpdir(os.getcwd())
    def test_get_simulations(self):
        database = Database(os.getcwd())
        load_info_to_db(
            database,
            **{
                "Experiment": [_EXPERIMENT_NAME],
                "Function": _FUNCTIONS,
                "Batch": [0],
                "control_definition": _CONTROLS,
                "Realization": zip(_REALIZATIONS, _REALIZATION_WEIGHTS),
                "Simulation": zip(
                    _REALIZATIONS[:10],
                    range(10),
                    ["simulation_{}".format(i) for i in range(1, 11)],
                ),
                "dict_order": ["Function", "Batch", "control_definition", "Simulation"],
            },
        )
        simulations = database.load_simulations()
        self.assertEqual(len(simulations), 10)
