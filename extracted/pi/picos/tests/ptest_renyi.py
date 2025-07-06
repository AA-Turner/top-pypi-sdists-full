# ------------------------------------------------------------------------------
# Copyright (C) 2024 Kerry He
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

"""Test quantum relative entropy programs."""

import cvxopt
import numpy as np

import picos

from .ptest import ProductionTestCase


def mpower(A, p):
    """Computes the matrix power of a hermitian matrix."""
    D, U = np.linalg.eigh(A)
    return U @ np.diag(np.power(D, p)) @ U.conj().T

class RMI_REAL(ProductionTestCase):
    """Renyi mutual information."""

    def setUp(self):  # noqa
        np.random.seed(42)

        # Primal problem.
        self.P = picos.Problem()
        self.X = picos.SymmetricVariable("X", 4)

        A = np.random.randn(16, 16)
        A = A @ A.T
        self.A = A / np.trace(A)
        self.tr2_A = picos.partial_trace(A, 1, (4, 4))

    def _opt_renyi_mutual_information(self, alpha):
        A, tr2_A = self.A, self.tr2_A
        temp = mpower(tr2_A @ picos.I(4), 1 - alpha) @ mpower(A, alpha)
        temp = mpower(picos.partial_trace(temp, 0, (4, 4)), 1 / alpha)
        return temp / np.trace(temp)

    def _opt_sand_renyi_mutual_information(self, Xstar, alpha):
        A, tr2_A = self.A, self.tr2_A
        temp = mpower(tr2_A @ Xstar, (1 - alpha) / (2 * alpha))
        temp = mpower(temp @ A @ temp, alpha)
        temp = picos.partial_trace(temp, 0, (4, 4))
        return temp / np.trace(temp)

    def testRenyi(self):  # noqa
        P, X, A, tr2_A = self.P, self.X, self.A, self.tr2_A

        alpha = 0.5

        P.set_objective("min", picos.renyientr(A, tr2_A @ X, alpha))
        P.add_constraint(picos.trace(X) == 1)

        Xstar = self._opt_renyi_mutual_information(alpha)

        self.primalSolve(self.P)
        self.expectVariable(self.X, cvxopt.matrix(Xstar))

    def _test_quasi(self, alpha, direction):
        P, X, A, tr2_A = self.P, self.X, self.A, self.tr2_A

        P.set_objective(direction, picos.quasientr(A, tr2_A @ X, alpha))
        P.add_constraint(picos.trace(X) == 1)

        Xstar = self._opt_renyi_mutual_information(alpha)

        self.primalSolve(self.P)
        self.expectVariable(self.X, cvxopt.matrix(Xstar))

    def testQuasi1(self):  # noqa
        self._test_quasi(-0.5, "min")

    def testQuasi2(self):  # noqa
        self._test_quasi(0.5, "max")

    def testQuasi3(self):  # noqa
        self._test_quasi(1.5, "min")

    def testSandwichedRenyi(self):  # noqa
        P, X, A, tr2_A = self.P, self.X, self.A, self.tr2_A

        alpha = 0.5

        P.set_objective("min", picos.sandrenyientr(A, tr2_A @ X, alpha))
        P.add_constraint(picos.trace(X) == 1)

        self.primalSolve(self.P)

        RHS = self._opt_sand_renyi_mutual_information(self.X, alpha)
        self.expectVariable(self.X, RHS.value)

    def _test_sandquasi(self, alpha, direction):
        P, X, A, tr2_A = self.P, self.X, self.A, self.tr2_A

        P.set_objective(direction, picos.sandquasientr(A, tr2_A @ X, alpha))
        P.add_constraint(picos.trace(X) == 1)

        self.primalSolve(self.P)

        RHS = self._opt_sand_renyi_mutual_information(self.X, alpha)
        self.expectVariable(self.X, RHS.value)

    def testSandwichedQuasi1(self):  # noqa
        self._test_sandquasi(0.75, "max")

    def testSandwichedQuasi2(self):  # noqa
        self._test_sandquasi(1.5, "min")

class RMI_COMPLEX(RMI_REAL):
    """Renyi mutual information."""

    def setUp(self):  # noqa
        np.random.seed(42)

        # Primal problem.
        self.P = picos.Problem()
        self.X = picos.HermitianVariable("X", 4)

        A = np.random.randn(16, 16) + np.random.randn(16, 16) * 1j
        A = A @ A.conj().T
        self.A = A / np.trace(A)
        self.tr2_A = picos.partial_trace(A, 1, (4, 4))
