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

"""Test infeasible, unbounded and other anomalous problems."""

import picos

from .ptest import ProductionTestCase


class NOCON(ProductionTestCase):
    """An unbounded problem with no constraints."""

    def setUp(self):  # noqa
        self.P = P = picos.Problem()
        x = picos.RealVariable("x")
        P.set_objective("min", x)

    def testSolution(self):  # noqa
        self.unboundedSolve(self.P)


class NOCON_BOUNDED(ProductionTestCase):
    """A problem with no constraint but with a variable bound."""

    def setUp(self):  # noqa
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x", lower=5)
        P.set_objective("min", x)

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, 5)
        self.expectVariable(self.x, 5)


class DUMMY(ProductionTestCase):
    """An unbounded problem with only a dummy constraint."""

    def setUp(self):  # noqa
        self.P = P = picos.Problem()
        x = picos.RealVariable("x")
        P.set_objective("min", x)
        P.add_constraint(x << picos.TheField())

    def testSolution(self):  # noqa
        self.unboundedSolve(self.P)


class DUMMY_BOUNDED(ProductionTestCase):
    """A problem with only a dummy constraint but with a variable bound."""

    def setUp(self):  # noqa
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x", lower=5)
        P.set_objective("min", x)
        P.add_constraint(x << picos.TheField())

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, 5)
        self.expectVariable(self.x, 5)


class DUMMYVAR(ProductionTestCase):
    """A problem with a gratuitous variable (via dummy constraint)."""

    def setUp(self):  # noqa
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x")
        self.y = y = picos.RealVariable("y")
        P.set_objective("min", x)
        P.add_constraint(x >= 5)
        P.add_constraint(y << picos.TheField())

    def testSolution(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, 5)
        self.expectVariable(self.x, 5)
        self.assertIsNotNone(self.y.value)


class INFCLP(ProductionTestCase):
    """A simple LP with infeasible constraints."""

    def setUp(self):  # noqa
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x")
        self.y = y = picos.RealVariable("y")
        P.set_objective("min", x)
        self.C  = P.add_constraint(x < y)
        self.Cx = P.add_constraint(x > 2)
        self.Cy = P.add_constraint(y < -2)

    def testSolution(self):  # noqa
        self.infeasibleSolve(self.P)


class INFBLP(ProductionTestCase):
    """A simple LP with infeasible variable bounds."""

    def setUp(self):  # noqa
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x", lower=2)
        self.y = y = picos.RealVariable("y", upper=-2)
        P.set_objective("min", x)
        self.C = P.add_constraint(x < y)

    def testSolution(self):  # noqa
        self.infeasibleSolve(self.P)


class UNBLP(ProductionTestCase):
    """A simple LP that is unbounded."""

    def setUp(self):  # noqa
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x")
        self.C = P.add_constraint(x < 0)
        P.set_objective("min", x)

    def testSolution(self):  # noqa
        self.unboundedSolve(self.P)
