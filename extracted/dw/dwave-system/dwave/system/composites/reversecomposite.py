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
Composites that do batch operations for
:ref:`reverse annealing <qpu_qa_anneal_sched_reverse>` based on sets of
:ref:`initial states <parameter_qpu_initial_state>` or
:ref:`anneal schedules <parameter_qpu_anneal_schedule>`.
"""

import collections.abc as abc

import dimod
import numpy as np

__all__ = ['ReverseAdvanceComposite', 'ReverseBatchStatesComposite']


class ReverseAdvanceComposite(dimod.ComposedSampler):
    r"""Reverse anneals an initial sample through a sequence of anneal
    schedules.

    The first submission uses your provided initial sample, or, if unspecified,
    generates a random sample. Each subsequent submission selects as its initial
    state one of the following samples:

    *   The most-found lowest-energy sample (``reinitialize_state = True``, the
        default).
    *   The last returned sample, making each submission behave as a random
        walk (``reinitialize_state = False``).

    Args:
       sampler (:class:`dimod.Sampler`):
            A dimod sampler.

    .. versionadded:: 1.30.0
        Support for context manager protocol with :class:`dimod.Scoped`
        implemented.

    Examples:
       This example runs 100 reverse anneals each for three schedules on a problem
       constructed by setting random :math:`\pm 1` values on a clique (complete
       graph) of 15 nodes, minor-embedded on a D-Wave quantum computer using the
       :class:`~dwave.system.samplers.DWaveCliqueSampler` sampler.

       >>> import dimod
       >>> from dwave.system import DWaveCliqueSampler, ReverseAdvanceComposite
       ...
       >>> schedule = [[[0.0, 1.0], [t, 0.5], [20, 1.0]] for t in (5, 10, 15)]
       >>> bqm = dimod.generators.ran_r(1, 15)
       >>> init_samples = {i: -1 for i in range(15)}
       ...
       >>> with DWaveCliqueSampler() as sampler:    # doctest: +SKIP
       ...      sampler_reverse = ReverseAdvanceComposite(sampler)
       ...      sampleset = sampler_reverse.sample(
       ...          bqm,
       ...          anneal_schedules=schedule,
       ...          initial_state=init_samples,
       ...          num_reads=100,
       ...          reinitialize_state=True)

    """

    def __init__(self, child_sampler):
        self._children = [child_sampler]

    @property
    def children(self) -> list:
        """Child samplers that are used by this composite."""
        return self._children

    @property
    def parameters(self):
        """dict: Supported parameters.

        For an instantiated composed sampler, keys are the keyword parameters
        accepted by the child sampler and parameters added by the composite."""
        param = self.child.parameters.copy()
        param['schedules'] = []
        return param

    @property
    def properties(self) -> dict:
        """Properties of the child sampler."""
        return {'child_properties': self.child.properties.copy()}

    def sample(self, bqm, anneal_schedules=None, **parameters):
        r"""Sample the binary quadratic model using reverse annealing.

        For each specified
        :ref:`anneal schedule <parameter_qpu_anneal_schedule>`, creates a
        :ref:`reverse annealing <qpu_qa_anneal_sched_reverse>` submission.

        Args:
            bqm (:class:`~dimod.binary.BinaryQuadraticModel`):
                Binary quadratic model to be sampled from.

            anneal_schedules (list of lists, optional, default=[[[0, 1], [1, 0.35], [9, 0.35], [10, 1]]]):
                Anneal schedules in order of submission. Each schedule is
                formatted as a list of ``[time, s]`` pairs, in which ``time`` is
                in microseconds and ``s`` is the normalized anneal fraction in
                the range :math:`[0,1]`.

            initial_state (dict, optional):
                The state to reverse anneal from. If not provided, a state is
                randomly generated.

            **parameters:
                Parameters for the sampling method, specified by the child
                sampler.

        Returns:
            :class:`~dimod.SampleSet` that has ``initial_state`` and
            ``schedule_index`` fields.

        Examples:
           See examples for the :class:`.ReverseAdvanceComposite` class.


        """
        child = self.child

        if anneal_schedules is None:
            anneal_schedules = [[[0, 1], [1, 0.35], [9, 0.35], [10, 1]]]

        vartype_values = list(bqm.vartype.value)
        if 'initial_state' not in parameters:
            initial_state = dict(zip(list(bqm.variables), np.random.choice(vartype_values, len(bqm))))
        else:
            initial_state = parameters.pop('initial_state')

        if not isinstance(initial_state, abc.Mapping):
            raise TypeError("initial state provided must be a dict, but received {}".format(initial_state))

        if 'reinitialize_state' not in parameters:
            parameters['reinitialize_state'] = True

            if "answer_mode" in child.parameters:
                parameters['answer_mode'] = 'histogram'

        samplesets = None
        for schedule_idx, anneal_schedule in enumerate(anneal_schedules):
            sampleset = child.sample(bqm, anneal_schedule=anneal_schedule, initial_state=initial_state,
                                     **parameters)

            initial_state, _ = dimod.as_samples(initial_state)

            if 'initial_state' not in sampleset.record.dtype.names:
                init_state_vect = []

                if parameters['reinitialize_state']:
                    init_state_vect = [initial_state[0].copy() for i in range(len(sampleset.record.energy))]
                else:
                    # each sample is the next sample's initial state
                    init_state_vect.append(initial_state[0].copy())
                    for sample in sampleset.record.sample[:-1]:
                        init_state_vect.append(sample)

                sampleset = dimod.append_data_vectors(sampleset, initial_state=init_state_vect)

            if 'schedule_index' not in sampleset.record.dtype.names:
                schedule_index_vect = [schedule_idx] * len(sampleset.record.energy)
                sampleset = dimod.append_data_vectors(sampleset, schedule_index=schedule_index_vect)

            if samplesets is None:
                samplesets = sampleset
            else:
                samplesets = dimod.concatenate((samplesets, sampleset))

            if schedule_idx+1 == len(anneal_schedules):
                # no need to create the next initial state - last iteration
                break

            # prepare the initial state for the next iteration
            if parameters['reinitialize_state']:
                # if reinitialize is on, choose the lowest energy, most probable state for next iteration
                ground_state_energy = sampleset.first.energy
                lowest_energy_samples = sampleset.record[sampleset.record.energy == ground_state_energy]
                lowest_energy_samples.sort(order='num_occurrences')
                initial_state = dict(zip(sampleset.variables, lowest_energy_samples[-1].sample))
            else:
                # if not reinitialized, take the last state as the next initial state
                initial_state = dict(zip(sampleset.variables, sampleset.record.sample[-1]))

        samplesets.info['anneal_schedules'] = anneal_schedules
        return samplesets


class ReverseBatchStatesComposite(dimod.ComposedSampler, dimod.Initialized):
    r"""Reverse anneals from multiple initial samples.

    Submissions are independent from one another.

    Args:
       sampler (:class:`~dimod.Sampler`):
            A dimod sampler.

    .. versionadded:: 1.30.0
        Support for context manager protocol with :class:`dimod.Scoped`
        implemented.

    Examples:
       This example runs three reverse anneals from two configured and one
       randomly generated initial states on a problem constructed by setting
       random :math:`\pm 1` values on a clique (complete graph) of 15 nodes,
       minor-embedded on a D-Wave quantum computer using the
       :class:`~dwave.system.samplers.DWaveCliqueSampler` sampler.

       >>> import dimod
       >>> from dwave.system import DWaveCliqueSampler, ReverseBatchStatesComposite
       ...
       >>> schedule = [[0.0, 1.0], [10.0, 0.5], [20, 1.0]]
       >>> bqm = dimod.generators.ran_r(1, 15)
       >>> init_samples = [{i: -1 for i in range(15)}, {i: 1 for i in range(15)}]
       ...
       >>> with DWaveCliqueSampler() as sampler:     # doctest: +SKIP
       ...      sampler_reverse = ReverseBatchStatesComposite(sampler)
       ...      sampleset = sampler_reverse.sample(
       ...          bqm,
       ...          anneal_schedule=schedule,
       ...          initial_states=init_samples,
       ...          num_reads=3,
       ...          reinitialize_state=True)

    """

    def __init__(self, child_sampler):
        self._children = [child_sampler]

    @property
    def children(self) -> list:
        """Child samplers that are used by this composite."""
        return self._children

    @property
    def parameters(self):
        """dict: Supported parameters.

        For an instantiated composed sampler, keys are the keyword parameters
        accepted by the child sampler and parameters added by the composite."""
        param = self.child.parameters.copy()
        param['initial_states'] = []
        return param

    @property
    def properties(self) -> dict:
        """Properties of the child sampler."""
        return {'child_properties': self.child.properties.copy()}

    def sample(self, bqm, initial_states=None, initial_states_generator='random', num_reads=None,
               seed=None, **parameters):
        r"""Sample the binary quadratic model using reverse annealing from
        multiple initial states.

        Args:
            bqm (:class:`~dimod.binary.BinaryQuadraticModel`):
                Binary quadratic model to be sampled from.

            initial_states (samples-like, optional, default=None):
                One or more samples, each defining an initial state for all the
                problem variables. If fewer than ``num_reads`` initial states
                are defined, additional values are generated as specified by the
                ``initial_states_generator`` parameter. See
                :func:`dimod.as_samples` for a description of "samples-like".

            initial_states_generator ({'none', 'tile', 'random'}, optional, default='random'):
                Defines the expansion of ``initial_states`` if fewer than
                ``num_reads`` are specified:

                * "none":
                    Not supported when the number of initial states specified is
                    smaller than ``num_reads``.

                * "tile":
                    Reuses the specified initial states if fewer than
                    ``num_reads`` or truncates if greater.

                * "random":
                    Expands the specified initial states with randomly generated
                    states if fewer than ``num_reads`` or truncates if greater.

            num_reads (int, optional, default=len(initial_states) or 1):
                Number of required anneals. If greater than the number of
                provided initial states, additional states must be generated
                using the ``initial_states_generator`` parameter. If not
                specified, set to the length of ``initial_states`` if provided.
                If ``initial_states`` is not provided, defaults to 1.

            seed (int (32-bit unsigned integer), optional):
                Seed to use for the pseudorandom number generator (PRNG).
                Specifying a particular seed with a constant set of parameters
                produces identical submissions. If not specified, a random seed
                is chosen.

            **parameters:
                Parameters for the sampling method, specified by the child
                sampler.

        Returns:
            :class:`~dimod.SampleSet` that has an ``initial_state`` field.

        Raises:
            :exc:`ValueError`:
                If the number of initial states specified is smaller than
                ``num_reads`` and ``initial_states_generator`` is set to
                ``"none"``.

        Examples:
           See examples in the :class:`.ReverseBatchStatesComposite` class.

        """
        child = self.child

        parsed = self.parse_initial_states(bqm,
                                           initial_states=initial_states,
                                           initial_states_generator=initial_states_generator,
                                           num_reads=num_reads,
                                           seed=seed)

        parsed_initial_states = np.ascontiguousarray(parsed.initial_states.record.sample)

        # there is gonna be way too much data generated - better to histogram them if possible
        if 'answer_mode' in child.parameters:
            parameters['answer_mode'] = 'histogram'

        samplesets = None

        for initial_state in parsed_initial_states:
            sampleset = child.sample(bqm, initial_state=dict(zip(bqm.variables, initial_state)), **parameters)

            if 'initial_state' not in sampleset.record.dtype.names:
                init_state_vect = [initial_state.copy() for i in range(len(sampleset.record.energy))]
                sampleset = dimod.append_data_vectors(sampleset, initial_state=init_state_vect)

            if samplesets is None:
                samplesets = sampleset
            else:
                samplesets = dimod.concatenate((samplesets, sampleset))

        return samplesets
