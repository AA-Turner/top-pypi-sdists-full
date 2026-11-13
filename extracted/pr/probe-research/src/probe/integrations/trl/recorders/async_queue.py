"""AsyncGRPO and AsyncDistillation samples (experimental, RL plan §6.6): every `RolloutSample` the trainer's queue
reader hands out (`RolloutQueueDataset.__iter__`, `async_grpo_trainer.py:286-349`), with its exact `model_version`,
and every stale drop with its true staleness. `__iter__` is looked up on the class, so the reader is watched through
the two attributes it calls instead: `queue.get` (what it drained) and `model_version_fn` (the version it judged
staleness by). AsyncGRPO's rollouts are live samples in its rollout process (`rollout_loop.py`); each drained sample names
its own. Line refs are `huggingface/trl@4ae4d34a86f3` `trl/experimental/async_grpo/`."""

from __future__ import annotations

import functools
import pickle
import time
from collections import Counter, deque
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from probe.generated.samples import CaptureField

from ..recorder import Recorder
from ..rollout_loop import ProbeRolloutLoop, take_rollout_key
from ..rows import (
    TOOL_FIELDS,
    RowReader,
    build_completion,
    render_prompt,
    to_finite,
    to_ints,
    to_numbers,
)

#: The worker sends a bare group id for a group it dropped whole (all rewards equal, `async_rollout_worker.py:997`):
#: no sample of it reaches the trainer, so it is a seal count. TRL sends a `filter_prompt` rejection the same way.
WHOLE_GROUP_DROP = "zero_variance"
REWARD_KEY = "reward_kept"  # the rollout's total reward (`async_rollout_worker.py:1442`)
REWARD_PART = ("rewards/", "/mean")  # each reward function's own (`:1445-1450`)
UNSCORED = "reward_fn: no reward function scored this rollout"
#: Kept samples waiting for their micro-batch: the batcher holds one micro-batch, so this never fills unless the
#: collator stops being watched; past it the oldest is forgotten (it then reads `generated`, never consumed).
MAX_WAITING = 10_000


#: What AsyncGRPO cannot give a sample (`plan(unsupported=)`), and why.
ASYNC_NUMBERED_IDS = ("TRL's parser gives tool calls no id: Probe numbers them probe-<turn>-<i> and links each result "
                      "in call order (the rollout process awaits each call in turn), checked by tool name")
ASYNC_FILES = ("AsyncGRPO runs tools in its rollout process, where the sample is not written: a tool's files cannot "
               "reach its sample")
#: AsyncDistillation's rollout is one plain student reply: its worker takes no tools (`async_distillation/
#: async_rollout_worker.py:688`) and decodes the reply as text (`:549-551`).
DISTILL_NO_TOOLS = ("AsyncDistillation runs no tools: each rollout is one student reply, so there are no tool calls, "
                    "results or tool files")
DISTILL_TEXT = ("AsyncDistillation decodes each student reply as plain text (async_rollout_worker.py:549-551): no "
                "reasoning apart from the content")


@dataclass
class _Drained:
    """One sample as the queue reader judged it."""

    sample: Any
    key: str
    drained_at: float
    queue_size: int | None
    version: int | None = None
    #: The live sample (rollout) it came from, carried in its `metrics` by the rollout process.
    attempt_key: str | None = None
    #: Its key's parts, (model version, group or prompt, index): the per-sample loss rows rebuild the key from them.
    place: tuple[int, int, int] | None = None


class _QueueTap:
    """The rollout queue as the reader uses it: `get` notes each item it hands out; everything else passes through."""

    def __init__(self, queue: Any, on_item: Any) -> None:
        self._queue = queue
        self._on_item = on_item

    def get(self, *args: Any, **kwargs: Any) -> Any:
        item = self._queue.get(*args, **kwargs)
        self._on_item(item)
        return item

    def __getattr__(self, name: str) -> Any:
        return getattr(self._queue, name)


class AsyncQueueRecorder(Recorder):
    """The queue reader's drains and drops (as they happen), which micro-batch each kept sample went into (the
    collator), and the optimizer step that trained it (the n-th `training_step` trains the n-th collated batch;
    the dataloader collates one ahead, so a drain's own time says nothing about its step)."""

    names = ("AsyncGRPOTrainer", "AsyncDistillationTrainer")

    def __init__(self, tracker: Any) -> None:
        super().__init__(tracker)
        self._dataset: Any = None
        self._pending: _Drained | None = None
        #: id(sample.input_ids) -> the drained sample: the yielded dict carries that same array to the collator.
        self._kept: dict[int, _Drained] = {}
        self._batches: deque[list[_Drained]] = deque()
        #: The last collated batch's samples' key parts, in collation order (None: not kept), until taken.
        self._places: list[tuple[int, int, int] | None] = []
        self._is_collator_watched = False
        self._indexes: Counter = Counter()
        #: weight version -> the optimizer step after which it went live.
        self._version_steps: dict[int, int] = {}
        self._last_version: int | None = None

    def get_unsupported(self) -> dict[CaptureField, str]:
        """AsyncGRPO: call ids are Probe's (the rollout process awaits each call in order,
        `async_rollout_worker.py:1209-1246`); tools run in TRL's rollout process, not where the sample is written.
        Reasoning is never declared: the rollout process always adds a response schema and parses each reply
        (`async_rollout_worker.py:458-463,1183`), whatever the trainer's tokenizer holds. AsyncDistillation runs no
        tools and keeps plain text."""
        if any(cls.__name__ == "AsyncDistillationTrainer" for cls in type(self.trainer).__mro__):
            return {**dict.fromkeys(TOOL_FIELDS, DISTILL_NO_TOOLS), CaptureField.REASONING: DISTILL_TEXT}
        return {CaptureField.TOOL_CALL_IDS: ASYNC_NUMBERED_IDS, CaptureField.ENVIRONMENT_FILES: ASYNC_FILES}

    def install(self) -> None:
        trainer = self.trainer
        get_loader = trainer.get_train_dataloader
        limit = getattr(trainer.args, "max_staleness", None)
        if isinstance(limit, int):
            self.tracker.max_staleness = limit

        @functools.wraps(get_loader)
        def call_get_train_dataloader(*args: Any, **kwargs: Any) -> Any:
            loader = get_loader(*args, **kwargs)
            self.tracker.guard.call("the rollout queue", self._watch_reader, loader)
            return loader

        self.tracker.install(trainer, "get_train_dataloader", call_get_train_dataloader)
        worker = getattr(trainer, "rollout_worker", None)
        start = getattr(worker, "start", None)
        if callable(start) and hasattr(worker, "_loop_cls"):  # AsyncGRPO's worker, on the main process only

            @functools.wraps(start)
            def call_start(*args: Any, **kwargs: Any) -> Any:
                self.tracker.guard.call("the rollout process", self._wrap_rollout_loop, worker)
                return start(*args, **kwargs)

            self.tracker.install(worker, "start", call_start)

    def handle_train_begin(self, step: int) -> None:
        """TRL's first weight sync ran in its own `on_train_begin` (`async_grpo_trainer.py:149-166`)."""
        self._record_version(step)

    def handle_step_end(self, step: int) -> None:
        """TRL syncs weights every `weight_sync_steps` in its own `on_step_end`, before this one: a new
        `model_version` is a weight version that went live after this step."""
        self._record_version(step)

    def handle_save(self, step: int, checkpoint: dict) -> None:
        version = self._last_version
        if version is not None and self._version_steps.get(version) == step:
            self.tracker.samples.weights(version, after_step=step, checkpoint=checkpoint)

    def handle_micro_batch(self, inputs: Any) -> None:
        """The next collated micro-batch is the one this `training_step` trains: its samples are consumed by the
        step being built."""
        if not self._batches or not self.tracker.is_recording():
            return
        batch = self._batches.popleft()
        step = self.tracker.get_step() + 1
        parts = [{"key": drained.key, "role": "trainer", "consumed_step": step, "consumed_until_step": step,
                  "consumed_version": drained.version} for drained in batch if drained.version is not None]
        self.tracker.send(parts, step)

    def _wrap_rollout_loop(self, worker: Any) -> None:
        """As TRL spawns its rollout process (`_TrainBeginCallback`, `async_grpo_trainer.py:166`), after the run
        opened: the loop it builds there records each rollout (`rollout_loop.py`). Only if it pickles: a spawn that
        cannot pickle it would stop training."""
        if not self.tracker.is_recording():
            return
        rows = self.tracker.rows
        loop = ProbeRolloutLoop(worker._loop_cls, run_id=str(self.tracker.run.id),
                                rows=rows if _is_picklable(rows) else RowReader(), reward_max=self.tracker.live.reward_max)
        pickle.dumps(loop)
        self.tracker.install(worker, "_loop_cls", loop)

    # -- the queue reader ----------------------------------------------------------------------------------------
    def _watch_reader(self, loader: Any) -> None:
        if not self.tracker.is_main:
            return  # other ranks read an empty dataset (`get_train_dataloader`, `:1396`)
        dataset = getattr(self.trainer, "_rollout_dataset", None) or _find_reader(getattr(loader, "dataset", None))
        if dataset is None:
            raise ValueError("no RolloutQueueDataset behind the train dataloader")
        self._dataset = dataset
        guard = self.tracker.guard
        read_version = dataset.model_version_fn

        def call_model_version() -> Any:
            version = read_version()
            guard.call("a queue read", self._check_staleness, version)
            return version

        self.tracker.install(dataset, "queue", _QueueTap(dataset.queue, lambda item: guard.call("a queue read", self._record_item, item)))
        self.tracker.install(dataset, "model_version_fn", call_model_version)
        collator = getattr(loader, "collate_fn", None)
        torch_call = getattr(collator, "torch_call", None)
        if callable(torch_call):

            @functools.wraps(torch_call)
            def call_torch_call(examples: Any, *args: Any, **kwargs: Any) -> Any:
                guard.call("a micro-batch", self._record_batch, examples)
                return torch_call(examples, *args, **kwargs)

            self.tracker.install(collator, "torch_call", call_torch_call)
            self._is_collator_watched = True

    def _record_item(self, item: Any) -> None:
        attempt_key = take_rollout_key(item)  # out of `metrics` before TRL's reader reads it, recording or not
        if not self.tracker.is_recording():
            return
        if isinstance(item, int):
            self.tracker.add_drops(self.tracker.get_step() + 1, WHOLE_GROUP_DROP)
            return
        try:
            size = int(self._dataset.queue.qsize())
        except Exception:  # noqa: BLE001 -- a queue that cannot count (macOS multiprocessing) still delivers
            size = None
        version = int(getattr(item, "model_version", 0))
        owner = getattr(item, "group_id", getattr(item, "prompt_id", 0))
        index = self._indexes[(version, owner)]
        self._indexes[(version, owner)] += 1
        place = (version, owner, index) if isinstance(owner, int) else None
        self._pending = _Drained(item, f"{version}:{owner}:{index}", time.time(), size, attempt_key=attempt_key,
                                 place=place)  # fmt: skip

    def _check_staleness(self, version: Any) -> None:
        """The reader's own rule (`:306-310`): staleness = its version - the sample's; past `max_staleness` it
        is dropped, else kept and yielded."""
        drained, self._pending = self._pending, None
        if drained is None or not isinstance(version, int):
            return
        drained.version = version
        staleness = version - int(getattr(drained.sample, "model_version", version))
        step = self.tracker.get_step() + 1
        part = self._map_sample(drained)
        if staleness > int(getattr(self._dataset, "max_staleness", staleness)):
            drop = {"key": drained.key, "role": "trainer", "drop_reason": "stale", "consumed_version": version}
            self.tracker.send([part, drop], step)
            return
        if self._is_collator_watched:
            self._kept[id(drained.sample.input_ids)] = drained
            if len(self._kept) > MAX_WAITING:
                self._kept.pop(next(iter(self._kept)))
        self.tracker.send([part], step)

    def _record_batch(self, examples: Any) -> None:
        found = [self._kept.pop(id(example["input_ids"]), None) for example in _flatten(examples)]
        self._batches.append([drained for drained in found if drained is not None])
        self._places = [drained.place if drained is not None else None for drained in found]

    def take_batch_places(self) -> list[tuple[int, int, int] | None]:
        """The batch just collated: each sample's key parts, in collation order (every rank's row in turn, each row's
        samples in order), once."""
        places, self._places = self._places, []
        return places

    def _record_version(self, step: int) -> None:
        version = getattr(self.trainer, "model_version", None)
        if not isinstance(version, int) or version == self._last_version or not self.tracker.is_recording():
            return
        self._last_version = version
        self._version_steps[version] = step
        self.tracker.samples.weights(version, after_step=step)

    # -- one sample ----------------------------------------------------------------------------------------------
    def _map_sample(self, drained: _Drained) -> dict:
        sample = drained.sample
        version = int(getattr(sample, "model_version", 0))
        row_index, row = self._get_row(sample)
        task = self.tracker.rows.read_task(row, sample.prompt)
        part: dict[str, Any] = {
            "key": drained.key,
            **task,
            "prompt": render_prompt(sample.prompt),
            **build_completion(sample.completion),
            "split": "train",
            "generated_by": [{"model": {"kind": "policy", "version": version}}],
            "host": self.tracker.host,
        }
        went_live = self._version_steps.get(version)
        if went_live is not None:
            part["scheduled_step"] = went_live + 1
        if hasattr(sample, "group_id"):
            part["group_key"] = f"{version}:{sample.group_id}"
        if drained.attempt_key is not None:
            part["attempt_key"] = drained.attempt_key
        mask = to_ints(getattr(sample, "completion_mask", None))
        if mask:
            part["response_tokens"] = sum(mask)
            part["prompt_tokens"] = len(mask) - sum(mask)
        metrics = self._map_scores(sample, part)
        if drained.queue_size is not None:
            metrics["queue_size"] = float(drained.queue_size)
        if getattr(sample, "enqueued_at", None) is not None:
            metrics["time_in_queue_s"] = max(0.0, drained.drained_at - float(sample.enqueued_at))
        if metrics:
            part["metrics"] = metrics
        if row_index is not None:
            part["extras"] = {**(part.get("extras") or {}), "dataset_row": row_index}
        part["token_arrays"] = self._get_token_arrays(sample, mask)
        return part

    def _map_scores(self, sample: Any, part: dict) -> dict[str, float]:
        """GRPO: the kept reward, each reward function's, the advantage. Distillation: the teacher that scored it."""
        numbers = {str(name): number for name, number in
                   ((name, to_finite(value)) for name, value in (getattr(sample, "metrics", None) or {}).items())
                   if number is not None}
        teacher = getattr(sample, "teacher_id", None)
        if teacher is not None:
            scorer = self.tracker.make_teacher_scorer()
            if scorer.get("model") is None:
                scorer.update(name=str(teacher)[:256], model={"kind": "external", "name": str(teacher)[:512]})
            part["scored_by"] = [scorer]
            return numbers
        reward = numbers.pop(REWARD_KEY, None)
        start, end = REWARD_PART
        parts = {name[len(start):-len(end)]: numbers.pop(name) for name in list(numbers)
                 if name.startswith(start) and name.endswith(end)}
        if reward is not None:
            part["reward"] = reward
        else:
            part["error_reason"], part["error_message"] = "reward_fn", UNSCORED
        if parts:
            part["reward_parts"] = parts
        advantage = to_finite(getattr(sample, "advantage", None))
        if advantage is not None:
            part["normalized_reward"] = advantage
        part["scored_by"] = [{"name": str(name)[:256], "kind": "verifier"}
                             for name in getattr(self.trainer, "reward_func_names", None) or parts]
        return numbers

    def _get_row(self, sample: Any) -> tuple[int | None, Any]:
        """The dataset row behind a sample. GRPO counts groups from the worker's start index, one per prompt
        (`_repeat_iterator`, `async_rollout_worker.py:1116-1140`); distillation names it (`prompt_id`)."""
        dataset = getattr(self.trainer, "train_dataset", None)
        try:
            size = len(dataset)
        except TypeError:
            return None, None
        if size <= 0:
            return None, None
        if hasattr(sample, "group_id"):
            worker = getattr(self.trainer, "rollout_worker", None)
            start = int((getattr(worker, "_loop_kwargs", None) or {}).get("dataset_start_index", 0) or 0)
            index = (start + int(sample.group_id)) % size
        else:
            index = int(getattr(sample, "prompt_id", 0)) % size
        try:
            return index, dataset[index]
        except Exception:  # noqa: BLE001 -- a dataset that cannot be indexed keys tasks by prompt
            return index, None

    def _get_token_arrays(self, sample: Any, mask: list[int]) -> dict:
        """The whole training row (prompt, completion, tool results): ids and text, the sampler's logprobs, the loss
        mask, and the top-k at each position (padding left out): distillation's teacher's, else the GRPO sampler's
        most likely tokens (`sampler_ids`, `num_sampler_logprobs` per position, `async_rollout_worker.py:306-307`)."""
        ids = to_ints(sample.input_ids)
        arrays: dict[str, Any] = {"token_ids": ids, "loss_mask": mask}
        text = self.tracker.decode_tokens(ids)
        if text is not None:
            arrays["token_text"] = text
        if getattr(sample, "old_log_probs", None) is not None:
            arrays["inference_logprobs"] = to_numbers(sample.old_log_probs)
        for ids_name, logprobs_name in (("teacher_topk_ids", "teacher_topk_logprobs"),
                                        ("sampler_ids", "sampler_log_probs")):
            top_ids, top_logprobs = getattr(sample, ids_name, None), getattr(sample, logprobs_name, None)
            if top_ids is not None and top_logprobs is not None:
                arrays["top_k_ids"], arrays["top_k_logprobs"] = _read_top_k(top_ids, top_logprobs)
                break
        return arrays


def _read_top_k(top_ids: Any, top_logprobs: Any) -> tuple[list[list[int]], list[list[float]]]:
    """Per-position top-k ids and logprobs from two (positions, k) arrays padded with -1 / -inf: padding left out."""
    ids_rows, logprobs_rows = [], []
    for ids_row, logprobs_row in zip(top_ids.tolist(), top_logprobs.tolist()):
        kept = [(int(i), float(p)) for i, p in zip(ids_row, logprobs_row) if i >= 0 and to_finite(p) is not None]
        ids_rows.append([i for i, _ in kept])
        logprobs_rows.append([p for _, p in kept])
    return ids_rows, logprobs_rows


def _is_picklable(value: Any) -> bool:
    """A scenario callable that is a lambda cannot reach the rollout process: it then reads the `scenario` column."""
    try:
        pickle.dumps(value)
    except Exception:  # noqa: BLE001 -- anything pickle refuses
        return False
    return True


def _find_reader(dataset: Any) -> Any:
    """The queue reader under a batcher (`FixedCountBatcher.dataset`, `TokenBudgetBatcher.dataset`)."""
    for _ in range(3):
        if dataset is None:
            return None
        if hasattr(dataset, "queue") and hasattr(dataset, "model_version_fn"):
            return dataset
        dataset = getattr(dataset, "dataset", None)
    return None


def _flatten(examples: Any) -> list[Mapping[str, Any]]:
    """The yielded sample dicts in one collator call: GRPO's rows hold them in `.samples` (`:385-404`),
    distillation's groups are lists of them."""
    found: list[Mapping[str, Any]] = []
    stack = [examples]
    while stack:
        item = stack.pop()
        if isinstance(item, Mapping) and "input_ids" in item:
            found.append(item)
        elif hasattr(item, "samples"):
            stack.extend(reversed(list(item.samples)))
        elif isinstance(item, (list, tuple)):
            stack.extend(reversed(item))
    return found
