import pytest

from agentic_devtools.cli.ci.pipeline.validation_evidence import _advance_backtick_fence


@pytest.mark.parametrize(
    ("line", "fence_length", "expected"),
    [
        ("ordinary text", 0, (0, False)),
        ("  ````markdown", 0, (4, True)),
        ("```", 4, (4, True)),
        ("````python", 4, (4, True)),
        ("````", 4, (0, True)),
        ("````  \t", 4, (0, True)),
        ("`````", 4, (0, True)),
        ("ordinary text", 4, (4, True)),
    ],
)
def test_advances_fence_only_for_valid_backtick_delimiters(
    line: str, fence_length: int, expected: tuple[int, bool]
) -> None:
    assert _advance_backtick_fence(line, fence_length) == expected
