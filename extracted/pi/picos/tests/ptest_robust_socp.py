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

"""Test robust counterparts of SOCPs affected by uncertainty in the data."""

import picos
import picos.uncertain

from .ptest import ProductionTestCase


class BALLUNCSOCP(ProductionTestCase):
    """SOCP with unit ball uncertainty."""

    def setUp(self):  # noqa
        self.n = n = 4
        self.x = x = picos.RealVariable("x", n)
        self.P = P = picos.Problem()

        P.set_objective("max", picos.sum(x))

    def testNominal(self):  # noqa
        P, n, x = self.P, self.n, self.x

        P.add_constraint(abs(x) <= 2)

        self.primalSolve(P)
        self.expectObjective(P, 2*(n**(-0.5))*n)
        self.expectVariable(x, [2*(n**(-0.5))]*n)

    def _test_robust(self, explicit_ball, certain_ub, via_norm):
        P, n, x = self.P, self.n, self.x

        assert certain_ub or via_norm

        if explicit_ball:
            # Explicit unit ball uncertainty.
            b = picos.uncertain.UnitBallPerturbationSet("b", n).parameter
        else:
            # Implicit unit ball uncertainty.
            B = picos.uncertain.ConicPerturbationSet("b", n)
            B.bound(5*abs(3*B.element) <= 5)
            b = 3*B.compile()

        if certain_ub:
            # Upper bound is certain.
            ub = 2
        else:
            # Upper bound is the interval [2, 4] defined via ball uncertainty.
            C = picos.uncertain.UnitBallPerturbationSet("c", 1)
            c = C.parameter
            ub = 3 + c

        if via_norm:
            # Define the constraint by upper bounding a norm.
            P.add_constraint(abs(x + b) <= ub)
        else:
            # Define the conic constraint explicitly.
            P.add_constraint((ub // (x + b)) << picos.SecondOrderCone())

        self.primalSolve(P)
        self.expectObjective(P, (n**(-0.5))*n)
        self.expectVariable(x, [(n**(-0.5))]*n)

    def testRobust1(self):  # noqa
        self._test_robust(False, False, True)

    def testRobust2(self):  # noqa
        self._test_robust(False, True, False)

    def testRobust3(self):  # noqa
        self._test_robust(False, True, True)

    def testRobust4(self):  # noqa
        self._test_robust(True, False, True)

    def testRobust5(self):  # noqa
        self._test_robust(True, True, False)

    def testRobust6(self):  # noqa
        self._test_robust(True, True, True)


class SCENUNCSOCP(ProductionTestCase):
    """SOCP with scenario uncertainty.

    See also :class:`SCENUNCOLS` which is almost equivalent in a mathematical
    sense but tests different code sections.

    (N) min. ‖x - (1, 1)‖

    (R) min. max_{s ∈ S} ‖x + s - [1; 1]‖
        for  S = conv({(3, 0), (-1, 0), (0, 1), (0, -1)})
    """

    def setUp(self):  # noqa
        self.x = x = picos.RealVariable("x", 2)
        self.t = t = picos.Constant("t", (1, 1))
        self.P = picos.Problem()

        self.nominal_objective = abs(x - t)

    def testNominal(self):  # noqa
        P, x = self.P, self.x

        P.set_objective("min", self.nominal_objective)

        self.primalSolve(P)
        self.expectObjective(P, 0)
        self.expectVariable(x, (1, 1))

    def _test_robust(self, in_obj):
        P, x, t = self.P, self.x, self.t

        S = picos.uncertain.ScenarioPerturbationSet("s",
            [(3, 0), (-1, 0), (0, 1), (0, -1)])
        s = S.parameter

        if in_obj:
            # Pass objective directly using abs().
            P.set_objective("min", abs((x + s) - t))
        else:
            # Pass objective via epigraph reformulation using conic membership.
            y = picos.RealVariable("y")
            P.set_objective("min", y)
            P.add_constraint((y // ((x + s) - t) << picos.SecondOrderCone()))

        self.primalSolve(P)
        self.expectObjective(P, 2)
        self.expectExpression(self.nominal_objective, 1)
        self.expectVariable(x, (0, 1))

    def testRobust1(self):  # noqa
        self._test_robust(True)

    def testRobust2(self):  # noqa
        self._test_robust(False)


class SCENUNCOLS(ProductionTestCase):
    """Ordinary least squares with scenario uncertainty.

    See also :class:`SCENUNCSOCP` which is almost equivalent in a mathematical
    sense but tests different code sections.

    (N) min. ‖x - (1, 1)‖²

    (R) min. max_{s ∈ S} ‖x + s - [1; 1]‖²
        for  S = conv({(3, 0), (-1, 0), (0, 1), (0, -1)})
    """

    def setUp(self):  # noqa
        self.x = x = picos.RealVariable("x", 2)
        self.t = t = picos.Constant("t", (1, 1))
        self.P = picos.Problem()

        self.nominal_objective = abs(x - t)**2

    def testNominal(self):  # noqa
        P, x = self.P, self.x

        P.set_objective("min", self.nominal_objective)

        self.primalSolve(P)
        self.expectObjective(P, 0)
        self.expectVariable(x, (1, 1))

    def _test_robust(self, in_obj):
        P, x, t = self.P, self.x, self.t

        S = picos.uncertain.ScenarioPerturbationSet("s",
            [(3, 0), (-1, 0), (0, 1), (0, -1)])
        s = S.parameter

        if in_obj:
            # Pass objective directly using abs().
            P.set_objective("min", abs((x + s) - t)**2)
        else:
            # Pass objective via epigraph reformulation using conic membership.
            y = picos.RealVariable("y")
            P.set_objective("min", y)
            P.add_constraint(
                (y // 1 // ((x + s) - t) << picos.RotatedSecondOrderCone()))

        self.primalSolve(P)
        self.expectObjective(P, 2**2)
        self.expectExpression(self.nominal_objective, 1**2)
        self.expectVariable(x, (0, 1))

    def testRobust1(self):  # noqa
        self._test_robust(True)

    def testRobust2(self):  # noqa
        self._test_robust(False)
