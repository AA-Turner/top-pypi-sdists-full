"""AsyncGRPO's per-sample loss (`async_grpo_trainer.py:1451-1628`; spike S1). Each micro-batch is one tree-packed row
per rank (`packing.TreeRow.pack`), and `segment_id` names, for every trained token, the index of its sample in that
row's `TreeRow.samples`. A forward hook keeps the `fused_lm_head=True` output of the one forward inside `compute_loss`
(as SFT's); the `compute_loss` wrap rebuilds the per-token terms (score centering, TRL's default, from the same
output's `score_log_probs`, `:1496-1507`) and sums them per sample. Which sample a segment is rides the collated
batch: the main process collates every rank's row, so it stamps each sample's queue key there (`STAMP`), and the
dispatcher hands each rank its own row's."""

from __future__ import annotations

import functools
from collections.abc import Mapping, Sequence
from typing import Any

from probe.generated.samples import SampleSplit
from probe.generated.samples.points import ContributionSource, Dtype, Reducer, hash_mask
from probe.sdk.run.samples.points import RowSummary, copy_to_host

from ..declarations import make_rollups
from ..hook import LossBatch, LossHook, get_tensor_dtype

WHAT = "a per-sample loss"
#: Per rank row, per segment: the drained sample's (model version, group, index), its queue key's parts; -1 unknown.
STAMP = "_probe_points_samples"
MEAN_KEYS = ("entropy", "clip_ratio/low_mean", "clip_ratio/high_mean", "clip_ratio/region_mean",
             "sampling/importance_sampling_ratio/mean", "sampling/sampling_logp_difference/mean",
             "sampling/masked_mean", "sampling/sampler_mass")  # fmt: skip
#: AsyncGRPO's `_reduce_metric` (`:83`) takes a `min` / `max` key's window extreme, not its mean: each row sends its own
#: extreme, each call takes the min / max over every rank's rows, and so does the step.
EXTREMES = {"sampling/importance_sampling_ratio/min": Reducer.MIN, "sampling/importance_sampling_ratio/max": Reducer.MAX,
            "sampling/sampling_logp_difference/max": Reducer.MAX, "clip_ratio/low_min": Reducer.MIN,
            "clip_ratio/high_max": Reducer.MAX}  # fmt: skip


class AsyncGrpoLoss(LossHook):
    names = ("AsyncGRPOTrainer",)
    loss_method = "compute_loss"
    extremes = EXTREMES

    def __init__(self, trainer: Any, recorder: Any) -> None:
        super().__init__(trainer, recorder)
        self._is_inside = False
        self._captured: Any = None
        self._handle: Any = None

    def get_reduction(self) -> str:
        return "score_centering" if getattr(self.trainer.args, "score_centering", False) else "clipped"

    def get_rollups(self, dtype: Dtype, logging_window: int | None, dtypes: Mapping[str, Dtype] | None = None,
                    eval_prefixes: Sequence[str] = ()) -> dict[str, dict]:  # fmt: skip
        keys = [key for key in MEAN_KEYS if key != "sampling/sampler_mass" or self.get_reduction() == "score_centering"]
        return make_rollups([*keys, *EXTREMES], dtype=dtype, dtypes=dtypes, logging_window=logging_window,
                            eval_prefixes=(), extremes=EXTREMES, step_reducers=EXTREMES)  # fmt: skip

    def install(self) -> None:
        trainer, guard = self.trainer, self.recorder.guard
        compute = trainer.compute_loss
        get_loader = trainer.get_train_dataloader

        def handle_forward(_module: Any, _args: Any, kwargs: Any, output: Any) -> None:
            if self._is_inside and kwargs.get("fused_lm_head"):
                self._captured = output

        @functools.wraps(compute)
        def call_compute(model: Any, inputs: Any, *args: Any, **kwargs: Any) -> Any:
            slot = guard.call(WHAT, self.recorder.open_call, SampleSplit.TRAIN)
            self._is_inside, self._captured = slot is not None, None
            try:
                loss = compute(model, inputs, *args, **kwargs)
            finally:
                captured, self._is_inside, self._captured = self._captured, False, None
            if slot is not None and captured is not None and STAMP in inputs:
                guard.call(WHAT, self._record, slot, inputs, loss, captured)
            return loss

        @functools.wraps(get_loader)
        def call_get_loader(*args: Any, **kwargs: Any) -> Any:
            loader = get_loader(*args, **kwargs)
            guard.call("the rollout collator", self._watch_collator, loader)
            return loader

        self._handle = trainer.model.register_forward_hook(handle_forward, with_kwargs=True)
        self.recorder.install(trainer, "compute_loss", call_compute)
        self.recorder.install(trainer, "get_train_dataloader", call_get_loader)

    def close(self) -> None:
        if self._handle is not None:
            self._handle.remove()
            self._handle = None

    # -- the stamp (main process) --------------------------------------------------------------------------------
    def _watch_collator(self, loader: Any) -> None:
        """Outside the sample recorder's own collator wrap, which noted the batch's drained samples first."""
        collator = getattr(loader, "collate_fn", None)
        torch_call = getattr(collator, "torch_call", None)
        take = getattr(getattr(self.recorder.tracker, "recorder", None), "take_batch_places", None)
        if not callable(torch_call) or not callable(take):
            return

        @functools.wraps(torch_call)
        def call_torch_call(examples: Any, *args: Any, **kwargs: Any) -> Any:
            batch = torch_call(examples, *args, **kwargs)
            self.recorder.guard.call(WHAT, self._stamp, batch, examples, take())
            return batch

        self.recorder.install(collator, "torch_call", call_torch_call)

    def _stamp(self, batch: Any, examples: Any, places: list) -> None:
        """Each rank row's samples, in `TreeRow.samples` order, as their queue keys' parts (`places`, aligned with
        every row's samples in turn)."""
        import torch

        (rows,) = examples
        counts = [len(row.samples) for row in rows]
        if not isinstance(batch, dict) or len(places) != sum(counts):
            return
        found = torch.full((len(rows), max(counts, default=0), 3), -1, dtype=torch.long)
        start = 0
        for index, count in enumerate(counts):
            for segment, place in enumerate(places[start:start + count]):
                if place is not None:
                    found[index, segment] = torch.tensor(place, dtype=torch.long)
            start += count
        batch[STAMP] = found

    # -- the rebuild ---------------------------------------------------------------------------------------------
    def _record(self, slot: Any, inputs: Any, loss: Any, captured: Any) -> None:
        batch = self._rebuild(inputs, loss, captured)
        if batch is not None:
            self.recorder.handle_loss(slot, batch)

    def _rebuild(self, inputs: Any, loss: Any, captured: Any) -> LossBatch | None:
        """TRL's per-token terms on the detached tensors, summed per sample (`index_add_`, extremes by
        `scatter_reduce`), `loss = sum / (global tokens / processes) / GA` (`:1515-1524`). One host copy."""
        import torch

        trainer, args = self.trainer, self.trainer.args
        selected = inputs["token_index"] >= 0
        token_index = inputs["token_index"][selected]
        log_probs = captured.log_probs.detach().flatten()[token_index]
        entropy = captured.entropy.detach().flatten()[token_index]
        old = inputs["old_log_probs"][selected]
        advantages = inputs["advantages"][selected]
        segment = inputs["segment_id"][selected].to(torch.long)
        log_ratio = log_probs - old
        ratio = torch.exp(log_ratio)
        low, high = args.vllm_importance_sampling_clip_min, args.vllm_importance_sampling_clip_max
        is_masked = (ratio < low) | (ratio > high)
        terms: dict[str, Any] = {}
        if args.score_centering:
            mask_bool = inputs["attention_mask"].bool()
            score = captured.score_log_probs[0].detach()[token_index]
            sampler = inputs["sampler_log_probs"][mask_bool][token_index].exp()  # TRL's q
            scored = score.exp() * (sampler > 0)  # TRL's p
            head = torch.where((scored >= low * sampler) & (scored <= high * sampler), scored, 0.0)
            tail_ratio = (1 - scored.sum(-1)).clamp(min=1e-6) / (1 - sampler.sum(-1)).clamp(min=1e-6)
            tail = ((tail_ratio >= low) & (tail_ratio <= high)).float()
            correction = ((head - tail.unsqueeze(-1) * scored) * score).sum(-1)
            per_token = -advantages * (torch.where(is_masked, 0.0, ratio) * log_probs - correction)
            terms["sampling/sampler_mass"] = sampler.sum(-1)
        else:
            clipped = torch.clamp(ratio, 1 - trainer.epsilon_low, 1 + trainer.epsilon_high)
            per_token = -torch.min(ratio * advantages, clipped * advantages) * ~is_masked
        is_low = (ratio < 1 - trainer.epsilon_low) & (advantages < 0)
        is_high = (ratio > 1 + trainer.epsilon_high) & (advantages > 0)
        terms = {"loss": per_token, "entropy": entropy, "clip_ratio/low_mean": is_low.float(),
                 "clip_ratio/high_mean": is_high.float(), "clip_ratio/region_mean": (is_low | is_high).float(),
                 "sampling/importance_sampling_ratio/mean": ratio,
                 "sampling/sampling_logp_difference/mean": log_ratio.abs(), "sampling/masked_mean": is_masked.float(),
                 **terms}  # fmt: skip
        count = int(segment.max()) + 1 if segment.numel() else 0
        places = inputs[STAMP][0][:count]
        if count == 0 or bool((places < 0).any()):
            return None  # a sample the main process did not key: its rows would name no sample

        def add(values: Any) -> Any:
            return torch.zeros(count, dtype=torch.float64, device=values.device).index_add_(0, segment, values.double())

        def reduce(values: Any, how: str) -> Any:
            start = torch.full((count,), float("inf") if how == "amin" else float("-inf"), dtype=torch.float64,
                               device=values.device)  # fmt: skip
            return start.scatter_reduce(0, segment, values.double(), reduce=how, include_self=True)

        columns = [add(torch.ones_like(ratio)), *(add(value) for value in terms.values()), reduce(ratio, "amin"),
                   reduce(ratio, "amax"), reduce(log_ratio.abs(), "amax"), *places.T.to(ratio.device)]  # fmt: skip
        aux = getattr(captured, "aux_loss", None) if getattr(trainer, "aux_loss_enabled", False) else None
        host = copy_to_host(columns, torch.ones(count, 1, device=ratio.device),
                            scalars=[loss, aux, inputs["global_n_tokens"][0]])  # fmt: skip
        reported, aux_value, global_tokens = host.scalars
        accumulation = float(trainer.current_gradient_accumulation_steps)
        normalizer = max(global_tokens / float(trainer.accelerator.num_processes), 1.0)
        names, width = list(terms), 1 + len(terms)
        rows, keys = [], []
        for values in host.rows:
            tokens = values[0]
            metrics = {name: total / tokens for name, total in zip(names, values[1:width], strict=True)}
            ratio_min, ratio_max, difference_max, version, group, index = values[width:]
            metrics.update({"sampling/importance_sampling_ratio/min": ratio_min,
                            "sampling/importance_sampling_ratio/max": ratio_max,
                            "sampling/sampling_logp_difference/max": difference_max,
                            "clip_ratio/low_min": metrics["clip_ratio/low_mean"],
                            "clip_ratio/high_max": metrics["clip_ratio/high_mean"]})  # fmt: skip
            loss_sum = values[1]
            rows.append(RowSummary(metrics=metrics, weight=tokens, token_count=int(tokens),
                                   mask_sha256=hash_mask([1.0] * int(tokens)), loss_sum=loss_sum,
                                   normalizer=normalizer, scale=1.0 / accumulation,
                                   contribution=loss_sum / normalizer / accumulation,
                                   contribution_source=ContributionSource.PROBE_REDUCER))  # fmt: skip
            keys.append(f"{int(version)}:{int(group)}:{int(index)}")
        batch_terms = {"aux_loss": trainer.router_aux_loss_coef * aux_value / accumulation} \
            if aux_value is not None else {}  # fmt: skip
        return LossBatch(split=SampleSplit.TRAIN, keys=keys, rows=rows, reported_loss=reported,
                         batch_terms=batch_terms, normalizer=normalizer, scale=1.0 / accumulation,
                         dtype=get_tensor_dtype(captured.log_probs),
                         dtypes={"entropy": get_tensor_dtype(captured.entropy)})  # fmt: skip
