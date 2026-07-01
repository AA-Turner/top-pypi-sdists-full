"""Reusable RL prompt-dataset ETL helpers for hosted training datasets."""

from __future__ import annotations

import typing as t
from dataclasses import dataclass

from dreadnode.training.etl._common import (
    normalize_messages,
    normalize_optional_string,
    normalize_prompt,
)

if t.TYPE_CHECKING:
    from dreadnode.datasets.dataset import Dataset
    from dreadnode.datasets.local import LocalDataset


@dataclass(slots=True)
class RLPromptRow:
    """Normalized prompt row for prompt-dataset-driven RL training."""

    prompt: str | None
    messages: list[dict[str, str]]
    expected_output: str | None
    template_context: dict[str, str | int | None]
    metadata: dict[str, t.Any]
    reward: float | None


def load_prompt_rows_from_dataset(
    dataset: Dataset | LocalDataset,
    *,
    split: str | None = None,
    limit: int | None = None,
) -> list[RLPromptRow]:
    """Load a published dataset into normalized RL prompt rows."""

    table = dataset.load(split=split)
    records = [record for record in table.to_pylist() if isinstance(record, dict)]
    rows = convert_records_to_prompt_rows(records)
    if limit is None:
        return rows
    return rows[:limit]


def convert_records_to_prompt_rows(
    records: list[dict[str, t.Any]],
) -> list[RLPromptRow]:
    """Convert dataset record dictionaries into RL prompt rows."""

    return [_normalize_prompt_row(record) for record in records]


def _normalize_prompt_row(record: dict[str, t.Any]) -> RLPromptRow:
    expected_output = normalize_optional_string(
        record.get("expected_output")
        or record.get("target")
        or record.get("answer")
        or record.get("output")
    )
    template_context = _normalize_template_context(
        record.get("template_context") or record.get("context")
    )
    metadata = {
        key: value
        for key, value in record.items()
        if key
        not in {
            "messages",
            "prompt",
            "input",
            "question",
            "task_prompt",
            "expected_output",
            "target",
            "answer",
            "output",
            "reward",
            "template_context",
            "context",
        }
    }
    return RLPromptRow(
        prompt=normalize_prompt(record),
        messages=normalize_messages(record.get("messages")),
        expected_output=expected_output,
        template_context=template_context,
        metadata=metadata,
        reward=_normalize_reward(record.get("reward")),
    )


def _normalize_template_context(
    value: t.Any,
) -> dict[str, str | int | None]:
    if not isinstance(value, dict):
        return {}
    context: dict[str, str | int | None] = {}
    for key, item in value.items():
        if not isinstance(key, str):
            continue
        if isinstance(item, str | int) or item is None:
            context[key] = item
    return context


def _normalize_reward(value: t.Any) -> float | None:
    if isinstance(value, int | float):
        return float(value)
    return None


__all__ = [
    "RLPromptRow",
    "convert_records_to_prompt_rows",
    "load_prompt_rows_from_dataset",
]
