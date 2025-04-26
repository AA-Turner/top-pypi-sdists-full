import os

import pytest

from mip import BINARY, CBC, GUROBI, MAXIMIZE, Model, OptimizationStatus

TOL = 1e-4
SOLVERS = [CBC]
if "GUROBI_HOME" in os.environ:
    SOLVERS += [GUROBI]


@pytest.mark.parametrize("solver", SOLVERS)
def test_write_logs(solver):
    m = Model(name="ModelWithLogs", solver_name=solver)
    x1 = m.add_var(name="x1", var_type=BINARY)
    x2 = m.add_var(name="x2", var_type=BINARY)
    x3 = m.add_var(name="x3", var_type=BINARY)
    x4 = m.add_var(name="x4", var_type=BINARY)

    m.add_constr(774 * x1 + 76 * x2 + 22 * x3 + 42 * x4 <= 875)
    m.add_constr(67 * x1 + 27 * x2 + 794 * x3 + 53 * x4 <= 875)

    m += 75 * x1 + 6 * x2 + 3 * x3 + 33 * x4, MAXIMIZE

    # activate store
    m.store_search_progress_log = True

    m.optimize()
    # check result
    assert m.status == OptimizationStatus.OPTIMAL

    m.search_progress_log.write(f"search_progress_log_{solver}.plog")
