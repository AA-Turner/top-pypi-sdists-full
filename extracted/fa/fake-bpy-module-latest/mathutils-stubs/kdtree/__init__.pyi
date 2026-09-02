"""
Generic 2D/3D KD-tree to perform spatial searches.

```../examples/mathutils.kdtree.0.py```

"""

import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import mathutils

class KDTree:
    """A KD-tree initialized to hold up to size items."""

    dimensions: int
    """ KDTree dimensions."""

    def balance(self) -> None:
        """Balance the tree."""

    def find(
        self,
        co: collections.abc.Sequence[float],
        *,
        filter: None | collections.abc.Callable[int, bool] | None = None,
    ) -> tuple[None, None, None] | tuple[mathutils.Vector, int, float]:
        """Find nearest point to co.

                :param co: Point position. Can be 2D or 3D, based on the KDTree dimensions.
                :param filter: function which takes an index and returns True for indices to include in the search.
                :return: Returns (position, index, distance),
        or (None, None, None) when no match is found.
        """

    def find_n(
        self, co: collections.abc.Sequence[float], n: int
    ) -> list[tuple[mathutils.Vector, int, float]]:
        """Find nearest n points to co.

        :param co: Point position. Can be 2D or 3D, based on the KDTree dimensions.
        :param n: Number of points to find.
        :return: Returns a list of tuples (position, index, distance).
        """

    def find_range(
        self, co: collections.abc.Sequence[float], radius: float
    ) -> list[tuple[mathutils.Vector, int, float]]:
        """Find all points within radius of co.

        :param co: Point position. Can be 2D or 3D, based on the KDTree dimensions.
        :param radius: Maximum distance to search for points.
        :return: Returns a list of tuples (position, index, distance).
        """

    def insert(self, co: collections.abc.Sequence[float], index: int) -> None:
        """Insert a point into the KDTree.

        :param co: Point position. Can be 2D or 3D, based on the KDTree dimensions.
        :param index: The index of the point (must be non-negative).
        """

    def __init__(self, size) -> None:
        """

        :param size:
        """
