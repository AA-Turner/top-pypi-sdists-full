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

"""Matrix geometric mean constraints."""

from collections import namedtuple

from .. import glyphs
from ..apidoc import api_end, api_start
from ..caching import cached_property
from .constraint import Constraint

_API_START = api_start(globals())
# -------------------------------


class MatrixGeoMeanEpiConstraint(Constraint):
    """Epigraph of a convex matrix geometric mean.

    This is the upper bound, in the Loewner order, of a convex matrix geometric
    mean, represented by :class:`~picos.expressions.MatrixGeometricMean`.
    """

    def __init__(self, divergence, upperBound):
        """Construct a :class:`MatrixGeoMeanEpiConstraint`.

        :param ~picos.expressions.MatrixGeometricMean divergence:
            Constrained expression.
        :param ~picos.expressions.AffineExpression upperBound:
            Upper bound on the expression.
        """
        from ..expressions import MatrixGeometricMean

        required_type = self._required_type()

        assert isinstance(divergence, MatrixGeometricMean)
        assert isinstance(upperBound, required_type)
        assert divergence.shape == upperBound.shape
        assert (-1 <= divergence.power and divergence.power <= 0) or \
               ( 1 <= divergence.power and divergence.power <= 2)

        self.divergence = divergence
        self.upperBound = upperBound

        assert isinstance(divergence.X, required_type)
        assert isinstance(divergence.Y, required_type)

        super(MatrixGeoMeanEpiConstraint, self).__init__(divergence._typeStr)

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
    def power(self):
        """The power :math:`p`."""
        return self.divergence.power

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


class ComplexMatrixGeoMeanEpiConstraint(MatrixGeoMeanEpiConstraint):
    """Epigraph of a complex convex matrix geometric mean."""

    # TODO: Implement real conversion of matrix geometric mean epigraph

    def _required_type(self):
        from ..expressions import ComplexAffineExpression

        return ComplexAffineExpression


class TrMatrixGeoMeanEpiConstraint(Constraint):
    """Upper bound of trace of a convex matrix geometric mean.

    This is the upper bound on the trace of a convex matrix geometric mean,
    represented by :class:`~picos.expressions.TrMatrixGeometricMean`.
    """

    def __init__(self, divergence, upperBound):
        """Construct a :class:`MatrixGeoMeanEpiConstraint`.

        :param ~picos.expressions.TrMatrixGeometricMean divergence:
            Constrained expression.
        :param ~picos.expressions.AffineExpression upperBound:
            Upper bound on the expression.
        """
        from ..expressions import AffineExpression, TrMatrixGeometricMean

        assert isinstance(divergence, TrMatrixGeometricMean)
        assert isinstance(upperBound, AffineExpression)
        assert len(upperBound) == 1
        assert (-1 <= divergence.power and divergence.power <= 0) or \
               ( 1 <= divergence.power and divergence.power <= 2)

        self.divergence = divergence
        self.upperBound = upperBound

        required_type = self._required_type()

        assert isinstance(divergence.X, required_type)
        assert isinstance(divergence.Y, required_type)

        super(TrMatrixGeoMeanEpiConstraint, self).__init__(divergence._typeStr)

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
    def power(self):
        """The power :math:`p`."""
        return self.divergence.power

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


class ComplexTrMatrixGeoMeanEpiConstraint(TrMatrixGeoMeanEpiConstraint):
    """Upper bound of trace of a complex convex matrix geometric mean."""

    # TODO: Implement real conversion of matrix geometric mean cone

    def _required_type(self):
        from ..expressions import ComplexAffineExpression

        return ComplexAffineExpression


class MatrixGeoMeanHypoConstraint(Constraint):
    """Hypograph of a concave matrix geometric mean.

    This is the lower bound, in the Loewner order, of a concave matrix geometric
    mean, represented by :class:`~picos.expressions.MatrixGeometricMean`.
    """

    def __init__(self, divergence, lowerBound):
        """Construct a :class:`MatrixGeoMeanEpiConstraint`.

        :param ~picos.expressions.MatrixGeometricMean divergence:
            Constrained expression.
        :param ~picos.expressions.AffineExpression lowerBound:
            Upper bound on the expression.
        """
        from ..expressions import MatrixGeometricMean

        required_type = self._required_type()

        assert isinstance(divergence, MatrixGeometricMean)
        assert isinstance(lowerBound, required_type)
        assert divergence.shape == lowerBound.shape
        assert 0 <= divergence.power and divergence.power <= 1

        self.divergence = divergence
        self.lowerBound = lowerBound

        assert isinstance(divergence.X, required_type)
        assert isinstance(divergence.Y, required_type)

        super(MatrixGeoMeanHypoConstraint, self).__init__(divergence._typeStr)

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
    def power(self):
        """The power :math:`p`."""
        return self.divergence.power

    Subtype = namedtuple("Subtype", ("argdim",))

    def _subtype(self):
        return self.Subtype(self.X.shape[0] ** 2)

    @classmethod
    def _cost(cls, subtype):
        n = subtype.argdim
        return n * (n + 1) // 2 * 3

    def _expression_names(self):
        yield "divergence"
        yield "lowerBound"

    def _str(self):
        return glyphs.psdge(self.divergence.string, self.lowerBound.string)

    def _get_size(self):
        n = self.X.shape[0]
        return (3 * n * n, 1)

    def _get_slack(self):
        return self.lowerBound.safe_value - self.divergence.safe_value


class ComplexMatrixGeoMeanHypoConstraint(MatrixGeoMeanHypoConstraint):
    """Hypograph of a complex concave matrix geometric mean."""

    # TODO: Implement real conversion of matrix geometric mean hypograph

    def _required_type(self):
        from ..expressions import ComplexAffineExpression

        return ComplexAffineExpression


class TrMatrixGeoMeanHypoConstraint(Constraint):
    """Lower bound of trace of a concave matrix geometric mean.

    This is the lower bound on the trace of a concave matrix geometric mean,
    represented by :class:`~picos.expressions.TrMatrixGeometricMean`.
    """

    def __init__(self, divergence, lowerBound):
        """Construct a :class:`MatrixGeoMeanEpiConstraint`.

        :param ~picos.expressions.TrMatrixGeometricMean divergence:
            Constrained expression.
        :param ~picos.expressions.AffineExpression lowerBound:
            Lower bound on the expression.
        """
        from ..expressions import AffineExpression, TrMatrixGeometricMean

        assert isinstance(divergence, TrMatrixGeometricMean)
        assert isinstance(lowerBound, AffineExpression)
        assert len(lowerBound) == 1
        assert 0 <= divergence.power and divergence.power <= 1

        self.divergence = divergence
        self.lowerBound = lowerBound

        required_type = self._required_type()

        assert isinstance(divergence.X, required_type)
        assert isinstance(divergence.Y, required_type)

        super(TrMatrixGeoMeanHypoConstraint, self).__init__(divergence._typeStr)

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
    def power(self):
        """The power :math:`p`."""
        return self.divergence.power

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


class ComplexTrMatrixGeoMeanHypoConstraint(TrMatrixGeoMeanHypoConstraint):
    """Lower bound of trace of a complex concave matrix geometric mean."""

    # TODO: Implement real conversion of matrix geometric mean cone

    def _required_type(self):
        from ..expressions import ComplexAffineExpression

        return ComplexAffineExpression


# --------------------------------------
__all__ = api_end(_API_START, globals())
