# Copyright 2018 D-Wave Systems Inc.
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

from collections.abc import Sequence, Hashable
from typing import Literal

import dimod
import networkx as nx

from dimod.decorators import graph_argument
from dimod.typing import GraphLike

__all__ = ["is_cycle",
           "is_vertex_coloring",
           "min_vertex_coloring",
           "vertex_coloring",
           "zephyr_four_color",
           "pegasus_four_color",
           "chimera_two_color",
           ]


@graph_argument('graph')
def vertex_coloring(graph: GraphLike,
                    colors: int | Sequence[Hashable],
                    sampler: dimod.Sampler,
                    **sampler_args,
                    ) -> dict[Hashable, Hashable]:
    """Returns an approximate vertex coloring.

    Vertex coloring is the problem of assigning a color to the vertices of a
    graph in a way that no adjacent vertices have the same color.

    Defines a binary quadratic model with ground states corresponding to valid
    vertex colorings and uses the sampler to sample from it.

    Args:
        graph:
            The graph on which to find a vertex coloring. Either an integer
            ``n``, interpreted as a complete graph of size ``n``, a nodes/edges
            pair, a list of edges or a NetworkX graph.

        colors:
            The colors. If an int, the colors are labelled ``[0, n)``. The
            number of colors must be greater or equal to the chromatic number of
            the graph.

        sampler:
            A dimod sampler.

        sampler_args:
            Additional keyword parameters are passed to the sampler.

    Returns:
        A coloring for each vertex in ``graph`` such that no adjacent nodes share
        the same color. A dict of the form ``{node: color, ...}``.

    """
    if not isinstance(colors, Sequence):
        # assume colors is Integral
        colors = range(int(colors))

    bqm = dimod.generators.vertex_coloring(graph, colors)

    # get the lowest energy sample
    sample = sampler.sample(bqm, **sampler_args).first.sample

    return {v: c for (v, c), val in sample.items() if val}


def min_vertex_coloring(graph: nx.Graph,
                        sampler: dimod.Sampler,
                        chromatic_lb: int | None = None,
                        chromatic_ub: int | None = None,
                        **sampler_args
                        ) -> dict[Hashable, Hashable]:
    """Returns an approximate minimum vertex coloring.

    Vertex coloring is the problem of assigning a color to the
    vertices of a graph in a way that no adjacent vertices have the
    same color. A minimum vertex coloring is the problem of solving
    the vertex coloring problem using the smallest number of colors.

    Defines a binary quadratic model with ground states corresponding to minimum
    vertex colorings and uses the sampler to sample from it.

    Args:
        graph:
            The graph on which to find a minimum vertex coloring.

        sampler:
            A dimod sampler.

        chromatic_lb:
            A lower bound on the chromatic number. If one is not provided, a
            bound is calculated.

        chromatic_ub:
            An upper bound on the chromatic number. If one is not provided, a
            bound is calculated.

        sampler_args:
            Additional keyword parameters are passed to the sampler.

    Returns:
        A coloring for each vertex in ``graph`` such that no adjacent nodes
        share the same color. A dict of the form ``{node: color, ...}``.

    """
    bqm = dimod.generators.min_vertex_coloring(
        graph, chromatic_lb=chromatic_lb, chromatic_ub=chromatic_ub)

    # get the lowest energy sample
    sample = sampler.sample(bqm, **sampler_args).first.sample

    return {v: c for (v, c), val in sample.items() if val}


def is_cycle(graph: nx.Graph) -> bool:
    """Determines whether the given graph is a cycle or circle graph.

    A cycle graph or circular graph is a graph that consists of a single cycle.

    https://en.wikipedia.org/wiki/Cycle_graph

    Args:
        graph: The graph to examine.

    Returns:
        True if the graph consists of a single cycle.

    """
    if len(graph) <= 2:
        return False

    trailing, leading = next(iter(graph.edges))
    start_node = trailing

    # travel around the graph, checking that each node has degree exactly two
    # also track how many nodes were visited
    n_visited = 1
    while leading != start_node:
        neighbors = graph[leading]

        if len(neighbors) != 2:
            return False

        node1, node2 = neighbors

        if node1 == trailing:
            trailing, leading = leading, node2
        else:
            trailing, leading = leading, node1

        n_visited += 1

    # if we haven't visited all of the nodes, then it is not a connected cycle
    return n_visited == len(graph)


def is_vertex_coloring(graph: nx.Graph, coloring: dict[Hashable, Hashable]) -> bool:
    """Determines whether the given coloring is a vertex coloring of graph G.

    Args:
        graph:
            The graph on which the vertex coloring is applied.

        coloring:
            A coloring of the nodes of ``graph``. Should be a dict of the form
            ``{node: color, ...}``.

    Returns:
        True if the given coloring defines a vertex coloring; that is, no
        two adjacent vertices share a color.

    Example:
        This example colors checks two colorings for a graph, ``graph``, of a
        single Chimera unit cell. The first uses one color (0) for the four
        horizontal qubits and another (1) for the four vertical qubits, in which
        case there are no adjacencies; the second coloring swaps the color of
        one node.

        >>> graph = dwave.graphs.chimera_graph(1,1,4)
        >>> colors = {0: 0, 1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 1, 7: 1}
        >>> dwave.graphs.is_vertex_coloring(graph, colors)
        True
        >>> colors[4]=0
        >>> dwave.graphs.is_vertex_coloring(graph, colors)
        False

   """
    return all(coloring[u] != coloring[v] for u, v in graph.edges)


def zephyr_four_color(q: tuple[int, int, int, int, int], scheme: Literal[0, 1] = 0) -> int:
    """Returns a node color sufficient for four coloring a Zephyr graph.

    Args:
        q:
            Qubit label in standard coordinate format: ``(u, w, k, j, z)``.

        scheme:
            Pattern selector. Two patterns not related by automorphism are
            supported.

    Returns:
        A color in ``{0, 1, 2, 3}``.

    Example:
        A mapping of every qubit in a Zephyr[m, t] graph to one of four colors.

        >>> m = 2
        >>> G = dwave.graphs.zephyr_graph(m, coordinates=True)
        >>> colors = {q: dwave.graphs.zephyr_four_color(q) for q in G.nodes()}
    """
    u, w, _, j, z = q
    
    if scheme == 0:
        return j + ((w + 2*(z+u) + j)&2)
    elif scheme == 1:
        return (2*u + w + 2*z + j) & 3
    else:
        raise ValueError('Unknown scheme')


def pegasus_four_color(q: tuple[int, int, int, int]) -> int:
    """Returns a node color sufficient for four coloring a Pegasus graph.

    Args:
        q:
            Qubit label in standard coordinate format: ``(u, w, k, z)``.

    Returns:
        A color in ``{0, 1, 2, 3}``.

    Example:
        A mapping of every qubit in a Pegasus[m] graph to one of four colors.

        >>> m = 2
        >>> G = dwave.graphs.pegasus_graph(m, coordinates=True)
        >>> colors = {q: dwave.graphs.pegasus_four_color(q) for q in G.nodes()}
    """
    u, w, k, z = q
    return 2 * u + ((k ^ z) & 1)


def chimera_two_color(q: tuple[int, int, int, int]) -> int:
    """Returns a node color sufficient for two coloring a Chimera graph.

    Args:
        q:
            Qubit label in standard coordinate format: ``(i, j, u, k)``.

    Returns:
        A color in ``{0, 1}``.

    Example:
        A mapping of every qubit in a Chimera graph to one of two colors.

        >>> m = 2
        >>> G = dwave.graphs.chimera_graph(m, coordinates=True)
        >>> colors = {q: dwave.graphs.chimera_two_color(q) for q in G.nodes()}
    """
    i, j, u, _ = q
    return (i ^ j ^ u) & 1
