"""SFTTrainer examples (opt-in, `track(trainer, record_sft=True)`, RL plan §6.6): each example once, as an `sft` sample
at the first optimizer step that trains it, `generated_by` whatever `track(sft_generated_by=...)` declares (an RFT
sampling run, a teacher). Read off the collated micro-batch `training_step` receives (`input_ids`, `attention_mask`,
`labels` with -100 off the loss, `sft_trainer.py:163-230`). A packed row (`padding_free`) is one sample."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from typing import Any

from ..recorder import Recorder
from ..rows import IGNORED_LABEL, make_prompt_key, to_ints
from ..runs import parse_model_ref


class SftRecorder(Recorder):
    """Every micro-batch on the main process; an example seen again (a second epoch) is not sent again."""

    names = ("SFTTrainer",)

    def __init__(self, tracker: Any) -> None:
        super().__init__(tracker)
        self._seen: set[str] = set()

    def handle_micro_batch(self, inputs: Any) -> None:
        if not isinstance(inputs, Mapping) or inputs.get("input_ids") is None or not self.tracker.is_recording():
            return
        step = self.tracker.get_step()
        writer = parse_model_ref(self.tracker.sft_generated_by)
        masks, labels = inputs.get("attention_mask"), inputs.get("labels")
        parts: list[dict] = []
        for row in range(len(inputs["input_ids"])):
            ids = to_ints(inputs["input_ids"][row])
            kept = to_ints(masks[row]) if masks is not None else [1] * len(ids)
            marks = to_ints(labels[row]) if labels is not None else ids
            real = [(token, mark) for token, keep, mark in zip(ids, kept, marks) if keep]
            digest = hashlib.sha256(",".join(str(token) for token, _ in real).encode("ascii")).hexdigest()
            if not real or digest in self._seen:
                continue
            self._seen.add(digest)
            first = next((index for index, (_, mark) in enumerate(real) if mark != IGNORED_LABEL), len(real))
            prompt = self.tracker.decode_text([token for token, _ in real[:first]])
            response = [token for token, mark in real[first:] if mark != IGNORED_LABEL]
            key = f"sft:{digest[:32]}"
            part: dict[str, Any] = {
                "key": key,
                "task_key": make_prompt_key(prompt) if prompt else f"sft:{digest[:16]}",
                "scenario": {},
                "response": self.tracker.decode_text(response),
                "split": "sft",
                "scheduled_step": step + 1,
                "prompt_tokens": first,
                "response_tokens": len(response),
                "host": self.tracker.host,
            }
            if prompt:
                part["prompt"] = prompt
            if writer is not None:
                part["generated_by"] = [{"model": writer}]
            parts.append(part)
            parts.append({"key": key, "role": "trainer", "consumed_step": step + 1, "consumed_until_step": step + 1,
                          "consumed_version": step})
        self.tracker.send(parts, step + 1)
