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

from collections.abc import Hashable

import dimod
from dimod.decorators import graph_argument
from dimod.typing import GraphLike

__all__ = ['maximal_matching',
           'min_maximal_matching',
           ]


@graph_argument('graph')
def maximal_matching(graph: GraphLike,
                     sampler: dimod.Sampler,
                     **sampler_args,
                     ) -> set[Hashable]:
    """Finds an approximate maximal matching.

    Defines a BQM with ground states corresponding to a maximal matching and
    uses the sampler to sample from it.

    A `matching`_ is a subset of edges in which no node occurs more than once.
    A maximal matching is one in which no edges from ``graph`` can be added
    without violating the matching rule.

    Finding maximal matchings can be done is polynomial time, so this method
    is only useful pedagogically.

    Based on the formulation presented in [Luc2014]_.

    Args:
        graph:
            The graph on which to find a maximal matching. Either an integer
            ``n``, interpreted as a complete graph of size ``n``, a nodes/edges
            pair, a list of edges or a NetworkX graph.

        sampler:
            A dimod sampler.

        **sampler_args:
            Additional keyword parameters are passed to the sampler.

    Returns:
        A maximal matching of the graph.

    .. _matching: https://en.wikipedia.org/wiki/Matching_(graph_theory)

    """
    nodes, edges = graph

    if not edges:
        return set()

    bqm = dimod.generators.maximal_matching(graph)
    sampleset = sampler.sample(bqm, **sampler_args)
    sample = sampleset.first.sample

    # the matching are the edges that are 1 in the sample
    return set(tuple(edge) for edge, val in sample.items() if val > 0)


@graph_argument('graph')
def min_maximal_matching(graph: GraphLike,
                         sampler: dimod.Sampler,
                         **sampler_args,
                         ) -> set[Hashable]:
    """Returns an approximate minimum maximal matching.

    Defines a BQM with ground states corresponding to a minimum maximal matching
    and uses the sampler to sample from it.

    A `matching`_ is a subset of edges in which no node occurs more than once.
    A maximal matching is one in which no edges from ``graph`` can be added
    without violating the matching rule. A minimum maximal matching is the
    smallest maximal matching for ``graph``.

    Args:
        graph:
            The graph on which to find a minimum maximal matching. Either an
            integer ``n``, interpreted as a complete graph of size ``n``, a
            nodes/edges pair, a list of edges or a NetworkX graph.

        sampler:
            A dimod sampler.

        **sampler_args:
            Additional keyword parameters are passed to the sampler.

    Returns:
        A minimum maximal matching of the graph.

    Example:
        This example uses a sampler from
        :ref:`index_dimod` to find a minimum maximal
        matching for a Chimera unit cell.

        >>> import dimod
        >>> sampler = dimod.ExactSolver()
        >>> G = dwave.graphs.chimera_graph(1, 1, 4)
        >>> matching = dwave.graphs.min_maximal_matching(G, sampler)

    .. _matching: https://en.wikipedia.org/wiki/Matching_(graph_theory)

    """
    nodes, edges = graph

    if not edges:
        return set()

    bqm = dimod.generators.min_maximal_matching(graph)
    sampleset = sampler.sample(bqm, **sampler_args)
    sample = sampleset.first.sample

    # the matching are the edges that are 1 in the sample
    return set(tuple(edge) for edge, val in sample.items() if val > 0)
