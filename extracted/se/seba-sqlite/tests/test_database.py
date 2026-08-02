import os
import random
import time
from datetime import datetime
from os.path import join
from unittest import TestCase

import pytest

from seba_sqlite import Database
from seba_sqlite.exceptions import ObjectNotFoundError


from .database_utils import (
    _CONTROLS,
    _EXPERIMENT_NAME,
    _FUNCTIONS,
    _NUMBER_OF_SIMULATIONS,
    _REALIZATION_WEIGHTS,
    _REALIZATIONS,
    load_info_to_db,
    relpath,
    tmpdir
)

_NEW_DATABASE_LOCATION = "dbTestRun"
_DATABASE_LOCATION = ""
_EMTPY_DATABASE_LOCATION = "emptyDB"


def _add_simulations(database):
    """
    Create a simulation
    """
    for inx in range(_NUMBER_OF_SIMULATIONS):
        for real in _REALIZATIONS:
            control_set_id = inx

            for control in _CONTROLS:
                database.add_control_value(
                    control_set_id, control, random.uniform(1.5, 4.9)
                )

            database.add_simulation(
                database.load_realization(name=real).name,
                control_set_id,
                "{0}_{1}_{2}".format(database.load_last_batch().batch_id, inx, real),
                True,
            )


def _add_sim_result(database):
    """
    Test storing simulation results  with a random result value for each
    simulation for each realization
    """
    for inx in range(_NUMBER_OF_SIMULATIONS):
        for real in _REALIZATIONS:
            for res in _FUNCTIONS:
                sim_name = "{0}_{1}_{2}".format(
                    database.load_last_batch().batch_id, inx, real
                )
                database.add_simulation_result(
                    sim_name, random.uniform(1.5, 4.9), res, 0
                )
                database.set_simulation_ended(sim_name, True)


@pytest.mark.database
class TestDatabase(TestCase):
    @tmpdir(relpath("test_data"))
    def test__full_circle(self):
        database = Database(join(os.getcwd(), _NEW_DATABASE_LOCATION))
        database.add_experiment(name=_EXPERIMENT_NAME, start_time_stamp=time.time())
        database.load_experiment(database.experiment.experiment_id)

        # Test control definitions
        for control in _CONTROLS:
            database.add_control_definition(control, 1, 1, 1)
            control = database.load_control_definition(name=control)
            self.assertIsNotNone(control)
            self.assertListEqual(
                [control.initial_value, control.min_value, control.max_value], [1, 1, 1]
            )

        # Test realization
        for real, weight in zip(_REALIZATIONS, _REALIZATION_WEIGHTS):
            database.add_realization(name=real, weight=weight)
            self.assertEqual(database.load_realization(name=real).name, real)

        # Test functions
        for real in _FUNCTIONS:
            database.add_function(
                name=real,
                function_type="OBJECTIVE",
                weight=1.0,
                normalization=1.0,
                rhs_value=0.0,
                constraint_type=None,
            )
            self.assertEqual(database.load_function(name=real).name, real)

        # Test add the last batch
        control_set_id = 0
        database.add_batch()
        self.assertIsNotNone(database.load_batch(database.load_last_batch().batch_id))

        # Set control values
        for control in _CONTROLS:
            database.add_control_value(
                set_id=control_set_id, control_name=control, value=random.uniform(0, 5)
            )

        _add_simulations(database)
        _add_sim_result(database)

        # Create a new database instance with the same database file
        Database(join(os.getcwd(), _NEW_DATABASE_LOCATION))

    @tmpdir(relpath("test_data"))
    def test__open_non_empty_db(self):
        database = Database(join(os.getcwd(), _DATABASE_LOCATION))
        self.assertIsNotNone(database.experiment)

    @tmpdir(relpath("test_data"))
    def test__load_last_batch_non_empty_db(self):
        database = Database(join(os.getcwd(), _DATABASE_LOCATION))
        self.assertIsNotNone(database.load_last_batch())

    @tmpdir(relpath("test_data"))
    def test__load_last_batch_empty_db(self):
        database = Database(join(os.getcwd(), _EMTPY_DATABASE_LOCATION))
        with self.assertRaises(AttributeError):
            database.load_last_batch()

    @tmpdir(relpath("test_data"))
    def test__load_non_existing_experiment(self):
        """
        Try to load an non existing Experiment from the database
        """
        database = Database(join(os.getcwd(), _DATABASE_LOCATION))
        with self.assertRaises(ObjectNotFoundError):
            database.load_experiment(experiment_id=1929837)

    @tmpdir(relpath("test_data"))
    def test__load_non_existing_experiment_children(self):
        """
        Try to load non existing experiment configurations from the experiment
        """
        database = Database(join(os.getcwd(), _DATABASE_LOCATION))
        with self.assertRaises(ObjectNotFoundError):
            database.load_control_definition("Non existing")
        with self.assertRaises(ObjectNotFoundError):
            database.load_function("Non existing")
        with self.assertRaises(ObjectNotFoundError):
            database.load_realization(name="Absolutely not existing")

    @tmpdir(relpath("test_data"))
    def test__load_non_existing_batch(self):
        """
        Try to load not existing batch
        """
        database = Database(join(os.getcwd(), _DATABASE_LOCATION))
        with self.assertRaises(ObjectNotFoundError):
            database.load_batch(batch_id=485745)

    @tmpdir(relpath("test_data"))
    def test__load_non_existing_simulation(self):
        """
        Try to load not existing simulation
        """
        database = Database(join(os.getcwd(), _DATABASE_LOCATION))
        with self.assertRaises(ObjectNotFoundError):
            database.load_simulation(name="Non existing")

    @tmpdir(relpath("test_data"))
    def test__end_non_existing_simulation(self):
        """
        End a non existing Simulation
        """
        database = Database(join(os.getcwd(), _DATABASE_LOCATION))
        with self.assertRaises(ObjectNotFoundError):
            database.set_simulation_ended("Non Exisiting", False)

    @tmpdir(relpath("test_data"))
    def test__add_result_to_non_existing_simulation(self):
        """
        Add a result to a non existing Simulation
        """
        database = Database(join(os.getcwd(), _DATABASE_LOCATION))
        with self.assertRaises(ObjectNotFoundError):
            database.add_simulation_result(
                "Non Exisiting", random.uniform(1.5, 4.9), "result1", 0
            )

    @tmpdir(relpath("test_data"))
    def test__add_result_with_non_existing_function(self):
        """
        Add a result to a existing Simulation with a non existing function
        """
        database = Database(join(os.getcwd(), _DATABASE_LOCATION))
        with self.assertRaises(ObjectNotFoundError):
            database.add_simulation_result(
                "0_0_realization1", random.uniform(1.5, 4.9), "Non Exisiting", 0
            )

    @tmpdir(relpath("test_data"))
    def test__add_batch_result_with_non_existing_result(self):
        """
        Add a result to a existing Batch with a non existing function
        """
        database = Database(join(os.getcwd(), _DATABASE_LOCATION))

        with self.assertRaises(ObjectNotFoundError):
            database.add_gradient_result(
                gradient_value=random.uniform(1.5, 4.9),
                function_name="NonExisting",
                success=True,
                control_definition_name=_CONTROLS[0],
            )

    @tmpdir(os.getcwd())
    def test_create_db(self):
        db_file_name = "seba.db"
        database = Database(os.getcwd())
        self.assertEqual(os.path.join(os.getcwd(), db_file_name), database.location)

    @tmpdir(os.getcwd())
    def test_open_write_empty_db(self):
        database = Database(os.getcwd())
        self.assertTrue(database.experiment is None)
        database.add_experiment("test_experiment", datetime.now())
        self.assertFalse(database.experiment is None)

    @tmpdir(os.getcwd())
    def test_open_write_existing_db(self):
        database = Database(os.getcwd())
        load_info_to_db(database, **{"Experiment": ["Test experiment"]})
        self.assertTrue(os.path.isfile(database.location))
        self.assertIsNotNone(database.experiment)
        existing_experiment = database.experiment.experiment_id
        database.add_experiment("New experiment", datetime.now())
        self.assertNotEqual(
            existing_experiment, database.load_experiment().experiment_id
        )
