import os
from unittest import TestCase

import pytest

from seba_sqlite import Database


from .database_utils import (
    _CONTROLS,
    _EXPERIMENT_NAME,
    _FUNCTIONS,
    load_info_to_db,
    tmpdir
)


@pytest.mark.database
class TestDatabaseGradientResult(TestCase):
    @tmpdir(os.getcwd())
    def test_add_gradient_result(self):
        database = Database(os.getcwd())
        load_info_to_db(
            database,
            **{
                "Experiment": [_EXPERIMENT_NAME],
                "Function": _FUNCTIONS,
                "Batch": range(10),
                "control_definition": _CONTROLS,
            },
        )
        gradient_results = database.load_gradient_results()
        self.assertEqual(len(gradient_results), 0)

        value = {
            "gradient_value": 15,
            "function_name": _FUNCTIONS[0],
            "success": False,
            "control_definition_name": _CONTROLS[0],
        }
        database.add_gradient_result(**value)
        gradient_results = database.load_gradient_results()
        self.assertEqual(len(gradient_results), 1)

    @tmpdir(os.getcwd())
    def test_load_gradient_results(self):
        database = Database(os.getcwd())
        load_info_to_db(
            database,
            **{
                "Experiment": [_EXPERIMENT_NAME],
                "Function": _FUNCTIONS,
                "Batch": range(10),
                "control_definition": _CONTROLS,
            },
        )
        for func, crt in zip(_FUNCTIONS, _CONTROLS[:3]):
            database.add_gradient_result(
                **{
                    "gradient_value": 15,
                    "function_name": func,
                    "success": False,
                    "control_definition_name": crt,
                }
            )
        gradient_results = database.load_gradient_results()
        self.assertEqual(len(gradient_results), 3)

    @tmpdir(os.getcwd())
    def test_load_gradient_results_by_batch_id(self):
        database = Database(os.getcwd())
        load_info_to_db(
            database,
            **{
                "Experiment": [_EXPERIMENT_NAME],
                "Function": _FUNCTIONS,
                "Batch": range(10),
                "control_definition": _CONTROLS,
            },
        )
        for func, crt in zip(_FUNCTIONS, _CONTROLS[:3]):
            database.add_gradient_result(
                **{
                    "gradient_value": 15,
                    "function_name": func,
                    "success": False,
                    "control_definition_name": crt,
                }
            )
        wrong_batch_id = 0
        correct_batch_id = 9

        result = database.load_gradient_results(batch_id=wrong_batch_id)
        expected_result = []
        self.assertListEqual(expected_result, result)

        result = database.load_gradient_results(batch_id=correct_batch_id)
        for gradient_result in result:
            self.assertTrue(gradient_result.batch_id == correct_batch_id)
