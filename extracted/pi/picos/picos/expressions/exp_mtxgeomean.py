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

"""Implements :class:`MatrixGeometricMean`."""

import operator
from collections import namedtuple

import cvxopt
import numpy

from .. import glyphs
from ..apidoc import api_end, api_start
from ..caching import cached_unary_operator
from ..constraints import (
    MatrixGeoMeanEpiConstraint,
    ComplexMatrixGeoMeanEpiConstraint,
    MatrixGeoMeanHypoConstraint,
    ComplexMatrixGeoMeanHypoConstraint,
    TrMatrixGeoMeanEpiConstraint,
    ComplexTrMatrixGeoMeanEpiConstraint,
    TrMatrixGeoMeanHypoConstraint,
    ComplexTrMatrixGeoMeanHypoConstraint,
)
from .data import convert_and_refine_arguments, convert_operands, cvx2np
from .exp_affine import AffineExpression, ComplexAffineExpression
from .expression import Expression, refine_operands, validate_prediction

_API_START = api_start(globals())
# -------------------------------


class MatrixGeometricMean(Expression):
    r"""Matrix geometric mean of an affine expression.

    :Definition:

    For :math:`n \times n`-dimensional symmetric or Hermitian matrices
    :math:`X` and :math:`Y`, this is defined as

        .. math::

            X^{1/2} (X^{-1/2}Y^{-1}X^{-1/2})^p X^{1/2}.

    for a given scalar :math:`p\in[-1, 2]`, where :math:`p=1/2` by default.

    .. warning::

        When you pose an upper or lower bound on this expression, then PICOS
        enforces :math:`X \succeq 0` and :math:`Y \succeq 0` through an
        auxiliary constraint during solution search.
    """

    # --------------------------------------------------------------------------
    # Initialization and factory methods.
    # --------------------------------------------------------------------------

    @convert_and_refine_arguments("X", "Y")
    def __init__(self, X, Y, power=0.5):
        """Construct an :class:`MatrixGeometricMean`.

        :param X: The affine expression :math:`X`.
        :type X: ~picos.expressions.AffineExpression
        :param Y: The affine expression :math:`Y`. This should have the same
            dimensions as :math:`X`.
        :type Y: ~picos.expressions.AffineExpression
        """
        if not isinstance(X, ComplexAffineExpression):
            raise TypeError(
                "Can only take the matrix powers of a real "
                "or complex affine expression, not of {}.".format(
                    type(X).__name__
                )
            )
        if not X.hermitian:
            raise TypeError(
                "Can only take the matrix powers of a symmetric "
                "or Hermitian expression, not of {}.".format(type(X).__name__)
            )

        if not isinstance(Y, ComplexAffineExpression):
            raise TypeError(
                "The additional parameter Y must be a real "
                "or complex affine expression, not {}.".format(type(Y).__name__)
            )
        if not Y.hermitian:
            raise TypeError(
                "Can only take the matrix powers of a symmetric "
                "or Hermitian expression, not of {}.".format(type(Y).__name__)
            )
        if X.shape != Y.shape:
            raise TypeError(
                "The additional parameter Y must be the same shape"
                "as X, not {}.".format(type(Y).__name__)
            )

        if not (numpy.isscalar(power) and -1 <= power and power <= 2):
            raise TypeError("The exponent p must be a scalar between [-1, 2]")

        self._X = X
        self._Y = Y
        self._power = power

        self._iscomplex = not isinstance(X, AffineExpression) or \
                          not isinstance(Y, AffineExpression)

        typeStr = "Matrix Geometric Mean"
        if power == 0.5:
            symbStr = glyphs.geomean(X.string, Y.string)
        else:
            symbStr = glyphs.wgeomean(X.string, str(power), Y.string)

        Expression.__init__(self, typeStr, symbStr)

    # --------------------------------------------------------------------------
    # Abstract method implementations and method overridings, except _predict.
    # --------------------------------------------------------------------------

    def _get_refined(self):
        if self._X.constant and self._Y.constant:
            return AffineExpression.from_constant(self.value, 1, self._symbStr)
        else:
            return self

    Subtype = namedtuple("Subtype", ("argdim", "power", "iscomplex"))

    def _get_subtype(self):
        return self.Subtype(len(self._X), self._power, self._iscomplex)

    def _get_value(self):
        X = cvx2np(self._X._get_value())
        Y = cvx2np(self._Y._get_value())

        Dx, Ux = numpy.linalg.eigh(X)
        rtX = Ux @ numpy.diag(numpy.sqrt(Dx)) @ Ux.conj().T
        irtX = Ux @ numpy.diag(numpy.reciprocal(numpy.sqrt(Dx))) @ Ux.conj().T

        XYX = irtX @ Y @ irtX
        Dxyx, Uxyx = numpy.linalg.eigh(XYX)
        XYX_p = Uxyx @ numpy.diag(numpy.power(Dxyx, self.power)) @ Uxyx.conj().T

        S = rtX @ XYX_p @ rtX

        return cvxopt.matrix(S)

    def _get_shape(self):
        return self._X.shape

    @cached_unary_operator
    def _get_mutables(self):
        return self._X._get_mutables().union(self._Y.mutables)

    def _is_convex(self):
        return (-1 <= self._power and self._power <= 0) or \
               ( 1 <= self._power and self._power <= 2)

    def _is_concave(self):
        return 0 <= self._power and self._power <= 1

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

    @property
    def power(self):
        """The power :math:`p`."""
        return self._power

    @property
    def tr(self):
        """Trace of the matrix geometric mean."""
        return TrMatrixGeometricMean(self.X, self.Y, self.power)

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

    # --------------------------------------------------------------------------
    # Constraint-creating operators, and _predict.
    # --------------------------------------------------------------------------

    @classmethod
    def _predict(cls, subtype, relation, other):
        assert isinstance(subtype, cls.Subtype)

        isconvex = (-1 <= subtype.power and subtype.power <= 0) or \
                   ( 1 <= subtype.power and subtype.power <= 2)
        isconcave = 0 <= subtype.power and subtype.power <= 1

        if relation == operator.__lshift__:
            if (
                isconvex
                and issubclass(other.clstype, ComplexAffineExpression)
                and other.subtype.dim == subtype.argdim
            ):
                if subtype.iscomplex or not issubclass(
                    other.clstype, AffineExpression
                ):
                    return ComplexMatrixGeoMeanEpiConstraint.make_type(
                        argdim=subtype.argdim
                    )
                else:
                    return MatrixGeoMeanEpiConstraint.make_type(
                        argdim=subtype.argdim
                    )

        if relation == operator.__rshift__:
            if (
                isconcave
                and issubclass(other.clstype, ComplexAffineExpression)
                and other.subtype.dim == subtype.argdim
            ):
                if subtype.iscomplex or not issubclass(
                    other.clstype, AffineExpression
                ):
                    return ComplexMatrixGeoMeanHypoConstraint.make_type(
                        argdim=subtype.argdim
                    )
                else:
                    return MatrixGeoMeanHypoConstraint.make_type(
                        argdim=subtype.argdim
                    )

        return NotImplemented

    def _lshift_implementation(self, other):
        if self.convex and isinstance(other, ComplexAffineExpression):
            if self.iscomplex or not isinstance(other, AffineExpression):
                return ComplexMatrixGeoMeanEpiConstraint(self, other)
            else:
                return MatrixGeoMeanEpiConstraint(self, other)
        else:
            return NotImplemented

    def _rshift_implementation(self, other):
        if self.concave and isinstance(other, ComplexAffineExpression):
            if self.iscomplex or not isinstance(other, AffineExpression):
                return ComplexMatrixGeoMeanHypoConstraint(self, other)
            else:
                return MatrixGeoMeanHypoConstraint(self, other)
        else:
            return NotImplemented


class TrMatrixGeometricMean(MatrixGeometricMean):
    r"""Trace matrix geometric mean of an affine expression.

    :Definition:

    For :math:`n \times n`-dimensional symmetric or Hermitian matrices
    :math:`X` and :math:`Y`, this is defined as

        .. math::

            \operatorname{Tr}(X^{1/2} (X^{-1/2}Y^{-1}X^{-1/2})^p X^{1/2}).

    for a given scalar :math:`p\in[-1, 2]`, where :math:`p=1/2` by default.

    .. warning::

        When you pose an upper or lower bound on this expression, then PICOS
        enforces :math:`X \succeq 0` and :math:`Y \succeq 0` through an
        auxiliary constraint during solution search.
    """

    # --------------------------------------------------------------------------
    # Initialization and factory methods.
    # --------------------------------------------------------------------------

    @convert_and_refine_arguments("X", "Y")
    def __init__(self, X, Y, power=0.5):
        """Construct an :class:`MatrixGeometricMean`.

        :param X: The affine expression :math:`X`.
        :type X: ~picos.expressions.AffineExpression
        :param Y: The affine expression :math:`Y`. This should have the same
            dimensions as :math:`X`.
        :type Y: ~picos.expressions.AffineExpression
        """
        if not isinstance(X, ComplexAffineExpression):
            raise TypeError(
                "Can only take the matrix powers of a real "
                "or complex affine expression, not of {}.".format(
                    type(X).__name__
                )
            )
        if not X.hermitian:
            raise TypeError(
                "Can only take the matrix powers of a symmetric "
                "or Hermitian expression, not of {}.".format(type(X).__name__)
            )

        if not isinstance(Y, ComplexAffineExpression):
            raise TypeError(
                "The additional parameter Y must be a real "
                "or complex affine expression, not {}.".format(type(Y).__name__)
            )
        if not Y.hermitian:
            raise TypeError(
                "Can only take the matrix powers of a symmetric "
                "or Hermitian expression, not of {}.".format(type(Y).__name__)
            )
        if X.shape != Y.shape:
            raise TypeError(
                "The additional parameter Y must be the same shape"
                "as X, not {}.".format(type(Y).__name__)
            )

        self._X = X
        self._Y = Y
        self._power = power

        self._iscomplex = not isinstance(X, AffineExpression) or \
                          not isinstance(Y, AffineExpression)

        typeStr = "Trace Matrix Geometric Mean"
        if power == 0.5:
            symbStr = glyphs.trace(glyphs.geomean(X.string, Y.string))
        else:
            pStr = str(power)
            symbStr = glyphs.trace(glyphs.wgeomean(X.string, pStr, Y.string))

        Expression.__init__(self, typeStr, symbStr)

    # --------------------------------------------------------------------------
    # Abstract method implementations and method overridings, except _predict.
    # --------------------------------------------------------------------------

    def _get_value(self):
        X = cvx2np(self._X._get_value())
        Y = cvx2np(self._Y._get_value())

        Dx, Ux = numpy.linalg.eigh(X)
        irtX = Ux @ numpy.diag(numpy.reciprocal(numpy.sqrt(Dx))) @ Ux.conj().T

        XYX = irtX @ Y @ irtX
        Dxyx, Uxyx = numpy.linalg.eigh(XYX)
        XYX_p = Uxyx @ numpy.diag(numpy.power(Dxyx, self.power)) @ Uxyx.conj().T

        s = numpy.sum(X * XYX_p.conj()).real

        return cvxopt.matrix(s)

    def _get_shape(self):
        return (1, 1)

    # --------------------------------------------------------------------------
    # Constraint-creating operators, and _predict.
    # --------------------------------------------------------------------------

    @classmethod
    def _predict(cls, subtype, relation, other):
        assert isinstance(subtype, cls.Subtype)

        isconvex = (-1 <= subtype.power and subtype.power <= 0) or \
                   ( 1 <= subtype.power and subtype.power <= 2)
        isconcave = 0 <= subtype.power and subtype.power <= 1

        if relation == operator.__le__:
            if (
                isconvex
                and issubclass(other.clstype, AffineExpression)
                and other.subtype.dim == 1
            ):
                if subtype.iscomplex or not issubclass(
                    other.clstype, AffineExpression
                ):
                    return ComplexTrMatrixGeoMeanEpiConstraint.make_type(
                        argdim=subtype.argdim
                    )
                else:
                    return TrMatrixGeoMeanEpiConstraint.make_type(
                        argdim=subtype.argdim
                    )

        if relation == operator.__ge__:
            if (
                isconcave
                and issubclass(other.clstype, AffineExpression)
                and other.subtype.dim == 1
            ):
                if subtype.iscomplex or not issubclass(
                    other.clstype, AffineExpression
                ):
                    return ComplexTrMatrixGeoMeanHypoConstraint.make_type(
                        argdim=subtype.argdim
                    )
                else:
                    return TrMatrixGeoMeanHypoConstraint.make_type(
                        argdim=subtype.argdim
                    )

        return NotImplemented

    @convert_operands(scalarRHS=True)
    @validate_prediction
    @refine_operands()
    def __le__(self, other):
        if self.convex and isinstance(other, AffineExpression):
            if self.iscomplex:
                return ComplexTrMatrixGeoMeanEpiConstraint(self, other)
            else:
                return TrMatrixGeoMeanEpiConstraint(self, other)
        else:
            return NotImplemented

    @convert_operands(scalarRHS=True)
    @validate_prediction
    @refine_operands()
    def __ge__(self, other):
        if self.concave and isinstance(other, AffineExpression):
            if self.iscomplex:
                return ComplexTrMatrixGeoMeanHypoConstraint(self, other)
            else:
                return TrMatrixGeoMeanHypoConstraint(self, other)
        else:
            return NotImplemented


# --------------------------------------
__all__ = api_end(_API_START, globals())
