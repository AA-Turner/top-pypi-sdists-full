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

"""Test problems featuring power expressions."""

import cvxopt as cvx
import numpy as np

import picos

from .ptest import ProductionTestCase


class POWER_TRACE(ProductionTestCase):
    """Parent class for tests involving Powertrace."""

    def setUp(self):  # noqa
        # Set the dimensionality.
        n = self.n = 3
        np.random.seed(42)

        # a symmetric matrix
        B1 = self.B1 = np.random.randn(n, n)
        B1 = B1 + B1.T

        # a skew-symmetric matrix
        B2 = self.B2 = np.random.randn(n, n)
        B2 = B2 - B2.T

        # a Hermitian matrix
        B = self.B = B1 + 1j * B2
        self.S, self.U = np.linalg.eigh(B)  # U is unitary
        U = self.U

        M0 = self.M0 = np.tensordot(U[0], U[0].conj(), 0)
        M1 = self.M1 = np.tensordot(U[1], U[1].conj(), 0)
        M2 = self.M2 = np.tensordot(U[2], U[2].conj(), 0)

        # The Mi are "orthogonal", so the eigs of \sum xi Mi are the xi's.

        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable('x', 3, lower=0)
        self.t = t = picos.RealVariable('t', 1)
        X = x[0] * M0 + x[1] * M1 + x[2] * M2

        if 0 < self.p < 1:
            P.add_constraint(picos.PowerTrace(X, self.p) >= t)
            P.add_constraint(x <= [1, 2, 3])
            P.set_objective('max', t)
        elif self.p >= 1:
            P.add_constraint(picos.PowerTrace(X, self.p) <= t)
            P.add_constraint(x >= [1, 2, 3])
            P.set_objective('min', t)
        else:
            P.add_constraint(picos.PowerTrace(X, self.p) <= t)
            P.add_constraint(x <= [1, 2, 3])
            P.set_objective('min', t)


class POWER_TRACE_1_2(POWER_TRACE):
    """Trace of a matrix raised to 1/2."""

    def __init__(self, *args, **kwargs):  # noqa
        super(POWER_TRACE_1_2, self).__init__(*args, **kwargs)
        self.p = 0.5

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, 1. ** self.p + 2. ** self.p + 3. ** self.p)
        self.expectVariable(self.t, 1. ** self.p + 2. ** self.p + 3. ** self.p)
        self.expectVariable(self.x, cvx.matrix([1., 2., 3.]))


class POWER_TRACE_2_3(POWER_TRACE):
    """Trace of a matrix raised to 2/3."""

    def __init__(self, *args, **kwargs):  # noqa
        super(POWER_TRACE_2_3, self).__init__(*args, **kwargs)
        self.p = 2./3

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, 1. ** self.p + 2. ** self.p + 3. ** self.p)
        self.expectVariable(self.t, 1. ** self.p + 2. ** self.p + 3. ** self.p)
        self.expectVariable(self.x, cvx.matrix([1., 2., 3.]))


class POWER_TRACE_1_5(POWER_TRACE):
    """Trace of a matrix raised to 1/5."""

    def __init__(self, *args, **kwargs):  # noqa
        super(POWER_TRACE_1_5, self).__init__(*args, **kwargs)
        self.p = 0.2

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, 1. ** self.p + 2. ** self.p + 3. ** self.p)
        self.expectVariable(self.t, 1. ** self.p + 2. ** self.p + 3. ** self.p)
        self.expectVariable(self.x, cvx.matrix([1., 2., 3.]))


class POWER_TRACE_1dot6(POWER_TRACE):
    """Trace of a matrix raised to 1.6."""

    def __init__(self, *args, **kwargs):  # noqa
        super(POWER_TRACE_1dot6, self).__init__(*args, **kwargs)
        self.p = 1.6

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, 1. ** self.p + 2. ** self.p + 3. ** self.p)
        self.expectVariable(self.t, 1. ** self.p + 2. ** self.p + 3. ** self.p)
        self.expectVariable(self.x, cvx.matrix([1., 2., 3.]))


class POWER_TRACE_m05(POWER_TRACE):
    """Trace of a matrix raised to -1/2."""

    def __init__(self, *args, **kwargs):  # noqa
        super(POWER_TRACE_m05, self).__init__(*args, **kwargs)
        self.p = -0.5

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, 1. ** self.p + 2. ** self.p + 3. ** self.p)
        self.expectVariable(self.t, 1. ** self.p + 2. ** self.p + 3. ** self.p)
        self.expectVariable(self.x, cvx.matrix([1., 2., 3.]))


class CONVEX_POWER(ProductionTestCase):
    """Sum of scalar powers problem."""

    def setUp(self):  # noqa
        Ppow = self.Ppow = picos.Problem()
        z = self.z = picos.RealVariable('z', lower=0)
        powers = [-5./3, 2, 1.5]
        t = {}
        for k, p in enumerate(powers):
            t[k] = picos.RealVariable('t'+str(p), lower=0)
            Ppow.add_constraint(z**p <= t[k])
        Ppow.set_objective('min', picos.sum([tk for tk in t.values()]))

    def testSolution(self):  # noqa
        self.primalSolve(self.Ppow)
        xstar = 0.806284
        self.to.objPlaces = 4
        self.expectObjective(self.Ppow,
            cvx.matrix([xstar ** (-5. / 3) + xstar ** 1.5 + xstar ** 2.]))
        self.expectVariable(self.z, xstar)


class MAXDET(ProductionTestCase):
    """Largest determinant problem."""

    def setUp(self):  # noqa
        np.random.seed(42)
        n = self.n = 6
        A = np.random.randn(n, n)
        self.A = A.dot(A.T)
        P = self.P = picos.Problem()
        A = picos.Constant(self.A)
        X = picos.SymmetricVariable('X', (n, n))
        t = picos.RealVariable('t')
        P.add_constraint(X << A)
        P.add_constraint(picos.detrootn(X) >= t)
        P.set_objective('max', t)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        detrn = (np.linalg.det(self.A)) ** (1./self.n)
        self.expectObjective(self.P, cvx.matrix([detrn]))
