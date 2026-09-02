import pytest

from agentic_devtools.ai_providers import copilot as copilot_module


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ({"code": "x"}, True),
        ({}, False),
        (["x"], True),
        ([], False),
        (0, True),
    ],
)
def test_has_non_empty_error_field_classifies_non_string_shapes(value: object, expected: bool) -> None:
    assert copilot_module._has_non_empty_error_field(value) is expected
