"""Tests for the Q11 format-example rule."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.checks.customization_quality import check_format_example
from tests.unit.cli.checks.customization_quality._support import make_unit


class TestCheckFormatExample:
    def test_ignores_files_that_prescribe_no_format(self) -> None:
        """A file that never prescribes a format needs no example."""
        assert check_format_example(make_unit(body="Explains the release process.\n")) == []

    @pytest.mark.parametrize("fence", ["```", "~~~"])
    def test_accepts_a_prescribed_format_with_a_fenced_instance(self, fence: str) -> None:
        """Either fence style counts as one concrete instance."""
        unit = make_unit(body=f"Use this output format:\n\n{fence}\nsummary: ok\n{fence}\n")

        assert check_format_example(unit) == []

    @pytest.mark.parametrize("info", ["json", "yaml", "python"])
    def test_accepts_a_fenced_block_with_an_info_string_immediately_after_the_fence(self, info: str) -> None:
        """CommonMark allows the info string to follow the fence marker without whitespace."""
        unit = make_unit(body=f"Use this output format:\n\n```{info}\nsummary: ok\n```\n")

        assert check_format_example(unit) == []

    def test_flags_a_prescribed_format_with_only_an_opening_fence(self) -> None:
        """An unmatched opening fence is not a complete example."""
        unit = make_unit(body="Use this output format:\n\n```\n")

        assert [v.rule for v in check_format_example(unit)] == ["Q11"]

    def test_flags_a_prescribed_format_with_an_empty_fenced_block(self) -> None:
        """A fence pair with no content between them is not a concrete example."""
        unit = make_unit(body="Use this output format:\n\n```\n```\n")

        assert [v.rule for v in check_format_example(unit)] == ["Q11"]

    def test_accepts_a_fenced_block_with_an_empty_interior_line(self) -> None:
        """An empty line inside a fence block does not prevent it from counting."""
        unit = make_unit(body="Use this output format:\n\n```\n\nsummary: ok\n```\n")

        assert check_format_example(unit) == []

    def test_requires_the_closing_fence_to_match_the_opening_length(self) -> None:
        """A shorter closing fence does not terminate a longer opening fence."""
        unit = make_unit(body="Use this output format:\n\n````\nsummary: ok\n```\n")

        assert [v.rule for v in check_format_example(unit)] == ["Q11"]

    def test_ignores_fence_lines_inside_a_four_space_indented_code_block(self) -> None:
        """Indented code content is not a fenced example under CommonMark."""
        unit = make_unit(body="Use this output format:\n\n    ```\n    summary: ok\n    ```\n")

        assert [v.rule for v in check_format_example(unit)] == ["Q11"]

    def test_flags_a_prescribed_format_without_a_fenced_instance(self) -> None:
        """Prescribing a format without showing one is the failure case."""
        violations = check_format_example(make_unit(body="Respond with a summary line and a verdict line.\n"))

        assert [v.rule for v in violations] == ["Q11"]
