"""Distillation logger — record (input, tool-augmented-output) pairs for training.

The play: when sage runs with tools (RAG, web search, REPL, multi-agent
pipeline), the *tool-augmented* output is significantly better than what
the raw model would produce. Logging those (raw_user_prompt, final_output)
pairs gives us a training set for distilling the augmented behavior into
the base model — so the smaller fine-tuned model learns to act *as if*
it had the tools.

Each session writes `~/.sage/distill/<session_id>.jsonl` with one event
per response. `compile_into_corpus()` rolls them up into a TrainingExample
JSONL ready for `sage ext finetune`.

This addresses Tier-3 item 11 (distillation) using only local model output
— no cloud required.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path

from sage.training.corpus import TrainingExample

__all__ = ["DistillEvent", "DistillLogger", "compile_into_corpus"]


@dataclass
class DistillEvent:
    user_prompt: str
    final_response: str
    used_tools: list[str] = field(default_factory=list)
    used_rag: bool = False
    pipeline_phases: list[str] = field(default_factory=list)
    project_hash: str = ""
    ts: float = field(default_factory=time.time)


class DistillLogger:
    """Append-only JSONL logger for one session."""

    def __init__(self, session_id: str | None = None, root: Path | None = None):
        self.session_id = session_id or uuid.uuid4().hex[:12]
        self.root = root or (Path.home() / ".sage" / "distill")
        self.root.mkdir(parents=True, exist_ok=True)
        self.path = self.root / f"{self.session_id}.jsonl"

    def log(self, event: DistillEvent) -> None:
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(asdict(event), ensure_ascii=False) + "\n")

    def events(self) -> list[DistillEvent]:
        if not self.path.exists():
            return []
        out: list[DistillEvent] = []
        for line in self.path.read_text("utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
                out.append(DistillEvent(**d))
            except (json.JSONDecodeError, TypeError):
                continue
        return out


def compile_into_corpus(
    distill_root: Path | None = None,
    *,
    output: Path | None = None,
    only_tool_augmented: bool = True,
    min_tool_count: int = 1,
) -> Path:
    """Walk ~/.sage/distill/*.jsonl, emit TrainingExample JSONL.

    Args:
        only_tool_augmented: skip events that didn't use any tools
        min_tool_count: minimum tools used to qualify
        output: target file (default: ~/.sage/distill/compiled.jsonl)
    """
    root = distill_root or (Path.home() / ".sage" / "distill")
    root.mkdir(parents=True, exist_ok=True)
    out = output or (root / "compiled.jsonl")

    seen_ids: set[str] = set()
    n = 0
    with out.open("w", encoding="utf-8") as fh:
        for jsonl in root.glob("*.jsonl"):
            if jsonl == out:
                continue
            for line in jsonl.read_text("utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if only_tool_augmented and len(d.get("used_tools") or []) < min_tool_count:
                    continue
                ex = TrainingExample(
                    instruction=d.get("user_prompt", ""),
                    input="",
                    output=d.get("final_response", ""),
                    tags=["distill", *d.get("used_tools", [])],
                    source={"kind": "distillation", "session": jsonl.stem},
                )
                if ex.id in seen_ids:
                    continue
                seen_ids.add(ex.id)
                fh.write(ex.to_jsonl() + "\n")
                n += 1
    return out
