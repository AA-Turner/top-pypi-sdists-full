# ------------------------------------------------------------------------------
# Copyright (C) 2024 Kerry He
#
# This file is part of PICOS.
#
# PICOS is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# PICOS is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------

"""Implements :class:`QuantumConditionalEntropy`."""

import math
import operator
from collections import namedtuple
from functools import reduce

import cvxopt
import numpy

from .. import glyphs
from ..apidoc import api_end, api_start
from ..caching import cached_unary_operator
from ..constraints import (
    QuantCondEntropyConstraint,
    ComplexQuantCondEntropyConstraint,
)
from .data import convert_and_refine_arguments, convert_operands, cvx2np
from .exp_affine import AffineExpression, ComplexAffineExpression
from .expression import Expression, refine_operands, validate_prediction

_API_START = api_start(globals())
# -------------------------------


class QuantumConditionalEntropy(Expression):
    r"""Quantum conditional entropy of an affine expression.

    :Definition:

    Let :math:`X` be an :math:`N \times N`-dimensional symmetric or hermitian
    matrix. Then this is defined as

    .. math::

        -S(X) + S(\operatorname{Tr}_i(X)),

    where :math:`S(X)=-\operatorname{Tr}(X\log(X))` is the quantum entropy, and
    :math:`\operatorname{Tr}_i` denotes the partial trace with respect to the
    :math:`i`-th subsystem.

    .. warning::

        When you pose a lower bound on this expression, then PICOS enforces
        :math:`X \succeq 0` through an auxiliary constraint during solution
        search.
    """

    # --------------------------------------------------------------------------
    # Initialization and factory methods.
    # --------------------------------------------------------------------------

    @convert_and_refine_arguments("X")
    def __init__(self, X, subsystems, dimensions=2):
        r"""Construct an :class:`QuantumConditionalEntropy`.

        :param X: The affine expression :math:`X`.
        :type X: ~picos.expressions.AffineExpression

        :param subsystems: A collection of or a single subystem number, indexed
            from zero, corresponding to subsystems that shall be traced over.
            The value :math:`-1` refers to the last subsystem.
        :type subsystems: int or tuple or list

        :param dimensions: Either an integer :math:`d` so that the subsystems
            are assumed to be all of shape :math:`d \times d`, or a sequence of
            subsystem shapes where an integer :math:`d` within the sequence is
            read as :math:`d \times d`. In any case, the elementwise product
            over all subsystem shapes must equal the expression's shape.
        :type dimensions: int or tuple or list
        """
        # Check that X is an affine Hermitian expression
        if not isinstance(X, ComplexAffineExpression):
            raise TypeError(
                "Can only take the matrix logarithm of a real "
                "or complex affine expression, not of {}.".format(
                    type(X).__name__
                )
            )
        if not X.hermitian:
            raise TypeError(
                "Can only take the matrix logarithm of a symmetric "
                "or Hermitian expression, not of {}.".format(type(X).__name__)
            )

        self._X = X

        self._iscomplex = not isinstance(X, AffineExpression)

        # Check that subsystems and dimension are compatible with X.
        if isinstance(dimensions, int):
            dimensions = self._square_equal_subsystem_dims(dimensions)
        else:
            dimensions = [
                (d, d) if isinstance(d, int) else d for d in dimensions
            ]

        total_dim = reduce(lambda x, y: (x[0] * y[0], x[1] * y[1]), dimensions)
        if total_dim != X.shape:
            raise TypeError("Subsystem dimensions do not match expression.")

        if isinstance(subsystems, int):
            subsystems = (subsystems,)

        numSys = len(dimensions)
        subsystems = set(numSys - 1 if sys == -1 else sys for sys in subsystems)

        for sys in subsystems:
            if not isinstance(sys, int):
                raise IndexError(
                    "Subsystem indices must be integer, not {}.".format(
                        type(sys).__name__
                    )
                )
            elif sys < 0:
                raise IndexError("Subsystem indices must be nonnegative.")
            elif sys >= numSys:
                raise IndexError(
                    "Subsystem index {} out of range for {} "
                    "systems total.".format(sys, numSys)
                )
            elif dimensions[sys][0] != dimensions[sys][1]:
                raise TypeError(
                    "Subsystem index {} refers to a non-square subsystem that "
                    "cannot be traced over.".format(sys)
                )

        self._subsystems = subsystems
        self._dimensions = dimensions

        sysStrings = None
        for sys in range(numSys):
            # Shape of current system.
            p, q = dimensions[sys]
            sysString = glyphs.matrix(glyphs.shape((p, q)))

            # Only trace over selected subsystems.
            if sys not in subsystems:
                sysStrings = glyphs.kron(sysStrings, sysString) \
                    if sysStrings else sysString
                continue
            else:
                sysStrings = glyphs.kron(sysStrings, glyphs.trace(sysString)) \
                    if sysStrings else glyphs.trace(sysString)

        typeStr = "Quantum Conditional Entropy"
        pxStr = glyphs.ptrace_(X.string, sysStrings)
        symbStr = glyphs.sub(glyphs.qe(X.string), glyphs.qe(pxStr))

        Expression.__init__(self, typeStr, symbStr)

    def _square_equal_subsystem_dims(self, diagLen):
        m, n = self._X.shape
        k = math.log(m, diagLen)

        if m != n or int(k) != k:
            raise TypeError(
                "The expression has shape {} so it cannot be "
                "decomposed into subsystems of shape {}.".format(
                    glyphs.shape(self._X.shape), glyphs.shape((diagLen,) * 2)
                )
            )

        return ((diagLen,) * 2,) * int(k)

    # --------------------------------------------------------------------------
    # Abstract method implementations and method overridings, except _predict.
    # --------------------------------------------------------------------------

    def _get_refined(self):
        if self._X.constant:
            return AffineExpression.from_constant(self.value, 1, self._symbStr)
        else:
            return self

    Subtype = namedtuple("Subtype", ("argdim", "iscomplex"))

    def _get_subtype(self):
        return self.Subtype(len(self._X), self._iscomplex)

    def _get_value(self):
        X = cvx2np(self._X._get_value())
        eigX = numpy.linalg.eigvalsh(X)
        eigX = eigX[eigX > 1e-12]

        pX = self._X.partial_trace(self.subsystems, self.dimensions)
        pX = cvx2np(pX._get_value())
        eigpX = numpy.linalg.eigvalsh(pX)
        eigpX = eigpX[eigpX > 1e-12]

        s = numpy.dot(eigpX, numpy.log(eigpX))
        s -= numpy.dot(eigX, numpy.log(eigX))

        return cvxopt.matrix(s)

    @cached_unary_operator
    def _get_mutables(self):
        return self._X._get_mutables()

    def _is_convex(self):
        return False

    def _is_concave(self):
        return True

    def _replace_mutables(self, mapping):
        return self.__class__(self._X._replace_mutables(mapping))

    def _freeze_mutables(self, freeze):
        return self.__class__(self._X._freeze_mutables(freeze))

    # --------------------------------------------------------------------------
    # Methods and properties that return expressions.
    # --------------------------------------------------------------------------

    @property
    def X(self):
        """The expression :math:`X`."""
        return self._X

    # --------------------------------------------------------------------------
    # Methods and properties that describe the expression.
    # --------------------------------------------------------------------------

    @property
    def subsystems(self):
        """The subsystems being traced out of :math:`X`."""
        return self._subsystems

    @property
    def dimensions(self):
        """The dimensions of the subsystems of :math:`X`."""
        return self._dimensions

    @property
    def n(self):
        """Length of :attr:`X`."""
        return len(self._X)

    @property
    def iscomplex(self):
        """Whether :attr:`X` is a complex expression or not."""
        return self._iscomplex

    # --------------------------------------------------------------------------
    # Constraint-creating operators, and _predict.
    # --------------------------------------------------------------------------

    @classmethod
    def _predict(cls, subtype, relation, other):
        assert isinstance(subtype, cls.Subtype)

        if relation == operator.__ge__:
            if (
                issubclass(other.clstype, AffineExpression)
                and other.subtype.dim == 1
            ):
                if subtype.iscomplex:
                    return ComplexQuantCondEntropyConstraint.make_type(
                        argdim=subtype.argdim
                    )
                else:
                    return QuantCondEntropyConstraint.make_type(
                        argdim=subtype.argdim
                    )
        return NotImplemented

    @convert_operands(scalarRHS=True)
    @validate_prediction
    @refine_operands()
    def __ge__(self, other):
        if isinstance(other, AffineExpression):
            if self.iscomplex:
                return ComplexQuantCondEntropyConstraint(self, other)
            else:
                return QuantCondEntropyConstraint(self, other)
        else:
            return NotImplemented


# --------------------------------------
__all__ = api_end(_API_START, globals())
