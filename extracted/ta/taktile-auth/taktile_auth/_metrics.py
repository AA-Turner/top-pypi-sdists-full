import typing as t

_emit: t.Optional[t.Callable[[str, float, t.Dict[str, str]], None]] = None

try:
    from aws_lambda_powertools.metrics import MetricUnit, single_metric

    def _powertools_emit(
        name: str,
        duration_ms: float,
        dimensions: t.Dict[str, str],
    ) -> None:
        with single_metric(
            name=name,
            unit=MetricUnit.Milliseconds,
            value=duration_ms,
            namespace="TaktileAuth",
        ) as metric:
            for k, v in dimensions.items():
                metric.add_dimension(name=k, value=v)

    _emit = _powertools_emit
except ImportError:  # pragma: no cover
    pass


def emit_metric(
    name: str,
    duration_ms: float,
    dimensions: t.Dict[str, str],
) -> None:
    if _emit is not None:
        _emit(name, duration_ms, dimensions)
