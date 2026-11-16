"""The dataset fields that key and name an RL task, read once for every integration. The name and description are
the setup agent's (instrument-code `rl-frameworks.md`), cleaned as the SDK cleans any label (`sdk/run/samples/wire.py`)
so a bad value never costs a task."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from probe.sdk.run.samples.wire import TASK_LABEL_CLEANERS

#: The dataset fields (a column, `extra_info` or metadata key) the setup agent writes per task.
TASK_ID_FIELD = "task_id"
TASK_NAME_FIELD = "task_name"
TASK_DESCRIPTION_FIELD = "task_description"
#: Each label field the task carries, by the dataset field it is read from.
_SOURCES = {"name": TASK_NAME_FIELD, "description": TASK_DESCRIPTION_FIELD}


def get_task_label(source: Any) -> dict[str, str]:
    """The task's ``name`` and ``description`` from ``source`` (a row, `extra_info` or metadata mapping), only the
    ones present after cleaning: a name is one line of ≤256 chars, a description ≤4,000; anything else is dropped."""
    if not isinstance(source, Mapping):
        return {}
    label = {name: TASK_LABEL_CLEANERS[name](source.get(field)) for name, field in _SOURCES.items()}
    return {name: value for name, value in label.items() if value is not None}
