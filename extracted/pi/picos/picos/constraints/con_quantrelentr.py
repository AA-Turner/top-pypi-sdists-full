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

"""Implementation of :class:`QuantRelEntropyConstraint`."""

from collections import namedtuple

from .. import glyphs
from ..apidoc import api_end, api_start
from ..caching import cached_property
from .constraint import Constraint

_API_START = api_start(globals())
# -------------------------------


class QuantRelEntropyConstraint(Constraint):
    """Upper bound on a quantum relative entropy.

    This is the upper bound on a negative or relative quantum entropy, both
    represented by :class:`~picos.expressions.NegativeQuantumEntropy`.
    """

    def __init__(self, divergence, upperBound):
        """Construct a :class:`QuantRelEntropyConstraint`.

        :param ~picos.expressions.NegativeQuantumEntropy divergence:
            Constrained expression.
        :param ~picos.expressions.AffineExpression upperBound:
            Upper bound on the expression.
        """
        from ..expressions import AffineExpression, NegativeQuantumEntropy

        assert isinstance(divergence, NegativeQuantumEntropy)
        assert isinstance(upperBound, AffineExpression)
        assert len(upperBound) == 1

        self.divergence = divergence
        self.upperBound = upperBound

        required_type = self._required_type()

        assert isinstance(divergence.X, required_type)
        assert isinstance(divergence.Y, required_type) or divergence.Y is None

        super(QuantRelEntropyConstraint, self).__init__(divergence._typeStr)

    def _required_type(self):
        from ..expressions import AffineExpression

        return AffineExpression

    @property
    def X(self):
        """The :math:`X` of the divergence."""
        return self.divergence.X

    @cached_property
    def Y(self):
        r"""The :math:`Y` of the divergence, or :math:`\mathbb{I}`."""
        from ..expressions import AffineExpression

        if self.divergence.Y is None:
            import numpy

            return AffineExpression.from_constant(
                numpy.eye(self.divergence.X.shape[0])
            )
        else:
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


class ComplexQuantRelEntropyConstraint(QuantRelEntropyConstraint):
    """Upper bound on a complex quantum relative entropy."""

    # TODO: Implement real conversion of quantum key distribution cone

    def _required_type(self):
        from ..expressions import ComplexAffineExpression

        return ComplexAffineExpression


# --------------------------------------
__all__ = api_end(_API_START, globals())
