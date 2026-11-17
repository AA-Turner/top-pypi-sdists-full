# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
The inference layer of sequence-ai: components for serving a robot policy fast on one GPU, each usable on its own in
your code.

    cuda_graphs    a torch module your model calls many times per run, replayed from CUDA graphs captured from its
                   own eager kernels, and kept only when its output is the same, byte for byte
    batcher        the calls waiting for a model, batched into one call to it
    replicas       replicas of a model, each in its own process, running one call at a time; a dead one is replaced
    slack          scheduling by the slack an action chunk leaves: how many robots a replica can serve, how long a
                   request may wait for a batch, and which requests are dispatched first
"""
