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

"""Implements Renyi entropy expressions."""

import operator
from collections import namedtuple

import cvxopt
import numpy

from .. import glyphs
from ..apidoc import api_end, api_start
from ..caching import cached_unary_operator
from ..constraints import (
    QuasiEntrEpiConstraint,
    ComplexQuasiEntrEpiConstraint,
    QuasiEntrHypoConstraint,
    ComplexQuasiEntrHypoConstraint,
    RenyiEntrConstraint,
    ComplexRenyiEntrConstraint,
    SandRenyiEntrConstraint,
    ComplexSandRenyiEntrConstraint,
    SandQuasiEntrEpiConstraint,
    ComplexSandQuasiEntrEpiConstraint,
    SandQuasiEntrHypoConstraint,
    ComplexSandQuasiEntrHypoConstraint,

)
from .data import convert_and_refine_arguments, convert_operands, cvx2np
from .exp_affine import AffineExpression, ComplexAffineExpression
from .expression import Expression, refine_operands, validate_prediction

_API_START = api_start(globals())
# -------------------------------

class BaseRenyiEntropy(Expression):
    r"""Base class used to define a general Renyi entropy expression."""

    # --------------------------------------------------------------------------
    # Initialization and factory methods.
    # --------------------------------------------------------------------------

    @convert_and_refine_arguments("X", "Y", "u", allowNone=True)
    def __init__(self, X, Y, alpha, u=None):
        r"""Construct an :class:`BaseRenyiEntropy`.

        :param X: The affine expression :math:`X`.
        :type X: ~picos.expressions.AffineExpression
        :param Y: The affine expression :math:`Y`. This should have the same
            dimensions as :math:`X`.
        :type Y: ~picos.expressions.AffineExpression
        :param alpha: The parameter :math:`\alpha`.
        :type alpha: float
        :param u: An additional scalar affine expression :math:`u`. If
            specified, then this defines the perspective of the Renyi entropy.
        :type u: ~picos.expressions.AffineExpression
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
        
        if u is not None:
            if u.shape != (1, 1) or not isinstance(u, AffineExpression):
                raise TypeError(
                    "The additional parameter u must be a real scalar affine "
                    "expression, not {}.".format(type(Y).__name__)
                )
            if u.is1:
                u = None
        
        self._is_valid_alpha(alpha)

        self._X = X
        self._Y = Y
        self._u = u
        self._alpha = alpha

        self._iscomplex = not isinstance(X, AffineExpression) or \
                          not isinstance(Y, AffineExpression)

        typeStr, symbStr = self._get_strings()

        Expression.__init__(self, typeStr, symbStr)

    # --------------------------------------------------------------------------
    # Abstract method implementations and method overridings, except _predict.
    # --------------------------------------------------------------------------

    def _get_refined(self):
        if self._X.constant and self._Y.constant:
            if (self._u is None or self._u.constant):
                return AffineExpression.from_constant(
                    self.value, 1, self._symbStr
                )

        return self

    Subtype = namedtuple("Subtype", ("argdim", "alpha", "iscomplex"))

    def _get_subtype(self):
        return self.Subtype(len(self._X), self._alpha, self._iscomplex)

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
            None if self._u is None else self._u._replace_mutables(mapping),
        )

    def _freeze_mutables(self, freeze):
        return self.__class__(
            self._X._freeze_mutables(freeze), 
            self._Y._freeze_mutables(freeze),
            None if self._u is None else self._u._freeze_mutables(freeze),
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
    def u(self):
        """The additional expression :math:`u`."""
        return self._u

    @property
    def alpha(self):
        r"""The alpha :math:`\alpha`."""
        return self._alpha

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

        if not issubclass(other.clstype, AffineExpression):
            return NotImplemented
        
        if relation == operator.__le__:
            if subtype.iscomplex:
                return cls._ComplexConstraint().make_type(argdim=subtype.argdim)
            else:
                return cls._RealConstraint().make_type(argdim=subtype.argdim)

        return NotImplemented

    @convert_operands(scalarRHS=True)
    @validate_prediction
    @refine_operands()
    def __le__(self, other):
        if not isinstance(other, AffineExpression):
            return NotImplemented

        if self.iscomplex:
            return self._ComplexConstraint()(self, other)
        else:
            return self._RealConstraint()(self, other)


class RenyiEntropy(BaseRenyiEntropy):
    r"""Renyi entropy of an affine expression.

    :Definition:

    Let :math:`X` and :math:`Y` be :math:`N \times N`-dimensional symmetric
    or hermitian matrices. Then this is defined as

    .. math::

        \frac{1}{\alpha-1}\log(\operatorname{Tr}[ X^\alpha Y^{1-\alpha} ]),

    for some :math:`\alpha\in[0, 1)`.

    .. warning::

        When you pose an upper or lower bound on this expression, then PICOS
        enforces :math:`X \succeq 0` and :math:`Y \succeq 0` through an
        auxiliary constraint during solution search.
    """

    # --------------------------------------------------------------------------
    # Initialization and factory methods.
    # --------------------------------------------------------------------------

    def _is_valid_alpha(self, alpha):
        if not (numpy.isscalar(alpha) and 0 <= alpha and alpha < 1):
            raise TypeError("The exponent alpha must be a scalar in [0, 1)")
        
    def _get_strings(self):
        typeStr = "Renyi Entropy"
        symbStr = glyphs.renyi(str(self._alpha), self._X.string, self._Y.string)
        return typeStr, symbStr

    # --------------------------------------------------------------------------
    # Abstract method implementations and method overridings, except _predict.
    # --------------------------------------------------------------------------

    def _get_value(self):
        X = cvx2np(self._X._get_value())
        Y = cvx2np(self._Y._get_value())
        u = cvx2np(self._u._get_value()) if self._u is not None else 1

        Dx, Ux = numpy.linalg.eigh(X)
        X_alpha = Ux @ numpy.diag(numpy.power(Dx, self._alpha)) @ Ux.conj().T

        Dy, Uy = numpy.linalg.eigh(Y)
        Y_beta = Uy @ numpy.diag(numpy.power(Dy, 1 - self._alpha)) @ Uy.conj().T

        t = numpy.sum(X_alpha * Y_beta.conj()).real
        s = u * numpy.log(t / u) / (self._alpha - 1)

        return cvxopt.matrix(s)

    # --------------------------------------------------------------------------
    # Constraint-creating operators, and _predict.
    # --------------------------------------------------------------------------

    @classmethod
    def _ComplexConstraint(cls):
        return ComplexRenyiEntrConstraint
    
    @classmethod
    def _RealConstraint(cls):
        return RenyiEntrConstraint


class SandRenyiEntropy(BaseRenyiEntropy):
    r"""Sandwiched Renyi entropy of an affine expression.

    :Definition:

    Let :math:`X` and :math:`Y` be :math:`N \times N`-dimensional symmetric
    or hermitian matrices. Then this is defined as

    .. math::

        \frac{1}{\alpha-1}\log(\operatorname{Tr}[ (Y^{\frac{1-\alpha}{2\alpha}}
        X Y^{\frac{1-\alpha}{2\alpha}})^\alpha ]),

    for some :math:`\alpha\in[1/2, 1)`.

    .. warning::

        When you pose an upper or lower bound on this expression, then PICOS
        enforces :math:`X \succeq 0` and :math:`Y \succeq 0` through an
        auxiliary constraint during solution search.
    """

    # --------------------------------------------------------------------------
    # Initialization and factory methods.
    # --------------------------------------------------------------------------

    def _is_valid_alpha(self, alpha):
        if not (numpy.isscalar(alpha) and 0.5 <= alpha and alpha < 1):
            raise TypeError("The exponent alpha must be a scalar in [1/2, 1)")

    def _get_strings(self):
        typeStr = "Sandwiched Renyi Entropy"
        symbStr = glyphs.renyi(str(self._alpha), self._X.string, self._Y.string)
        return typeStr, symbStr

    # --------------------------------------------------------------------------
    # Abstract method implementations and method overridings, except _predict.
    # --------------------------------------------------------------------------

    def _get_value(self):
        X = cvx2np(self._X._get_value())
        Y = cvx2np(self._Y._get_value())
        u = cvx2np(self._u._get_value()) if self._u is not None else 1

        Dy, Uy = numpy.linalg.eigh(Y)
        Dy_beta = numpy.power(Dy, (1 - self._alpha) / (2 * self._alpha))
        Y_beta = Uy @ numpy.diag(Dy_beta) @ Uy.conj().T

        Dyxy = numpy.linalg.eigvalsh(Y_beta @ X @ Y_beta)

        t = numpy.sum(numpy.power(Dyxy, self._alpha))
        s = u * numpy.log(t / u) / (self._alpha - 1)

        return cvxopt.matrix(s)

    # --------------------------------------------------------------------------
    # Constraint-creating operators, and _predict.
    # --------------------------------------------------------------------------

    @classmethod
    def _ComplexConstraint(cls):
        return ComplexSandRenyiEntrConstraint
    
    @classmethod
    def _RealConstraint(cls):
        return SandRenyiEntrConstraint


class BaseQuasiEntropy(Expression):
    r"""Base class defining a general quasi-relative entropy expression."""

    # --------------------------------------------------------------------------
    # Initialization and factory methods.
    # --------------------------------------------------------------------------

    @convert_and_refine_arguments("X", "Y")
    def __init__(self, X, Y, alpha):
        """Construct an :class:`BaseQuasiEntropy`.

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
        
        self._is_valid_alpha(alpha)

        self._X = X
        self._Y = Y
        self._alpha = alpha

        self._iscomplex = not isinstance(X, AffineExpression) or \
                          not isinstance(Y, AffineExpression)

        typeStr, symbStr = self._get_strings()

        Expression.__init__(self, typeStr, symbStr)

    # --------------------------------------------------------------------------
    # Abstract method implementations and method overridings, except _predict.
    # --------------------------------------------------------------------------

    def _get_refined(self):
        if self._X.constant and self._Y.constant:
            return AffineExpression.from_constant(self.value, 1, self._symbStr)
        else:
            return self

    Subtype = namedtuple("Subtype", ("argdim", "alpha", "iscomplex"))

    def _get_subtype(self):
        return self.Subtype(len(self._X), self._alpha, self._iscomplex)

    @cached_unary_operator
    def _get_mutables(self):
        return self._X._get_mutables().union(self._Y.mutables)

    def _is_convex(self):
        return (-1 <= self._alpha and self._alpha <= 0) or \
               ( 1 <= self._alpha and self._alpha <= 2)

    def _is_concave(self):
        return 0 <= self._alpha and self._alpha <= 1

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
    def alpha(self):
        r"""The alpha :math:`\alpha`."""
        return self._alpha

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

        if not issubclass(other.clstype, AffineExpression):
            return NotImplemented

        if other.subtype.dim != 1:
            return NotImplemented

        isconvex = (-1 <= subtype.alpha and subtype.alpha <= 0) or \
                   ( 1 <= subtype.alpha and subtype.alpha <= 2)
        isconcave = 0 <= subtype.alpha and subtype.alpha <= 1
        argdim = subtype.argdim

        if relation == operator.__le__ and isconvex:
            if subtype.iscomplex or not issubclass(
                other.clstype, AffineExpression
            ):
                return cls._ComplexEpiConstraint().make_type(argdim=argdim)
            else:
                return cls._RealEpiConstraint().make_type(argdim=argdim)

        if relation == operator.__ge__ and isconcave:
            if subtype.iscomplex or not issubclass(
                other.clstype, AffineExpression
            ):
                return cls._ComplexHypoConstraint().make_type(argdim=argdim)
            else:
                return cls._RealHypoConstraint().make_type(argdim=argdim)

        return NotImplemented

    @convert_operands(scalarRHS=True)
    @validate_prediction
    @refine_operands()
    def __le__(self, other):
        if self.convex and isinstance(other, AffineExpression):
            if self.iscomplex:
                return self._ComplexEpiConstraint()(self, other)
            else:
                return self._RealEpiConstraint()(self, other)
        else:
            return NotImplemented

    @convert_operands(scalarRHS=True)
    @validate_prediction
    @refine_operands()
    def __ge__(self, other):
        if self.concave and isinstance(other, AffineExpression):
            if self.iscomplex:
                return self._ComplexHypoConstraint()(self, other)
            else:
                return self._RealHypoConstraint()(self, other)
        else:
            return NotImplemented
        
class QuasiEntropy(BaseQuasiEntropy):
    r"""Quasi-relative entropy of an affine expression.

    :Definition:

    Let :math:`X` and :math:`Y` be :math:`N \times N`-dimensional symmetric
    or hermitian matrices. Then this is defined as

    .. math::

        \operatorname{Tr}[ X^\alpha Y^{1-\alpha} ],

    for some :math:`\alpha\in[-1, 2]`.

    .. warning::

        When you pose an upper or lower bound on this expression, then PICOS
        enforces :math:`X \succeq 0` and :math:`Y \succeq 0` through an
        auxiliary constraint during solution search.
    """

    # --------------------------------------------------------------------------
    # Initialization and factory methods.
    # --------------------------------------------------------------------------

    def _is_valid_alpha(self, alpha):
        if not (numpy.isscalar(alpha) and -1 <= alpha and alpha <= 2):
            raise TypeError("The exponent alpha must be a scalar in [-1, 2]")
        
    def _get_strings(self):
        typeStr = "Quasi-Relative Entropy"
        xStr = glyphs.power(self._X.string, "a")
        yStr = glyphs.power(self._Y.string, "1-a")
        symbStr = glyphs.trace(glyphs.mul(xStr, yStr))
        return typeStr, symbStr

    # --------------------------------------------------------------------------
    # Abstract method implementations and method overridings, except _predict.
    # --------------------------------------------------------------------------

    def _get_value(self):
        X = cvx2np(self._X._get_value())
        Y = cvx2np(self._Y._get_value())

        Dx, Ux = numpy.linalg.eigh(X)
        X_alpha = Ux @ numpy.diag(numpy.power(Dx, self._alpha)) @ Ux.conj().T

        Dy, Uy = numpy.linalg.eigh(Y)
        Y_beta = Uy @ numpy.diag(numpy.power(Dy, 1 - self._alpha)) @ Uy.conj().T

        s = numpy.sum(X_alpha * Y_beta.conj()).real

        return cvxopt.matrix(s)

    # --------------------------------------------------------------------------
    # Constraint-creating operators, and _predict.
    # --------------------------------------------------------------------------

    @classmethod
    def _RealEpiConstraint(cls):
        return QuasiEntrEpiConstraint
    
    @classmethod
    def _ComplexEpiConstraint(cls):
        return ComplexQuasiEntrEpiConstraint

    @classmethod
    def _RealHypoConstraint(cls):
        return QuasiEntrHypoConstraint
    
    @classmethod
    def _ComplexHypoConstraint(cls):
        return ComplexQuasiEntrHypoConstraint
    

class SandQuasiEntropy(BaseQuasiEntropy):
    r"""Sandwiched quasi-relative entropy of an affine expression.

    :Definition:

    Let :math:`X` and :math:`Y` be :math:`N \times N`-dimensional symmetric
    or hermitian matrices. Then this is defined as

    .. math::

        \operatorname{Tr}[ (Y^{\frac{1-\alpha}{2\alpha}}
        X Y^{\frac{1-\alpha}{2\alpha}})^\alpha ],

    for some :math:`\alpha\in[1/2, 2]`.

    .. warning::

        When you pose an upper or lower bound on this expression, then PICOS
        enforces :math:`X \succeq 0` and :math:`Y \succeq 0` through an
        auxiliary constraint during solution search.
    """

    # --------------------------------------------------------------------------
    # Initialization and factory methods.
    # --------------------------------------------------------------------------

    def _is_valid_alpha(self, alpha):
        if not (numpy.isscalar(alpha) and 0.5 <= alpha and alpha <= 2):
            raise TypeError("The exponent alpha must be a scalar in [1/2, 2]")
        
    def _get_strings(self):
        typeStr = "Sandwiched Quasi-Relative Entropy"
        xStr = self._X.string
        yStr = glyphs.power(self._Y.string, "(1-a)/2a")
        symbStr = glyphs.power(glyphs.mul(glyphs.mul(yStr, xStr), yStr), "a")
        symbStr = glyphs.trace(symbStr)
        return typeStr, symbStr

    # --------------------------------------------------------------------------
    # Abstract method implementations and method overridings, except _predict.
    # --------------------------------------------------------------------------

    def _get_value(self):
        X = cvx2np(self._X._get_value())
        Y = cvx2np(self._Y._get_value())

        Dy, Uy = numpy.linalg.eigh(Y)
        Dy_beta = numpy.power(Dy, (1 - self._alpha) / (2 * self._alpha))
        Y_beta = Uy @ numpy.diag(Dy_beta) @ Uy.conj().T

        Dyxy = numpy.linalg.eigvalsh(Y_beta @ X @ Y_beta)

        s = numpy.sum(numpy.power(Dyxy, self._alpha))

        return cvxopt.matrix(s)

    # --------------------------------------------------------------------------
    # Constraint-creating operators, and _predict.
    # --------------------------------------------------------------------------

    @classmethod
    def _RealEpiConstraint(cls):
        return SandQuasiEntrEpiConstraint
    
    @classmethod
    def _ComplexEpiConstraint(cls):
        return ComplexSandQuasiEntrEpiConstraint

    @classmethod
    def _RealHypoConstraint(cls):
        return SandQuasiEntrHypoConstraint
    
    @classmethod
    def _ComplexHypoConstraint(cls):
        return ComplexSandQuasiEntrHypoConstraint

# --------------------------------------
__all__ = api_end(_API_START, globals())
