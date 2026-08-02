import os
import random
from unittest import TestCase

import pytest

from seba_sqlite import Database, Function
from seba_sqlite.exceptions import ObjectNotFoundError


from .database_utils import (
    _CONTROLS,
    _EXISTING_SIMULATION_NAME,
    _EXPERIMENT_NAME,
    _FUNCTIONS,
    _NUMBER_OF_BATCHES,
    _REALIZATION_WEIGHTS,
    _REALIZATIONS,
    load_info_to_db,
    tmpdir
)


def _custom_update(database):
    value = {
        "sim_name": _EXISTING_SIMULATION_NAME,
        "result_value": random.uniform(0.0, 2.0),
        "function_name": _FUNCTIONS[-1],
        "times_index": 0,
    }
    database.add_simulation_result(**value)


@pytest.mark.database
class TestDatabaseSimulationResult(TestCase):
    @tmpdir(os.getcwd())
    def test_add_result_with_non_existing_function_non_existing_simulation(self):
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
        function_name = "NonExistingFunction"
        simulation_name = "NonExistingSimulation"
        with self.assertRaises(ObjectNotFoundError):
            database.load_simulation_results(name=simulation_name)
        value = {
            "sim_name": simulation_name,
            "result_value": random.uniform(0.0, 2.0),
            "function_name": function_name,
            "times_index": 0,
        }
        with self.assertRaises(ObjectNotFoundError):
            database.add_simulation_result(**value)

    @tmpdir(os.getcwd())
    def test_add_result_with_non_existing_function_existing_simulation(self):
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
        function_name = "NonExistingFunction"
        simulation_result = database.load_simulation_results(
            name=_EXISTING_SIMULATION_NAME
        )
        # Aparently the load_simulation_results(name=name) method returns a list of
        # functions! Since the function doesn exist, returns empty
        self.assertFalse(bool(simulation_result))
        value = {
            "sim_name": _EXISTING_SIMULATION_NAME,
            "result_value": random.uniform(0.0, 2.0),
            "function_name": function_name,
            "times_index": 0,
        }
        with self.assertRaises(ObjectNotFoundError):
            database.add_simulation_result(**value)

    @tmpdir(os.getcwd())
    def test_add_result_to_existing_function_non_existing_simulation(self):
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
        simulation_name = "NonExistingSimulation"
        value = {
            "sim_name": simulation_name,
            "result_value": random.uniform(0.0, 2.0),
            "function_name": _FUNCTIONS[0],
            "times_index": 0,
        }
        with self.assertRaises(ObjectNotFoundError):
            database.add_simulation_result(**value)

    @tmpdir(os.getcwd())
    def test_add_result_to_existing_function_existing_simulation(self):
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
        simulation_result = database.load_simulation_results(
            name=_EXISTING_SIMULATION_NAME
        )
        self.assertFalse(bool(simulation_result))
        value = {
            "sim_name": _EXISTING_SIMULATION_NAME,
            "result_value": random.uniform(0.0, 2.0),
            "function_name": _FUNCTIONS[0],
            "times_index": 0,
        }
        database.add_simulation_result(**value)
        new_simulation_result = database.load_simulation_results(
            name=_EXISTING_SIMULATION_NAME
        )
        self.assertTrue(bool(new_simulation_result))

    @tmpdir(os.getcwd())
    def test_load_existing_simulation_results(self):
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
        _custom_update(database)
        existing_result = database.load_simulation_results(
            name=_EXISTING_SIMULATION_NAME
        )
        self.assertIsNotNone(existing_result[0])
        self.assertEqual(existing_result[0]["name"], _FUNCTIONS[-1])
        self.assertIsNotNone(existing_result[0]["value"])

    @tmpdir(os.getcwd())
    def test_load_non_existing_simulation_results(self):
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
        non_existing = database.load_simulation_results(name=_EXISTING_SIMULATION_NAME)
        self.assertFalse(bool(non_existing))

    @tmpdir(os.getcwd())
    def test_load_result_objective_functions(self):
        database = Database(os.getcwd())
        simulations_values = [
            [realization, 0, _EXISTING_SIMULATION_NAME] for realization in _REALIZATIONS
        ]
        load_info_to_db(
            database,
            **{
                "Experiment": [_EXPERIMENT_NAME],
                "Function": _FUNCTIONS,
                "Batch": range(_NUMBER_OF_BATCHES),
                "control_definition": _CONTROLS,
                "Realization": zip(_REALIZATIONS, _REALIZATION_WEIGHTS),
                "Simulation": simulations_values,
                "dict_order": ["Function", "Batch", "control_definition", "Simulation"],
            },
        )

        # Add Simulation Results
        simulations = database.load_simulations()
        objective_functions = database.load_functions(
            function_type=Function.FUNCTION_OBJECTIVE_TYPE
        )
        for objective in objective_functions:
            for simulation in simulations:
                value = {
                    "sim_name": simulation.name,
                    "result_value": random.uniform(0.0, 2.0),
                    "function_name": objective.name,
                    "times_index": 0,
                }
                database.add_simulation_result(**value)

        for objective in objective_functions:
            self.assertIsNotNone(
                database.load_simulation_results(
                    function_name=objective.name,
                    function_type=Function.FUNCTION_OBJECTIVE_TYPE,
                )
            )

    @tmpdir(os.getcwd())
    def test_load_result_constraint_functions(self):
        database = Database(os.getcwd())
        simulations_values = [
            [realization, 0, _EXISTING_SIMULATION_NAME] for realization in _REALIZATIONS
        ]
        load_info_to_db(
            database,
            **{
                "Experiment": [_EXPERIMENT_NAME],
                "Function": _FUNCTIONS,
                "Batch": range(_NUMBER_OF_BATCHES),
                "control_definition": _CONTROLS,
                "Realization": zip(_REALIZATIONS, _REALIZATION_WEIGHTS),
                "Simulation": simulations_values,
                "dict_order": ["Function", "Batch", "control_definition", "Simulation"],
            },
        )

        # Add Simulation Results
        simulations = database.load_simulations()
        constraint_functions = database.load_functions(
            function_type=Function.FUNCTION_CONSTRAINT_TYPE
        )
        for constraint in constraint_functions:
            for simulation in simulations:
                value = {
                    "sim_name": simulation.name,
                    "result_value": random.uniform(0.0, 2.0),
                    "function_name": constraint.name,
                    "times_index": 0,
                }
                database.add_simulation_result(**value)

        for constraint in constraint_functions:
            self.assertIsNotNone(
                database.load_simulation_results(
                    function_name=constraint.name,
                    function_type=Function.FUNCTION_CONSTRAINT_TYPE,
                )
            )

    @tmpdir(os.getcwd())
    def test_load_objective_function_results(self):
        database = Database(os.getcwd())
        simulations_values = [
            [realization, 0, _EXISTING_SIMULATION_NAME] for realization in _REALIZATIONS
        ]

        load_info_to_db(
            database,
            **{
                "Experiment": [_EXPERIMENT_NAME],
                "Batch": range(_NUMBER_OF_BATCHES),
                "control_definition": _CONTROLS,
                "Realization": zip(_REALIZATIONS, _REALIZATION_WEIGHTS),
                "Simulation": simulations_values,
                "dict_order": ["Batch", "control_definition", "Simulation"],
            },
        )

        for fun in _FUNCTIONS:
            input_values = {
                "name": fun,
                "function_type": "OBJECTIVE",
                "weight": random.uniform(1.0, 2.0),
                "normalization": random.uniform(1.0, 2.0),
                "rhs_value": random.uniform(0.0, 0.5),
                "constraint_type": None,
            }
            database.add_function(**input_values)

        # Add Simulation Results
        simulations = database.load_simulations()
        objective_functions = database.load_functions(
            function_type=Function.FUNCTION_OBJECTIVE_TYPE
        )

        for objective in objective_functions:
            for simulation in simulations:
                value = {
                    "sim_name": simulation.name,
                    "result_value": random.uniform(0.0, 2.0),
                    "function_name": objective.name,
                    "times_index": 0,
                }
                database.add_simulation_result(**value)
        objective_functions_results = {
            objective.name: database.load_simulation_results(
                function_name=objective.name,
                function_type=Function.FUNCTION_OBJECTIVE_TYPE,
            )
            for objective in database.load_functions(
                function_type=Function.FUNCTION_OBJECTIVE_TYPE
            )
        }
        self.assertIsNotNone(objective_functions_results)

    @tmpdir(os.getcwd())
    def test_load_constraint_function_results(self):
        database = Database(os.getcwd())
        simulations_values = [
            [realization, 0, _EXISTING_SIMULATION_NAME] for realization in _REALIZATIONS
        ]

        load_info_to_db(
            database,
            **{
                "Experiment": [_EXPERIMENT_NAME],
                "Batch": range(_NUMBER_OF_BATCHES),
                "control_definition": _CONTROLS,
                "Realization": zip(_REALIZATIONS, _REALIZATION_WEIGHTS),
                "Simulation": simulations_values,
                "dict_order": ["Batch", "control_definition", "Simulation"],
            },
        )

        for fun in _FUNCTIONS:
            input_values = {
                "name": fun,
                "function_type": "CONSTRAINT",
                "weight": random.uniform(1.0, 2.0),
                "normalization": random.uniform(1.0, 2.0),
                "rhs_value": random.uniform(0.0, 0.5),
                "constraint_type": None,
            }
            database.add_function(**input_values)

        # Add Simulation Results
        simulations = database.load_simulations()
        constraint_functions = database.load_functions(
            function_type=Function.FUNCTION_CONSTRAINT_TYPE
        )

        for constraint in constraint_functions:
            for simulation in simulations:
                value = {
                    "sim_name": simulation.name,
                    "result_value": random.uniform(0.0, 2.0),
                    "function_name": constraint.name,
                    "times_index": 0,
                }
                database.add_simulation_result(**value)
        constraint_functions_results = {
            objective.name: database.load_simulation_results(
                function_name=objective.name,
                function_type=Function.FUNCTION_CONSTRAINT_TYPE,
            )
            for objective in database.load_functions(
                function_type=Function.FUNCTION_CONSTRAINT_TYPE
            )
        }
        self.assertIsNotNone(constraint_functions_results)

    @tmpdir(os.getcwd())
    def test_load_results_function(self):
        database = Database(os.getcwd())
        simulations_values = [
            [realization, 0, _EXISTING_SIMULATION_NAME] for realization in _REALIZATIONS
        ]
        load_info_to_db(
            database,
            **{
                "Experiment": [_EXPERIMENT_NAME],
                "Function": _FUNCTIONS,
                "Batch": range(_NUMBER_OF_BATCHES),
                "control_definition": _CONTROLS,
                "Realization": zip(_REALIZATIONS, _REALIZATION_WEIGHTS),
                "Simulation": simulations_values,
                "dict_order": ["Function", "Batch", "control_definition", "Simulation"],
            },
        )

        simulations = database.load_simulations()
        functions = database.load_functions()
        for function in functions:
            for simulation in simulations:
                value = {
                    "sim_name": simulation.name,
                    "result_value": random.uniform(0.0, 2.0),
                    "function_name": function.name,
                    "times_index": 0,
                }
                database.add_simulation_result(**value)

        self.assertIsNotNone(
            database.load_simulation_results(function_name=_FUNCTIONS[0])
        )
