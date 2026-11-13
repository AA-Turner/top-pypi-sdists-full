"""RLOO's per-sample loss (`rloo_trainer.py:1851-1920`; spike S1): a clipped objective on each row's SUMMED
log-probs, `loss = mean over rows`, which transformers divides by GA after (`loss_is_scaled_for_ga = False`). The same
wraps as GRPO (RLOO generates, shuffles and splits the same way, so the row stamps hold); `kl` is a reward term
logged at generation, not a loss key."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import replace
from typing import Any

from probe.generated.samples import SampleSplit
from probe.generated.samples.points import ContributionSource, Dtype

from ..declarations import EVAL_KEY_PREFIX, EXTREME_KEYS, GRPO_TOKEN_KEYS, make_rollups
from ..hook import LossBatch, copy_rows_to_host, get_tensor_dtype
from .grpo import GrpoLoss

#: One 0/1 (or ratio) value per row: RLOO gathers them and takes nanmean / nanmin / nanmax (`:1907-1918`).
ROW_KEYS = ("clip_ratio/low_mean", "clip_ratio/high_mean", "clip_ratio/region_mean", "importance_ratio",
            *EXTREME_KEYS)  # fmt: skip


class RlooLoss(GrpoLoss):
    names = ("RLOOTrainer",)

    def find_unsupported(self) -> list[str]:
        return []

    def get_reasons(self) -> dict[str, str]:
        return {}

    def get_reduction(self) -> str:
        return "rloo"

    def get_rollups(self, dtype: Dtype, logging_window: int | None, dtypes: Mapping[str, Dtype] | None = None,
                    eval_prefixes: Sequence[str] = (EVAL_KEY_PREFIX,)) -> dict[str, dict]:  # fmt: skip
        return make_rollups([*GRPO_TOKEN_KEYS, *EXTREME_KEYS], dtype=dtype, dtypes=dtypes,
                            logging_window=logging_window, eval_prefixes=eval_prefixes)  # fmt: skip

    def _rebuild(self, inputs: Any, loss: Any, captured: Any, parts: dict, coefficient: float,
                 split: str) -> LossBatch:  # fmt: skip
        """RLOO's per-sequence loss on the detached logps, each row's contribution `loss_i / B / GA` (transformers'
        division after the call), the clip indicators per row, the entropy token-weighted."""
        import torch

        trainer = self.trainer
        logps, entropies, aux_loss = captured
        logps = logps.detach()
        mask = inputs["completion_mask"]
        full = mask.to(torch.float32)
        ratio = torch.exp((logps * mask).sum(1) - inputs["old_logps"])
        advantages = inputs["advantages"]
        clipped = torch.clamp(ratio, 1 - trainer.epsilon_low, 1 + trainer.epsilon_high)
        per_sequence = -torch.min(ratio * advantages, clipped * advantages)
        is_low = ((ratio < 1 - trainer.epsilon_low) & (advantages < 0)).float()
        is_high = ((ratio > 1 + trainer.epsilon_high) & (advantages > 0)).float()
        values = {"entropy": entropies, "clip_ratio/low_mean": is_low, "clip_ratio/high_mean": is_high,
                  "clip_ratio/region_mean": ((is_low + is_high) > 0).float(), "importance_ratio": ratio,
                  "loss": per_sequence}  # fmt: skip
        values = {name: value.unsqueeze(1).expand_as(full) if value.dim() == 1 else value
                  for name, value in values.items()}  # fmt: skip
        has_aux = getattr(trainer, "aux_loss_enabled", False) and aux_loss is not None
        host = copy_rows_to_host(values, mask, loss="loss", extras=[*self.stamps.get_columns(inputs), per_sequence],
                                 scalars=[loss, aux_loss if has_aux else None])  # fmt: skip
        reported, aux = host.scalars
        keys = self.stamps.take_keys([(extra[0], extra[1]) for extra in host.extras], split)
        accumulation = float(trainer.current_gradient_accumulation_steps) if split == SampleSplit.TRAIN else 1.0
        count = len(host.rows)
        scale = 1.0 / accumulation  # transformers divides RLOO's loss after it returns
        built = []
        for row, extra in zip(host.rows, host.extras, strict=True):
            metrics = dict(row.metrics)
            if "loss" in metrics:  # the row's own sequence loss, never a token mean of it
                metrics["loss"] = extra[2]
            for key, source in (("clip_ratio/low_min", "clip_ratio/low_mean"), ("clip_ratio/high_max",
                                                                               "clip_ratio/high_mean")):
                if source in metrics:
                    metrics[key] = metrics[source]
            built.append(replace(row, metrics=metrics, loss_sum=extra[2], normalizer=float(count), scale=scale,
                                 contribution=extra[2] / count * scale,
                                 contribution_source=ContributionSource.PROBE_REDUCER))  # fmt: skip
        terms = {"aux_loss": trainer.router_aux_loss_coef * aux * scale} if aux is not None else {}
        weights = {"loss": [1.0 / count] * count, **{key: [1.0] * count for key in ROW_KEYS}}
        return LossBatch(split=split, keys=keys, rows=built,
                         reported_loss=reported * scale if reported is not None else None, weights=weights,
                         batch_terms=terms, normalizer=float(count), scale=scale, dtype=get_tensor_dtype(logps),
                         dtypes={"entropy": get_tensor_dtype(entropies)})  # fmt: skip
