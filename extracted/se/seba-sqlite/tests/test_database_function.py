import os
import random
from unittest import TestCase

import pytest

from seba_sqlite import Database, Function
from seba_sqlite.exceptions import ObjectNotFoundError


from .database_utils import (
    _EXISTING_FUNCTION_NAME,
    _EXPERIMENT_NAME,
    _FUNCTIONS,
    load_info_to_db,
    tmpdir
)


@pytest.mark.database
class TestDatabaseFunction(TestCase):
    @tmpdir(os.getcwd())
    def test_add_function(self):
        database = Database(os.getcwd())
        load_info_to_db(database, **{"Experiment": [_EXPERIMENT_NAME]})
        values = {
            "name": _FUNCTIONS[0],
            "function_type": "OBJECTIVE",
            "weight": 1.1,
            "normalization": 1.2,
            "rhs_value": 0.1,
            "constraint_type": None,
        }
        with self.assertRaises(ObjectNotFoundError):
            database.load_function(values["name"])
        database.add_function(**values)
        function = database.load_function(values["name"])
        self.assertIsNotNone(function)
        self.assertNotEqual(function.function_id, 0)
        self.assertEqual(function.experimentid, database.experiment.experiment_id)
        self.assertEqual(function.name, values["name"])
        self.assertEqual(function.weight, values["weight"])
        self.assertEqual(function.normalization, values["normalization"])
        self.assertEqual(function.function_type, values["function_type"])
        self.assertEqual(function.rhs_value, values["rhs_value"])
        self.assertEqual(function.constraint_type, values["constraint_type"])

    @tmpdir(os.getcwd())
    def test_add_multiple_functions(self):
        database = Database(os.getcwd())
        load_info_to_db(database, **{"Experiment": [_EXPERIMENT_NAME]})
        function_type_sequence = ["OBJECTIVE", "RANDOM", "UNDEFINED"]
        values = [
            {
                "name": name,
                "function_type": random.choice(function_type_sequence),
                "weight": random.uniform(1.0, 2.0),
                "normalization": random.uniform(1.0, 2.0),
                "rhs_value": random.uniform(-0.5, 0.5),
                "constraint_type": None,
            }
            for name in _FUNCTIONS
        ]
        for elem in values:
            with self.assertRaises(ObjectNotFoundError):
                database.load_function(elem["name"])
        for value in values:
            database.add_function(**value)
        for elem in values:
            function = database.load_function(elem["name"])
            self.assertIsNotNone(function)
            self.assertNotEqual(function.function_id, 0)
            self.assertEqual(function.experimentid, database.experiment.experiment_id)
            self.assertEqual(function.name, elem["name"])
            self.assertEqual(function.weight, elem["weight"])
            self.assertEqual(function.normalization, elem["normalization"])
            self.assertEqual(function.function_type, elem["function_type"])
            self.assertEqual(function.rhs_value, elem["rhs_value"])
            self.assertEqual(function.constraint_type, elem["constraint_type"])

    @tmpdir(os.getcwd())
    def test_get_existing_function(self):
        database = Database(os.getcwd())
        load_info_to_db(
            database,
            **{
                "Experiment": [_EXPERIMENT_NAME],
                "Function": [_EXISTING_FUNCTION_NAME],
            },
        )
        function = database.load_function(_EXISTING_FUNCTION_NAME)
        self.assertIsNotNone(function)
        self.assertNotEqual(function.function_id, 0)
        self.assertEqual(function.name, _EXISTING_FUNCTION_NAME)

    @tmpdir(os.getcwd())
    def test_get_non_existing_function(self):
        database = Database(os.getcwd())
        load_info_to_db(database, **{"Experiment": [_EXPERIMENT_NAME]})
        with self.assertRaises(ObjectNotFoundError):
            database.load_function("Inexistent Name")

    @tmpdir(os.getcwd())
    def test_get_constraint_functions(self):
        database = Database(os.getcwd())
        load_info_to_db(database, **{"Experiment": [_EXPERIMENT_NAME]})
        values = [
            {
                "name": name,
                "function_type": "CONSTRAINT",
                "weight": random.uniform(1.0, 2.0),
                "normalization": random.uniform(1.0, 2.0),
                "rhs_value": random.uniform(-0.5, 0.5),
                "constraint_type": None,
            }
            for name in _FUNCTIONS
        ]
        for value in values:
            database.add_function(**value)
        constraints = database.load_functions(
            function_type=Function.FUNCTION_CONSTRAINT_TYPE
        )
        self.assertEqual(len(constraints), len(_FUNCTIONS))

    @tmpdir(os.getcwd())
    def test_get_objective_functions(self):
        database = Database(os.getcwd())
        load_info_to_db(database, **{"Experiment": [_EXPERIMENT_NAME]})
        values = [
            {
                "name": name,
                "function_type": "OBJECTIVE",
                "weight": random.uniform(1.0, 2.0),
                "normalization": random.uniform(1.0, 2.0),
                "rhs_value": random.uniform(-0.5, 0.5),
                "constraint_type": None,
            }
            for name in _FUNCTIONS
        ]
        for value in values:
            database.add_function(**value)
        objectives = database.load_functions(
            function_type=Function.FUNCTION_OBJECTIVE_TYPE
        )
        self.assertEqual(len(objectives), len(_FUNCTIONS))

    @tmpdir(os.getcwd())
    def test_get_all_functions(self):
        database = Database(os.getcwd())
        load_info_to_db(
            database, **{"Experiment": [_EXPERIMENT_NAME], "Function": _FUNCTIONS}
        )
        objectives = database.load_functions()
        self.assertEqual(len(objectives), len(_FUNCTIONS))
