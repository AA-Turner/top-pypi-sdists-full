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

"""Test solving a problem's dual outside the reformulation framework."""

import cvxopt as cvx
import picos
import traceback


def setup_LP():
    """Create a simple LP."""
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
    P.set_objective('max', -(1 | x[:2]) + y - ('I' | X))
    P.solve()
    return P, 'LP'


def setup_SOCP():
    """Create a simple SOCP."""
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

    P.add_constraint(abs(AA[0] * u) ** 2 <= lbd[0])
    P.add_constraint(abs(AA[1] * u) ** 2 <= lbd[1])
    P.add_constraint(abs(AA[2] * u) ** 2 <= lbd[1])

    P.set_objective('min', (cc | u) + (1 | lbd))
    P.solve()
    return P, 'SOCP'


def setup_SDP():
    """Create an SDP with additional SOC and RSOC constraints."""
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
    return P, 'SDP'


def solve_as_primal(P):
    """Solve a problem directly and return its objective function value."""
    P.solve()
    return P.value


def solve_as_dual(P):
    """Solve a problem's dual and return its objective function value."""
    D = P.dual
    D.solve()
    return D.value


def solve_as_bidual(P):
    """Solve a problem's dual and return its objective function value."""
    D = P.dual
    DD = D.dual
    DD.solve()
    return DD.value


def test_primal_dual(P):
    """Test solving a problem and its dual."""
    try:
        pstar = solve_as_primal(P)
        dstar = solve_as_dual(P)
        ddstar = solve_as_bidual(P)

        assert abs(pstar-dstar) < 1e-5, \
            "assertion failed {0} != {1}".format(pstar, dstar)

        assert abs(pstar - ddstar) < 1e-5, \
            "assertion failed {0} != {1}".format(pstar, ddstar)

        print('OK')
        failure = 0
    except Exception as ex:
        print(ex)
        tb = traceback.format_exc()
        print(tb)
        failure = 1

    return failure


if __name__ == "__main__":
    count_failure = 0
    count_runs = 0

    for P, name in [setup_LP(), setup_SOCP(), setup_SDP()]:
        print('testing dualization of {0}...'.format(name))
        failure = test_primal_dual(P)
        count_failure += failure
        count_runs += 1

    print('{0} test runs, {1} failures'.format(count_runs, count_failure))
