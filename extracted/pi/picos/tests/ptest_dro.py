# ------------------------------------------------------------------------------
# Copyright (C) 2003 Travis Oliphant (scipy_signal_square)
# Copyright (C) 2021 Maximilian Stahlberg
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

"""Test distributionally robust optimization problems."""

import numpy

import picos

from .ptest import ProductionTestCase


class THESIS_5_2_3(ProductionTestCase):
    """Moment-robust piecewise linear stochastic program.

    This compares the exact DRO model with a discretization of the uncertainty,
    implemented as a RO model. Note that all reference values were computed by
    PICOS (using CVXOPT) in the first place; only the relationship between the
    solution values provides evidence of correctness.

    From "Robust conic optimization in Python" (Stahlberg 2020, Section 5.2.3).
    """

    def make_s(self, N):  # noqa
        return picos.Constant("s", numpy.linspace(self.a, self.b, N))

    def make_q(self, N, s):  # noqa
        return picos.Constant("q", (s - self.mu) ^ (s - self.mu))

    def make_p(self, N, s):  # noqa
        q = self.make_q(N, s)
        P = picos.uncertain.ConicPerturbationSet("p", N)
        p = P.element
        P.bound(p >= 0)
        P.bound(p <= 1)
        P.bound(picos.sum(p) == 1)
        P.bound(q.T*p <= self.beta*self.Sigma)
        P.bound(abs(s.T*p - self.mu) <= (self.alpha * self.Sigma)**0.5)
        return P.compile()

    def make_approximation(self, N):  # noqa
        s = self.make_s(N)
        p = self.make_p(N, s)
        P = picos.Problem()
        x = picos.RealVariable("x")
        y = picos.RealVariable("y", N)
        P.set_objective("min", p.T*y)
        P.add_list_of_constraints([
            self.C[i, :] * (s[j]*x // x // s[j] // 1) <= y[j]
            for i in range(self.k) for j in range(N)])
        return P

    def setUp(self):  # noqa
        # Same seed and precision as in the thesis.
        numpy.random.seed(1)
        self.to.objPlaces = 4

        # Common data.
        self.k = k = 5
        (self.a, self.b) = (a, b) = -1.0, 1.0
        self.mu = mu = a + (3.0 / 4.0)*(b - a)
        self.Sigma = min(abs(mu - a), abs(mu - b))**2 / 4.0
        self.alpha, self.beta = 0.1, 1.1
        self.C = picos.Constant("C", numpy.random.normal(size=(k, 4)))

    def testNominal(self):  # noqa
        P_mu = picos.Problem()
        x_mu = picos.RealVariable("x")
        t_mu = self.mu*x_mu // x_mu // self.mu // 1
        f_mu = picos.max([self.C[i, :]*t_mu for i in range(self.k)])
        P_mu.set_objective("min", f_mu)

        self.primalSolve(P_mu)
        self.expectObjective(P_mu, -1.003)

    def testApprox1(self):  # noqa
        self.knownFailure("osqp")  # Takes far too long.

        P_10 = self.make_approximation(10)

        self.primalSolve(P_10)
        self.expectObjective(P_10, -0.6210, False, True)

    def testApprox2(self):  # noqa
        self.knownFailure("osqp")  # Takes far too long.

        P_20 = self.make_approximation(20)

        self.primalSolve(P_20)
        self.expectObjective(P_20, -0.6142, False, True)

    def testRobust(self):  # noqa
        r = (self.b - self.a) / 2.0
        S = picos.Ellipsoid(n=1, A=r, c=(self.a + r))
        D = picos.uncertain.MomentAmbiguitySet(
            "xi", (1, 1), self.mu, self.Sigma, self.alpha, self.beta, S)
        xi = D.parameter
        P_dro = picos.Problem()
        x_dro = picos.RealVariable("x")
        t = xi*x_dro // x_dro // xi // 1
        f_dro = picos.max([self.C[i, :]*t for i in range(self.k)])
        P_dro.set_objective("min", f_dro)

        self.primalSolve(P_dro)
        self.expectObjective(P_dro, -0.6122, False, True)


class THESIS_5_2_4(ProductionTestCase):
    """Wasserstein-robust quadratic stochastic program.

    This recreates a toy application in linear signal estimation. Note that all
    reference values were computed by PICOS (using CVXOPT) in the first place;
    only the relationship between the solution values provides evidence of
    correctness.

    From "Robust conic optimization in Python" (Stahlberg 2020, Section 5.2.4).
    """

    def scipy_signal_square(self, t, duty=0.5):
        """A copy of scipy.signal.square."""
        t, w = numpy.asarray(t), numpy.asarray(duty)
        w = numpy.asarray(w + (t - t))
        t = numpy.asarray(t + (w - w))
        if t.dtype.char in ['fFdD']:
            ytype = t.dtype.char
        else:
            ytype = 'd'

        y = numpy.zeros(t.shape, ytype)

        # width must be between 0 and 1 inclusive
        mask1 = (w > 1) | (w < 0)
        numpy.place(y, mask1, numpy.nan)

        # on the interval 0 to duty*2*pi function is 1
        tmod = numpy.mod(t, 2 * numpy.pi)
        mask2 = (1 - mask1) & (tmod < w * 2 * numpy.pi)
        numpy.place(y, mask2, 1)

        # on the interval duty*2*pi to 2*pi function is
        #  (pi*(w+1)-tmod) / (pi*(1-w))
        mask3 = (1 - mask1) & (1 - mask2)
        numpy.place(y, mask3, -1)
        return y

    def make_signal(self):  # noqa
        a, b = 2*numpy.pi*numpy.random.random(2)
        smooth_part = numpy.sin(self.t + a)
        sharp_part = self.scipy_signal_square(self.t + b)
        return 0.4*smooth_part + 0.6*sharp_part

    def make_obstacle(self, coverage, returned, delay):  # noqa
        delay_lower = int(delay)
        delay_upper = delay_lower + 1
        coverage_upper = coverage*(delay - delay_lower)
        coverage_lower = coverage - coverage_upper
        A = (1.0 - coverage)*numpy.eye(self.n)
        B = coverage_lower*numpy.eye(self.n, k=-delay_lower)
        C = coverage_upper*numpy.eye(self.n, k=-delay_upper)
        return A + returned*(B + C)

    def make_noisy_obstacle(self, coverage, returned, delay):  # noqa
        c, r, d = numpy.clip(
            numpy.random.normal(1.0, 0.25, 3), 0.0, None)
        return self.make_obstacle(c*coverage, r*returned, d*delay)

    def make_channel(self):  # noqa
        A = self.make_noisy_obstacle(0.2, 0.5, 0.25*self.n)
        B = self.make_noisy_obstacle(0.2, 0.5, 0.50*self.n)
        C = self.make_noisy_obstacle(0.2, 0.5, 0.75*self.n)
        return A @ B @ C

    def sample(self):  # noqa
        signal = self.make_signal()
        channel = self.make_channel()
        return numpy.vstack([signal, channel @ signal]).T

    def amse(self, recovery_matrix, samples):  # noqa
        R = ~recovery_matrix
        X = samples.matrix[:self.n, :]
        Y = samples.matrix[self.n:, :]
        return sum(abs(R*Y - X)**2) / (len(samples)*self.n)

    def setUp(self):  # noqa
        # Set random seed and precision.
        numpy.random.seed(1)
        self.to.objPlaces = 4

        # Common data.
        # NOTE: Reduced signal dimension from 16, training samples from 1000.
        self.n = 6  # Signal dimension.
        self.t = numpy.linspace(0, 2*numpy.pi, self.n)
        self.N, self.M = 4, 200  # Number of training and validation samples.
        S = picos.Samples([self.sample() for _ in range(self.N + self.M)])
        self.T, self.V = S.partition(self.N)
        self.X = self.T.matrix[:self.n, :]  # Clean signals.
        self.Y = self.T.matrix[self.n:, :]  # Perturbed signals.

    def testNominal(self):  # noqa
        P_mse = picos.Problem()
        R_mse = picos.LowerTriangularVariable("R", (self.n, self.n))
        P_mse.set_objective("min",
            abs(R_mse*self.Y - self.X)**2 / (self.N*self.n))

        self.primalSolve(P_mse)
        self.expectObjective(P_mse, 0.0003)

    def testReularized(self):  # noqa
        lbd = 0.01
        P_reg = picos.Problem()
        R_reg = picos.LowerTriangularVariable("R", (self.n, self.n))
        P_reg.set_objective("min",
            abs(R_reg*self.Y - self.X)**2 + lbd*abs(R_reg)**2)

        self.primalSolve(P_reg)
        self.expectExpression(self.amse(R_reg, self.T), 0.0008)
        self.expectExpression(self.amse(R_reg, self.V), 0.0216)

    def testRobust(self):  # noqa
        self.knownFailure("smcp")  # Factorization failed (dualized works).

        D = picos.uncertain.WassersteinAmbiguitySet(
            parameter_name="[x, y]", p=2, eps=0.6, samples=self.T)
        x = D.parameter[:, 0].renamed("x")
        y = D.parameter[:, 1].renamed("y")
        P_dro = picos.Problem()
        R_dro = picos.LowerTriangularVariable("R", (self.n, self.n))
        P_dro.set_objective("min", abs(R_dro*y - x)**2)

        self.primalSolve(P_dro)
        self.expectExpression(self.amse(R_dro, self.T), 0.0014)
        self.expectExpression(self.amse(R_dro, self.V), 0.0131)
