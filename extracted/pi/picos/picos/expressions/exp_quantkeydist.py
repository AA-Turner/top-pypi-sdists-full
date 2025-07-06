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

"""Implements :class:`QuantumKeyDistribution`."""

# TODO: Common base class for QuantumEntropy and NegativeQuantumEntropy.

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
    QuantKeyDistributionConstraint,
    ComplexQuantKeyDistributionConstraint,
)
from .data import convert_and_refine_arguments, convert_operands, cvx2np
from .exp_affine import AffineExpression, ComplexAffineExpression
from .expression import Expression, refine_operands, validate_prediction

_API_START = api_start(globals())
# -------------------------------


class QuantumKeyDistribution(Expression):
    r"""Slice of quantum relative entropy used to compute quantum key rates.

    :Definition:

    Let :math:`X` be an :math:`n \times n`-dimensional symmetric or hermitian
    matrix. Let :math:`\mathcal{Z}` be the pinching map which maps off-diagonal
    blocks of a given block structure to zero, i.e., for a bipartite state

    .. math::

        \mathcal{Z}(X) = \sum_{i} Z_i X Z_i^\dagger,

    where :math:`Z_i= | i \rangle \langle i | \otimes \mathbb{I}` if we block-
    diagonalize over the first subsystem, and :math:`Z_i= \mathbb{I} \otimes
    | i \rangle \langle i |` if we block-diagonalize over the second subsystem.
    We also generalize this definition to multipartite systems where we block-
    diagonalize over any number of subsystems.

    1.  In general, this is the expression

        .. math::

            -S(\mathcal{G}(X)) + S(\mathcal{Z}(\mathcal{G}(X))),

        where :math:`S(X)=-\operatorname{Tr}(X \log(X))` is the quantum entropy,
        :math:`mathcal{G}` is a positive linear map given by Kraus operators

        .. math::

            \mathcal{G}(X) = \sum_{i} K_i X K_i^\dagger.

    2.  If ``K_list=None``, then :math:`\mathcal{G}` is assumed to be the
        identity map, and then this expression is simplified to

        .. math::

            -S(X) + S(\mathcal{Z}(X)).

    .. warning::

        When you pose an upper bound on this expression, then PICOS enforces
        :math:`X \succeq 0` through an auxiliary constraint during solution
        search.
    """

    # --------------------------------------------------------------------------
    # Initialization and factory methods.
    # --------------------------------------------------------------------------

    @convert_and_refine_arguments("X")
    def __init__(self, X, subsystems=0, dimensions=2, K_list=None):
        r"""Construct an :class:`QuantumKeyDistribution`.

        :param X: The affine expression :math:`X`.
        :type X: ~picos.expressions.AffineExpression

        :param subsystems: A collection of or a single subystem number, indexed
            from zero, corresponding to subsystems that will be block-
            diagonalized over. The value :math:`-1` refers to the last
            subsystem.
        :type subsystems: int or tuple or list

        :param dimensions: Either an integer :math:`d` so that the subsystems
            are assumed to be all of shape :math:`d \times d`, or a sequence of
            subsystem shapes where an integer :math:`d` within the sequence is
            read as :math:`d \times d`. In any case, the elementwise product
            over all subsystem shapes must equal the expression's shape.
        :type dimensions: int or tuple or list

        :param K_list: A list of Kraus operators representing the linear map
            :math:`\mathcal{G}`. If ``K_list=None``, then :math:`\mathcal{G}`
            is defined as the identity map.
        :type K_list: None or list(numpy.ndarray)
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

        self._iscomplex = (not isinstance(X, AffineExpression)) or (
            K_list is not None
            and any([numpy.iscomplexobj(Ki) for Ki in K_list])
        )

        # Check that subsystems and dimension are compatible with X.
        if isinstance(dimensions, int):
            dimensions = self._square_equal_subsystem_dims(dimensions)
        else:
            dimensions = [
                (d, d) if isinstance(d, int) else d for d in dimensions
            ]

        if (
            reduce(lambda x, y: (x[0] * y[0], x[1] * y[1]), dimensions)
            != X.shape
        ):
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
        self._K_list = K_list

        self._build_Z_list()

        typeStr = "Quantum Key Distribution"
        if K_list is None:
            zxStr = "Z(" + X.string + ")"
            symbStr = glyphs.qre(X.string, zxStr)
        else:
            gxStr = "G(" + X.string + ")"
            gzxStr = "Z(G(" + X.string + "))"
            symbStr = glyphs.qre(gxStr, gzxStr)

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

    def _build_Z_list(self):
        r = numpy.meshgrid(
            *[range(self.dimensions[k][0]) for k in list(self.subsystems)]
        )
        r = list(numpy.array(r).reshape(len(self.subsystems), -1).T)
        self._Z_list = []
        for i in range(len(r)):
            Z_i = numpy.array([1])
            counter = 0
            for k, dimk in enumerate(self.dimensions):
                if k in self.subsystems:
                    Z_ik = numpy.zeros(dimk[0])
                    Z_ik[r[i][counter]] = 1
                    Z_i = numpy.kron(Z_i, Z_ik)
                    counter += 1
                else:
                    Z_i = numpy.kron(Z_i, numpy.ones(dimk[0]))
            self._Z_list += [numpy.diag(Z_i)]
        return self._Z_list

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
        if self.K_list is not None:
            X = sum([K @ X @ K.conj().T for K in self.K_list])
        eigX = numpy.linalg.eigvalsh(X)
        eigX = eigX[eigX > 1e-12]

        ZX = sum([Z @ X @ Z.conj().T for Z in self.Z_list])
        eigZX = numpy.linalg.eigvalsh(ZX)
        eigZX = eigZX[eigZX > 1e-12]

        s = numpy.dot(eigX, numpy.log(eigX))
        s -= numpy.dot(eigZX, numpy.log(eigZX))

        return cvxopt.matrix(s)

    @cached_unary_operator
    def _get_mutables(self):
        return self._X._get_mutables()

    def _is_convex(self):
        return True

    def _is_concave(self):
        return False

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
        """The subsystems being block-diagonalized of :math:`X`."""
        return self._subsystems

    @property
    def dimensions(self):
        """The dimensions of the subsystems of :math:`X`."""
        return self._dimensions

    @property
    def K_list(self):
        r"""The Kraus operators :math:`K_i` of :math:`\mathcal{G}`."""
        return self._K_list

    @property
    def Z_list(self):
        r"""The Kraus operators :math:`Z_i` of :math:`\mathcal{Z}`."""
        return self._Z_list

    @property
    def n(self):
        """Length of :attr:`X`."""
        return self._X.shape[0]

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

        if relation == operator.__le__:
            if (
                issubclass(other.clstype, AffineExpression)
                and other.subtype.dim == 1
            ):
                if subtype.iscomplex:
                    return ComplexQuantKeyDistributionConstraint.make_type(
                        argdim=subtype.argdim
                    )
                else:
                    return QuantKeyDistributionConstraint.make_type(
                        argdim=subtype.argdim
                    )
        return NotImplemented

    @convert_operands(scalarRHS=True)
    @validate_prediction
    @refine_operands()
    def __le__(self, other):
        if isinstance(other, AffineExpression):
            if self.iscomplex:
                return ComplexQuantKeyDistributionConstraint(self, other)
            else:
                return QuantKeyDistributionConstraint(self, other)
        else:
            return NotImplemented


# --------------------------------------
__all__ = api_end(_API_START, globals())
