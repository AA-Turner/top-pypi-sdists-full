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

"""Implementation of :class:`QuantKeyDistributionConstraint`."""

from collections import namedtuple

from .. import glyphs
from ..apidoc import api_end, api_start
from ..caching import cached_property
from .constraint import Constraint

_API_START = api_start(globals())
# -------------------------------


class QuantKeyDistributionConstraint(Constraint):
    """Upper bound on a quantum key distribution function.

    This is the upper bound on a quantum key distribution function, represented
    by :class:`~picos.expressions.QuantumKeyDistribution`.
    """

    def __init__(self, function, upperBound):
        """Construct a :class:`QuantKeyDistributionConstraint`.

        :param ~picos.expressions.QuantumKeyDistribution function:
            Constrained expression.
        :param ~picos.expressions.AffineExpression upperBound:
            Upper bound on the expression.
        """
        from ..expressions import AffineExpression, QuantumKeyDistribution

        assert isinstance(function, QuantumKeyDistribution)
        assert isinstance(upperBound, AffineExpression)
        assert len(upperBound) == 1

        self.function = function
        self.upperBound = upperBound

        required_type = self._required_type()

        assert isinstance(function.X, required_type)

        super(QuantKeyDistributionConstraint, self).__init__(function._typeStr)

    def _required_type(self):
        from ..expressions import AffineExpression

        return AffineExpression

    @property
    def X(self):
        """The :math:`X` of the function."""
        return self.function.X

    @cached_property
    def subsystems(self):
        """The subsystems being block-diagonalized of :math:`X`."""
        return self.function.subsystems

    @cached_property
    def dimensions(self):
        """The dimensions of the subsystems of :math:`X`."""
        return self.function.dimensions

    @cached_property
    def K_list(self):
        r"""The Kraus operators :math:`K_i` of :math:`\mathcal{G}`."""
        return self.function.K_list

    @cached_property
    def Z_list(self):
        r"""The Kraus operators :math:`Z_i` of :math:`\mathcal{Z}`."""
        return self.function.Z_list

    Subtype = namedtuple("Subtype", ("argdim",))

    def _subtype(self):
        return self.Subtype(self.X.shape[0] ** 2)

    @classmethod
    def _cost(cls, subtype):
        n = subtype.argdim
        return n * (n + 1) // 2 + 1

    def _expression_names(self):
        yield "function"
        yield "upperBound"

    def _str(self):
        return glyphs.le(self.function.string, self.upperBound.string)

    def _get_size(self):
        n = self.X.shape[0]
        return (n * n + 1, 1)

    def _get_slack(self):
        return self.upperBound.safe_value - self.function.safe_value


class ComplexQuantKeyDistributionConstraint(QuantKeyDistributionConstraint):
    """Upper bound on a complex quantum key distribution function."""

    # TODO: Implement real conversion of quantum conditional entropy cone

    def _required_type(self):
        from ..expressions import ComplexAffineExpression

        return ComplexAffineExpression


# --------------------------------------
__all__ = api_end(_API_START, globals())
