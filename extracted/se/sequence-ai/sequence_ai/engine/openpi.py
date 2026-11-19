# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
An openpi policy's infer() for a list of observations, in one call to its model: the batch function serve() takes.

    from openpi.policies import policy_config
    import sequence_ai
    from sequence_ai.engine import openpi

    policy = policy_config.create_trained_policy(config, checkpoint_dir)
    sequence_ai.serve(openpi.batched(policy), batch=[1, 2, 4, 8], example=observation)

One observation per call needs no adapter: sequence_ai.serve(policy.infer).

In one sentence: batched(policy) is a function of a list of observations → each passes through the policy's input
transforms, as in infer() → they are stacked along a new first axis, where infer() adds an axis of one → the model
samples all their actions in one call, with a random key split from the policy's own, so each row draws its own noise
→ each row, with its state, passes through the output transforms → one output per observation, in order, the dict
infer() returns for it.

WHY: one forward pass over several observations costs far less than one per observation, because a GPU running one
observation is not using all of itself (engine.batcher has a measurement). serve(batch=...) gathers the observations
waiting into the sizes listed, and the JAX model compiles each listed size once, in serve()'s warm-up.

`policy_timing.infer_ms` in each output is the batch's model time, shared by its rows, measured until the actions are
read back - infer() measures the call alone, which with JAX returns before the actions are computed. A PyTorch model
has no batched path here: its observations run one by one, each through infer() itself.

Adapted from openpi's Policy.infer (src/openpi/policies/policy.py of Physical-Intelligence/openpi, Apache-2.0: see
THIRD_PARTY_NOTICES.md). It reads the attributes infer() reads, which openpi keeps private (_input_transform,
_sample_actions, _sample_kwargs, _rng, _output_transform), and raises TypeError for a policy without them. openpi is
imported when batched() is called: it is not one of sequence-ai's dependencies.
"""
from __future__ import annotations

import time
from typing import Any, Callable

__all__ = ["batched"]

_READS = ("_input_transform", "_output_transform", "_sample_actions", "_sample_kwargs", "_rng")


def batched(policy: Any) -> Callable[[list], list]:
    """The batch function for `policy`, an openpi Policy: a list of observations in, the list of the dicts its
    infer() returns for them out, in order (the module's docstring). For serve(..., batch=[...])."""
    if getattr(policy, "_is_pytorch_model", False):
        def one_by_one(observations: list) -> list:
            return [policy.infer(observation) for observation in observations]

        return one_by_one
    missing = [name for name in _READS if not hasattr(policy, name)]
    if missing:
        raise TypeError(f"batched() takes an openpi Policy (openpi.policies.policy.Policy), whose infer() it runs on a "
                        f"batch; this {type(policy).__name__} has no {', '.join(missing)}")
    import jax
    import jax.numpy as jnp
    import numpy as np
    from openpi.models import model as _model

    def infer_batch(observations: list) -> list:
        # a copy of each, as infer() makes: the transforms may change their input in place
        inputs = [policy._input_transform(jax.tree.map(lambda x: x, observation)) for observation in observations]
        batch = jax.tree.map(lambda *rows: jnp.stack([jnp.asarray(row) for row in rows]), *inputs)
        policy._rng, rng = jax.random.split(policy._rng)
        started = time.monotonic()
        actions = policy._sample_actions(rng, _model.Observation.from_dict(batch), **policy._sample_kwargs)
        stacked = jax.tree.map(np.asarray, {"state": batch["state"], "actions": actions})   # waits for the actions
        took_ms = (time.monotonic() - started) * 1000
        outputs = []
        for i in range(len(observations)):
            output = policy._output_transform(jax.tree.map(lambda x, i=i: x[i, ...], stacked))
            output["policy_timing"] = {"infer_ms": took_ms}
            outputs.append(output)
        return outputs

    return infer_batch
