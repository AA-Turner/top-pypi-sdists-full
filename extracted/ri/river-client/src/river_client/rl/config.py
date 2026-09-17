"""Explicit policies for rollout budgets, scheduling, and optimization."""

from __future__ import annotations

import math
import warnings
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Literal


def _integer(value, name, minimum=0):
    if type(value) is not int or (minimum is not None and value < minimum):
        bound = "" if minimum is None else f" >= {minimum}"
        raise ValueError(f"{name} must be an integer{bound}")


class RLConfigurationWarning(UserWarning):
    """An explicitly acknowledged configuration can waste rollout compute."""


def acknowledge_risk(allowed, flag, message):
    if type(allowed) is not bool:
        raise TypeError(f"{flag} must be a boolean")
    if not allowed:
        raise ValueError(f"{message} Set {flag}=True to explicitly allow it.")
    warnings.warn(message, RLConfigurationWarning, stacklevel=3)


@dataclass(frozen=True)
class KVCache:
    """Age relative to sampling weights, independent of training staleness.

    hold selects an existing snapshot within the bound; refill starts a new
    cache generation under current sampling weights when the bound is exceeded.
    """

    max_staleness: int = 0
    on_limit: Literal["hold", "refill"] = "hold"
    allow_reprefill: bool = False

    def __post_init__(self):
        _integer(self.max_staleness, "KV max_staleness")
        if self.max_staleness > 2**32 - 1:
            raise ValueError("KV max_staleness exceeds the wire limit")
        if self.on_limit not in {"hold", "refill"}:
            raise ValueError("KV on_limit must be hold or refill")
        if type(self.allow_reprefill) is not bool:
            raise TypeError("allow_reprefill must be a boolean")
        if self.on_limit == "refill":
            acknowledge_risk(
                self.allow_reprefill,
                "allow_reprefill",
                "Refreshing sampling weights beyond the KV age limit loses prefix reuse and requires a full prefill. "
                + (
                    "With KV max_staleness=0 this happens on every policy change."
                    if self.max_staleness == 0
                    else "Long trajectories may re-prefill repeatedly."
                ),
            )

    def validate_sampling_policy(self, sampling_policy):
        if sampling_policy == "trajectory" and (
            self.max_staleness != 0 or self.on_limit != "hold"
        ):
            raise ValueError(
                "trajectory pinning uses same-policy KV; select segment sampling for KV-age controls"
            )
        if (
            sampling_policy == "segment"
            and self.max_staleness == 0
            and self.on_limit == "hold"
        ):
            raise ValueError(
                "segment sampling needs a positive KV age limit, or explicit on_limit='refill' with allow_reprefill=True"
            )


@dataclass(frozen=True)
class ForwardBackwardBatch:
    """Submit when either useful-sequence or input-token threshold is reached.

    Complete reward groups stay together, so a chunk may overshoot. Tokens
    count full model inputs (including prompt context), not just loss tokens.
    The step boundary always flushes a smaller tail; no capacity is reserved.
    """

    min_sequences: int | None = 64
    min_tokens: int | None = 131_072

    def __post_init__(self):
        if self.min_sequences is None and self.min_tokens is None:
            raise ValueError(
                "ForwardBackwardBatch requires min_sequences or min_tokens"
            )
        for name in ("min_sequences", "min_tokens"):
            value = getattr(self, name)
            if value is not None:
                _integer(value, name, 1)

    def reached(self, sequences: int, tokens: int) -> bool:
        return (self.min_sequences is not None and sequences >= self.min_sequences) or (
            self.min_tokens is not None and tokens >= self.min_tokens
        )


@dataclass(frozen=True)
class Budget:
    max_turns: int = 8
    max_generated_tokens: int = 32768
    max_context_tokens: int = 131072
    segment_tokens: int = 4096
    final_answer_reserve: int = 0
    tool_output_tokens: int = 4096
    max_images: int | None = None
    max_turn_tokens: int | None = None

    def __post_init__(self):
        for key in (
            "max_turns",
            "max_generated_tokens",
            "max_context_tokens",
            "segment_tokens",
            "tool_output_tokens",
        ):
            _integer(getattr(self, key), key, 1)
        _integer(self.final_answer_reserve, "final_answer_reserve")
        if self.max_turn_tokens is not None:
            _integer(self.max_turn_tokens, "max_turn_tokens", 1)
        if self.max_images is not None:
            _integer(self.max_images, "max_images")
        if (
            not 0
            <= self.final_answer_reserve
            < min(self.max_generated_tokens, self.max_context_tokens)
        ):
            raise ValueError(
                "final_answer_reserve must fit inside generation and context budgets"
            )

    def next_segment(self, traj) -> int:
        remaining = min(
            self.max_generated_tokens - traj.generated_tokens,
            self.max_context_tokens - traj.context_tokens,
        )
        if (
            self.final_answer_reserve
            and not traj.wrap_up
            and remaining > self.final_answer_reserve
        ):
            remaining -= self.final_answer_reserve
        if self.max_turn_tokens is not None:
            remaining = min(remaining, self.max_turn_tokens - len(traj.pending_tokens))
        remaining = min(self.segment_tokens, remaining)
        # Quantize downward, never exceeding the budget. Segments that return
        # length are resumed; quantization does not shorten the trajectory.
        return max(0, remaining if remaining < 256 else remaining // 256 * 256)


@dataclass(frozen=True)
class Schedule:
    window: float = 0.01
    # Native sampling transport keeps per-prompt completions independent.
    max_batch: int = 128
    # Target expanded image/token bytes per submission; a larger single prompt
    # travels alone. This bounds envelopes without changing rollout admission.
    max_batch_bytes: int = 256 * 1024 * 1024
    concurrency: int = 256
    max_sample_requests: int | None = (
        None  # native: outstanding prompts; None uses concurrency
    )
    max_rpc_workers: int = 16  # submit, poll and decode; idle futures use no worker
    admit_ahead: int = 2
    priority: Literal["fifo", "predicted_length"] = "fifo"
    oversample_factor: float = 1.0

    def __post_init__(self):
        if self.window < 0 or not math.isfinite(self.window):
            raise ValueError("window must be finite and nonnegative")
        for name in ("max_batch", "max_batch_bytes", "concurrency", "max_rpc_workers"):
            _integer(getattr(self, name), name, 1)
        if self.max_sample_requests is not None:
            _integer(self.max_sample_requests, "max_sample_requests", 1)
        _integer(self.admit_ahead, "admit_ahead")
        if self.priority not in {"fifo", "predicted_length"}:
            raise ValueError("unknown scheduling priority")
        if not math.isfinite(self.oversample_factor) or self.oversample_factor < 1:
            raise ValueError("oversample_factor must be finite and >= 1")

    @property
    def sample_request_limit(self):
        return (
            self.concurrency
            if self.max_sample_requests is None
            else self.max_sample_requests
        )


@dataclass(frozen=True)
class GroupCompletion:
    mode: Literal["wait", "deadline"]
    min_members: int = 2
    max_straggler_tokens: int | None = None
    on_stragglers: Literal["truncate", "carry_over", "discard"] = "truncate"

    def __post_init__(self):
        if self.mode not in {"wait", "deadline"} or self.on_stragglers not in {
            "truncate",
            "carry_over",
            "discard",
        }:
            raise ValueError("unknown group completion policy")
        _integer(self.min_members, "min_members", 1)
        if self.max_straggler_tokens is not None and (
            type(self.max_straggler_tokens) is not int or self.max_straggler_tokens < 0
        ):
            raise ValueError("max_straggler_tokens must be a nonnegative integer")
        if self.mode == "deadline" and self.max_straggler_tokens is None:
            raise ValueError("deadline mode requires max_straggler_tokens")
        if self.mode == "wait" and self.max_straggler_tokens is not None:
            raise ValueError("max_straggler_tokens requires deadline mode")


@dataclass(frozen=True)
class Truncation:
    train: Literal[
        "zero_reward", "reward", "drop", "drop_and_exclude_from_baseline"
    ] = "zero_reward"
    by_cause: dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        if any(
            v not in {"zero_reward", "reward", "drop", "drop_and_exclude_from_baseline"}
            for v in (self.train, *self.by_cause.values())
        ):
            raise ValueError("unknown truncation policy")

    def policy(self, cause: str | None) -> str | None:
        return None if cause is None else self.by_cause.get(cause, self.train)


@dataclass(frozen=True)
class Cosine:
    warmup: int = 0
    floor: float = 0.0

    def __post_init__(self):
        _integer(self.warmup, "warmup")
        if not 0 <= self.floor <= 1:
            raise ValueError("invalid cosine schedule")

    def __call__(self, step: int, steps: int) -> float:
        if step < self.warmup:
            return (step + 1) / self.warmup
        progress = (step - self.warmup) / max(1, steps - self.warmup - 1)
        return (
            self.floor
            + (1 - self.floor) * (1 + math.cos(math.pi * min(1, progress))) / 2
        )


def cosine(*, warmup=0, floor=0.0):
    return Cosine(warmup, floor)


@dataclass(frozen=True)
class Adam:
    lr: float
    beta1: float = 0.9
    beta2: float = 0.95
    eps: float = 1e-8
    weight_decay: float = 0.0
    grad_clip_norm: float | None = None
    schedule: Callable[[int, int], float] | None = None

    def __post_init__(self):
        if (
            not math.isfinite(self.lr)
            or self.lr <= 0
            or not math.isfinite(self.eps)
            or self.eps <= 0
            or not math.isfinite(self.weight_decay)
            or self.weight_decay < 0
        ):
            raise ValueError("invalid Adam configuration")
        if not 0 <= self.beta1 < 1 or not 0 <= self.beta2 < 1:
            raise ValueError("Adam betas must be in [0, 1)")
        if self.grad_clip_norm is not None and (
            not math.isfinite(self.grad_clip_norm) or self.grad_clip_norm <= 0
        ):
            raise ValueError("grad_clip_norm must be finite and positive")

    def kwargs(self, step, steps):
        lr = self.lr * (1.0 if self.schedule is None else self.schedule(step, steps))
        if not math.isfinite(lr) or lr < 0:
            raise ValueError("learning-rate schedule returned an invalid rate")
        return {
            "lr": lr,
            "beta1": self.beta1,
            "beta2": self.beta2,
            "eps": self.eps,
            "weight_decay": self.weight_decay,
            "grad_clip_norm": self.grad_clip_norm,
        }
