"""GOLD's dataset row behind each batch row when dataloader workers collate (S1 C3): the main process reads the indices
its sampler hands out, in order, and checks each batch's prompts against those rows before naming their tasks (a
mid-epoch resume re-hands the batches it skips). Line refs are `huggingface/trl@4ae4d34a86f3`."""

from __future__ import annotations

from collections import deque
from collections.abc import Callable, Mapping, Sequence
from typing import Any

from .rows import IMAGE_MARK

#: Handed-out indices kept past what training consumed (prefetched batches, a resume's skipped ones), at most.
MAX_HANDED = 100_000


class IndexedSampler:
    """The trainer's sampler (GOLD's `RepeatSampler`, `gold_trainer.py:1614-1624`), remembering each index it hands
    out. The main process iterates it even with worker processes: torch sends the workers index batches."""

    def __init__(self, sampler: Any) -> None:
        self.sampler = sampler
        try:
            size = len(sampler)
        except TypeError:
            size = MAX_HANDED
        self.handed: deque[int] = deque(maxlen=min(MAX_HANDED, max(1024, 2 * size)))

    def __iter__(self) -> Any:
        for index in self.sampler:
            self.handed.append(int(index))
            yield index

    def __len__(self) -> int:
        return len(self.sampler)

    def set_epoch(self, epoch: int) -> None:
        set_epoch = getattr(self.sampler, "set_epoch", None)
        if callable(set_epoch):
            set_epoch(epoch)

    def __getattr__(self, name: str) -> Any:
        if name == "sampler":  # not set yet (a copy being built): never recurse
            raise AttributeError(name)
        return getattr(self.sampler, name)


class SampledRows:
    """Which dataset indices each training batch holds: the oldest handed-out window whose rows' prompts are in the
    batch's decoded prompts. A window before it went to a batch training never saw (a resume's skipped batches,
    `accelerate/data_loader.py:1406-1412`) and is dropped."""

    def __init__(self, sampler: IndexedSampler, read_row: Callable[[int], Mapping[str, Any] | None]) -> None:
        self.sampler = sampler
        self._read_row = read_row

    def take(self, prompts: Sequence[str]) -> list[int] | None:
        """The dataset indices of the batch whose decoded prompts are ``prompts``, in row order; None when no window
        matches (the batch's indices are dropped all the same)."""
        handed, count = self.sampler.handed, len(prompts)
        if count == 0:
            return None
        listed = list(handed)
        for offset in range(0, len(listed) - count + 1, count):
            window = listed[offset:offset + count]
            if self._is_match(window, prompts):
                for _ in range(offset + count):
                    handed.popleft()
                return window
        for _ in range(min(count, len(handed))):
            handed.popleft()
        return None

    def _is_match(self, window: Sequence[int], prompts: Sequence[str]) -> bool:
        for index, prompt in zip(window, prompts):
            texts = get_prompt_texts(self._read_row(index))
            if not texts or not all(text in prompt for text in texts):
                return False
        return True


def get_prompt_texts(row: Mapping[str, Any] | None) -> list[str]:
    """The text a dataset row's prompt puts into its batch row: its prompt's messages (or a conversation's all but
    the last), each text part on its own (the chat template wraps them)."""
    if not isinstance(row, Mapping):
        return []
    prompt = row.get("prompt")
    if prompt is None and isinstance(row.get("messages"), list):
        prompt = row["messages"][:-1]
    if isinstance(prompt, str):
        return [prompt.strip()] if prompt.strip() else []
    texts: list[str] = []
    for message in prompt if isinstance(prompt, list) else ():
        content = message.get("content") if isinstance(message, Mapping) else None
        parts = content if isinstance(content, list) else [content]
        for part in parts:
            text = part.get("text") if isinstance(part, Mapping) else part
            if isinstance(text, str) and text.strip() and text.strip() != IMAGE_MARK:
                texts.append(text.strip())
    return texts
