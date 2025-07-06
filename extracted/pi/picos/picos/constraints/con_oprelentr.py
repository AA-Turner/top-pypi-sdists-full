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

"""Operator relative entropy constraints."""

from collections import namedtuple

from .. import glyphs
from ..apidoc import api_end, api_start
from ..caching import cached_property
from .constraint import Constraint

_API_START = api_start(globals())
# -------------------------------


class OpRelEntropyConstraint(Constraint):
    """Epigraph of an operator relative entropy.

    This is the upper bound, in the Loewner order, of an operator relative
    entropy, represented by :class:`~picos.expressions.OperatorRelativeEntropy`.
    """

    def __init__(self, divergence, upperBound):
        """Construct a :class:`OpRelEntropyConstraint`.

        :param ~picos.expressions.OperatorRelativeEntropy divergence:
            Constrained expression.
        :param ~picos.expressions.AffineExpression upperBound:
            Upper bound on the expression.
        """
        from ..expressions import OperatorRelativeEntropy

        required_type = self._required_type()

        assert isinstance(divergence, OperatorRelativeEntropy)
        assert isinstance(upperBound, required_type)
        assert divergence.shape == upperBound.shape

        self.divergence = divergence
        self.upperBound = upperBound

        assert isinstance(divergence.X, required_type)
        assert isinstance(divergence.Y, required_type)

        super(OpRelEntropyConstraint, self).__init__(divergence._typeStr)

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

    Subtype = namedtuple("Subtype", ("argdim",))

    def _subtype(self):
        return self.Subtype(self.X.shape[0] ** 2)

    @classmethod
    def _cost(cls, subtype):
        n = subtype.argdim
        return n * (n + 1) // 2 * 3

    def _expression_names(self):
        yield "divergence"
        yield "upperBound"

    def _str(self):
        return glyphs.psdle(self.divergence.string, self.upperBound.string)

    def _get_size(self):
        n = self.X.shape[0]
        return (3 * n * n, 1)

    def _get_slack(self):
        return self.upperBound.safe_value - self.divergence.safe_value


class ComplexOpRelEntropyConstraint(OpRelEntropyConstraint):
    """Epigraph of a complex operator relative entropy."""

    # TODO: Implement real conversion of operator relative entropy epigraph

    def _required_type(self):
        from ..expressions import ComplexAffineExpression

        return ComplexAffineExpression


class TrOpRelEntropyConstraint(Constraint):
    """Upper bound of trace of operator relative entropy.

    This is the upper bound on the trace of an operator relative entropy,
    represented by :class:`~picos.expressions.TrOperatorRelativeEntropy`.
    """

    def __init__(self, divergence, upperBound):
        """Construct a :class:`TrOpRelEntropyConstraint`.

        :param ~picos.expressions.TrOperatorRelativeEntropy divergence:
            Constrained expression.
        :param ~picos.expressions.AffineExpression upperBound:
            Upper bound on the expression.
        """
        from ..expressions import AffineExpression, TrOperatorRelativeEntropy

        assert isinstance(divergence, TrOperatorRelativeEntropy)
        assert isinstance(upperBound, AffineExpression)
        assert len(upperBound) == 1

        self.divergence = divergence
        self.upperBound = upperBound

        required_type = self._required_type()

        assert isinstance(divergence.X, required_type)
        assert isinstance(divergence.Y, required_type)

        super(TrOpRelEntropyConstraint, self).__init__(divergence._typeStr)

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

    Subtype = namedtuple("Subtype", ("argdim",))

    def _subtype(self):
        return self.Subtype(self.X.shape[0] ** 2)

    @classmethod
    def _cost(cls, subtype):
        n = subtype.argdim
        return n * (n + 1) + 1

    def _expression_names(self):
        yield "divergence"
        yield "upperBound"

    def _str(self):
        return glyphs.le(self.divergence.string, self.upperBound.string)

    def _get_size(self):
        n = self.X.shape[0]
        return (2 * n * n + 1, 1)

    def _get_slack(self):
        return self.upperBound.safe_value - self.divergence.safe_value


class ComplexTrOpRelEntropyConstraint(TrOpRelEntropyConstraint):
    """Upper bound of trace of complex operator relative entropy."""

    # TODO: Implement real conversion of operator relative entropy cone

    def _required_type(self):
        from ..expressions import ComplexAffineExpression

        return ComplexAffineExpression


# --------------------------------------
__all__ = api_end(_API_START, globals())
