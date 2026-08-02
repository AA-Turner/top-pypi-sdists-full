# Copyright 2026 D-Wave
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

# Developer note: we could implement a function that creates the iter_*_to_* and
# iter_*_to_*_pairs methods just-in-time, but there are a small enough number
# that for now it makes sense to do them by hand.

__all__ = ["zephyr_coordinates"]


from collections.abc import Callable, Generator, Iterable, Sequence

import networkx as nx

from dwave.graphs.topologies.zephyr.graphs import zephyr_graph


class zephyr_coordinates:
    """Provides coordinate converters for the Zephyr indexing schemes.

    Args:
        m: Grid parameter for the Zephyr lattice.
        t: Tile parameter for the Zephyr lattice; must be even.

    See also :func:`~dwave.graphs.topologies.zephyr.graphs.zephyr_graph` for
    descriptions the various coordinate conventions.

    """
    def __init__(self, m: int, t: int = 4) -> None:
        self.args = m, 2 * m + 1, t

    def zephyr_to_linear(self, q: tuple[int, int, int, int, int]) -> int:
        """Converts a 5-term Zephyr coordinate into a linear index.

        Args:
            q: 5-term Zephyr coordinate.

        Returns:
            Linear index.

        Example:
            >>> dwave.graphs.zephyr_coordinates(2).zephyr_to_linear((0, 1, 2, 1, 0))
            26
        """
        u, w, k, j, z = q
        m, M, t = self.args
        return (((u * M + w) * t + k) * 2 + j) * m + z

    def linear_to_zephyr(self, r: int) -> tuple[int, int, int, int, int]:
        """Converts a linear index into a 5-term Zephyr coordinate.

        Args:
            r: Linear index.

        Returns:
            5-term Zephyr coordinate.

        Example:
            >>> dwave.graphs.zephyr_coordinates(2).linear_to_zephyr(137)
            (1, 3, 2, 0, 1)

        """
        m, M, t = self.args
        r, z = divmod(r, m)
        r, j = divmod(r, 2)
        r, k = divmod(r, t)
        u, w = divmod(r, M)
        return u, w, k, j, z

    def iter_zephyr_to_linear(
            self, qlist: Sequence[tuple[int, int, int, int, int]]
        ) -> Generator[int]:
        """Converts a sequence of 5-term Zephyr coordinates to linear indices.
        
        Args:
            qlist: Sequence of 5-term Zephyr coordinates.
            
        Yields:
            Linear index of each 5-term Zephyr coordinate.
        """
        m, M, t = self.args
        for (u, w, k, j, z) in qlist:
            yield (((u * M + w) * t + k) * 2 + j) * m + z

    def iter_linear_to_zephyr(
            self, rlist: Sequence[int]
        ) -> Generator[tuple[int, int, int, int, int]]:
        """Converts a sequence of linear indices to 5-term Zephyr coordinates.

        Args:
            rlist: Sequence of linear indices.
            
        Yields:
            5-term Zephyr coordinates of each linear index.
        """
        m, M, t = self.args
        for r in rlist:
            r, z = divmod(r, m)
            r, j = divmod(r, 2)
            r, k = divmod(r, t)
            u, w = divmod(r, M)
            yield u, w, k, j, z

    @staticmethod
    def _pair_repack(f: Callable, plist: Iterable[tuple]) -> Generator[tuple]:
        """Flattens a sequence of pairs to pass through f, and then re-pairs the result."""
        ulist = f(u for p in plist for u in p)
        for u in ulist:
            v = next(ulist)
            yield u, v

    def iter_zephyr_to_linear_pairs(self, plist: Iterable[tuple]) -> Generator[tuple]:
        """Converts pairs of 5-term Zephyr coordinates to pairs of linear indices."""
        return self._pair_repack(self.iter_zephyr_to_linear, plist)

    def iter_linear_to_zephyr_pairs(
        self,
        plist: Iterable[tuple],
    ) -> Generator[tuple]:
        """Converts pairs of linear indices to pairs of 5-term Zephyr coordinates."""
        return self._pair_repack(self.iter_linear_to_zephyr, plist)

    def graph_to_linear(self, g: nx.Graph) -> nx.Graph:
        """Returns a copy of the graph g relabeled to have linear indices.

        Args:
            g: The Zephyr graph to be relabeled.

        Returns:
            A Zephyr graph relabeled with linear indices.
        """
        labels = g.graph.get('labels')
        if labels == 'int':
            return g.copy()
        elif labels == 'coordinate':
            nodes = self.iter_zephyr_to_linear(g)
            edges = self.iter_zephyr_to_linear_pairs(g.edges)
        else:
            raise ValueError(
                f"Node labeling {labels} not recognized. "
                "Input must be generated by dwave.graphs.zephyr_graph."
            )

        return zephyr_graph(
            g.graph['rows'],
            t = g.graph['tile'],
            node_list=nodes,
            edge_list=edges,
            data=g.graph['data'],
        )

    def graph_to_zephyr(self, g: nx.Graph) -> nx.Graph:
        """Returns a copy of the graph g relabeled to have Zephyr coordinates.

        Args:
            g: The Zephyr graph to be relabeled.

        Returns:
            A Zephyr graph relabeled with Zephyr coordinates.
        """
        labels = g.graph.get('labels')
        if labels == 'int':
            nodes = self.iter_linear_to_zephyr(g)
            edges = self.iter_linear_to_zephyr_pairs(g.edges)
        elif labels == 'coordinate':
            return g.copy()
        else:
            raise ValueError(
                f"Node labeling {labels} not recognized. "
                "Input must be generated by dwave.graphs.zephyr_graph."
            )

        return zephyr_graph(
            g.graph['rows'],
            t=g.graph['tile'],
            node_list=nodes,
            edge_list=edges,
            data=g.graph['data'],
            coordinates=True,
        )


class __zephyr_coordinates_cache_dict(dict):
    """An internal-use cached factory for `zephyr_coordinates` objects."""

    def __missing__(self, key: tuple) -> zephyr_coordinates:
        self[key] = val = zephyr_coordinates(*key)
        return val


_zephyr_coordinates_cache = __zephyr_coordinates_cache_dict()