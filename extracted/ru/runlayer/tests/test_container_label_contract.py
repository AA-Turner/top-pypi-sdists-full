"""Golden cases for CLI/backend container-label normalization parity."""

import json
from pathlib import Path

import pytest

from runlayer_cli.scan.containers import inspect_parse

_FIXTURE = (
    Path(__file__).parent / "fixtures" / "container_label_normalization_cases.json"
)
_CASES = json.loads(_FIXTURE.read_text())


@pytest.mark.parametrize("case", _CASES, ids=lambda case: case["id"])
def test_container_label_normalization_contract(
    case: dict[str, object],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(inspect_parse, "MAX_LABELS", case["max_labels"])

    assert inspect_parse._bounded_labels(case["labels"]) == case["expected"]
