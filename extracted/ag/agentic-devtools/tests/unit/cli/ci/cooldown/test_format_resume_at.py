"""Tests for format_resume_at()."""

from agentic_devtools.cli.ci.cooldown import format_resume_at


class TestFormatResumeAt:
    """format_resume_at() emits a sanitized UTC timestamp."""

    def test_formats_epoch_zero(self) -> None:
        assert format_resume_at(0) == "1970-01-01T00:00:00Z"
