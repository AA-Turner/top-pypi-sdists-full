# ------------------------------------------------------------------------------
# Copyright (C) 2025 Kerry He
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

"""Renyi entropy constraints."""

from collections import namedtuple

from .. import glyphs
from ..apidoc import api_end, api_start
from ..caching import cached_property
from .constraint import Constraint

_API_START = api_start(globals())
# -------------------------------


class BaseRenyiEntrConstraint(Constraint):
    """Base class representing general Renyi entropy constraints."""

    def __init__(self, divergence, upperBound):
        """Construct a :class:`BaseRenyiEntrConstraint`.

        :param ~picos.expressions.QuasiEntropy divergence:
            Constrained expression.
        :param ~picos.expressions.AffineExpression upperBound:
            Upper bound on the expression.
        """
        from ..expressions import AffineExpression
        required_divergence = self._required_divergence()
        required_type = self._required_type()

        assert isinstance(divergence, required_divergence)
        assert isinstance(upperBound, AffineExpression)
        assert len(upperBound) == 1
        assert self._is_valid_alpha(divergence.alpha)

        self.divergence = divergence
        self.upperBound = upperBound

        assert isinstance(divergence.X, required_type)
        assert isinstance(divergence.Y, required_type)
        assert isinstance(divergence.u, AffineExpression) \
            or divergence.u is None

        super(BaseRenyiEntrConstraint, self).__init__(divergence._typeStr)

    def _required_type(self):
        from ..expressions import AffineExpression

        return AffineExpression

    @cached_property
    def u(self):
        r"""The :math:`u` of the divergence, or :math:`1`."""
        from ..expressions import AffineExpression

        if self.divergence.u is None:
            return AffineExpression.from_constant(1)
        else:
            return self.divergence.u

    @property
    def X(self):
        """The :math:`X` of the divergence."""
        return self.divergence.X

    @property
    def Y(self):
        """The :math:`Y` of the divergence."""
        return self.divergence.Y

    @property
    def alpha(self):
        r"""The parameter :math:`\alpha`."""
        return self.divergence.alpha

    Subtype = namedtuple("Subtype", ("argdim",))

    def _subtype(self):
        return self.Subtype(self.X.shape[0] ** 2)

    @classmethod
    def _cost(cls, subtype):
        n = subtype.argdim
        return n * (n + 1) + 2

    def _expression_names(self):
        yield "divergence"
        yield "upperBound"

    def _str(self):
        return glyphs.le(self.divergence.string, self.upperBound.string)

    def _get_size(self):
        n = self.X.shape[0]
        return (2 * n * n + 1, 2)

    def _get_slack(self):
        return self.upperBound.safe_value - self.divergence.safe_value

class RenyiEntrConstraint(BaseRenyiEntrConstraint):
    """Upper bound of Renyi entropies.

    This is the upper bound on Renyi entropies, represented by 
    :class:`~picos.expressions.RenyiEntropy`.
    """

    def _required_divergence(self):
        from ..expressions import RenyiEntropy

        return RenyiEntropy

    def _is_valid_alpha(self, alpha):
        return 0 <= alpha and alpha < 1

class ComplexRenyiEntrConstraint(RenyiEntrConstraint):
    """Upper bound of complex Renyi entropies."""

    def _required_type(self):
        from ..expressions import ComplexAffineExpression

        return ComplexAffineExpression

class SandRenyiEntrConstraint(BaseRenyiEntrConstraint):
    """Upper bound of sandwiched Renyi entropies.

    This is the upper bound on sandwiched Renyi entropies, represented by 
    :class:`~picos.expressions.SandRenyiEntropy`.
    """

    def _required_divergence(self):
        from ..expressions import SandRenyiEntropy

        return SandRenyiEntropy

    def _is_valid_alpha(self, alpha):
        return 0.5 <= alpha and alpha < 1

class ComplexSandRenyiEntrConstraint(SandRenyiEntrConstraint):
    """Upper bound of complex sandwiched Renyi entropies."""

    def _required_type(self):
        from ..expressions import ComplexAffineExpression

        return ComplexAffineExpression


# ----------------

class BaseQuasiEntrEpiConstraint(Constraint):
    """Base class for upper bound on quasi-relative entropies."""

    def __init__(self, divergence, upperBound):
        """Construct a :class:`BaseQuasiEntrEpiConstraint`.

        :param ~picos.expressions.QuasiEntropy divergence:
            Constrained expression.
        :param ~picos.expressions.AffineExpression upperBound:
            Upper bound on the expression.
        """
        from ..expressions import AffineExpression
        required_divergence = self._required_divergence()
        required_type = self._required_type()

        assert isinstance(divergence, required_divergence)
        assert isinstance(upperBound, AffineExpression)
        assert len(upperBound) == 1
        assert self._is_valid_alpha(divergence.alpha)

        self.divergence = divergence
        self.upperBound = upperBound

        assert isinstance(divergence.X, required_type)
        assert isinstance(divergence.Y, required_type)

        super(BaseQuasiEntrEpiConstraint, self).__init__(divergence._typeStr)

    def _required_type(self):
        from ..expressions import AffineExpression

        return AffineExpression

    @property
    def X(self):
        """The :math:`X` of the divergence."""
        return self.divergence.X

    @cached_property
    def Y(self):
        """The :math:`Y` of the divergence."""
        return self.divergence.Y

    @cached_property
    def alpha(self):
        r"""The parameter :math:`\alpha`."""
        return self.divergence.alpha

    Subtype = namedtuple("Subtype", ("argdim",))

    def _subtype(self):
        return self.Subtype(self.X.shape[0] ** 2)

    @classmethod
    def _cost(cls, subtype):
        n = subtype.argdim
        return n * (n + 1) + 2

    def _expression_names(self):
        yield "divergence"
        yield "upperBound"

    def _str(self):
        return glyphs.le(self.divergence.string, self.upperBound.string)

    def _get_size(self):
        n = self.X.shape[0]
        return (2 * n * n + 1, 2)

    def _get_slack(self):
        return self.upperBound.safe_value - self.divergence.safe_value


class QuasiEntrEpiConstraint(BaseQuasiEntrEpiConstraint):
    """Upper bound of convex quasi-relative entropies.

    This is the upper bound on convex trace functions used to define Renyi
    entropies, represented by :class:`~picos.expressions.QuasiEntropy`.
    """

    def _required_divergence(self):
        from ..expressions import QuasiEntropy

        return QuasiEntropy

    def _is_valid_alpha(self, alpha):
        return (-1 <= alpha and alpha <= 0) or (1 <= alpha and alpha <= 2)


class ComplexQuasiEntrEpiConstraint(QuasiEntrEpiConstraint):
    """Upper bound of complex convex quasi-relative entropies."""

    def _required_type(self):
        from ..expressions import ComplexAffineExpression

        return ComplexAffineExpression
    

class SandQuasiEntrEpiConstraint(BaseQuasiEntrEpiConstraint):
    """Upper bound of convex sandwiched quasi-relative entropies.

    This is the upper bound on convex trace functions used to define sandwiched
    Renyi entropies, represented by 
    :class:`~picos.expressions.SandQuasiEntropy`.
    """

    def _required_divergence(self):
        from ..expressions import SandQuasiEntropy

        return SandQuasiEntropy

    def _is_valid_alpha(self, alpha):
        return 1 <= alpha and alpha <= 2


class ComplexSandQuasiEntrEpiConstraint(SandQuasiEntrEpiConstraint):
    """Upper bound of complex trace func. used for sand. Renyi entropies."""

    def _required_type(self):
        from ..expressions import ComplexAffineExpression

        return ComplexAffineExpression

# --------------


class BaseQuasiEntrHypoConstraint(Constraint):
    """Base class for lower bound on concave quasi-relative entropies."""

    def __init__(self, divergence, lowerBound):
        """Construct a :class:`BaseQuasiEntrHypoConstraint`.

        :param ~picos.expressions.QuasiEntropy divergence:
            Constrained expression.
        :param ~picos.expressions.AffineExpression lowerBound:
            Lower bound on the expression.
        """
        from ..expressions import AffineExpression
        required_divergence = self._required_divergence()
        required_type = self._required_type()

        assert isinstance(divergence, required_divergence)
        assert isinstance(lowerBound, AffineExpression)
        assert len(lowerBound) == 1
        assert self._is_valid_alpha(divergence.alpha)

        self.divergence = divergence
        self.lowerBound = lowerBound

        required_type = self._required_type()

        assert isinstance(divergence.X, required_type)
        assert isinstance(divergence.Y, required_type)

        super(BaseQuasiEntrHypoConstraint, self).__init__(divergence._typeStr)

    def _required_type(self):
        from ..expressions import AffineExpression

        return AffineExpression

    @property
    def X(self):
        """The :math:`X` of the divergence."""
        return self.divergence.X

    @cached_property
    def Y(self):
        """The :math:`Y` of the divergence."""
        return self.divergence.Y

    @cached_property
    def alpha(self):
        r"""The parameter :math:`\alpha`."""
        return self.divergence.alpha

    Subtype = namedtuple("Subtype", ("argdim",))

    def _subtype(self):
        return self.Subtype(self.X.shape[0] ** 2)

    @classmethod
    def _cost(cls, subtype):
        n = subtype.argdim
        return n * (n + 1) + 1

    def _expression_names(self):
        yield "divergence"
        yield "lowerBound"

    def _str(self):
        return glyphs.ge(self.divergence.string, self.lowerBound.string)

    def _get_size(self):
        n = self.X.shape[0]
        return (2 * n * n + 1, 1)

    def _get_slack(self):
        return self.lowerBound.safe_value - self.divergence.safe_value

class QuasiEntrHypoConstraint(BaseQuasiEntrHypoConstraint):
    """Lower bound of concave quasi-relative entropies.

    This is the lower bound on concave trace functions used to define Renyi
    entropies, represented by :class:`~picos.expressions.QuasiEntropy`.
    """

    def _required_divergence(self):
        from ..expressions import QuasiEntropy

        return QuasiEntropy

    def _is_valid_alpha(self, alpha):
        return 0 <= alpha and alpha <= 1


class ComplexQuasiEntrHypoConstraint(QuasiEntrHypoConstraint):
    """Lower bound of complex concave quasi-relative entropies."""

    def _required_type(self):
        from ..expressions import ComplexAffineExpression

        return ComplexAffineExpression
    

class SandQuasiEntrHypoConstraint(BaseQuasiEntrHypoConstraint):
    """Lower bound of concave sandwiched quasi-relative entropies.

    This is the lower bound on concave trace functions used to define sandwiched
    Renyi entropies, represented by
    :class:`~picos.expressions.SandQuasiEntropy`.
    """

    def _required_divergence(self):
        from ..expressions import SandQuasiEntropy

        return SandQuasiEntropy

    def _is_valid_alpha(self, alpha):
        return 0.5 <= alpha and alpha <= 1


class ComplexSandQuasiEntrHypoConstraint(SandQuasiEntrHypoConstraint):
    """Lower bound of complex concave sandwiched quasi-relative entropies."""

    def _required_type(self):
        from ..expressions import ComplexAffineExpression

        return ComplexAffineExpression
    
# --------------------------------------
__all__ = api_end(_API_START, globals())
