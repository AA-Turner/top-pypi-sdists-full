"""The rollout process's sample hooks (RL plan §6.1 W15): train, eval and dropped samples as generator
parts of producer `rollout`, one seal per step. Each hook returns False (Miles still logs its own metrics)
and never raises. Hook signatures: upstream `ray/rollout/metrics.py:27-31,80-84`, `rollout/sglang_rollout.py:578`."""

from __future__ import annotations

import argparse
import functools
import json
import logging
import re
import threading
from collections.abc import Callable, Iterable, Mapping
from typing import Any

from probe.integrations.miles.samples.events import get_event_recorder
from probe.integrations.miles.samples.mapping import (
    MappingConfig,
    build_generator_part,
    build_group_key,
    build_train_key,
    get_harbor_key,
    get_status,
    read_reward,
    read_scheduled_step,
)
from probe.integrations.miles.samples.producers import PROCESS, ROLLOUT

logger = logging.getLogger(__name__)

#: Miles' count-only drops, by metric (`filter_hub/base_types.py:61-65`, `fully_async_data_buffer.py:331-336`).
DYNAMIC_FILTER_PREFIX = "rollout/dynamic_filter/drop_"
FULLY_ASYNC_DROPS = {
    "rollout/fully_async/stale_groups_filtered": "stale",
    "rollout/fully_async/aborted_groups_filtered": "aborted",
}
#: The stock dynamic filter's reasons (`filter_hub/common_filters.py:86,92,108`) as drop reasons.
_FILTER_REASONS = {"group_has_aborted": "aborted", "group_has_missing_reward": "invalid_reward"}
_FILTER_NAME = re.compile(r"[^A-Za-z0-9_.\-]+")


def add_hook_arguments(parser: argparse.ArgumentParser) -> None:
    """The hooks' own Miles flags: upstream turns them into the hook's `config_class` and hands the
    values back on frozen `fn_args` (`utils/args/custom_function.py:263-297`); the fork reads `args`."""
    parser.add_argument("--probe-sample-metrics", type=json.loads, default=None,
                        help='Extra per-sample metrics as JSON: {"metric name": "dotted Sample path"}.')
    parser.add_argument("--probe-reward-max", type=float, default=None,
                        help="The full reward a sample passes at (default 1.0, for 0/1 verifiers).")


class RolloutCapture:
    """One rollout process's step state: the dropped groups waiting for their step, the eval passes met
    per step, and the plan fields sent once."""

    def __init__(self) -> None:
        self._dropped: list[list] | None = None
        self._eval_calls: dict[int, int] = {}
        self._has_planned = False
        self._lock = threading.Lock()

    def log_train(self, rollout_id: int, args: Any, samples: list, extra_metrics: Mapping | None,
                  metric_paths: Mapping[str, str] | None = None) -> None:
        writer = PROCESS.get_samples(ROLLOUT, args)
        if writer is None:
            return
        self._plan_once(writer, args)
        config = MappingConfig.from_args(args, metric_paths=metric_paths, run_id=_get_run_id(args))
        is_async = bool(getattr(args, "fully_async", False))
        with self._lock:
            dropped, self._dropped = self._dropped, None
        kept = {_get_identity(sample) for sample in samples}
        parts, groups = _build_parts(samples, rollout_id, config, is_async=is_async)
        drop_groups = [g for g in dropped or () if not any(_get_identity(s) in kept for s in _iter_samples(g))]
        for group in drop_groups:
            reason = derive_drop_reason(list(_iter_samples(group)), args)
            more_parts, more_groups = _build_parts(list(_iter_samples(group)), rollout_id, config,
                                                   is_async=is_async, drop_reason=reason)
            parts += more_parts
            groups.update(more_groups)
        writer.log(parts, step=rollout_id)
        writer.log_groups(_to_group_items(groups, args))
        writer.seal(rollout_id, dropped=read_drop_counts(extra_metrics, has_stored_drops=dropped is not None))
        _end_live_tries(samples, args)

    def log_eval(self, rollout_id: int, args: Any, data: Mapping) -> None:
        writer = PROCESS.get_samples(ROLLOUT, args)
        if writer is None:
            return
        with self._lock:
            call = self._eval_calls.get(rollout_id, 0)
            self._eval_calls[rollout_id] = call + 1
        config = MappingConfig.from_args(args, run_id=_get_run_id(args))
        parts = []
        for dataset, entry in (data or {}).items():
            samples = list(_iter_samples(entry.get("samples") or [])) if isinstance(entry, Mapping) else []
            name = _FILTER_NAME.sub("_", str(dataset))[:64]
            for position, sample in enumerate(samples):
                key = get_harbor_key(sample) or f"eval:{rollout_id}:{call}:{name}:{position}"
                group = f"eval:{rollout_id}:{call}:{name}:{getattr(sample, 'group_index', position)}"
                parts.append(_build_one(sample, key, "eval", rollout_id, config, scheduled=rollout_id, group=group))
        writer.log([part for part in parts if part is not None], step=rollout_id)
        writer.seal(rollout_id)
        _end_live_tries([sample for entry in (data or {}).values() if isinstance(entry, Mapping)
                         for sample in _iter_samples(entry.get("samples") or [])], args)  # fmt: skip

    def stash_dropped(self, all_samples: Iterable) -> None:
        """Every group the rollout made, kept ones included (`sglang_rollout.py:562-580`); the step's
        `log_train` stores those it did not keep. Sync mode only (`arguments.py:155`)."""
        with self._lock:
            self._dropped = [group if isinstance(group, list) else [group] for group in all_samples]

    def _plan_once(self, writer: Any, args: Any) -> None:
        if self._has_planned:
            return
        self._has_planned = True
        fields = {}
        reward_max = getattr(args, "probe_reward_max", None)
        if isinstance(reward_max, (int, float)) and not isinstance(reward_max, bool):
            fields["reward_max"] = float(reward_max)
        staleness = getattr(args, "max_weight_staleness", None)
        if getattr(args, "fully_async", False) and isinstance(staleness, int) and staleness >= 0:
            fields["max_staleness"] = staleness
        if fields:
            writer.plan(**fields)


def read_drop_counts(metrics: Mapping | None, *, has_stored_drops: bool) -> dict[str, int]:
    """Drops Miles only counted, in groups. A step whose dropped groups were stored as samples (the
    all-samples hook ran) leaves its dynamic-filter counts out: never both stored and counted."""
    counts: dict[str, int] = {}
    for name, value in (metrics or {}).items():
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
            continue
        if name in FULLY_ASYNC_DROPS:
            reason = FULLY_ASYNC_DROPS[name]
        elif name.startswith(DYNAMIC_FILTER_PREFIX) and not has_stored_drops:
            reason = to_drop_reason(name[len(DYNAMIC_FILTER_PREFIX):])
        else:
            continue
        counts[reason] = counts.get(reason, 0) + int(value)
    return counts


def to_drop_reason(filter_reason: str) -> str:
    """`zero_std_<reward>` is no variance; the stock filter's other reasons map one to one; a custom
    filter's reason is `filter:<reason>`."""
    if filter_reason.startswith("zero_std"):
        return "zero_variance"
    if filter_reason in _FILTER_REASONS:
        return _FILTER_REASONS[filter_reason]
    return "filter:" + (_FILTER_NAME.sub("_", filter_reason)[:64] or "dynamic")


def derive_drop_reason(group: list, args: Any) -> str:
    """Why a stored group was not kept. Miles records no reason on the group, so the stock filter's
    rules are read again (`common_filters.py:80-110`): an aborted member, a missing reward, one reward
    for all; a group with none of those was over the batch (`sglang_rollout.py:543-546`)."""
    if any(get_status(sample) == "aborted" for sample in group):
        return "aborted"
    key = getattr(args, "reward_key", None)
    rewards = [read_reward(sample, key)[0] for sample in group]
    if any(reward is None for reward in rewards):
        return "invalid_reward"
    if len(group) > 1 and len(set(rewards)) == 1:
        return "zero_variance"
    return "oversampling"


def _build_parts(samples: list, rollout_id: int, config: MappingConfig, *, is_async: bool,
                 drop_reason: str | None = None) -> tuple[list[dict], dict[str, dict]]:
    """Sync: each sample is scheduled at ``rollout_id``. Fully async: at the step its group's first try began under
    (its live try's stamp), else none; its group key names that step too, as its live tries did."""
    parts, groups = [], {}
    for position, sample in enumerate(samples):
        index = getattr(sample, "index", None)
        if get_harbor_key(sample):
            key = get_harbor_key(sample)
        elif index is not None:
            key = build_train_key(rollout_id, index, getattr(sample, "tokens", None) or [])
        else:
            key = f"train:{rollout_id}:p{position}:{drop_reason or 'kept'}"
        scheduled = read_scheduled_step(sample) if is_async else rollout_id
        group = build_group_key(rollout_id if scheduled is None else scheduled, getattr(sample, "group_index", None))
        part = _build_one(sample, key, "train", rollout_id, config, scheduled=scheduled, group=group,
                          drop_reason=drop_reason)
        if part is not None:
            parts.append(part)
            groups.setdefault(group, {"task_key": part.get("task_key"), "scenario": part.get("scenario"),
                                      "drop_reason": drop_reason, "scheduled_step": scheduled})
    return parts, groups


def _build_one(sample: Any, key: str, split: str, step: int, config: MappingConfig, *, scheduled: int | None,
               group: str, drop_reason: str | None = None) -> dict | None:
    recorder = get_event_recorder()
    events = recorder.take_events(getattr(sample, "index", None)) if recorder is not None else None
    try:
        return build_generator_part(sample, key=key, split=split, step=step, config=config,
                                    scheduled_step=scheduled, group_key=group, drop_reason=drop_reason,
                                    events=events)
    except Exception as exc:  # noqa: BLE001 -- one odd sample never costs the rest
        logger.debug("Probe could not map a Miles sample: %s", exc)
        return None


def _to_group_items(groups: Mapping[str, dict], args: Any) -> list[dict]:
    size = getattr(args, "n_samples_per_prompt", None)
    items = []
    for key, facts in groups.items():
        item: dict[str, Any] = {"group_key": key}
        if isinstance(size, int) and size >= 1:
            item["size"] = size
        if facts.get("scheduled_step") is not None:
            item["scheduled_step"] = facts["scheduled_step"]
        for name in ("task_key", "scenario", "drop_reason"):
            if facts.get(name):
                item[name] = facts[name]
        items.append(item)
    return items


def _get_identity(sample: Any) -> Any:
    """`Sample.index` (unique per run, `dashboard/store.py:181`); the object itself when it has none."""
    index = getattr(sample, "index", None)
    return ("index", index) if isinstance(index, int) else ("object", id(sample))


def _iter_samples(items: Iterable) -> Iterable:
    for item in items or ():
        if isinstance(item, list):
            yield from _iter_samples(item)
        else:
            yield item


def _end_live_tries(samples: Iterable, args: Any) -> None:
    """The last chance for a live try still waiting on its grade (`--group-rm`, a wrap that came too late): its
    samples are logged, so it ends now (`../live/`)."""
    from probe.integrations.miles.live import LIVE

    LIVE.end_named(samples, args, is_last_chance=True)


def _get_run_id(args: Any) -> str | None:
    """The run this process writes into (a Harbor trial's span id is derived from it)."""
    return str(getattr(PROCESS.get_handle(args), "id", "") or "") or None


CAPTURE = RolloutCapture()


def _fail_open(hook: Callable[..., None]) -> Callable[..., bool]:
    """A Miles hook: False always (Miles' own logging runs), never a raise, one warning."""
    warned = []

    @functools.wraps(hook)
    def call(*args: Any, **kwargs: Any) -> bool:
        try:
            hook(*args, **kwargs)
        except Exception:  # noqa: BLE001 -- fail open: the rollout loop never sees a Probe error
            if not warned:
                warned.append(True)
                logger.warning("Probe's Miles %s hook failed; Miles continues", hook.__name__, exc_info=True)
        return False

    call.add_arguments = add_hook_arguments
    return call


def make_log_samples(metric_paths: Mapping[str, str] | None = None) -> Callable[..., bool]:
    """`--custom-rollout-log-function-path`: `(rollout_id, fn_args, samples, extra_metrics, rollout_time)`.
    ``metric_paths`` adds per-sample metrics (`{"agent/turns": "metadata.agent_metrics.turns"}`)."""
    configured = dict(metric_paths or {})
    for name, path in configured.items():
        if not isinstance(name, str) or not name or not isinstance(path, str) or not path:
            raise ValueError(f"sample metric {name!r}: names and paths are non-empty strings")

    @_fail_open
    def log_samples(rollout_id: int, args: Any, samples: list, rollout_extra_metrics: Mapping | None = None,
                    rollout_time: float | None = None) -> bool:
        """Kept training samples, as `rollout` generator parts sealed at ``rollout_id``."""
        CAPTURE.log_train(rollout_id, args, list(samples or []), rollout_extra_metrics, configured)

    return log_samples


log_samples = make_log_samples()


@_fail_open
def log_eval_samples(rollout_id: int, args: Any, data: Mapping, extra_metrics: Mapping | None = None) -> bool:
    """`--custom-eval-rollout-log-function-path`: an eval pass's samples, per dataset."""
    CAPTURE.log_eval(rollout_id, args, data)


@_fail_open
def log_dropped_samples(args: Any, all_samples: list, data_source: Any = None) -> bool:
    """`--rollout-all-samples-process-path`: every group, dropped ones included (sync mode only)."""
    CAPTURE.stash_dropped(all_samples)
