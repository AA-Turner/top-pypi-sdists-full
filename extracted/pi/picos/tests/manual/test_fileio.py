# ------------------------------------------------------------------------------
# Copyright (C) 2020 Guillaume Sagnol
#
# This file is part of PICOS Testbench.
#
# PICOS Testbench is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# PICOS Testbench is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------

"""Test reading and writing of problems from and to files."""

import os

import cvxopt as cvx
import numpy as np
import picos
import traceback
import cplex


def setup_LP():
    """A simple LP to be written in a file."""
    P = picos.Problem()
    x = picos.RealVariable('x', 4, lower=1.5)
    y = picos.RealVariable('y', lower=0, upper=1)
    X = picos.SymmetricVariable('X', (3, 3))
    P.add_constraint(x[0] + y - 1 <= x[1])
    P.add_constraint(2 * y + 0.5 - x[1] <= 0)
    P.add_constraint(2 * y + 0.4 - x[0] <= 0)
    P.add_constraint(X >= 2)
    P.add_constraint(X[0, 1] >= X[1, 2] + 2)
    P.add_constraint(X[1, 1] == 3)
    P.add_constraint(abs(y) <= 0.9)
    P.add_constraint(picos.sum_k_largest(x, 3) <= 5)
    P.set_objective('min', (1 | x[:2]) - y + ('I' | X))
    P.solve()
    return P


def setup_MIP():
    """A simple MIP to be written in a file."""
    E = [(0, 14), (1, 4), (1, 5), (1, 9), (1, 14), (1, 15), (1, 16), (2, 5),
        (2, 12), (2, 16), (2, 18), (3, 4), (3, 6), (3, 9), (3, 11), (3, 17),
        (4, 7), (4, 13), (5, 8), (6, 9), (6, 12), (6, 15), (6, 18), (6, 19),
        (7, 8), (7, 16), (8, 11), (8, 17), (8, 18), (9, 11), (9, 12), (9, 16),
        (10, 11), (10, 12), (10, 14), (11, 13), (11, 14), (11, 16), (12, 13),
        (12, 14), (12, 16), (13, 17), (14, 16), (15, 18), (16, 17), (16, 18),
        (16, 19), (17, 18)]
    n = 20
    seed = 553995
    np.random.seed(seed)
    w = np.random.randint(0, 100, n)

    IP = picos.Problem()
    x = picos.BinaryVariable('x', n)
    for i, j in E:
        IP.add_constraint(x[i] + x[j] <= 1)
    IP.set_objective('max', (w | x))
    IP.solve()
    return IP


def setup_SOCP(integer=False):
    """A simple SOCP to be written in a file."""
    A = [cvx.matrix([[1, 0, 0, 0, 0],
                     [0, 3, 0, 0, 0],
                     [0, 0, 1, 0, 0]]),
         cvx.matrix([[0, 0, 2, 0, 0],
                     [0, 1, 0, 0, 0],
                     [0, 0, 0, 1, 0]]),
         cvx.matrix([[0, 0, 0, 2, 0],
                     [4, 0, 0, 0, 0],
                     [0, 0, 1, 0, 1]])
         ]

    c = cvx.matrix([1, 2, 3, 4, 5])

    P = picos.Problem()
    AA = [picos.Constant('A[{0}]'.format(i), Ai.T) for i, Ai in enumerate(A)]
    cc = picos.Constant('c', c)
    u = picos.RealVariable('u', c.size)
    lbd = picos.RealVariable('lbd', 2)
    if integer:
        v = picos.IntegerVariable('v', c.size)
        P.add_constraint(10*u == v)

    P.add_constraint(abs(AA[0] * u) ** 2 <= lbd[0])
    P.add_constraint(abs(AA[1] * u) ** 2 <= lbd[1])
    P.add_constraint(abs(AA[2] * u) ** 2 <= lbd[1])

    P.set_objective('min', (cc | u) + (1 | lbd))
    P.solve()
    return P


def setup_SDP():
    """An SDP with additional SOC and RSOC constraints."""
    P = picos.Problem()
    x = picos.RealVariable('x', 2, lower=1.5)
    y = picos.RealVariable('y', lower=0, upper=1)
    X = picos.SymmetricVariable('X', (3, 3))
    P.add_constraint(x[0] + y - 1 <= x[1])
    P.add_constraint(2 * y + 0.5 - x[1] <= 0)
    P.add_constraint(2 * y + 0.4 - x[0] <= 0)
    P.add_constraint(X >= 2)
    P.add_constraint(X[0, 1] >= X[1, 2] + 2)
    P.add_constraint(X[1, 1] == 3)
    P.set_objective('min', (1 | x) - y + ('I' | X))
    P.add_constraint(X >> 0)
    P.add_constraint(x[0] ** 2 <= y * (x[1] + x[0]))
    P.add_constraint(abs(x) <= 5 * y)
    P.solve()
    return P


def solve_file_with_cplex(filename):  # noqa
    # load the .lp file with cplex
    task = cplex.Cplex()
    task.read(filename)
    task.set_results_stream(None)

    # Solve the cplex problem
    task.solve()
    opt = task.solution.get_objective_value()
    return opt


def solve_file_with_gurobi(filename):  # noqa
    ff = os.popen('gurobi_cl ' + filename + ' | tail -3')
    out = ff.read()
    obj = out.split('objective')[1]
    if ',' in obj:
        return float(obj.split(',')[0])
    else:
        return float(obj.split()[-1])


def solve_file_with_mosek(filename):  # noqa
    ff = os.popen('mosek ' + filename)
    out = ff.read()
    obj = out.split('Primal.  obj:')[1].split()[0]
    opt = float(obj)
    for ext in ('sol', 'bas', 'int'):
        try:
            os.remove(filename.split('.')[0] + '.' + ext)
        except OSError:
            pass
    return opt


def solve_file_with_sdpa(filename):  # noqa
    ff = os.popen('sdpa ' + filename + ' ' + filename.split('.')[0] + '.out')
    out = ff.read()
    obj = out.split('objValPrimal =')[1].split()[0]
    opt = float(obj)
    for ext in ('out',):
        try:
            os.remove(filename.split('.')[0] + '.' + ext)
        except OSError:
            pass
    return opt


def solve_file_after_picos_import(filename):  # noqa
    P, _, _, _ = picos.import_cbf(filename)
    P.solve()
    return P.value


def solve_file(filename, writer, picos_import=False):
    """Load a problem from a file and solve it.

    It seems that gurobi .lp files are not compatible with cplex
    so we solve them with gurobi from the command line.

    Similarly, mosek .mps files include a QSECTION for RSOC constraints
    so we solve them with mosek from the command line.
    """
    if picos_import:
        assert filename.endswith('.cbf')
        return solve_file_after_picos_import(filename)
    elif writer == 'gurobi' and filename.endswith('.lp'):
        return solve_file_with_gurobi(filename)
    elif writer == 'mosek' and filename.endswith('.mps'):
        return solve_file_with_mosek(filename)
    elif filename.endswith('.cbf'):
        return solve_file_with_mosek(filename)
    elif filename.endswith('.dat-s'):
        return solve_file_with_sdpa(filename)
    else:
        return solve_file_with_cplex(filename)


def test_read_write_format(P, writer, format, picos_import=False):
    """Write a problem in a file using the desired writer.

    Then, the problem is loaded again in CPLEX
    and we compare PICOS and CPLEX optimal values.
    """
    filename = 'tmp.' + format
    try:
        # write the problem to a file
        P.write_to_file(filename, writer=writer)

        # solve lp file with external solver
        opt = solve_file(filename, writer, picos_import)

        # compare objective value
        expected = P.value
        assert abs(abs(opt)-abs(expected)) < 1e-5, \
            "assertion failed {0} != {1}".format(opt, expected)

        print('OK')
        failure = 0
    except Exception as ex:
        print(ex)
        tb = traceback.format_exc()
        print(tb)
        failure = 1
    finally:
        # clean-up
        os.remove(filename)
    return failure


def main():  # noqa
    count_failure = 0
    count_runs = 0

    P = setup_LP()
    for writer in ['gurobi', 'mosek', 'cplex', 'picos']:
        print('testing LP with lp-writer {0}'.format(writer))
        failure = test_read_write_format(P, writer, 'lp')
        count_failure += failure
        count_runs += 1
    for writer in ['gurobi', 'mosek', 'cplex']:
        print('testing LP with mps-writer {0}'.format(writer))
        failure = test_read_write_format(P, writer, 'mps')
        count_failure += failure
        count_runs += 1

    IP = setup_MIP()
    for writer in ['gurobi', 'mosek', 'cplex', 'picos']:
        print('testing MIP with lp-writer {0}'.format(writer))
        failure = test_read_write_format(IP, writer, 'lp')
        count_failure += failure
        count_runs += 1
    for writer in ['gurobi', 'mosek', 'cplex']:
        print('testing MIP with mps-writer {0}'.format(writer))
        failure = test_read_write_format(IP, writer, 'mps')
        count_failure += failure
        count_runs += 1

    for integer in [False, True]:
        SOCP = setup_SOCP()
        for writer in ['gurobi', 'mosek', 'cplex']:
            print('testing {0}SOCP with lp-writer {1}'.format('MI'*integer,
                                                              writer))
            failure = test_read_write_format(SOCP, writer, 'lp')
            count_failure += failure
            count_runs += 1
        for writer in ['gurobi', 'mosek', 'cplex']:
            print('testing {0}SOCP with mps-writer {1}'.format('MI' * integer,
                                                              writer))
            failure = test_read_write_format(SOCP, writer, 'mps')
            count_failure += failure
            count_runs += 1

    SDP = setup_SDP()
    writer = 'picos'
    print('testing SDP with dat-s-writer {0}'.format(writer))
    failure = test_read_write_format(SDP, writer, 'dat-s')
    count_failure += failure
    count_runs += 1

    for writer in ['mosek', 'picos']:
        print(
            'testing SDP with cbf-writer {0} imported by MOSEK'.format(writer))
        failure = test_read_write_format(SDP, writer, 'cbf')
        count_failure += failure
        count_runs += 1

    for writer in ['mosek', 'picos']:
        print(
            'testing SDP with cbf-writer {0} imported by PICOS'.format(writer))
        failure = test_read_write_format(SDP, writer, 'cbf', picos_import=True)
        count_failure += failure
        count_runs += 1

    print('{0} test runs, {1} failures'.format(count_runs, count_failure))


if __name__ == "__main__":
    main()
