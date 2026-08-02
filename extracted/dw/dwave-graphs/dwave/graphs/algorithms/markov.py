# Copyright 2019 D-Wave Systems Inc.
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

from collections.abc import Mapping, Sequence

import networkx as nx

import dimod
from dimod.typing import Variable, Bias

__all__ = ['sample_markov_network']


###############################################################################
# The following code is partially based on https://github.com/tbabej/gibbs
#
# MIT License
# ===========
#
# Copyright 2017 Tomas Babej
# https://github.com/tbabej/gibbs
#
# This software is released under MIT licence.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


def sample_markov_network(graph: nx.Graph,
                          sampler: dimod.Sampler,
                          fixed_variables: Mapping[Variable, Bias] | None = None,
                          return_sampleset: bool = False,
                          **sampler_args,
                          ) -> Sequence[Mapping[Variable, Bias]] | dimod.SampleSet:
    """Samples from a Markov network using the provided sampler.

    Args:
        graph:
            A Markov network as returned by
            :func:`~dwave.graphs.topologies.markov.markov_network`. Potentials
            data is stored in a node/edge attribute ``potential``.

        sampler:
            A dimod sampler.

        fixed_variables:
            A dictionary of variable assignments to be fixed in the Markov
            network.

        return_sampleset:
            If True, returns a :class:`~dimod.SampleSet` rather than a list of
            samples.

        **sampler_args:
            Additional keyword parameters are passed to the sampler.

    Returns:
        A list of samples ordered from low-to-high energy or a sample set.

    Examples:

    >>> import dimod
    ...
    >>> potentials = {('a', 'b'): {(0, 0): -1,
    ...                            (0, 1): .5,
    ...                            (1, 0): .5,
    ...                            (1, 1): 2}}
    >>> MN = dwave.graphs.markov_network(potentials)
    >>> sampler = dimod.ExactSolver()
    >>> samples = dwave.graphs.sample_markov_network(MN, sampler)
    >>> samples[0]     # doctest: +SKIP
    {'a': 0, 'b': 0}

    >>> import dimod
    ...
    >>> potentials = {('a', 'b'): {(0, 0): -1,
    ...                            (0, 1): .5,
    ...                            (1, 0): .5,
    ...                            (1, 1): 2}}
    >>> MN = dwave.graphs.markov_network(potentials)
    >>> sampler = dimod.ExactSolver()
    >>> samples = dwave.graphs.sample_markov_network(MN, sampler, return_sampleset=True)
    >>> samples.first       # doctest: +SKIP
    Sample(sample={'a': 0, 'b': 0}, energy=-1.0, num_occurrences=1)

    >>> import dimod
    ...
    >>> potentials = {('a', 'b'): {(0, 0): -1,
    ...                            (0, 1): .5,
    ...                            (1, 0): .5,
    ...                            (1, 1): 2},
    ...               ('b', 'c'): {(0, 0): -9,
    ...                            (0, 1): 1.2,
    ...                            (1, 0): 7.2,
    ...                            (1, 1): 5}}
    >>> MN = dwave.graphs.markov_network(potentials)
    >>> sampler = dimod.ExactSolver()
    >>> samples = dwave.graphs.sample_markov_network(MN, sampler, fixed_variables={'b': 0})
    >>> samples[0]           # doctest: +SKIP
    {'a': 0, 'c': 0, 'b': 0}

    """
    bqm = dimod.generators.markov_network(graph)

    if fixed_variables:
        # we can modify in-place since we just made it
        bqm.fix_variables(fixed_variables)

    sampleset = sampler.sample(bqm, **sampler_args)

    if fixed_variables:
        # add the variables back in
        sampleset = dimod.append_variables(sampleset, fixed_variables)

    if return_sampleset:
        return sampleset
    else:
        return list(map(dict, sampleset.samples()))
