"""Sampling metadata requested by RL objectives."""

from dataclasses import dataclass


def _validate_top_logprobs(value: int, *, name: str = "top_logprobs") -> None:
    """Validate the number of returned sampling alternatives, not sampling top_k."""
    if type(value) is not int or not 1 <= value <= 32:
        raise ValueError(f"{name} must be an integer in [1, 32]")


@dataclass(frozen=True, kw_only=True)
class LossRequirements:
    """Additional rollout data required by an RL objective.

    ``top_logprobs`` requests K alternatives per sampled token, independently
    of sampling top_k. ``policy_age`` exposes optimizer-step ages at training
    time. ``unfiltered_sampling`` requires top_p=1 and top_k=-1 or 0; it never changes
    the user's sampling distribution.
    """

    top_logprobs: int | None = None
    policy_age: bool = False
    unfiltered_sampling: bool = False

    def __post_init__(self):
        if self.top_logprobs is not None:
            _validate_top_logprobs(self.top_logprobs)
        if (
            type(self.policy_age) is not bool
            or type(self.unfiltered_sampling) is not bool
        ):
            raise TypeError("policy_age and unfiltered_sampling must be booleans")
