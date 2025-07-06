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

"""Implementation of :class:`QuantCondEntropyConstraint`."""

from collections import namedtuple

from .. import glyphs
from ..apidoc import api_end, api_start
from ..caching import cached_property
from .constraint import Constraint

_API_START = api_start(globals())
# -------------------------------


class QuantCondEntropyConstraint(Constraint):
    """Lower bound on a quantum conditional entropy.

    This is the lower bound on a quantum conditional entropy, represented by
    :class:`~picos.expressions.QuantumConditionalEntropy`.
    """

    def __init__(self, function, lowerBound):
        """Construct a :class:`QuantCondEntropyConstraint`.

        :param ~picos.expressions.QuantumConditionalEntropy function:
            Constrained expression.
        :param ~picos.expressions.AffineExpression lowerBound:
            Lower bound on the expression.
        """
        from ..expressions import AffineExpression, QuantumConditionalEntropy

        assert isinstance(function, QuantumConditionalEntropy)
        assert isinstance(lowerBound, AffineExpression)
        assert len(lowerBound) == 1

        self.function = function
        self.lowerBound = lowerBound

        required_type = self._required_type()

        assert isinstance(function.X, required_type)

        super(QuantCondEntropyConstraint, self).__init__(function._typeStr)

    def _required_type(self):
        from ..expressions import AffineExpression

        return AffineExpression

    @property
    def X(self):
        """The :math:`X` of the function."""
        return self.function.X

    @cached_property
    def subsystems(self):
        """The subsystems being traced out of :math:`X`."""
        return self.function.subsystems

    @cached_property
    def dimensions(self):
        """The dimensions of the subsystems of :math:`X`."""
        return self.function.dimensions

    Subtype = namedtuple("Subtype", ("argdim",))

    def _subtype(self):
        return self.Subtype(self.X.shape[0] ** 2)

    @classmethod
    def _cost(cls, subtype):
        n = subtype.argdim
        return n * (n + 1) // 2 + 1

    def _expression_names(self):
        yield "function"
        yield "lowerBound"

    def _str(self):
        return glyphs.ge(self.function.string, self.lowerBound.string)

    def _get_size(self):
        n = self.X.shape[0]
        return (n * n + 1, 1)

    def _get_slack(self):
        return self.function.safe_value - self.lowerBound.safe_value


class ComplexQuantCondEntropyConstraint(QuantCondEntropyConstraint):
    """Lower bound on a complex quantum conditional entropy."""

    # TODO: Implement real conversion of quantum conditional entropy cone

    def _required_type(self):
        from ..expressions import ComplexAffineExpression

        return ComplexAffineExpression


# --------------------------------------
__all__ = api_end(_API_START, globals())
