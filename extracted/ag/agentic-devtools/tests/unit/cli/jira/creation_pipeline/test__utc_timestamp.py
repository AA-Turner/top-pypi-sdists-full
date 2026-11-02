from __future__ import annotations

from datetime import datetime

from agentic_devtools.cli.jira.creation_pipeline import _utc_timestamp


def test_utc_timestamp_is_millisecond_precision_and_utc() -> None:
    value = _utc_timestamp()
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))

    assert value.endswith("Z")
    assert parsed.tzinfo is not None
    assert parsed.microsecond % 1000 == 0
