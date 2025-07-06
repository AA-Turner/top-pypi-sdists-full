# ------------------------------------------------------------------------------
# Copyright (C) 2020 Maximilian Stahlberg
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

"""Test robust counterparts of LPs affected by uncertainty in the data."""

import cvxopt

import picos
import picos.uncertain

from .ptest import ProductionTestCase


class AFFUNCOBJLP(ProductionTestCase):
    """LP with affine uncertainty in the objective.

    (N) max. 4x + 3y
        s.t. x, y ≥ 0
             x + y ≤ 1

    (R) max. min_{(u, v) ∈ U} (4 + u)x + (3 + v)y
        s.t. x, y ≥ 0
             x + y ≤ 1
        for  U = {(u, v) | -3 ≤ u ≤ 3 ∧ -1 ≤ v ≤ 1}
    """

    def setUp(self):  # noqa
        self.P = P = picos.Problem()
        self.xy = xy = picos.RealVariable("xy", 2, lower=0)
        self.c = c = [4, 3]

        self.nominal_objective = (c | xy)

        P.add_constraint(picos.sum(xy) <= 1)

    def testNominal(self):  # noqa
        self.P.set_objective("max", self.nominal_objective)

        self.primalSolve(self.P)
        self.expectObjective(self.P, 4)
        self.expectVariable(self.xy, [1, 0])

    def _test_robust(self, via_bounds):
        if via_bounds:
            # Model uncertainty via bound constraints.
            U = picos.uncertain.ConicPerturbationSet("uv", 2)
            U.bound(abs(U.element[0]) <= 3)
            U.bound(abs(U.element[1]) <= 1)
            uv = U.compile()
        else:
            # Model uncertainty via scenarios.
            U = picos.uncertain.ScenarioPerturbationSet("uv", (
                (-3, -1), (-3, 1), (3, -1), (3, 1)), compute_hull=False)
            uv = U.parameter

        self.P.set_objective("max", (self.c + uv) | self.xy)

        self.primalSolve(self.P)
        self.expectObjective(self.P, 2)  # Worst case.
        self.expectExpression(self.nominal_objective, 3)  # Nominal case.
        self.expectVariable(self.xy, [0, 1])

    def testRobust1(self):  # noqa
        self._test_robust(True)

    def testRobust2(self):  # noqa
        self._test_robust(False)


class AFFUNCCONLP(ProductionTestCase):
    """LP with single affine uncertainty in two constraints.

    (N) max. ∑(x) + ∑(y)
        s.t. x, y ≤ 2

    (R) max. ∑ᵢ(xᵢ + yᵢ)
        s.t. x + u       ≤ 2 ∀ u ∈ U  (Additive uncertainty)
             y ^ (1 + u) ≤ 2 ∀ u ∈ U  (Multiplicative uncertainty)
        for  U = {u | u ≥ 0 ∧ ∑(u) ≤ 1}
    """

    def setUp(self):  # noqa
        self.n = n = 4
        self.x = x = picos.RealVariable("x", n)
        self.y = y = picos.RealVariable("y", n)
        self.P = P = picos.Problem()

        P.set_objective("max", picos.sum(x) + picos.sum(y))

    def testNominal(self):  # noqa
        P, n, x, y = self.P, self.n, self.x, self.y

        C = P.add_constraint(x // y <= 2)

        self.primalSolve(P)
        self.expectObjective(P, 4*n)
        self.expectVariable(x, [2]*n)
        self.expectVariable(y, [2]*n)
        self.expectSlack(C, [0]*(2*n))

    def _test_robust(self, via_bounds, via_comparison):
        P, n, x, y = self.P, self.n, self.x, self.y

        if via_bounds:
            # Model uncertainty via bound constraints.
            U = picos.uncertain.ConicPerturbationSet("u", n)
            U.bound(U.element << picos.Simplex())
            u = U.compile()
        else:
            # Model uncertainty via scenarios.
            U = picos.uncertain.ScenarioPerturbationSet("u", [[0]*n]
                + [cvxopt.spmatrix([1], [i], [0], (n, 1)) for i in range(n)],
                compute_hull=False)
            u = U.parameter

        if via_comparison:
            # Input constraints via the <= operator.
            C1 = P.add_constraint(x + u <= 2)
            C2 = P.add_constraint(y ^ (1 + u) <= 2)
        else:
            # Input constraints as set membership.
            C1 = P.add_constraint(2 - (x + u) << picos.NonnegativeOrthant())
            C2 = P.add_constraint(
                2 - (y ^ (1 + u)) << picos.NonnegativeOrthant())

        self.primalSolve(P)
        self.expectObjective(P, 2*n)
        self.expectVariable(x, [1]*n)
        self.expectVariable(y, [1]*n)
        self.expectSlack(C1, [0]*n)
        self.expectSlack(C2, [0]*n)

    def testRobust1(self):  # noqa
        self._test_robust(True, True)

    def testRobust2(self):  # noqa
        self._test_robust(True, False)

    def testRobust3(self):  # noqa
        self._test_robust(False, True)

    def testRobust4(self):  # noqa
        self._test_robust(False, False)


class BUDGETUNCOBJLP(ProductionTestCase):
    """LP with budgeted uncertainty in the objective.

    The problem is constructed as follows:

    1. The initial objective is to maximize the sum over an n-dimensional
       decision vector, with n even, which is bounded from above by a range.
       The unique nominal optimal solution is thus equal to that bound.
    2. Uncertainty is added in the form of an adversary who has a total budget
       of n/2 that they may decrease the objective coefficients by, but each
       coefficient may be decreased by at most one to then equal zero. It is
       thus optimal for the adversary to select the n/2 largest elements in the
       decision vector and zero their corresponding objective coefficients.
    3. The nominal optimal solution remains robust optimal, but its n/2 largets
       elements may be decreased without violating optimality as far as they
       remain the largest elements. A regulization term is introduced to
       encourage such a decrease. This makes the optimal robust solution unique.
    """

    def setUp(self):  # noqa
        self.n = n = 8
        assert n % 2 == 0
        self.N = n // 2  # Budget.
        self.b = b = picos.Constant(range(1, n + 1))
        self.x = x = picos.RealVariable("x", n)
        self.t = t = picos.RealVariable("t")
        self.P = P = picos.Problem()

        P.add_constraint(x <= b)
        P.add_constraint(t >= (1.0/n)*picos.max(x))

    def testNominal(self):  # noqa
        P, b, x = self.P, self.b, self.x

        P.set_objective("max", (1 | x) - self.t)

        self.primalSolve(P)
        self.expectObjective(P, sum(b.value) - self.t.value)
        self.expectVariable(x, b.value)

    def testRobust(self):  # noqa
        P, N, n, b, x = self.P, self.N, self.n, self.b, self.x

        U = picos.uncertain.ConicPerturbationSet("u", n)
        U.bound(picos.norm(U.element - 1, float("inf")) <= 1)
        U.bound(picos.norm(U.element - 1, 1) <= N)
        u = U.compile()

        P.set_objective("max", (u | x) - self.t)

        self.primalSolve(P)
        self.expectObjective(P, sum(b[:N].value) - self.t.value)
        self.expectExpression(x, list(b[:N].value) + [N]*N)


class BALLUNCLP(ProductionTestCase):
    """LP with single ball uncertainty in objective and constraints.

    The nominal problem asks for the nonpositive corner point of a two-wide,
    n-dimensional box. The uncertain problem requires the point to have a unit
    ball safety margin from the box. The objective is evaluated with respect to
    the worst case location within that ball, which does not affect the optimal
    solution but its value.

    (N) min. ∑(x)
        s.t. ‖x‖_∞ ≤ 2

    (R) min. max_{b ∈ B} ∑(x + b)
        s.t. +(x + b) ≤ 2 ∀ b ∈ B
             -(x + b) ≤ 2 ∀ b ∈ B
        for  B = {b | ‖b‖ ≤ 1}
    """

    def setUp(self):  # noqa
        self.n = n = 4
        self.x = picos.RealVariable("x", n)
        self.P = picos.Problem()

    def testNominal(self):  # noqa
        P, n, x = self.P, self.n, self.x

        P.set_objective("min", picos.sum(x))
        P.add_constraint(picos.Norm(x, float("inf")) <= 2)

        self.primalSolve(P)
        self.expectObjective(P, -2*n)
        self.expectVariable(x, [-2]*n)

    def testRobust(self):  # noqa
        P, n, x = self.P, self.n, self.x

        B = picos.uncertain.ConicPerturbationSet("b", n)
        B.bound(abs(B.element) <= 1)
        u = x + B.compile()

        P.set_objective("min", picos.sum(u))
        P.add_constraint(+u <= 2)
        P.add_constraint(-u <= 2)

        self.primalSolve(P)
        self.expectObjective(P, -n + n**0.5)  # Worst case.
        self.expectExpression(picos.sum(x), -n)  # Nominal case.
        self.expectVariable(x, [-1]*n)


class DRUGS(ProductionTestCase):
    """Ben-Tal et al. introductory example.

    Implements the robust linear program introductory example found in
    "Robust Optimization" (Ben-Tal, El Ghaoui, Nemirobvski, 2009).
    """

    def setUp(self):  # noqa
        # The book is accurate to three decimal places.
        self.to.objPlaces = 3
        self.to.varPlaces = 3

        # Variables.
        self.Raw  = picos.RealVariable("Raw",  2, lower=0)
        self.Drug = picos.RealVariable("Drug", 2, lower=0)

        # Drug data.                                      DrugI  DrugII
        self.SellPrice   = picos.Constant("SellPrice",   [6200,  6900])
        self.AgentNeeded = picos.Constant("AgentNeeded", [0.5,   0.6])
        self.WorkNeeded  = picos.Constant("WorkNeeded",  [90,    100])
        self.EquipNeeded = picos.Constant("EquipNeeded", [40,    50])
        self.ProdCost    = picos.Constant("ProdCost",    [700,   800])

        # Raw material data.                              RawI  RawII
        self.PurchPrice  = picos.Constant("PurchPrice",  [100,  199.9])
        self.AgentProv   = picos.Constant("AgentProv",   [0.01, 0.02])

        # Production resources.
        self.Budget      = picos.Constant("Budget",       100000)
        self.WorkHours   = picos.Constant("WorkHours",    2000)
        self.EquipHours  = picos.Constant("EquipHours",   800)
        self.RawStorage  = picos.Constant("RawStorage",   1000)

        # Uncertainty: 0.5%/2% margin for agent provided by RawI/RawII.
        AgentProvMargins = picos.uncertain.ConicPerturbationSet("Margins", 2)
        AgentProvMargins.bound(abs(AgentProvMargins.element[0] - 1) <= 0.005)
        AgentProvMargins.bound(abs(AgentProvMargins.element[1] - 1) <= 0.02)
        self.UncAgentProv = self.AgentProv ^ AgentProvMargins.compile()

    def _make_problem(self, nominal):
        P = picos.Problem()

        Raw, Drug   = self.Raw, self.Drug
        SellPrice   = self.SellPrice
        AgentNeeded = self.AgentNeeded
        WorkNeeded  = self.WorkNeeded
        EquipNeeded = self.EquipNeeded
        ProdCost    = self.ProdCost
        PurchPrice  = self.PurchPrice
        AgentProv   = self.AgentProv if nominal else self.UncAgentProv
        Budget      = self.Budget
        WorkHours   = self.WorkHours
        EquipHours  = self.EquipHours
        RawStorage  = self.RawStorage

        P.set_objective("max",
            (SellPrice | Drug) - (PurchPrice | Raw) - (ProdCost | Drug))

        P.add_constraint((AgentNeeded | Drug) <= (AgentProv | Raw))
        P.add_constraint(picos.sum(Raw) <= RawStorage)
        P.add_constraint((WorkNeeded | Drug) <= WorkHours)
        P.add_constraint((EquipNeeded | Drug) <= EquipHours)
        P.add_constraint((PurchPrice | Raw) + (ProdCost | Drug) <= Budget)

        return P

    def testNominal(self):  # noqa
        if "dualize" in self.options and self.options["dualize"]:
            self.knownFailure("cvxopt")  # Bad precision.
            self.knownFailure("osqp")  # Bad precision (no polishing of duals).

        P = self._make_problem(nominal=True)
        self.primalSolve(P)
        self.expectObjective(P, 8819.658)
        self.expectVariable(self.Raw, [0, 438.789])
        self.expectVariable(self.Drug, [17.552, 0])

    def testRobust(self):  # noqa
        if "dualize" in self.options and self.options["dualize"]:
            self.knownFailure("cvxopt")  # Solution failure with CVXOPT only.

        self.knownFailure("osqp")  # Takes far too long.

        P = self._make_problem(nominal=False)
        self.primalSolve(P)
        self.expectObjective(P, 8294.567)
        self.expectVariable(self.Raw, [877.732, 0])
        self.expectVariable(self.Drug, [17.467, 0])
