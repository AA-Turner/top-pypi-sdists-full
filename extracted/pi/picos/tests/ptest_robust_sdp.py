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

"""Test robust counterparts of SDPs affected by uncertainty in the data."""

import numpy as np

import picos
import picos.uncertain

from .ptest import ProductionTestCase


class SCENUNCSDP(ProductionTestCase):
    """SDP with scalar scenario uncertainty.

    This problem asks for the largest eigenvalue of a matrix with a positive,
    scenario-uncertain, scalar coefficient. While scalar scenario uncertainty is
    not so interesting, this should still test a good deal of the relevant code.
    """

    def setUp(self):  # noqa
        np.random.seed(23)
        self.n = n = 4
        self.I = picos.Constant("I", "I", (n, n))
        self.A = picos.Constant(np.random.randn(n, n))\
            .hermitianized.renamed("A")
        self.P = P = picos.Problem()
        self.t = t = picos.RealVariable("t")
        P.set_objective("min", t)

    def testNominal(self):  # noqa
        I, A, P, t = self.I, self.A, self.P, self.t

        P.add_constraint(A << t*I)

        self.primalSolve(P)
        lambda_max = float(max(np.linalg.eigvals(A.value)))
        self.expectObjective(self.P, lambda_max)

    def _test_robust(self, variant):  # noqa
        assert variant in range(4)

        I, A, P, t = self.I, self.A, self.P, self.t

        S = picos.uncertain.ScenarioPerturbationSet("s", [2, 3, 4.5])
        s = S.parameter

        if variant == 0:
            # Matrix in cone.
            P.add_constraint(t*I - s*A << picos.PositiveSemidefiniteCone())
        elif variant == 1:
            # Vectorized matrix in cone.
            P.add_constraint(
                (t*I - s*A).svec << picos.PositiveSemidefiniteCone())
        elif variant == 2:
            # Linear matrix inequality (lower or equal).
            P.add_constraint(s*A << t*I)
        elif variant == 3:
            # Linear matrix inequality (greater or equal).
            P.add_constraint(t*I >> s*A)

        self.primalSolve(P)
        lambda_max = float(max(np.linalg.eigvals(A.value)))
        opt = max(S.scenarios.matrix.value_as_matrix)*lambda_max
        self.expectObjective(self.P, opt)

    def testRobust1(self):  # noqa
        self._test_robust(0)

    def testRobust2(self):  # noqa
        self._test_robust(1)

    def testRobust3(self):  # noqa
        self._test_robust(2)

    def testRobust4(self):  # noqa
        self._test_robust(3)
