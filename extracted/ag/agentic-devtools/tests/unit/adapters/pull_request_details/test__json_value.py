from dataclasses import dataclass

from agentic_devtools.adapters.pull_request_details import _json_value


@dataclass
class _Value:
    number: int


def test_json_value_serializes_dataclasses() -> None:
    assert _json_value(_Value(number=3)) == {"number": 3}


def test_json_value_leaves_plain_values_unchanged() -> None:
    value = {"number": 3}
    assert _json_value(value) is value
