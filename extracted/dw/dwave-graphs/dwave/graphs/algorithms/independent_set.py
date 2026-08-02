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

from dimod.generators.graph import (
    maximum_weight_independent_set as maximum_weight_independent_set_bqm)

__all__ = ["maximum_weighted_independent_set",
           "maximum_independent_set",
           "is_independent_set",
           ]


def maximum_weighted_independent_set(G, sampler, weight=None, lagrange=2.0, **sampler_args):
    """Returns an approximate maximum weighted independent set.

    Defines a binary quadratic model with ground states corresponding to a
    maximum weighted independent set (see
    :func:`dimod.generators.maximum_weight_independent_set`) and uses the
    sampler to sample from it.

    An independent set is a set of nodes such that the subgraph
    of G induced by these nodes contains no edges. A maximum
    independent set is an independent set of maximum total node weight.

    Parameters
    ----------
    G : NetworkX graph
        The graph on which to find a maximum cut weighted independent set.

    weight : string, optional (default None)
        If None, every node has equal weight. If a string, use this node
        attribute as the node weight. A node without this attribute is
        assumed to have max weight.

    sampler : :class:`dimod.Sampler`
        A dimod sampler.
        
    lagrange : optional (default 2)
        Lagrange parameter to weight constraints (no edges within set) 
        versus objective (largest set possible).

    sampler_args
        Additional keyword parameters are passed to the sampler.

    Returns
    -------
    indep_nodes : list
       List of nodes that form a maximum weighted independent set, as
       determined by the given sampler.

    Notes
    -----
    Samplers by their nature may not return the optimal solution. This
    function does not attempt to confirm the quality of the returned
    sample.

    References
    ----------

    `Independent Set on Wikipedia <https://en.wikipedia.org/wiki/Independent_set_(graph_theory)>`_

    `QUBO on Wikipedia <https://en.wikipedia.org/wiki/Quadratic_unconstrained_binary_optimization>`_

    Lucas, A. (2014). Ising formulations of many NP problems.
    Frontiers in Physics, Volume 2, Article 5.

    """
    # Get a BQM representation of the problem
    bqm = maximum_weight_independent_set_bqm(G.edges,
                                             G.nodes(data=weight, default=1),
                                             strength_multiplier=lagrange)

    # use the sampler to find low energy states
    response = sampler.sample(bqm, **sampler_args)

    # we want the lowest energy sample
    sample = next(iter(response))

    # nodes that are spin up or true are exactly the ones in S.
    return [node for node in sample if sample[node] > 0]


def maximum_independent_set(G, sampler, lagrange=2.0, **sampler_args):
    """Returns an approximate maximum independent set.

    Defines a QUBO with ground states corresponding to a
    maximum independent set and uses the sampler to sample from
    it.

    An independent set is a set of nodes such that the subgraph
    of G induced by these nodes contains no edges. A maximum
    independent set is an independent set of largest possible size.

    Parameters
    ----------
    G : NetworkX graph
        The graph on which to find a maximum cut independent set.

    sampler : :class:`dimod.Sampler`
        A dimod sampler.
        
    lagrange : optional (default 2)
        Lagrange parameter to weight constraints (no edges within set) 
        versus objective (largest set possible).

    sampler_args
        Additional keyword parameters are passed to the sampler.

    Returns
    -------
    indep_nodes : list
       List of nodes that form a maximum independent set, as
       determined by the given sampler.

    Example
    -------
    This example uses a sampler from
    `dimod <https://github.com/dwavesystems/dimod>`_ to find a maximum
    independent set for a graph of a Chimera unit cell created using the
    `chimera_graph()` function.

    >>> import dimod
    >>> sampler = dimod.SimulatedAnnealingSampler()
    >>> G = dwave.graphs.chimera_graph(1, 1, 4)
    >>> indep_nodes = dwave.graphs.maximum_independent_set(G, sampler)

    Notes
    -----
    Samplers by their nature may not return the optimal solution. This
    function does not attempt to confirm the quality of the returned
    sample.

    References
    ----------

    `Independent Set on Wikipedia <https://en.wikipedia.org/wiki/Independent_set_(graph_theory)>`_

    `QUBO on Wikipedia <https://en.wikipedia.org/wiki/Quadratic_unconstrained_binary_optimization>`_

    Lucas, A. (2014). Ising formulations of many NP problems.
    Frontiers in Physics, Volume 2, Article 5.

    """
    return maximum_weighted_independent_set(G, sampler, lagrange=lagrange, **sampler_args)


def is_independent_set(G, indep_nodes):
    """Determines whether the given nodes form an independent set.

    An independent set is a set of nodes such that the subgraph
    of G induced by these nodes contains no edges.

    Parameters
    ----------
    G : NetworkX graph
       The graph on which to check the independent set.

    indep_nodes : list
       List of nodes that form a maximum independent set, as
       determined by the given sampler.

    Returns
    -------
    is_independent : bool
        True if indep_nodes form an independent set.

    Example
    -------
    This example checks two sets of nodes, both derived from a
    single Chimera unit cell, for an independent set. The first set is
    the horizontal tile's nodes; the second has nodes from the horizontal and
    verical tiles.

    >>> from dwave.graphs import chimera_graph, is_independent_set
    >>> G = chimera_graph(1, 1, 4)
    >>> is_independent_set(G, [0, 1, 2, 3])
    True
    >>> is_independent_set(G, [0, 4])
    False

    """
    return len(G.subgraph(indep_nodes).edges) == 0
