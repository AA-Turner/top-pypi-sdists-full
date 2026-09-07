from __future__ import annotations

import collections.abc

ALLOWED_METRIC_TAGS = frozenset(
    {
        "training_run_id",
        "split",
        "epoch",
        "step",
        "class",
        "threshold",
        "optimizer",
        "model_version",
    }
)


def validated_metric(name: object, value: object) -> tuple[str, float]:
    if not isinstance(name, str) or not name:
        raise ValueError("metric names must be non-empty strings.")
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        raise ValueError("metric values must be ints or floats.")
    return name, float(value)


def validated_metric_tags(tags: object) -> dict[str, str] | None:
    if tags is None:
        return None
    if not isinstance(tags, collections.abc.Mapping):
        raise ValueError("metric tags must be a mapping of strings to strings.")

    validated_tags: dict[str, str] = {}
    for key, value in tags.items():
        if not isinstance(key, str) or not key:
            raise ValueError("metric tag names must be non-empty strings.")
        if key not in ALLOWED_METRIC_TAGS:
            raise ValueError("metric tag names must be one of: " + ", ".join(sorted(ALLOWED_METRIC_TAGS)))
        if not isinstance(value, str):
            raise ValueError("metric tag values must be strings.")
        validated_tags[key] = value
    return validated_tags
