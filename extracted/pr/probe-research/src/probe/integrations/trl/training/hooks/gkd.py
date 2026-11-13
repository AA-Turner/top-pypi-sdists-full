"""GKD's per-sample divergence (`gkd_trainer.py:238-358`; spike S1). `compute_loss` calls the instance attribute
`generalized_jsd_loss` (a static method, looked up through `self.`) once; the hook wraps it, lets TRL's call run
untouched, and after `compute_loss` returns recomputes the per-token divergence of the SAME detached logits one row at
a time under `no_grad` (the real function, `reduction="none"`, summed over the vocabulary): one row's [T, V] at a
time, never the batch's. A row's key is the sample recorder's: the call `_maybe_generate` took for its micro-batch
(train, stamped on the batch it returns) or the eval call `prediction_step` took."""

from __future__ import annotations

import functools
import inspect
from collections.abc import Mapping, Sequence
from dataclasses import replace
from typing import Any

from probe.generated.samples import SampleSplit
from probe.generated.samples.points import ContributionSource, Dtype

from ..declarations import EVAL_KEY_PREFIX, make_rollups
from ..hook import LossBatch, LossHook, copy_rows_to_host, get_tensor_dtype, is_scaled_for_accumulation

WHAT = "a per-sample loss"
#: The batch key a train micro-batch's sample-key prefix rides from `_maybe_generate` to `compute_loss` (a string:
#: transformers' `_prepare_inputs` keeps it, GKD's loss reads named keys only).
KEY = "_probe_points_key"
#: Arguments the hook sets itself on the per-row recompute.
OWN = ("student_logits", "teacher_logits", "labels", "reduction", "num_items_in_batch")


class GkdLoss(LossHook):
    names = ("GKDTrainer",)
    loss_method = "compute_loss"

    def __init__(self, trainer: Any, recorder: Any) -> None:
        super().__init__(trainer, recorder)
        self._is_inside = False
        self._captured: list = []
        self._jsd: Any = None

    def get_reduction(self) -> str:
        return "jsd"

    def get_rollups(self, dtype: Dtype, logging_window: int | None, dtypes: Mapping[str, Dtype] | None = None,
                    eval_prefixes: Sequence[str] = (EVAL_KEY_PREFIX,)) -> dict[str, dict]:  # fmt: skip
        return make_rollups((), dtype=dtype, dtypes=dtypes, logging_window=logging_window, eval_prefixes=eval_prefixes)

    def install(self) -> None:
        trainer, guard = self.trainer, self.recorder.guard
        jsd = self._jsd = trainer.generalized_jsd_loss
        compute = trainer.compute_loss

        @functools.wraps(jsd)
        def call_jsd(*args: Any, **kwargs: Any) -> Any:
            result = jsd(*args, **kwargs)
            if self._is_inside:
                self._captured.append((args, kwargs))
            return result

        @functools.wraps(compute)
        def call_compute(model: Any, inputs: Any, *args: Any, **kwargs: Any) -> Any:
            split = guard.call(WHAT, self._get_split) or SampleSplit.TRAIN
            slot = guard.call(WHAT, self.recorder.open_call, split)
            prefix = guard.call(WHAT, self._get_prefix, inputs, split) if slot is not None else None
            self._is_inside, self._captured = slot is not None, []
            try:
                result = compute(model, inputs, *args, **kwargs)
            finally:
                captured, self._is_inside, self._captured = self._captured, False, []
            if slot is not None and prefix is not None and len(captured) == 1:  # one divergence per call
                items = kwargs.get("num_items_in_batch", args[1] if len(args) > 1 else None)
                guard.call(WHAT, self._record, slot, split, prefix, inputs, result, captured[0], items)
            return result

        self.recorder.install(trainer, "generalized_jsd_loss", call_jsd)
        self.recorder.install(trainer, "compute_loss", call_compute)
        self._install_stamp()

    def _install_stamp(self) -> None:
        """Each train micro-batch `_maybe_generate` returns carries its key prefix: transformers collects every
        micro-batch of an update before training the first (`get_batch_samples`), so the last call is not the one
        trained."""
        trainer, guard = self.trainer, self.recorder.guard
        maybe_generate = getattr(trainer, "_maybe_generate", None)
        if not callable(maybe_generate):
            return

        @functools.wraps(maybe_generate)
        def call_maybe_generate(*args: Any, **kwargs: Any) -> Any:
            batch = maybe_generate(*args, **kwargs)
            guard.call(WHAT, self._stamp, batch)
            return batch

        self.recorder.install(trainer, "_maybe_generate", call_maybe_generate)

    def _stamp(self, batch: Any) -> None:
        if isinstance(batch, dict):
            batch[KEY] = self._make_prefix(SampleSplit.TRAIN)

    def _get_split(self) -> str:
        return SampleSplit.TRAIN if self.trainer.model.training else SampleSplit.EVAL

    def _get_prefix(self, inputs: Any, split: str) -> str | None:
        """The sample recorder's key prefix for this call's rows (`{split}:{step}:{call}:{process}`)."""
        if split == SampleSplit.TRAIN:
            found = inputs.get(KEY) if isinstance(inputs, Mapping) else None
            return found if isinstance(found, str) else None
        return self._make_prefix(split)

    def _make_prefix(self, split: str) -> str:
        step, call = self.recorder.get_last_call(split)
        return f"{split}:{step}:{call}:{self.recorder.rank}"

    def _record(self, slot: Any, split: str, prefix: str, inputs: Any, result: Any, captured: Any,
                items: Any) -> None:  # fmt: skip
        self.recorder.handle_loss(slot, self._rebuild(split, prefix, inputs, result, captured, items))

    def _rebuild(self, split: str, prefix: str, inputs: Any, result: Any, captured: Any, items: Any) -> LossBatch:
        """`loss = sum / num_items_in_batch` (train, already GA-scaled when transformers says so) or the masked token
        mean (eval, `batchmean`); each row's divergence recomputed alone from the logits TRL passed in."""
        import torch

        args, kwargs = captured
        bound = inspect.signature(self._jsd).bind(*args, **kwargs).arguments
        student, teacher = bound["student_logits"].detach(), bound["teacher_logits"].detach()
        labels = bound["labels"]
        rest = {name: value for name, value in bound.items() if name not in OWN}
        per_token = torch.zeros(labels.shape, dtype=torch.float64, device=student.device)
        with torch.no_grad():
            for index in range(student.shape[0]):  # one row's [T, V] at a time
                divergence = self._jsd(student[index:index + 1], teacher[index:index + 1], labels=None,
                                       reduction="none", **rest)  # fmt: skip
                per_token[index] = divergence.sum(-1)[0]
        loss = result[0] if isinstance(result, tuple) else result
        given = bound.get("num_items_in_batch")
        host = copy_rows_to_host({"loss": per_token}, labels != -100, loss="loss", scalars=[loss, given])
        reported, given_number = host.scalars
        normalizer = given_number if given_number is not None else float(max(sum(r.token_count for r in host.rows), 1))
        accumulation = float(self.trainer.current_gradient_accumulation_steps)
        is_train = split == SampleSplit.TRAIN
        scale = 1.0 if not is_train or is_scaled_for_accumulation(self.trainer, items) else 1.0 / accumulation
        rows = [replace(row, normalizer=normalizer, scale=scale, contribution=(row.loss_sum or 0.0) / normalizer * scale,
                        contribution_source=ContributionSource.PROBE_REDUCER) for row in host.rows]  # fmt: skip
        return LossBatch(split=split, keys=[f"{prefix}:{row}" for row in range(len(rows))], rows=rows,
                         reported_loss=reported * scale if reported is not None else None, normalizer=normalizer,
                         scale=scale, dtype=get_tensor_dtype(student, teacher))  # fmt: skip
