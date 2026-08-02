import os
from datetime import datetime
from unittest import TestCase

import pytest

from seba_sqlite import Database
from seba_sqlite.exceptions import ObjectNotFoundError


from .database_utils import _EXPERIMENT_NAME, tmpdir


@pytest.mark.database
class TestDatabaseExperiment(TestCase):
    @tmpdir(os.getcwd())
    def test_create_experiment(self):
        database = Database(os.getcwd())
        self.assertTrue(database.experiment is None)
        database.add_experiment(_EXPERIMENT_NAME, datetime.now())
        self.assertFalse(database.experiment is None)
        experiment = database.load_experiment()
        self.assertEqual(experiment.name, _EXPERIMENT_NAME)

    @tmpdir(os.getcwd())
    def test_get_existing_experiment(self):
        database = Database(os.getcwd())
        name = "Experiment_1"
        database.add_experiment(name, datetime.now())
        self.assertGreater(database.load_experiment().experiment_id, 0)
        self.assertNotEqual(0, database.load_experiment())
        self.assertEqual(database.load_experiment().name, name)

    @tmpdir(os.getcwd())
    def test_get_non_existing_experiment_empty_db(self):
        database = Database(os.getcwd())
        with self.assertRaises(ObjectNotFoundError):
            database.load_experiment()

    @tmpdir(os.getcwd())
    def test_get_non_existing_experiment_non_empty_db(self):
        database = Database(os.getcwd())
        names = ["Experiment_{}".format(i) for i in range(10)]
        for name in names:
            database.add_experiment(name, datetime.now())
        with self.assertRaises(ObjectNotFoundError):
            database.load_experiment(1400)

    @tmpdir(os.getcwd())
    def test_get_existing_experiment_is_the_latest(self):
        database = Database(os.getcwd())
        names = ["Experiment_{}".format(i) for i in range(10)]
        for name in names:
            database.add_experiment(name, datetime.now())
        self.assertGreater(database.load_experiment().experiment_id, 0)
        self.assertNotEqual(0, database.load_experiment())
        self.assertEqual(database.load_experiment().name, names[-1])

    @tmpdir(os.getcwd())
    def test_set_end_experiment(self):
        database = Database(os.getcwd())
        database.add_experiment("Experiment", datetime.now())
        experiment = database.experiment
        self.assertIsNone(experiment.endtimestamp)
        database.set_experiment_ended(datetime.now())
        experiment = database.experiment
        self.assertIsNotNone(experiment.endtimestamp)
