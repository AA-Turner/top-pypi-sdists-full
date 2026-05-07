def _can_use_otel_trace() -> bool:
    try:
        from opentelemetry import context  # pyright: ignore[reportUnusedImport]
        from opentelemetry import trace  # pyright: ignore[reportUnusedImport]
        from opentelemetry.sdk.resources import Resource  # pyright: ignore[reportUnusedImport]
        from opentelemetry.sdk.trace import TracerProvider  # pyright: ignore[reportUnusedImport]

        return True
    except Exception:
        return False


can_use_otel_trace = _can_use_otel_trace()
