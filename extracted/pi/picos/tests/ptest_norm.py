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

"""Test problems featuring vector and matrix norms."""

import cvxopt as cvx
import numpy as np

import picos

from .ptest import ProductionTestCase


class VECTOR_1dot5_NORM(ProductionTestCase):
    """3/2-Norm problem."""

    def setUp(self):  # noqa

        self.P = P = picos.Problem()
        self.X = X = picos.RealVariable('X', (3, 5), lower=-1)
        self.A = A = np.reshape(range(-2, 13), X.size)
        P.add_constraint(X >= A)
        self.t = t = picos.RealVariable('t')

        P.add_constraint(picos.Norm(X, 3/2.) <= t)
        P.set_objective('min', t)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        Xopt = np.maximum(self.A, 0)
        self.to.objPlaces = 4
        self.expectObjective(
            self.P, cvx.matrix([np.linalg.norm(Xopt.ravel(), 1.5)]))


class MATRIX_1_2_NORM(ProductionTestCase):
    """(1,2)-Matrix Norm problem."""

    def setUp(self):  # noqa

        self.P = P = picos.Problem()
        self.X = X = picos.RealVariable('X', (3, 5), lower=-1)
        self.A = A = np.reshape(range(-2, 13), X.size)
        P.add_constraint(X >= A)
        self.t = t = picos.RealVariable('t')

        P.add_constraint(picos.Norm(X, 1, 2) <= t)
        P.set_objective('min', t)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        Xopt = np.maximum(self.A, 0)
        self.to.objPlaces = 4
        opt = np.linalg.norm(np.linalg.norm(Xopt, 1, axis=0), 2)
        self.expectObjective(self.P, cvx.matrix([opt]))


class MATRIX_2dot5_1dot5_NORM(ProductionTestCase):
    """(2.5,1.5)-Matrix Norm problem."""

    def setUp(self):  # noqa
        self.P = P = picos.Problem(rel_prim_fsb_tol=1e-7, rel_ipm_opt_tol=1e-7)
        self.X = X = picos.RealVariable('X', (3, 5), lower=-1)
        self.A = A = np.reshape(range(-2, 13), X.size)
        P.add_constraint(X >= A)
        self.t = t = picos.RealVariable('t')

        P.add_constraint(picos.Norm(X, 2.5, 1.5) <= t)
        P.set_objective('min', t)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        Xopt = np.maximum(self.A, 0)
        self.to.objPlaces = 4
        opt = np.linalg.norm(np.linalg.norm(Xopt, 2.5, axis=0), 1.5)
        self.expectObjective(self.P, cvx.matrix([opt]))


class SPECTRAL_NORM(ProductionTestCase):
    """Matrix Spectral Norm problem."""

    def setUp(self):  # noqa
        self.P = P = picos.Problem()
        self.X = X = picos.RealVariable('X', (3, 5))
        self.A = A = np.reshape(range(-2, 13), X.size)
        P.add_constraint(X >= A)
        self.t = t = picos.RealVariable('t')

        P.add_constraint(picos.SpectralNorm(X) <= t)
        P.set_objective('min', t)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.to.objPlaces = 5  # Necessary for MOSEK (Fusion).
        opt = np.linalg.norm(self.A, 2)
        self.expectObjective(self.P, cvx.matrix([opt]))


class COMPLEX_SPECTRAL_NORM(ProductionTestCase):
    """Complex Matrix Spectral Norm problem."""

    def setUp(self):  # noqa
        self.P = P = picos.Problem()
        self.X = X = picos.ComplexVariable('X', (3, 5))
        self.A = A = np.reshape(range(15), X.size)
        P.add_constraint(X.real >= A)
        P.add_constraint(X.imag >= 2 * A)
        self.t = t = picos.RealVariable('t')

        P.add_constraint(picos.SpectralNorm(X) <= t)
        P.set_objective('min', t)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.to.objPlaces = 4  # Necessary for QICS.
        opt = np.linalg.norm(self.A + self.A * 2j, 2)
        self.expectObjective(self.P, cvx.matrix([opt]))


class SYMMETRIC_SPECTRAL_NORM(ProductionTestCase):
    """Symmetric Matrix Spectral Norm problem."""

    def setUp(self):  # noqa
        np.random.seed(42)
        self.P = P = picos.Problem()
        self.X = X = picos.SymmetricVariable('X', (4, 4))
        A = np.random.randn(4, 4)
        self.A = A = A + A.T
        P.add_constraint(X << A)
        self.t = t = picos.RealVariable('t')

        P.add_constraint(picos.SpectralNorm(X) <= t)
        P.set_objective('min', t)

    def testSolution(self):  # noqa
        self.knownFailure("smcp")  # "Factorization failed"
        self.primalSolve(self.P)
        opt = max(abs(np.linalg.eigvalsh(self.A)))
        self.expectObjective(self.P, cvx.matrix([opt]))


class HERMITIAN_SPECTRAL_NORM(ProductionTestCase):
    """Hermitian Matrix Spectral Norm problem."""

    def setUp(self):  # noqa
        np.random.seed(42)
        self.P = P = picos.Problem()
        self.X = X = picos.HermitianVariable('X', (4, 4))
        A = np.random.randn(4, 4) + 1j * np.random.randn(4, 4)
        self.A = A = A + A.T.conj()
        P.add_constraint(X << A)
        self.t = t = picos.RealVariable('t')

        P.add_constraint(picos.SpectralNorm(X) <= t)
        P.set_objective('min', t)

    def testSolution(self):  # noqa
        self.knownFailure("smcp")  # "Factorization failed"
        self.primalSolve(self.P)
        opt = max(abs(np.linalg.eigvalsh(self.A)))
        self.expectObjective(self.P, cvx.matrix([opt]))


class NUCLEAR_NORM(ProductionTestCase):
    """Matrix Nuclear Norm problem."""

    def setUp(self):  # noqa
        self.P = P = picos.Problem()
        self.X = X = picos.RealVariable('X', (3, 5))
        self.A = A = np.reshape(range(-2, 13), X.size)
        P.add_constraint(X >= A)
        self.t = t = picos.RealVariable('t')

        P.add_constraint(picos.NuclearNorm(X) <= t)
        P.set_objective('min', t)


    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.to.objPlaces = 4
        self.expectObjective(self.P, cvx.matrix([25 + 2**0.5]))


class COMPLEX_NUCLEAR_NORM(ProductionTestCase):
    """Complex Matrix Nuclear Norm problem."""

    def setUp(self):  # noqa
        self.P = P = picos.Problem()
        self.X = X = picos.ComplexVariable('X', (3, 5))
        self.A = A = np.reshape(range(15), X.size)
        P.add_constraint(X.real >= A)
        P.add_constraint(X.imag >= 2 * A)
        self.t = t = picos.RealVariable('t')

        P.add_constraint(picos.NuclearNorm(X) <= t)
        P.set_objective('min', t)


    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.to.objPlaces = 5
        self.expectObjective(self.P, cvx.matrix([5 * 190473981**0.5 / 936.]))


class SYMMETRIC_NUCLEAR_NORM(ProductionTestCase):
    """Symmetric Matrix Nuclear Norm problem."""

    def setUp(self):  # noqa
        self.P = P = picos.Problem()
        self.X = X = picos.SymmetricVariable('X', (3, 3))
        P.add_constraint(X[0, 1] == 2)
        P.add_constraint(X[0, 2] == 3)
        P.add_constraint(X[1, 2] == 6)
        self.t = t = picos.RealVariable('t')

        P.add_constraint(picos.NuclearNorm(X) <= t)
        P.set_objective('min', t)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        Xopt = np.array([[1, 2, 3], [2, 4, 6], [3, 6, 5]])
        opt = np.linalg.norm(Xopt, 'nuc')
        self.expectObjective(self.P, cvx.matrix([opt]))


class HERMITIAN_NUCLEAR_NORM(ProductionTestCase):
    """Hermitian Matrix Nuclear Norm problem."""

    def setUp(self):  # noqa
        self.P = P = picos.Problem()
        self.X = X = picos.HermitianVariable('X', (3, 3))
        P.add_constraint(X[0, 1] == 2-1j)
        P.add_constraint(X[0, 2] == 3-2j)
        P.add_constraint(X[1, 2] == 8-1j)
        self.t = t = picos.RealVariable('t')

        P.add_constraint(picos.NuclearNorm(X) <= t)
        P.set_objective('min', t)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        Xopt = np.array([[1, 2-1j, 3-2j], [2+1j, 5, 8-1j], [3+2j, 8+1j, 6]])
        opt = np.linalg.norm(Xopt, 'nuc')
        self.expectObjective(self.P, cvx.matrix([opt]))
