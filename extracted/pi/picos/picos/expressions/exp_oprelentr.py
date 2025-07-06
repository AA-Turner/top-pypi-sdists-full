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

"""Implements :class:`OperatorRelativeEntropy`."""

import operator
from collections import namedtuple

import cvxopt
import numpy

from .. import glyphs
from ..apidoc import api_end, api_start
from ..caching import cached_unary_operator
from ..constraints import (
    OpRelEntropyConstraint,
    ComplexOpRelEntropyConstraint,
    TrOpRelEntropyConstraint,
    ComplexTrOpRelEntropyConstraint,
)
from .data import convert_and_refine_arguments, convert_operands, cvx2np
from .exp_affine import AffineExpression, ComplexAffineExpression
from .expression import Expression, refine_operands, validate_prediction

_API_START = api_start(globals())
# -------------------------------


class OperatorRelativeEntropy(Expression):
    r"""Operator relative entropy of an affine expression.

    :Definition:

    For :math:`n \times n`-dimensional symmetric or Hermitian matrices
    :math:`X` and :math:`Y`, this is defined as

    .. math::

        X^{1/2} \log(X^{1/2}Y^{-1}X^{1/2}) X^{1/2}.

    .. warning::

        When you pose an upper bound on this expression, then PICOS enforces
        :math:`X \succeq 0` and :math:`Y \succeq 0` through an auxiliary
        constraint during solution search.
    """

    # --------------------------------------------------------------------------
    # Initialization and factory methods.
    # --------------------------------------------------------------------------

    @convert_and_refine_arguments("X", "Y")
    def __init__(self, X, Y):
        """Construct an :class:`OperatorRelativeEntropy`.

        :param X: The affine expression :math:`X`.
        :type X: ~picos.expressions.AffineExpression
        :param Y: The affine expression :math:`Y`. This should have the same
            dimensions as :math:`X`.
        :type Y: ~picos.expressions.AffineExpression
        """
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

        if not isinstance(Y, ComplexAffineExpression):
            raise TypeError(
                "The additional parameter Y must be a real "
                "or complex affine expression, not {}.".format(type(Y).__name__)
            )
        if not Y.hermitian:
            raise TypeError(
                "Can only take the matrix logarithm of a symmetric "
                "or Hermitian expression, not of {}.".format(type(Y).__name__)
            )
        if X.shape != Y.shape:
            raise TypeError(
                "The additional parameter Y must be the same shape"
                "as X, not {}.".format(type(Y).__name__)
            )

        self._X = X
        self._Y = Y

        self._iscomplex = not isinstance(X, AffineExpression) or \
                          not isinstance(Y, AffineExpression)

        typeStr = "Operator Relative Entropy"
        rtxStr = glyphs.power(X.string, "(1/2)")
        invyStr = glyphs.inverse(Y.string)
        xyxStr = glyphs.mul(rtxStr, glyphs.mul(invyStr, rtxStr))
        symbStr = glyphs.mul(rtxStr, glyphs.mul(glyphs.log(xyxStr), rtxStr))

        Expression.__init__(self, typeStr, symbStr)

    # --------------------------------------------------------------------------
    # Abstract method implementations and method overridings, except _predict.
    # --------------------------------------------------------------------------

    def _get_refined(self):
        if self._X.constant and self._Y.constant:
            return AffineExpression.from_constant(self.value, 1, self._symbStr)
        else:
            return self

    Subtype = namedtuple("Subtype", ("argdim", "iscomplex"))

    def _get_subtype(self):
        return self.Subtype(len(self._X), self._iscomplex)

    def _get_value(self):
        X = cvx2np(self._X._get_value())
        Y = cvx2np(self._Y._get_value())

        Dx, Ux = numpy.linalg.eigh(X)
        rtX = Ux @ numpy.diag(numpy.sqrt(Dx)) @ Ux.conj().T
        invY = numpy.linalg.inv(Y)

        XYX = rtX @ invY @ rtX
        Dxyx, Uxyx = numpy.linalg.eigh(XYX)
        logXYX = Uxyx @ numpy.diag(numpy.log(Dxyx)) @ Uxyx.conj().T

        S = rtX @ logXYX @ rtX

        return cvxopt.matrix(S)

    def _get_shape(self):
        return self._X.shape

    @cached_unary_operator
    def _get_mutables(self):
        return self._X._get_mutables().union(self._Y.mutables)

    def _is_convex(self):
        return True

    def _is_concave(self):
        return False

    def _replace_mutables(self, mapping):
        return self.__class__(
            self._X._replace_mutables(mapping),
            self._Y._replace_mutables(mapping),
        )

    def _freeze_mutables(self, freeze):
        return self.__class__(
            self._X._freeze_mutables(freeze), self._Y._freeze_mutables(freeze)
        )

    # --------------------------------------------------------------------------
    # Methods and properties that return expressions.
    # --------------------------------------------------------------------------

    @property
    def X(self):
        """The expression :math:`X`."""
        return self._X

    @property
    def Y(self):
        """The additional expression :math:`Y`."""
        return self._Y

    # --------------------------------------------------------------------------
    # Methods and properties that describe the expression.
    # --------------------------------------------------------------------------

    @property
    def n(self):
        """Lengths of :attr:`X` and :attr:`Y`."""
        return len(self._X)

    @property
    def iscomplex(self):
        """Whether :attr:`X` and :attr:`Y` are complex expressions or not."""
        return self._iscomplex

    @property
    def tr(self):
        """Trace of the operator relative entropy."""
        return TrOperatorRelativeEntropy(self.X, self.Y)

    # --------------------------------------------------------------------------
    # Constraint-creating operators, and _predict.
    # --------------------------------------------------------------------------

    @classmethod
    def _predict(cls, subtype, relation, other):
        assert isinstance(subtype, cls.Subtype)

        if relation == operator.__lshift__:
            if (
                issubclass(other.clstype, ComplexAffineExpression)
                and other.subtype.dim == subtype.argdim
            ):
                if subtype.iscomplex or not issubclass(
                    other.clstype, AffineExpression
                ):
                    return ComplexOpRelEntropyConstraint.make_type(
                        argdim=subtype.argdim
                    )
                else:
                    return OpRelEntropyConstraint.make_type(
                        argdim=subtype.argdim
                    )
        return NotImplemented

    def _lshift_implementation(self, other):
        if isinstance(other, ComplexAffineExpression):
            if self.iscomplex or not isinstance(other, AffineExpression):
                return ComplexOpRelEntropyConstraint(self, other)
            else:
                return OpRelEntropyConstraint(self, other)
        else:
            return NotImplemented


class TrOperatorRelativeEntropy(OperatorRelativeEntropy):
    r"""Trace operator relative entropy of an affine expression.

    :Definition:

    For :math:`n \times n`-dimensional symmetric or Hermitian matrices
    :math:`X` and :math:`Y`, this is defined as

    .. math::

        \operatorname{Tr}(X^{1/2} \log(X^{1/2}Y^{-1}X^{1/2}) X^{1/2}).

    .. warning::

        When you pose an upper bound on this expression, then PICOS enforces
        :math:`X \succeq 0` and :math:`Y \succeq 0` through an auxiliary
        constraint during solution search.
    """

    # --------------------------------------------------------------------------
    # Initialization and factory methods.
    # --------------------------------------------------------------------------

    @convert_and_refine_arguments("X", "Y")
    def __init__(self, X, Y):
        """Construct an :class:`OperatorRelativeEntropy`.

        :param X: The affine expression :math:`X`.
        :type X: ~picos.expressions.AffineExpression
        :param Y: The affine expression :math:`Y`. This should have the same
            dimensions as :math:`X`.
        :type Y: ~picos.expressions.AffineExpression
        """
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

        if not isinstance(Y, ComplexAffineExpression):
            raise TypeError(
                "The additional parameter Y must be a real "
                "or complex affine expression, not {}.".format(type(Y).__name__)
            )
        if not Y.hermitian:
            raise TypeError(
                "Can only take the matrix logarithm of a symmetric "
                "or Hermitian expression, not of {}.".format(type(Y).__name__)
            )
        if X.shape != Y.shape:
            raise TypeError(
                "The additional parameter Y must be the same shape"
                "as X, not {}.".format(type(Y).__name__)
            )

        self._X = X
        self._Y = Y

        self._iscomplex = not isinstance(X, AffineExpression) or \
                          not isinstance(Y, AffineExpression)

        typeStr = "Trace Operator Relative Entropy"
        rtxStr = glyphs.power(X.string, "(1/2)")
        invyStr = glyphs.inverse(Y.string)
        xyxStr = glyphs.mul(rtxStr, glyphs.mul(invyStr, rtxStr))
        oprelStr = glyphs.mul(rtxStr, glyphs.mul(glyphs.log(xyxStr), rtxStr))
        symbStr = glyphs.trace(oprelStr)

        Expression.__init__(self, typeStr, symbStr)

    # --------------------------------------------------------------------------
    # Abstract method implementations and method overridings, except _predict.
    # --------------------------------------------------------------------------

    def _get_value(self):
        X = cvx2np(self._X._get_value())
        Y = cvx2np(self._Y._get_value())

        Dx, Ux = numpy.linalg.eigh(X)
        rtX = Ux @ numpy.diag(numpy.sqrt(Dx)) @ Ux.conj().T
        invY = numpy.linalg.inv(Y)

        XYX = rtX @ invY @ rtX
        Dxyx, Uxyx = numpy.linalg.eigh(XYX)
        logXYX = Uxyx @ numpy.diag(numpy.log(Dxyx)) @ Uxyx.conj().T

        s = numpy.sum(X * logXYX.conj()).real

        return cvxopt.matrix(s)

    def _get_shape(self):
        return (1, 1)

    # --------------------------------------------------------------------------
    # Constraint-creating operators, and _predict.
    # --------------------------------------------------------------------------

    @classmethod
    def _predict(cls, subtype, relation, other):
        assert isinstance(subtype, cls.Subtype)

        if relation == operator.__le__:
            if (
                issubclass(other.clstype, AffineExpression)
                and other.subtype.dim == 1
            ):
                if subtype.iscomplex:
                    return ComplexTrOpRelEntropyConstraint.make_type(
                        argdim=subtype.argdim
                    )
                else:
                    return TrOpRelEntropyConstraint.make_type(
                        argdim=subtype.argdim
                    )
        return NotImplemented

    @convert_operands(scalarRHS=True)
    @validate_prediction
    @refine_operands()
    def __le__(self, other):
        if isinstance(other, AffineExpression):
            if self.iscomplex:
                return ComplexTrOpRelEntropyConstraint(self, other)
            else:
                return TrOpRelEntropyConstraint(self, other)
        else:
            return NotImplemented


# --------------------------------------
__all__ = api_end(_API_START, globals())
