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

"""Implements :class:`QuantumEntropy`, :class:`NegativeQuantumEntropy`."""

# TODO: Common base class for QuantumEntropy and NegativeQuantumEntropy.

import operator
from collections import namedtuple

import cvxopt
import numpy

from .. import glyphs
from ..apidoc import api_end, api_start
from ..caching import cached_selfinverse_unary_operator, cached_unary_operator
from ..constraints import (
    QuantRelEntropyConstraint,
    ComplexQuantRelEntropyConstraint,
)
from .data import convert_and_refine_arguments, convert_operands, cvx2np
from .exp_affine import AffineExpression, ComplexAffineExpression
from .expression import Expression, refine_operands, validate_prediction

_API_START = api_start(globals())
# -------------------------------


class QuantumEntropy(Expression):
    r"""Quantum or negative quantum relative entropy of an affine expression.

    :Definition:

    Let :math:`X` be an :math:`n \times n`-dimensional symmetric or hermitian
    matrix.

    1.  If no additional expression :math:`Y` is given, this is the quantum
        entropy

        .. math::

            -\operatorname{Tr}(X \log(X)).

    2.  If an additional affine expression :math:`Y` of same shape as :math:`X`
        is given, this is the negative quantum relative entropy

        .. math::

            \operatorname{Tr}(X \log(Y) - X\log(X))

    3.  If an additional scalar valued real affine expression :math:`Y`
        is given, this is the homogenized quantum entropy

        .. math::

            -\operatorname{Tr}(X \log(X/y))

    .. warning::

        When you pose a lower bound on this expression, then PICOS enforces
        :math:`X \succeq 0` through an auxiliary constraint during solution
        search. When an additional expression :math:`Y` is given, PICOS enforces
        :math:`Y \succeq 0` as well.
    """

    # --------------------------------------------------------------------------
    # Initialization and factory methods.
    # --------------------------------------------------------------------------

    @convert_and_refine_arguments("X", "Y", allowNone=True)
    def __init__(self, X, Y=None):
        """Construct an :class:`QuantumEntropy`.

        :param X: The affine expression :math:`X`.
        :type X: ~picos.expressions.AffineExpression
        :param Y: An additional affine expression :math:`Y`. If necessary, PICOS
            will attempt to reshape or broadcast it to the shape of :math:`X`.
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

        if Y is not None:
            if not isinstance(Y, ComplexAffineExpression):
                raise TypeError(
                    "The additional parameter Y must be a real "
                    "or complex affine expression, not {}.".format(
                        type(Y).__name__
                    )
                )
            if not Y.hermitian:
                raise TypeError(
                    "Can only take the matrix logarithm of a symmetric "
                    "or Hermitian expression, not of {}.".format(
                        type(Y).__name__
                    )
                )
            if X.shape != Y.shape and Y.shape != (1, 1):
                raise TypeError(
                    "The additional parameter Y must either be the "
                    "same shape as X, or be a real scalar expression, "
                    "not {}.".format(type(Y).__name__)
                )
            if Y.is1:
                Y = None

        self._X = X
        self._Y = Y

        self._iscomplex = not isinstance(X, AffineExpression) or \
                          not isinstance(Y, AffineExpression)

        if Y is None:
            typeStr = "Quantum Entropy"
            symbStr = glyphs.qe(X.string)
        elif Y.shape == (1, 1):
            typeStr = "Homogenized Quantum Entropy"
            symbStr = glyphs.neg(
                glyphs.qre(X.string, glyphs.mul(Y.string, glyphs.idmatrix)))
        else:
            typeStr = "Negative Quantum Relative Entropy"
            symbStr = glyphs.neg(glyphs.qre(X.string, Y.string))

        Expression.__init__(self, typeStr, symbStr)

    # --------------------------------------------------------------------------
    # Abstract method implementations and method overridings, except _predict.
    # --------------------------------------------------------------------------

    def _get_refined(self):
        if self._X.constant and (self._Y is None or self._Y.constant):
            return AffineExpression.from_constant(self.value, 1, self._symbStr)
        else:
            return self

    Subtype = namedtuple("Subtype", ("argdim", "Y", "iscomplex"))

    def _get_subtype(self):
        return self.Subtype(len(self._X), self._Y is not None, self._iscomplex)

    def _get_value(self):
        X = cvx2np(self._X._get_value())
        eigvalsX, eigvecsX = numpy.linalg.eigh(X)

        if self._Y is None:
            eigvalsX = eigvalsX[eigvalsX > 1e-12]
            s = -numpy.sum(eigvalsX * numpy.log(eigvalsX))
        else:
            Y = eigvecsX.conj().T @ cvx2np(self._Y._get_value()) @ eigvecsX

            Dy, Uy = numpy.linalg.eigh(Y)
            logY = Uy @ numpy.diag(numpy.log(Dy)) @ Uy.conj().T

            s = numpy.sum(numpy.diag(eigvalsX) * logY.conj()).real
            eigvalsX = eigvalsX[eigvalsX > 1e-12]
            s -= numpy.sum(eigvalsX * numpy.log(eigvalsX))

        return cvxopt.matrix(s)

    @cached_unary_operator
    def _get_mutables(self):
        if self._Y is None:
            return self._X._get_mutables()
        else:
            return self._X._get_mutables().union(self._Y.mutables)

    def _is_convex(self):
        return False

    def _is_concave(self):
        return True

    def _replace_mutables(self, mapping):
        return self.__class__(
            self._X._replace_mutables(mapping),
            None if self._Y is None else self._Y._replace_mutables(mapping),
        )

    def _freeze_mutables(self, freeze):
        return self.__class__(
            self._X._freeze_mutables(freeze),
            None if self._Y is None else self._Y._freeze_mutables(freeze),
        )

    # --------------------------------------------------------------------------
    # Python special method implementations, except constraint-creating ones.
    # --------------------------------------------------------------------------

    @cached_selfinverse_unary_operator
    def __neg__(self):
        return NegativeQuantumEntropy(self._X, self._Y)

    # --------------------------------------------------------------------------
    # Methods and properties that return expressions.
    # --------------------------------------------------------------------------

    @property
    def X(self):
        """The expression :math:`X`."""
        return self._X

    @property
    def Y(self):
        """The additional expression :math:`Y`, or :obj:`None`."""
        return self._Y

    # --------------------------------------------------------------------------
    # Methods and properties that describe the expression.
    # --------------------------------------------------------------------------

    @property
    def n(self):
        """Length of :attr:`X`."""
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

        if relation == operator.__ge__:
            if (
                issubclass(other.clstype, AffineExpression)
                and other.subtype.dim == 1
            ):
                if subtype.iscomplex:
                    return ComplexQuantRelEntropyConstraint.make_type(
                        argdim=subtype.argdim
                    )
                else:
                    return QuantRelEntropyConstraint.make_type(
                        argdim=subtype.argdim
                    )
        return NotImplemented

    @convert_operands(scalarRHS=True)
    @validate_prediction
    @refine_operands()
    def __ge__(self, other):
        if isinstance(other, AffineExpression):
            if self.iscomplex:
                return ComplexQuantRelEntropyConstraint(-self, -other)
            else:
                return QuantRelEntropyConstraint(-self, -other)
        else:
            return NotImplemented


class NegativeQuantumEntropy(Expression):
    r"""Negative or quantum relative entropy of an affine expression.

    :Definition:

    Let :math:`X` be an :math:`n \times n`-dimensional symmetric or hermitian
    matrix.

    1.  If no additional expression :math:`Y` is given, this is the negative
        quantum entropy

        .. math::

            \operatorname{Tr}(X \log(X)).

    2.  If an additional affine expression :math:`Y` of same shape as :math:`X`
        is given, this is the quantum relative entropy

        .. math::

            \operatorname{Tr}(X\log(X) - X\log(Y)).

    3.  If an additional scalar valued real affine expression :math:`Y`
        is given, this is the homogenized negative quantum entropy

        .. math::

            \operatorname{Tr}(X \log(X/y)).

    .. warning::

        When you pose an upper bound on this expression, then PICOS enforces
        :math:`X \succeq 0` through an auxiliary constraint during solution
        search. When an additional expression :math:`Y` is given, PICOS enforces
        :math:`Y \succeq 0` as well.
    """

    # --------------------------------------------------------------------------
    # Initialization and factory methods.
    # --------------------------------------------------------------------------

    @convert_and_refine_arguments("X", "Y", allowNone=True)
    def __init__(self, X, Y=None):
        """Construct a :class:`NegativeQuantumEntropy`.

        :param X: The affine expression :math:`X`.
        :type X: ~picos.expressions.AffineExpression
        :param Y: An additional affine expression :math:`Y`. If necessary, PICOS
            will attempt to reshape or broadcast it to the shape of :math:`X`.
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

        if Y is not None:
            if not isinstance(Y, ComplexAffineExpression):
                raise TypeError(
                    "The additional parameter Y must be a real "
                    "or complex affine expression, not {}.".format(
                        type(Y).__name__
                    )
                )
            if not Y.hermitian:
                raise TypeError(
                    "Can only take the matrix logarithm of a symmetric "
                    "or Hermitian expression, not of {}.".format(
                        type(Y).__name__
                    )
                )
            if X.shape != Y.shape and Y.shape != (1, 1):
                raise TypeError(
                    "The additional parameter Y must either be the "
                    "same shape as X, or be a real scalar expression, "
                    "not {}.".format(type(Y).__name__)
                )
            if Y.is1:
                Y = None

        self._X = X
        self._Y = Y

        self._iscomplex = not isinstance(X, AffineExpression) or (
            not isinstance(Y, AffineExpression)
        )

        if Y is None:
            typeStr = "Negative Quantum Entropy"
            symbStr = glyphs.neg(glyphs.qe(X.string))
        elif Y.shape == (1, 1):
            typeStr = "Negative Homogenized Quantum Entropy"
            symbStr = glyphs.qre(
                X.string, glyphs.mul(Y.string, glyphs.idmatrix))
        else:
            typeStr = "Quantum Relative Entropy"
            symbStr = glyphs.qre(X.string, Y.string)

        Expression.__init__(self, typeStr, symbStr)

    # --------------------------------------------------------------------------
    # Abstract method implementations and method overridings, except _predict.
    # --------------------------------------------------------------------------

    def _get_refined(self):
        if self._X.constant and (self._Y is None or self._Y.constant):
            return AffineExpression.from_constant(self.value, 1, self._symbStr)
        else:
            return self

    Subtype = namedtuple("Subtype", ("argdim", "Y", "iscomplex"))

    def _get_subtype(self):
        return self.Subtype(len(self._X), self._Y is not None, self._iscomplex)

    def _get_value(self):
        X = cvx2np(self._X._get_value())
        eigvalsX, eigvecsX = numpy.linalg.eigh(X)

        if self._Y is None:
            eigvalsX = eigvalsX[eigvalsX > 1e-12]
            s = numpy.sum(eigvalsX * numpy.log(eigvalsX))
        else:
            Y = eigvecsX.conj().T @ cvx2np(self._Y._get_value()) @ eigvecsX

            Dy, Uy = numpy.linalg.eigh(Y)
            logY = Uy @ numpy.diag(numpy.log(Dy)) @ Uy.conj().T

            s = -numpy.sum(numpy.diag(eigvalsX) * logY.conj()).real
            eigvalsX = eigvalsX[eigvalsX > 1e-12]
            s += numpy.sum(eigvalsX * numpy.log(eigvalsX))

        return cvxopt.matrix(s)

    @cached_unary_operator
    def _get_mutables(self):
        if self._Y is None:
            return self._X._get_mutables()
        else:
            return self._X._get_mutables().union(self._Y.mutables)

    def _is_convex(self):
        return True

    def _is_concave(self):
        return False

    def _replace_mutables(self, mapping):
        return self.__class__(
            self._X._replace_mutables(mapping),
            None if self._Y is None else self._Y._replace_mutables(mapping),
        )

    def _freeze_mutables(self, freeze):
        return self.__class__(
            self._X._freeze_mutables(freeze),
            None if self._Y is None else self._Y._freeze_mutables(freeze),
        )

    # --------------------------------------------------------------------------
    # Python special method implementations, except constraint-creating ones.
    # --------------------------------------------------------------------------

    @cached_selfinverse_unary_operator
    def __neg__(self):
        return QuantumEntropy(self._X, self._Y)

    # --------------------------------------------------------------------------
    # Methods and properties that return expressions.
    # --------------------------------------------------------------------------

    @property
    def X(self):
        """The expression :math:`X`."""
        return self._X

    @property
    def Y(self):
        """The additional expression :math:`Y`, or :obj:`None`."""
        return self._Y

    # --------------------------------------------------------------------------
    # Methods and properties that describe the expression.
    # --------------------------------------------------------------------------

    @property
    def n(self):
        """Length of :attr:`X`."""
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

        if relation == operator.__le__:
            if (
                issubclass(other.clstype, AffineExpression)
                and other.subtype.dim == 1
            ):
                if subtype.iscomplex:
                    return ComplexQuantRelEntropyConstraint.make_type(
                        argdim=subtype.argdim
                    )
                else:
                    return QuantRelEntropyConstraint.make_type(
                        argdim=subtype.argdim
                    )

        return NotImplemented

    @convert_operands(scalarRHS=True)
    @validate_prediction
    @refine_operands()
    def __le__(self, other):
        if isinstance(other, AffineExpression):
            if self.iscomplex:
                return ComplexQuantRelEntropyConstraint(self, other)
            else:
                return QuantRelEntropyConstraint(self, other)
        else:
            return NotImplemented


# --------------------------------------
__all__ = api_end(_API_START, globals())
