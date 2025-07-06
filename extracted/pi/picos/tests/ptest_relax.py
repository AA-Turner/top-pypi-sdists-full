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

"""Test SDP relaxations of NP-hard problems."""

import numpy as np

import picos

from .ptest import ProductionTestCase


class MAXWSS(ProductionTestCase):
    """SDP relaxation of Max Weighted Stable Set.

    We solve the IP version of this problem, and the first round of its Lasserre
    Hierarchy.
    """

    SLOW = True

    def setUp(self):  # noqa
        self.E = E = [
            (0, 14), (1, 4), (1, 5), (1, 9), (1, 14), (1, 15), (1, 16), (2, 5),
            (2, 12), (2, 16), (2, 18), (3, 4), (3, 6), (3, 9), (3, 11), (3, 17),
            (4, 7), (4, 13), (5, 8), (6, 9), (6, 12), (6, 15), (6, 18), (6, 19),
            (7, 8), (7, 16), (8, 11), (8, 17), (8, 18), (9, 11), (9, 12),
            (9, 16), (10, 11), (10, 12), (10, 14), (11, 13), (11, 14), (11, 16),
            (12, 13), (12, 14), (12, 16), (13, 17), (14, 16), (15, 18),
            (16, 17), (16, 18), (16, 19), (17, 18)]
        self.n = n = 20
        seed = 553995
        np.random.seed(seed)
        self.w = w = np.random.randint(0, 100, n)

        self.IP = IP = picos.Problem()
        self.x = x = picos.BinaryVariable('x', n)
        for i, j in E:
            IP.add_constraint(x[i] + x[j] <= 1)
        IP.set_objective('max', (w | x))

        self.P0 = P0 = picos.Problem()
        x0 = self.x0 = picos.RealVariable('x', n)
        X0 = self.X0 = picos.SymmetricVariable('X', (n, n))
        P0.add_constraint(((X0 & x0)//(x0.T & 1)) >> 0)
        for i in range(n):
            P0.add_constraint(X0[i, i] == x0[i])
        for i, j in E:
            P0.add_constraint(X0[i, j] == 0)
        P0.set_objective('max', (w | x0))

    def testOriginal(self):  # noqa
        self.primalSolve(self.IP)
        self.expectObjective(self.IP, 450.)

    def testRelaxation(self):  # noqa
        self.to.objPlaces = 5
        self.primalSolve(self.P0)
        self.expectObjective(self.P0, 461.65607)


class MAX3CUT(ProductionTestCase):
    """Complex SDP relaxation of Max3Cut."""

    SLOW = True

    def setUp(self):  # noqa
        self.E = E = [
            (0, 14), (1, 4), (1, 5), (1, 9), (1, 14), (1, 15), (1, 16), (2, 5),
            (2, 12), (2, 14), (2, 16), (3, 4), (3, 6), (3, 9), (3, 11), (3, 15),
            (4, 7), (4, 13), (5, 8), (6, 9), (6, 12), (6, 15), (6, 16), (7, 8),
            (7, 16), (8, 11), (8, 14), (9, 11), (9, 12), (9, 16), (10, 11),
            (10, 12), (10, 14), (11, 13), (11, 14), (11, 16), (12, 13),
            (12, 14), (12, 16), (13, 15), (14, 16)]
        self.n = n = 17
        seed = 42
        np.random.seed(seed)
        self.w = w = {}
        for e in E:
            w[e] = np.random.randint(0, 100)

        # third roots of unity
        R3 = [1., -0.5 + 3 ** 0.5 / 2. * 1j, -0.5 - 3 ** 0.5 / 2. * 1j]

        self.Max3cut = Max3cut = picos.Problem()
        self.Z = Z = picos.HermitianVariable('Z', (n, n))
        Max3cut.add_constraint(Z >> 0)
        Max3cut.add_constraint(picos.diag_vect(Z) == 1)
        obj = 0.
        for i in range(n):
            for j in range(i + 1, n):
                for alpha in R3:
                    Max3cut.add_constraint(2 * alpha.real * Z[i, j].real
                        - 2 * alpha.imag * Z[i, j].imag >= -1.)
                obj += 2 / 3. * w.get((i, j), 0) * (1 - Z[i, j].real)

        Max3cut.set_objective('max', obj)

    def testRelaxation(self):  # noqa
        self.to.objPlaces = 5
        self.primalSolve(self.Max3cut)
        self.expectObjective(self.Max3cut, 2141.98917)
