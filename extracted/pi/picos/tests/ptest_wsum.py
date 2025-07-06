# ------------------------------------------------------------------------------
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

"""Test convex and concave weighted sums of expressions with different types."""

import random

import numpy as np

import picos as pc

from .ptest import ProductionTestCase


class WSUM_SOCP(ProductionTestCase):
    """SOCP using Weighted Sums.

    A constraint bounds a plus-minus-one-weighted sum over concave expressions:

    1)  1 × <Power: u^(1/2)>
    2) -1 × <1×1 Real Constant: 2>

    The objective function of the minimization variant is an unweighted sum over
    convex expressions:

    1)  1 × <Quadratic Expression: xᵀ·2·x>
    2)  1 × <Euclidean Norm: ‖x‖>
    3)  1 × <Absolute Value: |t|>
    4)  1 × <Squared Norm: xᵀ·x>
    5)  1 × <1×1 Real Linear Expression: 10·u>
    6)  1 × <1×1 Real Constant: 2>

    A first maximization variant negates every summand explicitly, some of which
    will register this negation internally and turn concave while others remain
    convex and are stored with a weight of minus one:

    1)  1 × <Quadratic Expression: -xᵀ·2·x>
    2) -1 × <Euclidean Norm: ‖x‖>
    3) -1 × <Absolute Value: |t|>
    4)  1 × <Quadratic Expression: -xᵀ·x>
    5)  1 × <1×1 Real Linear Expression: -10·u>
    6)  1 × <1×1 Real Constant: -2>

    A second maximization variant uses subtraction instead of addition, with the
    following result:

    1)  1 × <Quadratic Expression: -xᵀ·2·x>
    2) -1 × <Euclidean Norm: ‖x‖>
    3) -1 × <Absolute Value: |t|>
    4) -1 × <Squared Norm: xᵀ·x>
    5) -1 × <1×1 Real Linear Expression: 10·u>
    6) -1 × <1×1 Real Constant: 2>

    A third maximization variant negates the entire minimization objective,
    which will result in a weight vector of all minus one.
    """

    def setUp(self):  # noqa
        self.knownFailure("gurobi")  # Does not converge for default tolerance.

        self.to.objPlaces = 3

        t = pc.RealVariable("t", upper=-25)  # abs(t) >= 25
        u = pc.RealVariable("u")
        x = pc.RealVariable("x", 3, lower=10 / 3**0.5)  # abs(x) >= 10

        P = self.P = pc.Problem()
        P += u**0.5 - 2 >= 8  # u >= 100

        self.min_obj = x.T*2*x + abs(x) + abs(t) + x.T*x + 10*u + 2
        self.max_obj1 = -x.T*2*x + -abs(x) + -abs(t) + -x.T*x + -10*u + -2
        self.max_obj2 = 0 - x.T*2*x - abs(x) - abs(t) - x.T*x - 10*u - 2

    def testMinimize(self):  # noqa
        self.P.minimize = self.min_obj

        self.primalSolve(self.P)
        self.expectObjective(self.P, 1337)

    def testMaximize(self):  # noqa
        self.P.maximize = self.max_obj1

        self.primalSolve(self.P)
        self.expectObjective(self.P, -1337)

    def testMaximize2(self):  # noqa
        self.P.maximize = self.max_obj2

        self.primalSolve(self.P)
        self.expectObjective(self.P, -1337)

    def testMaximize3(self):  # noqa
        self.P.maximize = -self.min_obj

        self.primalSolve(self.P)
        self.expectObjective(self.P, -1337)


class WSUM_CREATION(ProductionTestCase):
    """Test forming weighted sums."""

    NUM_TESTS = 100

    def setUp(self):  # noqa
        # HACK: Run just once.
        # TODO: Add a framework for solver-independent tests.
        if self.solver != "cvxopt":
            self.skipTest("SOLVER-INDEPENDENT TEST")

        random.seed(1)
        np.random.seed(1)

        c = pc.Constant("c", np.random.random())
        t = pc.RealVariable("t")
        x = pc.RealVariable("x", 3)
        Y = pc.SymmetricVariable("Y", 3)

        t.value = np.random.random()
        x.value = np.random.random(3)
        Y_ = np.random.random((3, 3))
        Y.value = Y_.T @ Y_

        # Affine expressions.
        affine = (c, 2*t - 5, pc.sum(x))

        # Convex expressions.
        self.convex = affine + (
            abs(t),                 # Norm
            t**2,                   # SquaredNorm
            x.T*x + t**2 - t + 1,   # QuadraticExpression
            pc.PowerTrace(Y, 2.5),  # PowerTrace
            pc.lse(x),              # LogSumExp
            t*pc.Logarithm(t),      # NegativeEntropy
            pc.max(x),              # SumExtremes
            pc.max([t, x.T*x]),     # MaximumConvex
            pc.sumexp(x),           # SumExponentials
            pc.SpectralNorm(Y),     # SpectralNorm
            pc.NuclearNorm(Y),      # NuclearNorm
        )

        # Concave expressions.
        self.concave = affine + (
            -t**2,                  # QuadraticExpression
            pc.Logarithm(t),        # Logarithm
            -t*pc.Logarithm(t),     # Entropy
            pc.geomean(Y),          # GeometricMean
            pc.min(x),              # SumExtremes
            pc.min([t, -x.T*x]),    # MinimumConcave
            pc.detrootn(Y),         # DetRootN
        )

        # Check expressions.
        assert all(exp.convex for exp in self.convex)
        assert all(exp.concave for exp in self.concave)
        assert all(exp.scalar for exp in self.convex + self.concave)
        assert all(exp.valued for exp in self.convex + self.concave)

        # Make sure we don't miss a type listed above.
        assert not any(isinstance(exp, pc.expressions.exp_wsum.WeightedSum)
            for exp in self.convex + self.concave)

    def _test_sum(self, expressions, convex, places=10):
        # Compute reference value.
        value = sum(x.safe_value for x in expressions)

        # Randomly select a summing method and whether to refine the result.
        sum_func = sum if random.randint(0, 1) else pc.sum
        the_sum = sum_func(expressions)
        if random.randint(0, 1):
            the_sum = the_sum.refined

        # Check convexity/concavity.
        self.assertTrue(the_sum.convex if convex else the_sum.concave)

        # Check value.
        self.assertAlmostEqual(the_sum.value, value, places)

        # Test a nonnegative combination of the whole sum with itself.
        # Refine the result to test any optimizations being performed.
        c = np.random.random(2)
        combination = (c[0]*the_sum + c[1]*the_sum).refined
        combination_value = sum(c)*value
        self.assertAlmostEqual(combination.value, combination_value, places)

    def testExpressions(self):  # noqa
        for _ in range(self.NUM_TESTS):
            convex = random.randint(0, 1)

            pos = self.convex if convex else self.concave
            neg = self.concave if convex else self.convex

            summands = []
            for positive in range(2):
                candidates = pos if positive else neg
                n = random.randint(1, min(4, len(candidates)))

                weights = np.random.random(n)
                if not positive:
                    weights = -weights

                selected = random.choices(candidates, k=n)

                for w, x in zip(weights, selected):
                    summand = w*x if random.randint(0, 1) else x*w
                    summands.append(summand)

            if summands:
                self._test_sum(summands, convex)
