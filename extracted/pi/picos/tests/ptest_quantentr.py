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

import math

import cvxopt
import numpy as np

import picos

from .ptest import ProductionTestCase


class QBP(ProductionTestCase):
    """Quantum entropy Bregman projection.

    (P) min. -S(X) - Tr(X*log(Y)) - Tr(X)
        s.t. Tr(X) = 1
    """

    def setUp(self):  # noqa
        np.random.seed(42)

        # Primal problem.
        self.P = P = picos.Problem()
        self.X = X = picos.HermitianVariable("X", 4)

        Y = np.random.randn(4, 4) + np.random.randn(4, 4) * 1j
        Y = Y @ Y.conj().T
        self.Y = Y = Y / np.trace(Y) * 5.0

        Dy, Uy = np.linalg.eigh(Y)
        logY = Uy @ np.diag(np.log(Dy)) @ Uy.conj().T

        P.set_objective("min",
            -picos.quantentr(X) - (X | logY + np.eye(4)).real)
        P.add_constraint(picos.trace(X) == 1)

    def testSolution(self):  # noqa
        obj = -math.log(5.0) - 1.0
        Xstar = self.Y / 5.0

        self.primalSolve(self.P)
        self.expectObjective(self.P, obj)
        self.expectVariable(self.X, cvxopt.matrix(Xstar))


class NCM(ProductionTestCase):
    """Nearest correlation matrix.

    (P) min. Tr(X (log(X) - log(Y))
        s.t. maindiag(Y) = [1]
    """

    def setUp(self):  # noqa
        # Primal problem.
        self.P = P = picos.Problem()
        self.X = X = np.eye(2) + np.ones((2, 2))
        self.Y = Y = picos.SymmetricVariable("Y", (2, 2))
        P.set_objective("min", picos.quantrelentr(X, Y))
        P.add_constraint(picos.maindiag(Y) == 1)

    def testSolution(self):  # noqa
        Ystar = 0.5 * self.X

        self.primalSolve(self.P)
        self.expectObjective(self.P, 4.0 * math.log(2))
        self.expectVariable(self.Y, cvxopt.matrix(Ystar))


class ENCM(ProductionTestCase):
    """Epigraph reformulation of nearest correlation matrix.

    (P) min. t
        s.t. t >= Tr(X (log(X) - log(Y))
             maindiag(Y) = [1]
    """

    def setUp(self):  # noqa
        # Primal problem.
        self.P = P = picos.Problem()
        self.t = t = picos.RealVariable("t")
        self.X = X = np.eye(2) + np.ones((2, 2))
        self.Y = Y = picos.SymmetricVariable("Y", (2, 2))
        P.set_objective("min", t)
        P.add_constraint(t >= picos.quantrelentr(X, Y))
        P.add_constraint(picos.maindiag(Y) == 1)

    def testSolution(self):  # noqa
        Ystar = 0.5 * self.X

        self.primalSolve(self.P)
        self.expectObjective(self.P, 4.0 * math.log(2))
        self.expectVariable(self.t, 4.0 * math.log(2))
        self.expectVariable(self.Y, cvxopt.matrix(Ystar))


class REE(ProductionTestCase):
    """Relative entropy of entanglement.

    (P) min. Tr(X (log(X) - log(Y))
        s.t. Tr(Y) = 1
             P1(Y) ≽ 0
    """

    def setUp(self):  # noqa
        # Primal problem.
        self.P = P = picos.Problem()
        self.Y = Y = picos.SymmetricVariable("Y", 4)
        P.add_constraint(picos.trace(Y) == 1.0)
        P.add_constraint(picos.partial_transpose(Y, subsystems=1) >> 0)

    def testEntangled(self):  # noqa
        X = np.array([
            [0.5, 0.0, 0.0, 0.5],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.5, 0.0, 0.0, 0.5]
        ])

        P, Y = self.P, self.Y

        obj = math.log(2)

        P.set_objective("min", picos.quantrelentr(X, Y))

        self.primalSolve(P)
        self.expectObjective(self.P, obj)

    def testSeparable(self):  # noqa
        X = np.array([
            [0.25, 0.25, 0.0,  0.0 ],
            [0.25, 0.25, 0.0,  0.0 ],
            [0.0,  0.0,  0.25, 0.25],
            [0.0,  0.0,  0.25, 0.25]
        ])

        P, Y = self.P, self.Y

        P.set_objective("min", picos.quantrelentr(X, Y))

        self.primalSolve(P)
        self.expectObjective(self.P, 0.0)
        self.expectVariable(self.Y, cvxopt.matrix(X))


class CREE(ProductionTestCase):
    """Complex relative entropy of entanglement.

    (P) min. Tr(X (log(X) - log(Y))
        s.t. Tr(Y) = 1
             P1(Y) ≽ 0
    """

    def setUp(self):  # noqa
        # Primal problem.
        self.P = P = picos.Problem()
        self.Y = Y = picos.HermitianVariable("Y", 4)
        P.add_constraint(picos.trace(Y) == 1.0)
        P.add_constraint(picos.partial_transpose(Y, subsystems=1) >> 0)

    def testEntangled(self):  # noqa
        X = np.array([
            [ 0.5,  0.0,  0.0,  0.5j],
            [ 0.0,  0.0,  0.0,  0.0 ],
            [ 0.0,  0.0,  0.0,  0.0 ],
            [-0.5j, 0.0,  0.0,  0.5 ]
        ])

        P, Y = self.P, self.Y

        obj = math.log(2)

        P.set_objective("min", picos.quantrelentr(X, Y))

        self.primalSolve(P)
        self.expectObjective(self.P, obj)

    def testSeparable(self):  # noqa
        X = np.array([
            [ 0.25,  0.25j, 0.0,   0.0  ],
            [-0.25j, 0.25,  0.0,   0.0  ],
            [ 0.0,   0.0,   0.25,  0.25j],
            [ 0.0,   0.0,-  0.25j, 0.25 ]
        ])

        P, Y = self.P, self.Y

        P.set_objective("min", picos.quantrelentr(X, Y))
        P.add_constraint(picos.trace(Y) == 1.0)
        P.add_constraint(picos.partial_transpose(Y, subsystems=1) >> 0)

        self.primalSolve(P)
        self.expectObjective(self.P, 0.0)
        self.expectVariable(self.Y, cvxopt.matrix(X))


class CQCC(ProductionTestCase):
    """Classical-quantum channel capacity.

    (P) max. S(Σ pi Xi) - Σ pi S(Xi)
        s.t. Σ pi = 1
             p ≥ 0
    """

    def setUp(self):  # noqa
        # Primal problem.
        self.P = P = picos.Problem()
        self.p = p = picos.RealVariable("p", 2)

        X = [
            np.array([[0.5, 0.0], [0.0, 0.5]]),
            np.array([[0.5, 0.5], [0.5, 0.5]]),
        ]
        entr_X = -np.array([np.log(0.5), 0.0])

        P.set_objective("max",
            picos.quantentr(p[0]*X[0] + p[1]*X[1]) - (p | entr_X))
        P.add_constraint(picos.sum(p) == 1)
        P.add_constraint(p >= 0)

    def testSolution(self):  # noqa
        eigs = np.array([0.8, 0.2])
        obj = -np.sum(eigs * np.log(eigs)) + 0.4 * np.log(0.5)

        self.primalSolve(self.P)
        self.expectObjective(self.P, obj)
        self.expectVariable(self.p, cvxopt.matrix([0.4, 0.6]))


class EACC(ProductionTestCase):
    """Entanglement assisted channel capacity.

    (P) max. S(VXV') - S(tr_2(VXV')) + S(tr_1(VXV'))
        s.t. Tr(X) = 1
             X ≽ 0
    """

    def setUp(self):  # noqa
        # Primal problem.
        self.P = P = picos.Problem()
        self.X = X = picos.SymmetricVariable("X", 2)

        gamma = 0.5
        V = np.array([
            [1., 0.              ],
            [0., np.sqrt(1-gamma)],
            [0., np.sqrt(gamma)  ],
            [0., 0.              ]
        ])

        obj1 = picos.quantcondentr(V * X * V.T, 1)
        obj2 = picos.quantentr(picos.partial_trace(V * X * V.T, 0))

        P.set_objective("max", obj1 + obj2)
        P.add_constraint(picos.trace(X) == 1)
        P.add_constraint(X >> 0)

    def testSolution(self):  # noqa
        obj = math.log(2.0)
        Xstar = np.eye(2) * 0.5

        self.primalSolve(self.P)
        self.expectObjective(self.P, obj)
        self.expectVariable(self.X, cvxopt.matrix(Xstar))


class EARD(ProductionTestCase):
    """Entanglement assisted rate-distortion.

    (P) min. -S(X) + S(tr_2(X)) + S(Z)
        s.t. tr_1(X) = Z
             ⟨X, Δ⟩ ≤ D
    """

    def purify(self, X):  # noqa
        n = X.shape[0]
        D, U = np.linalg.eigh(X)

        vec = np.zeros((n * n, 1), dtype=X.dtype)
        for i in range(n):
            vec += np.sqrt(max(0.0, D[i])) * np.kron(U[:, [i]], U[:, [i]])

        return vec @ vec.conj().T

    def entr(self, X):  # noqa
        eig = np.linalg.eigvalsh(X)
        eig = eig[eig > 0]
        return -sum(eig * np.log(eig))

    def setUp(self):  # noqa
        np.random.seed(42)

        n = 4

        # Primal problem.
        self.P = P = picos.Problem()
        self.X = X = picos.HermitianVariable("X", n * n)

        rho = np.random.rand(n, n) + np.random.rand(n, n) * 1j
        rho = rho @ rho.conj().T
        self.rho = rho = rho / np.trace(rho)
        self.purfifiedRho = purfifiedRho = self.purify(rho)

        allowDistortion = 0.0

        P.set_objective("min",
            -picos.quantcondentr(X, 1, (n, n)) + self.entr(rho))
        P.add_constraint(picos.partial_trace(X, 0, (n, n)) == rho)
        P.add_constraint(X | np.eye(n * n) - purfifiedRho <= allowDistortion)

    def testSolution(self):  # noqa
        obj = 2.0 * self.entr(self.rho)
        Xstar = self.purfifiedRho

        self.primalSolve(self.P)
        self.expectObjective(self.P, obj)
        self.expectVariable(self.X, cvxopt.matrix(Xstar))


class QKD(ProductionTestCase):
    """Quantum key distribution.

    (P) min. -S(X) + S(Z(X))
        s.t. tr(X) = 1
             ⟨X, Ai⟩ = bi, i=[1,2]
    """

    def setUp(self):  # noqa
        # Primal problem.
        self.P = picos.Problem()

        self.qx = qx = 0.25

        X0 = np.array([[0.5, 0.5], [0.5, 0.5]])
        X1 = np.array([[0.5, -0.5], [-0.5, 0.5]])
        Z0 = np.array([[1.0, 0.0], [0.0, 0.0]])
        Z1 = np.array([[0.0, 0.0], [0.0, 1.0]])

        self.Ax = np.kron(X0, X1) + np.kron(X1, X0)
        self.Az = np.kron(Z0, Z1) + np.kron(Z1, Z0)

        self.obj = np.log(2) + ( qx*np.log(qx) + (1-qx)*np.log(1-qx) )
        self.Xstar = np.array([
            [0.1250, 0.0,    0.,     0.0625],
            [0.0,    0.3750, 0.1875, 0.0   ],
            [0.0,    0.1875, 0.3750, 0.0   ],
            [0.0625, 0.0,    0.,     0.1250]
        ])

    def testReal(self):  # noqa
        P, Ax, Az = self.P, self.Ax, self.Az
        qx = self.qx
        qz = 1 - qx

        self.X = X = picos.SymmetricVariable("X", 4)

        P.set_objective("min", picos.quantkeydist(X))
        P.add_constraint(picos.trace(X) == 1)
        P.add_constraint((X | Ax) == qx)
        P.add_constraint((X | Az) == qz)

        self.primalSolve(self.P)
        self.expectObjective(self.P, self.obj)
        self.expectVariable(self.X, cvxopt.matrix(self.Xstar))

    def testComplex(self):  # noqa
        P, Ax, Az = self.P, self.Ax, self.Az
        qx = self.qx
        qz = 1 - qx

        self.X = X = picos.HermitianVariable("X", 4)

        dummy_K_list = [math.sqrt(0.5) * np.eye(4), math.sqrt(0.5) * np.eye(4)]

        P.set_objective("min", picos.quantkeydist(X, K_list=dummy_K_list))
        P.add_constraint(picos.trace(X) == 1)
        P.add_constraint((X | Ax) == qx)
        P.add_constraint((X | Az) == qz)

        self.primalSolve(self.P)
        self.expectObjective(self.P, self.obj)
        self.expectVariable(self.X, cvxopt.matrix(self.Xstar))
