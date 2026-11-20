# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
The inference layer of sequence-ai: components for serving a robot policy fast on one GPU, each usable on its own in
your code.

    serve          a policy server in one call: your model as a function (or a batch function), served to robots
                   elsewhere, with the batcher below and the network's server side on by default (sequence_ai.serve)
    optimize       your policy made faster, each speed-up turned on only once its outputs are checked on your own
                   observations; serve() runs it by default (sequence_ai.engine.optimize)
    cuda_graphs    a torch module your model calls many times per run, replayed from CUDA graphs captured from its
                   own eager kernels, and kept only when its output is the same, byte for byte
    batcher        the calls waiting for a model, batched into one call to it
    replicas       replicas of a model, each in its own process, running one call at a time; a dead one is replaced
    ranks          one model across several processes, as torchrun starts them: rank 0 serves, and every call of the
                   policy goes to every rank first (serve does it where the launcher's environment says so)
    slack          scheduling by the slack an action chunk leaves: how many robots a replica can serve, how long a
                   request may wait for a batch, and which requests are dispatched first
"""
# The function, in the place of the module of its name: sequence_ai.engine.optimize(policy, examples). The module
# stays importable by its path (sequence_ai.engine.optimize's Optimized: `from sequence_ai.engine.optimize import ...`).
# optimize.py imports nothing but the standard library until it runs, so this costs nothing.
from .optimize import optimize  # noqa: E402,F401
