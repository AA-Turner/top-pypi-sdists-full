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

"""Test problems featuring maximums and minimums."""

import picos

from .ptest import ProductionTestCase


class MAXCVX(ProductionTestCase):
    """Minimize the maximum of convex functions."""

    def setUp(self):  # noqa
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x", 2, lower=2)
        P.set_objective("min", picos.max([
            abs(x),
            abs(2*x),
            picos.sum(x),
            x[0]-x[1]
        ]))

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, 32**0.5)  # abs(2*x) attains the maximum.


class MINCCV(ProductionTestCase):
    """Maximize the minimum of concave functions."""

    def setUp(self):  # noqa
        self.knownFailure("gurobi")  # Does not converge for default tolerance.

        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x", 2, upper=-3)
        P.set_objective("max", picos.min([
            -x[0]**2,
            picos.sum(x),
            x[0]-x[1]
        ]))

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, -9)  # -x[0]**2 attains the minium.
