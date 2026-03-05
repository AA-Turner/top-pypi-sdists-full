def _can_use_datadog_statsd() -> bool:
    try:
        from datadog.dogstatsd.base import statsd

        _ = statsd
        return True
    except ImportError:
        return False


can_use_datadog_statsd = _can_use_datadog_statsd()
