"""The verl driver's side of per-sample metrics. Before `_update_actor` it stamps the step's batch with a row id
column (it rides verl's dp split, shuffle and dynamic batching into the loss, proven in S0) and the step's sample
keys (the recorder's own); after it, takes them off again: a legacy `DataProto` in memory, a V1 `KVBatchMeta` through
the TransferQueue, a fully async mini-step at the step verl logs it at (T2c). A validation pass logs each sample's
eval values under the series verl builds from them (`val-core|val-aux/<data source>/<var>/mean@<n>`). Line refs are
`verl-project/verl@b17218ba58a6`."""

from __future__ import annotations

import json
import math
import sys
import threading
from collections import Counter, defaultdict
from collections.abc import Callable, Mapping, Sequence
from typing import Any, NamedTuple

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


class Stamp(NamedTuple):
    """A stamped batch: what takes the stamp off, and the step its rows go to (verl's logging step)."""

    clear: Callable[[], None]
    step: int


class LoggedPlace(NamedTuple):
    """Where verl's fully async trainer logs one mini-step's `actor/*` metrics: the step, the mini-step's position
    among the ones that log folds, and how many it folds."""

    step: int
    position: int
    mini_steps: int


def build_step_facts(trainer: Any, step: int, keys: Sequence[str | None], count: int, role: str = "actor",
                     place: LoggedPlace | None = None) -> dict[str, Any]:  # fmt: skip
    """The JSON facts the worker reads (`training.StepFacts`). ``count``: the batch's rows (padding included);
    ``place``: a fully async mini-step's, whose updates number from its position among the log's mini-steps."""
    updates = count_updates(trainer.config, count, role)
    facts = {"step": step, "keys": list(keys), "updates_in_step": updates, "reduction": get_reduction(trainer.config, role)}
    if place is not None and updates is not None:
        facts["updates_in_step"], facts["first_update"] = updates * place.mini_steps, updates * place.position
    return facts


def stamp_update_batch(trainer: Any, batch: Any, step: int, keys: Sequence[str], role: str = "actor",
                       place: LoggedPlace | None = None) -> Callable[[], None] | None:  # fmt: skip
    """The row ids and the step's facts on a legacy `DataProto` about to train the actor (`ray_trainer.py:1327`) or
    the critic (`:1378`); ``keys``: each row's sample key as the recorder names it (`VerlRecorder.record_train`), in
    batch order; ``place``: a fully async mini-step's (`get_logged_place`). Returns what takes them off again. None when
    this is not a real verl batch (no torch loaded: a fake in a test) or the keys do not name its rows one for one."""
    torch = sys.modules.get("torch")
    size = getattr(getattr(batch, "batch", None), "batch_size", None)
    if torch is None or not size or len(keys) != int(size[0]):
        return None
    count = int(size[0])
    facts = build_step_facts(trainer, step, keys, count, role, place)
    batch.batch[ROW_FIELD] = torch.arange(count)
    batch.meta_info[STEP_FIELD] = json.dumps(facts)

    def clear() -> None:
        if ROW_FIELD in batch.batch.keys():
            batch.batch.pop(ROW_FIELD)
        batch.meta_info.pop(STEP_FIELD, None)

    return clear


def get_logged_place(trainer: Any) -> LoggedPlace:
    """Where verl's fully async trainer logs this mini-step, read before `_fit_update_local_step` moves the counters.
    `fit_step` logs the version's aggregate (`fully_async_trainer.py:601-603`) BEFORE `_fit_postprocess_step` adds the
    current mini-step (`:604`), so a mini-step at version c with local trigger step l of T lands at c + 1 when l < T,
    else c + 2 (with the next cycle's), at position l % T; the first log (step 1) folds only the first T - 1."""
    version, local = int(trainer.current_param_version), int(trainer.local_trigger_step)
    cycle = int(trainer.trigger_parameter_sync_step)
    step = version + 1 if local < cycle else version + 2
    if step == 1:
        return LoggedPlace(step, local - 1, cycle - 1)
    return LoggedPlace(step, local % cycle, cycle)


def build_batch_keys(tags: Sequence[Any], keys: Sequence[str]) -> list[str | None] | None:
    """The recorder's keys (one per REAL row: `fetch_transfer_queue_rows` skips padding) over a V1 batch's positions,
    None at each padding row (`tag["is_padding"]`, `upsample_batch_to_divisible_size`); None when they do not line up."""
    real = [index for index, tag in enumerate(tags) if not (isinstance(tag, Mapping) and tag.get("is_padding"))]
    if len(real) != len(keys):
        return None
    spread: list[str | None] = [None] * len(tags)
    for position, key in zip(real, keys, strict=True):
        spread[position] = key
    return spread


def stamp_transfer_queue_batch(trainer: Any, batch: Any, step: int, keys: Sequence[str],
                               kv_batch_put: Callable[..., Any], role: str = "actor") -> Callable[[], None] | None:  # fmt: skip
    """A V1 `KVBatchMeta` about to train the actor (`v1/trainer_base.py:1840`) or the critic (`:1817`, which hands the
    worker the `KVBatchMeta` itself: the hook reads the facts off its `extra_info`): the row ids go into the TransferQueue
    as one more field of each key (`kv_batch_put`, as verl writes `old_log_probs` back, `:1681`), so each id rides its
    key's row through verl's fetch, dp split, shuffle and micro-batching; the facts go in `extra_info`, which verl's
    `tqbridge` hands the worker as a non-tensor field (`utils/transferqueue_utils.py:160-176`), where the worker hook
    reads it. One put of n int64 a step; the field is cleared with the step's keys (`:512`). Returns what takes the
    facts off again; None when the keys do not name the real rows one for one, or this is not a real verl batch (no
    torch or tensordict loaded: a fake in a test)."""
    torch, tensordict = sys.modules.get("torch"), sys.modules.get("tensordict")
    spread = build_batch_keys(batch.tags, keys)
    if torch is None or tensordict is None or spread is None:
        return None
    count = len(batch.keys)
    facts = build_step_facts(trainer, step, spread, count, role)
    kv_batch_put(keys=list(batch.keys), partition_id=batch.partition_id,
                 fields=tensordict.TensorDict({ROW_FIELD: torch.arange(count)}, batch_size=[count]))  # fmt: skip
    fields = batch.fields
    if fields is not None and ROW_FIELD not in fields:
        batch.fields = [*fields, ROW_FIELD]
    batch.extra_info[STEP_FIELD] = json.dumps(facts)

    def clear() -> None:
        batch.extra_info.pop(STEP_FIELD, None)
        batch.fields = fields

    return clear


def read_transfer_queue_entropy(batch: Any, kv_batch_get: Callable[..., Any]) -> list[tuple[float, float]]:
    """Each REAL row's (entropy sum, trained tokens) from the `entropy` and `response_mask` the V1 old-log-prob pass
    wrote to the TransferQueue, the fields verl folds into `actor/entropy` (`v1/trainer_base.py:1686-1693`), in batch
    order without the padding rows. One read of two fields; no forward of Probe's own."""
    import torch

    data = kv_batch_get(keys=list(batch.keys), partition_id=batch.partition_id,
                        select_fields=["entropy", "response_mask"]).to_padded_tensor()  # fmt: skip
    entropy = data["entropy"].detach()
    mask = data["response_mask"].to(entropy.dtype)
    pairs = torch.stack([(entropy * mask).sum(-1), mask.sum(-1)], dim=-1).double().tolist()
    return [(float(total), float(tokens)) for (total, tokens), tag in zip(pairs, batch.tags, strict=True)
            if not (isinstance(tag, Mapping) and tag.get("is_padding"))]  # fmt: skip


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


def build_entropy_points(step: int, keys: Sequence[str], rows: Sequence[tuple[float, float]], reduction: str | None,
                         is_per_mini_step: bool = False) -> list[dict[str, Any]]:  # fmt: skip
    """`actor/entropy` rows with no update (the pass trains nothing): each row's token mean, weighted by its tokens
    under token-mean, 1 under seq-mean-token-mean (`plan.ENTROPY_MODES`); a row with no trained token sends nothing
    (verl's own fold skips it). The step's weighted mean is verl's series. ``is_per_mini_step``: the fully async
    trainer folds each mini-step's pass, then takes the plain mean over the log's mini-steps (`detach_utils.py:
    248-307`), so each weight is divided by its pass's total (T2c finding 4)."""
    if len(keys) != len(rows):
        return []
    is_token_mean = (reduction or "token-mean") == "token-mean"
    points = []
    for key, (total, count) in zip(keys, rows, strict=True):
        if count <= 0 or not math.isfinite(total):
            continue
        points.append({"sample_key": key, "step": step, "metrics": {ENTROPY_KEY: total / count},
                       "weights": {ENTROPY_KEY: count if is_token_mean else 1.0}})  # fmt: skip
    total_weight = sum(point["weights"][ENTROPY_KEY] for point in points)
    if is_per_mini_step and total_weight:
        for point in points:
            point["weights"][ENTROPY_KEY] /= total_weight
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
