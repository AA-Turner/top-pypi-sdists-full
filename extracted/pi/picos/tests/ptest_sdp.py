# ------------------------------------------------------------------------------
# Copyright (C) 2018-2021 Maximilian Stahlberg
# Copyright (C) 2021 Guillaume Sagnol
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

"""Test semidefinite programs."""

import cvxopt
import numpy as np

import picos

from .ptest import ProductionTestCase


class SDP(ProductionTestCase):
    """SDP with PSD Constraint on Variable.

    (P) max. ⟨X, J⟩
        s.t. diag(X) = 𝟙 (CT)
             X ≽ 0       (CX)

    (D) min. ⟨-𝟙, μ⟩
        s.t. J + Diag(μ) + Z = 0
             μ free
             Z ≽ 0
    """

    def setUp(self):  # noqa
        # Set the dimensionality.
        n = self.n = 4

        # Primal problem.
        P = self.P = picos.Problem()
        X = self.X = picos.SymmetricVariable("X", (n, n))
        P.set_objective("max", X | 1)
        self.CT = P.add_constraint(picos.diag_vect(X) == 1)
        self.CX = P.add_constraint(X >> 0)

        # Dual problem.
        D = self.D = picos.Problem()
        mu = self.mu = picos.RealVariable("mu", n)
        Z = self.Z = picos.SymmetricVariable("Z", (n, n))
        D.set_objective("min", -(mu | 1))
        D.add_constraint(1 + picos.diag(mu) + Z == 0)
        D.add_constraint(Z >> 0)

    def testPrimal(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, self.n ** 2)
        self.expectVariable(self.X, cvxopt.matrix(1, (self.n, self.n)))

    def testDual(self):  # noqa
        self.dualSolve(self.P)
        self.readDual(self.CT, self.mu)
        self.readDual(self.CX, self.Z)
        self.expectObjective(self.D, self.n ** 2)


class SDP2(ProductionTestCase):
    """Projection onto the PSD Cone.

    (P) min. ‖X - A‖
        s.t. X ≽ 0

    (D) max. ⟨Y, -A⟩
        s.t. ‖Y‖ ≤ 1
             Y ≽ 0
    """

    def setUp(self):  # noqa
        # Set the dimensionality.
        n = 6

        # An arbitrary symmetric but not PSD matrix.
        B = np.reshape([(5 * i + 3) % 17 for i in range(n ** 2)], (n, n)) * 1e-1
        S = np.diag(np.arange(-n, n, 2))
        A = self.A = B.dot(S).dot(B.T) - 1e-2*np.eye(n)

        # Primal problem.
        X = self.X = picos.SymmetricVariable("X", (n, n))
        P = self.P = picos.Problem()
        P.set_objective("min", abs(A - X))
        self.PSD = P.add_constraint(X >> 0)

        # Dual problem.
        Y = self.Y = picos.SymmetricVariable("Y", (n, n))
        D = self.D = picos.Problem()
        D.set_objective("max", (Y | -A))
        D.add_constraint(abs(Y) <= 1)
        D.add_constraint(Y >> 0)

    def testPrimal(self):  # noqa
        s, U = np.linalg.eigh(self.A)
        Xstar = U.dot(np.diag(np.maximum(0, s))).dot(U.T)
        obj = np.linalg.norm(s[s < 0])

        self.primalSolve(self.P)
        self.expectObjective(self.P, cvxopt.matrix([obj]))
        self.expectVariable(self.X, cvxopt.matrix(Xstar))

    def testDual(self):  # noqa
        s, U = np.linalg.eigh(self.A)
        Xstar = U.dot(np.diag(np.maximum(0, s))).dot(U.T)
        Ystar = Xstar - self.A
        Ystar /= np.linalg.norm(Ystar, "fro")
        obj = np.linalg.norm(s[s < 0])

        self.dualSolve(self.P)
        self.readDual(self.PSD, self.Y)
        self.expectObjective(self.D, cvxopt.matrix([obj]))
        self.expectVariable(self.Y, cvxopt.matrix(Ystar))


class SDP3(ProductionTestCase):
    """SDP with Various Conic Constraints.

    To establish correctness of the numeric reference solutions, we solve both
    the primal and its dual problem to primal optimality. This is unlike most
    other tests, where a "dual test" solves the primal problem to dual
    optimality and values the dual problem with the dual solution of the primal.
    In short, this test case does not test dual solution retrieval.

    (P) min. ‖X - A‖ ≤ t
        s.t. tr(X + αI)^(0.5) ≥ β
             X ≽ 0

    (D) max. ⟨Z, A⟩ + βμ - ⟨I, C + αH⟩
        s.t. Z + H ≼ 0
             ‖Z‖_dual ≤ 1
             [H, mu/2 I; mu/2 I, C] ≽ 0
             μ ≥ 0
    """

    def setUp(self):  # noqa
        # Reduce precision requirements.
        self.to.objPlaces = 5

        # Define common constants.
        n = self.n = 4
        alpha = 0.5
        beta = 3.0
        I = np.eye(n)

        # An arbitrary symmetric but not PSD matrix.
        B = np.reshape([(5 * i + 3) % 17 for i in range(n ** 2)], (n, n)) * 1e-1
        S = np.diag(np.arange(-n, n, 2))
        A = self.A = B.dot(S).dot(B.T)

        # Primal problem.
        X = self.X = picos.SymmetricVariable("X", (n, n))
        t = self.t = picos.RealVariable("t")
        P = self.P = picos.Problem()
        P.set_objective("min", t)
        P.add_constraint(picos.PowerTrace(X + alpha * I, 0.5) >= beta)
        P.add_constraint(X >> 0)

        # Dual problem.
        H = picos.SymmetricVariable("H", (n, n))
        C = picos.SymmetricVariable("C", (n, n))
        Z = self.Z = picos.SymmetricVariable("Z", (n, n))
        mu = picos.RealVariable("mu", 1)
        D = self.D = picos.Problem()
        D.set_objective("max", -(C | I) - alpha * (H | I) + beta * mu + (A | Z))
        D.add_constraint(Z + H << 0)
        D.add_constraint(mu >= 0)
        D.add_constraint(((H & (mu / 2.0 * I)) // ((mu / 2.0 * I) & C)) >> 0)

    def norm_dependent_setup(self, norm_name):  # noqa
        n = self.n

        # Define norm and dual norm to use.
        if norm_name == "spectral":
            norm = picos.SpectralNorm
            dual_norm = picos.NuclearNorm
        elif norm_name == "nuclear":
            norm = picos.NuclearNorm
            dual_norm = picos.SpectralNorm
        elif norm_name == "frobenius":
            norm = abs
            dual_norm = abs
        else:
            assert len(norm_name) == 2
            p, q = norm_name
            assert (p >= 1) and (q >= 1)
            norm = lambda M: picos.Norm(M, p, q)  # noqa
            pp = p / (p - 1.0) if p > 1 else np.inf
            qq = q / (q - 1.0) if q > 1 else np.inf
            if pp == qq:
                dual_norm = lambda M: picos.Norm(M, pp, qq)  # noqa
            else:
                S = picos.SkewSymmetricVariable("S", (n, n))
                dual_norm = lambda M: picos.Norm(M + S, pp, qq)  # noqa

        # Define reference solution.
        if norm_name == (1.5, 1.5):
            self.opt_obj = 19.956028
            self.opt_X = np.array(
                [
                    [+0.08889863, -0.02165372, -0.05227937, +0.01098317],
                    [-0.02165372, +0.07733329, -0.05261871, +0.00125932],
                    [-0.05227937, -0.05261871, +0.09001519, -0.01002742],
                    [+0.01098317, +0.00125932, -0.01002742, +0.00157184],
                ]
            )
        elif norm_name == (4.0 / 3.0, 3.0):
            self.opt_obj = 14.665618
            self.opt_X = np.array(
                [
                    [+0.76041241, +0.13183728, -0.59796715, +0.24160958],
                    [+0.13183728, +0.07588375, -0.14722865, +0.05184898],
                    [-0.59796715, -0.14722865, +0.50600094, -0.19817590],
                    [+0.24160958, +0.05184898, -0.19817590, +0.07863855],
                ]
            )
        elif norm_name == "spectral":
            self.opt_obj = 12.9192075
            self.opt_X = np.array(
                [
                    [+5.27782678, -1.10057235, -1.45986354, -0.65253942],
                    [-1.10057235, +4.38646732, -2.16019949, -1.04367873],
                    [-1.45986354, -2.16019949, +3.15540401, -1.43521576],
                    [-0.65253942, -1.04367873, -1.43521576, +4.56940909],
                ]
            )
        elif norm_name == "nuclear":
            self.opt_obj = 15.3499999
            self.opt_X = np.array(
                [
                    [
                        +6.24490704e-02,
                        +4.14532168e-05,
                        +5.04285906e-05,
                        -4.67231456e-07,
                    ],
                    [
                        +4.14532168e-05,
                        +6.24842333e-02,
                        +6.52063183e-05,
                        +1.45328730e-05,
                    ],
                    [
                        +5.04285906e-05,
                        +6.52063183e-05,
                        +6.25218258e-02,
                        +2.52516893e-05,
                    ],
                    [
                        -4.67231456e-07,
                        +1.45328730e-05,
                        +2.52516893e-05,
                        +6.25448620e-02,
                    ],
                ]
            )
        elif norm_name == "frobenius":
            self.opt_obj = 13.1087748
            self.opt_X = np.array(
                [
                    [+0.11500401, -0.02236846, -0.04698618, +0.01083606],
                    [-0.02236846, +0.07757575, -0.04798765, +0.00171364],
                    [-0.04698618, -0.04798765, +0.06376399, -0.00740837],
                    [+0.01083606, +0.00171364, -0.00740837, +0.00122043],
                ]
            )
        else:
            assert False, "No reference solution for desired norm."

        # Add the norm constraints.
        self.P.add_constraint(norm(self.X - self.A) <= self.t)
        self.D.add_constraint(dual_norm(self.Z) <= 1)

        # Spectral norm: Do not check the solution (only the objective value)
        # due to numeric issues.
        self.test_primal_X = norm_name != "spectral"

    def run_primal_test(self):  # noqa
        self.primalSolve(self.P)
        self.expectObjective(self.P, cvxopt.matrix([self.opt_obj]))
        if self.test_primal_X:
            self.expectVariable(self.X, cvxopt.matrix(self.opt_X))

    def run_dual_test(self):  # noqa
        self.primalSolve(self.D)
        self.expectObjective(self.D, cvxopt.matrix([self.opt_obj]))

    def testPrimalNuclear(self):  # noqa
        self.norm_dependent_setup("nuclear")
        self.run_primal_test()

    def testDualNuclear(self):  # noqa
        self.norm_dependent_setup("nuclear")
        self.run_dual_test()

    def testPrimalSpectral(self):  # noqa
        self.knownFailure("smcp")

        self.norm_dependent_setup("spectral")
        self.run_primal_test()

    def testDualSpectral(self):  # noqa
        self.norm_dependent_setup("spectral")
        self.run_dual_test()

    def testPrimalFrobenius(self):  # noqa
        self.norm_dependent_setup("frobenius")
        self.run_primal_test()

    def testDualFrobenius(self):  # noqa
        self.norm_dependent_setup("frobenius")
        self.run_dual_test()

    def testPrimalP1dot5(self):  # noqa
        self.norm_dependent_setup((1.5, 1.5))
        self.run_primal_test()

    def testDualP1dot5(self):  # noqa
        self.norm_dependent_setup((1.5, 1.5))
        self.run_dual_test()

    def testPrimalP4by3Q3(self):  # noqa
        self.norm_dependent_setup((4.0 / 3.0, 3.0))
        self.run_primal_test()

    def testDualP4by3Q3(self):  # noqa
        self.norm_dependent_setup((4.0 / 3.0, 3.0))
        self.run_dual_test()
