"""The verl driver's side of per-sample metrics. Before `_update_actor` it stamps the step's batch with a row id
column (it rides verl's dp split, shuffle and dynamic batching into the loss, proven in S0) and the step's sample
keys (the recorder's own); after it, takes them off again. A validation pass logs each sample's eval values under the
series verl builds from them (`val-core|val-aux/<data source>/<var>/mean@<n>`). Line refs are `verl-project/verl@b17218ba58a6`."""

from __future__ import annotations

import json
import math
import sys
import threading
from collections import Counter, defaultdict
from collections.abc import Callable, Mapping, Sequence
from typing import Any

from probe.generated.samples import SampleSplit
from probe.generated.samples.points import UpdateLevel

from ..rows import Split, make_sample_key
from .loss import ROW_FIELD
from .plan import ENTROPY_KEY
from .training import STEP_FIELD


def get_role_config(config: Any, role: str) -> Any:
    """The actor's (`actor_rollout_ref.actor`) or the critic's (`critic`) section of the trainer's config."""
    return _get(config, "critic") if role == "critic" else _get(_get(config, "actor_rollout_ref"), "actor")


def get_reduction(config: Any, role: str = "actor") -> str | None:
    """The role's `loss_agg_mode`."""
    return _get(get_role_config(config, role), "loss_agg_mode")


def count_updates(config: Any, rows: int, role: str = "actor") -> int | None:
    """verl's optimizer updates in one step: mini-batches x `ppo_epochs` (`engine_workers.py:322-352`); the critic
    splits its batch by its own section's sizes (`ray_trainer.py:1378`)."""
    section = get_role_config(config, role)
    size = _as_int(_get(section, "ppo_mini_batch_size"))
    samples = _as_int(_get(_get(_get(config, "actor_rollout_ref"), "rollout"), "n")) or 1
    epochs = _as_int(_get(section, "ppo_epochs")) or 1
    if not size:
        return None
    return max(rows // (size * samples), 1) * epochs


def stamp_update_batch(trainer: Any, batch: Any, step: int, keys: Sequence[str],
                       role: str = "actor") -> Callable[[], None] | None:  # fmt: skip
    """The row ids and the step's facts on a legacy `DataProto` about to train the actor (`ray_trainer.py:1327`) or
    the critic (`:1378`); ``keys``: each row's sample key as the recorder names it (`VerlRecorder.record_train`), in
    batch order. Returns what takes them off again. None when this is not a real verl batch (no torch loaded: a fake
    in a test) or the keys do not name its rows one for one."""
    torch = sys.modules.get("torch")
    size = getattr(getattr(batch, "batch", None), "batch_size", None)
    if torch is None or not size or len(keys) != int(size[0]):
        return None
    count = int(size[0])
    facts = {"step": step, "keys": list(keys), "updates_in_step": count_updates(trainer.config, count, role),
             "reduction": get_reduction(trainer.config, role)}  # fmt: skip
    batch.batch[ROW_FIELD] = torch.arange(count)
    batch.meta_info[STEP_FIELD] = json.dumps(facts)

    def clear() -> None:
        if ROW_FIELD in batch.batch.keys():
            batch.batch.pop(ROW_FIELD)
        batch.meta_info.pop(STEP_FIELD, None)

    return clear


def read_entropy_rows(batch: Any, output: Any) -> list[tuple[float, float]] | None:
    """Each row's (entropy sum, trained tokens) from the driver's old-log-prob pass (`_compute_old_log_prob`,
    `ray_trainer.py:1290-1325`): the `entropys` it returns over the batch's `response_mask`, the very tensors `fit()`
    folds into `actor/entropy` (`:1587-1593`). One host copy; no forward of Probe's own. None: not that pass's output."""
    old_log_prob = output[0] if isinstance(output, tuple) else output
    entropys = old_log_prob.batch["entropys"]
    mask = batch.batch["response_mask"].to(entropys.dtype)
    sums, tokens = (entropys.detach() * mask).sum(-1), mask.sum(-1)
    import torch

    pairs = torch.stack([sums, tokens], dim=-1).double().tolist()
    return [(float(total), float(count)) for total, count in pairs]


def build_entropy_points(step: int, keys: Sequence[str], rows: Sequence[tuple[float, float]],
                         reduction: str | None) -> list[dict[str, Any]]:  # fmt: skip
    """`actor/entropy` rows with no update (the pass trains nothing): each row's token mean, weighted by its tokens
    under token-mean, 1 under seq-mean-token-mean (`plan.ENTROPY_MODES`); a row with no trained token sends nothing
    (verl's own fold skips it). The step's weighted mean is verl's series."""
    if len(keys) != len(rows):
        return []
    is_token_mean = (reduction or "token-mean") == "token-mean"
    points = []
    for key, (total, count) in zip(keys, rows, strict=True):
        if count <= 0 or not math.isfinite(total):
            continue
        points.append({"sample_key": key, "step": step, "metrics": {ENTROPY_KEY: total / count},
                       "weights": {ENTROPY_KEY: count if is_token_mean else 1.0}})  # fmt: skip
    return points


class EvalPoints:
    """Each validation pass's per-sample eval values, as producer `verl` (the driver's own)."""

    def __init__(self, samples: Any) -> None:
        self._samples = samples
        self._passes: Counter = Counter()
        self._lock = threading.Lock()

    def log(self, step: int, rows: Sequence[Any], reward_extras: Mapping[str, Sequence[Any]] | None) -> int:
        """One pass's rows (`readers.build_validation_rows`, in pass order) with verl's per-response values
        (`reward_extra_infos_dict`, aligned with them). Returns the rows sent."""
        points = build_eval_points(rows, reward_extras or {})
        if not points:
            return 0
        with self._lock:
            eval_pass = self._passes[step]
            self._passes[step] += 1
        sent = [{"sample_key": make_sample_key(Split.EVAL, step, row), "step": step, "split": SampleSplit.EVAL,
                 "eval_pass": eval_pass, "metrics": metrics} for row, metrics in points]  # fmt: skip
        self._samples.log_metrics_many(sent)
        self._samples.log_update(step, None, level=UpdateLevel.UPDATE, split=SampleSplit.EVAL, eval_pass=eval_pass,
                                 ranks_expected=1)  # fmt: skip
        self._samples.log_update(step, None, level=UpdateLevel.RANK, split=SampleSplit.EVAL, eval_pass=eval_pass,
                                 rows_expected=len(sent))  # fmt: skip
        return len(sent)


def build_eval_points(rows: Sequence[Any], reward_extras: Mapping[str, Sequence[Any]]) -> list[tuple[Any, dict]]:
    """Per row, its values under the keys verl's `_val_metrics_update` (`ray_trainer.py:721-746`) logs their means
    as: `mean@n` over a prompt's n responses, then the plain mean over the prompts with n (equal weights). A var is
    `val-core` for the data source's core var (`acc`, else `reward`) at its largest n, else `val-aux`. Texts and
    missing values are skipped, as `process_validation_metrics` skips them (`metric_utils.py:1001-1008`)."""
    count = len(rows)
    columns = {name: list(values) for name, values in reward_extras.items() if len(values) == count}
    groups: dict[tuple[str, str, str], list[int]] = defaultdict(list)
    for index, row in enumerate(rows):
        for name, values in columns.items():
            if _as_number(values[index]) is not None:
                groups[(str(row.data_source), str(row.uid), name)].append(index)
    largest: dict[tuple[str, str], int] = {}
    present: dict[str, set[str]] = defaultdict(set)
    for (source, _uid, name), indexes in groups.items():
        largest[(source, name)] = max(largest.get((source, name), 0), len(indexes))
        present[source].add(name)
    points: list[dict[str, float]] = [{} for _ in rows]
    for (source, _uid, name), indexes in groups.items():
        core = "acc" if "acc" in present[source] else "reward"
        size = len(indexes)
        section = "val-core" if name == core and size == largest[(source, name)] else "val-aux"
        for index in indexes:
            points[index][f"{section}/{source}/{name}/mean@{size}"] = _as_number(columns[name][index])
    return [(row, metrics) for row, metrics in zip(rows, points, strict=True) if metrics]


def _as_number(value: Any) -> float | None:
    if value is None or isinstance(value, str):
        return None
    item = getattr(value, "item", None)
    try:
        number = float(item() if callable(item) else value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _as_int(value: Any) -> int | None:
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _get(target: Any, name: str) -> Any:
    if target is None:
        return None
    if isinstance(target, Mapping):
        return target.get(name)
    try:
        return getattr(target, name, None)
    except Exception:  # noqa: BLE001 -- an OmegaConf interpolation that cannot resolve here
        return None
