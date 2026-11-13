"""GRPO's per-sample loss and diagnostics for every `loss_type` and mask at the pin (`huggingface/trl@4ae4d34a86f3`
`grpo_trainer.py:3152-3425`; spikes S0 and S1). TRL reduces inline in `_compute_loss`, so the hook keeps the live
per-token tensors of the one `_get_per_token_logps_and_entropies` call made inside it, and the batch-level pieces TRL
computes once (`get_high_entropy_mask`'s quantile across processes, `get_off_policy_mask`, `get_gamma_weights`) as
TRL's own calls returned them: never recomputed, so no collective. It rebuilds the per-token loss with TRL's formula
(`probe_reducer`); the shard check proves each rebuild against the loss `_compute_loss` returned."""

from __future__ import annotations

import functools
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, replace
from typing import Any

from probe.generated.samples import SampleSplit
from probe.generated.samples.points import ContributionSource, Dtype

from ..declarations import EVAL_KEY_PREFIX, EXTREME_KEYS, GRPO_TOKEN_KEYS, make_rollups
from ..hook import LossBatch, LossHook, copy_rows_to_host, get_tensor_dtype
from .generations import ROW, GenerationStamps

WHAT = "a per-sample loss"
#: TRL's own methods whose result the loss uses, captured inside the call by name (the mask or weight they return).
CAPTURED = {"entropy": "get_high_entropy_mask", "off_policy": "get_off_policy_mask", "phi": "get_gamma_weights"}


class GrpoLoss(LossHook):
    names = ("GRPOTrainer",)
    loss_method = "_compute_loss"

    def __init__(self, trainer: Any, recorder: Any) -> None:
        super().__init__(trainer, recorder)
        self.stamps = GenerationStamps(recorder)
        self._is_inside = False
        self._captured: Any = None
        #: What `CAPTURED`'s methods returned inside the call in flight.
        self._parts: dict[str, Any] = {}

    def find_unsupported(self) -> list[str]:
        return [] if self.trainer.loss_type in LOSS_RULES else [f"loss_type={self.trainer.loss_type}"]

    def get_reasons(self) -> dict[str, str]:
        return {f"loss_type={self.trainer.loss_type}": f"the loss hook rebuilds GRPO's {', '.join(LOSS_RULES)} losses "
                                                       "only; nothing per sample is sent"}  # fmt: skip

    def get_rollups(self, dtype: Dtype, logging_window: int | None, dtypes: Mapping[str, Dtype] | None = None,
                    eval_prefixes: Sequence[str] = (EVAL_KEY_PREFIX,)) -> dict[str, dict]:  # fmt: skip
        keys = ["entropy", *LOSS_RULES[self.trainer.loss_type].keys]
        if self.trainer.beta != 0.0:
            keys.append("kl")
        return make_rollups(keys, dtype=dtype, dtypes=dtypes, has_policy_loss=self._has_bonus(),
                            logging_window=logging_window, eval_prefixes=eval_prefixes)  # fmt: skip

    def install(self) -> None:
        trainer, guard = self.trainer, self.recorder.guard
        score = trainer._generate_and_score_completions
        get_logps = trainer._get_per_token_logps_and_entropies
        compute = trainer._compute_loss

        @functools.wraps(score)
        def call_score(*args: Any, **kwargs: Any) -> Any:
            output = score(*args, **kwargs)
            guard.call("a per-sample generation", self.stamps.stamp, output, self._get_split())
            return output

        @functools.wraps(get_logps)
        def call_get_logps(*args: Any, **kwargs: Any) -> Any:
            result = get_logps(*args, **kwargs)
            if self._is_inside:
                self._captured = result
            return result

        @functools.wraps(compute)
        def call_compute(model: Any, inputs: Any, *args: Any, **kwargs: Any) -> Any:
            split = guard.call(WHAT, self._get_split) or SampleSplit.TRAIN
            slot = guard.call(WHAT, self.recorder.open_call, split)  # counted before the call can fail
            coefficient = (guard.call(WHAT, self._get_entropy_coefficient) or 0.0) if slot is not None else 0.0
            self._is_inside, self._captured, self._parts = slot is not None, None, {}
            try:
                loss = compute(model, inputs, *args, **kwargs)
            finally:  # a raising loss never leaves its logps (and their graph) held here
                captured, parts = self._captured, self._parts
                self._is_inside, self._captured, self._parts = False, None, {}
            if slot is not None and captured is not None:
                guard.call(WHAT, self._record, slot, inputs, loss, captured, parts, coefficient, split)
            return loss

        self.recorder.install(trainer, "_generate_and_score_completions", call_score)
        self.recorder.install(trainer, "_get_per_token_logps_and_entropies", call_get_logps)
        self.recorder.install(trainer, "_compute_loss", call_compute)
        for name, method in CAPTURED.items():
            if callable(getattr(trainer, method, None)):
                self.recorder.install(trainer, method, self._wrap_part(name, getattr(trainer, method)))

    def _wrap_part(self, name: str, method: Any) -> Any:
        @functools.wraps(method)
        def call(*args: Any, **kwargs: Any) -> Any:
            result = method(*args, **kwargs)
            if self._is_inside:  # a result that is not a tensor fails into the guard, never into training
                self.recorder.guard.call(WHAT, self._keep_part, name, result)
            return result

        return call

    # -- inside -------------------------------------------------------------------------------------------------
    def _keep_part(self, name: str, result: Any) -> None:
        self._parts[name] = result.detach()

    def _get_split(self) -> str:
        return SampleSplit.TRAIN if self.trainer.model.training else SampleSplit.EVAL

    def _has_bonus(self) -> bool:
        return bool(getattr(self.trainer, "_entropy_bonus_enabled", False))

    def _get_entropy_coefficient(self) -> float:
        """The coefficient TRL applies in THIS call: the adaptive controller moves it inside the call (`:3330-3372`)."""
        trainer = self.trainer
        if not self._has_bonus():
            return 0.0
        if trainer.use_adaptive_entropy:
            return float(trainer.entropy_coef) if trainer._last_world_entropy <= trainer.args.entropy_target else 0.0
        return float(trainer.entropy_coef)

    def _record(self, slot: Any, inputs: Any, loss: Any, captured: Any, parts: dict, coefficient: float,
                split: str) -> None:  # fmt: skip
        if ROW not in inputs:
            return
        self.recorder.handle_loss(slot, self._rebuild(inputs, loss, captured, parts, coefficient, split))

    def _rebuild(self, inputs: Any, loss: Any, captured: Any, parts: dict, coefficient: float,
                 split: str) -> LossBatch:  # fmt: skip
        """TRL's per-token loss (`:3189-3284`) on the detached tensors, with the masks and weights its own call
        returned, then its reduction per loss type (`:3286-3317`) in float64, the entropy bonus's share per row over
        the effective (entropy-masked) tokens and the aux loss as a batch term. A (B, 1) sequence-level value counts
        each row once (`global_masked_mean`, `:3391`). Every number reaches the host in one copy."""
        import torch

        trainer, args, loss_type = self.trainer, self.trainer.args, self.trainer.loss_type
        logps, entropies, aux_loss = captured
        logps = logps.detach()
        mask = inputs["completion_mask"]
        mask = mask * inputs["tool_mask"] if "tool_mask" in inputs else mask
        advantages = inputs["advantages"]
        advantages = advantages.unsqueeze(1) if advantages.dim() == 1 else advantages
        old = inputs.get("old_per_token_logps")
        old = logps if old is None else old
        log_ratio = logps - old
        is_sequence = trainer.importance_sampling_level == "sequence"
        weights_log = ((log_ratio * mask).sum(-1) / mask.sum(-1).clamp(min=1.0)).unsqueeze(-1) if is_sequence \
            else log_ratio  # fmt: skip
        ratio = torch.exp(weights_log)
        kl = None
        if trainer.beta != 0.0:
            reference = inputs["ref_per_token_logps"]
            kl = torch.exp(reference - logps) - (reference - logps) - 1
            if args.use_bias_correction_kl:
                kl = kl * ratio
        rule = LOSS_RULES[loss_type]
        per_token, capped = rule.get_per_token(trainer, ratio, advantages, logps, parts)
        if trainer.off_policy_mask_threshold is not None:
            per_token = per_token * parts["off_policy"]
        entropy_mask = parts.get("entropy") if trainer.top_entropy_quantile < 1.0 else None
        if entropy_mask is not None:
            per_token = per_token * entropy_mask
        if trainer.use_vllm and trainer.vllm_importance_sampling_correction and rule.has_sampling_correction:
            per_token = per_token * inputs["importance_sampling_ratio"]
        if kl is not None:
            per_token = per_token + trainer.beta * kl
        full = mask.to(torch.float32)
        values: dict[str, Any] = {"loss": per_token.expand_as(full), "entropy": entropies}
        found = rule.get_diagnostics(trainer, ratio, capped, advantages, parts)
        row_weighted = [name for name, value in found.items() if value.shape[-1] == 1]  # (B, 1): each row once
        values.update({name: value.expand_as(full) for name, value in found.items()})
        if kl is not None:
            values["kl"] = kl.expand_as(full)
        values["importance_ratio"] = ratio.expand_as(full)
        effective = full if entropy_mask is None else full * entropy_mask
        extras = [*self.stamps.get_columns(inputs), (entropies.detach() * effective).sum(-1), effective.sum(-1)]
        has_aux = getattr(trainer, "aux_loss_enabled", False) and aux_loss is not None
        items = inputs.get("num_items_in_batch") if rule.is_item_normalized else None
        host = copy_rows_to_host(values, mask, loss="loss", extras=extras,
                                 scalars=[loss, aux_loss if has_aux else None, items])  # fmt: skip
        reported, aux, items_number = host.scalars
        keys = self.stamps.take_keys([(extra[0], extra[1]) for extra in host.extras], split)
        bonus = [(extra[2], extra[3]) for extra in host.extras]
        batch = self._reduce(host.rows, keys, reported, aux, items_number, coefficient, split, bonus, row_weighted)
        batch.dtype = get_tensor_dtype(logps, old, inputs.get("ref_per_token_logps") if kl is not None else None)
        batch.dtypes = {"entropy": get_tensor_dtype(entropies)}  # every other key is computed from the logps
        return batch

    def _reduce(self, rows: list, keys: list[str], reported: float | None, aux: float | None, items: float | None,
                coefficient: float, split: str, bonus: list[tuple[float, float]],
                row_weighted: list[str]) -> LossBatch:  # fmt: skip
        """Each row's share of its micro-batch's policy loss (the weight its value takes), its contribution to the
        returned loss, and the bonus and aux terms. ``bonus``: each row's entropy sum and count over the effective
        tokens; ``row_weighted``: (B, 1) keys, weighing each row once."""
        trainer = self.trainer
        accumulation = float(trainer.current_gradient_accumulation_steps) if split == SampleSplit.TRAIN else 1.0
        tokens = [float(row.token_count) for row in rows]
        normalizers, shares, normalizer, scale = LOSS_RULES[trainer.loss_type].reduce(trainer, tokens, accumulation,
                                                                                       split, items)  # fmt: skip
        effective = max(sum(count for _sum, count in bonus), 1.0)
        built = []
        for row, row_normalizer, (entropy_sum, _count) in zip(rows, normalizers, bonus, strict=True):
            contribution = (row.loss_sum or 0.0) / row_normalizer * scale
            if coefficient:  # its share of `- coef * H` over the effective tokens (`:3330-3346`)
                contribution -= coefficient * entropy_sum / effective / accumulation
            metrics = dict(row.metrics)
            for key, source in (("clip_ratio/low_min", "clip_ratio/low_mean"), ("clip_ratio/high_max",
                                                                               "clip_ratio/high_mean")):
                if source in metrics:
                    metrics[key] = metrics[source]
            if self._has_bonus() and "loss" in metrics:
                metrics["policy_loss"] = metrics["loss"]
            built.append(replace(row, metrics=metrics, normalizer=row_normalizer, scale=scale,
                                 contribution=contribution, contribution_source=ContributionSource.PROBE_REDUCER))
        terms = {"aux_loss": trainer.router_aux_loss_coef * aux / accumulation} if aux is not None else {}
        weights = {"loss": shares, "policy_loss": shares, **{key: [1.0] * len(rows) for key in row_weighted}}
        return LossBatch(split=split, keys=keys, rows=built, reported_loss=reported, weights=weights, batch_terms=terms,
                         normalizer=normalizer, scale=scale)  # fmt: skip


# -- TRL's reduction per loss type (`:3286-3317`) ------------------------------------------------------------------
#: (per-row normalizers, per-row shares of the micro-batch's policy loss before accumulation (a row's token-mean
#: value x its share sums to that loss), the one normalizer when every row shares it, the scale after it).
Reduction = tuple[list[float], list[float], "float | None", float]


def _reduce_grpo(trainer: Any, tokens: list[float], accumulation: float, split: str, items: float | None) -> Reduction:
    """grpo and sapo: the mean over rows of each row's token mean, / GA."""
    count = len(tokens)
    return [count * max(n, 1.0) for n in tokens], [1.0 / count] * count, None, 1.0 / accumulation


def _reduce_shared(normalizer: float, tokens: list[float], scale: float) -> Reduction:
    return [normalizer] * len(tokens), [n / normalizer for n in tokens], normalizer, scale


def _reduce_bnpo(trainer: Any, tokens: list[float], accumulation: float, split: str, items: float | None) -> Reduction:
    """The micro-batch's token mean, / GA."""
    return _reduce_shared(max(sum(tokens), 1.0), tokens, 1.0 / accumulation)


def _reduce_dr_grpo(trainer: Any, tokens: list[float], accumulation: float, split: str,
                    items: float | None) -> Reduction:  # fmt: skip
    """The token sum / (rows x `max_completion_length`), / GA."""
    return _reduce_shared(float(len(tokens) * trainer.max_completion_length), tokens, 1.0 / accumulation)


def _reduce_dapo(trainer: Any, tokens: list[float], accumulation: float, split: str, items: float | None) -> Reduction:
    """dapo, cispo and vespo: the token sum / (`num_items_in_batch`, the generation batch's tokens over every
    process, / processes x GA / `steps_per_generation` in train)."""
    normalizer = max(float(items if items is not None else 0.0), 1.0) / trainer.accelerator.num_processes
    if split == SampleSplit.TRAIN:
        normalizer = normalizer * accumulation / trainer.args.steps_per_generation
    return _reduce_shared(normalizer, tokens, 1.0)


def _reduce_luspo(trainer: Any, tokens: list[float], accumulation: float, split: str,
                  items: float | None) -> Reduction:  # fmt: skip
    """The mean over rows of each row's token SUM, / GA (`:3308-3316`)."""
    count = float(len(tokens))
    return [count] * len(tokens), [n / count for n in tokens], count, 1.0 / accumulation


# -- TRL's per-token loss and diagnostics per loss type (`:3233-3284`, `:3400-3425`) ---------------------------------
def _get_clipped(trainer: Any, ratio: Any, advantages: Any, logps: Any, parts: dict) -> tuple[Any, Any]:
    """Two-sided clipping; `delta` clamps the ratio before the clip indicators (`:3248`), the KL takes the raw one."""
    import torch

    low, high, delta = trainer.epsilon_low, trainer.epsilon_high, trainer.args.delta
    capped = ratio if delta is None else torch.clamp(ratio, max=delta)
    return -torch.min(capped * advantages, torch.clamp(ratio, 1 - low, 1 + high) * advantages), capped


def _get_cispo(trainer: Any, ratio: Any, advantages: Any, logps: Any, parts: dict) -> tuple[Any, Any]:
    import torch

    return -torch.clamp(ratio, max=trainer.epsilon_high) * advantages * logps, ratio


def _get_sapo(trainer: Any, ratio: Any, advantages: Any, logps: Any, parts: dict) -> tuple[Any, Any]:
    import torch

    args = trainer.args
    temperatures = torch.where(advantages > 0, args.sapo_temperature_pos, args.sapo_temperature_neg)
    return -(torch.sigmoid(temperatures * (ratio - 1)) * 4 / temperatures) * advantages, ratio


def _get_vespo(trainer: Any, ratio: Any, advantages: Any, logps: Any, parts: dict) -> tuple[Any, Any]:
    return -parts["phi"] * advantages * logps, ratio


def _get_clip_ratios(trainer: Any, ratio: Any, capped: Any, advantages: Any, parts: dict) -> dict[str, Any]:
    is_low = ((capped < 1 - trainer.epsilon_low) & (advantages < 0)).float()
    is_high = ((capped > 1 + trainer.epsilon_high) & (advantages > 0)).float()
    return {"clip_ratio/low_mean": is_low, "clip_ratio/high_mean": is_high,
            "clip_ratio/region_mean": ((is_low + is_high) > 0).float()}  # fmt: skip


def _get_cispo_ratio(trainer: Any, ratio: Any, capped: Any, advantages: Any, parts: dict) -> dict[str, Any]:
    return {"cispo_clip_ratio": ((ratio > trainer.epsilon_high) & (advantages > 0)).float()}


def _get_phi(trainer: Any, ratio: Any, capped: Any, advantages: Any, parts: dict) -> dict[str, Any]:
    return {"vespo/phi_seq_mean": parts["phi"]}


def _get_none(trainer: Any, ratio: Any, capped: Any, advantages: Any, parts: dict) -> dict[str, Any]:
    return {}


@dataclass(frozen=True)
class LossRule:
    """How TRL computes one `loss_type`: its per-token loss (and the ratio its clip indicators read), its reduction,
    the diagnostics it logs (a (B, 1) one weighs each row once), and what it reads."""

    get_per_token: Callable[..., tuple[Any, Any]]
    reduce: Callable[..., Reduction]
    get_diagnostics: Callable[..., dict[str, Any]]
    #: The series TRL logs beside `entropy` and `kl`.
    keys: tuple[str, ...] = ()
    #: Divides by `num_items_in_batch`.
    is_item_normalized: bool = False
    #: vLLM's importance-sampling correction multiplies its per-token loss (vespo folds it into phi).
    has_sampling_correction: bool = True


_CLIP_KEYS = (*GRPO_TOKEN_KEYS[1:], *EXTREME_KEYS)
#: Every loss type the hook rebuilds; any other is declared unsupported (`get_reasons` names these).
LOSS_RULES: dict[str, LossRule] = {
    "grpo": LossRule(_get_clipped, _reduce_grpo, _get_clip_ratios, _CLIP_KEYS),
    "bnpo": LossRule(_get_clipped, _reduce_bnpo, _get_clip_ratios, _CLIP_KEYS),
    "dr_grpo": LossRule(_get_clipped, _reduce_dr_grpo, _get_clip_ratios, _CLIP_KEYS),
    "dapo": LossRule(_get_clipped, _reduce_dapo, _get_clip_ratios, _CLIP_KEYS, is_item_normalized=True),
    "luspo": LossRule(_get_clipped, _reduce_luspo, _get_clip_ratios, _CLIP_KEYS),
    "sapo": LossRule(_get_sapo, _reduce_grpo, _get_none),
    "cispo": LossRule(_get_cispo, _reduce_dapo, _get_cispo_ratio, ("cispo_clip_ratio",), is_item_normalized=True),
    "vespo": LossRule(_get_vespo, _reduce_dapo, _get_phi, ("vespo/phi_seq_mean",), is_item_normalized=True,
                      has_sampling_correction=False),
}
