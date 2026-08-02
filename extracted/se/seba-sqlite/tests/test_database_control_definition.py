import os
from unittest import TestCase

import pytest

from seba_sqlite import Database
from seba_sqlite.exceptions import ObjectNotFoundError


from .database_utils import _CONTROLS, _EXPERIMENT_NAME, load_info_to_db, tmpdir


@pytest.mark.database
class TestDatabaseControlDefinition(TestCase):
    @tmpdir(os.getcwd())
    def test_add_control_definition(self):
        database = Database(os.getcwd())
        load_info_to_db(database, **{"Experiment": [_EXPERIMENT_NAME]})
        with self.assertRaises(ObjectNotFoundError):
            database.load_control_definition(name=_CONTROLS[0])
        database.add_control_definition(_CONTROLS[0], 1, 1.0, 1.5)
        new_control_definition = database.load_control_definition(name=_CONTROLS[0])
        self.assertEqual(new_control_definition.name, _CONTROLS[0])
        self.assertEqual(
            new_control_definition.experiment_id, database.experiment.experiment_id
        )
        self.assertNotEqual(new_control_definition.control_id, 0)
        self.assertTrue(
            None
            not in (
                new_control_definition.initial_value,
                new_control_definition.min_value,
                new_control_definition.max_value,
            )
        )

    @tmpdir(os.getcwd())
    def test_add_multiple_control_definitions(self):
        database = Database(os.getcwd())
        load_info_to_db(database, **{"Experiment": [_EXPERIMENT_NAME]})
        for c_name in _CONTROLS:
            with self.assertRaises(ObjectNotFoundError):
                database.load_control_definition(name=c_name)
        for control in _CONTROLS:
            database.add_control_definition(control, 1, 1.0, 1.5)
        for c_name in _CONTROLS:
            self.assertEqual(database.load_control_definition(name=c_name).name, c_name)

    @tmpdir(os.getcwd())
    def test_get_existing_control_definition(self):
        database = Database(os.getcwd())
        load_info_to_db(database, **{"Experiment": [_EXPERIMENT_NAME]})
        for control in _CONTROLS:
            database.add_control_definition(control, 1, 1.0, 1.5)
        self.assertEqual(
            _CONTROLS[2],
            database.load_control_definition(name=_CONTROLS[2]).name,
        )

    @tmpdir(os.getcwd())
    def test_load_control_definition_init(self):
        # load control definitions that doesn't exist in the system
        database = Database(os.getcwd())
        load_info_to_db(database, **{"Experiment": [_EXPERIMENT_NAME]})
        with self.assertRaises(ObjectNotFoundError):
            database.load_control_definition(name=_CONTROLS[0])

    @tmpdir(os.getcwd())
    def test_load_control_definitions(self):
        database = Database(os.getcwd())
        load_info_to_db(
            database,
            **{
                "Experiment": [_EXPERIMENT_NAME],
                "control_definition": _CONTROLS,
            },
        )
        self.assertEqual(len(database.load_control_definitions()), len(_CONTROLS))
