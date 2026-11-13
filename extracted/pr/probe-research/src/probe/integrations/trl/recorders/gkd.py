"""GKDTrainer samples (experimental, RL plan §6.6): the one TRL trainer whose batches are written three ways
(`_maybe_generate`, `gkd_trainer.py:411-450`): by the student (`lmbda`, on-policy), by the teacher (`seq_kd`: the
student trains on teacher-written sequences) or by the dataset. Every batch is graded by the teacher's logits. The
main process records the rows it trains on, and each eval batch's rows (the dataset's, at the step the pass runs). A
model-written batch's rows are live samples from `generate_on_policy_outputs` (`:428`, `:442`) until `_maybe_generate`
returns, `ungraded` (the loss grades them). Line refs are `huggingface/trl@4ae4d34a86f3`."""

from __future__ import annotations

import functools
from collections.abc import Mapping, MutableMapping
from typing import Any

from probe.generated.samples import CaptureField

from ..live import LiveBatch
from ..recorder import Recorder
from ..rows import CARRIED_ROWS_KEY, TOOL_FIELDS, read_labeled_rows
from ..runs import parse_model_ref

STUDENT, TEACHER, DATASET = "student", "teacher", "dataset"
#: What GKD cannot give a sample (`plan(unsupported=)`), and why.
UNSUPPORTED = {
    CaptureField.MESSAGES: (
        "GKD trains on DataCollatorForChatML's token ids (experimental/utils.py:289): the dataset's messages are "
        "rendered into tokens before the trainer sees them, and a generated completion stays token ids"),
    **dict.fromkeys(TOOL_FIELDS, (
        "GKD runs no tools or environment: a completion is a plain generation (`generate_on_policy_outputs`, "
        "gkd_trainer.py:364), so there are no tool calls, results or tool files")),
    CaptureField.REASONING: "GKD never parses a completion: it stays token ids, with no reasoning apart from the text",
}


class GkdRecorder(Recorder):
    """`_maybe_generate` (each micro-batch as the step will train it, `get_batch_samples`, `:406-409`) and
    `generate_on_policy_outputs` (which model wrote it)."""

    names = ("GKDTrainer",)

    def __init__(self, tracker: Any) -> None:
        super().__init__(tracker)
        self._writer = DATASET
        #: The `_maybe_generate` call in progress: its step and call ordinal (its rows' keys), and its live rows.
        self._call: tuple[int, int] = (0, 0)
        self._live = LiveBatch()

    def get_unsupported(self) -> dict[str, str]:
        """Every field: GKD keeps token ids and runs no tools."""
        return dict(UNSUPPORTED)

    def install(self) -> None:
        trainer = self.trainer
        maybe_generate = trainer._maybe_generate
        prediction_step = getattr(trainer, "prediction_step", None)  # transformers' eval step
        generate_outputs = trainer.generate_on_policy_outputs  # a staticmethod: an instance value is not bound
        guard = self.tracker.guard

        @functools.wraps(generate_outputs)
        def call_generate_outputs(model: Any, inputs: Any, generation_config: Any, *args: Any, **kwargs: Any) -> Any:
            self._writer = TEACHER if _is_same_model(model, getattr(trainer, "teacher_model", None)) else STUDENT
            self._live = guard.call("a live sample", self._start_live, inputs) or LiveBatch()
            return generate_outputs(model, inputs, generation_config, *args, **kwargs)

        @functools.wraps(maybe_generate)
        def call_maybe_generate(inputs: Any, *args: Any, **kwargs: Any) -> Any:
            self._writer = DATASET
            step = self.tracker.get_step()
            self._call = (step, self.tracker.take_call("train", step))  # taken first: the live rows' keys use it
            self._live = LiveBatch()
            take_carried(inputs)
            try:
                batch = maybe_generate(inputs, *args, **kwargs)
            except BaseException as exc:
                guard.call("a live sample", self._live.end_rest, exc)
                raise
            guard.call("a micro-batch", self._record, batch, step)
            guard.call("a live sample", self._live.end_rest)
            return batch

        @functools.wraps(prediction_step)
        def call_prediction_step(model: Any, inputs: Any, *args: Any, **kwargs: Any) -> Any:
            take_carried(inputs)  # an eval batch a worker collated: TRL never sees the key
            step = self.tracker.get_step()
            call = self.tracker.take_call("eval", step)  # every process: the per-sample rows' keys use it
            guard.call("an eval batch", self._record_eval, inputs, step, call)
            return prediction_step(model, inputs, *args, **kwargs)

        def take_carried(inputs: Any) -> None:
            """A worker-collated batch's rows (`dataloader_num_workers > 0`), out of the batch before TRL reads it."""
            guard.call("a worker's rows", self.tracker.collated.remember_carried, inputs)
            if isinstance(inputs, MutableMapping):
                inputs.pop(CARRIED_ROWS_KEY, None)  # out even when remembering them failed

        self.tracker.install(trainer, "generate_on_policy_outputs", call_generate_outputs)
        self.tracker.install(trainer, "_maybe_generate", call_maybe_generate)
        if callable(prediction_step):
            self.tracker.install(trainer, "prediction_step", call_prediction_step)
        self.tracker.remember_collated_rows(should_carry=True)

    def _start_live(self, inputs: Mapping[str, Any]) -> LiveBatch:
        """A model writes this micro-batch: its rows start, keyed as `_record` keys them, with the dataset row the
        collator kept (or the carried one) as each one's task."""
        if not self.tracker.is_main:
            return LiveBatch()
        step, call = self._call
        prompts = [prompt for prompt, _completion in read_labeled_rows(inputs)]
        starts = []
        for row, (prompt_ids, facts) in enumerate(zip(prompts, self.tracker.collated.get_rows(prompts))):
            task = self.tracker.read_row_task(prompt_ids, facts)
            start = {"key": f"train:{step}:{call}:0:{row}", "task_key": task["task_key"],
                     "scenario": task.get("scenario") or {}, "scheduled_step": step + 1, "host": self.tracker.host}
            if self._writer == STUDENT:
                start["weight_version"] = step
            starts.append(start)
        return self.tracker.start_live(starts)

    def _record(self, batch: Mapping[str, Any], step: int) -> None:
        if not self.tracker.is_recording():
            return
        writer = self._writer
        parts = self.tracker.make_labeled_parts(batch, step, split="train", writer=self._get_writer_ref(writer, step),
                                                extras={"gkd_source": writer}, call=self._call[1])  # fmt: skip
        for part in parts:
            if part.get("role", "generator") == "generator":
                self._live.link(part)
        self.tracker.send(parts, step + 1)
        self._live.end(parts)

    def _record_eval(self, batch: Any, step: int, call: int) -> None:
        if not isinstance(batch, Mapping) or batch.get("input_ids") is None or not self.tracker.is_recording():
            return
        parts = self.tracker.make_labeled_parts(batch, step, split="eval", writer=self._get_writer_ref(DATASET, step),
                                                extras={"gkd_source": DATASET}, call=call)  # fmt: skip
        self.tracker.send(parts, step)

    def _get_writer_ref(self, writer: str, step: int) -> dict | None:
        if writer == STUDENT:
            return {"kind": "policy", "version": step}
        if writer == TEACHER:
            return self.tracker.get_teacher_ref()
        return parse_model_ref(self.tracker.sft_generated_by)  # dataset completions: their declared writer, if any


def _is_same_model(model: Any, other: Any) -> bool:
    """Whether two handles are one model under accelerate / DDP / DeepSpeed wrappers (`.module`)."""
    return other is not None and _unwrap(model) is _unwrap(other)


def _unwrap(model: Any) -> Any:
    for _ in range(4):
        inner = getattr(model, "module", None)
        if inner is None:
            return model
        model = inner
    return model
