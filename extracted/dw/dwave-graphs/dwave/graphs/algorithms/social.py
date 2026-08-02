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

from collections.abc import Hashable, Mapping
from typing import Literal

import dimod
import networkx as nx

__all__ = ["structural_imbalance",
           ]


def structural_imbalance(graph: nx.Graph,
                         sampler: dimod.Sampler,
                         **sampler_args,
                         ) -> tuple[Mapping[tuple[Hashable, Hashable], Mapping[str, float]], # frustrated edges
                                    Mapping[tuple[Hashable, Hashable], Literal[0, 1]]]:      # colors
    """Returns an approximate set of frustrated edges and a bicoloring.

    A signed social network graph is a graph whose signed edges represent
    friendly/hostile interactions between nodes. A signed social network is
    considered balanced if it can be cleanly divided into two factions, where
    all relations within a faction are friendly, and all relations between
    factions are hostile. The measure of imbalance or frustration is the minimum
    number of edges that violate this rule.

    Args:
        graph:
            A social graph (in a NetworkX graph) on which each edge has a 'sign'
            attribute with a numeric value.

        sampler:
            A dimod sampler.

        **sampler_args:
            Additional keyword parameters passed to the sampler.

    Returns:
        A tuple with two dictionaries:

        - frustrated_edges:
            A dictionary of the edges that violate the edge sign. The imbalance
            of the network is the length of frustrated_edges.

        - colors:
            A bicoloring of the nodes into two factions.

    Raises:
        ValueError: If any edge does not have a 'sign' attribute.

    Examples:
        >>> import dimod
        >>> sampler = dimod.ExactSolver()
        >>> S = nx.Graph()
        >>> S.add_edge('Alice', 'Bob', sign=1)   # Alice and Bob are friendly
        >>> S.add_edge('Alice', 'Eve', sign=-1)  # Alice and Eve are hostile
        >>> S.add_edge('Bob', 'Eve', sign=-1)    # Bob and Eve are hostile
        >>> frustrated_edges, colors = dwave.graphs.structural_imbalance(S, sampler)
        >>> print(frustrated_edges)
        {}
        >>> print(colors)  # doctest: +SKIP
        {'Alice': 0, 'Bob': 0, 'Eve': 1}
        >>> S.add_edge('Ted', 'Bob', sign=1)     # Ted is friendly with all
        >>> S.add_edge('Ted', 'Alice', sign=1)
        >>> S.add_edge('Ted', 'Eve', sign=1)
        >>> frustrated_edges, colors = dwave.graphs.structural_imbalance(S, sampler)
        >>> print(frustrated_edges)  # doctest: +SKIP
        {('Ted', 'Eve'): {'sign': 1}}
        >>> print(colors)  # doctest: +SKIP
        {'Bob': 1, 'Ted': 1, 'Alice': 1, 'Eve': 0}

    References:
        `Ising model on Wikipedia <https://en.wikipedia.org/wiki/Ising_model>`_

        Facchetti, G., Iacono G., and Altafini C. (2011).
        Computing global structural balance in large-scale signed social networks.
        PNAS, 108, no. 52, 20953-20958

    """
    bqm = dimod.generators.social.structural_imbalance(graph)

    # use the sampler to find low energy states
    response = sampler.sample(bqm, **sampler_args)

    # we want the lowest energy sample
    sample = next(iter(response))

    # spins determine the color
    colors = {v: (spin + 1) // 2 for v, spin in sample.items()}

    # frustrated edges are the ones that are violated
    frustrated_edges = {}
    for u, v, data in graph.edges(data=True):
        sign = data['sign']

        if sign > 0 and colors[u] != colors[v]:
            frustrated_edges[(u, v)] = data
        elif sign < 0 and colors[u] == colors[v]:
            frustrated_edges[(u, v)] = data
        # else: not frustrated or sign == 0, no relation to violate

    return frustrated_edges, colors
