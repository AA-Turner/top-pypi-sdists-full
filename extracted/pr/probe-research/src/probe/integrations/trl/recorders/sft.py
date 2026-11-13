"""SFTTrainer examples (opt-in, `track(trainer, record_sft=True)`, RL plan §6.6): each example once, as an `sft` sample
at the first optimizer step that trains it, `generated_by` whatever `track(sft_generated_by=...)` declares (an RFT
sampling run, a teacher), and each eval example once, as an `eval` sample at the step its first `evaluate()` pass ran
(its own key, `rows.make_sft_key`). Read off the collated micro-batch `training_step` (or `prediction_step`) receives
(`input_ids`, `attention_mask`, `labels` with -100 off the loss, `sft_trainer.py:163-230`). A packed row
(`padding_free`) is one sample, or each of its examples once the per-sample rows split it (`GPU_PROVEN`)."""

from __future__ import annotations

import functools
from collections.abc import Mapping
from typing import Any

from probe.generated.samples import CaptureField

from ..recorder import Recorder
from ..rows import IGNORED_LABEL, TOOL_FIELDS, get_segment_starts, make_prompt_key, make_sft_key, to_ints
from ..runs import parse_model_ref
from ..training.declarations import GPU_PROVEN, PACKED_SFT

#: What an SFT sample cannot hold (`plan(unsupported=)`), and why.
UNSUPPORTED = {
    CaptureField.MESSAGES: (
        "SFT samples are dataset examples, not rollouts: SFTTrainer tokenizes the dataset's messages before training "
        "(`_prepare_dataset`, sft_trainer.py:1270), and Probe reads each example back off the micro-batch's token ids"),
    **dict.fromkeys(TOOL_FIELDS, (
        "SFT samples are dataset examples, not rollouts: nothing runs a tool, and a tool call in the data is only "
        "tokens")),
    CaptureField.REASONING: (
        "SFT samples are dataset examples, not rollouts: any reasoning in the data is only tokens in the text"),
}


class SftRecorder(Recorder):
    """Every micro-batch (and eval batch) on the main process; an example seen again (a second epoch, a second
    `evaluate()`) is not sent again."""

    names = ("SFTTrainer",)

    def __init__(self, tracker: Any) -> None:
        super().__init__(tracker)
        self._seen: set[str] = set()

    def get_unsupported(self) -> dict[str, str]:
        """Every field: an SFT sample is a tokenized dataset example."""
        return dict(UNSUPPORTED)

    def install(self) -> None:
        trainer = self.trainer
        predict = getattr(trainer, "prediction_step", None)
        if not callable(predict):
            return

        @functools.wraps(predict)
        def call_prediction_step(model: Any, inputs: Any, *args: Any, **kwargs: Any) -> Any:
            self.tracker.guard.call("an eval batch", self._record, inputs, is_eval=True)
            return predict(model, inputs, *args, **kwargs)

        self.tracker.install(trainer, "prediction_step", call_prediction_step)

    def handle_micro_batch(self, inputs: Any) -> None:
        self._record(inputs, is_eval=False)

    def _record(self, inputs: Any, *, is_eval: bool) -> None:
        if not isinstance(inputs, Mapping) or inputs.get("input_ids") is None or not self.tracker.is_recording():
            return
        step = self.tracker.get_step()
        writer = parse_model_ref(self.tracker.sft_generated_by)
        parts: list[dict] = []
        for real in _read_examples(inputs):
            key = make_sft_key([token for token, _ in real], is_eval=is_eval)
            if not real or key in self._seen:
                continue
            self._seen.add(key)
            first = next((index for index, (_, mark) in enumerate(real) if mark != IGNORED_LABEL), len(real))
            prompt = self.tracker.decode_text([token for token, _ in real[:first]])
            response = [token for token, mark in real[first:] if mark != IGNORED_LABEL]
            part: dict[str, Any] = {
                "key": key,
                "task_key": make_prompt_key(prompt) if prompt else key[:20],
                "scenario": {},
                "response": self.tracker.decode_text(response),
                "split": "eval" if is_eval else "sft",
                "scheduled_step": step if is_eval else step + 1,
                "prompt_tokens": first,
                "response_tokens": len(response),
                "host": self.tracker.host,
            }
            if prompt:
                part["prompt"] = prompt
            if writer is not None:
                part["generated_by"] = [{"model": writer}]
            parts.append(part)
            if not is_eval:
                parts.append({"key": key, "role": "trainer", "consumed_step": step + 1, "consumed_until_step": step + 1,
                              "consumed_version": step})
        self.tracker.send(parts, step if is_eval else step + 1)


def _read_examples(inputs: Mapping[str, Any]) -> list[list[tuple[int, int]]]:
    """Each example of a collated batch as its unpadded (token, label) pairs: a row each, or (a packed row, once its
    per-sample rows split it) each segment of the one row."""
    ids_rows, masks, labels = inputs["input_ids"], inputs.get("attention_mask"), inputs.get("labels")
    starts = get_segment_starts(inputs) if PACKED_SFT in GPU_PROVEN else None
    found = []
    for row in range(len(ids_rows)):
        ids = to_ints(ids_rows[row])
        kept = to_ints(masks[row]) if masks is not None else [1] * len(ids)
        marks = to_ints(labels[row]) if labels is not None else ids
        real = [(token, mark) for token, keep, mark in zip(ids, kept, marks) if keep]
        if starts is None or row > 0:
            found.append(real)
            continue
        bounds = [*starts, len(real)]
        found += [real[start:end] for start, end in zip(bounds[:-1], bounds[1:], strict=True)
                  if any(mark != IGNORED_LABEL for _, mark in real[start:end])]  # fmt: skip
    return found
