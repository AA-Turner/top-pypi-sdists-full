"""Configured RL objectives and their rollout-data contract."""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass, field

import numpy as np

from river_client.losses import CustomLoss as TensorLoss

from .checkpoint import fingerprint
from .custom_loss import validate_custom_loss_inputs
from .requirements import LossRequirements, _validate_top_logprobs


def _positive(value, name, *, zero=False):
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or (value < 0 if zero else value <= 0)
    ):
        raise ValueError(
            f"{name} must be finite and {'nonnegative' if zero else 'positive'}"
        )


def _number_spellings(value):
    if type(value) is float and math.isfinite(value) and value.is_integer():
        return [value, int(value)]
    if type(value) is int and math.isfinite(value) and float(value) == value:
        return [value, float(value)]
    return [value]


@dataclass(frozen=True, kw_only=True)
class ScoreCentering:
    """Sampling-policy top-K correction with a residual-probability tail bucket."""

    top_k: int = 32

    def __post_init__(self):
        _validate_top_logprobs(self.top_k, name="top_k")


@dataclass(frozen=True, kw_only=True)
class _NativeLoss:
    normalize: str

    def __post_init__(self):
        if self.normalize not in {"token", "prompt", "sequence", "batch", "sum"}:
            raise ValueError("normalize must be token, prompt, sequence, batch, or sum")

    def _resolve(self):
        raise NotImplementedError


@dataclass(frozen=True, kw_only=True)
class CISPO(_NativeLoss):
    """Clipped importance-weighted policy gradient; eps_max caps p/q."""

    eps_max: float = 6.0
    score_centering: ScoreCentering | None = None

    def __post_init__(self):
        super().__post_init__()
        _positive(self.eps_max, "eps_max")
        if self.score_centering is not None and not isinstance(
            self.score_centering, ScoreCentering
        ):
            raise TypeError("score_centering must be ScoreCentering or None")

    def _resolve(self):
        binding = _LossBinding(
            "cispo", self.normalize, {"eps_max": float(self.eps_max)}
        )
        binding.set_score_centering(self.score_centering)
        return binding


@dataclass(frozen=True, kw_only=True)
class PolicyGradient(_NativeLoss):
    """Unit-weight policy-gradient surrogate, optionally score centered.

    Does not imply on-policy sampling: stale data still has policy mismatch.
    Score centering requires unfiltered sampling and retained top-K probabilities.
    """

    score_centering: ScoreCentering | None = None

    def __post_init__(self):
        super().__post_init__()
        if self.score_centering is not None and not isinstance(
            self.score_centering, ScoreCentering
        ):
            raise TypeError("score_centering must be ScoreCentering or None")

    def _resolve(self):
        binding = _LossBinding("cispo", self.normalize, {"use_perfect_ratio": 1.0})
        binding.set_score_centering(self.score_centering)
        return binding


@dataclass(frozen=True, kw_only=True)
class PPO(_NativeLoss):
    """PPO with lower/upper clipping offsets around an importance ratio of one."""

    clip_low: float = 0.2
    clip_high: float = 0.2

    def __post_init__(self):
        super().__post_init__()
        _positive(self.clip_low, "clip_low", zero=True)
        _positive(self.clip_high, "clip_high", zero=True)

    def _resolve(self):
        return _LossBinding(
            "ppo",
            self.normalize,
            {"clip_low": float(self.clip_low), "clip_high": float(self.clip_high)},
        )


@dataclass(frozen=True, kw_only=True)
class DecoupledPPO(PPO):
    """PPO with a proximal-policy forward pass and bounded behavior correction."""

    max_importance_weight: float = 5.0

    def __post_init__(self):
        super().__post_init__()
        _positive(self.max_importance_weight, "max_importance_weight")

    def _resolve(self):
        return _LossBinding(
            "decoupled_ppo",
            self.normalize,
            super()._resolve().config,
            max_importance_weight=self.max_importance_weight,
        )


@dataclass(frozen=True, kw_only=True)
class ImportanceSampling(_NativeLoss):
    """Policy-gradient surrogate weighted by the unclipped importance ratio."""

    def _resolve(self):
        return _LossBinding("importance_sampling", self.normalize, {})


@dataclass(frozen=True, kw_only=True)
class CustomLoss:
    """Bind a low-level river.CustomLoss to rollout inputs for AsyncTrainer.

    The wrapped loss retains its graph-defined reduction. An input adapter
    receives loss_data and requested sampling_metadata and returns the declared
    graph columns. Checkpointed adapters implement contract().
    """

    loss: TensorLoss
    input_adapter: Callable | None = field(default=None, repr=False)
    requirements: LossRequirements = field(default_factory=LossRequirements)
    train_zero_advantage_batches: bool = False

    def __post_init__(self):
        if not isinstance(self.loss, TensorLoss):
            raise TypeError("loss must be a river.CustomLoss")
        if self.input_adapter is not None and not callable(self.input_adapter):
            raise TypeError("input_adapter must be callable")
        if not isinstance(self.requirements, LossRequirements):
            raise TypeError("requirements must be LossRequirements")
        if type(self.train_zero_advantage_batches) is not bool:
            raise TypeError("train_zero_advantage_batches must be a boolean")

    def _resolve(self):
        return _LossBinding(
            self.loss,
            "sum",
            {},
            input_adapter=self.input_adapter,
            requirements=self.requirements,
            train_zero_advantage_batches=self.train_zero_advantage_batches,
        )


@dataclass
class _LossBinding:
    """Resolved objective configuration and its RL input binding.

    Custom graph registration happens later; the trainer replaces ``loss`` here
    with the registered graph without copying configuration into trainer fields.
    """

    loss: str | TensorLoss
    normalize: str
    config: dict
    input_adapter: object = None
    train_zero_advantage_batches: bool = False
    max_importance_weight: float = 5.0
    requirements: LossRequirements = LossRequirements()

    def set_score_centering(self, centering):
        if centering is not None:
            self.config["score_centering"] = 1.0
            self.requirements = LossRequirements(
                top_logprobs=centering.top_k, unfiltered_sampling=True
            )

    @property
    def is_custom(self):
        return isinstance(self.loss, TensorLoss)

    @property
    def requires_proximal_forward(self):
        return self.loss == "decoupled_ppo"

    @property
    def backward_loss(self):
        return "ppo" if self.requires_proximal_forward else self.loss

    def compatible_fingerprints(self, config):
        """An explicit default and an omitted wire default describe the same run."""
        defaults = (
            {
                "cispo": {"eps_max": 6.0},
                "ppo": {"clip_low": 0.2, "clip_high": 0.2},
                "decoupled_ppo": {"clip_low": 0.2, "clip_high": 0.2},
            }.get(self.loss, {})
            if isinstance(self.loss, str)
            else {}
        )
        candidates = [dict(config["loss_config"])]
        for key, default in defaults.items():
            if config["loss_config"].get(key, default) == default:
                variants = []
                for candidate in candidates:
                    omitted = {k: v for k, v in candidate.items() if k != key}
                    variants.extend([omitted, omitted | {key: default}])
                candidates = variants
        # JSON distinguishes 6 from 6.0 even though the wire uses doubles.
        # Preserve both spellings for explicit defaults and non-default options.
        if isinstance(self.loss, str):
            numeric_keys = set(defaults) | {
                "logprob_temperature",
                "use_perfect_ratio",
                "score_centering",
            }
            for key in sorted(numeric_keys):
                variants = []
                for candidate in candidates:
                    if key not in candidate:
                        variants.append(candidate)
                    else:
                        variants.extend(
                            candidate | {key: value}
                            for value in _number_spellings(candidate[key])
                        )
                candidates = variants
        caps = (
            _number_spellings(config["max_importance_weight"])
            if isinstance(self.loss, str)
            else [config["max_importance_weight"]]
        )
        return {
            fingerprint(
                config | {"loss_config": candidate, "max_importance_weight": cap}
            )
            for candidate in candidates
            for cap in caps
        }

    def bind(self, engine, *, checkpointing=False):
        if self.normalize not in {"token", "prompt", "sequence", "batch", "sum"}:
            raise ValueError(
                "normalize must be explicitly token, prompt, sequence, batch, or sum"
            )
        if type(self.train_zero_advantage_batches) is not bool:
            raise TypeError("train_zero_advantage_batches must be a boolean")
        if self.train_zero_advantage_batches and not self.is_custom:
            raise ValueError("train_zero_advantage_batches requires CustomLoss")
        if self.is_custom:
            if self.normalize != "sum":
                raise ValueError(
                    "CustomLoss requires normalize='sum'; reduce in the objective"
                )
            if self.config:
                raise ValueError("custom loss constants belong in the objective")
            validate_custom_loss_inputs(self.loss, self.input_adapter)
            if checkpointing and self.input_adapter is not None:
                if not callable(getattr(self.input_adapter, "contract", None)):
                    raise ValueError(
                        "checkpointed custom_loss_inputs must implement contract()"
                    )
                fingerprint(self.input_adapter.contract())
        if (
            not math.isfinite(self.max_importance_weight)
            or self.max_importance_weight <= 0
        ):
            raise ValueError("max_importance_weight must be finite and positive")
        if any(not math.isfinite(v) or v < 0 for v in self.config.values()):
            raise ValueError("loss configuration values must be finite and nonnegative")
        if self.requirements.unfiltered_sampling and (
            engine.top_p != 1.0 or engine.top_k not in (-1, 0)
        ):
            raise ValueError(
                "this loss requires unfiltered sampling (top_p=1, top_k=-1 or 0)"
            )
        count = self.requirements.top_logprobs
        if count is not None:
            if engine._dispatcher is not None or engine._groups:
                raise ValueError(
                    "bind loss sampling requirements before starting rollouts"
                )
            if engine.top_logprobs is not None and engine.top_logprobs != count:
                raise ValueError(
                    "engine top_logprobs conflicts with the loss's required top-K width"
                )
            engine.top_logprobs = count
        if not self.is_custom:
            self.config.setdefault("logprob_temperature", engine.temperature)

    def encode_metadata(self, data):
        if self.is_custom:
            return data
        for datum in data:
            metadata = datum.pop("sampling_metadata", {})
            if self.requirements.top_logprobs is not None:
                for name in ("sampler_topk_ids", "sampler_topk_logprobs"):
                    if name not in metadata:
                        raise ValueError(
                            "score centering requires sampler top-K metadata"
                        )
                    datum[name] = metadata[name]
                # The native loss gathers every ID, including zero-weight rows.
                if np.any(datum["sampler_topk_ids"] < 0):
                    raise ValueError(
                        "score centering requires complete top-K rows without padding"
                    )
        return data


def resolve_loss(
    loss,
    *,
    normalize,
    options,
    input_adapter,
    train_zero_advantage_batches,
    max_importance_weight,
):
    """Resolve configured objects and the published string/callback interface."""
    for old, new in (
        ("backward_groups", "forward_backward_groups"),
        ("backward_batch", "forward_backward_batch"),
        ("max_pending_backward", "max_pending_forward_backward"),
    ):
        if old in options:
            raise TypeError(f"{old} was renamed to {new}")
    if isinstance(loss, (_NativeLoss, CustomLoss)):
        if (
            normalize is not None
            or options
            or input_adapter is not None
            or train_zero_advantage_batches is not None
            or max_importance_weight is not None
        ):
            raise ValueError(
                "configured losses own normalization and loss options; do not also pass legacy trainer loss options"
            )
        return loss._resolve()
    if isinstance(loss, TensorLoss):
        if options:
            raise ValueError("custom loss constants belong in the objective")
        if normalize not in (None, "sum"):
            raise ValueError(
                "CustomLoss requires normalize='sum'; reduce in the objective"
            )
        return _LossBinding(
            loss,
            "sum",
            {},
            input_adapter,
            False
            if train_zero_advantage_batches is None
            else train_zero_advantage_batches,
            5.0 if max_importance_weight is None else max_importance_weight,
        )
    allowed = {
        "cispo": {"eps_max"},
        "ppo": {"clip_low", "clip_high"},
        "decoupled_ppo": {"clip_low", "clip_high"},
        "importance_sampling": set(),
    }
    if not isinstance(loss, str) or loss not in allowed:
        raise ValueError("unsupported RL loss")
    if set(options) - allowed[loss]:
        raise ValueError(
            f"unsupported {loss} options: {sorted(set(options) - allowed[loss])}"
        )
    if input_adapter is not None:
        raise ValueError("custom_loss_inputs is only supported with CustomLoss")
    if train_zero_advantage_batches:
        raise ValueError("train_zero_advantage_batches requires CustomLoss")
    return _LossBinding(
        loss,
        normalize,
        dict(options),
        max_importance_weight=5.0
        if max_importance_weight is None
        else max_importance_weight,
    )
