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

"""Test matrix reshuffling."""

import random
import string
from functools import reduce

import numpy as np
import picos as pc

MAX_DIMS = 5
MAX_DIM = 5


def factors(n):
    """Return all factoriztations of a nonnegative integer as two integers."""
    return [(i, n // i) for i in range(1, int(n ** 0.5) + 1) if not n % i]


def make_picos_matrix(m, n):
    r"""Create a :math:`m \times n` PICOS testing matrix."""
    return pc.Constant(range(m * n), shape=(m, n))


def make_numpy_matrix(m, n):
    r"""Create a :math:`m \times n` NumPy testing matrix."""
    return np.array(range(m * n)).reshape(n, m).T


def reshuffle_picos(matrix, permutation, dimensions, order):
    """Reshuffle a PICOS matrix."""
    return matrix.reshuffled(permutation, dimensions, order)


def reshuffle_numpy(matrix, permutation, dimensions, order):
    """Reshuffle a NumPy matrix."""
    P = "{} -> {}".format("".join(sorted(permutation)), permutation)
    reshuffled = np.reshape(matrix, dimensions, order)
    reshuffled = np.einsum(P, reshuffled)
    return np.reshape(reshuffled, matrix.shape, order)


def equal(picos_matrix, numpy_matrix):
    """Report whether a PICOS and a NumPy matrix are equal."""
    return picos_matrix.equals(pc.Constant(numpy_matrix))


if __name__ == "__main__":
    while True:
        # Choose a number of tensor dimensions.
        d = random.randint(1, MAX_DIMS)

        # Produce random tensor dimensions.
        dimensions = tuple(random.randint(1, MAX_DIM) for _ in range(d))
        k = reduce(int.__mul__, dimensions, 1)

        # Factor k = m*n at random.
        m, n = random.choice(factors(k))

        # Create a pair of PICOS and NumPy matrices with equal data.
        picos_matrix = make_picos_matrix(m, n)
        numpy_matrix = make_numpy_matrix(m, n)
        assert equal(picos_matrix, numpy_matrix)

        # Choose a random perturbation of tensor dimensions.
        permutation = list(range(d))
        random.shuffle(permutation)
        permutation = reduce(
            str.__add__, (string.ascii_lowercase[i] for i in permutation), ""
        )

        # Choose a random reshaping order.
        order = random.choice("FC")

        # Reshuffle both matrices.
        picos_reshuffled = reshuffle_picos(
            picos_matrix, permutation, dimensions, order
        )
        numpy_reshuffled = reshuffle_numpy(
            numpy_matrix, permutation, dimensions, order
        )

        # Compare the results.
        if not equal(picos_reshuffled, numpy_reshuffled):
            raise RuntimeError(
                "dimensions={}, mn={}, permutation='{}', order='{}'"
                "\n\nBefore:\n{}\nPICOS:\n{}\nNumPy:\n{}".format(
                    dimensions,
                    (m, n),
                    permutation,
                    order,
                    picos_matrix,
                    picos_reshuffled,
                    pc.Constant(numpy_reshuffled),
                )
            )
