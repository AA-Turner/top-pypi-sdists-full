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

"""Test non-commutative persepective programs."""

import cvxopt
import numpy as np

import picos

from .ptest import ProductionTestCase


class OP_REL_ENTR_REAL(ProductionTestCase):
    """Operator relative entropy program."""

    def setUp(self):  # noqa
        np.random.seed(42)

        self.n = n = 4

        # Primal problem.
        self.P = P = picos.Problem()
        self.X = X = picos.SymmetricVariable("X", n)
        self.Y = Y = picos.SymmetricVariable("Y", n)

        self.X0 = X0 = np.eye(n)
        Y0 = np.random.randn(n, n)
        self.Y0 = Y0 = Y0 @ Y0.conj().T

        sign, logabsdet = np.linalg.slogdet(Y0)
        self.obj = -sign * logabsdet

        P.add_constraint(X == X0)
        P.add_constraint(Y == Y0)

    def testEpigraph(self):  # noqa
        P, X, Y = self.P, self.X, self.Y
        obj, X0, Y0 = self.obj, self.X0, self.Y0

        P.set_objective("min", picos.trace(picos.oprelentr(X, Y)))

        self.primalSolve(P)
        self.expectObjective(P, obj)
        self.expectVariable(X, cvxopt.matrix(X0))
        self.expectVariable(Y, cvxopt.matrix(Y0))

    def testTrace(self):  # noqa
        P, X, Y, n = self.P, self.X, self.Y, self.n
        obj, X0, Y0 = self.obj, self.X0, self.Y0

        T = picos.SymmetricVariable("T", n)

        P.set_objective("min", picos.trace(T))
        P.add_constraint(picos.oprelentr(X, Y) << T)

        self.primalSolve(P)
        self.expectObjective(P, obj)
        self.expectVariable(X, cvxopt.matrix(X0))
        self.expectVariable(Y, cvxopt.matrix(Y0))


class OP_REL_ENTR_COMPLEX(ProductionTestCase):
    """Complex operator relative entropy program."""

    def setUp(self):  # noqa
        np.random.seed(42)

        self.n = n = 4

        # Primal problem.
        self.P = P = picos.Problem()
        self.X = X = picos.HermitianVariable("X", n)
        self.Y = Y = picos.HermitianVariable("Y", n)

        self.X0 = X0 = np.eye(n)
        Y0 = np.random.randn(n, n) + np.random.randn(n, n) * 1j
        self.Y0 = Y0 = Y0 @ Y0.conj().T

        sign, logabsdet = np.linalg.slogdet(Y0)
        self.obj = -sign * logabsdet.real

        P.add_constraint(X == X0)
        P.add_constraint(Y == Y0)

    def testEpigraph(self):  # noqa
        P, X, Y = self.P, self.X, self.Y
        obj, X0, Y0 = self.obj, self.X0, self.Y0

        P.set_objective("min", picos.trace(picos.oprelentr(X, Y)))

        self.primalSolve(P)
        self.expectObjective(P, cvxopt.matrix([obj]))
        self.expectVariable(X, cvxopt.matrix(X0))
        self.expectVariable(Y, cvxopt.matrix(Y0))

    def testTrace(self):  # noqa
        P, X, Y, n = self.P, self.X, self.Y, self.n
        obj, X0, Y0 = self.obj, self.X0, self.Y0

        T = picos.HermitianVariable("T", n)

        P.set_objective("min", picos.trace(T))
        P.add_constraint(picos.oprelentr(X, Y) << T)

        self.primalSolve(P)
        self.expectObjective(P, cvxopt.matrix([obj]))
        self.expectVariable(X, cvxopt.matrix(X0))
        self.expectVariable(Y, cvxopt.matrix(Y0))


class MTX_GEO_MEAN_HYPO_REAL(ProductionTestCase):
    """Matrix concave geometric mean program."""

    def setUp(self):  # noqa
        np.random.seed(42)

        self.n = n = 4

        # Primal problem.
        self.P = P = picos.Problem()
        self.X = X = picos.SymmetricVariable("X", n)
        self.Y = Y = picos.SymmetricVariable("Y", n)

        self.X0 = X0 = np.eye(n)
        Y0 = np.random.randn(n, n)
        self.Y0 = Y0 = Y0 @ Y0.conj().T

        eigY = np.linalg.eigvalsh(Y0)
        self.obj = np.sum(np.sqrt(eigY))

        P.add_constraint(X == X0)
        P.add_constraint(Y == Y0)

    def testEpigraph(self):  # noqa
        P, X, Y = self.P, self.X, self.Y
        obj, X0, Y0 = self.obj, self.X0, self.Y0

        P.set_objective("max", picos.trace(picos.mtxgeomean(X, Y)))

        self.primalSolve(P)
        self.expectObjective(P, obj)
        self.expectVariable(X, cvxopt.matrix(X0))
        self.expectVariable(Y, cvxopt.matrix(Y0))

    def testTrace(self):  # noqa
        P, X, Y, n = self.P, self.X, self.Y, self.n
        obj, X0, Y0 = self.obj, self.X0, self.Y0

        T = picos.SymmetricVariable("T", n)

        P.set_objective("max", picos.trace(T))
        P.add_constraint(picos.mtxgeomean(X, Y) >> T)

        self.primalSolve(P)
        self.expectObjective(P, obj)
        self.expectVariable(X, cvxopt.matrix(X0))
        self.expectVariable(Y, cvxopt.matrix(Y0))


class MTX_GEO_MEAN_HYPO_COMPLEX(ProductionTestCase):
    """Complex concave matrix geometric mean program."""

    def setUp(self):  # noqa
        np.random.seed(42)

        self.n = n = 4

        # Primal problem.
        self.P = P = picos.Problem()
        self.X = X = picos.HermitianVariable("X", n)
        self.Y = Y = picos.HermitianVariable("Y", n)

        self.X0 = X0 = np.eye(n)
        Y0 = np.random.randn(n, n) + np.random.randn(n, n) * 1j
        self.Y0 = Y0 = Y0 @ Y0.conj().T

        eigY = np.linalg.eigvalsh(Y0)
        self.obj = np.sum(np.sqrt(eigY))

        P.add_constraint(X == X0)
        P.add_constraint(Y == Y0)

    def testEpigraph(self):  # noqa
        P, X, Y = self.P, self.X, self.Y
        obj, X0, Y0 = self.obj, self.X0, self.Y0

        P.set_objective("max", picos.trace(picos.mtxgeomean(X, Y)))

        self.primalSolve(P)
        self.expectObjective(P, cvxopt.matrix([obj]))
        self.expectVariable(X, cvxopt.matrix(X0))
        self.expectVariable(Y, cvxopt.matrix(Y0))

    def testTrace(self):  # noqa
        P, X, Y, n = self.P, self.X, self.Y, self.n
        obj, X0, Y0 = self.obj, self.X0, self.Y0

        T = picos.HermitianVariable("T", n)

        P.set_objective("max", picos.trace(T))
        P.add_constraint(picos.mtxgeomean(X, Y) >> T)

        self.primalSolve(P)
        self.expectObjective(P, cvxopt.matrix([obj]))
        self.expectVariable(X, cvxopt.matrix(X0))
        self.expectVariable(Y, cvxopt.matrix(Y0))


class MTX_GEO_MEAN_EPI_REAL(ProductionTestCase):
    """Matrix convex geometric mean program."""

    def setUp(self):  # noqa
        np.random.seed(42)

        self.n = n = 4

        # Primal problem.
        self.P = P = picos.Problem()
        self.X = X = picos.SymmetricVariable("X", n)
        self.Y = Y = picos.SymmetricVariable("Y", n)

        self.X0 = X0 = np.eye(n)
        Y0 = np.random.randn(n, n)
        self.Y0 = Y0 = Y0 @ Y0.conj().T

        eigY = np.linalg.eigvalsh(Y0)
        self.obj = np.sum(np.power(eigY, 1.5))

        P.add_constraint(X == X0)
        P.add_constraint(Y == Y0)

    def testEpigraph(self):  # noqa
        P, X, Y = self.P, self.X, self.Y
        obj, X0, Y0 = self.obj, self.X0, self.Y0

        P.set_objective("min", picos.trace(picos.mtxgeomean(X, Y, 1.5)))

        self.primalSolve(P)
        self.expectObjective(P, obj)
        self.expectVariable(X, cvxopt.matrix(X0))
        self.expectVariable(Y, cvxopt.matrix(Y0))

    def testTrace(self):  # noqa
        P, X, Y, n = self.P, self.X, self.Y, self.n
        obj, X0, Y0 = self.obj, self.X0, self.Y0

        T = picos.SymmetricVariable("T", n)

        P.set_objective("min", picos.trace(T))
        P.add_constraint(picos.mtxgeomean(X, Y, 1.5) << T)

        self.primalSolve(P)
        self.expectObjective(P, obj)
        self.expectVariable(X, cvxopt.matrix(X0))
        self.expectVariable(Y, cvxopt.matrix(Y0))


class MTX_GEO_MEAN_EPI_COMPLEX(ProductionTestCase):
    """Complex convex matrix geometric mean program."""

    def setUp(self):  # noqa
        np.random.seed(42)

        self.n = n = 4

        # Primal problem.
        self.P = P = picos.Problem()
        self.X = X = picos.HermitianVariable("X", n)
        self.Y = Y = picos.HermitianVariable("Y", n)

        self.X0 = X0 = np.eye(n)
        Y0 = np.random.randn(n, n) + np.random.randn(n, n) * 1j
        self.Y0 = Y0 = Y0 @ Y0.conj().T

        eigY = np.linalg.eigvalsh(Y0)
        self.obj = np.sum(np.power(eigY, 1.5))

        P.add_constraint(X == X0)
        P.add_constraint(Y == Y0)

    def testEpigraph(self):  # noqa
        P, X, Y = self.P, self.X, self.Y
        obj, X0, Y0 = self.obj, self.X0, self.Y0

        P.set_objective("min", picos.trace(picos.mtxgeomean(X, Y, 1.5)))

        self.primalSolve(P)
        self.expectObjective(P, cvxopt.matrix([obj]))
        self.expectVariable(X, cvxopt.matrix(X0))
        self.expectVariable(Y, cvxopt.matrix(Y0))

    def testTrace(self):  # noqa
        P, X, Y, n = self.P, self.X, self.Y, self.n
        obj, X0, Y0 = self.obj, self.X0, self.Y0

        T = picos.HermitianVariable("T", n)

        P.set_objective("min", picos.trace(T))
        P.add_constraint(picos.mtxgeomean(X, Y, 1.5) << T)

        self.primalSolve(P)
        self.to.objPlaces = 5
        self.expectObjective(P, cvxopt.matrix([obj]))
        self.expectVariable(X, cvxopt.matrix(X0))
        self.expectVariable(Y, cvxopt.matrix(Y0))
