# ------------------------------------------------------------------------------
# Copyright (C) 2018-2019 Maximilian Stahlberg
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

"""Test quadratic and quadratically constraint (quadratic) programs."""

import math

import cvxopt

import picos

from .ptest import ProductionTestCase


class USQP(ProductionTestCase):
    """Unconstrained Scalar QP.

    (P) min. x² + x + 1
    """

    def setUp(self):  # noqa
        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x")
        P.set_objective("min", x**2 + x + 1)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, 3.0/4.0)
        self.expectVariable(self.x, -1.0/2.0)


class ISQP(ProductionTestCase):
    """Inequality Scalar QP.

    (P) min. x² + x + 1
        s.t. x ≥ 1
    """

    def setUp(self):  # noqa
        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x")
        P.set_objective("min", x**2 + x + 1)
        P.add_constraint(x >= 1)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, 3.0)
        self.expectVariable(self.x, 1.0)


class UVQP(ProductionTestCase):
    """Unconstrained Vector QP.

    (P) min. xᵀIx + 𝟙ᵀx + 1
    """

    def setUp(self):  # noqa
        # Set the dimensionality.
        self.n = n = 4

        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x", n)
        P.set_objective("min", abs(x)**2 + (1 | x) + 1)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, -self.n/4.0 + 1.0)
        self.expectVariable(self.x, [-1.0/2.0]*self.n)


class IVQP(ProductionTestCase):
    """Inequality Vector QP.

    (P) min. xᵀIx + 𝟙ᵀx + 1
        s.t. x ≥ 1
    """

    def setUp(self):  # noqa
        # Set the dimensionality.
        self.n = n = 4

        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x", n)
        P.set_objective("min", abs(x)**2 + (1 | x) + 1)
        P.add_constraint(x >= 1)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, 2.0*self.n + 1.0)
        self.expectVariable(self.x, [1.0]*self.n)


class NCQP(ProductionTestCase):
    """Nonconvex QP.

    The objective function's nonempty sublevel sets are hyperspheres centered
    at 𝟙 and the constraint region is the unit hypercube centered at 𝟘, so the
    optimum solution is -𝟙 (the point in the constraint region furthest away
    from the objective function's unconstrained minimum).

    (P) max. xᵀx - 𝟙ᵀx
        s.t. -𝟙 ≤ x ≤ 𝟙
    """

    def setUp(self):  # noqa
        # Set the dimensionality.
        self.n = n = 4

        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x", n)
        P.set_objective("max", (x | x) - (1 | x))
        P.add_constraint(x >= -1)
        P.add_constraint(x <= 1)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, 2*self.n)
        self.expectVariable(self.x, [-1.0]*self.n)


class QCQP(ProductionTestCase):
    """Standard form QCQP.

    The objective function's nonempty sublevel sets are hyperspheres centered
    at 𝟙 and the constraint region is the unit hypersphere centered at 𝟘, so the
    optimum solution in n dimensions is 𝟙/sqrt(n) (the point in the constraint
    region closest to the objective function's unconstrained minimum).

    (P) min. 0.5xᵀIx - 𝟙ᵀx - 0.5
        s.t. 0.5xᵀIx + 𝟘ᵀx - 0.5 ≤ 0
    """

    def setUp(self):  # noqa
        # Set the dimensionality.
        self.n = n = 4

        # Define parameters.
        ones = picos.new_param("ones", [1.0]*n)
        I    = picos.diag(ones)

        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x", n)
        P.set_objective("min", 0.5*x.T*I*x - (1 | x) - 0.5)
        P.add_constraint(0.5*x.T*I*x + (0 | x) - 0.5 <= 0)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, -math.sqrt(self.n))
        self.expectVariable(self.x, [1.0/math.sqrt(self.n)]*self.n)


class NCQCQP(ProductionTestCase):
    """Nonconvex QCQP.

    The objective function's nonempty sublevel sets are hyperspheres centered
    at 𝟙 and the constraint region is the unit hypersphere centered at 𝟘, so the
    optimum solution in n dimensions is -𝟙/sqrt(n) (the point in the constraint
    region furthest away from the objective function's unconstrained minimum).

    (P) max. 0.5xᵀIx - 𝟙ᵀx - 0.5
        s.t. 0.5xᵀIx + 𝟘ᵀx - 0.5 ≤ 0
    """

    def setUp(self):  # noqa
        # Set the dimensionality.
        self.n = n = 4

        # Define parameters.
        ones = picos.new_param("ones", [1.0]*n)
        I    = picos.diag(ones)

        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x", n)
        P.set_objective("max", 0.5*x.T*I*x - (1 | x) - 0.5)
        P.add_constraint(0.5*x.T*I*x + (0 | x) - 0.5 <= 0)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, math.sqrt(self.n))
        self.expectVariable(self.x, [-1.0/math.sqrt(self.n)]*self.n)


class CHOLESKY(ProductionTestCase):
    """Cholesky Factorization QCQP.

    This is another nonconvex problem that asks for a Cholesky factorization
    of a positive semidefinite n×n matrix A.

    (P) max. ∑ᵢⱼ Lᵢ·Lᵀⱼ
        s.t. Lᵢⱼ    = 0   ∀ i < j
             Lᵢ·Lᵀⱼ ≤ Aᵢⱼ ∀ i ≥ j
    """

    def setUp(self):  # noqa
        # Set the dimensionality.
        self.n = n = 3

        # Build a symmetric positive semidefinite matrix.
        cvxopt.setseed(1)
        Q = cvxopt.normal(n, n)
        self.A = A = Q.T*Q

        # Primal problem.
        self.P = P = picos.Problem()
        self.L = L = picos.RealVariable("L", (n, n))
        # LLT is the row-major vectorization of L·Lᵀ.
        LLT = [L[i, 0:min(i, j) + 1]*L.T[0:min(i, j) + 1, j]
            for i in range(n) for j in range(n)]
        # Maximize the sum of the entries of L·Lᵀ.
        P.set_objective("max", sum(LLT))
        # Require L to be lower triangular.
        self.C0 = P.add_list_of_constraints([
            L[i, j] == 0 for i in range(n) for j in range(n) if i < j])
        # Require L·Lᵀ ≤ A, so that L·Lᵀ = A is sought.
        self.CA = P.add_list_of_constraints([LLT[i*n + j] <= A[i, j]
            for i in range(n) for j in range(n) if i >= j])

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, sum(self.A))
        L = self.L.value
        self.assertAlmostEqual(L*L.T, self.A, self.to.varPlaces,
            "Not a Cholesky factorization.")
