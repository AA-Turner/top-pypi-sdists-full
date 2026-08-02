# Copyright 2021 D-Wave Systems Inc.
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

import math
from collections.abc import Hashable, Mapping

import dimod
from dimod.typing import GraphLike
from dimod.decorators import graph_argument

__all__ = ["partition",
           ]


@graph_argument('graph', as_networkx=True)
def partition(graph: GraphLike,
              sampler: dimod.Sampler,
              num_partitions: int = 2,
              **sampler_args,
              ) -> Mapping[Hashable, int]:
    """Return an approximate k-partition of ``graph``.

    Defines a :term:`CQM` with ground states corresponding to a balanced k-partition of
    ``graph`` and uses the sampler to sample from it.
    A k-partition is a collection of :math:`k` subsets of the vertices of ``graph`` such
    that each vertex is in exactly one subset, and the number of edges between
    vertices in different subsets is as small as possible. If ``graph`` is a
    weighted graph, the sum of weights over those edges are minimized.

    Args:
        graph:
            The graph to partition. Either an integer ``n``, interpreted as a
            complete graph of size ``n``, a nodes/edges pair, a list of edges or
            a NetworkX graph. When NetworkX graph is provided, optional edge
            weights can be provided in the ``weight`` attribute.

        sampler:
            A dimod sampler.

        num_partitions:
            The number of subsets in the desired partition.

        **sampler_args:
            Additional keyword parameters are passed to the sampler.

    Returns:
        The partition as a dictionary mapping each node to subsets labelled
        as integers 0, 1, 2, ... ``num_partitions``.

    Example:
        This example uses a dimod reference sampler
        :class:`~dimod.reference.samplers.ExactCQMSolver` to find a 2-partition
        for a graph of a Chimera unit cell created using the
        :meth:`~dwave.graphs.topologies.chimera.chimera_graph` function.

        >>> import dimod
        >>> import dwave.graphs
        ...
        >>> sampler = dimod.ExactCQMSolver()
        >>> G = dwave.graphs.chimera_graph(1, 1, 4)
        >>> partitions = dwave.graphs.partition(G, sampler=sampler)

    """
    if not len(graph.nodes):
        return {}

    cqm = dimod.generators.graph_partition(graph, num_partitions)

    # Solve the problem using the CQM solver
    response = sampler.sample_cqm(cqm, **sampler_args)

    # Consider only results satisfying all constraints
    possible_partitions = response.filter(lambda d: d.is_feasible)

    if not possible_partitions:
        raise RuntimeError("No feasible solution could be found for this problem instance.")

    # Reinterpret result as partition assignment over nodes
    indicators = (key for key, value in possible_partitions.first.sample.items()
                  if math.isclose(value, 1.))
    node_partition = {key[0]: key[1] for key in indicators}

    return node_partition
