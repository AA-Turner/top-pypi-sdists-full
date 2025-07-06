# ------------------------------------------------------------------------------
# Copyright (C)      2018 Guillaume Sagnol
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

"""Test second order cone programs.

.. note::

    This test set is for problems that explicitly use the conic representation
    of constraints.
"""

import math

import picos

from .ptest import ProductionTestCase


class SOCPLP(ProductionTestCase):
    """SOCP with Affine Constraint.

    (P) max  x + y + z
        s.t. ‖[x; y; z]‖ ≤ 1   (CS)
             3x + 2y + z ≤ 3.3 (CL)

    (D) min  3.3μ + λ
        s.t. -zₛ + [3μ; 2μ; μ]ᵀ = [1; 1; 1]ᵀ
             ‖zₛ‖ ≤ λ
             μ ≥ 0
    """

    def setUp(self):  # noqa
        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x")
        self.y = y = picos.RealVariable("y")
        self.z = z = picos.RealVariable("z")
        P.set_objective("max", x + y + z)
        self.CS = P.add_constraint(abs(x // y // z) <= 1.0)
        self.CL = self.P.add_constraint(3.0*x + 2.0*y + z <= 3.3)

        # Dual problem.
        self.D = D = picos.Problem()
        self.lb = lb = picos.RealVariable("lambda")
        self.zs = zs = picos.RealVariable("zs", 3)
        self.mu = mu = picos.RealVariable("mu", lower=0.0)
        D.set_objective("min", 3.3*mu + lb)
        D.add_constraint(-zs + (3.0*mu) // (2.0*mu) // mu == 1.0)
        D.add_constraint(abs(zs) <= lb)

        self.expX = 99.0/140.0 - math.sqrt(1866)/210.0
        self.expY = 33.0/70.0 + math.sqrt(1866)/420.0
        self.expZ = 33.0/140.0 + math.sqrt(1866)/105.0
        self.expMu = 3.0/7.0 - (33.0*math.sqrt(3.0/622.0))/7.0
        self.expLb = 10.0*math.sqrt(6.0/311.0)
        self.expZs = [-1.0+3.0*self.expMu, -1.0+2.0*self.expMu, -1.0+self.expMu]
        self.optimum = 3.3*self.expMu + self.expLb

    def testPrimal(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, self.optimum)
        self.expectVariable(self.x, self.expX)
        self.expectVariable(self.y, self.expY)
        self.expectVariable(self.z, self.expZ)

    def testDual(self):  # noqa
        self.dualSolve(self.P)
        self.readDuals(self.CS, self.lb, self.zs)
        self.readDual(self.CL, self.mu)
        self.expectObjective(self.D, self.optimum)
        self.expectVariable(self.lb, self.expLb)
        self.expectVariable(self.zs, self.expZs)
        self.expectVariable(self.mu, self.expMu)


class RSOCP(ProductionTestCase):
    """Rotated SOCP.

    (P) min  3x + 2y
        s.t. 1 ≤ xy, x ≥ 0, y ≥ 0  (C)

    (D) max  -z
        s.t. α = 3
             β = 2
             z² ≤ 4αβ
    """

    def setUp(self):  # noqa
        # Primal problem.
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x")
        self.y = y = picos.RealVariable("y")
        P.set_objective("min", 3*x + 2*y)

        # COMPAT: Force a conic constraint with both old and new expressions:
        # TODO: Replace with commented-out new expressions code below.
        self.C = P.add_constraint(
            picos.constraints.RSOCConstraint(picos.new_param("1", 1), x, y))
        # self.C = P.add_constraint((x & y & 1) << picos.rsoc())

        # Dual problem.
        self.D = D = picos.Problem()
        self.a = a = picos.RealVariable("alpha")
        self.b = b = picos.RealVariable("beta")
        self.z = z = picos.RealVariable("z")
        D.set_objective("max", -z)
        D.add_constraint(a == 3.0)
        D.add_constraint(b == 2.0)
        D.add_constraint(z**2 <= 4.0*a*b)

    def testPrimal(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, 2*6**0.5)
        self.expectVariable(self.x, (2.0/3.0)**0.5)
        self.expectVariable(self.y, (3.0/2.0)**0.5)

    def testDual(self):  # noqa
        # Low numeric precision of conic quadratic duals with Gurobi.
        # See https://gitlab.com/picos-api/picos/-/issues/283.
        self.knownFailure("gurobi")

        self.dualSolve(self.P)
        self.readDuals(self.C, self.a, self.b, self.z)
        self.expectObjective(self.D, 2*6**0.5)
        self.expectVariable(self.a, 3.0)
        self.expectVariable(self.b, 2.0)
        self.expectVariable(self.z, -2*6**0.5)


class RSOCPLP(ProductionTestCase):
    """Rotated SOCP with Affine constraint.

    (P) max  1ᵀ x - 0.3y - 0.7z
        s.t. ‖x‖² ≤ yz, y ≥ 0, z ≥ 0  (C)
             x + y ≤ 1
    (D) min  λ
        s.t. λ = α - 0.3
             λ = β - 0.7
             w + 1 = 0
             ‖w‖² ≤ 4αβ, α ≥ 0, β ≥ 0
    """

    def setUp(self):  # noqa
        self.P = P = picos.Problem()
        self.x = x = picos.RealVariable("x", 3)
        self.y = y = picos.RealVariable("y", 1)
        self.z = z = picos.RealVariable("z", 1)
        # self.C = C = P.add_constraint( abs(x)**2 <= y*z)
        self.C = C = P.add_constraint((y // z // x) << picos.rsoc(1))
        self.L = L = P.add_constraint(y+z <= 1)
        P.set_objective("max", (1 | x) - 0.3*y - 0.7*z)

        self.D = D = picos.Problem()
        self.alpha = alpha = picos.RealVariable("al", 1)
        self.beta = beta = picos.RealVariable("bt", 1)
        self.w = w = picos.RealVariable("om", 3)
        self.lb = lb = picos.RealVariable("lb", 1, lower=0)

        D.add_constraint(abs(w) ** 2 <= 4 * alpha * beta)
        D.add_constraint(w == -1)
        D.add_constraint(lb == alpha - 0.3)
        D.add_constraint(lb == beta - 0.7)
        D.set_objective("min", lb)

    def testPrimal(self):  # noqa
        self.primalSolve(self.P)
        # xopt = np.array([(25. / 316) ** 0.5] * 3)
        yopt = 1. / 2 + 1. / 79 ** 0.5
        zopt = 1. / 2 - 1. / 79 ** 0.5
        self.expectObjective(self.P, 0.1*(79**0.5-2) - 0.3)
        self.expectVariable(self.y, yopt)
        self.expectVariable(self.z, zopt)

    def testDual(self):  # noqa
        self.dualSolve(self.P)
        self.readDuals(self.C, self.alpha, self.beta, self.w)
        self.readDual(self.L, self.lb)
        self.readDual(self.L, self.lb)
        alopt = 0.1 * (79 ** 0.5 - 2)
        btopt = alopt + 0.4
        lbopt = alopt - 0.3
        self.expectVariable(self.alpha, alopt)
        self.expectVariable(self.beta, btopt)
        self.expectVariable(self.lb, lbopt)
