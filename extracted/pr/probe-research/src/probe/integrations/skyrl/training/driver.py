"""SkyRL's training task (the driver of the policy workers) side of per-sample metrics. After the batch conversion
it puts each row's sample key in the batch's metadata (which rides SkyRL's dp chunks to the workers); its
`_normalize_advantages` wrap adds a row id column and each row's loss-reduction scale, from SkyRL's own
`apply_loss_reduction_to_advantages_minibatch` run on ones (S0: constant per row in every mode). An eval generate
call logs each trajectory's reward under the series SkyRL builds from it (`eval/<data source>/avg_score`,
`mean_positive_reward`). Line refs are `NovaSky-AI/SkyRL@d87004689e3a`."""

from __future__ import annotations

import functools
import threading
from collections import Counter
from collections.abc import Mapping, Sequence
from typing import Any

from probe.generated.samples import SampleSplit
from probe.generated.samples.points import UpdateLevel

from .loss import POLICY_LOSSES_MODULE, ROW_FIELD, SCALE_FIELD
from .training import KEYS_FIELD, UPDATES_FIELD, WHAT

#: SkyRL's own `batch_metadata.training_phase` for an eval generate call.
EVAL_PHASE = "eval"


def stamp_training_keys(trainer: Any, batch: Any, row_keys: Sequence[Sequence[str]]) -> bool:
    """Each training row's sample key in ``batch.metadata``; a row with no single sample (a merged step-wise row,
    SkyRL's dp padding that copies row 0) gets None. A step-wise row is one segment's own sample
    (`outputs.py:147-154`); dp padding is dropped in the worker (`training.drop_dp_padding_rows`). The row ids ride
    from here, so the critic (trained before `_normalize_advantages`) can name its rows."""
    import torch

    keys: list[str | None] = [found[0] if len(found) == 1 else None for found in row_keys]
    keys += [None] * max(len(batch) - len(keys), 0)
    if batch.metadata is None:
        batch.metadata = {}
    batch.metadata[KEYS_FIELD] = keys[: len(batch)]
    batch[ROW_FIELD] = torch.arange(len(batch))
    return True


def setup_trainer_wraps(trainer: Any, guard: Any) -> None:
    """On this instance: ``_normalize_advantages`` adds the row ids and scales to a stamped batch, and
    ``train_critic_and_policy`` takes every field Probe added off the batch once it has trained."""
    normalize_original = trainer._normalize_advantages
    train_original = trainer.train_critic_and_policy

    @functools.wraps(normalize_original)
    def normalize(data: Any, mini_batch_boundaries: Any, *args: Any, **kwargs: Any) -> Any:
        if KEYS_FIELD in (getattr(data, "metadata", None) or {}):
            prompt_boundaries = kwargs.get("prompt_boundaries", args[0] if args else None)
            guard.call(WHAT, stamp_scales, trainer, data, mini_batch_boundaries, prompt_boundaries)
        return normalize_original(data, mini_batch_boundaries, *args, **kwargs)

    @functools.wraps(train_original)
    def call_train_critic_and_policy(data: Any, *args: Any, **kwargs: Any) -> Any:
        try:
            return train_original(data, *args, **kwargs)
        finally:
            guard.call(WHAT, clear_stamps, data)

    object.__setattr__(trainer, "_normalize_advantages", normalize)
    object.__setattr__(trainer, "train_critic_and_policy", call_train_critic_and_policy)


def clear_stamps(data: Any) -> None:
    """The row ids, scales, keys and update count off a trained batch (SkyRL keeps the batch for its callbacks)."""
    for name in (ROW_FIELD, SCALE_FIELD):
        if name in data:
            dict.pop(data, name)
    metadata = getattr(data, "metadata", None)
    if isinstance(metadata, dict):
        metadata.pop(KEYS_FIELD, None)
        metadata.pop(UPDATES_FIELD, None)


def stamp_scales(trainer: Any, data: Any, mini_batch_boundaries: Sequence[tuple[int, int]],
                 prompt_boundaries: Sequence[tuple[int, int]] | None) -> None:  # fmt: skip
    """Each row's advantage scale (its 1 / normalizer) as SkyRL's own reduction computes it, its row id, and the
    step's update count (`update_epochs_per_batch` x mini-batches, `trainer.py:1645-1657`)."""
    import sys

    import torch

    apply = sys.modules[POLICY_LOSSES_MODULE].apply_loss_reduction_to_advantages_minibatch
    trainer_config = trainer.cfg.trainer
    ones = torch.ones_like(data["advantages"])
    scales = torch.zeros_like(ones)
    for start, end in mini_batch_boundaries:
        boundaries = None if prompt_boundaries is None else [
            (first - start, last - start) for first, last in prompt_boundaries if start <= first < end]  # fmt: skip
        scales[start:end] = apply(advantages=ones[start:end], loss_mask=data["loss_mask"][start:end],
                                  loss_reduction=trainer_config.algorithm.loss_reduction,
                                  micro_batch_size=trainer_config.micro_train_batch_size_per_gpu,
                                  max_seq_len=trainer_config.algorithm.max_seq_len, prompt_boundaries=boundaries)  # fmt: skip
    data[SCALE_FIELD] = scales[:, 0].clone().to(torch.float64)
    data[ROW_FIELD] = torch.arange(len(data))
    data.metadata[UPDATES_FIELD] = int(trainer_config.update_epochs_per_batch) * len(mini_batch_boundaries)


class EvalPoints:
    """Each eval pass's per-trajectory rewards, as producer `skyrl` (the training task's own)."""

    def __init__(self, samples: Any) -> None:
        self._samples = samples
        self._declared: set[int] = set()
        self._lock = threading.Lock()

    def log(self, inputs: Mapping[str, Any], output: Mapping[str, Any], parts: Sequence[Mapping[str, Any]]) -> int:
        """One eval generate call's rows (``parts``, one per output row). Every eval call of a step is that step's
        one pass (`eval_pass` 0): their keys carry the call, so two passes never collide."""
        metadata = inputs.get("batch_metadata")
        if getattr(metadata, "training_phase", None) != EVAL_PHASE or output.get("is_last_step") is not None:
            return 0  # train calls, and step-wise output (several rows a trajectory) are not eval passes here
        step = getattr(metadata, "global_step", None)
        step = step if isinstance(step, int) and not isinstance(step, bool) else 0
        sent = build_eval_rows(step, inputs.get("env_extras") or [], output.get("rewards") or [], parts)
        if not sent:
            return 0
        self._samples.log_metrics_many(sent)
        with self._lock:
            is_new = step not in self._declared
            self._declared.add(step)
        if is_new:
            self._samples.log_update(step, None, level=UpdateLevel.UPDATE, split=SampleSplit.EVAL, eval_pass=0,
                                     ranks_expected=1)  # fmt: skip
        return len(sent)


def build_eval_rows(step: int, env_extras: Sequence[Any], rewards: Sequence[Any],
                    parts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:  # fmt: skip
    """Per row, its reward under SkyRL's per-data-source keys (`trainer_utils.py:235-272`, the reward summed over
    tokens when it is a token list, `generators/utils.py:226-241`): plain means, weight 1."""
    rows = []
    seen: Counter = Counter()
    for index, part in enumerate(parts):
        if part.get("split") != SampleSplit.EVAL or index >= len(rewards):
            continue
        extra = env_extras[index] if index < len(env_extras) else None
        source = extra.get("data_source") if isinstance(extra, Mapping) else None
        source = "unknown" if source is None else str(source).replace("/", "_")  # `sanitize_data_source`
        reward = rewards[index]
        if isinstance(reward, (list, tuple)):
            total, positive = float(sum(reward)), float(sum(max(r, 0) for r in reward))
        else:
            total = float(reward)
            positive = max(total, 0.0)
        key = part["key"]
        rows.append({"sample_key": key, "step": step, "split": SampleSplit.EVAL, "eval_pass": 0, "occurrence": seen[key],
                     "metrics": {f"eval/{source}/avg_score": total, f"eval/{source}/mean_positive_reward": positive}})  # fmt: skip
        seen[key] += 1
    return rows


def _get(target: Any, name: str) -> Any:
    if target is None:
        return None
    if isinstance(target, Mapping):
        return target.get(name)
    return getattr(target, name, None)
