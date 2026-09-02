from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness.credits import CreditProbe


def test_cloudwatch_uses_iso8601_time_bounds(monkeypatch) -> None:
    captured: list[str] = []

    class Result:
        returncode = 0
        stdout = json.dumps(
            {"Datapoints": [{"Timestamp": "2026-08-20T10:00:00Z", "Average": 42.5}]}
        )

    def fake_run(command, **_kwargs):
        captured.extend(command)
        return Result()

    monkeypatch.setattr("harness.credits.subprocess.run", fake_run)
    probe = object.__new__(CreditProbe)
    probe.identity = {"instance_id": "i-proof"}
    probe.region = "us-east-1"

    assert probe._cloudwatch("CPUCreditBalance") == 42.5
    start = captured[captured.index("--start-time") + 1]
    end = captured[captured.index("--end-time") + 1]
    assert datetime.fromisoformat(start).tzinfo is not None
    assert datetime.fromisoformat(end).tzinfo is not None
    assert start != "-30 minutes"
    assert end != "now"
