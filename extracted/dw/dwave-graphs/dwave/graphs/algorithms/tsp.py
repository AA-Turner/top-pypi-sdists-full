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

from collections.abc import Hashable, Iterable, Sequence

import dimod
import networkx as nx

__all__ = ["traveling_salesperson",
           "traveling_salesman",
           "is_hamiltonian_path",
           ]


def traveling_salesperson(graph: nx.Graph,
                          sampler: dimod.Sampler,
                          lagrange: float | None = None,
                          weight: str = 'weight',
                          start: Hashable | None = None,
                          **sampler_args,
                          ) -> Sequence[Hashable]:
    """Returns an approximate minimum traveling salesperson route.

    Defines a binary quadratic model (:term:`BQM`) with ground states corresponding to
    the minimum routes and uses the sampler to sample from it.

    A route is a cycle in the graph that reaches each node exactly once.
    A minimum route is a route with the smallest total edge weight.

    Args:
        graph:
            The graph on which to find a minimum traveling salesperson route.
            This should be a complete graph with non-zero weights on every edge.

        sampler:
            A dimod sampler.

        lagrange:
            Lagrange parameter to weight constraints (visit every city once)
            versus objective (shortest distance route). If not specified, it's
            estimated based on graph size.
            See :meth:`~dimod.generators.tsp.traveling_salesperson` BQM generator.

        weight:
            The name of the edge attribute containing the weight.

        start:
            If provided, the route will begin at ``start``.

        **sampler_args:
            Additional keyword parameters passed to the sampler.

    Returns:
       List of nodes in order to be visited on a route.

    Example:
        >>> import dimod
        >>> import dwave.graphs
        >>> import networkx
        ...
        >>> G = networkx.Graph()
        >>> G.add_weighted_edges_from({(0, 1, .1), (0, 2, .5), (0, 3, .1),
        ...                            (1, 2, .1), (1, 3, .5), (2, 3, .1)})
        >>> dwave.graphs.traveling_salesperson(G, dimod.ExactSolver(), start=0) # doctest: +SKIP
        [0, 1, 2, 3]

    """
    # Get a QUBO representation of the problem
    bqm = dimod.generators.traveling_salesperson(graph, lagrange=lagrange, weight=weight)

    # use the sampler to find low energy states
    response = sampler.sample(bqm, **sampler_args)

    sample = response.first.sample

    route = [None] * len(graph)
    for (city, time), val in sample.items():
        if val:
            route[time] = city

    if start is not None and route[0] != start:
        # rotate to put the start in front
        idx = route.index(start)
        route = route[idx:] + route[:idx]

    return route


traveling_salesman = traveling_salesperson


def is_hamiltonian_path(graph: nx.Graph, route: Iterable[Hashable]) -> bool:
    """Determines whether the given list forms a valid TSP route.

    A traveling salesperson route must visit each city exactly once.

    Args:
        graph:
            The graph on which to check the route.

        route:
            List of nodes in the order that they are visited.

    Returns:
        True if route forms a valid traveling salesperson route.
    """

    return set(route) == set(graph)
