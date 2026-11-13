"""Per-token arrays of one sample: whether to keep them (`PROBE_SAMPLES_PER_TOKEN`) and the per-sample
summaries the SDK computes from them (RL plan §3.3c)."""

from __future__ import annotations

import hashlib
import math
import os
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

#: `on` (default), `off`, or `sample:<fraction>` (keep that share; error samples always kept).
PER_TOKEN_ENV = "PROBE_SAMPLES_PER_TOKEN"

#: The arrays a per-token record may carry, by name. Trainer-side arrays come from the trainer
#: producer and inference arrays from the rollout producer; the server merges them onto one sample.
TOKEN_ARRAYS = (
    "token_ids",
    "token_text",
    "inference_logprobs",
    "trainer_logprobs",
    "ref_logprobs",
    "entropy",
    "ref_entropy",
    "advantages",
    "returns",
    "loss_mask",
    "top_k_ids",
    "top_k_logprobs",
)


@dataclass(frozen=True)
class PerTokenPolicy:
    """What `PROBE_SAMPLES_PER_TOKEN` says: keep every sample's arrays, none, or a share."""

    fraction: float = 1.0

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> PerTokenPolicy:
        """Read the knob; an unreadable value keeps the default (on) and is not an error."""
        raw = ((env if env is not None else os.environ).get(PER_TOKEN_ENV) or "on").strip().lower()
        if raw in ("on", "1", "true", ""):
            return cls(1.0)
        if raw in ("off", "0", "false"):
            return cls(0.0)
        if raw.startswith("sample:"):
            try:
                share = float(raw.split(":", 1)[1])
            except ValueError:
                return cls(1.0)
            return cls(min(1.0, max(0.0, share)))
        return cls(1.0)

    def should_keep(self, sample_key: str, *, is_error: bool) -> bool:
        """Keep this sample's arrays? Error samples always; a share by a stable hash of the key,
        so a retry and every producer of the sample decide the same."""
        if is_error or self.fraction >= 1.0:
            return True
        if self.fraction <= 0.0:
            return False
        digest = hashlib.sha256(sample_key.encode("utf-8")).digest()
        return int.from_bytes(digest[:8], "big") / 2**64 < self.fraction


def _to_numbers(values: object) -> list[float]:
    if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
        return []
    found = []
    for value in values:
        try:
            number = float(value)
        except (TypeError, ValueError):
            continue
        if math.isfinite(number):
            found.append(number)
    return found


def _pick_masked(values: object, mask: list[float]) -> list[float]:
    """``values`` where the loss mask is on (all of them with no usable mask)."""
    numbers = _to_numbers(values)
    if not mask or len(mask) != len(numbers):
        return numbers
    return [value for value, keep in zip(numbers, mask) if keep]


def _compute_mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def _compute_std(values: list[float]) -> float | None:
    mean = _compute_mean(values)
    if mean is None:
        return None
    return math.sqrt(sum((value - mean) ** 2 for value in values) / len(values))


def summarize_tokens(arrays: Mapping[str, object]) -> dict[str, float]:
    """Per-sample summaries as sortable columns: entropy, logprob difference (inference vs
    trainer), importance ratio, advantage and return, over loss-masked tokens when a mask fits, and
    `masked_tokens` (the mask's ones) when a mask is given; a summary with no data is left out."""
    mask = _to_numbers(arrays.get("loss_mask"))
    entropy = _pick_masked(arrays.get("entropy"), mask)
    ref_entropy = _pick_masked(arrays.get("ref_entropy"), mask)
    inference = _pick_masked(arrays.get("inference_logprobs"), mask)
    trainer = _pick_masked(arrays.get("trainer_logprobs"), mask)
    advantages = _pick_masked(arrays.get("advantages"), mask)
    returns = _pick_masked(arrays.get("returns"), mask)
    differences = (
        [abs(t - i) for t, i in zip(trainer, inference)] if len(trainer) == len(inference) else []
    )
    ratios = (
        [math.exp(min(50.0, t - i)) for t, i in zip(trainer, inference)]
        if len(trainer) == len(inference)
        else []
    )
    summary = {
        "entropy_mean": _compute_mean(entropy),
        "entropy_max": max(entropy) if entropy else None,
        "ref_entropy_mean": _compute_mean(ref_entropy),
        "logprob_diff_abs_mean": _compute_mean(differences),
        "logprob_diff_abs_max": max(differences) if differences else None,
        "importance_ratio_mean": _compute_mean(ratios),
        "advantage_mean": _compute_mean(advantages),
        "advantage_std": _compute_std(advantages),
        "return_mean": _compute_mean(returns),
        # What the means above averaged over, so they combine token-weighted (`wmean:token_stats.<name>`).
        "masked_tokens": int(sum(1 for keep in mask if keep)) if mask else None,
    }
    return {name: value for name, value in summary.items() if value is not None}


def pick_token_arrays(arrays: Mapping[str, object]) -> dict[str, object]:
    """The known arrays of a per-token record, in a fixed order; unknown names are dropped."""
    return {name: arrays[name] for name in TOKEN_ARRAYS if arrays.get(name) is not None}
