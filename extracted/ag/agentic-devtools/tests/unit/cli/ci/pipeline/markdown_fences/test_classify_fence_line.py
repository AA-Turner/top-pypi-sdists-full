"""Tests for classify_fence_line."""

import pytest

from agentic_devtools.cli.ci.pipeline.markdown_fences import classify_fence_line


@pytest.mark.parametrize(
    ("line", "marker", "run_length", "can_open", "can_close"),
    [
        ("```", "`", 3, True, True),
        ("~~~", "~", 3, True, True),
        (" ~~~", "~", 3, True, True),
        ("  ``````", "`", 6, True, True),
        ("   ~~~~~", "~", 5, True, True),
        ("  ```python arbitrary info", "`", 3, True, False),
        ("```python`", "`", 3, False, False),
        ("~~~python`", "~", 3, True, False),
        ("~~~ \t", "~", 3, True, True),
        ("``` \t", "`", 3, True, True),
        ("   ``` trailing text", "`", 3, True, False),
        (" ``` ~~~", "`", 3, True, False),
    ],
)
def test_classifies_fence_candidates(
    line: str,
    marker: str,
    run_length: int,
    can_open: bool,
    can_close: bool,
) -> None:
    candidate = classify_fence_line(line, 7)

    assert candidate is not None
    assert candidate.line_number == 7
    assert candidate.marker == marker
    assert candidate.run_length == run_length
    assert candidate.can_open is can_open
    assert candidate.can_close is can_close


@pytest.mark.parametrize(
    "line",
    [
        "",
        "  ``",
        "`~`",
        "``~`",
        "    ```",
        "    ~~~",
        "\t```",
        "  \t~~~",
        "text ```",
    ],
)
def test_returns_none_for_non_candidates(line: str) -> None:
    assert classify_fence_line(line, 1) is None


@pytest.mark.parametrize("line_number", [0, -1])
def test_rejects_nonpositive_line_number(line_number: int) -> None:
    with pytest.raises(ValueError, match="line_number must be positive"):
        classify_fence_line("```", line_number)


def test_classification_is_independent_between_calls() -> None:
    first = classify_fence_line("```", 1)
    second = classify_fence_line("~~~ trailing", 2)

    assert first is not None
    assert first.can_open is True
    assert first.can_close is True
    assert second is not None
    assert second.line_number == 2
    assert second.marker == "~"
    assert second.can_close is False
