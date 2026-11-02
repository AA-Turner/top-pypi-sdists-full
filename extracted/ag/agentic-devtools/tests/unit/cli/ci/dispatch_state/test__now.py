from datetime import datetime

from agentic_devtools.cli.ci import dispatch_state as dispatch_state_module


def test_returns_iso8601_utc_timestamp() -> None:
    value = dispatch_state_module._now()

    parsed = datetime.fromisoformat(value)
    assert parsed.tzinfo is not None
    assert value.endswith("+00:00")
