import copy
from pathlib import Path
from typing import Any, Dict

import pytest

from ropt.enums import ConstraintType
from ropt.optimization import EnsembleOptimizer
from seba_sqlite import SebaSnapshot, SqliteStorage

_SEBA_CONFIG: Dict[str, Any] = {
    "optimizer": {
        "tolerance": 0.005,
    },
    "realizations": {"names": [0, 1], "weights": [0.25]},
    "objective_functions": {
        "names": ["distance_p", "distance_q"],
        "weights": [0.8, 0.2],
    },
    "gradient": {
        "number_of_perturbations": 5,
        "perturbation_magnitudes": 0.001,
    },
    "nonlinear_constraints": {
        "names": ["z_coord"],
        "rhs_values": [0.8],
        "types": [ConstraintType.LE],
    },
    "variables": {
        "initial_values": 0,
        "upper_bounds": 1.0,
        "lower_bounds": -1.0,
        "names": [("point_0", "x"), ("point_0", "y"), ("point_0", "z")],
    },
}


@pytest.mark.database
@pytest.mark.dakota
def test_construct_updated_optimization_progress(
    tmp_path: Path, evaluator: Any, test_functions: Any
):
    pytest.importorskip("seba_dakota_backend")
    seba_config = copy.deepcopy(_SEBA_CONFIG)
    seba_config["optimizer"]["backend"] = "dakota"
    seba_config["optimizer"]["algorithm"] = "optpp_q_newton"
    output_folder = tmp_path / "outputdir"
    output_folder.mkdir()
    seba_config["optimizer"]["output_dir"] = output_folder

    test_functions = test_functions + (lambda controls, context: controls[2],)

    optimization_work_flow = EnsembleOptimizer(evaluator(test_functions))
    _storage = SqliteStorage(optimization_work_flow, output_folder)
    optimization_work_flow.start_optimization(
        plan= [{ "config": seba_config}, {"optimizer": {}}]
    )

    result = SebaSnapshot(output_folder).get_snapshot(filter_out_gradient=True)

    # Check the objectives and constraints in the meta data.
    objectives = [(obj.name, obj.weight) for obj in result.metadata.objectives.values()]
    expected_objectives = zip(
        seba_config["objective_functions"]["names"],
        seba_config["objective_functions"]["weights"],
    )
    assert set(objectives) == set(expected_objectives)

    constraints = [
        (con.name, con.rhs_value) for con in result.metadata.constraints.values()
    ]
    expected_constraints = zip(
        seba_config["nonlinear_constraints"]["names"],
        seba_config["nonlinear_constraints"]["rhs_values"],
    )
    assert set(constraints) == set(expected_constraints)

    # For backwards compatibility, the metadata still has a
    # functions field, which is formed by the concatenation
    # of the functions and constraints.
    functions = list(result.metadata.functions.keys())
    objectives = list(result.metadata.objectives.keys())
    constraints = list(result.metadata.constraints.keys())
    assert functions == objectives + constraints
