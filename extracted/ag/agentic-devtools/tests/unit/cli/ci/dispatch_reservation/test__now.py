import re

from agentic_devtools.cli.ci.dispatch_reservation import _now


def test_returns_utc_timestamp_with_microseconds() -> None:
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z", _now())
