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

"""Test combinatorial problems using a cutting planes approach."""

import cvxopt as cvx
import numpy as np

import picos

from .ptest import ProductionTestCase


class CUTTING_PLANES(ProductionTestCase):
    """Configuration LP for a batch scheduling problem.

    The problem has an exponential number of variables and is solved using
    cutting planes.
    """

    def setUp(self):  # noqa
        self.s = s = np.array([99, 33, 100, 33, 100, 33, 33])
        self.w = w = np.array([1., 1., 1., 1., 1., 1., 1.])
        self.r = r = np.array([0, 0, 0, 0, 0, 0, 0])
        self.V = 100

        self.OPTGAP = 1e-4
        self.FEASGAP = 1e-3

        # initial configs
        self.S_KS = [[3, 5, 6], [4], [2], [1], [0]]
        n = len(s)
        self.K = K = 5

        self.av, self.costs = self.init_pricing_configLP(w, r, n, K)

        # define dual problem (for cutting planes)
        self.Q = Q = picos.Problem()
        self.lbda = lbda = picos.RealVariable('lambda', n)
        self.mu = mu = picos.RealVariable('mu', K, upper=0)

        self.setsk = {}
        self.constrk = {}
        for k, S in enumerate(self.S_KS):
            self.setsk[k] = [tuple(S)]
            cSk = sum([w[j] * (k + 1 - r[j]) for j in S])
            self.constrk[k] = [Q.add_constraint(
                mu[k] + picos.sum([lbda[j] for j in S]) <= cSk)]

        Q.set_objective('max', (1 | lbda) + (1 | mu))

    def init_pricing_configLP(self, w, r, n, K):  # noqa
        av = {}
        costs = {}
        for k in range(K):
            av[k] = [j for j in range(n) if r[j] <= k]
            costs[k] = [w[j] * (k + 1 - r[j]) for j in av[k]]

        return av, costs

    def pricing_configLP(self, lbda_value, mu_value, s, V, av, costs):  # noqa
        K = len(mu_value)
        sols = []
        for k in range(K):
            sk = s[av[k]]
            ck = np.array(
                [cj - lbda_value[av[k][j]] for j, cj in enumerate(costs[k])])
            I = np.where(ck < 0)[0]
            ss = list(sk[I])
            ww = list(-ck[I])
            pSk, KSk = self.ks(ss, ww, V)
            sols.append((pSk, [av[k][I[i]] for i in KSk]))
        return sols

    def ks(self, s, w, capa):
        """Solve a Knapsack problem.

        :param s: Item sizes.
        :param w: Profit.
        :param capa: Capacity.
        """
        # m[i,c] is best knapsack value with size c and items 0,...,i
        # KS[i,c] is best knapsack with size c and items 0,...,i

        m = {}
        KS = {}
        n = len(s)
        assert len(w) == n

        for c in range(capa + 1):
            m[-1, c] = 0
            KS[-1, c] = ()

        for i in range(n):
            for c in range(capa + 1):
                if s[i] > c:
                    m[i, c] = m[i - 1, c]
                    KS[i, c] = KS[i - 1, c]
                else:
                    m[i, c] = max(m[i - 1, c], m[i - 1, c - s[i]] + w[i])
                    if m[i, c] == m[i - 1, c]:
                        KS[i, c] = KS[i - 1, c]
                    else:
                        KS[i, c] = KS[i - 1, c - s[i]] + (i,)

        return m[n - 1, capa], KS[n - 1, capa]

    def cutting_plane_algo(self):  # noqa
        Q = self.Q

        self.solve(self.Q)
        lbda_value = np.array(self.lbda.value).ravel()
        mu_value = np.array(self.mu.value).ravel()

        s = self.s
        V = self.V
        av = self.av
        costs = self.costs

        sols = self.pricing_configLP(lbda_value, mu_value, s, V, av, costs)

        ub = Q.obj_value()
        lb = sum(lbda_value) - sum([m[0] for m in sols])

        feasgap = self.FEASGAP
        iter = 0
        while ub > lb + self.OPTGAP and iter < 20:
            adds = 0
            for k, (minus_mu, Sk) in enumerate(sols):
                pk = -minus_mu
                if pk < mu_value[k] - feasgap:
                    cSk = sum([self.w[j] * (k + 1 - self.r[j]) for j in Sk])
                    adds += 1
                    self.setsk[k].append(tuple(Sk))
                    self.constrk[k].append(Q.add_constraint(
                        self.mu[k] + picos.sum([self.lbda[j] for j in Sk])
                        <= cSk))

            self.solve(self.Q)
            lbda_value = np.array(self.lbda.value).ravel()
            mu_value = np.array(self.mu.value).ravel()

            sols = self.pricing_configLP(lbda_value, mu_value, s, V, av, costs)

            ub = Q.obj_value()
            lb = max(lb, sum(lbda_value) - sum([m[0] for m in sols]))
            iter += 1

        X = self.X = {}
        for k in range(self.K):
            X[k] = {}
            for cons, Sk in zip(self.constrk[k], self.setsk[k]):
                dk = cons.dual
                if dk > 1e-6:
                    X[k][tuple(Sk)] = dk
        self.value = (ub+lb)/2.

    def testSolution(self):  # noqa
        self.cutting_plane_algo()
        self.assertAlmostEqual(self.value, cvx.matrix([15.]), 6)
        self.expectObjective(self.Q, cvx.matrix([15.]))
