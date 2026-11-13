"""GOLDTrainer samples (experimental GOLD, RL plan §6.6 distillation rules). Each micro-step trains one slice of a
buffered generation batch (`_prepare_inputs`, `gold_trainer.py:1692-1726`). With probability `lmbda` a slice was
written by the student (`_fill_buffer`, `:2013-2021`, then `_generate_on_policy_for_slices`, `:2079-2131`); else it is
the dataset's own completion. The teacher writes nothing: `seq_kd` is read at `:1448` and never used. The teacher
grades every slice through its logits in the loss (`compute_loss`, `:3005-3050`). Evaluation forwards the dataset's
completions (`:1693-1707`). The main process records the slices it trains on; a student-written slice's rows are live
samples while it generates (S1 C2), and with dataloader workers each batch row's dataset index comes from the sampler
(S1 C3, `sampler.py`). Line refs are `huggingface/trl@4ae4d34a86f3`."""

from __future__ import annotations

import functools
from collections.abc import Mapping, Sequence
from typing import Any

from probe.foundation.safe_warn import safe_warn as _diagnostics

from probe.generated.samples import CaptureField

from ..live import LiveBatch
from ..recorder import Recorder
from ..rows import TOOL_FIELDS, read_labeled_rows
from ..runs import parse_model_ref
from ..sampler import IndexedSampler, SampledRows

STUDENT, DATASET = "student", "dataset"
#: What GOLD cannot give a sample (`plan(unsupported=)`), and why.
UNSUPPORTED = {
    CaptureField.MESSAGES: (
        "GOLD trains on DataCollatorForChatML's token ids (gold_trainer.py:1358): the dataset's messages are "
        "rendered into tokens before the trainer sees them, and a student completion stays token ids"),
    **dict.fromkeys(TOOL_FIELDS, (
        "GOLD runs no tools or environment (tool support is a TODO, gold_trainer.py:2228): a completion is a plain "
        "generation, so there are no tool calls, results or tool files")),
    CaptureField.REASONING: (
        "GOLD never parses a completion: it decodes plain text (gold_trainer.py:2473), with no reasoning apart from "
        "the content"),
}


class GoldRecorder(Recorder):
    """`_prepare_inputs`: the slice each micro-step trains on, whose writer `_buffered_on_policy` names (the slice is
    found in `_buffered_inputs` by identity: the cross-tokenizer path numbers slices its own way, `:1709-1716`).
    `_fill_buffer` reserves one call ordinal per slice, so a slice's live rows and its samples share keys."""

    names = ("GOLDTrainer",)

    def __init__(self, tracker: Any) -> None:
        super().__init__(tracker)
        #: The buffer's step and its first slice's call ordinal (`_fill_buffer`, `:1714` or `:1670`).
        self._fill: tuple[int, int] | None = None
        self._live = LiveBatch()
        #: Dataloader workers: the sampler's order (None without workers, or when the loader is unordered).
        self._sampled: SampledRows | None = None
        #: The last training batch and the dataset rows it was matched to.
        self._batch_rows: tuple[Any, list] | None = None
        self._warned: set[str] = set()

    def get_unsupported(self) -> dict[str, str]:
        """Every field: GOLD keeps token ids and runs no tools."""
        return dict(UNSUPPORTED)

    def install(self) -> None:
        trainer = self.trainer
        prepare = trainer._prepare_inputs
        fill = getattr(trainer, "_fill_buffer", None)
        generate = getattr(trainer, "_generate_on_policy_for_slices", None)
        guard = self.tracker.guard

        @functools.wraps(prepare)
        def call_prepare(generation_batch: Any, *args: Any, **kwargs: Any) -> Any:
            step = self.tracker.get_step()
            is_training = bool(getattr(getattr(trainer, "model", None), "training", True))
            if is_training and self._sampled is not None:
                guard.call("a batch's dataset rows", self._match_rows, generation_batch)
            inputs = prepare(generation_batch, *args, **kwargs)
            guard.call("a micro-batch", self._record, inputs, step, is_training)
            return inputs

        self.tracker.install(trainer, "_prepare_inputs", call_prepare)
        self.tracker.remember_collated_rows()
        if not callable(fill) or not callable(generate):
            return  # a GOLD without the pinned buffer: samples, no live rows

        @functools.wraps(fill)
        def call_fill(generation_batch: Any, buffer_steps: Any, *args: Any, **kwargs: Any) -> Any:
            guard.call("a generation batch", self._reserve, generation_batch, buffer_steps)
            return fill(generation_batch, buffer_steps, *args, **kwargs)

        @functools.wraps(generate)
        def call_generate(slices: Any, on_policy_indices: Any, *args: Any, **kwargs: Any) -> Any:
            self._live = guard.call("a live sample", self._start_live, slices, on_policy_indices) or LiveBatch()
            try:
                result = generate(slices, on_policy_indices, *args, **kwargs)
            except BaseException as exc:
                guard.call("a live sample", self._live.end_rest, exc)
                raise
            guard.call("a live sample", self._live.end_rest)  # `ungraded`: the loss grades them
            return result

        self.tracker.install(trainer, "_fill_buffer", call_fill)
        self.tracker.install(trainer, "_generate_on_policy_for_slices", call_generate)
        if int(getattr(trainer.args, "dataloader_num_workers", 0) or 0) > 0:
            self._watch_sampler()

    # -- live rows ---------------------------------------------------------------------------------------------
    def _reserve(self, generation_batch: Any, buffer_steps: Any) -> None:
        step = self.tracker.get_step()
        self._fill = (step, self.tracker.take_call("train", step, int(buffer_steps)))
        self._live = LiveBatch()
        rows = self._batch_rows
        if rows is not None and rows[0] is generation_batch:
            self.tracker.collated.remember(rows[1], generation_batch)

    def _start_live(self, slices: Sequence[Mapping[str, Any]], on_policy_indices: Sequence[int]) -> LiveBatch:
        """The student writes these slices now: their rows start, keyed as `_record` keys them (slice i at call
        base + i), each with its dataset row's task (peeked in the order the slices' records will take them)."""
        if not self.tracker.is_main or self._fill is None:
            return LiveBatch()
        step, base = self._fill
        prompts = [[prompt for prompt, _completion in read_labeled_rows(piece)] for piece in slices]
        facts = iter(self.tracker.collated.get_rows([prompt for piece in prompts for prompt in piece]))
        wanted = set(on_policy_indices)
        starts = []
        for index, piece in enumerate(prompts):
            for row, prompt_ids in enumerate(piece):
                task = self.tracker.read_row_task(prompt_ids, next(facts))
                if index in wanted:
                    starts.append({"key": f"train:{step}:{base + index}:0:{row}", "task_key": task["task_key"],
                                   "scenario": task.get("scenario") or {}, "scheduled_step": step + 1,
                                   "weight_version": step, "host": self.tracker.host})
        return self.tracker.start_live(starts)

    # -- the record --------------------------------------------------------------------------------------------
    def _record(self, inputs: Any, step: int, is_training: bool) -> None:
        """The slice's call, on every process (the per-sample rows' keys read it from `last_calls`), then its parts
        on the main process."""
        if not isinstance(inputs, Mapping) or inputs.get("input_ids") is None:
            return
        index = self._find_slice(inputs) if is_training else None
        split = "train" if is_training else "eval"
        call = self._fill[1] + index if index is not None and self._fill and self._fill[0] == step else None
        call = self.tracker.take_call(split, step) if call is None else call
        self.tracker.last_calls[split] = (step, call)
        if not self.tracker.is_recording():
            return
        writer = STUDENT if index is not None and self._is_on_policy(index) else DATASET
        ref = {"kind": "policy", "version": step} if writer == STUDENT else parse_model_ref(self.tracker.sft_generated_by)
        parts = self.tracker.make_labeled_parts(inputs, step, split=split, writer=ref, extras={"gold_source": writer},
                                                call=call)
        for part in parts:
            if part.get("role", "generator") == "generator":
                self._live.link(part)
        self.tracker.send(parts, step + 1 if is_training else step)

    def _find_slice(self, inputs: Mapping[str, Any]) -> int | None:
        buffered = getattr(self.trainer, "_buffered_inputs", None) or []
        return next((index for index, slice_inputs in enumerate(buffered) if slice_inputs is inputs), None)

    def _is_on_policy(self, index: int) -> bool:
        """Did the student write this slice: its flag in `_buffered_on_policy` (`:2013-2021`)."""
        flags = getattr(self.trainer, "_buffered_on_policy", None) or []
        return index < len(flags) and bool(flags[index])

    # -- dataloader workers (S1 C3) ----------------------------------------------------------------------------
    def _watch_sampler(self) -> None:
        """A worker collates each batch, so the collator's rows never reach this process: the sampler's order names
        them instead (`_get_train_sampler`, `:1614`), unless the loader may hand batches out of order."""
        trainer, guard = self.trainer, self.tracker.guard
        get_sampler, get_loader = trainer._get_train_sampler, trainer.get_train_dataloader

        @functools.wraps(get_sampler)
        def call_get_sampler(*args: Any, **kwargs: Any) -> Any:
            sampler = get_sampler(*args, **kwargs)
            return guard.call("the sampler", self._wrap_sampler, sampler) or sampler

        @functools.wraps(get_loader)
        def call_get_loader(*args: Any, **kwargs: Any) -> Any:
            loader = get_loader(*args, **kwargs)
            guard.call("the dataloader", self._check_order, loader)
            return loader

        self.tracker.install(trainer, "_get_train_sampler", call_get_sampler)
        self.tracker.install(trainer, "get_train_dataloader", call_get_loader)

    def _wrap_sampler(self, sampler: Any) -> IndexedSampler:
        indexed = IndexedSampler(sampler)
        self._sampled = SampledRows(indexed, self._read_dataset_row)
        return indexed

    def _check_order(self, loader: Any) -> None:
        """`DataLoader(in_order=False)` (torch >= 2.6) hands batches out as workers finish: sampler order then names
        the wrong rows, so the whole run keys tasks by prompt (plan E7)."""
        loaders = (loader, getattr(loader, "base_dataloader", None))
        if any(getattr(item, "in_order", True) is False for item in loaders if item is not None):
            self._sampled = None
            self._warn_once("unordered", "probe: GOLD's dataloader hands batches out of order (in_order=False), so "
                            "its samples key each task by the prompt's hash; their dataset task_id, scenario and label "
                            "are not recorded.")

    def _match_rows(self, generation_batch: Any) -> None:
        """Each training batch takes its indices off the sampler's order; a batch that fills the buffer hands its
        rows to the collated rows its slices are recorded from (`_reserve`)."""
        self._batch_rows = None
        if not isinstance(generation_batch, Mapping) or self._sampled is None:
            return
        prompts = [self.tracker.decode_text(prompt) for prompt, _completion in read_labeled_rows(generation_batch)]
        indices = self._sampled.take(prompts)
        if indices is None:
            self._warn_once("unmatched", "probe: a GOLD batch did not match the dataset rows its sampler handed out; "
                            "its samples key each task by the prompt's hash.")
            return
        self._batch_rows = (generation_batch, [self._read_dataset_row(index) for index in indices])

    def _read_dataset_row(self, index: int) -> Mapping[str, Any] | None:
        try:
            row = self.trainer.train_dataset[index]
        except Exception:  # noqa: BLE001 -- a dataset that cannot be indexed: no match, the prompt keys the task
            return None
        return row if isinstance(row, Mapping) else None

    def _warn_once(self, name: str, message: str) -> None:
        if name not in self._warned:
            self._warned.add(name)
            _diagnostics.warn(message)
