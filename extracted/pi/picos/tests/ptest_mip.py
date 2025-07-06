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

"""Test mixed integer programs."""

import cvxopt

import picos

from .ptest import ProductionTestCase


class ILP(ProductionTestCase):
    """Integer LP.

    (P) min. x + y + z
        s.t. x ≥ 1.5
             |y| ≤ 1
             |z| ≤ 2
             y + z ≥ 3
             x, y, z integer
    """

    def setUp(self):  # noqa
        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.IntegerVariable("x")
        self.y = y = picos.IntegerVariable("y")
        self.z = z = picos.IntegerVariable("z")
        P.set_objective("min", x + y + z)
        P.add_constraint(x >= 1.5)
        P.add_constraint(abs(y) <= 1)
        P.add_constraint(abs(z) <= 2)
        P.add_constraint(y + z >= 3)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, 5)
        self.expectVariable(self.x, 2)
        self.expectVariable(self.y, 1)
        self.expectVariable(self.z, 2)


class MILP(ProductionTestCase):
    """Mixed Integer LP.

    (P) min. x + y + z
        s.t. x ≥ 1.5
             |y| ≤ 1
             |z| ≤ 2
             y + z ≥ 3
             y, z integer
    """

    def setUp(self):  # noqa
        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x")
        self.y = y = picos.IntegerVariable("y")
        self.z = z = picos.IntegerVariable("z")
        P.set_objective("min", x + y + z)
        P.add_constraint(x >= 1.5)
        P.add_constraint(abs(y) <= 1)
        P.add_constraint(abs(z) <= 2)
        P.add_constraint(y + z >= 3)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, 4.5)
        self.expectVariable(self.x, 1.5)
        self.expectVariable(self.y, 1)
        self.expectVariable(self.z, 2)


class IQP(ProductionTestCase):
    """Integer QP.

    (P) min. x² + y² + z²
        s.t. x ≥ 1.5
             |y| ≤ 1
             |z| ≤ 2
             y + z ≥ 3
             x, y, z integer
    """

    def setUp(self):  # noqa
        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.IntegerVariable("x")
        self.y = y = picos.IntegerVariable("y")
        self.z = z = picos.IntegerVariable("z")
        P.set_objective("min", x**2 + y**2 + z**2)
        P.add_constraint(x >= 1.5)
        P.add_constraint(abs(y) <= 1)
        P.add_constraint(abs(z) <= 2)
        P.add_constraint(y + z >= 3)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, 9)
        self.expectVariable(self.x, 2)
        self.expectVariable(self.y, 1)
        self.expectVariable(self.z, 2)


class MIQP(ProductionTestCase):
    """Mixed Integer QP.

    (P) min. x² + y² + z²
        s.t. x ≥ 1.5
             |y| ≤ 1
             |z| ≤ 2
             y + z ≥ 3
             y, z integer
    """

    def setUp(self):  # noqa
        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x")
        self.y = y = picos.IntegerVariable("y")
        self.z = z = picos.IntegerVariable("z")
        P.set_objective("min", x**2 + y**2 + z**2)
        P.add_constraint(x >= 1.5)
        P.add_constraint(abs(y) <= 1)
        P.add_constraint(abs(z) <= 2)
        P.add_constraint(y + z >= 3)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, 7.25)
        self.expectVariable(self.x, 1.5)
        self.expectVariable(self.y, 1)
        self.expectVariable(self.z, 2)


class ISOCP(ProductionTestCase):
    """Integer SOCP.

    The SOC constraints have an affine representation.

    (P) max. ∑ᵢ i·xᵢ
        s.t. xᵢ² ≤ 1 ∀ i ∈ {1, …, n} [passed as SOC constraint]
             ∑ᵢ xᵢ = k
             x nonnegative integer vector
    """

    def setUp(self):  # noqa
        # Set the dimensionality and the parameter.
        self.n = n = 8
        self.k = k = 5

        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.IntegerVariable("x", n, lower=0)
        P.set_objective("max", sum([(i+1)*x[i] for i in range(n)]))
        P.add_list_of_constraints([(1 & x[i]) << picos.soc() for i in range(n)])
        P.add_constraint(1 | x == k)

    @staticmethod
    def f(n):
        """The sum of the natural numbers up to ``n``."""
        return (n*(n+1)) // 2

    def testSolution(self):  # noqa
        n = self.n
        k = self.k
        self.primalSolve(self.P)
        self.expectObjective(self.P, self.f(n) - self.f(n-k))
        self.expectVariable(self.x, [0]*(n-k) + [1]*k)


class IRSOCP(ProductionTestCase):
    """Integer RSOCP.

    (P) max. ∑ᵢ i·xᵢ
        s.t. xᵢ² ≤ 1 ∀ i ∈ {1, …, n} [passed as RSOC constraint]
             ∑ᵢ xᵢ = k
             x nonnegative integer vector
    """

    def setUp(self):  # noqa
        # Set the dimensionality and the parameter.
        self.n = n = 8
        self.k = k = 5

        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.IntegerVariable("x", n, lower=0)
        P.set_objective("max", sum([(i+1)*x[i] for i in range(n)]))

        P.add_list_of_constraints(
            [(1 & (1 & x[i])) << picos.rsoc() for i in range(n)])

        P.add_constraint(1 | x == k)

    @staticmethod
    def f(n):
        """The sum of the natural numbers up to ``n``."""
        return (n*(n+1)) // 2

    def testSolution(self):  # noqa
        n = self.n
        k = self.k
        self.primalSolve(self.P)
        # HACK: Known bad precision.
        self.expectObjective(self.P, self.f(n) - self.f(n-k),
            by_solver=(False if self.solver == "ecos" else None))
        self.expectVariable(self.x, [0]*(n-k) + [1]*k)


# TODO: IQCP 1/2 like for IQCQP and NCIQCQP?
class IQCP(ProductionTestCase):
    """Integer QCP.

    (P) max. ∑ᵢ i·xᵢ
        s.t. xᵢ² + xᵢ ≤ 2 ∀ i ∈ {1, …, n}
             ∑ᵢ xᵢ = k
             x nonnegative integer vector
    """

    def setUp(self):  # noqa
        # Set the dimensionality and the parameter.
        self.n = n = 8
        self.k = k = 5

        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.IntegerVariable("x", n, lower=0)
        P.set_objective("max", sum([(i+1)*x[i] for i in range(n)]))
        P.add_list_of_constraints([x[i]**2 + x[i] <= 2 for i in range(n)])
        P.add_constraint(1 | x == k)

    @staticmethod
    def f(n):
        """The sum of the natural numbers up to ``n``."""
        return (n*(n+1)) // 2

    def testSolution(self):  # noqa
        n = self.n
        k = self.k
        self.primalSolve(self.P)
        self.expectObjective(self.P, self.f(n) - self.f(n-k))
        self.expectVariable(self.x, [0]*(n-k) + [1]*k)


class IQCQP1(ProductionTestCase):
    """Integer QCQP 1.

    Quadratic constraints are convex and have an affine representation.

    (P) min. ∑ᵢ (i·xᵢ)²
        s.t. xᵢ² ≤ 1 ∀ i ∈ {1, …, n}
             ∑ᵢ xᵢ = k
             x nonnegative integer vector
    """

    def setUp(self):  # noqa
        # Set the dimensionality and the parameter.
        self.n = n = 8
        self.k = k = 5

        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.IntegerVariable("x", n, lower=0)
        P.set_objective("min", sum([((i+1)*x[i])**2 for i in range(n)]))
        P.add_list_of_constraints([x[i]**2 <= 1 for i in range(n)])
        P.add_constraint(1 | x == k)

    @staticmethod
    def f(n):
        """The sum of squares of the natural numbers up to ``n``."""
        return (n*(n+1)*(2*n+1)) // 6

    def testSolution(self):  # noqa
        # ECOS: Recurring solution failure. Almost certainly an interface bug.
        # See https://github.com/embotech/ecos-python/issues/34.
        self.knownFailure("ecos")

        n = self.n
        k = self.k
        self.primalSolve(self.P)
        self.expectObjective(self.P, self.f(k),  # HACK: Known bad precision.
            by_solver=(False if self.solver == "ecos" else None))
        self.expectVariable(self.x, [1]*k + [0]*(n-k))


class IQCQP2(ProductionTestCase):
    """Integer QCQP 2.

    Quadratic constraints are convex and have a conic representation.

    (P) min. ∑ᵢ (i·xᵢ)²
        s.t. xᵢ² + xᵢ ≤ 2 ∀ i ∈ {1, …, n}
             ∑ᵢ xᵢ = k
             x nonnegative integer vector
    """

    def setUp(self):  # noqa
        # Set the dimensionality and the parameter.
        self.n = n = 8
        self.k = k = 5

        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.IntegerVariable("x", n, lower=0)
        P.set_objective("min", sum([((i+1)*x[i])**2 for i in range(n)]))
        P.add_list_of_constraints([x[i]**2 + x[i] <= 2 for i in range(n)])
        P.add_constraint(1 | x == k)

    @staticmethod
    def f(n):
        """The sum of squares of the natural numbers up to ``n``."""
        return (n*(n+1)*(2*n+1)) // 6

    def testSolution(self):  # noqa
        # ECOS: Recurring solution failure. Almost certainly an interface bug.
        # See https://github.com/embotech/ecos-python/issues/34.
        self.knownFailure("ecos")

        n = self.n
        k = self.k
        self.primalSolve(self.P)
        self.expectObjective(self.P, self.f(k),  # HACK: Known bad precision.
            by_solver=(False if self.solver == "ecos" else None))
        self.expectVariable(self.x, [1]*k + [0]*(n-k))


class NCIQCQP1(ProductionTestCase):
    """Integer QCQP with Nonconvex Quadratic Objective 1.

    Quadratic constraints are convex and have an affine representation.

    (P) max. ∑ᵢ (i·xᵢ)²
        s.t. xᵢ² ≤ 1 ∀ i ∈ {1, …, n}
             ∑ᵢ xᵢ = k
             x nonnegative integer vector
    """

    def setUp(self):  # noqa
        # Set the dimensionality and the parameter.
        self.n = n = 8
        self.k = k = 5

        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.IntegerVariable("x", n, lower=0)
        P.set_objective("max", sum([((i+1)*x[i])**2 for i in range(n)]))
        P.add_list_of_constraints([x[i]**2 <= 1 for i in range(n)])
        P.add_constraint(1 | x == k)

    @staticmethod
    def f(n):
        """The sum of squares of the natural numbers up to ``n``."""
        return (n*(n+1)*(2*n+1)) // 6

    def testSolution(self):  # noqa
        n = self.n
        k = self.k

        self.primalSolve(self.P)
        self.expectObjective(self.P, self.f(n) - self.f(n-k))
        self.expectVariable(self.x, [0]*(n-k) + [1]*k)


class NCIQCQP2(ProductionTestCase):
    """Integer QCQP with Nonconvex Quadratic Objective 2.

    Quadratic constraints are convex and have a conic representation.

    (P) max. ∑ᵢ (i·xᵢ)²
        s.t. xᵢ² + xᵢ ≤ 2 ∀ i ∈ {1, …, n}
             ∑ᵢ xᵢ = k
             x nonnegative integer vector
    """

    def setUp(self):  # noqa
        # Set the dimensionality and the parameter.
        self.n = n = 8
        self.k = k = 5

        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.IntegerVariable("x", n, lower=0)
        P.set_objective("max", sum([((i+1)*x[i])**2 for i in range(n)]))
        P.add_list_of_constraints([x[i]**2 + x[i] <= 2 for i in range(n)])
        P.add_constraint(1 | x == k)

    @staticmethod
    def f(n):
        """The sum of squares of the natural numbers up to ``n``."""
        return (n*(n+1)*(2*n+1)) // 6

    def testSolution(self):  # noqa
        n = self.n
        k = self.k

        self.primalSolve(self.P)
        self.expectObjective(self.P, self.f(n) - self.f(n-k))
        self.expectVariable(self.x, [0]*(n-k) + [1]*k)


class ISDP(ProductionTestCase):
    """Integer SDP.

    (P) max. <X, J>
        s.t. diag(X) = 𝟙
             X ≽ 0
             X integer

    .. note:

        At the time where this test case was written, no solver supported by
        PICOS supports integer SDPs.
    """

    def setUp(self):  # noqa
        # Set the dimensionality.
        n = self.n = 4

        # Primal problem.
        self.P = P = picos.Problem()
        self.S = S = picos.SymmetricVariable("S", (n, n))
        self.X = X = picos.IntegerVariable("X", (n, n))
        P.set_objective("max", X | 1)
        P.add_constraint(picos.diag_vect(X) == 1)
        P.add_constraint(S == X)  # Make X symmetric.
        P.add_constraint(S >> 0)  # Make X psd.

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, self.n**2)
        self.expectVariable(self.X, cvxopt.matrix(1, (self.n, self.n)))
