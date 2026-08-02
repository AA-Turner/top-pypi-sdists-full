import os
from unittest import TestCase

import pytest

from seba_sqlite import Database
from seba_sqlite.exceptions import ObjectNotFoundError


from .database_utils import (
    _EXPERIMENT_NAME,
    _REALIZATION_WEIGHTS,
    _REALIZATIONS,
    load_info_to_db,
    tmpdir
)


@pytest.mark.database
class TestDatabaseRealization(TestCase):
    @tmpdir(os.getcwd())
    def test_add_realization(self):
        database = Database(os.getcwd())
        load_info_to_db(database, **{"Experiment": [_EXPERIMENT_NAME]})
        realization_name = _REALIZATIONS[0]
        realization_weight = _REALIZATION_WEIGHTS[0]
        with self.assertRaises(ObjectNotFoundError):
            database.load_realization(name=realization_name)
        database.add_realization(realization_name, realization_weight)
        realization = database.load_realization(name=realization_name)
        self.assertIsNotNone(realization)
        self.assertEqual(realization.name, realization_name)
        self.assertEqual(realization.weight, realization_weight)
        self.assertEqual(realization.experiment_id, database.experiment.experiment_id)
        self.assertNotEqual(realization.realization_id, 0)

    @tmpdir(os.getcwd())
    def test_add_multiple_realizations(self):
        database = Database(os.getcwd())
        load_info_to_db(database, **{"Experiment": [_EXPERIMENT_NAME]})
        for name in _REALIZATIONS:
            with self.assertRaises(ObjectNotFoundError):
                database.load_realization(name=name)
        for name, weight in zip(_REALIZATIONS, _REALIZATION_WEIGHTS):
            database.add_realization(name, weight)
        for name, weight in zip(_REALIZATIONS, _REALIZATION_WEIGHTS):
            realization = database.load_realization(name=name)
            self.assertIsNotNone(realization)
            self.assertEqual(realization.name, name)
            self.assertEqual(realization.weight, weight)
            self.assertEqual(
                realization.experiment_id, database.experiment.experiment_id
            )
            self.assertNotEqual(realization.realization_id, 0)

    @tmpdir(os.getcwd())
    def test_get_existing_realization(self):
        database = Database(os.getcwd())
        load_info_to_db(database, **{"Experiment": [_EXPERIMENT_NAME]})
        database.add_realization(_REALIZATIONS[0], _REALIZATION_WEIGHTS[0])
        realization = database.load_realization(name=_REALIZATIONS[0])
        self.assertIsNotNone(realization)
        self.assertEqual(realization.name, _REALIZATIONS[0])
        self.assertEqual(realization.weight, _REALIZATION_WEIGHTS[0])
        self.assertEqual(realization.experiment_id, database.experiment.experiment_id)
        self.assertNotEqual(realization.realization_id, 0)

    @tmpdir(os.getcwd())
    def test_get_non_existing_realization(self):
        database = Database(os.getcwd())
        load_info_to_db(database, **{"Experiment": [_EXPERIMENT_NAME]})
        realization_name = _REALIZATIONS[0]
        with self.assertRaises(ObjectNotFoundError):
            database.load_realization(name=realization_name)

    @tmpdir(os.getcwd())
    def test_get_all_realizations(self):
        database = Database(os.getcwd())
        load_info_to_db(
            database,
            **{
                "Experiment": [_EXPERIMENT_NAME],
                "Realization": zip(_REALIZATIONS, _REALIZATION_WEIGHTS),
            },
        )
        self.assertEqual(len(database.load_realizations()), len(_REALIZATIONS))
