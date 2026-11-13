"""DistillationTrainer samples (and ServerDistillationTrainer, its subclass; RL plan §6.6). At the pinned TRL the
trainer is on-policy only: the student writes every completion (`_generate`, `distillation_trainer.py:1430-1525`) and
the teacher grades it through the loss, so each sample is `generated_by policy(step)` + `scored_by teacher(...)`.
No completion text is gathered across processes here (only with `log_completions`), so the main process records the
rows it generated. With tools, the messages TRL's tool loop built (`_tool_call_loop`) become the sample's turns. Line
refs are `huggingface/trl@4ae4d34a86f3` `trl/trainer/distillation_trainer.py`."""

from __future__ import annotations

import functools
from collections.abc import Mapping, Sequence
from typing import Any

from probe.generated.samples import CaptureField

from ..live import LiveBatch
from ..recorder import Recorder
from ..rows import TOOL_FIELDS, build_completion, has_response_schema, render_prompt, to_ints

#: What DistillationTrainer cannot give a sample (`plan(unsupported=)`), and why.
NO_TOOLS = ("DistillationTrainer was given no tools, so it never parses a completion (`_generate`, :1442): each stays "
            "token ids, recorded as response text, with no messages, tool calls, reasoning or tool files")
NO_SCHEMA = ("the tokenizer has no response schema TRL knows (`add_response_schema`, :482-486), so DistillationTrainer "
             "decodes each completion as plain text (:1453-1455): no tool calls run, no reasoning apart from the content")
NUMBERED_IDS = ("TRL's parser gives tool calls no id: Probe numbers them probe-<turn>-<i> and links each result in "
                "call order (the tool loop runs each call in turn, :1243-1274), checked by tool name")
SHARED_TOOLS = ("DistillationTrainer calls every completion's tools through one shared table (`_tool_dict`, :478), so "
                "a tool call does not say whose sample it serves: its files cannot reach a sample")
#: The turns a tool-calling completion adds to its sample (`build_completion`).
TURN_FIELDS = ("turns", "turns_source", "turn_count", "tool_call_count", "extras")


class DistillationRecorder(Recorder):
    """`_generate` (the student's unpadded token lists) and `_generate_and_score_completions` (one call per optimizer
    step: TRL generates once per `gradient_accumulation_steps`, `:1835-1844`)."""

    names = ("DistillationTrainer",)

    def __init__(self, tracker: Any) -> None:
        super().__init__(tracker)
        self._generated: tuple | None = None
        #: This call's completions as message lists, from the tool loop (only with tools).
        self._completions: list | None = None
        self._live = LiveBatch()

    def get_unsupported(self) -> dict[str, str]:
        """No tools: TRL keeps token ids only. Tools without a response schema: plain text, so no tool runs. With both:
        call ids are Probe's, and a tool's files cannot reach their sample."""
        trainer = self.trainer
        if not getattr(trainer, "tools", None):
            return dict.fromkeys(CaptureField, NO_TOOLS)
        if not has_response_schema(getattr(trainer, "_tokenizer", None) or self.tracker.get_tokenizer()):
            return {**dict.fromkeys(TOOL_FIELDS, NO_SCHEMA), CaptureField.REASONING: NO_SCHEMA}
        return {CaptureField.TOOL_CALL_IDS: NUMBERED_IDS, CaptureField.ENVIRONMENT_FILES: SHARED_TOOLS}

    def install(self) -> None:
        trainer = self.trainer
        generate = trainer._generate
        score = trainer._generate_and_score_completions
        tool_loop = getattr(trainer, "_tool_call_loop", None)
        guard = self.tracker.guard

        @functools.wraps(generate)
        def call_generate(prompts: Any, *args: Any, **kwargs: Any) -> Any:
            result = generate(prompts, *args, **kwargs)
            self._generated = (result[0], result[1], result[2])  # prompt ids, completion ids, tool mask (`:1525`)
            return result

        @functools.wraps(score)
        def call_score(inputs: Any, *args: Any, **kwargs: Any) -> Any:
            self._generated = self._completions = None
            step = self.tracker.get_step()
            split = "train" if getattr(trainer.model, "training", True) else "eval"
            call = self.tracker.take_call(split, step)
            self._live = guard.call("a live sample", self._start_live, inputs, step, split, call) or LiveBatch()
            try:
                output = score(inputs, *args, **kwargs)
            except BaseException as exc:
                guard.call("a live sample", self._live.end_rest, exc)
                raise
            guard.call("a generation batch", self._record, inputs, step, split, call)
            guard.call("a live sample", self._live.end_rest)
            return output

        self.tracker.install(trainer, "_generate", call_generate)
        self.tracker.install(trainer, "_generate_and_score_completions", call_score)
        if not callable(tool_loop):
            return

        @functools.wraps(tool_loop)
        def call_tool_loop(*args: Any, **kwargs: Any) -> Any:
            result = tool_loop(*args, **kwargs)
            self._completions = result[1]  # each completion's messages: replies, tool results, the replies after
            return result

        self.tracker.install(trainer, "_tool_call_loop", call_tool_loop)

    def _start_live(self, inputs: Sequence[Any], step: int, split: str, call: int) -> LiveBatch:
        """The main process's rows as live samples, keyed as `_record` keys them, before the student generates."""
        if not self.tracker.is_main:
            return LiveBatch()
        seal_step = step + 1 if split == "train" else step
        starts = []
        for row, item in enumerate(inputs):
            prompt = item.get("prompt") if isinstance(item, Mapping) else None
            task = self.tracker.rows.read_task(item, prompt)
            starts.append({"key": f"{split}:{step}:{call}:0:{row}", "task_key": task["task_key"],
                           "scenario": task.get("scenario") or {}, "scheduled_step": seal_step, "weight_version": step,
                           "host": self.tracker.host})
        return self.tracker.start_live(starts)

    def _record(self, inputs: Sequence[Any], step: int, split: str, call: int) -> None:
        if self._generated is None or not self.tracker.is_recording():
            return
        prompt_ids, completion_ids, tool_masks = self._generated
        seal_step = step + 1 if split == "train" else step
        until = self.tracker.get_window_end(step, int(getattr(self.trainer.args, "gradient_accumulation_steps", 1) or 1))
        scorer = self.tracker.make_teacher_scorer()
        stops = set(getattr(self.trainer, "eos_token_ids", None) or ())
        parts: list[dict] = []
        for row, ids in enumerate(completion_ids):
            ids = to_ints(ids)
            item = inputs[row] if row < len(inputs) else {}
            prompt = item.get("prompt") if isinstance(item, Mapping) else None
            key = f"{split}:{step}:{call}:0:{row}"
            part: dict[str, Any] = {
                "key": key,
                **self.tracker.rows.read_task(item, prompt),
                "prompt": render_prompt(prompt),
                "response": self.tracker.decode_text(ids),
                "split": split,
                "scheduled_step": seal_step,
                "generated_by": [{"model": {"kind": "policy", "version": step}}],
                "scored_by": [scorer],
                "prompt_tokens": len(prompt_ids[row]) if row < len(prompt_ids) else None,
                "response_tokens": len(ids),
                "finish_reason": "stop" if ids and ids[-1] in stops else "length",
                "host": self.tracker.host,
            }
            if self._completions is not None and row < len(self._completions):
                built = build_completion(self._completions[row])
                part.update({name: built[name] for name in TURN_FIELDS if name in built})
            arrays: dict[str, Any] = {"token_ids": ids}
            text = self.tracker.decode_tokens(ids)
            if text is not None:
                arrays["token_text"] = text
            part["token_arrays"] = arrays
            self._live.link(part)
            parts.append({name: value for name, value in part.items() if value is not None})
            if split == "train":
                mask = to_ints(tool_masks[row]) if tool_masks is not None and row < len(tool_masks) else [1] * len(ids)
                parts.append({"key": key, "role": "trainer", "consumed_step": step + 1, "consumed_until_step": until,
                              "consumed_version": step, "trainer_token_arrays": {"loss_mask": mask}})
        self.tracker.send(parts, seal_step)
        self._live.end(parts)
