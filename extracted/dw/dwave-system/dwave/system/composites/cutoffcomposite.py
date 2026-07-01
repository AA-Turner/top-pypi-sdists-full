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

"""
Prunes a binary quadratic model (:term:`BQM`) or binary polynomial submitted to
the child sampler by retaining only interactions with values commensurate with
the sampler's precision (i.e., removing any interactions below a cutoff value).
Isolated variables are then also removed.
"""
import operator

import numpy as np

import dimod

__all__ = 'CutOffComposite', 'PolyCutOffComposite'


class CutOffComposite(dimod.ComposedSampler):
    r"""Removes interactions below a specified cutoff value.

    Prunes the binary quadratic model (:term:`BQM`) submitted to the child
    sampler by retaining only interactions with values commensurate with the
    sampler's precision, as specified by the ``cutoff`` argument. Also removes
    variables isolated post- or pre-removal of these interactions from the BQM
    passed on to the child sampler, setting these variables to values that
    minimize the original BQM's energy for the returned samples.

    Args:
       sampler (:class:`dimod.Sampler`):
            A :ref:`index_dimod` sampler.

       cutoff (number):
            Lower bound for absolute value of interactions. Interactions with
            absolute values lower than ``cutoff`` are removed. Isolated
            variables are also not passed on to the child sampler.

       cutoff_vartype (:class:`dimod.Vartype`/str/set, default='SPIN'):
            Variable space to execute the removal in. Accepted input values:

            * :attr:`~dimod.Vartype.SPIN`, ``'SPIN'``, ``{-1, 1}``
            * :attr:`~dimod.Vartype.BINARY`, ``'BINARY'``, ``{0, 1}``

       comparison (function, optional):
            A comparison operator for comparing interaction values to the cutoff
            value. Defaults to :func:`operator.lt`.

    .. versionadded:: 1.30.0
        Support for context manager protocol with :class:`dimod.Scoped`
        implemented.

    Examples:
        This example removes one interaction, ``('a', 'c'): -0.7``, before
        :term:`minor-embedding` on a D-Wave quantum computer. Note that the
        lowest-energy sample for the embedded problem remains
        ``{'a': 1, 'b': -1, 'c': -1}``, and this solution is found. The sample
        is attributed the energy appropriate to the BQM without thresholding.

        >>> import dimod
        ...
        >>> bqm = dimod.BinaryQuadraticModel(
        ...     {'a': -1, 'b': 1, 'c': 1},
        ...     {('a', 'b'): 0.8, ('a', 'c'): 0.7, ('b', 'c'): -1},
        ...     0,
        ...     dimod.SPIN)
        >>> with DWaveSampler() as sampler:
        ...     sampleset = CutOffComposite(AutoEmbeddingComposite(
        ...         sampler), 0.75).sample(bqm, num_reads=1000)
        >>> print(sampleset.first.energy)
        -5.5

    """

    @dimod.decorators.vartype_argument('cutoff_vartype')
    def __init__(self, child_sampler, cutoff, cutoff_vartype=dimod.SPIN,
                 comparison=operator.lt):
        self._children = [child_sampler]
        self._cutoff = cutoff
        self._cutoff_vartype = cutoff_vartype
        self._comparison = comparison

    @property
    def children(self) -> list:
        """Child samplers that are used by this composite."""
        return self._children

    @property
    def parameters(self) -> dict:
        """Supported parameters.

        For an instantiated composed sampler, keys are the keyword parameters
        accepted by the child sampler and parameters added by the composite."""
        return self.child.parameters.copy()

    @property
    def properties(self) -> dict:
        """Properties of the child sampler."""
        return {'child_properties': self.child.properties.copy()}

    def sample(self, bqm, **parameters):
        """Cut off interactions and sample from the provided binary quadratic model.

        Prunes the binary quadratic model (:term:`BQM`) submitted to the child
        sampler by retaining only interactions with value commensurate with the
        sampler's precision as specified by the ``cutoff`` argument. Also removes
        variables isolated post- or pre-removal of these interactions from the
        BQM passed on to the child sampler, setting these variables to values
        that minimize the original BQM's energy for the returned samples.

        Args:
            bqm (:class:`~dimod.binary.BinaryQuadraticModel`):
                Binary quadratic model to be sampled from.

            **parameters:
                Parameters for the sampling method, specified by the child sampler.

        Returns:
            :class:`~dimod.SampleSet`

        Examples:
            See the example in the :class:`CutOffComposite` class.

        """
        child = self.child
        cutoff = self._cutoff
        cutoff_vartype = self._cutoff_vartype
        comp = self._comparison

        if cutoff_vartype is dimod.SPIN:
            original = bqm.spin
        else:
            original = bqm.binary

        # remove all of the interactions less than cutoff
        new = type(bqm)(original.linear,
                        ((u, v, bias)
                         for (u, v), bias in original.quadratic.items()
                         if not comp(abs(bias), cutoff)),
                        original.offset,
                        original.vartype)

        # next we check for isolated qubits and remove them, we could do this as
        # part of the construction but the assumption is there should not be
        # a large number in the 'typical' case
        isolated = [v for v in new.variables if not new.adj[v]]
        new.remove_variables_from(isolated)

        if isolated and len(new) == 0:
            # in this case all variables are isolated, so we just put one back
            # to serve as the basis
            v = isolated.pop()
            new.linear[v] = original.linear[v]

        # get the samples from the child sampler and put them into the original vartype
        sampleset = child.sample(new, **parameters).change_vartype(bqm.vartype, inplace=True)

        # we now need to add the isolated back in, in a way that minimizes
        # the energy. There are lots of ways to do this but for now we'll just
        # do one
        if isolated:
            samples, variables = _restore_isolated(sampleset, bqm, isolated)
        else:
            samples = sampleset.record.sample
            variables = sampleset.variables

        vectors = sampleset.data_vectors
        vectors.pop('energy')  # we're going to recalculate the energy anyway

        return dimod.SampleSet.from_samples_bqm((samples, variables), bqm, **vectors)


def _restore_isolated(sampleset, bqm, isolated):
    """Return samples-like by adding isolated variables into sampleset in a
    way that minimizes the energy (relative to the other non-isolated variables).
    """

    samples = sampleset.record.sample
    variables = sampleset.variables

    new_samples = np.empty((len(sampleset), len(isolated)), dtype=samples.dtype)

    # we don't let the isolated variables interact with each other for now because
    # it will slow this down substantially
    for col, v in enumerate(isolated):
        try:
            neighbours, biases = zip(*((u, bias) for u, bias in bqm.adj[v].items()
                                       if u in variables))  # ignore other isolates
        except ValueError:
            # happens when only neighbors are other isolated variables
            new_samples[:, col] = bqm.linear[v] <= 0
            continue

        idxs = [variables.index(u) for u in neighbours]

        # figure out which value for v would minimize the energy
        # v(h_v + \sum_u J_uv * u)
        new_samples[:, col] = samples[:, idxs].dot(biases) < -bqm.linear[v]

    if bqm.vartype is dimod.SPIN:
        new_samples = 2*new_samples - 1

    return np.concatenate((samples, new_samples), axis=1), list(variables) + isolated


class PolyCutOffComposite(dimod.ComposedPolySampler):
    """Removes polynomial interactions below a specified cutoff value.

    Prunes the binary polynomial submitted to the child sampler by retaining
    only interactions with values commensurate with the sampler's precision, as
    specified by the ``cutoff`` argument. Also removes variables isolated post-
    or pre-removal of these interactions from the polynomial passed on to the
    child sampler, setting these variables to values that minimize the
    original polynomial's energy for the returned samples.

    Args:
       sampler (:class:`dimod.PolySampler`):
            A :ref:`index_dimod` binary polynomial sampler.

       cutoff (number):
            Lower bound for absolute value of interactions. Interactions
            with absolute values lower than ``cutoff`` are removed. Isolated variables
            are also not passed on to the child sampler.

       cutoff_vartype (:class:`dimod.Vartype`/str/set, default='SPIN'):
            Variable space to do the cutoff in. Accepted input values:

            * :attr:`~dimod.Vartype.SPIN`, ``'SPIN'``, ``{-1, 1}``
            * :attr:`~dimod.Vartype.BINARY`, ``'BINARY'``, ``{0, 1}``

       comparison (function, optional):
            A comparison operator for comparing the interaction value to the cutoff
            value. Defaults to :func:`operator.lt`.

    .. versionadded:: 1.30.0
        Support for context manager protocol with :class:`dimod.Scoped`
        implemented.

    Examples:
        This example removes one interaction, ``('a', 'c'): 0.2``, before
        submitting the polynomial to the child sampler
        :class:`~dimod.reference.samplers.ExactSolver`.

        >>> import dimod
        ...
        >>> poly = dimod.BinaryPolynomial(
        ...     {'a': 3, ('a', 'b', 'c'):-4, ('a', 'c'): 0.2}, dimod.SPIN)
        >>> with dimod.HigherOrderComposite(dimod.ExactSolver()) as sampler:
        ...     sampleset = PolyCutOffComposite(sampler, 1).sample_poly(poly)
        >>> print(sampleset.first.sample['a'])
        -1
    """
    @dimod.decorators.vartype_argument('cutoff_vartype')
    def __init__(self, child_sampler, cutoff, cutoff_vartype=dimod.SPIN,
                 comparison=operator.lt):
        if not isinstance(child_sampler, dimod.PolySampler):
            raise TypeError("Child sampler must be a PolySampler")
        self._children = [child_sampler]
        self._cutoff = cutoff
        self._cutoff_vartype = cutoff_vartype
        self._comparison = comparison

    @property
    def children(self) -> list:
        """Child samplers that are used by this composite."""
        return self._children

    @property
    def parameters(self) -> dict:
        """Supported parameters.

        For an instantiated composed sampler, keys are the keyword parameters
        accepted by the child sampler and parameters added by the composite."""
        return self.child.parameters.copy()

    @property
    def properties(self) -> dict:
        """Properties of the child sampler."""
        return {'child_properties': self.child.properties.copy()}

    def sample_poly(self, poly, **kwargs):
        """Cutoff and sample from the provided binary polynomial.

        Prunes the binary polynomial submitted to the child sampler by retaining
        only interactions with values commensurate with the sampler's precision,
        as specified by the ``cutoff`` argument. Also removes variables isolated
        post- or pre-removal of these interactions from the polynomial passed
        on to the child sampler, setting these variables to values that minimize
        the original polynomial's energy for the returned samples.

        Args:
            poly (:class:`~dimod.higherorder.polynomial.BinaryPolynomial`):
                Binary polynomial to be sampled from.

            **parameters:
                Parameters for the sampling method, supported by the child
                sampler.

        Returns:
            :class:`~dimod.SampleSet`

        Examples:
            See the example in the :class:`PolyCutOffComposite` class.

        """
        child = self.child
        cutoff = self._cutoff
        cutoff_vartype = self._cutoff_vartype
        comp = self._comparison

        if cutoff_vartype is dimod.SPIN:
            original = poly.to_spin(copy=False)
        else:
            original = poly.to_binary(copy=False)

        # remove all of the terms of order >= 2 that have a bias less than cutoff
        new = type(poly)(((term, bias) for term, bias in original.items()
                          if len(term) > 1 and not comp(abs(bias), cutoff)),
                         cutoff_vartype)

        # also include the linear biases for the variables in new
        for v in new.variables:
            term = v,
            if term in original:
                new[term] = original[term]

        # everything else is isolated
        isolated = list(original.variables.difference(new.variables))

        if isolated and len(new) == 0:
            # in this case all variables are isolated, so find the variable with
            # the strongest bias and use that as the seed for putting the other
            # variables back in
            v = max(isolated, key=lambda v: original.get((v,), 0.0))
            isolated.remove(v)
            new[(v,)] = original.get((v,), 0)

        # get the samples from the child sampler and put them into the original vartype
        sampleset = child.sample_poly(new, **kwargs).change_vartype(poly.vartype, inplace=True)

        # we now need to add the isolated back in, in a way that minimizes
        # the energy. There are lots of ways to do this but for now we'll just
        # do one
        if isolated:
            samples, variables = _restore_isolated_higherorder(sampleset, poly, isolated)
        else:
            samples = sampleset.record.sample
            variables = sampleset.variables

        vectors = sampleset.data_vectors
        vectors.pop('energy')  # we're going to recalculate the energy anyway

        return dimod.SampleSet.from_samples_bqm((samples, variables), poly, **vectors)


def _restore_isolated_higherorder(sampleset, poly, isolated):
    """Return samples-like by adding isolated variables into sampleset in a
    way that minimizes the energy (relative to the other non-isolated variables).

    Isolated should be ordered.
    """

    samples = sampleset.record.sample
    variables = sampleset.variables

    new_samples = np.empty((len(sampleset), len(isolated)), dtype=samples.dtype)

    # we don't let the isolated variables interact with eachother for now because
    # it will slow this down substantially
    isolated_energies = {v: 0. for v in isolated}
    for term, bias in poly.items():

        isolated_components = term.intersection(isolated)

        if not isolated_components:
            continue

        en = bias  # energy contribution of the term
        for v in term:
            if v in isolated_energies:
                continue
            en *= samples[:, sampleset.variables.index(v)]

        for v in isolated_components:
            isolated_energies[v] += en

    # now put those energies into new_samples
    for col, v in enumerate(isolated):
        new_samples[:, col] = isolated_energies[v] < 0

    if poly.vartype is dimod.SPIN:
        new_samples = 2*new_samples - 1

    return np.concatenate((samples, new_samples), axis=1), list(variables) + isolated
