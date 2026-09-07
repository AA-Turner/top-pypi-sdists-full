from __future__ import annotations

from typing import Mapping

from chalk.metric_utils import validated_metric, validated_metric_tags

CUSTOM_METRIC_PREFIX = "chalk.custom_metrics."


def _statsd_tags(tags: object) -> list[str] | None:
    validated_tags = validated_metric_tags(tags)
    if validated_tags is None:
        return None
    return [f"{key}:{value}" for key, value in validated_tags.items()]


def log_custom_metric(
    name: str,
    value: float | int,
    tags: Mapping[str, str] | None = None,
) -> None:
    from chalk.utils.tracing import safe_set_gauge

    metric_tags = _statsd_tags(tags)
    metric_name, metric_value = validated_metric(name, value)
    safe_set_gauge(f"{CUSTOM_METRIC_PREFIX}{metric_name}", metric_value, tags=metric_tags)
