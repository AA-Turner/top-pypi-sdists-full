import os
import random
from unittest import TestCase

import pytest

from seba_sqlite import Database


from .database_utils import (
    _CONTROLS,
    _EXISTING_SIMULATION_NAME,
    _EXPERIMENT_NAME,
    _FUNCTIONS,
    _NUMBER_OF_BATCHES,
    _REALIZATION_WEIGHTS,
    _REALIZATIONS,
    load_info_to_db,
    tmp
)


def _get_database():
    database = Database(os.getcwd())
    load_info_to_db(
        database,
        **{
            "Experiment": [_EXPERIMENT_NAME],
            "Function": _FUNCTIONS,
            "Batch": range(_NUMBER_OF_BATCHES),
            "control_definition": _CONTROLS,
            "Realization": zip(_REALIZATIONS, _REALIZATION_WEIGHTS),
            "Simulation": [[_REALIZATIONS[0], 0, _EXISTING_SIMULATION_NAME]],
            "dict_order": ["Function", "Batch", "control_definition", "Simulation"],
        },
    )
    return database


@pytest.mark.database
class TestDatabaseCalculationResult(TestCase):
    def test_add_calculation_result(self):
        with tmp():
            database = _get_database()
            set_id = 12345
            value = {
                "set_id": set_id,
                "object_function_value": random.uniform(0.0, 2.0),
                "merit_function_value": random.uniform(0.0, 200.0),
                "improved_flag": False,
            }
            database.add_calculation_result(**value)

            value = {
                "set_id": set_id + 1,
                "object_function_value": random.uniform(0.0, 2.0),
                "merit_function_value": random.uniform(0.0, 200.0),
                "improved_flag": False,
            }
            database.add_calculation_result(**value)
            eval_results = database.load_calculation_results()
            self.assertEqual(len(eval_results), 2)
            self.assertEqual(
                eval_results[1].merit_function_value, value["merit_function_value"]
            )
            self.assertEqual(
                eval_results[1].object_function_value, value["object_function_value"]
            )

    def test_update_calculation_result_merit(self):
        data = [
            {"obj": -38.094, "iter": 0, "value": None},
            {"obj": -34.9859, "iter": 1, "value": 30},
            {"obj": -12.5423, "iter": 2, "value": 18},
            {"obj": -20.3813, "iter": 3, "value": 13},
            {"obj": -18.3068, "iter": 4, "value": 10},
            {"obj": -13.2031, "iter": 5, "value": 3},
            # value increasing should result in improved_flag=False
            {"obj": -11.2027, "iter": 6, "value": 4},
            {"obj": -6.96819, "iter": 7, "value": 2},
            # value increasing should result in improved_flag=False
            {"obj": -3.02321, "iter": 8, "value": 3},
            {"obj": -4.8918, "iter": 9, "value": 1.88},
        ]

        def add_results():
            # insert an calculation result
            for item in data:
                database.add_calculation_result(
                    set_id=item["iter"], object_function_value=item["obj"]
                )
            for result in database.load_calculation_results():
                self.assertEqual(result.merit_function_value, None)
                self.assertEqual(result.improved_flag, False)

        with tmp():
            database = _get_database()

            add_results()
            merit_items = list(filter(lambda x: x["value"] is not None, data))
            database.update_calculation_result(
                [{"iter": item["iter"], "value": item["value"]} for item in merit_items]
            )
            for idx, result in enumerate(database.load_calculation_results()):
                if idx == 0:
                    self.assertEqual(result.merit_function_value, None)
                    self.assertEqual(result.improved_flag, True)
                elif idx in [6, 8]:
                    self.assertEqual(result.merit_function_value, None)
                    self.assertEqual(result.improved_flag, False)
                else:
                    self.assertEqual(result.merit_function_value, data[idx]["value"])
                    self.assertEqual(result.improved_flag, True)

        with tmp():
            # When no merit value information is present an calculation result is
            # considered to increase merit if the objective function value provides an
            # overall improvement
            database = _get_database()
            add_results()
            database.update_calculation_result([])
            for idx, result in enumerate(database.load_calculation_results()):
                if idx == 0:
                    self.assertEqual(result.merit_function_value, None)
                    self.assertEqual(result.improved_flag, True)
                elif idx in [3, 4, 5, 9]:
                    self.assertEqual(result.merit_function_value, None)
                    self.assertEqual(result.improved_flag, False)
                else:
                    self.assertEqual(result.merit_function_value, None)
                    self.assertEqual(result.improved_flag, True)
