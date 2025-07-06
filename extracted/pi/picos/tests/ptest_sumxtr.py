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

"""Test problems featuring sum of k extreme values."""

import cvxopt as cvx
import numpy as np

import picos

from .ptest import ProductionTestCase


class LARGEST_ELEMENTS(ProductionTestCase):
    """Bound the sum over largest elements."""

    def setUp(self):  # noqa
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable('x', 5, lower=0)
        P.add_constraint(picos.sum_k_largest(x, 3) <= 1)
        P.add_constraint((1 | x) <= 2)
        P.set_objective('max', (1 | x[:4]))

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, cvx.matrix([4./3]))


class LARGEST_LAMBDAS(ProductionTestCase):
    """Bound the sum over largest eigenvalues."""

    def setUp(self):  # noqa
        self.P = P = picos.Problem()
        self.X = X = picos.SymmetricVariable('X', (5, 5))
        P.add_constraint(picos.sum_k_largest_lambda(X, 3) <= 1)
        P.add_constraint(X >> 0)
        P.add_constraint(picos.trace(X) <= 2)
        P.add_constraint(X[0, 3] == 0.1)
        P.set_objective('max', picos.trace(X) - X[4, 4])

    def testSolution(self):  # noqa
        self.knownFailure("smcp")
        self.primalSolve(self.P)
        self.expectObjective(self.P, cvx.matrix([19. / 15]))


class LARGEST_LAMBDA_HERMITIAN(ProductionTestCase):
    """Find largest EV of a Hermitian matrix."""

    def setUp(self):  # noqa
        np.random.seed(42)
        self.P = P = picos.Problem()
        self.X = X = picos.HermitianVariable('X', (4, 4))
        A = np.random.randn(4, 4) + 1j * np.random.randn(4, 4)
        self.A = A = A + A.T.conj()
        self.t = t = picos.RealVariable('t')
        P.add_constraint(picos.lambda_max(X) <= t)
        P.add_constraint(X >> A)
        P.set_objective('min', t)

    def testSolution(self):  # noqa
        self.knownFailure("smcp")
        opt = float(max(np.linalg.eigvalsh(self.A)))
        self.primalSolve(self.P)
        self.expectObjective(self.P, opt)


class LARGEST_LAMBDAS_HERMITIAN(ProductionTestCase):
    """Sum largest EVs of a Hermitian matrix."""

    def setUp(self):  # noqa
        np.random.seed(42)
        self.k = 2
        self.P = P = picos.Problem()
        self.X = X = picos.HermitianVariable('X', (4, 4))
        A = np.random.randn(4, 4) + 1j * np.random.randn(4, 4)
        self.A = A = A + A.T.conj()
        self.t = t = picos.RealVariable('t')
        P.add_constraint(picos.sum_k_largest_lambda(X, self.k) <= t)
        P.add_constraint(X >> A)
        P.set_objective('min', t)

    def testSolution(self):  # noqa
        self.knownFailure("smcp")
        opt = float(sum(sorted(np.linalg.eigvalsh(self.A))[-self.k:]))
        self.primalSolve(self.P)
        self.expectObjective(self.P, opt)
