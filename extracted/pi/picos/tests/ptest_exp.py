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

"""Test problems with exponential and logarithmic constraints and objectives."""

import math

import picos

from .ptest import ProductionTestCase


class NGP(ProductionTestCase):
    """Geometric Program with Nonlinear Objective.

    This is the "GP" test of the old test_picos.py. Note that the constraints
    simplify to x + 2y = 0.

    (P) min. log(exp(x - y) + exp(-x + y + log(2)))
        s.t. log(exp( x + 2y)) ≤ 0
             log(exp(-x - 2y)) ≤ 0
    """

    def setUp(self):  # noqa
        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x")
        self.y = y = picos.RealVariable("y")
        P.set_objective("min", picos.lse((x - y) & (-x + y + math.log(2))))
        P.add_constraint(picos.lse( x + 2*y) <= 0)  # noqa
        P.add_constraint(picos.lse(-x - 2*y) <= 0)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, (3.0/2.0)*math.log(2))
        self.expectVariable(self.x,  math.log(2)/3.0)
        self.expectVariable(self.y, -math.log(2)/6.0)


class LGP(ProductionTestCase):
    """Geometric Program with Linear Objective.

    This is a reformulation of NLGP, with a linear objective function.

    (P) min. t
        s.t. log(exp(x - y - t) + exp(-x + y + log(2) - t)) ≤ 0
             log(exp( x + 2y)) ≤ 0
             log(exp(-x - 2y)) ≤ 0
    """

    def setUp(self):  # noqa
        # Primal problem.
        self.P = P = picos.Problem()
        self.t = t = picos.RealVariable("t")
        self.x = x = picos.RealVariable("x")
        self.y = y = picos.RealVariable("y")
        P.set_objective("min", t)
        P.add_constraint(
            picos.lse((x - y - t) & (-x + y + math.log(2) - t)) <= 0)
        P.add_constraint(picos.lse( x + 2*y) <= 0)  # noqa
        P.add_constraint(picos.lse(-x - 2*y) <= 0)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, (3.0/2.0)*math.log(2))
        self.expectVariable(self.t,  (3.0/2.0)*math.log(2))
        self.expectVariable(self.x,  math.log(2)/3.0)
        self.expectVariable(self.y, -math.log(2)/6.0)


class EGP(ProductionTestCase):
    """Epigraph Reformulation of a Geometric Program.

    This is an epigraph reformulation of NLGP.

    (P) min. t
        s.t. log(exp(x - y) + exp(-x + y + log(2))) ≤ t
             log(exp( x + 2y)) ≤ 0
             log(exp(-x - 2y)) ≤ 0
    """

    def setUp(self):  # noqa
        # Primal problem.
        self.P = P = picos.Problem()
        self.t = t = picos.RealVariable("t")
        self.x = x = picos.RealVariable("x")
        self.y = y = picos.RealVariable("y")
        P.set_objective("min", t)
        P.add_constraint(
            picos.lse((x - y) & (-x + y + math.log(2))) <= t)
        P.add_constraint(picos.lse( x + 2*y) <= 0)  # noqa
        P.add_constraint(picos.lse(-x - 2*y) <= 0)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, (3.0/2.0)*math.log(2))
        self.expectVariable(self.t,  (3.0/2.0)*math.log(2))
        self.expectVariable(self.x,  math.log(2)/3.0)
        self.expectVariable(self.y, -math.log(2)/6.0)


class ECP(ProductionTestCase):
    """Exponential Cone Program.

    In the following p is a scalar and Kₑ is the exponential cone. Note that
    the constraint (C) is equivalent to eˣ ≤ p so that the solution is ln(p).

    (P) max. x
        s.t. [p; 1; x] ∈ Kₑ (C)

    (D) min. p·r + s
        s.t. [r; s; t] ∈ Kₑ*
    """

    def setUp(self):  # noqa
        # Problem parameters.
        self.exponent = 10

        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x")
        P.set_objective("max", x)
        self.C = P.add_constraint(
            self.exponent // (1.0 // x) << picos.expcone())

    def testPrimal(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, math.log(self.exponent))
        self.expectVariable(self.x,  math.log(self.exponent))

    def testDual(self):  # noqa
        self.dualSolve(self.P)
        r, s, t = self.C.dual

        # Check feasibility, that is check if the dual value is in the dual
        # exponential cone cl{(r,s,t) | r ≥ -t*exp((t - s) / -t), t < 0}.
        m = "Infeasible."
        if t >= 0.0:
            self.assertGreaterEqual(r, 0.0, msg=m)
            self.assertGreaterEqual(s, 0.0, msg=m)
            self.assertAlmostEqual(t, 0.0, places=self.to.varPlaces, msg=m)
        else:
            self.assertGreaterEqual(r, -t*math.exp((t - s) / -t), msg=m)
            self.assertLess(t, 0, msg=m)

        # Check the objective value.
        self.assertAlmostEqual(self.exponent*r + s, math.log(self.exponent),
            places=self.to.objPlaces, msg="Objective value.")


class LBSOEP(ProductionTestCase):
    """Linearly Bounded Sum Of Exponentials Program.

    In the following p is a scalar.

    (P) max. x + y
        s.t. eˣ + eʸ ≤ p
    """

    def setUp(self):  # noqa
        # Problem parameters.
        self.bound = 10.0

        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x")
        self.y = y = picos.RealVariable("y")
        P.set_objective("max", x + y)
        P.add_constraint(picos.exp(x) + picos.exp(y) <= self.bound)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, 2.0 * math.log(self.bound / 2.0))
        self.expectVariable(self.x,  math.log(self.bound / 2.0))
        self.expectVariable(self.y,  math.log(self.bound / 2.0))


class EBSOEP(ProductionTestCase):
    """Exponentially Bounded Sum Of Exponentials Program.

    (P) min. x + y
        s.t. eˣ + eʸ ≤ eˣ⁺ʸ
    """

    def setUp(self):  # noqa
        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x")
        self.y = y = picos.RealVariable("y")
        P.set_objective("min", x + y)
        P.add_constraint(picos.exp(x) + picos.exp(y) <= picos.exp(x + y))

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, math.log(4.0))
        self.expectVariable(self.x,  math.log(4.0) / 2.0)
        self.expectVariable(self.y,  math.log(4.0) / 2.0)


class SOPEP(ProductionTestCase):
    """Sum Of Perspectives of Exponentials Program.

    In the following p and q are scalars.

    (P) max. x + y
        s.t. q·exp(x/q) + q·exp(y/q) ≤ p
    """

    def setUp(self):  # noqa
        # Problem parameters.
        self.p = 10.0
        self.q = 3.0

        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x")
        self.y = y = picos.RealVariable("y")
        P.set_objective("max", x + y)
        P.add_constraint(picos.sumexp(x // y, self.q) <= self.p)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(
            self.P, 2.0 * self.q * math.log(self.p / (2.0 * self.q)))
        self.expectVariable(self.x, self.q * math.log(self.p / (2.0 * self.q)))
        self.expectVariable(self.y, self.q * math.log(self.p / (2.0 * self.q)))


class SSNEP(ProductionTestCase):
    """Single-Summand Negative Entropy Program.

    (P) max. x
        s.t. x·log(x) ≤ 10
    """

    SOLUTION = 5.728925565386941508394833446269542858308301124518867997774
    """This is an approximation of e^W(10) where W is the Lambert W function."""

    def setUp(self):  # noqa
        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x")
        P.set_objective("max", x)
        P.add_constraint(picos.kullback_leibler(x) <= 10.0)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, self.SOLUTION)
        self.expectVariable(self.x, self.SOLUTION)


class NEP(ProductionTestCase):
    """Negative Entropy Program.

    (P) max. x + y
        s.t. x·log(x) + y·log(y) ≤ 10
    """

    XANDY = 3.768679463788535951475214706121251188708578998076632057977
    """This is an approximation of e^W(5) where W is the Lambert W function."""

    def setUp(self):  # noqa
        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x")
        self.y = y = picos.RealVariable("y")
        P.set_objective("max", x + y)
        P.add_constraint(picos.kullback_leibler(x // y) <= 10.0)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, 2.0 * self.XANDY)
        self.expectVariable(self.x, self.XANDY)
        self.expectVariable(self.y, self.XANDY)


class SSKLP(ProductionTestCase):
    """Single-Summand Kullback-Leibler divergence Program.

    (P) max. x
        s.t. x·log(x/3) ≤ 10
    """

    SOLUTION = 9.053526107742896756286643429465331153730743401904911644773
    """This is an approx. of 3·e^W(10/3) where W is the Lambert W function."""

    def setUp(self):  # noqa
        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x")
        P.set_objective("max", x)
        P.add_constraint(picos.kullback_leibler(x, 3.0) <= 10.0)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, self.SOLUTION)
        self.expectVariable(self.x, self.SOLUTION)


class KLP(ProductionTestCase):
    """Kullback-Leibler divergence Program.

    (P) max. x + y
        s.t. x·log(x/3) + y·log(y/3) ≤ 10
    """

    XANDY = 6.485477862082042277719097762844596655406564816196389529323
    """This is an approx. of 3·e^W(5/3) where W is the Lambert W function."""

    def setUp(self):  # noqa
        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x")
        self.y = y = picos.RealVariable("y")
        P.set_objective("max", x + y)
        P.add_constraint(picos.kullback_leibler(x // y, 3.0) <= 10.0)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, 2.0 * self.XANDY)
        self.expectVariable(self.x, self.XANDY)
        self.expectVariable(self.y, self.XANDY)


class LOGP(ProductionTestCase):
    """Logarithmic Program.

    In the following p is a scalar.

    (P) min. x
        s.t. log(x) ≥ p
    """

    def setUp(self):  # noqa
        # Problem parameters.
        self.bound = 2

        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x")
        P.set_objective("min", x)
        P.add_constraint(picos.log(x) >= self.bound)

    def testSolution(self):  # noqa
        solution = math.exp(self.bound)
        self.primalSolve(self.P)
        self.expectObjective(self.P, solution)
        self.expectVariable(self.x, solution)
