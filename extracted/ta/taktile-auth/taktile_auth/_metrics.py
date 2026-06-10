import typing as t

_emit: t.Optional[t.Callable[[str, float, t.Dict[str, str], str], None]] = None

try:
    from aws_lambda_powertools.metrics import MetricUnit, single_metric

    def _powertools_emit(
        name: str,
        value: float,
        dimensions: t.Dict[str, str],
        unit: str,
    ) -> None:
        with single_metric(
            name=name,
            unit=MetricUnit(unit),
            value=value,
            namespace="TaktileAuth",
        ) as metric:
            for k, v in dimensions.items():
                metric.add_dimension(name=k, value=v)

    _emit = _powertools_emit
except ImportError:  # pragma: no cover
    pass


def emit_metric(
    name: str,
    value: float,
    dimensions: t.Dict[str, str],
    unit: str = "Milliseconds",
) -> None:
    """Emit a CloudWatch metric via aws-lambda-powertools.

    ``unit`` must be one of the CloudWatch metric unit strings
    (``"Count"``, ``"Milliseconds"``, ``"Seconds"``, ``"Bytes"``, ...).
    No-op when aws-lambda-powertools isn't importable.
    """
    if _emit is not None:
        _emit(name, value, dimensions, unit)
