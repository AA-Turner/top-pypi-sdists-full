import os
from datetime import datetime
from unittest import TestCase

import pytest

from seba_sqlite import Database
from seba_sqlite.exceptions import ObjectNotFoundError


from .database_utils import (
    _EXPERIMENT_NAME,
    _NUMBER_OF_BATCHES,
    load_info_to_db,
    tmpdir
)


@pytest.mark.database
class TestDatabaseBatch(TestCase):
    @tmpdir(os.getcwd())
    def test_add_batch(self):
        database = Database(os.getcwd())
        load_info_to_db(database, **{"Experiment": [_EXPERIMENT_NAME]})
        self.assertEqual(database.get_number_of_batches(), 0)
        database.add_batch()
        self.assertEqual(database.get_number_of_batches(), 1)

    @tmpdir(os.getcwd())
    def test_add_multiple_batches(self):
        database = Database(os.getcwd())
        load_info_to_db(database, **{"Experiment": [_EXPERIMENT_NAME]})
        self.assertEqual(database.get_number_of_batches(), 0)
        for _ in range(_NUMBER_OF_BATCHES):
            database.add_batch()
        self.assertEqual(database.get_number_of_batches(), _NUMBER_OF_BATCHES)

    @tmpdir(os.getcwd())
    def test_load_last_batch(self):
        database = Database(os.getcwd())
        load_info_to_db(database, **{"Experiment": [_EXPERIMENT_NAME]})
        database.add_batch()
        batch = database.load_last_batch()
        self.assertIsNotNone(batch)
        self.assertEqual(batch.experiment_id, database.experiment.experiment_id)

    @tmpdir(os.getcwd())
    def test_load_non_existing_batch(self):
        database = Database(os.getcwd())
        load_info_to_db(database, **{"Experiment": [_EXPERIMENT_NAME]})
        with self.assertRaises(ObjectNotFoundError):
            database.load_batch(150)

    @tmpdir(os.getcwd())
    def test_load_existing_batch_but_not_last(self):
        database = Database(os.getcwd())
        load_info_to_db(database, **{"Experiment": [_EXPERIMENT_NAME]})
        for _ in range(_NUMBER_OF_BATCHES):
            database.add_batch()
        batch_id = database.load_last_batch().batch_id
        for _ in range(10):
            database.add_batch()
        batch = database.load_batch(batch_id)
        self.assertIsNotNone(batch)
        self.assertEqual(batch.batch_id, batch_id)
        self.assertEqual(batch.experiment_id, database.experiment.experiment_id)

    @tmpdir(os.getcwd())
    def test_load_batch_by_batch_id(self):
        database = Database(os.getcwd())
        load_info_to_db(database, **{"Experiment": [_EXPERIMENT_NAME]})
        for _ in range(_NUMBER_OF_BATCHES):
            database.add_batch()
        batch_id = database.load_last_batch().batch_id
        for _ in range(10):
            database.add_batch()
        batch = database.load_batch(batch_id)
        self.assertIsNotNone(batch)
        self.assertEqual(batch.batch_id, batch_id)
        self.assertEqual(batch.experiment_id, database.experiment.experiment_id)
        self.assertEqual(batch.batch_id, _NUMBER_OF_BATCHES - 1)

    @tmpdir(os.getcwd())
    def test_num_batches(self):
        database = Database(os.getcwd())
        load_info_to_db(database, **{"Experiment": [_EXPERIMENT_NAME]})
        self.assertEqual(database.get_number_of_batches(), 0)
        database.add_batch()
        self.assertEqual(database.get_number_of_batches(), 1)

    @tmpdir(os.getcwd())
    def test_set_batch_end(self):
        database = Database(os.getcwd())
        load_info_to_db(database, **{"Experiment": [_EXPERIMENT_NAME]})
        database.add_batch()
        batch = database.load_last_batch()
        self.assertIsNone(batch.end_time_stamp)
        self.assertFalse(batch.success)
        database.set_batch_ended(datetime.now(), True)
        batch = database.load_last_batch()
        self.assertIsNotNone(batch.end_time_stamp)
        self.assertTrue(batch.success)

    @tmpdir(os.getcwd())
    def test_load_all_batches(self):
        database = Database(os.getcwd())
        load_info_to_db(database, **{"Experiment": [_EXPERIMENT_NAME]})
        for _ in range(100):
            database.add_batch()
        num = database.get_number_of_batches()
        self.assertEqual(100, num)
